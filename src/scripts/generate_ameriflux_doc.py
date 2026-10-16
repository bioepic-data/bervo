"""Generate docs/ameriflux-alignment.md from bervo-src.csv and the AmeriFlux variable lists.

Run with `just ameriflux-doc`, or from any directory:

    python3 src/scripts/generate_ameriflux_doc.py

Inputs, in src/scripts/ameriflux/:

- fp_var.tsv: the AmeriFlux FP-Standard base names, from https://amfcdn.lbl.gov/api/v1/fp_var
- fluxnet_vars.tsv: the FLUXNET FULLSET variables, from
  https://fluxnet.org/data/fluxnet2015-dataset/fullset-data-product/
- badm_classified.tsv: each field of the BADM legacy list, sorted into the five classes the
  page counts, from
  https://raw.githubusercontent.com/chuhousen/amerifluxr/master/data-summary/AMF_AA-Net_BIF_LEGACY_VARIABLE-AVAILABILITY_LATEST.csv
- page_template.md: the hand-written text of the page, with {{PLACEHOLDERS}} for the tables

The tables are built from the AmeriFlux and BADM notes in the Comment column of bervo-src.csv.
Coverage problems, such as a base name no term records, are printed and make the script
exit non-zero, after the page has been written.
"""
import csv
import pathlib
import re
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
S = REPO_ROOT / "src" / "scripts" / "ameriflux"
OUT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else REPO_ROOT / "docs" / "ameriflux-alignment.md"
rows = list(csv.reader(open(REPO_ROOT / "src" / "ontology" / "bervo-src.csv", newline="", encoding="utf-8")))
H = {c: i for i, c in enumerate(rows[0])}
TERMS = [r for r in rows[2:] if r[H["obsolete"]] != "true"]
BY_LABEL = {r[1]: r for r in TERMS}
problems = []


def ref(label):
    if label not in BY_LABEL:
        problems.append(f"no BERVO term labelled {label!r}")
        return f"`{label}` (missing)"
    return f"`{BY_LABEL[label][0]}` {label}"


# ---------------------------------------------------------------- FP base names
fp = list(csv.DictReader(open(S / "fp_var.tsv", encoding="utf-8"), delimiter="\t"))
fp_codes = {r["Name"] for r in fp}
primary, noted = {}, {}
for r in TERMS:
    c = r[H["Comment"]]
    for m in re.finditer(r"AmeriFlux FP-Standard base names?: (.+?)\.(?: |$)", c):
        for code in re.findall(r"[A-Z][A-Z0-9_]*", m.group(1)):
            if code in fp_codes:
                primary.setdefault(code, []).append(r)
for r in TERMS:
    c = r[H["Comment"]]
    if "AmeriFlux" not in c:
        continue
    for code in fp_codes - set(primary):
        if re.search(rf"(?<![A-Za-z0-9_]){re.escape(code)}(?![A-Za-z0-9_])", c):
            noted.setdefault(code, []).append(r)
missing = sorted(fp_codes - set(primary) - set(noted))
if missing:
    problems.append(f"FP base names with no BERVO term: {missing}")

STAT = {"_SIGMA": "Standard deviation", "WS_MAX": "Maximum"}


def how_noted(code):
    if code.endswith("_SIGMA"):
        return "base term + `Standard deviation` qualifier"
    if code == "WS_MAX":
        return "base term + `Maximum` qualifier"
    if code.startswith("TIMESTAMP"):
        return "recorded on the concept"
    return "noted on the term"


fp_lines = ["| Group | Code | AmeriFlux description | AmeriFlux units | BERVO term | How |",
            "| --- | --- | --- | --- | --- | --- |"]
for r in sorted(fp, key=lambda r: (r["Type"], r["Name"])):
    code = r["Name"]
    if code in primary:
        terms = primary[code]
        how = "synonym" if any(code in t[H["Related Synonyms"]].split("|") or code in t[H["Exact Synonyms"]].split("|") or code.lower() == t[1].lower() for t in terms) else "`Comment` only"
    else:
        terms = noted.get(code, [])
        how = how_noted(code)
    cell = "<br>".join(f"`{t[0]}` {t[1]}" for t in terms) or "**none**"
    desc = r["Description"].replace("|", "/")
    fp_lines.append(f"| {r['Type']} | `{code}` | {desc} | {r['Units']} | {cell} | {how} |")
n_fp = len(fp_codes) - len(missing)

