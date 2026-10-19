# Exact binary map metadata

This Research Delta fully reads `research/owned-stack/2026-10-16/native-builder-slice/preparation-01/fixtures/expected/02.map`, `03.map` and `04.map` at Base12 commit `88382e793b65c84fd8e223840c27f6bb8682864a`, tree `5cf96129bdcb0dde075f6f5800ae0c68a95c4b82`. The three binary metadata files total 7,808 bytes. This chat owns the read-only contribution based on Continuum main `92742c5f4196cb48d387d3ce590e6653f73f6f56`. The [ledger](base12-coverage-builder-map-metadata.json) pins each file; the [validation record](../../research/runs/base12-builder-map-metadata/validation.json) preserves actual field checks and their scope. No private map payload is published.

## From predicted identity to metadata custody

Earlier reviews reconstructed these map digests from expected source-position records. This unit acquires the actual pinned expected-map bytes and reads every field through a lossless decoded projection. The version, record count, code length and every record's kind, physical source line, file offset and encoded length agree with the fully read layouts. Encoding the decoded values back into the fixed little-endian representation reproduces every acquired byte.

| Case | Metadata bytes | Records | Declared code bytes |
| --- | ---: | ---: | ---: |
| 02 | 7,200 | 224 | 538 |
| 03 | 192 | 5 | 24 |
| 04 | 416 | 12 | 58 |

All 241 records agree with the expected layouts. Checksum-list entries, case-manifest lengths/digests, authored counts and saved map metadata also agree. Acquisition changes the evidence from a predicted hash relation to exact custody and reading of the expected binary metadata. It does not become observation of a fresh native output or acquisition of the private execution attempt's raw maps.

## Reproducible bounded reader

The original public [reader](../../research/runs/base12-builder-map-metadata/map_metadata.py) decodes this frozen metadata format using only Python's standard library. It checks input size before decoding, requires an exact header/count/length relation, rejects unknown record kinds and invalid encoded lengths, preserves increasing physical source lines, and checks continuous code spans. It enforces the retained instruction and label bounds separately from the aggregate row bound.

Zero-length label rows may share file offsets or occur at code end. Those are legitimate cases already established by the reviewed source and layouts; a reader that required every row to advance the code cursor would lose them. The maximum record case combines 128 labels with 1,024 instructions for a 36,896-byte map.

Eight original [test methods](../../research/runs/base12-builder-map-metadata/test_map_metadata.py) pass. They cover complete little-endian fields, shared offsets and terminal labels, exact maximum capacity, truncation/trailing/oversized payloads, wrong magic/version/count/code bounds, a big-endian header, invalid kinds/lengths/line order/offsets, code-span disagreement and each individual count limit. Tests use synthetic public records and require no upstream payload access.

Reproduce them with:

```sh
python3 -m unittest discover -s research/runs/base12-builder-map-metadata -p 'test_*.py' -v
```

The same command is added to hosted CI. Passing these tests checks the reader's finite structural contract; it does not certify arbitrary instruction or ELF behavior.

## Metadata does not contain every identity

The map contains no label names, instruction bytes, ELF digest, source content, publication status or authenticated invocation identity. Structural decoding cannot recover those facts. This unit compares map rows with already reviewed layouts to establish the corresponding relation; the reader alone supplies no authenticity or runtime acceptance claim.

Pinned tree equality adds twelve identical-content alias paths, including expected maps in fault cases and retained paths in two other builder profiles. That gives content-reading credit, without newly acquiring those paths or reviewing their surrounding runtime/result contexts. In particular, a path containing a saved result name does not make this expected-map acquisition a fresh result verification.

The transferable lesson is to name exactly what changed at the evidence boundary. A reconstructed digest, acquired expected metadata, independently checked fields and observed native output are distinct facts. A small reproducible reader can close a representation gap while leaving absent identities explicit.

No native ELF/code artifact was acquired, upstream module imported, materializer/candidate executed, native artifact emitted, model consulted, live process scanned, workstation activated or upstream recipient acceptance obtained.

Semantic reading reaches **598 distinct blobs / 5,247,643 bytes**, plus **106 identical alias paths**. **4,889 paths / 3,831 distinct blobs** still lack full semantic-reading credit. Historical global acquisition overlap and whole-repository reading remain incomplete.

Next: fully decode twelve small expected-map metadata paths05/09/13/31/32/33/35/37/39/41/43/45, totaling 5,248 path bytes, and preserve repeated map-shape identity separately from code identity. Reconcile fresh main and ownership first; owned-storage, dispatch and public checkpoint lanes remain separate. No recipient has accepted that next unit.
