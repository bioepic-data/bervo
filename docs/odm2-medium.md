# Alignment with ODM2 medium

The ODM2 **medium** vocabulary (<http://vocabulary.odm2.org/medium/>) names
the physical medium of a specimen, reference material, or sampled environment.
In BERVO that role is carried by the `measured_in` relationship, so the
vocabulary maps onto the concepts that `measured_ins` names. This page records
the mapping. It is the second step on
[issue #66](https://github.com/bioepic-data/bervo/issues/66), after the
[speciation vocabulary](odm2-speciation.md).

## Source

The SKOS export at <http://vocabulary.odm2.org/api/v1/medium/?format=skos>,
fetched on 2026-09-18. It holds 20 concepts and the scheme. Cross-references
take the form `ODM2:medium/<id>`, using the `ODM2` prefix declared for the
speciation alignment; each emitted IRI redirects (301) to the same path with a
trailing slash, which returns the concept page. The ODM2 definition is quoted
in the term's `Comment`.

## ODM2 concepts mapped to existing BERVO terms

| ODM2 concept | BERVO term | Note |
| --- | --- | --- |
| `Soil` | Soil (`BERVO:8000062`) | |
| `Air` | Air (`BERVO:8000050`) | |
| `Gas` | Gas (`BERVO:8000086`) | |
| `Snow` | Snow (`BERVO:8000103`) | |
| `Ice` | Ice (`BERVO:8000027`) | |
| `Sediment` | Sediment (`BERVO:8000160`) | |
| `Tissue` | Tissue (`BERVO:8000494`) | |
| `Liquid aqueous` | Water (`BERVO:8000102`) | Water is the medium `measured_ins` already names 90 times; ODM2's concept is any aqueous liquid |
| `Equipment` | Instrument (`BERVO:8000306`) | ODM2 means the instrument or sensor as the thing measured, as in battery voltage |

`Not applicable`, `Unknown`, and `Other` are placeholders of the vocabulary and
are not mapped.

## New terms

| BERVO term | Parent | ODM2 concept | Other cross-reference |
| --- | --- | --- | --- |
| Vegetation (`BERVO:8000716`) | Concept | `Vegetation` | |
| Organism (`BERVO:8000717`) | Concept | `Organism` | `COB:0000022` |
| Habitat (`BERVO:8000718`) | Concept | `Habitat` | `ENVO:01000739` |
| Rock (`BERVO:8000719`) | Concept | `Rock` | `ENVO:00001995` |
| Mineral (`BERVO:8000720`) | Chemical | `Mineral` | `CHEBI:46662` |
| Regolith (`BERVO:8000721`) | Concept | `Regolith` | `ENVO:01000747` |
| Particulate matter (`BERVO:8000722`) | Concept | `Particulate` | `ENVO:01000060` |
| Organic liquid (`BERVO:8000723`) | Concept | `Liquid organic` | |

## Points to note

- Plant (`BERVO:8000021`) carried `vegetation` as an exact synonym. ODM2
  defines vegetation as the plant cover of an area, not taxonomically, which
  is a different thing from a plant. Vegetation is now its own term and
  `vegetation` is a related synonym of Plant.
- Soil (`BERVO:8000062`) carried `regolith` as a related synonym. Regolith
  includes soil rather than naming it, so the synonym is dropped.
- Where a term carries more than one ODM2 comment, as Water does, each quoted
  definition ends with a period before the next begins.
- Plant (`BERVO:8000021`) and Microbes (`BERVO:8000091`) move under the new
  Organism from Concept. Bacteria stays under Microbes.
- Mineral sits under Chemical, following CHEBI, and Apatite (`BERVO:8000052`)
  moves under it from Chemical. See the last point for its second parent.
- `COB` joins the validator's list of OBO prefixes ROBOT can expand, for the
  Organism cross-reference.
- The material media now sit under Environmental material
  (`BERVO:8000402`), which came from COMO with no children and is the same
  notion as ODM2 medium. Soil, Air, Gas, Sediment, Litter, Rock, Regolith,
  Particulate matter, and Organic liquid have it as `Category`. Water and
  Mineral keep Chemical as `Category` and take Environmental material as a
  second parent through `Parents`, so Rock and Mineral meet under one class.
  Environmental material gains `ENVO:00010483` and Mineral gains
  `ENVO:01000256` (mineral material) beside its CHEBI reference. Snow, Ice,
  and Surface water inherit through Water. Tissue, Vegetation, Organism,
  Habitat, and Instrument are media in ODM2 but not materials, and stay where
  they are.
