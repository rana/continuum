#!/usr/bin/env python3
"""Verify preserved retrieval bytes/exposure and receiver source comparison.

Does not execute the CSV sample, rerun inference, or authenticate the records.
"""
import gzip
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]


def read(name):
    path = ROOT / name
    return path.read_bytes() if path.exists() else gzip.decompress(Path(str(path) + '.gz').read_bytes())


def load(name):
    return json.loads(read(name))


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    assert load('turn-1-request.json')['context'].endswith(
        (REPOSITORY / 'research/runs/checkpoint-object-import/first/context.jsonl').read_text())
    for turn, retrieval in [('2', 1), ('3', 2), ('3b', 2), ('4', 3)]:
        assert load(f'turn-{turn}-request.json')['context'].endswith(
            read(f'retrieval-{retrieval}.json').decode('utf-8'))
    first = load('turn-1-request.json')
    second = load('turn-2-request.json')
    assert second['prior_exchange'][0]['text'] == first['context'] + '\n\n' + first['request']
    assert second['prior_exchange'][1]['text'] == load('turn-1-response.json')['structuredContent']['text']
    corrected = load('turn-3b-request.json')['context']
    for item in load('turn-3-request.json')['prior_exchange']:
        assert item['text'] in corrected
    assert load('turn-4-request.json')['context'].startswith(corrected)
    observations = []
    for index in [1, 2, 3]:
        raw = read(f'retrieval-{index}.json')
        payload = json.loads(raw)
        custody = load(f'retrieval-{index}-custody.json')
        assert len(raw) <= 65536 and len(payload['native_objects']) <= 6
        assert digest(raw) == custody['payload_sha256']
        logs = load(f'retrieval-{index}-native-log.json')
        native = {json.loads(item['stdout'])['id']: json.loads(item['stdout']) for item in logs}
        for obj in payload['native_objects']:
            original = native[obj['id']]
            if obj.get('type') == 'blob':
                data = bytes(original['object']['bytes'])
                assert data.decode('utf-8') == obj['content']
                assert len(data) == obj['bytes'] and digest(data) == obj['sha256']
            else:
                assert obj == original
        for item in payload.get('sidecars', []):
            data = item['content'].encode('utf-8')
            assert len(data) == item['bytes'] and digest(data) == item['sha256']
            assert (REPOSITORY / item['path']).read_bytes() == data
        observations.append({'round': index, 'bytes': len(raw), 'native_objects': len(payload['native_objects'])})
    receipt = json.loads(load('retrieval-1.json')['native_objects'][0]['content'])
    returned = json.loads(receipt['structuredContent']['text'])['files']
    snapshot = next(obj['object'] for obj in load('retrieval-2.json')['native_objects'] if 'object' in obj)
    historical = next(obj['object'] for obj in load('retrieval-1.json')['native_objects'] if 'object' in obj)
    old_sample = next(entry['blob'] for entry in historical['entries'] if entry['path'] == 'sample.csv')
    new_sample = next(entry['blob'] for entry in snapshot['entries'] if entry['path'] == 'sample.csv')
    assert old_sample == new_sample
    assert load('retrieval-2.json')['native_objects'][1]['id'] == new_sample
    blobs = {obj['id']: obj for obj in load('retrieval-3.json')['native_objects']}
    matched = []
    for entry in snapshot['entries']:
        if entry['path'] in returned:
            assert blobs[entry['blob']]['content'].encode('utf-8') == returned[entry['path']].encode('utf-8')
            matched.append(entry['path'])
    assert sorted(matched) == sorted(returned)
    print(json.dumps({'retrievals': observations, 'exact_source_matches': matched,
                      'fresh_csv_tests': False, 'new_inference': False}, indent=2))


if __name__ == '__main__':
    main()
