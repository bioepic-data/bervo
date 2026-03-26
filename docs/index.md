# BERVO Documentation

[//]: # "This file is meant to be edited by the ontology maintainer."

Welcome to the BERVO documentation!

BERVO is the Biological and Environmental Research Variable Ontology.

## Editing workflow

BERVO now follows a repo-first editing workflow:

- `src/ontology/bervo-src.csv` is the authoritative source of term content
- `src/ontology/bervo-edit.owl` is the ODK editor file
- `src/ontology/components/bervo-src.owl` is generated from the tracked CSV during the build

The Google Sheet is retained as a secondary collaboration artifact, but it is not the source of truth for releases or pull requests.

Please open a GitHub issue for requested changes when possible, and submit ontology edits through this repository.

You can find descriptions of the standard ontology engineering workflows [here](odk-workflows/index.md).
