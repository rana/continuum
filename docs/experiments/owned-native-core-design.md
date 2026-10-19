# An owned native core for Continuum

Status: original research design, not an implemented storage engine or an adoption decision. Dated 2026-10-19 UTC / 2026-10-18 America/Los_Angeles. The runtime inspected at `d126337d22c3a181d72ef559d2c84a436d9aec19` retains the storage and object implementation reviewed previously. [CURRENT.md](../../CURRENT.md) remains authoritative for advancing implementation work and the selected Codex pilot.

The [research provenance](../../research/runs/owned-native-review-2026-10-19.json) records actual source identities, model exposure and execution limits. This proposal opens application-specific native storage as a research objective in its own right. A demonstrated SQLite bottleneck is not a prerequisite for investigating architectural ownership. The operational SQLite core remains available while this separate experiment develops evidence. The [embedded-engine assessment](embedded-storage-evaluation.md) remains useful as a comparison, rather than an exhaustive catalog of possible designs.

## 1. The opportunity worth pursuing

Continuum needs work to survive interruption, reinterpretation, and changes of model or workstation. An agent needs to recover exact inputs, distinguish an attempted effect from an accepted effect, and discover the original outcome of a request whose reply disappeared. These needs suggest a storage instrument organized around continuing investigations and accountable transitions.

A purpose-built kernel could make its whole supported state space legible: a few admissible operations, explicit failure outcomes, one documented persistence protocol, and layouts chosen for objects, context, and evidence. Omitting unrelated database capabilities could reduce implementation and maintenance costs. It might also reduce resource use. These are design hypotheses, not established advantages.

The larger ambition is adaptive access over stable meaning. Models may prepare different context projections, indexes, or evidence selections while the historical inputs and accepted decisions remain recoverable. We can investigate physical layouts that place frequently consumed records together without letting a model's current preference rewrite prior evidence.

Two frontier models can propose alternatives, challenge invariants, write implementations, and retain counterexamples rapidly. Their agreement does not establish independent empirical confirmation. A useful joint workflow gives a separately formulated checker exact artifacts and a declared contract, then preserves both disagreements and observed results.

## 2. Ownership has several independent layers

| Layer | What we could own | What remains to establish |
|---|---|---|
| Domain semantics | Object identities, acceptance, retries, context coverage, evidence relationships | Whether the contract serves real continuing work |
| Storage mechanisms | Journal frames, indexing, checkpointing, allocation policy, persistence ordering | Recovery correctness and lifecycle behavior |
| Native userspace boundary | Selected allocator, system-call interface, startup, optional `no_std` components | Target-specific ABI and runtime obligations |
| Instruction emission | Restricted IR, machine encodings, relocations, executable format, bootstrap | Correct lowering, toolchain provenance, debugging and maintenance |
| Platform beneath userspace | Kernel, filesystem, device and network behavior | Explicit assumptions; ownership is a separate research program |

The first two layers can be implemented in Rust without adopting a general-purpose database. Rust does not require SQL, a particular journal, or a universal allocator strategy. That is substantial control.

Fully owned emission is a further capability, not another name for ordinary Rust compilation. It can make the admitted instruction set and exact lowerings inspectable, permit narrowly constrained executables, and reduce selected build/runtime dependencies. It also makes us responsible for code generation and ABI details that an established compiler normally handles.

