# Alignment with ODM2 variable name

The ODM2 **variable name** vocabulary (<http://vocabulary.odm2.org/variablename/>)
names the quantity an observation reports, such as `Canopy height`, `Albedo`, or
`Nitrogen, total`. It is the largest ODM2 vocabulary and the fourth step on
[issue #66](https://github.com/bioepic-data/bervo/issues/66), after the
[speciation](odm2-speciation.md), [medium](odm2-medium.md), and
[site type](odm2-sitetype.md) vocabularies.

It is too large for one change. This page records the triage of the whole
vocabulary and the slices it is being added in. The first slice, recorded
below, adds the concepts.

## Source

The CSV export at <http://vocabulary.odm2.org/api/v1/variablename/?format=csv>,
fetched on 2026-09-23. It holds 993 terms. Only 16 carry an ODM2 category, so the
triage below is BERVO's own.

Cross-references take the form `ODM2:variablename/<term>`, where `<term>` is the
ODM2 identifier, such as `pressureAbsolute`. Each emitted IRI redirects (301) to
the same path with a trailing slash, which returns the term page. The ODM2 name
and definition are quoted in the term's `Comment` as
`ODM2 variable name concept "<name>": <definition>`, with the Wikipedia citation
markers (`[1][2]`) that some definitions carry removed.

## Concept or variable

A name that is only a property, a thing, or a group of organisms becomes a
**concept**: `Albedo`, `Bulk density`, `Albite`, `Phytoplankton`, `E-coli`. In
ODM2 such a name means "the amount of this", and in BERVO that is what a
variable's `attributes` or `measurement_ofs` names.

A name that puts a property on a named thing becomes a **variable**:
`Canopy height`, `Soil respiration`, `Fish detections`, `Spartina alterniflora
coverage`.

Either way, the BERVO term carries the ODM2 cross-reference. That departs from
the habit of mapping concepts and not variables, because ODM2's variable names
are generic observables rather than model-specific composites.

Some names sit on the line. BERVO already has `Wind speed` and `Relative humidity`
as concepts and `Incoming shortwave radiation` as a variable, so the meteorology
and radiation slice settles those against that precedent rather than by this
rule alone.

ODM2 names are mapped by identifier, never by label, because some labels are
wrong. See "Points to note".

## Triage

| Bucket | Terms | Disposition |
| --- | --- | --- |
| Chemical species | 602 | Not now. Elements and their dissolved, total, and particulate forms, organic compounds, isotopes and isotope ratios, pigments, and distribution coefficients. |
| Instrument housekeeping | 41 | Not included. See below. |
| Ecotoxicology biomarkers | 12 | Not included. See below. |
| Quantities, placeholders, minerals, enzymes, organism groups | 90 | **Slice 1, this page.** |
| Meteorology, radiation, comfort indices | 45 | Slice 2, with the land-atmosphere fluxes |
| Land-atmosphere fluxes | 25 | Slice 2 |
| Vegetation | 32 | Slice 3, with ecology |
| Ecology | 8 left | Slice 3 |
| Hydrology and snow | 31 | Slice 4 |
| Soil and geology | 44 | Slice 5 |
| Water quality | 63 | Slice 6 |

The two excluded buckets:

- **Instrument housekeeping** (41): `agencyCode`, `batteryTemperature`,
  `batteryVoltage`, `carbonDioxideTransducerSignal`, `containerNumber`, `counter`,
  `courseOverGround`, `dataShuttleAttached`, `dataShuttleDetached`, `endOfFile`,
  `flashMemoryErrorCount`, `GNSSFixMode`, `horizontalDilutionOfPrecision`,
  `hostConnected`, `indicator`, `instrumentStatusCode`, `satellitesInView`,
  `loggerStopped`, `lowBatteryCount`, `orientation`,
  `oxygenDissolvedTransducerSignal`, `percentFullScale`,
  `positionDilutionOfPrecision`, `programSignature`,
  `receivedSignalStrenghtIndication`, `recorderCode`, `remark`, `speedOverGround`,
  `sequenceNumber`, `signalQuality`, `signalToNoiseRatio`,
  `tableOverrunErrorCount`, `TDRWaveformRelativeLength`, `temperatureDatalogger`,
  `temperatureSensor`, `temperatureTransducerSignal`, `timeStamp`,
  `verticalDilutionOfPrecision`, `watchdogErrorCount`,
  `waterColumnEquivalentHeightAbsolute`, `waterColumnEquivalentHeightBarometric`.
- **Ecotoxicology biomarkers** (12):
  `cytochromeP450Family1SubfamilyAPolypeptide1DeltaCycleThreshold`,
  `cytosolicProtein`, `DNADamageOliveDailMoment`, `DNADamagePercentTailDNA`,
  `DNADamageTailLength`, `ethoxyresorufin_O_DeethylaseActivity`,
  `glutathione_S_TransferaseActivity`,
  `glutathione_S_TransferaseDeltaCycleThreshold`, `liverMass`,
  `microsomalProtein`, `superoxideDismutaseActivity`,
  `superoxideDismutaseDeltaCycleThreshold`.

The later slices, by ODM2 identifier:

- **Meteorology** (21): `barometricPressure`, `cloudCover`, `frictionVelocity`,
  `hail`, `momentumFlux`, `precipitation`, `rainfallRate`, `relativeHumidity`,
  `sunshineDuration`, `temperatureDewPoint`, `vaporPressureDeficit`, `visibility`,
  `waterVaporConcentration`, `waterVaporDensity`, `windDirection`,
  `windGustDirection`, `windGustSpeed`, `windRun`, `windSpeed`, `windStress`, and
  `weatherConditions` from the placeholders.
- **Comfort indices** (6): `heatIndex`, `THSWIndex`, `THWIndex`,
  `ultravioletRadiationIndex`, `ultravioletRadiationDose`, `windChill`.
- **Radiation** (18): `globalRadiation`, `photosyntheticPhotonFluxDensity`, and
  the sixteen `radiation…` terms for incoming, outgoing, net, and total
  shortwave, longwave, PAR, and UV.
- **Land-atmosphere fluxes** (25): `ammoniumFlux`, `carbonDioxideFlux`,
  `carbonDioxideStorageFlux`, `effectiveEnergyAndMassTransfer`, `evaporation`,
  `evapotranspiration` (twice), `evapotranspirationPotential`, `groundHeatFlux`,
  `latentHeatFlux`, `netHeatFlux`, `oxygenFlux`, `oxygenUptake`,
  `hosphorusPhosphateFlux`, `primaryProductivity`, `primaryProductivityGross`,
  `respirationEcosystem`, `respirationNet`, `sapFlow`, `sensibleHeatFlux`,
  `silicicAcidFlux`, `soilRespiration`, `transpiration`, `ureaFlux`, `waterFlux`.
- **Vegetation** (32): `areaBasal`, `biomassAboveGround`, `biomassPhytoplankton`,
  `biomassTotal`, `biomassVegetation`, `canopyClosure`, `canopyHeight`,
  `diameterAtBreastHeight`, `leafAreaIndex`, `leafWetness`, `litterPlant`, `NDVI`,
  `throughfall`, `vegetationType`, and 18 coverage terms: 15 for salt marsh
  taxa, such as `spartinaAlternifloraCoverage`, plus `noVegetationCoverage`,
  `transientSpeciesCoverage`, and `wrackCoverage`.
- **Ecology** (8): `bodyLength`, `chlorophyllFluorescence`, `countAreal`,
  `e_coli`, `fishDetections`, `shannonDiversityIndex`, `shannonEvennessIndex`,
  `taxaCount`. The other ten ecology names are organism groups and are in
  slice 1.
- **Hydrology** (27): `alluviumDepth`, `baseflow`, `depthUnsaturatedZone`,
  `discharge`, `gageHeight`, `groundwaterDepth`, `heightAboveSeaFloor`,
  `lightAttenuationCoefficient`, `rechargeGroundwater`, `reservoirStorage`,
  `secchiDepth`, `sigma_t`, `streamflow`, `tideStage`, `volumetricWaterContent`,
  `waterDepth`, `waterDepthAveraged`, `waterLevel`, five `waterUse…` terms,
  `waveHeight`, `wellFlowRate`, `wellheadPressure`, and `position` (the
  position of a gate) from the placeholders.
- **Snow** (4): `depthSnow`, `snowDepth`, `snowLayerHardness`,
  `snowWaterEquivalent`.
- **Soil** (29): `acidityExchange`, `activityAcidPhosphatase`,
  `activityBetaGlucosidase`, `activityBetaNAcetylGlucosaminidase`,
  `activityPhenolOxidase`, `baseSaturation`, `biomassMicrobial`,
  `biomassSoilBacterialDeoxyribonucleicAcid`, `bulkElectricalConductivity`,
  `carbonToNitrogenMassRatio`, `carbonToNitrogenMolarRatio`,
  `cationExchangeCapacity`, `Clay`, `soilDepth`, `extracellularEnzymeActivity`,
  `grainSize`, `lossOnIgnition`, `Sand`, `sedimentPassingSieve`,
  `sedimentRetainedOnSieve`, `Silt`, `sodiumAdsorptionRatio`,
  `soilAggregateStability`, `soilClassification`, `soilCoarseFraction`,
  `soilHorizon`, `soilOrganicMatter`, `soilOrganicMatterDensityFractionation`,
  `soilTexture`.
- **Geology and terrain** (15): `aspect`, `bedrockType`,
  `boreholeLogMaterialClassification`, `curvature`, `diffractionXRay`,
  `erosionRate`, `fluorescenceXRay`, `gammaCounts`, `geologicUnit`,
  `landClassification`, `neutronCount`, `scatterAntiStokes`, `scatterStokes`,
  `seismicRefraction`, `topographicWetnessIndex`.
- **Water quality** (63): alkalinity (6), acidity (4) and acid neutralizing
  capacity, BOD (15) and COD, hardness (5), solids (9), `specificConductance`,
  `color`, `odor`, `oilAndGrease`, `SUVA254`, `SUVA280`, the three DOM and DOC
  fluorescence terms, `humificationIndex`, `coloredDissolvedOrganicMatter`,
  `absorbanceUltraviolet`, `oxygenDissolvedPercentOfSaturation`, `LSI`, `TSI`,
  `omegaAragonite`, `reductionPotential`, `particleCounts`,
  `grossAlphaRadionuclides`, `grossBetaRadionuclides`, `sedimentSuspended`,
  `loadSuspended`.

## Slice 1: ODM2 terms mapped to existing BERVO concepts

| ODM2 term | BERVO term | Note |
| --- | --- | --- |
| `absorbance` | Absorbance (`BERVO:8000236`) | |
| `albedo` | Albedo (`BERVO:8000263`) | |
| `altitude` | Altitude (`BERVO:8000099`) | |
| `area` | Area (`BERVO:8000079`) | |
| `biomass` | Biomass (`BERVO:8000296`) | |
| `density` | Density (`BERVO:8000233`) | |
| `depth` | Depth (`BERVO:8000069`) | |
| `diameter` | Diameter (`BERVO:8000444`) | |
| `distance` | Distance (`BERVO:8000520`) | |
| `height` | Height (`BERVO:8000076`) | |
| `latitude` | Latitude (`BERVO:8000395`) | |
| `length` | Length (`BERVO:8000260`) | |
| `longitude` | Longitude (`BERVO:8000396`) | |
| `mass` | Mass (`BERVO:8000137`) | |
| `michaelisConstant` | Michaelis constant (`BERVO:8000268`) | |
| `organicMatter` | Organic matter (`BERVO:8000286`) | |
| `pH` | pH (`BERVO:8000261`) | already mapped to `ODM2:speciation/pH` |
| `porosity` | Porosity (`BERVO:8000500`) | |
| `salinity` | Salinity (`BERVO:8000427`) | |
| `temperature` | Temperature (`BERVO:8000133`) | |
| `turbidity` | Turbidity (`BERVO:8000294`) | |
| `vaporPressure` | Vapor pressure (`BERVO:8000507`) | |
| `velocity` | Velocity (`BERVO:8000101`) | |
| `volume` | Volume (`BERVO:8000190`) | |
| `waterContent` | Water content (`BERVO:8000202`) | |
| `waterPotential` | Water potential (`BERVO:8000789`) | |
| `electricalConductivity` | Conductivity (`BERVO:8000348`) | gains `electrical conductivity` as an exact synonym; already mapped to `ODM2:speciation/EC` |
| `resistivityElectrical` | Resistivity (`BERVO:8000428`) | gains `electrical resistivity` as an exact synonym |
| `abundance` | Relative abundance (`BERVO:8000516`) | gains `abundance` as a related synonym; ODM2 defines it as the relative representation of a species |

## Slice 1: new terms

`BERVO:8000807` to `BERVO:8000870` except `BERVO:8000867`, 63 terms. All are
concepts.

| BERVO term | Parent | ODM2 term | Other cross-reference |
| --- | --- | --- | --- |
| Absolute pressure | Pressure | `pressureAbsolute` | |
| Gauge pressure | Pressure | `pressureGauge` | |
| Osmotic pressure | Pressure | `osmoticPressure` | |
| Bulk density | Density | `bulkDensity` | |
| Circumference | Physical property | `circumference` | `PATO:0001648` |
| Roundness | Physical property | `roundness` | |
| Hydraulic conductivity | Physical property | `hydraulicConductivity` | |
| Speed of sound | Physical property | `speedOfSound` | |
| Luminous flux | Physical property | `luminousFlux` | `PATO:0001296` |
| Radar reflectivity | Physical property | `reflectivity` | |
| Permittivity | Physical property | `permittivity`, `permittivityElectrical` | |
| Relative permittivity | Permittivity | `dielectricConstant` | |
| Real dielectric constant | Relative permittivity | `realDielectricConstant` | |
| Imaginary dielectric constant | Relative permittivity | `imaginaryDielectricConstant` | |
| Electric current | Physical property | `electricCurrent` | |
| Voltage | Physical property | `voltage` | |
| Electric power | Physical property | `electricPower` | |
| Electric energy | Energy | `electricEnergy` | |
| Temperature change | Temperature | `temperatureChange` | |
| Initial temperature | Temperature | `temperatureInitial` | |
| Elapsed time | Duration | `timeElapsed` | |
| Rotation frequency | Frequency | `frequencyOfRotation` | |
| Parameter | Concept | `parameter` | |
| Intercept | Coefficient | `intercept` | |
| Regression slope | Coefficient | `slope` | |
| Offset | Concept | `offset` | |
| Threshold | Concept | `threshold` | |
| Feldspar | Mineral | | `CHEBI:48733` |
| Alkali feldspar | Feldspar | `alkaliFeldspar` | |
| Plagioclase | Feldspar | `plagioclase` | |
| Albite | Plagioclase | `albite` | |
| Orthoclase | Alkali feldspar | `orthoclase` | |
| Amphibole | Mineral | `amphibole` | |
| Apophyllite | Mineral | `apophyllite` | |
| Augelite | Mineral | `augelite` | |
| Clinoptilolite | Mineral | `clinoptilolite` | |
| Cristobalite | Mineral, Silicon dioxide | `cristobalite` | |
| Gibbsite | Mineral | `gibbsite` | `CHEBI:30194` |
| Goethite | Mineral | `goethite` | |
| Halloysite | Mineral | `halloysite` | |
| Melanovanadite | Mineral | `melanovanadite` | |
| Mica | Mineral | `mica` | |
| Nacrite | Mineral | `nacrite` | |
| Quartz | Mineral, Silicon dioxide | `quartz` | `CHEBI:46727` |
| Vermiculite | Mineral | `vermiculite` | |
| Enzyme | Protein | | |
| Acid phosphatase | Enzyme | `acidPhosphatase` | |
| Glucosidase | Enzyme | `glucosidase` | |
| Beta-glucosidase | Glucosidase | `betaGlucosidase` | |
| Alpha-N-acetylglucosaminidase | Enzyme | `alphaNAcetylglucosaminidase` | |
| Cellobiohydrolase | Enzyme | `cellobiohydrolase` | |
| Xylosidase | Enzyme | `xylosidase` | |
| Phytoplankton | Organism | `phytoplankton` | |
| Zooplankton | Organism | `zooplankton` | |
| Benthos | Organism | `benthos` | |
| Cryptophytes | Microbes | `cryptophytes` | `NCBITaxon:3027` |
| Dinoflagellates | Microbes | `dinoflagellates` | `NCBITaxon:2864` |
| Cyanobacteria | Bacteria | `blue_GreenAlgae_Cyanobacteria_Phycocyanin` | `NCBITaxon:1117` |
| Coliform bacteria | Bacteria | `coliformTotal` | |
| Fecal coliform bacteria | Coliform bacteria | `coliformFecal` | |
| Enterococcus | Bacteria | `enterococci` | `NCBITaxon:1350` |
| Fecal streptococci | Bacteria | `streptococciFecal` | |
| Asterids | Plant | | `NCBITaxon:71274` |

Phosphoenolpyruvate carboxylase (`BERVO:8000061`) moves under the new Enzyme
from Concept.
Coefficient (`BERVO:8000227`) moves under the new Parameter from Concept, so
Intercept and Regression slope sit under Parameter through it. Coefficient's own
definition calls coefficients parameters.

Every NCBITaxon, CHEBI, and PATO identifier above was fetched from OLS and its
label or synonyms checked against the term.

## Points to note

- **ODM2 labels that are wrong.** `satellitesInView` is labelled "Location", and
  `speedOverGround` is labelled with a person's name. Both are instrument terms
  and are excluded. `slope` is defined as the slope of a linear relationship, so
  it maps to the new Regression slope, not to the land gradient Slope
  (`BERVO:8000031`). `position` is the position of a gate or other water-control
  element, not a spatial position, so it is not mapped to Position
  (`BERVO:8000443`); it goes to the hydrology slice as a variable.
- **ODM2 names that appear twice.** `evapotranspiration`, `pheophytin`,
  `cadmiumDissolved`, `calciumDissolved`, and `thorium` each appear twice in the
  export, and `snowDepth` and `depthSnow` are the same quantity. `Molbydenum,
  dissolved` is a misspelling that sits beside `Molybdenum, dissolved`.
  `hosphorusPhosphateFlux` is missing its first letter in the identifier; the
  cross-reference uses the identifier as ODM2 spells it.
- **No concepts for single species.** BERVO keeps terms for higher taxonomic
  groups where the variables need them, such as Asterids, Cryptophytes, and
  Enterococcus, and not for individual species. A variable
  that concerns one species is expected to carry that species as an NCBITaxon
  identifier in the data, not as a BERVO concept. A first draft of this slice
  added 14 salt marsh plants (13 species and the genus *Cuscuta*) as
  `BERVO:8000871` to `BERVO:8000884`. They were removed before merge, were
  never released, and `just next-id` may allocate those identifiers again.
  *Escherichia coli* (`BERVO:8000867`) was removed the same way. Fecal coliform
  bacteria stays, because that is the group water quality assays report.
  ODM2's `e_coli` goes to the ecology slice as a variable.
- **Labels of taxon groups.** A group takes the name its measurements use as
  the label, and NCBI's scientific name as an exact synonym: Cryptophytes
  (Cryptophyceae), Dinoflagellates (Dinophyceae), Cyanobacteria
  (Cyanobacteriota), Asterids (Asteridae). A genus kept as a group, such as
  Enterococcus, takes the genus name, with the plural in common use
  (`enterococci`) as a related synonym. Fungi (`BERVO:8000783`) already
  followed this.
- **Asterids has no subclasses.** It is the group ODM2's `asteridaeCoverage`
  names, and it is kept as a group, not as the root of a plant taxonomy. NCBI
  labels `NCBITaxon:71274` "asterids" with Asteridae as a synonym, and BERVO
  follows.
- **Salt marsh taxa for slice 3.** The coverage terms name taxa that NCBI
  Taxonomy has renamed since: *Spartina alterniflora* is now *Sporobolus
  alterniflorus* (`NCBITaxon:29706`), *Spartina spartinae* (which ODM2 spells
  "Spartina spartinea") is *Sporobolus spartinus* (`NCBITaxon:180094`), and
  *Monanthochloe littoralis* is *Distichlis littoralis* (`NCBITaxon:160556`).
  *Limonium nashii* is not in NCBI Taxonomy.
- **Organism groups that ODM2 measures as quantities.** ODM2 defines
  `cryptophytes` and `dinoflagellates` as the chlorophyll a contributed by each
  group, and `blue_GreenAlgae_Cyanobacteria_Phycocyanin` as cyanobacteria with
  phycocyanin. Under the rule above each is the organism group, and a variable
  that measures it names it.
- **No second parent of Phytoplankton.** Cryptophytes, Dinoflagellates, and
  Cyanobacteria are not given Phytoplankton as a second parent. Not every
  member of those groups is planktonic, and the subclass axiom would claim it.
- **Enzymes sit under Protein.** Protein (`BERVO:8000333`) sits under Concept,
  not under Chemical, so nothing enters the subtree `involves_chemicals` reasons
  over. Whether proteins belong under Chemical is a separate question. Enzyme
  Commission numbers are given in the definitions; `EC` is not a declared
  prefix.
- **Minerals.** Quartz and Cristobalite take Silicon dioxide as a second parent,
  as polymorphs of silica. Feldspar is added as a grouping term, not from ODM2,
  so that alkali feldspar and plagioclase have the parent they share. The other
  minerals sit flat under Mineral. `CHEBI:30194` is labelled
  "gamma-aluminium hydroxide" and carries gibbsite as a synonym.
- **Temperature change sits under Temperature for now.** A difference of two
  temperatures is not a temperature, so the subclass axiom overclaims. It is
  left in place and tracked as
  [issue #102](https://github.com/bioepic-data/bervo/issues/102).
- **Threshold and Critical.** Critical (`BERVO:8000005`) carried `threshold` as an
  exact synonym, so two terms answered to the word. Critical is a state near a
  tipping point, and the new Threshold is the operational level at which an
  action is taken. `threshold` is now a related synonym of Critical.
- **The ODM2 identifier is not kept as a synonym.** The speciation alignment
  kept ODM2's formulas, which people write. These identifiers are camelCase
  database keys that nobody writes.
