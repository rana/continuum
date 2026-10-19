# Builder fixture derivation and evidence limits

This Research Delta completes four full readings / 54,576 bytes at Base12 commit `88382e793b65c84fd8e223840c27f6bb8682864a`, tree `5cf96129bdcb0dde075f6f5800ae0c68a95c4b82`. The current Continuum chat owns this read-only contribution, based on main `fc1cd3c7d46c51232752533adbc4a9d1b5ce09b8`. Selected preparation files are `materialize_fixtures.py`, `FIXTURE_REVIEW.md`, `fixtures/PROVENANCE.json` and `fixtures/SHA256SUMS` under `research/owned-stack/2026-10-16/native-builder-slice/`. The [ledger](base12-coverage-builder-fixture-derivation.json) retains exact identities; the [validation record](../../research/runs/base12-builder-fixture-derivation/validation.json) records original static checks.

## What supplies the expectations

The materializer was read in full and syntax-parsed without import or execution. Its imports are standard-library hashing, JSON, paths, regular expressions and struct packing. Its instruction collector requires explicit statement/expected-hex pairs. Fixed ELF/map fields are serialized separately; no candidate or seed encoder is imported. Some branch displacement bytes are calculated from explicit labels/positions. This is offline expectation construction, not a fresh native encoding result or an exhaustive independent ISA oracle.

Provenance records ten pinned inputs. Seven bind held bytes: the contract, three witness JSON records, symbolic runner and two tiny source texts. Historical runner ELF/listing/layout remain three unheld dependencies here. The generator, fixture-review and fixture-manifest identities also agree with their containing records. Shared contract assumptions and retained historical bytes remain explicit even when expectations were authored separately from the candidate implementation.

The historical-runner case checks source annotations, listing lengths, label positions and code bytes against its saved artifact. The combined finite-witness case preserves each literal branch displacement with explicit CLD padding and uniquely named labels. The two tiny cases reuse their hand-derived source/code/map expectations. Encoding-only and looping outputs are deliberately excluded from later execution eligibility. These are source-derived behaviors of the materializer; none was reproduced here by calling it.

## Guard reachability is part of case design

The endpoints preserve enough valid structure to reach their intended guard. The 1,024-instruction case also reaches 128 labels and 1,152 map records; the one-over instruction case rejects before creating another map row. The relocation boundary uses 256 five-byte jumps and one label, staying below earlier instruction/input/label limits. The 32-byte name intentionally reaches token-length rejection. The stable 65,537-byte regular input reaches the fstat size guard; it does not test concurrent growth or the read overflow probe.

The AST contains sixteen explicit malformed-source cases and sixteen numeric endpoint cases. Seven endpoint byte literals received bounded immediate/displacement field checks, all agreeing with their statements. Ten fault specifications enumerate exactly six EINTR and four EIO cases, including syscall occurrence, semantic target, retry return class and expected process status. These checks inspect authored data, not native parser progress or fault-instrumentation behavior.

Successful ELF/map comparisons, empty reservations, absent outputs and collision sentinels have distinct expectations. A byte-complete pair is still invalid on nonzero builder exit. Invalid-source counts describe textual intent rather than claiming that the parser reached those statements.

## Two failure mechanisms require different evidence

Injected EIO suppresses the syscall. In close cases, the descriptor can remain open until process exit even after the candidate clears its ownership flag. An expected EIO marker therefore does not establish successful close. The reported corrected controls require no retry of the failed target while permitting cleanup of a different descriptor. Ordinary full-I/O call counts are qualified: genuine short I/O can increase read/write counts without relaxing the exact injection target and retry requirements.

Case60 uses a child-only 4,096-byte file-size limit, default/unblocked SIGXFSZ, predicted signal termination, a 4,096-byte ELF prefix and empty map. It is untraced. Together these can support the intended partial-write inference if observed, but they do not directly record a positive syscall return. Parent logging retains a separate limit. The two later tiny executions remain conditional predictions, not preparation observations.

## Complete fixture list and publication scope

All 157 checksum entries were read and reconstructed exactly. They agree with the complete packet's fixture subset and the pinned tree. Including the checksum file, the fixture subtree has 158 paths / 729,210 bytes. Tree metadata yields maxima of 65,537 source bytes, 6,930 expected ELF bytes, 36,896 expected map bytes and 65,928 layout-JSON bytes. These are inventory calculations; current filesystem modes and runtime resources were not reobserved. The larger layout JSON is not an input to the driver's narrower source/ELF/map helper according to the retained review.

The materializer checks derivation before creating its fresh fixture directory, then writes files exclusively and applies modes one by one. This avoids overwriting an existing set but does not make directory publication atomic or crash durable. A partial set after interruption remains possible. No materializer, control, expected ELF or candidate program ran in this unit, and no binary was newly acquired.

Coverage reaches **519 distinct blobs / 4,003,056 bytes**, plus **77 identical alias paths**. The remaining full-reading gap is **4,997 paths / 3,910 distinct blobs**; historical global acquisition overlap remains unresolved.

Next: the complete 140,815-byte `fixtures/cases.json`, read as case metadata without execution. Check every case's exact expectations and counts before the planned commands or saved results. Reconcile fresh main and other workers first; no recipient has accepted that next unit. Separate storage, dispatch-reconciliation and public checkpoint lanes retain their ownership.