# ---------------------------------------------------------------- FLUXNET FULLSET
fl = list(csv.DictReader(open(S / "fluxnet_vars.tsv", encoding="utf-8"), delimiter="\t"))
artefacts = [r for r in fl if not re.fullmatch(r"[A-Z0-9_#]+", r["name"])]
fl = [r for r in fl if r not in artefacts]

BASE = [  # longest prefix first
    ("TIMESTAMP_START", "DateTime"), ("TIMESTAMP_END", "DateTime"), ("TIMESTAMP", "DateTime"),
    ("SW_IN_POT", "Potential incoming shortwave radiation"), ("SW_IN", "Incoming shortwave radiation"),
    ("LW_IN", "Sky longwave radiation"), ("SW_DIF", "Diffuse shortwave radiation"),
    ("SW_OUT", "Outgoing shortwave radiation"), ("LW_OUT", "Outgoing longwave radiation"),
    ("PPFD_IN", "Photosynthetic photon flux density"), ("PPFD_DIF", "Diffuse photosynthetically active radiation"),
    ("PPFD_OUT", "Outgoing photosynthetically active radiation"), ("NETRAD", "Net radiation"),
    ("TA", "Air temperature"), ("VPD", "Vapor pressure deficit"), ("PA", "Atmospheric pressure"),
    ("P", "Precipitation amount"), ("WS", "Measured wind speed"), ("WD", "Near-surface wind direction"),
    ("RH", "Air relative humidity"), ("USTAR", "Friction velocity"),
    ("CO2", "Carbon dioxide mole fraction in wet air"), ("TS", "Soil temperature"), ("SWC", "Volumetric water content"),
    ("G", "Soil heat flux at measurement depth"), ("LE", "Latent heat flux"), ("H", "Sensible heat flux"),
    ("EBC_CF", "Energy balance closure correction factor"), ("NEE", "Net ecosystem exchange"),
    ("RECO", "Ecosystem respiration flux"), ("GPP", "Gross primary production rate"),
    ("NIGHT_RANDUNC", "Net ecosystem exchange"), ("DAY_RANDUNC", "Net ecosystem exchange"),
    ("NIGHT_D", None), ("DAY_D", None), ("NIGHT", "Nighttime flag"),
]
TOK = {
    "F": ["Gap-filled"], "MDS": ["Marginal distribution sampling"], "ERA": ["Reanalysis downscaling"],
    "JSB": [], "CORR": ["Energy balance closure correction"],
    "CUT": ["Constant friction velocity threshold"], "VUT": ["Variable friction velocity threshold"],
    "REF": ["Reference ensemble member"], "USTAR50": ["Median", "Friction velocity threshold"],
    "MEAN": ["Mean"], "SE": ["Standard error"], "XX": ["Percentile"], "25": ["Percentile"], "75": ["Percentile"],
    "NIGHT": ["Nighttime", "Mean"], "DAY": ["Daytime", "Mean"], "SD": ["Standard deviation"],
    "RANDUNC": ["Random uncertainty"], "JOINTUNC": ["Joint uncertainty"], "METHOD": ["Method"],
    "N": ["Sample size"], "NT": ["Nighttime flux partitioning"], "DT": ["Daytime flux partitioning"],
    "SR": ["Sundown respiration partitioning"], "#": [],
}
NOTES = {"JSB": "calculated with the JSBACH algorithm; no concept", "#": "layer index, deepest last; not modelled",
         "25": "25th percentile", "75": "75th percentile"}
fl_lines = ["| Section | FLUXNET variable | Units | BERVO term | Qualifiers and concepts | Notes |",
            "| --- | --- | --- | --- | --- | --- |"]
