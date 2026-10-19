# Native execution, build and measurement boundaries

Review date: 2026-10-19 UTC. Source: private Base12 commit `88382e793b65c84fd8e223840c27f6bb8682864a`, tree `5cf96129bdcb0dde075f6f5800ae0c68a95c4b82`. This completes direct reading of all six files / 25,430 bytes in `research/owned-stack/2026-10-15/native-execution-reset/`. The [additive ledger](base12-coverage-native-reset.json) identifies every file by Git blob, raw SHA-256, length and line count. Private source and historical messages remain outside this public repository.

This is source review. No upstream decoder, compiler, benchmark, data acquisition or collaborator invocation ran. Historical requests are material being examined, not current instructions to Continuum or an upstream worker.

## Research Delta: native execution is one part of an ownership claim

The group's README and saved consultation ledger distinguish three gates: complete native application execution, a native routine builder consuming editable source, and reproducible rebuilding of that builder and application. The original design includes a native measurement controller in its wider execution gate. A later integration guide describes a bounded scalar decoder correctness result while explicitly leaving the controller and builder milestones unestablished. Completing one component therefore does not silently satisfy the composite gate.

For Continuum, native Rust execution, ownership of acceptance semantics, an owned storage kernel, and ownership of the compiler are separate claims. The working SQLite implementation remains a useful baseline while [ADR 0002](../decisions/0002-owned-storage-research.md) investigates the kernel. Reproducible bytes alone would not establish compiler correctness or eliminate shared bootstrap defects. No new compiler or database implementation is selected by this reading.

Source anchors: `README.md`, `CLAUDE_REVIEW.md`, `INTEGRATION.md`. The consultation file is an authored summary/correction ledger of two historical supplied-text consultations; it is not their complete raw exchange, fresh model review, code inspection or independent experimental confirmation. `USER_MESSAGE.md` preserves the triggering instruction and declares limits to the earlier dialogue supplied. Its reading does not import that project's historical authority into this one.

## Research Delta: timing boundaries belong to the experiment contract

`MEASUREMENT.md` separates resident kernel, whole operation, fresh process, build/specialization/cache, and device/complete host-to-result boundaries. Parsing, validation, allocation and output checks belong in whichever whole-operation claim includes them. Launch-inclusive timing starts in the parent; a faster isolated child region cannot establish a faster full launch. First-use and reused-build costs need separate accounting. These are proposed measurement contracts in the reviewed source, not newly observed performance results.

Continuum's existing in-process release workload, CLI reservation probe and complete checkpoint attempts exercise different boundaries. Their numbers should remain attached to those boundaries rather than becoming a combined speed claim. A future owned-kernel comparison should fix semantic checks, included setup/recovery work, reuse state and the measured interval before comparing costs. The source also corrects an overly broad anti-Python conclusion: a Python-supervised native child can still provide a valid measurement for its declared boundary. Runtime ownership and measurement validity are different questions.

The cited external timing and platform references were not independently reopened for this reading. No hardware advantage, cold-cache result, target-device execution or broad decoder correctness claim is added.

## Research Delta: preserve historical packets and append narrower outcomes

The integration guide keeps the original design documents unchanged while explaining later reported outcomes and consumed execution clearance. Its manifest binds five original files; four are inside this six-file review. All four match the recorded Git blob, length and SHA-256. The fifth is an external historical handoff, outside the selected scope: it was not retrieved or checked. The integration guide and manifest themselves also have pinned acquisition identities, but are not among their own four checked original bindings.

The guide reports a later bounded decoder batch and linked merges. Those linked implementations, raw runs and recipient replies were not newly examined here. Treat the guide as historical authored navigation, not fresh reproduction or proof of current worker acceptance. It explicitly preserves the distinction between a Python-free runtime and a Python-bootstrapped build, and between a bounded decoder result and the wider original gate.

Continuum already retains immutable attempt evidence and appends corrections. A successor should similarly receive the old plan together with the exact completed subtask, outstanding components and current ownership evidence. An old packet saying a task is pending must not cause an already consumed external invocation to be repeated. No upstream dispatch, historical clearance reuse or worker activation occurred here.

## Coverage and validation

All six decoded files matched the pinned tree's Git blob and byte length; raw SHA-256 was recomputed. Five Markdown files were fully read, the JSON manifest was fully read and parsed, and four in-scope original-file bindings passed. No upstream code was imported or executed. The [validation record](../../research/runs/base12-native-reset/validation.json) preserves these mechanical checks separately from semantic reading.

Cumulative direct reading is **177 distinct blobs / 1,282,502 bytes**, plus **47 additional byte-identical alias paths**. This covers 224 paths by direct reading or byte equality; **5,369 paths / 4,252 distinct blobs** still have no complete semantic-reading claim. Alias directory context is not promoted into another reading. Whole-repository review remains incomplete.

The earlier exact-acquisition aggregate of 539 paths / 530 blobs / 4,536,603 path bytes remains historical. Its full private acquisition index was not recovered, so these six fetches may overlap previously acquired unread files and are not added to that aggregate. Hosted CI checks public changes; it cannot independently confirm private-source reading or recover private payloads.

Next bounded source unit: five distinct unread files / 20,074 bytes in the pinned `research/owned-stack/2026-10-15/signal-learning-readiness/` group. Reconcile current main and ownership first. Selection is not recipient acceptance or execution authority; the separate owned-storage model lane retains its ownership.
