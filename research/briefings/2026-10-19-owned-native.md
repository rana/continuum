# Progress Brief: Continuum owned-native research

Date: 2026-10-19 UTC / 2026-10-18 America/Los_Angeles. Evidence cutoff: this design review, with source reconciled through `4fc43550866a2794c1bdd492a4b1a79b0883faa4` before final publication. This is a dated projection; [CURRENT.md](../../CURRENT.md) owns the live next action.

## Judgment

The coordinator favors pursuing a purpose-built Continuum storage kernel now as a bounded research direction. The user's additions sharpen the same objective: own important mechanisms, make the system legible to fresh readers, and enable learning across projects. The stronger claim that a fully owned emitted stack will be faster, smaller and more reliable remains unestablished.

[ADR 0002](../../docs/decisions/0002-owned-storage-research.md) accepts the research direction. It does not replace the working Rust/SQLite baseline or claim that a new implementation exists. The [full design](../../docs/experiments/owned-native-core-design.md) describes the architecture, failure model, phases, conditional successor repository and shared-component options.

## Actual progress

- Read the current storage contract and reconciled newer public Codex work without changing the native implementation or its dependencies.
- Developed a concrete append-only authority with object-insertion and complete acceptance-outcome records, reconstructible indexes and explicit recovery obligations.
- Completed five actual Claude Opus 5.5 exchanges with supplied user wording, source summaries and corrections. Two additional reviewers examined architecture and durability. Their agreement is not an executed correctness result.
- Preserved a consequential counterexample to an incorrect model-review criterion: commit can succeed before a reply is lost, so an unacknowledged operation may correctly reappear during recovery.
- Defined a finite state/recovery-model experiment followed by a disposable file journal and optional independently emitted read-only verifier.
- Recorded a conditional fresh-reader repository structure, possible Continuum/continuum-prototype naming, actual worker acknowledgements and integration updates before future name reuse.
- Published and verified the exact Dot request through [private Base12 PR128](https://github.com/rana/base-12-ai/pull/128). A subsequent response confirms that the Base12 Codex chat actually read the immutable request and supplied an independent documentation/design response. This is distinct from Dot receipt or acceptance; no Dot-authored reply has been observed. Only the independently stated generic lessons enter the public [bridge record](../../docs/collaboration/native-ownership-bridge.md).

No owned storage engine, recovery simulation or emitted verifier was implemented or executed in this unit. No comparative benchmark, private-code transfer, repository rename or scheduler change was performed. The new output is a checked design, a durable collaboration request and a separately verified Base12 Codex response.

## What changed in understanding

The earlier question was which existing engine to embed. The expanded question is whether Continuum's small authoritative operation set admits a simpler purpose-built storage mechanism. That is worth investigating for control and comprehension even before profiling demonstrates a bottleneck.

Rust can implement that mechanism while owning its format, algorithms and resource policies. Owning instruction emission, ABI and bootstrap adds a different capability. The plan preserves both possibilities instead of treating ordinary Rust and fully owned emission as interchangeable.

Some general-purpose machinery could disappear: unrelated SQL and schema operations, unnecessary indexes and configurable transaction modes. Persistence ordering, conflicting changes, unknown replies, corruption and resource exhaustion remain. One writer centralizes coordination; it does not abolish it.

## Balance and remaining evidence

The strongest opportunity is a small core whose supported states and recovery behavior can be understood and challenged across models. The strongest counterweight is that storage complexity concentrates in failure handling, lifecycle and long histories. A concise fast-path implementation can still be an unreliable database.

The critical unresolved questions are whether recovery can preserve acknowledged history or clearly refuse ambiguous corruption, whether journal/index growth remains controlled, whether a service topology helps the actual clients, and whether emitted ownership adds value beyond the same custom architecture in Rust.

Base12 contributes methods for exact custody, narrow emitted stages and independent checking. Continuum can contribute durable operation reconciliation and precise research handoffs. Shared specifications, corpora, host tools, deliberate source copies or small libraries are all possible when their contracts and provenance match. No common runtime or code transfer has been selected.

## Next horizon

Immediate owned-storage unit: build a pure acceptance oracle and finite framed-record recovery model with declared bounds, exact traces and deliberate mutants. Test legal acceptance, stale rejection, changed identity reuse, generations, historical retry and interrupted acknowledgement. Keep submission/delivery ground truth in the external test harness, not as a hidden recovery input. Report corruption refusals separately from successful recovery.

Next: implement a disposable filesystem journal behind the same public operations and test actual process/I/O boundaries. Then use a stable read-only verification contract as a candidate for independent native emission. Compare useful end-to-end work and lifecycle costs before adopting a replacement.

The practical Codex pilot remains under its current owner and CURRENT.md. This brief does not create a timer, reserve a workstation or establish live utilization. No machine-capacity conclusion is drawn from recent commits or task labels.
