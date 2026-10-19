# Existing systems and the independent opportunity

Reviewed against primary project material on 2026-10-19 UTC. These are source-based assessments, not installation, benchmark, security, or production qualification. The faithful historical briefs retain their original dated descriptions.

## Source-control systems

| System | Useful existing work | Limitation relevant to this project |
|---|---|---|
| [Anthropic Scion](https://www.anthropic.com/engineering/redesigning-source-control) | Changesets, sparse object access, server queries, and reusable derived data for a very large monorepo | Its authors describe an internal, highly specialized system and explicitly caution against general replacement of Git. Always-online clients are an assumption to evaluate, not an intrinsic property of AI. |
| [gitai / Graft](https://github.com/feder-cr/git-ai) | MIT, Gitaly-derived source service with sparse operations, changeset log, compare-and-swap landing, and provider-neutral extension protocols | The README describes a first public 0.1.0 release and changing interfaces; pack garbage collection remains a stated gap. It retains Git plumbing. A strong integration/comparison candidate. |
| [CarterT27/scion](https://github.com/CarterT27/scion) | Independent Rust implementation with documented benchmarks and explicit measurement conditions | Its own durable local-storage comparison shows Git faster on several checkout workloads. Synthetic in-memory-server measurements exclude costs that disk-backed Git pays. No blanket speed conclusion follows. |
| [OpenScion](https://github.com/tinyhumansai/openscion/blob/main/ROADMAP.md) | Compact core design with objects, changesets, in-memory log, compare-and-swap refs, sparse import/commit/clone | The reviewed roadmap places queries and landing next, with persistent stores and access control later. Treat the checked roadmap as scope, not a promised complete service. |
| [Jujutsu](https://docs.jj-vcs.dev/latest/operation-log/) | Operation snapshots, undo/restore, and divergent concurrent operations | An excellent comparator for recovering source-control work. Continuum still needs its own explicit definitions for objectives, external effects, context scope, and evidence. This is our scope assessment, not a claim that Jujutsu is deficient at its mission. |
| [Unison](https://www.unison-lang.org/docs/the-big-idea/) | Content-addressed syntax definitions; names separate from identity; dependencies linked by hash | The strong semantic guarantees belong to its language and managed codebase. Arbitrary Rust, assembly, generated files, network effects, and experimental observations do not acquire those guarantees just by being hashed. |

Scion makes an especially useful distinction between immutable recorded changes and derived indexes. Continuum can similarly preserve exact artifacts while allowing context selectors, queries, and indexes to evolve. The accepted record and the current best way of interpreting it should have separate identities.

## Adjacent systems worth composing

| Concept or project | What it contributes | Our boundary |
|---|---|---|
| [GoogleCloudPlatform Scion](https://github.com/GoogleCloudPlatform/scion) | An unrelated orchestration project: agent harnesses, roles, communication, shared or isolated workspaces, local/hosted execution, and versioned skills | Potential execution adapter or comparison environment. Its README calls it pre-1.0 and not an officially supported Google product. It does not establish our evidence semantics. |
| [Bazel remote caching](https://bazel.build/remote/caching) | Content-addressed outputs and action-result reuse | A result's applicability depends on the action's actual input and environment contract. |
| [Temporal](https://docs.temporal.io/workflow-definition) | Durable workflow history and controlled replay | Reconstructing an orchestration history is different from safely repeating an arbitrary external action. |
| [IPLD](https://ipld.io/docs/data-model/) | A data model that separates content links from concrete codecs | Useful for future exchange; our initial codec is not an IPLD implementation. |
| [MCP](https://modelcontextprotocol.io/specification/2026-07-28) | A common interface through which hosts can expose tools and context | Connectivity does not define acceptance, provenance, or retention. |

## What would justify Continuum?

Our proposed contribution is a portable continuing-work contract: exact artifacts, explicit attempts and uncertainty, recoverable acceptance, context with stated coverage, and a handoff that another session can inspect. This can be useful independently of whether source transfer is slow.

The project should demonstrate benefit against a well-configured existing workflow. Measure correct continuation, avoided duplicated effects, orientation time, and useful completed work. A smaller checkout or a faster hash only matters when it improves the relevant workload without weakening the contract.

Adopt or integrate existing tools when they serve that mission. Keep the native experiment focused on semantics and measured bottlenecks that the chosen comparator does not already handle adequately.
