# Disposable project checkpoints

`tools/project_checkpoint.py` adapts a committed Git tree to the existing native CLI. It retains source bytes, the exact authored WorkState input and explicitly bound state, context rendering and coverage, acceptance/verification inputs and outputs, and caller-supplied build provenance. It uses a new disposable store on every run. Git remains outside the Rust core.

Build the CLI with `cargo build --locked`. Author a `continuum.work_state.v1` JSON record with `source_snapshot: null`; the adapter replaces only that field with the captured snapshot identity. For existing attempt references, supply `--import-objects /path/to/bundle.json` as described below. The adapter imports explicit immutable objects into the fresh store; it does not merge stores or rewrite attempt references. Empty attempts are appropriate when no recoverable attempt is being asserted. Keep operation history in its actual evidence home rather than inventing attempts.

Supply a build-provenance JSON document with `binary_sha256` and useful declarations such as source revision, exact build command, toolchain, and retained build log. The selected executable bytes are read once, digest-checked, retained in `runtime/`, and that copy is executed, so replacing the input binary during a build does not change later CLI invocations. The adapter does not verify that the declared build produced it. The captured project revision may differ from the tool's build revision. Record both explicitly.

```sh
python3 tools/project_checkpoint.py \
  --repository /path/to/project --revision HEAD \
  --binary /path/to/continuum \
  --work-state /path/to/authored-work-state.json \
  --build-provenance /path/to/build-provenance.json \
  --output /path/to/new-checkpoint --max-bytes 32768
```

The revision resolves once to a commit. Only committed regular files are captured, even when the working tree is dirty. Untracked and ignored files are excluded. Non-UTF-8 or unsupported paths, symlinks and submodules are rejected. NFC/casefold path aliases (including directory prefixes and file/directory conflicts) are conservatively rejected before store creation; retained source digests are rechecked before success. This policy can reject distinct paths supported by a case-sensitive host and does not implement every filesystem naming rule. Git executable modes are retained in the inventory but Snapshot v1 does not encode them. This is restricted content custody, not a complete restorable Git checkout. Source is read as Git blob bytes, avoiding working-tree line-ending filters.

A successful directory contains `checkpoint.json`, `source/`, `source-snapshot.json`, authored/bound WorkStates, build provenance, `runtime/` with the measured binary, `context.jsonl`, `coverage.json`, `verification.json`, native input JSONs, a CLI log, and `work.db`. Context coverage concerns authored records; source files are available for retrieval but are not rendered into the pack. The locally anchored head is observed during verification; it says nothing about later upstream changes.

Existing output directories are refused. Failure after initialization leaves diagnostic artifacts and no success manifest; inspect them and use a new output path for a corrected attempt. Preserve the non-database files needed to reconstruct a trial. This adapter does not provide migrations, consistent live backups, an installed worker, or dispatch. Delivering a pack and recording an actual successor response remain separate steps. Do not publish captured private source merely because the adapter can retain it.

Run `python3 -m unittest discover -s tools -p 'test_project_checkpoint.py'` after building the CLI. The integration checks exercise exact binary content despite a dirty working tree, deterministic reconstruction, output refusal, unsupported tree entries, digest binding, failed budget preparation, imported historical attempts, order-independent reconstruction, source overlap, malformed/oversized bundles, identity mismatch, incomplete/extra closure and acknowledgement-as-receipt rejection.

## Importing recorded attempt objects

The optional `--import-objects FILE` accepts one explicitly bounded auxiliary-history bundle:

```json
{
  "schema": "continuum.object_bundle.v1",
  "objects": [
    {"id": "sha256:...", "format_version": 1, "object": {"type": "blob", "bytes": [1, 2, 3]}}
  ]
}
```

The ellipsis is a placeholder: use exact envelopes returned by `continuum get DB OBJECT_ID`. Only version-1 Blob and Snapshot objects are supported. Each expected identity must be unique and use the native lowercase SHA-256 syntax. Object/envelope keys are explicit. `format_version` must be the integer `1`, not a boolean, float or string. All authored JSON inputs reject duplicate keys and nonfinite numbers. The import file is read with a 16 MiB bound and admits at most 256 objects. These are initial adapter limits for small auxiliary histories, not native store or source-tree capacities; revisit them with a measured need.

Start from each authored attempt's `source_snapshot`, `request` and optional `receipt`. Supply every required object not already captured from current source, including every Blob referenced by an imported Snapshot. The adapter rejects missing closure and any supplied object outside those reachable references. Supplied objects that overlap current source are allowed, revalidated and explicitly inventoried. Native context preparation still checks reference kinds and rejects handoff acknowledgements used as attempt receipts.

Input order does not matter: Snapshot v1 refers only to Blobs, so the adapter imports Blobs before Snapshots. Every `put` goes through the native CLI, and its returned identity must match the envelope's expected identity before work-state acceptance proceeds. The adapter does not implement a second hashing format. Identity mismatch or any later failure leaves no successful `checkpoint.json`. Partial diagnostic stores may remain; never reuse that output for a retry. Use a new disposable directory.

The original bundle bytes are retained as `import-objects.json`; `imports/` holds the native object inputs. `checkpoint.json` inventories imported IDs/kinds, source overlap, bundle digest and bounds. Existing attempt references are preserved exactly. Hash/custody verification does not bind a request semantically to its receipt or prove dispatch, actor identity, outcome truth or another effect. A reconstructed historical attempt must be labeled as authored reconstruction, with exact source-file bytes checked separately where available.

The [recorded CSV attempt example](../../research/runs/checkpoint-object-import/README.md) rebuilds two disposable stores from the earlier real handoff's retained visible request/response. It performs no inference. Run its `reproduce.py` with an explicit binary, matching build-provenance file and new output directory; its assertions check historical/current source separation, every imported envelope, raw request/response digests and identical pack identity after reconstruction.
