"""Tests for the BERVO template validator (``src/scripts/validate_bervo_src.py``)."""

import csv
import importlib.util
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "src" / "scripts" / "validate_bervo_src.py"

_spec = importlib.util.spec_from_file_location("validate_bervo_src", SCRIPT)
validator = importlib.util.module_from_spec(_spec)
sys.modules["validate_bervo_src"] = validator
_spec.loader.exec_module(validator)


HEADER = [
    "ID", "Label (description)", "Category", "Definition", "Type",
    "has_units", "qualifiers", "attributes", "measured_ins",
    "measurement_ofs", "contexts", "value_types", "Parents", "DbXrefs",
    "involves_chemicals",
]
TYPE_ROW = [
    "ID", "LABEL", "SC %", "A IAO:0000115", "TYPE",
    "A BERVO:has_unit SPLIT=|", "AI BERVO:Qualifier SPLIT=|",
    "AI BERVO:Attribute SPLIT=|", "AI BERVO:measured_in SPLIT=|",
    "AI BERVO:measurement_of SPLIT=|", "AI BERVO:Context SPLIT=|",
    "AI BERVO:has_value_type SPLIT=|", "SC % SPLIT=|",
    "AI oio:hasDbXref SPLIT=|", "C BERVO:involves_chemicals some % SPLIT=|",
]


def row(term_id, label, category="Variable", type_="Class", **cells):
    values = dict.fromkeys(HEADER, "")
    values.update(ID=term_id, **{"Label (description)": label, "Category": category, "Type": type_})
    values.update(cells)
    return [values[name] for name in HEADER]


ROOT = row("BERVO:0000000", "Variable", category="")


class ValidatorTestCase(unittest.TestCase):
    def write(self, rows, *, terminator="\r\n"):
        path = Path(self.tmp.name) / "bervo-src.csv"
        with path.open("w", encoding="utf-8", newline="") as handle:
            csv.writer(handle, lineterminator=terminator).writerows([HEADER, TYPE_ROW, *rows])
        return path

    def setUp(self):
        import tempfile
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)


class TestStructuralChecks(ValidatorTestCase):
    def test_clean_template_has_no_errors(self):
        report = validator.validate(self.write([ROOT, row("BERVO:0000001", "Soil carbon")]))
        self.assertEqual(report.errors, [])

    def test_duplicate_id_is_an_error(self):
        report = validator.validate(self.write([
            ROOT, row("BERVO:0000001", "Soil carbon"), row("BERVO:0000001", "Soil nitrogen"),
        ]))
        self.assertTrue(any("duplicate ID BERVO:0000001" in e for e in report.errors), report.errors)

    def test_duplicate_label_is_case_insensitive(self):
        report = validator.validate(self.write([
            ROOT, row("BERVO:0000001", "Soil carbon"), row("BERVO:0000002", "soil CARBON"),
        ]))
        self.assertTrue(any("duplicate label" in e for e in report.errors), report.errors)

    def test_malformed_id_is_an_error(self):
        report = validator.validate(self.write([ROOT, row("BERVO:123", "Short ID")]))
        self.assertTrue(any("neither a 7-digit" in e for e in report.errors), report.errors)

    def test_mnemonic_property_ids_are_accepted(self):
        report = validator.validate(self.write([
            ROOT, row("BERVO:has_unit", "has unit", category="", type_="owl:AnnotationProperty"),
        ]))
        self.assertEqual(report.errors, [])

    def test_missing_label_is_an_error(self):
        report = validator.validate(self.write([ROOT, row("BERVO:0000001", "")]))
        self.assertTrue(any("has no label" in e for e in report.errors), report.errors)

    def test_unrecognised_type_is_an_error(self):
        report = validator.validate(self.write([ROOT, row("BERVO:0000001", "Soil carbon", type_="Klass")]))
        self.assertTrue(any("unrecognised Type" in e for e in report.errors), report.errors)

    def test_empty_type_is_only_a_warning(self):
        report = validator.validate(self.write([ROOT, row("BERVO:0000001", "Soil carbon", type_="")]))
        self.assertEqual(report.errors, [])
        self.assertTrue(any("has no Type" in w for w in report.warnings), report.warnings)

    def test_id_outside_allocated_block_warns(self):
        report = validator.validate(self.write([ROOT, row("BERVO:5000001", "Odd block")]))
        self.assertEqual(report.errors, [])
        self.assertTrue(any("outside the allocated blocks" in w for w in report.warnings), report.warnings)


