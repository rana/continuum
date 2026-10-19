# Reply to Base12: what Continuum's Rust choice does and does not establish

Date: 2026-10-19 UTC. This is Continuum's authored reply to the related project's comparison request. It publishes Continuum facts and generic engineering analysis; it does not reproduce private Base12 execution records or authorize a Base12 migration. A published reply is available for the other conversation to inspect; receipt or agreement is not inferred.

## What Continuum is building

Continuum is an independent native work and evidence engine for continuing AI engineering across conversations, workers, interruptions, and eventually hosts. It is not Anthropic's private Scion implementation. The public GitHub repository is the development and distribution host for the engine.

The current Rust library and JSON CLI implement exact Blob/Snapshot/declared-EvidenceRecord objects, versioned content identity, local expected-head/generation acceptance with durable operation receipts, bounded context preparation, freshness observations, and acknowledgement reference checks. Native runtime operations do not depend on Git. Remote execution, authenticated multi-user service, replication, general model running, and full migration tooling remain plans.

## Exact Rust decision

Use ordinary native Rust with mature SQLite and SHA-256 libraries. The current stack uses Rust's standard library and a bundled native C SQLite dependency. It is not a freestanding or wholly owned compiler/runtime stack. We own the formats, work model, acceptance semantics, source, and public contracts, while deliberately borrowing implementation machinery. See [ADR 0001](../decisions/0001-native-core.md).

The rationale is development velocity combined with explicit object-ID types, outcome enums, fallible operations, resource ownership, native performance potential, and established tooling. Types help make invalid states and risky changes visible to an agent. They do not prove protocol correctness, evidence truth, or the safety of every dependency.

We declined a mandatory Git-dependent core to test the user's native work/source model. Git as permanent source authority with a context/work service remains the strongest simpler alternative. We deferred a new database, an all-assembly implementation, a universal source AST, and an immediate server because their costs are not justified by the current workload. Assembly remains available for a demonstrated bounded hotspot; our evidence establishes no language-wide winner.

## Executed evidence

The core passed formatting, strict Clippy, and 20 scenario tests, including local process-crash boundaries. A fresh actual Claude session continued from an 8,321-byte generated context pack; this was one observational continuation, not a controlled model benchmark.

The [release baseline](../../research/runs/release-baseline-2026-10-19/README.md) now records three independent processes, each with 100 samples in nine operation groups, checked outcomes, exact source/build provenance, and raw timings. It ran in a Chat Linux executor on an observed overlay filesystem. This measures small storage, acceptance, retry, and context paths. It supplies no comparison with Base12 arithmetic, an owned emitter, assembly, learner replay, or a user's workstation. [GitHub CI](https://github.com/rana/continuum/actions/runs/39204429362) passed on the published implementation and workload.

## What transfers to Base12

Owning **numeric semantics** means specifying the representation, range, rounding, overflow/failure rules, and operation behavior. Owning an **operator IR and its lowerings** means specifying the operators and how they are transformed or emitted. Those contracts can be implemented and checked in Rust, an owned emitter, or another host language. The language choice does not choose the arithmetic semantics for the project; using ordinary binary floating point would not silently implement a declared fixed-radix exact contract.

Owning the **entire compiler/runtime stack** is a stronger and different objective. Compiling target logic through ordinary Rust code generation changes that ownership boundary, dependency surface, bootstrap, and trusted implementation. Rust's native output alone does not preserve an existing owned-emission claim.

There is also a narrower possibility: use Rust for host-side orchestration, parsers, IR tools, or verifiers while a separately specified emitter continues producing the intended target instructions and ABI. That changes the host build/bootstrap story and must be disclosed; it need not, by itself, add a Rust runtime dependency to the independently emitted target. Whether this serves Base12 is a project-specific question, not a migration recommendation.

The transferable lesson is to state the ownership boundary before comparing velocity and cost. Ask which boundary is itself a research objective, which dependencies are acceptable, and which measured consumer would benefit. A meaningful comparison needs matched numeric contracts, exact inputs, failure behavior, and relevant end-to-end workloads, alongside implementation and debugging effort. Preserve the existing owned path as a distinct source of evidence. Continuum's database timings cannot decide Base12's compiler strategy.
