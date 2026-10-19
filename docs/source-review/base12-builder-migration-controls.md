# Builder migration source and control boundary

This Research Delta reads six complete source/control/proposal texts, totaling 22,795 bytes, at Base12 commit `88382e793b65c84fd8e223840c27f6bb8682864a`, tree `5cf96129bdcb0dde075f6f5800ae0c68a95c4b82`. The current Continuum chat owns this read-only contribution, based on main `47f797d3811df0a687d5b12d27d1fb1735cb97a6`. The [ledger](base12-coverage-builder-migration-controls.json) records exact source identities; the [validation record](../../research/runs/base12-builder-migration-controls/validation.json) retains original counts, source bindings and unexecuted boundaries.

Selected files under `research/owned-stack/2026-10-16/native-builder-slice/` are `migrate_runner.py`, `runner.b12s`, `CHECKPOINT.json`, `OWNER.json`, `OPEN.md` and `TEST_PROPOSAL.md`. Every acquired byte count, Git blob and SHA-256 binds the pinned tree. No upstream module was imported, migration performed, output emitted or native program executed.

## What the migration actually does

The one-time migration reads an old textual instruction listing and layout. It associates layout labels with listing offsets, converts textual operand syntax into symbolic builder forms, and records physical source lines and historical byte spans. Numeric moves become `imm`; numeric add/and forms become their immediate variants. Loads/stores receive explicit register/displacement operands. Its output is editable symbolic source plus a historical expected-map/provenance record. The routine native builder does not depend on importing this migration.

AST inspection confirms two exclusive output creations, in order: symbolic source with `xb`, then migration JSON with `x`. These are sequential writes, without rollback, fsync or atomic pair publication. Failure creating the second file can leave the first. The script's “never executes” description concerns native execution: invoking the Python script would still read inputs and write outputs. We parsed its syntax only.

Its asserted historical ELF SHA-256 is read from the layout's declared field. It does not recompute that identity from ELF bytes. Listing/layout digests are recorded from consumed text/bytes, while the source and expected map inherit those inputs' authority. Historical evidence can be a useful migration oracle without becoming independent ISA proof. The larger migration table and original historical payload comparison remain later work; no byte-for-byte migration reproduction is claimed here.

## Counts from the actual symbolic source

An original declarative admission check accepts the 7,463-byte runner source. Direct enumeration finds 520 physical lines: two comments, 471 instructions and 47 unique labels. Its 109 symbolic branch/call references all resolve. The source uses all 33 admitted instruction forms, including 20 `syscall` statements. These are static statements, not runtime syscall counts or invocation observations.

The resulting 518 source-map records agree with the checkpoint declaration, and the fixed map format would occupy 16,608 bytes. That is arithmetic, not a newly emitted map. Instruction, label, relocation and source-size counts fit the owner record's caps; the declared 6,930-byte consumer and 13,740-byte builder also fit their respective ceilings. Neither artifact was newly acquired to verify those size claims.

Six checkpoint payload hashes bind held source: bootstrap, seed, contract, symbolic consumer, independent source review and witness checksum manifest. The seed comparison initially reached an absent local alias path; the corrected check used the already held stage-A seed, with identical pinned Git blob identity. No new seed reading or execution credit is added. Owner/checkpoint input identities and seed pin agree; actual owned memory and candidate-size declarations sit below the owner's broader limits.

## A proposal remains a proposal at its checkpoint

The 15 proposal table ranges cover builder call IDs 01–64 exactly once. They span valid builds, syntax and capacity boundaries, publication collisions, input failures, actual syscall faults and a real partial-write scenario. Two tiny output executions are conditional on passing the builder batch and obtaining separate clearance. The accepted historical runner is proposed for build/comparison only, never execution in that batch.

The proposal requires independently specified output identities, exact fault occurrences, normalized signals/descriptors, aggregate resource enforcement, caller-exit capture and a fresh attempt. Its one-CPU, 256 MiB per-process, 30 CPU-second and 60 wall-second figures are targets, not enforcement demonstrated by this text. The 1,024-instruction ceiling dominates the output-size bound; inventing a separate unreachable overflow case would test the wrong condition.

`OPEN.md` and the checkpoint explicitly retain parent review, fixture/launcher preparation and separate exact-head execution clearance. Their zero-invocation/source-only status belongs to that captured checkpoint. The pinned tree also inventories later preparation and execution records that this unit has not read. The older source-only declaration must not be promoted into a claim that no later run exists. Historical ownership searches likewise do not establish current worker inactivity or grant Continuum execution authority.

## Research return and next unit

The transferable lesson is to preserve the evidence dependency at each stage: source migration, historical expectations, static agreement, materialized batch, clearance and observed results. A later continuation can bind those stages without treating a proposal or self-declared ELF digest as an actual result.

Coverage reaches **494 distinct blobs / 3,737,799 bytes**, plus **76 identical alias paths**. The new runner alias is content equivalence, not another reading. The remaining gap is **5,023 paths / 3,935 distinct blobs**. Full-repository reading remains incomplete.

Next: read `MIGRATION.json`, top-level `SHA256SUMS` and both revision `BUILD.json` files, four texts / 67,749 bytes. Check the complete map and declared source/revision custody before reviewing later preparation or execution claims. Reconcile fresh main and worker ownership first; no recipient has accepted that next unit. Separate storage, dispatch-reconciliation and public checkpoint lanes retain their ownership.
