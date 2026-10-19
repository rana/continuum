#!/usr/bin/env python3
"""Verify the actual incomplete first cell without replaying inference."""
import hashlib
import importlib.util
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('first_cell_capture',HERE/'cell.py');cell=importlib.util.module_from_spec(spec);spec.loader.exec_module(cell)

def verify():
    output=HERE/'cells/case-01-A-01';round1=output/'round-01'
    config=json.loads((output/'cell.json').read_text());validation=json.loads((HERE/'release-validation.json').read_text())
    assert config['case']=='case-01' and config['arm']=='A'
    assert config['release_manifest_sha256']==validation['release_manifest_sha256']
    request=(round1/'request.json').read_bytes()
    assert request==(HERE/'release/case-01/A-request.json').read_bytes()
    assert hashlib.sha256(request).hexdigest()==config['initial_request_sha256']==json.loads((round1/'submitted.json').read_text())['request_sha256']
    result=(round1/'provider-result.json').read_bytes();assert result==(round1/'provider-returned.json').read_bytes()
    capture=json.loads((round1/'capture.json').read_text());assert len(result)==capture['tool_result_bytes'] and hashlib.sha256(result).hexdigest()==capture['tool_result_sha256']
    metadata=json.loads(result)['structuredContent'];assert metadata==dict(status='ERROR',error_category='invalid_response',inference_outcome='unknown',upstream_http_status=200,error_code='INVALID_ARGUMENT')
    state=cell.project(HERE/'release',output)
    assert state==dict(kind='incomplete',reason='provider_result_not_accepted',inference_outcome='unknown',round=1)
    assert json.loads((round1/'observed-transition.json').read_text())==state
    assert not (output/'round-02').exists()
    return dict(tool_invocation_attempts=1,accepted_receiver_answers=0,observed_retrieval_requests=0,rater_calls=0,
                inference_outcome='unknown',provider_usage=None,actual_model=None,automatic_retries=0,
                initial_request_bytes=len(request),tool_result_bytes=len(result),caller_interval_seconds=capture['caller_interval_seconds'],
                timing_scope=capture['timing_scope'],request_sha256=hashlib.sha256(request).hexdigest(),tool_result_sha256=hashlib.sha256(result).hexdigest())

if __name__=='__main__':print(json.dumps(verify(),indent=2))
