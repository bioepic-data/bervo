---
description: Add a new term to the BERVO ontology
argument-hint: [term label or a description of the term / issue number]
---

Add a new term to BERVO for: $ARGUMENTS

Use the `bervo-terms` skill. Work through it in order:

1. **Search first** with `just find` on the proposed label and any obvious synonyms.
   If an equivalent term exists, stop and propose a synonym on that term instead.
2. If the argument is an issue number, read it with `gh issue view <n>` and use the
   requester's wording for the label and definition where it is usable.
3. Decide the block (variable / concept / grouping) and allocate the ID with
   `just next-id`.
4. Append the row to `src/ontology/bervo-src.csv` in place, preserving CRLF endings and
   the exact header width.
5. Run `just validate` and `just build`.
6. Report the new term as a table of the populated columns, and call out any column you
   left blank because it needs curator judgement.

Do not commit or push unless asked.
