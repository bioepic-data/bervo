"""Build src/scripts/try/try_alignment.tsv, the map of TRY traits to BERVO (issue #27).

Run with `just try-doc`, which then rebuilds the page, or on its own from any directory:

    python3 src/scripts/build_try_alignment.py

Every row of src/scripts/try/try_traits.csv gets a group, a status, a BERVO term and a
plant-functional-traits schema slot. They come from three places, in this order:

1. MAPPED, the hand-curated rows. A trait listed there takes that status, term and note.
2. SPECIES_ATTR, a rule on the name for traits that record a species rather than a plant.
3. BROADER, rules on the name for organ contents and ratios that a general plant tissue
   term covers with the organ in contexts. EXCLUDE keeps out names that look alike but are
   not tissue contents.

Anything else is a gap. GROUPS assigns the group by the start of the name, first match wins.
To map a trait, add it to MAPPED (or widen a rule), run `just try-doc`, and put the
matching sentence on the term; generate_try_doc.py fails if the two disagree.
"""
import csv
import pathlib
import re
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
S = REPO_ROOT / "src" / "scripts" / "try"
OUT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else S / "try_alignment.tsv"

GROUPS = [
    ("Litter and woody debris", r"^(Litter|Coarse woody debris|CWD|Snag)"),
    ("Species ecology and distribution", r"^(Species (occurrence|range|habitat|US |phyto|strategy|light|understory|environmental indicator|status|invasion|important|soil|nutrient req|use$|yield)|Plant human usage)"),
    ("Species genetics and phylogeny", r"^Species (genotype|genom|phylogen)"),
    ("Photosynthesis and gas exchange", r"^(Photosynthesis|Stomata|Leaf (respiration|transpiration|isoprene|volatile|mesophyll conductance|cuticular conductance)|Plant respiration)"),
    ("Fine root", r"^Fine root|^Fibrous root"),
    ("Root", r"^(Root|Coarse root|Belowground|Rhizome|Mycorrhiza|Mycorhizza)"),
    ("Leaf", r"^(Leaf|leaf|Leaflet|Metamer: leaf|Paleo trait|Trap)"),
    ("Stem, wood and bark", r"^(Stem|Wood|Bark|Xylem|Tree ring|Tiller|Internode|Stolon|Spines|Resprout)"),
    ("Twig, branch, shoot and bud", r"^(Twig|Branch|Shoot|Bud)"),
    ("Seed, fruit and dispersal", r"^(Seed|Fruit|Dispersal|Diaspore|Infructescence)"),
    ("Flower and reproduction", r"^(Flower|Inflorescen|Pollen|Pollination|Reproductive|Cone|Plant reproductive)"),
    ("Moss and fern", r"^Moss"),
    ("Crown and canopy", r"^(Crown|Woody area index)"),
    ("Plot and stand", r"^Plot"),
    ("Whole plant", r"^(Plant|Species|Budbank|Metamer|Mycoheterotrophy|Tree mortality|Primary vs)"),
]

SPECIES_ATTR = r"^(Species (occurrence|range|habitat|US |phyto|environmental indicator|status|invasion|important|phylogen|use$|light (requirement|preference)|soil (pH|moisture) requirement|nutrient requirements)|Plant human usage|Plot dominant species|Leaf herbivore species)"

