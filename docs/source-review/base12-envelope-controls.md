# Envelope controls: source ordering and saved self-check scope

Reviewed 2026-10-19 UTC at private Base12 commit `88382e793b65c84fd8e223840c27f6bb8682864a`, tree `5cf96129bdcb0dde075f6f5800ae0c68a95c4b82`. Six texts / 22,126 bytes were fully read: envelope source, self-check source, summary and three terminal self-check receipts. Python syntax was parsed without executing either source; four JSON records were parsed with duplicate-key rejection. The [ledger](base12-coverage-envelope-controls.json) records exact identities.

## Research Delta: separate release control from durable dispatch

The wrapper digest matches the full run's invocation/terminal limits, the self-check summary and all three self-check receipts. The source creates the invocation record before fork (lines 132–133). The child sets its session, affinity and resource limits, then waits on a release pipe. The parent verifies effective state and writes the before-exec record at line 176 before sending release at line 184. The child's exec follows receipt of that release byte. This is source ordering, not a newly observed execution.

Monitoring uses a process-local subreaper, descendant traversal and per-thread affinity checks plus per-process address-space, CPU and core-limit checks. The accounting estimate combines own/reaped ticks, parent-last sampling, elapsed scan allowance and tick-rounding allowances. Its stated scope is the bounded synchronous graph; polling and per-process limits retain the qualifications in the [saved accounting review](base12-full-accounting.md).

The parent observes root exit with `WNOWAIT` at line 195. It keeps the root unreaped while issuing the one group kill at line 223, then collects wait4 entries at line 234. This order preserves the root identity through group termination instead of reusing a group identifier after reaping. It does not establish that arbitrary escaped or unobserved processes are contained.

The JSON helper creates files exclusively, but this wrapper has no explicit fsync calls. The release record and terminal record therefore do not establish power-loss durability or durable supervisor-crash recovery. This is a boundary on the claim, not an observed failure or a violated durability promise. For Continuum, a release handshake, process-identity discipline and durable dispatch/effect reconciliation remain separate requirements.

## Research Delta: inspect what each self-check actually tests

The checker launches three separately configured wrapper/fixture processes and reads their receipts. Its inheritance assertions also depend on fixture-emitted stdout, not just a terminal receipt. The summary has four named categories covering inherited controls, retained child CPU, parent/child wall timeout and the kernel per-process CPU limit. The acquired checker source is not itself hash-attested by that summary; fixture source and inheritance stdout remain unacquired in this unit.

| Saved case | Status / reason | Final CPU | Wall time | Terminal evidence |
| --- | --- | --- | --- | --- |
| Inheritance | complete / root exited | 0.435943 s | 0.662405 s | One zero-exit root entry; three sampled descendants |
| Wall timeout | incomplete / wall limit | 0.031536 s | 0.550816 s | Two wait4 entries, both SIGKILL; cleanup complete |
| CPU | incomplete / root exited | 0.999873 s | 1.014143 s | One SIGKILL root entry; cleanup complete |

All three receipts bind the wrapper digest, and their wait4 sums reconcile. Their statuses agree with the source's terminal acceptance predicate: normal root exit, zero exit code, complete cleanup and no recorded violations. An incomplete resource check still has observed process effects; status does not mean nothing executed.

The timeout requests termination at 0.500166 seconds under a 0.5-second wall setting, then records about 0.050650 seconds of cleanup. Those distinct quantities should not be collapsed into either an exact half-second execution guarantee or a timeout failure.

The CPU case configures both a one-second per-process backstop and one-second monitored early stop. Its actual reason is root exit, its sampled maximum is 0.970437 seconds and its root exit code is SIGKILL. This is consistent with the checker's kernel-limit interpretation, but the terminal fields do not uniquely attribute the signal's cause. The checker asserts SIGKILL and a CPU range; it does not require the aggregate-stop reason. None of these three receipts records the aggregate early-stop branch. A passing self-check summary therefore does not establish execution coverage of every controller branch.

For Continuum, preserve test exposure, actual terminal reason and assertions alongside category names. A test's title is not its acceptance predicate, and a saved pass does not broaden its scenario coverage.

## Current evidence boundary and next unit

No self-check, wrapper, fixture, numerical code or model call ran here. No process-absence assertion was checked against the current host, and no arbitrary escape, supervisor loss or scheduler-starvation experiment was performed. Fixture hash and stdout-based inheritance assertions remain unbound until those payloads arrive. The [validation record](../../research/runs/base12-envelope-controls/validation.json) preserves source-line anchors, actual comparisons and these missing dependencies.

Cumulative semantic reading reaches **318 distinct blobs / 2,294,055 bytes**, plus **51 byte-identical alias paths**: 369 covered paths. **5,224 paths / 4,111 distinct blobs** remain without full semantic-reading claims. The historical global acquisition aggregate remains unchanged because its full overlap index is unavailable. No private raw source, receipt, operational identifier or signal payload is published. Hosted CI checks public repository behavior, not private reading or historical execution.

Next bounded unit: the self-check fixture, three sets of invocation/effective/journal records and two nonempty stdout records, twelve texts / 5,561 bytes, plus four empty stream payloads for mechanical custody only. Bind the fixture and inspect emitted state, sampled records and receipt consistency without executing upstream code. Empty payloads do not add semantic readings. Reconcile main and ownership first; no recipient has accepted it and the owned-storage lane retains its separate ownership.
