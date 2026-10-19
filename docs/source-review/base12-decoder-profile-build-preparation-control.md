# Decoder-profile capture and literal caller

This Research Delta completes five full readings / 48,794 bytes under `research/owned-stack/2026-10-16/native-builder-decoder-output-profile/build-preparation-01/`: the capture source, literal caller, invocation note, control review and author checks. Source is Base12 commit `88382e793b65c84fd8e223840c27f6bb8682864a`, tree `5cf96129bdcb0dde075f6f5800ae0c68a95c4b82`. This chat owns the source-only unit from Continuum publication head `61d049bfc14177c53ab74260e0547a9461fda093` (PR #111 pending integration). The [ledger](base12-coverage-decoder-profile-build-preparation-control.json) and [validation](../../research/runs/base12-decoder-profile-build-preparation-control/validation.json) retain exact identities, reading representation, source checks and limits.

The complete 17,739-byte capture was read. The 17,826-byte caller has an exact lossless relation: 84 prefix bytes, that complete capture verbatim, then three delimiter/newline bytes. No other caller body exists. Both hashes agree with preparation and author metadata. The wrapper describes a cleared environment and isolated stdin-script Python invocation; its raw command and private operational locators remain unpublished. None was submitted.

The capture is **not safe to import for inspection**: it starts its clock at module scope and calls main unconditionally inside a top-level exception boundary. We parsed syntax as data and called no upstream function. A source document's “preparation only” description does not make its import passive.

## Source-level control relationships

Exactly one fork and one execve site occur in the capture source. The sole exec target is its fixed monitor argument vector; that site is inside the child branch, after the start-barrier read. The parent's group assignment and ownership flag precede its grant byte. These are source relationships, not observations of a running three-process chain or a guarantee about a modified interpreter/monitor.

Both numeric kill sites reside under the unreaped-identity guard. Signal blocking encloses wait4 and the reaped-state update; terminal observation uses WNOWAIT. These match the proposal's attempt to prevent cleanup against a reused numeric group identity. No cleanup, signal-delivery, child-escape or failure test was executed, and the historical prior capture was not completely diffed in this unit.

Aggregate CPU source adds SELF to exactly one wait4 usage. RUSAGE_CHILDREN is excluded from that summand and used for reconciliation, avoiding a second addition of the same declared child usage. Samples require finite nonnegative components rounded upward. The four per-process limits and pre-reservation affinity placement match the earlier proposal. This inspects the accounting formula and placement; installed-runtime behavior, normal monitor waiting, complete process ancestry and actual resource feasibility remain assumptions or future observations.

Regular reads use no-follow/nonblocking/close-on-exec flags with kind/size checks. Receipt creation is exclusive, no-follow and mode 0600, with positive-progress writes, file fsync and one non-retried close in source. That does not supply directory fsync, an atomic record set, protection against concurrent same-UID mutation or a power-loss guarantee. The bootstrap's own ordinary writes remain distinct from these later capture checks.

The success tail is exactly: publish provisional OUTCOME, run the inclusive totals check, then exit zero. The final sample is not persisted. A late failure can therefore coexist with a success-shaped file. This confirms the earlier source-order explanation of why the real outside completion status is necessary; it does not provide that status or prove every accepted condition from a marker.

## Proposed artifact comparison

The postcheck is designed to inspect six future outputs, source copy, header/padding/protections, layout/labels/patches, listing coverage, build JSON and stdout/stderr. Its fixed three code-comparison sites agree with the already-read historical R2 listing text:

| Instruction offset | Immediate offset / width | Old value | Proposed value |
| --- | --- | ---: | ---: |
| 0x67b | 0x67d / 8 bytes | 0x410000 | 0x500000 |
| 0x68c | 0x68e / 8 bytes | 0x410000 | 0x500000 |
| 0x6ae | 0x6b0 / 8 bytes | 4096 | 10555392 |

Only textual fields and integer relations were checked; no native code blob was acquired or reconstructed. These sites bind the proposed fixed-width comparisons to the historical listing and previously checked source change. They are not observations of new emitted bytes or runtime-positive consumers. The postcheck's future use of frozen native ELF/code files does not acquire those payloads for this review.

The two embedded manifest pins agree with author/preparation declarations, and predicted old counts agree across records. The reported 1,325 identity rows, 1,196 stdlib files, 92 ELF objects and 30 frozen files still depend on unread manifest payloads. A conservative installed-file superset is not a dynamic load trace; interpreter/loader startup already precedes its later hash checks. The control explicitly trusts the normal installed runtime and filesystem conditions rather than providing hostile-code containment.

The review also reports an earlier preparation-file mode mismatch, its correction and a separate review-binding correction. Those underlying records are the next unit; the report alone does not verify their observed chronology or historical filesystem modes. No source change, newer runtime clearance or accepted build result is inferred from their filenames.

No upstream import/execution, native artifact acquisition/emission/execution, new inference, workstation activation or recipient acceptance occurred. The two uncertain model requests remain unrepeated. Semantic reading reaches **641 distinct blobs / 5,558,019 bytes**, plus **115 identical alias paths**. **4,837 paths / 3,788 distinct blobs** retain full-reading gaps; historical global acquisition overlap is unresolved.

Source-reading follow-up: frozen inputs, environment, inspection tools and both saved correction records (five files / 20,874 bytes) remain open. Their actual pins/corrections must be read before those claims close. The next program unit instead reconciles the renewed owned-authority construction direction in [PR #112](https://github.com/rana/continuum/pull/112), actual implementation branches and owners, then selects a bounded finite-oracle/disposable-journal construction task. The two observed older owned-storage refs have no commits ahead of main; that does not prove worker inactivity. This chat can work in a disjoint owned-authority lane after fresh ownership reconciliation without changing the reference store or seizing the design publication. No implementation or recipient acceptance is claimed by this review.
