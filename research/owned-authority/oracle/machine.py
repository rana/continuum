"""Separate mutable map implementation, with explicit deliberate defect switches."""


class Machine:
    def __init__(self, mutant=None):
        self.heads, self.receipts, self.sequence = {}, {}, 0
        self.mutant = mutant

    def apply(self, request):
        identity = (request.acceptor, request.operation)
        if self.mutant == 'target_scoped_operation':
            identity += (request.target,)
        key = (request.acceptor, request.target)
        current = self.heads.get(key)
        if identity in self.receipts:
            old, receipt = self.receipts[identity]
            if old != request and self.mutant != 'changed_request_ignored':
                return 'conflict'
            if self.mutant == 'retry_uses_current':
                receipt = dict(receipt, observed=current, resulting=current)
            return receipt, True
        equal = current == request.expected
        if self.mutant == 'root_only' and current and request.expected:
            equal = current[0] == request.expected[0]
        following = (request.candidate, (current[1] if current else 0) + 1) if equal else current
        if self.mutant != 'sequence_only_success' or equal:
            self.sequence += 1
        receipt = dict(sequence=self.sequence,
                       outcome='accepted' if equal else 'precondition_failed',
                       observed=current, resulting=following)
        if equal:
            self.heads[key] = following
        if equal or self.mutant != 'stale_not_retained':
            self.receipts[identity] = request, receipt
        return receipt, False