# Organ contents and ratios covered by a general term, with the organ in contexts.
BROADER = [
    (r"carbon(?: \(C\))? content per [\w\s(),-]*dry mass$", "BERVO:0002339"),
    (r"nitrogen \(N\) content per [\w\s(),-]*dry mass$", "BERVO:0002340"),
    (r"carbon/nitrogen \(C/N\)|\bC/N ratio", "BERVO:0002055"),
    (r"phos\w*rus \(P\) content per [\w\s(),-]*dry mass$", "BERVO:0002380"),  # TRY spells it "phosporus" once
    (r"nitrogen/phosphorus \(N/P\)|\bN/P ratio", "BERVO:0002381"),
]
# Look like tissue contents but are not: amounts per unit soil, microbial biomass, fractions...
EXCLUDE = r"soil dry mass|microbial|fungal|bacterial|labile|structural|soluble|TNC|non-structural|cellulose|lignin|isotope|versus| vs |per leaf nitrogen|cell wall|organic|ground area|per plant$|fraction"
# The concepts a broader row takes in contexts: its organ or part, and its status where the
# name gives one. First match wins, so each pattern carries the whole set for its name form,
# and the more specific forms come first. A broader row that matches none stops the builder.
CONTEXTS = [
    (r"^Litter (\(other|other)", ["Dead vegetation"]),  # mixed litter: twigs, bark, flowers...
    (r"^Litter \(fine root\)", ["Fine root", "Dead vegetation"]),
    (r"^Litter \(leaf\)", ["Leaf", "Dead vegetation"]),
    (r"^Litter \(cone", ["Cone", "Dead vegetation"]),
    (r"^Litter twig", ["Twig", "Dead vegetation"]),
    (r"^Litter", ["Dead vegetation"]),
    (r"^Coarse woody debris \(CWD\) root", ["Coarse woody debris", "Coarse root"]),
    (r"^Coarse woody debris \(CWD\) branch", ["Coarse woody debris", "Branch"]),
    (r"^Coarse woody debris \(CWD\) stem", ["Coarse woody debris", "Stem"]),
    (r"^Coarse woody debris", ["Coarse woody debris"]),
    (r"absorptive", ["Absorptive fine root"]),
    (r"\(transport\)", ["Transport fine root"]),
    (r"^Fine root", ["Fine root"]),
    (r"^Coarse root", ["Coarse root"]),
    (r"^Root", ["Root"]),
    (r"^Belowground", ["Belowground plant material"]),
    (r"^Bark: dead bark", ["Bark", "Dead vegetation"]),
    (r"^Branch bark", ["Bark", "Branch"]),
    (r"^Branch wood", ["Wood", "Branch"]),
    (r"^Bark", ["Bark"]),
    (r"^Branch", ["Branch"]),
    (r"^Twig", ["Twig"]),
    # Wood zones come after the organ prefixes, so a name with both, such as gap trait 171
    # "Stem, branch or twig sapwood ... (Huber value)", gets one concept; add a pattern for it
    # here, before ^Twig, when a slice maps it.
    (r"heartwood", ["Heartwood"]),
    (r"sapwood", ["Sapwood"]),
    (r"^Stem wood", ["Wood", "Stem"]),
    (r"^Wood", ["Wood"]),
    (r"^Stem", ["Stem"]),
    (r"^Shoot", ["Shoot"]),
    (r"^Leaf", ["Leaf"]),
    (r"^Reproductive organ", ["Reproductive structure"]),
    (r"^Cone", ["Cone"]),
    (r"^Fruit", ["Fruit"]),
    (r"^Trap", ["Carnivorous plant trap"]),
]

DECOMPOSITION = ("From litter decomposition studies, where the value may be taken at a stated time after "
                 "the start; check the TRY data release before mapping it to the static tissue term.")
WHOLE_PLANT = "Whole plant; the term covers whole plant material."


def ctx(*concepts):
    if len(concepts) == 1:
        return f"{concepts[0]} goes in contexts."
    return f"{', '.join(concepts[:-1])} and {concepts[-1]} go in contexts."


COTYLEDON = ctx("Cotyledon")


