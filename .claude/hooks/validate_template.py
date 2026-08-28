#!/usr/bin/env python3
"""Claude Code PostToolUse hook: validate bervo-src.csv after it is edited.

Registered in `.claude/settings.json` for Edit/Write/MultiEdit. It runs only when
the edited file is the BERVO term template, so it costs nothing on other edits.

Exit codes follow the PostToolUse contract: 0 means "carry on", 2 means "feed
this back to the model". Structural errors in the source of truth are worth
interrupting for; warnings are not.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = REPO_ROOT / "src" / "ontology" / "bervo-src.csv"
VALIDATOR = REPO_ROOT / "src" / "scripts" / "validate_bervo_src.py"


def edited_paths(payload: dict) -> list[str]:
    tool_input = payload.get("tool_input") or {}
    candidates = [tool_input.get("file_path"), tool_input.get("notebook_path")]
    for edit in tool_input.get("edits") or []:
        if isinstance(edit, dict):
            candidates.append(edit.get("file_path"))
    return [c for c in candidates if c]


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0  # Never let a malformed payload block the session.

    if not any(Path(p).name == TEMPLATE.name for p in edited_paths(payload)):
        return 0

    if not VALIDATOR.exists() or not TEMPLATE.exists():
        return 0

    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(TEMPLATE)],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        return 0

    errors = [ln for ln in result.stdout.splitlines() if ln.startswith("ERROR")]
    print(
        "bervo-src.csv failed validation after your edit:\n"
        + "\n".join(errors[:20])
        + ("\n… and more" if len(errors) > 20 else "")
        + "\n\nFix these before continuing. `just fix-template` handles row-width errors; "
          "everything else needs a real edit. See AGENTS.md for the template contract.",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
