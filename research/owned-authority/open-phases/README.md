# Opening versus already-open work: cost and ownership together

The original research worker completed **nine opens, 5,760 checked API samples and nine cross-process held/released lock controls** on 2026-10-19. Opening medians were 5.6–7.6 ms. Repeated already-open API calls measured tens to hundreds of nanoseconds in this small warm workload, with important timer/compiler limits. Every competing fresh-process read was refused while the handle remained open and succeeded after release. Reusing validated state therefore retains the existing exclusive-ownership cost; this is not a concurrent-reader optimization.

## Source and protocol

[PLAN.md](PLAN.md) precedes the measurement. The added [owned-phase.rs](../framing/src/bin/owned-phase.rs) is a disposable research binary in the separate framing crate. Journal/Store, synchronization policy, canonical objects and acceptance semantics are unchanged from `8bc0fc1578fb915f10fedd22ee016bf9c4e9b2df`. Parent source is `ae7e6c626586c1040e076d5efd92fcea3abbd068`; PR 117 was integrated separately after all four head checks passed.

[check.py](check.py) recreates the same 1/16/64-update histories, three stores each, in a newly created disposable checkout-filesystem parent. Each worker measures `Store::open` once, then 128 get/head/latest-receipt/first-exact-retry/duplicate-put calls on one handle. Request/object argument cloning happens before the timed calls. `std::time::Instant` wraps the API call, Result propagation and `black_box`; checking, JSON conversion and output occur outside that interval. All five results are checked on every sample; the final exact response for each operation is retained. The probe appends no new events during measurement.

The worker then executes the same CLI `head` command twice: while it holds the store, and after explicitly dropping the handle. All nine held commands returned code 1, empty stdout and `filesystem: lock acquisition failed because the operation would block`. All released commands returned code 0, empty stderr and the complete expected head. These controls are outside API timings. Parent-side byte checks found journal/boundary unchanged, and the separate Python semantic reader checked every final object/history against its oracle. Store directories contained only lock, journal and boundary files.

The release CLI SHA-256 is still `4a08fa52fd907e165cf8c3ee5a0596d7d780feb750b9c67f350c5a50cf9fe75c`; worker SHA-256 is `33e22233e6ca103840ec184eaf5941d4b039687885dd4c1f65d3625f42449b1f`. [result.json](result.json) retains exact source/size/hash metadata, workload specifications, checked response values, raw timing samples and actual lock-control outputs. Both binaries were built with the default release profile and locked dependencies; no executable is committed. Formatting and strict all-target Clippy passed before execution.

Observed environment: Linux x86_64, kernel 7.0.0-38-generic, Rust 1.91.1, Python 3.14.4; `findmnt` ext4 and `stat -f` ext2/ext3. These identify the mount namespace, not physical persistence or a qualified device. The four startup synchronization barriers remain in the unchanged open path. This probe does not instrument their individual timings or attribute the opening duration among hashing, decoding, synchronization and semantic replay.

## Observations

Open medians have **three samples per size**. API medians have **384 samples per operation/size**, taken in repeated fixed-order warm loops rather than independent worker invocations.

| Phase/operation | 1 update | 16 updates | 64 updates |
|---|---:|---:|---:|
| Store open, milliseconds | 5.576 | 6.735 | 7.555 |
| Already-open get, nanoseconds | 30 | 50 | 40 |
| Already-open head, nanoseconds | 60 | 90 | 61 |
| Already-open receipt, nanoseconds | 60 | 140 | 130 |
| Exact retry, nanoseconds | 261 | 391 | 261 |
| Duplicate put, nanoseconds | 401 | 611 | 441 |

Tens-of-nanoseconds samples are close to clock/measurement overhead and compiler effects; `black_box` does not prove their absence. No empty-loop calibration, CPU isolation, load measurement, randomization or cold-cache procedure was performed. Verification/serialization between samples also warms data. Do not promote these values into service latency, sustained throughput, precise lookup cost, a fitted scaling law or an equivalent-boundary speedup against full CLI calls.

The initial journal cut/hash, object count and receipt history for every cell match the earlier full-process workload exactly. All first retries still return the original sequence-1 receipt after head movement. Matching semantics reduces one source of comparison ambiguity while the timing and ownership boundaries remain different.

## Research Delta and next useful unit

The earlier full-process observations bundled opening with the selected operation. This probe places actual clocks around those different phases without weakening safety. The much smaller already-open samples make a bounded reuse path worth considering, while the lock controls show exactly what reuse excludes: another valid process cannot read through the same opening path until the holder releases it. A long-lived handle is not a free availability improvement.

Next: construct one bounded multi-read investigation view that opens once, verifies a source/receipt projection and releases ownership before emitting the view for slow external work. Keep inference and command execution outside the store lifetime; test competing access after release and exact source/receipt custody. This turns the phase result into useful continuation behavior without introducing a daemon, indefinite session, concurrent-read promise or barrier removal. Retained-data adoption, physical/kernel writeback qualification and independent version-2 protocol review remain open. No provider call, worker dispatch or activation occurred here.

## Verification

From repository root:

```sh
cargo build --release --locked --manifest-path research/owned-authority/framing/Cargo.toml
python3 research/owned-authority/open-phases/check.py --cli research/owned-authority/framing/target/release/owned-store --worker research/owned-authority/framing/target/release/owned-phase --output /tmp/owned-open-new-result.json
python3 research/owned-authority/open-phases/verify.py
```

Preserve any new observation separately. The offline verifier checks all response expectations using independently constructed object IDs/receipts, every timing count, both lock-control outcomes, byte-cut identity and probe/source custody. It reruns no measured worker or storage operation. CI compiles the research binary with existing strict checks and runs only the offline record check, with no timing threshold.
