#!/usr/bin/env python3
"""Resolve the Claude model for an agentic workflow from .github/agent-config.yaml.

Keeping the model choice in one config file means bumping a tier is a one-line
edit rather than a sweep across every workflow YAML.

Resolution order: --model-override, then the per-workflow `model`, then
`default_model`. Writes `model=<id>` to $GITHUB_OUTPUT and AGENT_MODEL to
$GITHUB_ENV when those are set.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - the runner always has PyYAML
    print("error: PyYAML is required to resolve the agent config", file=sys.stderr)
    raise SystemExit(2)

DEFAULT_CONFIG = Path(__file__).resolve().parents[2] / "agent-config.yaml"
FALLBACK_MODEL = "claude-sonnet-5"


def resolve(config_path: Path, workflow: str, override: str | None) -> str:
    if override:
        return override

    if not config_path.exists():
        print(f"warning: {config_path} not found; falling back to {FALLBACK_MODEL}", file=sys.stderr)
        return FALLBACK_MODEL

    config = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    workflows = config.get("workflows") or {}
    entry = workflows.get(workflow) or {}

    if isinstance(entry, dict) and entry.get("model"):
        return str(entry["model"])
    return str(config.get("default_model") or FALLBACK_MODEL)


def emit(name: str, value: str, env_var: str) -> None:
    for var, line in (("GITHUB_OUTPUT", f"{name}={value}"), ("GITHUB_ENV", f"{env_var}={value}")):
        path = os.environ.get(var)
        if path:
            with open(path, "a", encoding="utf-8") as handle:
                handle.write(line + "\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workflow", required=True, help="workflow file stem, e.g. 'claude-code-review'")
    parser.add_argument("--model-override", default="", help="explicit per-run override")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    args = parser.parse_args(argv)

    model = resolve(args.config, args.workflow, args.model_override.strip() or None)
    print(f"{args.workflow}: model={model}")
    emit("model", model, "AGENT_MODEL")
    return 0


if __name__ == "__main__":
    sys.exit(main())
