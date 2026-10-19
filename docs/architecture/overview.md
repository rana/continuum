# Native architecture

Status: design, with the first storage/acceptance slice implemented separately. Consult CURRENT.md for measured completion.

## 1. What the system is

Continuum is a native engine for continuing engineering work with exact artifacts and evidence. It has three related graphs:

- **Artifact graph:** exact blobs, source snapshots, manifests, environments, and produced outputs.
- **Work graph:** objectives, hypotheses, attempts, declared dependencies, handoffs, decisions, and reopen conditions.
- **Evidence graph:** observations and claims, their inputs and scope, review relationships, counterexamples, and applicability.

These relations must remain typed. A source dependency is not a permission edge; a citation is not a proof; a review is not a replication; a chronological successor is not automatically a stronger result.

The stored object body is immutable. State changes are new events or successor records. A stable logical identity, such as an objective ID, is distinct from a content ID identifying one exact revision.

## 2. A small reliable foundation

The initial Rust implementation has three object kinds:

| Object | Meaning |
|---|---|
| Blob | Exact bytes |
| Snapshot | Sorted relative source paths referencing blobs |
| EvidenceRecord | A declared result and provenance bound to a candidate snapshot |

A content digest identifies the versioned canonical object encoding, including its kind. The snapshot links create a small Merkle DAG. The first format is a deliberately restricted source-file model, not complete Git fidelity: executable modes, symbolic links, arbitrary byte filenames, and submodules require explicit later representations.

EvidenceRecord is a recorded assertion. Storing it does not prove the result, run a test, validate the author's identity, or establish whether it still applies.

A local acceptance stream is keyed by acceptor and target. Its head contains a content root and a monotonically advancing generation. An attempt supplies the exact expected head and a stable operation ID.

The transaction:

1. Reconciles an existing operation receipt; a different request under the same ID is an error.
2. Checks the expected head and generation.
3. Records the resulting acceptance or precondition failure.
4. Changes the head, when accepted, and stores the receipt atomically.
5. Acknowledges only after commit.

The same root returning later does not restore an older generation. This prevents the ABA mistake in which a caller treats a changed-then-restored root as an unchanged state. A retry after an uncertain reply reads the original receipt even if the head has advanced again.

Acceptor-scoped operation IDs bind the target as part of the request. This is slightly broader deduplication scope than a per-target ID, deliberately detecting accidental reuse across targets.

Local transactional idempotence is not a promise of exactly-once remote model inference, email, deployment, or arbitrary tools. Each effect needs its own recipient-supported idempotence or reconciliation contract. A cancellation request does not establish that an effect stopped.

## 3. Proposed records above the core

Keep new record schemas outside the transactional kernel until their invariants require deeper integration.

| Record | Essential content |
|---|---|
| Objective | Purpose, completion conditions, priority source, budget, declared scope |
| Hypothesis | Claim, assumptions, predicted observations, possible counterexample |
| Attempt | Objective, input snapshot, executor and invocation references, state events |
| Observation | What was actually observed, by which instrument, under which conditions |
| Claim | Statement, evidence references, applicability, uncertainty |
| Decision | Selected option, alternatives, rationale summary, authority, defeaters |
| Handoff | Offered scope, recipient, input checkpoint, explicit receipt events |
| ContextPack | Exact rendered inputs, selection provenance, known omissions and coverage |
| ProtocolDefinition | Method revision, input/output contracts, bounded composition |
| ReleaseManifest | Exact composition, compatibility contract, evidence and known gaps |

Store original inputs and concise visible rationale where authorized. Do not claim that hidden reasoning state can be exported across vendors. A context reconstruction is a new working context, not proof of continuous model identity.

## 4. Acceptance and authority

The prototype's acceptor name is just a caller-supplied namespace. A production service must authenticate the principal and enforce explicit grants at the acceptance and effect boundaries. Root authority begins in external owner/platform configuration; the first grant cannot authenticate itself by appearing in the same ledger it purports to authorize.

Before acceptance, expensive evaluators may prepare evidence against the exact candidate, policy, environment, and relevant authority epoch. The short transaction must reject stale prerequisite identities. This full policy-bound acceptance is a planned extension, not a current property of the CLI.

A registry entry or a model's confidence cannot grant permission. A plan's high priority does not authorize a forbidden effect. Revocation and leases require fencing enforced by the service receiving the effect; lease expiry alone does not stop an old worker.

## 5. Context as a queryable artifact

An agent requests a context pack for one objective, exact snapshot, and finite token budget. The pack includes decisive evidence, active constraints, relevant differences, uncertainty, and expandable references. It describes its selection procedure and known coverage limits.

A reverse index can later connect declared assumptions and omitted known dependencies to affected decisions. A change produces a review candidate. This cannot detect arbitrary unknown dependencies or certify the absence of relevant omitted facts.

A protocol registry is initially a small versioned manifest checked into this project. As the graph matures it can become a query over accepted definitions. Preserve one canonical definition; generate host-specific skill and prompt adapters from it where possible.

## 6. Distributed operation

Replicate immutable proposals and artifacts freely within authorized visibility. Preserve exact object identities, verify received bytes, and request missing dependencies. Select a bounded ordered authority for each accepted target.

For a production multi-host deployment, either route acceptance for a target to one authority or implement a tested consensus service within that authority domain. A Merkle DAG detects content identity and divergence; it does not establish consensus, authorization, freshness, availability, or truth.

Two disconnected hosts can propose independently. They cannot both promise final acceptance under one linearizable target during a partition. The system should expose provisional states rather than silently changing the acceptance contract.

Never share the prototype's writable SQLite WAL over a network filesystem. Each host has a local store and a real replication protocol in the later phase.

## 7. Data structures that serve the work

| Technique | Engineering use | Limitation |
|---|---|---|
| Merkle DAG | Integrity, deduplication, structural sharing, content-addressed exchange | Not evidence truth or authority |
| B-tree indexes | Object lookup, receipt lookup, ordered event queries | Choose indexes from actual query patterns |
| Append-only events | Recover state transitions and derive current views | Retention and correction semantics still required |
| Snapshot isolation / MVCC | Stable read views while work continues | Long-lived reads can retain old state |
| Dependency DAG | Ready work and affected-input analysis | Cycles need rejection or explicit iterative semantics |
| Reverse indexes | Find decisions touched by changed declared premises | Unknown dependencies remain unknown |
| Priority queues with aging | Useful work selection without indefinite starvation | Priority needs a defined owner and budget |
| Bounded channels | Backpressure and cancellation propagation | An acknowledged cancel still differs from actual effect termination |
| Reachability-based collection | Reclaim objects outside retained roots and evidence closures | A careless pin policy can delete future recovery inputs |
| CRDTs | Some replicated annotations or sets | Not a universal solution for acceptance or permission |

The complete native design should be portable at the object and protocol layer. Linux is the first implementation target, not a permanent wire-format requirement.