n_fl = 0
for r in fl:
    name = r["name"]
    base = next(((p, l) for p, l in BASE if name == p or name.startswith(p + "_")), None)
    if base is None:
        problems.append(f"FLUXNET variable with no base: {name}")
        continue
    prefix, label = base
    rest = name[len(prefix):].lstrip("_")
    toks = [t for t in rest.split("_") if t] if rest else []
    quals, notes = [], []
    qc = False
    for t in toks:
        if t == "QC":
            qc = True
            continue
        if t not in TOK:
            problems.append(f"{name}: unknown token {t}")
            continue
        quals += TOK[t]
        if t in NOTES:
            notes.append(NOTES[t])
    if prefix in ("NIGHT_D", "DAY_D"):
        quals = ["Count", "Nighttime" if prefix == "NIGHT_D" else "Daytime"]
        notes.append("number of half-hours in the period")
    if prefix in ("NIGHT_RANDUNC", "DAY_RANDUNC"):
        quals = ["Nighttime" if prefix.startswith("NIGHT") else "Daytime", "Random uncertainty", "Sample size"]
    if name == "RECO_SR_N":
        quals = ["Sundown respiration partitioning", "Fraction"]
        notes.append("fraction of the period's data available to fit the respiration model")
    if name.startswith("EBC_CF") and toks == ["N"]:
        notes.append("number of values used to compute the factor")
    # a qualifier mentioned twice (e.g. Mean from both _NIGHT and _MEAN) is listed once
    seen = []
    for q in quals:
        if q not in seen:
            seen.append(q)
    for q in seen:
        if q not in BY_LABEL:
            problems.append(f"{name}: qualifier label {q!r} is not a BERVO term")
    term = ref(label) if label else "none"
    if qc:
        notes.insert(0, f"flag for {label}" if label else "flag")
        term = ref("Quality control flag")
    n_fl += 1
    fl_lines.append(f"| {r['section'].title()} | `{name}` | {r['units']} | {term} | {', '.join(seen)} | {'; '.join(notes)} |")

# ---------------------------------------------------------------- concepts added for FLUXNET
CONCEPTS = ["Gap-filling method", "Marginal distribution sampling", "Reanalysis downscaling",
            "Flux partitioning method", "Nighttime flux partitioning", "Daytime flux partitioning",
            "Sundown respiration partitioning", "Energy balance closure correction",
            "Constant friction velocity threshold", "Variable friction velocity threshold",
            "Random uncertainty", "Joint uncertainty", "Percentile", "Reference ensemble member",
            "Daytime", "Nighttime", "Potential incoming shortwave radiation", "Friction velocity threshold",
            "Energy balance closure correction factor", "Nighttime flag"]
c_lines = ["| Term | Parent | Describes |", "| --- | --- | --- |"]
for l in CONCEPTS:
    t = BY_LABEL.get(l)
    if not t:
        problems.append(f"missing concept {l}")
        continue
    c_lines.append(f"| `{t[0]}` {l} | {t[2]} | {t[H['Comment']] or ''} |")

QUAL = [("_PI", "Processed by site team", "concept"), ("_QC", "Quality control flag", "existing term"),
        ("_F", "Gap-filled", "concept"), ("_IU", None, "not modelled: instrument units, an upload convention"),
        ("_H_V_R", None, "not modelled: relative position indices of a sensor at one site"),
        ("_H_V_A", "Mean", "existing concept: average across replicate sensors"),
        ("_#", None, "not modelled: layer index of an aggregated profile"),
        ("_SD", "Standard deviation", "existing concept: spread across replicate sensors"),
        ("_N", "Sample size", "concept: number of replicate sensors averaged")]
q_lines = ["| Qualifier | BERVO term | Note |", "| --- | --- | --- |"]
for q, l, n in QUAL:
    q_lines.append(f"| `{q}` | {ref(l) if l else '—'} | {n} |")

# ---------------------------------------------------------------- BADM site metadata


