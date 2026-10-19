#!/usr/bin/env python3
"""Retain one committed Git source and authored WorkState via the native CLI.

Git is used only by this adapter. Outputs use a fresh disposable database.
"""
import argparse
import hashlib
import json
import platform
import re
import subprocess
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def sha256(data):
    return hashlib.sha256(data).hexdigest()


MAX_IMPORT_BYTES = 16 * 1024 * 1024
MAX_IMPORT_OBJECTS = 256


def strict_json(data):
    def pairs(items):
        value = {}
        for key, item in items:
            if key in value:
                raise ValueError(f"duplicate JSON key: {key}")
            value[key] = item
        return value

    def nonfinite(value):
        raise ValueError(f"nonfinite JSON number: {value}")

    return json.loads(data, object_pairs_hook=pairs, parse_constant=nonfinite)


def read_imports(path):
    if path is None:
        return None, {}
    with path.open("rb") as stream:
        raw = stream.read(MAX_IMPORT_BYTES + 1)
    if len(raw) > MAX_IMPORT_BYTES:
        raise ValueError("object bundle exceeds 16 MiB")
    bundle = strict_json(raw)
    if (not isinstance(bundle, dict) or set(bundle) != {"schema", "objects"} or
            bundle["schema"] != "continuum.object_bundle.v1" or
            not isinstance(bundle["objects"], list)):
        raise ValueError("expected continuum.object_bundle.v1 with objects array")
    if len(bundle["objects"]) > MAX_IMPORT_OBJECTS:
        raise ValueError("object bundle exceeds 256 objects")
    objects = {}
    for envelope in bundle["objects"]:
        if (not isinstance(envelope, dict) or set(envelope) != {"id", "format_version", "object"} or
                type(envelope["format_version"]) is not int or envelope["format_version"] != 1):
            raise ValueError("object envelope requires id, integer format_version 1 and object")
        identity = envelope["id"]
        if not isinstance(identity, str) or not re.fullmatch(r"sha256:[0-9a-f]{64}", identity):
            raise ValueError("invalid imported object ID")
        if identity in objects:
            raise ValueError(f"duplicate imported object ID: {identity}")
        obj = envelope["object"]
        if not isinstance(obj, dict):
            raise ValueError("imported object must be a Blob or Snapshot")
        if obj.get("type") == "blob" and set(obj) == {"type", "bytes"}:
            pass  # The native CLI validates byte values and canonical identity.
        elif obj.get("type") == "snapshot" and set(obj) == {"type", "entries"}:
            if (not isinstance(obj["entries"], list) or
                    any(not isinstance(e, dict) or set(e) != {"path", "blob"} or
                        not isinstance(e["blob"], str) for e in obj["entries"])):
                raise ValueError("invalid imported Snapshot entries")
        else:
            raise ValueError("import supports only v1 Blob and Snapshot objects")
        objects[identity] = obj
    return raw, objects


