"""Independent decision criteria for a post-commit fence response."""
import unittest
from fence_oracle import World, conservative_retry, effect_counts_after_retry, naive_retry, sweep


class FenceOracleTests(unittest.TestCase):
    def test_postcommit_fence_must_not_authorize_new_effect(self):
        w = World(True, False, False, True, True, "committed")
        self.assertTrue(naive_retry(w))
        self.assertFalse(conservative_retry(w))
        self.assertEqual(effect_counts_after_retry(w, True)[0], 2)

    def test_precommit_authoritative_fence_permits_replay(self):
        w = World(False, False, False, True, True, "none_committed")
        self.assertTrue(conservative_retry(w))
        self.assertEqual(effect_counts_after_retry(w, True)[0], 1)

    def test_unknown_outcome_holds_even_with_fence(self):
        w = World(False, False, False, True, True, "unknown")
        self.assertFalse(conservative_retry(w))

    def test_fence_without_future_effect_proof_holds(self):
        w = World(False, True, False, True, False, "none_committed")
        self.assertFalse(conservative_retry(w))

    def test_downstream_non_idempotent_effect_holds(self):
        w = World(False, False, True, False, True, "none_committed")
        self.assertFalse(conservative_retry(w))
        self.assertEqual(effect_counts_after_retry(w, True)[1], 2)

    def test_downstream_effect_under_dedup_is_not_duplicate(self):
        w = World(False, False, True, True, True, "none_committed")
        self.assertTrue(conservative_retry(w))

    def test_sweep_discovers_wrong_admissions(self):
        worlds = sweep()
        self.assertGreaterEqual(len(worlds), 30)
        bad = [w for w in worlds if naive_retry(w) and not conservative_retry(w)]
        self.assertTrue(any(w.prior_provider_effect for w in bad))
        self.assertTrue(any(w.prior_downstream_effect and not w.downstream_idempotent for w in bad))
        self.assertFalse(any(conservative_retry(w) and (w.prior_provider_effect or w.possible_future_old_effect) for w in worlds))


if __name__ == "__main__":
    unittest.main()
