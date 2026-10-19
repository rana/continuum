# Same owned CLI workload on the checkout filesystem

One completed repeat on 2026-10-19 retained **369 fresh-process timings across nine disposable stores**, using the exact release binary and probe from the [earlier tmpfs run](../cli-cost/README.md). `findmnt` reported **ext4** for the selected checkout location; `stat -f` reported **ext2/ext3**. This is a non-tmpfs filesystem observation in this mount namespace, not identification or qualification of a physical device or its persistence guarantees.

Every exact returned response, initial journal cut/hash, complete object/history count and separately observed sync-role sequence matches the earlier workload. The timing samples differ and remain separate. No source storage implementation, synchronization barrier, historical result, model invocation, retained data or deployment changed.

## Protocol and custody

[PLAN.md](PLAN.md) was written before measurement. An outer Python `TemporaryDirectory` selected a newly created disposable directory on the checkout filesystem; only the child probe's `TMPDIR` changed. The unchanged `../cli-cost/check.py` then selected its own nested disposable directory normally. Both temporary directories were removed after successful completion. No mount options, devices, cache controls or unrelated files were changed.

The release executable's SHA-256 remained `4a08fa52fd907e165cf8c3ee5a0596d7d780feb750b9c67f350c5a50cf9fe75c` (990,720 bytes). Storage source is `8bc0fc1578fb915f10fedd22ee016bf9c4e9b2df`; the measured probe is pinned at `e03cca27bb81c4dd018f22a3ff1cea5dfa43f617`. Compiler/runtime/kernel fields and the probe's source manifest match the earlier observation exactly. The `base_commit` inside the unchanged probe remains its original base identity; it does not claim that the later measurement occurred before the earlier publication.

[result.json](result.json) retains all actual child stdout/stderr, individual wall times, summaries, binary/source identities and cell checks. [selection.json](selection.json) binds both exact result files and the separate filesystem-type observation without private mount paths. Timing includes launch, output capture, complete open/recovery, sync calls and serialization; input JSON preparation is excluded. Separate interposed sync samples are excluded from those timing distributions and inject no failures. The nine independent semantic-reader checks include both distinct stale outcomes from the timed and instrumented append phases.

## Observations

Full subprocess median milliseconds. Each non-appending operation has 24 samples per size (eight in each of three new stores); new stale acceptance has three. Raw ranges and samples remain available. The earlier tmpfs distribution is separately documented and not pooled.

| Operation | 1 update | 16 updates | 64 updates |
|---|---:|---:|---:|
| Get latest Blob | 10.906 | 9.041 | 10.906 |
| Head | 4.153 | 2.883 | 5.240 |
| Latest receipt | 3.748 | 2.969 | 5.141 |
| Retry first accepted request | 10.822 | 9.404 | 11.208 |
| Duplicate latest Blob put | 10.419 | 9.400 | 11.597 |
| New stale acceptance | 40.947 | 35.350 | 45.344 |

For context, the earlier tmpfs new-stale medians were 1.170 / 2.009 / 2.957 ms. These are sequential observations at different times, **not a randomized causal filesystem comparison**. Active host load, scheduling, cache state, process/output overhead and device stack were not controlled. Even within this run, the 16-update median can be lower than the one-update median. Do not fit a monotonic scaling law or attribute all difference to fsync or replay.

Non-appending commands still observed four successful libc fsync calls; new stale acceptance observed ten. Both records have identical 1,557 / 30,577 / 127,340-byte initial journals and byte-identical non-timing response/cell records. Exact first-request retries preserve the historical sequence-1 receipt after head movement. Successful calls establish their observed return/order, not actual persistence through power loss or recovery after kernel writeback errors.

## Research Delta

The first probe's tmpfs substrate did not answer the persistent-filesystem cost question. Selecting the checkout filesystem without changing workload or executable gives a second properly labeled observation: the new-stale medians are substantially higher here, while the semantic and sync-call boundaries remain identical. That is enough to justify isolating cost phases, not choosing a barrier-removal optimization.

Next bounded unit: measure recovery/open and already-open operations separately in a disposable in-process probe. Preserve the four startup barriers and pre-write fence, and account for the lifetime exclusive lock when interpreting any amortization benefit. That can distinguish reusable validated state from repeated fresh-process work without promising concurrent-reader availability. Physical durability, retained-data adoption and independent version-2 protocol review remain open. No model request was made or repeated in this unit.

## Offline verification and reproduction

From repository root:

```sh
python3 research/owned-authority/cli-cost-persistent/verify.py
```

This checks both raw result sets through the independent object/receipt verifier, confirms the same executable/source/workload and compares all non-timing sample fields and all nine complete cell records. It performs no storage or timing run. CI adds this offline comparison only, with no speed threshold.

To reproduce the actual selection, run the unchanged `research/owned-authority/cli-cost/check.py` with `TMPDIR` set to a **new disposable parent on the selected filesystem**, the same release CLI and a new output filename. Inspect the recorded filesystem before interpreting the timings. Do not overwrite either retained result or silently combine a new result with these distributions.
