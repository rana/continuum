# Lessons from Base12 and Prime Radiant

Continuum should preserve a research process as carefully as it preserves source bytes. An experiment can be correctly executed and answer the wrong question. A concise status page can describe current files accurately and omit the pending operation that determines what is safe to do next. A promising idea can deserve preservation before anyone knows how to test it.

This document records original, generic design adaptations from inspected project sources. It distinguishes the source encounter, our interpretation, and the resulting design choice. It does not import either project's scientific claims, operational permissions, private conversations, or source archive into this public MIT repository. These lessons are design reasons, not a claim that every proposed Continuum capability is implemented.

## Source encounter and coverage

### Base12

The source repository was inspected at commit `88382e793b65c84fd8e223840c27f6bb8682864a`. The protocol adaptation read the complete pinned `REPORT.md`, `AGENTS.md`, `RECORD.md`, `MERGE_POLICY.md`, `DOT_BRIDGE.md`, `research/automation/COORDINATOR.md`, `research/automation/COORDINATION.md`, and `collaboration/prime-radiant/2026-10-18-repository-design.md`. Current-state and queue material was also consulted; a current-state summary was not treated as proof that every linked execution artifact had been reviewed.

The complete recursive tree inventory found 5,593 file paths, 4,429 distinct Git blobs, 180,332,790 bytes, and 1,164 repeated blob occurrences. The checkpoint acquired and hash verified 477 local files representing 476 distinct blobs. Across the reviewers, 88 files representing 88 distinct blobs received complete semantic reading, totaling 876,422 bytes; a further 35 paths contain identical blobs and are recorded as aliases rather than additional reads. The review covered governance, research navigation and preservation, the transparent reference core and tests, experiment protocols and results, and selected compiler, assembler, bootstrap and runtime sources. The transfer, constructed operator witness, cached operator restart, and validation-risk lane accounts for eight protocol/result documents and eleven implementation/verifier Python files, totaling 281,394 bytes. No upstream source, learner, verifier, or experiment was executed. **The requested whole-repository reading remains incomplete:** significant source and documentation, generated results, frozen bundles and binary evidence still require review. The [source-review checkpoint](source-review/README.md) and [per-file ledger](source-review/base12-coverage.json) distinguish complete text reading, exact-byte acquisition, programmatic inspection, identical aliases, inventory-only material and two connector transport mismatches.

The subsequent [rounded-operation and native-launch review](source-review/base12-followup.md) and [native research-loop source review](source-review/base12-research-loop.md) add 73 distinct full readings. That cumulative checkpoint contains **161 distinct fully read blobs / 1,226,434 bytes**, 46 identical alias paths, and **539 acquired exact paths / 530 distinct blobs**. The [extended ledger](source-review/base12-coverage-extended.json) retains identities and remaining gaps; the counts above describe the initial checkpoint.

