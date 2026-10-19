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

    def test_default_report_shape_and_counts_unchanged(self):
        result = self.run_csv(b'x,y\nNA,\nna, NA \n')
        self.assertEqual(result, {"rows": 2, "columns": [
            {"name": "x", "present": 2, "missing": 0},
            {"name": "y", "present": 1, "missing": 1}]})

    def test_listed_token_matches_exactly_without_trimming_or_case_folding(self):
        result = self.run_csv(b'x\nNA\nna\n NA \nNA \n\t\n""\n', '--missing-value', 'NA')
        self.assertEqual(result, {"rows": 6, "columns": [
            {"name": "x", "present": 4, "missing": 2}]})

    def test_multiple_tokens_each_add_missing_values(self):
        result = self.run_csv(b'x,y\nNA,?\nN/A,ok\n,?\n',
                              '--missing-value', 'NA', '--missing-value', '?')
        self.assertEqual(result, {"rows": 3, "columns": [
            {"name": "x", "present": 1, "missing": 2},
            {"name": "y", "present": 1, "missing": 2}]})

    def test_duplicate_options_do_not_double_count(self):
        content = b'x\nNA\n""\nok\n'
        once = self.run_csv(content, '--missing-value', 'NA')
        repeated = self.run_csv(content, '--missing-value', 'NA', '--missing-value', 'NA',
                                '--missing-value', '', '--missing-value', '')
        self.assertEqual(repeated, once)
        self.assertEqual(repeated, {"rows": 3, "columns": [
            {"name": "x", "present": 1, "missing": 2}]})

    def test_empty_option_adds_nothing_beyond_default(self):
        content = b'x,y\nNA,""\n ,\n'
        default = self.run_csv(content)
        self.assertEqual(default, {"rows": 2, "columns": [
            {"name": "x", "present": 2, "missing": 0},
            {"name": "y", "present": 0, "missing": 2}]})
        self.assertEqual(self.run_csv(content, '--missing-value', ''), default)
        self.assertEqual(self.run_csv(content, '--missing-value='), default)

    def test_tokens_match_parsed_quoted_cells_not_header(self):
        result = self.run_csv(b'NA,y\n"NA","a,b"\n" NA ","two\nlines"\n"",ok\n',
                              '--missing-value', 'NA', '--missing-value', 'a,b',
                              '--missing-value', 'two\nlines')
        self.assertEqual(result, {"rows": 3, "columns": [
            {"name": "NA", "present": 1, "missing": 2},
            {"name": "y", "present": 1, "missing": 2}]})

    def test_invalid_inputs_still_fail_with_options(self):
        options = ('--missing-value', 'NA', '--missing-value', '')
        for content in (b'', b'x,x\n', b'x,\n', b'NA,NA\n', b'x,y\n1\n', b'x\n1,2\n',
                        b'x\n"unterminated\n', b'x\n\xff\n', b'x\nNA\n\n'):
            with self.subTest(content=content):
                self.run_csv(content, *options, success=False)


if __name__ == '__main__':
    unittest.main()
