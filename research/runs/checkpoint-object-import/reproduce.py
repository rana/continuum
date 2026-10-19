#!/usr/bin/env python3
"""Reconstruct the actual CSV model turn in two disposable checkpoint stores.

Uses retained public files only. No inference, dispatch, network or store upgrade.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    return path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", type=Path, required=True)
    parser.add_argument("--build-provenance", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[3]
    prior = root / "research/runs/independent-csv-pilot"
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    runtime = output / "runtime"
    runtime.mkdir()
    binary = runtime / args.binary.name
    binary.write_bytes(args.binary.resolve(strict=True).read_bytes())
    binary.chmod(0o700)
    database = output / "seed.db"

    def cli(command, *values, db=database):
        argv = [str(binary), command, str(db), *map(str, values)]
        run = subprocess.run(argv, capture_output=True, text=True)
        with (output / "native-seed-log.jsonl").open("a", encoding="utf-8") as log:
            log.write(json.dumps({"argv": argv, "returncode": run.returncode,
                                  "stdout": run.stdout, "stderr": run.stderr}) + "\n")
        if run.returncode:
            raise RuntimeError(run.stderr)
        return json.loads(run.stdout)

    cli("init")
    old_manifest = json.loads((prior / "checkpoint/checkpoint.json").read_text())
    objects = {}
    for item in old_manifest["source"]["files"]:
        identity = cli("blob", prior / "checkpoint/source" / item["path"])["id"]
        assert identity == item["blob"]
        objects[identity] = cli("get", identity)
    old_snapshot = cli("put", prior / "checkpoint/source-snapshot.json")["id"]
    assert old_snapshot == old_manifest["source"]["snapshot"]
    objects[old_snapshot] = cli("get", old_snapshot)
    provenance = []
    references = {}
    for role, name in [("request", "implementation-request.json"), ("receipt", "implementation-response.json")]:
        path = prior / name
        identity = cli("blob", path)["id"]
        objects[identity] = cli("get", identity)
        references[role] = identity
        provenance.append({"role": role, "retained_file": str(path.relative_to(root)),
                           "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "blob": identity})
    # Intentionally reverse dependency order; the adapter must import by kind.
    bundle = write_json(output / "import-objects.json", {
        "schema": "continuum.object_bundle.v1", "objects": list(reversed(list(objects.values())))})
    state = json.loads((prior / "completed-work-state.json").read_text())
    state["id"] = "csv-recorded-attempt-work"
    state["attempts"] = [{
        "id": "csv-visible-turn", "operation_id": "csv-visible-turn-retrospective-1",
        "source_snapshot": old_snapshot,
        "summary": "Actual CSV successor turn reconstructed from retained visible request/response files.",
        "dispatch_state": "receipt_recorded", **references,
        "outcome_note": "Authored retrospective: exact local projections, not provider wire bytes or an authenticated request-response binding. The earlier coordinator executed the returned code and checks; this run performs no inference.",
    }]
    state["decisions"][0]["basis_attempt_ids"] = ["csv-visible-turn"]
    state["uncertainties"] = [{
        "id": "record-scope", "question": "Which evidence can a future receiver reuse for a new decision?",
        "why_it_matters": "Exact custody and an authored recorded receipt do not establish semantic truth or authorize another dispatch.",
    }]
    state["handoff"]["id"] = "recorded-attempt-followup-offer"
    state["handoff"]["scope"] = "Inspect the retained historical attempt and its receipt; do not reissue the model call. No recipient acceptance is claimed."
    state_path = write_json(output / "authored-work-state.json", state)
    provenance_bytes = args.build_provenance.read_bytes()
    build = json.loads(provenance_bytes)
    assert build["binary_sha256"] == hashlib.sha256(binary.read_bytes()).hexdigest()
    provenance_path = output / "build-provenance.json"
    provenance_path.write_bytes(provenance_bytes)
    repository = output / "csv-source"
    subprocess.run(["git", "clone", str(prior / "csv-source.bundle"), str(repository)],
                   capture_output=True, check=True)
    checkpoints = []
    for label in ["first", "reconstructed"]:
        argv = [sys.executable, str(root / "tools/project_checkpoint.py"), "--repository", str(repository),
                "--revision", "27e03a7ffd90260fc9545d89e11434d341043110", "--binary", str(binary),
                "--work-state", str(state_path), "--build-provenance", str(provenance_path),
                "--import-objects", str(bundle), "--output", str(output / label), "--max-bytes", "16384"]
        run = subprocess.run(argv, capture_output=True, text=True)
        write_json(output / f"{label}-command.json", {
            "argv": argv, "returncode": run.returncode, "stdout": run.stdout, "stderr": run.stderr})
        if run.returncode:
            raise RuntimeError(run.stderr)
        manifest = json.loads((output / label / "checkpoint.json").read_text())
        for identity, envelope in objects.items():
            restored = cli("get", identity, db=output / label / "work.db")
            assert restored == envelope
        for item in provenance:
            restored = cli("get", item["blob"], db=output / label / "work.db")
            assert hashlib.sha256(bytes(restored["object"]["bytes"])).hexdigest() == item["sha256"]
        rendered = [json.loads(line) for line in (output / label / "context.jsonl").read_text().splitlines()]
        attempt = next(line for line in rendered if line["kind"] == "attempt")
        assert attempt["conditional_next_action"] == "inspect_recorded_receipt"
        assert manifest["source"]["snapshot"] != old_snapshot
        assert json.loads((output / label / "verification.json").read_text())["exact_projection_verified"]
        checkpoints.append(manifest)
    assert checkpoints[0]["context_pack"] == checkpoints[1]["context_pack"]
    write_json(output / "result.json", {
        "scope": "Authored historical reconstruction of actual visible CSV collaborator records; no new inference or effect.",
        "historical_source_snapshot": old_snapshot, "current_source_snapshot": checkpoints[0]["source"]["snapshot"],
        "context_pack": checkpoints[0]["context_pack"], "imported_objects": len(objects),
        "same_pack_in_fresh_store": True, "all_native_envelopes_restored": True,
        "exact_pilot_request_receipt_bytes_verified": provenance,
        "conditional_next_action": "inspect_recorded_receipt",
    })
    print((output / "result.json").read_text())


if __name__ == "__main__":
    main()