def badm_section():
    """The BADM section, from the BADM notes in Comment and the field classes in badm_classified.tsv."""
    import collections
    by_id = {r[0]: r for r in TERMS}
    variables = []  # (code, id, label, how)
    values = collections.defaultdict(list)  # list name -> [(value, id, label)]
    mapped = []  # (list name, value, id, label)
    end = r"(.+?)\.(?=\s|$)"
    for r in TERMS:
        c = r[H["Comment"]]
        for m in re.finditer(r"AmeriFlux BADM variable names?: " + end, c):
            for code in m.group(1).split(", "):
                variables.append((code.strip(), r[0], r[1], "current standard"))
        for m in re.finditer(r"Legacy BADM variable names?: " + end, c):
            for code in m.group(1).split(", "):
                variables.append((code.strip(), r[0], r[1], "legacy"))
        for m in re.finditer(r"Legacy BADM variables mapped here, with the variant in contexts or qualifiers: " + end, c):
            for code in m.group(1).split(", "):
                variables.append((code.strip(), r[0], r[1], "legacy, variant in contexts or qualifiers"))
        for m in re.finditer(r"AmeriFlux BADM ([A-Z_ ]+?(?: and [A-Z_]+)?) values?: " + end, c):
            for lst in m.group(1).split(" and "):
                values[lst.strip()].append((m.group(2).strip(), r[0], r[1]))
        for m in re.finditer(r"The ([A-Z_]+) values? (.+?) maps? to (.+?) \((BERVO:\d+)\)", c):
            mapped.append((m.group(1), m.group(2), m.group(4), by_id[m.group(4)][1]))
    with open(S / "badm_classified.tsv", encoding="utf-8") as f:
        cls = collections.Counter(line.split("\t")[1].strip() for line in f.read().splitlines()[1:])

    out = []
    w = out.append
    w("## BADM site metadata\n")
    w("BADM (Biological, Ancillary, Disturbance and Metadata) records what a site is like: its")
    w("vegetation, soils, climate, disturbance history and management. The fields come from the")
    w("BADM standard (<https://ameriflux.lbl.gov/data/badm/badm-standards/>) and the legacy")
    w("field list above. Each field of the legacy list was sorted into one of five classes:\n")
    w("| Class | Fields (legacy list) | In BERVO |")
    w("| --- | --- | --- |")
    names = {"a_quantity": "Quantities and site properties", "e_disturbance": "Disturbance and management",
             "b_metadata": "Measurement metadata: dates, method, statistic, organ, species, depth range, comment",
             "c_admin": "Administrative: DOIs, team members, addresses, acknowledgement, funding",
             "d_instrument": "Instrument settings (`INST_*`, `INSTPAIR_*`)"}
    for k in ("a_quantity", "e_disturbance", "b_metadata", "c_admin", "d_instrument"):
        w(f"| {names[k]} | {cls.get(k, 0)} | {'yes' if k in ('a_quantity', 'e_disturbance') else 'no'} |")
    w("")
    w("Measurement metadata, administrative fields and instrument settings describe a dataset")
    w("rather than a quantity, so they have no terms. Where a metadata field names a layer, organ")
    w("or status of a quantity, that becomes `contexts` or `qualifiers` on the general term,")
    w("following decision 6.\n")
    w("### Variables\n")
    w("The class counts above are of the legacy list. The table below also has the fields of the")
    w("current standard that the legacy list lacks, so it has more rows than the two in-scope")
    w("classes. A *legacy* code is a field of the older list only. Where the current standard")
    w("folds several legacy fields into one general field, they map to the general term with the")
    w("variant in `contexts` or `qualifiers`.\n")
    w("| BADM variable | BERVO term | Note |")
    w("| --- | --- | --- |")
    seen = set()
    for code, tid, label, how in sorted(variables):
        if (code, tid) in seen:
            continue
        seen.add((code, tid))
        w(f"| `{code}` | `{tid}` {label} | {how} |")
    w("")
    w("### Value lists\n")
    w("Every BADM controlled vocabulary is a set of BERVO concepts (decision 7).\n")
    for lst in sorted(values):
        w(f"#### {lst}\n")
        w("| BADM value | BERVO concept |")
        w("| --- | --- |")
        for v, tid, label in sorted(values[lst]):
            w(f"| {v} | `{tid}` {label} |")
        w("")
    if mapped:
        w("### Values that map to existing concepts\n")
        w("| List | BADM value | BERVO concept |")
        w("| --- | --- | --- |")
        for lst, v, tid, label in sorted(set(mapped)):
            w(f"| {lst} | {v} | `{tid}` {label} |")
        w("")
    print(f"BADM variables {len(seen)}, value lists {len(values)}, "
          f"values {sum(len(v) for v in values.values())}, mapped to existing {len(set(mapped))}", file=sys.stderr)
    return "\n".join(out)


TEXT = (S / "page_template.md").read_text(encoding="utf-8")
out = (TEXT.replace("{{FP_TABLE}}", "\n".join(fp_lines))
       .replace("{{FP_COVERED}}", f"{n_fp} of {len(fp_codes)}")
       .replace("{{QUAL_TABLE}}", "\n".join(q_lines))
       .replace("{{CONCEPT_TABLE}}", "\n".join(c_lines))
       .replace("{{FLUXNET_TABLE}}", "\n".join(fl_lines))
       .replace("{{FL_COVERED}}", f"{n_fl} of {len(fl)}")
       .replace("{{ARTEFACTS}}", str(len(artefacts)))
       .replace("{{BADM_SECTION}}", badm_section()))
OUT.write_text(out, encoding="utf-8")
for p in problems:
    print("PROBLEM:", p, file=sys.stderr)
print(f"wrote {OUT}", file=sys.stderr)
print(f"FP covered {n_fp}/{len(fp_codes)}; FLUXNET mapped {n_fl}/{len(fl)}; artefact rows skipped {len(artefacts)}", file=sys.stderr)
sys.exit(1 if problems else 0)
