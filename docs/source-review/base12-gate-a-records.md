# Gate-A records: inspect how the saved result was constructed

Reviewed 2026-10-19 UTC at private Base12 commit `88382e793b65c84fd8e223840c27f6bb8682864a`, tree `5cf96129bdcb0dde075f6f5800ae0c68a95c4b82`. Five texts / 36,830 bytes were fully read: RESULT, preservation manifest, saved-execution auditor, freeze and retained identities. Every matrix/fault/result field and every manifest/freeze entry was read directly. The auditor was syntax/AST inspected without import or execution. Exact identities are in the [ledger](base12-coverage-gate-a-records.json); comparisons and limits are in the [validation record](../../research/runs/base12-gate-a-records/validation.json). No decoder, raw signal, executable or trace buffer was acquired or run.

## Research Delta: retain the derivation of an actual-exit field

RESULT has 65 unique matrix cases: 36 expected/actual exit-zero rows and 29 exit-two rows, all with staging absent. Twelve unique fault rows divide into six EINTR exit-zero and six hard-I/O exit-three results. Their saved injected-result strings contain injection markers; successful rows identify the six expected syscall names and a subsequent nonnegative return. The two driver-dependent collision/retained completions bring 77 explicit rows to the declared 79 invocations. Retained file sizes/hashes agree with the separate three-item identity record. Decimal timing and reported user/system CPU arithmetic reconcile with the [claim review](base12-gate-a-claims.md).

The auditor reveals how these fields are constructed. For matrix entries, it reads expected values from the fixture TSV, requires corresponding expected/actual success text to occur in the saved log, checks output names/types/hashes or destination absence, then assigns the expected value into its summary's `actual_exit`. Fault rows similarly derive expected status from the case name and require matching log text, one injected marker and an expected terminal trace exit. This is a saved-file assertion pipeline with explicit dependencies, not independent parsing of a complete execution census. Current reading does not reopen the historical outputs or traces.

A typed receipt should preserve that derivation: expected value, matching log evidence, filesystem checks and reconstructed summary field answer related but different questions. This source pattern does not establish a historical false result; it describes the actual predicates behind the saved pass.

## Research Delta: syscall name alone does not identify a retry operation

The auditor finds the next trace line beginning with the same syscall name after an injection and checks a nonnegative return for the six EINTR cases. It does not itself compare all descriptors, paths, buffer arguments or counts. The separate delegated prose review reports additional argument checks; those retain their own review scope rather than being silently attributed to this script.

The hard close-error row also records a later same-named close returning zero. That alone does not show a forbidden retry of the same descriptor: it could be another close during cleanup. No such violation is inferred. Preserve call identity and argument evidence when the claim concerns a retry of a particular operation, rather than only another call of that name. Full traces remain unacquired here.

The auditor hashes saved decoded outputs, compares successful fault outputs with a baseline, parses traces and writes RESULT.json. Its source has no apparent child-launch path or research import. Thus it can avoid native re-execution while still reading payload bytes and creating a new summary. We did neither operation; only its source was parsed. It also relies on a trusted original private path layout and ordinary report writing, not a newly demonstrated durable publication transaction.

## Research Delta: separate a preservation inventory from held payloads

The preservation manifest lists 22 allowlisted receipt copies. Its RESULT and auditor entries now match acquired bytes; the other twenty remain declared payload identities until the next unit. The independent review binds separately by size/hash. All listed lengths match pinned tree metadata, which does not substitute for payload hashing.

The freeze file's own digest matches the earlier clearance and review. Its ten entries contain nine distinct digest values, including two manifest paths sharing one digest. Only the already held immutable seed bytes are bound as a freeze input in this unit. The ELF, emitter, launcher, driver, fixture source/manifest and private TSV inputs are not newly acquired. Retained archive/header/waveform hashes remain declarations, not fresh signal custody or repeated comparisons.

Cumulative semantic reading reaches **406 distinct blobs / 3,246,056 bytes**, plus **52 byte-identical alias paths**: 458 covered paths. **5,135 paths / 4,023 distinct blobs** remain without full semantic-reading claims. The historical global acquisition aggregate stays unchanged. No private raw source, receipt buffers, operational identifiers or signal/executable bytes are published. No historical instruction, native run, new model invocation or authority activation occurred. Hosted CI checks public repository behavior, not the saved execution.

Next bounded unit: the twenty remaining allowlisted receipt copies, **10,669 bytes**: nineteen nonempty texts and one empty stream for mechanical custody only. Bind the preservation manifest completely, compare verdict/resource/control summaries and retain snapshot/driver dependencies without acquiring output or trace buffers. Reconcile main and ownership first; no recipient has accepted it. Continuum's owned-storage and dispatch-reconciliation lanes remain separate.
