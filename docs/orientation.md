# Understanding Continuum

Continuum's purpose is to let AI engineering continue coherently when the conversation, model, worker, or machine changes. A source tree tells an agent what exists. Continuing work also requires knowing what was attempted, which result was accepted, why a decision was made, what remains uncertain, and what to do next. This project develops native representations and operations for that larger unit of work.

This guide explains the current design. [CURRENT.md](../CURRENT.md) remains the authoritative current-status entry point, and the [mission](../MISSION.md) and [roadmap](../ROADMAP.md) describe the purpose and intended sequence.

## Two related things

The public GitHub repository contains the project that builds Continuum: Rust source, tests, documentation, experiments, and collaboration records. It already gives our research Chat and Codex tasks a shared durable place to work.

The Continuum program being built is a separate native engine. It stores exact objects, records local acceptance transitions, prepares context, and verifies references. Its runtime has no Git dependency. Future Git import/export would connect it to existing source workflows without making a Git commit the only possible unit of work.

Using GitHub to construct and evaluate the engine keeps the project usable today. Whether a richer native engine improves real continuation is an experimental question. The [native-core decision](decisions/0001-native-core.md) retains the strongest simpler alternative: permanent Git source authority with better task and context tooling around it.

## The durable unit: an investigation

Consider an agent fixing a bug. It needs the source, but it may also need the failed reproduction, the rejected hypothesis, the exact test environment, a proposed patch, a pending integration request, and the reason another approach was abandoned. A second agent should be able to recover those distinctions without replaying the entire first conversation.

The architecture therefore distinguishes three kinds of relationship:

| Graph | What it connects | Why an agent needs it |
|---|---|---|
| Artifacts | Exact source, inputs, outputs, snapshots, and manifests | Identify and retrieve the bytes actually discussed or executed. |
| Work | Objectives, attempts, decisions, alternatives, and handoffs | Recover intent, unfinished responsibility, and the next useful move. |
| Evidence | Observations, claims, supporting inputs, scope, and counterexamples | Decide what a result supports and when it should be reconsidered. |

These are the architectural direction, not three complete deployed databases. The current kernel implements a small portion; structured context records and project documents express more of the work above it. The [architecture](architecture/overview.md) separates implemented invariants from proposed records.

## Why the repository has these files

| Home | Job | Reason for keeping it distinct |
|---|---|---|
| `README.md` | Public entry point and navigation | A reader can find the relevant contract without reading the whole archive. |
| `MISSION.md` | Purpose and success criteria | Current experiments can change while the purpose stays intelligible. |
| `CURRENT.md` | Verified state, open limits, selected next unit | A successor has one place to orient; older reports remain historical. |
| `ROADMAP.md` | Phased capabilities and exit conditions | An aspiration is visible without looking like completed work. |
| `AGENTS.md` | Instructions for contributors | Models and people share the same working rules. |
| `CODEX_HANDOFF.md` | A complete startup prompt | A new implementation task gets the purpose, current mechanism, and continuation method. |
| `src/`, `tests/`, `examples/` | Executable implementation and checks | Claims about behavior can be exercised. |
| `schemas/` | Structured record contracts | Adapters can exchange explicit fields instead of inferring everything from prose. |
| `protocols/` | Selectable methods and a versioned registry | Procedures can improve and compose without becoming a second runtime or source of authority. |
| `docs/architecture/`, `docs/decisions/` | Behavioral design and consequential choices | The reason for a choice and its reconsideration condition survive a chat. |
| `docs/collaboration/` | Actual model inputs, replies, and corrections | A later reader can inspect what was supplied and where collaborators disagreed. |
| `docs/source-review/`, `docs/research-lessons.md` | Reading coverage and adaptations | Source acquisition, semantic reading, interpretation, and imported conclusions stay distinguishable. |
| `research/` | Exact runs, raw results, provenance, and trial assessments | A polished summary can lead back to the observations it summarizes. |
| `docs/history/` | Faithful historical briefs | Original aspirations remain available without overriding current evidence. |

Markdown serves as a readable, editable coordination layer today. It does not make every statement a verified fact. The native program's checks apply to the objects and operations it actually processes; project prose cannot acquire those guarantees by describing them.

## What the native core can do now

**Retain exact artifacts.** A Blob stores bytes. A restricted Snapshot names paths and references Blobs. A declared EvidenceRecord binds an asserted outcome and provenance to a candidate. Versioned encodings and domain-separated SHA-256 identities distinguish kinds and exact content. Linked snapshot/object hashes form a small Merkle DAG, useful for integrity and identity. Hashes do not establish truth, permissions, or consensus.

**Accept a change conditionally and recover its receipt.** A caller names an operation and the exact head and generation it expects. A local SQLite transaction either records the accepted transition or its failed precondition, and retains the result. Repeating the identical operation recovers its historical receipt. Reusing its identity with different content fails. The generation catches a state that changed away and later returned to the same root. This is the implemented local acceptance contract, not a general guarantee about remote APIs.

