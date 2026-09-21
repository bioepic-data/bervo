# Alignment with ODM2 site type

The ODM2 **site type** vocabulary (<http://vocabulary.odm2.org/sitetype/>) names
the kind of place at which a site, an ODM2 sampling feature, is located: a
stream, a spring, a landfill, a laboratory. BERVO has no notion of a site. It
does have the features a site sits on, and those are what the vocabulary maps
onto, in the same way that the [medium vocabulary](odm2-medium.md) mapped onto
the materials rather than onto specimens. This page records the mapping. It is
the third step on
[issue #66](https://github.com/bioepic-data/bervo/issues/66), after the
[speciation](odm2-speciation.md) and [medium](odm2-medium.md) vocabularies.

## Source

The JSON export at <http://vocabulary.odm2.org/api/v1/sitetype/?format=json>,
fetched on 2026-09-21. It holds 53 concepts. Cross-references take the form
`ODM2:sitetype/<id>`, using the `ODM2` prefix already declared in
`src/ontology/bervo.Makefile`; each emitted IRI redirects (301) to the same
path with a trailing slash, which returns the concept page. The ODM2 definition
is quoted in the term's `Comment`. Where an ENVO term names the same feature it
is added as a second cross-reference; every ENVO ID was checked against OLS.

## Where the features live

Two branches of Concept hold them. Natural features sit under the existing
Environmental feature (`BERVO:8000400`), which came from COMO with no children.
COMO defined it as a characteristic of the environment, such as elevation or
soil type, and that reading does not hold once a glacier is a subclass of it.
It is redefined here as a material part of the environment on or in which
observations are made, and it gains `ENVO:01000813` (astronomical body
part), the ENVO class that Water body, Landform, and the atmosphere all
descend from, beside its `COMO:0000217`. The COMO reference stays for
provenance, as Environmental material keeps `COMO:0000230` beside
`ENVO:00010483`, and its reading is recorded in the term's `Comment`. The
ENVO class is far wider than this term; it is the nearest live class ENVO
has, and `ENVO:00002297` (environmental feature) is obsolete there.
Two new grouping concepts sit beneath it: Water body (`BERVO:8000724`) for the
surface water sites, and Landform (`BERVO:8000725`) for springs, caves, and
the other shapes of the ground. Built features sit under a new Human
construction (`BERVO:8000726`), with Facility (`BERVO:8000727`) beneath it for
ODM2's facility sites and Sewer (`BERVO:8000729`) for the three kinds of sewer.
Power plant (`BERVO:8000728`) gathers the hydroelectric and thermoelectric
plants under Facility. The five groupings carry ENVO cross-references where
ENVO has the class, and all of them are `8xxxxxx` concepts rather than
`9xxxxxx` grouping classes, since each is a thing a site can be on and a
context a variable can carry, as Chemical and Environmental material are.

## ODM2 concepts mapped to existing BERVO terms

| ODM2 concept | BERVO term | Note |
| --- | --- | --- |
| `Atmosphere` | Atmosphere (`BERVO:8000131`) | Moves under Environmental feature; gains `ENVO:01000810` |
| `Field, Pasture, Orchard, or Nursery` | Field (`BERVO:8000084`) | Moves under Land surface; gains `ENVO:00000114`; see below |
| `Lake, Reservoir, Impoundment` | Lake (`BERVO:8000285`) | Lake gains `reservoir` and `impoundment` as related synonyms and moves under Water body |
| `Land` | Land surface (`BERVO:8000134`) | Moves under Environmental feature; gains `ENVO:01001785` |
| `Subsurface` | Subsurface (`BERVO:8000053`) | Moves under Environmental feature; gains `ENVO:01000941` |

## New terms

| BERVO term | Parent | ODM2 concept | Other cross-reference |
| --- | --- | --- | --- |
| Water body (`BERVO:8000724`) | Environmental feature |  | `ENVO:00000063` |
| Landform (`BERVO:8000725`) | Environmental feature |  | `ENVO:01001886` |
| Human construction (`BERVO:8000726`) | Concept |  | `ENVO:00000070` |
| Facility (`BERVO:8000727`) | Human construction | `Facility` | `ENVO:03501288` |
| Power plant (`BERVO:8000728`) | Facility |  | `ENVO:00002214` |
| Sewer (`BERVO:8000729`) | Human construction |  |  |
| Stream (`BERVO:8000730`) | Water body | `Stream` | `ENVO:00000023` |
| Tidal stream (`BERVO:8000731`) | Stream | `Tidal stream` | `ENVO:00000412` |
| Wetland (`BERVO:8000732`) | Environmental feature | `Wetland` | `ENVO:00000043` |
| Estuary (`BERVO:8000733`) | Water body | `Estuary` | `ENVO:00000045` |
| Ocean (`BERVO:8000734`) | Water body | `Ocean` | `ENVO:00000015` |
| Coastal water (`BERVO:8000735`) | Water body | `Coastal` | `ENVO:02000049` |
| Canal (`BERVO:8000736`) | Water body and Human construction | `Canal` | `ENVO:00000014` |
| Ditch (`BERVO:8000737`) | Water body and Human construction | `Ditch` | `ENVO:00000037` |
| Spring (`BERVO:8000738`) | Landform | `Spring` | `ENVO:00000027` |
| Glacier (`BERVO:8000739`) | Environmental feature | `Glacier` | `ENVO:00000133` |
| Cave (`BERVO:8000740`) | Landform | `Cave` | `ENVO:00000067` |
| Outcrop (`BERVO:8000741`) | Landform | `Outcrop` | `ENVO:01000302` |
| Sinkhole (`BERVO:8000742`) | Landform | `Sinkhole` | `ENVO:00000195` |
| Playa (`BERVO:8000743`) | Landform | `Playa` | `ENVO:00000196` |
| Shore (`BERVO:8000744`) | Landform | `Shore` | `ENVO:00000304` |
| Volcanic vent (`BERVO:8000745`) | Landform | `Volcanic vent` | `ENVO:00000216` |
| Unsaturated zone (`BERVO:8000746`) | Subsurface | `Unsaturated zone` | `ENVO:00000328` |
| Cistern (`BERVO:8000747`) | Human construction | `Cistern` |  |
| Combined sewer (`BERVO:8000748`) | Sewer | `Combined sewer` |  |
| Storm sewer (`BERVO:8000749`) | Sewer | `Storm sewer` |  |
| Wastewater sewer (`BERVO:8000750`) | Sewer | `Wastewater sewer` |  |
| Septic system (`BERVO:8000751`) | Human construction | `Septic system` |  |
| Water distribution system (`BERVO:8000752`) | Human construction | `Water-distribution system` |  |
| Groundwater drain (`BERVO:8000753`) | Human construction | `Groundwater drain` |  |
| Underground excavation (`BERVO:8000754`) | Human construction | `Tunnel, shaft, or mine` |  |
| Soil pit (`BERVO:8000755`) | Human construction | `Soil hole` |  |
| Water diversion (`BERVO:8000756`) | Human construction | `Diversion` |  |
| Outfall (`BERVO:8000757`) | Human construction | `Outfall` |  |
| Pavement (`BERVO:8000758`) | Human construction | `Pavement` | `ENVO:01001272` |
| Animal waste lagoon (`BERVO:8000759`) | Facility | `Animal waste lagoon` |  |
| Golf course (`BERVO:8000760`) | Land surface | `Golf course` |  |
| House (`BERVO:8000761`) | Facility | `House` | `ENVO:01000417` |
| Hydroelectric plant (`BERVO:8000762`) | Power plant | `Hydroelectric plant` |  |
| Thermoelectric plant (`BERVO:8000763`) | Power plant | `Thermoelectric plant` |  |
| Laboratory (`BERVO:8000764`) | Facility | `Laboratory or sample-preparation area` | `ENVO:01001406` |
| Landfill (`BERVO:8000765`) | Landform | `Landfill` | `ENVO:00000533` |
| Wastewater treatment plant (`BERVO:8000766`) | Facility | `Wastewater-treatment plant` | `ENVO:00002043` |
| Water supply treatment plant (`BERVO:8000767`) | Facility | `Water-supply treatment plant` |  |
| Water-use establishment (`BERVO:8000768`) | Facility | `Water-use establishment` |  |
| Wastewater land application site (`BERVO:8000769`) | Land surface | `Wastewater land application` |  |

## Not mapped

Seven concepts are conveniences of the ODM2 database rather than kinds of
place, and are left out:

- `Unknown` is a placeholder.
- `Composite` is an aggregation of co-located sampling features at one point,
  such as a gauge, a weather station, and a well together.
- `Aggregate groundwater use`, `Aggregate surface-water-use`, and
  `Aggregate water-use establishment` are USGS water-use accounting classes
  that stand for many sites summed over an area.
- `Network infrastructure` is telemetry hardware such as a radio repeater.
- `Critical Zone Observatories` names a funding programme's network of sites,
  not a kind of site.

## Points to note

- Canal and Ditch have Water body as `Category` and Human construction as a
  second parent through `Parents`, since each is both. Pavement, Cistern, and
  the rest of the built list are constructions only.
- Wetland and Glacier sit directly under Environmental feature. ODM2 files
  wetland under its surface water sites and ENVO files it under vegetated
  area; ENVO files glacier under masses of environmental material. Neither is
  a water body or a landform in a way a reviewer would not argue with, so they
  are left at the top.
- Spring, Cave, and Shore follow ENVO under Landform. Outcrop and Sinkhole
  join them; ENVO classes outcrop as a portion of material, which is not a
  distinction BERVO draws.
- Land surface (`BERVO:8000134`) had no children before and now has Field,
  Golf course, and Wastewater land application site, each a tract of land.
  Its definition was a mass noun, the solid portion of the Earth's surface,
  and a golf course is not that. It is reworded distributively, as an area of
  that surface from the whole down to a single tract, and the sentence on
  energy exchange moves to its `Comment`. `terrain` stays as an exact synonym
  and `ENVO:01001785` (land) stays as the reference; both read as the whole,
  and the subclass reading is BERVO's own. ENVO does not file `agricultural
  field` under `land` either; its parent there is `field` (`ENVO:01000352`).
  Field under Land surface is BERVO's choice, not ENVO's, unlike Landfill
  under Landform.
- Atmosphere, Land surface, and Subsurface move from Concept to Environmental
  feature. Each is already used as a `contexts` value (23, 0, and 30 times),
  and the move changes none of those. ENVO makes the atmosphere and the
  geographic features alike parts of an astronomical body, which is the sense
  in which they are siblings here.
- Lake takes ODM2's `Lake, Reservoir, Impoundment` and gains `reservoir` and
  `impoundment` as related synonyms. ENVO keeps reservoir (`ENVO:00000025`) as
  a separate artificial water body; BERVO has no call for that split yet.
- ODM2's `Field, Pasture, Orchard, or Nursery` maps to Field
  (`BERVO:8000084`). Field's old definition also covered open land
  "supporting natural vegetation", which neither ODM2 nor ENVO's
  `agricultural field` (`ENVO:00000114`) includes. It is narrowed to land
  managed for agricultural use, whether cropped, grazed, planted as an
  orchard, or run as a nursery, so that it says what both cross-references
  say. `agricultural field` is an exact synonym and `pasture`, `orchard`,
  `nursery`, and `cropland` are related synonyms, recording ODM2's lumping.
  If a pasture or an orchard ever needs its own term it goes under Field.
- ODM2's `Tunnel, shaft, or mine` becomes Underground excavation, with
  `tunnel`, `shaft`, and `mine` as related synonyms. ENVO has each of the three
  as a separate class and none for their union, so no ENVO reference is made.
- ODM2's `Soil hole` becomes Soil pit, the name in common use, with `soil hole`
  as an exact synonym.
- ODM2's `Laboratory or sample-preparation area` becomes Laboratory, with
  `sample preparation area` as a related synonym.
- ODM2's `Coastal` becomes Coastal water, a marine water body, following ENVO's
  `coastal water body`. `Diversion` becomes Water diversion, and
  `Wastewater land application` becomes Wastewater land application site, so
  the labels read as things rather than acts.
- Outfall and Water diversion sit side by side under Human construction. ODM2
  files one under facility sites and the other under surface water sites; they
  are mirror images and are kept together.
- Golf course, Landfill, and Wastewater land application site are areas of
  land rather than assembled structures, and they follow ENVO rather than
  ODM2's facility grouping. ENVO files landfill (`ENVO:00000533`) as a
  depressed landform, so Landfill sits under Landform. ENVO has no golf
  course class and names golf courses in its `area of developed open space`
  (`ENVO:01000883`), a land-use zone; that class is wider than a golf course
  and is not cross-referenced. Golf course and Wastewater land application
  site sit under Land surface beside Field, as tracts of land under a use.
- ENVO's `alkaline flat` (`ENVO:00000196`) lists `playa` as a synonym and is
  the reference for Playa.
- `fumarole` is a related synonym of Volcanic vent, not an exact one. ODM2
  says "also known as fumarole", and ENVO's `fumarole` (`ENVO:00000216`) is
  the reference, but in geological usage a vent is the wider term.
- Five new labels use "plant" in the industrial sense: Power plant,
  Hydroelectric plant, Thermoelectric plant, Wastewater treatment plant, and
  Water supply treatment plant. Plant (`BERVO:8000021`) is the organism. The
  labels are distinct and the validator is content; a lexical matcher over
  BERVO labels will need to know the two senses.
- Facility and its children, the plants, the laboratory, the house, and the
  water-use establishment, reach further from earth systems modelling than
  the rest of BERVO. They are here so that a dataset's ODM2 site type can
  always be expressed; they can be pruned if that turns out not to matter.
