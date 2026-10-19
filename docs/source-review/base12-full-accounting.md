# Full accounting: saved audit scope and execution-envelope evidence

Reviewed 2026-10-19 UTC at private Base12 commit `88382e793b65c84fd8e223840c27f6bb8682864a`, tree `5cf96129bdcb0dde075f6f5800ae0c68a95c4b82`. Four texts / 46,234 bytes were fully read: the saved full-accounting audit source/result, terminal envelope receipt and effective-before-exec record. Exact identities are in the [ledger](base12-coverage-full-accounting.json). Python syntax was parsed without importing or executing upstream code; the three JSON records were parsed with duplicate-key rejection.

## Research Delta: an audit verdict retains its dependency boundary

The acquired script's hash matches the audit result. Its explicit fifteen-file allowlist matches the result's input list; all eighty-two historical check entries say pass and the failure list is empty. These are inspected historical entries, not eighty-two new tests or independent experiments.

Nine input references now match acquired payload bytes, representing eight distinct blobs because the earlier intake is byte-identical to the runner intake. Six remain unacquired: payload-file metadata, standalone invocation, accounting journal, launch gates, static preflight and recovery outcome. All six fixed input hashes in the script agree with the report's declarations, but only three currently have payload bindings. A declaration agreeing with another declaration does not close a missing input.

The script uses ordinary `json.loads`, unlike the separate learning audit's duplicate-key-rejecting parser. The three records read here contain no duplicate keys under the current stricter parse. This is a method distinction, not evidence that historical inputs were malformed. The full-accounting audit explicitly assigns training-cost, greedy-selection and native-identity validation to the separate learning audit. The [completed training-cost replay](base12-training-costs.md) does not expand either audit's predicate.

For Continuum, retain an audit's input identities, parser and explicit exclusions alongside its verdict. A saved pass and a currently closed input set are separate facts.

## Research Delta: recorded controls, samples and final usage are distinct

The terminal receipt records clean root exit and cleanup with no reported violations, signals or remaining descendants. Its resource summary agrees with the audit result. The before-exec record binds singleton CPU affinity, a 2 GiB per-process address-space limit, a 1,800-second per-process CPU backstop and disabled core dumps. These agree with terminal limits, which also declare a 1,660-second aggregate CPU early stop, 1,700-second wall deadline, 50 ms polling and no hard real-time guarantee.

| Recorded quantity | Value | Scope |
| --- | --- | --- |
| Wrapper wall time | 140.682229 s | Saved terminal receipt |
| Final wait4 CPU | 140.628834 s | Root includes its reaped descendants |
| Conservative sampled CPU maximum | 140.630442 s | Monitor estimate, not final wait4 |
| Monitor polls | 2,782 | Terminal counter |
| Journal rows | 140 | Audit declaration; journal remains unacquired |
| Sampled descendant identities | 2 | Observed identity inventory |
| Final wait4 entries | 1 | Root entry; reaped-child CPU already included |
| Recorded maxrss | 134,344 KiB | Recorded wait4 usage, not aggregate tree memory |

The sample maximum being slightly above final wait4 is consistent with their different stated meanings. Final root-inclusive CPU must not be augmented by adding the same reaped-child CPU again. The 140 journal rows are a roughly one-second subset of monitor polling, not a complete log of all polls or proof that short-lived children never existed. The source and report already state these limits; this return preserves their qualifications rather than presenting them as newly discovered failures.

No journal or wrapper implementation was inspected in this unit, and no live controller, descendant inventory or limit enforcement was tested. Saved before-exec limits do not establish continuous enforcement for arbitrary escaping processes. Per-process address-space and CPU limits do not themselves impose aggregate tree limits. Continuum should preserve quantity scope and observation method so successors cannot silently promote sampled evidence into a stronger guarantee.

## Accounting arithmetic without payload attestation

All four arm totals, hashes, selector counts and per-record sums match the acquired final result. All eight paired rows and five charged comparisons recompute, including the learned arm's 106,501-byte saving versus fixed and 1,874-byte excess versus full family. Framing arithmetic gives a per-record raw overhead bound of 1,027 bytes: 73 header bytes plus two channels × 159 blocks × three bytes. Eight records plus the eleven-byte global header give 8,227 before dictionary bytes; literal framing overhead is 594. This checks saved fields and source-derived arithmetic, not actual archive parsing.

Training, shared encoding, four decode timers and Zstd encoding sum to 136.006087 seconds; wrapper wall time exceeds that sum by 4.676142 seconds. No cause is assigned to that gap. The audit already states that named timers omit work, shared encoding is not per-arm throughput, and Zstd encoding excludes framing preparation and decompression. No Zstd decode time is saved. These values cannot support a per-arm speedup claim.

Payload permission/hash claims depend on parent-generated metadata, which is one of the six missing inputs here; no payload was rehashed or decoded. The audit explicitly excludes stdout/stderr, so its pass does not assert empty stderr. The [validation record](../../research/runs/base12-full-accounting/validation.json) separates actual comparisons from those missing inputs and historical controls. No new inference, native execution, waveform access or host measurement occurred.

Cumulative semantic reading reaches **306 distinct blobs / 2,217,456 bytes**, plus **51 byte-identical alias paths**: 357 covered paths. **5,236 paths / 4,123 distinct blobs** remain without full semantic-reading claims. The historical global acquisition aggregate remains unchanged because its full overlap index is unavailable. No private raw source, receipt, operational identifier or signal payload is published. Hosted CI checks public repository behavior, not private reading or historical execution.

Next bounded unit: the six missing metadata inputs / 54,473 bytes. Bind their exact identities, inspect every accounting row and compare source/launch/payload declarations. Keep payload attestation and wrapper enforcement outside that metadata-only unit. Reconcile main and ownership first; no recipient has accepted it and the owned-storage lane retains its separate ownership.
