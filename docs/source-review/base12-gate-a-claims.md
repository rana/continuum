# Gate-A claims: native application, bounded execution and contract scope

Reviewed 2026-10-19 UTC at private Base12 commit `88382e793b65c84fd8e223840c27f6bb8682864a`, tree `5cf96129bdcb0dde075f6f5800ae0c68a95c4b82`. Five texts / 28,641 bytes were fully read: overview, contract, execution overview, delegated saved-result review and consumed clearance. Exact identities are in the [ledger](base12-coverage-gate-a-claims.json); document comparisons and arithmetic are in the [validation record](../../research/runs/base12-gate-a-claims/validation.json). This is a review of authored contracts and execution claims. No ELF, waveform or trace buffer was acquired and no decoder was built or run.

## Research Delta: retain the boundary of native ownership

The overview describes a scalar Linux x86-64 stage-A decoder application using the loader, syscalls and hardware. It separates that application from its Python/seed ahead-of-time emission and existing shell/tool correctness controller. It asserts absence of dynamic/interpreter linkage in the ELF, but those artifact properties are not newly inspected here. Application runtime, build path and measurement controller remain different ownership milestones, as in the earlier [native-boundary return](base12-native-reset.md).

ELF, emitter, freeze, driver and launcher digests agree where repeated across the documents. The declared ELF length, 22,066 bytes, matches pinned tree metadata. These are consistent declarations, not new payload hash bindings. The execution revision agrees across execution overview, delegated review and clearance. Retained-output hash declarations agree between overview and review. Raw results, freeze contents, accepted parent reviews and executable bytes remain separate evidence to inspect.

## Research Delta: a declared invocation total has an evidence taxonomy

The saved-result review supports a declared 79-invocation batch as **65 matrix cases + 12 faults + collision + retained decode**. Matrix counts are 36 valid and 29 malformed; faults divide into six EINTR and six hard-I/O cases. There are **77 explicit matrix/fault verdict rows**. The two remaining completions depend on checked driver control flow and subsequent completion markers rather than separate printed verdict rows. This is not a kernel-wide execution census.

The delegated review reports actual injected-call markers, successful retries and exit outcomes from retained traces. Those are attributed observations by that reviewer; no trace was newly inspected or fault injected here. The documents explicitly preserve positive short read/write handling as source-only coverage. A successful passing batch also did not induce group timeout/kill or forced-exit accounting. Neither a fault label nor normal completion fills those coverage gaps.

Reported batch CPU arithmetic is 0.31 + 0.69 = 1.00 seconds, including driver utilities and tracing. Outer elapsed 2.866612 minus pre-launch 0.056587 equals launcher-call 2.810025 seconds. Subtracting rounded monitored wall 1.55 gives approximately 1.260 seconds of combined preflight/post-scan overhead, not separately instrumented components. These checks reproduce authored arithmetic, not decoder throughput or a comparative performance result.

## Research Delta: wire grammar and runtime admission limits can disagree

The contract deliberately treats arbitrarily many leading zeros within bounded metadata as valid decimal wire syntax. It records a 4,301-zero fixture rejected by the separate Python oracle's configured conversion safeguard, without adopting that runtime safeguard as the wire grammar. This is an explicit contract/oracle distinction, not a mismatch newly reproduced here. Agreement with an implementation-specific oracle is not the only definition of validity when the actual format states a different rule.

The contract also names its register discipline as an internal ABI rather than System V, and separates atomic output namespace publication from power-loss durability. It declares complete hashes/output before staging, exclusive private files, file/staging sync and no-overwrite rename, with parent-directory sync absent. Cleanup or forced termination may leave staging. These are stated contracts and limits, not source fidelity or crash behavior verified in this unit. Basic declared capacities reconcile: 650,000 frames × three bytes = 1,950,000; 4,096 signed64 slots = 32,768 bytes; a 4 MiB+1 input buffer distinguishes an over-limit read without relying solely on a size snapshot.

For Continuum, preserve the distinction between format validity, runtime admission policy, publication visibility and durability. A receipt should say which contract and failure surface was actually checked rather than promoting one broad pass label.

The clearance states the one historical batch is consumed. The overview reports separate parent acceptance; current reading neither retrieves that accepted review nor establishes fresh recipient acceptance or execution authority. No historical command, retry, security setting, service, timer or new model invocation occurred. No private raw payload or operational identifier is published. Hosted CI checks the public repository, not these native claims.

Cumulative semantic reading reaches **401 distinct blobs / 3,209,226 bytes**, plus **52 byte-identical alias paths**: 453 covered paths. **5,140 paths / 4,028 distinct blobs** remain without full semantic-reading claims. The completed hybrid packet remains a dated [scoped closeout](base12-packet-semantic-closeout.md); whole-repository reading remains incomplete. Historical global acquisition totals remain unchanged.

Next bounded unit: saved result, preservation manifest, saved-execution auditor, freeze and retained identities, **five texts / 36,830 bytes**. Bind raw record fields and available text payloads to these claims and inspect the auditor's predicates without running it. Acquire no executable, signal or raw trace buffer. Reconcile main and ownership first; no recipient has accepted it. Continuum's owned-storage and dispatch-reconciliation lanes remain separate.
