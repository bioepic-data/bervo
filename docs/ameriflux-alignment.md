# Alignment with AmeriFlux

[AmeriFlux](https://ameriflux.lbl.gov/) is the network of eddy covariance flux sites
in the Americas, supported by the DOE Environmental System Science program
(<https://ess.science.energy.gov/ameriflux/>). Its data products name their variables
with short codes such as `FC`, `SWC` or `NEE_VUT_REF`. This page records how each code
maps to BERVO. The work is tracked in
[issue #178](https://github.com/bioepic-data/bervo/issues/178) and added in slices.

## Sources

All fetched on 2026-10-15.

| Collection | Source | Size |
| --- | --- | --- |
| FP-Standard base names (half-hourly flux and weather data) | `https://amfcdn.lbl.gov/api/v1/fp_var`, the list behind <https://ameriflux.lbl.gov/data/aboutdata/data-variables/> | 145 names |
| Variable-name qualifiers | section 3 of the same page | 9 |
| Base names in use, by site | [`AMF_AA-Flx_BASE_VARIABLE-AVAILABILITY_LATEST.csv`](https://raw.githubusercontent.com/chuhousen/amerifluxr/master/data-summary/AMF_AA-Flx_BASE_VARIABLE-AVAILABILITY_LATEST.csv) from the `amerifluxr` package | 106 of the 145 in use |
| BADM site metadata | the BADM standard (<https://ameriflux.lbl.gov/data/badm/badm-standards/>) and [`AMF_AA-Net_BIF_LEGACY_VARIABLE-AVAILABILITY_LATEST.csv`](https://raw.githubusercontent.com/chuhousen/amerifluxr/master/data-summary/AMF_AA-Net_BIF_LEGACY_VARIABLE-AVAILABILITY_LATEST.csv) | 453 legacy fields |
| FLUXNET (ONEFlux) FULLSET product | <https://fluxnet.org/data/fluxnet2015-dataset/fullset-data-product/> | 232 variables |

## Decisions

These were settled on issue #178 and its pull requests.

1. **Scope.** Every AmeriFlux variable and concept is in scope. BADM fields that record
   dates, methods, comments, contacts or instrument settings describe a dataset rather
   than a quantity, and are left out.
2. **EcoSIM terms tied to the model are left as they are.** Where BERVO's only match was
   an EcoSIM variable defined for the model, such as the grid-cell
   `Net ecosystem carbon dioxide exchange` (`BERVO:0000326`, in `g.h-1/{grid}`), a
   tower-level term was added beside it, and the EcoSIM term was given the new term as
   an additional parent.
3. **Variants.** A variant that is a physically different quantity gets its own term:
   a mole fraction in wet air or in dry air, a turbulent flux or a storage flux. A variant
   that is a statistic or a flag does not: a `_SIGMA` variable is its base term with the
   `Standard deviation` qualifier, `WS_MAX` its base term with `Maximum`, and the nine
   `*_SSITC_TEST` flags share one term.
4. **Codes are related synonyms,** not cross-references, since AmeriFlux has no web
   address for a variable and a code is not an exact synonym. A code that is already the
   label, symbol or synonym of another BERVO term, case-insensitively, is recorded only in
   `Comment`, with the reason, because as a synonym it would lead text matchers to the
   wrong term. Examples are the chemical formulas `CO2` and `O3`, and `H` (Hydrogen),
   `LE` (Effective leaf area index), `SB` (Antimony), `SC` (Clayey sand), `P`
   (Phosphorus) and `SR` (Strontium). Every term records its code in `Comment` either way.
5. **FLUXNET processed variables get no term each.** BERVO adds the concepts that
   describe the processing and the few base quantities it lacked. The table below
   resolves each FLUXNET variable to a base term plus those concepts.
6. **BADM variants by layer, organ or live and dead status** take one generic term per
   quantity, with the variant in `contexts` or `qualifiers`, as the current BADM standard
   itself does.
7. **BADM value lists become concepts:** IGBP land cover, Köppen climate, and the BADM
   vegetation-type, phenology-event and disturbance lists.

Placement settled along the way:

- Tower gas mole fractions sit under `Atmospheric composition variable`
  (`BERVO:9000048`), not under the EcoSIM forcing group `Atmospheric gas concentration`.
- Turbulent and storage fluxes sit directly under `Surface flux variable`, because the
  generic flux terms, such as `Carbon dioxide flux`, are defined as exchange at the
  surface. `Net ecosystem exchange` is such an exchange and sits under
  `Carbon dioxide flux`.
- Fractions take BERVO's `1` even where AmeriFlux reports percent; the term's `Comment`
  says so.

## FP-Standard base names

145 of 145 base names resolve to a BERVO term. *How* says whether the code is a
synonym on the term, recorded only in its `Comment` (decision 4), or expressed as the
term plus a qualifier (decision 3).

| Group | Code | AmeriFlux description | AmeriFlux units | BERVO term | How |
| --- | --- | --- | --- | --- | --- |
| AQUATIC | `COND_WATER` | Conductivity (i.e., electrical conductivity) of water | µS cm-1 | `BERVO:0002313` Water electrical conductivity | synonym |
| AQUATIC | `DO` | Dissolved oxygen in water | µmol L-1 | `BERVO:0002314` Dissolved oxygen concentration | synonym |
| AQUATIC | `PCH4` | Dissolved methane (CH4) in water | nmolCH4 mol-1 | `BERVO:0002315` Dissolved methane equilibrium mole fraction | synonym |
| AQUATIC | `PCO2` | Dissolved carbon dioxide (CO2) in water | µmolCO2 mol-1 | `BERVO:0002316` Dissolved carbon dioxide equilibrium mole fraction | synonym |
| AQUATIC | `PN2O` | Dissolved nitrous oxide (N2O) in water | nmolN2O mol-1 | `BERVO:0002317` Dissolved nitrous oxide equilibrium mole fraction | synonym |
| AQUATIC | `PPFD_UW_IN` | Photosynthetic photon flux density, underwater, incoming | µmolPhotons m-2 s-1 | `BERVO:0002318` Underwater incoming photosynthetic photon flux density | synonym |
| AQUATIC | `TW` | Water temperature | deg C | `BERVO:0002312` Water temperature | synonym |
| BIOLOGICAL | `DBH` | Diameter of tree measured at breast height (1.3m) with continuous dendrometers | cm | `BERVO:0001885` Stem diameter at breast height | synonym |
| BIOLOGICAL | `LEAF_WET` | Leaf wetness, range 0-100 | % | `BERVO:0001972` Leaf wetness | synonym |
| BIOLOGICAL | `SAP_DT` | Difference of probes temperature for sapflow measurements | deg C | `BERVO:0002320` Sap flow probe temperature difference | synonym |
| BIOLOGICAL | `SAP_FLOW` | Sap flow | mmolH2O m-2 s-1 | `BERVO:0002319` Sap flux density | synonym |
| BIOLOGICAL | `T_BOLE` | Bole temperature | deg C | `BERVO:0002321` Bole temperature | synonym |
| BIOLOGICAL | `T_CANOPY` | Temperature of the canopy and/or surface underneath the sensor | deg C | `BERVO:0002322` Radiometric canopy surface temperature | synonym |
| FOOTPRINT | `FETCH_70` | Distance at which cross-wind integrated footprint cumulative probability is 70% | m | `BERVO:0002260` Flux footprint 70 percent distance | synonym |
| FOOTPRINT | `FETCH_80` | Distance at which cross-wind integrated footprint cumulative probability is 80% | m | `BERVO:0002261` Flux footprint 80 percent distance | synonym |
| FOOTPRINT | `FETCH_90` | Distance at which cross-wind integrated footprint cumulative probability is 90% | m | `BERVO:0002262` Flux footprint 90 percent distance | synonym |
| FOOTPRINT | `FETCH_FILTER` | Footprint quality flag (i.e., 0, 1): 0 and 1 indicate data measured when wind coming from direction that should be discarded and kept, respectively | nondimensional | `BERVO:0002264` Flux footprint wind direction flag | synonym |
| FOOTPRINT | `FETCH_MAX` | Distance at which footprint contribution is maximum | m | `BERVO:0002263` Flux footprint peak distance | synonym |
| GASES | `CH4` | Methane (CH4) mole fraction in wet air | nmolCH4 mol-1 | `BERVO:0002228` Methane mole fraction in wet air | `Comment` only |
| GASES | `CH4_MIXING_RATIO` | Methane (CH4) in mole fraction of dry air | nmolCH4 mol-1 | `BERVO:0002229` Methane mole fraction in dry air | synonym |
| GASES | `CO` | Carbon Monoxide (CO) mole fraction in wet air | nmolCO mol-1 | `BERVO:0002234` Carbon monoxide mole fraction in wet air | `Comment` only |
| GASES | `CO2` | Carbon Dioxide (CO2) mole fraction in wet air | µmolCO2 mol-1 | `BERVO:0002226` Carbon dioxide mole fraction in wet air | `Comment` only |
| GASES | `CO2C13` | Stable isotopic composition of CO2 - C13 (i.e., d13C of CO2) | ‰ (permil) | `BERVO:0002218` Carbon dioxide delta carbon-13 | synonym |
| GASES | `CO2_MIXING_RATIO` | Carbon Dioxide (CO2) in mole fraction of dry air | µmolCO2 mol-1 | `BERVO:0002227` Carbon dioxide mole fraction in dry air | synonym |
| GASES | `CO2_SIGMA` | Standard deviation of carbon dioxide mole fraction in wet air | µmolCO2 mol-1 | `BERVO:0002226` Carbon dioxide mole fraction in wet air | base term + `Standard deviation` qualifier |
| GASES | `FC` | Carbon Dioxide (CO2) turbulent flux (no storage correction) | µmolCO2 m-2 s-1 | `BERVO:0002239` Carbon dioxide turbulent flux | synonym |
| GASES | `FCH4` | Methane (CH4) turbulent flux (no storage correction) | nmolCH4 m-2 s-1 | `BERVO:0002240` Methane turbulent flux | synonym |
| GASES | `FN2O` | Nitrous oxide (N2O) turbulent flux (no storage correction) | nmolN2O m-2 s-1 | `BERVO:0002241` Nitrous oxide turbulent flux | synonym |
| GASES | `FNO` | Nitric oxide (NO) turbulent flux (no storage correction) | nmolNO m-2 s-1 | `BERVO:0002242` Nitric oxide turbulent flux | synonym |
| GASES | `FNO2` | Nitrogen dioxide (NO2) turbulent flux (no storage correction) | nmolNO2 m-2 s-1 | `BERVO:0002243` Nitrogen dioxide turbulent flux | synonym |
| GASES | `FO3` | Ozone (O3) turbulent flux (no storage correction) | nmolO3 m-2 s-1 | `BERVO:0002244` Ozone turbulent flux | synonym |
| GASES | `H2O` | Water (H2O) vapor in mole fraction of wet air | mmolH2O mol-1 | `BERVO:0002232` Water vapor mole fraction in wet air | synonym |
| GASES | `H2O_MIXING_RATIO` | Water (H2O) vapor in mole fraction of dry air | mmolH2O mol-1 | `BERVO:0002233` Water vapor mole fraction in dry air | synonym |
| GASES | `H2O_SIGMA` | Standard deviation of water vapor mole fraction | mmolH2O mol-1 | `BERVO:0002232` Water vapor mole fraction in wet air | base term + `Standard deviation` qualifier |
| GASES | `N2O` | Nitrous Oxide (N2O) mole fraction in wet air | nmolN2O mol-1 | `BERVO:0002230` Nitrous oxide mole fraction in wet air | `Comment` only |
| GASES | `N2O_MIXING_RATIO` | Nitrous Oxide (N2O) in mole fraction of dry air | nmolN2O mol-1 | `BERVO:0002231` Nitrous oxide mole fraction in dry air | synonym |
| GASES | `NO` | Nitric oxide (NO) mole fraction in wet air | nmolNO mol-1 | `BERVO:0002235` Nitric oxide mole fraction in wet air | `Comment` only |
| GASES | `NO2` | Nitrogen dioxide (NO2) mole fraction in wet air | nmolNO2 mol-1 | `BERVO:0002236` Nitrogen dioxide mole fraction in wet air | `Comment` only |
| GASES | `O3` | Ozone (O3) mole fraction in wet air | nmolO3 mol-1 | `BERVO:0002237` Ozone mole fraction in wet air | `Comment` only |
| GASES | `SC` | Carbon Dioxide (CO2) storage flux | µmolCO2 m-2 s-1 | `BERVO:0001944` Carbon dioxide storage flux | `Comment` only |
| GASES | `SCH4` | Methane (CH4) storage flux | nmolCH4 m-2 s-1 | `BERVO:0002248` Methane storage flux | synonym |
| GASES | `SN2O` | Nitrous oxide (N2O) storage flux | nmolN2O m-2 s-1 | `BERVO:0002249` Nitrous oxide storage flux | synonym |
| GASES | `SNO` | Nitric oxide (NO) storage flux | nmolNO m-2 s-1 | `BERVO:0002250` Nitric oxide storage flux | synonym |
| GASES | `SNO2` | Nitrogen dioxide (NO2) storage flux | nmolNO2 m-2 s-1 | `BERVO:0002251` Nitrogen dioxide storage flux | synonym |
| GASES | `SO2` | Sulfur Dioxide (SO2) mole fraction in wet air | nmolSO2 mol-1 | `BERVO:0002238` Sulfur dioxide mole fraction in wet air | `Comment` only |
| GASES | `SO3` | Ozone (O3) storage flux | nmolO3 m-2 s-1 | `BERVO:0002252` Ozone storage flux | `Comment` only |
| HEAT | `FH2O` | Water vapor (H2O) turbulent flux (no storage correction) | mmolH2O m-2 s-1 | `BERVO:0002245` Water vapor turbulent flux | synonym |
| HEAT | `G` | Soil heat flux | W m-2 | `BERVO:0002257` Soil heat flux at measurement depth | synonym |
| HEAT | `H` | Sensible heat turbulent flux (no storage correction) | W m-2 | `BERVO:0002246` Sensible heat turbulent flux | `Comment` only |
| HEAT | `LE` | Latent heat turbulent flux (no storage correction) | W m-2 | `BERVO:0002247` Latent heat turbulent flux | `Comment` only |
| HEAT | `SB` | Heat storage flux in biomass | W m-2 | `BERVO:0002255` Biomass heat storage flux | `Comment` only |
| HEAT | `SG` | Heat storage flux in the soil above the soil heat fluxes measurement | W m-2 | `BERVO:0002256` Soil heat storage flux | synonym |
| HEAT | `SH` | Sensible heat (H) storage flux | W m-2 | `BERVO:0002253` Sensible heat storage flux | synonym |
| HEAT | `SLE` | Latent heat (LE) storage flux | W m-2 | `BERVO:0002254` Latent heat storage flux | synonym |
| MET_ATM | `PA` | Atmospheric pressure | kPa | `BERVO:0001375` Atmospheric pressure | synonym |
| MET_ATM | `PBLH` | Planetary boundary layer height | m | `BERVO:0002266` Planetary boundary layer height | synonym |
| MET_ATM | `RH` | Relative humidity, range 0-100 | % | `BERVO:0001910` Air relative humidity | synonym |
| MET_ATM | `TA` | Air temperature | deg C | `BERVO:0001370` Air temperature | synonym |
| MET_ATM | `T_SONIC` | Sonic temperature | deg C | `BERVO:0002267` Sonic temperature | synonym |
| MET_ATM | `T_SONIC_SIGMA` | Standard deviation of sonic temperature | deg C | `BERVO:0002267` Sonic temperature | base term + `Standard deviation` qualifier |
| MET_ATM | `VPD` | Vapor Pressure Deficit | hPa | `BERVO:0001913` Vapor pressure deficit | synonym |
| MET_PRECIP | `D_SNOW` | Snow depth | cm | `BERVO:0001572` Snowpack depth | synonym |
| MET_PRECIP | `P` | Precipitation | mm | `BERVO:0001908` Precipitation amount | `Comment` only |
| MET_PRECIP | `P_RAIN` | Rainfall | mm | `BERVO:0002273` Rainfall amount | synonym |
| MET_PRECIP | `P_SNOW` | Snowfall | mm | `BERVO:0002274` Snowfall amount | synonym |
| MET_PRECIP | `RUNOFF` | Run off | mm | `BERVO:0002276` Runoff depth | `Comment` only |
| MET_PRECIP | `STEMFLOW` | Excess precipitation that drains from outlying branches and leaves and is channeled through the stems to the ground | mm | `BERVO:0002275` Stemflow | synonym |
| MET_PRECIP | `THROUGHFALL` | Excess precipitation that passes directly through a canopy or drips from wet leaves to the ground | mm | `BERVO:0001974` Throughfall | synonym |
| MET_RAD | `ALB` | Albedo, range 0-100 | % | `BERVO:0002278` Ecosystem shortwave albedo | synonym |
| MET_RAD | `APAR` | Absorbed PAR | µmolPhoton m-2 s-1 | `BERVO:0002279` Absorbed photosynthetic photon flux density | synonym |
| MET_RAD | `EVI` | Enhanced Vegetation Index | nondimensional | `BERVO:0002303` Enhanced vegetation index | synonym |
| MET_RAD | `FAPAR` | Fraction of absorbed PAR, range 0-100 | % | `BERVO:0002280` Fraction of absorbed photosynthetically active radiation | synonym |
| MET_RAD | `FIPAR` | Fraction of intercepted PAR, range 0-100 | % | `BERVO:0002281` Fraction of intercepted photosynthetically active radiation | synonym |
| MET_RAD | `LW_BC_IN` | Longwave radiation, below canopy incoming | W m-2 | `BERVO:0002284` Below-canopy incoming longwave radiation | synonym |
| MET_RAD | `LW_BC_OUT` | Longwave radiation, below canopy outgoing | W m-2 | `BERVO:0002285` Below-canopy outgoing longwave radiation | synonym |
| MET_RAD | `LW_IN` | Longwave radiation, incoming | W m-2 | `BERVO:0001380` Sky longwave radiation | synonym |
| MET_RAD | `LW_OUT` | Longwave radiation, outgoing | W m-2 | `BERVO:0001936` Outgoing longwave radiation | synonym |
| MET_RAD | `MCRI` | Carotenoid Reflectance Index (Gitelson et al., 2002) | nondimensional | `BERVO:0002304` Carotenoid reflectance index | synonym |
| MET_RAD | `MTCI` | Meris Terrestrial Chlorophyll Index (Dash and Curran, 2004) | nondimensional | `BERVO:0002305` MERIS terrestrial chlorophyll index | synonym |
| MET_RAD | `NDVI` | Normalized Difference Vegetation Index | nondimensional | `BERVO:0001969` Normalized difference vegetation index | synonym |
| MET_RAD | `NETRAD` | Net radiation | W m-2 | `BERVO:0001932` Net radiation | synonym |
| MET_RAD | `NIRV` | Near Infrared Vegetation Index (Badgley et al., 2017) | W m-2 sr-1 nm-1 | `BERVO:0002306` Near-infrared reflectance of vegetation | synonym |
| MET_RAD | `PPFD_BC_IN` | Photosynthetic photon flux density, below canopy incoming | µmolPhoton m-2 s-1 | `BERVO:0002286` Below-canopy incoming photosynthetic photon flux density | synonym |
| MET_RAD | `PPFD_BC_OUT` | Photosynthetic photon flux density, below canopy outgoing | µmolPhoton m-2 s-1 | `BERVO:0002287` Below-canopy outgoing photosynthetic photon flux density | synonym |
| MET_RAD | `PPFD_DIF` | Photosynthetic photon flux density, diffuse incoming | µmolPhoton m-2 s-1 | `BERVO:0001405` Diffuse photosynthetically active radiation | synonym |
| MET_RAD | `PPFD_DIR` | Photosynthetic photon flux density, direct incoming | µmolPhoton m-2 s-1 | `BERVO:0001404` Direct photosynthetically active radiation | synonym |
| MET_RAD | `PPFD_IN` | Photosynthetic photon flux density, incoming | µmolPhoton m-2 s-1 | `BERVO:0001927` Photosynthetic photon flux density | synonym |
| MET_RAD | `PPFD_OUT` | Photosynthetic photon flux density, outgoing | µmolPhoton m-2 s-1 | `BERVO:0001937` Outgoing photosynthetically active radiation | synonym |
| MET_RAD | `PRI` | Photochemical Reflectance Index | nondimensional | `BERVO:0002307` Photochemical reflectance index | synonym |
| MET_RAD | `REDCI` | Red Edge Chlorophyll Index | nondimensional | `BERVO:0002308` Red edge chlorophyll index | synonym |
| MET_RAD | `REP` | Red Edge Position (Dash and Curran, 2004) | nm | `BERVO:0002309` Red edge position | synonym |
| MET_RAD | `R_UVA` | UVA radiation, incoming | W m-2 | `BERVO:0001930` Incoming ultraviolet A radiation | synonym |
| MET_RAD | `R_UVB` | UVB radiation, incoming | W m-2 | `BERVO:0001931` Incoming ultraviolet B radiation | synonym |
| MET_RAD | `SPEC_NIR_IN` | Radiation (near infra-red band), incoming (hemispherical) | W m-2 nm-1 | `BERVO:0002291` Incoming near-infrared spectral irradiance | synonym |
| MET_RAD | `SPEC_NIR_OUT` | Radiation (near infra-red band), outgoing | W m-2 sr-1 nm-1 | `BERVO:0002292` Outgoing near-infrared spectral radiance | synonym |
| MET_RAD | `SPEC_NIR_REFL` | Reflectance (near infra-red band) | nondimensional | `BERVO:0002293` Near-infrared spectral reflectance | synonym |
| MET_RAD | `SPEC_PRI_REF_IN` | Radiation for PRI reference band (e.g., 570 nm), incoming (hemispherical) | W m-2 nm-1 | `BERVO:0002297` Incoming photochemical reflectance index reference band spectral irradiance | synonym |
| MET_RAD | `SPEC_PRI_REF_OUT` | Radiation for PRI reference band (e.g., 570 nm), outgoing | W m-2 sr-1 nm-1 | `BERVO:0002298` Outgoing photochemical reflectance index reference band spectral radiance | synonym |
| MET_RAD | `SPEC_PRI_REF_REFL` | Reflectance for PRI reference band (e.g., 570 nm) | nondimensional | `BERVO:0002299` Photochemical reflectance index reference band spectral reflectance | synonym |
| MET_RAD | `SPEC_PRI_TGT_IN` | Radiation for PRI target band (e.g., 531 nm), incoming (hemispherical) | W m-2 nm-1 | `BERVO:0002300` Incoming photochemical reflectance index target band spectral irradiance | synonym |
| MET_RAD | `SPEC_PRI_TGT_OUT` | Radiation for PRI target band (e.g., 531 nm), outgoing | W m-2 sr-1 nm-1 | `BERVO:0002301` Outgoing photochemical reflectance index target band spectral radiance | synonym |
| MET_RAD | `SPEC_PRI_TGT_REFL` | Reflectance for PRI target band (e.g., 531 nm) | nondimensional | `BERVO:0002302` Photochemical reflectance index target band spectral reflectance | synonym |
| MET_RAD | `SPEC_RED_IN` | Radiation (red band), incoming (hemispherical) | W m-2 nm-1 | `BERVO:0002294` Incoming red spectral irradiance | synonym |
| MET_RAD | `SPEC_RED_OUT` | Radiation (red band), outgoing | W m-2 sr-1 nm-1 | `BERVO:0002295` Outgoing red spectral radiance | synonym |
| MET_RAD | `SPEC_RED_REFL` | Reflectance (red band) | nondimensional | `BERVO:0002296` Red spectral reflectance | synonym |
| MET_RAD | `SR` | Simple Ratio | nondimensional | `BERVO:0002310` Simple ratio vegetation index | `Comment` only |
| MET_RAD | `SW_BC_IN` | Shortwave radiation, below canopy incoming | W m-2 | `BERVO:0002282` Below-canopy incoming shortwave radiation | synonym |
| MET_RAD | `SW_BC_OUT` | Shortwave radiation, below canopy outgoing | W m-2 | `BERVO:0002283` Below-canopy outgoing shortwave radiation | synonym |
| MET_RAD | `SW_DIF` | Shortwave radiation, diffuse incoming | W m-2 | `BERVO:0001403` Diffuse shortwave radiation | synonym |
| MET_RAD | `SW_DIR` | Shortwave radiation, direct incoming | W m-2 | `BERVO:0001402` Direct shortwave radiation | synonym |
| MET_RAD | `SW_IN` | Shortwave radiation, incoming | W m-2 | `BERVO:0001867` Incoming shortwave radiation | synonym |
| MET_RAD | `SW_OUT` | Shortwave radiation, outgoing | W m-2 | `BERVO:0001938` Outgoing shortwave radiation | synonym |
| MET_RAD | `TCARI` | Transformed Chlorophyll Absorption in Reflectance Index | nondimensional | `BERVO:0002311` Transformed chlorophyll absorption in reflectance index | synonym |
| MET_SOIL | `SECA` | Soil apparent Electrical Conductivity | dS m-1 | `BERVO:0002036` Bulk electrical conductivity | synonym |
| MET_SOIL | `SWC` | Soil water content (volumetric), range 0-100 | % | `BERVO:0001743` Volumetric water content | synonym |
| MET_SOIL | `SWP` | Soil water potential | kPa | `BERVO:0002277` Soil water potential | synonym |
| MET_SOIL | `TS` | Soil temperature | deg C | `BERVO:0001477` Soil temperature | synonym |
| MET_SOIL | `TSN` | Snow temperature | deg C | `BERVO:0001556` Snow temperature | synonym |
| MET_SOIL | `WTD` | Water table depth | m | `BERVO:0002005` Water table depth | synonym |
| MET_WIND | `MO_LENGTH` | Monin-Obukhov length | m | `BERVO:0002268` Monin-Obukhov length | synonym |
| MET_WIND | `TAU` | Momentum flux | kg m-1 s-2 | `BERVO:0001940` Momentum flux | synonym |
| MET_WIND | `USTAR` | Friction velocity | m s-1 | `BERVO:0001906` Friction velocity | synonym |
| MET_WIND | `U_SIGMA` | Standard deviation of velocity fluctuations (towards main-wind direction after coordinates rotation) | m s-1 | `BERVO:0002270` Streamwise wind velocity | base term + `Standard deviation` qualifier |
| MET_WIND | `V_SIGMA` | Standard deviation of lateral velocity fluctuations (cross main-wind direction after coordinates rotation) | m s-1 | `BERVO:0002271` Crosswind wind velocity | base term + `Standard deviation` qualifier |
| MET_WIND | `WD` | Wind direction | Decimal degrees | `BERVO:0001916` Near-surface wind direction | synonym |
| MET_WIND | `WD_SIGMA` | Standard deviation of wind direction (Yamartino, 1984) | decimal degree | `BERVO:0001916` Near-surface wind direction | base term + `Standard deviation` qualifier |
| MET_WIND | `WS` | Wind speed | m s-1 | `BERVO:0001372` Measured wind speed | synonym |
| MET_WIND | `WS_MAX` | maximum WS in the averaging period | m s-1 | `BERVO:0001372` Measured wind speed | base term + `Maximum` qualifier |
| MET_WIND | `W_SIGMA` | Standard deviation of vertical velocity fluctuations | m s-1 | `BERVO:0002272` Vertical wind velocity | base term + `Standard deviation` qualifier |
| MET_WIND | `ZL` | Monin-Obukhov Stability parameter | nondimensional | `BERVO:0002269` Monin-Obukhov stability parameter | synonym |
| PRODUCTS | `GPP` | Gross Primary Productivity | µmolCO2 m-2 s-1 | `BERVO:0001962` Gross primary production rate | synonym |
| PRODUCTS | `NEE` | Net Ecosystem Exchange | µmolCO2 m-2 s-1 | `BERVO:0002258` Net ecosystem exchange | synonym |
| PRODUCTS | `RECO` | Ecosystem Respiration | µmolCO2 m-2 s-1 | `BERVO:0001963` Ecosystem respiration flux | synonym |
| QC_FLAG | `FCH4_SSITC_TEST` | Results of the quality flagging for FCH4 according to Foken et al 2004, based on a combination of Steady State and Integral Turbulence Characteristics tests by Foken and Wichura (1996) (i.e., 0, 1, 2) | nondimensional | `BERVO:0002265` Steady state and integral turbulence characteristics test flag | synonym |
| QC_FLAG | `FC_SSITC_TEST` | Results of the quality flagging for FC according to Foken et al 2004, based on a combination of Steady State and Integral Turbulence Characteristics tests by Foken and Wichura (1996) (i.e., 0, 1, 2) | nondimensional | `BERVO:0002265` Steady state and integral turbulence characteristics test flag | synonym |
| QC_FLAG | `FN2O_SSITC_TEST` | Results of the quality flagging for FN2O according to Foken et al 2004, based on a combination of Steady State and Integral Turbulence Characteristics tests by Foken and Wichura (1996) (i.e., 0, 1, 2) | nondimensional | `BERVO:0002265` Steady state and integral turbulence characteristics test flag | synonym |
| QC_FLAG | `FNO2_SSITC_TEST` | Results of the quality flagging for FNO2 according to Foken et al 2004, based on a combination of Steady State and Integral Turbulence Characteristics tests by Foken and Wichura (1996) (i.e., 0, 1, 2) | nondimensional | `BERVO:0002265` Steady state and integral turbulence characteristics test flag | synonym |
| QC_FLAG | `FNO_SSITC_TEST` | Results of the quality flagging for FNO according to Foken et al 2004, based on a combination of Steady State and Integral Turbulence Characteristics tests by Foken and Wichura (1996) (i.e., 0, 1, 2) | nondimensional | `BERVO:0002265` Steady state and integral turbulence characteristics test flag | synonym |
| QC_FLAG | `FO3_SSITC_TEST` | Results of the quality flagging for FO3 according to Foken et al 2004, based on a combination of Steady State and Integral Turbulence Characteristics tests by Foken and Wichura (1996) (i.e., 0, 1, 2) | nondimensional | `BERVO:0002265` Steady state and integral turbulence characteristics test flag | synonym |
| QC_FLAG | `H_SSITC_TEST` | Results of the quality flagging for H according to Foken et al 2004, based on a combination of Steady State and Integral Turbulence Characteristics tests by Foken and Wichura (1996) (i.e., 0, 1, 2) | nondimensional | `BERVO:0002265` Steady state and integral turbulence characteristics test flag | synonym |
| QC_FLAG | `LE_SSITC_TEST` | Results of the quality flagging for LE according to Foken et al 2004, based on a combination of Steady State and Integral Turbulence Characteristics tests by Foken and Wichura (1996) (i.e., 0, 1, 2) | nondimensional | `BERVO:0002265` Steady state and integral turbulence characteristics test flag | synonym |
| QC_FLAG | `TAU_SSITC_TEST` | Results of the quality flagging for TAU according to Foken et al 2004, based on a combination of Steady State and Integral Turbulence Characteristics tests by Foken and Wichura (1996) (i.e., 0, 1, 2) | nondimensional | `BERVO:0002265` Steady state and integral turbulence characteristics test flag | synonym |
| TIMEKEEPING | `TIMESTAMP` | ISO timestamp – short format | YYYYMMDDHHMM | `BERVO:8000240` DateTime | recorded on the concept |
| TIMEKEEPING | `TIMESTAMP_END` | ISO timestamp end of averaging period - short format (12-digit integer) | YYYYMMDDHHMM | `BERVO:8000240` DateTime | recorded on the concept |
| TIMEKEEPING | `TIMESTAMP_START` | ISO timestamp start of averaging period - short format (12-digit integer) | YYYYMMDDHHMM | `BERVO:8000240` DateTime | recorded on the concept |

## Qualifiers

| Qualifier | BERVO term | Note |
| --- | --- | --- |
| `_PI` | `BERVO:8001087` Processed by site team | concept |
| `_QC` | `BERVO:8000563` Quality control flag | existing term |
| `_F` | `BERVO:8001086` Gap-filled | concept |
| `_IU` | — | not modelled: instrument units, an upload convention |
| `_H_V_R` | — | not modelled: relative position indices of a sensor at one site |
| `_H_V_A` | `BERVO:8000259` Mean | existing concept: average across replicate sensors |
| `_#` | — | not modelled: layer index of an aggregated profile |
| `_SD` | `BERVO:8000362` Standard deviation | existing concept: spread across replicate sensors |
| `_N` | `BERVO:8001088` Sample size | concept: number of replicate sensors averaged |

## FLUXNET FULLSET variables

### Concepts and base terms added

| Term | Parent | Describes |
| --- | --- | --- |
| `BERVO:8001089` Gap-filling method | Method |  |
| `BERVO:8001090` Marginal distribution sampling | Gap-filling method | FLUXNET FULLSET suffix: _MDS. |
| `BERVO:8001091` Reanalysis downscaling | Method | FLUXNET FULLSET suffix: _ERA, for values downscaled from the ERA reanalysis. |
| `BERVO:8001092` Flux partitioning method | Method |  |
| `BERVO:8001093` Nighttime flux partitioning | Flux partitioning method | FLUXNET FULLSET suffix: _NT. |
| `BERVO:8001094` Daytime flux partitioning | Flux partitioning method | FLUXNET FULLSET suffix: _DT. |
| `BERVO:8001095` Sundown respiration partitioning | Flux partitioning method | FLUXNET FULLSET suffix: _SR. |
| `BERVO:8001096` Energy balance closure correction | Method | FLUXNET FULLSET suffix: _CORR. |
| `BERVO:8001097` Constant friction velocity threshold | Threshold | FLUXNET FULLSET suffix: _CUT. |
| `BERVO:8001098` Variable friction velocity threshold | Threshold | FLUXNET FULLSET suffix: _VUT. |
| `BERVO:8001099` Random uncertainty | Error range | FLUXNET FULLSET suffix: _RANDUNC. |
| `BERVO:8001100` Joint uncertainty | Error range | FLUXNET FULLSET suffix: _JOINTUNC. |
| `BERVO:8001101` Percentile | Quantitative value | FLUXNET FULLSET suffixes: _XX (05, 16, 25, 50, 75, 84, 95) and _25, _75. |
| `BERVO:8001102` Reference ensemble member | Quantitative value | FLUXNET FULLSET suffix: _REF, chosen among the 40 estimates made with different friction velocity thresholds. |
| `BERVO:8001103` Daytime | Time | FLUXNET FULLSET suffix: _DAY. Flux processing counts as daytime the periods when the potential incoming shortwave radiation is above zero. |
| `BERVO:8001104` Nighttime | Time | FLUXNET FULLSET suffix: _NIGHT. Flux processing counts as nighttime the periods when the potential incoming shortwave radiation is zero. |
| `BERVO:0002323` Potential incoming shortwave radiation | Incoming radiation | FLUXNET FULLSET variable: SW_IN_POT. |
| `BERVO:0002324` Friction velocity threshold | Meteorological variable | FLUXNET FULLSET does not report the threshold itself; its constant and variable forms (_CUT, _VUT) and the percentile used (_USTAR50) qualify the NEE, GPP and RECO variables. |
| `BERVO:0002325` Energy balance closure correction factor | Surface flux variable | FLUXNET FULLSET reports the number of values used to compute it (EBC_CF_N) and the method used (EBC_CF_METHOD), and applies it in H_CORR and LE_CORR. |
| `BERVO:0002326` Nighttime flag | Flag data type | FLUXNET FULLSET variable: NIGHT. The code is not recorded as a synonym because it is also the label, symbol or synonym of another BERVO term. |

### Variables

232 of 232 FULLSET variables resolve to a base term and its qualifiers. A `_QC`
variable is a `Quality control flag` for the variable it names. The list was taken from
the FULLSET page, where 3 rows give time-resolution notes rather than
variable names; they are not counted. The same names serve every time resolution
(half-hourly to yearly), so they are listed once.

| Section | FLUXNET variable | Units | BERVO term | Qualifiers and concepts | Notes |
| --- | --- | --- | --- | --- | --- |
| Timekeeping | `TIMESTAMP` | YYYYMMDDHHMM | `BERVO:8000240` DateTime |  |  |
| Timekeeping | `TIMESTAMP_START` | YYYYMMDDHHMM | `BERVO:8000240` DateTime |  |  |
| Timekeeping | `TIMESTAMP_END` | YYYYMMDDHHMM | `BERVO:8000240` DateTime |  |  |
| Micrometeorological | `TA_F_MDS` | deg C | `BERVO:0001370` Air temperature | Gap-filled, Marginal distribution sampling |  |
| Micrometeorological | `TA_F_MDS_QC` | nondimensional | `BERVO:8000563` Quality control flag | Gap-filled, Marginal distribution sampling | flag for Air temperature |
| Micrometeorological | `TA_F_MDS_NIGHT` | deg C | `BERVO:0001370` Air temperature | Gap-filled, Marginal distribution sampling, Nighttime, Mean |  |
| Micrometeorological | `TA_F_MDS_NIGHT_SD` | deg C | `BERVO:0001370` Air temperature | Gap-filled, Marginal distribution sampling, Nighttime, Mean, Standard deviation |  |
| Micrometeorological | `TA_F_MDS_NIGHT_QC` | nondimensional | `BERVO:8000563` Quality control flag | Gap-filled, Marginal distribution sampling, Nighttime, Mean | flag for Air temperature |
| Micrometeorological | `TA_F_MDS_DAY` | deg C | `BERVO:0001370` Air temperature | Gap-filled, Marginal distribution sampling, Daytime, Mean |  |
| Micrometeorological | `TA_F_MDS_DAY_SD` | deg C | `BERVO:0001370` Air temperature | Gap-filled, Marginal distribution sampling, Daytime, Mean, Standard deviation |  |
| Micrometeorological | `TA_F_MDS_DAY_QC` | nondimensional | `BERVO:8000563` Quality control flag | Gap-filled, Marginal distribution sampling, Daytime, Mean | flag for Air temperature |
| Micrometeorological | `TA_ERA` | deg C | `BERVO:0001370` Air temperature | Reanalysis downscaling |  |
| Micrometeorological | `TA_ERA_NIGHT` | deg C | `BERVO:0001370` Air temperature | Reanalysis downscaling, Nighttime, Mean |  |
| Micrometeorological | `TA_ERA_NIGHT_SD` | deg C | `BERVO:0001370` Air temperature | Reanalysis downscaling, Nighttime, Mean, Standard deviation |  |
| Micrometeorological | `TA_ERA_DAY` | deg C | `BERVO:0001370` Air temperature | Reanalysis downscaling, Daytime, Mean |  |
| Micrometeorological | `TA_ERA_DAY_SD` | deg C | `BERVO:0001370` Air temperature | Reanalysis downscaling, Daytime, Mean, Standard deviation |  |
| Micrometeorological | `TA_F` | deg C | `BERVO:0001370` Air temperature | Gap-filled |  |
| Micrometeorological | `TA_F_QC` | nondimensional | `BERVO:8000563` Quality control flag | Gap-filled | flag for Air temperature |
| Micrometeorological | `TA_F_NIGHT` | deg C | `BERVO:0001370` Air temperature | Gap-filled, Nighttime, Mean |  |
| Micrometeorological | `TA_F_NIGHT_SD` | deg C | `BERVO:0001370` Air temperature | Gap-filled, Nighttime, Mean, Standard deviation |  |
| Micrometeorological | `TA_F_NIGHT_QC` | nondimensional | `BERVO:8000563` Quality control flag | Gap-filled, Nighttime, Mean | flag for Air temperature |
| Micrometeorological | `TA_F_DAY` | deg C | `BERVO:0001370` Air temperature | Gap-filled, Daytime, Mean |  |
| Micrometeorological | `TA_F_DAY_SD` | deg C | `BERVO:0001370` Air temperature | Gap-filled, Daytime, Mean, Standard deviation |  |
| Micrometeorological | `TA_F_DAY_QC` | nondimensional | `BERVO:8000563` Quality control flag | Gap-filled, Daytime, Mean | flag for Air temperature |
| Micrometeorological | `SW_IN_POT` | W m-2 | `BERVO:0002323` Potential incoming shortwave radiation |  |  |
| Micrometeorological | `SW_IN_F_MDS` | W m-2 | `BERVO:0001867` Incoming shortwave radiation | Gap-filled, Marginal distribution sampling |  |
| Micrometeorological | `SW_IN_F_MDS_QC` | nondimensional | `BERVO:8000563` Quality control flag | Gap-filled, Marginal distribution sampling | flag for Incoming shortwave radiation |
| Micrometeorological | `SW_IN_ERA` | W m-2 | `BERVO:0001867` Incoming shortwave radiation | Reanalysis downscaling |  |
| Micrometeorological | `SW_IN_F` | W m-2 | `BERVO:0001867` Incoming shortwave radiation | Gap-filled |  |
| Micrometeorological | `SW_IN_F_QC` | nondimensional | `BERVO:8000563` Quality control flag | Gap-filled | flag for Incoming shortwave radiation |
| Micrometeorological | `LW_IN_F_MDS` | W m-2 | `BERVO:0001380` Sky longwave radiation | Gap-filled, Marginal distribution sampling |  |
| Micrometeorological | `LW_IN_F_MDS_QC` | nondimensional | `BERVO:8000563` Quality control flag | Gap-filled, Marginal distribution sampling | flag for Sky longwave radiation |
| Micrometeorological | `LW_IN_ERA` | W m-2 | `BERVO:0001380` Sky longwave radiation | Reanalysis downscaling |  |
| Micrometeorological | `LW_IN_F` | W m-2 | `BERVO:0001380` Sky longwave radiation | Gap-filled |  |
| Micrometeorological | `LW_IN_F_QC` | nondimensional | `BERVO:8000563` Quality control flag | Gap-filled | flag for Sky longwave radiation |
| Micrometeorological | `LW_IN_JSB` | W m-2 | `BERVO:0001380` Sky longwave radiation |  | calculated with the JSBACH algorithm; no concept |
| Micrometeorological | `LW_IN_JSB_QC` | nondimensional | `BERVO:8000563` Quality control flag |  | flag for Sky longwave radiation; calculated with the JSBACH algorithm; no concept |
| Micrometeorological | `LW_IN_JSB_ERA` | W m-2 | `BERVO:0001380` Sky longwave radiation | Reanalysis downscaling | calculated with the JSBACH algorithm; no concept |
| Micrometeorological | `LW_IN_JSB_F` | W m-2 | `BERVO:0001380` Sky longwave radiation | Gap-filled | calculated with the JSBACH algorithm; no concept |
| Micrometeorological | `LW_IN_JSB_F_QC` | nondimensional | `BERVO:8000563` Quality control flag | Gap-filled | flag for Sky longwave radiation; calculated with the JSBACH algorithm; no concept |
| Micrometeorological | `VPD_F_MDS` | hPa | `BERVO:0001913` Vapor pressure deficit | Gap-filled, Marginal distribution sampling |  |
| Micrometeorological | `VPD_F_MDS_QC` | nondimensional | `BERVO:8000563` Quality control flag | Gap-filled, Marginal distribution sampling | flag for Vapor pressure deficit |
| Micrometeorological | `VPD_ERA` | hPa | `BERVO:0001913` Vapor pressure deficit | Reanalysis downscaling |  |
| Micrometeorological | `VPD_F` | hPa | `BERVO:0001913` Vapor pressure deficit | Gap-filled |  |
| Micrometeorological | `VPD_F_QC` | nondimensional | `BERVO:8000563` Quality control flag | Gap-filled | flag for Vapor pressure deficit |
| Micrometeorological | `PA` | kPa | `BERVO:0001375` Atmospheric pressure |  |  |
| Micrometeorological | `PA_ERA` | kPa | `BERVO:0001375` Atmospheric pressure | Reanalysis downscaling |  |
| Micrometeorological | `PA_F` | kPa | `BERVO:0001375` Atmospheric pressure | Gap-filled |  |
| Micrometeorological | `PA_F_QC` | nondimensional | `BERVO:8000563` Quality control flag | Gap-filled | flag for Atmospheric pressure |
| Micrometeorological | `P` | mm | `BERVO:0001908` Precipitation amount |  |  |
| Micrometeorological | `P_ERA` | mm | `BERVO:0001908` Precipitation amount | Reanalysis downscaling |  |
| Micrometeorological | `P_F` | mm | `BERVO:0001908` Precipitation amount | Gap-filled |  |
| Micrometeorological | `P_F_QC` | nondimensional | `BERVO:8000563` Quality control flag | Gap-filled | flag for Precipitation amount |
| Micrometeorological | `WS` | m s-1 | `BERVO:0001372` Measured wind speed |  |  |
| Micrometeorological | `WS_ERA` | m s-1 | `BERVO:0001372` Measured wind speed | Reanalysis downscaling |  |
| Micrometeorological | `WS_F` | m s-1 | `BERVO:0001372` Measured wind speed | Gap-filled |  |
| Micrometeorological | `WS_F_QC` | nondimensional | `BERVO:8000563` Quality control flag | Gap-filled | flag for Measured wind speed |
| Micrometeorological | `WD` | Decimal degrees | `BERVO:0001916` Near-surface wind direction |  |  |
| Micrometeorological | `RH` | % | `BERVO:0001910` Air relative humidity |  |  |
| Micrometeorological | `USTAR` | m s-1 | `BERVO:0001906` Friction velocity |  |  |
| Micrometeorological | `USTAR_QC` | nondimensional | `BERVO:8000563` Quality control flag |  | flag for Friction velocity |
| Micrometeorological | `NETRAD` | W m-2 | `BERVO:0001932` Net radiation |  |  |
| Micrometeorological | `NETRAD_QC` | nondimensional | `BERVO:8000563` Quality control flag |  | flag for Net radiation |
| Micrometeorological | `PPFD_IN` | µmolPhoton m-2 s-1 | `BERVO:0001927` Photosynthetic photon flux density |  |  |
| Micrometeorological | `PPFD_IN_QC` | nondimensional | `BERVO:8000563` Quality control flag |  | flag for Photosynthetic photon flux density |
| Micrometeorological | `PPFD_DIF` | µmolPhoton m-2 s-1 | `BERVO:0001405` Diffuse photosynthetically active radiation |  |  |
| Micrometeorological | `PPFD_DIF_QC` | nondimensional | `BERVO:8000563` Quality control flag |  | flag for Diffuse photosynthetically active radiation |
| Micrometeorological | `PPFD_OUT` | µmolPhoton m-2 s-1 | `BERVO:0001937` Outgoing photosynthetically active radiation |  |  |
| Micrometeorological | `PPFD_OUT_QC` | nondimensional | `BERVO:8000563` Quality control flag |  | flag for Outgoing photosynthetically active radiation |
| Micrometeorological | `SW_DIF` | W m-2 | `BERVO:0001403` Diffuse shortwave radiation |  |  |
| Micrometeorological | `SW_DIF_QC` | nondimensional | `BERVO:8000563` Quality control flag |  | flag for Diffuse shortwave radiation |
| Micrometeorological | `SW_OUT` | W m-2 | `BERVO:0001938` Outgoing shortwave radiation |  |  |
| Micrometeorological | `SW_OUT_QC` | nondimensional | `BERVO:8000563` Quality control flag |  | flag for Outgoing shortwave radiation |
| Micrometeorological | `LW_OUT` | W m-2 | `BERVO:0001936` Outgoing longwave radiation |  |  |
| Micrometeorological | `LW_OUT_QC` | nondimensional | `BERVO:8000563` Quality control flag |  | flag for Outgoing longwave radiation |
| Micrometeorological | `CO2_F_MDS` | umolCO2 mol-1 | `BERVO:0002226` Carbon dioxide mole fraction in wet air | Gap-filled, Marginal distribution sampling |  |
| Micrometeorological | `CO2_F_MDS_QC` | nondimensional | `BERVO:8000563` Quality control flag | Gap-filled, Marginal distribution sampling | flag for Carbon dioxide mole fraction in wet air |
| Micrometeorological | `TS_F_MDS_#` | deg C | `BERVO:0001477` Soil temperature | Gap-filled, Marginal distribution sampling | layer index, deepest last; not modelled |
| Micrometeorological | `TS_F_MDS_#_QC` | nondimensional | `BERVO:8000563` Quality control flag | Gap-filled, Marginal distribution sampling | flag for Soil temperature; layer index, deepest last; not modelled |
| Micrometeorological | `SWC_F_MDS_#` | % | `BERVO:0001743` Volumetric water content | Gap-filled, Marginal distribution sampling | layer index, deepest last; not modelled |
| Micrometeorological | `SWC_F_MDS_#_QC` | nondimensional | `BERVO:8000563` Quality control flag | Gap-filled, Marginal distribution sampling | flag for Volumetric water content; layer index, deepest last; not modelled |
| Energy Processing | `G_F_MDS` | W m-2 | `BERVO:0002257` Soil heat flux at measurement depth | Gap-filled, Marginal distribution sampling |  |
| Energy Processing | `G_F_MDS_QC` | nondimensional | `BERVO:8000563` Quality control flag | Gap-filled, Marginal distribution sampling | flag for Soil heat flux at measurement depth |
| Energy Processing | `LE_F_MDS` | W m-2 | `BERVO:0001953` Latent heat flux | Gap-filled, Marginal distribution sampling |  |
| Energy Processing | `LE_F_MDS_QC` | nondimensional | `BERVO:8000563` Quality control flag | Gap-filled, Marginal distribution sampling | flag for Latent heat flux |
| Energy Processing | `LE_CORR` | W m-2 | `BERVO:0001953` Latent heat flux | Energy balance closure correction |  |
| Energy Processing | `LE_CORR_25` | W m-2 | `BERVO:0001953` Latent heat flux | Energy balance closure correction, Percentile | 25th percentile |
| Energy Processing | `LE_CORR_75` | W m-2 | `BERVO:0001953` Latent heat flux | Energy balance closure correction, Percentile | 75th percentile |
| Energy Processing | `LE_RANDUNC` | W m-2 | `BERVO:0001953` Latent heat flux | Random uncertainty |  |
| Energy Processing | `LE_RANDUNC_METHOD` | nondimensional | `BERVO:0001953` Latent heat flux | Random uncertainty, Method |  |
| Energy Processing | `LE_RANDUNC_N` | nondimensional | `BERVO:0001953` Latent heat flux | Random uncertainty, Sample size |  |
| Energy Processing | `LE_CORR_JOINTUNC` | W m-2 | `BERVO:0001953` Latent heat flux | Energy balance closure correction, Joint uncertainty |  |
| Energy Processing | `H_F_MDS` | W m-2 | `BERVO:0001954` Sensible heat flux | Gap-filled, Marginal distribution sampling |  |
| Energy Processing | `H_F_MDS_QC` | nondimensional | `BERVO:8000563` Quality control flag | Gap-filled, Marginal distribution sampling | flag for Sensible heat flux |
| Energy Processing | `H_CORR` | W m-2 | `BERVO:0001954` Sensible heat flux | Energy balance closure correction |  |
| Energy Processing | `H_CORR_25` | W m-2 | `BERVO:0001954` Sensible heat flux | Energy balance closure correction, Percentile | 25th percentile |
| Energy Processing | `H_CORR_75` | W m-2 | `BERVO:0001954` Sensible heat flux | Energy balance closure correction, Percentile | 75th percentile |
| Energy Processing | `H_RANDUNC` | W m-2 | `BERVO:0001954` Sensible heat flux | Random uncertainty |  |
| Energy Processing | `H_RANDUNC_METHOD` | nondimensional | `BERVO:0001954` Sensible heat flux | Random uncertainty, Method |  |
| Energy Processing | `H_RANDUNC_N` | nondimensional | `BERVO:0001954` Sensible heat flux | Random uncertainty, Sample size |  |
| Energy Processing | `H_CORR_JOINTUNC` | W m-2 | `BERVO:0001954` Sensible heat flux | Energy balance closure correction, Joint uncertainty |  |
| Energy Processing | `EBC_CF_N` | nondimensional | `BERVO:0002325` Energy balance closure correction factor | Sample size | number of values used to compute the factor |
| Energy Processing | `EBC_CF_METHOD` | nondimensional | `BERVO:0002325` Energy balance closure correction factor | Method |  |
| Net Ecosystem Exchange | `NIGHT` | nondimensional | `BERVO:0002326` Nighttime flag |  |  |
| Net Ecosystem Exchange | `NIGHT_D` | nondimensional | none | Count, Nighttime | number of half-hours in the period |
| Net Ecosystem Exchange | `DAY_D` | nondimensional | none | Count, Daytime | number of half-hours in the period |
| Net Ecosystem Exchange | `NIGHT_RANDUNC_N` | nondimensional | `BERVO:0002258` Net ecosystem exchange | Nighttime, Random uncertainty, Sample size |  |
| Net Ecosystem Exchange | `DAY_RANDUNC_N` | nondimensional | `BERVO:0002258` Net ecosystem exchange | Daytime, Random uncertainty, Sample size |  |
| Net Ecosystem Exchange | `NEE_CUT_REF` | umolCO2 m-2 s-1 | `BERVO:0002258` Net ecosystem exchange | Constant friction velocity threshold, Reference ensemble member |  |
| Net Ecosystem Exchange | `NEE_VUT_REF` | umolCO2 m-2 s-1 | `BERVO:0002258` Net ecosystem exchange | Variable friction velocity threshold, Reference ensemble member |  |
| Net Ecosystem Exchange | `NEE_CUT_REF_QC` | nondimensional | `BERVO:8000563` Quality control flag | Constant friction velocity threshold, Reference ensemble member | flag for Net ecosystem exchange |
| Net Ecosystem Exchange | `NEE_VUT_REF_QC` | nondimensional | `BERVO:8000563` Quality control flag | Variable friction velocity threshold, Reference ensemble member | flag for Net ecosystem exchange |
| Net Ecosystem Exchange | `NEE_CUT_REF_RANDUNC` | umolCO2 m-2 s-1 | `BERVO:0002258` Net ecosystem exchange | Constant friction velocity threshold, Reference ensemble member, Random uncertainty |  |
| Net Ecosystem Exchange | `NEE_VUT_REF_RANDUNC` | umolCO2 m-2 s-1 | `BERVO:0002258` Net ecosystem exchange | Variable friction velocity threshold, Reference ensemble member, Random uncertainty |  |
| Net Ecosystem Exchange | `NEE_CUT_REF_RANDUNC_METHOD` | nondimensional | `BERVO:0002258` Net ecosystem exchange | Constant friction velocity threshold, Reference ensemble member, Random uncertainty, Method |  |
| Net Ecosystem Exchange | `NEE_VUT_REF_RANDUNC_METHOD` | nondimensional | `BERVO:0002258` Net ecosystem exchange | Variable friction velocity threshold, Reference ensemble member, Random uncertainty, Method |  |
| Net Ecosystem Exchange | `NEE_CUT_REF_RANDUNC_N` | nondimensional | `BERVO:0002258` Net ecosystem exchange | Constant friction velocity threshold, Reference ensemble member, Random uncertainty, Sample size |  |
| Net Ecosystem Exchange | `NEE_VUT_REF_RANDUNC_N` | nondimensional | `BERVO:0002258` Net ecosystem exchange | Variable friction velocity threshold, Reference ensemble member, Random uncertainty, Sample size |  |
| Net Ecosystem Exchange | `NEE_CUT_REF_JOINTUNC` | umolCO2 m-2 s-1 | `BERVO:0002258` Net ecosystem exchange | Constant friction velocity threshold, Reference ensemble member, Joint uncertainty |  |
| Net Ecosystem Exchange | `NEE_VUT_REF_JOINTUNC` | umolCO2 m-2 s-1 | `BERVO:0002258` Net ecosystem exchange | Variable friction velocity threshold, Reference ensemble member, Joint uncertainty |  |
| Net Ecosystem Exchange | `NEE_CUT_USTAR50` | umolCO2 m-2 s-1 | `BERVO:0002258` Net ecosystem exchange | Constant friction velocity threshold, Median, Friction velocity threshold |  |
| Net Ecosystem Exchange | `NEE_VUT_USTAR50` | umolCO2 m-2 s-1 | `BERVO:0002258` Net ecosystem exchange | Variable friction velocity threshold, Median, Friction velocity threshold |  |
| Net Ecosystem Exchange | `NEE_CUT_USTAR50_QC` | nondimensional | `BERVO:8000563` Quality control flag | Constant friction velocity threshold, Median, Friction velocity threshold | flag for Net ecosystem exchange |
| Net Ecosystem Exchange | `NEE_VUT_USTAR50_QC` | nondimensional | `BERVO:8000563` Quality control flag | Variable friction velocity threshold, Median, Friction velocity threshold | flag for Net ecosystem exchange |
| Net Ecosystem Exchange | `NEE_CUT_USTAR50_RANDUNC` | umolCO2 m-2 s-1 | `BERVO:0002258` Net ecosystem exchange | Constant friction velocity threshold, Median, Friction velocity threshold, Random uncertainty |  |
| Net Ecosystem Exchange | `NEE_VUT_USTAR50_RANDUNC` | umolCO2 m-2 s-1 | `BERVO:0002258` Net ecosystem exchange | Variable friction velocity threshold, Median, Friction velocity threshold, Random uncertainty |  |
| Net Ecosystem Exchange | `NEE_CUT_USTAR50_RANDUNC_METHOD` | nondimensional | `BERVO:0002258` Net ecosystem exchange | Constant friction velocity threshold, Median, Friction velocity threshold, Random uncertainty, Method |  |
| Net Ecosystem Exchange | `NEE_VUT_USTAR50_RANDUNC_METHOD` | nondimensional | `BERVO:0002258` Net ecosystem exchange | Variable friction velocity threshold, Median, Friction velocity threshold, Random uncertainty, Method |  |
| Net Ecosystem Exchange | `NEE_CUT_USTAR50_RANDUNC_N` | nondimensional | `BERVO:0002258` Net ecosystem exchange | Constant friction velocity threshold, Median, Friction velocity threshold, Random uncertainty, Sample size |  |
| Net Ecosystem Exchange | `NEE_VUT_USTAR50_RANDUNC_N` | nondimensional | `BERVO:0002258` Net ecosystem exchange | Variable friction velocity threshold, Median, Friction velocity threshold, Random uncertainty, Sample size |  |
| Net Ecosystem Exchange | `NEE_CUT_USTAR50_JOINTUNC` | umolCO2 m-2 s-1 | `BERVO:0002258` Net ecosystem exchange | Constant friction velocity threshold, Median, Friction velocity threshold, Joint uncertainty |  |
| Net Ecosystem Exchange | `NEE_VUT_USTAR50_JOINTUNC` | umolCO2 m-2 s-1 | `BERVO:0002258` Net ecosystem exchange | Variable friction velocity threshold, Median, Friction velocity threshold, Joint uncertainty |  |
| Net Ecosystem Exchange | `NEE_CUT_MEAN` | umolCO2 m-2 s-1 | `BERVO:0002258` Net ecosystem exchange | Constant friction velocity threshold, Mean |  |
| Net Ecosystem Exchange | `NEE_VUT_MEAN` | umolCO2 m-2 s-1 | `BERVO:0002258` Net ecosystem exchange | Variable friction velocity threshold, Mean |  |
| Net Ecosystem Exchange | `NEE_CUT_MEAN_QC` | nondimensional | `BERVO:8000563` Quality control flag | Constant friction velocity threshold, Mean | flag for Net ecosystem exchange |
| Net Ecosystem Exchange | `NEE_VUT_MEAN_QC` | nondimensional | `BERVO:8000563` Quality control flag | Variable friction velocity threshold, Mean | flag for Net ecosystem exchange |
| Net Ecosystem Exchange | `NEE_CUT_SE` | umolCO2 m-2 s-1 | `BERVO:0002258` Net ecosystem exchange | Constant friction velocity threshold, Standard error |  |
| Net Ecosystem Exchange | `NEE_VUT_SE` | umolCO2 m-2 s-1 | `BERVO:0002258` Net ecosystem exchange | Variable friction velocity threshold, Standard error |  |
| Net Ecosystem Exchange | `NEE_CUT_XX` | umolCO2 m-2 s-1 | `BERVO:0002258` Net ecosystem exchange | Constant friction velocity threshold, Percentile |  |
| Net Ecosystem Exchange | `NEE_VUT_XX` | umolCO2 m-2 s-1 | `BERVO:0002258` Net ecosystem exchange | Variable friction velocity threshold, Percentile |  |
| Net Ecosystem Exchange | `NEE_CUT_XX_QC` | nondimensional | `BERVO:8000563` Quality control flag | Constant friction velocity threshold, Percentile | flag for Net ecosystem exchange |
| Net Ecosystem Exchange | `NEE_VUT_XX_QC` | nondimensional | `BERVO:8000563` Quality control flag | Variable friction velocity threshold, Percentile | flag for Net ecosystem exchange |
| Net Ecosystem Exchange | `NEE_CUT_REF_NIGHT` | umolCO2 m-2 s-1 | `BERVO:0002258` Net ecosystem exchange | Constant friction velocity threshold, Reference ensemble member, Nighttime, Mean |  |
| Net Ecosystem Exchange | `NEE_VUT_REF_NIGHT` | umolCO2 m-2 s-1 | `BERVO:0002258` Net ecosystem exchange | Variable friction velocity threshold, Reference ensemble member, Nighttime, Mean |  |
| Net Ecosystem Exchange | `NEE_CUT_REF_NIGHT_SD` | umolCO2 m-2 s-1 | `BERVO:0002258` Net ecosystem exchange | Constant friction velocity threshold, Reference ensemble member, Nighttime, Mean, Standard deviation |  |
| Net Ecosystem Exchange | `NEE_VUT_REF_NIGHT_SD` | umolCO2 m-2 s-1 | `BERVO:0002258` Net ecosystem exchange | Variable friction velocity threshold, Reference ensemble member, Nighttime, Mean, Standard deviation |  |
| Net Ecosystem Exchange | `NEE_CUT_REF_NIGHT_QC` | nondimensional | `BERVO:8000563` Quality control flag | Constant friction velocity threshold, Reference ensemble member, Nighttime, Mean | flag for Net ecosystem exchange |
| Net Ecosystem Exchange | `NEE_VUT_REF_NIGHT_QC` | nondimensional | `BERVO:8000563` Quality control flag | Variable friction velocity threshold, Reference ensemble member, Nighttime, Mean | flag for Net ecosystem exchange |
| Net Ecosystem Exchange | `NEE_CUT_REF_NIGHT_RANDUNC` | umolCO2 m-2 s-1 | `BERVO:0002258` Net ecosystem exchange | Constant friction velocity threshold, Reference ensemble member, Nighttime, Mean, Random uncertainty |  |
| Net Ecosystem Exchange | `NEE_VUT_REF_NIGHT_RANDUNC` | umolCO2 m-2 s-1 | `BERVO:0002258` Net ecosystem exchange | Variable friction velocity threshold, Reference ensemble member, Nighttime, Mean, Random uncertainty |  |
| Net Ecosystem Exchange | `NEE_CUT_REF_NIGHT_JOINTUNC` | umolCO2 m-2 s-1 | `BERVO:0002258` Net ecosystem exchange | Constant friction velocity threshold, Reference ensemble member, Nighttime, Mean, Joint uncertainty |  |
| Net Ecosystem Exchange | `NEE_VUT_REF_NIGHT_JOINTUNC` | umolCO2 m-2 s-1 | `BERVO:0002258` Net ecosystem exchange | Variable friction velocity threshold, Reference ensemble member, Nighttime, Mean, Joint uncertainty |  |
| Net Ecosystem Exchange | `NEE_CUT_REF_DAY` | umolCO2 m-2 s-1 | `BERVO:0002258` Net ecosystem exchange | Constant friction velocity threshold, Reference ensemble member, Daytime, Mean |  |
| Net Ecosystem Exchange | `NEE_VUT_REF_DAY` | umolCO2 m-2 s-1 | `BERVO:0002258` Net ecosystem exchange | Variable friction velocity threshold, Reference ensemble member, Daytime, Mean |  |
| Net Ecosystem Exchange | `NEE_CUT_REF_DAY_SD` | umolCO2 m-2 s-1 | `BERVO:0002258` Net ecosystem exchange | Constant friction velocity threshold, Reference ensemble member, Daytime, Mean, Standard deviation |  |
| Net Ecosystem Exchange | `NEE_VUT_REF_DAY_SD` | umolCO2 m-2 s-1 | `BERVO:0002258` Net ecosystem exchange | Variable friction velocity threshold, Reference ensemble member, Daytime, Mean, Standard deviation |  |
| Net Ecosystem Exchange | `NEE_CUT_REF_DAY_QC` | nondimensional | `BERVO:8000563` Quality control flag | Constant friction velocity threshold, Reference ensemble member, Daytime, Mean | flag for Net ecosystem exchange |
| Net Ecosystem Exchange | `NEE_VUT_REF_DAY_QC` | nondimensional | `BERVO:8000563` Quality control flag | Variable friction velocity threshold, Reference ensemble member, Daytime, Mean | flag for Net ecosystem exchange |
| Net Ecosystem Exchange | `NEE_CUT_REF_DAY_RANDUNC` | umolCO2 m-2 s-1 | `BERVO:0002258` Net ecosystem exchange | Constant friction velocity threshold, Reference ensemble member, Daytime, Mean, Random uncertainty |  |
| Net Ecosystem Exchange | `NEE_VUT_REF_DAY_RANDUNC` | umolCO2 m-2 s-1 | `BERVO:0002258` Net ecosystem exchange | Variable friction velocity threshold, Reference ensemble member, Daytime, Mean, Random uncertainty |  |
| Net Ecosystem Exchange | `NEE_CUT_REF_DAY_JOINTUNC` | umolCO2 m-2 s-1 | `BERVO:0002258` Net ecosystem exchange | Constant friction velocity threshold, Reference ensemble member, Daytime, Mean, Joint uncertainty |  |
| Net Ecosystem Exchange | `NEE_VUT_REF_DAY_JOINTUNC` | umolCO2 m-2 s-1 | `BERVO:0002258` Net ecosystem exchange | Variable friction velocity threshold, Reference ensemble member, Daytime, Mean, Joint uncertainty |  |
| Net Ecosystem Exchange | `NEE_CUT_USTAR50_NIGHT` | umolCO2 m-2 s-1 | `BERVO:0002258` Net ecosystem exchange | Constant friction velocity threshold, Median, Friction velocity threshold, Nighttime, Mean |  |
| Net Ecosystem Exchange | `NEE_VUT_USTAR50_NIGHT` | umolCO2 m-2 s-1 | `BERVO:0002258` Net ecosystem exchange | Variable friction velocity threshold, Median, Friction velocity threshold, Nighttime, Mean |  |
| Net Ecosystem Exchange | `NEE_CUT_USTAR50_NIGHT_SD` | umolCO2 m-2 s-1 | `BERVO:0002258` Net ecosystem exchange | Constant friction velocity threshold, Median, Friction velocity threshold, Nighttime, Mean, Standard deviation |  |
| Net Ecosystem Exchange | `NEE_VUT_USTAR50_NIGHT_SD` | umolCO2 m-2 s-1 | `BERVO:0002258` Net ecosystem exchange | Variable friction velocity threshold, Median, Friction velocity threshold, Nighttime, Mean, Standard deviation |  |
| Net Ecosystem Exchange | `NEE_CUT_USTAR50_NIGHT_QC` | nondimensional | `BERVO:8000563` Quality control flag | Constant friction velocity threshold, Median, Friction velocity threshold, Nighttime, Mean | flag for Net ecosystem exchange |
| Net Ecosystem Exchange | `NEE_VUT_USTAR50_NIGHT_QC` | nondimensional | `BERVO:8000563` Quality control flag | Variable friction velocity threshold, Median, Friction velocity threshold, Nighttime, Mean | flag for Net ecosystem exchange |
| Net Ecosystem Exchange | `NEE_CUT_USTAR50_NIGHT_RANDUNC` | umolCO2 m-2 s-1 | `BERVO:0002258` Net ecosystem exchange | Constant friction velocity threshold, Median, Friction velocity threshold, Nighttime, Mean, Random uncertainty |  |
| Net Ecosystem Exchange | `NEE_VUT_USTAR50_NIGHT_RANDUNC` | umolCO2 m-2 s-1 | `BERVO:0002258` Net ecosystem exchange | Variable friction velocity threshold, Median, Friction velocity threshold, Nighttime, Mean, Random uncertainty |  |
| Net Ecosystem Exchange | `NEE_CUT_USTAR50_NIGHT_JOINTUNC` | umolCO2 m-2 s-1 | `BERVO:0002258` Net ecosystem exchange | Constant friction velocity threshold, Median, Friction velocity threshold, Nighttime, Mean, Joint uncertainty |  |
| Net Ecosystem Exchange | `NEE_VUT_USTAR50_NIGHT_JOINTUNC` | umolCO2 m-2 s-1 | `BERVO:0002258` Net ecosystem exchange | Variable friction velocity threshold, Median, Friction velocity threshold, Nighttime, Mean, Joint uncertainty |  |
| Net Ecosystem Exchange | `NEE_CUT_USTAR50_DAY` | umolCO2 m-2 s-1 | `BERVO:0002258` Net ecosystem exchange | Constant friction velocity threshold, Median, Friction velocity threshold, Daytime, Mean |  |
| Net Ecosystem Exchange | `NEE_VUT_USTAR50_DAY` | umolCO2 m-2 s-1 | `BERVO:0002258` Net ecosystem exchange | Variable friction velocity threshold, Median, Friction velocity threshold, Daytime, Mean |  |
| Net Ecosystem Exchange | `NEE_CUT_USTAR50_DAY_SD` | umolCO2 m-2 s-1 | `BERVO:0002258` Net ecosystem exchange | Constant friction velocity threshold, Median, Friction velocity threshold, Daytime, Mean, Standard deviation |  |
| Net Ecosystem Exchange | `NEE_VUT_USTAR50_DAY_SD` | umolCO2 m-2 s-1 | `BERVO:0002258` Net ecosystem exchange | Variable friction velocity threshold, Median, Friction velocity threshold, Daytime, Mean, Standard deviation |  |
| Net Ecosystem Exchange | `NEE_CUT_USTAR50_DAY_QC` | nondimensional | `BERVO:8000563` Quality control flag | Constant friction velocity threshold, Median, Friction velocity threshold, Daytime, Mean | flag for Net ecosystem exchange |
| Net Ecosystem Exchange | `NEE_VUT_USTAR50_DAY_QC` | nondimensional | `BERVO:8000563` Quality control flag | Variable friction velocity threshold, Median, Friction velocity threshold, Daytime, Mean | flag for Net ecosystem exchange |
| Net Ecosystem Exchange | `NEE_CUT_USTAR50_DAY_RANDUNC` | umolCO2 m-2 s-1 | `BERVO:0002258` Net ecosystem exchange | Constant friction velocity threshold, Median, Friction velocity threshold, Daytime, Mean, Random uncertainty |  |
| Net Ecosystem Exchange | `NEE_VUT_USTAR50_DAY_RANDUNC` | umolCO2 m-2 s-1 | `BERVO:0002258` Net ecosystem exchange | Variable friction velocity threshold, Median, Friction velocity threshold, Daytime, Mean, Random uncertainty |  |
| Net Ecosystem Exchange | `NEE_CUT_USTAR50_DAY_JOINTUNC` | umolCO2 m-2 s-1 | `BERVO:0002258` Net ecosystem exchange | Constant friction velocity threshold, Median, Friction velocity threshold, Daytime, Mean, Joint uncertainty |  |
| Net Ecosystem Exchange | `NEE_VUT_USTAR50_DAY_JOINTUNC` | umolCO2 m-2 s-1 | `BERVO:0002258` Net ecosystem exchange | Variable friction velocity threshold, Median, Friction velocity threshold, Daytime, Mean, Joint uncertainty |  |
| Net Ecosystem Exchange | `NEE_CUT_XX_NIGHT` | umolCO2 m-2 s-1 | `BERVO:0002258` Net ecosystem exchange | Constant friction velocity threshold, Percentile, Nighttime, Mean |  |
| Net Ecosystem Exchange | `NEE_VUT_XX_NIGHT` | umolCO2 m-2 s-1 | `BERVO:0002258` Net ecosystem exchange | Variable friction velocity threshold, Percentile, Nighttime, Mean |  |
| Net Ecosystem Exchange | `NEE_CUT_XX_NIGHT_QC` | nondimensional | `BERVO:8000563` Quality control flag | Constant friction velocity threshold, Percentile, Nighttime, Mean | flag for Net ecosystem exchange |
| Net Ecosystem Exchange | `NEE_VUT_XX_NIGHT_QC` | nondimensional | `BERVO:8000563` Quality control flag | Variable friction velocity threshold, Percentile, Nighttime, Mean | flag for Net ecosystem exchange |
| Net Ecosystem Exchange | `NEE_CUT_XX_DAY` | umolCO2 m-2 s-1 | `BERVO:0002258` Net ecosystem exchange | Constant friction velocity threshold, Percentile, Daytime, Mean |  |
| Net Ecosystem Exchange | `NEE_VUT_XX_DAY` | umolCO2 m-2 s-1 | `BERVO:0002258` Net ecosystem exchange | Variable friction velocity threshold, Percentile, Daytime, Mean |  |
| Net Ecosystem Exchange | `NEE_CUT_XX_DAY_QC` | nondimensional | `BERVO:8000563` Quality control flag | Constant friction velocity threshold, Percentile, Daytime, Mean | flag for Net ecosystem exchange |
| Net Ecosystem Exchange | `NEE_VUT_XX_DAY_QC` | nondimensional | `BERVO:8000563` Quality control flag | Variable friction velocity threshold, Percentile, Daytime, Mean | flag for Net ecosystem exchange |
| Nighttime | `RECO_NT_VUT_REF` | umolCO2 m-2 s-1 | `BERVO:0001963` Ecosystem respiration flux | Nighttime flux partitioning, Variable friction velocity threshold, Reference ensemble member |  |
| Nighttime | `RECO_NT_VUT_USTAR50` | umolCO2 m-2 s-1 | `BERVO:0001963` Ecosystem respiration flux | Nighttime flux partitioning, Variable friction velocity threshold, Median, Friction velocity threshold |  |
| Nighttime | `RECO_NT_VUT_MEAN` | umolCO2 m-2 s-1 | `BERVO:0001963` Ecosystem respiration flux | Nighttime flux partitioning, Variable friction velocity threshold, Mean |  |
| Nighttime | `RECO_NT_VUT_SE` | umolCO2 m-2 s-1 | `BERVO:0001963` Ecosystem respiration flux | Nighttime flux partitioning, Variable friction velocity threshold, Standard error |  |
| Nighttime | `RECO_NT_VUT_XX` | umolCO2 m-2 s-1 | `BERVO:0001963` Ecosystem respiration flux | Nighttime flux partitioning, Variable friction velocity threshold, Percentile |  |
| Nighttime | `RECO_NT_CUT_REF` | umolCO2 m-2 s-1 | `BERVO:0001963` Ecosystem respiration flux | Nighttime flux partitioning, Constant friction velocity threshold, Reference ensemble member |  |
| Nighttime | `RECO_NT_CUT_USTAR50` | umolCO2 m-2 s-1 | `BERVO:0001963` Ecosystem respiration flux | Nighttime flux partitioning, Constant friction velocity threshold, Median, Friction velocity threshold |  |
| Nighttime | `RECO_NT_CUT_MEAN` | umolCO2 m-2 s-1 | `BERVO:0001963` Ecosystem respiration flux | Nighttime flux partitioning, Constant friction velocity threshold, Mean |  |
| Nighttime | `RECO_NT_CUT_SE` | umolCO2 m-2 s-1 | `BERVO:0001963` Ecosystem respiration flux | Nighttime flux partitioning, Constant friction velocity threshold, Standard error |  |
| Nighttime | `RECO_NT_CUT_XX` | umolCO2 m-2 s-1 | `BERVO:0001963` Ecosystem respiration flux | Nighttime flux partitioning, Constant friction velocity threshold, Percentile |  |
| Nighttime | `GPP_NT_VUT_REF` | umolCO2 m-2 s-1 | `BERVO:0001962` Gross primary production rate | Nighttime flux partitioning, Variable friction velocity threshold, Reference ensemble member |  |
| Nighttime | `GPP_NT_VUT_USTAR50` | umolCO2 m-2 s-1 | `BERVO:0001962` Gross primary production rate | Nighttime flux partitioning, Variable friction velocity threshold, Median, Friction velocity threshold |  |
| Nighttime | `GPP_NT_VUT_MEAN` | umolCO2 m-2 s-1 | `BERVO:0001962` Gross primary production rate | Nighttime flux partitioning, Variable friction velocity threshold, Mean |  |
| Nighttime | `GPP_NT_VUT_SE` | umolCO2 m-2 s-1 | `BERVO:0001962` Gross primary production rate | Nighttime flux partitioning, Variable friction velocity threshold, Standard error |  |
| Nighttime | `GPP_NT_VUT_XX` | umolCO2 m-2 s-1 | `BERVO:0001962` Gross primary production rate | Nighttime flux partitioning, Variable friction velocity threshold, Percentile |  |
| Nighttime | `GPP_NT_CUT_REF` | umolCO2 m-2 s-1 | `BERVO:0001962` Gross primary production rate | Nighttime flux partitioning, Constant friction velocity threshold, Reference ensemble member |  |
| Nighttime | `GPP_NT_CUT_USTAR50` | umolCO2 m-2 s-1 | `BERVO:0001962` Gross primary production rate | Nighttime flux partitioning, Constant friction velocity threshold, Median, Friction velocity threshold |  |
| Nighttime | `GPP_NT_CUT_MEAN` | umolCO2 m-2 s-1 | `BERVO:0001962` Gross primary production rate | Nighttime flux partitioning, Constant friction velocity threshold, Mean |  |
| Nighttime | `GPP_NT_CUT_SE` | umolCO2 m-2 s-1 | `BERVO:0001962` Gross primary production rate | Nighttime flux partitioning, Constant friction velocity threshold, Standard error |  |
| Nighttime | `GPP_NT_CUT_XX` | umolCO2 m-2 s-1 | `BERVO:0001962` Gross primary production rate | Nighttime flux partitioning, Constant friction velocity threshold, Percentile |  |
| Daytime | `RECO_DT_VUT_REF` | umolCO2 m-2 s-1 | `BERVO:0001963` Ecosystem respiration flux | Daytime flux partitioning, Variable friction velocity threshold, Reference ensemble member |  |
| Daytime | `RECO_DT_VUT_USTAR50` | umolCO2 m-2 s-1 | `BERVO:0001963` Ecosystem respiration flux | Daytime flux partitioning, Variable friction velocity threshold, Median, Friction velocity threshold |  |
| Daytime | `RECO_DT_VUT_MEAN` | umolCO2 m-2 s-1 | `BERVO:0001963` Ecosystem respiration flux | Daytime flux partitioning, Variable friction velocity threshold, Mean |  |
| Daytime | `RECO_DT_VUT_SE` | umolCO2 m-2 s-1 | `BERVO:0001963` Ecosystem respiration flux | Daytime flux partitioning, Variable friction velocity threshold, Standard error |  |
| Daytime | `RECO_DT_VUT_XX` | umolCO2 m-2 s-1 | `BERVO:0001963` Ecosystem respiration flux | Daytime flux partitioning, Variable friction velocity threshold, Percentile |  |
| Daytime | `RECO_DT_CUT_REF` | umolCO2 m-2 s-1 | `BERVO:0001963` Ecosystem respiration flux | Daytime flux partitioning, Constant friction velocity threshold, Reference ensemble member |  |
| Daytime | `RECO_DT_CUT_USTAR50` | umolCO2 m-2 s-1 | `BERVO:0001963` Ecosystem respiration flux | Daytime flux partitioning, Constant friction velocity threshold, Median, Friction velocity threshold |  |
| Daytime | `RECO_DT_CUT_MEAN` | umolCO2 m-2 s-1 | `BERVO:0001963` Ecosystem respiration flux | Daytime flux partitioning, Constant friction velocity threshold, Mean |  |
| Daytime | `RECO_DT_CUT_SE` | umolCO2 m-2 s-1 | `BERVO:0001963` Ecosystem respiration flux | Daytime flux partitioning, Constant friction velocity threshold, Standard error |  |
| Daytime | `RECO_DT_CUT_XX` | umolCO2 m-2 s-1 | `BERVO:0001963` Ecosystem respiration flux | Daytime flux partitioning, Constant friction velocity threshold, Percentile |  |
| Daytime | `GPP_DT_VUT_REF` | umolCO2 m-2 s-1 | `BERVO:0001962` Gross primary production rate | Daytime flux partitioning, Variable friction velocity threshold, Reference ensemble member |  |
| Daytime | `GPP_DT_VUT_USTAR50` | umolCO2 m-2 s-1 | `BERVO:0001962` Gross primary production rate | Daytime flux partitioning, Variable friction velocity threshold, Median, Friction velocity threshold |  |
| Daytime | `GPP_DT_VUT_MEAN` | umolCO2 m-2 s-1 | `BERVO:0001962` Gross primary production rate | Daytime flux partitioning, Variable friction velocity threshold, Mean |  |
| Daytime | `GPP_DT_VUT_SE` | umolCO2 m-2 s-1 | `BERVO:0001962` Gross primary production rate | Daytime flux partitioning, Variable friction velocity threshold, Standard error |  |
| Daytime | `GPP_DT_VUT_XX` | umolCO2 m-2 s-1 | `BERVO:0001962` Gross primary production rate | Daytime flux partitioning, Variable friction velocity threshold, Percentile |  |
| Daytime | `GPP_DT_CUT_REF` | umolCO2 m-2 s-1 | `BERVO:0001962` Gross primary production rate | Daytime flux partitioning, Constant friction velocity threshold, Reference ensemble member |  |
| Daytime | `GPP_DT_CUT_USTAR50` | umolCO2 m-2 s-1 | `BERVO:0001962` Gross primary production rate | Daytime flux partitioning, Constant friction velocity threshold, Median, Friction velocity threshold |  |
| Daytime | `GPP_DT_CUT_MEAN` | umolCO2 m-2 s-1 | `BERVO:0001962` Gross primary production rate | Daytime flux partitioning, Constant friction velocity threshold, Mean |  |
| Daytime | `GPP_DT_CUT_SE` | umolCO2 m-2 s-1 | `BERVO:0001962` Gross primary production rate | Daytime flux partitioning, Constant friction velocity threshold, Standard error |  |
| Daytime | `GPP_DT_CUT_XX` | umolCO2 m-2 s-1 | `BERVO:0001962` Gross primary production rate | Daytime flux partitioning, Constant friction velocity threshold, Percentile |  |
| Sundown | `RECO_SR` | umolCO2 m-2 s-1 | `BERVO:0001963` Ecosystem respiration flux | Sundown respiration partitioning |  |
| Sundown | `RECO_SR_N` | nondimensional | `BERVO:0001963` Ecosystem respiration flux | Sundown respiration partitioning, Fraction | fraction of the period's data available to fit the respiration model |

## BADM site metadata

*Pending: slice 5 of issue #178 adds the BADM quantities, disturbance and management
terms, and the BADM value lists.*
