# CSV inspection pilot workload

This is a small independent public sample for a Continuum handoff, not a general data-analysis product. Requires Python 3; uses its standard library only.

Run `python3 inspect_csv.py sample.csv`. Output is one JSON object with data-row count and ordered per-column present/missing counts. Exact empty strings, including quoted empty cells, are missing. Whitespace and `NA` are present. Do not trim or case-fold values. A header-only file has zero data rows. Inputs use UTF-8 and the standard comma dialect, allowing quoted commas/newlines.

Header names must be nonempty and unique. Every parsed data record must have the header's width; missing trailing cells are an error, not inferred empties. Invalid UTF-8/CSV, missing header, duplicate names, and ragged rows fail with exit code 1, a JSON error on stderr, and no partial stdout. Blank physical records parse as zero-width records and therefore fail. CSV decoding uses `strict=True`; no stronger CSV standard compliance is claimed.

Run tests with `python3 -m unittest -v`.

## Offered requirement change

Add repeatable `--missing-value TOKEN` options. Exact `""` remains missing whether options are supplied or not. Every supplied token is additionally missing, with exact case-sensitive equality and no trimming. Repeated identical options must not double-count. Default behavior and output shape stay unchanged. The sample's `NA` temperature becomes missing only when `--missing-value NA` is passed; `na`, ` NA ` and whitespace stay present unless each is explicitly listed. Preserve all validation and quoted-field behavior. Add meaningful tests of defaults, multiple tokens, duplicate options, empty option, exact matching, and interaction with quoted cells.
