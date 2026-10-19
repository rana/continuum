# Base12 follow-up: rounded operations and native execution evidence

This follow-up records two successive source-review units at Base12 commit `88382e793b65c84fd8e223840c27f6bb8682864a`: the rounded-program learner with its checked-substitution consumer, followed by the native launch controller's orchestration and saved execution summaries. Their scopes are recorded separately below. It is an additive review dated October 19, 2026. The [earlier coverage checkpoint](README.md) remains a dated record of the preceding review.

The central engineering lesson is concrete: **reusing or replacing an operation requires preserving its declared observations, numerical contract and input conditions.** A matching ideal formula or a favorable summary cannot establish that relationship. These files also show a useful positive case: a restricted rewrite can be justified, bound to exact implementation identities, and consumed by a smaller native routine.

## What was read

The two selected subtrees are relative to `research/owned-stack/2026-10-15/`:

| Source scope | Paths | Bytes across paths | Coverage |
| --- | ---: | ---: | --- |
| `rounded-learning/` | 14 | 68,570 | Complete content coverage, including its existing assembler and runtime dependencies |
| `substitution-check/` | 15 | 51,331 | Complete content coverage, with shared backend files recognized by exact identity |
| Combined | 29 | 119,901 | 26 distinct blobs, containing 105,582 distinct bytes |

This adds **24 direct full semantic readings, totaling 96,545 bytes**. Two distinct assembler/runtime dependency blobs had already been fully read; their four alternate paths were checked for exact identity and were not counted as new readings. The substitution consumer's copy of the rounded emitter is another identical path, represented by the newly read original emitter.

All 29 paths now have exact private copies, checked against their pinned Git blob identities and byte counts, with SHA-256 identities recorded separately. Four previously unmaterialized unique files were fetched, adding 4,921 distinct bytes. Seven additional paths were materialized from already verified identical blobs, adding no new repository content identities. Thus local acquisition increased by **11 paths and four globally new blobs**, with 31,687 additional bytes across local paths.

The newly read files are:

- Under `rounded-learning/`: `ALIGNMENT_AND_REVIEW.md`, `PRESERVATION.json`, `PROTOCOL.md`, `README.md`, `TABLE.md`, `audit.py`, `check.py`, `learner.py`, `model.py`, `native.py`, `radix_core.py`, and `run.py`.
- Under `substitution-check/`: `BACKEND_IDENTITY.json`, `MATHEMATICS.md`, `PRESERVATION.json`, `PROTOCOL.md`, `README.md`, `REVIEW_AND_ALIGNMENT.md`, `TABLE.md`, `apply_checked.py`, `audit.py`, `corruption_checks.py`, `rules.json`, and `scan.py`.

The mechanical pass parsed all 16 Python paths without importing them, parsed four JSON documents, and checked all nine Markdown documents as complete UTF-8 text. All 19 checked source bindings in preservation records and the backend manifest match the actual pinned files. These checks establish byte and record consistency. Semantic reading is separately recorded in the private follow-up ledger.

No upstream program, learner, native routine, audit, test suite or benchmark was executed. No new scientific result or performance measurement is claimed.

## The actual implementation boundary

The learner enumerates a small authored expression grammar. It compiles candidates into scalar x86-64 instructions, evaluates encoded training inputs, and selects by source squared error, then expression size, then lexical order. It retains all minimum-error candidates and all minimum-size ties. Exact teacher calculations and held-out evaluation are outside the fitting function's arguments. This is a software separation of supplied information; the files do not claim adversarial process isolation. See the pinned [learner](https://github.com/rana/base-12-ai/blob/88382e793b65c84fd8e223840c27f6bb8682864a/research/owned-stack/2026-10-15/rounded-learning/learner.py), [runner](https://github.com/rana/base-12-ai/blob/88382e793b65c84fd8e223840c27f6bb8682864a/research/owned-stack/2026-10-15/rounded-learning/run.py), and [protocol](https://github.com/rana/base-12-ai/blob/88382e793b65c84fd8e223840c27f6bb8682864a/research/owned-stack/2026-10-15/rounded-learning/PROTOCOL.md).

