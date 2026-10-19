# Signal-learning readiness and comparison contracts

Reviewed 2026-10-19 UTC at private Base12 commit `88382e793b65c84fd8e223840c27f6bb8682864a`, tree `5cf96129bdcb0dde075f6f5800ae0c68a95c4b82`. All five documents / 20,074 bytes under `research/owned-stack/2026-10-15/signal-learning-readiness/` were read completely. Exact source identities are in the [additive ledger](base12-coverage-signal-readiness.json); private payloads remain outside this public repository.

This unit reviews the readiness documents, not a fresh execution or a new audit of their referenced implementation. No upstream module, data, learner, decoder, benchmark or model consultation ran.

## Research Delta: derive the possible benefit before measuring it

`COST_BOUND.md` describes a nested predictor family. A smaller learned dictionary retains every baseline candidate; the full family retains every learned candidate. Under identical framing and choice-independent future context, the full family cannot have a larger minimum block payload. Its possible size disadvantage is therefore bounded by extra serialized dictionary entries.

In the documented one-stream format, the full family has 35 optional entries and the learned arm has L, with each entry costing one byte. Thus `size(full) - size(learned) <= 35 - L`. At L=4, the ceiling is 31 bytes for the entire archive, not per record or block. The documented baseline relation is also useful: adding L entries can increase total size by at most L bytes while preserving the baseline's payload choices. Neither bound predicts the selected entries or actual sizes.

The conditions matter. Predictor choice must not change later context; the source attributes that property to using actual reconstructed history. Repeating dictionaries in multiple streams changes the overhead bound. Changing framing, selector sizes or the available candidates requires a new derivation. We reviewed that argument as written; the underlying codec and driver were not newly acquired or checked in this unit, so their compliance remains attributed to `SOURCE_REVIEW.md`.

For Continuum, a proposed compression or context-selection benefit should state its accounting unit, candidate inclusion and downstream dependencies. A result outside a valid bound is a reason to inspect execution and accounting. This compression theorem is not a universal theorem about AI context: a representation can change a successor's choices and future retrieval costs, violating its assumptions.

## Research Delta: paired outputs and shared work answer different questions

The readiness documents describe four arms evaluated with shared candidate computation. Their candidate-count reduction is an analytical work-count observation, not separately measured encoding throughput. The source also corrects a broad claim that dictionary reduction cannot affect decoding speed: the decoder's one selected predictor count does not determine the cost of the selected predictor or code. No direction or magnitude follows without measurement.

`README.md` and `SOURCE_REVIEW.md` reject using an older codec's archive size as the new learner's baseline because prediction bounds, history resets, partitioning and wire format differ. A valid comparison uses the new task's matched arms. The source's saved real-record outcome is attributed historical evidence, not reproduction here or evidence of a radix advantage.

Continuum's future context experiments likewise need matched source/task exposure, omission rules, scoring and cost boundaries. Shared retrieval or cached computation may support a paired outcome comparison while preventing attribution of independent per-arm cost. This reading does not add a performance claim to the completed CSV pilot.

## Research Delta: readiness failures can consume a scientific attempt

`SOURCE_REVIEW.md` identifies a reference-software check occurring only after validation streams are generated. The proposed external readiness check would detect that prerequisite before the scored exposure. Installing a missing comparator afterward must not silently turn a completed exposure into an unseen first attempt. Retain partial outputs and disposition before considering a successor.

`CONCURRENT_UPDATE.md` records discovery of an existing execution owner and narrows the request to coordination with that owner. It does not establish that owner's present state. Publication, historical acknowledgement, current ownership and actual execution remain separate. No historical request was sent or replayed here.

`REVIEW_AND_ALIGNMENT.md` summarizes two historical supplied-context Claude consultations and explicitly limits their exposure. It is not a complete raw exchange or independent execution. It also records source and scientific interpretations; the linked external references and underlying claims were not independently reopened or validated in this reading. The five documents are a bounded source return, not a blanket endorsement of their broader project.

## Coverage and continuation

All five decoded files matched the pinned tree's Git blob and length, and raw SHA-256 was recomputed. Five UTF-8 full readings were completed. The [validation record](../../research/runs/base12-signal-readiness/validation.json) separates these checks from the unperformed implementation audit and execution.

Cumulative direct reading reaches **182 distinct blobs / 1,302,576 bytes**, plus **47 additional byte-identical alias paths**. That covers 229 paths by reading or byte equality; **5,364 paths / 4,247 distinct blobs** still lack a complete semantic-reading claim. Alias directory context is not separately reviewed. The historical acquisition aggregate remains 539 paths / 530 blobs / 4,536,603 path bytes: its full overlap index was not recovered, so new fetches are not blindly added. Hosted CI cannot independently confirm this private-source reading.

Next bounded review: three distinct unread documents / 20,038 bytes in the pinned `research/owned-stack/2026-10-15/learning-performance-followup/` group, after reconciling fresh main and ownership. No recipient acceptance or upstream execution authority is claimed. The separate owned-storage model lane retains its ownership.
