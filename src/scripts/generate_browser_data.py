#!/usr/bin/env python3

import csv
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE_CSV = REPO_ROOT / "src" / "ontology" / "bervo-src.csv"
TARGET_JSON = REPO_ROOT / "docs" / "assets" / "data" / "bervo-browser.json"
BIOPORTAL_URL = "https://bioportal.bioontology.org/ontologies/BERVO"
GITHUB_SOURCE_URL = "https://github.com/bioepic-data/bervo/blob/main/src/ontology/bervo-src.csv"

FIELD_MAP = {
    "ID": "id",
    "Label (description)": "label",
    "Category": "category",
    "EcoSIM Other Names": "ecosim_other_names",
    "EcoSIM Variable Name": "ecosim_variable_name",
    "File Name": "file_name",
    "Definition": "definition",
    "Comment": "comment",
    "Related Synonyms": "related_synonyms",
    "Exact Synonyms": "exact_synonyms",
    "Type": "type",
    "DbXrefs": "dbxrefs",
    "has_units": "has_units",
    "qualifiers": "qualifiers",
    "attributes": "attributes",
    "measured_ins": "measured_ins",
    "measurement_ofs": "measurement_ofs",
    "contexts": "contexts",
    "value_types": "value_types",
    "Parents": "parents",
    "Group Curated?": "group_curated",
    "Definition Curated?": "definition_curated",
    "Definition Source": "definition_source",
    "Comment from Ulas": "comment_from_ulas",
    "Comment from Joan": "comment_from_joan",
    "Comment from John-Marc": "comment_from_john_marc",
    "Comment from Jinyun": "comment_from_jinyun",
    "Comment from Harry": "comment_from_harry",
    "Comment from Chris": "comment_from_chris",
}

LIST_FIELDS = {
    "related_synonyms",
    "exact_synonyms",
    "dbxrefs",
    "qualifiers",
    "attributes",
    "measured_ins",
    "measurement_ofs",
    "contexts",
    "value_types",
    "parents",
}


def clean(value: str) -> str:
    return value.strip()


def split_pipe_field(value: str) -> list[str]:
    value = clean(value)
    if not value or value in {"NA", "NONE"}:
        return []
    return [item.strip() for item in value.split("|") if item.strip()]


def make_iri(term_id: str) -> str:
    return f"https://w3id.org/bervo/{term_id.replace(':', '_')}"


def make_search_blob(entry: dict) -> str:
    parts = []
    for key, value in entry.items():
        if key == "search_blob":
            continue
        if isinstance(value, list):
            parts.extend(value)
        elif isinstance(value, str):
            parts.append(value)
    return " ".join(parts).lower()


def read_entries() -> tuple[list[dict], dict]:
    with SOURCE_CSV.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader)
        metadata = next(reader)

        entries = []
        for index, row in enumerate(reader, start=1):
            if not row or not clean(row[0]):
                continue

            padded_row = row + [""] * (len(header) - len(row))
            raw_entry = dict(zip(header, padded_row))
            entry = {"order": index}

            for csv_name, json_name in FIELD_MAP.items():
                value = clean(raw_entry.get(csv_name, ""))
                if json_name in LIST_FIELDS:
                    entry[json_name] = split_pipe_field(value)
                else:
                    entry[json_name] = value

            entry["iri"] = make_iri(entry["id"])
            entry["has_definition"] = bool(entry["definition"])
            entry["bioportal_url"] = BIOPORTAL_URL
            entry["source_url"] = GITHUB_SOURCE_URL
            entry["search_blob"] = make_search_blob(entry)
            entries.append(entry)

    metadata_map = {
        FIELD_MAP.get(name, name): clean(value)
        for name, value in zip(header, metadata)
        if name in FIELD_MAP
    }
    return entries, metadata_map


def summarise(entries: list[dict]) -> dict:
    types = sorted({entry["type"] for entry in entries if entry["type"]})
    categories = sorted({entry["category"] for entry in entries if entry["category"]})
    concept_count = sum(1 for entry in entries if entry["category"] == "Concept")
    class_count = sum(1 for entry in entries if entry["type"] in {"Class", "owl:Class"})
    property_count = sum(1 for entry in entries if "Property" in entry["type"])

    return {
        "term_count": len(entries),
        "concept_count": concept_count,
        "class_count": class_count,
        "property_count": property_count,
        "types": types,
        "categories": categories,
    }


def main() -> None:
    entries, metadata = read_entries()
    payload = {
        "title": "BERVO Browser Data",
        "source_csv": str(SOURCE_CSV.relative_to(REPO_ROOT)),
        "bioportal_url": BIOPORTAL_URL,
        "source_url": GITHUB_SOURCE_URL,
        "template_metadata": metadata,
        "summary": summarise(entries),
        "entries": entries,
    }

    TARGET_JSON.parent.mkdir(parents=True, exist_ok=True)
    with TARGET_JSON.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
        handle.write("\n")

    print(f"Wrote {TARGET_JSON.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