def require_import_closure(state, objects, captured):
    """Require only attempt roots and their Snapshot-to-Blob edges; no inference."""
    pending = []
    attempts = state.get("attempts", [])
    if not isinstance(attempts, list) or any(not isinstance(a, dict) for a in attempts):
        raise ValueError("attempts must be an array of records")
    for attempt in attempts:
        pending.extend([attempt["source_snapshot"], attempt["request"]])
        if attempt.get("receipt") is not None:
            pending.append(attempt["receipt"])
    visited = set()
    while pending:
        identity = pending.pop()
        if not isinstance(identity, str):
            raise ValueError("attempt reference must be an object ID")
        if identity in visited:
            continue
        visited.add(identity)
        obj = objects.get(identity, captured.get(identity))
        if obj is None:
            raise ValueError(f"missing attempt object closure: {identity}")
        if obj["type"] == "snapshot":
            pending.extend(entry["blob"] for entry in obj["entries"])
    extra = set(objects) - visited
    if extra:
        raise ValueError(f"unreferenced imported objects: {sorted(extra)}")


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
    # Conservatively reject names that common host filesystems may alias,
    # including file/directory conflicts. Shared identical directory prefixes are OK.
    names = {}
    for path, _, _ in files:
        parts = PurePosixPath(path).parts
        for count in range(1, len(parts) + 1):
            prefix = "/".join(parts[:count])
            kind = "file" if count == len(parts) else "directory"
            key = unicodedata.normalize("NFC", prefix).casefold()
            previous = names.get(key)
            if previous is not None and previous != (prefix, kind):
                raise ValueError(f"filesystem-aliased snapshot paths: {previous[0]!r}, {prefix!r}")
            names[key] = (prefix, kind)
    state_bytes = args.work_state.read_bytes()
    state = strict_json(state_bytes)
    if not isinstance(state, dict) or state.get("source_snapshot", "missing") is not None:
        raise ValueError("authored WorkState must set source_snapshot to null for explicit binding")
    provenance_bytes = args.build_provenance.read_bytes()
    provenance = strict_json(provenance_bytes)
    import_bytes, imported = read_imports(args.import_objects)
    binary_bytes = binary.read_bytes()
    binary_digest = sha256(binary_bytes)
    if not isinstance(provenance, dict) or provenance.get("binary_sha256") != binary_digest:
        raise ValueError("build provenance binary digest does not match executable")
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    # Run the measured bytes, even if a concurrent build replaces the input binary.
    runtime = output / "runtime"
    runtime.mkdir()
    binary = runtime / binary.name
    binary.write_bytes(binary_bytes)
    binary.chmod(0o700)
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

    if import_bytes is not None:
        (output / "import-objects.json").write_bytes(import_bytes)
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
    captured = {item["blob"]: {"type": "blob"} for item in inventory}
    captured[snapshot] = {"type": "snapshot", "entries": entries}
    require_import_closure(state, imported, captured)
    imported_records = []
    if imported:
        imports_dir = output / "imports"
        imports_dir.mkdir()
        # Snapshot v1 has only Blob edges, so two passes suffice in any input order.
        ordered = sorted(imported, key=lambda identity: (imported[identity]["type"] != "blob", identity))
        for index, identity in enumerate(ordered):
            obj = imported[identity]
            path = write_json(imports_dir / f"{index:04d}.json", obj)
            actual = cli("put", path)["id"]
            if actual != identity:
                raise ValueError(f"imported object identity mismatch: expected {identity}, got {actual}")
            imported_records.append({"id": identity, "type": obj["type"],
                                     "preexisting_in_source_capture": identity in captured})
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
    for item in inventory:
        if sha256((source / item["path"]).read_bytes()) != item["sha256"]:
            raise ValueError(f"retained source bytes changed: {item['path']!r}")
    manifest = {
        "schema": "continuum.project_checkpoint.v1", "created_utc": datetime.now(timezone.utc).isoformat(),
        "source": {"commit": revision, "git_tree": git("rev-parse", revision + "^{tree}").decode().strip(),
                   "snapshot": snapshot, "files": inventory},
        "work_state": state_id, "context_pack": pack_id,
        "imports": {"bundle_sha256": sha256(import_bytes) if import_bytes is not None else None,
                    "objects": imported_records,
                    "limits": {"max_bundle_bytes": MAX_IMPORT_BYTES, "max_objects": MAX_IMPORT_OBJECTS}},
        "binary_sha256": binary_digest, "build_provenance_sha256": sha256(provenance_bytes),
        "adapter_sha256": sha256(Path(__file__).read_bytes()),
        "environment": {"platform": platform.platform(), "python": sys.version},
        "limits": ["Committed regular UTF-8 paths only; working-tree edits and untracked files are excluded.",
                   "NFC/casefold path aliases and file/directory aliases are conservatively rejected; retained bytes are rechecked.",
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
    parser.add_argument("--import-objects", type=Path, help="exact v1 Blob/Snapshot bundle for attempt references")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--max-bytes", type=int, default=32768)
    args = parser.parse_args()
    try:
        print(json.dumps(checkpoint(args), indent=2))
    except (OSError, ValueError, KeyError, TypeError, subprocess.CalledProcessError, RuntimeError) as error:
        parser.exit(1, f"checkpoint failed: {error}\n")


if __name__ == "__main__":
    main()
