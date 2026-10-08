# Custom Makefile settings for BERVO

# The repo-tracked CSV is the authoritative ROBOT template for BERVO.
# The Google Sheet is retained as an optional sync target for collaborators,
# but it must not be used as the primary build input.

BERVO_TEMPLATE = bervo-src.csv
BERVO_COMPONENT = $(COMPONENTSDIR)/bervo-src.owl
GOOGLE_SHEET_URL = https://docs.google.com/spreadsheets/d/1mS8VVtr-m24vZ7nQUtUbQrN8r-UBy3AwRzTfQsmwVL8
GOOGLE_SHEET_EXPORT_URL = $(GOOGLE_SHEET_URL)/export?exportFormat=csv
GOOGLE_SHEET_SNAPSHOT = $(TMPDIR)/bervo-src-google-sheet.csv
GOOGLE_SHEET_EXPORT = $(TMPDIR)/bervo-src-for-google-sheet.csv
BROWSER_DATA = ../../docs/assets/data/bervo-browser.json

.PHONY: refresh-google-sheet-snapshot compare-google-sheet export-google-sheet browser_data integration_test remove-old-input

# Build the ODK-managed component from the repo-tracked template.
# Depends on this makefile too: a --add-prefix change alters the emitted IRIs,
# so the component must rebuild even when the template itself is unchanged.
$(BERVO_COMPONENT): $(BERVO_TEMPLATE) bervo-annotations.ttl bervo.Makefile | $(COMPONENTSDIR)
	$(ROBOT) template \
	  --add-prefix 'BERVO: https://w3id.org/bervo/BERVO_' \
	  --add-prefix 'oio: http://www.geneontology.org/formats/oboInOwl#' \
	  --add-prefix 'MIXS: https://w3id.org/mixs/' \
	  --add-prefix 'ODM2: http://vocabulary.odm2.org/' \
	  --add-prefix 'COMO: http://purl.obolibrary.org/obo/COMO_' \
	  --add-prefix 'ENVTHES: http://vocabs.lter-europe.net/EnvThes/' \
	  -t $< \
	  annotate --annotation-file bervo-annotations.ttl \
	  -o $@

# Optional utility: download the current Google Sheet export for comparison.
$(GOOGLE_SHEET_SNAPSHOT): | $(TMPDIR)
	curl -L -s $(GOOGLE_SHEET_EXPORT_URL) > $@

refresh-google-sheet-snapshot: $(GOOGLE_SHEET_SNAPSHOT)

compare-google-sheet: $(GOOGLE_SHEET_SNAPSHOT) $(BERVO_TEMPLATE)
	diff -u $(BERVO_TEMPLATE) $(GOOGLE_SHEET_SNAPSHOT) || true

# Optional utility: produce the CSV that can be uploaded into Google Sheets.
$(GOOGLE_SHEET_EXPORT): $(BERVO_TEMPLATE) | $(TMPDIR)
	cp $< $@

export-google-sheet: $(GOOGLE_SHEET_EXPORT)
	@echo "Wrote $(GOOGLE_SHEET_EXPORT) from $(BERVO_TEMPLATE)"

# Backwards-compatible alias for the historical sheet export filename.
bervo_for_sheet.csv: $(BERVO_TEMPLATE)
	cp $< $@

# OBO release files: write non-OBO cross-references as strings (issue #131).
# The OWLAPI OBO writer reads the last path segment of a hasDbXref IRI as an
# OBO identifier when it looks like PREFIX_ID (one underscore, or several with
# an all-digit last part) and writes only that fragment, so
# http://vocabulary.odm2.org/variablename/sigma_t became "xref: sigma:t".
# A string is written as it is. OBO Library IRIs stay IRIs, so CHEBI and the
# rest still contract to CURIEs. The rewrite is done on the RDF/XML text
# rather than with `robot query --update`, because a query drops the
# document's namespace declarations and changes every ID in the OBO output.
# The grep stops the build if ROBOT ever serialises a cross-reference in a
# shape the substitution does not match. The .owl and .json files keep IRIs.
OBO_NON_OBO_XREF_IRI = hasDbXref rdf:resource="(?!http://purl\.obolibrary\.org/obo/)
define obo_with_string_xrefs
	perl -pe 's{<oboInOwl:$(OBO_NON_OBO_XREF_IRI)([^"]*)"/>}{<oboInOwl:hasDbXref>$$1</oboInOwl:hasDbXref>}g' $< > $(TMPDIR)/$@.xrefs.owl
	! grep -qP '$(OBO_NON_OBO_XREF_IRI)' $(TMPDIR)/$@.xrefs.owl
	$(ROBOT) convert --input $(TMPDIR)/$@.xrefs.owl --check false -f obo $(OBO_FORMAT_OPTIONS) -o $@
endef

$(ONT).obo: $(ONT).owl | $(TMPDIR)
	$(obo_with_string_xrefs)

$(ONT)-full.obo: $(ONT)-full.owl | $(TMPDIR)
	$(obo_with_string_xrefs)

