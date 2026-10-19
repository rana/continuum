# Fresh-process owned CLI cost on tmpfs

The fixed [pre-measurement plan](PLAN.md) completed on 2026-10-19 with **nine disposable stores and 369 retained uninstrumented invocations**. Exact semantic responses, byte preservation for non-appending operations, separate successful synchronization observations and final independently decoded histories passed. This is a **tmpfs process/replay probe**, not a durable-device latency benchmark or a reason to remove safety barriers.

## Source and method

The owned storage source is `8bc0fc1578fb915f10fedd22ee016bf9c4e9b2df`, unchanged at measured base `ea197d7c37352dbe13585ecf0e2c7fa489a03fe2`. [check.py](check.py) is an original fixed workload; [result.json](result.json) retains its digest, source-file identities, executable identity/size, individual wall times, exact child stdout/stderr and summaries. Release binary SHA-256: `4a08fa52fd907e165cf8c3ee5a0596d7d780feb750b9c67f350c5a50cf9fe75c`, 990,720 bytes. No binary is committed.

Build: `cargo build --release --locked --manifest-path research/owned-authority/framing/Cargo.toml`, default release profile. Observed environment: Linux x86_64, kernel `7.0.0-38-generic`, Rust 1.91.1, Python 3.14.4. `stat -f` classified the disposable-directory filesystem as **tmpfs**. No CPU isolation, load measurement, cold-cache procedure or physical-storage identification was performed. Successful fsync on this substrate cannot establish disk durability or disk synchronization cost.

At each of 1, 16 and 64 updates, three fresh stores each received a distinct 128-byte Blob, one-entry Snapshot and acceptance per update. Each store then ran eight repetitions of five non-appending operations, followed by one new stale acceptance. Each timed invocation starts a fresh process and includes launch, output capture, complete recovery/replay, synchronization and serialization; input JSON preparation is outside the timer. It is not an in-process map-lookup measurement. Sizes and operations run in fixed ascending order, with warm caches and no randomization.

The first local attempt failed on a **harness outcome-label error**, before producing a result file: it expected `stale` instead of the actual contract label `precondition_failed`. [initial-failure.txt](initial-failure.txt) preserves that disposition. The completed run follows the corrected assertion, with no storage implementation change. Its 369 samples exclude all incomplete-run timings; no successful completed run was discarded or repeated for speed.

## Observed results

Full subprocess median milliseconds; n=24 per non-appending operation/history size, n=3 for new stale acceptance. These distributions are small, sequential and environment-specific; raw minima/maxima and every sample remain in result.json.

| Operation | 1 update | 16 updates | 64 updates |
|---|---:|---:|---:|
| Get latest Blob | 1.022 | 1.231 | 2.444 |
| Head | 0.965 | 1.289 | 2.469 |
| Latest receipt | 0.649 | 1.292 | 2.422 |
| Retry first accepted request | 1.129 | 1.347 | 2.476 |
| Duplicate latest Blob put | 1.007 | 1.317 | 2.422 |
| New stale acceptance | 1.170 | 2.009 | 2.957 |

The initial journals were 1,557 / 30,577 / 127,340 bytes for 128 / 2,048 / 8,192 source Blob bytes, respectively, with 2 / 32 / 128 objects and 1 / 16 / 64 outcomes. These bytes include canonical object envelopes, JSON number arrays, Snapshot references, complete requests/receipts and frame overhead. Their ratio is not pure codec overhead or a whole-project storage amplification metric. Every history remained below the one-MiB journal limit.

For every non-appending sample, the complete object/head/receipt response matched and journal/boundary bytes stayed identical. The exact first request returned its original sequence-1 receipt even after later head movement. The new stale request allocated the next sequence with `precondition_failed` and preserved the current head.

Separately, the existing original Linux libc interposer logged successful fsync roles for six operations on each store (54 instrumented invocations). Failure injection was disabled and those invocations were excluded from timing samples. Each read, historical retry and duplicate put called journal, boundary, store directory and parent sync. A new stale acceptance called those four plus intent file, directory, appended journal, pending boundary, commit directory and cleanup directory: **ten total**. The instrumented append followed the timed append and had a distinct operation ID; its final history therefore contains two additional stale outcomes. The independent Python reader/oracle checked all nine final histories and complete object closure. Final store directories contained only lock, journal and boundary files.

## Research Delta and next action

The source rebuilds state and canonical framing on each CLI open, and the local observations show greater fresh-process latency with the larger tested histories. They do not isolate replay from hashing, parsing, synchronization, process scheduling or caching, nor establish a fitted complexity law. Explicit sync-call counting identifies policy work even when tmpfs hides physical-device cost. A model review is unnecessary to interpret these directly retained measurements; no inference was invoked or uncertain call repeated.

Next: rerun this fixed workload on an explicitly selected persistent-filesystem disposable directory, preserving tmpfs as a separately labeled substrate, before choosing an optimization. Consider an in-process phase breakdown only after that comparison. Keep the four startup barriers and persistent fence in place; this probe does not authorize weakening them. Independent version-2 protocol review, kernel/device error qualification and retained-data adoption remain open. SQLite comparison, sustained throughput, concurrency, multi-user security, actual receiver acceptance and workstation activation are not established.

## Reproduce and inspect

From repository root, build as above, then run:

```sh
python3 research/owned-authority/cli-cost/check.py --binary research/owned-authority/framing/target/release/owned-store --output /tmp/owned-cli-cost-result.json
python3 research/owned-authority/cli-cost/verify.py
```

The probe requires Linux, `cc`, `stat` and a release CLI; it measures whichever filesystem the default temporary-directory selection actually uses and records its classification. Preserve a new run separately rather than overwriting the retained observation. The offline verifier reruns no child processes or timing: it checks source custody, all raw returned values against independently constructed object IDs/receipts, sample counts, summaries and the retained sync-role observations. CI runs only that offline check; there is no performance threshold.
