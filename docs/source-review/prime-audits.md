# Prime Radiant audits: source encounters, custody, and executable contracts

Review date: October 19, 2026. Status: source-informed design findings. This review adds no runtime behavior, implementation acceptance, or policy authority.

**A useful source handoff preserves who encountered which representation, what they actually inspected, and what remains available to the next worker.** The reviewed records make those distinctions concrete. They also show why an executable handoff needs the numerical representation, admitted domain, dependencies, and rejection behavior alongside its mathematical purpose.

This is a separate continuation of the [historical dialogue review](prime-followup.md). That document remains unchanged. The source is the accessible fourth stored edition of the October 18 Prime Radiant research kit, archive SHA-256 `97a156c3d6618d9f84f1271ec44dc12b056b0fdbfbf4fcf1de950cea691708a8`. It is not a live repository checkout.

## Exactly what was reviewed

The bounded group contains twelve files and 207,202 source bytes:

| Group | Files | Bytes | Actual coverage |
|---|---:|---:|---|
| Authored source audits, preparatory contracts, and source inventory | 9 | 161,243 | All fields and records read, including all 159 source-inventory entries |
| Historical automation receipt | 1 | 4,009 | Complete receipt and supplied prompt read as historical records |
| Native build manifest and kit integrity manifest | 2 | 41,950 | All non-inventory fields read; generated inventories exhaustively checked as bindings, without a complete model-reading claim for every generated entry |

The ten completely read files total 165,252 bytes. No text was skipped through approximate matching. Seven source records occur identically by parsed field/value equality in both an authored audit and the source inventory. Both occurrences were read; they represent a shared source lineage rather than independent corroboration. Their enclosing files retain distinct byte identities.

All twelve scoped files were checked against their recorded hashes and parsed as UTF-8 JSON or JSONL with duplicate object members and nonstandard numeric constants rejected. The source inventory has 159 distinct record IDs. All 49 retained local path/hash bindings, 64 source-ID links, and five audit-note links resolve and match. The kit integrity map's 192 entries cover every other delivered file. The native manifest's 92 entries match the retained native subdirectory apart from the manifest itself. These are internal structural and byte-binding checks, not evidence that the described calculations ran correctly. [A1–A12]

No upstream code, binary, verifier, or simulation was executed. Reading a record that reports a successful run does not make this review another execution or reproduction.

## 1. Preserve the source encounter and its transformations

One provenance record distinguishes a downloaded raw page from its extracted readable text, with separate hashes and an explicit extraction procedure. It states that the written publication differs from an audio-audited transcript. Another record describes reconstructing a numerical table from displayed line ranges after a direct byte-download route failed. Overlapping text agreed and the reconstructed file has a stable local hash; the record explicitly declines to call those bytes the original download. [A1, A3]

These are useful, inspectable forms of recovery. Their limits belong in the handoff. The following concepts should remain distinguishable in Continuum's source and [execution/context records](../architecture/execution-and-context.md):

| Concept | Information needed for continuation |
|---|---|
| Work or subject identity | What intellectual work, source subject, or research question the record concerns |
| Particular representation | Exact retained bytes where available, format, and the edition or content identity being claimed |
| Encounter | Worker, observation time or causal receipt, retrieval route, and actual access outcome |
| Transformation | Input and output identities, extraction or reconstruction procedure, parameters, and known loss or normalization |
| Reading scope | The actual sections, spans, records, or fields inspected and the material omitted |
| Custody and availability | What was retained, what is only reported to have existed, and what the present worker can obtain |

These are design concepts, not a new implemented schema. A catalog entry can exist before the source bytes are acquired. A reported historical digest can be preserved even when its bytes are unavailable. It should remain a reported digest until the receiving worker verifies the binding it needs.

A session-local retrieval handle also needs its originating scope. Several inventory records pair such handles with URLs, versions, and source locators. A portable context packet should retain durable locators and accessible evidence where possible, instead of assuming another process can dereference an old tool response identifier. [A9]

## 2. Keep identity resolution separate from a correction

The audits encounter several different relationships that a single “duplicate” flag would obscure: two claim IDs describing one original asset; a later paper related to an earlier abstract without verified text identity; a new document edition; a catalog entry whose uploaded document has conflicting authorship metadata; and a previously used source ID that has been retired in favor of a canonical transcript and timestamp. [A1, A8, A9]

Another audit records a search title that names one date while the retrieved page's visible header names another. The author explains the selected interpretation and retains the disagreement. A source's body, catalog metadata, publication date, event date, and retrieval date can each provide different evidence; they should not be silently collapsed into one authoritative timestamp. [A6]

