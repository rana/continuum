import unittest
from model import Case, Decision, Evidence, check_case, decide, verify_all, max_effects_after_decision


class DispatchModelTest(unittest.TestCase):
    def test_finite_oracle_and_mutants(self):
        result = verify_all()
        self.assertEqual(result["synthetic_cases"], 96)
        self.assertEqual(result["oracle_failures"], 0)
        self.assertEqual(result["mutants_tested"], 6)
        self.assertEqual(result["mutants_rejected"], 6)
        self.assertEqual(set(result["first_discriminating_counterexample_by_enumeration"]), {
            "blind_retry_unknown", "retry_point_in_time_absence", "http_200_equals_valid_output",
            "ignore_changed_request_identity", "always_hold", "effect_equals_usable_output",
        })

    def test_lost_ack_cannot_justify_another_ordinary_send(self):
        c = Case(Evidence.UNKNOWN, True, False, upstream_http_200=True)
        self.assertEqual(decide(c), Decision.HOLD)
        self.assertEqual(max_effects_after_decision(c, Decision.REPLAY), 2)

    def test_point_in_time_not_found_may_precede_late_commit(self):
        c = Case(Evidence.NOT_FOUND_NOW, True, False)
        self.assertEqual(decide(c), Decision.HOLD)
        self.assertEqual(max_effects_after_decision(c, Decision.REPLAY), 2)

    def test_authoritative_final_absence_allows_replay(self):
        c = Case(Evidence.FINAL_ABSENCE, True, False)
        self.assertEqual(decide(c), Decision.REPLAY)
        self.assertEqual(max_effects_after_decision(c, Decision.REPLAY), 1)

    def test_hypothetical_idempotency_works_only_for_exact_binding(self):
        self.assertEqual(decide(Case(Evidence.UNKNOWN, True, True)), Decision.REPLAY)
        self.assertEqual(decide(Case(Evidence.UNKNOWN, False, True)), Decision.REJECT)

    def test_effect_receipt_without_useful_answer_requires_reconciliation(self):
        self.assertEqual(decide(Case(Evidence.EFFECT_FOUND, True, False)), Decision.RECONCILE)
        self.assertEqual(decide(Case(Evidence.EFFECT_FOUND, True, False, validated_output=True)), Decision.OUTPUT)
        good, why = check_case(Case(Evidence.EFFECT_FOUND, True, False), Decision.OUTPUT)
        self.assertFalse(good)
        self.assertEqual(why, "unbound_or_missing_output")

    def test_confirmed_local_rejection_does_not_keep_changed_identity(self):
        self.assertEqual(decide(Case(Evidence.PREFLIGHT_REJECTED, True, False)), Decision.REPAIR)
        self.assertEqual(decide(Case(Evidence.PREFLIGHT_REJECTED, False, False)), Decision.REJECT)

    def test_no_dispatch_is_a_live_action_not_a_terminal_block(self):
        c = Case(Evidence.NEVER_SENT, True, False)
        self.assertEqual(decide(c), Decision.FIRST_SEND)
        self.assertEqual(check_case(c, decide(c)), (True, "pass"))


if __name__ == "__main__":
    unittest.main()
