# Holographic Walk

**Protocol:** `holographic-walk@0.1.0`  
**Mode:** agent-guided, bounded multiscale inquiry  
**Invocation:** “Run a holographic walk on [question].”

## Purpose and applicability

Investigate a consequential question across representations, scales, and interfaces, then return with a changed constraint, clearer question, or useful next observation. “Holographic” names a method and metaphor; it does not assert a physical mechanism or that every part literally contains the whole.

Use a walk when local and whole-system reasoning disagree, an interface hides uncertainty, or a wider objective could change a local design. If ordinary local analysis already identifies the decisive uncertainty and next action, report `WALK_NOT_NEEDED` and perform that analysis.

A new imaginative seed can be a useful result. It need not acquire a fabricated experiment.

## Inputs and bounds

Start from one question, discrepancy, source encounter, or design choice. Identify the objective, relevant source snapshot, current authority, and available evidence.

Choose a local anchor, an enclosing system or outcome, and a short connected route. Name what each transition changes: abstraction, granularity, representation, locality, trust boundary, temporal resolution, or another relevant axis. Scale is not merely chronology. Do not relabel a long sequence of events as a multiscale explanation.

Set a finite context and work budget. Expand only a station that can change the decision.

## Procedure

### 1. Walk outward

Trace what the local object enables or constrains at the next boundary. Identify new interactions, assumptions that cease to hold, and properties that survive. Distinguish evidence, inference, hypothesis, design choice, and unknown at each station.

### 2. Inspect interfaces

Trace conversions, APIs, data movement, ownership transfers, evidence handoffs, and contact with the environment. Keep source history, dependency, information flow, authority, and evidence relationships distinct even when they share nodes.

For each consequential bridge, record:

- Starting and ending objects and the changed axis.
- The mapping or operation and its supplied inputs.
- Assumptions and applicability.
- Information preserved, transformed, approximated, or discarded.
- Relevant evidence, uncertainty, and the strongest alternative.
- What the next station adds to the question.

A lossy representation does not license reconstruction of discarded information by silently inserting a preferred assumption.

### 3. Walk inward

Start from the intended outcome and derive the needed observation, system obligation, interface contract, and local behavior. Distinguish requirements derived from the objective from those inherited by habit.

Ask what cheaper evidence could relax or overturn a constraint. Available implementation precision does not by itself establish required precision.

### 4. Reconcile and return

Compare the outward account with the inward requirements. Surface contradictions, missing mechanisms, unsupported invariants, and requirements without a defensible purpose.

Returning through the same assumptions provides consistency evidence, not independent validation. Seek a new constraint where needed: a counterexample, alternate derivation, changed boundary condition, separate observation channel, or targeted fault injection.

Record what changed. The outcome can be a corrected design, an improved question, a useful seed, an unresolved gap, or a specified experiment.

## Example: an interrupted acceptance

Local anchor: a late reply to an acceptance request. Walk through operation identity, durable receipts, target authority, replica behavior, and the user's expectation that interrupted engineering resumes reliably.

Return with the requirement that a fresh worker can recover an already committed result without creating another effect. A discriminating check interrupts the coordinator after durable acceptance but before its reply. This one route is sufficient; it does not require an exhaustive tour of every networking, compiler, and agent subsystem.

## Output and stop rule

Return the endpoints and compact route, bridge assumptions, outward and inward findings, interface discrepancies, decision delta or useful seed, and next action. Include actual source/model/execution coverage and evidence references.

Stop when the route changes a consequential decision or exposes a definite unresolved gap. If repeated passes add no information, change the representation, evidence, or question. A requested larger investigation may contain several separately bounded walks; no fixed pass count proves convergence.

The procedure does not automatically run a test, contact a model, install a skill, or create recurrence. Actual effects use the invocation's existing authority and capabilities.

## Source adaptation

Original Continuum adaptation informed by the accessible Prime Radiant `WALK.md` and the experimental Lenses Holographic Walk instrument. Source pins and limits are recorded in [research lessons](../docs/research-lessons.md). This is a project procedure, not a verbatim installation of either upstream instrument.

