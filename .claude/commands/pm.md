---
description: BERVO project status - issues, PRs, and curation backlog
argument-hint: "status" | [specific question]
---

Report on BERVO project status. Focus: ${ARGUMENTS:-status}

## Repository

`gh issue list --repo bioepic-data/bervo --state open --limit 50`
`gh pr list --repo bioepic-data/bervo --state open`

Identify: stale PRs, issues with no assignee, term requests that could be closed by an
existing term (check with `just find`), and anything blocked on a curator decision.

## Ontology health

```bash
just stats
just validate
```

Report the warning backlog by category — unresolvable relationship labels, orphan
classes, missing types — with counts and a sense of whether it is growing.

## Output

A short status summary, then a prioritised list of what to do next. Flag blockers
explicitly. Do not open, close, or comment on issues unless asked.
