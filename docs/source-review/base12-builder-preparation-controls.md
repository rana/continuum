# Builder preparation and control-review chronology

This Research Delta completes five full readings / 20,587 bytes at Base12 commit `88382e793b65c84fd8e223840c27f6bb8682864a`, tree `5cf96129bdcb0dde075f6f5800ae0c68a95c4b82`. The current Continuum chat owns this read-only contribution, based on main `23276eeba9d819e62db2bb904c2ab8ea6da27c31`. The selected preparation README, preparation/provenance JSON, review request and control review are under `research/owned-stack/2026-10-16/native-builder-slice/preparation-01/`. The [ledger](base12-coverage-builder-preparation-controls.json) retains exact identities; the [validation record](../../research/runs/base12-builder-preparation-controls/validation.json) separates fresh bindings, prior ledger identities and reported behavior.

## From proposal to a concrete packet

The source-only checkpoint's later preparation record describes materialized synthetic inputs, expected files, planned commands and controls. Its declared scope remains 64 builder invocations followed conditionally by two new tiny-program calls. The migrated historical runner is built and compared, never selected for execution. Case descriptions distinguish a stable oversized input rejected by fstat from concurrent-growth/read-probe behavior. The maximum instruction case also reaches the label and map ceilings; these are not independent observations of three unrelated overflow guards.

Preparation reports ten actual-error injection specifications: six EINTR retries and four EIO non-retry cases. The file-limit case is different: a real child-only 4,096-byte limit, default/unblocked SIGXFSZ, expected signal termination, exact ELF prefix and empty map. It does not fabricate a positive short-write syscall result or claim a traced return that it did not collect. These remain descriptions of the prepared batch, not fresh invocations here.

The expected successful tree's 495 regular files, one symlink and byte totals are explicitly static derivation. The acceptance caps—1,024 regular files, 128 MiB total, 8 MiB per file and 1 MiB per injection trace—are checks before acceptance, not a filesystem quota that prevents all intermediate growth. Attempt-directory absence is a capture-time observation. No attempt marker or directory was created by this review.

## A concrete no-retry review correction

The control review preserves a defect in the first driver draft: it checked the injected EIO and final status/output state but did not reject a retry of the failed operation. Those checks could pass after an extra close of the failed descriptor. The reviewed revision reportedly rejects later same-syscall operations with the same target prefix, and the caller requires the resulting no-retry proof.

For the output-close case, cleanup of a different descriptor remains allowed; another close of the failed descriptor rejects. For input-close EIO, a subsequent close of that descriptor rejects. This is a useful refinement of failure evidence: unchanged bytes and an expected exit do not by themselves establish absence of an invalid retry. The caller reportedly reconciles the identified driver's proof and trace identity rather than independently parsing the syscall grammar. Agreement therefore retains that implementation dependency.

This unit reads the review and cross-checks its pins. It does not freshly inspect those control bodies or replay a fault. The earlier full-reading ledger records caller/driver source identities, but their local cache payloads were not recovered here; that prior reading is not counted again or mislabeled as fresh byte verification.

## Review chronology keeps the stale draft explicit

All eleven review-request table pins agree with preparation fields. The four control hashes in the control review agree as well. Three unchanged source pins—bootstrap, seed and original lane checksum manifest—bind held bytes. Three other source identities agree with the earlier full-reading ledger: caller, driver and envelope. The R2 ELF digest agrees with its build declaration, retaining the unheld binary gap.

The control review was written before the final freeze. It explicitly records a 212-entry draft payload and obsolete launch/guard pins inside the draft invocation. The later request names a 217-entry payload, a different command-document digest and a separate final static-verification record. These are successive states, not an invitation to execute the stale draft or to rewrite the earlier report. The final verification and literal command have not yet been read in this unit.

Preparation also reports a parent's independent source/actual-byte PASS while saying the full external report was not recovered there. That is reported historical input. Continuum's current unheld ELF gap does not imply that the earlier reviewer lacked the bytes; nor does the summary replace that full review record.

## Acceptance is later than receipt writing

The reviewed design permits acceptance only on a normal, fully waited process chain. CPU0, per-process 256 MiB, aggregate 30 CPU seconds/60 wall seconds and nested 25/27/29-second deadlines retain scheduling and kernel assumptions. Group scans are snapshots under no-detach/non-hostile conditions. The review does not claim hard-real-time containment.

It also separates provisional receipts from independent terminal exit of the same trusted caller. The persisted resource sample is prepublication; a later fresh check is intended to include receipt write/fsync/close costs. Full-looking files alone cannot attest that final path. These are control-design claims pending exact-source and later result review, not new containment or durability measurements.

Coverage reaches **507 distinct blobs / 3,856,578 bytes**, plus **77 identical alias paths**; **5,009 paths / 3,922 distinct blobs** remain without full semantic-reading claims. No model, candidate control or native program was invoked.

Next: launch/guard source, literal invocation, final static verification and environment record, five texts / 20,660 bytes. Bind the actual final control/freeze state before interpreting saved outcomes. Reconcile fresh main and other workers first; no recipient has accepted the next unit. Separate storage, dispatch-reconciliation and public checkpoint lanes retain their ownership.
