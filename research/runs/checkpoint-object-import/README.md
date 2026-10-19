# Importing a real recorded attempt into a fresh checkpoint

## Research Delta

Question: can the smallest explicit object import preserve an actual prior attempt's exact request, visible response and historical source in a fresh checkpoint store? This was selected from the concrete limitation in both [earlier](../project-checkpoint-pilot-1/README.md) and [independent CSV](../independent-csv-pilot/README.md) pilot work. Input main: `6f2a11465bc610276495de636c85071e2424d1c9`; first implementation/experiment source: `06f8a18b24cd02ea30d8f7f2666e1e91e942e08c`. The active Codex coordinator owns implementation and integration. This unit was started by the one-minute local heartbeat at 2026-10-19 06:06:01.672 UTC (2026-10-18 23:06 Pacific), rather than a new manual prompt.

## Implemented mechanism

The checkpoint adapter now accepts an optional bounded `continuum.object_bundle.v1` containing exact native `get` envelopes. It admits only version-1 Blob/Snapshot objects; expected IDs are unique and syntax-checked. The file is read with a 16 MiB bound and a 256-object limit, deliberately scoped to small auxiliary histories. JSON rejects duplicate keys and nonfinite values. These adapter limits are not claims about native capacity or optimum sizing.

Starting from the authored attempts' source/request/receipt references, the adapter walks Snapshot-to-Blob dependencies against the supplied bundle and already-captured source. Missing closure and unrelated supplied objects fail. Source overlap is allowed, explicitly recorded and verified. Blobs import before Snapshots, independent of input order; native `put` validates content, paths/dependencies and canonical identity, and the adapter checks each returned ID against the expected ID. Historical references are never rewritten. Native context checks retain kind/acknowledgement restrictions. No Rust object/context format or acceptance transaction changed.

The original import bytes, native object inputs and command results are retained in each actual checkpoint directory. The checkpoint manifest inventories IDs/kinds, source overlap, bundle digest and bounds. Any failure leaves no successful manifest. Existing diagnostic-store behavior is retained: a failed disposable directory may remain, and retries require a fresh directory. This is neither atomic whole-bundle ingestion into a retained store nor a store migration/merge API.

## Actual evidence

[reproduce.py](reproduce.py) loads the independent CSV baseline's four source Blobs and Snapshot plus the exact retained implementation-call request and visible response. These **seven objects** reconstruct a real earlier turn; no inference, dispatch or model re-query occurs. Its operation identifier and receipt-recorded state are explicitly authored retrospectively, not recovered provider identifiers. The request/receipt are exact local visible projections, not provider wire bytes and not an authenticated request-response binding.

The [result](result.json) establishes:

- All imported native envelopes were retrieved unchanged from both fresh stores.
- Request and receipt Blob bytes match SHA-256 of the exact original public pilot files. The original files remain authoritative; they were not reserialized into new alleged historical inputs.
- The attempt preserves the baseline source Snapshot while the checkpoint points at the later CSV implementation source. The roots are different and remain explicit.
- Both fresh stores produce identical context-pack identities and pass native historical/current-anchor verification.
- The rendered conditional next action is `inspect_recorded_receipt`, with the source's authored scope intact. No new request was sent.

The [authored WorkState](authored-work-state.json), [exact import bundle](import-objects.json), [first checkpoint](first/) and [reconstructed checkpoint](reconstructed/) retain the inputs, rendering, coverage, native verification and command logs. The raw seed/get log is losslessly compressed in `native-seed-log.jsonl.gz`; its decompressed SHA-256 is `b7c8248e6e5731cb0a3dff95e7d047725edac6934988e0be0dbe2a5e66f2f376`. Build provenance identifies the reused, already-measured CSV-pilot binary; no rebuild is claimed for that run. Runtime copies and disposable databases are excluded from public commits. Duplicated source files, import bundle copies and per-object put-input files are omitted from this public run projection: the native source bytes and exact bundle contents remain fully retained in the earlier pilot and this bundle. The local actual checkpoint directories retain those outputs.

[adapter-tests.log](adapter-tests.log) records 11 integration tests. New cases exercise historical-source custody, exact binary request/receipt bytes, shuffled-order reconstruction, explicitly recorded source overlap, missing direct references and Snapshot leaves, unrelated extra objects, mislabeled content, ambiguous JSON, duplicate IDs, booleans/floats/strings/unsupported format versions, unsupported object kinds, byte/object limits, and native rejection of an imported acknowledgement as an attempt receipt. Rejected cases produce no success manifest; preflight errors produce no output directory. Existing six adapter cases remain. [validation.json](validation.json) retains formatting, strict all-feature Clippy, all 20 Rust scenario tests and all 11 adapter checks in this desktop shell. Hosted CI additionally exercises the real-record reconstruction with an explicitly identified current binary.

## Consultation and decisions

The actual [Claude request](claude-request.json) supplied the proposed mechanism and relevant native behavior, not the full implementation or prior conversation. The [visible reply and returned metadata](claude-response.json) reported `claude-opus-5-5`, medium effort, adaptive thinking, completed `end_turn`, no truncation. It prompted closure rejection and exact historical-file comparisons. The coordinator adopted those concrete checks, while allowing verified overlap with current source. The recommendation to discard failed stores was rejected in favor of the adapter's existing diagnostic-retention contract and mandatory fresh retries. Agreement is not empirical evidence; the executed failure and reconstruction tests support only the specified behavior.

Rejected approach: deriving alleged build provenance merely by changing a digest in an old manifest. The reproducible entry point instead requires an explicit caller-supplied build-provenance file, verifies its digest against copied runtime bytes, and preserves the file unchanged. A rebuilt binary requires new provenance. Rejected scope: automatic scanning of unrelated stores, generic evidence-object import, native format changes, a model runner or a migration engine. None is needed for this observed gap.

## Replay, limits and next action

Build a native CLI or select identified retained bytes and supply corresponding provenance:

```sh
python3 research/runs/checkpoint-object-import/reproduce.py \
  --binary /absolute/path/to/continuum \
  --build-provenance /absolute/path/to/build-provenance.json \
  --output /absolute/path/to/new-run
```

The script uses the retained independent-source Git bundle locally, with no network. Its copied binary must match the supplied digest. It reconstructs both stores and checks the original historical object identities, exact file bytes, source separation and pack equality. Full source-file paths and invocation logs are capture-time observations; choose new output locations. Rebuilding does not reproduce the original binary's provenance merely because native behavior passes.

This is the first observed local scheduled continuation unit; the saved schedule alone was not treated as proof. No cloud-task cancellation, exclusive distributed ownership, persistent installed worker, retained-store upgrade/backup, physical power-loss durability, outcome truth or model-performance benefit is established. The existing hourly cloud responsibility remains outside verified local control; the coordinator found fresh main and no open PR or overlapping remote contribution before starting. Core validation used four Cargo jobs; no new infrastructure, scheduler, spending limit or resource reservation was introduced.

Next useful action: give a real fresh receiver the resulting pack and a bounded way to request exact referenced Blobs, then observe whether recorded attempt history prevents a repeated investigation. The object import mechanism now removes the concrete transport gap; this experiment should test practical use rather than add another record type. No receiver has accepted that new offer. The current local heartbeat retains responsibility for the next active unit, subject to fresh repository/ownership reconciliation.
