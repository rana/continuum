#!/usr/bin/env python3
"""Prepare one *real* Continuum development checkpoint through CLI subprocesses.

The source allowlist is deliberately small and public. A checkpoint is an
offered handoff, not an observed recipient execution, and the resulting SQLite
store is disposable pending an upgrade/backup contract.
"""

import argparse
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

SOURCE_PATHS = (
    "AGENTS.md",
    "CURRENT.md",
    "docs/experiments/real-use-pilot.md",
    "docs/architecture/context-handoff-v1.md",
)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def json_bytes(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def git_observation(root):
    def call(*args):
        try:
            return subprocess.run(
                ["git", "-C", str(root), *args],
                check=True, capture_output=True, text=True
            ).stdout.strip()
        except (OSError, subprocess.CalledProcessError):
            return None

    head = call("rev-parse", "HEAD")
    status = call("status", "--porcelain", "--untracked-files=no")
    return {
        "head": head,
        "tracked_tree_dirty": status != "" if status is not None else None,
        "note": "An observed Git HEAD does not by itself identify modified source bytes.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", type=Path, required=True)
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    binary = args.binary.resolve(strict=True)
    project = args.project.resolve(strict=True)
    output = args.output.resolve()
    if not project.is_dir() or not binary.is_file():
        raise ValueError("expected a source directory and an executable file")
    if output.is_relative_to(project):
        raise ValueError("the trial output must be outside the source tree")
    # No implicit reuse, deletion, or overwrite of a retained project database.
    output.mkdir(parents=True, exist_ok=False)
    database = output / "work.db"

    def write(name, data):
        path = output / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path

    def write_json(name, value):
        return write(name, json_bytes(value))

    subprocess_count = 0

    def cli(command, *values):
        nonlocal subprocess_count
        completed = subprocess.run(
            [str(binary), command, str(database), *(str(v) for v in values)],
            check=False, capture_output=True, text=True,
        )
        subprocess_count += 1
        if completed.returncode:
            raise RuntimeError(
                f"continuum {command} exited {completed.returncode}: "
                + completed.stderr[:2048]
            )
        return json.loads(completed.stdout)

    cli("init")
    inputs = []
    entries = []
    for relative in SOURCE_PATHS:
        source = project / relative
        if source.is_symlink() or not source.is_file():
            raise ValueError(f"missing regular public project file: {relative}")
        data = source.read_bytes()
        if len(data) > 256 * 1024:
            raise ValueError(f"input exceeds the pilot's 256 KiB/file bound: {relative}")
        staged = write("source/" + relative, data)
        object_id = cli("blob", staged)["id"]
        inputs.append({
            "path": relative,
            "bytes": len(data),
            "sha256": sha256(data),
            "blob": object_id,
        })
        entries.append({"path": relative, "blob": object_id})

    source_snapshot = cli("put", write_json(
        "source-snapshot.json", {"type": "snapshot", "entries": entries}
    ))["id"]

    # These are authored observations and direction, not a remotely verified
    # execution history. In particular, no dispatch state is invented.
    work_state = {
        "schema": "continuum.work_state.v1",
        "id": "pilot.self-use.checkpoint.v1",
        "source_snapshot": source_snapshot,
        "objective": {
            "id": "objective.self-use",
            "statement": "Review a real Continuum development checkpoint and select the next evidence-generating engineering action.",
            "done_when": "A fresh recipient identifies a bounded next action, required evidence, and any decisive information absent from the supplied context.",
            "constraints": [
                "Use only the actual supplied context and explicitly identify gaps.",
                "Do not confuse an offered handoff, a source reference, or a CI result with verified recipient execution.",
                "Keep other projects' private sources and operating records out of public trial artifacts.",
            ],
        },
        "attempts": [],
        "decisions": [{
            "id": "decision.first-consumer",
            "state": "active",
            "statement": "Exercise Continuum on its own development before using a small independent public CLI example.",
            "basis_attempt_ids": [],
            "reopen_when": "Observed handoff friction or a clearer independent test suggests a different sequence.",
        }],
        "uncertainties": [{
            "id": "uncertainty.context-sufficiency",
            "question": "Does the selected context provide enough decision-relevant information, or must the recipient retrieve other source and run evidence?",
            "why_it_matters": "A reference-consistent packet can still omit information needed to choose the correct next action.",
        }],
        "handoff": {
            "id": "handoff.first-self-use",
            "from_worker": "producer.project-checkpoint",
            "to_worker": "recipient.fresh-reviewer",
            "scope": "From the received pack, identify one useful next engineering unit and what evidence would change the recommendation; distinguish missing facts from observed ones.",
            "required_decision_ids": ["decision.first-consumer"],
        },
    }
    state_file = write_json("work-state.json", work_state)
    work_id = cli("blob", state_file)["id"]
    root = cli("put", write_json("work-state-snapshot.json", {
        "type": "snapshot",
        "entries": [{"path": "work/state.json", "blob": work_id}],
    }))["id"]
    accepted = cli("accept", write_json("accept.json", {
        "acceptor": "pilot.self-use",
        "target": "context",
        "operation_id": "stage.initial",
        "expected": None,
        "candidate": root,
    }))
    assert accepted["receipt"]["outcome"] == "accepted"
    head = accepted["receipt"]["resulting"]
    request = {
        "schema": "continuum.prepare_context.v1",
        "work_state": work_id,
        "max_bytes": 32768,
        "anchor": {
            "acceptor": "pilot.self-use",
            "target": "context",
            "expected": head,
            "work_state_path": "work/state.json",
        },
    }
    prepared = cli("prepare-context", write_json("prepare.json", request))
    pack_id = prepared["context_pack"]
    inspected = cli("inspect-context", pack_id)
    verified = cli("verify-current-context", pack_id)
    assert verified["exact_projection_verified"] is True
    assert verified["action_authority_verified"] is False
    assert verified["freshness"]["status"] == "matches_at_observation"
    assert prepared["manifest"] == inspected["manifest"]
    assert not prepared["manifest"]["omitted"]
    rendered = inspected["rendered"].encode("utf-8")
    assert len(rendered) == inspected["manifest"]["rendered_bytes"]
    write("context.jsonl", rendered)
    write_json("prepared.json", prepared)
    write_json("verified.json", verified)

    # Keep byte-complete source copies, authored state, projection and the
    # disposable DB together. The report itself declares no actual recipient.
    binary_bytes = binary.read_bytes()
    report = {
        "schema": "continuum.real_checkpoint_observation.v1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "purpose": "First public self-use checkpoint; producer only.",
        "project_revision": git_observation(project),
        "binary_sha256": sha256(binary_bytes),
        "binary_bytes": len(binary_bytes),
        "source_snapshot": source_snapshot,
        "source": inputs,
        "work_state": work_id,
        "context_pack": pack_id,
        "context_jsonl_sha256": sha256(rendered),
        "included_records": inspected["manifest"]["included"],
        "omitted_records": inspected["manifest"]["omitted"],
        "freshness_at_observation": verified["freshness"],
        "cli_processes_completed": subprocess_count,
        "recipient_state": "offered_only",
        "limitations": [
            "Source references and staged files are retained; the rendered context does not inline source file bytes.",
            "The producer created a local disposable SQLite store; no workstation installation or remote dispatch occurred.",
            "A recipient has not yet inspected, accepted or completed this handoff.",
            "The producer's authored WorkState is not independent evidence that its assertions are true.",
        ],
    }
    write_json("result.json", report)
    print(json.dumps({
        "result": str(output / "result.json"),
        "context": str(output / "context.jsonl"),
        "context_pack": pack_id,
        "source_snapshot": source_snapshot,
        "rendered_bytes": len(rendered),
        "omitted_count": len(inspected["manifest"]["omitted"]),
        "exact_projection_verified": True,
        "recipient_state": "offered_only",
    }, indent=2))


if __name__ == "__main__":
    main()
