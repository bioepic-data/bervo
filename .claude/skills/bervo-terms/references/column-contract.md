# BERVO template column contract

Generated reference for `src/ontology/bervo-src.csv`. Row 1 is the human-readable
header, row 2 is the ROBOT template string, and data starts on row 3.

Regenerate this table with `python3 src/scripts/dump_column_contract.py`.

| # | Column | ROBOT template | Kind |
| --- | --- | --- | --- |
| 1 | `ID` | `ID` | identifier |
| 2 | `Label (description)` | `LABEL` | label |
| 3 | `Category` | `SC %` | **parent** (label or ID) |
| 4 | `EcoSIM Other Names` | `A oio:hasRelatedSynonym SPLIT=\|` | literal annotation |
| 5 | `EcoSIM Variable Name` | `A oio:hasRelatedSynonym ` | literal annotation |
| 6 | `File Name` | `A rdfs:comment` | literal annotation |
| 7 | `Definition` | `A IAO:0000115` | literal annotation |
| 8 | `Comment` | `A rdfs:comment` | literal annotation |
| 9 | `Related Synonyms` | `A oio:hasRelatedSynonym SPLIT=\|` | literal annotation |
| 10 | `Exact Synonyms` | `A oio:hasExactSynonym SPLIT=\|` | literal annotation |
| 11 | `Type` | `TYPE` | OWL type |
| 12 | `DbXrefs` | `AI oio:hasDbXref SPLIT=\|` | **term reference** (label or ID) |
| 13 | `has_units` | `A BERVO:has_unit SPLIT=\|` | literal annotation |
| 14 | `qualifiers` | `AI BERVO:Qualifier SPLIT=\|` | **term reference** (label or ID) |
| 15 | `attributes` | `AI BERVO:Attribute SPLIT=\|` | **term reference** (label or ID) |
| 16 | `measured_ins` | `AI BERVO:measured_in SPLIT=\|` | **term reference** (label or ID) |
| 17 | `measurement_ofs` | `AI BERVO:measurement_of SPLIT=\|` | **term reference** (label or ID) |
| 18 | `contexts` | `AI BERVO:Context SPLIT=\|` | **term reference** (label or ID) |
| 19 | `value_types` | `AI BERVO:has_value_type SPLIT=\|` | **term reference** (label or ID) |
| 20 | `Parents` | `SC % SPLIT=\|` | **parent** (label or ID) |
| 21 | `Group Curated?` | `A rdfs:comment` | literal annotation |
| 22 | `Definition Curated?` | `A rdfs:comment` | literal annotation |
| 23 | `Definition Source` | `A rdfs:comment` | literal annotation |
| 24 | `Comment from Ulas` | `A rdfs:comment` | literal annotation |
| 25 | `Comment from Joan` | `A rdfs:comment` | literal annotation |
| 26 | `Comment from John-Marc` | `A rdfs:comment` | literal annotation |
| 27 | `Comment from Jinyun` | `A rdfs:comment` | literal annotation |
| 28 | `Comment from Harry` | `A rdfs:comment` | literal annotation |
| 29 | `Comment from Chris` | `A rdfs:comment` | literal annotation |

## Reading the template strings

- `SC %` — subclass axiom; `%` is the cell value, resolved as a label or an ID.
- `A <prop>` — annotation with a **literal** value.
- `AI <prop>` — annotation whose value is an **IRI**, so the cell must name a term.
- `SPLIT=|` — the cell holds multiple `|`-separated values.

The practical consequence: every `AI` and `SC` column is checked for referential
integrity by `just validate`; `A` columns are free text.