The native layer includes expression evaluation, a bounded eight-row squared-error kernel, and rational-input quantization. Python still controls syntax enumeration, orchestration, metadata, loading and records. The digit-based arithmetic reference provides a different implementation of the rounding contract. These are distinct layers of the stack, with distinct trust and cost boundaries; directly emitted arithmetic does not make every surrounding operation native. The [emitter](https://github.com/rana/base-12-ai/blob/88382e793b65c84fd8e223840c27f6bb8682864a/research/owned-stack/2026-10-15/rounded-learning/native.py) and [digit reference](https://github.com/rana/base-12-ai/blob/88382e793b65c84fd8e223840c27f6bb8682864a/research/owned-stack/2026-10-15/rounded-learning/radix_core.py) make those boundaries inspectable.

For Continuum, the useful adaptation is to identify which operations a native engine actually owns. Storage, context selection, dependency checks, query execution and acceptance can each have a precise implementation and measurement boundary. The mere presence of an emitter should not imply a self-hosted compiler, a sandbox or an end-to-end speed advantage.

## Counterexamples that a reusable operation must retain

The following examples are derived from the inspected specifications and source, without executing upstream code. A value is represented by an integer coefficient divided by scale `S`. At `S = 12`, valid coefficients lie in `[-36, 36]`. Multiplication and literal division round at each primitive boundary to the nearest integer, with ties to even. A leaf or intermediate result outside the range returns the declared fault sentinel.

| Proposed change | Valid input coefficients at `S = 12` | Observable difference |
| --- | --- | --- |
| Change `/2` followed by `/3` into `/3` followed by `/2` | `x = 3` | The first path gives `3 → 2 → 1`; the second gives `3 → 1 → 0`. Both ideal formulas divide by six. |
| Replace `(x + y) / 2` with `x / 2 + y / 2` | `x = 1`, `y = 1` | Joint rounding returns coefficient `1`; separate tie-to-even rounding returns `0`. |
| Replace `(x + y) - y` with `x` | `x = -1`, `y = -36` | The original addition produces `-37` and faults; the replacement returns `-1`. |
| Factor `x*x - y*y` into `(x+y)*(x-y)` | `x = -2`, `y = -3` | Separately rounded squares give coefficient `-1`; the factored program gives `0`. |

These examples concern the declared total function from admitted inputs to a value or a defined fault. They are not floating-point anecdotes or claims about unspecified behavior. The pinned [mathematical note](https://github.com/rana/base-12-ai/blob/88382e793b65c84fd8e223840c27f6bb8682864a/research/owned-stack/2026-10-15/substitution-check/MATHEMATICS.md), [rule definitions](https://github.com/rana/base-12-ai/blob/88382e793b65c84fd8e223840c27f6bb8682864a/research/owned-stack/2026-10-15/substitution-check/rules.json), and [native checks](https://github.com/rana/base-12-ai/blob/88382e793b65c84fd8e223840c27f6bb8682864a/research/owned-stack/2026-10-15/rounded-learning/check.py) give the relevant contracts and witnesses.

The cancellation rule becomes valid on the restricted input domain satisfying `|x + y| ≤ 3S`. That condition belongs to the reusable result. If the condition fails, the evidence does not cover that state; it does not establish that every possible implementation or future attempt must fail. Likewise, simplifying an expression so that it stops reading an argument does not remove the caller's separate obligation to validate that argument.

Fault observability must also be explicit. This particular substitution contract equates two faults represented by the same sentinel. It does not preserve different fault causes, fault locations, instruction counts, external effects or timing. A future consumer that observes those distinctions needs a stronger contract before reusing the same acceptance decision. See the [substitution protocol](https://github.com/rana/base-12-ai/blob/88382e793b65c84fd8e223840c27f6bb8682864a/research/owned-stack/2026-10-15/substitution-check/PROTOCOL.md).

## A positive rewrite with a specific argument

Nearest-even rounding does admit some useful transformations. The inspected mathematical argument establishes, for every integer coefficient `n`, that rounding `n/2` and then dividing and rounding by two equals rounding `n/4` once. The proof separates `n` into eight residue classes and uses only even integer translations, which preserve tie parity. It does not justify arbitrary fusion or reordering of rounded divisions.

The historical consumer checks source bindings, backend bindings, the declared scale and domain, and freshly emitted code hashes before using this one substitution. Its recorded example reduces the routine from 278 to 175 bytes and from two divisions to one. Those are source-reported code and operation counts; this review did not reproduce the execution, and those counts are not a timing result. The [consumer](https://github.com/rana/base-12-ai/blob/88382e793b65c84fd8e223840c27f6bb8682864a/research/owned-stack/2026-10-15/substitution-check/apply_checked.py) explicitly consumes a trusted local certificate and is not an adversarial proof-checking service.

This is a promising shape for native repository optimization: establish a useful restricted transformation, state what it preserves, check applicability, bind the actual source and implementation, and retain the counterexamples that delimit it. The first practical targets can be constrained repository queries and context operations with clear observations. General source equivalence is a substantially larger problem.

## What this means for context and evidence

These sources suggest three concrete distinction pairs for a context-and-handoff experiment:

1. Two summaries both say a cancellation rewrite was checked, but only one carries an applicable range guard. A resumed worker must distinguish unconditional acceptance from acceptance within that guard.
2. Two descriptions name the same ideal formula, but their primitive rounding placement differs. A context projection must preserve the numerical contract or a retrievable exact reference to it.
3. Two learning summaries report a perfect source fit, but one still has distinct tied explanations. A lexical selection is a chosen candidate, while identification remains unresolved.

The third distinction comes directly from the retained candidate sets and the historical [rounded-learning findings](https://github.com/rana/base-12-ai/blob/88382e793b65c84fd8e223840c27f6bb8682864a/research/owned-stack/2026-10-15/rounded-learning/README.md). A compact context need not reproduce every candidate inline. It should preserve the unresolved status and an exact route to the candidates or the inputs needed to reconstruct them. Whether that reconstruction is cheap enough is a separate measurement.

The saved-output audit also clarifies what evidence can establish. Its independently written arithmetic path checks saved values without importing the emitter; its corruption controls alter an output, remove an output, change the contract and change an identity binding. Those are targeted checks of specific failure modes. They do not turn saved output into a new historical execution observation, and shared authorship remains visible. See the [audit](https://github.com/rana/base-12-ai/blob/88382e793b65c84fd8e223840c27f6bb8682864a/research/owned-stack/2026-10-15/substitution-check/audit.py) and [negative controls](https://github.com/rana/base-12-ai/blob/88382e793b65c84fd8e223840c27f6bb8682864a/research/owned-stack/2026-10-15/substitution-check/corruption_checks.py).

For Continuum, a reusable finding should therefore bind the exact source or operation, semantic contract, admitted state, checker identity and policy, supporting observations, and known counterexamples. A self-declared passing receipt remains evidence to assess. It does not authenticate its issuer or prove its own contents. These are proposed adaptations; the existing native storage and receipt mechanics do not yet implement a semantic optimization validator.

## Remaining scope

The two selected source subtrees are complete by unique content, including previously read dependencies. Their later preservation and review directories, compressed raw run archives, and complete historical numerical records were outside this follow-up. Original READMEs describe publication and review states at their own dates; those historical states have not been promoted to claims about the latest repository or collaborator status.

The full Base12 repository reading remains incomplete. This first unit adds 24 distinct full reads to the earlier 88, yielding 112 directly reviewed content identities and 972,967 bytes at that checkpoint. It does not update the earlier public coverage JSON or imply that unreviewed neighboring directories are covered. The second unit below follows the connection from native operations into caller control and execution evidence.

## Second review unit: native launch orchestration

The second selected scope is `research/owned-stack/2026-10-16/native-launch-controller/`, including every source, contract, fixture, provenance and execution-summary file outside its generated `artifact-r1/` directory. It contains **26 paths and 149,643 bytes**. Three dependency files had already been read completely: `build.py`, `CONTRACT.md`, and the byte-identical instruction encoder. The remaining **23 files, containing 117,020 bytes, were acquired exactly and read in full**. Materializing the encoder's alternate path adds one more local path and 6,390 bytes without adding a new content identity.

The newly read files are `CALLER_INVOCATION.md`, `DEPENDENCIES.json`, `ENVELOPE.md`, `ENVELOPE_PROVENANCE.json`, `FREEZE.sha256`, `OPEN.md`, `OWNER.json`, `README.md`, `REVIEWER.md`, `REVIEW_REQUEST.md`, `SCOPE_CHECK.json`, `STATIC_CHECK.json`, `fixtures.json`, `inspect_static.py`, `proposed-caller.py`, `proposed-group.sh`, `proposed-launch.sh`, `proposed_cases.py`, and all five `execution-01/` files: `EVIDENCE.json`, `README.md`, `RESULTS.json`, `REVIEWER.md`, and `SHA256SUMS`.

Thirty-three checked source and record bindings match their actual pinned bytes. This includes the available source entries in the freeze, the inline caller's literal pins, available source/control identities in the execution summary, and the four result-document checksums. The 26 saved case summaries also match the fixture return codes, explicitly specified receipt lengths and injected-error identities; their aggregate counts are consistent. This is source and metadata checking, not a new verification of raw execution evidence.

The excluded generated directory contains **38 paths and 139,174 bytes**: emitted binaries, instruction listings, disassemblies and artifact records. Those artifacts were inventoried but were not newly acquired or semantically audited in this unit. The referenced raw execution receipts, traces and independent terminal captures were also outside this scope. No control script, fixture, binary or upstream verifier was run.

### Four different meanings of success

The source separates the native runner, its child, the synthetic test driver and the enclosing acceptance caller. These scopes must survive a handoff.

| Observation | What the inspected contract permits a reader to infer |
| --- | --- |
| Runner returns zero | Its launch/receipt procedure can have completed even when the child failed or reported an exec error. |
| Child returns zero | A child outcome; it does not establish that receipt publication or enclosing acceptance succeeded. |
| A complete-sized receipt exists | Bytes exist; injected fsync or close failures can still make publication invalid under this contract. |
| A completion-looking candidate file exists | Provisional evidence; this particular caller contract also requires the externally captured terminal status and valid accounting. |

These distinctions are visible in the pinned [fixture matrix](https://github.com/rana/base-12-ai/blob/88382e793b65c84fd8e223840c27f6bb8682864a/research/owned-stack/2026-10-16/native-launch-controller/fixtures.json), [test driver](https://github.com/rana/base-12-ai/blob/88382e793b65c84fd8e223840c27f6bb8682864a/research/owned-stack/2026-10-16/native-launch-controller/proposed_cases.py), and [acceptance caller](https://github.com/rana/base-12-ai/blob/88382e793b65c84fd8e223840c27f6bb8682864a/research/owned-stack/2026-10-16/native-launch-controller/proposed-caller.py).

The caller can write complete-looking candidate and accounting files before its final publication-inclusive budget check. A later failure or missing terminal observation prevents those files from establishing acceptance. This supplies a useful distinction pair for context testing: the files are the same, while the required external terminal evidence differs.

The authority boundary is specific to the operation. Continuum's already committed local acceptance transaction has a different recovery contract: its durable receipt can establish the committed result even if the acknowledgement is lost. A repository should retain which commit or observation boundary governs a claim, instead of applying one universal interpretation to every success marker. See the [native foundation's current scope](../../CURRENT.md).

### Authenticate before control execution

The controller's review history records a correction from a candidate launcher's self-check to a separately supplied gate. The gate receives literal expected hashes, checks source bytes before evaluating candidate control code, and passes already authenticated caller bytes into execution. The source tree is required to remain quiescent; the described checks do not constitute hostile same-user isolation. The [inline invocation](https://github.com/rana/base-12-ai/blob/88382e793b65c84fd8e223840c27f6bb8682864a/research/owned-stack/2026-10-16/native-launch-controller/CALLER_INVOCATION.md) and [review record](https://github.com/rana/base-12-ai/blob/88382e793b65c84fd8e223840c27f6bb8682864a/research/owned-stack/2026-10-16/native-launch-controller/REVIEWER.md) state this boundary explicitly.

The transferable requirement is that an execution request must identify the authority for its expected bytes before those bytes become executable control. Self-reported identity after execution answers a different question. For a future remote worker, that distinction belongs in dispatch and admission, together with the actual isolation and input-mediation contract.

### Account for the whole attempt

The external envelope distinguishes the native launch interval from preparation, authentication, postchecks, process observation and publication. Nested watchdogs own different process groups, so a shared start and latest-start checks are needed to relate their targets. Per-process resource limits remain separate from aggregate accounting. The source also avoids adding the same descendant CPU time through two overlapping measurements. These are documented mechanisms in the [envelope](https://github.com/rana/base-12-ai/blob/88382e793b65c84fd8e223840c27f6bb8682864a/research/owned-stack/2026-10-16/native-launch-controller/ENVELOPE.md); this review did not exercise them.

The historical successful batch did not test watchdog expiry or hostile descendants. Its saved accounting sample precedes final publication; the source reports a captured caller exit as evidence that the later inclusive check passed, without a persisted final numeric sample. Those are different evidence shapes. A context record should preserve the missing measurement while retaining what the observed terminal event actually supports. The [dated result](https://github.com/rana/base-12-ai/blob/88382e793b65c84fd8e223840c27f6bb8682864a/research/owned-stack/2026-10-16/native-launch-controller/execution-01/README.md) states both limits.

Two further details are useful. The driver preserves observations before checking expectations, so a failure leaves evidence. Its injected-error cases require a trace of the intended error, and interruption-retry cases require a subsequent successful syscall; merely reaching an expected exit status is insufficient. A later correction also distinguishes a harmless disappeared-process diagnostic from an unreadable still-existing process. Diagnostic text and the actual scan outcome carry different meanings.

### Preserve historical state without reviving it

The frozen owner and fixture records still describe preparation and an unused attempt. The later dated execution result records that the selected attempt was consumed. Keeping the old bytes is correct preservation; treating their historical status as the current instruction would be a context error. Source identity, statement time, scope and the later superseding observation need to remain connected. See the pinned [owner record](https://github.com/rana/base-12-ai/blob/88382e793b65c84fd8e223840c27f6bb8682864a/research/owned-stack/2026-10-16/native-launch-controller/OWNER.json) and [later result](https://github.com/rana/base-12-ai/blob/88382e793b65c84fd8e223840c27f6bb8682864a/research/owned-stack/2026-10-16/native-launch-controller/execution-01/README.md).

This is a concrete reason for a native context engine to preserve evidence-backed changes of state and unresolved observations. It should let an agent recover the governing state without rewriting old records, discarding diagnostic evidence, or silently granting another execution attempt.

## Combined follow-up checkpoint

Together these two units add **47 directly read distinct blobs and 213,565 bytes**. Relative to the preceding review, exact local acquisition increases by **35 paths and 155,097 bytes across paths**, including **27 globally new blobs containing 121,941 bytes**; the other new paths reuse content already present. The additive direct-reading total is **135 distinct blobs and 1,089,987 bytes**. These are source-review counts, not completed experiments or claims about correctness.

The earlier public JSON remains unchanged. The complete per-file follow-up ledgers and exact source copies remain private. Whole-repository reading is still incomplete, including the controller's generated artifact directory, referenced raw execution evidence, neighboring native research-loop consumers, and substantial other source and data. This follow-up establishes the two declared reading scopes and the design consequences above.
