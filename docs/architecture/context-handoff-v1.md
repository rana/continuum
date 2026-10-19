# Context and handoff, version 1

This is the contract for the local context implementation in [context.rs](../../src/context.rs). It uses the existing v1 Blob and Snapshot formats; it adds no database format, remote executor, model dependency, or source codec. See the [structural JSON schema](../../schemas/context.schema.json) and [runnable example](../../examples/context_handoff.py).

## The useful unit

One WorkState describes one objective and one offered handoff. It retains attempts, decisions, unresolved questions, source references, and constraints. A context selector produces exact rendered bytes and an immutable manifest. A new process can verify that the manifest and rendering are precisely the selector's projection of the retained WorkState.

Logical record IDs identify the work. Content IDs identify exact bytes. Two revisions of the same logical work can have different content IDs; those facts should not be conflated.

The first selector is deliberately simple. Its identifier is `continuum.whole_records.v1`. It includes the objective and constraints, every declared attempt, every unresolved question, the offered handoff, every active decision, and every decision required by the handoff. Only other historical decisions are optional. It considers those in stable-ID order and includes whole records while they fit. This is reproducible selection, not a relevance model or a claim that every possible future question is covered.

The budget counts exact UTF-8 bytes, including newlines, the header, source identities, limitations, and coverage record. It is not a token estimate. If required content and omission metadata cannot fit, preparation fails with a required-byte count. It does not shorten critical records or silently remove an unresolved operation.

## Stored records and scope

| Record | Purpose |
|---|---|
| Objective | Statement, completion condition, and current authored constraints |
| Attempt | Logical attempt and operation IDs, its own historical source snapshot, request bytes, declared dispatch state, optional opaque receipt, and authored outcome note |
| Decision | Active or historical statement, declared attempt basis, and reopening condition |
| Uncertainty | Open question and why it affects continuation |
| Handoff | Authored offer naming sender, recipient, scope, and required decisions |
| ContextPack | Exact source and rendered Blob identities, selector revision, budget, included records, omissions, optional acceptance anchor, and limits |
| ContextAcknowledgement | Caller-authored declaration naming the intended recipient and exact included and omitted context references |

WorkState, preparation-request, and acknowledgement fields are caller-authored. The selector generates the manifest, rendered metadata, and conditional guidance. In particular, `never_dispatched`, `may_have_been_sent`, and `receipt_recorded` are declared states. This module does not instrument a dispatch boundary and cannot prove those states independently. Conditional guidance makes that assumption visible. An active decision whose declared basis includes a possibly sent operation carries a `basis_unresolved` marker; other states do not thereby prove the decision's validity.

An attempt with `receipt_recorded` must name retained receipt bytes, and the other two states must not name a receipt. Receipt bytes can be arbitrary, including invalid JSON or partial output. Custody does not establish request binding, issuer identity, completeness, success, or scientific validity. A recognized context-acknowledgement document is rejected as an attempt receipt to avoid conflating these two record types. This is a type-boundary check, not adversarial authentication of opaque documents.

## Integrity and freshness are separate observations

A historical pack can remain exact after the accepted state changes. The optional anchor names an acceptor namespace, target, expected root and generation, and a path whose Snapshot entry must name the exact WorkState Blob. A source-tree reference alone would not establish that relationship.

| Result | What it establishes |
|---|---|
| `exact_projection_verified: true` | The retained manifest and rendered bytes reproduce the declared selector applied to the retained state. |
| `matches_at_observation` | The named local accepted head matched the recorded root and generation when checked. |
| `stale_at_observation` | The named head no longer matched when checked. The historical pack can still be valid. |
| `unanchored_freshness_unchecked` | No accepted-head comparison is available for this historical snapshot. |
| `reference_consistency_verified: true` | An acknowledgement names the offered recipient and exactly the included/omitted context references. |

`verify-context` checks historical integrity and reports freshness separately. `verify-current-context` additionally requires a matching anchor. `prepare-context` rejects an already stale supplied anchor. An acknowledgement of an old pack remains a historical record and reports current observed staleness; it is not erased.

The freshness observation is not a lock. The head may move immediately afterward. An operation that acts on current state still needs its own enforced expected-head and authority checks at the effect boundary. Local acceptor and recipient names are not authenticated principals.

## Exact custody

The WorkState is stored before preparation as an exact Blob. Preparation stores the exact rendering before the manifest that refers to it. A failure can leave an unreferenced immutable Blob, but no accepted head is changed by preparing context. This slice does not claim a multi-object transaction or implement garbage collection.

The manifest itself uses the implementation's deterministic compact JSON encoding. A manually reserialized, semantically equivalent manifest is a different Blob and is not accepted as the exact generated manifest. A future selector/codec revision needs an explicit identifier and retained reader; it must not silently redefine the old projection.

Each typed JSON document admitted by the context module is limited to 256 KiB. The requested budget for rendered bytes is independently capped at 256 KiB; an enclosing CLI response can be larger because it includes metadata and JSON escaping. Parsing rejects duplicate object keys at every level, including equivalent escaped spellings, before typed decoding. Unknown fields and unsupported schemas are rejected. A WorkState has at most 256 records, at most 32 objective constraints, and at most 8,192 UTF-8 bytes per nonempty text field. IDs, cross-record references, object kinds, direct reference byte totals, and anchor membership are checked. The structural JSON schema does not replace these runtime validations.

Direct referenced objects are checked within a 16 MiB aggregate bound. Source Snapshot files are not automatically materialized, and arbitrary external dependencies are not discovered. Omission accounting covers the declared WorkState, not everything ever discussed in a project.

## Run the example

From the project root, build the CLI and choose a new output directory:

```sh
cargo build --locked
python3 examples/context_handoff.py \
  --binary target/debug/continuum \
  --output /tmp/continuum-context-example
```

The example constructs two synthetic histories with identical source and request bytes. Their WorkState declarations differ only in dispatch state. Separate CLI processes prepare and inspect the packs, record context acknowledgements, and check current anchors. It then advances one accepted work-state root and demonstrates that its old pack is intact but stale. It sends no external request.

The result is a process-continuation and representation check. It does not establish that a model understood the context, that authored operational claims were true, or that this representation improves end-to-end performance. A separate model trial must record the exact input exposure and avoid putting its grading key in the prompt. The wider [representation experiment](representation-experiment.md) keeps those questions open.
