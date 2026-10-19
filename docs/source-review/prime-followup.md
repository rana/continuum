# Prime Radiant follow-up: continuity, representation, and evidence custody

Review date: October 19, 2026. Status: source-informed design proposals; this document adds no runtime behavior or policy authority.

**The strongest additional requirement is to preserve the distinctions that change a future action.** Those distinctions include an unresolved operation outcome, the assumptions behind an interpretation, an unavailable observation, and a historical result whose original bytes have been lost. A readable summary and a retained source tree can both be accurate while omitting these facts.

This follow-up extends the earlier [research lessons](../research-lessons.md) and informs the proposed [context experiment](../architecture/representation-experiment.md). It reads a coherent remaining group in the accessible Prime Radiant kit: three complete dialogues, their report and numerical results, and the records of failed output and artifact recovery. It adapts the method and failure lessons without importing the upstream physics models or private conversations into Continuum.

## What was actually read

The source is the fourth stored edition of the October 18, 2026 research kit, archive SHA-256 `97a156c3d6618d9f84f1271ec44dc12b056b0fdbfbf4fcf1de950cea691708a8`. The earlier review checked all 193 archive entries against its integrity metadata. This follow-up read **15 complete files totaling 340,039 bytes**. Thirteen files, totaling 328,860 bytes, newly reached complete semantic reading; two provenance records were revisited.

| Complete follow-up reading | Files | Scope |
|---|---:|---|
| AI-native, resonance, and whole-physics dialogues | 3 | Twenty top-level message records, including the complete supplied request payloads and authored audits |
| Their capture receipts | 3 | Exact byte identities, message counts, and declared roles |
| Observability and resonance-memory results | 2 | All saved fields, numerical values, assumptions, checks, and limits |
| Zero/native/laboratory report | 1 | Complete dated synthesis and embedded architecture decisions |
| Native failure outputs | 3 | Complete original metadata text, including malformed output |
| Native review and recovery provenance | 2 | Original custody gaps, recovered source, and correction scope |
| Research-state snapshot | 1 | Complete orientation, continuation, and capability claims at its cutoff |

The dialogues contain three top-level user messages, seven records labeled Claude, and ten assistant request/audit records. Earlier messages repeated inside a request remain exposure history, not additional independent contributions. This review did not make new Claude requests or authenticate the original service independently.

All fifteen file hashes match the previously integrity-checked archive metadata. The three capture receipts match their exact capture bytes and declared message counts. The current observability result names the hash of the retained current script. These are internal provenance checks. **No upstream source, verifier, binary, scientific calculation, or simulation was executed.** Reading a saved numerical result is not reproducing it.

## 1. Preserve raw output before interpreting it

Two retained native failure reports contain `inf` or `-inf` tokens that are invalid JSON. The archive deliberately preserves them as exact text. Their invalid serialization is evidence of the defect. Replacing those values with `null`, reserializing through a permissive parser, or refusing to retain the output would alter or lose that evidence. A third report parses successfully while the implementation and a closely related reference share a numerical error. Syntax, byte integrity, and substantive correctness are separate properties. [S10–S14]

Continuum should support the following sequence for content within the authorized capture scope:

1. Retain the exact received bytes as an immutable blob, with an explicit complete or partial capture boundary.
2. Run an identified decoder or evaluator on that blob.
3. Append an interpretation receipt that names the raw identity, decoder version, result, and diagnostics.
4. Admit a typed domain object only when its own contract is satisfied.

An output that cannot become a valid domain object can still be valid evidence of a failed execution. A corrected decoding creates a new interpretation; it does not rewrite the original capture. The [execution record design](../architecture/execution-and-context.md) should preserve this distinction as typed ingestion is implemented.

## 2. A known result and custody of its original evidence are different facts

The observability records describe a wider initial execution and a later narrowed one. The current result has 41 source-matched checks. The earlier execution included an additional control and 42 checks, but its complete original JSON was overwritten during scope refinement. A separate historical record preserves the reported finding, exact mathematical values, and the explicit absence of the original raw snapshot. The extra result is excluded from the current check count. [S1, S7, S9]

