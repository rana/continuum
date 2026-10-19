# Gate-A private inventory: complete metadata reconciliation without payload access

Reviewed 2026-10-19 UTC at private Base12 commit `88382e793b65c84fd8e223840c27f6bb8682864a`, tree `5cf96129bdcb0dde075f6f5800ae0c68a95c4b82`. The 59,438-byte inventory was fully read through a private field-preserving table: all three header fields, all 61 distinct digest values and all 368 ordered path/length/digest rows. Reconstructing the original JSON reproduces every byte exactly. The [ledger](base12-coverage-gate-a-private-inventory.json) records its identity; the [validation record](../../research/runs/base12-gate-a-private-inventory/validation.json) records comparisons. The raw inventory/view and operational root remain private.

## Research Delta: the complete expected metadata set matches

An original derivation from the frozen 65-case manifest, twelve fault-result rows and fixed collision/retained checks yields **352 output-related paths**. That set equals the inventory's output-related set exactly, with no duplicate or extra listed path. The other **16** rows describe attempt-level receipts, giving **368 unique paths** total. This establishes consistency of the saved metadata set, not the present filesystem or an independently observed execution census.

All **72 matrix output hash declarations** match the 36 accepted fixtures' header/data expectations. All **12 EINTR output hash declarations** match the accepted baseline pair. The retained pair's lengths and digests match RESULT, and the seven-byte collision sentinel matches the exact expected bytes' digest. These are comparisons among preserved declarations; none of the named output payloads was opened or rehashed here.

All **130 matrix stdout/stderr rows** and **79 staging receipt rows** declare zero bytes and the empty digest. All **44 entry-receipt length/digest pairs** match a NUL-delimited permutation of exactly their expected filenames: 36 matrix directories, six EINTR directories, collision and retained output. This reproduces the metadata consistency checks behind the accepted result audit. It does not read the original entry receipts, attest file types, or demonstrate current absence of staging/rejected paths. Those observations keep their frozen-driver/on-host-review dependency.

All **twelve trace digest declarations** match the saved fault summaries. A trace digest without trace bytes cannot independently substantiate an injected syscall, retry arguments or call ordering. No syscall-buffer payload was acquired.

## Research Delta: distinguish a copied receipt from an omitted private observation

Fifteen of the sixteen attempt-level inventory entries match exact held receipt copies by length and hash, including the mechanical empty stderr. The remaining entry declares a **4,325-byte process-list receipt** whose bytes remain omitted. It supplies content identity, not a reconstructible process list or evidence identifying which vanished process was related to the monitored group. No process-list read, live scan or attribution was performed.

The inventory's flags describe inventory-only preservation and exclusion of full traces/payloads from Git. Their presence is an authored scope declaration, not itself a recursive privacy audit. This contribution publishes original findings and counts only, with no raw inventory, private root, process identities, decoded outputs, trace buffers or source payloads.

For Continuum, a complete hash inventory can close a metadata reconciliation while retaining explicit missing-payload and live-observation boundaries. Reconstructible views should preserve every field and prove exact source roundtrip; compression must not silently remove the evidence needed to assess the result.

## Scoped Gate-A reading boundary

The pinned Gate-A directory has **61 paths**. Full semantic reading now covers its **56 nonempty source/document/metadata paths**. One zero-byte receipt is separately mechanically checked. Two instruction texts and two binary instruction artifacts remain without semantic credit; the binaries are unacquired. No whole-directory semantic-completion or fresh executable-verification claim follows. The next return moves to the related decoder B1 port-boundary documents rather than repeating an accepted, consumed batch.

Cumulative repository semantic reading reaches **452 distinct blobs / 3,501,864 bytes**, plus **52 byte-identical alias paths**, covering 504 paths. **5,089 paths / 3,977 distinct blobs** remain without full semantic-reading claims. Historical acquisition totals stay unchanged. No upstream audit/controller/native program or model ran. Hosted CI checks this public contribution, not historical filesystem state or native correctness.

Next bounded unit: decoder B1 port-boundary README, requirements, layout sketch, next-source and opening documents, **five texts / 25,425 bytes**. Recover the proposed portability/interface boundary and its stated evidence before following implementation claims. Reconcile main and lane ownership first; no recipient has accepted this next unit. Owned-storage, dispatch-reconciliation and public self-use checkpoint lanes remain separate.
