# Disposable project checkpoints

`tools/project_checkpoint.py` adapts a committed Git tree to the existing native CLI. It retains source bytes, the exact authored WorkState input and explicitly bound state, context rendering and coverage, acceptance/verification inputs and outputs, and caller-supplied build provenance. It uses a new disposable store on every run. Git remains outside the Rust core.

Build the CLI with `cargo build --locked`. Author a `continuum.work_state.v1` JSON record with `source_snapshot: null`; the adapter replaces only that field with the captured snapshot identity. Existing attempt references must already identify objects present in the new store; this first adapter does not import prior stores or their objects. Empty attempts are appropriate when no recoverable attempt is being asserted. Keep operation history in its actual evidence home rather than inventing attempts.

Supply a build-provenance JSON document with `binary_sha256` and useful declarations such as source revision, exact build command, toolchain, and retained build log. The digest is checked against the selected binary; the adapter does not verify that the declared build produced it. The captured project revision may differ from the tool's build revision. Record both explicitly.

```sh
python3 tools/project_checkpoint.py \
  --repository /path/to/project --revision HEAD \
  --binary /path/to/continuum \
  --work-state /path/to/authored-work-state.json \
  --build-provenance /path/to/build-provenance.json \
  --output /path/to/new-checkpoint --max-bytes 32768
```

The revision resolves once to a commit. Only committed regular files are captured, even when the working tree is dirty. Untracked and ignored files are excluded. Non-UTF-8 or unsupported paths, symlinks and submodules are rejected. Git executable modes are retained in the inventory but Snapshot v1 does not encode them. This is restricted content custody, not a complete restorable Git checkout. Source is read as Git blob bytes, avoiding working-tree line-ending filters.

A successful directory contains `checkpoint.json`, `source/`, `source-snapshot.json`, authored/bound WorkStates, build provenance, `context.jsonl`, `coverage.json`, `verification.json`, native input JSONs, a CLI log, and `work.db`. Context coverage concerns authored records; source files are available for retrieval but are not rendered into the pack. The locally anchored head is observed during verification; it says nothing about later upstream changes.

Existing output directories are refused. Failure after initialization leaves diagnostic artifacts and no success manifest; inspect them and use a new output path for a corrected attempt. Preserve the non-database files needed to reconstruct a trial. This adapter does not provide migrations, consistent live backups, an installed worker, or dispatch. Delivering a pack and recording an actual successor response remain separate steps. Do not publish captured private source merely because the adapter can retain it.

Run `python3 -m unittest discover -s tools -p 'test_project_checkpoint.py'` after building the CLI. The integration checks exercise exact binary content despite a dirty working tree, deterministic reconstruction, output refusal, unsupported tree entries, digest binding, and failed budget preparation.
