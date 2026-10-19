# Recovery records: complete file states and distinct clocks

Reviewed 2026-10-19 UTC at private Base12 commit `88382e793b65c84fd8e223840c27f6bb8682864a`, tree `5cf96129bdcb0dde075f6f5800ae0c68a95c4b82`. Five texts / 71,828 bytes were fully read: helper receipt, attempts journal, invocation, effective controls and terminal envelope receipt. Every repeated attempt field and all 72 journal events were read through a complete field-preserving view: common fields, verified derived fields, all variable rows, initial-row overrides and event order reconstruct both original payloads byte-for-byte. No fields were omitted. Envelope JSON was read directly. Exact identities are in the [ledger](base12-coverage-transport-recovery.json); comparisons and arithmetic are in the [validation record](../../research/runs/base12-transport-recovery/validation.json). No transfer, helper or scientific run was executed.

## Research Delta: close this attempt without inferring global exactly-once behavior

The receipt lists 36 unique files, matching the initial outcome's exact remaining scope. Each has one requested journal row and one complete row identical to its terminal receipt entry. Every final row records HTTP 200, published true, no error, one attempt, a complete digest equal to the expected digest, and equal actual/declared/partial byte counts. Prefix digests are null after complete framing. No remaining files or orchestration error are reported.

The eighteen data files total **35,100,000 bytes** and eighteen headers total **4,372 bytes**, giving **35,104,372 received body bytes**. All data files have the exact 1,950,000-byte size; all headers fit 16,384 bytes. Those totals and all 36 size/hash declarations match the previously read later recovery inventory and intake. The new names are disjoint from the 44 initially retained files and their union equals the later 80-file inventory. Three later recovery artifact digests now bind to the acquired receipt, journal and terminal envelope payloads. Helper, prior-outcome and wrapper identities also match acquired bytes.

This supports completed states within this saved helper attempt. It does not independently rehash waveform/header payloads, recover a publisher manifest payload, observe server-side effects, or prove a host-wide exactly-once history. The earlier acquisition attempt remains a distinct recorded event. The [source review's](base12-transport-controls.md) possible post-link failed states are not observed here; a successful record does not test their recovery behavior.

## Research Delta: append order, worker intervals and socket activity differ

Reading journal events in append order gives at most four requested-but-not-yet-complete files, ending at zero. The maximum overlap of recorded worker UTC intervals is also four, agreeing with the helper's reported maximum active count. These are checks on retained worker records, not independent socket telemetry.

The first requested rows contain two small timestamp inversions in journal order. The source captures each worker's start before entering the serialized log, so append order need not equal start-timestamp order. The receipt also presents files in requested-scope order rather than completion order. None of these representations should silently stand in for another when reconstructing concurrency or causality. No clock failure or extra request is inferred.

The data-file elapsed range is **68.92955766100022–87.53871432699998 seconds**; header elapsed is **0.5270700000000943–2.4981643210003313 seconds**. Whole-file times exceeding 30 seconds are compatible with a 30-second blocking-operation timeout and the distinct cooperative 300-second file deadline. The record does not retain per-read timings, so it cannot identify the slow operation or explain throughput. Low CPU relative to elapsed time does not identify a unique bottleneck.

## Research Delta: bind resource summaries at their actual boundaries

Invocation and terminal embedded limits are equal. Effective controls match CPU affinity, 2 GiB per-process address space, 120-second CPU limits and zero core limit; root/group/session identities agree with the single wait4 record. The terminal record reports root exit zero, release, completed cleanup, no violations, no received signals and no remaining processes at root exit. It records no sampled descendants.

The helper measures **391.03869451799983 seconds** internally. The outer envelope measures **391.1402269370001 seconds**, a difference of **0.10153241900025023 seconds**. Their boundaries differ; this difference is not a directly measured attribution of startup, teardown or one overhead category. The later recovery summary uses the outer value.

Root-inclusive wait4 CPU is **2.517461 seconds**, equal to retained user plus system CPU. The conservative sampled maximum is **2.5110542849995547 seconds**, with 7,688 monitor samples declared and root maximum RSS 32,660 KiB. The wall/CPU summaries fit the declared 1,700/110-second envelope bounds. This unit binds terminal summaries and effective controls; it does not yet semantically read the 84,236-byte accounting journal or authenticate every sampled observation. No new resource experiment or crash test ran.

Cumulative semantic reading reaches **364 distinct blobs / 2,657,304 bytes**, plus **52 byte-identical alias paths**: 416 covered paths. **5,177 paths / 4,065 distinct blobs** remain without full semantic-reading claims. Archive custody and empty streams remain mechanical; the historical global acquisition aggregate is unchanged. No private raw source, receipts, operational identifiers or signal payloads are published, and no model invocation occurred. Hosted CI checks public repository behavior, not this historical transfer.

Next bounded review: recovery accounting journal/stdout and five intake envelope records, **seven texts / 87,605 bytes**. Compare sampled resource history and output projections with terminal summaries, then place intake verification at its own execution boundary. Reconcile main and ownership first; no recipient has accepted this next unit. Owned-storage and dispatch-reconciliation work remain separate.
