import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "workspace" / "snapshot.py"


class SnapshotTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.outputs = self.root / "outputs"
        self.outputs.mkdir()

    def snapshot(self, path, limit, staging_name="snapshot"):
        return subprocess.run(
            [sys.executable, "-I", str(SCRIPT), str(self.root), path,
             str(self.root / staging_name), str(limit)], capture_output=True
        )

    def test_unicode_binary(self):
        target = self.outputs / "报告" / "结果.bin"
        target.parent.mkdir()
        data = bytes([0, 1, 255, 13, 10])
        target.write_bytes(data)
        self.assertEqual(self.snapshot("报告/结果.bin", 10).returncode, 0)
        self.assertEqual((self.root / "snapshot/file").read_bytes(), data)

    def test_rejects_paths_outside_outputs(self):
        secret = self.root / "secret"
        secret.write_text("private fixture")
        (self.outputs / "nested").mkdir()
        for index, path in enumerate(("../secret", "nested/../../secret", str(secret))):
            with self.subTest(path=path):
                staging = f"snapshot-{index}"
                self.assertNotEqual(self.snapshot(path, 1024, staging).returncode, 0)
                self.assertFalse((self.root / staging).exists())

    def test_rejects_links_and_oversized_files(self):
        (self.root / "secret").write_text("secret")
        (self.outputs / "link").symlink_to(self.root / "secret")
        (self.outputs / "dir").symlink_to(self.root, target_is_directory=True)
        (self.outputs / "large").write_bytes(b"12345")
        for name in ("link", "dir/secret", "large"):
            with self.subTest(name=name):
                self.assertNotEqual(self.snapshot(name, 4).returncode, 0)


if __name__ == "__main__":
    unittest.main()
