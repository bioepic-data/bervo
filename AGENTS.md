# AGENTS.md

Guidance for AI coding agents (Claude Code, Codex, Copilot, Goose) working in the BERVO
repository. `CLAUDE.md`, `.github/copilot-instructions.md`, and `.goosehints` are symlinks
to this file — edit this file, not the symlinks.

## Project overview

**BERVO** (Biological and Environmental Research Variable Ontology, formerly the EcoSIM
Ontology) is an OBO-style ontology of variables and supporting concepts for earth-systems
and environmental modelling. It began as a catalogue of EcoSIM model parameters and has
grown to cover measurement contexts, units, qualifiers, and attributes.

It is built with the [Ontology Development Kit](https://github.com/INCATools/ontology-development-kit)
(ODK v1.6) and released as OWL, OBO, and JSON.

- Browse: <https://bioportal.bioontology.org/ontologies/BERVO>
- Issues: <https://github.com/bioepic-data/bervo/issues>
- Term IRIs use the `https://w3id.org/bervo/BERVO_` base with the `BERVO:` CURIE prefix.

## The one rule that matters most

**`src/ontology/bervo-src.csv` is the source of truth for BERVO terms.** It is a ROBOT
template. Nearly every other ontology file in this repository is generated from it.

Never hand-edit these — your changes will be silently overwritten on the next build:

| Path | Generated from |
| --- | --- |
| `src/ontology/components/bervo-src.owl` | `bervo-src.csv` via `robot template` |
| `bervo.owl`, `bervo.obo`, `bervo.json` | ODK release pipeline |
| `bervo-full.owl`, `bervo-full.obo`, `bervo-full.json` | ODK release pipeline |
| `src/ontology/bervo.owl`/`.obo`/`.json` (transient, produced during a release) | ODK release pipeline |
| `docs/assets/data/bervo-browser.json` | `src/scripts/generate_browser_data.py` |
| `site/` | `mkdocs build` |

Files that **are** hand-edited:

- `src/ontology/bervo-src.csv` — all term content
- `src/ontology/bervo-edit.owl` — the ODK edit file (axioms not expressible in the template)
- `src/ontology/bervo-annotations.ttl` — ontology-level annotations
- `src/ontology/bervo-odk.yaml` — ODK configuration
- `src/sparql/*.sparql` — QC queries
- Anything under `docs/` except `docs/assets/data/`

The Google Sheet linked from the README is a **collaboration artefact only**. It is not
authoritative and must not be used as a build input. Propose changes here, via a branch
and pull request.

## Commands

Everything is exposed through `just` (see `justfile`); `just --list` shows the full set.

```bash
just validate          # structural checks on bervo-src.csv -- run this after every edit
just fix-template      # normalise row widths in bervo-src.csv, then re-validate
just test              # validator + Makefile integration tests
just build             # rebuild components/bervo-src.owl from the CSV
just browser-data      # regenerate the docs browser JSON
just qc                # full ODK QC suite (needs Docker; slow)
just docs              # build the mkdocs site locally
just stats             # term counts by ID block and category
```

The underlying commands, if you need them directly:

```bash
python3 src/scripts/validate_bervo_src.py           # validator
cd src/ontology && make components/bervo-src.owl    # component build (needs robot)
cd src/ontology && make browser_data
cd src/ontology && make test IMP=false PAT=false MIR=false   # ODK QC, inside odkfull
cd src/ontology && sh run.sh make test              # same, wrapped in Docker
```

`robot` must be on `PATH` for a local component build. If it is not, use `sh run.sh make …`
from `src/ontology/`, which runs the ODK Docker image (`obolibrary/odkfull:v1.6`).

## The template contract

`bervo-src.csv` has a two-row header:

1. **Row 1** — human-readable column names (`ID`, `Label (description)`, `Category`, …).
2. **Row 2** — the ROBOT template string for each column (`ID`, `LABEL`, `SC %`,
   `A IAO:0000115`, `TYPE`, `AI BERVO:Attribute SPLIT=|`, …).

Data starts on **row 3**. Both header rows must be preserved verbatim; changing a row-2
template string changes the axioms ROBOT emits for the entire column.

Columns that carry ontology semantics:

| Column | ROBOT template | Meaning |
| --- | --- | --- |
| `ID` | `ID` | The term's CURIE |
| `Label (description)` | `LABEL` | `rdfs:label`; must be unique across the ontology |
| `Category` | `SC %` | Parent class, given as a **label** or an ID. This is the main hierarchy driver. |
| `Parents` | `SC % SPLIT=\|` | Additional parents |
| `Definition` | `A IAO:0000115` | Textual definition |
| `Type` | `TYPE` | `Class`, `owl:AnnotationProperty`, or `owl:ObjectProperty` |
| `Exact Synonyms` / `Related Synonyms` | `A oio:hasExactSynonym` / `hasRelatedSynonym` | `SPLIT=\|` |
| `has_units`, `qualifiers`, `attributes`, `measured_ins`, `measurement_ofs`, `contexts`, `value_types` | `A`/`AI BERVO:…` | References to other BERVO terms, `SPLIT=\|` |
| `involves_chemicals` | `C BERVO:involves_chemicals some % SPLIT=\|` | An OWL **existential restriction**, not an annotation. Each filler must name a class; `NA` is an error, so leave it empty when it does not apply. See "Variables that involve a set of chemicals" in the `bervo-terms` skill. |

Remaining columns are provenance and curation bookkeeping. Two of them matter more than
that sounds: **`EcoSIM Variable Name` and `File Name` are populated on 1,749 of 2,352 terms
(74%)**, recording the model parameter and source file a term came from. `just find`
searches both, so a request phrased in model terms (`just find "Eco_NetRad_col"`) resolves
directly, and a term's EcoSIM source file predicts its `Category` for 32 of the 33 files.
See the "EcoSIM provenance" section of the `bervo-terms` skill.

`EcoSIM Other Names` is populated on zero rows.

Conventions:

- Multi-valued cells are separated by `|` with no surrounding spaces.
- `NA` means "deliberately not applicable"; an empty cell means "not yet filled in".
  Both are ignored by the validator, but they mean different things to curators.
- Every row must have exactly as many fields as the header. Rows appended from a
  spreadsheet export often pick up trailing commas — `just fix-template` trims them.
- The file uses **CRLF** line endings. Preserve them; a whole-file re-encoding turns a
  three-row change into a 2,000-row diff and destroys `git blame`.

## ID allocation

Numeric IDs are 7 digits, allocated in blocks by term kind:

| Block | Range | Kind | Approx. count |
| --- | --- | --- | --- |
| `0xxxxxx` | `BERVO:0000000`–`BERVO:0999999` | Variables (the core parameter terms) | ~1,760 |
| `8xxxxxx` | `BERVO:8000000`–`BERVO:8999999` | Concepts (units, qualifiers, attributes, contexts) | ~550 |
| `9xxxxxx` | `BERVO:9000000`–`BERVO:9999999` | Grouping classes | ~35 |

`BERVO:0000000` ("Variable") is the ontology root.

Nine properties predate this scheme and keep mnemonic local names: `BERVO:has_unit`,
`BERVO:Qualifier`, `BERVO:Attribute`, `BERVO:measured_in`, `BERVO:measurement_of`,
`BERVO:Context`, `BERVO:has_value_type`, `BERVO:involves_taxa`, `BERVO:involves_chemicals`.
Do not invent new mnemonic IDs; if a new property is genuinely needed, raise it in an issue
first, then add it to `MNEMONIC_IDS` in `src/scripts/validate_bervo_src.py`.

**To allocate a new ID**, take the next unused number in the appropriate block:

```bash
just next-id 0     # next free variable ID
just next-id 8     # next free concept ID
just next-id 9     # next free grouping class ID
```

Never reuse an ID, even for a term that was removed. Obsolete terms stay in the template
with an `obsolete ` label prefix and a `replaced_by` where one applies.

> **Known inconsistency:** `src/ontology/bervo-idranges.owl` still declares only
> `0`–`999999` and `1000000`–`1999999`, and uses the old `purl.obolibrary.org/obo/BERVO_`
> prefix rather than the `w3id.org` base actually in use. The `8xxxxxx` and `9xxxxxx`
> blocks are undeclared there. The table above reflects actual practice. Reconciling the
> two is tracked work; do not "fix" the CSV to match the stale idranges file.

## Adding or editing a term

1. Search first — `just find "<text>"` greps IDs, labels, definitions, synonyms, and the
   EcoSIM variable name and source file. Duplicate labels
   are a hard error, and near-duplicates are the most common review finding.
2. Allocate an ID with `just next-id <block>`.
3. Append the row to `src/ontology/bervo-src.csv`, matching the header width exactly.
4. Give it a `Category` that resolves to an existing label or ID.
5. Write a definition. House style: a noun phrase, no leading article, no restating the
   label, and it should read as an ontology definition rather than a dictionary gloss —
   *"The balance between incoming solar shortwave radiation and atmospheric longwave
   radiation…"*, not *"Net radiation is when…"*. Record where it came from in
   `Definition Source`.
6. Run `just validate`. Fix every error; read the warnings and decide.
7. Run `just build` to confirm ROBOT accepts the template.
8. Do **not** commit regenerated release artefacts (`bervo.owl`, `bervo-full.*`, `site/`)
   alongside a term change unless you are cutting a release. They create enormous diffs
   that hide the actual edit.

## Validation

`src/scripts/validate_bervo_src.py` checks what ROBOT does not. ROBOT will happily build a
subtly broken ontology from a broken template, so run the validator first.

**Errors** (fail CI): ragged rows, duplicate IDs, duplicate labels (case-insensitive),
malformed IDs, missing labels, unrecognised `Type`, references to terms that do not exist,
`Category`/`Parents` values that resolve to neither an ID nor a label, and `DbXrefs` values
that are not CURIE-shaped.

**Warnings** (do not fail CI): missing `Type`, IDs outside the allocated blocks, orphan
classes with no parent, mixed `Class`/`owl:Class` spelling, unresolvable relationship
labels, and `DbXrefs` prefixes ROBOT cannot expand (reported once per prefix, not per row).

On cross-references specifically, see the "Cross-references to other ontologies" section of
the `bervo-terms` skill: map concepts rather than variables, verify the target term exists,
and declare any new prefix in `src/ontology/bervo.Makefile` or it is emitted as a broken
relative IRI.

The checked-in template is expected to be error-free at all times;
`tests/test_validate_bervo_src.py` enforces that.

## Working with the ontology from the command line

```bash
runoak -i src/ontology/bervo-edit.owl info BERVO:0000001      # term details
runoak -i src/ontology/bervo-edit.owl tree BERVO:0000000      # hierarchy
robot query -i bervo.owl -q src/sparql/terms.sparql out.tsv   # SPARQL over a release
```

The `src/sparql/` directory holds both reporting queries and `*-violation.sparql` QC
queries that ODK runs during `make test`.

## Pitfalls

1. **Never edit generated files.** If a change seems to belong in `components/bervo-src.owl`
   or a release artefact, it belongs in `bervo-src.csv` or `bervo-edit.owl` instead.
2. **Never re-encode the CSV.** Preserve CRLF endings and existing quoting. Append rows and
   edit cells in place; do not round-trip the whole file through a CSV writer that
   normalises quoting.
3. **`Category` is by label, not ID.** A typo in a category silently creates an
   unresolvable parent. The validator catches it; ROBOT does not.
4. **Labels must be unique.** Case-insensitively. The ontology has had duplicate-label
   bugs before.
5. **Don't touch `bervo-idranges.owl`** to make it agree with the CSV without discussing it
   — see the note under ID allocation.
6. **Don't add release artefacts to a content PR.** `bervo-full.owl` alone is 3.5 MB.
7. **Docker is required for full ODK QC.** `just validate` and `just test` run without it;
   `just qc` does not.

## Repository layout

```
src/ontology/bervo-src.csv      # SOURCE OF TRUTH for all terms
src/ontology/bervo-edit.owl     # ODK edit file
src/ontology/bervo-odk.yaml     # ODK configuration
src/ontology/Makefile           # ODK-generated; do not hand-edit
src/ontology/bervo.Makefile     # BERVO-specific make targets; hand-edited
src/ontology/components/        # generated components
src/scripts/                    # helper scripts (validator, browser data, CSV tools)
src/sparql/                     # reporting and QC queries
tests/                          # pytest suite
docs/                           # mkdocs sources; docs/assets/data is generated
.claude/skills/                 # task-specific agent skills
.claude/rules/                  # path-scoped agent rules
```

## Agent skills

Task-specific instructions live in `.claude/skills/`:

- **bervo-terms** — adding, editing, and reviewing terms in `bervo-src.csv`, including
  EcoSIM provenance and cross-references to other ontologies
- **bervo-build** — building, validating, and releasing
- **bervo-pr-review** — reviewing a pull request that touches ontology content

Path-scoped rules in `.claude/rules/` apply automatically when you touch the files they
name.

## Conventions for agent-authored changes

- One logical change per branch and per pull request.
- Reference the issue number in the branch name (`issue123`) and the PR body.
- Say plainly in the PR what was generated versus hand-written.
- If you regenerate an artefact, say which command produced it so a reviewer can reproduce it.
- When a task is blocked on a curation judgement call (which parent, which definition
  source), surface the question rather than guessing — a wrong parent is harder to find
  later than a missing term.