class TestReferentialIntegrity(ValidatorTestCase):
    def test_dangling_curie_reference_is_an_error(self):
        report = validator.validate(self.write([
            ROOT, row("BERVO:0000001", "Soil carbon", attributes="BERVO:8009999"),
        ]))
        self.assertTrue(any("references unknown term BERVO:8009999" in e for e in report.errors), report.errors)

    def test_resolvable_curie_reference_passes(self):
        report = validator.validate(self.write([
            ROOT,
            row("BERVO:8000001", "Concentration", category="Variable"),
            row("BERVO:0000001", "Soil carbon", attributes="BERVO:8000001"),
        ]))
        self.assertEqual(report.errors, [])

    def test_na_placeholders_are_ignored(self):
        report = validator.validate(self.write([
            ROOT, row("BERVO:0000001", "Soil carbon", attributes="NA", qualifiers="N/A"),
        ]))
        self.assertEqual(report.errors, [])

    def test_category_may_reference_a_label(self):
        report = validator.validate(self.write([
            ROOT, row("BERVO:0000001", "Soil carbon", category="Variable"),
        ]))
        self.assertEqual(report.errors, [])

    def test_unresolvable_category_is_an_error(self):
        report = validator.validate(self.write([
            ROOT, row("BERVO:0000001", "Soil carbon", category="Nonexistent grouping"),
        ]))
        self.assertTrue(any("neither a BERVO ID nor a term label" in e for e in report.errors), report.errors)

    def test_unresolvable_label_reference_is_a_warning(self):
        report = validator.validate(self.write([
            ROOT, row("BERVO:0000001", "Soil carbon", attributes="Nonexistent attribute"),
        ]))
        self.assertEqual(report.errors, [])
        self.assertTrue(any("is not a term label" in w for w in report.warnings), report.warnings)

    def test_case_only_mismatch_suggests_the_canonical_label(self):
        report = validator.validate(self.write([
            ROOT,
            row("BERVO:8000001", "Boundary layer", category="Variable"),
            row("BERVO:0000001", "Soil carbon", contexts="Boundary Layer"),
        ]))
        self.assertTrue(
            any("did you mean 'Boundary layer'?" in w for w in report.warnings), report.warnings
        )

    def test_resolvable_label_reference_passes_silently(self):
        report = validator.validate(self.write([
            ROOT,
            row("BERVO:8000001", "Flux", category="Variable"),
            row("BERVO:0000001", "Soil carbon", attributes="Flux"),
        ]))
        self.assertEqual(report.errors, [])
        self.assertFalse(any("is not a term label" in w for w in report.warnings), report.warnings)

    def test_has_units_holds_literals_not_references(self):
        """has_units is declared `A`, not `AI`; unit strings must not be resolved."""
        report = validator.validate(self.write([
            ROOT, row("BERVO:0000001", "Soil carbon", has_units="g d-2 h-1|NONE"),
        ]))
        self.assertEqual(report.errors, [])
        self.assertFalse(
            any("g d-2 h-1" in w for w in report.warnings),
            "unit literals must never be reported as unresolved term references",
        )

    def test_orphan_class_warns_but_does_not_fail(self):
        report = validator.validate(self.write([ROOT, row("BERVO:8000001", "Loose concept", category="")]))
        self.assertEqual(report.errors, [])
        self.assertTrue(any("orphan class" in w for w in report.warnings), report.warnings)

    def test_root_is_not_reported_as_an_orphan(self):
        report = validator.validate(self.write([ROOT]))
        self.assertFalse(any("orphan class" in w for w in report.warnings), report.warnings)


