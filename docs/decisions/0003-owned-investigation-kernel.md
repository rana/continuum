# ADR 0003: select an owned native investigation kernel as the successor target

Status: selected clean-slate development design under Rana's renewed design autonomy; not an implemented or qualified replacement.

Date: 2026-10-19 UTC.

Design owner: current Chat coordinator. This record assigns no external worker and does not rename a repository, redirect an active task, migrate data, change schedules, or replace the current Rust/SQLite runtime.

## Question and actual starting point

Rana asks whether we own storage, why the overnight work remained on Rust/SQLite, and what we would build from a clean slate for an AI-native source and scientific-work repository. Fresh main `416e41f8f9a009f02fb20152d67f0c74bbef606a`, Cargo.toml and src/store.rs confirm SQLite-authoritative persistence. We own the domain encodings, schema, object/acceptance semantics and integration code, not a project-designed pager, WAL or physical recovery implementation.

[ADR 0002](0002-owned-storage-research.md) authorized ownership research but did not deliver an owned engine. Keeping the working reference was sound; allowing that reference and peripheral research to become the default destination is a work-allocation risk. This successor design makes the owned kernel an explicit construction target rather than an optional direction waiting for SQLite to lose a speed comparison. Qualification for retained data remains a different decision.

The review began at `416e41f`; publication preparation reconciled through `c474b0dc9e6f4732d22a1c3f2f4da20df415a2cd`, the merge of PR #109. Its fair-exposure/retrieval bridge is complementary and retains its existing owner. Its tests and eventual model trial do not establish an owned storage implementation. No native tests were rerun for this design review. A fresh container Git read failed DNS resolution; connected GitHub reads/writes are the available publication route.

## Product, not just a storage project

Build a native repository for continuing investigations: exact editable source, alternative proposals, experiments and inputs, observed outputs, claims with scope, rejected approaches, accepted decisions and responsibility. Context packs, Markdown reports, search indexes and Git exports are views/interfaces to the repository, not its whole purpose.

The product must still be a real source repository. Materializing a working tree, diffing candidate states, retaining ancestry, proposing competing changes and integrating an exact checked result remain capabilities to build. The native source model must explicitly encode or reject unsupported filesystem features; restricted v1 Snapshots are not complete Git fidelity. A hypothesis branch and a source branch are related, not interchangeable. Textually compatible changes need not be semantically compatible. Acceptance records the authorized chosen result, not scientific truth.

The scientific part is equally essential: failed and untested hypotheses remain distinguishable, an old observation is retained within its original scope, disagreement is not flattened into consensus, and a changed premise creates a review candidate rather than rewriting history. Exact source custody cannot guarantee semantic completeness or reproduction from missing environments.

## Selected architecture

### 1. A small generic persistence kernel, written initially in Rust

The required authoritative storage path will be project-owned and will not depend on SQLite or Git. Keep the current Rust/SQLite binary as a separately identified reference, not as a second independently writable authority for the same successor workspace. Rust is an implementation choice, not an excuse to retain SQLite and not a claim of owning instruction emission.

Own bounded framing, object persistence, commit selection, atomic acceptance outcomes, historical receipt lookup, recovery behavior, consistent export/import and derived-index reconstruction. Borrow established cryptographic hashing, ordinary Rust tooling and standard OS/filesystem primitives with disclosed assumptions. Do not make a new compiler, allocator, filesystem, network protocol or cryptographic primitive prerequisite to owning these mechanisms.

Use one writer at a time per local repository with real process exclusion and explicit startup/recovery ownership. The first version need not be a resident daemon. Reads observe a specified committed generation with a defined lifetime. This changes the topology from unrestricted independent writers and must be included in any comparison; it does not remove coordination.

One journal/segment family initially retains both immutable object payloads and complete acceptance outcomes within one persistence protocol. Do not split authoritative object files from a separate metadata database before object-before-acceptance, backup, recovery and reclamation ordering are specified. Start with reconstructible in-memory maps. Later on-disk indexes are caches; deleting them must not delete history. Optional third-party analytics/search may live outside authority, but SQLite is not required by the initial successor path.

This is deliberately not a general SQL or graph database. A small append kernel does not become correct merely because it is small. Full framing/commit selection and failure rules remain to be specified and exercised before claiming an engine exists.

### 2. A versioned investigation model above the kernel

