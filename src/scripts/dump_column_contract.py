#!/usr/bin/env python3
"""Regenerate the agent-facing column contract for the BERVO ROBOT template.

The template's second row declares what ROBOT does with each column. That mapping
is what an agent needs in order to edit the CSV safely -- in particular, which
columns are term references (`AI`, `SC`) and which are free-text literals (`A`).

Writes `.claude/skills/bervo-terms/references/column-contract.md`.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = REPO_ROOT / "src" / "ontology" / "bervo-src.csv"
TARGET = REPO_ROOT / ".claude" / "skills" / "bervo-terms" / "references" / "column-contract.md"

PREAMBLE = """# BERVO template column contract

Generated reference for `src/ontology/bervo-src.csv`. Row 1 is the human-readable
header, row 2 is the ROBOT template string, and data starts on row 3.

Regenerate this table with `python3 src/scripts/dump_column_contract.py`.

| # | Column | ROBOT template | Kind |
| --- | --- | --- | --- |"""

EPILOGUE = """
## Reading the template strings

- `SC %` — subclass axiom; `%` is the cell value, resolved as a label or an ID.
- `C <prop> some %` — an OWL existential restriction; `%` must name a class, and the
  property is an ObjectProperty rather than an annotation property.
- `A <prop>` — annotation with a **literal** value.
- `AI <prop>` — annotation whose value is an **IRI**, so the cell must name a term.
- `SPLIT=|` — the cell holds multiple `|`-separated values.

The practical consequence: every `AI`, `SC` and `C` column is checked for referential
integrity by `just validate`; `A` columns are free text.
"""


def classify(template: str) -> str:
    template = template.strip()
    if template == "ID":
        return "identifier"
    if template == "LABEL":
        return "label"
    if template == "TYPE":
        return "OWL type"
    if template.startswith("SC"):
        return "**parent** (label or ID)"
    if template.startswith("AI"):
        return "**term reference** (label or ID)"
    if template.startswith("AT "):
        return "typed literal annotation"
    if template.startswith("A "):
        return "literal annotation"
    if template.startswith("C "):
        return "**restriction filler** (must name a class)"
    return "other"


def main() -> int:
    with TEMPLATE.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.reader(handle))
    if len(rows) < 2:
        print(f"error: {TEMPLATE} is missing its header rows", file=sys.stderr)
        return 2

    header, templates = rows[0], rows[1]
    lines = [PREAMBLE]
    for i, (name, template) in enumerate(zip(header, templates), start=1):
        escaped = template.replace("|", "\\|")
        lines.append(f"| {i} | `{name}` | `{escaped}` | {classify(template)} |")
    lines.append(EPILOGUE)

    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {TARGET.relative_to(REPO_ROOT)} ({len(header)} columns)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
