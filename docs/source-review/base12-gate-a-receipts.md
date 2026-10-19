# Gate-A receipt custody: bind the log without upgrading its claims

Reviewed 2026-10-19 UTC at private Base12 commit `88382e793b65c84fd8e223840c27f6bb8682864a`, tree `5cf96129bdcb0dde075f6f5800ae0c68a95c4b82`. Twenty receipt paths / 10,669 bytes were acquired and checked: nineteen nonempty texts fully read and one empty stderr checked mechanically. All 22 entries in the previously read preservation manifest now match exact payload lengths and SHA-256. Exact identities are in the [ledger](base12-coverage-gate-a-receipts.json); comparisons are in the [validation record](../../research/runs/base12-gate-a-receipts/validation.json). No batch, auditor, tool or native artifact was executed.

## Research Delta: a complete receipt set retains its evidence dependencies

The saved stdout contains exactly 77 unique expected/actual verdict rows. Every expected value equals its actual value, and the case-to-exit mapping exactly matches all 65 matrix and twelve fault rows in RESULT. Ten frozen-input check lines precede the cases; the synthetic/fault-gate marker precedes retained-file hash declarations, retained completion and final COMPLETE. Retained hash strings match RESULT. No separate collision or retained-decode verdict row appears, so their exit outcomes still depend on the frozen driver rather than being inferred as two additional printed rows.

The consumed-attempt marker, freeze-file digest, normal-completion outcome, zero command/driver/group-scan exits and no launcher interruption match the earlier summary. Empty stderr is actual byte custody, not another semantic reading. The six-field group record and saved scan-error text also match RESULT. The scan retains a no-members snapshot and a vanished-process diagnostic; the launcher/scanner's exact predicates remain selected next. These files do not establish a current process census, authenticated worker identity or immunity to interference. Private boot/namespace/group values remain unpublished.

This closes preservation custody, not the entire native proof chain. Frozen-input OK messages are historical tool output; they do not newly hash the ELF or source inputs here. Full traces, decoded outputs and fixture payloads remain unacquired. A complete collection of copied receipts can still depend on driver control flow, output checks and reviewer observations outside that collection.

## Research Delta: compare summaries against their underlying measurements

GNU time's retained fields match RESULT: 0.31 user + 0.69 system = **1.00 CPU seconds**, **1.55 rounded monitored wall seconds**, maximum RSS **8,392 KiB**, exit zero. These concern the complete monitored batch with utilities and tracing, not per-decoder throughput or aggregate memory. Other counters, including zero recorded socket messages, do not constitute an independent network audit.

Exact decimal differences from separately retained epoch records reproduce all five summary intervals: **0.109131** seconds for separate preflight, **2.866612** approved block, **0.056587** before launcher call, **2.810025** launcher total and approximately **1.260025** combined launcher preflight/post-scan after subtracting rounded monitored time. Absolute workstation timestamps are not published. These are consistent recorded boundaries; their subtraction does not isolate uninstrumented preflight and post-scan components or remove clock/rounding qualifications.

## Research Delta: tool-path declarations are not independent binary custody

The launcher tool list has six rows; all six digests agree with corresponding preflight declarations. Preflight has thirteen tool paths but nine distinct digest values: five utility paths share one digest. Repeated equal digests do not provide five independent implementation checks, nor prove whether the paths were aliases, links or distinct equal copies. No tool binary was acquired or rehashed here. Keep path observations, content identity, independence and trusted-tool assumptions separate.

For Continuum, a useful receipt view should retain what was checked and where a summary's fields came from. Complete byte custody improves recoverability; it does not erase historical, control-flow, toolchain or snapshot limitations.

Cumulative semantic reading reaches **425 distinct blobs / 3,256,725 bytes**, plus **52 byte-identical alias paths**: 477 covered paths. **5,116 paths / 4,004 distinct blobs** remain without full semantic-reading claims. The hybrid packet closeout remains scoped; historical global acquisition totals remain unchanged. No private raw receipt, operational identifier, trace/output buffer, signal or executable bytes are published, and no new model invocation occurred. Hosted CI checks the public repository, not historical execution.

Next bounded unit: launcher, driver and fixture manifest, **three texts / 40,143 bytes**. Bind the two source digests and fixture metadata to the freeze, inspect one-shot admission/group cleanup and case/control-flow predicates without execution. Acquire no executable, decoded output or raw trace. Reconcile main and ownership first; no recipient has accepted it. Continuum's owned-storage and dispatch-reconciliation lanes remain separate.
