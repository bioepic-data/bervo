"""Check that hand-written ROBOT template strings in docs match bervo-src.csv row 2 (issue #57)."""

import csv
import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = REPO_ROOT / "src" / "ontology" / "bervo-src.csv"
DOC_FILES = (
    REPO_ROOT / "AGENTS.md",
    REPO_ROOT / ".claude" / "skills" / "bervo-terms" / "SKILL.md",
    REPO_ROOT / ".claude" / "rules" / "term-template.md",
)

TEMPLATE_PREFIXES = ("A ", "AI ", "AT ", "SC ", "C ")
TEMPLATE_EXACT = {"ID", "LABEL", "TYPE"}

# Deliberately abbreviated shorthands in prose (contain an ellipsis, not a literal cell).
ILLUSTRATIVE_ALLOWLIST = {
    "AI BERVO:…": "AGENTS.md shorthand for BERVO:Qualifier, BERVO:Attribute, etc.",
    "C … some % SPLIT=|": "SKILL.md shorthand covering involves_chemicals and part_ofs",
}


def extract_template_strings(text: str) -> list[tuple[int, str]]:
    """Return (line_number, normalized_string) for backtick-quoted ROBOT template spans."""
    found: list[tuple[int, str]] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        for match in re.finditer(r"`([^`]+)`", line):
            candidate = match.group(1).replace(r"\|", "|")
            if candidate in TEMPLATE_EXACT or candidate.startswith(TEMPLATE_PREFIXES):
                found.append((lineno, candidate))
    return found


class TestDocTemplateStrings(unittest.TestCase):
    def test_doc_robot_template_strings_match_csv_row2(self):
        with TEMPLATE.open(encoding="utf-8", newline="") as handle:
            reader = csv.reader(handle)
            next(reader)
            row2 = set(next(reader))

        mismatches: list[str] = []
        checked = 0
        for doc in DOC_FILES:
            rel = doc.relative_to(REPO_ROOT)
            for lineno, template_str in extract_template_strings(doc.read_text(encoding="utf-8")):
                if template_str in ILLUSTRATIVE_ALLOWLIST:
                    continue
                checked += 1
                if template_str not in row2:
                    mismatches.append(f"{rel}:{lineno}: {template_str!r} is not in bervo-src.csv row 2")

        self.assertGreater(checked, 0, "Expected to find ROBOT template strings in docs")
        self.assertEqual(mismatches, [], "\n".join(mismatches))


if __name__ == "__main__":
    unittest.main()
