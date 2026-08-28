---
name: bervo-pr-review
description: Review a pull request or diff that changes BERVO ontology content - new or edited terms, definitions, hierarchy, or relationships. Use when asked to review a BERVO PR, check a term addition before merging, or assess whether a change to bervo-src.csv is sound.
---

# Reviewing BERVO ontology changes

Ontology review is about *content*, not style. A structurally valid term can still be
the wrong term. Run the mechanical checks first so you can spend attention on the
judgement calls.

## 1. Mechanical checks (do these first)

```bash
just validate          # structural + referential integrity
just test              # validator and integration tests
git diff --stat        # is the diff the size it should be?
```

If `just validate` reports errors, stop and report them — everything else is moot.

## 2. Scope check

Flag these before reading the content:

- **Regenerated artefacts in a content PR.** `bervo.owl`, `bervo-full.*`, `site/`, or
  `docs/assets/data/bervo-browser.json` alongside a handful of new terms. These belong
  in a release, not a content change; they hide the real edit.
- **A whole-file CSV rewrite.** If `git diff --stat` shows ~2,300 changed rows for a
  few new terms, the file was re-encoded (CRLF → LF, or requoted). Ask for it to be
  redone in place.
- **Hand-edited generated files.** `src/ontology/components/bervo-src.owl` is a tracked
  build product, and a content PR is *expected* to commit it regenerated alongside the
  CSV edit — that is not a problem. What is a problem is a component diff that does not
  correspond to the CSV diff: axioms changed that no CSV cell explains, or a component
  change with no CSV change at all. That means someone edited the build output by hand,
  and the next `just build` will silently discard it. Spot-check that each changed axiom
  traces back to a changed cell.

## 3. Content review

For each added or changed term:

**Identity**
- Does an equivalent term already exist? Check with `just find` on the label and on
  each synonym. This is the single most valuable thing a reviewer does.
- Is the ID from the right block (`0` variables, `8` concepts, `9` groupings) and
  genuinely unused? Is it the next free ID rather than an arbitrary one?
- Is the label unique, and does it read consistently with its siblings? Compare against
  `just show` output for a few terms sharing the parent.

**Definition**
- Present, and not a restatement of the label.
- A noun phrase describing what the thing *is*, in the house style used by neighbouring
  terms.
- `Definition Source` filled in. Machine-generated definitions should say so.
- Scientifically accurate for the domain. If you cannot judge, say so explicitly rather
  than approving by default.

**Placement**
- Is `Category` the most specific correct parent? A term parented directly to a broad
  grouping when a narrower one exists is a common and easily fixed problem.
- Does the parent make sense as an `is-a`? "Soil carbon content *is a* soil variable"
  should read true.

**Relationships**
- `has_units` holds a literal unit string (or `NONE`) — not a term reference.
- `attributes`, `measured_ins`, `measurement_ofs`, `qualifiers`, `contexts`, and
  `value_types` must name existing terms. `just validate` warns when they do not, with
  a suggested spelling for case-only typos.
- Blank means "not yet curated", `NA` means "not applicable". Silently converting one to
  the other loses information.

## 4. Report

Lead with anything blocking, then the judgement calls, then nits — and say which is
which. Be concrete: quote the row, name the term, and propose the fix.

Distinguish clearly between:

- **Blocking** — validator errors, wrong or reused IDs, duplicate terms, edits to
  generated files.
- **Should fix** — missing or weak definitions, an over-broad parent, a dangling
  relationship label.
- **Optional** — wording, ordering, a synonym worth adding.

If the change needs domain expertise you do not have — whether a variable is
scientifically distinct from an existing one, whether a unit is right — say that
plainly and name the question for a curator, rather than approving or blocking on a
guess.
