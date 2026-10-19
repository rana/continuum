import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('calibration_cell',HERE/'cell.py');cell=importlib.util.module_from_spec(spec);spec.loader.exec_module(cell)

class CaptureTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);self.output=self.root/'cell';self.release=HERE/'release'
        identity=cell.sha((self.release/'manifest.json').read_bytes());cell.init(self.release,self.output,'case-01','A','test-cell',identity)
    def result(self,value):
        path=self.root/'result.json';path.write_bytes(cell.encoded(value));return path
    def good(self,text):return dict(structuredContent=dict(status='OK',text=text,truncated=False,stop_reason='end_turn',actual_model='test-double',usage=dict(input_tokens=3,output_tokens=4)))
    def test_exact_frozen_initial_request_and_exclusive_cell(self):
        request=cell.submit(self.release,self.output)
        self.assertEqual(request,json.loads((self.release/'case-01/A-request.json').read_text()))
        with self.assertRaises(ValueError):cell.submit(self.release,self.output)
        with self.assertRaises(FileExistsError):cell.init(self.release,self.output,'case-01','A','second',cell.sha((self.release/'manifest.json').read_bytes()))
    def test_unknown_outcome_ends_cell_without_retry(self):
        cell.submit(self.release,self.output)
        result=cell.record(self.release,self.output,self.result(dict(structuredContent=dict(status='ERROR',inference_outcome='unknown'))))
        self.assertEqual(result['kind'],'incomplete');self.assertEqual(result['inference_outcome'],'unknown')
        with self.assertRaises(ValueError):cell.submit(self.release,self.output)
        self.assertFalse((self.output/'round-02').exists())
    def test_retrieval_next_request_retains_visible_history(self):
        cell.submit(self.release,self.output);value=self.good('{"paths":["current/report.md"]}')
        result=cell.record(self.release,self.output,self.result(value));self.assertEqual(result['kind'],'prepared')
        request=cell.submit(self.release,self.output);self.assertIn(value['structuredContent']['text'].replace('"','\\"'),request['context'])
        self.assertIn('current/report.md',request['context']);self.assertIn('source_bytes',request['context'])
        final=cell.record(self.release,self.output,self.result(self.good('{"answer":"A bounded read-only route and held-writer check are warranted."}')))
        self.assertEqual(final['kind'],'final')
        with self.assertRaises(ValueError):cell.submit(self.release,self.output)
    def test_malformed_and_truncated_output_preserved_and_stops(self):
        for value in [self.good('not JSON'),dict(structuredContent=dict(status='OK',text='partial',truncated=True,stop_reason='max_tokens'))]:
            with tempfile.TemporaryDirectory() as directory:
                output=Path(directory)/'cell';cell.init(self.release,output,'case-01','A','bad-output',cell.sha((self.release/'manifest.json').read_bytes()));cell.submit(self.release,output)
                state=cell.record(self.release,output,self.result(value));self.assertEqual(state['kind'],'incomplete');self.assertTrue((output/'round-01/provider-result.json').exists())
    def test_different_outcome_cannot_replace_retained_result(self):
        cell.submit(self.release,self.output);original=self.result(self.good('{"answer":"First response."}'));cell.record(self.release,self.output,original)
        with self.assertRaises(ValueError):cell.record(self.release,self.output,self.result(self.good('{"answer":"Changed response."}')))
    def test_request_mutation_refused_before_submission(self):
        (self.output/'round-01/request.json').write_text('{}')
        with self.assertRaises(ValueError):cell.submit(self.release,self.output)
    def test_capture_can_recover_after_known_result_before_transition(self):
        cell.submit(self.release,self.output);raw=cell.encoded(self.good('{"answer":"A supported recommendation."}'));(self.output/'round-01/provider-result.json').write_bytes(raw)
        state=cell.record(self.release,self.output,self.result(json.loads(raw)));self.assertEqual(state['kind'],'final')
        self.assertEqual((self.output/'round-01/provider-result.json').read_bytes(),raw)

if __name__=='__main__':unittest.main()
