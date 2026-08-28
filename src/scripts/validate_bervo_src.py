#!/usr/bin/env python3
"""Structural validator for the BERVO ROBOT template (``src/ontology/bervo-src.csv``).

``bervo-src.csv`` is the source of truth for BERVO. Everything else -- the OWL
component, the release artefacts, the browser JSON -- is generated from it. ROBOT
happily builds a broken ontology from a subtly broken template, so this script
checks the invariants ROBOT does not, before a build is ever attempted.

Run it directly, via ``just validate``, or as a Claude Code hook after any edit
to the template.

Exit status is 0 when there are no errors (warnings alone do not fail), 1 when
at least one error was found, and 2 when the template could not be read at all.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_TEMPLATE = REPO_ROOT / "src" / "ontology" / "bervo-src.csv"

# The template's first row is human-readable headers and its second row is the
# ROBOT template string for each column. Data starts on the third row, which is
# spreadsheet row 3.
FIRST_DATA_ROW = 3

NUMERIC_ID = re.compile(r"^BERVO:\d{7}$")

# Properties predate the numeric ID scheme and keep mnemonic local names.
# New properties are rare; add them here deliberately rather than loosening the
# ID pattern.
MNEMONIC_IDS = {
    "BERVO:has_unit",
    "BERVO:Qualifier",
    "BERVO:Attribute",
    "BERVO:measured_in",
    "BERVO:measurement_of",
    "BERVO:Context",
    "BERVO:has_value_type",
    "BERVO:involves_taxa",
    "BERVO:involves_chemicals",
}

# Numeric IDs are allocated in blocks by term kind. See AGENTS.md.
ID_BLOCKS = {
    0: "variable",
    8: "concept",
    9: "grouping class",
}

VALID_TYPES = {"Class", "owl:Class", "owl:AnnotationProperty", "owl:ObjectProperty"}

# Placeholders that mean "deliberately empty" rather than "unfilled".
NULL_TOKENS = {"", "NA", "N/A", "none", "None"}

# Columns declared ``AI`` in the ROBOT type row: each value is resolved to an
# IRI, so it must name an existing term -- either as a CURIE or as a label.
TERM_REF_COLUMNS = (
    "qualifiers",
    "attributes",
    "measured_ins",
    "measurement_ofs",
    "contexts",
    "value_types",
)

# Declared ``A`` rather than ``AI``: the value is a literal (a unit string such
# as "g d-2 h-1"), not a reference. Never resolve these against the term list.
LITERAL_COLUMNS = ("has_units",)

# Columns whose values may be either a CURIE or a term label (ROBOT's ``SC %``
# resolves both).
LABEL_OR_CURIE_COLUMNS = ("Category", "Parents")

# Terms legitimately without a parent: the ontology root and the properties.
ROOTLESS_IDS = {"BERVO:0000000"} | MNEMONIC_IDS


@dataclass
class Report:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def error(self, row: int | None, msg: str) -> None:
        self.errors.append(_locate(row, msg))

    def warn(self, row: int | None, msg: str) -> None:
        self.warnings.append(_locate(row, msg))


def _locate(row: int | None, msg: str) -> str:
    return f"row {row}: {msg}" if row is not None else msg


def _split(value: str) -> list[str]:
    """Split a ROBOT ``SPLIT=|`` cell into meaningful tokens."""
    return [tok.strip() for tok in value.split("|") if tok.strip() not in NULL_TOKENS]


def read_template(path: Path) -> tuple[list[str], list[str], list[list[str]]]:
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.reader(handle))
    if len(rows) < 3:
        raise ValueError(f"{path} has {len(rows)} rows; expected a header row, a ROBOT type row, and data")
    return rows[0], rows[1], rows[2:]


def validate(path: Path) -> Report:
    report = Report()
    header, types, data = read_template(path)
    width = len(header)
    index = {name: i for i, name in enumerate(header)}

    if len(types) != width:
        report.error(2, f"ROBOT type row has {len(types)} fields but the header has {width}")

    for required in ("ID", "Label (description)", "Type", *LABEL_OR_CURIE_COLUMNS):
        if required not in index:
            report.error(1, f"required column {required!r} is missing from the header")
    if report.errors:
        # Without a trustworthy header the row-level checks would be noise.
        return report

    id_col = index["ID"]
    label_col = index["Label (description)"]
    type_col = index["Type"]

    # --- Pass 1: shape, identity, and the term index the later passes need. ---
    ids: dict[str, int] = {}
    labels: dict[str, int] = {}
    known_labels: set[str] = set()
    # casefolded label -> canonical spelling, for "did you mean" hints.
    folded_labels: dict[str, str] = {}
    type_styles: dict[str, int] = defaultdict(int)

    for offset, row in enumerate(data):
        line = FIRST_DATA_ROW + offset

        if len(row) != width:
            extra = row[width:]
            if len(row) > width and all(cell.strip() == "" for cell in extra):
                report.error(
                    line,
                    f"has {len(row)} fields but the header has {width}; "
                    f"{len(extra)} trailing empty field(s). Run 'just fix-template' to trim.",
                )
            else:
                report.error(line, f"has {len(row)} fields but the header has {width}")

        def cell(col: int) -> str:
            return row[col].strip() if col < len(row) else ""

        term_id = cell(id_col)
        label = cell(label_col)

        if not term_id:
            report.error(line, "has no ID")
        elif term_id in ids:
            report.error(line, f"duplicate ID {term_id} (first seen on row {ids[term_id]})")
        else:
            ids[term_id] = line
            if not NUMERIC_ID.match(term_id) and term_id not in MNEMONIC_IDS:
                report.error(
                    line,
                    f"ID {term_id!r} is neither a 7-digit BERVO CURIE nor a known mnemonic property ID",
                )
            elif NUMERIC_ID.match(term_id):
                block = int(term_id.split(":")[1]) // 1_000_000
                if block not in ID_BLOCKS:
                    report.warn(
                        line,
                        f"ID {term_id} falls outside the allocated blocks "
                        f"({', '.join(f'{k}xxxxxx={v}' for k, v in sorted(ID_BLOCKS.items()))})",
                    )

        if not label:
            report.error(line, f"{term_id or '<no ID>'} has no label")
        else:
            key = label.casefold()
            if key in labels:
                report.error(line, f"duplicate label {label!r} (first seen on row {labels[key]})")
            else:
                labels[key] = line
            known_labels.add(label)
            folded_labels.setdefault(key, label)

        term_type = cell(type_col)
        if not term_type:
            report.warn(line, f"{term_id} has no Type; ROBOT will default it to owl:Class")
        elif term_type not in VALID_TYPES:
            report.error(line, f"{term_id} has unrecognised Type {term_type!r}")
        else:
            type_styles[term_type] += 1

    if {"Class", "owl:Class"} <= type_styles.keys():
        report.warn(
            None,
            f"Type column mixes 'Class' ({type_styles['Class']} rows) and "
            f"'owl:Class' ({type_styles['owl:Class']} rows); prefer one spelling",
        )

    # --- Pass 2: referential integrity, now that every term is known. ---
    for offset, row in enumerate(data):
        line = FIRST_DATA_ROW + offset
        term_id = row[id_col].strip() if id_col < len(row) else ""

        for column in TERM_REF_COLUMNS:
            col = index.get(column)
            if col is None or col >= len(row):
                continue
            for token in _split(row[col]):
                if token.startswith("BERVO:"):
                    # A CURIE that does not exist is unambiguously wrong.
                    if token not in ids:
                        report.error(line, f"{term_id}.{column} references unknown term {token}")
                elif token not in known_labels:
                    # A label that does not resolve is usually a typo, but the
                    # backlog predates this check, so it is a warning.
                    hint = folded_labels.get(token.casefold())
                    suggestion = f"; did you mean {hint!r}?" if hint else ""
                    report.warn(
                        line,
                        f"{term_id}.{column} references {token!r}, which is not a term label{suggestion}",
                    )

        parented = False
        for column in LABEL_OR_CURIE_COLUMNS:
            col = index.get(column)
            if col is None or col >= len(row):
                continue
            for token in _split(row[col]):
                parented = True
                if token not in ids and token not in known_labels:
                    report.error(
                        line,
                        f"{term_id}.{column} references {token!r}, which is neither a BERVO ID nor a term label",
                    )

        if not parented and term_id not in ROOTLESS_IDS:
            report.warn(line, f"{term_id} has no Category and no Parents; it will be an orphan class")

    return report


def detect_line_terminator(path: Path) -> str:
    """Return the file's dominant line terminator so --fix does not rewrite every line."""
    blob = path.read_bytes()
    return "\r\n" if blob.count(b"\r\n") > blob.count(b"\n") - blob.count(b"\r\n") else "\n"


