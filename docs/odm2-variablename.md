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
**concept**: `Albedo`, `Bulk density`, `Albite`, `Phytoplankton`. In
ODM2 such a name means "the amount of this", and in BERVO that is what a
variable's `attributes` or `measurement_ofs` names.

A name that puts a property on a named thing becomes a **variable**:
`Canopy height`, `Soil respiration`, `Fish detections`, `Spartina alterniflora
coverage`.

Either way, the BERVO term carries the ODM2 cross-reference. BERVO maps
variables as well as concepts wherever a true equivalent exists; earlier
alignments landed mostly on concepts only because their vocabularies named
things and properties.

Some names sit on the line. BERVO already has `Wind speed` and `Relative humidity`
as concepts and `Incoming shortwave radiation` as a variable. Slice 2 settled it:
an observable with a unit is a variable, and the property it measures is a
concept. See "Slice 2".

ODM2 names are mapped by identifier, never by label, because some labels are
wrong. See "Points to note".

## Triage

| Bucket | Terms | Disposition |
| --- | --- | --- |
| Chemical species | 602 | Not now. Elements and their dissolved, total, and particulate forms, organic compounds, isotopes and isotope ratios, pigments, and distribution coefficients. |
| Instrument housekeeping | 41 | Not included. See below. |
| Ecotoxicology biomarkers | 12 | Not included. See below. |
| Quantities, placeholders, minerals, enzymes, organism groups | 90 | **Slice 1, this page.** |
| Meteorology, radiation, comfort indices | 45 | **Slice 2**, with the land-atmosphere fluxes |
| Land-atmosphere fluxes | 25 | **Slice 2** |
| Vegetation | 32 | **Slice 3**, with ecology |
| Ecology | 8 left | **Slice 3** |
| Hydrology and snow | 31 | **Slice 4** |
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
| `resistivityElectrical` | Resistivity (`BERVO:8000428`) | gains `electrical resistivity` as an exact synonym |
| `abundance` | Relative abundance (`BERVO:8000516`) | gains `abundance` as a related synonym, which Concentration (`BERVO:8000023`) gives up; ODM2 defines it as the relative representation of a species |

## Slice 1: new terms

`BERVO:8000807` to `BERVO:8000869` except `BERVO:8000867`, and `BERVO:8000885`
and `BERVO:8000886`, 64 terms. All are
concepts.

| BERVO term | Parent | ODM2 term | Other cross-reference |
| --- | --- | --- | --- |
| Absolute pressure | Pressure | `pressureAbsolute` | |
| Gauge pressure | Pressure | `pressureGauge` | |
| Osmotic pressure | Pressure | `osmoticPressure` | |
| Bulk density | Density | `bulkDensity` | |
| Circumference | Length | `circumference` | `PATO:0001648` |
| Roundness | Physical property | `roundness` | |
| Hydraulic conductivity | Conductivity | `hydraulicConductivity` | |
| Electrical conductivity | Conductivity | `electricalConductivity` | |
| Power | Physical property | | `PATO:0001024` |
| Speed of sound | Physical property | `speedOfSound` | |
| Luminous flux | Physical property | `luminousFlux` | `PATO:0001296` |
| Radar reflectivity | Physical property | `reflectivity` | |
| Permittivity | Physical property | `permittivity`, `permittivityElectrical` | |
| Relative permittivity | Permittivity | `dielectricConstant` | |
| Real dielectric constant | Relative permittivity | `realDielectricConstant` | |
| Imaginary dielectric constant | Relative permittivity | `imaginaryDielectricConstant` | |
| Electric current | Physical property | `electricCurrent` | |
| Voltage | Physical property | `voltage` | |
| Electric power | Power | `electricPower` | |
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
| Albite | Plagioclase, Alkali feldspar | `albite` | |
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
| Phytoplankton | Microbes | `phytoplankton` | |
| Zooplankton | Organism | `zooplankton` | |
| Benthos | Organism | `benthos` | |
| Cryptophytes | Microbes | `cryptophytes` | `NCBITaxon:3027` |
| Dinoflagellates | Microbes | `dinoflagellates` | `NCBITaxon:2864` |
| Cyanobacteria | Bacteria | `blue_GreenAlgae_Cyanobacteria_Phycocyanin` | `NCBITaxon:1117` |
| Coliform bacteria | Bacteria | `coliformTotal` | |
| Fecal coliform bacteria | Coliform bacteria | `coliformFecal` | |
| Enterococcus | Bacteria | `enterococci` | `NCBITaxon:1350` |
| Fecal streptococci | Bacteria | `streptococciFecal` | |

Phosphoenolpyruvate carboxylase (`BERVO:8000061`) moves under the new Enzyme
from Concept.
Coefficient (`BERVO:8000227`) moves under the new Parameter from Concept, so
Intercept and Regression slope sit under Parameter through it. Coefficient's own
definition calls coefficients parameters.

Every NCBITaxon, CHEBI, and PATO identifier above was fetched from OLS and its
label or synonyms checked against the term.

## Slice 2: meteorology, radiation, comfort indices, and fluxes

The 70 names of slice 2 (69 identifiers, since `evapotranspiration` appears twice)
are observables: quantities a weather station, radiometer, or flux tower reports,
each with a unit. They enter BERVO as **variables**, whose `attributes`,
`measured_ins`, `measurement_ofs`, and `contexts` name the concepts that describe
them, such as Wind speed, Latent heat, or Carbon dioxide. This settles the question
the "Concept or variable" section left open: a concept is the property, and the
ODM2 observable is a variable that measures it.

