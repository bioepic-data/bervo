# BERVO - Biological and Environmental Research Variable Ontology

(Formerly the EcoSIM Ontology)

## Browse

<https://bioportal.bioontology.org/ontologies/BERVO>
(OLS coming soon)

## Editing BERVO

The source of truth for BERVO is the repository on this branch.

Editors should update:

- `src/ontology/bervo-src.csv` for the ROBOT template that defines BERVO terms
- `src/ontology/bervo-edit.owl` for the ODK edit file that imports the generated component

All terms are preceded by the BERVO: prefix.

The Google Sheet is still available as a collaboration artifact:

https://docs.google.com/spreadsheets/d/1mS8VVtr-m24vZ7nQUtUbQrN8r-UBy3AwRzTfQsmwVL8/edit?usp=sharing

However, it is no longer the authoritative source for builds or pull requests. Changes should be proposed in this repository, ideally through a GitHub issue and pull request.

To rebuild the generated source component from the tracked CSV, run:

```bash
cd src/ontology
make components/bervo-src.owl
```

To prepare a CSV for uploading back into Google Sheets, run:

```bash
cd src/ontology
make export-google-sheet
```

## Working on BERVO with an AI agent

This repository is set up for AI coding agents (Claude Code, Codex, Copilot, Goose).

- **[AGENTS.md](AGENTS.md)** is the canonical instruction file — the source-of-truth
  rules, the template contract, ID allocation policy, and the pitfalls that matter.
  `CLAUDE.md`, `.github/copilot-instructions.md`, and `.goosehints` are symlinks to it.
- **`.claude/skills/`** holds task-specific guidance: `bervo-terms` for curation,
  `bervo-build` for builds and QC, `bervo-pr-review` for reviewing changes.
- **`.claude/commands/`** provides `/add-term`, `/qc`, and `/pm`.
- A **PostToolUse hook** validates `bervo-src.csv` automatically after any edit.
- Mentioning **`@claude`** on an issue or PR triggers a response, and PRs touching
  ontology content get an automated review. Both need `ANTHROPIC_API_KEY` in the
  repository secrets and are skipped without it.

## Commands

Common tasks are exposed through [`just`](https://just.systems) (`just --list` for all):

```bash
just validate                # structural checks on bervo-src.csv
just find "soil carbon"      # search labels, definitions, synonyms, EcoSIM names
just next-id 0               # next free variable ID
just show BERVO:0000001      # inspect one term
just stats                   # term counts by ID block and category
just test                    # run the test suite
just build                   # rebuild the OWL component from the CSV
```

`just validate` runs `src/scripts/validate_bervo_src.py`, which checks the invariants
ROBOT does not: ragged rows, duplicate IDs and labels, malformed IDs, and references
to terms that do not exist.

## Methods

See also [this slide deck](https://docs.google.com/presentation/d/1W6FHsfv1p4Ko_RVKFgrVg2ruJnZwBW3M9dKoz4HR7n8/edit#slide=id.p)

### Seeding of initial parameter list

chatgpt ADA was used to create a program to iterate through the bervo fortran codebase and generate an obo format file of all parameter codes plus their names.

IDs of the form `BERVO:<CODE>` were created

Note: in future these may be translated to numeric IDs but for now the codes are convenient

### Generation of definitions

The OAK generate-definitions command was used to generate definitions for all terms

### Generation of grouping classes

Each parameter was organized into a grouping class.

We used Claude due to the large context window. A csv of all CODE-label pairs were uploaded to Claude, Claude then suggested groupings for these.
These were examined in text format, we then asked Claude to convert to OBO format.

### Inferring linkages to other concepts

We curated a handful of OBO stanzas where we linked each parameter to other concepts.

This was loaded into a curategpt database, to serve as in-context examples.
