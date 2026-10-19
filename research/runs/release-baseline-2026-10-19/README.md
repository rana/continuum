# First observed release workload

## Question and result

Can the existing native core perform a reproducible bounded workload, return the intended results, and expose enough timing and provenance to select a useful next experiment?

Yes under the recorded conditions. Three independently started release-build processes each completed 100 samples for all nine operation groups (2,700 timed calls total). Every declared correctness assertion passed; all three runs produced the same fixture and semantic fingerprints. This is one environment with three repetitions, not 2,700 independent scientific trials.

The implementation adds one standalone example and no core dependency or storage change. [Methodology](../../../docs/experiments/release-baseline.md) explains the fixture, timing boundaries, percentiles, and exclusions. [Provenance](provenance.json) retains exact source-file hashes, build/run commands, toolchain, binary digest, environment observations and validation output. The input core is the public `b57df43a05f4b15a5a931765c91d3fcb50516d37` source; the new harness was uncommitted at measurement time and is identified byte-for-byte in that record.

## Observations

The table gives the range of each run's descriptive p50 and p95, in microseconds. It does not pool samples or imply confidence intervals.

| Operation | p50 across three runs, µs | p95 across three runs, µs |
|---|---:|---:|
| Insert unique 1 KiB blob | 497.5–586.2 | 1300.3–1644.7 |
| Read existing 1 KiB blob | 5.4–5.6 | 5.9–31.0 |
| Accept expected head | 579.0–735.0 | 1018.6–1730.6 |
| Reject stale precondition | 345.4–370.5 | 967.4–1070.9 |
| Retry exact accepted request | 7.4–7.4 | 8.8–25.2 |
| Prepare unique anchored context | 831.5–957.5 | 1785.0–2683.7 |
| Prepare existing anchored context | 91.3–96.9 | 155.8–1094.6 |
| Verify historical context | 109.4–148.6 | 400.6–1344.4 |
| Verify current context | 105.0–135.6 | 297.0–1811.0 |

Raw samples remain in [run 1](run-01.json), [run 2](run-02.json), and [run 3](run-03.json). Each output was accepted only after its process succeeded and its correctness fields and release configuration were checked. The fixture and semantic fingerprints agreed across all three processes.

## What this changes

We now have a repeatable observation path rather than an unmeasured claim that the kernel is fast. In this workload, inserting new persisted content costs much more than reading already present small blobs or replaying stored acceptance receipts. First context preparation is also more expensive than preparing already retained context. Those are observations of these paths and settings; this experiment does not isolate whether synchronization, query work, hashing, allocation, checkpointing, or scheduling accounts for the differences.

The measured tails vary substantially between runs, including on read-oriented paths. Preserve that variability rather than selecting the most favorable run. The next unit should measure controlled context-history growth with a fixed byte budget and explicit coverage, so we can see whether selection cost or persistence dominates an actual continuation need. A host/storage comparison or contention study remains separate work.

## Evidence and limits

The coordinator read the complete harness and methodology, then independently ran formatting, strict all-target/all-feature Clippy, the existing 20 scenario tests, and the release build before the three recorded invocations. The implementation agent also checked small sample counts, same-input fingerprint stability, invalid sample rejection, and temporary-database cleanup. Those preliminary smoke observations are not included in the three-run timing table.

The executor reported Linux x86-64, an Intel Xeon Platinum 8573C CPU model, an 8 GiB cgroup memory maximum, and an overlay filesystem for `/tmp`. This is a task executor, not Rana's workstation. Physical backing storage, power-loss behavior, and unrelated host workload were not independently observed. SQLite requested WAL and FULL synchronization; that configuration is not proof of physical persistence behavior.

All operations share one store connection per process. The fixtures are small and fixed in shape. Reads are on previously inserted data without cache flushing. Timed calls exclude compilation, process startup, fixture/setup work, assertions, output, database close and cleanup. Aggregate rates in raw output exclude untimed gaps and are not sustained end-to-end throughput. These results establish no high-load, multi-host, model-quality, Rust-versus-assembly, Git, or Scion comparison.

## Research Delta

- **Owner and source:** coordinating Chat task, with a delegated implementation of two explicitly owned files; source identities in provenance.
- **Contribution:** deterministic native workload, machine-readable timing and correctness output, precise methodology, three observed runs, and a small CI smoke invocation without latency gates.
- **Negative/limiting finding:** variable tails and unisolated storage effects prevent a broad speed or bottleneck claim; no production-capacity conclusion follows.
- **Unresolved effects:** no model or remote work was dispatched by this harness. Git publication and scheduled continuation are separate operations.
- **Next action:** the continuing project owner should select controlled context-history growth, or the next source-review group if the needed execution environment is unavailable. No separate workstation recipient is claimed to have accepted this handoff.