# (status, BERVO term, TRY trait IDs, note), grouped by term.
MAPPED = [
    # Leaf carbon and nitrogen (ESS-DIVE leaf terms, #171)
    ("match", "BERVO:0002188", "13", ""),
    ("broader", "BERVO:0002188", "674", COTYLEDON),
    ("broader", "BERVO:0002188", "3955", ctx("Leaf", "Senescent vegetation")),
    ("match", "BERVO:0002189", "14", ""),
    ("broader", "BERVO:0002189", "667", COTYLEDON),
    ("broader", "BERVO:0002189", "3954", ctx("Leaf", "Senescent vegetation")),
    ("match", "BERVO:0002187", "50", ""),
    ("match", "BERVO:0002186", "570", ""),
    ("match", "BERVO:0002185", "2950", "Reconstructed from fossil leaves; the quantity is the same."),
    # General plant tissue terms
    ("match", "BERVO:0002339", "3027", WHOLE_PLANT),
    ("related", "BERVO:0002339", "3521", DECOMPOSITION),
    ("match", "BERVO:0002340", "668", WHOLE_PLANT),
    ("related", "BERVO:0002340", "3522", DECOMPOSITION),
    ("match", "BERVO:0002055", "1021", "Whole plant; the term covers a whole plant."),
    ("related", "BERVO:0002055", "3527", DECOMPOSITION),
    ("match", "BERVO:0002380", "3028", WHOLE_PLANT),
    ("related", "BERVO:0002380", "3523", DECOMPOSITION),
    ("broader", "BERVO:0002381", "56", "Leaf goes in contexts."),
    ("related", "BERVO:0002381", "3529", DECOMPOSITION),
    # Existing terms: EcoSIM parameters and others
    ("match", "BERVO:0001884", "21", ""),
    ("match", "BERVO:0000705", "27", ""),
    ("match", "BERVO:0000704", "3042", ""),
    ("match", "BERVO:0000706", "3043", ""),
    ("match", "BERVO:0001077", "246", ""),
    ("match", "BERVO:0000787", "511", ""),
    ("match", "BERVO:0001967", "4025", ""),
    ("related", "BERVO:0002351", "6", "BERVO Rooting depth is for a plant community; TRY records it per plant or species."),
    ("related", "BERVO:8000785", "197", "BERVO has Plant functional type as a concept, not a variable whose value is a PFT."),
    ("related", "BERVO:0000835", "22", "The BERVO term distinguishes only C3 and C4; TRY includes CAM and intermediates."),
    ("related", "BERVO:0000176", "3402", "The BERVO term is water per unit leaf carbon, an EcoSIM parameter."),
    ("related", "BERVO:0001632", "3", "BERVO has only the cosine and sine of leaf angle, as canopy radiation parameters."),
    ("related", "BERVO:0002346", "4046", "The BERVO term is the increment at breast height over a stated period."),
    ("related", "BERVO:0000773", "437", "The BERVO term comes from a per-branch EcoSIM variable."),
    ("related", "BERVO:0000562", "3656", "An EcoSIM parameter; the mass basis is not stated as dry mass."),
    ("related", "BERVO:0000562", "504", "The BERVO term is per unit leaf mass, not per leaf area."),
    # Slice 2: the plant-functional-traits schema traits
    ("match", "BERVO:0002365", "18", ""),
    ("match", "BERVO:0002366", "3106", ""),
    ("match", "BERVO:0002367", "3107", ""),
    ("match", "BERVO:0002368", "3058 3108 3110 3112 3114", "TRY variants differ in whether the petiole is included."),
    ("related", "BERVO:0002368", "3109 3111 3113", "The area of one leaflet of a compound leaf, not of the whole leaf."),
    ("match", "BERVO:0002369", "3086 3115 3116 3117", "TRY variants differ in whether the petiole, rhachis and midrib are included."),
    ("related", "BERVO:0002369", "4083", "Uses the total leaf area rather than the one-sided area."),
    ("related", "BERVO:0002369", "125", "Per unit fresh mass rather than dry mass."),
    ("broader", "BERVO:0002369", "69", ctx("Leaf", "Dead vegetation")),
    ("match", "BERVO:0002370", "47", ""),
    ("broader", "BERVO:0002370", "3055", COTYLEDON),
    ("match", "BERVO:0002371", "4 3764", ""),
    ("broader", "BERVO:0002371", "3473 3877", "Branch goes in contexts."),
    ("broader", "BERVO:0002371", "1204", ctx("Twig", "Branch")),
    ("broader", "BERVO:0002371", "3736", ctx("Twig")),
    ("broader", "BERVO:0002371", "3452", ctx("Heartwood")),
    ("broader", "BERVO:0002371", "3472", ctx("Sapwood")),
    ("match", "BERVO:0002372", "26", ""),
    ("match", "BERVO:0002373", "233", ""),
    ("match", "BERVO:0002374", "1080", ""),
    ("broader", "BERVO:0002374", "614", "Fine root goes in contexts."),
    ("broader", "BERVO:0002374", "1550", "Coarse root goes in contexts."),
    ("broader", "BERVO:0002374", "2062", ctx("Absorptive fine root")),
    ("broader", "BERVO:0002374", "2318", ctx("Transport fine root")),
    ("match", "BERVO:0002375", "83", ""),
    ("broader", "BERVO:0002375", "896", "Fine root goes in contexts."),
    ("broader", "BERVO:0002375", "1526", "Coarse root goes in contexts."),
    ("broader", "BERVO:0002375", "2038", ctx("Absorptive fine root")),
    ("broader", "BERVO:0002375", "2294", ctx("Transport fine root")),
    ("match", "BERVO:0002376", "82 116", ""),
    ("broader", "BERVO:0002376", "1781", "Fine root goes in contexts."),
    ("broader", "BERVO:0002376", "1525", "Coarse root goes in contexts."),
    ("broader", "BERVO:0002376", "2037", ctx("Absorptive fine root")),
    ("broader", "BERVO:0002376", "2293", ctx("Transport fine root")),
    ("match", "BERVO:0002377", "38", ""),
    ("match", "BERVO:0002378", "42 3400 3401", "TRY variants differ in their value lists."),
    ("match", "BERVO:0002379", "43", ""),
    # Slice 3: leaf economics and photosynthesis
    ("match", "BERVO:0002382", "15", ""),
    ("match", "BERVO:0002383", "51", ""),
    ("match", "BERVO:0002384", "53", ""),
    ("match", "BERVO:0002385", "40", ""),
    ("match", "BERVO:0002386", "54", ""),
    ("match", "BERVO:0002387", "41", ""),
    ("match", "BERVO:0002388", "186", ""),
    ("match", "BERVO:0002389", "185", ""),
    ("match", "BERVO:0002390", "269", ""),
    ("match", "BERVO:0002391", "270", ""),
    ("match", "BERVO:0002392", "45", ""),
    ("match", "BERVO:0002393", "12", ""),
    ("match", "BERVO:0002394", "46", ""),
    ("match", "BERVO:0002395", "48", ""),
    ("match", "BERVO:0002396", "55", ""),
    ("broader", "BERVO:0002396", "3050", COTYLEDON),
    ("match", "BERVO:0002397", "37", ""),
]

