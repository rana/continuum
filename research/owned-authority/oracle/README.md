# Finite acceptance oracle

This independent history-projection oracle prepares semantic checks for owned storage. It does not decode journals or claim that bytes are committed. Inputs are finite symbolic, valid requests over already present Snapshot roots A/B. The reference semantics come from [v1 object/acceptance contract](../../../docs/architecture/object-format-v1.md), `src/store.rs` at main `c474b0dc9e6f4732d22a1c3f2f4da20df415a2cd`, and [ADR 0002](../../../docs/decisions/0002-owned-storage-research.md). The frame primitive is separately pinned at `2c07d91df54d9ad98f515217a6022bf6e8869354`.

`oracle.py` reconstructs each head from the ordered history of accepted requests and derives event sequence from evaluated history length. It does not maintain a mutable head/receipt map. `machine.py` is a separate mutable map formulation with six deliberate defect switches. Neither imports the other. This structural separation helps expose shared mistakes; both were authored by the same engineer from the same contract, so agreement is not independent human review or a correctness proof.

`check.py` enumerates every request trace of lengths 1–4 over an ordered 20-request alphabet, without pruning: 18 combinations of three operation IDs, two roots and three preconditions (absent/A1/B1), plus a changed-target request and changed-acceptor request. It compares every step of the nonmutant machine to the history oracle. For each mutant it preserves the first shortest distinguishing trace in that enumeration. This means shortest within the declared alphabet, not globally minimal.

Six mutants must be caught: root-only precondition matching; retry result replaced with current head; changed request ignored under an old operation identity; stale evaluations omitted from the global sequence; stale receipts not retained; and operation identity incorrectly scoped to target. An additional six-step ABA trace accepts A1, B2, A3, rejects an old A1 precondition, retries the original acceptance and retries the stale result. No root-only ABA pass is allowed.

An optional SQLite comparison materializes the six witnesses and ABA trace as valid v1 objects and requests. Blob and Snapshot IDs are independently derived with Python SHA-256 from the published wire format and compared with the native CLI. Every acceptance uses a separate process; every returned receipt is compared in full (including original request, sequence, observed/resulting heads and replay flag), and a separately opened receipt lookup is checked. Conflicts must return an operation error. Databases and inputs are temporary and removed after checks. This is not dual-writing one authoritative workspace.

From repository root:

```sh
cargo build --locked
python3 research/owned-authority/oracle/check.py --binary target/debug/continuum
```

Without `--binary`, it only runs finite semantic comparison. It prints a JSON result, never rewrites retained evidence. [result.json](result.json) preserves this run's witnesses, expected/actual mutant differences, exact counts, separate ABA trace, SQLite comparison counts and actual binary SHA-256. It is evidence for this run, not a requirement that future build digests match.

## Research Delta — 2026-10-19

Owner: continuing Codex engineering session; disjoint owned-authority implementation files. Reconciled main, unchanged repository instructions and existing PRs before construction. No other owned implementation branch had commits beyond main; that is not a claim that another worker was inactive. Successor design remains in separately owned PR 112.

Executed on Linux/Python 3.14/Rust 1.91.1: **168,420 finite traces, 664,820 transition comparisons**, all nonmutant comparisons matched. All six mutants were distinguished, at lengths 1, 2 or 3. **Seven SQLite traces / 18 acceptance invocations** matched, including expected errors; all successful receipt lookups matched. This is a selected baseline sample, not SQLite execution of all 168,420 traces. Actual source is the main revision above; binary identity is in result.json.

The first baseline harness attempt failed before any acceptance because it omitted explicit database initialization: native error `database does not exist; run continuum init first`. That known local harness error was corrected by adding and checking `init`; a new disposable run then passed. This was not an unknown external effect or storage-engine defect.

Finding: stale evaluations consume a global event sequence even when no head moves, while object puts and exact replays consume none. Operation identity spans targets within an acceptor. Root equality without generation admits stale acceptance after returning to the same root. A later head must not overwrite a historical accepted or stale receipt. These requirements now have executable short counterexamples rather than only prose.

Limits: valid finite symbolic requests, two roots, named namespaces, depth four plus the explicit ABA trace. Not a complete validator for arbitrary UTF-8 names, canonical request bytes, malformed objects, missing closure, integer exhaustion, concurrency, crashes, persistence reordering, uncertain sync, corruption or lost commit metadata. The model has no physical recovery or delivery history. It must not be used to select readable state from a damaged journal. No new Claude call, provider outcome, real successor acceptance, performance claim, migration or activated runtime is established.

Next: connect these semantic fixtures to a disposable owned journal only after declaring committed-boundary selection and uncertainty behavior. Preserve complete-frame-loss and damaged-boundary counterexamples; never infer a safe writable prefix from checksum validity alone. Qualify actual process interruption and no-overwrite export/restore before a real investigation uses this path.
