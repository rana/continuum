# Stage-A launcher: implemented controls and their dependencies

Reviewed 2026-10-19 UTC at private Base12 commit `88382e793b65c84fd8e223840c27f6bb8682864a`, tree `5cf96129bdcb0dde075f6f5800ae0c68a95c4b82`. Seven files / 21,611 bytes were fully read: launcher and acquisition source, launcher review/freeze, parent clearance, environment and intake verification. The [ledger](base12-coverage-stage-a-launcher.json) records exact identities. Two Python sources were parsed without import; four JSON records were parsed as data.

No helper, acquisition, native code, timer, model or research run was executed. Private paths, parent identities and executable/payload identifiers remain outside this public report. Historical records and source inspection do not independently authenticate execution or current authority.

## Research Delta: consuming an attempt is deliberately earlier than learning its outcome

The launcher creates a fresh run directory and an exclusive attempt file, flushes/fsyncs that file, then starts the child. Syntax inspection places the marker fsync at line 115 and `Popen` at line 119. Existing directories or markers stop another ordinary invocation; the code contains no automatic retry. The marker persists even if launch fails, which conservatively preserves the possibility of an external effect.

This is a useful bounded mechanism for Continuum's future executor work: record the exact attempted request before issuing its effect, then append the observed outcome separately. It is not an exactly-once external-execution proof. The marker does not establish sender authentication, immutable dependencies or recovery after every filesystem/power failure. A stale consumed marker requires reconciliation rather than automatic deletion or another invocation. We inspected the source, not a fault-injected launch.

The earlier receipt review now has a concrete producer to compare with its records. The helper freeze matches both acquired source files, and the acquired parent-clearance record equals the clearance copied into the saved execution receipt. These are content links, not independent confirmation that the recorded runtime controls were active.

## Research Delta: enforcement depends on both the controller and its invocation

The launcher applies the declared resource limits before child execution, starts a new session, waits with a wall timeout, and kills the process group on timeout, ordinary completion and handled Python exceptions. Its CPU/address-space limits remain per-process, not aggregate process-tree quotas. The wall-time cleanup depends on the live controller; an uncatchable controller kill or machine failure cannot run its cleanup code. Recorded waited-child usage also includes the preflight version subprocess and is not exact native-kernel CPU cost.

The saved review explicitly requires non-optimized Python because the helpers use assertion-based admission checks. Syntax inspection finds nineteen assertion statements in the launcher and seven in acquisition. The child's recorded interpreter arguments do not by themselves prove the mode used to invoke the parent helper. No assertion bypass or incorrect historical mode was observed. The lesson is to bind the producer's own invocation conditions and failure model, not only its child command and source digest.

Continuum should distinguish a controller's implemented timeout path from an independently surviving supervisor. It should also state which invocation and environment facts make its checks effective. This reading installs no executor, watchdog or new schedule.

## Research Delta: bind the manifest before trusting what it names

The historical launcher review records a concrete preflight correction: an extracted manifest was initially trusted without binding it to the approved source archive. The final launcher reads the archived manifest, compares its bytes to the extracted copy, and validates the listed packet files from that approved manifest. Both final helper identities match their freeze. The earlier launcher version is named by digest but its bytes were not acquired here.

The source still depends on trusted stable paths while hashing and later loading files; the archive itself is hashed and then reopened for parsing. This repeats the conditional checked-path/consumed-bytes distinction in the earlier decision-gate review. No path replacement was executed and no historical failure is inferred. Correcting one manifest relationship does not establish every immutability assumption or turn the helper into a general untrusted service.

The acquisition helper restricts itself to a fixed list, rejects redirects, counts response-body bytes with bounded lookahead, retains failed partial files and finalizes only after its declared checks. Its four per-file caps sum to 4,047,295 bytes; even four extra lookahead bytes remain below the declared 4 MiB total. That is arithmetic over this fixed list, not measurement of network overhead or proof of historical enforcement. Its conservative exposure flag is set before requesting either signal/header payload. The reviewer also notes that the helper contains no internal acquisition timestamps; later readers must not manufacture them from unrelated receipt times.

## Validation and continuation

All seven byte strings match the pinned tree's Git blob and length; raw SHA-256 was recomputed. Intake file-size/hash declarations agree across the saved acquisition and verification records, without retrieving their original payloads. Twelve of twenty-seven delivery-manifest entries and twenty-seven of forty-nine preservation entries now match acquired bytes; remaining entries are explicit. The [validation record](../../research/runs/base12-stage-a-launcher/validation.json) preserves each check separately from source-derived observations and execution.

Cumulative direct reading reaches **237 distinct blobs / 1,551,628 bytes**, plus **48 byte-identical alias paths**. This covers 285 paths by reading or byte equality; **5,308 paths / 4,192 distinct blobs** remain without complete semantic-reading claims. Alias directory context is not separately reviewed. The historical acquisition aggregate remains 539 paths / 530 blobs / 4,536,603 path bytes because its full overlap index was not recovered; new fetches are not blindly added. Hosted CI checks the public contribution, not private reading, control enforcement or historical actions.

Next bounded unit: three unread result documents / 67,473 bytes in the same retained evidence: `review/RESULT.md`, `review/result-static-verification.md` and `run/RESULTS.json`. Reconcile main and ownership; connect the complete numerical record to the source and receipts without rerunning the codec. No recipient has accepted that unit. The separate owned-storage model lane retains its ownership.
