# Execution, context, and model evolution

Status: portable design contract; live model invocation and automatic context preparation are not implemented in the first Rust slice.

## A model name is not an execution identity

Record the requested provider route and the actual response metadata separately. The same model label can sit behind an alias, regional deployment, routing profile, or provider revision that is not exposed. Unknown revision means unknown; do not infer exact weights from a friendly name.

An execution description should include:

| Group | Fields |
|---|---|
| Logical identities | Objective, principal, worker, conversation, host, attempt, operation |
| Provider selection | Vendor, service, API family, requested model, region or deployment when relevant |
| Observed identity | Returned model identifier, revision if exposed, provider request ID, observation source |
| Requested settings | Reasoning mode and effort, thinking configuration, output budget, sampling settings where supported |
| Effective settings | Known resolved settings, ordered configuration updates, provider-reported values, unknown fields |
| Software and inputs | Harness/tool versions, prompt and context hashes, source snapshot, environment, protocol revision, policy/grant references |
| Outcome | Visible outputs, errors, stop reason, partial result state, actual tool-effect receipts |
| Resources | Reported token usage, measured elapsed time and resource use, cost with rate source and date if calculated |

A claimed field and a provider-reported field are both statements with sources. Neither proves the provider's hidden implementation. A transport signature authenticates a sender; it does not prove model quality.

Do not impose a universal numeric thinking-depth scale across providers. Preserve namespaced settings and their meanings. Do not silently drop a required capability or substitute a provider when an adapter cannot meet the request.

Current official OpenAI documentation distinguishes reasoning mode from effort and documents configuration updates whose effective effort can differ from the request-level response field. The adapter therefore needs configuration history, not just one copied response property. Source: [OpenAI reasoning guide](https://developers.openai.com/api/docs/guides/reasoning).

Bedrock Converse exposes a shared inference configuration plus additional model-specific request and response fields. Preserve both layers rather than pretending every model has identical controls. Source: [AWS Converse API](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html).

No API key or private credential belongs in an immutable public artifact. Use an opaque runtime credential reference. Record enough identity to reproduce authorized configuration without publishing account secrets or unrelated private inputs.

## Adapters in order

1. **Manual import and local CLI:** represent the actual cross-model collaboration already taking place.
2. **One common tool surface:** small structured operations for inspect, prepare-context, propose, acknowledge-handoff, and reconcile-operation. Add an MCP adapter and ordinary CLI around the same contracts.
3. **One real provider runner:** use the user's existing authorized Bedrock route when integrated, with bounded spending, identity capture, streaming partial results, and uncertain-response reconciliation.
4. **OpenAI runner:** use current documented APIs after credentials and policy exist. Provider identity and capability negotiation remain explicit.
5. **Local model runner:** add a local service such as Ollama only when a task demonstrates useful cost, privacy, latency, or offline value.
6. **Routing and fleet scheduling:** follow measured workload demand.

Provider plugins should be replaceable. The native engine must open and inspect a project with no model service available. Model calls are computations that produce attempts and observations; they do not own the canonical state.

A provider request ID is useful for reconciliation but is not automatically an idempotency key. On timeout, record an unknown inference outcome when the provider might have run the request. Do not automatically spend again merely because no visible answer arrived.

## Context packs

A context pack has a stable exact-byte identity and structured selection metadata:

- Objective and source snapshot.
- Query or selection procedure and revision.
- Token or byte budget and tokenizer/measurement method.
- Included items, source identities, selection reasons, and ordering.
- Known omissions, unavailable sources, truncation, and coverage scope.
- Active constraints, pending disagreements, next action, and reopening conditions.
- Access/disclosure scope and any redacted projection relationships.

Store exact rendered bytes when permitted. A hash of a summary alone does not show that its claims are faithful. Typed extracts can be checked mechanically; arbitrary prose needs source review. A stale-context detector works only over declared or discoverable dependency relations. It should emit a review candidate, not invalidate a decision automatically.

The high-value first experiment is context recovery: can a fresh agent identify the accepted state, most important uncertainty, and next action without rereading the entire project or duplicating completed work?

## Collaboration as a controlled method

Use different models for roles that supply a useful contrast: independent framing, implementation, counterexample search, and integration review. For an independent judgment, collect first-pass proposals before showing each model the other proposal. Then expose disagreements and ask for the smallest discriminating observation.

A collaborative result records exposure: which source excerpts and previous answers each participant saw. Two models reading the same mistaken input can agree incorrectly. A different vendor is not automatically an independent instrument.

A bounded collaboration method should preserve:

- Initial independent proposals.
- Shared artifacts and exact exposure boundaries.
- Disagreements and reasons.
- Empirical or formal checks when available.
- A named integrator's decision and remaining uncertainty.

Do not build a debate tournament or universal model parliament into the first kernel. The graph can represent this method before the method has a custom runtime.

## Reliability without model prestige

A frontier model can be a sensible candidate for a difficult task. Its name does not make each output reliable. A smaller model may outperform it on a narrow evaluated workload; a deterministic compiler or direct observation may provide stronger evidence for a specific claim.

Keep calibration by task family, evaluator, environment, time, and sample size. Preserve the uncertainty and selection biases. Do not convert one global model score into truth or authorization.

A later model release can create a targeted re-evaluation proposal, especially where a consequential decision depends on unverified model judgment, a weak result, an unresolved uncertainty, or a known capability gap. It should not automatically rerun all historical work or invalidate sound independent evidence.

## Workflow vocabulary

| Operation | Meaning |
|---|---|
| Inspect | Read existing state without producing another attempt |
| Replay records | Reconstruct a recorded sequence or deterministic projection |
| Re-execute | Run a new attempt against explicitly selected inputs |
| Re-evaluate | Apply a new evaluator or protocol to preserved outputs |
| Fork | Create an alternative investigation with shared immutable ancestry |
| Rebase premises | Reconsider an attempt under changed inputs or assumptions |
| Compare | Evaluate alternatives under a declared common contract |
| Resume | Continue from a supported checkpoint, otherwise start a new attempt |
| Reconcile | Recover the known/unknown result of an existing operation |
| Cancel | Request cessation; preserve actual completion or unknown outcome |
| Supersede/retract | Append a correction or withdraw a claim within a scope |
| Undo accepted state | Accept a previous root at a new generation after current checks |
| Compensate | Perform a new authorized action addressing an external effect |
| Pin/archive | Set an explicit retention promise |
| Promote | Accept an exact composition for a named target or channel |

Re-executing an LLM with the same prompt is a new sample, not bitwise replay. Sampling seeds alone rarely establish a closed reproducible environment. Cached output is not an additional independent sample.

## Evidence applicability

Use applies / does_not_apply / unknown for a specific target and reuse contract. Exact file hashes are insufficient when results also depend on directory listings, absent paths, environment variables, clock, randomness, network responses, hardware, or concurrency.

Reuse requires declared input closure and enforcement appropriate to the claim. A replayed network response is evidence about the recording, not a fresh observation of the live service. State which meaning the workload needs before deciding that a cached result is reusable.

