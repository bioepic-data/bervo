---
description: Run BERVO quality checks and summarise what needs attention
argument-hint: ["fast" (default) | "full" for the Docker ODK suite]
---

Run BERVO quality checks. Scope: ${ARGUMENTS:-fast}

**fast** — `just validate` then `just test`. No Docker required.
**full** — the above, then `just build` and `just qc` (ODK suite in Docker; slow).

Then summarise:

- Every **error**, with the row, the term, and the fix.
- **Warnings grouped by kind**, with counts — do not list 60 warnings individually.
  Separate the ones this branch introduced from the pre-existing backlog by checking
  `git diff main...HEAD -- src/ontology/bervo-src.csv`.
- Anything that looks like a regression against `main`.

Recommend the smallest set of fixes worth making now. Do not bulk-fix the pre-existing
warning backlog as a side effect — those need curator judgement.
