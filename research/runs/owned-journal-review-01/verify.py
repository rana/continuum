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
assert actual['status'] == 'OK' and actual['stop_reason'] == 'end_turn' and not actual['truncated']
assert actual['usage'] == retained['usage'] and actual['actual_model'] == retained['actual_model']
assert wrapper['content'][0]['text'] == actual['text']
assert retained['attempts'] == 1
print('PASS: exact three-module exposure, request digest, one complete actual review and returned usage retained; no inference performed')