Neither full ownership nor Rust guarantees speed, correctness, or freedom from dependencies. A `no_std` component still needs its external services and linking arrangements specified. A directly emitted program still relies on the platform executing its instructions correctly. We should keep each boundary visible and explore them independently. Rust documents [inline assembly](https://doc.rust-lang.org/reference/inline-assembly.html), the [precise effect of no_std](https://doc.rust-lang.org/reference/names/preludes.html#the-no_std-attribute), and its [normal compiler/backend boundary](https://rustc-dev-guide.rust-lang.org/backend/codegen.html); these are capabilities and dependency descriptions, not Continuum benchmark results.

## 3. Preserve the current behavioral contract

The authoritative starting points are [store.rs](../../src/store.rs) and [object.rs](../../src/object.rs). The current SQL schema contains immutable objects, heads, and acceptance events. Its narrow domain makes specialization plausible.

The compatible experiment must preserve these relationships:

- Canonical object bytes determine their existing versioned, domain-separated identities; referenced objects must have the required kinds.
- Acceptance compares the complete expected root and generation, preventing an intervening change from disappearing merely because a root recurs.
- An operation identity binds its exact canonical request. Changed reuse fails; an exact retry recovers the historical receipt even after the head moves.
- A stale precondition receives a durable rejected receipt. Invalid requests and missing or invalid candidates retain their specified error behavior.
- Recording the outcome and changing the head are one atomic domain transition.
- Acceptance events use the existing database-wide event counter. Object insertions do not consume that counter, and exact retries do not allocate another event.

The event counter is consequently not a journal byte offset or a count of all frames. Generation and sequence exhaustion remain explicit. A different ordering scheme requires a separately named contract change.

## 4. Candidate architecture: one append-only authority

The first physical design uses two logical record types:

**ObjectInsertion** retains exact canonical bytes and their identity. **AcceptanceOutcome** retains the canonical request and complete receipt, including the observed head, resulting head, outcome, and event sequence.

A proposed frame carries a format/domain identifier, record type, bounded lengths, and integrity protection over its relevant metadata and payload. The parser must reject impossible lengths and unknown required semantics before allocating from them. Object-envelope limits remain distinct from a frame's additional overhead. Framing and commit rules must be specified before filesystem implementation; this note does not choose final field widths or declare a complete commit protocol.

A digest link to the previous frame or segment is worth evaluating for detecting gaps or reordered history and for binding checkpoint prefixes. It does not authenticate an author, prove that the entire history was retained, or repair missing bytes. Existing cryptographic hashing libraries remain the initial implementation choice. A Merkle structure may later serve partial verification or transfer; the first local journal does not need one merely because objects are content addressed.

Objects and acceptance records stay within the same persistence domain initially. Before accepting a candidate, the protocol must establish that its referenced closure is retained under the required durability conditions. Independent blob files would add an object-before-head ordering problem, so that separation is deferred.

Replay reconstructs object lookup, current heads, operation lookup, and per-target event indexes. A stored outcome is checked against the preceding semantic state rather than treated as a trusted assertion solely because its checksum matches.

## 5. Durability and uncertain outcomes are central

The proposed owner serializes acceptance decisions. A valid new request produces a proposed transition; its complete record is written under the framing protocol; the covering persistence operation must succeed before a durable success response is released. Read visibility needs an explicit committed generation as well. A batch may share a barrier if each acknowledged operation is covered by it.

Short writes, interruptions, allocation failures, disk-full errors, and failed synchronization need defined transitions. A write completing is not itself the durability boundary. Linux documents that `fsync` waits for the device to report completion and that synchronizing a file does not necessarily persist its directory entry; directory synchronization is separately relevant when creating or installing files. These are platform obligations to model and test, not properties supplied by our chosen language. [Linux fsync documentation](https://man7.org/linux/man-pages/man2/fsync.2.html)

After a crash, an operation admitted by the specified recovery protocol may be discoverable even though the caller never received its reply. Stable operation identity makes that outcome recoverable. A failed sync must not be simplistically translated into “nothing happened”; recovery may have to determine which outcomes are supported before further acceptance proceeds.

Under the declared model, every acknowledged outcome must survive. Additional recovered outcomes must correspond to legal submitted operations with intact dependencies and atomic transitions; they need not have been acknowledged. A fault harness can retain the actual acknowledgement schedule as ground truth, but the recovering implementation cannot consult that hidden oracle.

The difficult boundary is distinguishing an incomplete unacknowledged tail from later corruption of acknowledged history. A bad final checksum does not, by itself, authorize truncation. The fault model must state what writes can tear or reorder, what successful synchronization establishes, and whether previously persisted bytes may later be corrupted. Ambiguity should preserve diagnostic evidence and report an integrity or uncertain state, rather than silently invent a shorter successful history.

SQLite's atomic-commit discussion makes hardware assumptions and write-ordering obligations explicit. Its described mechanism is rollback journaling, not the current Continuum WAL path; it is useful here as a study of the obligations an owned protocol inherits. [SQLite atomic commit](https://www.sqlite.org/atomiccommit.html)

The first design does not claim to repair arbitrary disk damage. Detection, recovery from interruption, independent backup, and redundant repair are distinct capabilities. TigerBeetle's safety design combines a narrow state machine, explicit storage faults, simulation, and replication. The transferable lesson is to design and test the failure model alongside the fast path; its guarantees do not transfer to our unreplicated prototype. [TigerBeetle safety](https://docs.tigerbeetle.com/concepts/safety/)

## 6. Indexes, checkpoints, and read lifetimes

Indexes are disposable projections of authoritative records. A checkpoint identifies its exact covered journal prefix, format, generation, and last acceptance-event sequence, together with the derived structures it accelerates. A damaged checkpoint should permit reconstruction from retained history. It is not a replacement for source custody or an independent backup.

Initially retain all history and omit garbage collection. This avoids making compaction correctness part of the first experiment, while keeping growth and rebuild time visible as costs. Checkpoint installation, file rotation, and later deletion each need their own ordering and recovery rules.

Readers consume a defined committed generation. The implementation must keep the referenced bytes and index version alive for the read's duration, and must specify how new generations become visible. Memory mapping could be an implementation option; it does not remove publication, lifetime, truncation, or coordination requirements. Begin with an understandable read path and optimize only identified costs.

Future context layouts may cluster a work state's likely evidence closure, retain explicit omission maps, and rebuild model-specific retrieval indexes. Those projections should bind their inputs and selection policy. A faster projection is useful only if successors still recover the distinctions that determine their next action.

## 7. Process topology and the Linux boundary

One owner process is the initial option to investigate, with several local clients submitting bounded requests. It provides a clear serialization point and a place to batch persistence. Its startup, memory, IPC, lifecycle, and recovery costs belong in comparisons with today's independent SQLite-opening CLI processes.

Direct multi-process journal access is a different option requiring initialization coordination, locking, consistent reads, and recovery ownership. We should not claim a topology-independent improvement from a benchmark that silently replaces those obligations with a permanently running service. Slow model inference remains outside acceptance transactions and long-lived storage snapshots.

Linux remains responsible for the kernel, filesystem interfaces, and TCP/IP. A native userspace implementation does not require reconstructing network transport. A future multi-host protocol must define identity, admission, replication, and uncertain effects above established transport. Use established TLS when encryption and authentication are needed; a custom storage kernel is not a reason to invent cryptography or expose the currently trusted local CLI as a multi-user server.

## 8. Exact custody differs from identity and sealing

Content addressing identifies bytes; it does not prevent a mutable source from changing after hashing. Moving validation before a short acceptance interval therefore requires a justified custody mechanism: retained immutable bytes, a protected handle under a stated threat model, or revalidation of the actual bytes consumed.

Linux `memfd_create` can support volatile files and checked sealing restrictions for an execution handoff. Its storage is RAM-backed and volatile, so it is not the durable journal. The recipient must verify the actual applicable restrictions and bindings. A descriptor number is a process-local reference, never an identity guarantee. [Linux memfd documentation](https://man7.org/linux/man-pages/man2/memfd_create.2.html)

The public [Base12 follow-up](../source-review/base12-followup.md) motivates binding admitted inputs, implementation, and observation contract before reusing a native result. The [research-loop review](../source-review/base12-research-loop.md) motivates preserving counterexample class, reduction scope, completion reason, and execution evidence separately. These are method transfers, not imports of private operational records or claims that Continuum has executed Base12's programs.

## 9. Phases that produce discriminating evidence

| Phase | Concrete artifact | Completion condition and limit |
|---|---|---|
| 1. Transition oracle and finite fault model | Independent semantic oracle, bounded framed-log model, exact corpus, retained counterexamples | Explain every modeled outcome; this is finite model coverage, not real disk validation |
| 2. Filesystem shadow journal | Disposable alternate store behind the existing domain operations, explicit owner mode | Reproduce the contract and exercise real process/I/O failures under stated assumptions |
| 3. Optional emitted verifier | Restricted read-only decoder/transition checker, instruction inventory, bootstrap provenance | Independently check admitted traces; no mutable persistence authority is transferred |
| 4. Comparative workloads and lifecycle | Matched workloads, resource records, backup/restore and upgrade experiments | Establish useful benefits and acceptable recovery/migration costs before adoption |

Phase 1 should begin with exact traces for acceptance, stale rejection, historical retry, changed identity reuse, competing candidates, object references, and exhaustion. Define finite bounds and distinguish volatile state from modeled durable state. Explore short and interrupted frames, loss or reordering permitted by the model, corruption, and sync failures. Retain minimized witnesses with the property they violate. No generated case count should be mistaken for exhaustive hardware coverage.

Phase 2 implements actual byte custody, I/O, and restart behavior. Keep the existing SQLite behavior as a comparator, while an independent oracle helps expose shared assumptions. Process termination tests establish only their stated failure boundary; broader disk-fault experiments need a separate harness and explicit coverage.

Phase 3 answers the fully owned-emission question without coupling it to writable storage. Record the exact seed, emitter, executable bytes, admitted instruction forms, ABI, inputs, and observed outputs. A valid checker verdict establishes conformity of supplied bytes; it does not attest which historical process produced them. Expanding into a writer, general compiler, or self-hosted bootstrap requires another bounded objective.

Phase 4 measures complete useful operations: startup, reads with validation, durable outcomes, contention, memory, disk growth, checkpointing, and recovery. Include owner-service costs and maintenance. Retained use requires independently restorable backups, format recognition, and a migration story. Speed is one possible benefit; legibility, predictable resources, target support, or improved continuation can also justify the design.

## 10. Conditions that would change the direction

Six findings would require narrowing or rejecting a candidate:

1. It changes acceptance, historical retry, identity, validation, or ordering semantics unintentionally.
2. Recovery cannot distinguish supported outcomes from corruption without silently losing acknowledged history.
3. Its benefit depends on shifted process topology or weaker persistence that the comparison omitted.
4. It provides no meaningful resource, operability, comprehension, or continuation benefit over the maintained baseline.
5. Index growth, replay time, feature exceptions, or maintenance enlarge the supported state space beyond the intended small kernel.
6. Emission and bootstrap costs obscure the semantic boundary or exceed the value of owning that layer.

The immediate research deliverable is the oracle and finite journal model. It can advance without replacing working storage or displacing the current pilot. This separates permission to investigate from evidence to adopt, and lets the native vision grow through exact, reviewable artifacts.

## 11. A fresh reader and a conditional successor repository

The user's additional consideration is conditional: if a fully owned native target is adopted, its repository should explain that chosen design directly. No switch, successor repository, archive or rename has occurred. [ADR 0002](../decisions/0002-owned-storage-research.md) authorizes research, not a claim that adoption has already succeeded.

If the product becomes a distinct emitted kernel with a different build root, runtime boundary and release process, a new repository could provide a clearer home. If custom storage remains a component of the current Rust build, a refreshed current architecture and concise historical pointers may suffice. A runnable Rust reference does not prevent a fresh repository: it can be an explicitly identified oracle or pinned external comparator. Keeping two repositories must not create competing writable authorities for the same active contract.

| Fresh-reader question | Proposed authoritative home |
|---|---|
| What is this system and what works? | README routes to current capability/status and a working example |
| What must implementations preserve? | Versioned contracts and executable conformance fixtures |
| How is the owned target constructed? | Kernel source, emitter/ABI/bootstrap documentation and build manifest |
| What was actually established? | Exact evidence, minimized counterexamples, independent checks and measured limits |
| Why was this path selected? | One short transition decision with pinned predecessor links |
| What should the next worker do? | Current bounded objective, owner and acceptance condition |

The transition note would identify what changed, why, which contracts and fixtures carried over, what did not carry over, and where the preserved Rust/SQLite baseline remains reproducible. It would not require a new reader to traverse the full design conversation. Historical evidence remains accessible, with its old capture-time claims intact.

Pull requests should explain the concrete behavior or invariant changed, its connection to the current objective, relevant verification, and unresolved limits. Link the exact run artifacts rather than repeating the entire historical debate. A fresh reader should be able to build, inspect the trusted boundary and find the next task without first studying the predecessor's narrative.

Do not confuse a clean source tree with clean evidence: preserve the counterexamples and compatibility obligations that taught us what correctness requires. If the contract itself changes, version and explain that change instead of presenting a new repository as evidence that the old obligations disappeared. Claude's [actual conditional-repository review](../collaboration/2026-10-19-claude-12.md) and [coordinator qualifications](../collaboration/README.md#owned-native-design-corrections) are retained.

## 12. Naming and a coordinated future transition

Continuum remains the preferred working project name. If a distinct owned implementation becomes the adopted successor, the predecessor could be named `continuum-prototype` and the successor `continuum`. These are conditional candidate names, not created or reserved repositories. Use `frozen` only for an actual frozen baseline and `deprecated` only when the corresponding support status is true; a useful comparator need not be called obsolete.

GitHub normally redirects renamed repository web and Git operations, but explicitly warns that reusing the old name for a new repository stops those redirects. Its hosted-action references also have separate rename behavior. A new repository named `continuum` would have a different repository identity, even though an old remote URL has the same text. [GitHub repository-renaming documentation](https://docs.github.com/en/repositories/creating-and-managing-repositories/renaming-a-repository)

A transition must therefore migrate collaborators and integrations as well as source:

| Transition step | Required observation |
|---|---|
| Inventory active consumers | Identify research chats, Codex checkouts, Dot mailbox/tasks, scheduled prompts, CI, links and open work from actual available state |
| Prepare the successor | Build and verify it under an unambiguous temporary identity; retain predecessor baseline, contracts, fixtures and transition decision |
| Reconcile active work | Each overlapping writer completes, transfers or explicitly stops its current unit; silence is not proof that a worker stopped |
| Publish a versioned transition record | Record old/new repository IDs and URLs, pinned baseline and successor commits, current authority, compatibility scope and backout conditions |
| Update concrete references | Change actual local remotes, worker prompts, schedules, CI references and documentation through supported capabilities |
| Obtain recipient acknowledgements | Record which chats/workers actually read the new repository ID/revision and accepted the transition; distinguish offered, received and verified |
| Move the enduring name | Recheck identities and active writers immediately before any rename/name reuse; verify the resulting repositories and write routes |
| Verify a fresh continuation | A newly started worker reads the right contract, performs a bounded contribution in the intended home and identifies the exact repository and source revision |

The ordering can be refined for the chosen deployment, but reusing a live URL before reconciling old writers is not a harmless cosmetic rename. Expected branch heads help reject stale publication; they do not prove all workers are idle or all schedules were updated. Receivers should validate the expected repository identity as well as its name at a transition.

A posted migration note cannot wake every dormant conversation or rewrite its private context. Use actual supported notification/task routes, preserve a discoverable notice in the predecessor and established mailboxes, and require resumed workers to reconcile current authority before writing. Unreachable consumers remain listed as unresolved rather than being declared notified. If an old writer cannot be positively accounted for, delay name reuse or choose a transition arrangement that prevents it from writing to the wrong destination.

No repository rename, archive, successor creation, remote rewrite, schedule change or coordinated migration has been performed by this design review. The latest user additions are planning considerations. Current writers continue using the existing repository and their selected bounded work.

## 13. Forms of two-way cross-pollination

Cross-pollination can progress from ideas to real components. It is not restricted to prose, and it need not force a common implementation language.

| Form | Concrete possible exchange | Boundary to preserve |
|---|---|---|
| Research methods | Exact input custody, independently formulated checks, deliberate mutants, minimized counterexamples | A method is not a borrowed experiment result |
| Specifications and corpora | Versioned record/receipt contracts, finite valid and invalid inputs, failure traces | Include origin and independently checked expectations; do not let a buggy producer define every oracle |
| Host-side tools | Evidence manifests, corpus runners, trace inspectors, deterministic rebuild comparison | Host dependencies do not silently enter a separately emitted target runtime |
| Native components | A bounded byte reader, framing validator, syscall-error adapter or independent verifier | Agree on ABI, bounds, failure behavior and actual admitted instructions |
| Deliberate copies | A small stable component adapted to the other project | Pin repository/commit/content identity, license, local changes and track/fork/freeze policy |
| Shared library or emitter module | One tested implementation used by two actual consumers | Extract after both consumers demonstrate the same semantics; version changes and retain independent checking |

Base12's narrow-stage construction and custody discipline can inform Continuum's verifier and execution boundaries. Continuum's stable operation identities, recoverable receipts and source/context handoffs can in turn serve Base12's continuing investigations. These are candidate consumers and method transfers; integration has not occurred in this review.

A portable specification can have a Rust reference and an independently emitted implementation. The emitted target need not link the reference runtime. Conversely, a host tool written in Rust can generate or check a bounded target while its build seed and provenance remain disclosed. Shared code is useful when it reduces duplicated maintenance without hiding a difference in scientific or persistence contracts.

Keep the initial component small and named for an actual consumer need. Do not begin by building a universal shared framework. Inspect source rights before any private-to-public code transfer; original public method adaptations and public-to-private reuse have different provenance from publishing private source. The [actual Claude discussion](../collaboration/2026-10-19-claude-13.md) and [Dot request](../collaboration/native-ownership-bridge.md) preserve the questions and observed collaboration state.
