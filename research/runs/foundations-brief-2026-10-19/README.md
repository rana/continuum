# Progress brief and foundations review — 2026-10-19

## Research Delta and evidence cutoff

Rana requested a candid progress brief, an assessment of whether Continuum is well considered and should exist, an explanation of native-stack versus Rust decisions, imaginative alternatives, and actual Claude collaboration. Rana also reiterated availability to grant GitHub authorization. Existing authority suffices for this scoped public research record; platform capability and successful publication remain separate observations.

Owner: the current Chat research coordinator, for this assessment and its publication only. Initial source: public main `96d63a033b60b8b043ba824f11bb81150f801695`, merged 2026-10-19 14:36:53 UTC / 07:36:53 America/Los_Angeles. Late reconciliation: `2506de176425baf21f7613049312909c7151f5ce`, merged 14:46:55 UTC / 07:46:55 Pacific. The four-commit comparison adds two source-review units and their status/coverage; it does not change runtime code or the native ADRs. This contribution is based on the latter tree. It does not supersede CURRENT.md or take another worker's implementation lane.

Fresh reads included AGENTS.md, CURRENT.md and its later next-unit section, the continuation method, progress-brief protocol, MISSION.md, native architecture, ADRs 0001/0002, the owned-native design, real-use pilot plan, read-only-store and bounded-receipt-view Research Deltas, Cargo.toml, and the public native-ownership collaboration bridge. Earlier pilot records are also available in this conversation's verified repository reads. Not every historical run or every source file was reviewed for this brief.

Original work in this unit is a synthesis and an improved comparative experiment design, with two actual Claude consultations. No Rust/Python test suite, native binary, custom engine, provider retry or new recipient experiment was run for this brief. PR #100's exact head `9b4d503f66a39f379a0fd0458cbe873cf115a274` has a separately verified successful PR workflow, run `39270352195`; this does not validate this assessment's opinions. The open-PR query at initial recovery returned none, not evidence of worker inactivity. Branch names likewise do not prove implementation or acceptance.

## Judgment

Continuum has a well-considered small correctness foundation and an empirically immature usefulness claim. The real-use chain produced meaningful implementation improvements: reproducible checkpoint custody, historical-attempt transport, scoped receipt retrieval, correct live backup/export, and read-only access under a writer reservation. These are more valuable than commit or synthetic-case counts.

The central unproved proposition is whether using these mechanisms improves real continuation enough to exceed good GitHub source plus concise, disciplined notes, including preparation, retrieval, integration and maintenance cost. Existing pilots support feasibility and specific useful actions, not a causal comparison or ongoing adoption. A functioning local engine is not an installed autonomous worker.

Continue the research, but shorten the loop between a consequential question, real use, a measured decision and an integrated result. Broad authorized source review remains legitimate and incomplete; it should not silently substitute for product evaluation or become a prerequisite to the next use experiment. The large chronological CURRENT section and branch/attachment-only evidence are themselves concrete interface and integration frictions to examine, not reasons to add another dashboard.

## What is decided about the stack

[ADR 0001](../../../docs/decisions/0001-native-core.md) retains the compiled Rust library/CLI, SQLite and established hashing as the operational baseline. [ADR 0002](../../../docs/decisions/0002-owned-storage-research.md) separately accepts owned-storage and independently emitted-verifier research. It does not adopt a replacement.

Native execution, semantic ownership, storage ownership, userspace dependencies and instruction emission are different axes. Rust can implement a purpose-built journal and own its transaction/recovery format without SQLite. That would still normally use the Rust compiler and its backend. Owning an emitter adds instruction/ABI/bootstrap obligations; it does not mean owning the kernel, filesystem, device or every dependency. No such replacement, migration or successor repository is established by this review.

The two inspected owned-recovery/journal branch heads were existing earlier main merge commits, not evidence of a completed storage implementation. This is a bounded observation, not a claim that private or local uncommitted work cannot exist.

Preserve the reference implementation and exact behavioral contract. Investigate the finite journal/recovery oracle as authorized. A small independently implemented read-only verifier is an attractive parallel ownership target, but a second language or emitter alone does not establish independent assurance: specification, fixtures, encoder and oracle assumptions may still be shared. Keep the shadow candidate away from retained authoritative stores until its own recovery/lifecycle evidence earns adoption. A measured speed bottleneck is not required to investigate architectural control; claimed control and reviewability benefits still need discriminating evidence.

## Three hypotheses, not one moving goalpost

1. Product usefulness: does the workflow improve correct resumption, evidence reuse or effort relative to simpler alternatives?
2. Mechanism correctness: do identities, acceptance, historical receipts, and recovery satisfy their explicit contract under stated faults?
3. Ownership/reviewability: does a narrower owned mechanism improve comprehension, supported targets, dependency control, predictable resources or lifecycle behavior enough to justify its burden?

A result can support one and not another. Do not label good mechanisms as demonstrated product value, or treat a poor handoff comparison as disproving every ownership research objective. Conversely, research interest cannot excuse indefinite activity without a specified artifact or falsifiable finding.

## Next proposed experiment: three-arm real-work continuation

Status: designed here, not executed or assigned to an external worker. Use genuine Continuum-development recovery/review/integration episodes rather than another CSV feature. Include an independent public task family when it adds a distinct use pattern. Use isolated frozen copies; any seeded perturbation is experimental, not a rewrite of historical evidence.

- A: the best concise GitHub/Markdown handoff.
- B: explicit claims, evidence scope, omissions and corrections conveyed as ordinary files, without native verification.
- C: corresponding structured context with native checks and bounded evidence retrieval.

