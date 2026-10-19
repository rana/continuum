# Continuum

**A native work and evidence engine for continuing AI engineering.**

Continuum explores how work can survive changes of conversation, model, worker, and workstation. Its durable unit is a continuing investigation: exact artifacts, questions, attempts, observations, decisions, and accountable acceptance.

This is an early MIT-licensed research implementation. The working name is provisional. It is an independent design, not an implementation of Anthropic's private Scion and not a claim to know Scion's internals.

## Working implementation

The Rust prototype stores exact-byte blobs, source snapshots, and declared evidence records in a content-addressed store. A local SQLite transaction moves an acceptance head only if the expected head and generation still match, and records a durable operation receipt atomically with that outcome. An exact retry returns that receipt.

It also prepares a bounded context pack from an exact work-state record: objective, attempts, decisions, uncertainties, and an offered handoff. A new process can reconstruct and verify the exact selection, distinguish intact historical context from current accepted state, and record a recipient acknowledgement whose references are checked explicitly.

The prototype establishes storage and retry mechanics. It does not yet authenticate acceptors, establish evidence truth, execute protocols or models, sandbox workers, synchronize hosts, or implement a production repository server. See [current status](CURRENT.md) for the verified boundary.

## Try it

Use a current stable Rust toolchain and a C compiler for bundled SQLite:

```sh
cargo test --locked --all-features
cargo run --locked -- demo /tmp/continuum-demo.sqlite
```

The context example uses several separately started CLI processes. It preserves two histories with the same source but different declared dispatch states, then moves an accepted head and checks that the old pack remains intact while reporting staleness:

```sh
cargo build --locked
python3 examples/context_handoff.py --binary target/debug/continuum --output /tmp/continuum-context-example
```

Use a fresh output directory. This is a reproducible correctness example, not a model-performance or throughput benchmark. The [context contract](docs/architecture/context-handoff-v1.md) states its limits.

Use a fresh local database path for a fresh demo. The CLI help describes individual operations. SQLite WAL databases belong on a local filesystem; multi-host replication is a future protocol, not a shared database file on a network mount.

## Read the design

Start with [Understanding Continuum](docs/orientation.md) for the vision, information architecture, and source-derived choices. Use the [complete Codex handoff](CODEX_HANDOFF.md) to begin an implementation task.

| Question | Authoritative home |
|---|---|
| Why build this? | [Mission](MISSION.md) |
| What works now, and what comes next? | [Current status](CURRENT.md), [roadmap](ROADMAP.md) |
| What is the native architecture? | [Architecture](docs/architecture/overview.md), [object format](docs/architecture/object-format-v1.md) |
| How do missions, directives, and work streams relate? | [Coordination](docs/architecture/coordination.md) |
| How do models, contexts, and reruns work? | [Execution and context](docs/architecture/execution-and-context.md) |
| What does the implemented context path guarantee? | [Context and handoff v1](docs/architecture/context-handoff-v1.md) |
| How do releases and high-load operation work? | [Publication and capacity](docs/architecture/publication-and-capacity.md) |
| How are protocols selected and adapted? | [Protocol design](docs/architecture/protocols.md), [registry](protocols/registry.json) |
| What did Base12 and Prime Radiant teach us? | [Research lessons and coverage](docs/research-lessons.md) |
| Why these initial choices? | [Native core decision](docs/decisions/0001-native-core.md) |
| Which existing systems inform this work? | [Current landscape](docs/landscape.md), [borrowed ideas](docs/borrowed-ideas.md) |
| Where are the original briefs? | [Faithful Markdown conversions](docs/history/README.md) |
| What did Claude contribute? | [Collaboration record](docs/collaboration/README.md) |
| How should agents contribute? | [Project instructions](AGENTS.md) |
| How do research Chat and Codex continue together? | [Continuing work and startup prompt](docs/operations/continuation.md) |

## Design principles

- Preserve exact source bytes and immutable evidence; treat summaries as views.
- Separate proposals from acceptance, and acceptance from external activation.
- Preserve disagreement and unknowns; model agreement is not independent validation.
- Make context, declared assumptions, and known omissions inspectable.
- Give every externally consequential attempt a stable identity and a recovery path.
- Use native implementation where it serves measured workloads, with portable documented formats.
- Add adapters around the core. Keep the core independent of a model vendor and of Git.
- Borrow strong ideas from existing systems and credit them; test the claims that motivate new machinery.

## License and provenance

New project code and original project documentation are available under the [MIT License](LICENSE). Dependencies retain their own licenses. Historical briefs and collaborator transcripts document the design process; they do not turn cited third-party material into MIT-licensed code. No private upstream repository is copied into this project.
