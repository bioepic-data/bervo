---
hide:
  - navigation
  - toc
---

# BERVO

[//]: # "This file is meant to be edited by the ontology maintainer."

The Biological and Environmental Research Variable Ontology is a repo-first ontology for earth and environmental research variables. The browser below is generated directly from `src/ontology/bervo-src.csv`, so it will usually reflect newer changes than the current BioPortal release.

<div
  id="bervo-browser-root"
  class="bervo-browser bervo-browser--home"
  data-source="assets/data/bervo-browser.json"
  data-bioportal-url="https://bioportal.bioontology.org/ontologies/BERVO"
>
  <div class="bervo-browser__hero">
    <div>
      <p class="bervo-browser__eyebrow">Ecological Ontology Explorer</p>
      <h1>Browse BERVO terms, concepts, and properties on the docs home page.</h1>
      <p class="bervo-browser__lede">
        Search BERVO IDs, labels, definitions, categories, parentage, units, and curation fields in a lightweight static interface built for GitHub Pages.
      </p>
    </div>
    <div class="bervo-browser__hero-links">
      <a class="md-button md-button--primary" href="https://bioportal.bioontology.org/ontologies/BERVO" target="_blank" rel="noopener noreferrer">View BERVO ontology on BioPortal</a>
      <a class="md-button" href="https://github.com/bioepic-data/bervo/blob/main/src/ontology/bervo-src.csv" target="_blank" rel="noopener noreferrer">View Source CSV</a>
    </div>
  </div>

  <div class="bervo-browser__summary" id="bervo-browser-summary">
    <div class="bervo-browser__card bervo-browser__loading">Loading BERVO browser data...</div>
  </div>

  <div class="bervo-browser__layout">
    <section class="bervo-browser__panel bervo-browser__panel--filters">
      <label class="bervo-browser__field">
        <span>Search</span>
        <input id="bervo-search" type="search" placeholder="Search IDs, labels, definitions, categories..." />
      </label>

      <div class="bervo-browser__filter-grid">
        <label class="bervo-browser__field">
          <span>Type</span>
          <select id="bervo-type-filter">
            <option value="">All types</option>
          </select>
        </label>
        <label class="bervo-browser__field">
          <span>Category</span>
          <select id="bervo-category-filter">
            <option value="">All categories</option>
          </select>
        </label>
      </div>

      <div class="bervo-browser__results-meta">
        <strong id="bervo-result-count">0 terms</strong>
        <button id="bervo-clear-filters" type="button" class="bervo-browser__clear">Clear filters</button>
      </div>

      <div id="bervo-results" class="bervo-browser__results" aria-live="polite"></div>
    </section>

    <section class="bervo-browser__panel bervo-browser__panel--detail">
      <div id="bervo-detail" class="bervo-browser__detail">
        <div class="bervo-browser__empty">
          <h2>Select a BERVO term</h2>
          <p>The detail pane shows definition, parentage, synonyms, and related curation fields.</p>
        </div>
      </div>
    </section>
  </div>

  <div class="bervo-browser__notes">
    <div class="bervo-browser__card">
      <p class="bervo-browser__card-label">Editing Workflow</p>
      <p>The repo-tracked source of truth is <code>src/ontology/bervo-src.csv</code>. The ODK editor file is <code>src/ontology/bervo-edit.owl</code>, and the generated component is <code>src/ontology/components/bervo-src.owl</code>.</p>
    </div>
    <div class="bervo-browser__card">
      <p class="bervo-browser__card-label">Contributing</p>
      <p>Use GitHub issues and pull requests for change requests. The Google Sheet can still support collaboration, but it is not the authoritative source for releases.</p>
    </div>
    <div class="bervo-browser__card">
      <p class="bervo-browser__card-label">Ontology Workflows</p>
      <p>For standard editing and release guidance, see the <a href="odk-workflows/index/">ODK workflow documentation</a>.</p>
    </div>
  </div>

  <noscript>
    <p>This page requires JavaScript. The BERVO source remains available in <a href="https://github.com/bioepic-data/bervo/blob/main/src/ontology/bervo-src.csv">the tracked CSV file</a>.</p>
  </noscript>
</div>
