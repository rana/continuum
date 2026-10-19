# ADR 0003: select an owned native investigation kernel as the successor target

Status: selected clean-slate development design under Rana's renewed design autonomy; not an implemented or qualified replacement.

Date: 2026-10-19 UTC. Design owner: current Chat coordinator. No external worker is assigned by this record. No repository, schedule, runtime or retained data is changed by the selection.

## Question, source and finding

Rana asks whether we own storage, why work continued on Rust/SQLite, and what we would build from a clean slate for an AI-native source and scientific-work repository. Fresh main `416e41f8f9a009f02fb20152d67f0c74bbef606a`, Cargo.toml and src/store.rs confirm SQLite-authoritative persistence. We own domain encodings, schema, object/acceptance rules and integration code, not a project-designed pager, WAL or physical recovery engine.

[ADR 0002](0002-owned-storage-research.md) authorized ownership research but did not deliver an owned engine. Keeping the working reference was sound; allowing it and peripheral studies to become the default destination is a work-allocation risk. This successor design selects owned storage as a construction target rather than an optional direction waiting for SQLite to lose a speed comparison. Qualification for retained data remains separate.

Publication preparation reconciled through `c474b0dc9e6f4732d22a1c3f2f4da20df415a2cd`, the merge of PR #109. Its trial exposure/retrieval bridge is complementary and retains its existing owner. No native test was rerun for this design review. A fresh container Git read failed DNS resolution; connected GitHub is the functioning repository route.

## Product: a repository for continuing investigations

Build a repository containing exact editable source, competing proposals, experiment inputs and outputs, attempted actions, claims with scope, rejected approaches, accepted decisions and responsibility. Context packs, Markdown reports, search indexes and Git exports are views and interfaces, not the entire product.

Source control remains real: materialize a tree, inspect differences and ancestry, retain named proposals, and integrate an exact checked result. Explicitly encode or reject unsupported filesystem features; restricted v1 Snapshots are not complete Git fidelity. A hypothesis branch is not automatically a source branch, and a textually clean merge is not established semantic compatibility.

Preserve failed versus untested alternatives, disagreement, and historical observations within their tested scope. Acceptance records the authorized chosen state, not scientific truth. Changed premises produce review candidates without rewriting old evidence. Exact bytes do not guarantee complete context or reproduction from missing environments.

## Selected architecture

### Small project-owned persistence kernel, initially in Rust

The successor's required authoritative storage path has no SQLite or Git dependency. The existing Rust/SQLite binary remains a separately identified reference, not a second independently writable authority for the same workspace. Rust is a language choice; owning the storage mechanism is a different choice from owning instruction emission.

Own bounded framing, object persistence, commit selection, atomic acceptance outcomes, historical receipt lookup, recovery, consistent export/import and index reconstruction. Borrow established hashing, ordinary Rust tooling and qualified OS/filesystem primitives. A new compiler, filesystem, allocator, cryptographic primitive or network stack is not a prerequisite.

Allow one writer at a time per local repository, with actual interprocess exclusion and explicit startup/recovery ownership. Initially no resident daemon is required. Reads observe a defined committed generation for a declared lifetime. SQLite already serializes writes; the successor cannot claim an advantage merely for doing the same. Independently opening CLI clients and a permanently resident owner are different process topologies. Include startup, locking, snapshot and any IPC costs in comparisons.

One journal/segment family initially retains object payloads and complete acceptance outcomes in one persistence protocol. Defer splitting authoritative blob files from a metadata database until object-before-acceptance, backup, recovery and reclamation ordering are specified. Start with reconstructible in-memory maps; later on-disk indexes are discardable caches. Optional third-party analytics can live outside authority, but SQLite is not required by the initial successor path.

This is not a general SQL or graph database. A small append kernel still needs an explicit framing/commit protocol and failure tests; naming a journal does not establish an engine.

### Versioned investigation model above the kernel

Keep scientific schemas, hypothesis interpretation and slow policy evaluation outside the durability transaction. The kernel checks canonical bytes, declared structural references, kinds required by the contract, request identity and atomic head changes. Domain validators enforce record meanings above it. Opaque payloads need canonical reference manifests for the kernel to check their declared closure; that does not prove every semantic dependency was declared.

Begin with artifacts/source states, attempts/observations, claims/assumptions and decisions. Permit ordinary text and attachments rather than a universal ontology. Separate content IDs from stable logical identities, and type source ancestry, evidence/provenance and acceptance/authority relations. Not every useful reasoning relation must be a DAG.

Retain existing object IDs and acceptance semantics for compatible records. Richer source metadata, envelopes, policy binding or multi-head transactions require explicit versioning, not silent reinterpretation of historical bytes.

### Native work operations and interoperable edges

Give agents bounded typed operations to retrieve exact objects, materialize source, propose candidates, attach evidence, inspect alternatives/omissions, accept under exact preconditions, recover receipts and export self-contained closure. Do not require a long narrative dashboard to interpret every operation.

Git is a compatibility/publication adapter, not the successor workspace's hidden storage backend. GitHub can remain the development host for the program's source; that differs from making it the product's runtime authority. Existing GitHub-owned source must be imported explicitly. Use isolated native-authoritative successor workspaces rather than claiming two independent authorities for the same accepted head.

Minimal named proposals/heads and exact snapshot differences belong early; a universal automatic semantic merge engine does not. Reuse editors, build tools and diff/merge algorithms where appropriate. Check an integrated candidate at its actual combined state, not solely through old results for individual components.

### Evidence-scoped review without automatic truth or dispatch

Follow explicit dependencies when a premise, environment binding or observation is corrected. Emit advisory review records naming the changed premise, affected decision and original evidence. Start with bounded equality/version/retraction conditions, not arbitrary scripts or inference in acceptance transactions. Historical validity, current applicability and authorization remain separate.

