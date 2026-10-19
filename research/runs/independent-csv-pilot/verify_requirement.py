#!/usr/bin/env python3
"""Coordinator-authored CLI oracle, withheld from the successor's input."""
import csv
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile


def verify(script):
    # Counts below were derived manually from these five records, not from
    # the successor implementation or tests. They include a quoted newline.
    records = [["NA", ""], ["na", " NA "], ["", "null"], [" ", "NA"], ["a,\nb", "null"]]
    cases = [
        ([], [1, 1]),
        (["--missing-value", "NA"], [2, 2]),
        (["--missing-value", "NA", "--missing-value", "null"], [2, 4]),
        (["--missing-value", "NA", "--missing-value", "NA"], [2, 2]),
        (["--missing-value", ""], [1, 1]),
        (["--missing-value", "na", "--missing-value", " NA "], [2, 2]),
        (["--missing-value", " "], [2, 1]),
        (["--missing-value", "a,\nb"], [2, 1]),
    ]
    observed = []
    with tempfile.TemporaryDirectory() as directory:
        source = Path(directory) / "fixture.csv"
        with source.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.writer(stream)
            writer.writerow(["a", "b"])
            writer.writerows(records)
        for options, missing in cases:
            command = [sys.executable, str(script), str(source), *options]
            run = subprocess.run(command, capture_output=True, text=True)
            expected = {"rows": 5, "columns": [
                {"name": name, "present": 5 - count, "missing": count}
                for name, count in zip(["a", "b"], missing)
            ]}
            observed.append({"options": options, "returncode": run.returncode,
                             "stdout": run.stdout, "stderr": run.stderr, "expected": expected})
            if run.returncode != 0 or json.loads(run.stdout) != expected:
                print(json.dumps({"passed": False, "observations": observed}, indent=2))
                return 1
        source.write_text("a,b\nNA\n", encoding="utf-8")
        run = subprocess.run([sys.executable, str(script), str(source), "--missing-value", "NA"],
                             capture_output=True, text=True)
        assert run.returncode == 1 and run.stdout == "" and "error" in json.loads(run.stderr)
        observed.append({"case": "ragged input under options", "returncode": run.returncode,
                         "stdout": run.stdout, "stderr": run.stderr})
    print(json.dumps({"passed": True, "observations": observed}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(verify(Path(sys.argv[1]).resolve()))