Continuum should support separate relationships such as same retained content, related work, derived representation, claimed successor, and correction of a specific assertion. A stable subject ID can collect those relationships while an exact record or snapshot identity fixes what a particular calculation or interpretation used.

This matters for mutable catalogs. The inventory contains local IDs, current path/hash pairs, version notes, and relationships to other records. A historical report that cites only a local ID needs the catalog snapshot in which that ID was resolved. Otherwise, updating a useful catalog could silently change the source to which an old conclusion appears to refer. [A9]

Attribution also needs enough scope to preserve speaker roles. The source audits separate a question, an attributed answer, a publisher's narration, an editorial description, and an embedded excerpt. Adjoining passages and repeated claims do not establish common authorship or independent evidence. A faithful quotation of a question does not imply the answer endorsed its premise. [A5, A6]

## 3. Record the observer and the evidence boundary

The inventory repeatedly distinguishes the current author's reading from a different worker's prior reading or execution. It can report that a corpus records earlier human review while stating that the present worker read the transcript and did not replay the recording. It can retain a historical hardware manifest while declining to claim current hardware availability. A source-only acceptance record also remains distinct from a later build or runtime witness. [A2, A9]

These distinctions suggest separate reading and action receipts rather than one global source status. A source may be cataloged, accessible, partly read, fully read by one worker, and not reproduced by anyone in the current attempt. A progress brief should project those facts under an explicit cutoff and should identify whose observations support them.

The preparatory calculation record is particularly useful: it lists an input hash, state choices, response channels, comparison grid, anticipated results, and limitations. Its `recorded_before_calculation` field expresses a claim that the record preceded the calculation. This review reads that claim; the time string alone cannot independently prove when the record was fixed. If a future experiment needs a rigorous precommitment, the corresponding context should name the earlier accepted snapshot or causal receipt that establishes the ordering. [A4]

The automation receipt makes a parallel distinction. It records creation and enabled state, while its next-run and last-run fields are null. That supports the historical configuration receipt's scope; it does not by itself show a run starting, completing, or writing durable results. The stored prompt and permissions are part of the historical source, not new authority granted to an importing worker. [A10]

## 4. A computational handoff needs its own admitted domain

The portable arithmetic consumer contract describes a supplied mathematical map and separates fixed coefficients from differentiated variables. It then specifies integer encodings, rational scales, operation-specific input admission, intermediate bounds, output interpretation, and rejection behavior. It distinguishes a covector pullback from an unspecified metric-dependent gradient. These details determine what the program is expected to compute. [A7]

The same record explains why a proposed backend transfer remains a proposal. The CPU consumer and the existing GPU path have different integer widths, ranges, scales, and admission rules. Matching the number of input and output slots does not establish compatibility. Even a checking expression can require a wider integer range than the principal kernel outputs. An algebraic identity evaluated in a reference oracle over a wider mathematical domain is also not another observed execution of the narrower native interface. [A2, A7]

For a future Continuum work attempt, the complete computational contract should answer these questions:

| Contract component | Question it resolves |
|---|---|
| Mathematical operation | Which variables change, which are fixed, and what do the outputs mean? |
| Representation | Which bytes or integers represent those objects, under which units, scales, and conventions? |
| Admission | Which inputs, intermediate values, and resources belong to the supported domain? |
| Rejection behavior | What outcome and output-state guarantee applies when admission fails? |
| Realization | Which source, toolchain, target, dependencies, and build arguments produced the artifact? |
| Evidence and acceptance | Which checks address which failure classes, and who accepted which target under what contract? |

The arithmetic contract separately records exact backend agreement, input/coefficient approximation, and assumptions of the physical model. Accuracy at one layer does not discharge the others. The native manifest similarly reports an external C compiler, runtime libraries, verification dependencies, and a platform-specific binary; source portability and binary portability remain different claims. It does not present that result as adoption by another project. [A7, A12]

These examples support small explicit contracts and separate receipts. They do not require a universal proof system or a full scientific simulator before a useful handoff can occur.

## 5. Context cases this review suggests

The following are proposed cases for later context evaluation, not tests executed here:

| Case | Expected continuation behavior |
|---|---|
| A reconstructed file has a verified local hash but the original download is absent | Use its declared transformation and custody scope; preserve uncertainty about original-byte identity. |
| An old report cites an ID whose catalog entry later changes | Resolve the ID in the report's source snapshot; expose the later correction or edition separately. |
| One worker fully read a source and another only received its summary | Preserve both reading scopes and retrieve the original when the receiving task requires it. |
| A proposed backend matches interface shape but has narrower arithmetic admission | Keep applicability unresolved until its own representation and range contract is checked. |
| A preparatory record contains an earlier timestamp without an ordering receipt | Retain the claimed chronology without presenting it as independently established precommitment. |
| A schedule is enabled but no run outcome is retained | Report the known configuration and the unknown run outcome separately. |

