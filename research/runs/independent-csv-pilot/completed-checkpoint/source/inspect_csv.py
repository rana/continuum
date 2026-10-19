#!/usr/bin/env python3
"""Count present and missing cells in a rectangular UTF-8 CSV."""
import argparse
import csv
import json
from pathlib import Path
import sys


def inspect(path, missing_values=()):
    tokens = {"", *missing_values}
    with Path(path).open(encoding="utf-8", newline="") as stream:
        reader = csv.reader(stream, strict=True)
        header = next(reader, None)
        if not header or any(name == "" for name in header) or len(set(header)) != len(header):
            raise ValueError("CSV requires nonempty unique column names")
        missing = [0] * len(header)
        rows = 0
        for row in reader:
            if len(row) != len(header):
                raise ValueError(f"record {rows + 1} has {len(row)} cells; expected {len(header)}")
            rows += 1
            for index, value in enumerate(row):
                missing[index] += value in tokens
    return {"rows": rows, "columns": [
        {"name": name, "present": rows - absent, "missing": absent}
        for name, absent in zip(header, missing)
    ]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--missing-value", action="append", default=[], metavar="TOKEN",
                        help="additional exact, case-sensitive missing token; repeatable")
    args = parser.parse_args()
    try:
        result = inspect(args.input, args.missing_value)
    except (OSError, UnicodeError, csv.Error, ValueError) as error:
        print(json.dumps({"error": str(error)}), file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
