# CSV inspection pilot workload

This is a small independent public sample for a Continuum handoff, not a general data-analysis product. Requires Python 3; uses its standard library only.

Run `python3 inspect_csv.py sample.csv`. Output is one JSON object with data-row count and ordered per-column present/missing counts. Exact empty strings, including quoted empty cells, are missing. Whitespace and `NA` are present. Do not trim or case-fold values. A header-only file has zero data rows. Inputs use UTF-8 and the standard comma dialect, allowing quoted commas/newlines.

Header names must be nonempty and unique. Every parsed data record must have the header's width; missing trailing cells are an error, not inferred empties. Invalid UTF-8/CSV, missing header, duplicate names, and ragged rows fail with exit code 1, a JSON error on stderr, and no partial stdout. Blank physical records parse as zero-width records and therefore fail. CSV decoding uses `strict=True`; no stronger CSV standard compliance is claimed.

Run tests with `python3 -m unittest -v`.

## Missing-value tokens

Use the repeatable `--missing-value TOKEN` option to mark more values as missing, for example `python3 inspect_csv.py sample.csv --missing-value NA --missing-value N/A`. The exact empty string is always missing. Each listed token also counts as missing. Matching uses exact, case-sensitive equality against the parsed cell value, so quoting is removed before comparison and no trimming is done. With `--missing-value NA`, `NA` and `"NA"` are missing, while `na`, ` NA ` and whitespace stay present unless each is listed explicitly.

Repeating a token does not double-count. Each cell counts as missing at most once. `--missing-value ""` (or `--missing-value=`) is valid and changes nothing, because the empty string is already missing. Header names are never compared with tokens. Without the option, behavior and output shape are unchanged, and all validation rules above still apply when it is supplied. To pass a token that begins with `-`, use the `--missing-value=TOKEN` form.