def fix(path: Path) -> int:
    """Normalise every row to the header width. Returns the number of rows changed."""
    header, types, data = read_template(path)
    width = len(header)
    rows = [header, types, *data]
    terminator = detect_line_terminator(path)
    changed = 0

    for i, row in enumerate(rows):
        if len(row) == width:
            continue
        if len(row) > width and all(cell.strip() == "" for cell in row[width:]):
            rows[i] = row[:width]
        elif len(row) < width:
            rows[i] = row + [""] * (width - len(row))
        else:
            # Non-empty overflow is a data question, not a formatting one.
            continue
        changed += 1

    if changed:
        with path.open("w", encoding="utf-8", newline="") as handle:
            csv.writer(handle, lineterminator=terminator).writerows(rows)
    return changed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("template", nargs="?", type=Path, default=DEFAULT_TEMPLATE,
                        help="path to bervo-src.csv (default: the repo's template)")
    parser.add_argument("--fix", action="store_true",
                        help="normalise row widths in place, then re-validate")
    parser.add_argument("--strict", action="store_true",
                        help="treat warnings as errors")
    parser.add_argument("--quiet", action="store_true",
                        help="print only the summary line")
    args = parser.parse_args(argv)

    if not args.template.exists():
        print(f"error: {args.template} does not exist", file=sys.stderr)
        return 2

    if args.fix:
        changed = fix(args.template)
        print(f"fixed row width on {changed} row(s)")

    try:
        report = validate(args.template)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if not args.quiet:
        for message in report.errors:
            print(f"ERROR {message}")
        for message in report.warnings:
            print(f"warn  {message}")

    failed = bool(report.errors) or (args.strict and bool(report.warnings))
    print(
        f"{args.template.name}: {len(report.errors)} error(s), {len(report.warnings)} warning(s)"
        f" -- {'FAIL' if failed else 'OK'}"
    )
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
