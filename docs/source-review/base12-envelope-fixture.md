# Envelope fixture: emitted-state evidence and partial journals

Reviewed 2026-10-19 UTC at private Base12 commit `88382e793b65c84fd8e223840c27f6bb8682864a`, tree `5cf96129bdcb0dde075f6f5800ae0c68a95c4b82`. Twelve nonempty texts / 5,561 bytes were fully read: fixture source, three sets of invocation/effective/journal records and two stdout records. Four empty stream payloads were separately verified mechanically. Exact length, Git blob framing and SHA-256 checks passed. Empty payloads add no semantic readings and do not promote all empty-blob aliases into reviewed paths. The [ledger](base12-coverage-envelope-fixture.json) preserves that distinction.

## Research Delta: close emitted-state dependencies without replaying effects

The fixture digest matches the [self-check summary](base12-envelope-controls.md). The inspected fixture defines child, inheritance, timeout, sleep and CPU modes. Inheritance starts three child processes sequentially; each child consumes at least the source's 0.12-second process-time loop before emitting its state. Timeout starts a sleeping child, prints parent state and the child PID, then sleeps. CPU mode is a busy loop. This is source intent, not a fresh execution or unique authentication of historical signal causes.

Every standalone invocation equals its terminal limits object. All three before-exec records match declared affinity, address-space, CPU and core limits plus root session/group identity. Each journal root's PID and start time match its before-exec record.

The acquired inheritance stdout contains four emitted states: parent plus three children. They satisfy the checker's affinity, 2 GiB address-space, ten-second CPU, disabled-core and common session/group assertions. Its recorded reaped-child CPU is 0.414631 seconds, exceeding the checker's 0.36-second minimum; terminal CPU and sampled maximum satisfy the corresponding saved-data comparisons. These numerical relations are now checked against available output bytes rather than a summary alone.

The emitted child PID set matches the terminal sampled PID set. Stdout does not include process start times, so that join has PID-set scope; it is not a full identity binding. Timeout's printed parent/child PIDs match the two wait4 entries, both recorded as SIGKILL. The checker's historical live `/proc` absence assertion was not repeated against the current host, where those old PIDs would have a different meaning.

All three stderr streams and CPU stdout are zero bytes in this retained set. This is actual acquired empty-payload custody for these streams, not an assertion about other runs. No fixture or wrapper was executed, and the summary still does not hash-attest the checker source itself.

For Continuum, a missing emitted-state dependency can now be promoted to a checked saved-data relation while process effects and live observations remain historical. Do not replay an old host assertion using an identifier whose original lifetime has ended.

## Research Delta: a journal is a view of monitoring activity

Each case has exactly one logged row near two milliseconds after start. Each row has zero own/reaped ticks and no descendants. Terminal records preserve additional monitor samples and later observations:

| Case | Journal rows | Monitor samples | Terminal sampled descendants | Final CPU |
| --- | --- | --- | --- | --- |
| CPU | 1 | 20 | 0 | 0.999873 s |
| Inheritance | 1 | 13 | 3 | 0.435943 s |
| Timeout | 1 | 10 | 1 | 0.031536 s |

The wrapper journals roughly once per second, while these fixtures are short. The inheritance and timeout journals therefore omit descendant observations that remain in the terminal inventory. Their zero early counters do not contradict later measured CPU. All three logged rows lie within their terminal time and CPU maxima.

A filtered journal cannot support the same absence claim as the full monitor history. The source's journal frequency, monitor counters and terminal inventory make this projection boundary explicit. Continuum's bounded evidence views should similarly retain selection/omission scope and avoid treating an unselected observation as an event that never happened.

Fixture and stdout acquisition strengthen the [preceding control review](base12-envelope-controls.md) without changing its branch-coverage result: none of the three saved cases records aggregate CPU early-stop. No new test, resource measurement, numerical program, signal decode or model call occurred. The [validation record](../../research/runs/base12-envelope-fixture/validation.json) records the actual comparisons and remaining provenance limits.

Cumulative semantic reading reaches **330 distinct blobs / 2,299,616 bytes**, plus **51 byte-identical alias paths**: 381 covered paths. **5,212 paths / 4,099 distinct blobs** remain without full semantic-reading claims. Mechanical empty-stream custody remains separate. The historical global acquisition aggregate remains unchanged because its full overlap index is unavailable. No private raw source, stdout, receipt, operational identifier or signal payload is published. Hosted CI checks public repository behavior, not private reading or historical execution.

Next bounded unit: audit closeout, post-run verification, reconnection history and stage clearance, four texts / 17,704 bytes. Inspect how later reconciliation preserves earlier uncertainty, source/run identity and authority boundaries without renewing historical effects. Reconcile main and ownership first; no recipient has accepted it and the owned-storage lane retains its separate ownership.
