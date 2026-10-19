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

    def native(self, database, command, *values):
        run = subprocess.run([str(BINARY), command, str(database), *map(str, values)],
                             capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        return json.loads(run.stdout)

    def recorded_attempt_bundle(self, receipt=b"recorded response\xff\n", source=b"historical source\x00\n"):
        database = self.root / "seed.db"
        self.native(database, "init")
        objects = []
        ids = []
        for index, data in enumerate([source, b"exact request\x00\n", receipt]):
            path = self.root / f"blob-{index}"
            path.write_bytes(data)
            identity = self.native(database, "blob", path)["id"]
            ids.append(identity)
            objects.append(self.native(database, "get", identity))
        path = self.root / "historical.json"
        path.write_text(json.dumps({"type": "snapshot", "entries": [{"path": "old.txt", "blob": ids[0]}]}))
        snapshot = self.native(database, "put", path)["id"]
        objects.insert(0, self.native(database, "get", snapshot))  # Deliberately dependency-first reversed.
        state = json.loads(self.state.read_text())
        state["attempts"] = [{"id": "prior", "operation_id": "historical-operation",
                              "source_snapshot": snapshot, "summary": "Historical authored attempt.",
                              "dispatch_state": "receipt_recorded", "request": ids[1],
                              "receipt": ids[2], "outcome_note": "Opaque retained bytes, no truth claim."}]
        self.state.write_text(json.dumps(state))
        bundle = {"schema": "continuum.object_bundle.v1", "objects": objects}
        path = self.root / "bundle.json"
        path.write_text(json.dumps(bundle))
        return path, bundle

    def test_recorded_attempt_exact_bytes_historical_scope_and_reconstruction(self):
        path, bundle = self.recorded_attempt_bundle()
        first = self.run_checkpoint(extra=("--import-objects", str(path)))
        self.assertEqual((first / "import-objects.json").read_bytes(), path.read_bytes())
        for envelope in bundle["objects"]:
            self.assertEqual(self.native(first / "work.db", "get", envelope["id"]), envelope)
        state = json.loads((first / "work-state.json").read_text())
        self.assertEqual(state["attempts"], json.loads(self.state.read_text())["attempts"])
        self.assertNotEqual(state["source_snapshot"], state["attempts"][0]["source_snapshot"])
        bundle["objects"].reverse()
        path.write_text(json.dumps(bundle))
        second = self.run_checkpoint("reconstructed", extra=("--import-objects", str(path)))
        self.assertEqual(json.loads((first / "checkpoint.json").read_text())["context_pack"],
                         json.loads((second / "checkpoint.json").read_text())["context_pack"])
        self.assertEqual(json.loads((first / "verification.json").read_text())["exact_projection_verified"], True)

    def test_imported_source_overlap_is_explicit_and_verified(self):
        path, _ = self.recorded_attempt_bundle(source=b"\x00\xff\r\nexact\n")
        output = self.run_checkpoint(extra=("--import-objects", str(path)))
        manifest = json.loads((output / "checkpoint.json").read_text())
        overlap = [entry for entry in manifest["imports"]["objects"]
                   if entry["preexisting_in_source_capture"]]
        self.assertEqual(len(overlap), 1)
        self.assertEqual(overlap[0]["id"], manifest["source"]["files"][0]["blob"])

    def test_missing_extra_and_mislabeled_objects_have_no_success_manifest(self):
        path, original = self.recorded_attempt_bundle()
        import copy
        mutations = {}
        missing = copy.deepcopy(original)
        missing["objects"].pop()  # A required receipt or leaf cannot disappear.
        mutations["missing"] = missing
        leaf = copy.deepcopy(original)
        leaf["objects"].pop(1)
        mutations["missing-snapshot-leaf"] = leaf
        extra = copy.deepcopy(original)
        database = self.root / "seed.db"
        file = self.root / "unrelated"
        file.write_bytes(b"unrelated")
        extra_id = self.native(database, "blob", file)["id"]
        extra["objects"].append(self.native(database, "get", extra_id))
        mutations["extra"] = extra
        mismatch = copy.deepcopy(original)
        mismatch["objects"][1]["object"]["bytes"].append(1)
        mutations["mismatch"] = mismatch
        for label, bundle in mutations.items():
            with self.subTest(label=label):
                path.write_text(json.dumps(bundle))
                output = self.run_checkpoint(label, extra=("--import-objects", str(path)), succeeds=False)
                self.assertFalse((output / "checkpoint.json").exists())

    def test_bundle_preflight_rejects_ambiguity_versions_kinds_and_limits(self):
        path, original = self.recorded_attempt_bundle()
        import copy
        invalid = []
        for version in [True, 1.0, "1", 2]:
            bundle = copy.deepcopy(original)
            bundle["objects"][0]["format_version"] = version
            invalid.append(json.dumps(bundle))
        duplicate = copy.deepcopy(original)
        duplicate["objects"].append(duplicate["objects"][0])
        invalid.append(json.dumps(duplicate))
        kind = copy.deepcopy(original)
        kind["objects"][0]["object"]["type"] = "evidence_record"
        invalid.append(json.dumps(kind))
        invalid.extend(['{"schema":"x","schema":"continuum.object_bundle.v1","objects":[]}',
                        '{"schema":"continuum.object_bundle.v1","objects":[],"extra":NaN}',
                        json.dumps({"schema": "continuum.object_bundle.v1", "objects": [None] * 257}),
                        ' ' * (16 * 1024 * 1024 + 1)])
        for index, value in enumerate(invalid):
            with self.subTest(case=index):
                path.write_text(value)
                output = self.run_checkpoint(f"invalid-{index}", extra=("--import-objects", str(path)),
                                             succeeds=False)
                self.assertFalse(output.exists())

    def test_native_context_rejects_acknowledgement_as_imported_receipt(self):
        path, _ = self.recorded_attempt_bundle(
            json.dumps({"schema": "continuum.context_acknowledgement.v1"}).encode())
        output = self.run_checkpoint(extra=("--import-objects", str(path)), succeeds=False)
        self.assertFalse((output / "checkpoint.json").exists())
        self.assertTrue((output / "imports").exists())
        log = [json.loads(line) for line in (output / "cli-log.jsonl").read_text().splitlines()]
        self.assertIn("acknowledgement is not an attempt receipt", log[-1]["stderr"])

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

    def test_original_binary_replacement_does_not_change_later_invocations(self):
        # The wrapper replaces its original path during init. Reopening that path
        # for the next CLI command would fail, while the retained executable works.
        wrapper = self.root / "replaceable-continuum"
        code = ("#!/usr/bin/env python3\nimport os, sys\nfrom pathlib import Path\n"
                f"if sys.argv[1] == 'init': Path({str(wrapper)!r}).write_bytes(b'replaced')\n"
                f"os.execv({str(BINARY)!r}, [{str(BINARY)!r}, *sys.argv[1:]])\n")
        wrapper.write_text(code)
        wrapper.chmod(0o700)
        digest = hashlib.sha256(wrapper.read_bytes()).hexdigest()
        self.provenance.write_text(json.dumps({"binary_sha256": digest}))
        output = self.run_checkpoint(extra=("--binary", str(wrapper)))
        self.assertEqual(wrapper.read_bytes(), b"replaced")
        self.assertEqual(hashlib.sha256((output / "runtime" / wrapper.name).read_bytes()).hexdigest(),
                         digest)
        self.assertTrue((output / "checkpoint.json").exists())

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
