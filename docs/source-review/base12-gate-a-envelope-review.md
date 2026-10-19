# Gate-A envelope review: four corrections and a bounded static pass

Reviewed 2026-10-19 UTC at private Base12 commit `88382e793b65c84fd8e223840c27f6bb8682864a`, tree `5cf96129bdcb0dde075f6f5800ae0c68a95c4b82`. Five complete envelope/revision/static records total 37,141 bytes. Exact identities are in the [ledger](base12-coverage-gate-a-envelope-review.json); original comparisons are in the [validation record](../../research/runs/base12-gate-a-envelope-review/validation.json). No control test, launcher, driver, native artifact or new model invocation ran here.

## Research Delta: review conditions caused a narrow control revision

The original parent envelope review is conditional and grants no clearance. It raises four concrete conditions, while accepting that the fixed candidate and finite sequence can be reviewed within a single-CPU/watchdog budget:

1. Bind the freeze and canonical scripts actually invoked. Checking an unpinned absolute-path manifest alone did not close the copied-launcher case.
2. Preserve all evidence. An exclusive attempt marker did not prevent unrelated sidecar resource/exit files from being truncated when that marker was absent.
3. Correct whole-group termination claims. A TERM-terminated direct shell could end the timeout monitor before its later escalation, leaving a descendant outside the promised second signal.
4. Assert the entire output state. Counting regular files, comparing only expected contents, newline-stripping sentinel comparisons and existence-only rejection checks left other entries or dangling symlinks outside the asserted predicates.

Those are reported enforcement/prose gaps, not demonstrations that the pinned decoder produced bad outputs or escaped its actual batch. The reviewer requested a narrow script revision, not a new decoder, fixtures, acquisition campaign or containment infrastructure.

The revision and later reviews identify the same three changed control/freeze hashes recovered in the previous return. Current launcher, driver and freeze payloads match the static record and both revised reviews; the static record's delegated-review digest matches the acquired report. The original delegated-review digest is also preserved. The sixteen-file unchanged inventory is a historical cross-revision declaration: twelve text payloads are held here, while ELF, materialized code and two instruction-text artifacts remain unacquired. We did not newly compare all sixteen against the old packet.

## Research Delta: resolution is tied to source, assumptions and live preflight

The revised parent review marks all four conditions PASS at the separately identified revision. It describes the external freeze digest and canonical paths; atomic attempt-directory reservation with new evidence paths; direct group KILL at 280 seconds plus validated current-group failure cleanup; and complete entry-set/sentinel/staging checks. These agree with the held control source previously read. Actual process-group failure behavior was not dynamically exercised by either revised static reviewer.

The revised parent report explicitly says its ten freeze-entry checks concern packet equivalents, including an identical manifest alias for the outside-Git path. That is not verification of the workstation's current absolute paths. Its eight conditions for parent clearance include matching exact identities and canonical invocation, passing live preflight and unused-attempt checks, preserving every outcome, allowing only the frozen sequence, retaining limits, reviewing completed evidence, reporting resources honestly, and reopening review after a relevant change. The report's static PASS is expressly not independent execution authorization. The earlier consumed-clearance and later run records retain their separate stages; no historical permission is renewed here.

The sequence remains **65 matrix + 12 fault + 1 collision + at most 1 retained decode = 79** invocations, with retained decoding last. The held manifest's declared archive lengths sum to **6,764,879 bytes**, matching the original review. This is inventory arithmetic, not fresh archive custody or execution. The original parent review already reconstructed the TSV and then checked actual packet bytes; our later reconstruction independently repeats that content-identity method rather than originating it.

## Research Delta: failure cause, completion and accounting are different observations

The delegated revised review explains that exit 137 alone cannot distinguish watchdog expiry from the driver's own failure-triggered group KILL. A preserved driver status can retain the earlier cause when writing succeeds. Whole-group termination can also prevent descendant usage from reaching waited-child accounting. A missing cause receipt or incomplete CPU total must remain missing/incomplete rather than being inferred from the signal exit.

Both revised reviews retain the same limitations: the 20-second nominal margin below 300 depends on confinement and ordinary scheduling/signal delivery; per-process CPU/address-space limits are not aggregate counters; external SIGKILL or fatal shell failure cannot run traps; a post-return scan is a conservative snapshot and intentionally avoids a stale numeric-group recovery kill. Uninterruptible I/O and hostile concurrent intervention remain outside the bounded proof. The later normal passing run does not dynamically cover those failure paths.

The reviews also already keep positive short IO static-only, finite fixtures nonexhaustive, preflight/post-scan overhead outside decoder timing, maximum RSS separate from aggregate memory, and publication separate from crash durability. These qualifications belong to the original evidence and remain attributed. The useful result is a traceable correction-and-review sequence, not a universal containment or recovery guarantee.

For Continuum, retain the conditions that changed a decision and the exact revision that resolved them. A directory called accepted, a static PASS, a live preflight, an execution grant and an observed result are distinct events with different evidence.

Cumulative semantic reading reaches **445 distinct blobs / 3,425,563 bytes**, plus **52 byte-identical alias paths**, covering 497 paths. **5,096 paths / 3,984 distinct blobs** remain without full semantic-reading claims. Historical acquisition totals stay unchanged. No private raw review, Library/task identifier, absolute operational path, executable, signal, listing, decoded output or trace buffer is published; no new inference occurred. Hosted CI checks this public contribution, not the historical envelope or native artifact.

Next bounded unit: opening/owner declarations, two parent provenance records, accepted result assessment and checks, **six texts / 16,863 bytes**. Bind the retained reviewer outputs and distinguish result acceptance from the earlier conditional/static stages. Reconcile main and lane ownership first; no recipient has accepted this next unit. Owned-storage, dispatch-reconciliation and public self-use checkpoint lanes remain separate.