B separates the value of structure from enforcement. Evaluate both causal interface ablations and end-to-end production cost: do not secretly credit B with free preparation by C, or handicap A with bad notes. All arms receive equal access to underlying authoritative evidence and current source; identify exact differences in provided material. Source presence, model, tools and context volume must not silently confound storage value.

Predeclare task-specific acceptable actions using evidence independent of Continuum's own verdicts. Sample content drift, semantic changes with unchanged bytes, missing corrections, uncertain attempts, and no-change controls. Do not tell the receiver whether to retry or hold. Blind the evaluator where feasible; do not claim receivers are blind to their interface. Use fresh independent contexts, matched actual model/settings and randomized/counterbalanced assignment. A few episodes are a qualitative screen, not proof of general efficacy; preregister a larger design before statistical claims.

Measure correct next action, unsafe repetition, unsupported inference, missed corrections, unnecessary holds/rework, retrieval and total author/receiver/integration effort. Record token use and actual timing without inventing billing. Score productive progress as well as conservative refusals. Use a sampled or explicitly varied drift prevalence rather than a hidden test mix that rewards blanket holding.

Important boundary: native current-anchor verification observes an accepted local store. It is not automatic remote-Git freshness, evidence truth, completeness, or current worker ownership. Every arm must be able to inspect the appropriate actual authority. An experiment that defines all truth by the C arm's checks is circular.

A plausible outcome is that structured ordinary records capture most value. In that case simplify the default integration and retain native checks where their particular guarantees matter. A custom database should not receive causal credit from a context-presentation improvement. No universal numeric adoption threshold is declared from this small assessment.

## Promising bounded directions

**Evidence-scoped continuation.** Help a successor distinguish what remains intact, what is currently applicable, what was merely asserted, what changed, and what can usefully proceed. These are supported claims with scope, not permission grants or a proof of truth. Statistical confidence calibration would require predictions and observed outcomes beyond the current pilot.

**Dependency-scoped review notices.** Follow only explicit citations when a record is corrected or superseded. Produce advisory review candidates with original reasons and evidence. Never infer that unlisted dependencies are absent, automatically invalidate a still-valid old observation, or automatically cancel another worker. Test missed and spurious notices on a corpus containing unaffected controls.

**Smallest sufficient decision context.** Experiment with removing records and observing whether a specified decision changes, while separately recording omitted known content. Hash identity cannot establish semantic sufficiency. Useful selection may depend on task and model.

**Portable counterexamples and conformance fixtures.** Preserve exact failures and independently authored oracles so another storage backend or emitted target can be assessed without inheriting every implementation choice. Successful shared-code agreement is weaker than deliberate fault discrimination.

**Localized uncertainty rather than global paralysis.** Hold an uncertain external effect while continuing independent analysis, verification and reconciliation. No local receipt gives an external provider a guarantee it does not actually implement. Repeated synthetic dispatch edge cases should now converge into a bounded contract and conformance corpus rather than endlessly expanding the same family without integration.

## Actual Claude collaboration and corrections

Two calls completed with actual `claude-opus-5-5`, configured medium effort, adaptive thinking, text-only exposure, no server memory, `end_turn`, and no truncation. Exact request fields, visible responses and returned metadata are preserved in `claude-exchanges.json`. Call one reports 2,510 input / 3,001 output tokens; call two 2,172 / 3,784. These are reported usage, not cost or independent empirical evidence. The second call replayed selected prior conclusions through its explicit context, not shared model memory.

Claude's independent assessment praised scoped engineering and challenged the lack of a best-notes control. It favored an independently emitted verifier over a custom writable journal and proposed evidence-scope transfer. Its first answer conflated lost acknowledgement with lost read-snapshot state and attributed useful custody review to the pack too strongly. The second request corrected those points; Claude explicitly accepted both corrections and withdrew the overly broad claim that a notes-equivalent result leaves every ownership experiment without a customer.

We converge on separate hypotheses and the need to measure authoring cost. We do not adopt every suggestion. Claude's proposed mandatory schema-change milestone before journal work, fixed iteration cutoffs, and mutant-kill superiority as a sole verifier retention rule are not new project gates. A verifier can be valuable for auditability or target independence without defeating a reference on one finite corpus. A traceable negative finding can be useful without producing a new implementation. "Entitlement" language is replaced with evidence scope to avoid confusing an epistemic judgment with authorization.

Source-verification correction: the second request described external primary documentation as already checked. In this brief's visible sequence, fresh external web verification followed the two model turns. The later reads confirmed the limited compiler/no_std/WAL statements, but cannot retroactively change what had been verified when that request was made. The original request remains exact.

## Continuation and limits

This Chat coordinator owns publishing this assessment and retaining the exact consultation. Proposed next ownership: the next active implementation owner, after fresh remote and actual worker reconciliation, prepares one three-arm real-work packet and its independent action rubric; no recipient acceptance or task dispatch is claimed. This recommendation is not a rewrite of the current source-review owner's selected unit, a new scheduler, or a storage adoption decision.

Keep learning from real use. Be willing to retain only the portable contract, evidence format or a few useful primitives if those are what earn their cost. The mission is continuing useful work; perpetuating a particular engine is not the mission.

## Primary external references verified for this brief

- Rust Compiler Development Guide, Code generation: https://rustc-dev-guide.rust-lang.org/backend/codegen.html — usual LLVM backend and alternative backend boundary.
- Rust Reference, Preludes/no_std: https://doc.rust-lang.org/reference/names/preludes.html — no automatic std linkage is not universal dependency freedom.
- SQLite WAL: https://www.sqlite.org/wal.html — reader snapshots, concurrent readers/writer, single writer and WAL custody boundary.

These establish documented mechanisms, not comparative Continuum performance or physical durability. No private Base12/Prime Radiant payload, new provider credential, workstation installation, live utilization or model-setting change is included or claimed.
