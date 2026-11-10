# Scripts

- `build_catalog.py`: reads the header of every rule page and generates
  `INDEX.md`, `FIELD-VIEW.md` and `catalog.csv`, then checks the repository.
- `omop_fields.csv`: list of OMOP CDM fields (v5.4) used to show which fields
  have no rule. Add more tables as the group takes them on.

Requires Python 3 and PyYAML (`pip install pyyaml`). Run from the repository
root:

    python scripts/build_catalog.py

Exit code is 1 if errors were found, so it can be used as an automatic check
on every save.

## What it checks

Errors (exit code 1):
- header present, valid YAML, required fields filled in
- `status`, `type`, `home_table`, ID format, file name and folder match
- fields are qualified and lowercase (`person.gender_concept_id`)
- `ratified` and `under-revision` have `ratified_on`; `under-revision` has `revision_issue`
- `revision_issue` or `superseded_by` present where the status does not allow it
- links between rules (`depends_on`, `affects`, `supersedes`, `superseded_by`) point to rules that exist
- `superseded_by` does not point to a retired or rejected rule
- site conformance rows: known rule, valid status, `deviation` has a reason
- broken links between pages; issue links with the wrong number of `../`; issue links naming another page's ID (a classic copy-paste slip)

Warnings:
- a rule depends on, or affects, a retired or rejected rule
- a retired rule still has site rows other than `not-applicable`
- a template placeholder (`TABLE-NN`, `YYYY-MM-DD`, `#NN`) is still in a page
- a field is not in `omop_fields.csv`
- a rule page has no change log
