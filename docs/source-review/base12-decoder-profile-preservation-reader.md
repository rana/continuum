# Complete preservation inventory and reader correction

This Research Delta fully reads `PRESERVED_BASE.json`, `reader.py` and `reader-r2.py` under `research/owned-stack/2026-10-16/native-builder-decoder-output-profile/independent-review/`. They total 87,959 bytes at Base12 commit `88382e793b65c84fd8e223840c27f6bb8682864a`, tree `5cf96129bdcb0dde075f6f5800ae0c68a95c4b82`. This chat owns the read-only contribution based on Continuum main `7a9612c45f55eb4536ecf98d385d6d5bdd02875f`. The [ledger](base12-coverage-decoder-profile-preservation-reader.json) binds all three; the [validation record](../../research/runs/base12-decoder-profile-preservation-reader/validation.json) preserves every baseline classification and observed check.

## Actual reader delta

The first reader was read completely. The second has a lossless full-file relation: it is exactly the first plus the four characters adding `n=4` to the unified-diff call. Removing that single keyword from its parsed syntax makes the complete reader ASTs equal. Both acquired hashes match the checksum list, identity record, correction and provenance.

This closes the earlier pending source-comparison claim. It confirms a formatting-only reader correction without importing or replaying either reader, altering candidate source or observing a new historical exit result. The saved failed/corrected outcomes retain their original reported scope.

The source explains why the first stop precedes output creation: all three top-level save calls occur after the diff-comparison assertion. That is consistent with the recorded zero first-attempt outputs, rather than a fresh filesystem observation of that historical directory.

## Reader effects are explicit

The reader parses candidate source as data and performs two fixed Git metadata reads. It checks regular input files and pinned source identities before comparison. It then reads all original builder-lane files for hash preservation, including native artifacts as data in that historical invocation. That historical hashing is separate from this chat's current payload custody and semantic review.

Its three JSON outputs are written sequentially with exclusive creation and 0600 mode. It provides neither an atomic set-level commit nor fsync of those records. A later write failure could therefore leave earlier review outputs present. This is a narrow property of the inspection machinery, not a claim about candidate publication behavior.

The reader has top-level effects and is not imported here. Its actual source, rather than its descriptive name alone, defines the distinction between source parsing, Git reads, payload hashing and review-file writes. One draft checker assumption about AST traversal order was corrected to use source-line order before producing the retained record.

## All preservation rows checked

The complete 65,811-byte baseline inventory contains 230 records / 1,987,240 path bytes. Every path, Git blob, byte length and SHA-256 field was read; the JSON round-trips exactly. Fresh, nontruncated historical tree metadata was recovered for base commit `4e2f235c9810454559b0711468c7610570e1436e`, tree `4298d0ae056f9873d17bf8489a0fa9da1877f7d9`.

Membership, blob identities and lengths match both that historical tree and the current pin for all 230 paths. Tracked Git modes also agree: all 230 are 100644. This verifies the complete metadata preservation relation rather than relying on the matching count alone.

The inventory itself records **no mode field**. The reader source asserts execute-bit agreement during its historical invocation, but no per-file workstation permission observation is retained in these rows or refreshed here. Fresh Git mode equality must remain separate from historical filesystem-mode evidence. Private cache permissions are custody controls, not the original checkout's modes.

SHA-256 custody remains separately classified:

| Evidence available now | Paths |
| --- | ---: |
| Exact held path bytes hashed | 139 |
| Held identical blob bytes hashed | 51 |
| Prior semantic ledger identity agrees; payload not held | 4 |
| Empty identity only; no semantic promotion | 5 |
| Payload checksum declaration remains unheld | 31 |

Git identity preservation does not acquire the 31 unheld native/prefix payload paths or turn their checksum declarations into fresh semantic readings. This maintains the previously recorded artifact gaps while strengthening the metadata claim.

The lesson is to inspect both the review machinery and the evidence it actually retains. Correct source comparison, preserved Git identity, tracked modes, historical workstation permissions and durable publication are separate properties; a PASS in one category should not silently supply another.

No historical reader executed, candidate imported, native artifact acquired/emitted/executed, model consulted, live process scanned, workstation activated or recipient acceptance obtained.

Semantic reading reaches **626 distinct blobs / 5,466,396 bytes**, plus **115 identical alias paths**. **4,852 paths / 3,803 distinct blobs** retain full-reading gaps. Whole-repository reading and historical global acquisition overlap remain incomplete.

Next: complete five remaining source-packet files—provenance, publication checks, future build-review needs, root checksum list and inspection-reader text—totaling 25,619 bytes, preserving their source-only and future-gate scope. Reconcile fresh main and ownership first; owned-storage, dispatch and public checkpoint lanes remain separate. No recipient has accepted that next unit.
