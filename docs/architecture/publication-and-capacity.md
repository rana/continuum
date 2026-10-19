# Publication, capacity, and performance

Status: design beyond the local prototype.

## Releases as accepted compositions

Work may flow continuously without every intermediate result becoming a release. A release names an immutable composition: source root, selected interfaces and protocol revisions, environment or build description, relevant evidence, known gaps, and compatibility promises for an audience.

A moving channel selects one accepted composition. It does not mean “take the latest independently approved version of every component.” Independently valid components can be invalid together.

Version several things separately:

- Object encoding and hash algorithm identifier.
- Record schema and required semantics.
- Protocol definition.
- Public API compatibility.
- Executor/harness/toolchain environment.
- Product release or human-friendly channel.

Unknown optional annotations can be preserved. Unknown critical semantics must stop the affected operation. Old records retain their original interpretation; migration produces explicit successor identities and verifiable mappings.

## What publishing means

Use explicit operations instead of one overloaded publish switch.

| Operation | Effect |
|---|---|
| Store | Durable possession by one service |
| Replicate | Transfer exact objects to another authorized holder |
| Discover | Make a reference findable by an audience |
| Share | Grant or exercise a visibility scope |
| Accept | A named authority selects a root for its target |
| Activate | An external system begins using the selected composition |

These can happen separately. A research proposal may be shared before acceptance. A release can be accepted privately before public discovery. Deploying an accepted root is an external effect with its own receipt and rollback/compensation conditions.

The first prototype implements local storage and caller-namespaced acceptance only. It does not implement authenticated sharing, replication, public channels, or deployment.

## Capacity has a place

An agent choosing work benefits from knowing whether a suitable executor exists and whether it is currently usable. Begin with observed capabilities and per-attempt measurements; avoid building a fleet scheduler before there is a fleet workload.

Distinguish:

1. Declared hardware or model capability.
2. Recently verified reachability, with observation time and expiry.
3. Reserved capacity with a recipient-issued lease or reservation.
4. Measured utilization and completed execution.
5. Granted budget and permitted workload.

A configured host is not an idle host. A heartbeat is not free GPU memory. A reservation is not completed work. Missing telemetry remains unknown.

A later placement request can specify CPU architecture, memory range, accelerators, storage, network locality, toolchain, data visibility, latency objective, and cost bound. Prefer data locality and necessary capability to maximal activity. An LLM's token budget and a host's RAM are different resources.

## Linux primitives that may help

Linux cgroup v2 offers CPU, memory, and I/O controls and accounting. Use a properly delegated group per attempt where available, and record observed limits. Permission and kernel configuration must be checked; the existence of an API does not mean a worker can use it. Source: [Linux cgroup v2](https://docs.kernel.org/admin-guide/cgroup-v2.html).

Namespaces, process supervision, file descriptor discipline, and sandbox mechanisms belong in an execution adapter, not inside the immutable-object format. Resource limits do not alone make arbitrary code execution safe or make a test hermetic.

Use ordinary filesystem operations, mature database transactions, buffered I/O, and established network libraries first. Consider memory mapping, asynchronous I/O, io_uring, NUMA-aware placement, SIMD, compression, or custom allocation only after profiling a concrete bottleneck.

A native stack does not require rebuilding TCP/IP. The first network service can use existing HTTP, TLS, and Linux sockets. Choose QUIC or a different transport only when its actual properties serve a measured requirement. Keep authenticated object exchange and acceptance semantics above the transport.

## High-load design order

- Keep inference, tests, compression, and large object transfers outside the short serialized acceptance transaction.
- Use immutable shared inputs and stable read snapshots.
- Batch safe metadata operations; set bounded queues and deadlines.
- Apply backpressure before overload turns into unbounded retries.
- Reconcile uncertain operations before creating more work.
- Index actual queries; watch long readers and checkpoint behavior.
- Partition authority by target only where the contract permits it.
- Measure before sharding or replacing storage.

SQLite WAL allows readers and a writer concurrently but has one writer at a time and same-host shared-memory assumptions. It is appropriate for the first local kernel, not evidence of unlimited throughput. Source: [SQLite WAL](https://www.sqlite.org/wal.html).

## Benchmarks that matter

The initial test suite checks semantics, not comparative speed. Future benchmarks should publish workload, hardware, storage, toolchain, dataset, concurrency, failure rate, and distribution of measurements.

Prioritize:

- Time for a fresh session to recover correct task context.
- Duplicate external work and wrong-state acceptance rate.
- Context-pack size, retrieval latency, and omitted decisive evidence.
- Acceptance p50/p95/p99 latency under concurrent attempts.
- Memory amplification and storage growth per retained attempt.
- Recovery after process death and interrupted transmission.
- Useful independently accepted work per unit of time and cost.

Do not infer a hundred-agent throughput gain from an isolated hash benchmark. The important limitation may be shared mutation, evaluator throughput, correlated mistakes, storage contention, or the model service itself.

## Long-term portability

Keep schemas, object fixtures, errors, and protocol contracts openly documented. Add a second independent reader before calling the format durable across implementations. Use explicit migrations for new codecs and digest algorithms, and preserve the old bytes needed to verify history.

A hundred-year ambition is served by interpretable data, export, replaceable services, clear authority, and measured evolution. It cannot be guaranteed by a language choice or by freezing today's model abstractions.

