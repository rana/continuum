# Extensible protocols without authority confusion

## Roles

A **procedure** describes a bounded method and its evidence obligations. A **skill adapter** makes a method discoverable in a particular agent runtime. A **prompt template** supplies an invocation or optional aid. A **policy reference** points to an identifiable governing constraint or grant.

Registry membership does not grant permission, tool access, spending, publication, recurrence, or another agent. Current platform and user instructions remain controlling. A method is selected because it helps the objective, not because it exists in the catalog.

The initial registry contains agent-guided procedures. Its JSON contracts support discovery and receipt validation. They do not imply an implemented generic workflow engine, automatic semantic validation, or installed platform skills.

## Three versioned records

A **ProtocolDefinition** has a stable ID, exact version, canonical Markdown path and digest, purpose, applicability, inputs, possible effects, output contract, and finite composition defaults. Optional lineage identifies an upstream encounter or earlier definition; it does not import that source's project authority.

A **ProtocolInvocation** pins the definition version and digest, objective, source snapshot, input references, actual actor, existing authority references, capabilities, parameters, and finite bounds. It is an account of one selected use, not a permission request by default.

An applicability probe may begin with partial inputs and conclude that the method is unnecessary. The fixture marks this in `parameters.phase` and reports only the probe. Before performing the substantive method, resolve its required inputs and capabilities; missing required semantics block the affected step or produce an explicitly partial receipt. An early probe does not claim the method was completed.

A **ProtocolReceipt** records actual scope, outcome, evidence, artifacts, limitations, performed effects, and next action. Receipts are immutable historical records; a correction creates another receipt linked through `supersedes`. Multiple receipts can describe checkpoints and later completion. New schema versions can add richer lifecycle semantics without pretending the present JSON contracts implement them.

The native object layer can later carry these record bodies. Their current JSON representation does not redefine canonical source encoding or content identity. The Markdown definition digest is SHA-256 over exact UTF-8 file bytes.

## Authority and preference precedence

Resolve applicable authority from the real instruction hierarchy and current grants. Platform constraints cannot be overridden by repository prose. Direct user directions and standing grants establish the intended scope; project governing documents record and route that scope; task requirements refine the selected objective; procedures and prompt preferences choose a method inside it.

A borrowed protocol cannot grant itself authority. Its historical holds, local machine rules, owners, or disclosure choices do not automatically become this project's restrictions. Conversely, a prompt cannot widen the user's grant by describing itself as autonomous. Later explicit user direction can amend an earlier project choice when it clearly does so.

Distinguish a requirement from a preference. Apply a narrower compatible task constraint without turning an optional style preference into an execution gate. When requirements conflict, record the sources, affected scope, and action. Resolve from existing authority where possible, continue independent work, and ask only for the genuinely missing decision.

Policy references must point to real source authority. Hashing, signing, or placing a statement in the registry does not make the statement authoritative.

## Bounded composition

Start with one instrument. Add another only for a named missing function. Each invocation supplies finite depth and step limits; catalog defaults are implementation safeguards, not claims that a particular count is scientifically optimal. A larger authorized investigation consists of further bounded invocations.

Pin exact component versions, validate their input/output contracts, reject recursive cycles, and preserve one accountable composition owner. Do not duplicate shared facts in each step's output. Thread source references and exact coverage forward.

Repeat a method only when new evidence, a changed question, or a changed representation can make another pass useful. A count of repetitions does not prove convergence. An unproductive walk can return not applicable; a creative seed can remain incomplete.

## Effects and receipts

Possible effects in a definition describe what an invocation might do. At invocation time, the worker checks actual tools and existing authority. No capability is inferred from a registry string.

Separate prepared, attempted, observed, and confirmed external actions. Record effect references and their actual state. A timeout produces uncertainty; reconcile before retry. A saved handoff establishes an offer, while receipt and acceptance require the recipient's own record. This registry does not wake a dormant chat.

Record validation can check identifiers, paths, digest formats, and explicit field contracts. It cannot establish that a scientific interpretation follows from the evidence or that a model's prose is true. Typed claims and interpretive synthesis remain distinguishable.

## Provenance and replay

Record model/provider identities as exposed, the requested and reported model separately when they differ, supplied visible input and returned output identities, relevant exposed settings, completion state, and actual review. Unknown fields stay unknown. Do not preserve hidden reasoning, platform instructions, credentials, or unrelated private payloads.

Deterministic record replay is retrieval, validation, or rendering of existing material. Re-executing an experiment is another attempt. Re-querying a model is another inference and may produce a different output. Cached evidence is not a new independent observation.

When a definition changes, its bytes and digest change. Existing invocations retain their pinned definition. Use explicit semantic versions for communicated contract changes and immutable content identities for exact reproduction. Record migrations without rewriting old receipts.

Unknown optional annotations may be retained. Unknown required semantics or capabilities must prevent the affected execution, not be silently ignored. Adapters should be generated or linked from canonical definitions rather than hand-maintained competing copies.

## Public and private boundaries

Continuum's public procedures contain original, generic adaptations. Source research archives, private operational identifiers, protected source passages, secrets, and unrelated personal records stay outside this repository. A source pin is attribution and identity, not a claim that the public project contains the upstream bytes.

The [research lessons](../research-lessons.md) document states what was actually inspected and where access was unavailable. New procedures should name the concrete benefit they aim to provide and a condition for revision or retirement.

