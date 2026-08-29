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

## EcoSIM provenance

BERVO began as a catalogue of EcoSIM model parameters, and that origin is still the single
biggest thing about the term set: **1,749 of 2,352 terms (74%) carry an
`EcoSIM Variable Name` and a `File Name`** naming the EcoSIM source file they came from.

These two columns are provenance, not logical content — `EcoSIM Variable Name` emits
`oio:hasRelatedSynonym` and `File Name` emits `rdfs:comment`, so neither produces an
axiom. Note that the synonym does put the EcoSIM code identifier into the released
ontology, where lexical matchers and search will find it. They are the most useful
handle you have when a term request comes from someone working with the model.

### Finding a term from the model side

`just find` searches the EcoSIM variable name as well as labels and definitions, so a
request phrased in model terms resolves directly:

```bash
just find "Eco_NetRad_col"       # by EcoSIM variable name
just find "CanopyDataType"       # everything from one EcoSIM source file
```

Always try this before creating a term for an EcoSIM parameter. A variable that exists in
the model very often already exists in BERVO under a human-readable label you would not
have guessed from the code identifier.

### The source file usually tells you the category

There are 33 distinct EcoSIM source files, and **32 of them map to one dominant BERVO
`Category`**. This is the strongest placement heuristic available.

Shares run from 60% to 100% across those 32, with one outlier at 19% (see below). The
seven files below are simply the **largest by term count**; their shares are typical
rather than exceptional — the median across all 33 files is 90%, and so is the mean of
these seven. A file's absence from this table says nothing about how strong its prior
is: `SoilPhysDataType.txt` (100%), `MicrobialDataType.txt` (98%) and `SOMDataType.txt`
(97%) are all stronger than most of what is shown. The weaker end — `NitroPars.txt` and
`FlagDataType.txt` at 60%, `ChemTracerParsMod.txt` 62%, `AqueChemDatatype.txt` 66% —
needs a judgement call. Check your own file rather than reading across from these:

| `File Name` | Dominant `Category` | Share |
| --- | --- | --- |
| `SoluteParMod.txt` | Constants for specific chemical reactions | 100% |
| `SoilBGCDataType.txt` | Soil biogeochemistry variable | 98% |
| `SoilWaterDataType.txt` | Soil and water variable | 96% |
| `CanopyDataType.txt` | Canopy variable | 90% |
| `ClimForcDataType.txt` | Climate force variable | 83% |
| `PlantDataRateType.txt` | Plant rate variable | 81% |
| `PlantTraitDataType.txt` | Plant trait variable | 79% |

When adding a term from a known EcoSIM file, check what its file's neighbours use:

```bash
just find "SoilBGCDataType.txt"
```

**The one exception is `EcoSimSumDataType.txt`**: its 32 terms spread across 10 categories
with a top share of 19%, because it is a summary/aggregation file with no natural home. The
heuristic tells you nothing there.

Treat this as a strong prior, not a rule — the minority cases are real, and the category
should still be the most specific correct parent.

### Naming conventions in EcoSIM variable names

Suffixes mark the dimension a variable is resolved over. These are observed conventions,
so confirm against the definition rather than assuming:

| Suffix | Count | Reading |
| --- | --- | --- |
| `_col` | 361 | Column-level, i.e. aggregated over the whole ecosystem column |
| `_vr` | 304 | Vertically resolved, i.e. per soil layer. Only ~19% say so explicitly — confirm |
| `_pft` | 263 | Per plant functional type |
| `_brch` | 70 | Per branch (64% of definitions mention a branch) |
| `_2D`, `_2DH` | 43 | Two-dimensional / horizontal |

Prefixes group tracers and chemistry: `trcg_`, `trcs_`, `trcn_`, `trcSalt_`, `TRChem_`,
`DOM_`, and `Eco_`/`ECO_` for ecosystem-level quantities.

A term whose EcoSIM name differs only by suffix from an existing term is usually a genuinely
distinct variable (a column aggregate and its vertically resolved counterpart are different
things) — but say so explicitly in the definition, or the two become impossible to tell
apart.

> `EcoSIM Other Names` is populated on **zero** rows. Leave it alone rather than inventing a
> use for it.

## Variables that involve a set of chemicals

Some variables apply to *any* chemical rather than a named one — `Gaseous diffusivity`
alongside the specific `Gaseous argon diffusivity`. For those, `involves_chemicals` carries
the fact that a set is involved, and `measurement_ofs` names the medium or class rather than
a substance:

| Term | `measurement_ofs` | `involves_chemicals` |
| --- | --- | --- |
| `Gaseous argon diffusivity` | `Argon` | *(blank)* |
| `Gaseous diffusivity` | `Gas` | `Chemical` |

`involves_chemicals` is the ontology's one **`C … some % SPLIT=|`** column: it emits an OWL
existential restriction rather than an annotation, so its value must name a class. `Chemical`
(`BERVO:8000586`) is the general filler. Do not put a literal or a bare adjective there —
`just validate` reports an unresolvable filler as a hard error.

