# Alignment with CHESS

The Colorado Headwaters Ecological Spectroscopy Study (CHESS) publishes field
vegetation surveys, leaf area index measurements, soil characterisation, terrain
derivatives, spectroscopy, and LiDAR on
[ESS-DIVE](https://data.ess-dive.lbl.gov/data?query=CHESS). The
[chess-data](https://github.com/bioepic-data/chess-data) repository downloads
those datasets and maps their column names to BERVO. This page records the
terms BERVO added, or amended, so that the mapping resolves. It addresses
[issue #29](https://github.com/bioepic-data/bervo/issues/29).

## Sources

| Source | Used for |
| --- | --- |
| Issue #29 and its correction comment | The gap list. The correction withdraws most of the soil gaps in the original post; the tables below follow the corrected list. |
| `chess-data`, `data/mapped/bervo-mapping-curated.tsv` | The vegetation survey mapping and its `NO_MATCH` rows |

## How the alignment is recorded

- A CHESS column name is written into the term's **`Comment`** after `CHESS:`,
  exactly as the dataset spells it. CHESS headers are dataset-specific rather
  than a controlled vocabulary, so they are not stored as synonyms.
- CHESS measures some quantities that EcoSIM computes, such as leaf area index
  and canopy height. BERVO keeps **one term per quantity**; whether a value was
  observed or modelled belongs to the dataset, not to the term. No observed
  versus modelled term pairs were added.
- Where a CHESS variable already had a BERVO term under another name, the CHESS
  name was added as a synonym and the column names went into the comment.

## CHESS variables mapped to new BERVO terms

### Vegetation structure

| CHESS columns | BERVO term | Parent | Unit |
| --- | --- | --- | --- |
| `Vegetation_Cover`, `Cover_Percent`, `FractionalCover` | Fractional vegetation cover (`BERVO:0001883`) | Land surface variable | `1` |
| | Stem diameter (`BERVO:0001884`) | Plant trait variable | `cm`, `m` |
| `Stem_DBH`, `DBH_1_CM`, `DBH_2_CM`, `DBH_Avg_CM` | Stem diameter at breast height (`BERVO:0001885`) | Stem diameter | `cm` |
| `Crown_Class`, `Canopy_Position` | Crown class (`BERVO:0001886`) | Plant trait variable | categorical |
| `ba` | Stand basal area (`BERVO:0001887`) | Plant trait variable | `m2.har-1` |
| `density`, `abla_density`, `pien_density`, `pico_density` | Stem count per unit area (`BERVO:0001888`) | Plant trait variable | `har-1`, `m-2` |

Stem diameter is the general form and exists so that a diameter taken at a
different height has a home. Stem count per unit area counts stems; Plant population
(`BERVO:0000725`) counts individuals, and the two differ for multi-stemmed
plants.

### Leaf area index

| CHESS columns | BERVO term | Parent | Unit |
| --- | --- | --- | --- |
| `Le_2200`, `Le_FV2200`, `Le_WN` | Effective leaf area index (`BERVO:0001889`) | Canopy variable | `m2.m-2` |
| | Plant area index (`BERVO:0001890`) | Canopy variable | `m2.m-2` |

Plant area index has no CHESS column. It is what an optical canopy analyser
measures before the woody correction, and the corrected columns are derived
from it, so it is here as the quantity the corrections start from.

The method-specific true LAI columns (`L_2200`, `L_SCATCOR`, `L_WN`, `L_LANG`,
`L_ELLIP`, `L_FV2200`) all map to Canopy leaf area index (`BERVO:0001879`).
They differ in retrieval method, not in the quantity. The clumping columns
(`CII`, `ACF_2200`, `ACF_SCATCOR`) map to Apparent clumping factor
(`BERVO:8000562`). The scattering correction factors (`SCATCOR_*`,
`CHI_SCATCOR`, `S_SCATCOR`) are instrument correction terms and were not
given BERVO terms.

### Terrain

| CHESS columns | BERVO term | Parent | Unit |
| --- | --- | --- | --- |
| `twi` | Topographic wetness index (`BERVO:0001891`) | Land surface variable | dimensionless |
| `tpi` | Topographic position index (`BERVO:0001892`) | Land surface variable | `m` |
| `curvature` | Land surface curvature (`BERVO:0001893`) | Land surface variable | `m-1` |
| `heat_load` | Heat load index (`BERVO:0001894`) | Land surface variable | dimensionless |
| `folded_aspect_205` | Folded aspect (`BERVO:0001895`) | Aspect | `deg` |

### Climate

| CHESS columns | BERVO term | Parent | Unit |
| --- | --- | --- | --- |
| `cwd` | Climatic water deficit (`BERVO:0001896`) | Soil and water variable | `mm` |
| `mean annual precipitation` | Mean annual precipitation (`BERVO:0001897`) | Climate force variable | `mm` |

### Soil

| CHESS columns | BERVO term | Parent | Unit |
| --- | --- | --- | --- |
| `infiltrations` | Soil infiltration rate (`BERVO:0001898`) | Soil and water variable | `mm.h-1` |
| `microbial biomass carbon` | Soil microbial biomass carbon (`BERVO:0001899`) | Microbial biomass chemical element | `mg{C}.kg-1` |
| `microbial biomass nitrogen` | Soil microbial biomass nitrogen (`BERVO:0001900`) | Microbial biomass chemical element | `mg{N}.kg-1` |
| `nitrite_nitrogen` | Soil nitrite content (`BERVO:0001901`) | Soil biogeochemistry variable | `mg.kg-1` |
| `manganese` | Soil manganese content (`BERVO:0001902`) | Soil and water variable | `mg{Mn}.kg-1` |
| `zinc` | Soil zinc content (`BERVO:0001903`) | Soil and water variable | `mg{Zn}.kg-1` |
| `lime buffer capacity` | Soil lime buffer capacity (`BERVO:0001904`) | Soil biogeochemistry variable | `mg{CaCO3}.kg-1/{pH}` |

Soil infiltration rate is the capacity measured with an infiltrometer under
an unlimited supply of water. Infiltration into soil (`BERVO:0001821`) is the
flux that actually enters the soil under the rain or irrigation present, the
quantity EcoSIM and ATS exchange. They share a dimension and not a meaning.

## CHESS variables mapped to existing BERVO terms

| CHESS columns | BERVO term | Change made |
| --- | --- | --- |
| `Elevation`, `Elevation_m`, `Topographical_Elevation` | Measurement of altitude (`BERVO:0000683`) | `elevation` added as a related synonym; columns noted in the comment. Three altitude variables overlap (`BERVO:0000670`, `BERVO:0000676`, `BERVO:0000683`) and which one should own the word is not settled |
| `aet` | Evapotranspiration (`BERVO:0001809`) | `actual evapotranspiration` and `AET` added as related synonyms, since a potential evapotranspiration term may follow |
| `swe`, `delta_swe` | Snow water equivalent (`BERVO:0001873`) | none; added for ATS in #65 |
| `L_*` (true LAI, any method) | Canopy leaf area index (`BERVO:0001879`) | none |
| `CII`, `ACF_*` | Apparent clumping factor (`BERVO:8000562`) | none |
| `Terrain_Aspect` | Aspect (`BERVO:0000685`) | none |
| `Vegetation_Height`, `Stem_Height` | Pft canopy height (`BERVO:0000695`) | none |
| `mean annual temperature` | Mean annual temperature (`BERVO:0001371`) | none |
| soil properties listed in the issue's correction comment | as given there | none |

## Not added

- **Taxonomy** (`Taxon_*`, `GBIF_Taxon_ID`, `Vegetation_Species`). Outside
  BERVO's scope. The link from species to plant functional type is a workflow
  question, not a variable.
- **Tree condition** (`Crown_Remaining`, `Health_Status`, `Damage_Mode`,
  `Trunk_Wound`, `Leaves_Remaining`, `Cones_Present`) and **cover type**
  (`Cover_Type`, `Cover_Class_Name`). Field survey classifications with no
  biogeochemical counterpart yet. They can be raised separately if a use
  appears.
- **Spectroscopy and LiDAR products** (hyperspectral reflectance, canopy
  water content from spectra, shade fraction, canopy height model, DTM/DSM).
  Data products rather than variables; deferred.
- **`non-microbial biomass`**, **`mean seasonal temperature`**, and
  **`average seasonal precipitation`**. Too ambiguous to define without the
  dataset's own definition of the season.
- **Administrative columns** (dates, photo references, plot identifiers,
  notes). Not variables.
