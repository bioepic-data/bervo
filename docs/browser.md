# BERVO Browser

Explore the current BERVO source tracked in this repository.

The browser below is generated from `src/ontology/bervo-src.csv`, so it will usually reflect newer changes than the ontology currently shown on BioPortal.

<div
  id="bervo-browser-root"
  class="bervo-browser"
  data-source="../assets/data/bervo-browser.json"
  data-bioportal-url="https://bioportal.bioontology.org/ontologies/BERVO"
>
  <div class="bervo-browser__hero">
    <div>
      <p class="bervo-browser__eyebrow">Static BERVO Explorer</p>
      <h1>Browse terms, concepts, and properties without leaving GitHub Pages.</h1>
      <p class="bervo-browser__lede">
        Search by BERVO ID, label, definition, category, parent, or related metadata.
      </p>
    </div>
    <div class="bervo-browser__hero-links">
      <a class="md-button md-button--primary" href="https://bioportal.bioontology.org/ontologies/BERVO" target="_blank" rel="noopener noreferrer">View on BioPortal</a>
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
          <p>The detail pane will show definition, parentage, synonyms, and related curation fields.</p>
        </div>
      </div>
    </section>
  </div>

  <noscript>
    <p>This page requires JavaScript. The BERVO source remains available in <a href="https://github.com/bioepic-data/bervo/blob/main/src/ontology/bervo-src.csv">the tracked CSV file</a>.</p>
  </noscript>
</div>
