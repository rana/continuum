# Disposable owned v1 object and acceptance store

`src/store.rs` now connects the bounded journal to original v1 objects and complete acceptance outcomes. This is the first semantic owned-store construction, **not qualification for retained data**. Sources: boundary/oracle commit `0a28ecafc06f61ed52f2e25fbc6fdbbb171822fe`, canonical codec and SQLite contract at main `c474b0dc9e6f4732d22a1c3f2f4da20df415a2cd`, ADR 0002 and the separately owned successor design in PR 112. This Codex session owns these disjoint implementation files. Fresh remote main and open PRs were reconciled before work; no overlapping implementation branch was observed.

## Authority and encoding

The separate crate links serde, serde_json, SHA-256 and thiserror; `cargo tree` confirms no rusqlite dependency. It includes **only** the original `src/object.rs` canonical codec at compile time using a source-relative path. It does not link the root core/store, use SQLite/Git at runtime, duplicate object encoding or run private upstream code. This deliberately shares object codec implementation with the SQLite reference; object-codec independence is not claimed. A separately authored Python decoder/hasher supplies additional checks. The source checkout, rather than the subdirectory alone, is currently needed to build; a shared codec crate can be extracted later.

Each frame contains exactly the serde_json serialization of a version-tagged enum:

- `ObjectV1`: `canonical`, an array of canonical object bytes. Replay verifies decoding, exact canonical re-encoding, ID, prior reference existence and kinds. Duplicate object events refuse; ordinary repeated puts return the existing ID without adding a frame.
- `AcceptanceV1`: `request_bytes` and `receipt`. The request bytes use the published v1 domain-separated encoding. The receipt contains sequence, full request, outcome, observed head and resulting head. Replay recomputes the request identity and expected transition against previously replayed state, compares the complete receipt, then installs it. Replayed/changed requests cannot masquerade as newly evaluated events.

Unknown versions/fields, duplicate serde fields, noncanonical event JSON, missing/wrong-kind closure, invalid names/preconditions, impossible sequences/outcomes and invented historical receipts refuse the entire opening. Objects and outcomes share the same journal and boundary protocol. In-memory object, head and receipt maps are rebuilt from bytes on every open. All store reads/writes retain cooperative exclusive ownership for that process; no separate index or concurrent-reader optimization exists.

New acceptances preserve full root-and-generation preconditions, generation increments only on accepted updates, and one global event sequence for each newly evaluated accepted **or stale** request. Object puts, exact retries and identity conflicts allocate no acceptance event. Exact retries return their original historical receipt even after later head movement. Operation identity is acceptor plus operation ID, while target is bound into request bytes. A changed request under that identity fails. This records local authority, not authentication or scientific truth; declared test evidence does not gate acceptance automatically.

The generic journal's existing limits and [fault assumptions](JOURNAL.md) still apply. Its 65,536-byte frame cap also bounds serialized object/event records, so this prototype accepts a **smaller object domain** than the reference codec's 16 MiB maximum. There is no chunking. Journal growth is capped at 1 MiB. CLI JSON reads are trusted local laboratory inputs, not a hostile-input service. Uncertain append/sync errors poison the journal handle; every store method checks journal health before using cached state.

## Executed Research Delta — 2026-10-19

Question: can the owned journal preserve original objects and historical acceptance semantics through an actual lost reply?

Local build, formatting, strict all-target Clippy and three existing framing tests passed after correcting a local Result-alias type collision and boxing the large event variant flagged by Clippy. No failed build is counted as a passed gate. Python store checks and the earlier journal process/corruption controls passed with the integrated code. [Actual store-check output and binary identity](store-validation.txt) are retained. Linux/Python 3.14/Rust 1.91.1; no physical-device durability qualification.

Observed in fresh disposable directories:

- The seven retained semantic traces / 18 acceptance invocations match the independently formulated finite oracle. These are the **same selected traces previously matched by the SQLite reference**, run against a separate store rather than dual-writing one authority. This is not all finite traces executed through Rust.
- A small original `positive(value)` investigation stores two exact source approaches, direct Python execution observations for inputs -1, 0, 1, and actual negative/pass EvidenceRecords. The first approach includes zero and fails the declared expectation; the second excludes it and passes. Both exact source blobs are recovered through independently opened CLI processes.
- The second approach is accepted; the process exits 76 after journal/marker/directory synchronization and before emitting a response. A fresh process, given only directory bytes, recovers sequence-1 receipt with the complete original request. Exact retry returns it with `replayed:true` and **no byte changes**.
- A stale alternative receives sequence 2; a later accepted movement receives sequence 3/generation 2. Both old accepted and stale requests still return their original receipts without new bytes. Changed-key reuse, missing closure and wrong-kind candidate fail without mutation.
- The independent Python frame/boundary/object/semantic reader validates **eight canonical objects and three evaluated outcomes**, derives IDs itself and checks each outcome through the history oracle.
- A copied journal is deliberately rewritten with a sequence-99 invented receipt and recomputed frame chains/boundary checksums. Both the Rust semantic opener and Python oracle reader refuse it without changing bytes. Physically consistent bytes therefore do not alone establish a legal accepted history.

Reproduce from repository root:

```sh
cargo build --manifest-path research/owned-authority/framing/Cargo.toml --locked
python3 research/owned-authority/framing/check_store.py research/owned-authority/framing/target/debug/owned-store
```

The Python reader and oracle share authorship and the published contract with the implementation. They reduce representation dependence, not all correlated-error risk. The negative/pass evidence is caller-authored from observed local test execution, not authenticated execution or a claim that the store itself ran Python. The chosen source is a synthetic small investigation, not a new model continuation of the CSV pilot. No provider call was made or retried; receiver acceptance, export/restore and retained-data adoption are not established. Coherent rollback remains undetectable; process exit is not power loss.

Next: no-overwrite export and fresh-directory restore preserving original objects and receipts, then one real continuation of this owned-store development and a distinct public investigation. Review resource limits, interruption/uncertainty behavior and complete contract coverage before adopting the path for retained work.

The subsequent [exact-image export/restore](ARCHIVE.md) now implements the next transport step with five process-exit controls. The original store observations above retain their original scope.
