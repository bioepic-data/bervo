(function () {
  const root = document.getElementById("bervo-browser-root");
  if (!root) {
    return;
  }

  const source = root.dataset.source;
  const bioportalUrl = root.dataset.bioportalUrl;
  const summaryEl = document.getElementById("bervo-browser-summary");
  const searchEl = document.getElementById("bervo-search");
  const categoryFilterEl = document.getElementById("bervo-category-filter");
  const resultCountEl = document.getElementById("bervo-result-count");
  const resultsEl = document.getElementById("bervo-results");
  const detailEl = document.getElementById("bervo-detail");
  const clearEl = document.getElementById("bervo-clear-filters");

  const state = {
    data: null,
    filtered: [],
    selectedId: null,
    query: "",
    category: "",
    entryById: new Map(),
    entryByKey: new Map(),
  };

  function esc(value) {
    return String(value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function prettyNumber(value) {
    return new Intl.NumberFormat().format(value);
  }

  function resolveEntry(term) {
    return state.entryByKey.get(String(term).toLowerCase()) || null;
  }

  function renderChip(item, linkable) {
    const targetEntry = linkable ? resolveEntry(item) : null;
    if (targetEntry) {
      return `<button type="button" class="bervo-browser__chip bervo-browser__chip--link" data-related-term-id="${esc(targetEntry.id)}">${esc(item)}</button>`;
    }
    return `<span class="bervo-browser__chip">${esc(item)}</span>`;
  }

  function chips(items, linkable = false) {
    if (!items || items.length === 0) {
      return '<p class="bervo-browser__empty">None recorded</p>';
    }
    return `<div class="bervo-browser__chip-list">${items
      .map((item) => renderChip(item, linkable))
      .join("")}</div>`;
  }

  function populateSelect(selectEl, values, label) {
    const options = [`<option value="">All ${label}</option>`]
      .concat(
        values.map((value) => `<option value="${esc(value)}">${esc(value)}</option>`)
      )
      .join("");
    selectEl.innerHTML = options;
  }

  function textBlock(title, value) {
    if (!value) {
      return "";
    }
    return `
      <div class="bervo-browser__detail-block">
        <h3>${esc(title)}</h3>
        <p>${esc(value)}</p>
      </div>
    `;
  }

  function listBlock(title, items, linkable = false) {
    if (!items || items.length === 0) {
      return "";
    }
    return `
      <div class="bervo-browser__detail-block">
        <h3>${esc(title)}</h3>
        ${chips(items, linkable)}
      </div>
    `;
  }

  function navigateToTerm(termId) {
    if (!state.entryById.has(termId)) {
      return;
    }

    const visibleInCurrentResults = state.filtered.some((entry) => entry.id === termId);
    if (!visibleInCurrentResults) {
      state.query = "";
      state.category = "";
      searchEl.value = "";
      categoryFilterEl.value = "";
    }

    state.selectedId = termId;
    applyFilters();
  }

  function renderSummary(summary) {
    summaryEl.innerHTML = [
      ["Total terms", prettyNumber(summary.term_count)],
      ["Classes", prettyNumber(summary.class_count)],
      ["Properties", prettyNumber(summary.property_count)],
      ["Concepts", prettyNumber(summary.concept_count)],
    ]
      .map(
        ([label, value]) =>
          `<div class="bervo-browser__card"><p class="bervo-browser__card-label">${label}</p><p class="bervo-browser__card-value">${value}</p></div>`
      )
      .join("");
  }

  function applyFilters() {
    const query = state.query.trim().toLowerCase();
    state.filtered = state.data.entries.filter((entry) => {
      const matchesQuery = !query || entry.search_blob.includes(query);
      const matchesCategory = !state.category || entry.category === state.category;
      return matchesQuery && matchesCategory;
    });

    if (!state.filtered.some((entry) => entry.id === state.selectedId)) {
      state.selectedId = state.filtered[0] ? state.filtered[0].id : null;
    }

    renderResults();
    renderDetail();
  }

  function renderResults() {
    resultCountEl.textContent = `${prettyNumber(state.filtered.length)} terms`;

    if (state.filtered.length === 0) {
      resultsEl.innerHTML =
        '<div class="bervo-browser__card bervo-browser__empty">No BERVO terms match the current filters.</div>';
      return;
    }

    resultsEl.innerHTML = state.filtered
      .slice(0, 300)
      .map((entry) => {
        const activeClass = entry.id === state.selectedId ? " is-active" : "";
        const tags = [entry.type, entry.category].filter(Boolean);
        return `
          <button class="bervo-browser__result${activeClass}" type="button" data-term-id="${esc(entry.id)}">
            <h3 class="bervo-browser__result-title">${esc(entry.label || entry.id)}</h3>
            <p class="bervo-browser__result-id">${esc(entry.id)}</p>
            <div class="bervo-browser__result-meta">
              ${tags.map((tag) => `<span class="bervo-browser__tag">${esc(tag)}</span>`).join("")}
            </div>
          </button>
        `;
      })
      .join("");

    if (state.filtered.length > 300) {
      resultsEl.insertAdjacentHTML(
        "beforeend",
        `<div class="bervo-browser__card bervo-browser__empty">Showing the first 300 matches. Narrow the search to inspect more specific results.</div>`
      );
    }

    resultsEl.querySelectorAll("[data-term-id]").forEach((button) => {
      button.addEventListener("click", () => {
        state.selectedId = button.dataset.termId;
        renderResults();
        renderDetail();
      });
    });
  }

  function renderDetail() {
    const entry = state.filtered.find((item) => item.id === state.selectedId);
    if (!entry) {
      detailEl.innerHTML = `
        <div class="bervo-browser__empty">
          <h2>No BERVO term selected</h2>
          <p>Adjust the filters or choose a result from the list.</p>
        </div>
      `;
      return;
    }

    const definitionBlock = entry.definition
      ? `
        <div class="bervo-browser__detail-block">
          <h3>Definition</h3>
          <p>${esc(entry.definition)}</p>
          ${entry.definition_source ? `<p class="bervo-browser__detail-note">${esc(entry.definition_source)}</p>` : ""}
        </div>
      `
      : "";
    const detailBlocks = [
      textBlock("Comment", entry.comment),
      textBlock("EcoSIM Variable Name", entry.ecosim_variable_name),
      textBlock("File Name", entry.file_name),
      textBlock("Units", entry.has_units),
      listBlock("Parents", entry.parents),
      listBlock("Attributes", entry.attributes, true),
      listBlock("Qualifiers", entry.qualifiers, true),
      listBlock("Measured In", entry.measured_ins, true),
      listBlock("Measurement Of", entry.measurement_ofs, true),
      listBlock("Contexts", entry.contexts, true),
      listBlock("Value Types", entry.value_types, true),
      listBlock("Related Synonyms", entry.related_synonyms),
      listBlock("Exact Synonyms", entry.exact_synonyms),
      listBlock("DbXrefs", entry.dbxrefs),
    ]
      .filter(Boolean)
      .join("");

    detailEl.innerHTML = `
      <div class="bervo-browser__detail-header">
        <div>
          <h2>${esc(entry.label || entry.id)}</h2>
          <p class="bervo-browser__detail-id">${esc(entry.id)}${entry.iri ? ` · <a href="${esc(entry.iri)}" target="_blank" rel="noopener noreferrer">IRI</a>` : ""}</p>
        </div>
        <div class="bervo-browser__detail-links">
          <a class="md-button md-button--primary" href="${esc(entry.bioportal_term_url || bioportalUrl)}" target="_blank" rel="noopener noreferrer">Open this term in BioPortal</a>
          <a class="md-button" href="${esc(entry.source_url)}" target="_blank" rel="noopener noreferrer">Source CSV</a>
        </div>
      </div>

      <div class="bervo-browser__chip-list" style="margin-bottom: 1rem;">
        ${entry.type ? `<span class="bervo-browser__tag">${esc(entry.type)}</span>` : ""}
        ${entry.category ? renderChip(entry.category, true).replace("bervo-browser__chip", "bervo-browser__tag bervo-browser__tag--link") : ""}
        ${entry.group_curated ? `<span class="bervo-browser__tag">${esc(entry.group_curated)}</span>` : ""}
        ${entry.definition_curated ? `<span class="bervo-browser__tag">${esc(entry.definition_curated)}</span>` : ""}
      </div>

      ${definitionBlock}

      <div class="bervo-browser__detail-grid">
        ${detailBlocks}
      </div>
    `;

    detailEl.querySelectorAll("[data-related-term-id]").forEach((button) => {
      button.addEventListener("click", () => {
        navigateToTerm(button.dataset.relatedTermId);
      });
    });
  }

  function bindEvents() {
    searchEl.addEventListener("input", (event) => {
      state.query = event.target.value;
      applyFilters();
    });

    categoryFilterEl.addEventListener("change", (event) => {
      state.category = event.target.value;
      applyFilters();
    });

    clearEl.addEventListener("click", () => {
      state.query = "";
      state.category = "";
      searchEl.value = "";
      categoryFilterEl.value = "";
      applyFilters();
    });
  }

  async function load() {
    try {
      const response = await fetch(source);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      state.data = await response.json();
      state.entryById = new Map(state.data.entries.map((entry) => [entry.id, entry]));
      state.entryByKey = new Map();
      state.data.entries.forEach((entry) => {
        if (entry.id) {
          state.entryByKey.set(entry.id.toLowerCase(), entry);
        }
        if (entry.label) {
          state.entryByKey.set(entry.label.toLowerCase(), entry);
        }
      });
      state.filtered = state.data.entries.slice();
      state.selectedId = state.filtered[0] ? state.filtered[0].id : null;

      populateSelect(categoryFilterEl, state.data.summary.categories, "categories");
      renderSummary(state.data.summary);
      bindEvents();
      applyFilters();
    } catch (error) {
      summaryEl.innerHTML = `<div class="bervo-browser__card bervo-browser__error">Unable to load BERVO browser data: ${esc(error.message)}</div>`;
      resultsEl.innerHTML = "";
      detailEl.innerHTML = `
        <div class="bervo-browser__error">
          <h2>Browser data unavailable</h2>
          <p>Try reloading the page or open the BERVO source CSV directly on GitHub.</p>
        </div>
      `;
    }
  }

  load();
})();
