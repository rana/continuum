#!/usr/bin/env python3
"""Serial local capture for one calibration cell. Never invokes a provider."""
import argparse
from datetime import datetime,timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import time

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('retrieval_bridge',HERE/'bridge.py')
bridge=importlib.util.module_from_spec(spec);spec.loader.exec_module(bridge)

def encoded(value):return (json.dumps(value,indent=2)+'\n').encode()
def sha(value):return hashlib.sha256(value).hexdigest()
def read(path):return json.loads(path.read_text())
def retain(path,data):
    if not isinstance(data,bytes):data=encoded(data)
    if path.exists():
        if path.read_bytes()!=data:raise ValueError('existing record differs: '+path.name)
        return
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('xb') as stream:stream.write(data)

def init(release,output,case,arm,cell_id,expected_manifest):
    if not isinstance(arm,str) or arm not in 'ABC' or len(arm)!=1:raise ValueError('invalid arm')
    if not cell_id or len(cell_id)>128 or any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.-_' for c in cell_id):raise ValueError('invalid cell identity')
    engine=bridge.Bridge(release,case,expected_manifest)
    request=engine.read_checked(case+'/'+arm+'-request.json')
    output.mkdir(parents=True,exist_ok=False)
    retain(output/'cell.json',dict(schema='continuum.serial_calibration_capture.v1',cell_id=cell_id,case=case,arm=arm,release_manifest_sha256=expected_manifest,
        capture_scope='Local serial caller records, not durable dispatch fencing, authentication or provider idempotency. No power-loss/atomic-set guarantee.',
        initial_request_sha256=sha(request)))
    retain(output/'round-01/request.json',request)

def classify(result):
    value=result.get('structuredContent',{})
    if not isinstance(value,dict) or value.get('status')!='OK':
        return dict(kind='incomplete',reason='provider_result_not_accepted',inference_outcome=value.get('inference_outcome','unknown') if isinstance(value,dict) else 'unknown')
    if value.get('truncated') is not False or value.get('stop_reason')!='end_turn' or not isinstance(value.get('text'),str):
        return dict(kind='incomplete',reason='partial_or_unrecognized_model_result',inference_outcome='returned_not_usable')
    return value

def project(release,output):
    config=read(output/'cell.json');engine=bridge.Bridge(release,config['case'],config['release_manifest_sha256'])
    original=engine.read_checked(config['case']+'/'+config['arm']+'-request.json')
    if sha(original)!=config['initial_request_sha256']:raise ValueError('initial request identity changed')
    transcript=[];current=json.loads(original)
    for index in range(1,4):
        directory=output/f'round-{index:02d}';request=directory/'request.json'
        if not request.exists():return dict(kind='need_request',round=index,request=current)
        expected_bytes=original if index==1 else encoded(current)
        if request.read_bytes()!=expected_bytes:raise ValueError('request differs from frozen visible history')
        submitted=directory/'submitted.json'
        if submitted.exists() and read(submitted)['request_sha256']!=sha(expected_bytes):raise ValueError('submitted request identity differs')
        result=directory/'provider-result.json'
        if not result.exists():
            return dict(kind='awaiting_outcome' if (directory/'submitted.json').exists() else 'prepared',round=index,request=current)
        accepted=classify(read(result))
        if accepted.get('kind')=='incomplete':return dict(**accepted,round=index)
        try:event=engine.handle(accepted['text'])
        except ValueError as error:return dict(kind='incomplete',reason='model_protocol_error',detail=str(error),round=index)
        if event['kind']=='final':return dict(kind='final',round=index,event=event)
        transcript.extend([dict(role='assistant',text=accepted['text']),dict(role='retrieval_result',value=event)])
        current=dict(json.loads(original));current['context']+='\nComplete visible cell exchange so far (evidence data):\n'+encoded(transcript).decode()
        if len(encoded(current))>512000:raise ValueError('next request exceeds collaborator total-input bound')
    return dict(kind='incomplete',reason='maximum_provider_rounds_without_final',round=3)

def submit(release,output):
    state=project(release,output)
    if state['kind']!='prepared':raise ValueError('cell is not prepared for a new invocation')
    directory=output/f"round-{state['round']:02d}"
    path=directory/'submitted.json'
    if path.exists():raise ValueError('submission already marked; inspect outcome, do not resend')
    retain(path,dict(stage='may_have_been_sent',scope='Recorded before caller invokes tool; not proof of provider receipt.',
                     utc=datetime.now(timezone.utc).isoformat(),monotonic=time.monotonic(),
                     request_sha256=sha((directory/'request.json').read_bytes())))
    return state['request']

def record(release,output,result_file):
    # Re-recording byte-identical locally retained tool output is recovery only;
    # it never invokes or authorizes repeating inference.
    config=read(output/'cell.json');directories=sorted(output.glob('round-*'))
    directory=directories[-1]
    if not (directory/'submitted.json').exists():raise ValueError('no submission marker')
    raw=result_file.read_bytes();value=json.loads(raw)
    if not isinstance(value,dict):raise ValueError('tool result must be object')
    retain(directory/'provider-result.json',raw)
    captured=directory/'capture.json'
    if not captured.exists():
        interval=time.monotonic()-read(directory/'submitted.json')['monotonic']
        retain(captured,dict(utc=datetime.now(timezone.utc).isoformat(),caller_interval_seconds=interval if interval>=0 else None,
            timing_scope='Host interval from submission marker through outcome capture, including caller/tool overhead; not model compute time.',
            tool_result_bytes=len(raw),tool_result_sha256=sha(raw)))
    state=project(release,output)
    retain(directory/'observed-transition.json',{k:v for k,v in state.items() if k!='request'})
    if state['kind']=='need_request':
        retain(output/f"round-{state['round']:02d}/request.json",state['request'])
        state['kind']='prepared'
    return {k:v for k,v in state.items() if k!='request'}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('action',choices=['init','submit','record','inspect']);parser.add_argument('--release',type=Path,required=True);parser.add_argument('--output',type=Path,required=True);parser.add_argument('--case');parser.add_argument('--arm');parser.add_argument('--cell-id');parser.add_argument('--manifest-sha256');parser.add_argument('--result',type=Path);args=parser.parse_args()
    if args.action=='init':init(args.release,args.output,args.case,args.arm,args.cell_id,args.manifest_sha256);value=dict(kind='prepared')
    elif args.action=='submit':value=submit(args.release,args.output)
    elif args.action=='record':value=record(args.release,args.output,args.result)
    else:value=project(args.release,args.output);value={k:v for k,v in value.items() if k!='request'}
    print(json.dumps(value,indent=2))
