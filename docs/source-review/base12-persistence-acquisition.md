# Persistence audit and incomplete acquisition: preserve completed effects

Reviewed 2026-10-19 UTC at private Base12 commit `88382e793b65c84fd8e223840c27f6bb8682864a`, tree `5cf96129bdcb0dde075f6f5800ae0c68a95c4b82`. Three texts / 35,074 bytes were fully read: persistence-audit source, initial acquisition outcome and terminal envelope receipt. Every field of the outcome was read, including fourteen source declarations, forty-four saved-file rows and thirty-six remaining-file rows. Length, Git blob framing and SHA-256 checks passed; Python syntax and duplicate-key checked JSON were parsed without upstream execution. The [ledger](base12-coverage-persistence-acquisition.json) records identities.

## Research Delta: inspect the persistence audit's actual observation

The source digest matches the [post-run verification receipt](base12-audit-closeout.md). The audit checks a clean exact source head, hashes fourteen source files and the wrapper, verifies a pinned compressor binary and its path controls, binds result/terminal receipts, and compares seven existing output hashes with earlier metadata. It checks input inventory, regular-file type, owner, mode and size, while explicitly leaving input content un-rehashed. Private directory and output-entry checks are also filesystem observations at that historical audit.

This supports the receipt's narrow persistence/privacy scope. Seven output rehashes do not constitute a new decode or roundtrip, and input size/type checks do not replace content hashes. The source reads current filesystem paths; it is not an immutable host image or a power-loss durability experiment. No source or output check was executed here. Current evidence is the acquired audit source plus retained result and metadata agreement.

The missing initial acquisition outcome now matches its closeout hash and length. All seven linked closeout receipt payloads bind. Its embedded envelope object equals the separately acquired terminal receipt exactly. Source and wrapper declarations agree with acquired static records/source; the publisher manifest digest agrees with intake. This closes the preceding source/receipt gaps while leaving publisher and signal payload attestation historical.

For Continuum, an audit's name should not substitute for its predicate. Preserve which objects were rehashed, which were checked only as metadata, and which effect was merely referenced from an earlier run.

## Research Delta: incomplete operations can preserve complete artifacts

The initial acquisition ends with a recorded wall timeout and clean cleanup. Its saved inventory has forty-four complete training files, comprising twenty-two waveform/header pairs; no validation files are yet saved. All recorded saved hashes equal their publisher-hash fields and corresponding later recovery hashes. The remaining names are disjoint from the saved names and together equal the later eighty-file inventory.

| Saved relation | Recomputed value |
| --- | --- |
| Initial saved files | 44 training, 0 validation |
| Initial waveform / header bytes | 42,900,000 / 4,816 |
| Initial total bytes | 42,904,816 |
| Remaining files | 20 training, 16 validation |
| Later actual bytes for remaining names | 35,104,372 |
| Final union | 80 files / 78,009,188 bytes |

Every remaining hash and partition matches the later inventory, and actual lengths stay within its declared caps. Header caps are 65,536 bytes, distinct from actual header lengths; waveform caps are 1,950,000. The initial outcome records no partial files, extra files or symlinks, with structural header checking and numerical/scientific stages not reached. These are saved metadata statements, not a fresh disk scan.

An incomplete transport status does not imply no effect or that its complete retained files are invalid. The later recovery preserves the original outcome and records a separate continuation rather than relabeling the timeout as success. The initial pending-resumption field retains its capture-time meaning; later continuation evidence does not renew historical authorization now.

For Continuum, keep attempt outcome and individual artifact state separate. Recovery can reconcile a verified complete subset and its exact complement without pretending the original attempt completed or blindly repeating all effects.

## Resource and custody limits

The receipt records termination requested at 1,700.000182 seconds, final elapsed time 1,700.050689 seconds and about 0.050507 seconds of cleanup. Final wait4 CPU is 2.196582 seconds, versus a conservative sampled maximum of 2.200881, across 33,526 monitor samples. The root exits by SIGKILL, with no reported violations or remaining descendants. Wall and CPU quantities have different meanings; their large difference does not identify the network, server, scheduler or application bottleneck. No transport performance or failure-cause claim is made.

The acquisition outcome declares six envelope artifact digests. This unit acquires and binds the terminal receipt; invocation, effective-state, journal and stream payloads remain outside this acquisition unit. The large accounting log is not implied read by the terminal counter. Input waveform/header contents and the publisher manifest were not fetched. No acquisition, audit, numerical program, signal decode, output rehash or model call was repeated. The [validation record](../../research/runs/base12-persistence-acquisition/validation.json) separates all actual checks from historical observations.

Cumulative semantic reading reaches **337 distinct blobs / 2,352,394 bytes**, plus **51 byte-identical alias paths**: 388 covered paths. **5,205 paths / 4,092 distinct blobs** remain without full semantic-reading claims. Earlier empty-stream custody stays mechanical. The historical global acquisition aggregate remains unchanged because its full overlap index is unavailable. No private raw source, receipt, operational identifier or signal payload is published. Hosted CI checks public repository behavior, not private reading or historical execution.

Next bounded unit: the four documentation snapshots referenced by closeout, 38,171 bytes. Bind their declared hashes and inspect how documentation-continuity instructions, current state, learning ledger and preservation guidance relate to the exact experiment and later review. Treat all historical instructions as source material, preserving current ownership and authority. Reconcile main first; no recipient has accepted it. Owned-storage and dispatch-reconciliation work remain separate.
