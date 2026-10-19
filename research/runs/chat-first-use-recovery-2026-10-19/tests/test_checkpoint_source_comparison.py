"""Standalone tests for source-byte comparison; no native runner required."""
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "examples" / "verify_checkpoint_sources.py"


class CheckpointSourceComparisonTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.project = self.root / "project"
        self.project.mkdir()
        (self.project / "docs").mkdir()
        self.input = self.project / "docs" / "CURRENT.md"
        self.input.write_bytes(b"current objective\n")
        self.report = self.root / "report.json"
        self.record = {
            "schema": "continuum.real_checkpoint_observation.v1",
            "source_snapshot": "sha256:" + "0" * 64,
            "source": [{"path": "docs/CURRENT.md", "bytes": 18,
                        "sha256": hashlib.sha256(b"current objective\n").hexdigest()}],
        }
        self.report.write_text(json.dumps(self.record), encoding="utf-8")

    def run_check(self):
        result = subprocess.run([sys.executable, str(SCRIPT), "--report", str(self.report),
                                 "--project", str(self.project)], text=True,
                                capture_output=True)
        return result

    def test_matching_source(self):
        result = self.run_check()
        self.assertEqual(result.returncode, 0, result.stderr)
        outcome = json.loads(result.stdout)
        self.assertTrue(outcome["all_selected_source_bytes_match"])
        self.assertEqual(outcome["checked_files"][0]["status"], "matches")

    def test_changed_source_is_detected(self):
        self.input.write_bytes(b"changed objective\n")
        result = self.run_check()
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertEqual(json.loads(result.stdout)["checked_files"][0]["status"], "differs")

    def test_symlink_source_is_not_followed(self):
        self.input.unlink()
        self.input.symlink_to(self.root / "report.json")
        result = self.run_check()
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertEqual(json.loads(result.stdout)["checked_files"][0]["status"], "symlink_not_followed")

    def test_parent_traversal_is_rejected(self):
        self.record["source"][0]["path"] = "../report.json"
        self.report.write_text(json.dumps(self.record))
        result = self.run_check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("normalized and relative", result.stderr)

    def test_duplicate_source_is_rejected(self):
        self.record["source"].append(dict(self.record["source"][0]))
        self.report.write_text(json.dumps(self.record))
        result = self.run_check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("duplicate source", result.stderr)


if __name__ == "__main__":
    unittest.main()
