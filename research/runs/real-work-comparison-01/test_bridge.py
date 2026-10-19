import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('comparison_bridge',HERE/'bridge.py')
bridge=importlib.util.module_from_spec(spec);spec.loader.exec_module(bridge)

class RetrievalTests(unittest.TestCase):
    def setUp(self):
        self.release=HERE/'release';self.root=bridge.sha((self.release/'manifest.json').read_bytes())
    def cell(self,case='case-01',release=None):return bridge.Bridge(release or self.release,case,self.root)
    def test_exact_order_and_source_byte_accounting(self):
        cell=self.cell();event=cell.handle(json.dumps({'paths':['current/src/main.rs','current/result.json']}))
        self.assertEqual(event['kind'],'retrieval');self.assertEqual([x['path'] for x in event['files']],['current/src/main.rs','current/result.json'])
        self.assertEqual(cell.retrieved_bytes,sum(len(x['text'].encode()) for x in event['files']))
        for row in event['files']:self.assertEqual(bridge.sha(row['text'].encode()),row['sha256'])
    def test_cross_case_private_and_grading_paths_are_denied(self):
        for alias in ['../README.md','/etc/passwd','case-02/menu.json','evidence/after/src/store.rs','source-pins.json','claude-methodology-review.json']:
            cell=self.cell();event=cell.handle(json.dumps({'paths':[alias]}));self.assertEqual(event['kind'],'retrieval_denied');self.assertEqual(cell.retrieved_bytes,0)
    def test_malformed_duplicate_and_nonfinite_json_rejected(self):
        for raw in ['{"paths":[],"paths":["current/report.md"]}','{"paths":[NaN]}','{"paths":[true]}','{"paths":["x","x"]}','{"paths":[],"answer":"x"}', '[]', '{"paths":["x"],"command":"run"}']:
            with self.assertRaises(ValueError):self.cell().handle(raw)
    def test_utf8_response_size_bound(self):
        with self.assertRaises(ValueError):self.cell().handle(json.dumps({'answer':'\u00e9'*20000},ensure_ascii=False))
    def test_denied_rounds_count_and_final_remains_available(self):
        cell=self.cell()
        for _ in range(2):self.assertEqual(cell.handle('{"paths":["unknown"]}')['kind'],'retrieval_denied')
        with self.assertRaises(ValueError):cell.handle('{"paths":["current/report.md"]}')
        self.assertEqual(cell.handle('{"answer":"Need source evidence before proposing a change."}')['kind'],'final')
        with self.assertRaises(ValueError):cell.handle('{"answer":"second"}')
    def test_aggregate_budget_rejects_whole_round_without_partial_bytes(self):
        cell=self.cell();cell.retrieved_bytes=bridge.MAX_RETRIEVED_BYTES-1
        event=cell.handle('{"paths":["current/report.md"]}');self.assertEqual(event['kind'],'retrieval_denied');self.assertEqual(cell.retrieved_bytes,bridge.MAX_RETRIEVED_BYTES-1)
    def test_changed_artifact_or_manifest_and_symlink_refused(self):
        with tempfile.TemporaryDirectory() as directory:
            dest=Path(directory)/'release';shutil.copytree(self.release,dest)
            artifact=dest/'case-01/evidence/current/report.md';old=artifact.read_bytes();artifact.write_bytes(old+b' ')
            with self.assertRaises(ValueError):self.cell(release=dest)
            artifact.write_bytes(old);artifact.unlink();artifact.symlink_to(dest/'case-02/evidence/current/report.md')
            with self.assertRaises(ValueError):self.cell(release=dest)
            (dest/'manifest.json').write_bytes(b'{}')
            with self.assertRaises(ValueError):self.cell(release=dest)
    def test_case01_does_not_reveal_other_revision_pins(self):
        cell=self.cell();event=cell.handle('{"paths":["current-source-pins.json"]}')
        pins=json.loads(event['files'][0]['text']);self.assertEqual(len(pins),5)
        self.assertEqual({x['commit'] for x in pins},{'cedade61fbc377519dce68829679c954399bc854'})
        self.assertNotIn('f00b135',json.dumps(pins));self.assertTrue(all(x['file'].startswith('current/') for x in pins))
    def test_all_authored_decision_relevant_strings_have_initial_exposure(self):
        state=json.loads((HERE/'packet/native/original/work-state.json').read_text())
        values=[state['id'],state['source_snapshot'],state['objective']['statement'],state['objective']['done_when'],*state['objective']['constraints']]
        for record in state['decisions']:values.extend([record['id'],record['state'],record['statement'],record['reopen_when']])
        for record in state['uncertainties']:values.extend([record['id'],record['question'],record['why_it_matters']])
        values.extend(state['handoff'][key] for key in ['id','from_worker','to_worker','scope'])
        values.extend(state['handoff']['required_decision_ids'])
        for case in ['case-01','case-02','case-03']:
            for arm in 'ABC':
                context=json.loads((self.release/case/(arm+'-request.json')).read_text())['context']
                for value in values:self.assertIn(value,context)

    def test_same_arm_common_facts_and_task_all_cases(self):
        for case in ['case-01','case-02','case-03']:
            values=[json.loads((self.release/case/(arm+'-request.json')).read_text()) for arm in 'ABC']
            self.assertEqual(len({v['request'] for v in values}),1)
            common=[v['context'].split('\nHandoff:\n')[0] for v in values];self.assertEqual(len(set(common)),1)
            menus=[v['context'].split('\nAvailable files:\n')[1] for v in values];self.assertEqual(len(set(menus)),1)
            self.assertEqual({(v['model'],v['effort']) for v in values},{('opus','medium')})

if __name__=='__main__':unittest.main()
