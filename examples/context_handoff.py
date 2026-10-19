#!/usr/bin/env python3
"""Exercise Continuum through separate CLI processes, without external effects.

Requires a built continuum binary and a new output directory. All operational
states below are synthetic fixture declarations, not observed remote activity.
"""

import argparse
import copy
import json
import subprocess
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    binary = args.binary.resolve(strict=True)
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    database = output / "work.db"

    def write_json(name, value):
        path = output / name
        path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
        return path

    def cli(command, *values, succeeds=True):
        result = subprocess.run(
            [str(binary), command, str(database), *(str(v) for v in values)],
            capture_output=True,
            text=True,
            check=False,
        )
        if succeeds:
            if result.returncode != 0:
                raise RuntimeError(result.stderr)
            return json.loads(result.stdout)
        if result.returncode == 0:
            raise AssertionError(f"{command} unexpectedly succeeded")
        return json.loads(result.stderr)

    def blob(name, content):
        path = output / name
        path.write_bytes(content)
        return cli("blob", path)["id"]

    def json_blob(name, value):
        return cli("blob", write_json(name, value))["id"]

    def snapshot(name, path, blob_id):
        value = {"type": "snapshot", "entries": [{"path": path, "blob": blob_id}]}
        return cli("put", write_json(name, value))["id"]

    cli("init")
    source_blob = blob("fixture-source.txt", b"An unchanged source artifact.\n")
    source_snapshot = snapshot("source-snapshot.json", "source.txt", source_blob)
    request_blob = json_blob(
        "unexecuted-request.json",
        {"operation_id": "operation-17", "action": "build-example-artifact"},
    )
    base = {
        "schema": "continuum.work_state.v1",
        "id": "work-17",
        "source_snapshot": source_snapshot,
        "objective": {
            "id": "objective-17",
            "statement": "Continue the example build workflow from its recorded state.",
            "done_when": "The operation has an inspected result under its own contract.",
            "constraints": ["This is a synthetic local fixture; perform no external action."],
        },
        "attempts": [{
            "id": "attempt-17",
            "operation_id": "operation-17",
            "source_snapshot": source_snapshot,
            "summary": "The build request and its declared operational state are retained.",
            "dispatch_state": "never_dispatched",
            "request": request_blob,
            "receipt": None,
            "outcome_note": "There is no retained execution receipt for this request.",
        }],
        "decisions": [{
            "id": "decision-17",
            "state": "active",
            "statement": "Continue using the recorded operation identity and its scoped evidence.",
            "basis_attempt_ids": ["attempt-17"],
            "reopen_when": "A new operational observation changes the declared state.",
        }, {
            "id": "historical-17",
            "state": "historical",
            "statement": "An earlier design alternative remains available for inspection.",
            "basis_attempt_ids": [],
            "reopen_when": "A relevant requirement changes.",
        }],
        "uncertainties": [{
            "id": "uncertainty-17",
            "question": "What can the actual execution service verify?",
            "why_it_matters": "Authored fixture state is not a dispatch log or action authority.",
        }],
        "handoff": {
            "id": "handoff-17",
            "from_worker": "producer",
            "to_worker": "recipient",
            "scope": "Inspect context and record the references received.",
            "required_decision_ids": ["decision-17"],
        },
    }

    cases = []
    for label, dispatch_state in [("a", "never_dispatched"), ("b", "may_have_been_sent")]:
        state = copy.deepcopy(base)
        state["attempts"][0]["dispatch_state"] = dispatch_state
        state_id = json_blob(f"{label}-work-state.json", state)
        wrapper = snapshot(f"{label}-state-snapshot.json", "work-state.json", state_id)
        initial = cli("accept", write_json(f"{label}-accept.json", {
            "acceptor": "example", "target": label, "operation_id": f"create-{label}",
            "expected": None, "candidate": wrapper,
        }))
        head = initial["receipt"]["resulting"]
        request = {
            "schema": "continuum.prepare_context.v1",
            "work_state": state_id,
            "max_bytes": 32768,
            "anchor": {
                "acceptor": "example", "target": label, "expected": head,
                "work_state_path": "work-state.json",
            },
        }
        prepared = cli("prepare-context", write_json(f"{label}-prepare.json", request))
        pack_id = prepared["context_pack"]
        write_json(f"{label}-prepared.json", prepared)
        # This is a new OS process: no producer memory is reused.
        inspected = cli("inspect-context", pack_id)
        (output / f"{label}-context.jsonl").write_text(inspected["rendered"], encoding="utf-8")
        manifest = inspected["manifest"]
        ack = {
            "schema": "continuum.context_acknowledgement.v1",
            "id": f"ack-{label}", "context_pack": pack_id,
            "handoff_id": manifest["handoff_id"], "recipient_worker": "recipient",
            "included_ids": [item["id"] for item in manifest["included"]],
            "omitted_ids": [item["id"] for item in manifest["omitted"]],
            "note": "The example recipient declares these exact context references; no execution is claimed.",
        }
        acknowledged = cli("acknowledge-handoff", write_json(f"{label}-ack.json", ack))
        verified = cli("verify-handoff", acknowledged["acknowledgement"])
        assert verified["reference_consistency_verified"] is True
        assert verified["external_effect_verified"] is False
        assert cli("verify-current-context", pack_id)["freshness"]["status"] == "matches_at_observation"
        lines = [json.loads(line) for line in inspected["rendered"].splitlines()]
        attempt_line = next(line for line in lines if line["kind"] == "attempt")
        cases.append({
            "case": label, "source_snapshot": source_snapshot, "work_state": state_id,
            "context_pack": pack_id, "dispatch_state": dispatch_state,
            "conditional_next_action": attempt_line["conditional_next_action"],
            "rendered_bytes": manifest["rendered_bytes"], "acknowledgement": verified,
        })

    assert cases[0]["source_snapshot"] == cases[1]["source_snapshot"]
    assert cases[0]["conditional_next_action"] != cases[1]["conditional_next_action"]
    assert cases[0]["work_state"] != cases[1]["work_state"]
    # Move the accepted state to a genuinely new work-state object.
    changed = copy.deepcopy(base)
    changed["objective"]["constraints"].append("The current fixture now has an additional scope condition.")
    new_state = json_blob("updated-work-state.json", changed)
    new_wrapper = snapshot("updated-state-snapshot.json", "work-state.json", new_state)
    current_head = cli("head", "example", "a")
    cli("accept", write_json("advance-state.json", {
        "acceptor": "example", "target": "a", "operation_id": "advance-a",
        "expected": current_head, "candidate": new_wrapper,
    }))
    historical = cli("verify-context", cases[0]["context_pack"])
    assert historical["exact_projection_verified"] is True
    assert historical["freshness"]["status"] == "stale_at_observation"
    current_rejection = cli("verify-current-context", cases[0]["context_pack"], succeeds=False)
    summary = {
        "kind": "local_context_handoff_example", "cases": cases,
        "historical_verification_after_head_movement": historical,
        "current_verification_rejection": current_rejection,
        "limits": [
            "Synthetic operational declarations; no external request was sent.",
            "Separate CLI processes demonstrate custody/recovery, not model performance.",
            "Acknowledgements verify references, not identity, understanding, or effect truth.",
            "This is a correctness example, not a performance benchmark.",
        ],
    }
    write_json("result.json", summary)
    print(json.dumps({"result": str(output / "result.json"), "same_source_distinguished": True,
                      "old_pack_intact_but_stale": True}, indent=2))


if __name__ == "__main__":
    main()
