# Continuum

**A native work and evidence engine for continuing AI engineering.**

Continuum explores how work can survive changes of conversation, model, worker, and workstation. Its durable unit is a continuing investigation: exact artifacts, questions, attempts, observations, decisions, and accountable acceptance.

This is an early MIT-licensed research implementation. The working name is provisional. It is an independent design, not an implementation of Anthropic's private Scion and not a claim to know Scion's internals.

## Working foundation

The Rust prototype stores exact-byte blobs, source snapshots, and declared evidence records in a content-addressed store. A local SQLite transaction moves an acceptance head only if the expected head and generation still match, and records a durable operation receipt atomically with that outcome. An exact retry returns that receipt.

The prototype establishes storage and retry mechanics. It does not yet authenticate acceptors, establish evidence truth, execute protocols or models, sandbox workers, synchronize hosts, or implement a production repository server. See [current status](CURRENT.md) for the verified boundary.

## Try it

Use a current stable Rust toolchain and a C compiler for bundled SQLite:

```sh
cargo test --locked --all-features
cargo run --locked -- demo /tmp/continuum-demo.sqlite
```

Use a fresh local database path for a fresh demo. The CLI help describes individual operations. SQLite WAL databases belong on a local filesystem; multi-host replication is a future protocol, not a shared database file on a network mount.

## Read the design

| Question | Authoritative home |
|---|---|
| Why build this? | [Mission](MISSION.md) |
| What works now, and what comes next? | [Current status](CURRENT.md), [roadmap](ROADMAP.md) |
| What is the native architecture? | [Architecture](docs/architecture/overview.md), [object format](docs/architecture/object-format-v1.md) |
| How do missions, directives, and work streams relate? | [Coordination](docs/architecture/coordination.md) |
| How do models, contexts, and reruns work? | [Execution and context](docs/architecture/execution-and-context.md) |
| How do releases and high-load operation work? | [Publication and capacity](docs/architecture/publication-and-capacity.md) |
| How are protocols selected and adapted? | [Protocol design](docs/architecture/protocols.md), [registry](protocols/registry.json) |
| What did Base12 and Prime Radiant teach us? | [Research lessons and coverage](docs/research-lessons.md) |
| Why these initial choices? | [Native core decision](docs/decisions/0001-native-core.md) |
| Where are the original briefs? | [Faithful Markdown conversions](docs/history/README.md) |
| What did Claude contribute? | [Collaboration record](docs/collaboration/README.md) |
| How should agents contribute? | [Project instructions](AGENTS.md) |

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
