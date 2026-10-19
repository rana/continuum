# Complete builder case-expectation manifest

This Research Delta reads the complete 140,815-byte `research/owned-stack/2026-10-16/native-builder-slice/preparation-01/fixtures/cases.json` at Base12 commit `88382e793b65c84fd8e223840c27f6bb8682864a`, tree `5cf96129bdcb0dde075f6f5800ae0c68a95c4b82`. The current Continuum chat owns this read-only contribution, based on main `9ea3b2069a15f221981c915c791ab909c641031e`. The [ledger](base12-coverage-builder-case-expectations.json) binds the source identity; the [validation record](../../research/runs/base12-builder-case-expectations/validation.json) retains original complete-schema checks.

## Full reading and exact structure

The complete JSON reconstructs byte-for-byte with its original formatting and final newline. Header, ten provenance inputs, bounds and both tiny-run objects were read, followed by every field in all 64 builder cases. Checked common path/zero-output/publication templates and the previously read complete digest dictionary shortened repeated fields without dropping their values. This is a complete manifest reading, not a sample inferred from the generator or case count.

Builder IDs are exactly 01–64 and conditional tiny IDs are 65/66. The header's provenance inputs agree with the fixture provenance record; candidate and contract pins agree with their existing records. All future runtime paths follow the declared per-case input/output template, including the symlink target. These are path declarations; no historical runtime directory was created or inspected.

The 64 expected builder outcomes are 24 exit-zero, 30 source-error, two reservation-error, four input-error, three publication-error and one signal-termination case. Input setup is 61 regular, one missing, one directory and one symlink. These are authored expectations, not new test results. Every stdout/stderr expectation is empty, and publication validity is tied to exit zero rather than the appearance of output bytes.

## References and accounting close exactly

All 155 unique fixture references resolve to the fixture checksum list with matching digest declarations and pinned-tree byte sizes. Together they account for 573,119 bytes. They exclude the case manifest, provenance and checksum metadata; adding 140,815, 2,204 and 13,072 bytes respectively gives the independently reconciled 729,210-byte fixture tree. The smaller payload-file subtotal therefore does not contradict the larger directory total.

Seventeen source references have available identical held bytes. Their source hashes, LF counts and physical-line counts agree, including reused tiny sources. Remaining reference checks bind declarations and tree sizes; they do not establish fresh possession or semantic review of every source/output/layout payload.

All exit-zero map sizes satisfy the fixed header plus 32 bytes per declared map record, with record counts equal to instruction plus label counts. ELF sizes fit the admitted output range. These arithmetic checks do not encode instructions or verify native output. The combined witness case's 209 instructions, 15 labels and 14 relocations remain an encoding fixture; the looping relocation case remains ineligible for execution.

## A source layout is not failure progress

Eight nonzero cases retain a full intended source layout: the two collisions, symlink input and five publication/input-fault cases. This metadata describes what the valid source would build. It does not claim that parsing or publication reached that layout.

The distinction is concrete in case53: the symlink is expected to reject before parsing, although the referenced source has a five-record layout. Case60 also names that full layout while expecting only a 4,096-byte ELF prefix and empty map. Case50 preserves a map sentinel and an empty ELF reservation. Cases58/59 expect complete-looking ELF/map bytes but invalid publication. A later receiver must evaluate the case's actual output-state fields and terminal outcome rather than treating layout presence as completion evidence.

## Fault and tiny-run conditions remain exact

All ten injection specifications agree with the materializer's literal syscall, ordinal, semantic target, retry class and expected status. Their ordinary full-I/O counts also reconcile, retaining the explicit short-I/O qualification. Six EINTR cases require the next same syscall to retry the same operation successfully; four EIO cases require no retry of the failed target. Case60 has no injection and retains its file-size/signal requirements, rather than masquerading as another traced fault.

Both tiny-run references match only their respective case03/04 expected ELF identities, with predicted exits 17/42 and empty streams. Their conditions require all 64 builder cases to pass under separate clearance, then a copied, hash-reverified output before enabling execution. No historical runner, witness-only, numeric-boundary or looping output becomes eligible through those references.

The present checks validate the manifest's relations and intended evidence requirements. No fixture payload was newly acquired, no assembler or materializer ran, and no candidate, control, model or native program was invoked.

Coverage reaches **520 distinct blobs / 4,143,871 bytes**, plus **77 identical alias paths**. The remaining full-reading gap is **4,996 paths / 3,909 distinct blobs**; historical global acquisition overlap remains unresolved.

Next: the complete 71,425-byte `PLANNED_COMMANDS.json`. Bind the actual proposed invocation arguments to these case semantics before reading saved execution results. Reconcile fresh main and other workers first; no recipient has accepted the next unit. Separate storage, dispatch-reconciliation and public checkpoint lanes retain their ownership.