# The plant-functional-traits schema slot each TRY trait feeds
# (bioepic-data/plant-functional-traits, src/plant_functional_traits/schema/, at d083f09).
PFT_SLOTS = {
    "plant_height": "18 3106 3107",
    "stem_specific_density": "4 3764",
    "leaf_area": "3108 3109 3110 3111 3112 3113 3114",
    "leaf_nitrogen_content": "14",
    "diaspore_mass": "26 233",
    "specific_leaf_area": "3115 3116 3117",
    "leaf_dry_matter_content": "47",
    "specific_root_length": "1080 614",
    "root_diameter": "83 896",
    "root_tissue_density": "82 1781",
    "root_nitrogen_content": "80 475",
    "woodiness": "38",
    "growth_form": "42 3400 3401",
    "leaf_type": "43",
}

curated = {}
for status, term, ids, note in MAPPED:
    for tid in ids.split():
        if tid in curated:
            sys.exit(f"TRY trait {tid} is listed twice in MAPPED")
        curated[tid] = (status, term, note)
slot_of = {}
for slot, ids in PFT_SLOTS.items():
    for tid in ids.split():
        if tid in slot_of:
            sys.exit(f"TRY trait {tid} is in two PFT_SLOTS entries, {slot_of[tid]} and {slot}")
        slot_of[tid] = slot


def broader_term(name):
    if re.search(EXCLUDE, name):
        return None
    return next((term for pat, term in BROADER if re.search(pat, name)), None)


with open(S / "try_traits.csv", encoding="utf-8") as f:
    traits = list(csv.DictReader(f))
known = {t["trait_id"] for t in traits}
for what, ids in (("MAPPED", curated.keys()), ("PFT_SLOTS", slot_of.keys())):
    if ids - known:
        sys.exit(f"{what} names TRY traits that are not in try_traits.csv: {sorted(ids - known, key=int)}")

with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["trait_id", "trait_name", "group", "status", "bervo_id", "pft_slot", "note"])
    for t in traits:
        tid, name = t["trait_id"], t["trait_name"]
        group = next((g for g, pat in GROUPS if re.match(pat, name)), "Other")
        status, term, note = "gap", "", ""
        if tid in curated:
            status, term, note = curated[tid]
        elif re.match(SPECIES_ATTR, name):
            status = "species_attribute"
        elif term := broader_term(name):
            status = "broader"
            concepts = next((c for pat, c in CONTEXTS if re.search(pat, name)), None)
            if concepts is None:
                sys.exit(f"TRY trait {tid} is broader, but no CONTEXTS pattern names its organ: {name}")
            note = ctx(*concepts)
        w.writerow([tid, name, group, status, term, slot_of.get(tid, ""), note])
print(f"wrote {OUT}", file=sys.stderr)
