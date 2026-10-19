# Reference-decoder launcher and receipt reconciliation

Reviewed 2026-10-19 UTC at private Base12 commit `88382e793b65c84fd8e223840c27f6bb8682864a`, tree `5cf96129bdcb0dde075f6f5800ae0c68a95c4b82`. Eight texts / 23,272 bytes were fully read: six attempt/clearance/source/freeze/execution/postrun JSON records, the launcher, and its review. The [ledger](base12-coverage-reference-launcher.json) records exact identities. The launcher was parsed as syntax, never imported or executed. No historical decoder, acquisition or inference was replayed.

## Research Delta: zero exit does not erase a violated condition

The saved launcher review describes a pre-execution correction: a deadline could expire, then the child could naturally exit zero while termination and waiting raced. A success branch based only on the eventual exit code could overwrite the timeout. In the retained final source, the deadline exception first records `wall_timeout`; a later branch checks that status before considering exit code or output acceptance. A zero exit therefore cannot enter its ordinary success branch after that recorded timeout.

Source locations make the mechanism reviewable: timeout status is assigned at line 119, checked at line 125, and ordinary pass assigned at line 141. The final launcher's bytes match its freeze. Only the earlier launcher's digest and the attributed correction account are retained in this unit; its original failed-version bytes were not acquired. No deadline race was exercised, so this is static confirmation of the final branch order, not a reproduced timeout test or proof of every exception path.

Continuum should keep independently required acceptance conditions distinct from a worker's exit code. A later successful-looking output cannot erase a deadline or other terminal restriction already recorded for the attempt. The final decision needs those conditions together; replacing one with the last observed field can promote an unacceptable attempt.

## Research Delta: receipts describe a phase of an effect

Every shared attempt/execution field except status agrees exactly, including command, environment, limits, before-identities, clearance and interpreter metadata. The execution record's before/after file identities and modes agree. Both clearance copies agree; source receipt and launcher freeze match acquired payloads; the launcher's literal source/input/output pins, limits and interpreter digest reconcile with the receipts. The input archive and original-file identities also agree with the earlier saved encoding result. These checks compare retained records and acquired source, not the excluded signal payloads or the historical interpreter binary.

Both output sizes, hashes and direct-equality flags agree across execution and postrun records. Execution reports mode 0600 while postrun reports 0400. The source records each output's metadata at line 136, then changes its mode at line 140. The later postrun check sees the resulting permission state. The two entries concern different phases rather than contradictory file identities. Neither output payload was retrieved here.

For Continuum, an observation should retain its point in the operation. A later permission, publication or acceptance transition belongs in later evidence; rewriting earlier observations would destroy chronology. Metadata collected by a supervisor also retains that collector's scope: for example, the launcher's version string comes from its own `sys.version`, while the child command separately pins an executable digest. This unit does not infer a fresh child-version query from that field.

## Attempt and supervision boundaries

The exclusive marker at line 101 is flushed and fsynced at line 105 before `Popen` at line 112. Fresh-directory creation and exclusive marker creation prevent ordinary reuse through this launcher. They do not establish global exactly-once execution, receiver fencing, or power-loss recovery. The final execution receipt uses exclusive creation but is not fsynced by this source. An absent final receipt would not prove that no child ran.

The source sets explicit per-process resource limits and a process-group wall timeout, uses isolated child Python arguments, and cleans up the group on ordinary completion or catchable exceptions. These are source-inspected mechanisms for the trusted fixed decoder, not general adversarial isolation. Cleanup depends on a live supervisor; an uncatchable supervisor loss cannot run its cleanup. Path checks and subsequent reads/exec still assume stable trusted paths. No cancellation, crash, power-loss or hostile-path experiment was performed.

The historical execution receipt records pass/zero exit and accepted output checks. This supports a reconciled historical record under the stated collection conditions, not authenticated worker identity or new execution evidence. The [validation record](../../research/runs/base12-reference-launcher/validation.json) separates the actual checks, source lines and untested conditions.

Reference-packet custody now reaches **13/17 evidence-manifest entries** and **14/19 preservation entries**, each including one pinned empty-payload alias admitted only mechanically. Four unread texts and the original evidence archive remain outside current custody checks. The preceding original encoding packet's complete bindings remain unchanged. No private payload, operational path or collaborator identifier is published.

Cumulative full semantic reading reaches **266 distinct blobs / 1,747,612 bytes**, plus **49 byte-identical alias paths**: 315 covered paths. **5,278 paths / 4,163 distinct blobs** remain without complete semantic-reading claims. The historical global acquisition aggregate remains unchanged because its overlap index is unavailable. Public CI checks this contribution and existing behavior, not private reading or historical execution.

Next bounded unit: read the remaining draft reply, stdout, package review and result review / 14,253 bytes, then mechanically inspect the 17,888-byte reference evidence archive against installed members. Reconcile current main and ownership first; replay no effect. A new remote owned-journal branch was observed with no commits beyond current main at this reconciliation; that does not establish worker inactivity or transfer its ownership. The owned-storage lane remains separate, and no recipient has accepted this next unit.
