"""Generate docs/try-alignment.md from the TRY alignment map and bervo-src.csv.

Run with `just try-doc`, or from any directory:

    python3 src/scripts/generate_try_doc.py

Inputs, in src/scripts/try/:

- try_traits.csv: the TRY trait list attached to issue #27 (trait_id, trait_name)
- try_alignment.tsv: the curated map, one row per TRY trait
- page_template.md: the hand-written text of the page, with {{PLACEHOLDERS}} for the tables

The map and the template must agree: a `match` or `broader` row names a term whose Comment
lists the trait ID in the matching sentence, and every TRY trait ID in a Comment has such a
row. Disagreements are printed and make the script exit non-zero, after the page has been
written.
"""
import collections
import csv
import pathlib
import re
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
S = REPO_ROOT / "src" / "scripts" / "try"
OUT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else REPO_ROOT / "docs" / "try-alignment.md"
rows = list(csv.reader(open(REPO_ROOT / "src" / "ontology" / "bervo-src.csv", newline="", encoding="utf-8-sig")))
H = {c: i for i, c in enumerate(rows[0])}
TERMS = {r[0]: r for r in rows[2:]}
STATUSES = ["match", "broader", "related", "gap", "species_attribute"]
MAPPED = {"match", "broader", "related"}
# The two Comment sentences, as written by curators; see src/scripts/try/README.md.
SENTENCES = {
    "match": re.compile(r"TRY trait IDs?: ([0-9, ]+)\."),
    "broader": re.compile(r"TRY traits mapped here, with the organ or status in contexts: ([0-9, ]+)\."),
}
problems = []

traits = list(csv.DictReader(open(S / "try_traits.csv", encoding="utf-8")))
amap = list(csv.DictReader(open(S / "try_alignment.tsv", encoding="utf-8"), delimiter="\t"))

# ------------------------------------------------------------- map against the TRY list
names = {t["trait_id"]: t["trait_name"] for t in traits}
seen = collections.Counter(r["trait_id"] for r in amap)
for tid, n in seen.items():
    if n > 1:
        problems.append(f"TRY trait {tid} has {n} rows in try_alignment.tsv")
for tid in names.keys() - seen.keys():
    problems.append(f"TRY trait {tid} is missing from try_alignment.tsv")
for r in amap:
    tid = r["trait_id"]
    if tid not in names:
        problems.append(f"try_alignment.tsv row {tid} is not in try_traits.csv")
    elif r["trait_name"] != names[tid]:
        problems.append(f"TRY trait {tid}: name differs from try_traits.csv")
    if r["status"] not in STATUSES:
        problems.append(f"TRY trait {tid}: unknown status {r['status']!r}")
    if not r["group"]:
        problems.append(f"TRY trait {tid}: no group")
    b = r["bervo_id"]
    if (r["status"] in MAPPED) != bool(b):
        problems.append(f"TRY trait {tid}: status {r['status']} with bervo_id {b!r}")
    if b and b not in TERMS:
        problems.append(f"TRY trait {tid}: {b} is not a BERVO term")
    elif b and TERMS[b][H["obsolete"]] == "true":
        problems.append(f"TRY trait {tid}: {b} is obsolete")

# A note that BERVO lacks a concept goes stale once a slice adds it, and a note naming the
# concept for contexts must name one that exists.
LABELS = {t[1].casefold() for t in TERMS.values() if t[H["obsolete"]] != "true"}


def as_labels(names):
    """True if names reads as labels joined by ', ' and a final ' and ', so a label that
    itself contains ' and ' or a comma is not split."""
    if names.casefold() in LABELS:
        return True
    for sep in (", ", " and "):
        for i in [m.start() for m in re.finditer(re.escape(sep), names)]:
            if names[:i].casefold() in LABELS and as_labels(names[i + len(sep):]):
                return True
    return False


for r in amap:
    m = re.search(r"BERVO has no (.+?) concept yet\.", r["note"])
    if m and m.group(1).casefold() in LABELS:
        problems.append(f"TRY trait {r['trait_id']}: note says BERVO has no {m.group(1)} concept, but it has one")
    # Every clause about contexts must read "X goes in contexts." or "X, Y and Z go in contexts."
    for clause in re.split(r"(?<=[.;]) ", r["note"]):
        if "in contexts" not in clause:
            continue
        m = re.fullmatch(r"(.+?) go(?:es)? in contexts[.;]", clause)
        if not m:
            problems.append(f"TRY trait {r['trait_id']}: note mentions contexts without naming the concepts: {clause!r}")
            continue
        for concept in [] if as_labels(m.group(1)) else re.split(r", | and ", m.group(1)):
            if concept.casefold() not in LABELS:
                problems.append(f"TRY trait {r['trait_id']}: note puts {concept} in contexts, but it is not a BERVO label")