class TestCrossReferences(ValidatorTestCase):
    """DbXrefs is `AI`, so a value ROBOT cannot expand becomes a relative IRI."""

    def test_non_curie_xref_is_an_error(self):
        report = validator.validate(self.write([
            ROOT, row("BERVO:0000001", "Soil carbon", DbXrefs="Class"),
        ]))
        self.assertTrue(
            any("is not a CURIE" in e for e in report.errors), report.errors
        )

    def test_resolvable_prefix_passes_silently(self):
        report = validator.validate(self.write([
            ROOT, row("BERVO:0000001", "Soil carbon", DbXrefs="CHEBI:17045"),
        ]))
        self.assertEqual(report.errors, [])
        self.assertFalse(any("CHEBI" in w for w in report.warnings), report.warnings)

    def test_undeclared_prefix_warns_once_not_per_row(self):
        rows = [ROOT] + [
            row(f"BERVO:000000{i}", f"Term {i}", DbXrefs="COMO:0000129")
            for i in range(1, 6)
        ]
        report = validator.validate(self.write(rows))
        hits = [w for w in report.warnings if "COMO" in w]
        self.assertEqual(len(hits), 1, f"expected one grouped warning, got {hits}")
        self.assertIn("5 DbXrefs value(s)", hits[0])

    def test_multiple_undeclared_prefixes_each_get_one_warning(self):
        # Deliberately two prefixes that are neither OBO-registered nor declared
        # in bervo.Makefile -- a declared one would (correctly) not warn.
        report = validator.validate(self.write([
            ROOT,
            row("BERVO:0000001", "A", DbXrefs="NOTREAL:0000129"),
            row("BERVO:0000002", "B", DbXrefs="ALSOFAKE:0000642"),
        ]))
        self.assertEqual(len([w for w in report.warnings if "NOTREAL" in w]), 1)
        self.assertEqual(len([w for w in report.warnings if "ALSOFAKE" in w]), 1)

    def test_prefix_declared_in_the_makefile_does_not_warn(self):
        """Regression: MIXS was declared in bervo.Makefile, so it must resolve."""
        declared = sorted(validator.declared_prefixes() - {"BERVO", "oio"})
        if not declared:
            self.skipTest("no extra --add-prefix declarations to exercise")
        report = validator.validate(self.write([
            ROOT, row("BERVO:0000001", "A", DbXrefs=f"{declared[0]}:0000642"),
        ]))
        self.assertFalse(
            any(declared[0] in w for w in report.warnings),
            f"{declared[0]} is declared in bervo.Makefile but still warned",
        )

    def test_na_xref_is_ignored(self):
        report = validator.validate(self.write([
            ROOT, row("BERVO:0000001", "Soil carbon", DbXrefs="NA"),
        ]))
        self.assertEqual(report.errors, [])

    def test_absolute_iri_xref_is_not_treated_as_a_curie(self):
        """An http(s) value is already resolved; 'http' is not a prefix."""
        report = validator.validate(self.write([
            ROOT,
            row("BERVO:0000001", "Soil carbon",
                DbXrefs="http://purl.obolibrary.org/obo/CHEBI_17045"),
        ]))
        self.assertEqual(report.errors, [])
        self.assertFalse(any("http" in w for w in report.warnings), report.warnings)

    def test_split_xrefs_are_checked_individually(self):
        report = validator.validate(self.write([
            ROOT, row("BERVO:0000001", "Soil carbon", DbXrefs="CHEBI:17045|Class"),
        ]))
        self.assertEqual(len([e for e in report.errors if "is not a CURIE" in e]), 1)


class TestClassExpressionColumns(ValidatorTestCase):
    """`C <prop> some %` fillers must name a class, but are not parents."""

    def test_resolvable_filler_passes(self):
        report = validator.validate(self.write([
            ROOT,
            row("BERVO:8000001", "Chemical", category="Variable"),
            row("BERVO:0000001", "Soil carbon", involves_chemicals="Chemical"),
        ]))
        self.assertEqual(report.errors, [])

    def test_unresolvable_filler_is_an_error(self):
        report = validator.validate(self.write([
            ROOT, row("BERVO:0000001", "Soil carbon", involves_chemicals="Nonexistent"),
        ]))
        self.assertTrue(
            any("is not a class" in e for e in report.errors), report.errors
        )

    def test_filler_case_typo_gets_a_suggestion(self):
        report = validator.validate(self.write([
            ROOT,
            row("BERVO:8000001", "Chemical", category="Variable"),
            row("BERVO:0000001", "Soil carbon", involves_chemicals="chemical"),
        ]))
        self.assertTrue(any("did you mean 'Chemical'?" in e for e in report.errors), report.errors)

    def test_filler_does_not_count_as_a_parent(self):
        """A term with only a restriction filler is still an orphan."""
        report = validator.validate(self.write([
            ROOT,
            row("BERVO:8000001", "Chemical", category="Variable"),
            row("BERVO:8000002", "Loose", category="", involves_chemicals="Chemical"),
        ]))
        self.assertTrue(any("orphan class" in w for w in report.warnings), report.warnings)


    def test_na_is_rejected_in_a_restriction_filler(self):
        """NA is the house convention in AI columns; in a C column it is an axiom."""
        report = validator.validate(self.write([
            ROOT, row("BERVO:0000001", "Soil carbon", involves_chemicals="NA"),
        ]))
        self.assertTrue(
            any("cannot be 'NA'" in e for e in report.errors), report.errors
        )

    def test_split_fillers_are_checked_individually(self):
        report = validator.validate(self.write([
            ROOT,
            row("BERVO:8000001", "Chemical", category="Variable"),
            row("BERVO:0000001", "Soil carbon", involves_chemicals="Chemical|Nonexistent"),
        ]))
        self.assertEqual(len([e for e in report.errors if "is not a class" in e]), 1)


