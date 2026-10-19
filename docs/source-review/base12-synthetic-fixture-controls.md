# Synthetic and fixture controls: preserve the scope of a pass

Reviewed 2026-10-19 UTC at private Base12 commit `88382e793b65c84fd8e223840c27f6bb8682864a`, tree `5cf96129bdcb0dde075f6f5800ae0c68a95c4b82`. Ten texts / 6,703 bytes were fully read: pre-synthetic gate, verification, five synthetic envelope records and three remaining transport-fixture control records. Exact identities are in the [ledger](base12-coverage-synthetic-fixture-controls.json); bindings and arithmetic are in the [validation record](../../research/runs/base12-synthetic-fixture-controls/validation.json). Neither suite nor upstream source was executed.

## Research Delta: bind a test pass to its actual representations

The synthetic verification's five artifact digests match the acquired checker result, envelope receipt, invocation, effective controls and envelope-selfcheck summary. The checker result's three source digests match acquired codec, native generator and checker bytes. Its category sum is **2,052 assertions**, with **84 native identities** and **84 mapping checks**, matching the verification. These are saved assertions and variants, not 2,052 independent empirical replications or a general correctness guarantee. Earlier [learning-audit analysis](base12-learning-audit.md) preserves the distinction between the synthetic variants and forty scored encoder variants.

Stdout is the exact rounded projection: 2,052 assertions and 0.705 seconds. The checker retains **0.7053347320002104 seconds** internally; the outer envelope records **0.8119005800003833 wall seconds** and **0.770254 wait4 CPU seconds**. Their elapsed difference, **0.10656584800017299 seconds**, is not an isolated measurement of startup or cleanup overhead. Effective controls and terminal embedded limits equal their separate payloads.

The synthetic profile has a 300-second wall ceiling, 120-second CPU backstop and 120-second aggregate early stop. The fixture profile instead has 60, 30 and 25 seconds respectively; its previously read receipt binds to the local fixture gate. Both show clean root exits and completed cleanup under their own profiles. A profile name or successful fixture result does not make those control budgets interchangeable with acquisition, recovery or the full scientific run.

## Research Delta: process counts and sample counts are scoped observations

Synthetic monitoring declares sixteen samples; the fixture declares four. Each journal has one early row with zero own/reaped ticks and no descendants. Both rows' identities match effective controls and terminal root records, but they do not reconstruct final CPU or the unlogged monitor observations. The [sparse-history qualification](base12-recovery-intake-accounting.md) applies to short successful checks as well as long transfers.

Both recorded root PIDs have numeric value three, while start identities and commands differ. Numeric PID equality alone does not join attempts or establish a shared host/namespace. No process continuation or PID recycling event is inferred from these records.

The synthetic result's native variants are in-process generated-code checks in the already read source. No sampled descendants does not imply that no generated machine code executed: child-process monitoring and in-process execution are different boundaries. No native program, fixture or network operation was replayed here.

## Research Delta: historical gates do not describe the current workstation

The pre-gate declares fourteen changed sources rehashed, selfchecks passed, data empty and research execution not yet begun. Its wrapper identity binds acquired source, and its Zstd digest agrees with the saved static declaration; the executable payload was not acquired. Recorded remote revisions remain historical observations, not fresh remote queries performed by this review.

The later synthetic-only record still holds waveform acquisition and the full runner. Its invocation count of one is authored scope for that preserved attempt, not host-wide exactly-once evidence. Empty-directory, source-unchanged and original-archive fields are stage-specific claims. They do not renew historical authority, prove current filesystem state or contradict later separately recorded work merely because later status differs. Continuum should keep a gate's revision, exposure, control profile and stage attached when reusing its pass.

Cumulative semantic reading reaches **384 distinct blobs / 3,118,427 bytes**, plus **52 byte-identical alias paths**: 436 covered paths. **5,157 paths / 4,045 distinct blobs** remain without full semantic-reading claims. Archive custody and empty streams remain mechanical; the historical global acquisition aggregate stays unchanged. No private raw source/receipt bytes, operational identifiers or signal payloads are published. Hosted CI checks the public repository, not these historical suites.

Next bounded review: nine historical packet notes, **55,656 bytes**. Read launch plans, readiness, acquisition/audit notes and envelope design in full, distinguishing superseded plans from later source/receipt evidence without activating their instructions. Reconcile main and ownership first; no recipient has accepted it. Owned-storage and dispatch-reconciliation work remain separate.
