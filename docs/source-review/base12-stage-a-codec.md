# Stage-A codec: integrity, reconstruction and publication boundaries

Reviewed 2026-10-19 UTC at private Base12 commit `88382e793b65c84fd8e223840c27f6bb8682864a`, tree `5cf96129bdcb0dde075f6f5800ae0c68a95c4b82`. All seven selected files / 44,506 bytes were fully read: `README.md`, `PROTOCOL.md`, `WIRE.md`, `codec.py`, `native_signal.py`, `record100.py` and `check.py` in `research/owned-stack/2026-10-15/ecg-codec-stage-a/`. Exact identities are in the [ledger](base12-coverage-stage-a-codec.json).

Four Python sources were parsed without import. No upstream module, native instruction, test, codec, acquisition or benchmark ran. No waveform/header payload was acquired. The README's preparation-time statements about unpublished work and absent real-record execution are historical; later integrations reviewed elsewhere already describe subsequent work. Neither those older statements nor their later wrappers are a current instruction to repeat it.

## Research Delta: integrity gates exercise different failure classes

The source separates an outer archive checksum, bounded metadata and structural parsing, exact reconstruction, and an inner digest of the framed original header/signal pair. `check.py` distinguishes single-bit mutations rejected by the outer digest from rehashed faults that reach selected metadata, mode and original-digest checks. These checks answer different questions: a successful checksum rejection does not exercise the parser path behind that checksum. An unkeyed digest also does not authenticate an author.

For Continuum, corruption checks should state which admission layer they reach. Source-object integrity, valid structure, accepted state and semantic truth remain separate. Testing many mutations stopped at the same outer gate does not establish broad coverage of deeper invariants. This reading inspects test intent and control flow; it does not verify the README's reported assertion totals or rerun malformed inputs.

The code also uses separately formulated finite differences, packing checks and published-value pins to challenge self-consistent encode/decode behavior. `record100.py` checks selected source identities and declared initial/sample-sum values before its local run. The correctness of those external publisher facts was not independently reopened here. Same-author alternative calculations can detect particular errors without becoming independent institutions or proof of all machine instructions.

## Research Delta: validated bytes do not make a multi-file effect atomic

`codec.py` validates an archive and reconstructs the pair before its CLI creates the destination directory. It then writes the header and signal as separate effects. The source order is directory creation on line 193, followed by the two `write_bytes` calls on line 194. A stop after the header write and before completion of the signal write can therefore leave an incomplete destination. A later invocation refuses an existing output path.

This is a source-derived interruption schedule, not a fault-injection result, observed historical failure, or claim that the codec promised atomic publication. It distinguishes three properties: valid reconstructed content, completed output publication, and safe recovery after an uncertain effect. A fresh destination rule avoids ordinary overwrite but does not itself reconcile a partial earlier effect.

Continuum's backup exporter already has its own staging/publication contract. Future multi-artifact exports or executor results should similarly specify the coherent completion marker and reconciliation behavior. Do not retry into an existing directory merely because the earlier caller lacked acknowledgement. Preserve partial evidence and determine the actual effect first. This review implements no new export mechanism and makes no upstream edit.

## Research Delta: inspect the boundary actually used by each component

Unlike the previously reviewed alignment runner, `native_signal.py` checks its declared vendor file hashes before its explicit `isa` and `runtime` imports. This narrower source-order observation is useful; it is not proof of immutable files between reading and loading, a fresh module namespace, or a sandbox. Its wrapper checks sample/residual ranges and block lengths before calling generated routines, while parsing and Rice coding remain Python work.

The wire contract bounds archive, frame, header and tail sizes, fixes exact byte-cost selection and padding rules, and retains original opaque bytes. Native kernels cover numerical prediction/reconstruction, not the complete application or producer toolchain. The source's common decoder code and optional external compressor wrappers have distinct roles. Exact reconstruction, native ownership, compression benefit and performance each need their own evidence.

`record100.py` refuses existing run directories and records intermediate artifacts before later external references finish. Missing or mismatched optional tools are reported rather than installed automatically. A failure after useful intermediate work is thus a partial attempt to preserve, not grounds to invent a completed result or silently rerun the scientific exposure.

## Coverage and next evidence

All seven byte strings match the pinned Git blob and length; raw SHA-256 was recomputed and full UTF-8 texts read. Three Markdown documents and four Python sources were inspected. Syntax-derived source-order observations are retained in the [validation record](../../research/runs/base12-stage-a-codec/validation.json). Saved check records, subsequent integration manifests and inherited vendor bytes were not newly audited in this unit. Private code and operational payloads remain outside public Git.

Cumulative direct reading is **215 distinct blobs / 1,479,552 bytes**, plus **48 byte-identical alias paths**. This covers 263 paths by reading or byte equality; **5,330 paths / 4,214 distinct blobs** remain without complete semantic-reading claims. Alias directory context is not separately reviewed. The historical acquisition aggregate remains 539 paths / 530 blobs / 4,536,603 path bytes because its full overlap index was not recovered. New fetches are not blindly added. Hosted CI checks this public contribution, not private-source reading or historical execution.

Next bounded unit: nine unread files / 28,461 bytes comprising this group's `INTEGRATION.md`, `PRESERVATION.json`, `MANIFEST.json` and six direct children of `records/`. Reconcile fresh main and ownership, then connect the source contracts to retained checks and publication history without executing upstream code or repeating an old run. No recipient has accepted that unit; the separate owned-storage model lane retains its ownership.
