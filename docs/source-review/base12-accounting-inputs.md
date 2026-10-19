# Accounting inputs: complete saved set and sampled journal

Reviewed 2026-10-19 UTC at private Base12 commit `88382e793b65c84fd8e223840c27f6bb8682864a`, tree `5cf96129bdcb0dde075f6f5800ae0c68a95c4b82`. Six texts / 54,473 bytes were fully read: payload-file metadata, invocation, the complete 140-row accounting journal, launch gates, static preflight and the recovery outcome with all eighty inventory rows. Length, Git blob framing and SHA-256 checks passed; every JSON object was parsed with duplicate-key rejection. The [ledger](base12-coverage-accounting-inputs.json) records exact identities. No upstream program ran.

## Research Delta: input closure changes one specific claim

All fifteen inputs of the [full-accounting audit](base12-full-accounting.md) now match acquired payload bytes. They represent fourteen distinct blobs because the earlier intake and runner intake are identical. All six fixed input pins in the audit source now have byte bindings. This closes the earlier six-input gap; it does not turn the historical eighty-two passes into a new audit execution or independent experimental evidence.

The invocation equals the terminal receipt's limits object exactly, and launch-gate limits agree. All fourteen static source-manifest entries match acquired bytes, sizes, SHA-256 and Git blob identities, with explicit identical-blob aliases where the exact preserved path is not cached. The six runner source declarations and protocol digest also match. These checks establish payload agreement with a declared manifest; they do not newly prove the original source head's complete changed-file set.

The seven payload metadata entries reconcile with saved result sizes, hashes and receipt links. Their permission and owner fields remain parent-generated historical observations. The compressed literal's digest has no corresponding digest in final RESULTS to compare; its saved size does agree. No archive, framed signal, original waveform or header bytes were opened or freshly attested.

For Continuum, input closure should be a precise change in evidence state. A dependency is now available for inspection; historical execution, provenance and live filesystem facts retain their own acceptance conditions.

## Research Delta: inspect the journal's actual granularity

All 140 rows preserve the root identity, process group and session. Times strictly increase, root own/reaped CPU tick counters never regress, and all rows stay within the terminal time and conservative CPU maxima. Five rows contain descendants; their two distinct identities exactly match the terminal sampled inventory. This is consistency of the saved samples, not proof that no other process existed between them.

| Saved journal quantity | Recomputed value |
| --- | --- |
| First / last elapsed time | 0.002905 / 140.579955 s |
| Interval minimum / maximum | 1.009677 / 1.017700 s |
| Mean interval | 1.011346 s |
| Maximum logged conservative CPU | 140.590731 s |
| Terminal monitor maximum | 140.630442 s |
| Rows with descendants | 5 of 140 |
| Last sample to recorded root exit | 0.102021 s |

The journal is a subset of the 2,782 monitor polls. Its last sample is not the terminal event, and its maximum is lower than the terminal monitor maximum. The last root sample has 13,592 own ticks and 463 reaped-child ticks; the latter agrees with the audit summary. It also includes a later child's identity with zero own ticks at that instant. Zero sampled ticks do not establish that the child did no work over its lifetime. A process state letter is likewise an instant's observation, not an interval utilization measurement.

The final root-inclusive wait4 value remains a separate terminal measurement; do not add reaped-child CPU to it again. No tick-to-second conversion or attribution to particular commands is made from these records. Continuum should preserve both observation granularity and terminal summaries so a successor can reason about gaps without inventing an event history.

## Historical stages retain their capture-time meaning

The eighty-row recovery inventory exactly matches intake: sixty-four training files, sixteen validation files, 78,000,000 declared waveform bytes and 78,009,188 total source bytes. The recorded thirty-six new files plus forty-four retained files reconcile with eighty. The retained-file unchanged claim and publisher-hash claims were not independently checked against actual signal payloads or the publisher here. Recovery helper and transport artifact identities remain declarations; their payloads were not acquired in this unit.

Timestamps order static preflight, transport recovery, launch gates, runner pre-run, model freeze and payload metadata. Static preflight holds execution and has empty data; recovery reports transport/hash inventory completion while structural checking is pending and scoring has not begun; later launch gates report the structural check passed. These capture-time statements can all be valid. They should be retained, not overwritten with the latest stage or misread as simultaneous contradictory states. The historical launch gate's publication flag does not grant current authority; no historical invocation is renewed.

The [validation record](../../research/runs/base12-accounting-inputs/validation.json) preserves actual input/source bindings, journal arithmetic and timestamp comparisons. No new model call, live resource measurement, wrapper enforcement check, signal decoding or upstream audit execution occurred.

Cumulative semantic reading reaches **312 distinct blobs / 2,271,929 bytes**, plus **51 byte-identical alias paths**: 363 covered paths. **5,230 paths / 4,117 distinct blobs** remain without full semantic-reading claims. The historical global acquisition aggregate remains unchanged because its full overlap index is unavailable. No private raw source, receipt, journal row, operational identifier or signal payload is published. Hosted CI checks public repository behavior, not private reading or historical execution.

Next bounded unit: the envelope implementation, self-check source, self-check summary and three terminal self-check receipts, six files / 22,126 bytes. Compare actual enforcement logic and tested scenarios with the stated monitor limits, without executing the upstream code. Reconcile main and ownership first; no recipient has accepted it and the owned-storage lane retains its separate ownership.
