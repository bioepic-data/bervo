# Alignment with a survey of ESS-DIVE datasets

[TROWEL](https://github.com/bioepic-data/trowel) extracted the variable names from
10 public [ESS-DIVE](https://ess-dive.lbl.gov/) datasets, drawn at random from
those submitted between 2023-10-15 and 2026-10-15. This page records how each
name is represented in BERVO, and the terms added for the ones it lacked
([issue #171](https://github.com/bioepic-data/bervo/issues/171)).

## Source

| Source | Revision | Used for |
| --- | --- | --- |
| [`bioepic-data/trowel`](https://github.com/bioepic-data/trowel), `data/essdive_random10_2026-10-15/` | `3b114b8` | `variable_names.tsv` (189 names), `data_dictionaries.tsv`, and the dataset methods in `results.tsv` |

Seven of the ten datasets supplied names. Three keep their data in zip archives
or images and supplied none: the meteoric 10Be flux calibration, the
manganese-carbon model output, and the Utqiagvik phenology camera imagery. The
one name from the tundra land surface modelling archive,
`196.19585    64.862976     1     1`, is a data row read as a header.

The counts below are per dataset, so a name used by two datasets counts in
both. They sum to 192, or 193 with the tundra name. Four names appear in two
datasets each, `treatment`, `depth`, `site`, and `date`, which leaves the 189
unique names in `variable_names.tsv`.

| Dataset | Names | Topic |
| --- | --- | --- |
| [doi:10.15485/2395957](https://doi.org/10.15485/2395957) | 5 | Active layer and permafrost temperature, Teller 47, Alaska |
| [doi:10.15485/3412618](https://doi.org/10.15485/3412618) | 22 | XANES, NEXAFS, and SANS of mineral-coated sands, Walker Branch, Tennessee |
| [doi:10.15485/3015733](https://doi.org/10.15485/3015733) | 111 | Flooded coastal forest soil mesocosms: gas fluxes, porewater chemistry, CDOM, FTIR |
| [doi:10.15485/2475392](https://doi.org/10.15485/2475392) | 14 | Leaf mass per area and leaf carbon and nitrogen, Seward Peninsula, Alaska |
| [doi:10.15485/2998439](https://doi.org/10.15485/2998439) | 21 | Porewater chemistry in a brackish tidal marsh, Plum Island, Massachusetts |
| [doi:10.15485/3020155](https://doi.org/10.15485/3020155) | 19 | Fungal mat growth and litter colonization, TRACE warming experiment, Puerto Rico |

## Reducing names to variables

Most of the 189 names are not distinct variables. They reduce to about 45, by
these rules:

- **Summary and treatment suffixes are dropped.** The mesocosm dataset reports
  each porewater analyte as a mean and a standard deviation for each of three
  treatments: `c` (control), `fw` (freshwater flood), and `bw` (brackish water
  flood). `sulfate fw mean`, `sulfate bw std`, and the other five combinations
  are all Dissolved sulfate concentration.
- **Per-sample columns are not variables.** `day 28 rep 2`, `quartz rep 1`,
  `fe oxide-coated sand rep 1`, `c before`, `fw after`, and similar names head
  the columns of a spectrum, one per sample. In the same way, `c1` to `bw2` in
  the moisture file are one column of soil water content per mesocosm. The variable is the absorbance or
  scattering intensity on the y axis. `energy`, `wavenumbers`, `scattering vector`,
  and the like are the x axis.
- **Fit statistics are not variables.** `fco2 dry r2`, `fch4 dry lin`, and
  `fn2o dry lin r2` record which model a flux came from, linear or exponential,
  and how well it fitted.
- **Abbreviations are expanded** from the dataset's own data dictionary or
  methods text: `hix`, `bix`, `fi`, `sr`, `suva`, `lma`, `pf`, `pftemp`,
  `pfdepth`, `eh`.

## Survey names mapped to existing BERVO terms

| Survey names | BERVO term | Note |
| --- | --- | --- |
| `pfdepth` | Active layer depth of a permafrost soil (`BERVO:0001522`) | A probe reading of 120 cm means no permafrost was reached |
| `avg temperature` | Soil temperature (`BERVO:0001477`) | |
| `c1`, `c2`, `fw1`, `fw2`, `bw1`, `bw2` | Volumetric water content (`BERVO:0001743`) | One column per mesocosm in the moisture file |
| `cnratio` | Plant tissue carbon to nitrogen mass ratio (`BERVO:0002055`) | Leaf tissue |
| `doc …` | Dissolved organic carbon concentration (`BERVO:0001670`) | Already defined for soil water |
| `suva …` | Specific ultraviolet absorbance (`BERVO:0002104`) | |
| `hix …` | Humification index (`BERVO:0002109`) | |
| `fi …` | Fluorescence index (`BERVO:0002108`) | |
| `fco2 dry` | Carbon dioxide flux (`BERVO:0001943`) | Chamber flux from soil |
| `co2 dry mean`, `ch4 dry mean`, `n2o dry mean`, `h2o mean` | Not mapped | Chamber headspace mole fractions and water vapor; see below |
| `eh …` | Redox potential (`BERVO:8000349`) | A concept that carries `ODM2:variablename/reductionPotential` |
| `ph …` | pH (`BERVO:8000261`) | A concept; BERVO has pH variables for soil, precipitation, irrigation, and wastewater, not for water in general |
| `ch4 flag`, `fe flag`, `hs flag`, … | Quality control flag (`BERVO:8000563`) | Six flags |
| `easting`, `northing` | Easting (`BERVO:8000440`), Northing (`BERVO:8000441`) | |
| `normalized absorption` | Absorbance (`BERVO:8000236`) | Y axis of the XANES and NEXAFS spectra |
| `rep` | Biological replicate (`BERVO:8000420`) | |

## New terms

### Concepts

| New BERVO term | Parent | Cross-reference | From |
| --- | --- | --- | --- |
| Pore water (`BERVO:8001059`) | Environmental material | none; see below | Both porewater datasets |
| Permafrost (`BERVO:8001060`) | Environmental material | `ENVO:00000134` | Teller 47 |
| Iron(II) (`BERVO:8001061`) | Ion | `CHEBI:29033` | `fe` |
| Dissolved sulfide (`BERVO:8001062`) | Chemical pool | none | `hs`, `sulfide …` |
| Carbon-13 (`BERVO:8001063`) | Isotope | `CHEBI:36928` | `delta 13ch4` |
| X-ray absorption near edge structure spectroscopy (`BERVO:8001064`) | Method | `CHMO:0000305` | Walker Branch |
| Small-angle neutron scattering (`BERVO:8001065`) | Method | `CHMO:0000184` | Walker Branch |
| Fourier transform infrared spectroscopy (`BERVO:8001066`) | Method | `CHMO:0000636` | Mesocosms |

### Variables

| Survey names | New BERVO term | Parent | BERVO unit | Cross-reference |
| --- | --- | --- | --- | --- |
| `lma` | Leaf mass per area (`BERVO:0002185`) | Plant trait variable | `g.m-2` | |
| `c area` | Leaf carbon content per unit area (`BERVO:0002186`) | Plant trait variable | `g{C}.m-2` | |
| `n area` | Leaf nitrogen content per unit area (`BERVO:0002187`) | Plant trait variable | `g{N}.m-2` | |
| `c mass` | Leaf carbon content per unit dry mass (`BERVO:0002188`) | Plant trait variable | `mg{C}.g-1{dry_mass}` | |
| `n mass` | Leaf nitrogen content per unit dry mass (`BERVO:0002189`) | Plant trait variable | `mg{N}.g-1{dry_mass}` | |
| `pftemp` | Temperature at the top of permafrost (`BERVO:0002190`) | Soil heat variable | `Cel`, `K` | |
| `pf` | Near-surface permafrost presence (`BERVO:0002191`) | Soil variable | `NA` | |
| `dic …` | Dissolved inorganic carbon concentration (`BERVO:0002192`) | Water quality variable | `mg{C}.L-1` | `carbonDissolvedInorganic` |
| `fe`, `fe …` | Dissolved ferrous iron concentration (`BERVO:0002193`) | Water quality variable | `umol.L-1` | |
| `mn …` | Dissolved manganese concentration (`BERVO:0002194`) | Water quality variable | `umol.L-1` | `manganeseDissolved` |
| `hs`, `sulfide …` | Dissolved sulfide concentration (`BERVO:0002195`) | Water quality variable | `umol.L-1` | `sulfideDissolved` |
| `so4`, `sulfate …` | Dissolved sulfate concentration (`BERVO:0002196`) | Water quality variable | `umol.L-1` | `sulfateDissolved` |
| `cl` | Dissolved chloride concentration (`BERVO:0002197`) | Water quality variable | `umol.L-1` | `chlorideDissolved` |
| `nh4`, `nh4 …` | Dissolved ammonium concentration (`BERVO:0002198`) | Water quality variable | `umol.L-1` | |
| `nh3 …` | Dissolved ammonia concentration (`BERVO:0002199`) | Water quality variable | `umol.L-1` | |
| `nox …` | Dissolved nitrate plus nitrite concentration (`BERVO:0002200`) | Water quality variable | `umol.L-1` | `nitrogenDissolvedNitrite_NO2_Nitrate_NO3` |
| `po4` | Dissolved orthophosphate concentration (`BERVO:0002201`) | Water quality variable | `umol.L-1` | `phosphorusOrthophosphateDissolved` |
| `ch4` | Dissolved methane concentration (`BERVO:0002202`) | Water quality variable | `umol.L-1` | `methaneDissolved` |
| `bix …` | Biological index (`BERVO:0002203`) | Water quality variable | `1` | |
| `sr …` | Spectral slope ratio (`BERVO:0002204`) | Water quality variable | `1` | |
| `fresh …` | Freshness index (`BERVO:0002213`) | Water quality variable | `1` | |
| `fch4 dry` | Methane flux (`BERVO:0002205`) | Surface flux variable | `nmol.m-2.s-1`, `umol.m-2.s-1` | |
| `fn2o dry` | Nitrous oxide flux (`BERVO:0002206`) | Surface flux variable | `nmol.m-2.s-1`, `umol.m-2.s-1` | |
| `delta 13ch4` | Methane delta carbon-13 (`BERVO:0002207`) | Delta carbon-13 | `[ppth]` | `delta_13COfCH4` |
| `initial area`, `final area`, `raw growth` | Fungal mat area (`BERVO:0002208`) | Ecology variable | `cm2` | |
| `relative growth rate weekly` | Fungal mat relative growth rate (`BERVO:0002209`) | Ecology variable | `d-1` | |
| `colonization status` | Litter colonization status (`BERVO:0002210`) | Ecology variable | `NA` | |
| `time to colonization` | Time to litter colonization (`BERVO:0002211`) | Ecology variable | `d` | |
| `number dry days week` | Number of dry days (`BERVO:0002212`) | Meteorological variable | `1` | |

Cross-references in the last column are ODM2 variable names, written in full as
`ODM2:variablename/<name>`.

## Points to note

- **Solute variables are for any water.** The porewater analytes became
  variables measured in Water, not in Pore water, so that one set serves
  porewater, stream, and groundwater data alike. Pore water is a concept that
  porewater data can name as the medium. The one exception predates this page:
  Dissolved organic carbon concentration (`BERVO:0001670`) is an EcoSIM variable
  defined for soil water.
- **Only ODM2 names that say "dissolved" are cross-referenced.** ODM2's
  `ironFerrous`, `nitrogen_NH4`, and `nitrogen_NH3` do not say whether the sample
  was filtered, so they are broader than the BERVO variables and are recorded
  only in each term's `Comment`. ODM2 has no names for methane or nitrous oxide
  flux, biological index, or spectral slope ratio.
- **Molar units for solutes.** Both porewater datasets report solutes in `uM` or
  `mM`, so BERVO uses `umol.L-1`. The ODM2 nitrogen names are "as nitrogen",
  which a molar unit makes no different. Carbon is the exception: dissolved
  carbon is conventionally reported by mass, in `mg{C}.L-1`.
- **Pore water is not cross-referenced to ENVO.** ENVO's interstitial water
  (`ENVO:03600009`) is defined for rocks and sediments, and BERVO's term also
  covers soil.
- **XANES and NEXAFS are one method.** CHMO treats them as synonyms. The Walker
  Branch dataset uses NEXAFS for the carbon K-edge and XANES for the iron and
  manganese K-edges.
- **Chamber headspace concentrations are not added.** `co2 dry mean` and its
  methane and nitrous oxide counterparts are dry-air mole fractions inside a
  closed chamber, an intermediate result in calculating a flux. `h2o mean` is
  the water vapor reading from the same analyzer, not soil moisture.
- **Biological index and freshness index are two variables.** Both use
  excitation at 310 nm and emission at 380 nm. The biological index divides by
  the emission at 430 nm, and the freshness index (beta:alpha) by the maximum
  between 420 and 435 nm. The mesocosm dataset reports them in separate columns.
- **`raw growth` is a change in Fungal mat area,** final minus initial, so it
  maps to the area variable.
- **Leaf mass per area is not cross-referenced** to specific leaf area
  (`TO:0000562`), which is its reciprocal.

## Stable isotope variables

`delta 13ch4` was BERVO's first isotope delta variable, so it came without a
parent. Rather than place one variable under an ill-fitting grouping, the
review of this alignment added the stable isotope deltas from the ODM2
variable names as a family, with the concepts they need.

| BERVO term | Parent | Reference standard (`contexts`) | ODM2 variable name |
| --- | --- | --- | --- |
| Stable isotope variable (`BERVO:9000047`) | Variable | | |
| Delta carbon-13 (`BERVO:0002214`) | Stable isotope variable | Vienna Pee Dee Belemnite | `carbon_13StableIsotopeRatioDelta` |
| Delta deuterium (`BERVO:0002215`) | Stable isotope variable | Vienna Standard Mean Ocean Water | `hydrogen_2_StableIsotopeRatioDelta` |
| Delta nitrogen-15 (`BERVO:0002216`) | Stable isotope variable | Atmospheric nitrogen standard | `nitrogen_15_StableIsotopeRatioDelta` |
| Delta oxygen-18 (`BERVO:0002217`) | Stable isotope variable | Vienna Standard Mean Ocean Water, Vienna Pee Dee Belemnite | `oxygen_18_StableIsotopeRatioDelta` |
| Methane delta carbon-13 (`BERVO:0002207`) | Delta carbon-13 | Vienna Pee Dee Belemnite | `delta_13COfCH4` |
| Carbon dioxide delta carbon-13 (`BERVO:0002218`) | Delta carbon-13 | Vienna Pee Dee Belemnite | `delta_13COfCO2` |
| Dissolved inorganic carbon delta carbon-13 (`BERVO:0002219`) | Delta carbon-13 | Vienna Pee Dee Belemnite | `delta_13COfDIC` |
| Ethane delta carbon-13 (`BERVO:0002220`) | Delta carbon-13 | Vienna Pee Dee Belemnite | `delta_13COfC2H6` |
| Propane delta carbon-13 (`BERVO:0002221`) | Delta carbon-13 | Vienna Pee Dee Belemnite | `delta_13COfC3H8` |
| Butane delta carbon-13 (`BERVO:0002222`) | Delta carbon-13 | Vienna Pee Dee Belemnite | `delta_13COfC4H10` |
| Water delta oxygen-18 (`BERVO:0002223`) | Delta oxygen-18 | Vienna Standard Mean Ocean Water | `delta_18OOfH2O` |
| Water delta deuterium (`BERVO:0002224`) | Delta deuterium | Vienna Standard Mean Ocean Water | `delta_DOfH2O` |
| Methane delta deuterium (`BERVO:0002225`) | Delta deuterium | Vienna Standard Mean Ocean Water | `delta_DOfCH4` |

All take `[ppth]`, UCUM's parts per thousand (per mil), and Isotope delta in
`attributes`. `measurement_ofs` names the isotope, and the substance where there
is one.

New concepts:

| BERVO term | Parent | Cross-reference |
| --- | --- | --- |
| Isotope delta (`BERVO:8001067`) | Relative value | |
| Isotope reference standard (`BERVO:8001068`) | Concept | |
| Vienna Pee Dee Belemnite (`BERVO:8001069`) | Isotope reference standard | |
| Vienna Standard Mean Ocean Water (`BERVO:8001070`) | Isotope reference standard | |
| Atmospheric nitrogen standard (`BERVO:8001071`) | Isotope reference standard | |
| Propane (`BERVO:8001072`) | Alkane | `CHEBI:32879` |
| Butane (`BERVO:8001073`) | Alkane | `CHEBI:37808` |

- **The reference standard goes in `contexts`.** It is the condition the value
  is reported under, like Standard ambient temperature on a rate. Delta
  oxygen-18 names both standards, because carbonates and carbon dioxide are
  reported against Vienna Pee Dee Belemnite.
- **Not added:** ODM2's `carbon_14` and `tritium_3H_DeltaTOfH2O`. Both isotopes
  are radioactive and are reported as activities, ages, or tritium units, not as
  a stable isotope delta, so they belong to a different family.

## Survey names left unmapped

| Survey names | Reason |
| --- | --- |
| `treatment`, `phase`, `site`, `plot`, `season` | Experimental design, recorded as metadata |
| `sampleid`, `ch4 sample id`, `fungal mat id` | Identifiers |
| `species`, `genus`, `common name`, `usda plants symbol`, `usda citation`, `fungi species` | Taxonomy |
| `date`, `start date`, `end date`, `week start`, `week end`, `time edt`, `time est`, `total weeks`, `n` | Dates and times; `n` is days since the mesocosm experiment began |
| `scattering intensity`, `scattering vector`, `energy`, `wavenumbers` | Spectrum axes |
| `fco2 dry r2`, `fco2 dry lin`, `fco2 dry lin r2`, and the methane and nitrous oxide equivalents | Flux fit statistics |
