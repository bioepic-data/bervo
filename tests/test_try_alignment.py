"""Tests that the TRY alignment map agrees with the template and that ``docs/try-alignment.md`` is in sync."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
GENERATOR = REPO_ROOT / "src" / "scripts" / "generate_try_doc.py"
PAGE = REPO_ROOT / "docs" / "try-alignment.md"


class TryAlignmentTests(unittest.TestCase):
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
