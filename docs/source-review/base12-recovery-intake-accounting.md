# Sparse resource history and the intake boundary

Reviewed 2026-10-19 UTC at private Base12 commit `88382e793b65c84fd8e223840c27f6bb8682864a`, tree `5cf96129bdcb0dde075f6f5800ae0c68a95c4b82`. Seven texts / 87,605 bytes were fully read: recovery accounting journal/stdout and intake invocation, effective controls, terminal receipt, accounting row and stdout. Every field of all 385 recovery rows was read through a lossless view of common identities and variable elapsed/upper-CPU/state/tick values. Rebuilding the rows reproduces the original journal bytes exactly; the other six files were read directly. Exact identities are in the [ledger](base12-coverage-recovery-intake-accounting.json); checks and source line anchors are in the [validation record](../../research/runs/base12-recovery-intake-accounting/validation.json). No source or historical operation ran.

## Research Delta: journal cadence is not monitor cadence

All 385 recovery rows preserve the same root identity, parent, group, session and start identity, matching effective controls. Own CPU ticks increase from zero to 249 without decreases; reaped ticks stay zero and descendants are empty. The leader is recorded running in the first row and sleeping in the other 384. That is process-leader state at sampled instants, not a description of every thread or a bottleneck diagnosis.

The journal spans **0.003216082999642822–390.7313185009998 seconds**. Its 384 intervals range **1.0134357329998238–1.0212593740006923 seconds**, averaging **1.0175211000468753 seconds**. The wrapper increments its monitor counter and updates a running maximum each loop, but normally writes a row only after at least one second. Its declared **7,688 monitor samples** therefore need not equal 385 journal rows. Root-exit detection can break before a final snapshot. The last journal row precedes terminal wall time by **0.4089084360002744 seconds**; the journal is not a complete syscall, state-transition or monitor history.

The journal's maximum conservative upper estimate is **2.510801750000392 CPU seconds**, below the terminal monitor maximum **2.5110542849995547**, itself below exit wait4 CPU **2.517461**. Every journal estimate and elapsed value fits the declared stop bounds. This reconciles the retained summaries without reconstructing unlogged samples or asserting that no unobserved transient event occurred.

## Research Delta: instantaneous bounds can fall while cumulative work rises

The journal's `upper_cpu` estimate decreases on 102 adjacent steps even though own ticks never decrease. Source inspection explains the distinction: each estimate adds the current scan duration and tick margin to accumulated ticks; the monitor separately retains the maximum over samples. A varying instantaneous margin need not be monotone. There is no negative CPU work implied by those steps.

For Continuum, identify whether a reported number is a counter, instantaneous estimate, running maximum or exit account before imposing consistency rules. Comparing the last journal value, journal maximum and terminal maximum as though they were one quantity would reject a consistent record. No current-host tick rate was substituted for the historical runtime's value.

Recovery stdout is the exact four-field projection of the helper receipt: complete status, 35,104,372 body bytes, maximum active count four and no remaining files. This closes output projection custody, not another independent transfer observation.

## Research Delta: intake verification has its own scope

The intake command runs `corpus.py --dir` without `--acquire`. Invocation equals terminal embedded limits; wrapper identity, CPU affinity, 2 GiB per-process address space, 120-second CPU limits, zero core limit and root/group/session identities reconcile. The receipt records a clean root exit, release and cleanup without violations or sampled descendants.

Its wall time is **0.10317648899945198 seconds**, wait4 CPU **0.09389399999999999**, monitor maximum **0.06025052100045286**, and root maximum RSS 28,152 KiB. There are two declared monitor samples but only one journal row, at **0.0022612639995713835 seconds**, with zero CPU ticks and upper estimate **0.02017333300002065**. As with recovery, the early sparse row does not reconstruct terminal CPU.

The saved stdout says that 80 files were verified and the test partition is locked. Its file count agrees with the retained intake and pre-run gate, and the gate's intake digest matches acquired bytes. The already read source dispatches verification without acquisition, hashes named training/validation files and checks structural header fields. Packing and overlap remain the later runner's responsibility. No waveform/header bytes were rehashed, headers parsed or numerical checks rerun here.

The source's verification loop does not enumerate unlisted directory entries. Its test-lock output describes its allowed access scope; stdout alone does not prove that no test or extra file exists anywhere in the directory or host. The earlier recovery inventory and pre-run gate carry their own absence claims. The intake CLI also checks for an existing receipt before an ordinary text write; this is not an exclusive atomic publication or demonstrated crash-safe receipt protocol. These are scope and source-derived limits, not observed historical failures.

Cumulative semantic reading reaches **371 distinct blobs / 2,744,909 bytes**, plus **52 byte-identical alias paths**: 423 covered paths. **5,170 paths / 4,058 distinct blobs** remain without full semantic-reading claims. Archive custody and empty streams remain mechanical; the historical global acquisition aggregate stays unchanged. No private source/receipt bytes, operational identifiers, signal payloads or model output are newly published. Hosted CI checks the public repository, not historical sampling or intake execution.

Next bounded unit: initial acquisition invocation, effective controls and accounting journal, **three texts / 366,815 bytes**. Read every retained row through a field-preserving view, bind the initial timeout's resource history and compare its scope with the already read terminal outcome without replaying acquisition or inferring a network bottleneck. Reconcile main and ownership first; no recipient has accepted it. Owned-storage and dispatch-reconciliation work remain separate.
