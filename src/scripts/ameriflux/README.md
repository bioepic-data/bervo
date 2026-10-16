# AmeriFlux inputs for the alignment page

Snapshots read by `src/scripts/generate_ameriflux_doc.py` (`just ameriflux-doc`) to build
`docs/ameriflux-alignment.md`. They are kept here so the page can be rebuilt without network
access and so a change upstream shows up as a reviewable diff.

| File | Source | Fetched | Notes |
| --- | --- | --- | --- |
| `fp_var.tsv` | <https://amfcdn.lbl.gov/api/v1/fp_var> | 2026-10-15 | The AmeriFlux FP-Standard base names: `Name`, `Type`, `Units`, `Description`. |
| `fluxnet_vars.tsv` | <https://fluxnet.org/data/fluxnet2015-dataset/fullset-data-product/> | 2026-10-15 | The FLUXNET FULLSET variables: `section`, `name`, `units`, `description`. The 3 rows whose name is not a variable name are time-resolution notes; the generator skips them. |
| `badm_classified.tsv` | Field names from <https://raw.githubusercontent.com/chuhousen/amerifluxr/master/data-summary/AMF_AA-Net_BIF_LEGACY_VARIABLE-AVAILABILITY_LATEST.csv> | 2026-10-15 | Made for #178, not a download: each legacy BADM field sorted into one of five classes (`a_quantity`, `b_metadata`, `c_admin`, `d_instrument`, `e_disturbance`). The page counts the classes. |
| `page_template.md` | Written for #178 | — | The page's prose, with `{{PLACEHOLDERS}}` for the generated tables. Edit this, not the page. |

## How the generator reads `Comment`

The tables are built from fixed sentences in a term's `Comment`. Each must be a whole
sentence that ends at the code or value, because everything up to the full stop is printed
in a table:

| Sentence | Builds |
| --- | --- |
| `AmeriFlux FP-Standard base name: CODE.` (or `names: A, B.`) | the FP-Standard table |
| `AmeriFlux BADM variable name: CODE.` | the BADM variables table, as current standard |
| `Legacy BADM variable name: CODE.` | the same table, as legacy |
| `Legacy BADM variables mapped here, with the variant in contexts or qualifiers: A, B.` | the same table, as legacy with a variant |
| `AmeriFlux BADM LIST value: Value.` (or `LIST and LIST values: Value.`) | the value-list tables |
| `The LIST value Value maps to Label (BERVO:nnnnnnn).` | the existing-concept mappings |

Put any gloss in a separate sentence: `AmeriFlux BADM DM_TILL value: Stripe till. AmeriFlux
spells it…`, never `…value: Stripe till, which…`. Commas inside a value are allowed, since
some BADM values contain them, so the generator cannot tell a gloss from a value.
`tests/test_ameriflux_doc.py` checks only that the page matches the generator, not that the
values are right; read the page diff after `just ameriflux-doc`.

To refresh a snapshot, fetch it again, keep the same columns, run `just ameriflux-doc`, and
fix whatever coverage problems the script reports before committing.
