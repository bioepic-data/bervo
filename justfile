# BERVO command surface.
#
# These recipes are the supported entry points for both humans and agents.
# `just --list` shows everything; see AGENTS.md for the workflow around them.

set shell := ["bash", "-uc"]

ontology_dir := "src/ontology"
template := "src/ontology/bervo-src.csv"
validator := "src/scripts/validate_bervo_src.py"

# List available recipes.
default:
    @just --list

# --- Validation -------------------------------------------------------------

# Structural checks on the term template. Run after every edit.
validate:
    python3 {{validator}} {{template}}

# Validate, treating warnings as errors.
validate-strict:
    python3 {{validator}} {{template}} --strict

# Normalise row widths in the template, then re-validate.
fix-template:
    python3 {{validator}} {{template}} --fix

# Run the Python test suite (validator + Makefile integration).
test:
    python3 -m pytest tests/ -q

# Validator tests only (fast; no robot or Docker needed).
test-fast:
    python3 -m pytest tests/test_validate_bervo_src.py -q

# --- Building ---------------------------------------------------------------

# Rebuild the OWL component from the template. Needs `robot` on PATH.
build:
    cd {{ontology_dir}} && make components/bervo-src.owl

# Rebuild the component inside the ODK Docker image (no local robot needed).
build-docker:
    cd {{ontology_dir}} && sh run.sh make components/bervo-src.owl

# Regenerate the documentation browser data.
browser-data:
    cd {{ontology_dir}} && make browser_data

# Full ODK QC suite. Slow, and needs the odkfull Docker image.
qc:
    cd {{ontology_dir}} && sh run.sh make test IMP=false PAT=false MIR=false

# Build the mkdocs site locally into ./site.
docs:
    mkdocs build --strict

# Everything CI runs that does not need Docker.
ci: validate test

# --- Inspection -------------------------------------------------------------

# Term counts by ID block and by category.
stats:
    #!/usr/bin/env python3
    import csv, re, collections
    rows = list(csv.reader(open("{{template}}", encoding="utf-8")))[2:]
    blocks = {0: "variables", 8: "concepts", 9: "grouping classes"}
    by_block = collections.Counter()
    for r in rows:
        m = re.fullmatch(r"BERVO:(\d{7})", r[0])
        by_block[blocks.get(int(m.group(1)) // 1_000_000, "other") if m else "properties"] += 1
    print(f"{len(rows)} terms total")
    for name, n in by_block.most_common():
        print(f"  {n:>5}  {name}")
    cats = collections.Counter(r[2] for r in rows if r[2].strip())
    print(f"\n{len(cats)} distinct categories; top 10:")
    for name, n in cats.most_common(10):
        print(f"  {n:>5}  {name}")

# Search IDs, labels, definitions, and synonyms. Usage: just find "soil carbon"
find query:
    #!/usr/bin/env python3
    import csv
    q = "{{query}}".casefold()
    rows = list(csv.reader(open("{{template}}", encoding="utf-8")))
    header, data = rows[0], rows[2:]
    cols = {n: i for i, n in enumerate(header)}
    # EcoSIM provenance is searched too: 74% of terms carry a model variable
    # name, and a request phrased in model terms should resolve directly.
    watch = [cols[n] for n in ("ID", "Label (description)", "Definition",
                               "Exact Synonyms", "Related Synonyms",
                               "EcoSIM Variable Name", "File Name") if n in cols]
    ecosim, fname = cols.get("EcoSIM Variable Name"), cols.get("File Name")
    hits = [r for r in data if any(q in r[i].casefold() for i in watch if i < len(r))]
    def cell(r, i):
        return r[i].strip() if i is not None and i < len(r) else ""
    for r in hits[:40]:
        # Show both EcoSIM columns: they are searched, so a hit that matches
        # neither the label nor the definition is otherwise unexplainable.
        prov = " / ".join(x for x in (cell(r, ecosim), cell(r, fname)) if x)
        print(f"{r[0]:<20} {r[1]:<45} [{r[2]}]" + (f"  <{prov}>" if prov else ""))
    print(f"\n{len(hits)} match(es)" + (" (showing first 40)" if len(hits) > 40 else ""))

# Next free ID in a block: 0 = variables, 8 = concepts, 9 = grouping classes.
next-id block="0":
    #!/usr/bin/env python3
    import csv, re
    block = int("{{block}}")
    assert block in (0, 8, 9), "block must be 0 (variables), 8 (concepts), or 9 (groupings)"
    rows = list(csv.reader(open("{{template}}", encoding="utf-8")))[2:]
    used = {int(m.group(1)) for r in rows
            if (m := re.fullmatch(r"BERVO:(\d{7})", r[0])) and int(m.group(1)) // 1_000_000 == block}
    print(f"BERVO:{(max(used) + 1) if used else block * 1_000_000:07d}")

# Show a single term as key/value pairs. Usage: just show BERVO:0000001
show id:
    #!/usr/bin/env python3
    import csv, sys
    rows = list(csv.reader(open("{{template}}", encoding="utf-8")))
    header, data = rows[0], rows[2:]
    for r in data:
        if r[0] == "{{id}}":
            for name, value in zip(header, r):
                if value.strip():
                    print(f"{name:<24} {value}")
            sys.exit(0)
    sys.exit("{{id}} not found in the template")

# --- Housekeeping -----------------------------------------------------------

# Remove generated components and scratch files.
clean:
    cd {{ontology_dir}} && make remove-old-input
