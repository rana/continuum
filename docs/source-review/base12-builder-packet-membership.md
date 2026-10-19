# Complete builder packet and payload membership

This Research Delta reads three complete texts / 71,242 bytes at Base12 commit `88382e793b65c84fd8e223840c27f6bb8682864a`, tree `5cf96129bdcb0dde075f6f5800ae0c68a95c4b82`. The current Continuum chat owns this read-only contribution, based on main `39f2dbb0f0e2920552f09c728cacf8406973ff76`. Selected files under `research/owned-stack/2026-10-16/native-builder-slice/preparation-01/` are `freeze_review_packet.py`, `PACKET.sha256` and `PAYLOAD.sha256`. The [ledger](base12-coverage-builder-packet-membership.json) retains identities; the [validation record](../../research/runs/base12-builder-packet-membership/validation.json) classifies every referenced member.

## Two complete lists, different purposes

Both lists were reconstructed byte-for-byte, including separators and final newlines. Every row was read through a complete 157-digest dictionary and lossless path projections, retaining the common payload root separately. This preserves full list reading without publishing private absolute operational paths. No payload acquisition is inferred from reading a checksum.

The review packet has 177 members. They are exactly the pinned preparation subtree except `PACKET.sha256` itself. The runtime payload has 217 members: 45 original-lane dependencies plus 172 preparation members. Their intersection has 172 paths with matching digest declarations; the union has 222 unique paths. Both lists are sorted and unique, and every name resolves to a pinned tree blob with regular Git file mode. That checks repository metadata, not current workstation canonical paths or filesystem modes.

The original-lane dependencies are all 44 original checksum entries plus that checksum file. Five packet members are excluded from the payload: the payload list, literal-command document, preparation metadata, final static review and review request. These later documents can bind and describe the runtime freeze without creating a recursive payload hash. The packet includes them while excluding itself. This layering requires an externally trusted packet/literal identity; a list cannot authorize its own execution.

The fixture subtree has 158 packet paths including its checksum file. The previous final review's 157 fixture-manifest members exclude that file. An initial local count equated the two, and the assertion stopped; correcting the scope reconciled the counts. No fixture manifest was acquired or treated as freshly verified in this unit.

## Writer source and exact literal relation

The offline writer first checks the original checksum entries, gathers original files and nonexcluded preparation files, rejects duplicate/noncanonical/symlink paths, writes the payload list, and formats the proposed literal command with its digest, count and four control hashes. The source was read in full and syntax-parsed only.

An original extraction of its inert template string, formatted with the saved metadata, reproduces the complete existing literal command exactly. Its digest also agrees with preparation. This checks the relationship between writer source and the saved review deliverable without importing the writer, calling its main routine, evaluating the gate or writing any historical output.

The writer's own code writes the payload list and command document; it does not write the packet checksum list. Complete packet membership was independently compared with the pinned tree rather than attributed to an unobserved call of this routine. Its ordinary write operations also do not provide atomic multi-file publication or durable acceptance.

## Available bindings and remaining gaps

Across the 222 unique referenced paths, 44 bind held exact-path bytes and 19 bind held bytes through identical pinned Git blobs. Four agree only with earlier full-reading ledger identities whose cache bodies were not recovered here. Five zero-size entries have consistent pinned size and empty digest. The remaining 150 are unheld digest declarations. Each classification is explicit in the validation record; none becomes a fresh semantic reading merely because it appears in both lists.

The alias bindings include existing tiny source texts and frozen source copies. Empty expected files are mechanical metadata checks, not successful publication observations. Binary expectations remain unacquired. Reading the whole list establishes membership closure and available custody, not correctness of all fixture derivations or reproduction of the reported original verifier's full hash checks.

One useful new relation closes: the independently predicted 16,608-byte runner map from the complete source/migration review has the same digest as `fixtures/expected/01.map` declares. That expected map remains unheld. This binds the earlier whole-map prediction to the packet's intended comparison target while keeping actual generated output and runtime success separate.

## Research return and next unit

A complete freeze can be internally closed while many payloads remain unread or unheld by a later reviewer. Preserve list membership, byte custody, semantic inspection and observed execution separately. The original final review's fuller access remains its historical claim; current narrower access does not revise that history.

Coverage reaches **515 distinct blobs / 3,948,480 bytes**, plus **77 identical alias paths**. The remaining full-reading gap is **5,001 paths / 3,914 distinct blobs**. Historical global acquisition overlap remains unresolved. No candidate binary, control, model or native program was invoked; no binary was newly acquired.

Next: fixture materializer, fixture review, fixture provenance and fixture checksum list, four texts / 54,576 bytes. Check how expected fixtures are derived before interpreting case manifests and execution results. Reconcile fresh main and other workers first; no recipient has accepted the next unit. Separate storage, dispatch-reconciliation and public checkpoint lanes retain their ownership.