# ------------------------------------------------------------- map against the Comments
from_map = {(r["status"], r["bervo_id"], r["trait_id"]) for r in amap if r["status"] in SENTENCES}
from_comments = set()
for tid, t in TERMS.items():
    for status, pat in SENTENCES.items():
        for m in pat.finditer(t[H["Comment"]]):
            for n in re.findall(r"[0-9]+", m.group(1)):
                from_comments.add((status, tid, n))
for status, b, tid in sorted(from_map - from_comments):
    problems.append(f"TRY trait {tid} is {status} to {b} in the map, but its Comment does not say so")
for status, b, tid in sorted(from_comments - from_map):
    problems.append(f"{b} Comment lists TRY trait {tid} as {status}, but the map does not")


def term(b):
    return f"`{b}` {TERMS[b][1]}" if b in TERMS else f"`{b}` (missing)"


def cell(s):
    """Escape a TRY name for a Markdown table cell, so it renders as written."""
    return re.sub(r"([\\|*_<`\[\]])", r"\\\1", s)


# ------------------------------------------------------------- tables
groups = sorted({r["group"] for r in amap})
count = collections.Counter((r["group"], r["status"]) for r in amap)
summary = ["| Group | " + " | ".join(f"`{s}`" for s in STATUSES) + " | Total |",
           "| --- |" + " ---: |" * (len(STATUSES) + 1)]
for g in groups:
    summary.append(f"| {g} | " + " | ".join(str(count[g, s] or "") for s in STATUSES)
                   + f" | {sum(count[g, s] for s in STATUSES)} |")
totals = collections.Counter(r["status"] for r in amap)
summary.append("| **Total** | " + " | ".join(f"**{totals[s]}**" for s in STATUSES) + f" | **{len(amap)}** |")


def by_status(status, with_note):
    head = "| TRY ID | TRY trait | BERVO term |" + (" Note |" if with_note else "")
    out = [head, "| ---: | --- | --- |" + (" --- |" if with_note else "")]
    for r in sorted((r for r in amap if r["status"] == status), key=lambda r: int(r["trait_id"])):
        line = f"| {r['trait_id']} | {cell(r['trait_name'])} | {term(r['bervo_id'])} |"
        out.append(line + (f" {cell(r['note'])} |" if with_note else ""))
    return out


broader = ["| BERVO term | TRY traits |", "| --- | --- |"]
grouped = collections.defaultdict(list)
for r in amap:
    if r["status"] == "broader":
        grouped[r["bervo_id"]].append(r)
for b in sorted(grouped):
    ts = sorted(grouped[b], key=lambda r: int(r["trait_id"]))
    broader.append(f"| {term(b)} | " + "; ".join(f"{r['trait_id']} {cell(r['trait_name'])}" for r in ts) + " |")

slots = collections.defaultdict(list)
for r in amap:
    if r["pft_slot"]:
        slots[r["pft_slot"]].append(r)
pft = ["| Schema slot | TRY trait | Status | BERVO term |", "| --- | --- | --- | --- |"]
for slot in sorted(slots):
    for r in sorted(slots[slot], key=lambda r: int(r["trait_id"])):
        pft.append(f"| `{slot}` | {r['trait_id']} {cell(r['trait_name'])} | `{r['status']}` | "
                   + (term(r["bervo_id"]) if r["bervo_id"] else "") + " |")

species = ["| TRY ID | TRY trait |", "| ---: | --- |"]
for r in sorted((r for r in amap if r["status"] == "species_attribute"), key=lambda r: int(r["trait_id"])):
    species.append(f"| {r['trait_id']} | {cell(r['trait_name'])} |")

TEXT = (S / "page_template.md").read_text(encoding="utf-8")
out = (TEXT.replace("{{N_TRAITS}}", str(len(traits)))
       .replace("{{N_MAPPED}}", str(sum(totals[s] for s in MAPPED)))
       .replace("{{N_GAP}}", str(totals["gap"]))
       .replace("{{N_SPECIES}}", str(totals["species_attribute"]))
       .replace("{{SUMMARY_TABLE}}", "\n".join(summary))
       .replace("{{MATCH_TABLE}}", "\n".join(by_status("match", True)))
       .replace("{{BROADER_TABLE}}", "\n".join(broader))
       .replace("{{RELATED_TABLE}}", "\n".join(by_status("related", True)))
       .replace("{{PFT_TABLE}}", "\n".join(pft))
       .replace("{{SPECIES_TABLE}}", "\n".join(species)))
OUT.write_text(out, encoding="utf-8")
for p in problems:
    print("PROBLEM:", p, file=sys.stderr)
print(f"wrote {OUT}", file=sys.stderr)
print("; ".join(f"{s} {totals[s]}" for s in STATUSES), file=sys.stderr)
sys.exit(1 if problems else 0)
