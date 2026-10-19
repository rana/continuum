# Current state

Last reconciled: 2026-10-19 UTC (2026-10-18 America/Los_Angeles).

## Selected direction

Continuum is a native work and evidence engine for continuing AI engineering. The first implementation is a small Rust core, with exact source custody and durable local acceptance receipts. Git is the intended public development host and a future interoperability edge; the core has no Git runtime dependency.

## Completed locally

- Both original DOCX briefs converted faithfully to Markdown, including their full historical appendices, five tables, and 37 source hyperlinks. Visible-text round trips match after whitespace normalization.
- Rust library and JSON CLI compiled on Rust 1.99.1.
- Exact-byte Blob, restricted source Snapshot, and untrusted EvidenceRecord objects.
- Domain-separated versioned SHA-256 object IDs.
- Local SQLite expected-root/generation acceptance, operation identity binding, durable retries, and receipt queries.
- Four agent-guided protocols: Progress Brief, Holographic Walk, Research Record, Bounded Research Loop.
- Versioned digest-pinned registry, protocol schemas and fixtures, and a proposed execution-metadata schema.
- Four further actual Claude Opus 5.5 exchanges, with supplied inputs, visible responses, metadata, adopted proposals, and retained corrections. The fourth uses only a generated context pack for a fresh continuation of this project; the original briefs also retain their historical exchanges.
- Exact WorkState records, bounded whole-record context selection, retained rendered packs, historical and current-anchor verification, and explicit handoff acknowledgement-reference checks.
- A reproducible context example using independently started CLI processes.
- One actual fresh Claude continuation from an 8,321-byte pack, with an exact model-authored acknowledgement whose references passed native verification.
- Current architecture, native-core decision, research experiment, and phased roadmap.

## Validation

The current Rust code passes formatting, strict Clippy, and 20 scenario tests: nine context cases, nine invariants, and two child-process recovery cases. Recovery was checked immediately before commit and after commit before acknowledgement. The coordinating agent independently reran these checks after the implementation was frozen.

The checks establish the specified local process-failure behavior. They do not establish physical power-loss durability, authenticated multi-user operation, semantic evidence truth, replication correctness, or comparative high-load performance.

The acceptance demo demonstrates one accepted competing candidate, one stale rejected candidate, and an exact retry returning its historical receipt after the current head moves. The context example preserves different declared dispatch states for the same source, and distinguishes an intact old pack from current accepted state. Acknowledgement checks establish reference consistency, not identity, understanding, or external execution.

See the historical [foundation verification](research/runs/foundation-verification.json), current [context verification](research/runs/context-verification.json), and [example result](research/runs/context-example.json) for commands and artifact identities.

## Repository review coverage

Base12's full pinned tree has 5,593 files / 180,332,790 bytes. The cumulative review acquired 539 exact file paths and completed semantic reading of 161 distinct blobs (1,226,434 bytes), with 46 additional byte-identical alias paths. It distinguishes full inventory, programmatic inspection, and actual semantic reading. The requested whole-repository reading is incomplete; the [extended ledger](docs/source-review/base12-coverage-extended.json) preserves the precise remaining scope.

Prime Radiant's live checkout was not discovered through available repository access. The current retained research kit was reviewed instead: 193 files / 8,984,055 uncompressed bytes, with complete archive identity verification. The latest checkpoint has 86 complete semantic readings, seven separate complete historical source diffs, and two separately classified generated-manifest checks. All eight retained dialogue captures, eight associated receipts, three prose reports, and all 159 source-inventory records were read. The [latest audit](docs/source-review/prime-audits.md) keeps the 98 remaining numerical, visual, and binary files explicit; authored annotations in numerical records are among the gaps.

The precise source scope and transferable findings live in [research lessons](docs/research-lessons.md). No upstream code was executed or imported into this public project.

## Publication status

The original project is published at [rana/continuum](https://github.com/rana/continuum), a public MIT repository. GitHub sign-in completed, and connected read/write operations created the repository and published all 95 prepared files. The first published project commit is `3439f61989d344ff89df1b0cad4ea7fd119918e7`.

All three local development snapshots were imported with identical Git tree identities. The GitHub API assigned new commit metadata and parent links, so the public commit IDs differ from the local research IDs. The [source-commit map](research/publication/source-commit-map.json) records the exact correspondence, including the source used by the fresh Claude continuation. Original local history remains in the recoverable archive and the local `local-research-history` branch. Historical context packs and transcripts retain their original capture-time claims.

The first [GitHub Actions run](https://github.com/rana/continuum/actions/runs/39199405358) completed successfully on that project commit: formatting, strict Clippy, all-feature tests, and the acceptance demo. This confirms those checks on GitHub's hosted runner; it adds no high-load or comparative performance evidence. No packaged release or remotely deployed service is claimed.

## Next useful unit

Continue the next bounded source-review group and define a representative workload for release-build measurements before expanding the storage engine. The [fresh-model trial](research/continuation-trial/README.md) is complete. The full upstream reading request and a controlled model-performance comparison remain open.

Before adding a remote executor or model runner, specify durable dispatch and uncertain-outcome reconciliation. Add resource measurements before a fleet scheduler.
