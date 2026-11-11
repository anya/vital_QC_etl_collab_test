# Editor's guide: editing pages in the browser

It is possible to edit a file on the platform's website and save ("commit") straight to `main`. Alternatively, the teams may agree to work on individual branches until the rule is ratified.

### Creating a new draft page from a proposal issue

- Create a new `.md` file in the right folder (for example `rules/PERSON/`).
- Use the following convention for file names: `PE03-short-slug.md`. The number is the next free number for that prefix (check INDEX.md). **Never reuse a number.**
- Paste the contents of `TEMPLATE.md`, delete the comment blocks and fill in the sections.
- Make sure to replace **every** `TABLENN` with the real ID, including in the three links under the title.
- Set `discussion: "#12"` and the **Origin** link to the proposal issue.
- Keep `status: draft`.

### What to edit when a status changes

The full checklist by outcome is in [GOVERNANCE.md](GOVERNANCE.md), section 8.
In short, the page edits are:

| Change | Edit in the page |
|:---|:---|
| `draft` to `ratified` | `status`, `ratified_on`, status line, first change log row |
| `ratified` to `under-revision` | `status`, `revision_issue: "#31"`, add the "Under revision" line (copy from the comment in TEMPLATE.md) |
| `under-revision` to `ratified` | `status`; remove `revision_issue` and the "Under revision" line; if a change was accepted, new text, new `ratified_on` and a change log row |
| any to `retired` | `status`, `superseded_by` (if replaced), change log row with the reason |
| `draft` to `rejected` | `status`, change log row with the reason |
| abandoned draft | delete the file (history keeps it) and close the issue as "not planned" |

Always update the **Status** word and **Last changed** date in the line under the title as well as `status` in the header. 

### After every rule edit

- [ ] Header `status` and the status line under the title agree
- [ ] Change log row added when a decision was made 
- [ ] `depends_on` / `affects` still correct
- [ ] `sites/conformance.csv` updated if the rule was newly ratified, changed or retired
- [ ] Catalog script ran without errors (INDEX and FIELD-VIEW refresh)

### Commit message guidance

Messages are not parsed by any tool; they are for people browsing the
History button. One line, starting with the rule ID, saying what changed.
Put the reason in the description. Examples:

```
PE02: add "other" to excluded source values
OP01: ratified (meeting 2026-11-18), gap threshold 548 days
README: fix link to governance page
```

### Running the catalog script

To run it by hand on a computer with Python:

```
python scripts/build_catalog.py
```

It rewrites `INDEX.md`, `FIELD-VIEW.md` and `catalog.csv`, and prints any problems it found. Fix the problems on the rule pages, not in the generated files; those are overwritten each time.
