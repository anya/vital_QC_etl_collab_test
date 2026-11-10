# Editor's guide: editing pages in the browser

No branches, no pull requests. You edit a file on the platform's website and
save ("commit") straight to `main`.

## Edit an existing page

1. Open the file in the repository on the website.
2. Click the pencil icon ("Edit this file").
3. Change the text. Use the Preview tab to check the layout.
4. At the bottom, in the commit box:
   - **Title** (one line): `PERSON-02: handle unknown sex values`
   - **Description** (optional but encouraged): the reason, and the meeting date
5. Choose **"Commit directly to the main branch"** and click Commit.

## Create a draft page from a proposal issue

1. Navigate to the right folder (for example `rules/PERSON/`).
2. "Add file", then "Create new file".
3. Type the file name: `PERSON-03-short-slug.md`. The number is the next free
   number for that prefix (check INDEX.md). **Never reuse a number.**
4. Paste the contents of `TEMPLATE.md`, delete the comment block at the top,
   and fill it in.
5. Replace **every** `TABLE-NN` with the real ID, including in the three links
   under the title. Set `discussion: "#12"` and the **Origin** link to the
   proposal issue. Keep `status: draft`.
6. Commit as above, then post a comment in the issue linking to the new page.

## What to edit when a status changes

The full checklist by outcome is in [GOVERNANCE.md](GOVERNANCE.md), section 8.
In short, the page edits are:

| Change | Edit in the page |
|---|---|
| `draft` to `ratified` | `status`, `ratified_on`, status line, first change log row |
| `ratified` to `under-revision` | `status`, `revision_issue: "#31"`, add the "Under revision" line (copy it from the comment at the top of TEMPLATE.md) |
| `under-revision` to `ratified` | `status`; remove `revision_issue` and the "Under revision" line; if a change was accepted, new text, new `ratified_on` and a change log row |
| any to `retired` | `status`, `superseded_by` (if replaced), change log row with the reason |
| `draft` to `rejected` | `status`, change log row with the reason |
| abandoned draft | delete the file (history keeps it) and close the issue as "not planned" |

Always update the **Status** word and **Last changed** date in the line under
the title as well as `status` in the header. The script checks the header, not
the line under the title.

## After every rule edit

- [ ] Header `status` and the status line under the title agree
- [ ] Change log row added when a decision was made (date, change, reason, alternatives or trade-off)
- [ ] `depends_on` / `affects` still correct
- [ ] `sites/conformance.csv` updated if the rule was newly ratified, changed or retired
- [ ] Catalog script ran without errors (INDEX and FIELD-VIEW refresh)

## Commit message guidance

Messages are not parsed by any tool; they are for people browsing the
History button. One line, starting with the rule ID, saying what changed.
Put the reason in the description. Examples:

```
PERSON-02: add "other" to excluded source values
OBSERVATION_PERIOD-01: ratified (meeting 2026-11-18), gap threshold 548 days
README: fix link to governance page
```

## If you make a mistake

Every saved version is kept. On the file's History page you can open an older
version and copy its text back. A colleague comfortable with git can also use
the Revert button. Nothing is lost.

## Running the catalog script

Normally this runs automatically (once someone sets that up; see
`scripts/README.md`). To run it by hand on a computer with Python:

```
python scripts/build_catalog.py
```

It rewrites `INDEX.md`, `FIELD-VIEW.md` and `catalog.csv`, and prints any
problems it found. Fix the problems on the rule pages, not in the generated
files; those are overwritten each time.
