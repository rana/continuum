# ADR 0003: Build an AI-native scientific repository with an owned storage authority

**Status:** accepted **development target**, not an adopted durable store or a completed implementation  
**Date:** 2026-10-19 America/Los_Angeles  
**Baseline reviewed:** `c474b0dc9e6f4732d22a1c3f2f4da20df415a2cd`  
**Design authority:** Rana's renewed clean-slate/AI-native direction and standing design autonomy; integration owner for this ADR is the contributing Chat coordinator.

## The question we are actually solving

The original Scion-inspired question was whether agents should have a public, MIT, AI-native *scientific code repository*, rather than another chat summary facility. The current project owns canonical object formats, work/evidence semantics and local acceptance rules, but `src/store.rs` persists through `rusqlite`, SQLite tables, WAL and the SQLite pager. We **do not currently own** the physical storage engine or its recovery algorithm. The distinction is material, not a terminology dispute.

The central product is a **repository of continuing investigations**. A useful repository binds a versioned code tree to a question, competing hypotheses and implementations, exact attempts, observations under declared environments, negative findings, decisions, and their reconsideration conditions. A source tree, work history and evidence relationships are distinguishable projections, not one untyped graph. An agent must recover what happened and what remains actionable without an earlier chat or the user carrying messages between workers. The source-tree part remains real: editable contents, lineage, diff, candidate review and accepted integration must be addressable, even if the first editing adapter is Git.

Historical validity, current local acceptance, applicability of a scientific conclusion, authorization of an effect and actual effect confirmation remain five different claims. No digest, model agreement or evidence citation collapses them.

## Decision: advance owned authority into implementation, without premature activation

**Select a minimal project-owned persistence authority as the next architectural development target.** Do not leave it indefinitely as an optional benchmark response to SQLite. Design ownership, inspectable recovery and an exact portable evidence contract are legitimate objectives even when SQLite is performant. This is a **target choice**, not a finding that an alternative already works or should hold the user's retained data.

Start with a small Rust implementation because it can express the domain contract, native file I/O and explicit failure paths without a VM or GC. This does **not** own the Rust compiler/backend, runtime services, kernel, filesystem or cryptography. Language and emission remain replaceable behind the versioned format and conformance fixtures; a different language is not prerequisite to owning storage.

The first owned authority is **one local append-only record domain** containing immutable canonical object insertions and complete accepted/stale acceptance outcomes. A single local writer is serialized with explicit cross-process exclusion and recovery ownership; no daemon, remote coordinator or replication is initially required. Indexes (object lookup, current heads, historical operation receipts, target events) begin as rebuildable in-memory projections. Any later SQLite, embedded KV or search system may provide disposable derived indexes, never a second authoritative writable home. Keep canonical IDs unchanged for v1 unless a future explicit versioned contract requires otherwise.

Use a narrowly specified bounded framing and commit/recovery protocol, including version, record kind, lengths, integrity coverage, accepted-prefix selection and startup/recovery rules. File write, successful synchronization, publication, returned acknowledgement and downstream effect are separate events. A checksum and a terminal marker alone are not proof of durable recovery. Fail closed when an ambiguous image cannot be classified; count integrity refusals as an availability cost. Prevent readers from consuming a not-yet-committed tail.

**Preserve the operational SQLite implementation unchanged as the reference and safe home of any existing retained trial state.** Test the owned candidate on isolated, disposable stores. Compare common traces against a separately formulated oracle and the actual SQLite reference. Never dual-write as though two different stores are one accepted authority. There is no silent migration, new production backend, scheduler, repository rename, external model dispatch or workstation installation in this decision.

The owned storage kernel is deliberately ignorant of hypotheses, scientific truth and external authorization. It stores and verifies bounded opaque canonical objects, checks required object closure/kinds, enforces conditional local acceptance, and returns receipts. Versioned investigation schema, citation/dependency graph, evidence-scope review, and model context selection live above it. Host permissions and effect admission sit outside it. No Git push, model call or notification fires as an implicit consequence of an append.

## Preserve the existing semantics exactly

The development target MUST preserve the versioned, domain-separated exact canonical object ID and object-kind checks; complete expected root **and generation** for the CAS precondition; canonical request binding to the operation ID in its acceptor namespace (including target); permanent changed-request reuse rejection; identical historical receipt on exact retry even after later head movement; durable **accepted and stale** outcomes; one monotonically increasing database-wide acceptance sequence allocated only for new evaluated acceptance operations. Object insertion and exact replay consume **no** acceptance sequence number. A journal offset or all-frame ordinal does not replace that sequence. Preserve the existing candidate source closure, and expose absent dependencies rather than inventing them.

An operation may have committed even when its reply was lost. An invalid/ambiguous recovered image does not license a fresh retry. Independent remote Git, model and tool effects need their recipients' *actual* finality/idempotency/receipt guarantees; a local operation key alone cannot make them exactly once.

## What the first implementation must demonstrate

**A. Exact finite model, independent oracle, deliberate mutants.** Enumerate declared bounded traces with competing acceptors, stale and accepted outcomes, ABA generations, retries after later head movement, changed operation-ID reuse, interrupted write stages, missing closure and ambiguous commit boundaries. Retain exact smallest counterexamples to intentionally wrong rules. Measure model coverage and integrity refusal separately from correct recovery; do not label finite enumeration hardware durability.

