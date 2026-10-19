# Decoder-output profile foundation

This Research Delta fully reads five foundation files under `research/owned-stack/2026-10-16/native-builder-decoder-output-profile/`: README, ownership, open status, manifest and source diff. They total 13,638 new semantic bytes at Base12 commit `88382e793b65c84fd8e223840c27f6bb8682864a`, tree `5cf96129bdcb0dde075f6f5800ae0c68a95c4b82`. The previously credited 5,556-byte contract was also recovered and reread, with no additional coverage credit. This chat owns the read-only contribution based on Continuum main `63a2365b0a24ad4dd26da3b92ea90ad1ef103286`. The [ledger](base12-coverage-decoder-profile-foundation.json) pins all acquired identities; the [validation record](../../research/runs/base12-decoder-profile-foundation/validation.json) records exact checks and limits.

## Three consumer-header values

The complete retained diff contains one nine-line hunk with one replaced source line. Applying it as data to the held R2 source reproduces the declared 24,745-byte variant source SHA-256 and pinned Git blob identity. The resulting source is parsed as syntax only; no upstream source was imported or executed. Full direct acquisition/reading of the variant source remains a separate next unit and gains no credit here.

Restricted numeric AST evaluation and comparison isolate exactly three generated consumer-header values:

| ELF field offset | R2 value | Profile value |
| --- | --- | --- |
| 136: RW virtual address | `0x410000` | `0x500000` |
| 144: RW physical address | `0x410000` | `0x500000` |
| 160: RW memory size | 4,096 | 10,555,392 |

Replacing that field-list node makes the rest of the complete source AST equal. The RW file size remains zero, alignment remains 4,096, and entry/RX address constants agree. The new consumer interval is `[0x500000,0xF11000)`. Base and size are page-aligned; at the declared maximum consumer ELF size, its RX/RW address gap is `0xFC000`. These are source/contract arithmetic checks, not loaded-memory or emitted-header observations.

The builder's own writable state is a different region and remains unchanged by this diff. Enlarging the generated consumer mapping does not enlarge the admitted source, instruction, label, relocation, code or map bounds. It does not make the accepted decoder's incomplete lowering fit those bounds.

## Identity joins with explicit custody

The complete manifest contains 22 file records and excludes itself and the root checksum list. Every declared length agrees with the pinned tree. Five payload hashes bind exact held paths, one binds the unchanged seed through an already held identical blob, and one binds the variant source reconstructed from the exact diff. Fifteen payload hashes remain unheld declarations rather than newly verified bytes. The preserved source/seed identities agree with the README and manifest.

Both JSON documents reconstruct exactly, preserving every field. The ownership record includes a historical task/worktree inventory and explicitly does not claim a live process scan or full-host absence. Historical consumed attempts, parent-owned integration and pending exact-head review remain facts of that source unit; they neither transfer ownership to this chat nor establish current worker inactivity.

## Source-only status is a dated boundary

The README, contract, manifest and open record describe a source-only unit awaiting later gates. The pinned tree also contains later build/correctness/result directories. Their existence is observed, but their contents have not been reviewed in this unit. Consequently the source-unit status must not be presented as a reconciled claim that the entire profile was never subsequently built, nor as evidence that any later result was accepted.

The contract requires equal code/map output for identical admitted input, with only the three specified consumer-header fields changing. That remains an obligation and static prediction here. Old R2 whole-ELF hashes and positive output expectations do not become profile-specific oracles.

Runtime compatibility is narrower still. Absolute writable addresses embedded in source immediates are not relocated by changing the output header. A source using the old RW address can retain identical code and map bytes yet refer to a region the new profile does not provide. Code/map identity therefore cannot substitute for memory-contract compatibility. No new source form, configurable profile selector or general memory verifier is introduced by this diff.

No native artifact was acquired or emitted, model consulted, live process scanned, workstation activated or recipient acceptance obtained. The transferable lesson is to bind a narrow source delta precisely while keeping generated-artifact identity, memory assumptions, dated permissions and later execution history separate.

Semantic reading reaches **614 distinct blobs / 5,327,763 bytes**, plus **114 identical alias paths**. **4,865 paths / 3,815 distinct blobs** retain full-reading gaps; historical global acquisition overlap remains unresolved. Whole-repository reading is incomplete.

Next: fully read the profile bootstrap, static review and author checks, totaling 32,987 bytes, and join their complete evidence to this exact source delta without importing or executing upstream code. Reconcile fresh main and ownership first; owned-storage, dispatch and public checkpoint lanes remain separate. No recipient has accepted that next unit.
