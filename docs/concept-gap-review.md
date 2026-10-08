# Concept gap review

The ODM2 alignments of September 2026 added 184 concepts. Variables reference
seven of them. That prompted a review of the 1,622 live variables beneath the Variable root to find the
concepts they name but the ontology lacks, and the concepts it has that they
cannot reach. This page records the method, what the first pass added, and
what remains.

## Method

Every variable label was tokenised and its words, bigrams, and trigrams
counted, and each was checked against every concept label and synonym. The
same was done for definitions, weighted lower. A word that recurs across many
labels and matches nothing on the concept side is a gap. A word that matches
a concept which the variable's relationship columns do not name is a linking
gap. Counts below are labels naming the thing unless they say otherwise.

## Added in the first pass

| BERVO term | Parent | Cross-reference | Variables asking for it |
| --- | --- | --- | --- |
| Demand (`BERVO:8000770`) | Concept |  | 29 labels; all carried `attributes=Uptake` |
| Microbial functional group (`BERVO:8000771`) | Microbes |  | "microbial" in 100 labels, "functional group" in 9 |
| Heterotrophic microbes (`BERVO:8000772`) | Microbial functional group |  | "heterotrophic microbial" in 18 labels |
| Autotrophic microbes (`BERVO:8000773`) | Microbial functional group |  | "autotrophic microbial" in 19 |
| Aerobic heterotrophs (`BERVO:8000774`) | Heterotrophic microbes |  | "aerobic bacteria" in 3 |
| Fermenters (`BERVO:8000775`) | Heterotrophic microbes |  | 4 |
| Denitrifiers (`BERVO:8000776`) | Heterotrophic microbes |  | 10 |
| Nitrifiers (`BERVO:8000777`) | Autotrophic microbes |  | 14 |
| Methanogens (`BERVO:8000778`) | Microbial functional group |  | 6 |
| Acetotrophic methanogens (`BERVO:8000779`) | Methanogens |  | 2 |
| Hydrogenotrophic methanogens (`BERVO:8000780`) | Methanogens |  | 3 |
| Methanotrophs (`BERVO:8000781`) | Microbial functional group |  | 1 |
| Diazotrophs (`BERVO:8000782`) | Microbial functional group |  | "diazotroph" 3, "nitrogen fixer" 1 |
| Fungi (`BERVO:8000783`) | Microbes | `NCBITaxon:4751` | 4 |
| Mycorrhizal fungi (`BERVO:8000784`) | Fungi |  | "myco" and "mycorrhizal" in 6 |
| Plant functional type (`BERVO:8000785`) | Concept |  | `pft` in 8 labels and 266 EcoSIM names, 15 definitions |
| Chemical transformation (`BERVO:8000786`) | Process |  | "transformation" in 24 labels |
| Time step (`BERVO:8000787`) | Time |  | 19 labels |
| Iteration (`BERVO:8000788`) | Concept |  | 5 labels |
| Water potential (`BERVO:8000789`) | Physical property |  | 22 labels |
| Turgor potential (`BERVO:8000790`) | Water potential |  | 4 |
| Osmotic potential (`BERVO:8000791`) | Water potential |  | 4 |
| Latent heat (`BERVO:8000792`) | Heat |  | 7 |
| Sensible heat (`BERVO:8000793`) | Heat |  | 4 |
| Convective heat (`BERVO:8000794`) | Heat |  | 6 |
| Field capacity (`BERVO:8000795`) | Water content | `ENVO:06105302` | 8 |
| Wilting point (`BERVO:8000796`) | Water content | `ENVO:06105303` | 6 |
| Population (`BERVO:8000797`) | Concept |  | 12 labels |
| Primary axes (`BERVO:8000798`) | Concept |  | 8; Secondary axes existed |
| Groundwater (`BERVO:8000799`) | Water | `ENVO:01001004` | 68 definitions |
| Dissolved organic matter (`BERVO:8000800`) | Chemical pool |  | 7 labels |
| Particulate organic matter (`BERVO:8000801`) | Chemical pool | `ENVO:04000012` | 1 label; the parallel of DOM |
| Particulate organic carbon (`BERVO:8000802`) | Organic carbon | `ENVO:04000013` | 1 label; the parallel of DOC |

