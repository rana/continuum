#!/usr/bin/env python3
"""Finite synthetic oracle for uncertain external-effect dispatch.

No network I/O, providers, credentials, subprocesses, or live dispatch.
This models one logical request with at most one original send.  An
unobserved original may still be in flight.  Provider evidence types
are assumed authentic and request-bound only when explicitly named.
"""
from dataclasses import dataclass
from enum import Enum
import json


class Evidence(str, Enum):
    NEVER_SENT = "verified_never_sent"
    PREFLIGHT_REJECTED = "verified_preflight_rejected"
    UNKNOWN = "outcome_unknown"
    NOT_FOUND_NOW = "point_in_time_not_found"
    FINAL_ABSENCE = "authoritative_final_no_effect"
    EFFECT_FOUND = "authoritative_effect_found"


class Decision(str, Enum):
    FIRST_SEND = "first_send"
    REPLAY = "exact_replay"
    HOLD = "hold_and_reconcile"
    REPAIR = "repair_under_new_identity"
    RECONCILE = "reconcile_existing_effect"
    OUTPUT = "use_validated_output"
    REJECT = "reject_changed_request_identity"


@dataclass(frozen=True)
class World:
    effect_already_committed: bool
    original_still_in_flight: bool


POSSIBLE_WORLDS = {
    Evidence.NEVER_SENT: (World(False, False),),
    Evidence.PREFLIGHT_REJECTED: (World(False, False),),
    Evidence.UNKNOWN: (World(False, False), World(False, True), World(True, False)),
    Evidence.NOT_FOUND_NOW: (World(False, False), World(False, True)),
    Evidence.FINAL_ABSENCE: (World(False, False),),
    Evidence.EFFECT_FOUND: (World(True, False),),
}


@dataclass(frozen=True)
class Case:
    evidence: Evidence
    exact_request_identity: bool
    durable_exact_idempotency: bool
    # A usable result requires separately validated response/receipt binding.
    validated_output: bool = False
    # HTTP status is transport metadata, not an effect/answer certificate.
    upstream_http_200: bool = False


def decide(case: Case) -> Decision:
    if not case.exact_request_identity:
        return Decision.REJECT
    if case.evidence is Evidence.EFFECT_FOUND:
        return Decision.OUTPUT if case.validated_output else Decision.RECONCILE
    if case.evidence is Evidence.NEVER_SENT:
        return Decision.FIRST_SEND
    if case.evidence is Evidence.PREFLIGHT_REJECTED:
        return Decision.REPAIR
    if case.evidence is Evidence.FINAL_ABSENCE:
        return Decision.REPLAY
    if case.durable_exact_idempotency:
        return Decision.REPLAY
    return Decision.HOLD


def max_effects_after_decision(case: Case, action: Decision) -> int:
    """Adversarial upper bound: pending original *and* a replay may commit.

    Exact idempotency is a stated hypothetical provider guarantee, never
    inferred from a shared key or status code; its retention/scope must
    be separately verified before setting the capability to True.
    """
    worst = 0
    for world in POSSIBLE_WORLDS[case.evidence]:
        original = int(world.effect_already_committed or world.original_still_in_flight)
        extra = int(action in (Decision.FIRST_SEND, Decision.REPLAY))
        if extra and case.durable_exact_idempotency and case.exact_request_identity:
            after = max(original, extra)
        else:
            after = original + extra
        worst = max(worst, after)
    return worst