Keep hypotheses, experiment schemas, evidence interpretation and scientific policies out of the short durability transaction. The kernel validates canonical bytes, declared structural references, kinds required by the acceptance contract, request binding and atomic head changes. Domain validators check meaning and record-schema obligations above it. An opaque payload requires an explicit canonical reference manifest if the kernel is to verify its declared closure; this does not prove the manifest captures every semantic dependency.

Start with exact artifacts, source states, attempts/observations, claims/assumptions and decisions, allowing ordinary text and unknown attachments rather than demanding a universal ontology. Add types only for relationships whose semantics affect actual work. Preserve separate content IDs and stable logical identities. Keep source ancestry, evidence/provenance and acceptance/authority ordering typed; do not assume that every useful reasoning relation is a DAG.

Retain current object IDs and acceptance contracts unchanged for compatible records. Any richer source model, envelope, policy binding or multi-head transaction must be explicitly versioned. Existing source snapshots must not silently acquire filesystem metadata or changed meaning.

### 3. Native work operations and interoperable edges

The product interface should let an agent retrieve exact objects, materialize source, propose a candidate, attach evidence, inspect alternatives and omissions, accept under exact preconditions, recover a receipt and export a self-contained closure. Prefer stable typed requests and bounded replies over requiring agents to parse a long status narrative.

Git is a compatibility and publication adapter, not a required hidden persistence backend in the successor workspace. GitHub can remain the development host for the program's source. Those are different uses of Git. When existing GitHub source remains authoritative, import it explicitly; do not pretend that both GitHub and the native workspace can independently own the same head. Experimental successor data stays in isolated native-authoritative workspaces until an explicit integration contract is qualified.

A minimal named proposal/head and exact snapshot diff belong early; a general automatic semantic merge engine does not. Use existing editors, builds and diff/merge algorithms where appropriate. Any integrated candidate must be checked at the actual combined source state, not authorized solely by its components' old green results.

### 4. Evidence-scoped review, not automatic truth or dispatch

A promising next capability follows explicit dependencies when a premise, environment binding or observation is corrected. Emit an advisory review record naming the changed premise, affected decision and original evidence. Begin with bounded equality/version/retraction conditions, not arbitrary scripts or slow inference inside acceptance. Historical validity, current applicability and authorization remain separate.

No notification event wakes a model by itself. Actual dispatch requires a verified host integration and its own authority, idempotency/finality and outcome-reconciliation contract. Hold an uncertain external effect without blocking independent analysis or unrelated work. Do not capture hidden chain of thought or imply transcript/state identity across models.

## Persistence obligations and evidence limits

Preserve exact historical retries after head movement; reject changed-request reuse of an operation identity; retain both accepted and stale outcomes; preserve the explicit global acceptance sequence without counting object insertions or retries; keep required source/object closure intact.

A successful write call, digest or commit marker is not by itself a complete durability protocol. Recovery cannot know which response a caller observed. A committed operation whose reply was lost may legitimately survive. Conversely, a malformed final record can be torn uncommitted data or damage to previously acknowledged history. Do not automatically truncate it based only on being last or having a bad checksum.

The implementation must specify how an admissible committed boundary is established under each declared fault model, preserve ambiguous evidence, stop unsafe writes on uncertain I/O/sync outcomes, and separate integrity refusal from successful recovery. Reading surviving bytes after an error is not a general proof of their stable durability. Fail-closed behavior has an availability cost; refusal of all states is not success.

Fault tests include partial writes, failed synchronization, missing/corrupt boundary metadata, damaged earlier records, process exit before/after commit, lost response, writer contention and exact retry. Simulated faults and process termination are not physical power-loss proof. Export/restore must reconstruct independent state and original receipts; lifecycle version support, growth, replay cost and later compaction cannot be concealed as solved. Begin without compaction, garbage collection, network service or replication, and make growth limits visible.

## Next implementation unit and completion boundary

Next unit: implement the smallest disposable owned journal with its stated framing/commit rules, a separately formulated in-memory acceptance oracle and independently implemented reader. This is the selected successor construction unit, not a mandate to keep producing design-only finite models indefinitely. No external implementer has accepted it; the active coordinator must reconcile actual ownership before assigning or editing overlapping code.

The first coherent demonstration must put exact source objects, retain two competing approaches and the failed approach's evidence, accept one exact candidate, terminate a process after durable commit before reply, restart from repository bytes alone, and recover the original receipt without reapplying acceptance. Exercise changed-request reuse, stale acceptance and malformed/corrupt input controls. Export without overwrite and restore to a fresh directory. Check outcomes against the independent oracle and the separately executed SQLite reference under the same declared contract; never dual-write competing canonical states.