$(BROWSER_DATA): $(BERVO_TEMPLATE) ../scripts/generate_browser_data.py
	python3 ../scripts/generate_browser_data.py

browser_data: $(BROWSER_DATA)

integration_test:
	python3 ../../tests/test_makefile_integration.py

remove-old-input:
	rm -f $(BERVO_COMPONENT) $(GOOGLE_SHEET_SNAPSHOT) $(GOOGLE_SHEET_EXPORT) bervo_for_sheet.csv

# ----------------------------------------
# curategpt and OAK LLM utilities
# ----------------------------------------
# Optional curation aids, not part of the build or the release (issue #145;
# moved here from the old repository-root Makefile). They index the released
# ontology for curategpt and draft definitions with OAK.
#
# Where each target runs:
#   curategpt-db           needs semsql, rdftab and relation-graph, which the
#                          ODK image has: sh run.sh make curategpt-db
#   curategpt-index*       needs curategpt, which the ODK image lacks: install
#                          it locally and run outside Docker, after building
#                          the database. curategpt 0.2.4 does not declare
#                          psutil, so: pip install curategpt psutil. Its
#                          `view index` also imports paperqa, an optional
#                          extra; curategpt-index fails without it.
#   generate-definitions   needs the OAK llm extension (pip install llm)
# curategpt-index-ontology and generate-definitions call a paid API by
# default, so they need a key (OPENAI_API_KEY) and cost money to run.
# curategpt-index, like the old root target, passes no model and so uses
# curategpt's local embedding model.
#
# The inputs are the released files at the repository root, so the results
# reflect the last release rather than unreleased edits to bervo-src.csv.

CURATEGPT_OWL ?= ../../$(ONT).owl
CURATEGPT_OBO ?= ../../$(ONT).obo
CURATEGPT_DIR = $(TMPDIR)/curategpt
CURATEGPT_DB = $(CURATEGPT_DIR)/$(ONT).db
CURATEGPT_PREFIXES = $(CURATEGPT_DIR)/prefixes.csv
# Embedding model for curategpt-index-ontology. Set it empty to use curategpt's
# local default, which needs no API key: make curategpt-index-ontology CURATEGPT_MODEL=
CURATEGPT_MODEL ?= openai:
# OAK sends every selected term to the model, including terms that already
# have a definition (oaklib's LLMImplementation.generate_definitions does not
# check). Nearly every BERVO term has one, so name the terms you want, e.g.
#   make generate-definitions DEFINITION_TERMS="BERVO:0001234 BERVO:0005678"
DEFINITION_TERMS ?= .all
DEFINITION_STYLE_HINTS = Write definitions as if they come from an ontology of parameters for earth systems modeling.

.PHONY: curategpt-db curategpt-index curategpt-index-ontology generate-definitions

$(CURATEGPT_DIR):
	mkdir -p $@

# semsql has no prefix for the w3id.org BERVO base, so without this it stores
# every term as a full IRI and BERVO: CURIEs find nothing. -P replaces the
# default prefixes rather than adding to them, hence the copy. Written to a
# temporary file first: a partial prefixes.csv would otherwise look up to date
# and quietly produce that full-IRI database. Depends on this makefile because
# the BERVO line is set here.
$(CURATEGPT_PREFIXES): bervo.Makefile | $(CURATEGPT_DIR)
	cat "$$(python3 -c 'import pathlib, semsql; print(pathlib.Path(semsql.__path__[0], "builder", "prefixes", "prefixes.csv"))')" > $@.tmp
	echo 'BERVO,https://w3id.org/bervo/BERVO_' >> $@.tmp
	mv $@.tmp $@

# semsql builds <name>.db from <name>.owl in the same directory.
$(CURATEGPT_DB): $(CURATEGPT_OWL) $(CURATEGPT_PREFIXES) | $(CURATEGPT_DIR)
	cp $< $(CURATEGPT_DIR)/$(ONT).owl
	rm -f $@
	semsql make -P $(CURATEGPT_PREFIXES) $@

curategpt-db: $(CURATEGPT_DB)

# Collection names match the ones the old root Makefile used, so existing
# local curategpt databases keep working.
curategpt-index: $(CURATEGPT_OBO)
	curategpt view index -V oboformat -c $(ONT) --source-locator $<

curategpt-index-ontology: $(CURATEGPT_DB)
	curategpt ontology index -c ont_$(ONT) $(if $(CURATEGPT_MODEL),-m $(CURATEGPT_MODEL)) sqlite:$<

# Writes suggested definitions as KGCL; it does not edit bervo-src.csv.
# Depends on this makefile so that editing DEFINITION_STYLE_HINTS or
# DEFINITION_TERMS here reruns it. A value given on the command line does not
# change any file, so add -B (or delete the output) when you pass one.
$(CURATEGPT_DIR)/definitions.kgcl.json: $(CURATEGPT_DB) bervo.Makefile
	runoak --stacktrace -v -i llm:sqlite:$< generate-definitions $(DEFINITION_TERMS) -O json -o $@ --style-hints "$(DEFINITION_STYLE_HINTS)"

generate-definitions: $(CURATEGPT_DIR)/definitions.kgcl.json
