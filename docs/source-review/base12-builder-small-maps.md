# Small binary map metadata

This Research Delta fully reads twelve files under `research/owned-stack/2026-10-16/native-builder-slice/preparation-01/fixtures/expected/`: maps05/09/13/31/32/33/35/37/39/41/43/45. They total 5,248 path bytes at Base12 commit `88382e793b65c84fd8e223840c27f6bb8682864a`, tree `5cf96129bdcb0dde075f6f5800ae0c68a95c4b82`. This chat owns the read-only contribution based on Continuum main `86722fc449a9ce229b934b77d73301dd4d34a451`. The [ledger](base12-coverage-builder-small-maps.json) pins each new blob and repeated path; the [validation record](../../research/runs/base12-builder-small-maps/validation.json) retains every executed join and the unchanged reader identity.

## Complete acquired-field reading

All headers and all 152 records were read through complete decoded projections. The existing [bounded reader](../../research/runs/base12-builder-map-metadata/map_metadata.py) decodes each little-endian field, and re-encoding the resulting values reproduces every acquired byte. Every record agrees with its fully reviewed expected layout on kind, physical source line, file offset and encoded length. Version, code length, record count, instruction/label counts, checksum-list identity, frozen map declaration and saved result metadata all agree.

The twelve paths contain **six distinct blobs / 4,672 bytes** and **six exact repeated payload reads**. New semantic coverage counts each distinct blob once. The repeated paths remain separately identified so their source conditions and case names survive deduplication. No private map payload is published.

## Map equality and code equality differ

The acquired map bytes now directly substantiate equivalence groups previously predicted from source and layouts:

| Cases with identical map bytes | Map bytes | Distinct code digests |
| --- | ---: | ---: |
| 05/32 | 96 | 1 |
| 31/33/35 | 96 | 3 |
| 37/39 | 96 | 2 |
| 41/43/45 | 96 | 3 |

The last three groups share source-position structure and instruction lengths while retaining different instruction contents. Their map identity cannot stand in for code identity, even after the map itself is acquired and its complete structure verified. The reader cannot recover code bytes that the representation does not contain.

Conversely, cases05/09/13/32 share one code identity while their maps retain different label and source-line structure. Map09 contains 128 zero-length label records at the same code offset and one instruction record on line 129. Map13 adds its own second label record, whereas maps05/32 have only the entry label and one instruction. The binary records preserve these differences directly.

Maps05/32 are completely identical despite distinct source conditions: one source reaches the input byte ceiling through a long comment, while the other omits its final LF. Identical result metadata does not erase why the two fixtures exist.

## Scope and remaining exceptional outputs

The existing reader is unchanged. Its eight synthetic test methods already exercise structural endpoints and malformed data; this unit contributes acquired-data observations rather than another test that merely restates the implementation. Hosted CI continues to run those synthetic checks without private payload access.

Six expected-map paths remain outside full reading/identical-blob coverage: the runner and two capacity maps, a 25-byte sentinel, and two empty files. The sentinel and empty files belong to failure-path output expectations. They must retain their own classification rather than being coerced into valid map records or used to grant semantic credit to every identical empty blob in the repository. Their exact content and case relations are the next bounded review.

The transferable lesson is to keep content deduplication and semantic interpretation on different axes. Acquired identical maps strengthen a specific map-identity claim. They neither identify the absent instruction bytes nor merge the source and runtime contexts in which those bytes are expected.

No native ELF/code artifact was acquired, upstream module imported, materializer/candidate executed, native artifact emitted, model consulted, live process scanned, workstation activated or upstream recipient acceptance obtained. These are acquired expected metadata files, not a new native execution result.

Semantic reading reaches **604 distinct blobs / 5,252,315 bytes**, plus **112 identical alias paths**. **4,877 paths / 3,825 distinct blobs** still lack full semantic-reading credit. Whole-repository reading and historical global acquisition overlap remain incomplete.

Next: read the six remaining expected-map paths01/07/11/50/57/60, totaling 61,785 path bytes, and distinguish valid records, sentinel content and mechanical empty-file custody. Reconcile fresh main and ownership first; owned-storage, dispatch and public checkpoint lanes remain separate. No recipient has accepted that next unit.
