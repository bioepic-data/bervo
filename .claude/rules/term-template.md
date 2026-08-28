---
paths:
  - "src/ontology/bervo-src.csv"
---

# Editing the BERVO term template

`bervo-src.csv` is the source of truth for every BERVO term. A subtle break here
propagates into every release artefact, and ROBOT will not stop you.

**Before editing:** search for an existing term with `just find "<text>"`. Duplicate
labels are a hard error and near-duplicates are the most common review finding.

**While editing:**

- Row 1 is human-readable headers, row 2 is the ROBOT template strings, data starts
  on row 3. Never reorder, rename, or reflow the first two rows.
- Every row must have exactly the header's field count.
- The file is **CRLF**. Append and edit in place; never round-trip the whole file
  through a CSV writer — it re-encodes 2,000+ untouched rows and destroys `git blame`.
- `Category` and `Parents` take a term **label** or ID. `qualifiers`, `attributes`,
  `measured_ins`, `measurement_ofs`, `contexts`, and `value_types` also resolve to
  terms. `has_units` holds **literal** unit strings and is not a reference.
- Allocate IDs with `just next-id <0|8|9>`. Never reuse a retired ID.

**After editing:** run `just validate`. A PostToolUse hook runs it automatically and
will interrupt you on errors. Fix every error; read the warnings and decide
deliberately. `just fix-template` resolves row-width errors only.
