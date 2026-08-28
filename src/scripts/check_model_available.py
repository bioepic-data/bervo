#!/usr/bin/env python3
"""Check that a configured Claude model is available to the current API key.

Used by the agentic GitHub workflows as a preflight. `claude-code-action` hides
its output, so an auth or model-access problem otherwise surfaces only as an
opaque `is_error: true` after several minutes of running. This turns it into a
clear message in seconds.

Takes the JSON body of `GET /v1/models` and the desired model id. Never reads or
prints the API key itself.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(f"usage: {Path(argv[0]).name} <models.json> <model-id>", file=sys.stderr)
        return 2

    payload, wanted = Path(argv[1]), argv[2].strip()
    try:
        available = [m["id"] for m in json.loads(payload.read_text())["data"]]
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"::error::Could not parse the model list: {exc}")
        return 1

    print("Models available to this key:")
    for model in available:
        print(f"  {model}")

    if not wanted:
        print("::error::No model was configured; check .github/agent-config.yaml.")
        return 1

    # Claude Code may append a context-window suffix such as "[1m]" to the id it
    # actually requests, so compare on the base id too.
    base = wanted.split("[")[0]
    if any(model == wanted or model.startswith(base) for model in available):
        print(f"Configured model {wanted!r} is available.")
        return 0

    print(
        f"::error::Configured model {wanted!r} is not available to this API key. "
        f"Pick one of the models listed above and set it in .github/agent-config.yaml."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