The native recovery record has a related boundary. Seven original core source files were recovered from retained tool reads, with prior hashes or unchanged current source available for comparison. The original executable, original verifier, and complete initial verification report remained unavailable. The archive retains compact observations and defect outputs without claiming those missing artifacts were recovered. [S10–S11]

Continuum needs more than a single `verified` or `archived` flag:

| Fact | Meaning |
|---|---|
| Existence reported | An identified producer says an artifact or execution existed. |
| Exact bytes captured | A content identity names retained bytes from a stated capture. |
| Retrieval checked | A specified store returned matching bytes at an observed time. |
| Retention promised | A policy or custodian promises a stated preservation scope. |
| Original missing | The original artifact is unavailable; surviving summaries remain separately identified. |
| Partial recovery | Some original components were recovered, with the method and identities stated. |
| New reproduction | A new build or execution produced new artifacts. |

These are related observations and commitments, not a universal progression. A retention promise is not proof of current availability. A last successful retrieval is not proof that bytes remain available indefinitely. A hash recorded in a source file is not custody of the referenced content.

The practical design requirement is to let a retained record state its own missing dependencies. An agent should be able to use a historical observation with an appropriate qualification while avoiding the stronger claim that the original experiment can be replayed from complete retained evidence.

## 3. Context sufficiency depends on the next question and available operations

The reviewed examples compare descriptions that collapse distinct states. In the bounded spring model, two preparations have the same current local position and velocity but different local futures. Eliminating the omitted oscillator requires both a memory term and hidden initial-condition information. An augmented state or a higher-order description provides another possible repair. Ideal observations over time can reveal the known full state even when an instantaneous local snapshot cannot predict its own continuation. [S3, S8]

The observability example makes a complementary point. Its declared controls leave a distinction invisible. An additional control can expose that distinction only if the control is available. A new coordinate system alone does not add evidence. The saved ranks concern a specified noiseless model; they do not establish an optimal experiment under finite noise, latency, or cost. [S1, S7]

These are mathematical examples, not a claim that agent memory obeys those equations. Their useful software consequence is precise: a context pack should declare the decision family it supports, the history it includes, the distinctions it omits, and the retrieval or reconciliation operations available to its recipient.

A packet may suffice for inspection while an external action still requires checking an operation receipt. It may name an informative probe that the receiving workstation cannot currently perform. In that case the uncertainty remains. Neither the method definition nor the packet creates access to the missing source or service.

