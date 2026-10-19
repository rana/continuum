# Owned journal framing: first construction slice

Disposable Rust implementation with no SQLite/Git runtime dependency, plus a separately authored Python reader. This is a framing primitive, **not a qualified store or acceptance engine**. It does not read or modify retained Continuum stores.

Sources: main `c474b0dc9e6f4732d22a1c3f2f4da20df415a2cd`, [ADR 0002](../../../docs/decisions/0002-owned-storage-research.md), and selected successor design at Git commit `c7e3f48` ([PR 112](https://github.com/rana/continuum/pull/112)). The design and earlier owned-model branch tips were reconciled before construction; neither older tip contained implementation beyond main. Design publication remains independently owned. Implementation owner: this continuing Codex engineering session, disjoint `research/owned-authority/` files.

## Wire contract

Each frame, concatenated without padding:

| Offset | Encoding |
| --- | --- |
| 0 | eight exact bytes `CTJFR001` |
| 8 | u32 little endian payload length, 0 through 65,536 |
| 12 | u64 little endian frame ordinal, starts at zero |
| 20 | 32 bytes previous frame digest; zero for first frame |
| 52 | exact payload bytes |
| 52 + length | SHA-256 of `continuum:journal-frame:v1` followed by NUL followed by this frame's preceding bytes |

Ordinal is a structural counter, **not the global acceptance sequence**. Payloads are opaque bytes; this primitive supplies no v1 object encoding, acceptance, operation identity or receipt semantics. Both readers reject the entire supplied image on malformed version, length, sequence, chain, digest or partial frame. They return no valid prefix on error and never truncate. Empty image is structurally valid.

A whole-frame suffix loss is indistinguishable from an intentionally shorter image. This is deliberately tested, not repaired with an assumed marker. Checksums are accidental-corruption detection, not authenticity. No committed boundary or acknowledgement history can be inferred from a syntactically valid image.

`create` exclusively creates a fresh file, writes its entire image, calls `sync_all`, then returns. Any error preserves the path and returns error; do not automatically repeat against another path after uncertain I/O. Existing files cannot be opened for writing by this API. No append/reopen writer, writer takeover, parent-directory sync, index, export, upgrade, migration, compaction or power-loss guarantee is provided. The CLI is a trusted disposable test interface, not bounded hostile-input service: it reads the supplied file into memory. These limitations preclude adoption as authoritative storage.

## Reproduce

From repository root:

```sh
cargo fmt --manifest-path research/owned-authority/framing/Cargo.toml -- --check
cargo clippy --manifest-path research/owned-authority/framing/Cargo.toml --locked --all-targets -- -D warnings
cargo test --manifest-path research/owned-authority/framing/Cargo.toml --locked
cargo build --manifest-path research/owned-authority/framing/Cargo.toml --locked
python3 research/owned-authority/framing/check.py research/owned-authority/framing/target/debug/continuum-journal-framing
```

No provider calls, upstream execution, native binary acquisition or retained-data changes. This separate crate has its own lockfile and workspace. Root tests do not implicitly test it; a scoped workflow explicitly runs these checks.

## Research Delta — 2026-10-19

Question: can we start owning persistent bytes while making recovery ambiguity executable?

Executed on Linux, Rust 1.91.1, filesystem reported `ext2/ext3` by `stat -f` (not device/physical durability qualification). Formatting, strict all-target Clippy, three Rust tests and the Python subprocess check passed. Python output is retained in [validation.txt](validation.txt). The temporary directory is removed after checks; no production data was created.

Observed: exclusive fresh-file creation, file-sync return followed by deliberate process exit 73 before reply, recovery of all three original payloads in a fresh reader process and independent Python decoder; an overwrite attempt fails without changing bytes; corrupt-file reading refuses and preserves bytes. The Python reader refuses all 297 nonboundary proper cuts and all 300 single-byte flips in its 300-byte fixture. Rust independently checks all nonboundary cuts and flips in a distinct two-frame fixture, maximum payload, oversize payload and reordered frames.

Finding: frame integrity is useful but insufficient. Losing complete final frames, including the whole file, passes framing. The test makes this counterexample explicit. Do not label it successful committed-history recovery. Independent syntax implementations still share the authored format and are not an independent acceptance oracle. A deliberate process exit is not physical power loss or proof of parent directory persistence. No performance comparison or receiver acceptance is established.

Next coherent unit: formulate the finite acceptance oracle independently of journal replay; preserve v1 identity, ABA generations, accepted/stale historical receipts and changed-request rejection; implement a committed-boundary selection protocol with declared uncertain-sync behavior and counterexamples before enabling journal reopening or accepting real work. Then connect one disposable source/failed-approach/accepted-proposal investigation, lost-reply receipt recovery and no-overwrite restore. This slice intentionally does not claim that complete demonstration is done.
