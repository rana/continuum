"""Integration checks for exact committed capture and failure boundaries."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ADAPTER = Path(__file__).with_name("project_checkpoint.py")
BINARY = Path(os.environ.get("CONTINUUM_BINARY", "target/debug/continuum")).resolve()


class CheckpointTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        self.git("init", "-q")
        self.git("config", "user.name", "Checkpoint test")
        self.git("config", "user.email", "test@example.invalid")
        (self.repo / "binary data").write_bytes(b"\x00\xff\r\nexact\n")
        self.git("add", ".")
        self.git("commit", "-qm", "fixture")
        self.state = self.root / "state.json"
        self.state.write_text(json.dumps({
            "schema": "continuum.work_state.v1", "id": "work", "source_snapshot": None,
            "objective": {"id": "goal", "statement": "Inspect exact fixture bytes.",
                          "done_when": "Inspection recorded.", "constraints": []},
            "attempts": [], "decisions": [], "uncertainties": [],
            "handoff": {"id": "handoff", "from_worker": "sender", "to_worker": "receiver",
                        "scope": "Inspect fixture.", "required_decision_ids": []},
        }))
        self.provenance = self.root / "build.json"
        self.provenance.write_text(json.dumps({
            "binary_sha256": hashlib.sha256(BINARY.read_bytes()).hexdigest(),
            "note": "Integration test caller declaration",
        }))

    def git(self, *args):
        return subprocess.run(["git", "-C", str(self.repo), *args], check=True,
                              capture_output=True).stdout

    def run_checkpoint(self, name="output", extra=(), succeeds=True):
        output = self.root / name
        result = subprocess.run(["python3", str(ADAPTER), "--binary", str(BINARY),
                                 "--repository", str(self.repo), "--work-state", str(self.state),
                                 "--build-provenance", str(self.provenance), "--output", str(output),
                                 *extra], capture_output=True, text=True)
        self.assertEqual(result.returncode == 0, succeeds, result.stderr)
        return output

    def test_exact_committed_bytes_replay_and_existing_output(self):
        (self.repo / "binary data").write_bytes(b"dirty")
        (self.repo / "untracked").write_text("excluded")
        first = self.run_checkpoint()
        second = self.run_checkpoint("replay")
        self.assertEqual((first / "source/binary data").read_bytes(), b"\x00\xff\r\nexact\n")
        self.assertFalse((first / "source/untracked").exists())
        a = json.loads((first / "checkpoint.json").read_text())
        b = json.loads((second / "checkpoint.json").read_text())
        self.assertEqual(a["context_pack"], b["context_pack"])
        self.assertEqual(a["source"], b["source"])
        coverage = json.loads((first / "coverage.json").read_text())
        self.assertEqual(coverage["rendered_bytes"], len((first / "context.jsonl").read_bytes()))
        self.assertEqual(coverage["omitted"], [])
        self.run_checkpoint(succeeds=False)
        self.assertEqual(json.loads((first / "checkpoint.json").read_text()), a)

    def test_filesystem_aliases_rejected_before_output(self):
        # Index plumbing creates colliding trees even on case-insensitive hosts.
        for paths in (("README", "readme"), ("Foo", "foo/bar"),
                      ("caf\u00e9", "cafe\u0301"), ("Dir/a", "dir/b")):
            with self.subTest(paths=paths):
                self.git("read-tree", "--empty")
                oid = self.git("rev-parse", "HEAD:binary data").decode().strip()
                for path in paths:
                    self.git("update-index", "--add", "--cacheinfo", f"100644,{oid},{path}")
                tree = self.git("write-tree").decode().strip()
                commit = self.git("commit-tree", tree, "-m", "alias fixture").decode().strip()
                output = self.run_checkpoint(name="alias", extra=("--revision", commit), succeeds=False)
                self.assertFalse(output.exists())

    def test_symlink_rejected_before_output(self):
        (self.repo / "link").symlink_to("binary data")
        self.git("add", ".")
        self.git("commit", "-qm", "unsupported symlink")
        self.assertFalse(self.run_checkpoint(succeeds=False).exists())

    def test_digest_mismatch_before_output(self):
        self.provenance.write_text('{"binary_sha256":"wrong"}')
        self.assertFalse(self.run_checkpoint(succeeds=False).exists())

    def test_insufficient_budget_retains_failure_without_success_manifest(self):
        output = self.run_checkpoint(extra=("--max-bytes", "1"), succeeds=False)
        self.assertFalse((output / "checkpoint.json").exists())
        log = [json.loads(line) for line in (output / "cli-log.jsonl").read_text().splitlines()]
        self.assertNotEqual(log[-1]["returncode"], 0)
        self.assertTrue((output / "authored-work-state.json").exists())


if __name__ == "__main__":
    unittest.main()