**Prepare inspectable context.** A WorkState records the objective, attempts, decisions, uncertainties, and an offered handoff. Preparation chooses complete records under an explicit byte budget and retains both the rendering and its manifest. Verification can check the historical projection and observe whether its accepted anchor is still current. A recipient acknowledgement binds references; identity, understanding, and actual external execution need additional evidence.

The most concrete motivation is two histories with identical source bytes. In one, an operation was never dispatched; in the other, it may have succeeded before its reply was lost. The correct next action can differ. A useful continuation record must preserve that distinction. The current WorkState displays authored dispatch claims with their limitations; a future instrumented runner must provide actual dispatch and reconciliation evidence.

## What Base12 and Prime Radiant contributed

The complete adaptation and source coverage live in [research lessons](research-lessons.md). Whole-repository reading is still incomplete. Base12 received substantial pinned-source review; Prime Radiant's accessible research kit was reviewed because its live checkout was not obtained. These sources informed original methods and engineering questions.

**Base12 contributed continuity through research records.** Progress briefs reconcile source and evidence at a stated cutoff. Decisions, negative findings, and open questions remain available after implementation moves ahead. A possibility graph can contain promising alternatives without turning all of them into execution prerequisites. Its existing Chat/Codex/GitHub pattern also supplies an immediate way for this project to continue across separate conversations.

**Prime Radiant sharpened the question of representation.** Which distinctions must a description preserve for a future decision? What does a lossy summary hide? Its retained research and correction records motivate exact input/output custody, explicit evidence scope, and preservation of failed or incomplete attempts. A successor should recover a genuine unresolved question rather than inherit an overly confident summary.

**Holographic Walk became a selective method.** Move between a local mechanism, its interfaces, and the larger objective, then return with a changed question, a missing constraint, or a counterexample. Its value is the concrete change it enables. Coherence across descriptions is not independent proof, and every task need not invoke it.

Together these lessons favor explicit artifacts, bounded context, typed relationships, actual counterpart responses, and honest coverage. They do not make another project's arithmetic, scientific hypotheses, compiler strategy, or private operating state requirements of Continuum.

## Other engineering choices

The design borrows familiar strengths: Git-style immutable snapshots and content identity; database transactions for local atomic acceptance; idempotency keys and receipts for retries; explicit state machines for uncertain work; build-system dependency thinking for future applicability; bounded queries for context. These mechanisms have different jobs. A Merkle DAG does not elect an owner, a dependency edge does not grant permission, and model provenance does not measure reliability.

Rust is the starting language for a small native implementation with explicit types, ownership, errors, and systems access. Mature SQLite and hashing code let us examine the new work model before building another storage engine. Portable object and behavioral contracts are the longer-lived commitment. Ordinary Linux and networking facilities can serve future adapters; a custom assembler, kernel, TCP/IP stack, or cryptographic implementation is not required to test this vision.

The [first measured release workload](../research/runs/release-baseline-2026-10-19/README.md) now gives a reproducible baseline for small local operations. It includes raw samples and exact conditions; it does not compare languages or demonstrate production capacity. Optimization should follow a measured limiting cost.

## How research and implementation operate today

The [operating method](operations/continuation.md) keeps research framing in the ongoing conversation, uses Codex or another actual code-capable task for implementation, and preserves their useful exchange in GitHub. A Research Delta records what changed, what was learned, negative findings, evidence and its limits, and the next action. The user need not shuttle every message.

Actual Claude reviews contribute another perspective at consequential decisions. Their visible responses and corrections remain inspectable. Dot becomes a coordinator only through a real supported task/host connection or acknowledged repository exchange. Scheduling, a running task, and verified progress remain separate observations.

## The longer vision

The [real-use pilot](experiments/real-use-pilot.md) makes Continuum itself the first consumer, followed by a small independent example. Its purpose is to discover useful design changes through actual handoffs, including missing context, awkward record shapes, unused material, and upkeep cost. A persistent workstation pilot needs exact build identity and a tested data-preservation path; current executor use is not a workstation deployment.

The next useful progression is to show better continuation on real work: a fresh session recovers the correct next action; an interrupted external attempt can be reconciled; another host receives exact artifacts and accepted responsibility; changed assumptions identify the decisions worth revisiting. Each step needs its own working mechanism and evidence.

Further out, an agent could ask for the smallest sufficient context for one decision, compare alternative investigations without merging them prematurely, reuse an observation only within its valid scope, and re-evaluate selected work when a new model or tool changes what is possible. A release could retain exact artifacts, compatibility, evidence, and accepted scope while development continues in other streams.

The strongest test is practical: does this preserve a decision-relevant distinction or avoid real repeated work better than a simpler GitHub-and-notes baseline? If it does, deepen the mechanism. If it does not, simplify. The mission is continuing useful engineering, and the repository's structure should remain accountable to that outcome.
