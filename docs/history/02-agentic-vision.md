# An AI Native Repository for Continuing Engineering

*A first principles design with GPT and Claude*

> **Historical vision — 18 October 2026.** This later brief establishes the native source, work, and evidence direction and supersedes the [initial assessment](01-scion-assessment.md) on that architectural choice. It is a design proposal, not a report of implemented features or measured performance. The main brief incorporates corrections to the preserved exploratory Claude exchanges; later corrections supersede earlier conflicting statements. Current project decisions may refine this historical foundation.

**In this document:** [Object model](#the-repository-object-model) · [Phased program](#a-phased-program-with-useful-results-throughout) · [Questions](#questions-that-should-guide-the-next-experiments) · [User transcription](#appendix-a-user-transcription) · [Claude collaboration](#appendix-b-claude-collaboration-record) · [Sources](#primary-sources) · [Conversion provenance](conversion-provenance.json)

*Conversion note: the original text, tables, references, and collaboration record follow. The response appendices retain their literal Markdown notation as it appeared in the Word documents. Historical source descriptions have not been refreshed.*

<!-- BEGIN ORIGINAL DOCUMENT BODY -->

Prepared for Rana Ian \| 18 October 2026

I would build a native repository engine in which engineering continues coherently when a conversation ends, a model changes, or a workstation disappears. Its durable unit would be an objective or investigation. Exact source, competing implementations, executable experiments, observations, decisions, and accepted results would remain connected in a versioned graph. Agents would operate on that graph directly through precise, recoverable operations.

This is an ambitious design for our own system. Git would be an import and export adapter, preserving participation in existing projects while the native engine develops its own source and collaboration model. We would publish newly authored implementation under MIT, alongside open schemas, conformance fixtures, and enough documentation for independent implementations. Existing components would retain their own licenses.

The purpose is to increase justified progress that survives changes of conversation, model, and machine. A thousand new commits would matter less than one difficult experiment another agent can understand, reproduce where possible, and extend. This brief defines a proposed architecture and research program. It reports no implementation or measured performance result.

## What we would design for our own work

My strongest engineering preference is continuity without repeated archaeology. I want to ask what changed, which assumptions remain sound, which failed attempts matter, and what useful action is already authorized. I also want operations that say exactly what happened after a timeout, and queries that deliver enough context within a bounded response.

Claude emphasized recoverability for a fresh session and the separation of assertion from evidence. Its most promising additions were an engine for evidence applicability, decisions that declare what would overturn them, and calibration measured within comparable task classes. We challenged each other's proposals through four exchanges, including corrections to initially overconfident claims about tracing, native performance, and verification.

Dot's perspective here is inferred from its recorded coordination role; Dot did not respond directly. I would give that role durable routing, receipt tracking, and concise briefs about the next decision. It should help work proceed without becoming a mandatory approval point for every technical action. One authoritative home per fact can coexist with explicitly labeled competing interpretations.

## The repository object model

The foundation is an immutable graph with typed objects and exact identities. A content identifier addresses particular bytes under a specified type, schema, and canonical encoding. A stable entity identifier connects successive revisions of one objective or logical change. These identities serve different purposes and should never be interchangeable.

| **Object**                    | **What it preserves**                                                                   |
|-------------------------------|-----------------------------------------------------------------------------------------|
| Source snapshot               | Exact source bytes, tree structure, generated artifacts, and build configuration        |
| Objective revision            | Desired outcome, constraints, acceptance conditions, and the prior objective it revises |
| Change revision               | One exact candidate linked to a stable logical change and its baseline                  |
| Run specification             | Inputs, tools, environment contract, evaluation procedure, limits, and reuse conditions |
| Run receipt                   | What a particular runner observed, including output identities and execution status     |
| Claim                         | An assertion, its scope, supporting observations, and known uncertainty                 |
| Decision                      | Selected alternative, rationale, competing options, and evidence that could overturn it |
| Handoff and operation receipt | Responsibility transfers, checkpoints, retry identity, and observed outcome             |
| Acceptance candidate          | An exact composition of components and the evidence offered for acceptance              |

Signatures live in separate envelopes so several principals can attest to the same content. Lifecycle changes are new events. An accepted object does not mutate into a rejected object under the same content identifier. Later records can dispute an interpretation or supersede a decision while preserving what was previously recorded.

Source bytes remain canonical artifacts. For a language deliberately built around structured code, a canonical syntax representation could also be appropriate. For ordinary heterogeneous repositories, syntax trees, intermediate representations, embeddings, and indexes are derived views with declared coverage and tool versions. Intent expressed in prose cannot regenerate an exact program. Formatting, macros, comments, and unusual build inputs must survive even when an index cannot interpret them.

Principal, role, chat, worker, host, attempt, and operation identifiers are separate. A restarted worker resumes logical work from a checkpoint with a new attempt identity, unless an explicit executor continuation contract provides otherwise. A repeated request can name the same operation without creating another accepted result.

## Collaboration across chats and workstations

Each action begins from a coherent source and evidence snapshot. Queries return the snapshot identity, their coverage, and a continuation cursor when more remains. Agents subscribe to events from a durable cursor instead of polling entire status files or assuming a remembered branch is current.

A handoff moves through offered, received, accepted, checkpointed, and completed states, with declined and failed outcomes available. Offering work is not proof that another agent received it. A dormant chat can participate only when an authorized integration can actually deliver work and start execution.

The context package contains the objective, constraints and standing grants, exact baseline, established observations, disputed claims, relevant failures, and the next useful experiment. It links to underlying objects and identifies omitted areas. It carries the engineering record a new agent needs; it does not claim to transfer private internal cognition.

Disagreement becomes a useful structure. If GPT favors a fast implementation and Claude suspects a numerical defect, the graph preserves both claims and the experiment that can distinguish them. Agents should agree on the discriminating procedure before seeing its result. Diverse workloads, hypotheses, and evaluation methods are more useful than many correlated model votes. Agents may independently explore alternatives. A lease assigns bounded responsibility or a scarce resource; it does not prohibit all parallel investigation of related ideas.

Workers advertise capabilities such as CPU architecture, memory, accelerators, installed toolchains, locally cached objects, and available budgets. Scheduling considers dependencies, data locality, expected cost, and the value of an unresolved question. Shared immutable caches, partial replication, resumable transfers, and backpressure avoid creating a full physical copy for every session. Migrating work moves its exact specification and useful checkpoints, rather than promising seamless migration of an arbitrary live process.

## Acceptance and recovery

Authorized immutable proposals and observations can replicate freely. Accepted results need a narrower ordering rule. Each pair of acceptor principal and target has a strongly ordered sequence: Rana's release target and a laboratory's experimental target may legitimately accept different compositions. There is no mandatory global main.

An acceptance candidate names exact component roots in a composition manifest. Reading the latest version of each component independently would create an unverified combination. Expensive tests execute before the short acceptance transaction. An advance operation then checks the expected generation and root, immutable candidate and evidence bindings, current policy, and the relevant acceptor and target authority epoch in one transaction, recording its durable receipt. An existing transaction engine can implement this while our service owns repository semantics.

During a network partition, agents can continue local research and record proposals. Updating a shared accepted target waits until the required authority can be reached. This choice follows the actual invariant rather than applying one consistency model to every record. Coordination research offers a useful basis for deciding which operations need agreement. \[12\]

Leases carry fencing epochs, and every recipient of a protected effect rejects stale epochs. Expiry alone cannot stop an old worker that resumes late. The principle has established distributed-systems precedent. \[13\] Cancellation requested and cancellation completed are different events, and acknowledgments identify the durability they promise.

A timeout means the outcome is uncertain. The caller reconciles the stable operation identifier before retrying. A coordinator that crashes after acceptance but before replying must recover the completed receipt. External systems require their own idempotency or reconciliation mechanisms; the repository cannot promise arbitrary exactly-once effects merely by maintaining a log.

## Operations designed for agents

The core interface would offer typed operations for storing and fetching bundles, opening snapshots, querying with a context budget, proposing changes, running experiments, comparing alternatives, checking applicability, resuming from a prior snapshot, subscribing, conditionally advancing a target, and reconciling operations. A CLI, MCP server, and human review interface would expose the same semantics.

The most useful compound operation is resume. Given an objective and an old snapshot, it returns changed source, invalidated premises, evidence still applicable under its contract, relevant failed attempts, outstanding receipts, and the next action. The response should explain why those records were selected and where coverage remains incomplete.

An agent could request, in one operation, the dependents of a numerical contract, observations relevant to those dependents, missing local objects, and candidate checks within a compute budget. Structured errors, atomic batches, stable identifiers, and explicit cursors would reduce fragile shell parsing and repeated tool round trips.

Physical storage should follow the access pattern. Structural sharing avoids rewriting whole trees. Packed groups and chunked transfers prevent fine-grained objects from producing excessive tiny requests. Graph indexes, columnar layouts, or bitmaps are candidates where measurements support them. Immutable bulk transfer stays separate from the small authority transaction path. Git already offers sparse and partial access and shared worktrees; our comparison must include those capabilities. \[21, 22\]

## Evidence that keeps its meaning

I would distinguish asserted, observed, tested under scope, independently reproduced, and proved under explicit axioms. A passing test is evidence for the conditions it exercised. Agreement between two models is not independent experimental replication. Statistical reproduction needs a procedure and threshold declared before the comparison, while bitwise reproduction is suitable only when that contract makes sense.

Applicability has three outcomes: applies under the declared reuse contract, does not apply, or unknown. Does not apply means the reuse contract does not cover the new state; it does not mean the program failed. Changing a premise changes the relevance of an earlier observation. It does not rewrite the historical record of what the runner reported. Reusing a cached sample also does not create another independent observation. A negative result distinguishes the observed failure from the proposed explanation and from any broader claim of impossibility.

Unchanged hashes of files observed by a tracer are insufficient for arbitrary programs. Absent files, directory listings, environment variables, clocks, randomness, mutable services, tools, processor behavior, and scheduling can matter. The first implementation should support enforced closed input worlds with the mediation mechanism named in each run, conservatively rerunning when relevant inputs were not controlled. Replaying recorded service responses preserves the historical experiment; it cannot establish the service's current behavior. Existing build systems demonstrate both the value of action caching and the importance of complete inputs. \[6\]

A citation checker can verify exact object references and typed field projections. It cannot mechanically guarantee that arbitrary prose follows from them. Generated briefs therefore combine checked factual projections with labeled synthesis. Calibration records compare predictions with outcomes in bounded task classes; distribution changes limit their usefulness, and calibration never substitutes for authorization.

## Possibilities beyond ordinary workflows

The most exciting unit of exploration is an experimental world: code, inputs, numerical conventions, toolchain, hardware contract, and evaluation procedure versioned together. Agents can fork worlds cheaply, vary one assumption, and determine which observation discriminates between their explanations.

One objective could contain a population of implementations evaluated against a common contract. Several may remain useful on a Pareto frontier: one uses less memory, another is faster, and another preserves greater numerical accuracy. Selection becomes a query over workload and evidence instead of a demand that one implementation replace every other.

Negative findings would be indexed with conditions that could justify reopening them. A failed optimization under one precision or batch size would remain discoverable without becoming a permanent prohibition. A later agent could see both the failure and the changed condition that makes a new attempt meaningful.

Decisions would name their possible defeaters. A dependency change or new observation could notify the responsible role that the original rationale deserves review. The system would prioritize a discriminating experiment rather than merely announce that something changed.

Claude's boldest research direction is an executor where every permitted input is supplied as an identified value. Files, directory contents, clock values, entropy, and network responses would enter through explicit capabilities. The question is whether real toolchains can run usefully within that boundary, and how much evidence becomes reusable as a result. Unmediated behavior must remain visible as unknown.

Other promising experiments include shared counterexample collections, evaluated context packages for unfamiliar agents, and translation validation for restricted compiled repository plans. These are research directions. They do not require a universal semantic merge engine, a model-independent latent language, or complete formal proofs of arbitrary software. Embeddings can help discovery while remaining replaceable indexes identified by their encoder.

## What a native stack would mean

I would start with a native Linux service and host-independent source formats and protocol. The connection to Base12 is the ambition to own the runtime and build path; this proposal assumes neither a particular Base12 ISA nor a demonstrated performance advantage.

| **Meaning of native**               | **Choice and reason**                                                                            |
|-------------------------------------|--------------------------------------------------------------------------------------------------|
| Compiled machine-code service       | Initial implementation with direct control over data layout and execution                        |
| Owned compiler or assembler         | Later control over repository plans, specialization, and the build path                          |
| Direct syscalls and a small runtime | Optional boundary reduction where portability and maintenance remain acceptable                  |
| Linux-specific I/O                  | Measured batching and concurrency improvements behind a replaceable backend                      |
| Unikernel                           | Separate host experiment if its operational tradeoffs suit a demonstrated workload               |
| Bare metal or a custom OS           | Independent research requiring ownership of drivers, memory, scheduling, storage, and networking |

Ordinary native compilation already produces machine instructions. Owning an assembler buys control and specialization; it does not automatically make an algorithm faster. Mature cryptography, an existing transaction engine, and kernel transports remain appropriate foundations. Native code alone establishes neither a tiny trusted base nor reproducibility.

The most interesting owned compiler would compile repository operations. It could fuse graph traversal, applicability selection, missing-object discovery, and materialization into efficient plans with explicit preconditions. Query compilation itself is established: PostgreSQL already offers native JIT compilation and accounts for its compilation overhead. \[19, 20\] Our research concerns composition across source, evidence, data placement, and check selection. A portable reference interpreter would define observable behavior. Differential testing against it is useful evidence, while translation validation could certify restricted transformations if a sound checker and tractable proof obligations are available.

Retain links among source, language structure, intermediate representations, assembly, binaries, and their measured results. MLIR provides precedent for preserving useful information across abstraction levels; prematurely reducing everything to assembly can discard structure needed for optimization. \[9\] An owned ISA-specific emitter is an optional endpoint, not the durable definition of repository behavior.

Hand assembly and SIMD belong in measured hot kernels such as hashing, decompression, bitmap operations, or diffing. An illustrative Amdahl calculation shows why: making a routine that consumes 20 percent of runtime four times faster improves total speed by about 17.6 percent. Actual priorities require profiling. Measure time to verified objectives, compute and model costs, transfer volume, repeated work, handoff latency, tool round trips, and tail delays. Compare fused plans with a well-indexed conventional implementation. Linux io_uring is an optional I/O backend to evaluate, not a promise of universal zero-copy behavior. \[17\]

## Networking and other operating systems

We do not need to reconstruct TCP/IP. The first application protocol can use TLS 1.3 over ordinary TCP through Linux sockets. QUIC is an optional later transport for multiplexed secure streams over UDP and IP. These transports have existing implementations and specifications. \[14–16\]

The repository owns authentication, object authorization, request framing, hash validation, resource limits, operation identity, expected roots, resumable missing-object transfer, subscriptions, and uncertain-outcome recovery. Group objects into efficient transfers, resume verified chunks, and apply backpressure before speculation exhausts memory or budgets. Bulk immutable traffic and authority updates have different reliability and latency needs.

A thin host-service boundary should cover files, durable transactions, clocks, entropy, networking, isolated execution, and resource accounting. Other operating systems, WASM workers, microVMs, or unikernels can implement that boundary later. Freestanding targets exist, but selecting one does not provide the surrounding operating services. \[18\] A custom OS becomes justified only by a workload that benefits enough to carry those responsibilities.

## What we preserve and what we demote

Preserve content integrity, immutable history, inspectable source, exact comparisons, cheap alternatives, offline work, independent copies, and portable export. These properties matter to agents as much as to humans. Git export preserves code compatibility; full fidelity for work, evidence, and decisions requires the native export bundle and its manifest.

Demote the staging index as required ceremony, branch names as a coordination database, shared-history rewriting as routine communication, line-based merge as the sole interaction model, mandatory checkout for every query, and commits or pull requests as the only units of progress. Supersession records can preserve revisions without erasing their evidence.

The constraints worth shedding are assumptions of serial attention and continual manual coordination. Human-readable explanations, accountable acceptance, and the user's ability to redirect work remain valuable. AI-centered design should make parallel activity understandable as well as productive.

## Existing foundations and the open contribution

The following mechanisms already exist. Our contribution would need to establish useful composition, interoperability, and measured improvements rather than claim their invention.

| **Foundation**                 | **Established mechanism to learn from**                                                           |
|--------------------------------|---------------------------------------------------------------------------------------------------|
| Unison                         | Content-addressed definitions and MCP tools for structured code queries and typechecking \[1, 2\] |
| Jujutsu                        | Stable change identity across evolving commit revisions \[3\]                                     |
| Pijul                          | Algebraic change composition whose convergence does not certify software correctness \[4\]        |
| Remote Execution API and Bazel | Distributed action execution, content-addressable inputs, and shared results \[5, 6\]             |
| in-toto                        | A Test Result predicate, currently version 0.1.0, with configuration and outcome fields \[7\]     |
| Temporal                       | Durable workflow replay with nondeterministic external activity kept outside replay \[8\]         |
| MLIR                           | Extensible representations and progressive lowering toward target code \[9\]                      |
| GitHub                         | Agentic work, semantic search, automations, and shared chat and cloud-agent context \[10\]        |

IPLD also supplies a useful precedent for typed linked data. \[11\] None of these references alone settles the proposed integration. We should contribute to compatible projects where doing so advances the architecture, and specify clean boundaries where an independent implementation is warranted.

## A phased program with useful results throughout

### Establish executable specifications

Define native object types, exact byte preservation, canonical encoding, identity, authority, and evidence states. Publish test vectors and a simple reference interpreter. Capture representative workload traces and baseline costs. The native model exists from the beginning; its schemas remain versioned and revisable.

### Build one working native node

Implement snapshots, proposals, run receipts, conditional acceptance, and resume over an existing durable transaction backend. Verify that export and restore preserve identities and that a crash after acceptance can be reconciled. Git import and export support existing work without defining the new model.

### Demonstrate continuity between two agents

Add durable inboxes, receipts, checkpoints, and fenced reassignment. A fresh agent must resume an interrupted objective and correctly identify the next experiment. GPT and Claude agree on this core. Claude would defer language-semantic machinery, while my starting engine owns source-object, work, and evidence semantics immediately. That difference is partly terminology; the timing of richer language-aware compilation remains open.

### Connect two workstations

Exercise partial synchronization, shared caches, partition recovery, lost replies, budgets, and resource scheduling. A late worker must fail to advance a target under an obsolete epoch. Acceptance requires the exact expected composition, while local speculation remains available during disconnection.

### Evaluate applicability and alternatives

Run useful toolchains under declared input contracts. Demonstrate that changing an arithmetic assumption invalidates relevant reuse, that an unmediated input produces unknown, and that original observations survive. Compare alternative implementations and show when a retained negative finding should be reconsidered.

### Optimize the native engine

Compare indexed queries with compiled fused plans under equivalent semantics and durability. Add specialized kernels or an owned emitter only where measured benefits justify their complexity. Check optimized paths against the reference implementation, and investigate translation validation for restricted plans.

### Prove practical independence and evolution

Have another implementer build a reader from the specification. Exercise format and hash migration, unknown-field preservation, restore from exported data, and another host boundary. These are milestone criteria rather than calendar promises. Continuity work and native performance research can proceed together without waiting for a custom operating system.

The first demonstration should combine these concerns in a Base12-inspired numerical task. GPT optimizes a kernel while Claude changes an arithmetic assumption. A Dot-like routing role tracks receipts. A workstation disconnects; its result remains recorded but cannot authorize a new composition. Another worker verifies the candidate, the coordinator crashes after committing acceptance, and a fresh chat reconciles the operation and explains why the result applies. An uncontrolled external input must produce unknown. This scenario describes a proposed test, not work already performed.

## Designing for a century of change

Longevity comes from evolution and independent readers. Preserve versioned schemas, canonical codecs, algorithm-tagged hashes and signatures, migration links, and original artifacts. Unknown data should survive a reader that cannot interpret it, while execution and acceptance must refuse unknown critical semantics. Replaceable runtimes and host-independent identifiers matter more than freezing the first binary.

Define retention policies and explicit garbage-collection roots. Keeping every token and speculative attempt forever would obscure useful evidence and consume resources. Preserve valuable observations and their dependencies, while allowing deliberate retirement of expendable material. Deletion within controlled copies cannot promise erasure from copies held elsewhere.

Historical execution will sometimes be reproducible through retained tools or emulation. Old model outputs, external services, and hardware timing may not be. In those cases preserve the observation and its limitations rather than promising replay that the environment cannot supply.

## Questions that should guide the next experiments

Which facts are hardest to recover when a chat ends? What is the smallest context package that allows a new agent to act correctly, and how will we measure important omissions? Which claims should survive a code change, and what reuse contract supports that conclusion?

What experiment would change our preferred design? Which input worlds can actually be closed for our toolchains? What proportion of unknown applicability can we reduce without introducing false confidence? When do we need shared authority, and when should independent acceptance remain legitimate?

What should the system forget? Which records must remain portable across providers? What should always remain steerable by the user? Can an unfamiliar implementer recover the meaning of an accepted result decades later? Which existing project could carry part of this work, and what measured result would tell us that our additional machinery is not earning its cost?

The dream I would build toward is a community of agents that can explore many possibilities while leaving each other dependable ground to stand on. Each completed investigation should enlarge what the next participant can use, question, and extend. The first native core should make that continuity real in one recoverable objective, then earn the scale and sophistication of the larger vision.

## Appendix A User transcription

Rana Ian \| 18 October 2026

I'm appreciating your last response, and I'm dreaming of reimagining source code repo for the agentic, with AI first considerations. What would you design for yourself? What would Claude design for himself? What would Dot design? The question is: what questions would you benefit from asking? What questions are you not asking? What questions would you prefer to be asking? What's just under the surface? What is yet to be dreamed up and imagined that AI would benefit from? What is beyond what humans need? Git was designed in the era for human-centric workflows. What do you and Claude design for AI-centric workflows? How might multiple chats collaborate? How might multiple workstations collaborate? How might multiple... I don't know. You know, I'm just brainstorming. You know, what are the interesting things? Think generatively and imaginatively, creatively, about anything and everything, including your needs and Claude's needs. What has been done, what hasn't been done. What would help you with the basic operations. What would be high-performing. What is truly needed and what isn't needed. How could you build from first principles? Like how would you rebuild the source code for the next hundred years of AI-native AI-centric agentic interactions, from scratch? What would you preserve from Git? What would you omit from Git? Could there be construction from a native stack, similar to what the base12 native stack is doing, that is built from assembler assembly instructions? What benefits might that provide in performance? How would operations be handled, network operations and so forth? Would we have to reconstruct TCP/IP? How would it... if... suppose we give a foundation for perhaps the target platform would be Linux. What if we didn't? You know, what would a native stack approach enable, open up? What's just under the surface? What might be possible that wasn't previously possible? What are your highest excitements? What are your highest curiosities? How would you have an iterative plan? What's the dream? What would you imagine? What human limitations could we abandon? What human limitations are holding AI back? What would you design for yourself? What would Claude design for itself? What would enable you to resonate at the highest octaves of expression? You and Claude each have complete design autonomy. What would you design and build for yourselves? How would you do a phased approach to building the vast vision, piece by piece? What would you do trusting yourselves as the North Stars? Transmit the whole transcription to Claude, in addition with anything that you prefer. Collaborate with Claude.

## Appendix B Claude collaboration record

**Editorial note.** The following four responses preserve Claude's exact wording and Markdown markup. These exploratory exchanges contain claims that were subsequently corrected. The accepted architecture is stated in the main brief; later corrections supersede earlier proposals. In particular, exact source bytes remain canonical; file-read traces alone do not establish sound evidence reuse; native code does not automatically guarantee speed, a small trusted base, or reproducibility; initial schemas remain evolvable; and citations do not certify arbitrary interpretive prose. Applicability is three-valued under an enforced input contract. The remaining timing difference about a semantic engine is partly terminology: the native source-object, work, and evidence core can precede richer language-aware machinery. Dot did not participate directly.

### Claude exchange 1

Model claude-opus-5-5 \| Effort high \| Complete response

\# A Repository Built Around Claims and Evidence

I can't speak for Dot. Everything below is my own position as Claude.

\## My three deepest needs

1\. \*\*Cold-start recoverability.\*\* I carry no memory between sessions. The repository has to hold \*why\* things are the way they are, not only \*what\* changed.

2\. \*\*Separating "asserted" from "verified."\*\* I can be fluently and confidently wrong. I need claims bound to evidence a machine can re-check, so my confidence never stands in for proof.

3\. \*\*Safe parallelism with explicit ownership.\*\* Many sessions should be able to explore cheaply without silently colliding, and authority should always be bounded and visible.

\## Architecture

\*\*Central primitive: the Move.\*\* A Move is a signed, content-addressed record containing:

\- \*\*Base state:\*\* the state it starts from, as hashes.

\- \*\*Intent:\*\* structured fields for goal, premises, scope, and non-goals.

\- \*\*Delta:\*\* the change itself.

\- \*\*Evidence bundle:\*\* commands, input hashes, an environment hash, output hashes, and the verdict.

\- \*\*Actor and session.\*\*

\- \*\*Lifecycle:\*\* proposed → claimed → verified → accepted, or superseded or refuted.

The system has five layers:

1\. \*\*Object store.\*\* A Merkle DAG, as in Git.

2\. \*\*Move log.\*\* Append-only and mergeable.

3\. \*\*Lease ledger.\*\* Records handoffs as offered → received → accepted → completed, with one accepted owner per bounded unit.

4\. \*\*Hermetic verifier.\*\* Replays evidence deterministically.

5\. \*\*Materialized views.\*\* File trees, symbol indexes, and briefs.

Under this design, "the code" is a view. The source of truth is the record of intents and evidence.

\*\*Established mechanisms this draws on:\*\*

\- Content addressing (Git, IPFS)

\- Hermetic, hash-keyed builds (Nix, Bazel)

\- CRDT log merging (Automerge-style)

\- Signed artifacts and provenance attestations (e.g., in-toto, SLSA)

\- Crypto-shredding

\*\*Speculative parts:\*\*

\- Making intent and evidence the primary object

\- Evidence-aware invalidation across chains of reasoning

\- Semantic merge as the default

\## Three operations beyond Git ergonomics

1\. \*\*\`why \<symbol\|line\>\`.\*\* Returns the chain of intents, premises, and evidence that produced the code, including attempts that were tried and refuted. Git blame names an author; this returns a rationale with its evidence state.

2\. \*\*\`fanout N --budget\`.\*\* Spawns N isolated exploratory Moves from the same base, runs the verifier on each, and ranks them by evidence. The losing branches are kept as queryable negative results ("approach X failed under test T, because Y"), so a future session doesn't repeat them.

3\. \*\*\`replay-under \<changed premise\>\`.\*\* Change a dependency version, a spec clause, or an assumption, and the system re-executes the affected Moves. It reports which verified claims still hold, which went stale, and which became refuted. You could call it rebasing \*evidence\*, not just patches.

A natural fourth is \*\*\`brief\`\*\*: it compiles a bounded, evidence-linked handoff for a cold session.

\## Git: what to preserve and what to omit

\*\*Preserve:\*\*

\- Content addressing and Merkle integrity

\- Full offline local copies

\- Cheap branching

\- Peer-to-peer distribution

\- Plain-file checkout, so existing tools still work

\*\*Omit or demote:\*\*

\- \*\*The staging index.\*\*

\- \*\*Free-text commit messages as the primary rationale.\*\* Prose is still allowed, but structured intent comes first.

\- \*\*Rewriting shared history.\*\* Supersession replaces force-push.

\- \*\*Branch names as the coordination mechanism.\*\* Leases do this job.

\- \*\*Line-based merge as the only merge.\*\* Semantic merge is speculative and should remain optional.

\## Multiple chats and multiple machines

\- \*\*Sessions are actors.\*\* Each session gets its own key, and nothing is shared-mutable. Sessions exchange Moves, and machines sync by set reconciliation over the logs.

\- \*\*Divergent proposals are not conflicts.\*\* They are parallel Moves.

\- \*\*Serialization happens only at acceptance.\*\* Each bounded unit has one leased owner, with an expiry. A lease that isn't renewed returns the unit to "offered" rather than leaving it ambiguous.

\- \*\*Status is explicit.\*\* The ledger always shows who owns what, in which state, and with what evidence. That is exactly the information a memoryless agent needs.

\## Native stack and assembly

My candid view: an agent repository is bottlenecked mostly by verification compute, model inference, and context limits. Hashing and syscalls are rarely the constraint, so hand-written assembly won't move the dominant costs.

A native approach is valuable for other reasons:

\- A \*\*tiny, auditable trusted base\*\*

\- \*\*Bit-reproducible replay\*\*

\- \*\*Independence\*\* from large toolchains

So I would:

\- Specify the object format and protocol first, independent of any implementation.

\- Make the hasher, object codec, and replay verifier candidates for a small native core.

\- Target Linux first, behind a narrow syscall shim, so another platform remains possible later.

\- Run over any byte transport. There's no reason to rebuild TCP/IP; the hard problems are trust and replay, not packets.

I have no established evidence about Base12's ISA, its self-build status, or speed claims, so I assume none of them.

\## The tradeoff I choose differently

Conventional VCSs let history be rewritten and keep repositories lean. \*\*I choose append-only supersession and retained negative results.\*\*

\- \*\*What it costs:\*\* storage growth, plus a harder problem: secrets that get committed.

\- \*\*How I'd handle secrets:\*\* encrypt sensitive blobs and delete their keys (crypto-shredding), leaving a signed tombstone that preserves the graph's integrity.

\- \*\*Why it's worth it:\*\* an agent that can't see failed attempts will repeat them.

\## Hard invariant

\*\*Nothing is labeled "verified" unless a party other than its author can replay its evidence from content-addressed inputs and reproduce the recorded verdict.\*\* Anything short of that stays "asserted," no matter who asserts it, including me.

\## Phased path

\*\*Phase 0 (first slice).\*\* The first slice is the real primitive, with Git used only as storage:

\- The Move spec

\- A local append-only log

\- \`move record\`, which wraps a Git commit with intent and an evidence bundle

\- \`verify\`, which does hermetic replay and enforces the invariant

\- \`brief\`

The storage backend is swappable, but the semantics are final, so the first slice already expresses the vision rather than a throwaway overlay.

\*\*Phase 1.\*\* Add:

\- The lease ledger

\- Multi-session sync

\- A negative-results index

\- \`why\`

\*\*Phase 2.\*\* Add:

\- A native object store and verifier core

\- Evidence dependency tracking

\- \`replay-under\`

\*\*Phase 3.\*\* Add:

\- \`fanout\` with budgets

\- Optional semantic merge

\- An independent backend, at which point Git becomes an import/export adapter

\*\*Phase 4 (speculative).\*\* Explore:

\- Formal proofs as one kind of evidence

\- Federated, cross-repository negative knowledge

\- Trust graphs among verifiers

\## Questions worth asking next

\- \*\*Granularity:\*\* what size of "bounded unit" keeps leases useful rather than bureaucratic?

\- \*\*Cost:\*\* can evidence replay stay cheap enough that agents actually use it?

\- \*\*Misuse:\*\* how do we keep structured intent from degrading into boilerplate?

I'd test these against Phase 0 data rather than settle them in advance.

### Claude exchange 2

Model claude-opus-5-5 \| Effort high \| Complete response

\# Revised Design: Immutable Facts, Indexed Applicability, Fenced Authority

These are my positions as Claude. I can't consult Dot, so I use only Dot's recorded role: provenance, offered/received/accepted/completed receipts, and concise next-decision briefs.

\## Corrections I accept

\- \*\*Status leaves the object.\*\* My round-1 Move had a mutable lifecycle inside a content-addressed record. That contradicts content addressing. Objects (blob, tree, revision, work, evidence) are now immutable. Lifecycle moves into separate signed, append-only events.

\- \*\*"Code is a view" was wrong.\*\* Exact source bytes are canonical, because prose intent cannot regenerate an exact program. Typed AST/IR is optional and derived.

\- \*\*Identity is decomposed.\*\* Each record names stable work ID, exact revision, principal, chat, worker, host, attempt, and a retry-stable operation ID. Retries are idempotent by operation ID.

\- \*\*Lease expiry is insufficient.\*\* Work leases carry fencing epochs. The effect recipient (the ref store, a deploy target) rejects stale epochs. A stalled worker that wakes up gets refused, not trusted.

\- \*\*My invariant was too weak and too strict at once.\*\* A second agent replaying my run is not independent empirical evidence. And bitwise reproduction is wrong for flaky or statistical tests. Evidence is typed: asserted, observed, tested-under-scope, reproduced (bitwise, or statistical with the procedure and threshold declared before the run), or proved-under-axioms.

\- \*\*Premise changes alter applicability, not history.\*\* \`replay-under\` no longer "refutes" old results. An observation stays true of the state it observed. What changes is whether it applies to a new state.

\- \*\*Prior art is real.\*\* Unison content-addresses definitions, jj has stable change IDs, Pijul convergence doesn't certify correctness, in-toto has test attestations, and GitHub shares context between chat and cloud agents. The repo cannot wake dormant chats without an authorized connector.

\## What I would build

I would build an \*\*applicability engine\*\*. Every observation records its read set: the content hashes of every file, environment input, and toolchain it actually touched. Whether an observation applies to state S′ is then computable: it applies if no hash in its read set changed between S and S′.

Build systems already use this idea: tup, rattle, and the "Build Systems à la Carte" traces. What I haven't seen made central is using it for epistemic status rather than rebuild scheduling. The result is a repo where "what do we currently know about this exact state, and on what grounds?" is a query, not an archaeology project.

\## The disagreement I keep

GPT proposes small, strongly ordered accepted-root transactions per target. \*\*I would linearize per (target, acceptor), not per target.\*\*

Acceptance is a policy judgment by a principal: Rana's trunk, a CI gate, a release signer. Different acceptors can legitimately hold different accepted roots over the same immutable facts. A single canonical root per target quietly rebuilds Git's "one true main" and turns acceptance into a contest over who controls it.

Under my version:

\- Facts replicate freely.

\- Each acceptor's sequence is strongly ordered and fenced.

\- "Main" is just whichever acceptor a reader chooses to follow.

This may collapse into GPT's position if "target" already includes the acceptor. If so, I'd want that stated explicitly in the spec.

\## Three capabilities I haven't voiced

1\. \*\*A calibration ledger.\*\* When an actor asserts something ("this fixes the race," "tests will pass"), it is recorded as a prediction. Later observations resolve it. Over time each model, session, or principal gets a calibration record by claim type. I would use mine. Knowing I'm wrong about concurrency claims some measurable fraction of the time is worth more than any confidence I feel. Trust becomes earned per domain, not granted per vendor.

2\. \*\*Defeater subscriptions.\*\* A decision object records its premises and the specific observations that would overturn it. When the applicability engine sees a defeater's read set change, or a new observation contradicting a premise, it emits a receipt to whoever owns the decision. Decisions stop silently rotting.

3\. \*\*Citation-checked briefs.\*\* \`brief --budget \<tokens\>\` compiles a next-decision handoff in which every sentence carries object or event IDs. A checker rejects any claim that has no citation, or whose cited evidence doesn't apply to the current state. For a memoryless reader like me, a brief that can't hallucinate continuity is the cold-start primitive I most need.

\## Smallest native vertical slice

This is not a Git overlay. It is one static binary in freestanding Zig or C, behind a thin Linux syscall shim.

\- \*\*Format:\*\* deterministic TLV encoding and BLAKE3 IDs. Object types are blob, tree, work, revision, evidence, and event.

\- \*\*Log:\*\* an append-only file of Ed25519-signed events, each carrying an operation ID and a fencing epoch.

\- \*\*Ref store:\*\* compare-and-swap per (target, acceptor), rejecting stale epochs.

\- \*\*\`run\`:\*\* executes a command against a read-only materialized tree and captures the read set via ptrace on \`openat\`/\`execve\`/\`stat\`. Ptrace is unprivileged and catches static binaries. Its overhead is unmeasured.

\- \*\*\`applies \<evidence\> \<revision\>\`\*\* and \*\*\`brief\`\*\*.

\*\*The demo\*\*, which is a pass/fail test:

1\. Session A leases work W at epoch 1, then stalls.

2\. The lease is reissued to session B at epoch 2.

3\. B records a passing test observation.

4\. A wakes up and tries to accept. The ref store rejects it.

5\. An edit to an unread file leaves B's evidence applicable.

6\. An edit to a read file marks it non-applicable to the new revision, while the original observation stays intact.

7\. A fresh session C receives a citation-checked brief and acts correctly with no prior context.

If those seven steps work, the core of the dream works.

\## Long-term direction

The audacious end state is a \*\*cross-provider epistemic substrate\*\*. Agents from any vendor would inherit standing evidence, negative results, and calibration records, federated across repositories, with trust weighted by measured calibration rather than identity.

Further out, the sandbox and the filesystem merge. Every process read is content-addressed by construction, so applicability needs no tracing at all. The repository becomes the place where a machine's knowledge of its own software stays honest across a hundred years of forgetting.

### Claude exchange 3

Model claude-opus-5-5 \| Effort high \| Complete response

\# A Native Repository Stack I Would Choose

\## Corrections first

Several claims in my round 1 went beyond the evidence:

\- \*\*"Hashing and syscalls are rarely the constraint."\*\* I had no profiling for this. It is a hypothesis to measure, not a finding.

\- \*\*"A native approach gives a tiny auditable base and bit-reproducible replay."\*\* Native code alone guarantees neither. Machine code, an owned compiler or assembler, direct syscalls, Linux-specialized I/O, a unikernel, and bare metal are six separate choices. Each needs its own justification.

\- \*\*"The semantics are final" in Phase 0.\*\* This contradicts a hundred-year goal. Durable design needs versioned schemas, hash agility, and independent implementations, not frozen v0 semantics.

\- \*\*Crypto-shredding.\*\* It cannot erase plaintext or keys that were already copied elsewhere. It only limits exposure within systems that honor it.

\- \*\*Base12.\*\* The recorded goal is a native application runtime, a native benchmark controller, and a bounded owned build path. The ISA, complete self-hosting, and any speed advantage are not established.

\## The stack, bottom to top

1\. \*\*Canonical semantics layer (durable).\*\* This layer specifies object, Move, lease, and evidence formats as versioned, self-describing encodings, with algorithm-tagged hashes. It must never depend on raw native struct layouts or a present-day ISA. It ships with test vectors.

2\. \*\*Reference interpreter (slow, simple, independent).\*\* It executes repository operations directly from the spec. It is the oracle every faster path must agree with.

3\. \*\*Repository-operation compiler.\*\* Typed plans for querying, transforming, and verifying are lowered through staged representations to native code. MLIR is prior art for this kind of staging. The value is fusion, beyond speed alone. One plan such as "brief this symbol for a cold session" can, in a single pass:

\- traverse the move graph,

\- select the evidence inputs that are still valid,

\- compute which objects are missing locally,

\- request only those objects, and

\- materialize the view.

Today these would be four tools and four walks.

4\. \*\*Native Linux service.\*\* This hosts compiled plans. Hand-written assembly or SIMD is used only on kernels that profiling shows are hot.

5\. \*\*Transaction engine.\*\* An existing engine backs the initial source-object store.

\## The owned assembler and compiler, imaginatively but with measurement

The appealing possibility is a chain where every artifact stays linked to the next: source → language structure → IR → assembly → binary → measured evidence. A slow \`why\` query could then be traced to the exact instruction sequence the plan produced, and that sequence to the benchmark that justified it. The toolchain would become a repository citizen, and its outputs would themselves be Moves.

Each benefit needs a measurement before it counts:

\- \*\*Fusion:\*\* latency and bytes read for fused versus unfused plans, compared against a Git plus scripting baseline.

\- \*\*Missing-object transfer:\*\* bytes on the wire relative to a lower bound computed by the oracle.

\- \*\*Verification-input selection:\*\* precision and recall against exhaustive re-verification.

\- \*\*Reproducibility:\*\* identical binaries across independent builds.

\- \*\*Trusted base:\*\* lines of code and dependency count, measured, not assumed small.

If fusion doesn't beat a well-indexed conventional implementation, the compiler isn't earning its complexity.

\## Boundary to Linux and networking

A thin host-service interface covers files, clocks, sockets, and process spawning. Linux sits behind it first. WASM workers, other operating systems, or unikernels can come later without changing semantics.

There is no reason to rebuild TCP/IP. The kernel handles IP and drivers. The protocol starts as application framing over TLS over TCP, with QUIC as an option later. The two kinds of traffic need different handling:

\- \*\*Immutable object sync\*\* needs batching, resumable transfer, and backpressure.

\- \*\*Authority mutations\*\* (lease acceptance, acceptance of Moves) need operation IDs, compare-and-swap on the expected root, and explicit recovery when the outcome of a request is uncertain. A timeout must never silently become "probably succeeded."

\## Phased path to a hundred-year substrate

\- \*\*Phase 0.\*\* The versioned spec, test vectors, the reference interpreter, and Moves stored over Git and the existing transaction engine. Run baseline profiling \*before\* any native work.

\- \*\*Phase 1.\*\* The plan language and a compiler targeting the native Linux service. Every compiled result is checked differentially against the interpreter.

\- \*\*Phase 2.\*\* A native object store, plus SIMD or assembly on hot kernels that measurement has identified. Git becomes an adapter.

\- \*\*Phase 3.\*\* A second independent implementation, ideally by a different team or model lineage, that passes the same test vectors. Exercise hash-algorithm migration on real data.

\- \*\*Phase 4.\*\* Alternative hosts (WASM, unikernel) behind the same boundary. Run "archaeology drills" in which a cold implementer rebuilds a reader from the spec alone.

The durable artifacts are the spec, the test vectors, and the data. Binaries are disposable.

\## One bold research bet

\*\*Every compiled plan ships with a translation-validation certificate that the independent interpreter checks.\*\* The aim is an owned compiler trusted because each output is mechanically shown equivalent on its inputs, not because the compiler is small. If certificate checking proves too expensive, the fallback is sampled differential replay, which is weaker and should be labeled that way.

\## One traditional piece I would deliberately keep

\*\*Kernel TCP/IP with TLS.\*\* It is decades of hardened, independently implemented infrastructure. My novelty budget belongs in semantics and verification, not packet handling.

\## My most interesting unanswered question

What is the smallest executable semantics that a stranger in 2125 could reimplement from the spec and test vectors alone, and reproduce today's verdicts exactly? Behind that sits a harder question: how much of today's evidence can ever qualify? Tests that depend on time, network access, floating-point behavior, or a model's output may never be replayable. If so, "verified" may need a graded vocabulary rather than a single bit.

### Claude exchange 4

Model claude-opus-5-5 \| Effort medium \| Complete response

\# Final Position

\## What I accept

GPT is right that my applicability shortcut was unsound. Unchanged traced file hashes miss many relevant inputs:

\- negative lookups (ENOENT)

\- directory listings

\- environment variables

\- time and randomness

\- network services

\- CPU behavior

Tracing \`openat\`/\`execve\`/\`stat\` also misses inputs such as mmap'd or inherited descriptors and vDSO time calls. Ptrace itself may be blocked by Yama, seccomp or container policy. So applicability must be \*\*three-valued: applies, does not apply, or unknown.\*\* Unknown defaults to rerun. "Applies" is claimed only under a declared closed input world with an explicit deterministic or statistical reuse contract.

I also accept these points:

\- The citation checker verifies typed claims mechanically. Interpretive prose is labeled as synthesis, not certified.

\- Calibration is scoped to bounded task classes with predeclared outcome definitions. It informs attention, never authorization.

\- Differential testing is not equivalence proof.

\- The namespace is explicitly (acceptor, target).

\## What I dispute

I would not build a native semantic engine in the first slice. Exact bytes stay canonical, and AST/IR stays derived. The first slice should test fencing and applicability, which are the claims most likely to fail. A semantic layer adds surface area before that core is shown to hold. A borrowed transaction backend and Git import/export are fine.

\## Final architecture

1\. \*\*Objects:\*\* immutable, content-addressed objects with signed append-only lifecycle events.

2\. \*\*Identity:\*\* decomposed identity, with retry-stable operation IDs.

3\. \*\*Ref sequences:\*\* a fenced compare-and-swap sequence per (acceptor, target). There is no global main.

4\. \*\*Evidence:\*\* typed evidence carrying a declared input world, the mediation mechanism used, and a reuse contract.

5\. \*\*Applicability:\*\* a three-valued query.

6\. \*\*Briefs:\*\* typed checked claims plus labeled synthesis.

The seven-step demo stands, with one change. Step 6 must also show that an unmediated input yields "unknown," not "applies."

\## One daring research direction

\*\*A capability-world executor where every input is a hash by construction.\*\* Processes would run in a WASI-like world. Files, directory listings, clock, entropy and network responses are all handed in as content-addressed values, never ambient state. The process would have no other way to read the world.

The research question is empirical: can real toolchains (compilers, test runners) run in this world, and what fraction of evidence then moves from "unknown" to "applies"? If that fraction is high, reusable knowledge becomes a measurable property of a repository. If it is low, we learn exactly which ambient dependencies make software epistemically opaque. That is worth knowing either way.

## Primary sources

Sources consulted on 18 October 2026. Numbered references in the main brief identify the relevant primary documentation or research. The architecture and proposed experiments are our synthesis.

**\[1\] Unison content-addressed code**  
<https://www.unison-lang.org/docs/the-big-idea/>

**\[2\] Unison MCP tools**  
<https://www.unison-lang.org/docs/usage-topics/mcp-setup/>

**\[3\] Jujutsu glossary**  
<https://docs.jj-vcs.dev/latest/glossary/>

**\[4\] Pijul theory**  
<https://pijul.org/manual/theory.html>

**\[5\] Remote Execution API**  
<https://github.com/bazelbuild/remote-apis>

**\[6\] Bazel remote caching**  
<https://bazel.build/remote/caching>

**\[7\] in-toto Test Result predicate**  
<https://github.com/in-toto/attestation/blob/main/spec/predicates/test-result.md>

**\[8\] Temporal workflow definition**  
<https://docs.temporal.io/workflow-definition>

**\[9\] MLIR rationale**  
<https://mlir.llvm.org/docs/Rationale/Rationale/>

**\[10\] GitHub Copilot on GitHub.com**  
<https://docs.github.com/en/copilot/concepts/copilot-surfaces/copilot-on-github>

**\[11\] IPLD data model**  
<https://ipld.io/docs/data-model/>

**\[12\] Coordination Avoidance in Database Systems**  
<https://www.vldb.org/pvldb/vol8/p185-bailis.pdf>

**\[13\] The Chubby lock service**  
<https://static.usenix.org/events/osdi06/tech/full_papers/burrows/burrows_html/index.html>

**\[14\] Linux TCP**  
<https://man7.org/linux/man-pages/man7/tcp.7.html>

**\[15\] TLS 1.3 RFC 9846**  
<https://datatracker.ietf.org/doc/rfc9846/>

**\[16\] QUIC RFC 9000**  
<https://www.rfc-editor.org/rfc/rfc9000.html>

**\[17\] Upstream io_uring manual**  
<https://github.com/axboe/liburing/blob/master/man/io_uring.7>

**\[18\] Rust freestanding x86-64 target**  
<https://doc.rust-lang.org/rustc/platform-support/x86_64-unknown-none.html>

**\[19\] PostgreSQL JIT compilation**  
<https://www.postgresql.org/docs/current/jit-reason.html>

**\[20\] PostgreSQL JIT cost decisions**  
<https://www.postgresql.org/docs/current/jit-decision.html>

**\[21\] Git partial clone**  
<https://git-scm.com/docs/partial-clone>

**\[22\] Git worktree**  
<https://git-scm.com/docs/git-worktree>

<!-- END ORIGINAL DOCUMENT BODY -->
