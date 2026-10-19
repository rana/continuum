# Complete builder planned-command metadata

This Research Delta reads the complete 71,425-byte `research/owned-stack/2026-10-16/native-builder-slice/preparation-01/PLANNED_COMMANDS.json` at Base12 commit `88382e793b65c84fd8e223840c27f6bb8682864a`, tree `5cf96129bdcb0dde075f6f5800ae0c68a95c4b82`. The current Continuum chat owns this read-only contribution, based on main `e6d2d3f6ce844aa41e664a674b68be36a81c51f1`. The [ledger](base12-coverage-builder-planned-commands.json) binds identity; the [validation record](../../research/runs/base12-builder-planned-commands/validation.json) records a comparison for every proposed call.

## Exact planned rows bind the case semantics

The complete JSON reconstructs byte-for-byte with its original formatting and final newline. Every field in all 66 ordered-call objects was read, together with the precondition, aggregate counters, inherited settings and case60 override. Common private-root substitution shortened repeated path text without dropping any argument. No row was submitted for execution.

An original reconstruction from the complete case manifest equals every planned row, including argv order, environment, stdin, stdout/stderr paths, expected returncode and invocation counters. IDs are exactly 01–66 in order. There are 53 plain builder calls, ten traced injection calls, one child file-limit call and two conditional tiny calls. Builder counters sum to 64; generated-program counters sum to two. The accepted historical runner has no execution target.

The first 64 rows retain 24 expected exit-zero outcomes and 40 expected failure/signal outcomes. The final two add predicted exits 17 and 42. These numbers describe a plan, not an invocation log or executed PASS count. Its historical never-submitted status also cannot establish that no later result record exists.

## Fault prefixes and the file-limit exception

Each injection row names the tracing executable, quiet/string/trace-filter options, per-case trace path and exact syscall/error/occurrence specification, then directly names the static builder and its three paths. The filter covers the builder's admitted read/write/open/close/fstat/fsync/exit calls. The ten prefixes agree exactly with the case metadata; no shell command string is interposed in those argv vectors.

This supports the intended occurrence scope: fault numbering belongs to the fresh static builder tracee rather than an accidentally traced dynamic wrapper. It does not itself prove that the instrumentation started, injected the specified operation, used the intended descriptor/path, or observed the required retry/no-retry behavior. Those claims require the actual trace and result evidence.

Case60 alone prepends a file-size-limit wrapper with the 4,096-byte soft/hard limit. It has no tracing prefix. The declared override applies only to the builder child, retaining default/unblocked SIGXFSZ. Its expected negative returncode and output prefix remain the already documented untraced signal/file-state inference. Applying that limit to parent log writers would describe a different experiment.

The two tiny rows contain only their private copied-program destinations as argv. Their origins, exact output identities and prerequisite/clearance conditions live in the case manifest. A command vector is therefore a projection of that broader condition set; it cannot replace the source manifest as the complete execution authority.

## Environment and limits are scoped declarations

All rows specify an empty environment object and `/dev/null` stdin, with separate per-case or per-tiny stdout/stderr paths. These declarations reduce ambiguity but are not complete process, inherited-descriptor, filesystem, shared-library or kernel images. They also do not establish that later stream captures were created or preserved.

The inherited settings name CPU0, 256 MiB address space, per-process 25 CPU seconds, an 8 MiB file-size limit and zero core size. Affinity and address-space values agree with preparation. Per-process CPU is not the aggregate 30 CPU-second budget, and these fields do not contain the entire caller/outer/inner deadline or terminal accounting path. That behavior belongs to the separately identified controls and their later observations.

The precondition retains separate exact review and execution clearance, with stopping at the first mismatch or unresolved condition. The row list contains no retry authorization. If a later dispatch outcome is unknown, reconstructing a correct plan does not make replay safe; preserve and reconcile that attempt's evidence first.

## Research return and next unit

The contribution closes a concrete metadata relation: every proposed invocation agrees with its case, not merely its ID or expected status. It preserves three distinct records for continuation: authored case semantics, exact proposed process arguments and eventual observed operation. Agreement between the first two is useful preparation evidence without becoming a completed run.

The packet checksum entry also binds the newly held command metadata. No candidate control, model or native program was invoked, no binary was acquired, and no execution state or workstation activation was inferred from the plan.

Coverage reaches **521 distinct blobs / 4,215,296 bytes**, plus **77 identical alias paths**. The remaining full-reading gap is **4,995 paths / 3,908 distinct blobs**; historical global acquisition overlap remains unresolved.

Next: execution README, result summary, independent result review, evidence provenance and checksum list, five texts / 22,441 bytes. Read saved outcomes and their dependencies before deciding what was actually observed or accepted. Reconcile fresh main and other workers first; no recipient has accepted that next unit. Separate storage, dispatch-reconciliation and public checkpoint lanes retain their ownership.