**B. Bounded Rust-owned shadow authority with an independently implemented read-only decoder.** Write the framing specification *before* trusting the on-disk bytes. Start with an isolated simple file layout and fixed limits; explicitly state OS/filesystem/sync assumptions and startup writer-exclusion policy. Test faults at write, barrier, segment creation, metadata publication, read and interruption boundaries. Test a layer that can discard unsynced writes, not merely process termination. Distinguish a torn uncommitted tail (only when the fault model makes it unambiguous), acknowledged-prefix damage and missing/corrupt commit metadata. No automatic truncation of ambiguous data; retain the forensic input. Report safety and availability. A different decoder implementation sharing only the format contract must inspect bytes without importing writer parser code.

**C. Three-way same-trace comparison.** Run the independent oracle, SQLite reference and shadow implementation on exact common traces. Compare canonical bytes, heads, event sequences and receipts. Seed mutations that drop stale receipts, allocate an event on an exact retry or mix operation IDs. A mismatch blocks adoption, not an opportunity to rename incompatible behavior an optimization. Reuse the existing test suite where applicable, but source-code similarity among oracle implementations is a known common-mode limitation.

**D. One actual scientific source/work continuation.** Use an identified source snapshot and two competing approaches; preserve a negative result and evidence; accept one verified candidate; interrupt and recover a local acceptance; export exact closure into another disposable directory and independently verify receipt/query results. Then give a fresh receiver an explicitly limited context and measure its next correct action against *good Git/Markdown notes*, including authoring/retrieval effort. Same-host process recovery comes first; cross-host and actual independent model continuation require observed executor availability and are not silently claimed. The real-use three-arm study remains owned by its current worker; do not duplicate PR #110's receiver or uncertain model invocation.

This work is **not done** because we created an ADR. No owned journal or native emitter is established by this change. The next implementation worker starts with A, then a small B prototype as soon as A can discriminate defects. More model prose cannot replace real byte custody and fault experiments.

## Deliberately borrowed layers and deferred work

Borrow well-established hashing and integrity libraries, system I/O primitives, file locks and test tools. Do not design new cryptography or a filesystem. Git remains a public distribution/editing/interop edge initially; native source identity and investigation records must nevertheless be the product's own semantics. Full native branch/rebase/merge, network server, auth service, replication/consensus, general scheduler, machine instruction emitter and garbage collection remain separate questions. Native branch/merge may later be justified by real multi-agent integration workloads, not assumed away permanently. A narrow emitted read-only verifier is attractive but not a prerequisite for the first owned Rust storage prototype.

## Why this rather than a clean repository rename today?

A new repository name would not give us an owned engine, a verified migration or a better continuation experience. Keep `rana/continuum` and its historical baseline as the development host for now. If a genuinely different target later deserves the `Continuum` identity, preserve immutable source/evidence links, work owner acknowledgements, adapter remotes, workflows and GitHub redirect implications. Do not assume a renamed slug can be reused without breaking existing redirects. No repository rename or migration is authorized by this ADR alone.

## Alternatives, counterweights, and reopening conditions

The lower-risk alternative is to use SQLite indefinitely, adding a portable science-work protocol; this remains a valid comparator and potential eventual result. A full new database, monolithic compiler/emitter, universal graph/ontology and immediately replacing Git editing were rejected as first steps because they add unverified failure and integration surfaces.

**Main counterweight:** owning persistence creates a substantial durability and lifecycle tax with no presently demonstrated causal continuation gain. We accept that research burden deliberately, but will not relabel correctness failures, missing power-loss proof, poor backup/restore/upgrade behavior, growth/replay cost, unbounded integrity refusal, or inferior real use as successes. A meaningful ownership win can be control and reviewability, not only speed; it must be demonstrated on its own criteria. If the owned engine adds no worthwhile inspection, portability, operability, resource or scientific-work benefit over the maintained baseline, simplify or stop it. Do not rewrite retained stores while that answer is unknown.

This decision refines the *priority* of [ADR 0002](0002-owned-storage-research.md) and preserves its safety contract, fault-model limitations and adoption gate. It does not retroactively change the [ADR 0001](0001-native-core.md) implemented/validated baseline. The active human and agent authority remains outside the database.

## Collaboration, corrections, and owner

The associated [Research Delta](../../research/runs/owned-authority-target-2026-10-19/README.md) includes source pins, actual independent Claude Opus 5.5 critique, corrections and next owner. Claude specifically challenged shared-oracle semantic drift and fictitious one-append atomicity. Its proposed binary old/new recovery classification and definite negative commit reply are too strong under ambiguous corruption or lost acknowledgements; an explicit integrity/uncertain refusal is required as a third result. Nor can an operation key make a remote provider idempotent absent recipient guarantees.

This scoped ADR is integrated by the current Chat coordinator. The next code-capable worker is **not yet contacted or acknowledged**; it must reconcile active owner/work first and work only in a disjoint owned-kernel lane. PR #110's live real-use owner and current source-review work continue without an overlapping task or schedule change.
