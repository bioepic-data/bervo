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

.PHONY: refresh-google-sheet-snapshot compare-google-sheet export-google-sheet remove-old-input

# Build the ODK-managed component from the repo-tracked template.
$(BERVO_COMPONENT): $(BERVO_TEMPLATE) bervo-annotations.ttl | $(COMPONENTSDIR)
	$(ROBOT) template \
	  --add-prefix 'BERVO: https://w3id.org/bervo/BERVO_' \
	  --add-prefix 'oio: http://www.geneontology.org/formats/oboInOwl#' \
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

remove-old-input:
	rm -f $(BERVO_COMPONENT) $(GOOGLE_SHEET_SNAPSHOT) $(GOOGLE_SHEET_EXPORT) bervo_for_sheet.csv