Two decisions follow from that.

- **A variable whose natural label is an existing concept's label names its
  medium or its form.** Wind direction, Relative humidity, Precipitation,
  Evaporation, Water flux, and Primary productivity are concepts, so the variables
  are Near-surface wind direction, Air relative humidity, Precipitation amount,
  Evaporation flux, Water flux across a surface, and Primary production rate.
  Evapotranspiration and Transpiration follow Evaporation and become fluxes too,
  since BERVO's Evapotranspiration is an EcoSIM variable.
- **Two grouping classes hold the new variables**, apart from EcoSIM's model
  forcing and outputs: Meteorological variable (`BERVO:9000038`) for weather,
  radiation, and the comfort indices, and Surface flux variable (`BERVO:9000039`)
  for the fluxes of energy, water, carbon, momentum, and solutes.

### ODM2 names mapped to existing variables

Where BERVO already had the same quantity, the ODM2 name maps to it. Each keeps
Climate force variable as its `Category` and takes a second parent: Incoming
radiation for the two radiation variables, and Meteorological variable for the
other three.

| ODM2 term | BERVO variable | Unit |
| --- | --- | --- |
| `windSpeed` | Measured wind speed (`BERVO:0001372`) | `m.h-1\|m.s-1` |
| `waterVaporConcentration` | Atmospheric vapor concentration (`BERVO:0001373`) | `m3.m-3` |
| `barometricPressure` | Atmospheric pressure (`BERVO:0001375`) | `kPa` |
| `radiationIncomingLongwave` | Sky longwave radiation (`BERVO:0001380`) | `MJ.h-1\|MJ.m-2.h-1\|W.m-2` |
| `radiationIncomingShortwave`, `globalRadiation`, `radiationTotalShortwave` | Incoming shortwave radiation (`BERVO:0001867`) | `W.m-2` |

The EcoSIM variables that share a name with an ODM2 observable, such as
Evapotranspiration (`BERVO:0001809`), Ecosystem respiration (`BERVO:0000018`),
and Ecosystem latent heat flux (`BERVO:0000002`), are not mapped. Each is a total
for an EcoSIM grid cell (`…/{grid}`), not a flux per unit area, so it is not the
same quantity.

### New grouping classes and concepts

| BERVO term | Parent | Cross-reference |
| --- | --- | --- |
| Meteorological variable (`BERVO:9000038`) | Variable | |
| Surface flux variable (`BERVO:9000039`) | Variable | |
| Gross (`BERVO:8000887`) | Quantitative value |  |
| Potential (`BERVO:8000888`) | Quantitative value |  |
| Cloud (`BERVO:8000889`) | Environmental feature | `ENVO:01000760` |
| Hail (`BERVO:8000890`) | Precipitation | `ENVO:03400011`, and ODM2 `hail` |
| Momentum (`BERVO:8000891`) | Physical property | `PATO:0001023` |
| Ultraviolet radiation (`BERVO:8000892`) | Radiation | `ENVO:21001216` |
| Ultraviolet A radiation (`BERVO:8000893`) | Ultraviolet radiation |  |
| Ultraviolet B radiation (`BERVO:8000894`) | Ultraviolet radiation |  |
| Transpiration (`BERVO:8000895`) | Biological process | `GO:0010148` |
| Silicic acid (`BERVO:8000896`) | Chemical | `CHEBI:26675` |

Gross and Potential join Net and Total as qualifiers. The others are what the
new variables measure. The concepts' cross-references were each fetched from OLS
and checked.

### New variables

`BERVO:0001905` to `BERVO:0001966` except `BERVO:0001941`, 61 variables. The units are the conventional SI
ones for each observable; ODM2 records units separately from variable names, so
a dataset may report another.