The smallest useful context is therefore relative to an action and its input contract. A selector that optimizes only size or agreement can favor an uninformative constant summary. Evaluate whether the context supports correct decisions, then account for retrieval, time, and storage costs. The existing [context-pack design](../architecture/execution-and-context.md#context-packs) already provides the foundation; an explicit decision scope and required probes are useful candidate refinements.

## 4. Preserve corrections at the claim level

The full dialogues contain substantive proposals followed by consequential corrections. Examples include claims that an unimplemented capability already existed, an unconditional scaling rule, and an attribution of error discovery to an interval backend that had not been implemented. The final authored audits preserve what was accepted, corrected, rejected, and still open. They remain separate from the raw collaborator replies. [S1, S3, S5]

A continuation packet containing only the initial proposal can revive a corrected error. A packet containing only a confident final sentence can omit the conditions that made it valid. A useful projection carries the accepted claim with its scope, a link to the correction, and relevant unresolved objections.

The review also records an explicit disagreement about method. Agreement within a selected ensemble of formalizations was not accepted as proof of a source's invariant meaning. Consensus was not made a prerequisite for exploring an individual branch. A fixed three-round stopping policy was not adopted as a universal rule. Those distinctions matter for Continuum's extensible protocols: a method's suggestion, a trial's chosen budget, and current policy authority remain different objects. [S1, S9]

Repeated quotation should not inflate independent support. A model reply copied into several later requests remains the same exposed source. Preserve the outer request bytes and the relation to its earlier source, so later evaluation can distinguish independent judgments from judgments formed after seeing the same argument.

## 5. A correction can change the admissible domain

The native correction combined arithmetic and finite-output guards with a narrower dimensionless input contract. The retained extreme cases became explicit rejections. That is useful progress, but it does not demonstrate accurate computation on the excluded inputs. [S10, S12–S14]

Continuum should let a successor say which kind of change resolved an issue: the algorithm changed, the accepted input world narrowed, a claim was withdrawn, or the evaluator was corrected. The old counterexample remains meaningful under its old scope. This fits the proposed `applies / does_not_apply / unknown` evidence contract: reuse is a judgment about an exact target and scope, not a property inherited from a green check.

Independent verification also needs an explicit comparison boundary. A second implementation sharing the same mistaken intermediate can agree perfectly. The retained failure illustrates why the evaluator's dependencies and the faults it can detect matter more than a count of reviewers or checks. [S10, S12]

## 6. A current pointer and an acceptance authority are different things

The dated report and the later research-state snapshot have different cutoffs. The report contains fewer accumulated dialogue records than the state after a subsequent extension. This does not make the earlier report false. It makes cutoff and source snapshot necessary metadata for a projection. [S9, S15]

The state also describes a standalone kit awaiting reconciliation with a separate canonical checkout. Its navigation and historical capability statements do not establish that integration happened. Continuum should preserve an import's origin and intended destination while requiring actual target acceptance under the target's authority contract. Copied policy text or a producer's `current` label does not grant the receiving process new authority.

## Concrete additions to the context experiment

The following are candidate semantic scenarios, not tests executed by this review:

| Scenario | Required distinction |
|---|---|
| Capture malformed output, then restart | Raw byte retention succeeds while typed decoding fails; neither fact erases the other. |
| Narrow an experiment after a wider result | The predecessor remains identified, its raw-custody gap stays visible, and its checks are not counted in the successor. |
| Quote the same reply in several requests | Exposure is preserved without treating repeated text as several independent observations. |
| Lose a reply after an operation may have run | Reconcile the original operation or report uncertainty before deciding whether another dispatch is appropriate. |
| Transfer a packet to a workstation lacking its proposed probe | Keep the missing distinction unknown; do not infer that the probe happened. |
| Exclude a failing input under a revised contract | Report a narrower accepted domain without claiming the excluded computation now succeeds. |

Compare compact projections with the complete retained histories under the same decision contract. Measure wrong actions, missed uncertainty, unnecessary repeated work, required retrieval, and time to a correct next decision. These cases can reveal whether the proposed work graph improves continuity before a general scheduler or automatic summarizer exists.

## Source identities and remaining limits

The identifiers below refer to files inside the private source archive, not files copied into this public repository. They make the source encounter precise without publishing the underlying conversations or unrelated operational details.

| ID | Archive path | SHA-256 |
|---|---|---|
| S1 | `conversations/pr-20261018-ai-native-inquiry.json` | `3d5ba168492dffb4b2418c37ade8a08f44cbcbcd4f8e4ccd55ae77230c10f82d` |
| S2 | `conversations/pr-20261018-ai-native-inquiry.receipt.json` | `8a013cba101f02ae0bd684be22987a854a706030d48142cfabf3fbe5faf3ce1a` |
| S3 | `conversations/pr-20261018-resonance-chambers.json` | `9a4519672f833feb323d7e4d65836267bd802425fe57d8cf6adb65865a2e3ea4` |
| S4 | `conversations/pr-20261018-resonance-chambers.receipt.json` | `a5190818e31d49ac538dfbbc599c96939e5e57a1fd3f3d44e6e04c640502a5f1` |
| S5 | `conversations/pr-20261018-whole-physics-laboratory.json` | `0b3e124c81438a86b839e1965f1f3cccb6a75fbc821ff4f94475febe849f7409` |
| S6 | `conversations/pr-20261018-whole-physics-laboratory.receipt.json` | `76b8092f8922a94518bcfca6d18db461c09f4feb2b57b21724ffb9fa51ed57b5` |
| S7 | `calculations/ai-native-observability/results.json` | `2874b800a6641d2708806addae4f51145e047dd4aa2c32461902a02b0a6ffc17` |
| S8 | `calculations/resonance-memory/results.json` | `f0bc2e5446e7323c809c02ce8b03014f226dc62c0b7afad5f277c1359be7eea7` |
| S9 | `reports/prime-radiant-zero-native-laboratory-report-2026-10-18.txt` | `c5f3f2471a028c5f14e3c58688718c87771e3b9bbe746bd5cd2e2e0c2bf3ab7c` |
| S10 | `native/physics-seed/review/peer-review-provenance.json` | `9b3a539a190ecac777c3151ad5af8de4ace6bc0fd947e03a6ddba4cf7929d8be` |
| S11 | `native/physics-seed/review/pre-fix-source/recovery-provenance.json` | `df9d6541a5224f409fd5b78b85c90b48c2df63afedfe7ccd85ebda0d0283a428` |
| S12 | `native/physics-seed/review/dx_squared_overflow.original-metadata.txt` | `f3c64d314f5c2477fb0dbad28f9b6b133967cff38b061008efa747e0e6681df4` |
| S13 | `native/physics-seed/review/boundary_sum_overflow.original-metadata.txt` | `09d5a94bf70486d30adc820937e0284e5c85c041551fd3f4f6f2a8ee028241cb` |
| S14 | `native/physics-seed/review/fourier_product_overflow.original-metadata.txt` | `71bdaddcb5186d40aec8b237c2257dd1edd9fb213d87a14e42d9b81013c75e04` |
| S15 | `prime-radiant-research-state.json` | `da5e21b837d54608df537a25fe2191afe8d7644727063b7d6324312d071f0ed4` |

Together with the previous review, 64 archive paths have a complete direct text or structured-record reading claim, totaling 860,244 bytes. Seven historical source paths remain separately recorded as complete diff reviews against fully read current source. The other 122 archive paths are not promoted to either category by this follow-up. Five other dialogue captures, two older reports, remaining source-record content, numerical traces, images, and binaries remain outside this new reading group.

The live Prime Radiant checkout remains unavailable. No absent original artifact was recovered here, no external source cited inside the historical dialogues was freshly authenticated, and no scientific result was rerun. The completed work is a source-informed refinement of what Continuum should preserve and how that preservation can be tested.

## Scope extension: the remaining historical dialogues and reports

This separately scoped continuation, also completed on October 19, 2026, covers the historical material left outside the first follow-up above. It adds **five conversation captures, their five receipts, and two older prose reports: 12 files totaling 261,747 source bytes**. The earlier section's counts describe its own completed group; the combined coverage below includes this extension.

All fields and previously unread text were read in complete coherent records. Eleven files were read directly. In the remaining capture, 58 exact paragraph occurrences, totaling 29,662 decoded characters, had already been read in earlier source records. Its review view replaced only those exact quotations with provenance markers. Every match was checked against both its source and target location by character count and SHA-256; the original capture bytes were unchanged. Decoded character counts are not source-byte counts. No approximate similarity or inferred equivalence was used to omit text.

The five captures add 34 top-level message records: nine labeled user, eleven labeled Claude, and fourteen assistant requests or audits. **All eight archived captures, all eight accompanying receipts, and all three prose reports in this kit now have complete semantic coverage.** Together the captures contain 54 top-level records: twelve user, eighteen Claude, and twenty-four assistant records. Repeated quotation inside a request is exposure history, not another independent contribution. The receipts bind the saved bytes and declared counts; they do not independently authenticate the original service or authorship. [D1–D12]

### A passing example can conceal a changed formal input

One historical reply states a dimensionless expression containing `2i/x²`; the later report gives the corrected term `2i/x` and explicitly records the denominator correction. Both expressions agree at the emphasized special case `x = 1`, so checking that example alone would miss the change. The report also separates a spatial attenuation ratio from a proposed temporal response interpretation. This is a useful failure pattern even without adopting any upstream physical model. [D1, D11]

For Continuum, a handoff should identify the exact formal object used by a claim and the input domain in which it is asserted. A polished paraphrase, a familiar label, or one successful example cannot establish that the operator survived transmission. A useful context experiment would preserve both candidates, test the shared example, and then require a discriminating input admitted by the same contract. The evaluator should be able to report “these examples agree; equivalence remains unknown” until that distinction is resolved.

### Corrections apply to claims, with their own scope

The local-structure dialogue contains a concrete counterexample to an earlier generalization. Claude retracts that generalization and proposes new interpretations; the following authored audit qualifies additional statements in the revised reply. The record therefore does not support a single corrected/uncorrected flag for an entire message. It supports a chain of individually scoped claims, objections, revisions, and remaining questions. [D3]

This suggests a precise retrieval rule: when a context packet includes a claim, it should also retrieve consequential corrections and the evidence or assumptions to which they apply. A message accepted as useful context does not thereby become a set of accepted assertions. A correction can preserve part of the original observation while changing the inferred mechanism or its domain. The old bytes remain available to explain how the research changed.

### A shared word does not establish a shared object

Across the dialogues, the same words are applied to different objects: a geometric crossing, a zero of an amplitude, a zero eigenvalue, and an unobserved component of a state. The authored audits repeatedly reject silent identifications between these uses. The walk also changes more than physical size: particle number, representation, measurement channel, and retained information are separate axes. [D5, D9, D12]

Continuum should carry a small bridge record when an agent transfers a conclusion between descriptions: the starting object, proposed map, destination object, assumptions, and information retained or lost. Domain-specific fields such as units, basis, dynamics, or observation channel apply when relevant. A new label does not supply the map. The same principle applies to software terms such as source, build, test, acceptance, and deployment: a common name must not erase the operation or authority that gives it meaning.

### Novel questions may remain useful before a test exists

The protocol dialogue revises an initially rigid walk into a bounded inquiry whose lenses are chosen for the question. A walk may end with an unresolved interpretation, a new source-access question, or a newly visible ambiguity. It need not invent an experiment or force every stage of a scale traversal. At the same time, returning through the same assumptions supplies no independent evidence. [D5, D9]

This reinforces a distinction between an imaginative seed and an accepted work attempt. A seed can preserve a question, origin, and reason to revisit it with little overhead. An executable attempt adds exact inputs, permitted actions, budget, and an outcome record. Promotion should add obligations appropriate to the action without retrospectively treating every early thought as a failed specification. Useful negative findings remain scoped to the particular interpretation or observable that was actually examined.

### Independence and coverage need more than a reviewer count

The historical requests disclose what material the collaborator received and when it lacked independent source access. The reports separate source quotation fidelity, mathematical interpretation, numerical execution, and empirical comparison. Their bibliographies also distinguish catalog records, abstracts, selected sections, and complete readings; upload dates and repository labels do not by themselves establish new document editions or completed research. [D1, D11, D12]

For Continuum, reviewer identity, supplied context, source retrieval, and execution observation are separate provenance facts. Two agents checking a common supplied formula may offer useful reasoning without supplying two independent source observations. A report's cutoff should identify the records used to generate it, while its coverage statement identifies what those workers actually read or did. A retained source pointer should not be upgraded to a verified derivation by aggregation.

### Additional context scenarios suggested by this group

These are proposed semantic cases, not newly executed tests:

| Scenario | Distinction the continuation should preserve |
|---|---|
| A formula changes while its headline example still passes | Exact formal input and an admitted discriminating case remain available; agreement at one input does not prove equivalence. |
| A useful reply contains one accepted correction and another unresolved assertion | Claim-level acceptance and correction scope survive message-level summarization. |
| Two agents use the same noun for incompatible objects | The proposed mapping and its assumptions stay explicit or the correspondence remains unresolved. |
| A promising inquiry stops before a discriminator exists | The seed retains its rationale and open question without a fabricated success criterion or failure status. |
| Two reviewers receive the same source excerpt | Exposure and reasoning contributions remain distinct from independent retrieval or execution. |

### Exact source identities for this extension

These paths identify entries in the private archive. Their contents are not included in this public repository.

| ID | Archive path | SHA-256 |
|---|---|---|
| D1 | `conversations/pr-20261018-claude-dialogue.json` | `284317fa3ec6cb055bb4ca70f91211834eea73dd2b7e49560dce19ae6bb58090` |
| D2 | `conversations/pr-20261018-claude-dialogue.receipt.json` | `6de93a6683a1f2b4a856909f216765238d416af563ba92cff941a1c683f619e2` |
| D3 | `conversations/pr-20261018-local-phi-structures.json` | `2cac5bb962973c334cfb17353f8d198485b25487d702b4533f586252e028e3dc` |
| D4 | `conversations/pr-20261018-local-phi-structures.receipt.json` | `8b913a6a4b4dcde453079b5456b26e650ea422b02573de7ab7ef235b39c5912c` |
| D5 | `conversations/pr-20261018-walk-flash-matrix.json` | `66f88c437ea1233d967be91715f734848fcf2621c884b94bd949e326d689bfe9` |
| D6 | `conversations/pr-20261018-walk-flash-matrix.receipt.json` | `d3ef5f5b82192abb00b4740bb47360627091118ec217cf43e12ddf6126b4782a` |
| D7 | `conversations/pr-20261018-visible-user-transcriptions.json` | `61809e0a961667a029e4d7dd24aa257aee75676f0e3e8ea7b5554599c8397999` |
| D8 | `conversations/pr-20261018-visible-user-transcriptions.receipt.json` | `ada7ab7d9a4f5e9e11dae4da0a62a6593ef024863bedf8e0e28b1358c81e6780` |
| D9 | `conversations/pr-20261018-kryon-zero-protocol.json` | `72a3de9734971ac89cc4c772e5453811d304795544949f8bd93c80502e1f1ccc` |
| D10 | `conversations/pr-20261018-kryon-zero-protocol.receipt.json` | `74a6c7cee13d3989d4bbbbc29db53d7c52325423b9daf023c6416b06c78daec7` |
| D11 | `reports/prime-radiant-research-report-2026-10-18.txt` | `8a697cdce7e71bf93233b2265c879f7a1a7457c61ca4353d160dbd9497490fca` |
| D12 | `reports/prime-radiant-walk-flash-matrix-report-2026-10-18.txt` | `635b3c9b59f7e06057caa2a451b034b2432e38a4aa6e779eeb2439113aa797cb` |

### Combined coverage and the remaining material

The accessible kit contains 193 files and 8,984,055 uncompressed bytes. Combining the initial review and both follow-up groups gives **76 paths with complete semantic coverage, representing 1,121,991 source bytes**: 75 directly read paths and one capture read with exact prior-quotation deduplication. Seven additional historical source paths, totaling 35,247 bytes, retain their separate complete diff-review classification. Source-byte volume measures the files covered, not unique information or verified scientific claims.

The remaining **110 files, totaling 7,826,817 bytes**, have no complete semantic or full diff-review claim. The remaining human-authored material is not hidden behind a generated-data exclusion:

| Remaining category | Files | Source bytes | Reading boundary |
|---|---:|---:|---|
| Source audits, preparatory contracts, and source inventory | 9 | 161,243 | Authored structured research material; parsed and selectively inspected, without complete semantic coverage |
| Numerical results, fixtures, and raw tables | 86 | 1,724,201 | Includes authored assumptions and annotations as well as generated values; no claim that every row or annotation was read |
| Operational and integrity metadata | 3 | 45,959 | Receipt, manifest, and integrity records; prior structural checks do not imply a complete semantic reading |
| Figures | 10 | 5,832,014 | Inventory and hashes only; no complete visual review |
| Compiled binaries | 2 | 63,400 | Inventory and hashes only; not executed or disassembled |

The nine authored structured files include source-attribution audits, a pre-calculation record, a proposed arithmetic contract, and the source inventory. No historical conversation capture or prose report remains in that gap. The captures nevertheless describe their own omissions, including some interim commentary; complete reading of the captures is not a complete export of every historical event.

The live checkout is still unavailable. This extension did not execute upstream code, reproduce the numerical claims, recover missing original artifacts, or freshly authenticate source media and papers cited by the archived authors. It adds source-informed design questions and exact reading coverage; it does not add runtime behavior, implementation acceptance, or policy authority.
