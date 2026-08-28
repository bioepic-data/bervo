---
name: bervo-build
description: Build, validate, and troubleshoot the BERVO ontology - running ROBOT, the ODK make targets, QC checks, the docs site, and the release pipeline. Use when a task involves rebuilding artefacts, diagnosing a failing build or CI run, or preparing a release.
---

# Building and validating BERVO

BERVO is an ODK v1.6 project. The build turns `src/ontology/bervo-src.csv` into an OWL
component, merges it with `bervo-edit.owl`, and emits OWL/OBO/JSON release artefacts.

## The pipeline

```
src/ontology/bervo-src.csv          (source of truth, hand-edited)
  └─ robot template ──▶ src/ontology/components/bervo-src.owl
       └─ merged with src/ontology/bervo-edit.owl
            └─ ODK release ──▶ bervo.owl / bervo.obo / bervo.json
                               bervo-full.owl / .obo / .json

src/ontology/bervo-src.csv
  └─ generate_browser_data.py ──▶ docs/assets/data/bervo-browser.json
       └─ mkdocs build ──▶ site/
```

## Escalation order

Work up this ladder; stop as soon as the problem shows itself. Each rung is slower than
the one above.

| Step | Command | Needs |
| --- | --- | --- |
| 1. Structural validation | `just validate` | Python only — seconds |
| 2. Tests | `just test` | Python, `robot` for the integration tests |
| 3. Component build | `just build` | `robot` on `PATH` |
| 4. Full ODK QC | `just qc` | Docker + `obolibrary/odkfull:v1.6` — slow |

Most template mistakes are caught at step 1. Never jump straight to step 4.

## If `robot` is not installed

Use the Docker wrapper from `src/ontology/`:

```bash
cd src/ontology && sh run.sh make components/bervo-src.owl
```

`run.sh` mounts the repository into `obolibrary/odkfull` and runs make inside it.
`just build-docker` is the same thing.

## What CI runs

- `.github/workflows/qc.yml` — `make test IMP=false PAT=false MIR=false` inside
  `obolibrary/odkfull:v1.6`, then `make integration_test`.
- `.github/workflows/template-qc.yml` — the fast validator and pytest suite.
- `.github/workflows/docs.yml` — regenerates browser data and deploys the mkdocs site.

Reproduce the fast checks locally with `just ci`.

## Troubleshooting

**`robot template` fails with a parse error.** Run `just validate` first — a ragged row
or a bad `SPLIT=|` cell is the usual cause. Note the row number ROBOT reports is a
*physical line*, which differs from the spreadsheet row when a definition contains an
embedded newline.

**A term is missing from the built ontology.** Check its `Type` column. An empty `Type`
defaults to `owl:Class`, but a typo like `Klass` is an error the validator catches.

**A term has an unexpected parent, or none.** `Category` resolves by label. If the label
does not match exactly (including case), ROBOT does not error — it produces a dangling
reference. `just validate` reports these as warnings with a suggested spelling.

**The diff is enormous after a small edit.** The CSV was re-encoded. `bervo-src.csv` uses
CRLF line endings; a writer that emits LF rewrites all 2,300+ rows. Reset and redo the
edit in place.

**ODK QC reports violations.** The queries live in `src/sparql/*-violation.sparql`. Run
one directly against a built artefact:

```bash
robot query -i bervo.owl -q src/sparql/iri-range-violation.sparql /dev/stdout
```

## Releases

Releases go through the ODK pipeline (`make prepare_release`) inside the Docker image, and
are the only time regenerated artefacts belong in a commit. Do not mix a release with a
content change — the artefact diffs bury it.