| BERVO variable | Parent | ODM2 term | Unit |
| --- | --- | --- | --- |
| Cloud cover (`BERVO:0001905`) | Meteorological | `cloudCover` | `1` |
| Friction velocity (`BERVO:0001906`) | Meteorological | `frictionVelocity` | `m.s-1` |
| Hail depth (`BERVO:0001907`) | Meteorological | none | `mm` |
| Precipitation amount (`BERVO:0001908`) | Meteorological | `precipitation` | `mm` |
| Rainfall rate (`BERVO:0001909`) | Meteorological | `rainfallRate` | `mm.h-1` |
| Air relative humidity (`BERVO:0001910`) | Meteorological | `relativeHumidity` | `1` |
| Sunshine duration (`BERVO:0001911`) | Meteorological | `sunshineDuration` | `h` |
| Dewpoint temperature (`BERVO:0001912`) | Meteorological | `temperatureDewPoint` | `Cel` |
| Vapor pressure deficit (`BERVO:0001913`) | Meteorological | `vaporPressureDeficit` | `kPa` |
| Visibility (`BERVO:0001914`) | Meteorological | `visibility` | `m` |
| Water vapor density (`BERVO:0001915`) | Meteorological | `waterVaporDensity` | `g.m-3` |
| Near-surface wind direction (`BERVO:0001916`) | Meteorological | `windDirection` | `deg` |
| Wind gust direction (`BERVO:0001917`) | Meteorological | `windGustDirection` | `deg` |
| Wind gust speed (`BERVO:0001918`) | Meteorological | `windGustSpeed` | `m.s-1` |
| Wind run (`BERVO:0001919`) | Meteorological | `windRun` | `m` |
| Weather conditions (`BERVO:0001920`) | Meteorological | `weatherConditions` | `NA` |
| Heat index (`BERVO:0001921`) | Meteorological | `heatIndex` | `Cel` |
| Temperature-humidity-sun-wind index (`BERVO:0001922`) | Meteorological | `THSWIndex` | `Cel` |
| Temperature-humidity-wind index (`BERVO:0001923`) | Meteorological | `THWIndex` | `Cel` |
| UV index (`BERVO:0001924`) | Meteorological | `ultravioletRadiationIndex` | `1` |
| Ultraviolet radiation dose (`BERVO:0001925`) | Meteorological | `ultravioletRadiationDose` | `J.m-2` |
| Wind chill (`BERVO:0001926`) | Meteorological | `windChill` | `Cel` |
| Photosynthetic photon flux density (`BERVO:0001927`) | Meteorological | `photosyntheticPhotonFluxDensity` | `umol.m-2.s-1` |
| Incoming radiation (`BERVO:0001928`) | Meteorological | `radiationIncoming`, `radiationTotalIncoming` | `W.m-2` |
| Incoming photosynthetically active radiation (`BERVO:0001929`) | Incoming radiation | `radiationIncomingPAR` | `umol.m-2.s-1\|W.m-2` |
| Incoming ultraviolet A radiation (`BERVO:0001930`) | Incoming radiation | `radiationIncomingUV_A` | `W.m-2` |
| Incoming ultraviolet B radiation (`BERVO:0001931`) | Incoming radiation | `radiationIncomingUV_B` | `W.m-2` |
| Net radiation (`BERVO:0001932`) | Meteorological | `radiationNet` | `W.m-2` |
| Net longwave radiation (`BERVO:0001933`) | Net radiation | `radiationNetLongwave` | `W.m-2` |
| Net photosynthetically active radiation (`BERVO:0001934`) | Net radiation | `radiationNetPAR` | `umol.m-2.s-1\|W.m-2` |
| Net shortwave radiation (`BERVO:0001935`) | Net radiation | `radiationNetShortwave` | `W.m-2` |
| Outgoing longwave radiation (`BERVO:0001936`) | Outgoing radiation | `radiationOutgoingLongwave` | `W.m-2` |
| Outgoing photosynthetically active radiation (`BERVO:0001937`) | Outgoing radiation | `radiationOutgoingPAR` | `umol.m-2.s-1\|W.m-2` |
| Outgoing shortwave radiation (`BERVO:0001938`) | Outgoing radiation | `radiationOutgoingShortwave` | `W.m-2` |
| Outgoing radiation (`BERVO:0001939`) | Meteorological | `radiationTotalOutgoing` | `W.m-2` |
| Momentum flux (`BERVO:0001940`) | Surface flux | `momentumFlux`, `windStress` | `N.m-2` |
| Ammonium flux (`BERVO:0001942`) | Surface flux | `ammoniumFlux` | `mmol.m-2.d-1` |
| Carbon dioxide flux (`BERVO:0001943`) | Surface flux | `carbonDioxideFlux` | `umol.m-2.s-1` |
| Carbon dioxide storage flux (`BERVO:0001944`) | Surface flux | `carbonDioxideStorageFlux` | `umol.m-2.s-1` |
| Effective energy and mass transfer (`BERVO:0001945`) | Surface flux | `effectiveEnergyAndMassTransfer` | `MJ.m-2.a-1` |
| Evaporation flux (`BERVO:0001946`) | Surface flux | `evaporation` | `mm.h-1` |
| Evapotranspiration flux (`BERVO:0001947`) | Surface flux | `evapotranspiration` | `mm.h-1` |
| Potential evapotranspiration (`BERVO:0001948`) | Evapotranspiration flux | `evapotranspirationPotential` | `mm.d-1` |
| Transpiration flux (`BERVO:0001949`) | Surface flux | `transpiration` | `mm.h-1` |
| Water flux across a surface (`BERVO:0001950`) | Surface flux | `waterFlux` | `mm.h-1` |
| Sap flow (`BERVO:0001951`) | Plant rate | `sapFlow` | `kg.h-1/{plant}` |
| Ground heat flux (`BERVO:0001952`) | Surface flux | `groundHeatFlux` | `W.m-2` |
| Latent heat flux (`BERVO:0001953`) | Surface flux | `latentHeatFlux` | `W.m-2` |
| Sensible heat flux (`BERVO:0001954`) | Surface flux | `sensibleHeatFlux` | `W.m-2` |
| Net heat flux (`BERVO:0001955`) | Surface flux | `netHeatFlux` | `W.m-2` |
| Oxygen flux (`BERVO:0001956`) | Surface flux | `oxygenFlux` | `mmol.m-2.d-1` |
| Oxygen uptake (`BERVO:0001957`) | Surface flux | `oxygenUptake` | `mmol.m-2.d-1` |
| Phosphate flux (`BERVO:0001958`) | Surface flux | `hosphorusPhosphateFlux` | `mmol.m-2.d-1` |
| Silicic acid flux (`BERVO:0001959`) | Surface flux | `silicicAcidFlux` | `mmol.m-2.d-1` |
| Urea flux (`BERVO:0001960`) | Surface flux | `ureaFlux` | `mmol.m-2.d-1` |
| Primary production rate (`BERVO:0001961`) | Surface flux | `primaryProductivity` | `g{C}.m-2.d-1` |
| Gross primary production rate (`BERVO:0001962`) | Primary production rate | `primaryProductivityGross` | `g{C}.m-2.d-1` |
| Ecosystem respiration flux (`BERVO:0001963`) | Surface flux | `respirationEcosystem` | `umol.m-2.s-1` |
| Net respiration (`BERVO:0001964`) | Surface flux | `respirationNet` | `umol.m-2.s-1` |
| Soil respiration (`BERVO:0001965`) | Surface flux | `soilRespiration` | `umol.m-2.s-1` |
| Hailstone size (`BERVO:0001966`) | Meteorological | none | `mm` |

