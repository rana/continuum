# ADR 0002: research an owned storage kernel and an independent native verifier

Status: accepted research direction; no storage replacement adopted

Date: 2026-10-19 UTC / 2026-10-18 America/Los_Angeles

Source baseline: `d126337d22c3a181d72ef559d2c84a436d9aec19`

## Question and intent

The user's native-stack direction asks for control over the important mechanisms of continuing AI work, not merely a preferred implementation language. A comparison among existing databases leaves out a real alternative: designing a much narrower engine around exact objects, conditional acceptance, historical receipts and recovery.

The [existing storage survey](../experiments/embedded-storage-evaluation.md) found only three authoritative tables and a small SQL surface. That supports a bounded architecture experiment. It does not establish a smaller, faster or more reliable replacement.

## Decision

Open a purpose-built storage research track now. Its purpose is to discover whether a smaller supported state space, explicit persistence protocol and reconstructible indexes improve control, reviewability, resource use or useful continuation. A demonstrated performance bottleneck is not a prerequisite for this bounded research question.

Keep the implemented SQLite path as a retained behavioral and measurement baseline. The active checkpoint/receiver work continues under CURRENT.md and its existing ownership. This decision supplies an independent research unit; it does not claim that a worker has accepted or started that unit.

Separate two experiments:

1. **Own the domain storage mechanism.** Specify and model a journal containing immutable object insertions and complete acceptance outcomes. A transparent Rust reference can own the format, transactions, allocation choices and recovery rules without a third-party database.
2. **Own a bounded emitted target.** Once an immutable record/checking contract is stable, independently implement a read-only verifier through a disclosed native emitter and target ABI. Compare it with the reference using exact positive and negative inputs. The first emitted target does not own live mutable storage.

Ordinary Rust code generation and fully owned emission remain different boundaries. Rust is the starting reference language, not a permanent requirement imposed on a successful future target. Owning an emitter does not automatically remove kernel, filesystem, device, firmware, integrity-library or bootstrap assumptions. No Base12 migration or private-source import is selected.

## Non-negotiable comparison contract

Preserve exact canonical object identities, candidate/type checks, root-and-generation preconditions, exact historical retries, changed-request reuse rejection, durable accepted and stale outcomes, and the existing explicit global acceptance sequence. Object insertions and exact retries must not allocate acceptance events. A byte offset or generic journal-record ordinal is not that sequence.

A single writer is an explicit architecture option, not the disappearance of coordination. If clients go through IPC, include ownership discovery, takeover, startup and service costs. Keep immutable objects and acceptance outcomes in one persistence domain for the first candidate.

Durable acknowledgement follows the completed barrier covering the operation. Recovery may legitimately restore a committed operation whose reply was lost. The external test oracle can know submission and delivery history; the recovery algorithm cannot use that knowledge as an extra input.

A checksum cannot always distinguish a torn unfinished append from damaged acknowledged data. Protected commit-boundary selection, rollback/missing-marker behavior and ambiguous images are part of the experiment. A synced marker alone is not a completed solution. Fail closed when integrity cannot be established; count those refusals as an operability cost, not as successful recovery.

## First bounded unit

Develop a pure acceptance oracle and framed-record recovery model before entrusting a new engine with retained work. Keep the unit isolated from production paths and current pilot changes. Declare finite object/operation/target/history bounds, fault alphabet, enumeration or pruning rules, actual counts and exact failing traces.

Include successful and stale outcomes, ABA generations, changed-operation reuse, retries after later head movement, commit-before-lost-reply, partial writes, completed versus failed barriers, reordered/subset persistence in the declared model, malformed lengths, corrupt records and missing or damaged commit metadata. Preserve preconditions and intact object dependencies.

A pass requires legal all-or-nothing recovered transitions, preservation of acknowledged outcomes under the stated crash model, unchanged historical receipts for recovered operations, and no invented requests or mixed request identities. Under modeled corruption, an explicit integrity refusal is acceptable where reconstruction is not established; it must never be relabeled clean recovery. Report safety and availability separately. A model that rejects every image does not satisfy useful availability requirements.

Use an independently formulated oracle and deliberate mutants. Retain one minimal counterexample for each discovered defect. Pure model execution is not filesystem execution or physical power-loss validation. No model has been executed by this decision.

## Follow-on and adoption

The [full design](../experiments/owned-native-core-design.md) describes a shadow file journal, real process/I/O faults, the emitted-verifier experiment, lifecycle requirements and comparative measurements. Preserve SQLite results unchanged and compare any tuned SQLite successor separately. Investigate the current open-time writer reservation and hashing scope without assuming a safe fix or diagnosed bottleneck.

Adoption requires a concrete worthwhile benefit with preserved semantics and acceptable backup, restore, upgrade, growth and recovery behavior. Reopen or stop a candidate when its correctness model remains ambiguous, its state space becomes less legible, benefits come from an unacknowledged topology/durability change, or total implementation and maintenance costs outweigh useful gains. A negative result is a completed research contribution.

## Collaboration and evidence

Actual Claude exchanges [9](../collaboration/2026-10-19-claude-09.md), [10](../collaboration/2026-10-19-claude-10.md) and [11](../collaboration/2026-10-19-claude-11.md) support exploring custom storage while exposing consequential mistakes in proposed recovery criteria. Their exact visible responses and the [corrections](../collaboration/README.md#owned-native-design-corrections) remain separate. Model agreement is not verification.

The [cross-project request](../collaboration/native-ownership-bridge.md) records the Dot route and actual delivery state. Public method adaptations remain separate from private Base12 operational records. The operational decision in [ADR 0001](0001-native-core.md) remains in force until an evaluated replacement is adopted.

## Conditional repository transition

The user proposes a fresh reader-facing home if a fully owned target is adopted, potentially renaming the predecessor and retaining Continuum for the successor. This remains conditional. The [fresh-reader and transition design](../experiments/owned-native-core-design.md#11-a-fresh-reader-and-a-conditional-successor-repository) preserves current contracts at the front door, pinned historical evidence, exact repository identity, actual worker acknowledgements and concrete integration updates. Name reuse must account for GitHub redirect behavior and active research/Codex/Dot writers. No current repository, worker schedule or remote was changed by this consideration.
