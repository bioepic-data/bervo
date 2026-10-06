import shutil
import subprocess
import tempfile
import unittest
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class MakefileIntegrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tempdir = tempfile.TemporaryDirectory()
        cls.repo_copy = Path(cls.tempdir.name) / "bervo"
        shutil.copytree(
            REPO_ROOT,
            cls.repo_copy,
            ignore=shutil.ignore_patterns(".git", "__pycache__", ".pytest_cache"),
        )
        cls.ontology_dir = cls.repo_copy / "src" / "ontology"

    @classmethod
    def tearDownClass(cls) -> None:
        cls.tempdir.cleanup()

    def run_make(self, *targets: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["make", *targets],
            cwd=self.ontology_dir,
            text=True,
            capture_output=True,
            check=True,
        )

    def test_component_build_recreates_generated_component(self) -> None:
        component = self.ontology_dir / "components" / "bervo-src.owl"
        component.unlink(missing_ok=True)

        self.run_make("components/bervo-src.owl")

        self.assertTrue(component.exists(), "make should regenerate bervo-src.owl")
        self.assertGreater(component.stat().st_size, 0, "generated component should not be empty")

    def test_export_google_sheet_copies_repo_tracked_template(self) -> None:
        template = self.ontology_dir / "bervo-src.csv"
        export_path = self.ontology_dir / "tmp" / "bervo-src-for-google-sheet.csv"
        export_path.unlink(missing_ok=True)

        result = self.run_make("export-google-sheet")

        self.assertIn("Wrote tmp/bervo-src-for-google-sheet.csv", result.stdout)
        self.assertEqual(template.read_bytes(), export_path.read_bytes())

    def test_browser_data_generation_creates_json_snapshot(self) -> None:
        browser_data = self.repo_copy / "docs" / "assets" / "data" / "bervo-browser.json"
        browser_data.unlink(missing_ok=True)

        self.run_make("browser_data")

        self.assertTrue(browser_data.exists(), "make should generate the browser data snapshot")
        payload = json.loads(browser_data.read_text(encoding="utf-8"))
        self.assertIn("entries", payload)
        self.assertGreater(len(payload["entries"]), 0)
        self.assertEqual(payload["entries"][0]["id"], "BERVO:0000000")
        self.assertIn("bioportal_term_url", payload["entries"][0])
        self.assertIn("conceptid=https%3A%2F%2Fw3id.org%2Fbervo%2FBERVO_0000000", payload["entries"][0]["bioportal_term_url"])

    def test_obo_release_keeps_underscored_odm2_xrefs_whole(self) -> None:
        # Issue #131: the OBO writer split these at an underscore. The
        # Cyanobacteria value was never split and must stay whole too.
        odm2 = [
            "variablename/radiationIncomingUV_A",
            "variablename/radiationIncomingUV_B",
            "variablename/sigma_t",
            "speciation/C10H6_CH3_2",
            "speciation/C10H5_CH3_3",
            "speciation/C10H4_CH3_4",
            "speciation/C6H4_CH3_2",
            "variablename/blue_GreenAlgae_Cyanobacteria_Phycocyanin",
        ]
        xrefs = "\n".join(
            f'        <oboInOwl:hasDbXref rdf:resource="http://vocabulary.odm2.org/{v}"/>'
            for v in odm2
        )
        owl = self.ontology_dir / "bervo.owl"
        obo = self.ontology_dir / "bervo.obo"
        owl.write_text(
            f"""<?xml version="1.0"?>
<rdf:RDF xmlns:owl="http://www.w3.org/2002/07/owl#"
     xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
     xmlns:oboInOwl="http://www.geneontology.org/formats/oboInOwl#">
    <owl:Ontology rdf:about="http://purl.obolibrary.org/obo/bervo.owl"/>
    <owl:AnnotationProperty rdf:about="http://www.geneontology.org/formats/oboInOwl#hasDbXref"/>
    <owl:Class rdf:about="https://w3id.org/bervo/BERVO_0000001">
{xrefs}
        <oboInOwl:hasDbXref rdf:resource="http://purl.obolibrary.org/obo/CHEBI_17045"/>
    </owl:Class>
</rdf:RDF>
""",
            encoding="utf-8",
        )
        obo.unlink(missing_ok=True)

        # -o: use the fixture as is rather than rebuilding it from bervo-full.owl.
        # OBO_FORMAT_OPTIONS is cleared because --clean-obo needs ROBOT 1.9.8.
        self.run_make("-o", "bervo.owl", "bervo.obo", "OBO_FORMAT_OPTIONS=")

        lines = set(obo.read_text(encoding="utf-8").splitlines())
        for v in odm2:
            self.assertIn(f"xref: http://vocabulary.odm2.org/{v}", lines)
        self.assertIn("xref: CHEBI:17045", lines)
        owl.unlink()
        obo.unlink()

    def test_legacy_sheet_export_alias_matches_template(self) -> None:
        template = self.ontology_dir / "bervo-src.csv"
        legacy_export = self.ontology_dir / "bervo_for_sheet.csv"
        legacy_export.unlink(missing_ok=True)

        self.run_make("bervo_for_sheet.csv")

        self.assertEqual(template.read_bytes(), legacy_export.read_bytes())

    def test_remove_old_input_cleans_generated_outputs_only(self) -> None:
        template = self.ontology_dir / "bervo-src.csv"
        component = self.ontology_dir / "components" / "bervo-src.owl"
        sheet_snapshot = self.ontology_dir / "tmp" / "bervo-src-google-sheet.csv"
        sheet_export = self.ontology_dir / "tmp" / "bervo-src-for-google-sheet.csv"
        legacy_export = self.ontology_dir / "bervo_for_sheet.csv"

        self.run_make("components/bervo-src.owl")
        self.run_make("export-google-sheet")
        sheet_snapshot.write_bytes(template.read_bytes())
        self.run_make("bervo_for_sheet.csv")

        self.run_make("remove-old-input")

        self.assertTrue(template.exists(), "remove-old-input must not remove the tracked template")
        self.assertFalse(component.exists(), "remove-old-input should remove the generated component")
        self.assertFalse(sheet_snapshot.exists(), "remove-old-input should remove the cached sheet snapshot")
        self.assertFalse(sheet_export.exists(), "remove-old-input should remove the sheet export")
        self.assertFalse(legacy_export.exists(), "remove-old-input should remove the legacy export alias")


if __name__ == "__main__":
    unittest.main()
