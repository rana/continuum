#!/usr/bin/env python3
"""Retain one committed Git source and authored WorkState via the native CLI.

Git is used only by this adapter. Outputs use a fresh disposable database.
"""
import argparse
import hashlib
import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def checkpoint(args):
    binary = args.binary.resolve(strict=True)
    repository = args.repository.resolve(strict=True)

    def git(*values):
        return subprocess.run(["git", "-C", str(repository), *values], check=True,
                              capture_output=True).stdout

    revision = git("rev-parse", "--verify", args.revision + "^{commit}").decode().strip()
    # Validate the entire inventory before writing output or initializing a store.
    files = []
    for record in git("ls-tree", "-rz", "--full-tree", revision).split(b"\0"):
        if not record:
            continue
        header, raw_path = record.split(b"\t", 1)
        mode, kind, oid = header.decode("ascii").split()
        path = raw_path.decode("utf-8", errors="strict")
        parts = PurePosixPath(path).parts
        if (mode not in ("100644", "100755") or kind != "blob" or
                path.startswith("/") or ".." in parts or "\\" in path or
                str(PurePosixPath(path)) != path):
            raise ValueError(f"unsupported snapshot entry: {mode} {path!r}")
        files.append((path, mode, oid))
    state_bytes = args.work_state.read_bytes()
    state = json.loads(state_bytes)
    if state.get("source_snapshot", "missing") is not None:
        raise ValueError("authored WorkState must set source_snapshot to null for explicit binding")
    provenance_bytes = args.build_provenance.read_bytes()
    provenance = json.loads(provenance_bytes)
    binary_digest = sha256(binary.read_bytes())
    if provenance["binary_sha256"] != binary_digest:
        raise ValueError("build provenance binary digest does not match executable")
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    source = output / "source"
    source.mkdir()
    database = output / "work.db"
    (output / "authored-work-state.json").write_bytes(state_bytes)
    (output / "build-provenance.json").write_bytes(provenance_bytes)

    def cli(command, *values):
        argv = [str(binary), command, str(database), *(str(v) for v in values)]
        result = subprocess.run(argv, capture_output=True, text=True, check=False)
        with (output / "cli-log.jsonl").open("a", encoding="utf-8") as log:
            log.write(json.dumps({"argv": argv, "returncode": result.returncode,
                                  "stdout": result.stdout, "stderr": result.stderr}) + "\n")
        if result.returncode:
            raise RuntimeError(result.stderr)
        return json.loads(result.stdout)

    cli("init")
    entries, inventory = [], []
    for path, mode, oid in files:
        data = git("cat-file", "blob", oid)
        retained = source / path
        retained.parent.mkdir(parents=True, exist_ok=True)
        retained.write_bytes(data)
        blob_id = cli("blob", retained)["id"]
        entries.append({"path": path, "blob": blob_id})
        inventory.append({"path": path, "git_mode": mode, "git_blob": oid,
                          "sha256": sha256(data), "bytes": len(data), "blob": blob_id})
    snapshot = cli("put", write_json(output / "source-snapshot.json",
                                    {"type": "snapshot", "entries": entries}))["id"]
    state["source_snapshot"] = snapshot
    state_id = cli("blob", write_json(output / "work-state.json", state))["id"]
    wrapper = cli("put", write_json(output / "state-snapshot.json", {
        "type": "snapshot", "entries": [{"path": "work-state.json", "blob": state_id}]
    }))["id"]
    accepted = cli("accept", write_json(output / "accept.json", {
        "acceptor": "project-checkpoint", "target": "work",
        "operation_id": "initial-checkpoint", "expected": None, "candidate": wrapper,
    }))
    prepared = cli("prepare-context", write_json(output / "prepare.json", {
        "schema": "continuum.prepare_context.v1", "work_state": state_id,
        "max_bytes": args.max_bytes, "anchor": {
            "acceptor": "project-checkpoint", "target": "work",
            "expected": accepted["receipt"]["resulting"], "work_state_path": "work-state.json",
        },
    }))
    pack_id = prepared["context_pack"]
    inspected = cli("inspect-context", pack_id)
    (output / "context.jsonl").write_text(inspected["rendered"], encoding="utf-8")
    write_json(output / "coverage.json", inspected["manifest"])
    verification = cli("verify-current-context", pack_id)
    write_json(output / "verification.json", verification)
    manifest = {
        "schema": "continuum.project_checkpoint.v1", "created_utc": datetime.now(timezone.utc).isoformat(),
        "source": {"commit": revision, "git_tree": git("rev-parse", revision + "^{tree}").decode().strip(),
                   "snapshot": snapshot, "files": inventory},
        "work_state": state_id, "context_pack": pack_id,
        "binary_sha256": binary_digest, "build_provenance_sha256": sha256(provenance_bytes),
        "adapter_sha256": sha256(Path(__file__).read_bytes()),
        "environment": {"platform": platform.platform(), "python": sys.version},
        "limits": ["Committed regular UTF-8 paths only; working-tree edits and untracked files are excluded.",
                   "Git executable modes are inventoried but not represented by native Snapshot v1.",
                   "Build provenance is caller-authored; digest binding is checked, build truth is not.",
                   "Disposable store: no upgrade, backup, workstation installation or recipient effect claimed.",
                   "Context coverage describes WorkState records, not source-file reading coverage."],
    }
    write_json(output / "checkpoint.json", manifest)
    return {"checkpoint": str(output / "checkpoint.json"), "context_pack": pack_id}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", type=Path, required=True)
    parser.add_argument("--repository", type=Path, required=True)
    parser.add_argument("--revision", default="HEAD")
    parser.add_argument("--work-state", type=Path, required=True)
    parser.add_argument("--build-provenance", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--max-bytes", type=int, default=32768)
    args = parser.parse_args()
    try:
        print(json.dumps(checkpoint(args), indent=2))
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError, RuntimeError) as error:
        parser.exit(1, f"checkpoint failed: {error}\n")


if __name__ == "__main__":
    main()
