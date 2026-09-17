# Alignment with ATS

The [Advanced Terrestrial Simulator](https://github.com/amanzi/ats) (ATS) is
coupled to EcoSIM through an `EcoSIM for ATS` process kernel. This page records
how the variables that cross that coupling, and the surface energy balance
variables ATS documents alongside them, are represented in BERVO. It resolves
[issue #36](https://github.com/bioepic-data/bervo/issues/36).

## Sources

| Source | Revision | Used for |
| --- | --- | --- |
| `amanzi/ats`, branch `agraus/ecosim_pk`, `src/pks/ecosim/` | `c67630b` (2026-09-14) | The keys the EcoSIM PK reads and writes, and the `BGCState` / `BGCProperties` containers |
| `amanzi/ats`, `src/pks/surface_balance/constitutive_relations/land_cover/seb_threecomponent_evaluator.hh` | same | Names and units of the surface energy balance variables |
| `jinyun1tang/EcoSIM`, branch `agraus/PrescribedPhenology`, `f90src/ATSUtils/` | `c431939` (2026-09-08) | Which EcoSIM variable receives or supplies each ATS field, and the unit conversions applied |

ATS variable names carry a domain prefix. Surface fields are `surface-<key>`,
snow fields are `snow-<key>`, and subsurface fields have no prefix.

## How the alignment is recorded

- An ATS variable name is stored on the BERVO term as a **related synonym**
  (`oio:hasRelatedSynonym`), exactly as ATS spells it.
- The term's **`Comment`** starts with `ATS:`, gives the ATS unit in brackets,
  and, where the coupling converts or renames the quantity, says what EcoSIM
  variable it lands in.
- Where ATS uses an SI unit BERVO did not list, that unit is **appended to
  `has_units`**. Existing EcoSIM units are kept.
- EcoSIM identifiers that the coupling uses and BERVO lacked are added as
  related synonyms on the matching term, or as the `EcoSIM Variable Name` of a
  new term.

## ATS variables mapped to existing BERVO terms

| ATS variable | BERVO term | Unit added | Note |
| --- | --- | --- | --- |
| `temperature` (subsurface) | Soil temperature (`BERVO:0001477`) | | Bare key is not stored as a synonym; `TKSoil1_vr` is |
| `surface-air_temperature` | Air temperature (`BERVO:0001370`) | | `TairK_col` added |
| `snow-temperature` | Snow temperature (`BERVO:0001556`) | | |
| `surface-vapor_pressure_air` | Atmospheric vapor pressure (`BERVO:0001374`) | Pa | Coupling divides by 1000 for `VPK_col` |
| `surface-wind_speed` | Measured wind speed (`BERVO:0001372`) | m s-1 | Coupling multiplies by 3600 for `WindSpeedAtm_col` |
| `surface-precipitation_rain` | Rainfall measurement (`BERVO:0001421`) | m s-1 | |
| `surface-precipitation_snow`, `snow-precipitation` | Snowfall measurement (`BERVO:0001422`) | m SWE s-1 | |
| `surface-precipitation_total` | Precipitation from atmosphere to land surface (`BERVO:0001828`) | m s-1 | Chosen over Total precipitation (`BERVO:0000309`), which is a cumulative volume |
| `surface-incoming_longwave_radiation` | Sky longwave radiation (`BERVO:0001380`) | W m-2 | |
| `surface-albedo` | Surface albedo (`BERVO:0001507`) | | |
| `surface-snow_albedo` | Snowpack albedo (`BERVO:0001554`) | | `SnowAlbedo_col` added; see open questions |
| `surface-net_radiation` | Total net radiation at ground surface (`BERVO:0001443`) | W m-2 | |
| `surface-qE_latent_heat` | Total latent heat flux at ground surface (`BERVO:0001444`) | W m-2 | |
| `surface-qE_sensible_heat` | Total sensible heat flux at ground surface (`BERVO:0001445`) | W m-2 | |
| `surface-qE_conducted`, `surface-ecosim_source` | Heat flux into ground, computed from surface energy balance model (`BERVO:0001488`) | W m-2, MW m-2 | `ecosim_source` is `HeatFlx2Grnd_col` per area per second |
| `surface-ecosim_water_source` | Infiltration into soil (`BERVO:0001821`) | m s-1 | `Qinflx2Soil_col` divided by 3600 |
| `subsurface_ecosim_water_source` | Current step vertical root water uptake profile (`BERVO:0000392`) | | Sum over PFTs of `RPlantRootH2OUptk_pvr` |
| `surface-water_table_depth` | Internal water table depth (`BERVO:0001763`) | | |
| `porosity` | Soil porosity (`BERVO:0001524`) | | `POROS_vr` added |
| `bulk_density` | Soil bulk density (`BERVO:0001535`) | | Computed from `density_rock` and `porosity` |
| `hydraulic_conductivity` | Hydraulic conductivity at different moisture levels (`BERVO:0001771`) | | Unit corrected from `NONE` to `m MPa-1 h-1`, EcoSIM's declared unit |
| `matric_pressure` | Soil micropore matric water potential (`BERVO:0001750`) | Pa | `PSISM1_vr` added; fed from ATS capillary pressure |
| `field_capacity` | Water potentials at field capacity (`BERVO:0001503`) | | EcoSIM PK input parameter |
| `wilting_point` | Water potentials at wilting point (`BERVO:0001504`) | | EcoSIM PK input parameter |
| `surface-canopy_surface_water` | Canopy held water content (`BERVO:0000579`) | | |
| `surface-canopy_longwave_radiation` | Longwave radiation emitted by canopy (`BERVO:0000577`) | | |
| `surface-canopy_latent_heat` | Canopy latent heat flux (`BERVO:0000582`) | | Column total via `Air_Heat_Latent_store_col` |
| `surface-canopy_sensible_heat` | Air to canopy sensible heat flux (`BERVO:0000583`) | | Column total via `Air_Heat_Sens_store_col` |
| `surface-transpiration` | Canopy transpiration (`BERVO:0000591`) | | Summed over PFTs |
| `surface-evaporation_canopy` | Total canopy evaporation (`BERVO:0000599`) | | Summed over PFTs |
| `surface-evapotranspiration` | Total canopy evaporation + transpiration (`BERVO:0000598`) | | |
| `surface-snow_depth`, `snow-depth` | Snowpack depth (`BERVO:0001572`) | | |
| `snow-density` | Snowpack density (`BERVO:0001563`) | kg m-3 | |
| `surface-elevation` | Altitude of grid cell (`BERVO:0000676`) | | |
| `surface-aspect` | Aspect (`BERVO:0000685`) | | |
| `surface-slope_magnitude` | Measurement of slope (`BERVO:0000684`) | | ATS value is dimensionless, not degrees |
| `atm_n2`, `atm_o2`, `atm_co2`, `atm_ch4`, `atm_n2o`, `atm_nh3`, `atm_h2` | The seven `Atmospheric … concentration` terms (`BERVO:0001393` to `BERVO:0001399`) | | Scalar PK properties |

Two rows carry a comment without a synonym:

- **Volumetric water content** (`BERVO:0001743`, `THETW_vr`) is a fraction of
  bulk soil volume. The coupling currently writes ATS `saturation_liquid`, a
  fraction of pore volume, into it. The ATS key is on the new term
  Soil liquid water saturation instead.
- **Soil micropore water content** (`BERVO:0001747`) gains `VLWatMicP1_vr` and
  a note that ATS `water_content` is an extensive molar quantity, converted by
  liquid molar density and column area. The bare `water_content` key is not
  stored as a synonym anywhere.

## New terms

| BERVO term | Category | ATS variable | Unit |
| --- | --- | --- | --- |
| Surface skin temperature (`BERVO:0001859`) | Soil surface variable | `surface-temperature` | K |
| Ponded water depth (`BERVO:0001860`) | Soil surface variable | `surface-ponded_depth` | m |
| Thaw depth (`BERVO:0001861`) | Soil heat variable | `surface-thaw_depth` | m |
| Active layer mean temperature (`BERVO:0001862`) | Soil heat variable | `surface-active_layer_average_temperature` | K |
| Surface water unfrozen fraction (`BERVO:0001863`) | Soil surface variable | `surface-unfrozen_fraction` | NONE |
| Soil liquid water saturation (`BERVO:0001864`) | Soil and water variable | `saturation_liquid` | m3 m-3 |
| Soil ice saturation (`BERVO:0001865`) | Soil and water variable | `saturation_ice` | m3 m-3 |
| Soil gas saturation (`BERVO:0001866`) | Soil and water variable | `saturation_gas` | m3 m-3 |
| Incoming shortwave radiation (`BERVO:0001867`) | Climate force variable | `surface-incoming_shortwave_radiation` | W m-2 |
| Soil surface resistance to vapor transfer (`BERVO:0001868`) | Soil surface variable | `surface-rsoil`, `surface-soil_resistance` | s m-1 |
| Microtopographic relief (`BERVO:0001869`) | Land surface variable | `surface-microtopographic_relief` | m |
| Soil thermal conductivity (`BERVO:0001870`) | Soil heat variable | `thermal_conductivity` | W m-1 K-1 |
| Soil relative permeability (`BERVO:0001871`) | Soil and water variable | `relative_permeability` | NONE |
| Soil capillary pressure (`BERVO:0001872`) | Soil and water variable | `capillary_pressure_gas_liq` | Pa |
| Snow water equivalent (`BERVO:0001873`) | Snow variable | `snow-water_equivalent` | m |
| Canopy held snow content (`BERVO:0001874`) | Canopy variable | `surface-canopy_snow` | m3 d-2 |
| Bare ground evaporation (`BERVO:0001875`) | Soil surface variable | `surface-evaporation_ground` | m3 H2O d-2 h-1 |
| Surface litter evaporation (`BERVO:0001876`) | Surface litter variable | `surface-evaporation_litter` | m3 H2O d-2 h-1 |
| Snowpack evaporation (`BERVO:0001877`) | Snow variable | `surface-evaporation_snow` | m3 H2O d-2 h-1 |
| Snowpack sublimation (`BERVO:0001878`) | Snow variable | `surface-sublimation_snow` | m3 H2O d-2 h-1 |
| Canopy leaf area index (`BERVO:0001879`) | Plant trait variable | `surface-LAI` | m2 m-2 |
| Canopy stem area index (`BERVO:0001880`) | Plant trait variable | `surface-SAI` | m2 m-2 |
| Liquid water molar density (`BERVO:0001881`) | Water variable | `molar_density_liquid` | mol m-3 |
| Soil particle density (`BERVO:0001882`) | Soil variable | `density_rock` | kg m-3 |
| Stem area index (`BERVO:8000588`) | Concept | | |

Seven of the new variables also name the EcoSIM variable that supplies them:
`SnowOnCanopy_pft`, `TEvapXAir2Toplay_col`, `TEvapXAir2LitR_col`, `EVAPW_col`,
`EVAPS_col`, plus `tlai_day_pft` and `tsai_day_pft` for the two area indices.

One hierarchy change: Water equivalent snowpack (`BERVO:0001577`) is now a child
of Snow water equivalent rather than of Snow variable.

## Not mapped, and why

| ATS field | Reason |
| --- | --- |
| `water_content` (subsurface) | Extensive molar quantity per cell, and the same root key names several distinct quantities in ATS. Noted on `BERVO:0001747` only. |
| `heat capacity [MJ mol^-1 K^-1]` | The parameter is labelled molar but is written straight into EcoSIM `VHeatCapacity1_vr`, a volumetric heat capacity. The quantity is not well defined enough to mint. |
| `plant_wilting_factor`, `rooting_depth_fraction` | Both keys are aliased to `porosity` in the PK; the fields are placeholders. |
| `vegetation_type` | An integer plant functional type code, not a measured quantity. |
| `mole_fraction` | A per-component tracer array; needs a decision on how BERVO represents transported species. |
| `subsurface_ecosim_source` | Declared, but never assigned on the EcoSIM side. |
| `incident_shortwave_radiation` | Read by the PK but never copied to EcoSIM. |
| `cell_volume`, `column_area`, `depth`, `dz`, `mass_density_ice`, `mass_density_gas` | Grid geometry and phase densities used only inside the coupling. |

## Open questions

- **Snowpack albedo** (`BERVO:0001554`) carries EcoSIM name `SoilAlbedo_col`,
  which EcoSIM's own declaration also documents as snowpack albedo. The coupling
  sets `SoilAlbedo_col` to a constant 0.2 and writes the ATS snow albedo into
  `SnowAlbedo_col`. Either the EcoSIM declaration comment or the BERVO
  provenance is wrong. `SnowAlbedo_col` is added as a related synonym for now.
- **Volumetric water content** versus **Soil liquid water saturation**: the
  coupling writes a pore-volume fraction into a bulk-volume fraction. That is a
  coupling question for the ATS and EcoSIM developers, not a BERVO one, but the
  comments on both terms record it.
- **Root water uptake** (`BERVO:0001116`) records `AllPlantRootH2OLoss_pvr`,
  which no longer exists in the EcoSIM tree checked here. `RPlantRootH2OUptk_pvr`
  has the same shape and documentation and is added as a related synonym.
