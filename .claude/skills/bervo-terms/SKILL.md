---
name: bervo-terms
description: Add, edit, or review terms in the BERVO term template (src/ontology/bervo-src.csv). Use whenever a task involves creating a new BERVO term, changing a label, definition, parent, or relationship, resolving a term request issue, or checking whether a concept already exists in the ontology.
---

# Curating BERVO terms

All BERVO term content lives in one ROBOT template: `src/ontology/bervo-src.csv`.
Everything else is generated. See `references/column-contract.md` for the full
column-by-column reference.

## Always search first

```bash
just find "canopy temperature"
just show BERVO:0000123
```

Most term requests are already covered by an existing term or a synonym. If you find
a near match, propose adding a synonym to the existing term rather than a new term —
duplicate and near-duplicate terms are the hardest problem to unwind later.

## Adding a term

1. **Search** (above). Confirm it does not exist.
2. **Pick the block and allocate an ID:**

   | Block | Use for | Command |
   | --- | --- | --- |
   | `0xxxxxx` | Variables — measurable/computable model quantities | `just next-id 0` |
   | `8xxxxxx` | Concepts — units, qualifiers, attributes, contexts, materials | `just next-id 8` |
   | `9xxxxxx` | Grouping classes — organisational parents | `just next-id 9` |

   If you are unsure whether something is a variable or a concept: a *variable* is
   something a model reports or consumes as a number over time; a *concept* is
   something used to describe or qualify a variable.

3. **Choose a parent.** `Category` takes the parent's **label**. Find candidates with
   `just find`, and prefer an existing grouping class over inventing a new one.
4. **Append the row**, matching the header width exactly and preserving CRLF endings.
   Append in place — do not rewrite the file.
5. **Write a definition.** House style:
   - A noun phrase describing what the term *is*, not a sentence starting with the label.
   - No leading article; do not restate the label as a definition.
   - Say what it measures and, where it matters, over what and in what context.
   - Good: *"The balance between incoming solar shortwave radiation and atmospheric
     longwave radiation versus reflected shortwave and outgoing longwave radiation
     from terrestrial surfaces and vegetation."*
   - Bad: *"Net radiation is when radiation is net."*
   - Record provenance in `Definition Source`, e.g. `Definition source - Manual (JHC, Sep 25 2025)`.
6. **Fill the relationship columns** where they apply — `has_units` (literal unit
   string, or `NONE`), `attributes`, `measured_ins`, `measurement_ofs`, `qualifiers`,
   `contexts`, `value_types`. Each of those except `has_units` must name an existing
   term. Use `NA` for "deliberately not applicable" and leave blank for "not yet done".
7. **Validate and build:**

   ```bash
   just validate
   just build
   ```

## Editing an existing term

- Changing a **label** changes the ontology's public surface and breaks any
  `Category`/relationship cell that referenced the old label. After a label change,
  run `just validate` and fix the references it flags.
- Never change an **ID**. If a term is wrong, obsolete it rather than repurposing it.
- To obsolete: prefix the label with `obsolete `, and record a `replaced_by` where a
  successor exists. Keep the row; never delete it and never reuse the ID.

## Interpreting validator output

Errors always block. Warnings need a judgement call:

| Warning | What to do |
| --- | --- |
| `references '<label>' … did you mean '<other>'?` | Almost always a case or spelling typo. Fix it. |
| `references '<label>', which is not a term label` (no suggestion) | Either the target term needs creating, or the cell should be a literal. Ask a curator if unclear. |
| `has no Type` | Set `Class` unless it is a property. |
| `has no Category and no Parents` | Give it a parent unless it is the root or a property. |
| `ID … outside the allocated blocks` | You allocated by hand. Use `just next-id`. |

There is a known backlog of unresolvable-label warnings in `qualifiers`,
`measurement_ofs`, and `contexts`. Do not bulk-fix them as a side effect of an
unrelated task — they need curator judgement about whether the target term should
exist. Fix only the ones your change touches.

## What not to do

- Do not edit `src/ontology/components/bervo-src.owl` or any `bervo*.owl/obo/json`.
- Do not re-encode or reformat the CSV.
- Do not commit regenerated release artefacts with a term change.
- Do not add new mnemonic (non-numeric) IDs.
