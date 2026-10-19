# Roadmap

Milestones are gated by demonstrated behavior, not promised dates.

## 0. A reviewable foundation

Deliver exact-byte objects, a documented snapshot model, transactional acceptance with expected generation, durable operation receipts, a working CLI, and failure-oriented tests. Preserve both historical briefs as faithful Markdown. Add the initial protocol definitions and current design decisions.

Exit: compile and run locally; retries, stale heads, concurrent candidates, and crash boundaries behave as documented. State the limits precisely.

## 1. Continuing work across two sessions

Add minimal Objective, Attempt, Decision, Handoff, and ContextPack schemas plus inspection and explicit handoff receipts. Implement one budgeted context query with coverage and source references. Use it on a real project with two separately started sessions.

Exit: a new session restores the right state and next action without repeating completed work; disagreement and missing context remain visible.

## 2. One common tool adapter and one model runner

Expose the same operations through a small structured tool interface and CLI. Add one authorized provider runner, starting with the existing Bedrock route when available. Capture actual metadata, input exposure, resource use, partial output, and unknown outcomes. Add bounded multi-model comparison as a selectable protocol.

Exit: one real end-to-end task survives interruption and reconciliation. No universal vendor router is required.

## 3. Two hosts and measured capacity

Add verified object exchange, missing-object negotiation, access controls, and recipient-authored handoffs. Keep accepted-target authority explicit. Observe executor capability and resource usage before adding placement.

Exit: a task continues on another host without corrupting artifacts or misrepresenting ownership. A late worker cannot violate the receiving service's enforced authority.

## 4. Evidence applicability and targeted re-evaluation

Represent declared input closure and evidence scope. Add reverse indexes from premises and context selections to decisions. Propose re-evaluation on relevant changes, including a new evaluator/model capability when justified.

Exit: changed declared premises select affected work, sound results are retained, unknown dependence stays unknown, and budgeted evaluation demonstrates practical value.

## 5. Measured native optimization

Profile representative work. Improve query planning, object layout, transaction contention, context preparation, or execution placement where measurement identifies the limiting cost. Use lower-level code only for a demonstrated hotspot.

Exit: reproducible performance evidence with correctness and recovery preserved.

## 6. Open ecosystem and longevity

Publish a portable object specification, conformance fixtures, export/import contracts, and a second independent reader. Add Git interoperability, provider adapters, and protocol catalogs that share core contracts. Exercise schema/hash migrations and selective retention.

Exit: an independent implementation can interpret retained data without relying on the original service.

## Reconsider or stop

Reopen the plan if existing tools solve the measured problem adequately, the graph costs more to maintain than it saves, context packs repeatedly omit decisive information, or usage cannot demonstrate better continuation than a simpler baseline. The mission is effective work, not building every imaginable subsystem.