The 29 variables whose label says "demand" carried `attributes=Uptake`. They
now carry `Demand`. No other variable was changed.

### Placement notes

- The microbial groups sit under Microbes in two ways. Fungi is a taxon-like
  group beside Bacteria, with Mycorrhizal fungi beneath it. The rest are
  metabolic roles under Microbial functional group, and Aerobic heterotrophs,
  Fermenters, and Denitrifiers sit under Heterotrophic microbes, Nitrifiers
  under Autotrophic microbes, and the two kinds of methanogen under
  Methanogens. The set is the set EcoSIM parameterizes. Two of them are
  modes rather than pools in the model, and their `Comment` says so:
  fermentation is an anaerobic mode of the heterotrophic carbon pool, and
  the acetotrophic and hydrogenotrophic methanogens are two pathways of one
  methanogen pool. The terms exist for the parameters that name them. This
  is as far into microbial metabolism as BERVO means to go.
- Methanogens are archaea. BERVO has no Archaea term, so the group sits as a
  metabolic role; if Archaea is added (`NCBITaxon:2157`) it is a second
  parent. EcoSIM's parameters call the aerobic heterotrophs aerobic
  bacteria, and the term's `Comment` records that.
- Latent, Sensible, and Convective heat sit under Heat as kinds of heat, not
  under Heat flux. The variables that name them are fluxes, and those carry
  Heat flux in `attributes` already; the new terms went in `measurement_ofs`,
  saying which heat the flux is of. Done, and the three no longer sit flat.

  They were added as three siblings, which read as alternatives. They are not.
  Latent and Sensible divide heat by **thermodynamic form**, by what a transfer
  does to a body. Convective divides it by **transfer mechanism**, by how the
  energy moves. Heat carried convectively is also sensible heat. Two grouping
  classes now hold the two axes apart:

  ```
  Heat (BERVO:8000092)
    Heat by thermodynamic form (BERVO:9000036)
      Latent heat, Sensible heat
    Heat by transfer mechanism (BERVO:9000037)
      Convective heat, Conductive heat, Radiative heat
  ```

  Conductive heat (`BERVO:8000803`) and Radiative heat (`BERVO:8000804`) were
  added with the groupings, because an axis with one member is not an axis and
  the variables name all three mechanisms. A variable may carry one term from
  each axis, and six now do, such as Ecosystem sensible heat flux, whose
  definition says "through conduction and convection".

  Counts: Latent 11, Sensible 5, Convective 11, Conductive 5, Radiative 1. The
  generic Heat went from 62 rows to 49. Five rows are fluxes by their units
  that had no `Heat flux` attribute and now do.

  Heat capacity, Heat flux and Heat content remain flat under Heat. They are
  quantities of heat rather than kinds of it, and sorting that out is a
  separate question.
- Dissolved organic matter and Particulate organic matter have Chemical pool
  as `Category` and Organic matter as a second parent, as Soil organic
  matter does. Particulate organic matter also takes Particulate matter,
  mirroring ENVO.
- Plant functional type sits under Concept beside Taxon. It is a way of
  classing plants, not a plant and not vegetation.
- Iteration sits under Concept rather than under Time. A solver pass is not
  an interval of time.
- Field capacity and Wilting point sit under Water content, which is what
  ENVO says they are. `ENVO:06105303` is labelled "permanent wilting point"
  there; that is an exact synonym here.
- Chemical transformation carries `transformation` as a related synonym,
  since that is the word the 24 variable labels use. It is not exact: the
  bare word is wider, and Plant transformant uses it in the genetic sense.

## Remaining gaps

These were found in the same pass and not acted on.

**Processes.** Process has 24 descendants (#51 folded in Biological process,
Fixation and Community assembly process, which sat beside it under Concept).
The variables name many more processes than that, mostly in definitions: Photosynthesis (61
definitions; only C4 photosynthesis exists and it sits under Concept),
Decomposition (101), Transpiration (32), Evapotranspiration (24),
Nitrification (31), Denitrification (29), Deposition (35), Interception (32),
Infiltration (26), Leaching (21), Dissolution (21), Immobilization (13),
Volatilization (12), Freeze-thaw (12), Exudation (8), Ebullition, Adsorption,
Disturbance (18), and Growth respiration and Maintenance respiration under
Respiration.