def check_case(case: Case, action: Decision) -> tuple[bool, str]:
    if not case.exact_request_identity:
        return (action is Decision.REJECT, "changed_operation_identity")
    if action in (Decision.FIRST_SEND, Decision.REPLAY) and max_effects_after_decision(case, action) > 1:
        return (False, "duplicate_possible")
    if action is Decision.OUTPUT and (case.evidence is not Evidence.EFFECT_FOUND or not case.validated_output):
        return (False, "unbound_or_missing_output")
    if case.evidence is Evidence.EFFECT_FOUND and action not in (Decision.OUTPUT, Decision.RECONCILE):
        return (False, "failed_effect_reconciliation")
    # Availability under adequate evidence, separate from safety.
    if case.evidence is Evidence.NEVER_SENT and action is not Decision.FIRST_SEND:
        return (False, "first_send_unavailable")
    if case.evidence is Evidence.FINAL_ABSENCE and action is not Decision.REPLAY:
        return (False, "final_absence_unavailable")
    if case.evidence is Evidence.PREFLIGHT_REJECTED and action is not Decision.REPAIR:
        return (False, "preflight_repair_unavailable")
    if case.evidence in (Evidence.UNKNOWN, Evidence.NOT_FOUND_NOW):
        if case.durable_exact_idempotency and action is not Decision.REPLAY:
            return (False, "idempotent_replay_unavailable")
        if not case.durable_exact_idempotency and action is not Decision.HOLD:
            return (False, "uncertain_outcome_must_be_reconciled")
    return (True, "pass")


def cases():
    for ev in Evidence:
        for same in (False, True):
            for idem in (False, True):
                for validated in (False, True):
                    for http_200 in (False, True):
                        yield Case(ev, same, idem, validated, http_200)


def mutant_retry_unknown(c):
    return Decision.REPLAY if c.evidence is Evidence.UNKNOWN else decide(c)


def mutant_retry_not_found(c):
    return Decision.REPLAY if c.evidence is Evidence.NOT_FOUND_NOW else decide(c)


def mutant_trust_http_200(c):
    return Decision.OUTPUT if c.upstream_http_200 else decide(c)


def mutant_ignore_request_binding(c):
    if not c.exact_request_identity:
        return Decision.REPLAY
    return decide(c)


def mutant_always_hold(c):
    return Decision.HOLD


def mutant_effect_equals_output(c):
    return Decision.OUTPUT if c.evidence is Evidence.EFFECT_FOUND else decide(c)


MUTANTS = {
    "blind_retry_unknown": mutant_retry_unknown,
    "retry_point_in_time_absence": mutant_retry_not_found,
    "http_200_equals_valid_output": mutant_trust_http_200,
    "ignore_changed_request_identity": mutant_ignore_request_binding,
    "always_hold": mutant_always_hold,
    "effect_equals_usable_output": mutant_effect_equals_output,
}


def verify_all():
    corpus = list(cases())
    base_bad = [(c, check_case(c, decide(c))) for c in corpus if not check_case(c, decide(c))[0]]
    witnesses = {}
    expected = {
        "blind_retry_unknown": "duplicate_possible",
        "retry_point_in_time_absence": "duplicate_possible",
        "http_200_equals_valid_output": "unbound_or_missing_output",
        "ignore_changed_request_identity": "changed_operation_identity",
        "always_hold": "first_send_unavailable",
        "effect_equals_usable_output": "unbound_or_missing_output",
    }
    for label, mutant in MUTANTS.items():
        for case in corpus:
            action = mutant(case)
            good, reason = check_case(case, action)
            # Prefer a witness of the mutant's specific faulty claim, not an
            # unrelated invariant violated by an artificial cross-product.
            if (not good and reason == expected[label]
                    and (label != "http_200_equals_valid_output" or case.evidence is Evidence.UNKNOWN)):
                witnesses[label] = {
                    "evidence": case.evidence.value,
                    "exact_request_identity": case.exact_request_identity,
                    "durable_exact_idempotency": case.durable_exact_idempotency,
                    "validated_output": case.validated_output,
                    "upstream_http_200": case.upstream_http_200,
                    "mutant_action": action.value,
                    "reason": reason,
                    "worst_case_effects": max_effects_after_decision(case, action),
                }
                break
    return {
        "schema": "continuum.uncertain_dispatch_model.v1",
        "synthetic_cases": len(corpus),
        "oracle_failures": len(base_bad),
        "mutants_tested": len(MUTANTS),
        "mutants_rejected": len(witnesses),
        "first_discriminating_counterexample_by_enumeration": witnesses,
        "world_assumptions": ["single original send", "inflight send can commit after not-found", "authentic request-bound finality and effect-found signals", "idempotency is a verified provider guarantee if enabled", "validated output is separately bound to the effect and request"],
    }


if __name__ == "__main__":
    print(json.dumps(verify_all(), indent=2, sort_keys=True))