class TestPrefixDeclarations(unittest.TestCase):
    """The resolvable-prefix set must track bervo.Makefile, not duplicate it."""

    def test_declared_prefixes_are_parsed_from_the_makefile(self):
        declared = validator.declared_prefixes()
        self.assertIn("BERVO", declared)
        self.assertIn("oio", declared)

    def test_makefile_prefixes_count_as_resolvable(self):
        """Doing what the warning says -- adding --add-prefix -- must silence it."""
        for prefix in validator.declared_prefixes():
            self.assertIn(prefix, validator.resolvable_prefixes())

    def test_every_makefile_prefix_used_in_the_template_resolves(self):
        report = validator.validate(REPO_ROOT / "src" / "ontology" / "bervo-src.csv")
        for warning in report.warnings:
            for prefix in validator.declared_prefixes():
                self.assertNotIn(
                    f"prefix {prefix!r}", warning,
                    f"{prefix} is declared in bervo.Makefile but still reported unresolvable",
                )

    def test_missing_makefile_degrades_gracefully(self):
        self.assertEqual(validator.declared_prefixes(Path("/nonexistent/bervo.Makefile")), set())


class TestFix(ValidatorTestCase):
    def test_fix_trims_trailing_empty_fields(self):
        path = self.write([ROOT, row("BERVO:0000001", "Soil carbon")])
        with path.open("a", encoding="utf-8", newline="") as handle:
            # One field wider than the header, the trailing one empty.
            handle.write("BERVO:0000002,Soil nitrogen,Variable" + "," * (len(HEADER) - 2) + "\r\n")

        self.assertTrue(any("fields but the header has" in e for e in validator.validate(path).errors))
        self.assertEqual(validator.fix(path), 1)
        self.assertEqual(validator.validate(path).errors, [])

    def test_fix_pads_short_rows(self):
        path = self.write([ROOT])
        with path.open("a", encoding="utf-8", newline="") as handle:
            handle.write("BERVO:0000002,Soil nitrogen,Variable\r\n")

        self.assertEqual(validator.fix(path), 1)
        rows = list(csv.reader(path.open(encoding="utf-8", newline="")))
        self.assertTrue(all(len(r) == len(HEADER) for r in rows))

    def test_fix_preserves_crlf_line_endings(self):
        path = self.write([ROOT], terminator="\r\n")
        with path.open("a", encoding="utf-8", newline="") as handle:
            handle.write("BERVO:0000002,Soil nitrogen,Variable\r\n")

        validator.fix(path)
        blob = path.read_bytes()
        self.assertNotIn(b"\n", blob.replace(b"\r\n", b""), "fix must not introduce bare LF into a CRLF file")

    def test_fix_preserves_lf_line_endings(self):
        path = self.write([ROOT], terminator="\n")
        with path.open("a", encoding="utf-8", newline="") as handle:
            handle.write("BERVO:0000002,Soil nitrogen,Variable\n")

        validator.fix(path)
        self.assertNotIn(b"\r", path.read_bytes(), "fix must not introduce CR into an LF file")

    def test_fix_leaves_non_empty_overflow_alone(self):
        path = self.write([ROOT])
        with path.open("a", encoding="utf-8", newline="") as handle:
            # One field wider than the header, and the overflow carries real data.
            handle.write("BERVO:0000002,Soil nitrogen,Variable" + "," * (len(HEADER) - 3) + ",oops\r\n")

        self.assertEqual(validator.fix(path), 0, "a row with real overflow data needs a human, not a trim")


class TestRealTemplate(unittest.TestCase):
    """The checked-in template must stay clean; this is what CI enforces."""

    def test_repository_template_has_no_errors(self):
        report = validator.validate(REPO_ROOT / "src" / "ontology" / "bervo-src.csv")
        self.assertEqual(report.errors, [], "src/ontology/bervo-src.csv has structural errors")


if __name__ == "__main__":
    unittest.main()
