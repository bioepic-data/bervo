# Alignment with HWSD2 and soil classification systems

The [Harmonized World Soil Database v2.0](https://www.fao.org/soils-portal/data-hub/soil-maps-and-databases/harmonized-world-soil-database-v20/en/)
(HWSD2), published by FAO and IIASA, gives soil properties for every 30
arc-second cell of the land surface, in seven depth layers to 200 cm, and
classifies each soil in WRB 2022 and in the FAO-90 legend. This page records
how its fields are represented in BERVO. It also adds the soil classification
systems requested in
[issue #120](https://github.com/bioepic-data/bervo/issues/120): USDA Soil
Taxonomy and the Unified Soil Classification System (USCS).

## Source

| Source | Revision | Used for |
| --- | --- | --- |
| [`bioepic-data/fao-soils`](https://github.com/bioepic-data/fao-soils), `src/fao_soils/schema/fao_soils.yaml` | `b2a58f5` | Field names, units, and code lists, as structured in LinkML |
| same repository, `data/hwsd2/HWSD2_csv/` | same | `HWSD2_LAYERS_METADATA.csv`, `HWSD2_SMU_METADATA.csv`, and the `D_*` lookup tables, which are FAO's own |

HWSD2 has two attribute tables. `HWSD2_SMU` has one row per soil mapping unit,
and `HWSD2_LAYERS` has one row per soil component and depth layer. Several
fields appear in both, sometimes under different names, such as `BULK` in the
layer table and `BULK_DENSITY` in the mapping unit table.

## How the alignment is recorded

This follows the [ATS alignment](ats-alignment.md):

- The HWSD2 field name is stored on the BERVO term as a **related synonym**,
  spelled as in the FAO tables (`ORG_CARBON`, not `org_carbon`). Field names that
  are plain English words, `SAND`, `SILT`, `CLAY`, `COARSE`, `BULK`, `GYPSUM`,
  `DRAINAGE`, and `SHARE`, are left out, because as synonyms they would match the
  material rather than the variable.
- The term's **`Comment`** starts with `HWSD2:` and gives the field name and its
  HWSD2 unit in brackets.
- A unit HWSD2 uses that BERVO did not list is **appended to `has_units`** when it
  is a distinct unit (`g.cm-3` on Soil bulk density, `cm` on the depths).
  Percentages are not: BERVO writes a fraction as `1` and a mass content as
  `g.kg-1`, so an HWSD2 value in `% weight` is ten times smaller than the same
  value in `g.kg-1`.

HWSD2 fields are not cross-referenced in `DbXrefs`. The fao-soils schema
declares `https://w3id.org/bioepic-data/fao-soils/hwsd2/` as its namespace, but
that IRI is not registered with w3id and returns 404, so a cross-reference to it
would never resolve. Once it resolves, the field names on this page can become
`DbXrefs`, or the mappings can be carried from the fao-soils side as
`exact_mappings` on each slot.

## HWSD2 fields mapped to existing BERVO terms

| HWSD2 field | HWSD2 unit | BERVO term | Note |
| --- | --- | --- | --- |
| `SAND` | % weight | Soil sand content (`BERVO:0001526`) | |
| `SILT` | % weight | Soil silt content (`BERVO:0001527`) | |
| `CLAY` | % weight | Soil clay content (`BERVO:0001528`) | |
| `COARSE` | % volume | Soil coarse fraction (`BERVO:0002038`) | Volume basis |
| `BULK`, `BULK_DENSITY` | g/cm3 | Soil bulk density (`BERVO:0001535`) | `g.cm-3` added |
| `ORG_CARBON` | % weight | Soil organic carbon content (`BERVO:0001523`) | |
| `CN_RATIO` | | Soil carbon to nitrogen mass ratio (`BERVO:0002053`) | HWSD2 does not state the basis; mass is the convention |
| `CEC_SOIL` | cmolc/kg | Soil cation exchange capacity (`BERVO:0000883`) | |
| `BSAT` | % of CEC | Soil base saturation (`BERVO:0002025`) | |
| `KOPPEN` | | Köppen climate zone (`BERVO:0000235`) | HWSD2 gives the main group only, A to E |
| `BOTDEP` | cm | Depth to bottom of soil layer (`BERVO:0000974`) | `cm` added |
| `NSC_MU_SOURCE1`, `NSC_MU_SOURCE2` | | Soil classification (`BERVO:0002041`) | A national classification; comment only |

## HWSD2 fields that needed new variables

| HWSD2 field | HWSD2 unit | New BERVO term | BERVO unit |
| --- | --- | --- | --- |
| `TOTAL_N` | g/kg | Soil total nitrogen content (`BERVO:0002159`) | `g.kg-1` |
| `PH_WATER` | -log(H+) | Soil pH in water (`BERVO:0002160`), under Soil pH | `1` |
| `CEC_CLAY` | cmolc/kg | Soil clay fraction cation exchange capacity (`BERVO:0002161`) | `cmol.kg-1{clay}` |
| `CEC_EFF` | cmolc/kg | Soil effective cation exchange capacity (`BERVO:0002162`) | `cmol.kg-1` |
| `TEB` | cmolc/kg | Soil total exchangeable bases (`BERVO:0002163`) | `cmol.kg-1` |
| `ALUM_SAT` | % of ECEC | Soil aluminum saturation (`BERVO:0002164`) | `1` |
| `ESP` | % | Soil exchangeable sodium fraction (`BERVO:0002165`) | `1` |
| `TCARBON_EQ` | % weight | Soil calcium carbonate equivalent (`BERVO:0002166`) | `g.kg-1` |
| `GYPSUM` | % weight | Soil gypsum content (`BERVO:0002167`) | `g.kg-1` |
| `ELEC_COND` | dS/m | Soil saturation extract electrical conductivity (`BERVO:0002168`) | `dS.m-1` |
| `REF_BULK`, `REF_BULK_DENSITY` | g/cm3 | Soil reference bulk density (`BERVO:0002169`) | `Mg.m-3`, `g.cm-3` |
| `AWC` (mapping unit table) | mm/m | Soil available water capacity (`BERVO:0002170`) | `mm.m-1` |
| `AWC` (layer table) | mm | Root zone available water capacity (`BERVO:0002171`) | `mm` |
| `DRAINAGE` | class | Soil drainage class (`BERVO:0002172`) | `NA` |
| `ROOT_DEPTH`, `ROOTS` | class, cm ranges | Rootable soil depth (`BERVO:0002173`) | `m`, `cm` |
| `IL` | cm ranges | Depth to impermeable layer (`BERVO:0002174`) | `m`, `cm` |
| `SWR` | class | Soil water regime class (`BERVO:0002175`) | `NA` |
| `PHASE1`, `PHASE2` | class | Soil phase (`BERVO:0002176`) | `NA` |
| `TOPDEP` | cm | Depth to top of soil layer (`BERVO:0002177`) | `m`, `cm` |
| `SHARE` | % | Soil mapping unit component share (`BERVO:0002178`) | `1` |
| `WRB2`, `WRB4`, `WRB_PHASES` | class | WRB soil classification (`BERVO:0002179`) | `NA` |
| `FAO90` | class | FAO-90 soil classification (`BERVO:0002180`) | `NA` |
| `TEXTURE_USDA` | class | USDA soil texture classification (`BERVO:0002183`) | `NA` |
| `TEXTURE_SOTER` | class | SOTER soil texture classification (`BERVO:0002184`) | `NA` |

`Gypsum` (`BERVO:8000981`, `CHEBI:48838`) was added under `Mineral` as the
`measurement_ofs` of Soil gypsum content.

Points to note:

- **Two `AWC` fields.** The layer table's `AWC` is not a per-layer value. In the
  fao-soils copy of HWSD2 it is filled only on layer D1, once for each of the
  58,405 soil components, and is the total over the rootable depth in mm. The
  mapping unit table's `AWC` is a capacity per metre of soil. They are two
  variables.
- **Depths reported as classes.** `ROOT_DEPTH`, `ROOTS`, and `IL` give a depth as a
  class or a range of centimetres. The BERVO terms are the depths themselves,
  with units, so the same terms serve data that give a measured depth.
  `ROOT_DEPTH` and `ROOTS` both map to Rootable soil depth: the first is HWSD2's
  own class, the second the European Soil Database's depth of an obstacle to
  roots.
- **Total soil nitrogen is not total soil nitrogen.** The existing term Total soil
  nitrogen (`BERVO:0000324`, EcoSIM `TGasN_lnd`) is defined as nitrogen gas in soil
  air. `TOTAL_N` maps to the new Soil total nitrogen content instead. The label of
  `BERVO:0000324` is misleading and needs its own issue.
- **Electrical conductivity.** HWSD v1.2 named the field `T_ECE` and `S_ECE`, the
  conductivity of a saturated paste extract. That is distinct from Bulk
  electrical conductivity (`BERVO:0002036`), read in place by a sensor, and from
  EcoSIM's Measured electrical conductivity (`BERVO:0001703`), whose method is not
  stated.

## HWSD2 fields not mapped

| HWSD2 field | Why |
| --- | --- |
| `ID`, `HWSD2_SMU_ID`, `WISE30s_SMU_ID`, `HWSD1_SMU_ID`, `NSC` | Database identifiers and codes |
| `COVERAGE` | Which source database a record came from |
| `SEQUENCE` | Order of a component within its mapping unit; recorded in the comment on Soil mapping unit component share |
| `LAYER` | Layer code `D1` to `D7`; Depth to top and Depth to bottom of soil layer carry the depths |
| `WRB2_CODE` | Numeric code for `WRB2` |
| `ROOT_DEPTH_LAYER`, `AWC_LAYER` | Not present in the FAO tables; the fao-soils schema names the layer table's `ROOT_DEPTH` and `AWC` this way |
| `ADD_PROP` | Gelic or vertic properties. Neither a phase nor a classification; left until a use appears |

## Soil classification systems

Each system is a variable under Soil classification (`BERVO:0002041`) or Soil
texture class (`BERVO:0002040`), and, where its classes are few enough to list,
a grouping concept under `Soil` whose children are the classes.

| System | Variable | Classes in BERVO | ENVO cross-references |
| --- | --- | --- | --- |
| World Reference Base for Soil Resources, 2022 | WRB soil classification (`BERVO:0002179`) | 32 reference soil groups under WRB reference soil group (`BERVO:8000982`) | 31 of 32; ENVO has no Retisol |
| FAO-UNESCO Soil Map of the World, revised legend (FAO-90) | FAO-90 soil classification (`BERVO:0002180`) | None; 193 units in HWSD2 | |
| USDA Soil Taxonomy | USDA Soil Taxonomy classification (`BERVO:0002181`) | 12 orders under USDA soil order (`BERVO:8001015`) | Ultisol only |
| USDA soil texture triangle | USDA soil texture classification (`BERVO:0002183`) | 12 classes, plus heavy and light clay, under USDA soil texture class (`BERVO:8001028`) | 9 of 12 |
| SOTER texture | SOTER soil texture classification (`BERVO:0002184`) | None; five classes in the comment | |
| Unified Soil Classification System (ASTM D2487) | USCS soil classification (`BERVO:0002182`) | 15 groups under USCS soil group (`BERVO:8001043`) | None in ENVO |

A USDA order is cross-referenced only to an ENVO class labelled with that order.
That is why Ultisol (`ENVO:01001397`) has one and the other orders do not. ENVO's
cryosol (`ENVO:00002236`) carries *gelisol* as an exact synonym, and its ferralsol
(`ENVO:00002246`) carries *oxisol*. Both classes are labelled and defined by the
WRB group, and the WRB group and the USDA order draw their boundaries
differently. So Gelisol and Oxisol stay unmapped, rather than being asserted
equivalent to a WRB class.

Below the reference soil group and the order, the WRB qualifiers (191 `WRB4`
units and 556 `WRB_PHASES` units in HWSD2), the FAO-90 units, and the lower
levels of Soil Taxonomy are recorded as values of the classification variables,
not as BERVO classes. Each WRB group's `Comment` gives its HWSD2 `WRB2` code where
it has one, and each texture class its `TEXTURE_USDA` code, so HWSD2 data can be
read onto the classes directly. Durisol is the one group without a code: HWSD2
does not use it.

These codes were checked against `D_WRB2.csv`, `D_WRB4.csv`, and
`D_TEXTURE_USDA.csv` at `b2a58f5`. All 31 `WRB2` codes and all 13
`TEXTURE_USDA` codes match the class they are on. No `WRB2` or `WRB4` code is a
Durisol. The four `WRB2` codes on no BERVO class, `GG`, `IS`, `ND`, and `WR`, are
glaciers, islands, no data, and open water.

Label choices:

- **WRB and USDA share two names.** Histosol and Vertisol are both WRB reference
  soil groups and USDA orders, with different criteria. The WRB groups take the
  plain label, because ENVO's `histosol` and `vertisol` are WRB definitions; the
  USDA orders are `Histosol (USDA)` and `Vertisol (USDA)`.
- **Three texture classes share a name with a particle-size fraction.** BERVO's
  `Sand`, `Silt`, and `Clay` are the particle-size fractions, so the texture
  classes are `Sand texture class`, `Silt texture class`, and `Clay texture class`.
  The other nine take their plain names. ENVO's sand, silt, and clay are likewise
  the materials, which is why those three have no cross-reference.
- **Heavy and light clay** are FAO's subdivision of the USDA clay class at 60
  percent clay, used by HWSD2's `TEXTURE_USDA` codes 1 and 3.
- **USCS group names** follow ASTM D2487, except where the plain name would
  collide: `ML` is Low-plasticity silt, `OL` and `OH` are Low-plasticity and
  High-plasticity organic soil, and `PT` is Highly organic soil. Each group's
  symbol is a related synonym.

Definitions of the classes follow IUSS Working Group WRB (2022), Soil Survey
Staff (2022) *Keys to Soil Taxonomy*, 13th edition, the USDA *Soil Survey
Manual* (2017), FAO (2006) *Guidelines for Soil Description*, and ASTM D2487,
and each row's `Definition Source` says which.

## Points to note for fao-soils

- `TextureUSDAEnum` in `fao_soils.yaml` lists 9 of the 13 codes in
  `D_TEXTURE_USDA.csv`. It is missing sandy clay loam, sandy loam, loamy sand, and
  sand.
- The fao-soils documentation gives silt as 0.05 to 0.002 mm, which agrees with
  BERVO's `Silt`. The ODM2 definition quoted in that term's comment gives 0.002 to
  0.5 mm, which is ODM2's error.
