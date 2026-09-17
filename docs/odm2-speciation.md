# Alignment with ODM2 speciation

[ODM2](https://www.odm2.org/) publishes a set of controlled vocabularies at
<http://vocabulary.odm2.org/>. Its **speciation** vocabulary names the chemical
form in which a measured result is expressed, for example nitrogen reported as
nitrate or as ammonium. This page records how each of its concepts is
represented in BERVO. It is the first step on
[issue #66](https://github.com/bioepic-data/bervo/issues/66).

## Source

The SKOS export at
<http://vocabulary.odm2.org/api/v1/speciation/?format=skos>, fetched on
2026-09-17. It holds 145 concepts and the scheme itself. Every concept's
definition takes the form "Expressed as X"; that definition is copied into the
BERVO term's `Comment`.

## How the alignment is recorded

- Each ODM2 concept becomes a **`DbXrefs`** entry in the form
  `ODM2:speciation/<id>`, on either an existing BERVO concept or a new one.
  The `ODM2` prefix expands to `http://vocabulary.odm2.org/`, so the emitted
  IRI is the concept's own URI and the same prefix serves the other ODM2
  vocabularies later.
- The ODM2 identifier (usually a chemical formula) is kept as an **exact
  synonym**, and the ODM2 definition is quoted in the term's **`Comment`**.
- Where a CHEBI term for the substance exists and was verified against OLS, it
  is added as a second cross-reference. Existing BERVO element and ion terms
  that lacked one gain it at the same time.
- Chemical species sit under Chemical (`BERVO:8000586`): elements under
  Element, ions under Ion, and organic species under a new Organic compound
  with four subgroups (Polycyclic aromatic hydrocarbon, Alkane, Organohalogen
  compound, Phthalate ester). Isotopes sit under Isotope, and the two
  non-chemical concepts under Physical property.

## ODM2 concepts mapped to existing BERVO terms

| ODM2 concept | BERVO term | CHEBI added |
| --- | --- | --- |
| `Al` | Aluminum (`BERVO:8000180`) |  |
| `C` | Carbon (`BERVO:8000075`) |  |
| `Ca` | Calcium (`BERVO:8000108`) | `CHEBI:22984` |
| `Fe` | Iron (`BERVO:8000182`) |  |
| `K` | Potassium (`BERVO:8000198`) |  |
| `Mg` | Magnesium (`BERVO:8000207`) | `CHEBI:25107` |
| `N` | Nitrogen (`BERVO:8000167`) | `CHEBI:25555` |
| `Na` | Sodium (`BERVO:8000143`) | `CHEBI:26708` |
| `P` | Phosphorus (`BERVO:8000001`) | `CHEBI:28659` |
| `O2` | Oxygen (`BERVO:8000124`) |  |
| `NH4` | Ammonium (`BERVO:8000113`) | `CHEBI:28938` |
| `CO3` | Carbonate (`BERVO:8000098`) | `CHEBI:41609` |
| `HCO3` | Bicarbonate (`BERVO:8000141`) |  |
| `NO3` | Nitrate (`BERVO:8000168`) |  |
| `PO4` | Phosphate (`BERVO:8000138`) | `CHEBI:18367` |
| `SO4` | Sulfate (`BERVO:8000228`) |  |
| `CO2` | Carbon dioxide (`BERVO:8000188`) | `CHEBI:16526` |
| `CaCO3` | Calcium carbonate (`BERVO:8000094`) |  |
| `CH4` | Methane (`BERVO:8000024`) |  |
| `H2O` | Water (`BERVO:8000102`) |  |
| `EC` | Conductivity (`BERVO:8000348`) |  |
| `pH` | pH (`BERVO:8000261`) |  |

Three ODM2 concepts are not mapped: `Not Applicable` and `Unknown` are
placeholders of the vocabulary rather than speciations, and `speciation` is
the scheme itself.

## Points to note

- ODM2 `Cl` is defined as "expressed as chlorine", so it maps to the new
  element Chlorine, not to Chloride (`BERVO:8000036`). Chloride's exact synonym
  `Cl` becomes `Cl-`, with `Cl` kept as a related synonym, so that no exact
  synonym names two terms.
- ODM2 `NO2` is nitrite. It maps to the new Nitrite, not to Nitrogen dioxide
  (`BERVO:8000123`), whose synonym is also `NO2`.
- ODM2 `SiO2` is defined as "expressed as silicate". The BERVO term is
  Silicon dioxide, with `silica` as a synonym, and the comment carries the
  ODM2 wording.
- ODM2 `O2` maps to Oxygen (`BERVO:8000124`), which sits under Element with
  `O2` as a synonym. No CHEBI cross-reference is added there, because the term
  is used for dioxygen and the parent says element.
- Twelve ODM2 concepts are molecular formulas that stand for several isomers
  ("C16H10, e.g., fluoranthene, pyrene"). Six of them get a formula-based
  label such as C16H10 aromatic hydrocarbons, with the named isomers as related
  synonyms and no CHEBI cross-reference. The rest, such as dichloroethane,
  trichloroethane, dichlorobenzene, and the methylated naphthalenes, get the
  generic name, and a CHEBI class cross-reference only where CHEBI has the
  generic class.
- Total alkalinity has no CHEBI term. It sits under Physical property beside
  pH.
- Aluminum (`BERVO:8000180`) already carries `CHEBI:33620`, which is
  "aluminium molecular entity" rather than the atom. It is left as it was.

## New terms

| BERVO term | Parent | ODM2 concept | CHEBI |
| --- | --- | --- | --- |
| Organic compound (`BERVO:8000590`) | Chemical |  | `CHEBI:50860` |
| Polycyclic aromatic hydrocarbon (`BERVO:8000591`) | Organic compound |  | `CHEBI:33848` |
| Alkane (`BERVO:8000592`) | Organic compound |  | `CHEBI:18310` |
| Organohalogen compound (`BERVO:8000593`) | Organic compound |  | `CHEBI:17792` |
| Phthalate ester (`BERVO:8000594`) | Organic compound |  | `CHEBI:35484` |
| Silver (`BERVO:8000595`) | Element | `Ag` | `CHEBI:30512` |
| Arsenic (`BERVO:8000596`) | Element | `As` | `CHEBI:27563` |
| Boron (`BERVO:8000597`) | Element | `B` | `CHEBI:27560` |
| Barium (`BERVO:8000598`) | Element | `Ba` | `CHEBI:32594` |
| Beryllium (`BERVO:8000599`) | Element | `Be` | `CHEBI:30501` |
| Bromine (`BERVO:8000600`) | Element | `Br` | `CHEBI:22927` |
| Cadmium (`BERVO:8000601`) | Element | `Cd` | `CHEBI:22977` |
| Chlorine (`BERVO:8000602`) | Element | `Cl` | `CHEBI:23116` |
| Cobalt (`BERVO:8000603`) | Element | `Co` | `CHEBI:27638` |
| Chromium (`BERVO:8000604`) | Element | `Cr` | `CHEBI:28073` |
| Copper (`BERVO:8000605`) | Element | `Cu` | `CHEBI:28694` |
| Fluorine (`BERVO:8000606`) | Element | `F` | `CHEBI:24061` |
| Mercury (`BERVO:8000607`) | Element | `Hg` | `CHEBI:25195` |
| Manganese (`BERVO:8000608`) | Element | `Mn` | `CHEBI:18291` |
| Molybdenum (`BERVO:8000609`) | Element | `Mo` | `CHEBI:28685` |
| Nickel (`BERVO:8000610`) | Element | `Ni` | `CHEBI:28112` |
| Lead (`BERVO:8000611`) | Element | `Pb` | `CHEBI:25016` |
| Radium (`BERVO:8000612`) | Element | `Ra` | `CHEBI:33325` |
| Rhenium (`BERVO:8000613`) | Element | `Re` | `CHEBI:49882` |
| Sulfur (`BERVO:8000614`) | Element | `S` | `CHEBI:26833` |
| Antimony (`BERVO:8000615`) | Element | `Sb` | `CHEBI:30513` |
| Selenium (`BERVO:8000616`) | Element | `Se` | `CHEBI:27568` |
| Silicon (`BERVO:8000617`) | Element | `Si` | `CHEBI:27573` |
| Tin (`BERVO:8000618`) | Element | `Sn` | `CHEBI:27007` |
| Strontium (`BERVO:8000619`) | Element | `Sr` | `CHEBI:33324` |
| Thorium (`BERVO:8000620`) | Element | `Th` | `CHEBI:33385` |
| Titanium (`BERVO:8000621`) | Element | `Ti` | `CHEBI:33341` |
| Thallium (`BERVO:8000622`) | Element | `Tl` | `CHEBI:30440` |
| Uranium (`BERVO:8000623`) | Element | `U` | `CHEBI:27214` |
| Vanadium (`BERVO:8000624`) | Element | `V` | `CHEBI:27698` |
| Zinc (`BERVO:8000625`) | Element | `Zn` | `CHEBI:27363` |
| Zirconium (`BERVO:8000626`) | Element | `Zr` | `CHEBI:33342` |
| Nitrite (`BERVO:8000627`) | Ion | `NO2` | `CHEBI:16301` |
| Cyanide (`BERVO:8000628`) | Ion | `CN-` | `CHEBI:17514` |
| Methylmercury (`BERVO:8000629`) | Ion | `CH3Hg` | `CHEBI:49747` |
| Silicon dioxide (`BERVO:8000630`) | Chemical | `SiO2` | `CHEBI:30563` |
| Deuterium (`BERVO:8000631`) | Isotope | `delta 2H` | `CHEBI:29237` |
| Nitrogen-15 (`BERVO:8000632`) | Isotope | `delta N15` | `CHEBI:36934` |
| Oxygen-18 (`BERVO:8000633`) | Isotope | `delta O18` | `CHEBI:33815` |
| Total alkalinity (`BERVO:8000634`) | Physical property | `TA` |  |
| Naphthalene (`BERVO:8000635`) | Polycyclic aromatic hydrocarbon | `C10H8` | `CHEBI:16482` |
| Methylnaphthalene (`BERVO:8000636`) | Polycyclic aromatic hydrocarbon | `C10H7CH3` | `CHEBI:50715` |
| Dimethylnaphthalene (`BERVO:8000637`) | Polycyclic aromatic hydrocarbon | `C10H6(CH3)2` | `CHEBI:48853` |
| Trimethylnaphthalene (`BERVO:8000638`) | Polycyclic aromatic hydrocarbon | `C10H5(CH3)3` |  |
| Tetramethylnaphthalene (`BERVO:8000639`) | Polycyclic aromatic hydrocarbon | `C10H4(CH3)4` |  |
| Ethylnaphthalene (`BERVO:8000640`) | Polycyclic aromatic hydrocarbon | `C10H7C2H5` |  |
| Acenaphthylene (`BERVO:8000641`) | Polycyclic aromatic hydrocarbon | `C12H8` | `CHEBI:33081` |
| C12H10 aromatic hydrocarbons (`BERVO:8000642`) | Polycyclic aromatic hydrocarbon | `C12H10` |  |
| Fluorene (`BERVO:8000643`) | Polycyclic aromatic hydrocarbon | `C13H10` | `CHEBI:28266` |
| Methylfluorene (`BERVO:8000644`) | Polycyclic aromatic hydrocarbon | `C14H12` |  |
| Phenanthrene (`BERVO:8000645`) | Polycyclic aromatic hydrocarbon | `C14H10` | `CHEBI:28851` |
| C15H12 aromatic hydrocarbons (`BERVO:8000646`) | Polycyclic aromatic hydrocarbon | `C15H12` |  |
| C16H10 aromatic hydrocarbons (`BERVO:8000647`) | Polycyclic aromatic hydrocarbon | `C16H10` |  |
| Dimethylphenanthrene (`BERVO:8000648`) | Polycyclic aromatic hydrocarbon | `C16H14` |  |
| C17H12 aromatic hydrocarbons (`BERVO:8000649`) | Polycyclic aromatic hydrocarbon | `C17H12` |  |
| C18H12 aromatic hydrocarbons (`BERVO:8000650`) | Polycyclic aromatic hydrocarbon | `C18H12` |  |
| Retene (`BERVO:8000651`) | Polycyclic aromatic hydrocarbon | `C18H18` |  |
| Methylchrysene (`BERVO:8000652`) | Polycyclic aromatic hydrocarbon | `C19H14` |  |
| C20H12 aromatic hydrocarbons (`BERVO:8000653`) | Polycyclic aromatic hydrocarbon | `C20H12` |  |
| Dibenz[a,h]anthracene (`BERVO:8000654`) | Polycyclic aromatic hydrocarbon | `C22H14` | `CHEBI:35299` |
| Dibenzofuran (`BERVO:8000655`) | Organic compound | `C12H8O` | `CHEBI:28145` |
| Dibenzothiophene (`BERVO:8000656`) | Organic compound | `C12H8S` | `CHEBI:23681` |
| Methyldibenzothiophene (`BERVO:8000657`) | Organic compound | `C13H10S` |  |
| Carbazole (`BERVO:8000658`) | Organic compound | `C12H9N` | `CHEBI:27543` |
| Benzene (`BERVO:8000659`) | Organic compound | `C6H6` | `CHEBI:16716` |
| Toluene (`BERVO:8000660`) | Organic compound | `C7H8` | `CHEBI:17578` |
| Ethylbenzene (`BERVO:8000661`) | Organic compound | `C8H10` | `CHEBI:16101` |
| Xylene (`BERVO:8000662`) | Organic compound | `C6H4(CH3)2` | `CHEBI:27338` |
| Styrene (`BERVO:8000663`) | Organic compound | `C8H8` | `CHEBI:27452` |
| Phenol (`BERVO:8000664`) | Organic compound | `C6H5OH` | `CHEBI:15882` |
| Aniline (`BERVO:8000665`) | Organic compound | `C6H5NH2` | `CHEBI:17296` |
| Nitrobenzene (`BERVO:8000666`) | Organic compound | `C6H5NO2` | `CHEBI:27798` |
| Dinitrophenol (`BERVO:8000667`) | Organic compound | `C6H4N2O5` | `CHEBI:39352` |
| Dinitrotoluene (`BERVO:8000668`) | Organic compound | `C7H6N2O4` | `CHEBI:23822` |
| Isophorone (`BERVO:8000669`) | Organic compound | `C9H14O` | `CHEBI:34800` |
| Acetone (`BERVO:8000670`) | Organic compound | `C3H6O` | `CHEBI:15347` |
| Butanone (`BERVO:8000671`) | Organic compound | `C4H8O` | `CHEBI:28398` |
| Ethylene glycol (`BERVO:8000672`) | Organic compound | `C2H6O2` | `CHEBI:30742` |
| Diethyl phthalate (`BERVO:8000673`) | Phthalate ester | `C12H14O4` | `CHEBI:34698` |
| Benzyl butyl phthalate (`BERVO:8000674`) | Phthalate ester | `C19H20O4` |  |
| Dimethyl terephthalate (`BERVO:8000675`) | Organic compound | `C10H10O4` | `CHEBI:156286` |
| Ethane (`BERVO:8000676`) | Alkane | `C2H6` | `CHEBI:42266` |
| Pentadecane (`BERVO:8000677`) | Alkane | `C15H32` | `CHEBI:28897` |
| Hexadecane (`BERVO:8000678`) | Alkane | `C16H34` | `CHEBI:45296` |
| Heptadecane (`BERVO:8000679`) | Alkane | `C17H36` | `CHEBI:16148` |
| Octadecane (`BERVO:8000680`) | Alkane | `C18H38` | `CHEBI:32926` |
| Nonadecane (`BERVO:8000681`) | Alkane | `C19H40` | `CHEBI:32927` |
| Icosane (`BERVO:8000682`) | Alkane | `C20H42` | `CHEBI:43619` |
| Henicosane (`BERVO:8000683`) | Alkane | `C21H44` | `CHEBI:32931` |
| Docosane (`BERVO:8000684`) | Alkane | `C22H46` | `CHEBI:46050` |
| Tricosane (`BERVO:8000685`) | Alkane | `C23H48` | `CHEBI:32934` |
| Tetracosane (`BERVO:8000686`) | Alkane | `C24H50` | `CHEBI:32936` |
| Pentacosane (`BERVO:8000687`) | Alkane | `C25H52` | `CHEBI:32938` |
| Hexacosane (`BERVO:8000688`) | Alkane | `C26H54` | `CHEBI:32940` |
| Heptacosane (`BERVO:8000689`) | Alkane | `C27H56` | `CHEBI:32941` |
| Octacosane (`BERVO:8000690`) | Alkane | `C28H58` | `CHEBI:32943` |
| Nonacosane (`BERVO:8000691`) | Alkane | `C29H60` | `CHEBI:7613` |
| Hentriacontane (`BERVO:8000692`) | Alkane | `C31H64` | `CHEBI:5659` |
| Chloromethane (`BERVO:8000693`) | Organohalogen compound | `CH3Cl` | `CHEBI:36014` |
| Dichloromethane (`BERVO:8000694`) | Organohalogen compound | `CH2Cl2` | `CHEBI:15767` |
| Chloroform (`BERVO:8000695`) | Organohalogen compound | `CHCl3` | `CHEBI:35255` |
| Bromomethane (`BERVO:8000696`) | Organohalogen compound | `CH3Br` | `CHEBI:39275` |
| Bromoform (`BERVO:8000697`) | Organohalogen compound | `CHBr3` | `CHEBI:38682` |
| Bromodichloromethane (`BERVO:8000698`) | Organohalogen compound | `CHBrCl2` | `CHEBI:34591` |
| Dibromochloromethane (`BERVO:8000699`) | Organohalogen compound | `CHBr2Cl` | `CHEBI:34627` |
| Chloroethane (`BERVO:8000700`) | Organohalogen compound | `C2H5Cl` | `CHEBI:47554` |
| Dichloroethane (`BERVO:8000701`) | Organohalogen compound | `C2H4Cl2` |  |
| Trichloroethane (`BERVO:8000702`) | Organohalogen compound | `C2H3Cl3` |  |
| Tetrachloroethane (`BERVO:8000703`) | Organohalogen compound | `C2H2Cl4` |  |
| Hexachloroethane (`BERVO:8000704`) | Organohalogen compound | `C2Cl6` | `CHEBI:39227` |
| Chloroethene (`BERVO:8000705`) | Organohalogen compound | `C2H3Cl` | `CHEBI:28509` |
| Trichloroethene (`BERVO:8000706`) | Organohalogen compound | `C2HCl3` | `CHEBI:16602` |
| Tetrachloroethene (`BERVO:8000707`) | Organohalogen compound | `C2Cl4` | `CHEBI:17300` |
| Hexachlorobutadiene (`BERVO:8000708`) | Organohalogen compound | `C4Cl6` | `CHEBI:5691` |
| Hexachlorocyclopentadiene (`BERVO:8000709`) | Organohalogen compound | `C5Cl6` |  |
| Bis(2-chloroethyl) ether (`BERVO:8000710`) | Organohalogen compound | `C4H8Cl2O` | `CHEBI:34573` |
| Chlorobenzene (`BERVO:8000711`) | Organohalogen compound | `C6H5Cl` | `CHEBI:28097` |
| Dichlorobenzene (`BERVO:8000712`) | Organohalogen compound | `C6H4Cl2` | `CHEBI:23697` |
| Trichlorobenzene (`BERVO:8000713`) | Organohalogen compound | `C6H3Cl3` | `CHEBI:27096` |
| Hexachlorobenzene (`BERVO:8000714`) | Organohalogen compound | `C6Cl6` | `CHEBI:5692` |
| Pentachlorophenol (`BERVO:8000715`) | Organohalogen compound | `C6HCl5O` | `CHEBI:17642` |