**Phenology.** Leafout (12 labels), Senescence (7), Leafoff (5), Hardening
(5), Dehardening (5). Phenological progress and Growth stage exist and are
referenced once between them.

**Management.** Land management and Amendment have no children. Fertilizer,
Harvest, and Irrigation sit directly under Concept. The variables name
Planting (7), Side-dressing (5), Tillage, Manure, Lime, Crop residue. Crop is
in 67 definitions with no concept.

**Spatial.** Column (8 labels, 361 `_col` EcoSIM names) and Profile (49
definitions, 304 `_vr` names) are the two dimensions the EcoSIM set is
resolved over and neither has a concept. Watershed (22 definitions) and
Permafrost (10) have ENVO classes.

## Existing concepts that should change

- Non-structural carbohydrate and Non-structural organic compounds live under
  Chemical pool; 38 labels say "nonstructural" and no synonym bridges the
  hyphen. Non-structural C3 content sits under Content.
- Reserve is what the variables call storage (13 labels, 106 definitions).
- Aqueous is what the variables call dissolved (39 labels).
- Altitude is what CHESS calls elevation.
- Surface carries `boundary` as an exact synonym; in 23 labels "boundary"
  means the model domain edge.
- Surface, Ground surface, Soil surface, and Land surface sit apart, and Soil
  surface lists `ground surface` as its own synonym.
- Canopy could sit under Vegetation; Snowpack under Environmental feature;
  Rainfall under Precipitation with Snowfall added; Harvest, Fertilizer, and
  Irrigation under Land management; Water table under Subsurface. Ecosystem,
  Biome, Landscape, Region, Zone, Grid cell, Habitat, and Community are all
  loose under Concept.
- Dead standing tree should carry `standing dead` (4 labels).

## Variables that should point at the new concepts

