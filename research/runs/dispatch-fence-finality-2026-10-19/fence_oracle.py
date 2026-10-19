"""Finite counterexample oracle for effect-bearing replay fences.

Models logical provider/downstream effect counts, not a live API or a runner.
"""
from dataclasses import dataclass
from itertools import product


@dataclass(frozen=True)
class World:
    prior_provider_effect: bool
    possible_future_old_effect: bool
    prior_downstream_effect: bool
    downstream_idempotent: bool
    fence_proves_no_future_old_effect: bool
    fence_report: str  # absent, unknown, none_committed, committed


def naive_retry(w: World) -> bool:
    """Mutant: treats a no-future-effect fence as proof nothing ever happened."""
    return w.fence_proves_no_future_old_effect


def conservative_retry(w: World) -> bool:
    """Requires an outcome-bearing fence and downstream-effect closure."""
    return (w.fence_proves_no_future_old_effect
            and w.fence_report == "none_committed"
            and (not w.prior_downstream_effect or w.downstream_idempotent))


def valid(w: World) -> bool:
    """Only accept claimed receipts consistent with the synthetic world."""
    if w.fence_proves_no_future_old_effect and w.possible_future_old_effect:
        return False
    if w.fence_report == "none_committed" and w.prior_provider_effect:
        return False
    if w.fence_report == "committed" and not w.prior_provider_effect:
        return False
    return True


def effect_counts_after_retry(w: World, retry: bool) -> tuple[int, int]:
    """Worst case: possible original effects occur, replay causes one new effect."""
    prior = int(w.prior_provider_effect)
    future = int(w.possible_future_old_effect)
    provider = prior + future + int(retry)
    downstream = int(w.prior_downstream_effect) + int(retry and not w.downstream_idempotent)
    return provider, downstream


def sweep():
    cases = []
    for pe, future, downstream, sink, fence in product((False, True), repeat=5):
        for report in ("absent", "unknown", "none_committed", "committed"):
            w = World(pe, future, downstream, sink, fence, report)
            if valid(w):
                cases.append(w)
    return cases


if __name__ == "__main__":
    all_cases = sweep()
    false_positive = [w for w in all_cases if naive_retry(w) and not conservative_retry(w)]
    committed_fence = World(True, False, False, True, True, "committed")
    assert committed_fence in false_positive
    print(f"valid_synthetic_worlds={len(all_cases)} blind_fence_false_admissions={len(false_positive)}")
    print("post_commit_fence_example:", committed_fence)
    print("naive:", effect_counts_after_retry(committed_fence, naive_retry(committed_fence)))
    print("conservative:", effect_counts_after_retry(committed_fence, conservative_retry(committed_fence)))
