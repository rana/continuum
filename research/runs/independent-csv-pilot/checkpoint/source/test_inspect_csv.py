import json
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).with_name("inspect_csv.py")


class CsvTests(unittest.TestCase):
    def run_csv(self, content, *options, success=True):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "input.csv"
            source.write_bytes(content)
            result = subprocess.run(["python3", str(SCRIPT), str(source), *options],
                                    capture_output=True, text=True)
        self.assertEqual(result.returncode == 0, success, result.stderr)
        if not success:
            self.assertEqual(result.stdout, "")
            self.assertIn("error", json.loads(result.stderr))
            return None
        return json.loads(result.stdout)

    def test_exact_empty_cells_and_quoted_records(self):
        result = self.run_csv(b'name,note\r\nAda,"hello, world"\r\nBob,""\r\n,"two\nlines"\r\n')
        self.assertEqual(result, {"rows": 3, "columns": [
            {"name": "name", "present": 2, "missing": 1},
            {"name": "note", "present": 2, "missing": 1}]})

    def test_whitespace_and_na_are_present(self):
        result = self.run_csv(b'x\n \nNA\n')
        self.assertEqual(result['columns'][0], {"name": "x", "present": 2, "missing": 0})

    def test_header_only(self):
        self.assertEqual(self.run_csv(b'x,y\n')['rows'], 0)

    def test_invalid_inputs_fail_without_partial_report(self):
        for content in (b'', b'x,x\n', b'x,\n', b'x,y\n1\n',
                        b'x\n1,2\n', b'x\n"unterminated\n', b'x\n\xff\n'):
            with self.subTest(content=content):
                self.run_csv(content, success=False)


if __name__ == '__main__':
    unittest.main()
