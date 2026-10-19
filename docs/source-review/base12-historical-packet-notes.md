# Historical packet notes: attribute qualifications and retain plan versions

Reviewed 2026-10-19 UTC at private Base12 commit `88382e793b65c84fd8e223840c27f6bb8682864a`, tree `5cf96129bdcb0dde075f6f5800ae0c68a95c4b82`. Nine historical notes / 55,656 bytes were fully read: preparedness, envelope design, synthetic launch/result, acquisition result, transport proposal, full-run launch and two audit plans. Exact identities are in the [ledger](base12-coverage-historical-packet-notes.json); comparisons and arithmetic are in the [validation record](../../research/runs/base12-historical-packet-notes/validation.json). Historical commands were treated as text and never executed.

## Research Delta: preserve who already knew a limitation

The original post-acquisition plan explicitly distinguishes required-file verification from directory-wide absence. It requires a separate inventory for extra/test/annotation/symlink claims and says a console count or completed intake cannot override an incomplete wrapper. The recent [intake review](base12-recovery-intake-accounting.md) confirms the source boundary; this reading establishes that the boundary was already recognized in the authored audit plan. It is not a newly discovered historical oversight.

Likewise, the saved-result checklist already distinguishes validation-byte integrity/header reads before freeze from numerical validation afterward. It favors source order and bound payload identities over timestamps, qualifies greedy selection rather than claiming global optimality, and keeps shared encoding work separate from per-arm speed. Missing decoder identities and Zstd decode timing are explicit. Earlier source/receipt returns provide additional checks; they do not own the original qualifications or turn agreement into independent experimental replication.

The checklist's finite arithmetic agrees with separate recalculation: 256 training contexts, 10,240 predictor calls, 41,943,040 candidate sample evaluations over 1,048,576 distinct context positions; 2,544 validation blocks, 101,760 calls and 416,000,000 candidate sample evaluations; 5,167,240 overlap starts. Framing bounds of 1,027 bytes per raw record, 8,227 global raw overhead without dictionary, 594 literal overhead, and the 31-byte full-versus-four-member-learned inclusion bound reconcile. These are accounting/source invariants already stated by the author, not fresh waveform evaluation or evidence of learning superiority. The declared 23,985-byte common decoder source total also matches pinned file sizes.

## Research Delta: a proposal is a retained alternative, not the final contract

Early transport and watchdog examples differ from the later source and receipt profiles:

| Setting | Historical proposal/example | Later adopted profile |
| --- | ---: | ---: |
| Transport header cap | 65,536 bytes | 16,384 bytes |
| Transport operation timeout | 60 seconds | 30 seconds |
| Watchdog poll interval | 100 ms | 50 ms |
| Full-run aggregate early stop | 1,790-second example | 1,660 seconds |

The final transport gate also uses tighter CPU limits than the early proposal. These differences preserve design evolution; an old proposal is not an implemented promise or evidence of an unauthorized change. The proposed absolute file deadline must also be read alongside the final helper's explicit cooperative checks and external wall envelope.

Envelope design retains unadopted per-process allocation and isolated-cgroup options. Its nominal arithmetic, four allocations of 440 seconds giving 1,760 and 60% over 2,700 seconds giving 1,620, agrees. The note itself explains why those figures do not establish an unconditional kernel/manager-failure lifetime bound. No alternative was applied, facility tested or security/service setting changed here. Historical unavailable objects and an incompletely addressed bus request remain different from approval denial.

## Research Delta: bind prospective launch text without promoting it to execution

The synthetic and full-run shell blocks were tokenized as data. Their worker argument lists, CPU/wall/early-stop values and descendant settings equal the saved invocations. This binds the prospective command descriptions to later records; only those later receipts support execution claims.

Ten preparedness source hashes match acquired payloads, and its static-preflight digest binds. Seven artifact hashes in synthetic/acquisition summaries match acquired results and receipts. The notes preserve distinct preparation-held, synthetic-only, incomplete-acquisition and conditional-full-launch stages. Claims that a helper was not yet implemented or a runner had not started describe those stages, not the current pinned tree. Original-archive unavailability is retained without substituting the later review ZIP. No historical permission was activated and no current remote/platform state was inferred from the notes.

Cumulative semantic reading reaches **393 distinct blobs / 3,174,083 bytes**, plus **52 byte-identical alias paths**: 445 covered paths. **5,148 paths / 4,036 distinct blobs** remain without full semantic-reading claims. Archive custody and empty streams remain mechanical; the historical acquisition aggregate stays unchanged. No private raw source/receipt bytes, operational identifiers or signal payloads are published. No model, numerical code, acquisition or historical launch ran. Hosted CI checks the public repository, not historical execution.

Next bounded review: documentation read receipt, reconciliation proposal and official-license receipt, **three texts / 6,502 bytes**. Bind their declared sources and claims, attribute proposal/approval scope, then reconcile remaining packet semantic coverage without promoting inventories or license declarations into fresh authority. Reconcile main and ownership first; no recipient has accepted it. Owned-storage and dispatch-reconciliation work remain separate.
