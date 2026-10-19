# Exact builder grammar-boundary inputs

This Research Delta reads fixture inputs 15–32 under `research/owned-stack/2026-10-16/native-builder-slice/preparation-01/fixtures/inputs/` at Base12 commit `88382e793b65c84fd8e223840c27f6bb8682864a`, tree `5cf96129bdcb0dde075f6f5800ae0c68a95c4b82`. The eighteen paths total 401 bytes. This chat owns the read-only contribution, based on Continuum main `533fca0d1bf13c14865fda524a85cac278aabbd2`. The [ledger](base12-coverage-builder-grammar-inputs.json) binds every source identity; the [validation record](../../research/runs/base12-builder-grammar-inputs/validation.json) records original byte and metadata checks.

## Complete byte reading, explicit empty-file classification

All eighteen byte sequences were inspected through a lossless escaped-byte representation. Seventeen nonempty sources receive complete semantic-reading credit. Input15 is exactly zero bytes and receives a mechanical length/Git/SHA-256 identity check, without semantic-reading credit. That check does not promote every empty file alias in the repository into a full reading.

Every source length and SHA-256 agrees with the frozen case manifest and fixture checksum list. LF-byte counts and physical-line counts also agree. Input32 has one LF byte but two physical lines because its final line lacks a terminating LF. The distinction is checked directly from the bytes, rather than delegated to a text API that might split other control characters.

All sixteen inputs15–30 exactly match the materializer's literal invalid-source dictionary, read with `ast.literal_eval` without importing or running the materializer. Inputs31/32 agree with bounded source derivations for the two accepted grammar boundaries. No source was normalized or repaired before comparison.

## Rejection examples retain their intended bytes

The sixteen declared rejections cover empty and label-only input; absent, misplaced, duplicate or undefined entry/target labels; invalid name characters; an unknown mnemonic/register; wrong arity; a fifth token; and four byte-level conditions. These remain authored admission cases, not newly executed parser tests.

The byte-level inputs contain one NUL, one carriage return, one byte `0x80`, and one control byte in a comment, respectively. Input29 is not valid UTF-8. Input30 demonstrates that a comment delimiter does not make every later byte acceptable under this grammar. Dropping a NUL, normalizing CRLF, decoding with replacement, or stripping comments before checking byte restrictions would change the test input or the condition it is intended to exercise.

These observations preserve the actual fixture payloads. They do not claim exhaustive lexical coverage or independently prove which native guard executes first.

## Two positive boundaries and their map relations

Input31 places a comment delimiter immediately after a numeric operand, without intervening whitespace. Its frozen expectation is acceptance. Input32 omits the final LF and likewise expects acceptance. Treating every unusual input in this numbered group as malformed would therefore lose the positive boundary cases.

Original lexical source-count checks agree with the manifest for all eighteen files. Those counts describe authored statements and labels, including statements that a rejecting parser might never reach. They are not observations of parser progress.

Each positive case declares one label and one instruction. Reconstructing its two literal map records and header produces 96 bytes and matches the expected map digest. The declared ELF lengths agree with the fixed prefix plus the respective authored instruction length. No expected ELF was generated, and neither actual output map was acquired.

All eighteen case statuses and output-state declarations also match the already held derived saved review: sixteen source-error statuses with absent outputs and two accepted output pairs. This is a source/expectation/saved-metadata join. It neither reruns the candidate nor acquires the private output files that underlie the historical review.

## Transferable result and remaining scope

Byte custody matters even for tiny text-like inputs. A continuation pack should preserve whether its source representation is raw bytes, decoded text, or normalized text, and state where transformations occur. A small boundary corpus can lose its purpose through apparently helpful decoding or cleanup. Empty sources and missing terminators also need deliberate accounting rather than inflated reading claims.

Two additional pinned input paths share a newly read nonempty blob and receive identical-blob credit. That content identity does not review their associated cases, profiles or result metadata.

No upstream module was imported, materializer/candidate executed, native artifact emitted, model consulted, live process scanned, workstation worker activated or upstream result accepted.

Semantic reading reaches **551 distinct blobs / 4,883,117 bytes**, plus **79 identical alias paths**. The remaining semantic-reading gap is **4,963 paths / 3,878 distinct blobs**; mechanical empty-file checks remain separately classified. Historical global acquisition overlap remains unresolved, and whole-repository reading remains incomplete.

Next: complete numeric-endpoint fixture inputs33–48, sixteen paths / 530 bytes, and join their literal values to the earlier endpoint specifications and frozen expectations without execution. Reconcile fresh main and ownership first; no recipient has accepted that unit. Separate storage, dispatch and public checkpoint lanes retain ownership.
