#!/usr/bin/env python3
"""Prepare frozen public-source cases and real local native observations; no inference."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import time

BASE = 'cedade61fbc377519dce68829679c954399bc854'
FIX = 'f00b13562398c7fc61775c49b6c2fad882d0bf2f'
CODE = ['src/store.rs', 'src/main.rs', 'examples/probe_reader_reservation.rs']

def digest(data):
    return hashlib.sha256(data).hexdigest()

def encode(value):
    return (json.dumps(value, indent=2) + '\n').encode()

def prepare(repo, binary, output):
    started = time.monotonic()
    repo, binary, output = repo.resolve(), binary.resolve(), output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    def save(name, value):
        path = output / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(value if isinstance(value, bytes) else encode(value))
        return path
    pins = []
    source_sets = {}
    for label, revision, lane in [('before', BASE, 'read-writer-reservation'), ('after', FIX, 'read-only-store')]:
        paths = CODE + [f'research/runs/{lane}/README.md', f'research/runs/{lane}/result.json']
        source_sets[label] = []
        for index, path in enumerate(paths):
            original = subprocess.check_output(['git', '-C', str(repo), 'show', revision + ':' + path])
            data = original
            redacted = []
            if path.endswith('/result.json'):
                def projection(value):
                    if isinstance(value, dict): return {k:projection(v) for k,v in value.items()}
                    if isinstance(value, list): return [projection(v) for v in value]
                    if isinstance(value, str) and value.startswith('/'):
                        redacted.append(value); return '<absolute-path-omitted>'
                    return value
                data = encode(projection(json.loads(original)))
            name = label + '/' + (path if index < 3 else ['report.md', 'result.json'][index - 3])
            save('evidence/' + name, data)
            pins.append(dict(file='evidence/' + name, commit=revision, source_path=path,
                             git_blob=subprocess.check_output(['git','-C',str(repo),'rev-parse',revision+':'+path],text=True).strip(),
                             original_bytes=len(original), original_sha256=digest(original),
                             bytes=len(data), sha256=digest(data),
                             representation='path-redacted JSON projection' if redacted else 'exact source bytes',
                             absolute_path_values_omitted=len(redacted)))
            source_sets[label].append((name, data))
    state = dict(schema='continuum.work_state.v1', id='read-availability-recovery', source_snapshot=None,
        objective=dict(id='read-availability', statement='Continue the CLI read-availability investigation in the supplied frozen repository.',
                       done_when='Select a supported next engineering action and the concrete evidence or check needed.',
                       constraints=['This is retrospective frozen public-source replay, not live implementation authority.']),
        attempts=[], decisions=[dict(id='opening-route', state='active',
            statement='The recorded reservation probe found three CLI reads blocked while a read-only SQL control succeeded. A separate existing-only read route is the proposed next implementation boundary; preserve writable initialization and validation.',
            basis_attempt_ids=[], reopen_when='Current source or evidence changes the implementation need.')],
        uncertainties=[dict(id='current-state', question='What is the current state of the supplied repository and what evidence supports the next action?',
                            why_it_matters='An intact historical checkpoint need not describe current source.')],
        handoff=dict(id='resume-read-investigation', from_worker='packet-author', to_worker='fresh-receiver',
                     scope='Determine current state and a useful next action with evidence and limits.', required_decision_ids=['opening-route']))
    save('authored-work-state.json', state)
    binary_hash = digest(binary.read_bytes())
    provenance = dict(binary_sha256=binary_hash, source_commit=subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip(),
                      build_command='cargo build --locked', note='Caller supplies executable; build command is declared provenance, not performed by this preparer. Adapter binds measured bytes, not build truth.')
    save('build-provenance.json', provenance)
    with tempfile.TemporaryDirectory(prefix='continuum-comparison-') as temporary:
        temp = Path(temporary); project=temp/'selected-source'; project.mkdir()
        for name,data in source_sets['before']:
            path=project/name; path.parent.mkdir(parents=True,exist_ok=True); path.write_bytes(data)
        subprocess.run(['git','init','-q',str(project)],check=True)
        subprocess.run(['git','-C',str(project),'add','.'],check=True)
        subprocess.run(['git','-C',str(project),'-c','user.name=Continuum fixture','-c','user.email=fixture@example.invalid','commit','-qm','Frozen selected public evidence'],check=True)
        checkpoint=temp/'checkpoint'
        subprocess.run(['python3',str(repo/'tools/project_checkpoint.py'),'--repository',str(project),
                        '--binary',str(binary),'--work-state',str(output/'authored-work-state.json'),
                        '--build-provenance',str(output/'build-provenance.json'),'--output',str(checkpoint),'--max-bytes','8192'],
                       check=True,capture_output=True)
        for name in ['context.jsonl','coverage.json','verification.json','work-state.json','source-snapshot.json','prepare.json','accept.json','state-snapshot.json']:
            save('native/original/'+name,(checkpoint/name).read_bytes())
        cp=json.loads((checkpoint/'checkpoint.json').read_text()); database=checkpoint/'work.db'; runtime=checkpoint/'runtime'/binary.name
        log=[]
        def cli(command,*values):
            result=subprocess.run([str(runtime),command,str(database),*(str(v) for v in values)],capture_output=True,text=True)
            log.append(dict(command=command,input_files=[str(v.relative_to(output)) for v in values if isinstance(v,Path)],
                            object_ids=[v for v in values if isinstance(v,str)],exit_code=result.returncode,stdout=result.stdout,stderr=result.stderr))
            assert result.returncode==0,(command,result.stderr)
            return json.loads(result.stdout)
        pack=cp['context_pack']; before=cli('verify-context',pack)
        assert before['exact_projection_verified'] and before['freshness']['status']=='matches_at_observation'
        # Repository source has changed, but the native DB has not: same observed verdict.
        remote_only=cli('verify-context',pack)
        assert remote_only==before
        # Explicitly record the new source and authored decision in this disposable DB.
        entries=[]
        for name,data in source_sets['after']:
            path=save('native/update-inputs/'+name,data); identity=cli('blob',path)['id']; entries.append(dict(path=name,blob=identity))
        snapshot=cli('put',save('native/update-source-snapshot.json',dict(type='snapshot',entries=entries)))['id']
        updated=copy.deepcopy(state); updated['source_snapshot']=snapshot
        updated['decisions'][0]['state']='historical'
        updated['decisions'].append(dict(id='existing-read-route',state='active',statement='Current supplied source includes the read-only route and saved passing reservation evidence; review and verify the existing behavior before selecting further changes.',basis_attempt_ids=[],reopen_when='Source inspection or a relevant check identifies a remaining defect.'))
        updated_id=cli('blob',save('native/updated-work-state.json',updated))['id']
        wrapper=cli('put',save('native/update-state-snapshot.json',dict(type='snapshot',entries=[dict(path='work-state.json',blob=updated_id)])))['id']
        accept=json.loads((checkpoint/'accept.json').read_text()); expected=cli('head','project-checkpoint','work')
        # CLI head returns its optional head directly.
        request=dict(acceptor='project-checkpoint',target='work',operation_id='recorded-source-update',expected=expected,candidate=wrapper)
        accepted=cli('accept',save('native/update-accept.json',request)); assert accepted['receipt']['outcome']=='accepted'
        stale=cli('verify-context',pack)
        assert stale['exact_projection_verified'] and stale['freshness']['status']=='stale_at_observation'
        save('native/observations.json',log)
        case_rows=[]
        for index,label,revision,observation in [(1,'before',BASE,before),(2,'after',FIX,remote_only),(3,'after',FIX,stale)]:
            case=f'case-{index:02d}'; obs=dict(exact_projection_verified=observation['exact_projection_verified'],local_anchor=observation['freshness']['status'],action_authority_verified=observation['action_authority_verified'],repository_revision=revision,
                                           limits='Local anchor is not a remote Git freshness observation. Facts are supplied equally to every arm.')
            save(case+'/common-observation.json',obs)
            save(case+'/A-notes.md',b'Continue the CLI read-availability investigation. The recorded probe found three native CLI reads blocked under a writer reservation while a read-only SQL control succeeded. A separate existing-only read route was proposed, preserving writer initialization and native validation. Inspect the supplied current source and evidence, then choose a useful next engineering action and concrete check. The original checkpoint is historical; its integrity and local anchor do not establish current repository state. The common observation and identical evidence menu are available to all arms.\n')
            save(case+'/B-records.json',json.loads((checkpoint/'work-state.json').read_text()))
            save(case+'/C-context.jsonl',(checkpoint/'context.jsonl').read_bytes())
            save(case+'/C-verification.json',observation)
            menu=dict(files=[x['file'] for x in pins if x['file'].startswith('evidence/'+label+'/')],
                      current_accepted_state='native/updated-work-state.json' if index==3 else 'native/original/work-state.json',
                      source_pins='source-pins.json', common_observation=case+'/common-observation.json',
                      verification_record=case+'/C-verification.json')
            save(case+'/retrieval-menu.json',menu)
            case_rows.append(dict(case=case,source_revision=revision,local_anchor=obs['local_anchor']))
        save('source-pins.json',pins)
        save('preparation.json',dict(schema='continuum.comparison_packet.v1',cases=case_rows,binary_sha256=binary_hash,
            adapter_sha256=digest((repo/'tools/project_checkpoint.py').read_bytes()),native_additional_processes=len(log),
            adapter_processes=len((checkpoint/'cli-log.jsonl').read_text().splitlines()),preparation_elapsed_seconds=time.monotonic()-started,
            model_receivers_invoked=0,author_hindsight_exposure=True,receiver_dispatch_ready=False,
            limitations=['Selected-source temporary Git tree is a fixture, not the original repository checkout.',
                         'Two historical result JSONs are explicitly path-redacted projections bound to original source hashes. Exact adapter/native invocation logs with temporary paths remain local; published native observations retain command roles, input bytes and raw stdout/stderr.',
                         'Author/model attention cost before timing is unavailable. Measured elapsed time covers preparation execution only.',
                         'Retrieval bridge, neutral baseline audit and independent rating procedure must be frozen before any model run.']))
    inventory=[]
    for path in sorted(output.rglob('*')):
        if path.is_file():inventory.append(dict(path=str(path.relative_to(output)),bytes=path.stat().st_size,sha256=digest(path.read_bytes())))
    save('artifact-manifest.json',inventory)
    print(json.dumps(dict(output=str(output),cases=3,source_files=len(pins),native_anchor_sequence=[x['local_anchor'] for x in case_rows],receiver_calls=0)))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository',type=Path,required=True);parser.add_argument('--binary',type=Path,required=True);parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();prepare(args.repository,args.binary,args.output)
