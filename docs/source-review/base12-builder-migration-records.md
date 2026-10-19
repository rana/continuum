# Complete migration map and revision custody

This Research Delta completes four full readings / 67,749 bytes at Base12 commit `88382e793b65c84fd8e223840c27f6bb8682864a`, tree `5cf96129bdcb0dde075f6f5800ae0c68a95c4b82`. The current Continuum chat owns this read-only contribution, based on main `ec33e182811c3b7693e6e6eab60daefecad9bdbc`. The selected files under `research/owned-stack/2026-10-16/native-builder-slice/` are `MIGRATION.json`, `SHA256SUMS` and the R1/R2 `BUILD.json` records. The [ledger](base12-coverage-builder-migration-records.json) binds source identities and the [validation record](../../research/runs/base12-builder-migration-records/validation.json) records exact checks and remaining dependencies.

## Full table reading and source-derived checks

The migration JSON was parsed and reconstructed with its original indentation and final newline; every reconstructed byte matches. Its header and all 47 named virtual addresses were read, followed by all 518 records and 109 patches in lossless field projections. This is complete table reading, rather than a sample of representative rows or a count inferred from its header.

An original length calculation over the already held symbolic source now derives the complete map. It handles fixed instruction widths, conditional versus unconditional branches, memory base/SIB requirements, minimal displacement widths and the admitted register-prefix rules. The source's physical line, record kind, offset, length and label agree with every migration row. Its 471 instructions total 2,834 code bytes, starting at file offset 4,096 and ending at 6,930. Labels can share an offset: the consecutive closed-pipe and wait labels demonstrate this without consuming code bytes.

All 47 virtual label addresses also match the source-derived file offsets plus the declared image base. Each of the 109 branch/call patches is derived from its actual source statement: the last four bytes of that instruction hold target minus next-instruction offset. Patch locations, symbolic targets and signed displacements agree with the entire table. This extends the earlier four selected relocation checks to a complete source/table relation. It remains a relation between source and historical metadata; no original ELF, listing or layout payload was newly acquired or compared.

A predicted map buffer built from these metadata fields is 16,608 bytes, SHA-256 `48a4f80ab464ccfee23f7bd69df03dc5e40cd5e9ad2dfdbedeac94cea2332c4d`. It uses the fixed header and four-u64 record format. This is an original prediction available for a later output comparison, not observed native-builder output. No ELF was generated.

## Checksums do not erase payload gaps

The top-level checksum file has 44 unique entries. Twenty-seven bind held exact-path payloads and one binds the already held seed through identical pinned Git blob identity. Sixteen remain declarations for unheld payloads. The validation record retains the classification for every entry. All names resolve in the pinned tree; tree membership alone cannot verify their declared SHA-256 values.

This matters especially for the candidate ELF, raw code, instruction/disassembly listings and layout records. Matching a checksum string in two documents establishes agreement of those documents; it does not establish possession or fresh verification of the artifact. The complete checksum reading therefore adds custody coverage while keeping the binary gap explicit. The checksum file does not hash itself, and does not purport to inventory the later preparation/execution directories.

## R1/R2 build records

The two build records differ in exactly two fields: bootstrap-source SHA-256 and ELF SHA-256. Their remaining fields agree, including emitted-only historical status, 13,740 declared ELF bytes, 155,648 owned writable bytes and seven runtime syscall numbers. Shared seed identity binds held bytes; the R2 bootstrap identity binds the held current bootstrap. The R1 bootstrap and both ELF identities agree with the checksum declarations, with their unheld payload limits retained.

Both records distinguish temporary Python/seed bootstrap dependencies from the emitted runtime's Linux loader/syscall ABI, hardware and initial-stack dependencies. They declare that the bootstrap did not read the symbolic consumer and that execution was not authorized at that checkpoint. These fields support the separation between a general bounded builder and one migrated consumer; they are not fresh observations of emission or runtime behavior.

The earlier correction report says six displacement bytes changed. Two changed digest fields in these build records neither prove nor contradict that byte-diff claim. Its verification requires the corresponding payloads or a separately bounded source comparison. Historical emitted-only status also does not imply that unread later execution records contain no run.

## Research return and next unit

Complete source/table derivation provides a stronger continuation anchor than selected saved comparison rows: a successor can compare a later result with the identified whole map. It still must preserve the distinction between deriving expected offsets, emitting bytes and observing execution. The present unit imported no upstream code, emitted no candidate and invoked no model or native program.

Coverage reaches **498 distinct blobs / 3,805,548 bytes**, plus **76 identical alias paths**. The remaining full-reading gap is **5,019 paths / 3,931 distinct blobs**. Historical global acquisition overlap remains unresolved.

Next: read the R1 bootstrap snapshot, both static-check records and the R2 readelf text, four texts / 30,443 bytes. Compare the earlier source with the held R2 source and inspect structural observations before later preparation/results. The other readelf path has identical pinned content and retains alias treatment. Reconcile fresh main and other workers first; no recipient has accepted this next unit. Separate storage, dispatch-reconciliation and public checkpoint lanes retain their ownership.
