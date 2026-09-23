# Units

`has_units` holds [UCUM](https://ucum.org/ucum) (issues
[#14](https://github.com/bioepic-data/bervo/issues/14) and
[#88](https://github.com/bioepic-data/bervo/issues/88)). BERVO does not define its own
unit terms, and does not map units to a unit ontology such as UO, which cannot carry
the detail these variables need: which element a mass is of, and whether a value is a
total for a grid cell. The rules for writing a unit are in the `has_units` section of
`AGENTS.md`. This page records the conversion.

## The decisions

| Question | Decision |
| --- | --- |
| EcoSIM's `d-2` | A trailing `/{grid}`. In EcoSIM it marks a total for a grid cell, and in UCUM `d` is the day. |
| A substance inside a unit (`gC`, `m3 H2O`) | A UCUM annotation on the unit it qualifies: `g{C}`, `m3{H2O}`. |
| `NONE` | UCUM's unity, `1`. `NA` stays for a variable with no numeric magnitude. |
| Syntax | Exponents joined by `.`. Once a `/` appears, no `.` follows it outside parentheses. |

## What `d-2` means

EcoSIM builds its `d-2` quantities from grid-cell totals. `VGeomLayer_vr`, declared
`[m3 d-2]`, is set as `AREA_3D(3,L,NY,NX)*DLYR_3D(3,L,NY,NX)` in `StartsMod.F90`: the
layer's ground area times its thickness, the volume of the whole cell. EcoSIM's own
`AGENTS.md` tells its developers to keep "per-area values" apart from "grid-cell
totals". So `g d-2` is grams in the grid cell, written here as `g/{grid}`. `{grid}` is
unity to a converter, so the dimension is mass, as a total should be.

This reading comes from the code, not from an EcoSIM statement of the convention. If a
`d-2` variable turns out to be normalised per square metre, its unit becomes `.m-2`.

`d-3` appears once, on `Root autotrophic respiration` (`BERVO:0000434`), and is
treated the same way, since each layer is its own grid cell. `t-1` is per time step,
written `/{step}`, and `p-1` is per plant, written `/{plant}`.

## Mapping

All 235 strings that were in the column, with the number of rows each was on.
1572 of the 2707 filled cells changed. A note marks a typo fixed on the
way (the row's meaning was clear) or a meaning that looks wrong (converted as written,
and left for a curator).

| Was | UCUM | Rows | Note |
| --- | --- | --- | --- |
| `NA` | `NA` | 951 |  |
| `NONE` | `1` | 222 |  |
| `g d-2` | `g/{grid}` | 174 |  |
| `g d-2 h-1` | `g.h-1/{grid}` | 171 |  |
| `m` | `m` | 87 |  |
| `g m-3` | `g.m-3` | 66 |  |
| `m3 d-2` | `m3/{grid}` | 52 |  |
| `mol m^-3` | `mol.m-3` | 52 |  |
| `m2 h-1` | `m2.h-1` | 51 |  |
| `g g-1` | `g.g-1` | 50 |  |
| `m3 d-2 h-1` | `m3.h-1/{grid}` | 43 |  |
| `MJ d-2 h-1` | `MJ.h-1/{grid}` | 35 |  |
| `h-1` | `h-1` | 31 |  |
| `mol d-2 h-1` | `mol.h-1/{grid}` | 26 |  |
| `m2 d-2` | `m2/{grid}` | 21 |  |
| `m3 m-3` | `m3.m-3` | 19 |  |
| `h` | `h` | 18 |  |
| `oC` | `Cel` | 15 |  |
| `mol^2 m^-6` | `mol2.m-6` | 14 |  |
| `gC d-2 h-1` | `g{C}.h-1/{grid}` | 13 |  |
| `m3 H2O d-2 h-1` | `m3{H2O}.h-1/{grid}` | 13 |  |
| `m^3 mol^-1` | `m3.mol-1` | 13 |  |
| `MPa` | `MPa` | 12 |  |
| `gC d-2` | `g{C}/{grid}` | 12 |  |
| `mol^3 m^-9` | `mol3.m-9` | 12 |  |
| `umol m-2 s-1` | `umol.m-2.s-1` | 12 |  |
| `Mpa` | `MPa` | 11 | typo: Mpa is not a unit; megapascal is MPa |
| `kJ g-1 C` | `kJ.g-1{C}` | 11 |  |
| `C` | `Cel` | 10 | suspect: most of these rows are functions, factors or element masses, not temperatures |
| `K` | `K` | 10 |  |
| `MJ d-2` | `MJ/{grid}` | 10 |  |
| `mol d-2` | `mol/{grid}` | 10 |  |
| `mol m-3` | `mol.m-3` | 10 |  |
| `uM` | `umol.L-1` | 10 |  |
| `g solute /g gas` | `g{solute}.g-1{gas}` | 9 |  |
| `umol mol-1` | `umol.mol-1` | 9 |  |
| `d-2` | `/{grid}` | 8 |  |
| `g C m-3` | `g{C}.m-3` | 8 |  |
| `g N m-3` | `g{N}.m-3` | 8 |  |
| `MJ d-2 t-1` | `MJ/{grid}/{step}` | 7 | suspect: several rows are water transfers, not energy |
| `g/d2/h` | `g.h-1/{grid}` | 7 |  |
| `gN d-2 h-1` | `g{N}.h-1/{grid}` | 7 |  |
| `ppmv` | `[ppm]{vol}` | 7 |  |
| `MJ d-2 K-1` | `MJ.K-1/{grid}` | 6 |  |
| `degree` | `deg` | 6 |  |
| `h^-1` | `h-1` | 6 |  |
| `kPa` | `kPa` | 6 |  |
| `oC\|K` | `Cel\|K` | 6 |  |
| `MJ m-2 h-1` | `MJ.m-2.h-1` | 5 |  |
| `Mg d-2` | `Mg/{grid}` | 5 |  |
| `Mg d-2 h-1` | `Mg.h-1/{grid}` | 5 |  |
| `g m-2` | `g.m-2` | 5 |  |
| `gN gC-1` | `g{N}.g-1{C}` | 5 |  |
| `gN m-3` | `g{N}.m-3` | 5 |  |
| `m2 m-2` | `m2.m-2` | 5 |  |
| `m3 d-2 t-1` | `m3/{grid}/{step}` | 5 |  |
| `mm h-1` | `mm.h-1` | 5 |  |
| `Mg m-3` | `Mg.m-3` | 4 |  |
| `g C g-1 N h-1` | `g{C}.g-1{N}.h-1` | 4 |  |
| `g/mol` | `g.mol-1` | 4 |  |
| `gP d-2 h-1` | `g{P}.h-1/{grid}` | 4 |  |
| `m d-2` | `m/{grid}` | 4 | suspect: a length per grid cell; the root length rows may mean m, the conductance row m.h-1 |
| `m g-1` | `m.g-1` | 4 |  |
| `m2` | `m2` | 4 |  |
| `m3 H2O d-2` | `m3{H2O}/{grid}` | 4 |  |
| `m^6 mol^-2` | `m6.mol-2` | 4 |  |
| `mg P kg-1` | `mg{P}.kg-1` | 4 |  |
| `mg kg-1` | `mg.kg-1` | 4 |  |
| `mm d-1` | `mm.d-1` | 4 |  |
| `umol g-1 h-1` | `umol.g-1.h-1` | 4 |  |
| `0-1` | `1` | 3 |  |
| `MJ d-2 t-1\|W m-2` | `MJ/{grid}/{step}\|W.m-2` | 3 |  |
| `MJ/K` | `MJ.K-1` | 3 |  |
| `W m-2` | `W.m-2` | 3 |  |
| `g C g-1C h-1` | `g{C}.g-1{C}.h-1` | 3 |  |
| `g kg-1` | `g.kg-1` | 3 |  |
| `g m-2 h-1` | `g.m-2.h-1` | 3 |  |
| `g/m2/hr` | `g.m-2.h-1` | 3 |  |
| `gC` | `g{C}` | 3 |  |
| `gP gC-1` | `g{P}.g-1{C}` | 3 |  |
| `kJ/kg` | `kJ.kg-1` | 3 |  |
| `kg Mg-1` | `kg.Mg-1` | 3 |  |
| `m MPa-1 h-1` | `m.MPa-1.h-1` | 3 |  |
| `m h-1` | `m.h-1` | 3 |  |
| `m2 d-2 h-1` | `m2.h-1/{grid}` | 3 |  |
| `m3 d-2 h-1\|m s-1` | `m3.h-1/{grid}\|m.s-1` | 3 |  |
| `mg Ca kg-1` | `mg{Ca}.kg-1` | 3 |  |
| `s m-1` | `s.m-1` | 3 |  |
| `umol m-3` | `umol.m-3` | 3 |  |
| `MJ h-1` | `MJ.h-1` | 2 |  |
| `MJ m-1` | `MJ.m-1` | 2 |  |
| `MJ/d2/h` | `MJ.h-1/{grid}` | 2 |  |
| `MJ/m3/K` | `MJ.m-3.K-1` | 2 |  |
| `MPa h m-2` | `MPa.h.m-2` | 2 |  |
| `Pa` | `Pa` | 2 |  |
| `cmol kg-1` | `cmol.kg-1` | 2 |  |
| `degrees from horizontal` | `deg` | 2 |  |
| `g` | `g` | 2 |  |
| `g   g-1C h-1` | `g.g-1{C}.h-1` | 2 |  |
| `g  g-1C h-1` | `g.g-1{C}.h-1` | 2 |  |
| `g H m-3` | `g{H}.m-3` | 2 |  |
| `g N m-2 h-1` | `g{N}.m-2.h-1` | 2 |  |
| `g P m-3` | `g{P}.m-3` | 2 |  |
| `g m^-3` | `g.m-3` | 2 |  |
| `g micr C g-1 subs C` | `g{C_microbial}.g-1{C_substrate}` | 2 |  |
| `g subs. C g-1 micr. C` | `g{C_substrate}.g-1{C_microbial}` | 2 |  |
| `gC d2 h-1` | `g{C}.h-1/{grid}` | 2 | typo: d2 was missing its minus sign |
| `gC gC-1` | `g{C}.g-1{C}` | 2 |  |
| `gO d-2 h-1` | `g{O}.h-1/{grid}` | 2 |  |
| `h m-1` | `h.m-1` | 2 |  |
| `kJ g-1 N` | `kJ.g-1{N}` | 2 |  |
| `kg m-2` | `kg.m-2` | 2 |  |
| `m d-1` | `m.d-1` | 2 |  |
| `m d-2 h-1` | `m.h-1/{grid}` | 2 |  |
| `m m-3` | `m.m-3` | 2 |  |
| `m p-1` | `m/{plant}` | 2 |  |
| `m t-1` | `m/{step}` | 2 |  |
| `m-1` | `m-1` | 2 |  |
| `m-2` | `m-2` | 2 |  |
| `m3 H2O (gC)-1` | `m3{H2O}.g-1{C}` | 2 |  |
| `mg Al kg-1` | `mg{Al}.kg-1` | 2 |  |
| `mg Fe kg-1` | `mg{Fe}.kg-1` | 2 |  |
| `mm` | `mm` | 2 |  |
| `mol N m-3` | `mol{N}.m-3` | 2 |  |
| `mol m-2` | `mol.m-2` | 2 |  |
| `mol^4 m^-12` | `mol4.m-12` | 2 |  |
| `uM /umol mol-1` | `umol.L-1/(umol.mol-1)` | 2 |  |
| `umol e- umol CO2` | `umol{e-}.umol-1{CO2}` | 2 | typo: the CO2 denominator was missing its -1 |
| `umol umol-1` | `umol.umol-1` | 2 |  |
| `J (mole K)^-1` | `J.mol-1.K-1` | 1 |  |
| `J m-2` | `J.m-2` | 1 |  |
| `J/g/K~MJ/m3/K` | `J.g-1.K-1\|MJ.m-3.K-1` | 1 |  |
| `MJ  d-2` | `MJ/{grid}` | 1 |  |
| `MJ  d-2 h-1` | `MJ.h-1/{grid}` | 1 |  |
| `MJ K-1` | `MJ.K-1` | 1 |  |
| `MJ d-1` | `MJ.d-1` | 1 |  |
| `MJ d-2 h-1\|W m-2\|MW m-2` | `MJ.h-1/{grid}\|W.m-2\|MW.m-2` | 1 |  |
| `MJ k-1 d-2` | `MJ.K-1/{grid}` | 1 | typo: k-1 for K-1 |
| `MJ m h-1 K-1` | `MJ.m.h-1.K-1` | 1 |  |
| `MJ m-1 h-1 K-1` | `MJ.m-1.h-1.K-1` | 1 |  |
| `MJ m-2 d-1` | `MJ.m-2.d-1` | 1 |  |
| `MJ m-3` | `MJ.m-3` | 1 | suspect: a heat flux in MJ m-3 |
| `MJ/K d-2` | `MJ.K-1/{grid}` | 1 |  |
| `MJ/K/gC` | `MJ.K-1.g-1{C}` | 1 |  |
| `MJ/h` | `MJ.h-1` | 1 |  |
| `MJ/h\|MJ m-2 h-1\|W m-2` | `MJ.h-1\|MJ.m-2.h-1\|W.m-2` | 1 |  |
| `MPa h m-4` | `MPa.h.m-4` | 1 |  |
| `MPa\|Pa` | `MPa\|Pa` | 1 |  |
| `Mg d-2 t-1` | `Mg/{grid}/{step}` | 1 |  |
| `Mg m-1 s` | `Mg.m-1.s-1` | 1 | typo: a viscosity is Mg m-1 s-1; EcoSIM declares VISCW = 1.0E-06 [Mg m-1 s], which is 1 mPa s only with s-1 |
| `Mg m-3\|kg m-3` | `Mg.m-3\|kg.m-3` | 1 |  |
| `Mg soil/gC` | `Mg{soil}.g-1{C}` | 1 |  |
| `MgC m-3` | `Mg{C}.m-3` | 1 |  |
| `W m-1 K-1` | `W.m-1.K-1` | 1 |  |
| `cm` | `cm` | 1 |  |
| `cm\|m` | `cm\|m` | 1 |  |
| `dS m-1` | `dS.m-1` | 1 |  |
| `degrees north` | `deg` | 1 |  |
| `eqv (gC)^-1` | `eq.g-1{C}` | 1 |  |
| `g /d2` | `g/{grid}` | 1 |  |
| `g C g-1 C` | `g{C}.g-1{C}` | 1 |  |
| `g C g-1 soil` | `g{C}.g-1{soil}` | 1 |  |
| `g C m-2` | `g{C}.m-2` | 1 |  |
| `g H2O g-1 C` | `g{H2O}.g-1{C}` | 1 |  |
| `g J-1` | `g.J-1` | 1 |  |
| `g Mg-1` | `g.Mg-1` | 1 |  |
| `g Mg-1\|g g-1` | `g.Mg-1\|g.g-1` | 1 |  |
| `g N g-1 C` | `g{N}.g-1{C}` | 1 |  |
| `g N, g-1 C` | `g{N}.g-1{C}` | 1 |  |
| `g O m-3` | `g{O}.m-3` | 1 |  |
| `g P g-1 C` | `g{P}.g-1{C}` | 1 |  |
| `g P m-2 h-1` | `g{P}.m-2.h-1` | 1 |  |
| `g cm-3` | `g.cm-3` | 1 |  |
| `g d-2 t-1` | `g/{grid}/{step}` | 1 |  |
| `g g-1 h-1` | `g.g-1.h-1` | 1 |  |
| `g gC-1` | `g.g-1{C}` | 1 |  |
| `g h-1` | `g.h-1` | 1 |  |
| `g m-3\|umol mol-1` | `g.m-3\|umol.mol-1` | 1 |  |
| `g p-1` | `g/{plant}` | 1 |  |
| `g/cm3~ton/m3` | `g.cm-3\|t.m-3` | 1 |  |
| `g/d2` | `g/{grid}` | 1 |  |
| `gC d-2 hr-1` | `g{C}.h-1/{grid}` | 1 |  |
| `gC d-3 hr-1` | `g{C}.h-1/{grid}` | 1 | suspect: EcoSIM declares d-3, a per-volume grid measure; still a total per grid cell |
| `gC m-3` | `g{C}.m-3` | 1 |  |
| `gC/d2/hr` | `g{C}.h-1/{grid}` | 1 |  |
| `gC/h` | `g{C}.h-1` | 1 |  |
| `gN` | `g{N}` | 1 |  |
| `gN d-2` | `g{N}/{grid}` | 1 |  |
| `gO m-3` | `g{O}.m-3` | 1 |  |
| `gP` | `g{P}` | 1 |  |
| `gP d-2` | `g{P}/{grid}` | 1 |  |
| `ha-1\|m-2` | `har-1\|m-2` | 1 |  |
| `kPa\|Pa` | `kPa\|Pa` | 1 |  |
| `kg m-3` | `kg.m-3` | 1 |  |
| `m h-1\|h m-1` | `m.h-1\|h.m-1` | 1 |  |
| `m h-1\|m s-1` | `m.h-1\|m.s-1` | 1 |  |
| `m s-1` | `m.s-1` | 1 |  |
| `m2 g-1` | `m2.g-1` | 1 |  |
| `m2 ha-1` | `m2.har-1` | 1 |  |
| `m2 m-3` | `m2.m-3` | 1 |  |
| `m3` | `m3` | 1 |  |
| `m3 H2O/d2/h` | `m3{H2O}.h-1/{grid}` | 1 |  |
| `m3 H3O d-2 h-1` | `m3{H2O}.h-1/{grid}` | 1 | typo: H3O for H2O |
| `m3 d-2 h-1\|m SWE s-1` | `m3.h-1/{grid}\|m{SWE}.s-1` | 1 |  |
| `m3 g-1` | `m3.g-1` | 1 |  |
| `m3 gC-1` | `m3.g-1{C}` | 1 |  |
| `m3 pore m-3 litr` | `m3{pore}.m-3{litter}` | 1 |  |
| `m3 s-1` | `m3.s-1` | 1 |  |
| `m^9 mol^-3` | `m9.mol-3` | 1 |  |
| `mg C kg-1` | `mg{C}.kg-1` | 1 |  |
| `mg CaCO3 kg-1 pH-1` | `mg{CaCO3}.kg-1/{pH}` | 1 |  |
| `mg Cl kg-1` | `mg{Cl}.kg-1` | 1 |  |
| `mg K kg-1` | `mg{K}.kg-1` | 1 |  |
| `mg Mg kg-1` | `mg{Mg}.kg-1` | 1 |  |
| `mg Mn kg-1` | `mg{Mn}.kg-1` | 1 |  |
| `mg N kg-1` | `mg{N}.kg-1` | 1 |  |
| `mg Na kg-1` | `mg{Na}.kg-1` | 1 |  |
| `mg S kg-1` | `mg{S}.kg-1` | 1 |  |
| `mg Zn kg-1` | `mg{Zn}.kg-1` | 1 |  |
| `mol h-1` | `mol.h-1` | 1 |  |
| `mol m^-^3` | `mol.m-3` | 1 | typo: stray caret |
| `mol/d2/h` | `mol.h-1/{grid}` | 1 |  |
| `mol^11 m^-33` | `mol11.m-33` | 1 |  |
| `mol^11 mol^-33` | `mol11.m-33` | 1 | typo: mol^-33 for m^-33, as its sibling SYCAH1 has |
| `mol^8 m^-24` | `mol8.m-24` | 1 |  |
| `n m-3` | `{cells}.m-3` | 1 |  |
| `nephelometric turbidity units` | `{NTU}` | 1 |  |
| `oC-1` | `K-1` | 1 | a Celsius degree cannot take an exponent in UCUM; per degree Celsius is per kelvin |
| `s` | `s` | 1 |  |
| `s h-1` | `s.h-1` | 1 |  |
| `s m-1\|s h-1` | `s.m-1\|s.h-1` | 1 |  |
| `s/day` | `s.d-1` | 1 |  |
| `s/hour` | `s.h-1` | 1 |  |
| `umol e- umol-1 PAR` | `umol{e-}.umol-1{PAR}` | 1 |  |
| `umol mol-1\|gC m-3` | `umol.mol-1\|g{C}.m-3` | 1 |  |

## Logarithms

A logarithm has no unit, whatever the unit of the value it was taken of. Six `Log …`
rows carried the unit of that value, `g d-2` or `MPa`, and now take `1`, as `Log soil
porosity` (`BERVO:0001508`) already did: `BERVO:0001509`, `BERVO:0001510`,
`BERVO:0001511`, `BERVO:0001516`, `BERVO:0001517`, `BERVO:0001518`. This settles the
log rows of [issue #95](https://github.com/bioepic-data/bervo/issues/95). Its question
about the two volumetric water contents is still open.

## Suspect meanings

These were converted faithfully and are listed so a curator can check the rows. The
validator cannot see any of them, because each is valid UCUM.

- `m d-2` on 4 row(s) (`BERVO:0000354`, `BERVO:0001101`, `BERVO:0001102`, `BERVO:0001452`): a length per grid cell; the root length rows may mean m, the conductance row m.h-1.
- `gC d-3 hr-1` on 1 row(s) (`BERVO:0000434`): EcoSIM declares d-3, a per-volume grid measure; still a total per grid cell.
- `MJ d-2 t-1` on 7 row(s) (`BERVO:0000580`, `BERVO:0000581`, `BERVO:0001146`, `BERVO:0001150`, `BERVO:0001442`, `BERVO:0001446`, `BERVO:0001447`): several rows are water transfers, not energy.
- `C` on 10 row(s) (`BERVO:0000760`, `BERVO:0000885`, `BERVO:0000926`, `BERVO:0001074`, `BERVO:0001353`, `BERVO:0001354`, `BERVO:0001362`, `BERVO:0001363`, `BERVO:0001435`, `BERVO:0001653`): most of these rows are functions, factors or element masses, not temperatures.
- `MJ m-3` on 1 row(s) (`BERVO:0001489`): a heat flux in MJ m-3.

## What the validator checks

- Every value is valid UCUM, when `ucumvert` is installed. CI installs it from
  `src/scripts/requirements.txt`. Without it, the validator says so in a warning.
- `NONE` is an error; the value is `1`.
- A space is an error; UCUM joins units with `.`.
- `d` with any exponent but 1 or -1 is an error, because it is almost certainly an
  EcoSIM grid-cell total written as UCUM days.
- A `.` after a `/` is an error, because UCUM reads left to right.

It does not check that a unit fits its quantity.
