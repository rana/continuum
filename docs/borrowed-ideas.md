# Prior art to borrow from

The project claims an independent composition of ideas, not invention of content addressing, workflow replay, typed evidence, or agent tools. The historical briefs contain the broader Scion-style landscape and dated assessments.

| Existing concept | Useful lesson | Boundary for Continuum |
|---|---|---|
| Git and Jujutsu | Immutable history, cheap branching, recoverable operations, practical source exchange | Do not make chat transcripts and evidence live only in commit prose |
| IPLD | Separate a data model, content links, codecs, and traversal | Our v1 codec is not currently an IPLD implementation |
| Bazel remote caching / remote execution | Exact action inputs and content-addressed results | A cache hit does not establish that undeclared inputs were captured |
| Temporal | Durable history, deterministic workflow replay, explicit activity boundaries | Replaying orchestration is not repeating external effects safely by itself |
| MCP | A common tool/context interface for host integrations | Tool connectivity does not provide the engine's acceptance or evidence contract |
| SQLite | A tested transaction engine and indexed local records | Standard WAL has one writer and same-host assumptions |
| Linux cgroups | Resource accounting and bounded execution groups | Scheduling, sandboxing, and scientific reproducibility are separate concerns |
| Base12 project methods | Canonical fact ownership, source returns, bounded research, honest progress and handoffs | Preserve actual coverage; do not import historical operational restrictions |
| Prime Radiant research kit | Test representations, observability, interface losses, counterexamples, and model scope | Kit review is not access to the live project; a method's name is not physical evidence |

## Primary references

- [Jujutsu glossary](https://docs.jj-vcs.dev/latest/glossary/)
- [IPLD data model](https://ipld.io/docs/data-model/)
- [Bazel remote caching](https://bazel.build/remote/caching)
- [Remote execution API](https://github.com/bazelbuild/remote-apis)
- [Temporal workflow definitions](https://docs.temporal.io/workflow-definition)
- [MCP specification, 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28)
- [SQLite WAL](https://www.sqlite.org/wal.html)
- [Linux cgroup v2](https://docs.kernel.org/admin-guide/cgroup-v2.html)
- [Source-specific review coverage](research-lessons.md)

Links identify sources to revisit as interfaces evolve. A citation is not an implementation claim or a promise of interoperability.

