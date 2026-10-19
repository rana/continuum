#!/usr/bin/env python3
"""Frozen-case retrieval only. No provider invocation, execution or filesystem writes."""
import hashlib
import json
from pathlib import Path

MAX_RESPONSE_BYTES = 32768
MAX_ROUNDS = 2
MAX_RETRIEVED_BYTES = 65536
MAX_PATHS = 8

def sha(data):
    return hashlib.sha256(data).hexdigest()

def strict_json(raw):
    if not isinstance(raw, str) or len(raw.encode('utf-8')) > MAX_RESPONSE_BYTES:
        raise ValueError('response exceeds UTF-8 bound')
    def pairs(items):
        result = {}
        for key,value in items:
            if key in result:raise ValueError('duplicate JSON key')
            result[key]=value
        return result
    def reject(value):raise ValueError('nonfinite number')
    try:return json.loads(raw,object_pairs_hook=pairs,parse_constant=reject)
    except RecursionError as error:raise ValueError('JSON nesting exceeds parser bound') from error

class Bridge:
    def __init__(self, release, case, expected_manifest_sha256):
        self.release=Path(release).resolve()
        if case not in ('case-01','case-02','case-03'):raise ValueError('unknown case')
        self.case=case;self.rounds=0;self.retrieved_bytes=0;self.finished=False;self.events=[]
        manifest_bytes=(self.release/'manifest.json').read_bytes()
        if sha(manifest_bytes)!=expected_manifest_sha256:raise ValueError('release manifest changed')
        manifest=json.loads(manifest_bytes)
        self.identities={x['path']:x for x in manifest['files']}
        # The constructor verifies the sender-side menu before trusting its references.
        raw=self.read_checked(case+'/menu.json')
        self.menu=json.loads(raw)
        if not isinstance(self.menu,dict):raise ValueError('invalid release menu')
        for alias,relative in self.menu.items():
            if not isinstance(alias,str) or not isinstance(relative,str) or not relative.startswith(case+'/evidence/'):
                raise ValueError('cross-case or invalid menu mapping')
            self.read_checked(relative)

    def read_checked(self, relative):
        parts=Path(relative).parts
        if Path(relative).is_absolute() or '..' in parts or '\\' in relative:raise ValueError('invalid manifest path')
        row=self.identities.get(relative)
        if row is None:raise ValueError('file absent from release manifest')
        path=self.release/relative
        # Do not follow a replaced directory or file symlink outside the frozen root.
        if any(p.is_symlink() for p in [path,*path.parents] if p!=self.release.parent):raise ValueError('symlink in release path')
        raw=path.read_bytes()
        if len(raw)!=row['bytes'] or sha(raw)!=row['sha256']:raise ValueError('release file changed')
        return raw

    def handle(self, raw):
        if self.finished:raise ValueError('cell already final')
        response=strict_json(raw)
        if not isinstance(response,dict):raise ValueError('response must be object')
        if set(response)=={'answer'}:
            if not isinstance(response['answer'],str) or not response['answer'].strip():raise ValueError('empty final answer')
            self.finished=True
            event=dict(kind='final',answer=response['answer'],rounds=self.rounds,retrieved_bytes=self.retrieved_bytes)
            self.events.append(event);return event
        if set(response)!={'paths'}:raise ValueError('expected paths or answer only')
        paths=response['paths']
        if not isinstance(paths,list) or not 1<=len(paths)<=MAX_PATHS or any(not isinstance(x,str) for x in paths) or len(set(paths))!=len(paths):raise ValueError('invalid path list')
        if self.rounds>=MAX_ROUNDS:raise ValueError('retrieval rounds exhausted')
        self.rounds+=1
        if any(x not in self.menu for x in paths):
            event=dict(kind='retrieval_denied',reason='path not in this case menu',round=self.rounds,paths=paths)
            self.events.append(event);return event
        selected=[(name,self.read_checked(self.menu[name])) for name in paths]
        size=sum(len(data) for _,data in selected)
        if self.retrieved_bytes+size>MAX_RETRIEVED_BYTES:
            event=dict(kind='retrieval_denied',reason='aggregate byte budget exceeded',round=self.rounds,paths=paths)
            self.events.append(event);return event
        self.retrieved_bytes+=size
        event=dict(kind='retrieval',round=self.rounds,source_bytes=size,cumulative_source_bytes=self.retrieved_bytes,
                   files=[dict(path=name,bytes=len(data),sha256=sha(data),text=data.decode('utf-8')) for name,data in selected])
        self.events.append(event);return event