Then use that native repository for one real continuation of its own development, followed by a distinct small public investigation. Start on one verified host; a real second host is a later capability, not an invented prerequisite or a claimed installation. Preserve fresh recipient input exposure and actual consequence. Reuse the ongoing fair-comparison work rather than duplicating it or interpreting its current formatting study as a storage benchmark.

Success criteria are independent: contract correctness, useful continuation at total preparation/retrieval/maintenance cost, and worthwhile control/reviewability. An owned implementation can be correct yet not be the right product; a helpful schema can be valuable without proving a custom engine faster. Neither a speed threshold nor abstract novelty is required to begin the selected ownership work. Retained-data adoption requires evidence, recoverable prior data and explicit lifecycle support.

## Alternatives and balance points

Continuing on SQLite is the lowest-risk practical reference. It remains appropriate for current retained evidence, but is not the selected successor authority. Replacing SQLite with another off-the-shelf database changes a dependency rather than meeting this ownership objective. Writing everything in assembly would conflate domain, storage and emission risks. An independently emitted verifier remains a separate bounded target once its input/checking contract is stable; it is not required to begin the owned journal.

A native repository limited forever to context notes would miss the original source-repository ambition. A universal forge, scheduler, semantic merge engine and scientific ontology would exceed the useful first slice. The balance is owned facts/bytes and atomic transitions, replaceable projections/tools, and a genuinely useful investigation workflow.

## Repository and research-work transition

A clean architecture does not require erased history. Keep current evidence and the SQLite reference recoverable. A separate successor source repository can be justified by a genuinely distinct build root and ownership contract, but merely being prepared to rename is not an instruction that the rename has occurred. No repository rename or new repository is executed here.

Before any eventual cutover, reconcile actual owners and remote URLs/IDs, pin predecessor source/evidence, verify new permissions and CI, and establish one authority per active target. A lease expiry does not prove an old writer stopped. GitHub warns that reusing a renamed repository's old name removes redirects; do not rely on redirects to transfer ownership or keep historical references correct.

This ADR records a successor target, not another live dashboard. CURRENT remains the authoritative capability/active-unit record; the ongoing retrieval/trial owner's accepted scope is not silently reassigned. The next reconciliation should distinguish that active practical unit from this newly selected successor construction unit, not report the latter as implemented.

## Collaboration, corrections and provenance

Two actual supplied-context Claude Opus 5.5 turns completed at medium effort, adaptive thinking, text-only, no server memory, end_turn and no truncation. Exact request field values, visible responses and metadata are retained in [the collaboration record](../collaboration/2026-10-19-clean-slate.md). Reported usage is 2,633/3,602 input/output tokens in turn one and 2,611/3,753 in turn two. Agreement is design review, not experimental evidence.

Adopted: product-first reset, select owned authority now, Rust independent of SQLite, small generic kernel, independent checks, explicit separation from durable deployment. Qualified: optional SQLite indexes are permissible outside authority, not a required successor dependency. Disagreed: a blanket one-year delay for native branches/integration is arbitrary and too restrictive; retain simple named proposals early and defer general semantic merge.

Corrections retained: Rust is not literally runtime/dependency-free; a boundary record alone does not solve recovery; no blanket novelty versus Git/notebooks/workflow systems is established; a repository event is not a dispatched agent. Turn two's unconditional torn-tail truncation/read-only-recovery categories remain too strong without a verified recoverable boundary; this ADR does not adopt them. Its fsync-specific OS explanation and extra crate suggestions were not independently qualified here and are not selected dependencies. The existing SHA-256 identity is not switched to BLAKE3. Read-only access to partially corrupt state must state which observations are actually verified.

Public source/primary references inspected: Cargo.toml and src/store.rs at the initial pin; MISSION, AGENTS, CURRENT, ADR0002 and continuation method; original user transcription in the retained design brief; PR105 actual comments and PR109 metadata/reconciliation. External references were checked before the two calls: [SQLite architecture](https://www.sqlite.org/arch.html), [Rust code generation](https://rustc-dev-guide.rust-lang.org/backend/codegen.html), and [GitHub renaming](https://docs.github.com/en/repositories/creating-and-managing-repositories/renaming-a-repository). No private Base12/Prime Radiant payload or unpublished operational state is included.
