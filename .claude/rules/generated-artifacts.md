---
paths:
  - "bervo*.owl"
  - "bervo*.obo"
  - "bervo*.json"
  - "src/ontology/components/**"
  - "src/ontology/bervo.owl"
  - "src/ontology/bervo.obo"
  - "src/ontology/bervo.json"
  - "docs/assets/data/**"
  - "site/**"
---

# Generated artefacts

These files are build products. Do not hand-edit them — the next build overwrites
your change, and the diff hides real edits from reviewers.

The change you want almost certainly belongs in one of:

- `src/ontology/bervo-src.csv` — term content (labels, definitions, relationships)
- `src/ontology/bervo-edit.owl` — axioms the ROBOT template cannot express
- `src/ontology/bervo-annotations.ttl` — ontology-level annotations

Regenerate rather than edit:

| Target | Command |
| --- | --- |
| `src/ontology/components/bervo-src.owl` | `just build` |
| `docs/assets/data/bervo-browser.json` | `just browser-data` |
| `site/` | `just docs` |
| release artefacts (`bervo*.owl/obo/json`) | ODK release pipeline only |

Do not commit regenerated release artefacts alongside a content change unless you
are deliberately cutting a release.
