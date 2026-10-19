"""Finite v1 semantic oracle: history projection, no journal/parser/SQLite imports.

Inputs are valid finite symbolic requests. This is not a full input validator or
canonical object codec. Roots A/B denote pre-existing valid Snapshot objects.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Request:
    operation: str
    candidate: str
    expected: tuple | None = None
    acceptor: str = 'local'
    target: str = 'main'


def evaluate(history, request):
    """Return (next immutable evaluated history, response).

    A history entry is (request, receipt); rejected identity conflicts and exact
    replays are not new evaluated entries. Head is derived only from previous
    accepted requests for this acceptor/target, never from a replay's result.
    """
    same_key = [item for item in history
                if (item[0].acceptor, item[0].operation) == (request.acceptor, request.operation)]
    if same_key:
        old_request, receipt = same_key[0]
        return history, ('conflict' if old_request != request else (receipt, True))
    accepted = [item for item in history
                if item[0].acceptor == request.acceptor and item[0].target == request.target
                and item[1]['outcome'] == 'accepted']
    observed = (accepted[-1][0].candidate, len(accepted)) if accepted else None
    matches = request.expected == observed
    resulting = (request.candidate, len(accepted) + 1) if matches else observed
    receipt = dict(sequence=len(history) + 1,
                   outcome='accepted' if matches else 'precondition_failed',
                   observed=observed, resulting=resulting)
    return history + ((request, receipt),), (receipt, False)
