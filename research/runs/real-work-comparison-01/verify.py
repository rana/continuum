#!/usr/bin/env python3
"""Check packet custody, source projections and actual case boundaries; no inference."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

def sha(data):
    return hashlib.sha256(data).hexdigest()

def redact(value):
    if isinstance(value,dict):return {k:redact(v) for k,v in value.items()}
    if isinstance(value,list):return [redact(v) for v in value]
    if isinstance(value,str) and value.startswith('/'):return '<absolute-path-omitted>'
    return value

def verify(packet, repo):
    manifest=json.loads((packet/'artifact-manifest.json').read_text())
    actual={str(p.relative_to(packet)) for p in packet.rglob('*') if p.is_file() and p.name!='artifact-manifest.json'}
    assert {x['path'] for x in manifest}==actual and len(manifest)==len(actual)
    for row in manifest:
        path=Path(row['path']);assert not path.is_absolute() and '..' not in path.parts
        data=(packet/path).read_bytes();assert len(data)==row['bytes'] and sha(data)==row['sha256']
        assert b'/home/' not in data and b'/root/' not in data and b'libfile_' not in data
    pins=json.loads((packet/'source-pins.json').read_text());assert len(pins)==10
    for row in pins:
        original=subprocess.check_output(['git','-C',str(repo),'show',row['commit']+':'+row['source_path']])
        assert len(original)==row['original_bytes'] and sha(original)==row['original_sha256']
        assert hashlib.sha1(b'blob '+str(len(original)).encode()+b'\0'+original).hexdigest()==row['git_blob']
        data=(packet/row['file']).read_bytes()
        if row['representation']=='exact source bytes':assert data==original
        else:assert row['representation']=='path-redacted JSON projection' and json.loads(data)==redact(json.loads(original))
    preparation=json.loads((packet/'preparation.json').read_text());assert preparation['model_receivers_invoked']==0 and preparation['receiver_dispatch_ready'] is False
    assert [x['local_anchor'] for x in preparation['cases']]==['matches_at_observation','matches_at_observation','stale_at_observation']
    assert preparation['adapter_processes']==13 and preparation['native_additional_processes']==13
    for index in range(1,4):
        case=packet/f'case-{index:02d}'
        observed=json.loads((case/'C-verification.json').read_text());common=json.loads((case/'common-observation.json').read_text())
        assert observed['exact_projection_verified'] is True and observed['action_authority_verified'] is False
        assert observed['freshness']['status']==common['local_anchor']
        assert (case/'C-context.jsonl').read_bytes()==(packet/'native/original/context.jsonl').read_bytes()
        assert json.loads((case/'B-records.json').read_text())==json.loads((packet/'native/original/work-state.json').read_text())
        menu=json.loads((case/'retrieval-menu.json').read_text())
        for path in menu['files']+[menu['current_accepted_state'],menu['source_pins'],menu['common_observation'],menu['verification_record']]:assert (packet/path).is_file()
        assert menu['verification_record']==f'case-{index:02d}/C-verification.json'
    log=json.loads((packet/'native/observations.json').read_text());assert len(log)==13 and all(x['exit_code']==0 for x in log)
    assert json.loads(log[0]['stdout'])==json.loads(log[1]['stdout'])
    assert json.loads(log[-1]['stdout'])['freshness']['status']=='stale_at_observation'
    return dict(source_pins=10,cases=3,adapter_processes=13,additional_native_processes=13,receiver_observations=0,
                checks=['all retained byte/hash identities','exact Git sources and declared path projections','shared proof access and case menu membership','actual native match/match/stale with exact historical validity'])

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--packet',type=Path,required=True);parser.add_argument('--repository',type=Path,required=True);args=parser.parse_args()
    print(json.dumps(verify(args.packet,args.repository),indent=2))
