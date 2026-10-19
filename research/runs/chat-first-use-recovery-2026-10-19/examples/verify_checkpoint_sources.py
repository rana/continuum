#!/usr/bin/env python3
"""Compare a public project checkpoint's recorded source bytes with a checkout.

This is a read-only, selected-file comparison, not native context verification,
Git HEAD acceptance, or an authentication/authorization mechanism.
"""

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

MAX_REPORT_BYTES = 1_048_576
MAX_SOURCE_BYTES = 262_144
HEX_SHA256 = re.compile(r"[0-9a-f]{64}\Z")


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def check(report_path, project):
    raw = report_path.read_bytes()
    if len(raw) > MAX_REPORT_BYTES:
        raise ValueError("report exceeds 1 MiB")
    report = json.loads(raw)
    if report.get("schema") != "continuum.real_checkpoint_observation.v1":
        raise ValueError("unsupported checkpoint report schema")
    records = report.get("source")
    if not isinstance(records, list) or not 1 <= len(records) <= 256:
        raise ValueError("source must contain 1..256 entries")

    found = []
    seen = set()
    for item in records:
        if not isinstance(item, dict):
            raise ValueError("invalid source entry")
        name = item.get("path")
        expected_sha = item.get("sha256")
        expected_bytes = item.get("bytes")
        if (not isinstance(name, str) or not name or name.startswith("/")
                or "\\" in name or any(p in ("", ".", "..") for p in name.split("/"))):
            raise ValueError("source path must be normalized and relative")
        if name in seen:
            raise ValueError("duplicate source path")
        seen.add(name)
        if not isinstance(expected_sha, str) or not HEX_SHA256.fullmatch(expected_sha):
            raise ValueError("invalid source SHA-256")
        if type(expected_bytes) is not int or not 0 <= expected_bytes <= MAX_SOURCE_BYTES:
            raise ValueError("invalid recorded source byte count")
        candidate = project.joinpath(*name.split("/"))
        parts = [project]
        for part in name.split("/"):
            parts.append(parts[-1] / part)
        entry = {"path": name, "expected_sha256": expected_sha,
                 "expected_bytes": expected_bytes}
        if any(path.is_symlink() for path in parts):
            entry["status"] = "symlink_not_followed"
        elif not candidate.is_file():
            entry["status"] = "not_a_regular_file"
        else:
            with candidate.open("rb") as handle:
                content = handle.read(MAX_SOURCE_BYTES + 1)
            if len(content) > MAX_SOURCE_BYTES:
                entry["status"] = "current_file_exceeds_256kib"
            else:
                actual_sha = sha256(content)
                entry["actual_sha256"] = actual_sha
                entry["actual_bytes"] = len(content)
                entry["status"] = ("matches" if
                    actual_sha == expected_sha and len(content) == expected_bytes
                    else "differs")
        found.append(entry)

    return {
        "schema": "continuum.selected_source_comparison.v1",
        "checkpoint_report_sha256": sha256(raw),
        "source_snapshot": report.get("source_snapshot"),
        "checked_files": found,
        "all_selected_source_bytes_match": all(f["status"] == "matches" for f in found),
        "limits": [
            "Compares only the source file paths explicitly listed in the checkpoint report.",
            "Does not compare unlisted files, Git tree identity, model inputs, or received context.",
            "Does not inspect Continuum's SQLite accepted head or verify a context projection.",
            "A matching checkout does not establish that the report, author, or source was trusted.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--project", type=Path, required=True)
    args = parser.parse_args()
    try:
        project = args.project.resolve(strict=True)
        if not project.is_dir():
            raise ValueError("project must be a directory")
        result = check(args.report.resolve(strict=True), project)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"checkpoint source comparison error: {error}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0 if result["all_selected_source_bytes_match"] else 2


if __name__ == "__main__":
    sys.exit(main())
