# Complete saved builder attempt inventory

This Research Delta completes reading of the 99,153-byte `research/owned-stack/2026-10-16/native-builder-slice/execution-01/INDEPENDENT_ATTEMPT_MANIFEST.json` at Base12 commit `88382e793b65c84fd8e223840c27f6bb8682864a`, tree `5cf96129bdcb0dde075f6f5800ae0c68a95c4b82`. This chat owns the read-only contribution, based on Continuum main `2006f3bbf9c1b2a650dc6d2fd29a6fc8da4a5074`. The [additive ledger](base12-coverage-builder-attempt-inventory.json) binds the source; the [validation record](../../research/runs/base12-builder-attempt-inventory/validation.json) preserves the original metadata checks.

## Complete inventory reading and exact join

All header fields, 495 regular-file objects, 135 directory paths, the sole symlink and every distinct digest value were read. A lossless projection preserves each file's path, size, mode and digest; every file state is `file`. Reconstructing the JSON with its original formatting and final newline reproduces the complete source bytes. Git blob, length and SHA-256 checks bind those bytes to the pinned tree and prior review declaration.

The inventory declares 531,729 regular-file bytes. An exact set comparison accounts for every regular path, with no extras or missing paths: 21 root receipts, one candidate, 132 streams, 66 invocation records, 66 observation records, 66 verdicts, 62 source files, 59 output files, two tiny executable copies, ten traces and ten injection-proof records. This checks the complete saved metadata topology against the earlier case and review records. It does not compare against a freshly observed private filesystem.

All 66 invocation and observation digest declarations match their corresponding saved case records. Every output's absent/file state, size, mode and digest agrees with that review; every present source size and digest agrees with the frozen case manifest. All ten trace sizes/hashes and proof hashes bind the injection summaries. Every root receipt's length and digest binds its detailed saved-review entry. These relationships strengthen continuity across identified records without promoting their underlying payloads into current custody.

All 66 verdicts declare the same 38-byte content identity. The inventory contains 213 distinct regular-file digest declarations across its 495 paths. Repeated verdict, stream, source and output content is expected in this metadata structure; digest multiplicity does not count independent invocations. The preceding review's 66 distinct invocation digests remain the separate association evidence.

## Topology and permissions retain different scope

The directory list matches the expected root, binary/case/tiny containers, all 64 case directories and output directories, both tiny directories, and the special directory-input case. The missing-input case has no input entry; the directory-input case has a directory rather than a regular file; the symlink-input case has one relative symlink and a separate regular target. Treating every input path as an ordinary file would lose these intended failure conditions.

The inventory has no directory-mode fields. Its directory count and path set cannot independently establish permissions, freshness, exclusivity or successful creation of those directories. Historical reviewer statements about stronger filesystem checks retain their own scope.

For regular files, 492 entries declare mode 0600. Only the candidate and two tiny copies declare 0700. In particular, the 59 case output files remain nonexecutable according to this record. The executable tiny copies bind their respective originating build output size and digest. These metadata relationships describe the reported permission separation; permission alone is not evidence that a program ran or that execution was authorized.

## Scoped packet closure

The provenance record's three unchanged derived-copy declarations now all bind held repository bytes: this inventory, the detailed saved review and the prose result review. The seven tracked texts in the execution directory total 173,906 bytes and now all have complete semantic reading credit. This is a useful closure boundary: the reported execution packet can be recovered through its summaries, provenance, checksum and full derived records.

The raw traces, invocation and observation files, private receipts, original command captures and native programs remain unacquired. No upstream code was imported, candidate executed, live process scanned, model consulted or batch accepted during this unit. Earlier reports of a reviewer examining fuller raw evidence are preserved as historical reports. The narrower present access does not disprove that earlier work, and internal metadata agreement does not independently reproduce it.

For Continuum, the transferable distinction is between a closed metadata inventory and custody of the objects it names. Exact path-set joins can detect omitted or mismatched references while leaving content truth and execution claims dependent on separately available evidence. Directory metadata also needs an explicit schema if permission claims must survive a handoff.

Cumulative semantic reading reaches **528 distinct blobs / 4,389,202 bytes**, plus **77 identical alias paths**. The remaining gap is **4,988 paths / 3,901 distinct blobs**. Historical global acquisition overlap remains unresolved; neither the whole builder lane nor the whole repository is closed.

Next: read the 53,163-byte `artifact-r2/builder.layout.json` as static artifact metadata and join it with the already read source/build records. Reconcile fresh main and ownership first. No recipient has accepted that next unit. Storage, dispatch and public checkpoint work retain their separate ownership.
