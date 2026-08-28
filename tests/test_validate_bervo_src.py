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
    "measurement_ofs", "contexts", "value_types", "Parents",
]
TYPE_ROW = [
    "ID", "LABEL", "SC %", "A IAO:0000115", "TYPE",
    "A BERVO:has_unit SPLIT=|", "AI BERVO:Qualifier SPLIT=|",
    "AI BERVO:Attribute SPLIT=|", "AI BERVO:measured_in SPLIT=|",
    "AI BERVO:measurement_of SPLIT=|", "AI BERVO:Context SPLIT=|",
    "AI BERVO:has_value_type SPLIT=|", "SC % SPLIT=|",
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


class TestFix(ValidatorTestCase):
    def test_fix_trims_trailing_empty_fields(self):
        path = self.write([ROOT, row("BERVO:0000001", "Soil carbon")])
        with path.open("a", encoding="utf-8", newline="") as handle:
            handle.write("BERVO:0000002,Soil nitrogen,Variable,,Class,,,,,,,,,,\r\n")

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
            handle.write("BERVO:0000002,Soil nitrogen,Variable,,Class,,,,,,,,,oops\r\n")

        self.assertEqual(validator.fix(path), 0, "a row with real overflow data needs a human, not a trim")


class TestRealTemplate(unittest.TestCase):
    """The checked-in template must stay clean; this is what CI enforces."""

    def test_repository_template_has_no_errors(self):
        report = validator.validate(REPO_ROOT / "src" / "ontology" / "bervo-src.csv")
        self.assertEqual(report.errors, [], "src/ontology/bervo-src.csv has structural errors")


if __name__ == "__main__":
    unittest.main()
