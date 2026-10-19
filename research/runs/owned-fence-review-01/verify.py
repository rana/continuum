#!/usr/bin/env python3
"""Retained review exposure/metadata check; no inference or project writes."""
import hashlib
import json
import pathlib

root = pathlib.Path(__file__).resolve().parent
request_bytes = (root / 'request.json').read_bytes()
submitted = json.loads((root / 'submitted.json').read_text())
assert hashlib.sha256(request_bytes).hexdigest() == submitted['request_sha256']
request = json.loads(request_bytes)
pins = json.loads((root / 'source-pins.json').read_text())
context = request['context'].encode()
for source in pins['sources']:
    marker = f"Exact source {source['path']} at {pins['source_commit']}:\n".encode()
    assert context.count(marker) == 1
    start = context.index(marker) + len(marker)
    value = context[start:start + source['bytes']]
    assert hashlib.sha256(value).hexdigest() == source['sha256']
wrapper = json.loads((root / 'provider-result.json').read_text())
actual = wrapper['structuredContent']
retained = json.loads((root / 'result.json').read_text())
assert actual == {"status": "ERROR", "error_category": "output_budget_exhausted", "inference_outcome": "unknown", "upstream_http_status": 200, "error_code": "INVALID_ARGUMENT"}
assert retained['attempts'] == 1 and not retained['retry_attempted']
assert not retained['visible_answer_received'] and retained['actual_model'] is None and retained['usage'] is None
for key, value in actual.items():
    assert retained[key] == value
assert wrapper['isError'] is True and len(wrapper['content']) == 1
assert "before producing a visible answer" in wrapper['content'][0]['text']
print('PASS: four-module exposure, request digest and one unknown provider outcome retained; no review answer or retry claimed')
