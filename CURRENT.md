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
- Two actual Claude Opus 5.5 design exchanges, with supplied inputs, visible responses, metadata, adopted proposals, and retained corrections.
- Current architecture, native-core decision, research experiment, and phased roadmap.

## Validation

The final Rust code passes formatting, strict Clippy, and 11 scenario tests: nine invariants and two child-process recovery cases. Recovery was checked immediately before commit and after commit before acknowledgement.

The checks establish the specified local process-failure behavior. They do not establish physical power-loss durability, authenticated multi-user operation, semantic evidence truth, replication correctness, or comparative high-load performance.

The CLI demo demonstrates one accepted competing candidate, one stale rejected candidate, and an exact retry returning its historical receipt after the current head moves.

See [verification record](research/runs/foundation-verification.json) for commands and artifact identities.

## Repository review coverage

Base12's full pinned tree has 5,593 files / 180,332,790 bytes. The review acquired 477 exact files and completed semantic reading of 88 distinct files (876,422 bytes), with 35 additional byte-identical alias paths. It distinguishes full inventory, programmatic inspection, and actual semantic reading. It is not a claim to have semantically read every file.

Prime Radiant's live checkout was not discovered through available repository access. The current retained research kit was reviewed instead: 193 files / 8,984,055 uncompressed bytes, with complete archive identity verification and detailed source/document reading. Historical dialogues and bulk generated numerical results have separate coverage limits.

The precise source scope and transferable findings live in [research lessons](docs/research-lessons.md). No upstream code was executed or imported into this public project.

## Publication status

A local read-write Git repository is initialized. Public GitHub publication is pending GitHub sign-in for repository creation. The connected GitHub account exposes read/write on accessible existing repositories, but the connector does not create repositories. The browser reached GitHub's sign-in page. No remote Continuum repository has been created or claimed as published.

## Next useful unit

Complete repository publication once the authenticated creation surface is available. Then implement the smallest context-and-handoff path for two separately started sessions, using a distinction-pair experiment to check that unresolved operations and important uncertainty survive context preparation.

Before adding a remote executor or model runner, specify durable dispatch and uncertain-outcome reconciliation. Add resource measurements before a fleet scheduler.
