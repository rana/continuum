# Packaging boundaries: staged bytes, readback and authored metadata

Reviewed 2026-10-19 UTC at private Base12 commit `88382e793b65c84fd8e223840c27f6bb8682864a`, tree `5cf96129bdcb0dde075f6f5800ae0c68a95c4b82`. Three sources / 18,148 bytes were fully read and syntax-parsed: builder, metadata preparer and verifier. Exact identities are in the [ledger](base12-coverage-packaging-boundary.json). No source was imported or executed and no packet was generated.

## Research Delta: bind the bytes used at each stage

The builder enumerates 126 content members, including its explicit allowlist. It checks source paths, reads each once into an in-memory content map, computes manifest hashes from that map, then writes those same retained bytes to the ZIP. The manifest excludes itself; adding it gives the 127-member packet. This keeps member hashing and archive writing on the same staged representation, while initial source-path checks still assume stable trusted inputs during their reads.

The verifier checks exact membership against an external allowlist. Before reading each member, it checks normalized relative names, path components, regular-file metadata, permissions, encryption/comment/extra fields, suffixes and a two-million-byte member limit. It then reads/decompresses into memory, checks UTF-8/NUL and JSON/JSONL structure, CRC, manifest sizes/hashes and fourteen frozen source identities against a pinned static preflight. It does not extract files. This is a different boundary from the [parent checker's](base12-parent-checker.md) post-access checks on an already materialized tree.

Exact membership depends on the supplied allowlist. The per-member cap is not an independent total byte or member-count budget. The verifier rejects duplicate JSON keys, but does not explicitly reject nonfinite constants as the parent checker does. These are contract distinctions; no malformed historical payload or resource-exhaustion event was observed.

At the end, the verifier obtains the reported ZIP digest by rereading its path; it also rereads the allowlist for comparisons/digest. Connecting those returned identities to the previously verified open archive assumes path stability. No replacement race was exercised. For Continuum, preserve which bytes a check consumed and which bytes a receipt names; a correct member check alone does not establish that every later path read names the same object.

## Research Delta: file synchronization and output publication are different

The builder creates the allowlist and ZIP exclusively. It syncs the ZIP file before readback verification, then exclusively writes a verification record and digest sidecar. Its helper syncs each record file, but there is no directory sync or atomic transaction covering all outputs. A failure after a create can leave a visible artifact without the later verification record; exact rerun is not a recovery protocol because exclusive creation rejects existing paths.

The metadata preparer similarly creates/syncs history first and summary second, followed by permission checks/changes on auxiliary trees. These are useful no-overwrite and file-sync properties, not a demonstrated crash-safe multi-artifact publication guarantee. No interruption, power-loss or filesystem recovery test ran here, and no historical failure is inferred.

For Continuum, retain staging, created output, verified output and published receipt as distinct states. Readback can validate existing bytes; it does not by itself supply atomic visibility or recovery semantics for the set.

## Research Delta: a pinned input does not make narrative fields observed

The preparer's seven fixed receipt digests match acquired payloads and closeout references. Its experiment/documentation revision constants and verifier's static-preflight digest also bind to already acquired records. That gives actual custody checks for its declared inputs.

Its five reconnection events and resumed-scope fields are constructed as authored literals. Reading those AST literal values reproduces the saved history fields exactly, including the explicit retrospective provenance. Statements about an earlier process inspection, missing audit files and authorization are not fresh host queries performed by this preparer. Summary arm/resource fields are copied from the saved accounting audit. This confirms the [closeout review's](base12-audit-closeout.md) distinction between checked identities, inherited audit results and authored reconciliation.

The sources retain their original local layout assumptions; they are not newly runnable relocation-independent commands inside the extracted packet. The [validation record](../../research/runs/base12-packaging-boundary/validation.json) preserves actual pins, literal comparisons and source ordering. No model, worker, transport, numerical code or historical authority was activated.

Cumulative semantic reading reaches **350 distinct blobs / 2,480,717 bytes**, plus **52 byte-identical alias paths**: 402 covered paths. **5,191 paths / 4,079 distinct blobs** remain without full semantic-reading claims. Earlier empty-stream custody stays mechanical. The historical global acquisition aggregate remains unchanged because its full overlap index is unavailable. No private raw source, receipt, operational identifier or signal payload is published. Hosted CI checks public repository behavior, not private reading or historical execution.

Next bounded unit: manifest and allowlist, two texts / 51,361 bytes, plus the 309,057-byte review ZIP for mechanical custody only. Bind declared identities and compare archive members with the pinned tree and inventories using separately written inspection, without executing packaged code. Archive custody does not add semantic readings of its members. Reconcile main and ownership first; no recipient has accepted it. Owned-storage and dispatch-reconciliation work remain separate.
