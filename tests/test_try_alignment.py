"""Tests that the TRY alignment map and ``docs/try-alignment.md`` are in sync with their sources."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
BUILDER = REPO_ROOT / "src" / "scripts" / "build_try_alignment.py"
GENERATOR = REPO_ROOT / "src" / "scripts" / "generate_try_doc.py"
MAP = REPO_ROOT / "src" / "scripts" / "try" / "try_alignment.tsv"
PAGE = REPO_ROOT / "docs" / "try-alignment.md"


class TryAlignmentTests(unittest.TestCase):
    def test_committed_map_matches_builder(self) -> None:
        """try_alignment.tsv is generated; it must match a fresh run of build_try_alignment.py."""
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "try_alignment.tsv"
            proc = subprocess.run([sys.executable, str(BUILDER), str(out)],
                                  text=True, capture_output=True)
            self.assertEqual(proc.returncode, 0, f"builder failed:\n{proc.stderr}")
            self.assertEqual(
                out.read_text(encoding="utf-8"), MAP.read_text(encoding="utf-8"),
                "src/scripts/try/try_alignment.tsv is out of date; run `just try-doc` and commit it",
            )

    def test_committed_page_matches_generator(self) -> None:
        """docs/try-alignment.md is generated; it must match a fresh run, with no map problems."""
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "try-alignment.md"
            proc = subprocess.run([sys.executable, str(GENERATOR), str(out)],
                                  text=True, capture_output=True)
            self.assertEqual(proc.returncode, 0, f"generator reported problems:\n{proc.stderr}")
            self.assertEqual(
                out.read_text(encoding="utf-8"), PAGE.read_text(encoding="utf-8"),
                "docs/try-alignment.md is out of date; run `just try-doc` and commit it",
            )


if __name__ == "__main__":
    unittest.main()
