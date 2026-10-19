# Stage-A execution receipts: reconcile effects without replay

Reviewed 2026-10-19 UTC at private Base12 commit `88382e793b65c84fd8e223840c27f6bb8682864a`, tree `5cf96129bdcb0dde075f6f5800ae0c68a95c4b82`. Six JSON documents / 22,004 bytes under the stage-A retained run evidence were fully read: delivery manifest, acquisition receipt, consumed-attempt record, exit receipt, input/code record and postrun verification. Exact source identities are in the [ledger](base12-coverage-stage-a-execution.json).

No upstream code, acquisition, codec, benchmark or model ran. No dataset waveform/header payload or run output archive was retrieved. Historical command paths, clearance identities and operational payload contents remain private. These are checks of retained source-authored receipts, not authentication of a sender, host or scientific execution.

## Research Delta: an attempt marker and an outcome answer different questions

The consumed-attempt record and exit receipt agree on all common fields except their deliberately different status: declared clearance, command, working directory, environment, limits, start timestamp and warning. The intake record carries the same clearance. The exit receipt reports return code zero and a completed interval; the postrun record describes saved-file verification rather than another codec run.

This is coherent linked evidence for the reported history. A consumed marker by itself would not distinguish a failed launch, an uncertain running process or a completed effect whose reply was lost. The exit and postrun records add different observations; matching copies of shared fields are not independent confirmations. This unit does not inspect the launcher implementation, live process or original payloads, so it does not establish enforcement, idempotency or current worker acceptance.

Continuum should preserve the attempted operation and its observed outcome separately, keeping the exact request/source binding. Reconcile those records before deciding whether a new invocation is appropriate. Historical clearance recorded in a receipt does not grant another invocation or confer authority on this reader. No consumed run was repeated.

## Research Delta: metadata knowledge is not payload exposure

The input record contains ninety-six source hash entries but declares only one waveform/header pair accessed. Its manifest digest agrees with the acquisition record; the pair's hash declarations agree across intake, source inventory and accessed-payload fields. The split is disjoint with 32/8/8 recordings and retains the documented same-subject pair in training. The record explicitly leaves long-overlap checking unperformed.

Those checks reconcile declarations, not ninety-six acquired payloads or corpus-wide independence. Even the empty duplicate-hash groups describe the recorded checksum inventory rather than a fresh comparison of every source file. A continuation benchmark should record what was listed, what bytes were actually retrieved, what interpretation was exposed, and what checks ran. A source manifest can be available without making its whole population observed training data.

The four reported intake sizes sum to 2,046,316 bytes, below the declared 4 MiB budget. That arithmetic does not prove a network cap was enforced or establish the contents of bytes not retrieved here. Dataset identity and format facts remain attributed historical observations, without new external-source verification or clinical inference.

## Research Delta: budgets and accounting require their actual scope

The exit/attempt records explicitly distinguish per-process CPU/address-space limits from a process-group wall timeout. Those are not an aggregate process-tree compute/memory quota. The exit record's reported usage and timing are not this workstation's current utilization or a new performance measurement. Launcher enforcement is a separate source question selected next.

Postrun arithmetic is internally consistent: 234 metadata/digest bytes + 1,908 subframe-header bytes + 671,270 payload bytes = 673,412 archive bytes. The header count is 318 times six bytes, and meaningful plus padding bits equals eight times the coded payload bytes. The postrun input/code digest also matches the exact input record acquired here. Other private artifacts named there, including reconstructed files and binary archives, were not retrieved or revalidated.

This supports exact reported accounting without upgrading it to fresh reconstruction or comparative throughput. Continuum should keep the measured boundary, resource-limit scope, payload-accounting unit and execution environment attached to any result it reuses.

## Validation, remaining custody and continuation

All six acquired JSON byte strings match the pinned tree's Git blob and length; raw SHA-256 was recomputed and full data read. Five of the delivery manifest's twenty-seven entries match acquired payloads; twenty-two remain unchecked here. Cumulative acquired checks against the earlier forty-nine-entry preservation manifest now reach twenty, leaving twenty-nine explicit gaps. Four run source hashes match acquired source bytes; two vendor entries were not rebound. These are overlapping identity checks, not new experiments. The [validation record](../../research/runs/base12-stage-a-execution/validation.json) lists each checked and unchecked entry.

Cumulative direct reading is **230 distinct blobs / 1,530,017 bytes**, plus **48 byte-identical alias paths**. This covers 278 paths by reading or byte equality; **5,315 paths / 4,199 distinct blobs** remain without complete semantic-reading claims. Alias directory context is not separately reviewed. The earlier acquisition aggregate remains historical at 539 paths / 530 blobs / 4,536,603 path bytes because its full overlap index was not recovered. New fetches are not blindly added. Hosted CI checks the public contribution, not private reading, inaccessible payloads or historical enforcement.

Next bounded unit: seven unread files / 21,611 bytes in the same retained `review/` directory: the launcher and acquisition source, launcher review/freeze, parent clearance, environment and intake verification. Reconcile fresh main and ownership; inspect source without importing or running it. No recipient has accepted this unit; the separate owned-storage model lane retains its ownership.