Tracked as [issue #83](https://github.com/bioepic-data/bervo/issues/83), and
done in slices. The five bullets below were the first slice; all five are
settled.

- ~~Rock fraction and the two "Soil volume including macropores and rock" rows
  name Rock and reference nothing.~~ Done. All three name Rock in
  `measurement_ofs`, and the two volume rows name Macropore beside it.
- ~~Eleven of the 27 Sediment variables have `measured_ins=NA`.~~ Done, with a
  split. Seven of the eleven are erosion of a substance carried as sediment
  (carbon, urea, ammonium, aluminum) and take `measured_ins=Sediment`. Four
  measure the sediment itself and take `measurement_ofs=Sediment` instead:
  Erosion rate, Hourly sinking rate, Sediment transport, and Sediment erosion.
  Hourly sinking rate takes `measured_ins=Water`, since the particles settle
  through the water column. Three Sediment variables keep `measured_ins=NA`
  because no material is the medium.
- ~~Unsaturated water flux should sit in Unsaturated zone.~~ Done.
- ~~The 17 Land surface variables reference Land surface 7 times.~~ Done, ten
  of the seventeen, up from six. Four of the seventeen gained it: Altitude of
  landscape, Altitude of grid cell, Measurement of altitude, and Measurement of
  slope, each with Altitude or Slope beside it in `measurement_ofs`. Three rows
  outside the seventeen gained it too, the `Measurement of slope` children
  Azimuth, Sine, and Cosine of slope. Land surface is now named by 14 rows in
  all. The seven of the seventeen left are roughness heights, the wind speed
  measurement height, and the two boundary layer terms; none of those six is
  about the land surface. Zero plane displacement height is the seventh. It is
  a height above the ground surface, but what it measures is canopy drag, so it
  takes `contexts=Canopy|Vegetation` instead.
- ~~Nothing references Vegetation except Fractional vegetation cover.~~ Done,
  fourteen rows. Zero plane displacement height takes
  `contexts=Canopy|Vegetation`. Every `Plant management variable` row that is
  about vegetation takes `contexts=Vegetation`: the eight planting and harvest
  date rows, the stand-replacing disturbance flag, the species death flag,
  Type of harvest, and Thinning of plant population. A date does not measure
  vegetation, so the column is `contexts` and not `measurement_ofs`;
  `Date of fire` sets the same precedent.

  Harvest (`BERVO:8000003`) is now named in one column only. The five harvest
  rows take it in `contexts`, and the two rows that already named it were moved
  there: Harvest efficiency had it in `measurement_ofs`, Harvest cutting height
  in `measured_ins`. Harvest is an event, not a material, so neither of those
  columns can hold it. Harvest efficiency was left with nothing in any relation
  column by that move, so it took what it actually measures: it is
  `FracBiomHarvsted`, the fraction of biomass harvested, and it now reads
  `attributes=Fraction`, `measurement_ofs=Biomass`, `contexts=Harvest`.

  **Plant or Vegetation.** Both are now in use in the `Plant management
  variable` block and the two concepts say which is which. Plant
  (`BERVO:8000021`) sits under Organism and is *"a multicellular organism that
  typically produces its own food through photosynthesis"*. Vegetation
  (`BERVO:8000716`) is *"plant cover of an area taken as a whole, without
  regard to the taxa that compose it"*. So a row about organisms or taxa takes
  Plant, as Number of plant species does, and a row about the stand on a piece
  of ground takes Vegetation, as the planting and harvest dates do. The later
  slices of #83 should follow that split rather than re-deriving it.

  One row in the block is left with no relation at all: Match plant functional
  type from different scenarios (`BERVO:0001059`). It was considered and left.
  It is scenario bookkeeping rather than a statement about vegetation, and its
  label and its definition do not agree with each other, which wants settling
  before anything is linked to it.

The heat kinds were the second slice of #83, the water potential terms the
third, field capacity and wilting point the fourth, the microbial guilds the
fifth, and chemical transformation the sixth. The remaining slices are the
`_pft` variables, time step, and population.

The chemical transformation slice put Chemical transformation in `attributes`
on 22 of the 24 rows whose label says "transformation", all of which had `NA`
there, and on the two iron adsorption rows below.
That is the column the other processes named as the quantity of a variable
already use: Fixation on 13 variables, Mineralization on 6, Erosion on 23.
(Counting every row gives 14, 7, and 24, because each of the three concept
rows names itself in its own `attributes`.) Each of
the 24 is the net rate of change of a pool by reaction, sorption,
precipitation, or dissolution, which is what the concept's definition says,
and the substance stays in `measurement_ofs`.

Total iron adsorption and Total iron hydroxide adsorption (`BERVO:0001730`,
`BERVO:0001731`) take it too, though their labels say adsorption. They are
`TRChem_Fe_sorbed_soil_vr` and `TRChem_FeO2H2_sorbed_soil_vr`, in the same
run as the ten adsorbed transformation rows, and the EcoSIM source treats them
as rates: they are set beside `TRChem_AlO2H2_sorbed_soil_vr`, which is declared
`[mol d-2 h-1]`, reset each hour with it, and the FeO2H2 one is subtracted
from the dissolved pool as the AlO2H2 one is. Their unit was `mol.m-2` and
their definitions spoke of a total amount; both now say a rate, in
`mol.h-1/{grid}` like their siblings.

The other two transformation rows, Microbial gases transformation and Total
microbial gases transformation (`BERVO:0000919`, `BERVO:0000920`), take Uptake
instead. Their labels follow EcoSIM's own comment on `trcs_RMicbUptake_vr`,
"microbial gases transformation", but the code fills it with net microbial
uptake of each gas (`RCO2NetUptkMicb`, `RCH4UptkAutor`, `RH2NetUptkMicb` in
MicBGCAPI.F90), and the transport code takes a positive value as a sink.
The labels may want to say uptake too; that is left to a change of its own.

The microbial guild slice named a guild in `measured_ins` on 115 rows, the
column where 102 rows already named Microbes, 90 of them variables. 66 still
do. Where a row named Microbes, the
guild replaced it (36 rows), since every guild sits beneath Microbes. Where a
row named another medium, such as Soil, the guild went beside it (37 rows), as
Soil|Microbes already did for heterotrophic respiration. The other 42 rows had
`NA`. The rows came from labels and definitions that name the guild or its
process: heterotrophic 32, autotrophic 20, nitrifiers 15 (the ammonia and
nitrite oxidation rows among them), denitrifiers 12, methanogens 9 (six of
them on the hydrogenotrophic and acetotrophic terms), diazotrophs 12 (the
nodule nitrogen fixers among them, since Diazotrophs covers symbionts),
fermenters 4, methanotrophs 5, fungi 3, aerobic heterotrophs 3 (EcoSIM's
"aerobic bacteria"), and mycorrhizal fungi 1, which takes
`Root|Mycorrhizal fungi` because it is an exchange between the two. 21 of the
115 are the `NitroPars.txt` oxidation rates, half-saturation constants, and
growth efficiencies, which name their guild in the label, or, on the carbon
dioxide and methane half-saturation constants, in the definition. The five
heterotrophic nitrate, nitrite and nitrous oxide uptake rows
(`BERVO:0001005`-`BERVO:0001009`) had Microbes alone, where their band and
non-band neighbours had Soil beside it; all ten now read
`Soil|Heterotrophic microbes`. The plant nitrogen fixation rows follow the same
rule, medium and guild together: Root nitrogen fixation, its vertical profile,
Total root nitrogen fixation, Total plant nitrogen fixation, and Nitrogen
fixation yield from carbon oxidation keep Root or Plant and take Diazotrophs
beside it, since the bacteria in the nodules do the fixing.

Left out on purpose: the plant autotrophic respiration rows, which are plant
metabolism and not autotrophic microbes; the Gibbs free energy yields of the
redox reactions, which are properties of the reactions; Surface litter organic matter in the autotrophic complex
(`BERVO:0001157`), whose definition is about photosynthetic organisms; and
Minimum ratio of branch or mycorrhizae to root (`BERVO:0000157`), whose label
names a branch and whose definition does not.

Heterotrophic respiration as methane (`BERVO:0000011`) names two guilds,
`Soil|Methanogens|Methanotrophs`. Its label says heterotrophic, but in EcoSIM
`ECO_HR_CH4_vr` is set from `RCH4UptkAutor` (RedistMod.F90), which
MicBGCFGMod.F90 computes as microbial methane production netted against
methanotroph oxidation: "complete net microbial CH4-C uptake; negative values
represent production". Neither guild sits under Heterotrophic microbes, and
the variable is not production alone. It is the one row counted under both guilds
above.

Naming an organism group in `measured_ins` follows the precedent the rows
already set, but the ontology is not uniform on it. Microbial cell density
and Colony-forming unit density (`BERVO:0001987`, `BERVO:0001990`) put
Microbes in `measurement_ofs` and point at `BERVO:involves_taxa`, an object
property with no template column. If that property gets a column, the guild
rows here and the rows still naming Microbes are the set to move.

The water potential slice put the terms in `attributes` rather than
`measurement_ofs`, because Water potential sits under Physical property and
that is overwhelmingly where the Physical property tree is used. Of its 45
descendants, 25 are referenced at all, and between them they account for 491
uses in `attributes` against 4 everywhere else: 117 rows for Concentration, 75
for Content, 53 for Diffusivity. Three descendants are the exceptions, and all
four stray uses are in `measurement_ofs`: pH (2 uses, and none in
`attributes`), Non-structural C3 content (1, likewise none), and Mass (1,
against 62). The heat kinds went in `measurement_ofs` because they sit under
Heat, which is a form of energy and not a property. The column follows the
concept's own parent.

Water potential had two components and the variables name four. Matric
potential (`BERVO:8000805`) and Gravitational potential (`BERVO:8000806`) were
added beside Turgor and Osmotic, which completes the classical decomposition.
Root total water potential says so itself: "the sum of osmotic, turgor, and
matric potentials".

Field capacity and Wilting point went in `contexts`, on twelve rows. That is
an exception to the rule above, and it follows an older one. Both are named
states of soil water, and a variable is measured *at* them: a water potential
at field capacity is a water potential. The rows that say "at standard ambient
temperature" and "dewpoint" already put the reference state in `contexts` and
the quantity in `attributes`, and Daily dewpoint temperature does so even
though the variable is the dewpoint itself. The water content rows follow
Dewpoint. So each term is named in one column only, as Harvest is.

Three field capacity rows carried `attributes=Capacity|Water potential`.
Capacity was standing in for field capacity, and a water potential is not a
capacity. Those three now carry `Water potential` alone.

The two automatic irrigation thresholds are fractions of the water held
between the two points, so they name both. Excess water (`BERVO:0001769`) was
left out. Its definition says "beyond field capacity" once, and its own
quantity is mobile water, not a state of the soil.

A sweep for concepts that a variable's label names but its own columns do not
reference filled 62 cells beside the earlier slices. The concepts were mostly added for the ODM2
alignment and the concept gap review, and few rows used them:

- `attributes`: Hydraulic conductivity on five rows. On the root water uptake
  one it replaced Uptake, which moved to `contexts`, since the label names
  the uptake the conductivity serves. Electrical conductivity on Measured
  electrical conductivity; Bulk density in place of Density on the three bulk
  density rows.
- `measurement_ofs`: Dissolved organic matter on seven rows, in place of the
  generic Organic matter on four of them; Dissolved organic carbon in place of
  Organic carbon on Dissolved organic carbon concentration, the same move one
  level down.
- `measured_ins`: Petiole on the two petiole growth parameters, and on Petiole
  length:mass during growth, which had it the wrong way round: Growth in
  `measured_ins` and Petiole in `measurement_ofs`. It now reads as its sibling
  Internode length:mass during growth does, `measured_ins=Petiole` and
  `contexts=Growth`, so Petiole sits in one column on all three rows.
- `qualifiers`: Cumulative on 14 of the 15 rows whose label begins
  "Cumulative", the 14 that accumulate over time, beside the Total or Net
  they had, and on Pft cumulative nodule infection and Pft cumulative
  phosphorus uptake, the two siblings of Pft cumulative nitrogen uptake, which
  already carried it; Gross on the three gross primary productivity and gross
  carbon dioxide fixation rows;
  Daily on seven, Yearly on the two mean annual rows, Current on three, Hourly
  on one, Gaseous on two, Aqueous on two; Total on the five "Total … solids"
  rows.

Left out: Cumulative depth to bottom of snowpack layer (`BERVO:0001570`), a
sum down through layers rather than over time. Gross alpha activity and Gross
beta activity (`BERVO:0002116`, `BERVO:0002117`), where gross means the
nuclides are not told apart, which is not what Gross means here. Soil
electrical conductivity (`BERVO:0000916`), whose unit `mol/{grid}` is not a
conductivity. Here the label is what is wrong: EcoSIM declares `UION_col` as
"total soil ion content, [mol d-2]", which agrees with the row's unit, its
`attributes=Content`, and its `measurement_ofs=Ion`. The fix is a relabel to
a soil ion content, with the conductivity label dropped, and that belongs to a
change of its own. The two thermal conductivity
rows (`BERVO:0001486`, `BERVO:0001487`), which are the numerator and the
denominator of a formula rather than conductivities. The two parameters to
calculate an hourly air temperature and vapor pressure from the daily value
(`BERVO:0001321`, `BERVO:0001327`), which keep Hourly alone: the daily value is
their input, and the quantity they set is hourly. The nine root primary
axes rows: Secondary axes is named in `contexts` on one row and in
`measurement_ofs` on another, so the column for Primary axes is not settled.

Behind this is an older backlog: 128 labels name Carbon and do not reference
it, 69 Water, 62 Irrigation, 45 Soil.

A sweep keyed on the EcoSIM name would reach rows the label sweeps cannot.
44 variables have `_CumYr` in their EcoSIM name, a total accumulated from the
start of the year. 34 of them lack Cumulative and none carries Yearly. Their
labels mostly say "Total" (24 of the 44), such as Total canopy ammonia flux
(`NH3Emis_CumYr_pft`), and the twelve fire emission rows (`*byFire_CumYr_*`)
carry no time qualifier at all.