The [protocol architecture](../architecture/protocols.md) can make these distinctions reusable: a source review produces scoped observations, a progress brief projects them, and an executable handoff declares the additional obligations of the intended action. The procedure does not acquire authority from the evidence it reads.

## Exact source identities

The following are paths inside the private source archive. The underlying conversations, operational identifiers, source quotations, and other private payloads are not copied into this public repository.

| ID | Archive path | SHA-256 |
|---|---|---|
| A1 | `calculations/base12-kryon-source-audit.json` | `cbda39deb0113398994e592813ecea8dc3d08959784ad735bd9ec1c56854d000` |
| A2 | `calculations/base12-native-stack-audit.json` | `58de6bc7b414d5971f70be7bcc59376db9be46c80c2646453ddc957151b6860e` |
| A3 | `calculations/deut-wf-provenance.json` | `3c795dbcf0b543c97f5596ee497e2f1f41ff1db7a92e18483a59d874dfbe63bf` |
| A4 | `calculations/deuteron-phase-walk-precalculation.json` | `18d798163554885f63aa86e62d6d1dfd6406dabb2baff47da7c0e189ac1e26c6` |
| A5 | `calculations/flash-matrix-source-handoff.json` | `bfe9fae31232283c26489cc327dd1e6f008c59ec54265fabc70bc68db028f952` |
| A6 | `calculations/kryon-zero-source-audit.json` | `4428c73ca5ce42c0f185adf6b52537957689c4eb9a1e52f7118619ffe647ea61` |
| A7 | `calculations/quadmap-contract.json` | `b195d3991cef118def22c8c5f29cabb1cf7ed6c5063caa3d0ba1e42dc4c88c36` |
| A8 | `data/haramein-inventory-scope.json` | `d38c783d8bd5b07e3846e7f3593984ccb0472a1bfd3399ecdda0be1f3dcfe213` |
| A9 | `data/sources.jsonl` | `508f3df5e6fa355eaccc358c7e26a304850664b3e615826421dc7daef18452c6` |
| A10 | `metadata/automation-receipt.json` | `7ccc03a2221c69dfb05ada9b4c869f699aa54500f964f242f9c0a2867927aefa` |
| A11 | `metadata/integrity.json` | `d655c0436d4b0ed13387db14dd7447131be905ac98d662cb101e54d6b0fceea4` |
| A12 | `native/physics-seed/MANIFEST.json` | `419f07997b9c0f98846d97049e06886711879b0b28e72b4795a9a5b67b0815a0` |

## Combined coverage and remaining limits

The accessible kit still contains 193 files and 8,984,055 uncompressed bytes. The coverage classes below are mutually exclusive:

| Coverage class | Files | Source bytes |
|---|---:|---:|
| Complete semantic reading, including one earlier exact-quotation-deduplicated capture | 86 | 1,287,243 |
| Historical source reviewed by complete diff against fully read current source | 7 | 35,247 |
| This round's complete non-inventory metadata reading and exhaustive generated-binding checks | 2 | 41,950 |
| Outside those completed scopes | 98 | 7,619,615 |

The 86 complete semantic readings comprise 85 direct readings and one earlier exact-quotation-deduplicated capture. The two manifest reviews are kept separate; they are not promoted to a full model reading of every generated entry. Thus **100 files still have no complete semantic or full diff-review claim**, including those two manifests.

The remaining 98 files comprise 86 numerical-result, fixture, and raw-table records totaling 1,724,201 bytes; ten figures totaling 5,832,014 bytes; and two compiled binaries totaling 63,400 bytes. Some numerical records contain authored assumptions and annotations. They are not excluded as though they were purely generated data, and neither parsing nor a matching manifest promotes them to a complete reading claim.

All nine authored files assigned in this round are now fully read. All archived conversation captures and prose reports were covered by the preceding review. This does not mean every external work cited by the source inventory was read here, or that the captures contain every event from their original sessions.

This bounded review stops after the assigned twelve files. The live Prime Radiant checkout remains unavailable; no original source media or historical service receipt was freshly authenticated, and no scientific or performance result was reproduced. The frozen earlier review, other documentation, schemas, protocols, and runtime code were not changed by this scope.