### Points to note for slice 2

- **Three ODM2 names map to Incoming shortwave radiation.** `globalRadiation` is
  defined as direct and diffuse solar radiation on a horizontal surface, which is
  incoming shortwave radiation. `radiationTotalShortwave`, "Total Shortwave
  Radiation", is read the same way, as the total of direct and diffuse incoming
  shortwave. If it was meant as incoming plus reflected, it needs its own term.
- **Two ODM2 names map to Incoming radiation.** `radiationIncoming` and
  `radiationTotalIncoming` differ only in that the second says "from all
  frequencies", which is what incoming radiation means.
- **`hail` maps to the Hail concept.** ODM2 defines hail only as a form of
  precipitation, so its cross-reference sits on Hail, not on a variable. Hail
  depth and Hailstone size (`BERVO:0001966`) are the variables that measure it;
  neither carries an ODM2 name.
- **No Evapotranspiration concept.** The label is taken by an EcoSIM variable, so
  the evapotranspiration rows name both processes in `contexts`: Evaporation and
  Transpiration.
- **No Incoming or Outgoing qualifier.** BERVO has no class for direction, and the
  labels carry it.
- **Weather conditions is categorical**, with `has_units=NA` and
  `value_types=Category`. What its categories are is the question of
  [issue #108](https://github.com/bioepic-data/bervo/issues/108).
- **Wind stress is Momentum flux.** The surface momentum flux is the shear stress
  the wind exerts on the surface, so ODM2's `windStress` is a second
  cross-reference on Momentum flux, with `wind stress` as a related synonym.
  Momentum flux sits with the fluxes, although the triage listed it under
  meteorology. `BERVO:0001941`, which held Wind stress in a first draft, was
  removed before merge.
- **Variables nest where one is a kind of another.** Incoming, Outgoing, and Net
  radiation hold their waveband variables; Incoming shortwave radiation and Sky
  longwave radiation take Incoming radiation as a second parent; Total net
  radiation at ground surface (`BERVO:0001443`) takes Net radiation as a second
  parent; Gross primary production rate sits under Primary production rate; and
  Potential evapotranspiration under Evapotranspiration flux.
- **Incoming and Outgoing radiation carry no Total qualifier**, although each also
  holds a `radiationTotal…` ODM2 name. They are the plain incoming and outgoing
  quantities over all wavelengths, and "total" in those ODM2 names adds nothing.
- **Dewpoint temperature** (spelled as the live Dewpoint concept is) takes
  `attributes=Dewpoint`, and is the parent of Daily and Hourly dewpoint
  temperature (`BERVO:0001344`, `BERVO:0001349`), which take the same attribute.
- **Sap flow** sits under Plant rate variable, not Surface flux variable. It is
  transport inside a plant, reported per plant, so its unit is `kg.h-1/{plant}`.
- **Cloud cover and Air relative humidity are `1`**, fractions, as AGENTS.md sets
  for ratios of like quantities. Datasets often report both in percent.
- **Curator readings confirmed.** Water vapor concentration (a mole or volume
  fraction, on Atmospheric vapor concentration) and Water vapor density (a mass per
  volume) are different quantities. ODM2's `respirationNet` is Net respiration.
  Measured wind speed now takes `attributes=Wind speed`.
- **Slice 1 is not revisited here.** It mapped some names that are observables
  under this rule, such as `albedo`, `salinity`, `turbidity`, and `pH`, onto
  concepts. By slice 2's reading each would be a variable that names the concept.
  Moving those cross-references is a separate change.

## Slice 3: vegetation and ecology

The 40 names of slice 3 follow slice 2: an observable is a variable, and a name
for a thing is a concept. A variable has to be an observation *of* something or
*somewhere*, so a bare quantity such as biomass is a concept.

### Deliberately unmapped: the per-taxon names

17 ODM2 names fix a taxon: a coverage for each of 15 salt marsh taxa, one for
transient species, and `e_coli`, a count of one species. BERVO keeps no concepts
or variables for single species, and its variables are generic, with the taxon
recorded alongside the data through `BERVO:involves_taxa` or an NCBITaxon
identifier. No BERVO term is equivalent to a name that fixes a taxon, so these are
left unmapped. This is a difference between the two vocabularies, not a gap to
fill: `asteridaeCoverage`, `batisMaritimaCoverage`, `borrichiaFrutescensCoverage`, `cuscutaSppCoverage`, `distichlisSpicataCoverage`, `ivaFrutescenscoverage`, `limoniumNashiiCoverage`, `lyciumCarolinianumCoverage`, `monanthochloeLittoralisCoverage`, `salicorniaBigeloviiCoverage`, `salicorniaVirginicaCoverage`, `spartinaAlternifloraCoverage`, `spartinaSpartineaCoverage`, `suaedaLinearisCoverage`, `suaedaMaritimaCoverage`, `transientSpeciesCoverage`, `e_coli`.

The other four ODM2 indicator-organism names, `coliformTotal`, `coliformFecal`,
`enterococci`, and `streptococciFecal`, did get concepts in slice 1. They name
groups that water quality assays report, not single species, which is the line
`e_coli` falls on the other side of.

A dataset of these observations would use Percent area covered by specified plant
(`BERVO:0001834`) or Area covered by specified plant (`BERVO:0001833`) for the
coverages, and Colony-forming unit density in water for *E. coli*, each with the
taxon attached.

### Mapped to existing terms

| ODM2 term(s) | BERVO term |
| --- | --- |
| `areaBasal` | Stand basal area (`BERVO:0001887`) |
| `diameterAtBreastHeight` | Stem diameter at breast height (`BERVO:0001885`) |
| `leafAreaIndex` | Canopy leaf area index (`BERVO:0001879`) |
| `litterPlant` | Litter (`BERVO:8000055`), a concept, which also gains `ENVO:01000628` "plant litter" |
| `biomassTotal` | Biomass (`BERVO:8000296`), a concept, beside `biomass` from slice 1 |

`litterPlant` and `biomassTotal` name a thing or a bare quantity, so they map to
concepts, as `hail` did in slice 2.

### New terms

Ecology variable (`BERVO:9000040`), under Variable, holds observations of
organisms and communities. Fish (`BERVO:8000897`) sits under Organism with no
taxon cross-reference, since the grouping is not monophyletic. Wrack
(`BERVO:8000898`), dead plant material cast up by tides, sits under Litter. It
has no cross-reference: ENVO has no term for wrack or beach-cast material. Number
density (`BERVO:8000899`), a count of discrete objects or organisms per unit area
or volume, sits under Physical property beside Density, which is mass per volume.

23 variables (`0001967`, `0001968`, `0001969`, `0001970`, `0001971`, `0001972`, `0001973`, `0001974`, `0001975`, `0001976`, `0001978`, `0001979`, `0001980`, `0001981`, `0001983`, `0001984`, `0001985`, `0001986`, `0001987`, `0001988`, `0001990`, `0001991`, `0001992`):

| BERVO variable | Parent | ODM2 term | Unit |
| --- | --- | --- | --- |
| Canopy height (`BERVO:0001967`) | Canopy variable | `canopyHeight` | `m` |
| Canopy closure (`BERVO:0001968`) | Canopy variable | `canopyClosure` | `1` |
| Normalized difference vegetation index (`BERVO:0001969`) | Land surface variable | `NDVI` | `1` |
| Vegetation biomass (`BERVO:0001970`) | Ecology variable | `biomassVegetation` | `g.m-2` |
| Aboveground biomass (`BERVO:0001971`) | Vegetation biomass | `biomassAboveGround` | `g.m-2` |
| Leaf wetness (`BERVO:0001972`) | Meteorological variable | `leafWetness` | `1` |
| Vegetation type (`BERVO:0001973`) | Ecology variable | `vegetationType` | `NA` |
| Throughfall (`BERVO:0001974`) | Precipitation amount | `throughfall` | `mm` |
| Unvegetated cover (`BERVO:0001975`) | Land surface variable | `noVegetationCoverage` | `1` |
| Wrack cover (`BERVO:0001976`) | Surface litter variable | `wrackCoverage` | `1` |
| Phytoplankton biomass (`BERVO:0001978`) | Ecology variable | `biomassPhytoplankton` | `g.m-3` |
| Body length (`BERVO:0001979`) | Ecology variable | `bodyLength` | `m` |
| Chlorophyll fluorescence (`BERVO:0001980`) | Water variable | `chlorophyllFluorescence` | `{RFU}` |
| Organism count per unit area (`BERVO:0001981`) | Ecology variable | `countAreal` | `m-2` |
| Fish detections (`BERVO:0001983`) | Ecology variable | `fishDetections` | `1` |
| Shannon diversity index (`BERVO:0001984`) | Ecology variable | `shannonDiversityIndex` | `1` |
| Shannon evenness index (`BERVO:0001985`) | Ecology variable | `shannonEvennessIndex` | `1` |
| Taxa count (`BERVO:0001986`) | Ecology variable | `taxaCount` | `1` |
| Microbial cell density (`BERVO:0001987`) | Ecology variable | none | `{cells}.m-3` |
| Microbial cell density in water (`BERVO:0001988`) | Microbial cell density | none | `{cells}.m-3` |
| Colony-forming unit density (`BERVO:0001990`) | Ecology variable | none | `{CFU}.m-3` |
| Colony-forming unit density in water (`BERVO:0001991`) | Colony-forming unit density | none | `{CFU}.m-3` |
| Fish body length (`BERVO:0001992`) | Body length | none | `m` |

None of the new variables is a plant trait, so none sits under Plant trait
variable. Canopy height is the parent of EcoSIM's Pft canopy height
(`BERVO:0000695`) and Canopy height over grid (`BERVO:0000708`).

### Existing terms changed

- **Microbial density (`BERVO:0001162`) is now Microbial cell density in soil**,
  with "microbial density" as an exact synonym. It is defined for soil or sediment,
  so it is the soil member of the Microbial cell density family, not the generic
  term. It takes `measured_ins=Soil`, keeps its EcoSIM provenance (`BIOS`), and keeps
  Microbial parameters as its `Category`.
- **Stem density (`BERVO:0001888`) is now Stem count per unit area**, with "stem
  density" as an exact synonym, since the old label could as well mean the density
  of stem wood.
- **Canopy leaf area index, Canopy stem area index, Effective leaf area index, and
  Plant area index** move to Canopy variable, beside Canopy height and closure.
- **Fractional vegetation cover** moves to Land surface variable, beside its
  complement Unvegetated cover, and changes unit from `m2.m-2` to `1`.
- **Stand basal area and Stem count per unit area** move to Ecology variable,
  beside Vegetation biomass and Organism count per unit area.
- **Stand-level observables leave the Plant variable branch.** Canopy variable sits
  under Plant variable, so the canopy indices stay inside it. Ecology variable and
  Land surface variable do not, so Stand basal area, Stem count per unit area,
  and Fractional vegetation cover are no longer plant variables. That is
  deliberate: each describes a stand or a stretch of ground, a community rather
  than a plant.

### Points to note for slice 3

- **A count per area is not a count.** Stem count per unit area, Organism count
  per unit area, and the microbial cell and colony densities take
  `attributes=Number density` and `value_types=Quantitative value`, and the first
  two a label that says "per unit area". A count, per grid cell or dimensionless,
  such as Fish detections, Taxa count, and Plant population (`BERVO:0000725`, the
  number of plants in a grid cell), takes `attributes=Count` and
  `value_types=Count`. The seven other EcoSIM grid-cell counts took it in the same
  change: Total plant population, the three grain number rows, and the three root
  layer axis counts. Maximum root layer number (`BERVO:0000985`) did not. Despite
  its label, it is the index of the deepest rooted layer, not a count, and it
  waits on issue #108 with the other layer indices.
- **Where Number density sits.** Under Physical property, beside Density, because
  Density is defined as mass per volume and a number density is not a mass. Five
  older terms use Density for something that is not a mass per volume, and none is
  changed here: Area density (`BERVO:8000267`), mass per unit area, sits under it;
  Total root length density (`BERVO:0000408`) and Root length density in soil
  layers (`BERVO:0001103`), both `m.m-3`, Liquid water molar density
  (`BERVO:0001881`), `mol.m-3`, and Optical density (`BERVO:8000515`), light
  attenuation, name it in `attributes`.
  Count, the other candidate parent, sits under Quantitative value, and a number
  density is a physical quantity, not a kind of value.
- **The Stem density relabel was the curator's call.** "Stem density" is the usual
  forestry term, and it stays as an exact synonym, so a search for it still finds
  Stem count per unit area.
- **Two kinds of microbial count.** A count of cells and a count of colonies grown
  in culture measure different things, so each has its own family: Microbial cell
  density, with children for water and soil, and Colony-forming unit density, with
  a child for water. The cell family names no method, so a modelled density, such
  as EcoSIM's, belongs in it as much as a microscope count does. Both families take
  Number density and are per cubic metre, one scale for each family.
- **Body length is in `m`**, one scale for the whole family, so that a fish and a
  copepod compare directly, whatever scale each is usually reported in. Fish body
  length holds the fish standards: total, fork, and standard length.
- **Cover fractions take `1` and `value_types=Fraction`**: Canopy closure,
  Unvegetated cover, Wrack cover, Leaf wetness, and Fractional vegetation cover. Leaf area index keeps
  `m2.m-2`, because it is not a fraction and can exceed 1.
- **Leaf wetness** is the fraction of a leaf surface covered by liquid water. A
  sensor index approximates it; leaf wetness duration, time wet per interval, is a
  different quantity. Chlorophyll fluorescence is `{RFU}` unless a sensor is
  calibrated to a concentration.
- **Biomass rows** name Biomass in `measurement_ofs` and the organism or
  compartment in `measured_ins`, Phytoplankton biomass included.
- **No Index attribute.** NDVI and the Shannon indices keep `attributes=NA`: the
  only Index concept (`BERVO:8000488`) is a position identifier.
- **Percent area covered by specified plant has unit `1`**, while its label and
  definition say percent. That is older than this slice.
- **Vegetation type is categorical**, `NA` with `value_types=Category`; its
  categories are the question of issue #108.

## Slice 4: hydrology and snow

The 31 names of slice 4 follow the rules of slices 2 and 3: an observable is a
variable, a name for a thing is a concept, a true equivalent is mapped rather than
duplicated, and a generic observable becomes the parent of the EcoSIM variables
that are narrower forms of it.

### Mapped to existing variables

| ODM2 term(s) | BERVO variable |
| --- | --- |
| `snowDepth`, `depthSnow` | Snowpack depth (`BERVO:0001572`) |
| `snowWaterEquivalent` | Snow water equivalent (`BERVO:0001873`) |
| `volumetricWaterContent` | Volumetric water content (`BERVO:0001743`) |
| `discharge` | Water current (`BERVO:0001837`) |

ODM2 lists snow depth twice, as `snowDepth` and `depthSnow`; both land on Snowpack
depth. Water current carries `MIXS:0000203`, the MIxS field for a volumetric
flow, which is what discharge is. It gains `discharge` as a related synonym and
Hydrology variable as a second parent beside Water variable.

### New terms

Hydrology variable (`BERVO:9000041`), under Variable, holds observations of the
quantity, level, and movement of surface water and groundwater, and its use. Water
variable was not used: its definition is water chemistry.

| BERVO term | Parent | Cross-reference |
| --- | --- | --- |
| Alluvium (`BERVO:8000900`) | Sediment | `ENVO:01001202` |
| Reservoir (`BERVO:8000901`) | Water body | `ENVO:00000025` |
| Water well (`BERVO:8000902`) | Human construction | `ENVO:01000002` |
| Sea floor (`BERVO:8000903`) | Environmental feature | `ENVO:00000482` |

26 variables, `BERVO:0001993` to `BERVO:0002018`:

| BERVO variable | Parent | ODM2 term | Unit |
| --- | --- | --- | --- |
| Streamflow (`BERVO:0001993`) | Water current | `streamflow` | `m3.s-1` |
| Baseflow (`BERVO:0001994`) | Streamflow | `baseflow` | `m3.s-1` |
| Water depth (`BERVO:0001995`) | Hydrology variable | `waterDepth` | `m` |
| Averaged water depth (`BERVO:0001996`) | Water depth | `waterDepthAveraged` | `m` |
| Water level (`BERVO:0001997`) | Hydrology variable | `waterLevel` | `m` |
| Gage height (`BERVO:0001998`) | Water level | `gageHeight` | `m` |
| Tide stage (`BERVO:0001999`) | Water level | `tideStage` | `m` |
| Wave height (`BERVO:0002000`) | Hydrology variable | `waveHeight` | `m` |
| Secchi depth (`BERVO:0002001`) | Hydrology variable | `secchiDepth` | `m` |
| Light attenuation coefficient (`BERVO:0002002`) | Hydrology variable | `lightAttenuationCoefficient` | `m-1` |
| Sigma-t (`BERVO:0002003`) | Hydrology variable | `sigma_t` | `kg.m-3` |
| Height above sea floor (`BERVO:0002004`) | Hydrology variable | `heightAboveSeaFloor` | `m` |
| Water table depth (`BERVO:0002005`) | Hydrology variable | `groundwaterDepth`, `depthUnsaturatedZone` | `m` |
| Groundwater recharge (`BERVO:0002006`) | Hydrology variable | `rechargeGroundwater` | `mm.d-1` |
| Reservoir storage (`BERVO:0002007`) | Hydrology variable | `reservoirStorage` | `m3` |
| Well flow rate (`BERVO:0002008`) | Hydrology variable | `wellFlowRate` | `m3.s-1` |
| Wellhead pressure (`BERVO:0002009`) | Hydrology variable | `wellheadPressure` | `kPa` |
| Water use (`BERVO:0002010`) | Hydrology variable | none | `m3.d-1` |
| Agricultural water use (`BERVO:0002011`) | Water use | `waterUseAgriculture` | `m3.d-1` |
| Commercial, industrial, and power water use (`BERVO:0002012`) | Water use | `waterUseCommercialIndustrialPower` | `m3.d-1` |
| Domestic well water use (`BERVO:0002013`) | Water use | `waterUseDomesticWells` | `m3.d-1` |
| Public supply water use (`BERVO:0002014`) | Water use | `waterUsePublicSupply` | `m3.d-1` |
| Recreational water use (`BERVO:0002015`) | Water use | `waterUseRecreation` | `m3.d-1` |
| Gate position (`BERVO:0002016`) | Hydrology variable | `position` | `1` |
| Alluvium depth (`BERVO:0002017`) | Hydrology variable | `alluviumDepth` | `m` |
| Snow layer hardness (`BERVO:0002018`) | Snow variable | `snowLayerHardness` | `NA` |

### Points to note for slice 4

- **Hierarchies.** Streamflow sits under Water current, the discharge term, and
  Baseflow under Streamflow. Gage height and Tide stage sit under Water level,
  Averaged water depth under Water depth, and the five ODM2 water use names under a
  new generic Water use, which carries no ODM2 name of its own.
- **Water table depth is the parent of EcoSIM's water table depths**: Depth of
  artificial water table (`BERVO:0001760`), Artificial water table depth
  (`BERVO:0001761`), Depth of artificial water table adjusted for elevation
  (`BERVO:0001762`), Internal water table depth (`BERVO:0001763`), and External
  water table depth (`BERVO:0001766`), which already holds the initial and current
  elevation-corrected forms. ODM2 calls the quantity groundwater depth, an exact
  synonym here.
- **Two ODM2 names on Water table depth.** `depthUnsaturatedZone` maps there beside
  `groundwaterDepth`: the unsaturated zone runs from the land surface down to the
  water table, so its depth is the same distance.
- **Gate position** is ODM2's `position`, the setting of a gate or other
  water-control element, not a spatial position. It is a fraction of fully open;
  some datasets report a height or a number of turns instead.
- **Snow layer hardness is categorical**, `NA` with `value_types=Category`: it is
  recorded on the hand hardness scale, fist to ice. Its categories belong to issue
  #108.
- **Units.** Discharge-like flows are `m3.s-1`, water use `m3.d-1`, and groundwater
  recharge `mm.d-1`, per unit area.

## Points to note (slice 1)

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
  groups where the variables need them, such as Cryptophytes and
  Enterococcus, and not for individual species. A variable
  that concerns one species is expected to carry that species as an NCBITaxon
  identifier in the data, not as a BERVO concept. A first draft of this slice
  added 14 salt marsh plants (13 species and the genus *Cuscuta*) as
  `BERVO:8000871` to `BERVO:8000884`, and the clade Asterids as
  `BERVO:8000870`. They were removed before merge and were never released.
  The one term added after that, Electrical conductivity, was given
  `BERVO:8000885`, so `just next-id` counts on from there and does not hand
  the removed identifiers out again. Keeping them retired for good is
  [issue #103](https://github.com/bioepic-data/bervo/issues/103). Plant is
  otherwise a parent of plant organs, and a clade among them read badly.
  *Escherichia coli* (`BERVO:8000867`) was removed the same way. Fecal coliform
  bacteria stays, because that is the group water quality assays report.
  ODM2's `e_coli` goes to the ecology slice as a variable.
- **Labels of taxon groups.** A group takes the name its measurements use as
  the label, and NCBI's scientific name as an exact synonym: Cryptophytes
  (Cryptophyceae), Dinoflagellates (Dinophyceae), Cyanobacteria
  (Cyanobacteriota). A genus kept as a group, such as
  Enterococcus, takes the genus name, with the plural in common use
  (`enterococci`) as a related synonym. Fungi (`BERVO:8000783`) already
  followed this.
- **Salt marsh taxa.** The coverage terms, left unmapped in slice 3, name taxa that NCBI
  Taxonomy has renamed since: *Spartina alterniflora* is now *Sporobolus
  alterniflorus* (`NCBITaxon:29706`), *Spartina spartinae* (which ODM2 spells
  "Spartina spartinea") is *Sporobolus spartinus* (`NCBITaxon:180094`), and
  *Monanthochloe littoralis* is *Distichlis littoralis* (`NCBITaxon:160556`).
  *Limonium nashii* is not in NCBI Taxonomy. `asteridaeCoverage` names a
  clade, which NCBI labels "asterids" (`NCBITaxon:71274`) with Asteridae as a
  synonym.
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
- **Two N-acetylglucosaminidases.** Alpha-N-acetylglucosaminidase
  (`BERVO:8000856`, EC 3.2.1.50) is added here for ODM2's
  `alphaNAcetylglucosaminidase`. The soil slice's
  `activityBetaNAcetylGlucosaminidase` is a different enzyme,
  beta-N-acetylglucosaminidase (EC 3.2.1.52), the one the standard soil NAG
  assay measures. It must not be mapped onto the alpha term, which
  `just find "acetylglucosaminidase"` returns.
- **Minerals.** Quartz and Cristobalite take Silicon dioxide as a second parent,
  as polymorphs of silica. Albite takes Alkali feldspar as a second parent beside
  Plagioclase, since it is the sodium endmember of both series. Feldspar is added as a grouping term, not from ODM2,
  so that alkali feldspar and plagioclase have the parent they share. The other
  minerals sit flat under Mineral. `CHEBI:30194` is labelled
  "gamma-aluminium hydroxide" and carries gibbsite as a synonym.
- **Temperature change sits under Temperature for now.** A difference of two
  temperatures is not a temperature, so the subclass axiom overclaims. It is
  left in place and tracked as
  [issue #102](https://github.com/bioepic-data/bervo/issues/102).
- **Conductivity is now the general term.** Conductivity (`BERVO:8000348`)
  was defined as electrical conductivity, while Thermal conductivity sat apart
  under Physical property. It is
  now the general ability to transmit a flow in proportion to its driving
  gradient, under Physical property, with Electrical conductivity
  (`BERVO:8000885`, new), Thermal conductivity (`BERVO:8000589`), and
  Hydraulic conductivity beneath it. Electrical conductivity takes the two ODM2
  cross-references, `ODM2:speciation/EC` and
  `ODM2:variablename/electricalConductivity`, and their comments. Conductivity
  keeps `COMO:0000124`, whose COMO label could not be checked.
- **Specific conductivity is Specific conductance.** `BERVO:8000426` is
  relabelled, redefined as electrical conductivity corrected to a reference
  temperature, and placed under Electrical conductivity, with `specific
  conductivity` as a related synonym. ODM2's `specificConductance` maps to it
  in the water quality slice.
- **Pressure gathers its kinds.** Pressure (`BERVO:8000518`) had no children
  before this slice. Air pressure, Water pressure, and Vapor pressure move
  under it from Concept, and Partial pressure from Physical property, beside
  the three new pressures. Pressure itself moves under Physical property, as
  Conductivity does, so Partial pressure keeps that ancestor.
- **Power.** Power (`BERVO:8000886`, `PATO:0001024`) is added so that Electric
  power has the parent its name implies, as Electric energy has Energy. Energy
  (`BERVO:8000132`) gives up `power` as a related synonym. Electric current and
  Voltage stay under Physical property; neither is a kind of a broader BERVO
  quantity.
- **Threshold and Critical.** Critical (`BERVO:8000005`) carried `threshold` as an
  exact synonym, so two terms answered to the word. Critical is a state near a
  tipping point, and the new Threshold is the operational level at which an
  action is taken. `threshold` is now a related synonym of Critical.
- **The ODM2 identifier is not kept as a synonym.** The speciation alignment
  kept ODM2's formulas, which people write. These identifiers are camelCase
  database keys that nobody writes.
