"""Tests that the generated AmeriFlux alignment page (``docs/ameriflux-alignment.md``) is in sync."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
GENERATOR = REPO_ROOT / "src" / "scripts" / "generate_ameriflux_doc.py"
PAGE = REPO_ROOT / "docs" / "ameriflux-alignment.md"


class AmerifluxDocTests(unittest.TestCase):
    def test_committed_page_matches_generator(self) -> None:
        """docs/ameriflux-alignment.md is generated; it must match a fresh run, with no coverage problems."""
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "ameriflux-alignment.md"
            proc = subprocess.run([sys.executable, str(GENERATOR), str(out)],
                                  text=True, capture_output=True)
            self.assertEqual(proc.returncode, 0, f"generator reported problems:\n{proc.stderr}")
            self.assertEqual(
                out.read_text(encoding="utf-8"), PAGE.read_text(encoding="utf-8"),
                "docs/ameriflux-alignment.md is out of date; run `just ameriflux-doc` and commit it",
            )


if __name__ == "__main__":
    unittest.main()