A repository event does not wake a model. Dispatch requires a verified host integration, authority and a recipient-specific outcome-reconciliation contract. Hold an uncertain external effect while allowing useful independent work. Do not capture hidden reasoning or claim model/transcript identity across sessions.

## Persistence contract and limits

Preserve exact historical retries after head movement, changed-request operation-ID rejection, durable accepted and stale outcomes, full declared object closure and the explicit global acceptance sequence. Object insertions and retries do not consume acceptance sequence numbers; file offsets are not those numbers.

A successful write, digest or commit marker alone is not a complete durability protocol. Recovery cannot know which reply a caller saw. A committed outcome may legitimately survive its lost reply. A malformed final record may be an unfinished append or damage to acknowledged history: never truncate it solely because it is last or has a bad checksum.

Specify admissible committed-boundary selection under each declared fault model. Preserve ambiguous evidence and stop unsafe writes after uncertain I/O/sync outcomes. Re-reading surviving bytes is not by itself proof of their stable durability. Report integrity refusal separately from successful recovery and count its availability cost.

Exercise partial writes, failed synchronization, missing/corrupt boundary metadata, earlier-record damage, process exit before/after commit, lost reply, writer contention and exact retry. Simulation and process termination are not physical power-loss proof. Export/restore must recover independent state and original receipts. Version recognition, growth, replay cost and lifecycle qualification stay explicit. Begin without compaction, garbage collection, network service or replication; expose growth limits rather than claiming those obligations disappeared.

## Next implementation unit

Implement the smallest disposable owned journal with a framing/commit specification, a separately formulated in-memory acceptance oracle and an independently implemented reader. This is a construction unit, not an instruction to produce indefinite design-only models. No external implementer has accepted it; reconcile actual ownership before overlapping work.

Its coherent demonstration must store exact source, retain two approaches and failed-approach evidence, accept one candidate, kill a process after durable commit before reply, restart from repository bytes alone, and recover the original receipt without applying acceptance again. Include stale acceptance, changed-request reuse and malformed/corrupt input controls. Export without overwrite and restore in a fresh directory. Check the same semantic fixtures independently against the oracle and retained SQLite reference; do not dual-write competing canonical states.

Use the result for one actual continuation of its own development, then a distinct small public investigation. Start on one verified host; a real second host comes later. Preserve receiver exposure and consequence. Reuse the ongoing fair-comparison work rather than duplicating it or claiming its formatting study measures storage performance.

Evaluate three independent claims: mechanism correctness, useful continuation at total preparation/retrieval/maintenance cost, and worthwhile ownership/reviewability. A correct kernel may still be the wrong product. A helpful schema does not prove a faster database. Neither speed superiority nor novelty is required to begin ownership work. Retained-data adoption requires explicit qualification and recoverable prior state.

## Alternatives, transition and balance

SQLite remains the practical reference, not the selected successor authority. Another packaged database would exchange dependencies rather than meet this ownership objective. Assembly throughout would conflate domain, persistence and emission risks. An independently emitted verifier remains a bounded later target with its own stable input/checking contract, not a prerequisite to constructing the journal.

A context-only system misses the source-repository ambition; a universal forge, scheduler, semantic merge engine and scientific ontology exceed the first slice. The balance is owned persistent bytes and atomic transitions, replaceable projections/tools, and real investigation use.

A clean architecture does not require erased history. Preserve the reference, source and evidence. A distinct successor source repository may be useful for a different build root/contract, but no rename or new repository is executed here. Before cutover, reconcile owners and remote IDs/URLs, source/evidence mapping, CI/permissions and one authority per active target. An expired lease does not prove a stopped writer. GitHub warns that reusing a renamed repository's old name removes redirects.

CURRENT remains the capability/active-unit record. This ADR is the successor design selection, not another live dashboard or silent reassignment of the practical trial. The next reconciliation must distinguish that active unit from this new construction target and must not report the engine as implemented.

## Actual collaboration and corrections

Two supplied-context Claude Opus 5.5 calls completed at medium effort, adaptive thinking, text-only, no server memory, end_turn and no truncation. [Complete visible requests, responses and metadata](../collaboration/2026-10-19-clean-slate.md) remain unchanged. Usage: 2,633/3,602 input/output tokens in turn one; 2,611/3,753 in turn two. These are usage observations, not billing or independent verification.

Adopted: product-first reset, owned authority as development target, Rust independent of SQLite, generic kernel and independent checks. Qualified: optional SQLite indexes are outside authority, not required. Disagreed: a blanket one-year native-branching delay is arbitrary; keep simple proposals early and defer general semantic merge.

Corrections: Rust is not runtime/dependency-free; a boundary record alone does not solve recovery; no blanket novelty versus Git/notebooks is established; events do not dispatch agents. Turn two's automatic torn-tail truncation/read-only recovery categories are not adopted without a verified boundary and scope for readable state. Its specific fsync OS explanation and crate suggestions were not independently qualified and are not selected dependencies. Existing SHA-256 IDs are not switched to BLAKE3. This revised ADR also corrects its initial topology wording: SQLite already serializes writers.

Sources read: Cargo.toml, src/store.rs, MISSION, AGENTS, CURRENT, ADR0002, continuation method; original user transcription in the retained brief; PR105 comments and PR109 reconciliation. Primary documentation checked before both calls: [SQLite architecture](https://www.sqlite.org/arch.html), [Rust code generation](https://rustc-dev-guide.rust-lang.org/backend/codegen.html), [GitHub renaming](https://docs.github.com/en/repositories/creating-and-managing-repositories/renaming-a-repository). No private Base12/Prime Radiant payload or unpublished operational state is included.
