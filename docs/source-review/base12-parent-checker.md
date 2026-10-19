# Parent checker: actual predicate, dependent verdicts and failure boundaries

Reviewed 2026-10-19 UTC at private Base12 commit `88382e793b65c84fd8e223840c27f6bb8682864a`, tree `5cf96129bdcb0dde075f6f5800ae0c68a95c4b82`. Two texts / 56,899 bytes were fully read: checker source and complete report, including all 332 check entries. Python syntax was parsed without execution; report parsing rejects duplicate keys and nonfinite JSON constants. Exact identities are in the [ledger](base12-coverage-parent-checker.json). All four files declared in the [review provenance](base12-parent-packet-review.md) now match acquired lengths and hashes.

## Research Delta: count the predicate, not imagined experiments

Every saved entry says pass; all 332 names are unique. Both per-member name sets match the 127 paths in the pinned packet tree:

| Entry class | Count | Meaning |
| --- | --- | --- |
| UTF-8 without NUL | 127 | One encoding/content-shape check per member |
| Safe regular member | 127 | One extracted-file type/path/extension check per member |
| Other checks | 78 | Packaging, identities, saved arithmetic, dependent verdicts and indicators |

The earlier 82-check accounting audit is represented by one predicate requiring its saved count, flags and empty failure list. That does not make those 82 checks newly executed independent tests. Other predicates do recompute specified arithmetic from saved inputs. A useful evidence graph preserves both dependencies and additional derivations without counting every transitive assertion as another experiment.

The report's greedy events, singleton ties, initial 554,263-byte total and charged final 542,914-byte total agree with the [separate set-objective replay](base12-training-costs.md). All four arm summaries, eight paired rows and resource summary agree with the acquired saved results/audit. These are comparisons on the same retained cost matrix and receipts, not new waveform costs, decoding or host observations. No upstream checker was executed here and its complete predicate was not rerun.

For Continuum, retain check class, input scope and dependency edges alongside totals. An aggregate pass count is a projection whose meaning depends on those definitions.

## Research Delta: validation order defines an access boundary

The source reads extracted files at line 18 and decodes their bytes at line 21 before the member-shape predicate at line 23. That predicate checks regular-file status, symlink/path properties and allowed extensions after the access has happened. The checker operates on an already materialized tree and accompanies separate ZIP checks; its later member verdict should not be presented as a pre-access safe extractor or containment boundary.

This is source-derived ordering, not an observed unsafe extraction or historical exploit. It identifies the assumption needed when reusing the checker. Continuum adapters likewise need to distinguish checks that prevent access from checks that validate already acquired evidence.

JSON parsing explicitly rejects duplicate keys and nonfinite constants, and Python files are syntax-parsed. These operations can raise before the final report write. The checker accumulates Boolean failures into a `BLOCK` verdict only if execution reaches report construction; read/decode/parse exceptions can end without a completed verdict. Missing output, explicit validation failure and successful output are different observations. The report is written with ordinary `write_text` at line 118, so no durable retry/publication protocol is established by this research helper.

## Indicators, exposure and remaining inputs

The source's final privacy-related entries check credential patterns across text and exclude raw/reversible/archive/executable filename extensions. Those are supplementary indicators. The parent prose review describes broader manual inspection of content and constants; its full judgment is not reproduced merely by rerunning these two entries. This unit performs no new recursive privacy audit.

The checker also consumes manifest, allowlist and the complete extracted packet. Manifest and allowlist payloads remain unacquired here, and current complete custody/semantic reading of all 127 packet inputs is not claimed. The report declares a manifest digest; a declared digest is not the missing manifest bytes. All four review artifacts now bind, which closes their provenance-payload gap without closing every checker dependency or authenticating historical execution.

The [validation record](../../research/runs/base12-parent-checker/validation.json) records the actual taxonomy, name-set comparison, scoped saved-value matches, source-line anchors and missing inputs. No packaged source, model, worker, transport or numerical program ran.

Cumulative semantic reading reaches **347 distinct blobs / 2,462,569 bytes**, plus **52 byte-identical alias paths**: 399 covered paths. **5,194 paths / 4,082 distinct blobs** remain without full semantic-reading claims. Earlier empty-stream custody stays mechanical. The historical global acquisition aggregate remains unchanged because its full overlap index is unavailable. No private raw source, report entries, operational identifier or signal payload is published. Hosted CI checks public repository behavior, not private reading or historical execution.

Next bounded unit: packet builder, metadata preparer and verifier sources, three texts / 18,148 bytes. Inspect the packaging/materialization boundary and exact member-policy checks without executing them. Reconcile main and ownership first; no recipient has accepted it. Owned-storage and dispatch-reconciliation work remain separate.