**`NA` is an error here**, unlike every neighbouring column. In an `AI` column `NA` degrades
to a harmless relative IRI (issue #44); in a restriction it would end up inside a subclass
axiom. Leave the cell empty when the variable does not range over chemicals.

**The variable ranging over many chemicals is what earns the column; the filler is still one
class.** All 50 uses today are the single generic `Chemical` — do not enumerate the
individual substances there. The column is `SPLIT=|` and each filler is checked
independently, so several are possible, but nothing uses that yet and a specific substance
belongs in `measurement_ofs`.

Leave it blank unless the variable genuinely ranges over multiple chemicals. A variable about
one named substance should say so in `measurement_ofs` instead.

## Cross-references to other ontologies

The `DbXrefs` column maps a BERVO term to an equivalent term elsewhere. There are 351
cross-references on 342 terms today — about 15% of the ontology.

### Map concepts, not variables

**338 of the 342 cross-referenced terms are concepts (`8xxxxxx`); only 4 are variables.**
This is the established convention and it makes sense: a concept like *Nitrous oxide* or
*Leaf* has a clean equivalent in an existing ontology, whereas a BERVO variable like
*Cumulative ecosystem heterotrophic respiration* is a model-specific composite that usually
does not. Do not force a mapping onto a variable to fill the column in.

Most terms carry exactly one cross-reference; nine carry two (typically a domain ontology
plus a quality). Leave the column blank when no good match exists — a wrong mapping is
worse than none.

### Which ontology to reach for

| Prefix | Use for | Current count |
| --- | --- | --- |
| `CHEBI` | Chemical entities — *Nitrous oxide* → `CHEBI:17045` | 26 |
| `ENVO` | Environmental materials, features, biomes — *Runoff* → `ENVO:06105211` | 20 |
| `PO` | Plant anatomy and development — *Leaf* → `PO:0025034` | 10 |
| `PATO` | Qualities and properties — *Concentration* → `PATO:0000033` | 9 |
| `GO` | Biological processes — *Biological process* → `GO:0008150` | 1 |
| `AGRO` | Agronomy — *Irrigation* → `AGRO:00000006` | 1 |
| `MIXS` | Sequence-metadata standard fields | 4 |
| `COMO` | Measurement and experiment metadata concepts | 275 |

`COMO` is the dominant prefix and covers the generic measurement/experiment vocabulary
(`BERVO:8000298`–`BERVO:8000527` are largely a systematic COMO mapping): *Experimental
context*, *Replicate series*, *Standard deviation*, *Genome N50*, and so on. Follow that
existing pattern when adding a term in that space.

### Verify the target term exists

Never assert a cross-reference you have not checked — a plausible-looking ID that does not
exist is worse than no mapping, because it looks authoritative.

```bash
runoak -i sqlite:obo:chebi info CHEBI:17045
runoak -i ols:envo info ENVO:06105211
```

### Prefixes must be declared to resolve

`DbXrefs` is declared `AI oio:hasDbXref` — the value is emitted as an **IRI**, not a string.
ROBOT expands OBO-registered prefixes (`CHEBI`, `ENVO`, `PO`, `PATO`, `GO`, `AGRO`, …) to
absolute IRIs automatically. Anything else is emitted as a *relative* IRI, which is
silently meaningless:

```xml
<!-- ENVO: correct, absolute -->
<oboInOwl:hasDbXref rdf:resource="http://purl.obolibrary.org/obo/ENVO_06105211"/>

<!-- COMO: no prefix declaration, so this is a broken relative IRI -->
<oboInOwl:hasDbXref rdf:resource="COMO:0000129"/>
```

`just validate` reports this as one grouped warning per undeclared prefix. **Do not add a
cross-reference using a new prefix without also declaring it** with `--add-prefix` in the
`robot template` call in `src/ontology/bervo.Makefile`, alongside the existing `BERVO:` and
`oio:` declarations.

A `DbXrefs` value that is not CURIE-shaped at all (a bare word such as `Class`) is a hard
error — it usually means a value landed in the wrong column.

### The same trap applies to `NA`

`qualifiers`, `attributes`, `measured_ins`, `measurement_ofs`, `contexts`, and `value_types`
are all `AI` columns too. The `NA` sentinel in them is emitted as a relative IRI exactly like
an undeclared prefix:

```xml
<bervo:BERVO_Qualifier rdf:resource="NA"/>
```

There are ~6,900 of these today (tracked in issue #44). The validator stays silent on them
because `NA` carries a real curatorial meaning in the CSV — "deliberately not applicable", as
opposed to an empty cell meaning "not yet curated". Follow the existing convention when
editing rows; do not start converting `NA` to empty, or vice versa, as a side effect of
another change.

## What not to do

- Do not edit `src/ontology/components/bervo-src.owl` or any `bervo*.owl/obo/json`.
- Do not re-encode or reformat the CSV.
- Do not commit regenerated release artefacts with a term change.
- Do not add new mnemonic (non-numeric) IDs.