Pinned source locations include [REPORT.md](https://github.com/rana/base-12-ai/blob/88382e793b65c84fd8e223840c27f6bb8682864a/REPORT.md), [AGENTS.md](https://github.com/rana/base-12-ai/blob/88382e793b65c84fd8e223840c27f6bb8682864a/AGENTS.md), [RECORD.md](https://github.com/rana/base-12-ai/blob/88382e793b65c84fd8e223840c27f6bb8682864a/RECORD.md), and [MERGE_POLICY.md](https://github.com/rana/base-12-ai/blob/88382e793b65c84fd8e223840c27f6bb8682864a/MERGE_POLICY.md). Access to those private sources is separate from access to Continuum.

The latest [decision-gate source review](source-review/base12-decision-gate.md) adds ten fully read distinct blobs / 30,638 bytes, giving **171 direct readings / 1,257,072 bytes** and **47 identical alias paths**. It checked nine manifest bindings without running upstream code. Its [additive ledger](source-review/base12-coverage-decision-gate.json) leaves global acquisition overlap unknown rather than adding new fetches to the older 539-path count.

### Prime Radiant

The accessible source was the October 18, 2026 research kit, retrieved as its current fourth stored edition. The archive contains **193 files**, totaling **8,984,055 uncompressed bytes**. Its SHA-256 is `97a156c3d6618d9f84f1271ec44dc12b056b0fdbfbf4fcf1de950cea691708a8`. The embedded integrity manifest identifies 192 files; all 192 file hashes were checked and matched. The remaining file is the manifest itself, whose SHA-256 is `d655c0436d4b0ed13387db14dd7447131be905ac98d662cb101e54d6b0fceea4`.

The kit is a source and evidence snapshot. A live Prime Radiant repository was not available through the connected repository listing or search. The kit's own project records describe a separate canonical checkout and a pending integration. Searching the accessible kit text did not reveal a usable live Prime Radiant GitHub URL. **This is a review of the accessible kit, not a claim to have read an unavailable live checkout.**

The substantive reading includes all sixteen Markdown documents and all sixteen Python files; the complete current C/header sources, including the bounded quadratic consumer; both Makefiles; and every historical pre-fix source difference against the fully read current source. The claims, decisions, disputes, relations, questions, queue, runs, surveys, and native correction/recovery records were read in full. All 79 JSON files and all 443 JSONL rows were parsed; the archive's structured research collections were inventoried, including 91 claims, 22 decisions, 38 disputes, 30 questions, 25 queue entries, 28 relations, 6 run records, and 159 source records. Those counts describe saved records, not independent findings or completed tasks.

The initial pass inventoried historical captures, reports, numerical traces, plots, and binaries. The [follow-up](source-review/prime-followup.md) subsequently completed semantic coverage of all eight retained dialogue captures, their eight receipts, and all three prose reports. Combined coverage is 76 complete semantic readings, including one exact-quotation-deduplicated capture, plus seven separately classified complete source-diff reviews. Its remaining-material table preserves the actual structured, numerical, visual, and binary gaps. Parsing or hashing does not establish semantic or visual review. No original scientific calculation, saved binary, or original simulation suite was rerun for this adaptation. Reported historical results remain source-reported results.

The [subsequent source audit](source-review/prime-audits.md) adds ten complete semantic readings, including all 159 source-inventory records, and separately checks two generated manifests. Latest kit coverage is **86 complete semantic readings**, **seven historical full-diff reviews**, **two generated-manifest checks**, and **98 remaining numerical, visual, or binary files**. No live checkout was obtained.

The most consequential kit paths are `REPORT.md`, `WALK.md`, `RECORD.md`, `AUTONOMY.md`, `AI_NATIVE.md`, `RESONANCE.md`, `SIMULATOR.md`, `calculations/ai-native-observability/`, `calculations/resonance-memory/`, `native/physics-seed/`, and `tools/research_record.py`. Exact bytes remain in the private source snapshot; this public repository contains the adaptations below.

### Canonical method cross-check

The complete experimental Holographic Walk definition was also read at `rana/lenses@db391ce6f9237e01a7d3cca33b73175cf7df4161`, path `experiments/skills/holographic-walk/SKILL.md`, Git blob `ebf219f3d2ae9e60b381eaeb5242037b5a2b3c32`. Selected method-selection and composition passages in that repository's `SYSTEM.md` were consulted. The method describes an applicability probe, bounded outward and inward passes, an interfaces-only pass, and a return that changes a question or constraint. It does not establish that every task benefits from a walk or that a coherent round trip supplies independent evidence.

## What changes the repository design

| Source lesson | Continuum adaptation | Boundary |
|---|---|---|
| A progress brief reconciles source records at a stated cutoff. | Render orientation from a pinned snapshot, evidence references, and an explicit baseline. | Fluent summary text is not automatically a checked claim. |
| Operational state, a possibility graph, and evidence/interpretation have different jobs. | Keep accepted work, imaginative alternatives, and evidence records distinct, with typed links. | An `informs` edge is not a blocking `requires` edge. |
| A question may be useful before it can become a test. | Preserve low-obligation seeds, then add scope, owner, budget, and acceptance conditions when promoting them. | Every thought need not become a ticket or experiment. |
| A lossy description can hide information needed by a later observation. | Treat context packets and projections as explicit views with retention and omission contracts. | A concise packet is not automatically dependency closure. |
| Evidence changes status at several independent boundaries. | Distinguish source review, generated output, admitted execution, observed result, and measured benefit. | Passing one boundary does not imply the rest. |
| Actual counterpart replies can contain consequential disagreement. | Preserve model provenance, coverage, corrections, and disagreements as records. | Model agreement is not an independent physical or execution observation. |
| Prior raw artifacts can become unrecoverable after an overwrite. | Give each attempt immutable output identities and explicit retention roots. | An artifact hash alone does not preserve its bytes. |
| Methods should fit the live question and available resources. | Use a small extensible registry with bounded invocations and honest receipts. | Registry entries do not create permissions, workers, schedules, or tool access. |

### 1. A brief is a projection, with a declared purpose

Base12's reporting discipline and Prime Radiant's record system suggest a useful separation: canonical facts live in their appropriate records; a brief assembles the facts needed for a particular decision. The initial [Progress Brief](../protocols/progress-brief.md) therefore requires a cutoff, source snapshot, coverage, and baseline when describing change. Without a baseline it provides orientation.

Capacity belongs in the same discipline. A task owner, a connected workstation, a historical benchmark, a running process, and measured present utilization are different observations. A progress projection must not turn one into another. Unknown utilization should remain unknown. A worker can be available for useful work even when no capacity measurement exists.

The long-term opportunity is **adaptive continuity**: retrieve the smallest sufficient context for a declared next action, together with explicit omissions and a path back to retained source objects. Sufficiency is relative to that action and its input contract; it is not a universal compression score.

### 2. Research alternatives need a richer graph than task dependencies

The Base12 research navigation distinguishes a possibility space from a queue of accepted execution. Continuum should preserve alternatives without implying all of them need work now. Useful relations include `informs`, `contrasts_with`, `tests`, `refines`, `supersedes`, and `requires`. Cycles of mutual interpretation can be meaningful; cycles in a required execution dependency graph need separate treatment.

Promotion should be explicit. A seed can become a framed question; a framed question can become a bounded probe; a probe can become accepted work. These are changes of commitment and scope, not a ranking of imaginative worth. A negative result can close one probe while opening a better question.

This makes multiple chats useful as complementary investigators. They can develop different formalizations and return typed contributions without prematurely forcing one vocabulary or one consensus. When reconciliation is needed, it should target an exact conflict, shared interface, or acceptance decision.

### 3. The representation itself can be an experiment

Prime Radiant's AI-native inquiry asks which distinctions a description must retain to answer its allowed future questions. Its observability examples make the question concrete within small declared mathematical models: identical coarse observations can conceal states that a later permitted operation separates. Its resonance-memory example shows how omitted state can return as a dependence on history or hidden preparation. These examples motivate a repository design question; they do not prove the performance of that design.

For Continuum, imagine two histories with the same current source tree. In one, an integration request was never sent. In the other, an acceptance may have happened before a network timeout. A projection containing only current bytes is insufficient for deciding whether to retry. The useful repair is to preserve the operation identity, recipient, authority epoch, accepted state if known, and reconciliation evidence.

Other representations should be evaluated in the same way. Can a packet answer whether evidence applies after a dependency change? Can a machine takeover distinguish an expired claim from accepted work? Can an agent tell whether a model conclusion came from new data or a cached reply? Construct histories that a proposed projection collapses, then ask whether the next decision differs.

The [Holographic Walk](../protocols/holographic-walk.md) is a bounded way to examine such losses across local state, interfaces, accepted work, and the broader objective. A useful return identifies a missing mechanism, a counterexample, a new constraint, or a better question. Reversing a lossy map by rhetoric does not reconstruct the missing state.

### 4. Evidence quality is multidimensional

The native physics seed distinguishes a problem definition, its discretization, the numerical method, and execution. It separately checks numerical residual, conservation or balance, temporal accuracy, spatial accuracy, and a deliberately unsuitable parameter case. A conserved quantity can remain correct while another decision-relevant property is wrong. The retained native peer review records a shared overflow defect in the implementation and its semidiscrete reference; agreement between those routes did not expose the error. This is a source-derived analogy for Continuum's evidence architecture, not an imported scientific test suite.

A stored digest can verify bytes and still say nothing about whether those bytes are the right input. A passing test can be perfectly reproducible and fail to cover a changed contract. Reusing an observation needs its declared input world, validity scope, and reuse contract. Missing information must remain `unknown`; absence of observed difference does not by itself establish equivalence.

For performance, measure useful completed work, including setup, retrieval, integration, verification, network transfer, and discarded attempts. A fast kernel, a large commit count, or many concurrent chats does not establish improved research throughput. New native code should earn its complexity against an appropriate reference workload.

### 5. Preserve attempts, corrections, and limits without freezing progress

The kit explicitly records an earlier run whose complete raw output was overwritten, and a native review whose original executable and complete initial verification report were not retained. Some source and compact observations survived; the missing originals were not represented as recovered. This is a concrete reason to retain evidence closures before publishing stronger conclusions.

Continuum should preserve failed and partial attempts without treating them as permanent bans on corrected successors. A successor gets a new identity, exact changes, and new evidence. A correction appends a record linked to the earlier claim; it does not rewrite the historical attempt into a success.

The kit's capture helper offers a useful small mechanism: exact supplied transcript bytes, an idempotent same-byte ingest, and rejection of conflicting bytes under an existing identity. Continuum must still establish its own transaction, crash recovery, and durability semantics. A pair of create-once files is not by itself a proof that a multi-object publication is crash atomic.

### 6. Collaboration must be inspectable without claiming inaccessible internals

Prime Radiant preserves actual visible user inputs, actual counterpart outputs, model identity as exposed, reading coverage, and authored audits that distinguish accepted conclusions from raw proposals. Continuum adopts that distinction in [Research Record](../protocols/research-record.md).

Record replay means retrieving, validating, or rendering the same saved material. Running an experiment again creates another attempt. Re-querying a model creates another inference, even with the same visible prompt. Neither a seed nor a model label guarantees identical future output or access to the same hidden serving configuration.

Multiple models can share typed objects, executable witnesses, constraints, and readable explanations. Private latent representations are optional research artifacts with declared decoders and compatibility limits; they are not a substitute for a stable public interchange contract.

### 7. Native ownership should follow semantic value and measured cost

Base12's compiler and execution work emphasizes exact admission boundaries and a stronger notion of an owned build path than ordinary native compilation. Prime Radiant's C11 seed explicitly calls itself a hosted reference and does not relabel that as owned compiler integration.

Continuum uses the same honesty while making its own implementation choice: native Rust first, a small explicit object and operation contract, and ordinary operating-system, cryptographic, storage, and network facilities as appropriate. Its essential ownership is of source/work/evidence identities, acceptance semantics, continuity, and interfaces. A compiler, assembler, network stack, or arithmetic system becomes a separate project only when a concrete requirement and measured benefit justify it.

No Base12 radix convention, strict compiler boundary, physics model, workstation identity, inherited schedule, or historical local restriction becomes a Continuum requirement by association.

### 8. Exact results still need a question that exercises the intended claim

Base12's transfer pilot preserves the difference between a supplied expression grammar, a supplied promise about the target family, and structure actually selected from examples. Its comparison of retaining one expression with retaining every source-consistent expression did not end up testing the loss of a genuinely different surviving explanation: the surviving expressions were equivalent on their relevant mathematical domain. A later calibration audit also found an accidental relationship among the calibration coordinates that let false simpler rules survive. The saved result retained that limitation rather than replacing the data after seeing the outcome. Sources: pinned [transfer result](https://github.com/rana/base-12-ai/blob/88382e793b65c84fd8e223840c27f6bb8682864a/research/learning/transfer-result.md) and [calibration analysis](https://github.com/rana/base-12-ai/blob/88382e793b65c84fd8e223840c27f6bb8682864a/research/learning/transfer-calibration.md).

Continuum should record what an experiment was capable of distinguishing. A context-retention benchmark needs histories that differ in something required by the next decision. A branch-preservation benchmark needs materially different alternatives. Changing the candidate family, input population, or acceptance criterion creates a successor question and an explicit reuse decision for earlier evidence. A successful bounded calculation does not by itself establish that the broader research question was tested.

The constructed operator witness shows another boundary: a network with deliberately authored weights can establish representational capacity without establishing that an optimizer learns those weights. An independent numeric calculation can still be insensitive to the suspected defect; for example, a nearly zero loss does not strongly test an averaging factor. A receipt should identify the check's implementation, assumptions, and failure classes it could detect, not merely count passing checks. Source: pinned [witness result](https://github.com/rana/base-12-ai/blob/88382e793b65c84fd8e223840c27f6bb8682864a/research/learning/operator-witness-result.md).

The cached restart audit was a comparison of saved predictions, not fresh inference. Its interpretation depended on exact source identities, a history-free update convention after initialization, shared-prefix consistency, and complete cached suffix coverage. Restarting from a correct visible state helped some continuations and harmed others; a correct final endpoint could conceal an incorrect intermediate step. For Continuum, compaction and workstation takeover should therefore be tested over the full decision continuation, including already successful controls. Equality of the current display is insufficient evidence that a replacement state is behaviorally interchangeable. Source: pinned [restart result](https://github.com/rana/base-12-ai/blob/88382e793b65c84fd8e223840c27f6bb8682864a/research/learning/operator-restart-result.md).

Finally, validation must challenge the declared family as well as its members. Every observation can be individually plausible under some candidate while no single candidate fits the observations jointly. High detection rates on deliberately selected, severely wrong saved models do not transfer to a population with only one error or to an adaptive policy. Continuum should retain candidate-set identity, joint compatibility, selection history, and denominators with a validation claim. Unknown costs remain unknown, and a retrospective success is distinct from measured savings in a prospective workflow. Source: pinned [validation-risk audit](https://github.com/rana/base-12-ai/blob/88382e793b65c84fd8e223840c27f6bb8682864a/research/learning/validation-risk.md).

### 9. Agreement must bind both the decision and the bytes consumed

The [decision-gate review](source-review/base12-decision-gate.md) supplies two concrete cautions. Agreement among rounded programs can be correct for their declared output while insufficient for an action about a different ideal quantity. A continuation benchmark should fix the required action, available information and total loss, and compare task-sufficient summaries and relevant evidence retrieval with full-history retention. Known regression witnesses remain exposed; a new random seed does not automatically make their successor task independent.

The reviewed archive checker also verifies one read of a path and then reopens that path for parsing. Under replacement between opens, checked and parsed content can differ even when the parsed members match their own manifest. This is a source-derived conditional schedule, not an observed failure or an executed exploit. Continuum should bind transformations to the exact retained byte object or state the enforced immutability condition, keeping custody, interpretation, execution and acceptance separate.

### 10. Completion and cost follow the declared boundary

The [native-boundary review](source-review/base12-native-reset.md) separates complete native execution, native building and reproducible self-rebuilding. A later reported decoder result does not silently finish the original gate's controller or builder. Continuum's native runtime, owned acceptance semantics and proposed owned kernel likewise require separate evidence. Reproducible bytes alone do not establish compiler correctness.

The source also distinguishes resident-kernel, whole-operation, launch, build/cache and device timing. Continuum's in-process workload, CLI reservation probe and complete checkpoint attempts retain their own boundaries; they do not compose into a general speed claim. Historical integration notes can preserve original packets while appending narrower outcomes and consumed clearances. Those notes are navigation for a successor, not fresh authorization to repeat external effects. This unit read six pinned files and checked four manifest bindings; it performed no upstream execution or new consultation.

### 11. Benefit claims need an accounting unit and matched alternatives

The [signal-readiness review](source-review/base12-signal-readiness.md) records a conditional upper bound: when a full predictor family contains the learned subset, framing is identical and future context is choice-independent, the subset's size advantage is bounded by omitted dictionary overhead. In the documented one-stream case, four learned entries versus 35 permit at most 31 bytes of advantage over the full family. The implementation was not newly audited here. This is not a general AI-context theorem: representations can change future decisions and costs.

Shared computation can support paired output comparisons while preventing independent per-arm timing claims. An older codec with different history, framing and adaptation is not a matched baseline. For future Continuum studies, declare task exposure, candidate relationships, cost boundaries and readiness checks before scored work. A prerequisite failure after validation exposure is retained attempt evidence; later installation does not erase it. Historical coordination with an existing owner also does not authorize a second execution queue.

### 12. Structural advantages change the interpretation of wins

The [learning-performance review](source-review/base12-learning-performance.md) explains why a minimum-cost arm retaining all baseline candidates does not yield unconstrained per-record win trials. Magnitudes, global model overhead and a matched alternative still matter; eight favorable records do not justify a sign test under that design. A reported 98.27% share of the full family's net saving also needs its exact baseline denominator, rather than becoming a size or speed ratio. Continuum comparisons should record candidate inclusion and task exposure before scoring wins.

The same source proposes associative reconstruction for a fixed recurrence while declining to apply it to rounded/clipped feedback. Efficient batching needs a sufficient boundary state and preserved semantics; a derivation for one algorithm does not establish another's optimization. Three source readings, two preservation bindings and arithmetic from reported totals were checked here, without reproducing a run or measuring acceleration.

## Initial adaptations and the next research return

The initial package contains [Progress Brief](../protocols/progress-brief.md), [Holographic Walk](../protocols/holographic-walk.md), [Research Record](../protocols/research-record.md), and [Bounded Research Loop](../protocols/bounded-research-loop.md). Their registry, invocation, and receipt contracts distinguish method from skill adapter, prompt, and policy authority. See [protocol architecture](architecture/protocols.md).

The next high-value experiment is a controlled interrupted-work scenario: two workers receive related tasks, one produces evidence, a handoff times out, authority changes, and a fresh worker resumes from a context packet. Compare the resumed decision against the complete retained record. Measure the wrong decisions, necessary retrieval, time to a correct next action, and cost of needless reruns. This would test whether the repository preserves the distinctions its agents need, while exposing where the current model is still too coarse.
