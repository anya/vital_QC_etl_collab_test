# Cross-site OMOP ETL rules for VITAL-QC

This repository holds the ETL rules that all participating sites have agreed to
harmonize when populating OMOP CDM tables. One page = one rule = one decision
that the workgroup can ratify or revise independently. The pages hold the
current rule; discussion happens in GitHub issues.

**Looking for something?**

| I want to... | Go to |
|:---|:---|
| See every rule and its status | [INDEX.md](INDEX.md) (generated) |
| See which rules govern a given OMOP field | [FIELD-VIEW.md](FIELD-VIEW.md) (generated) |
| Read the rules for one table | `rules/<TABLE>/<TABLE>-overview.md` |
| Propose a rule, ask a question, or suggest a change | [HOW-TO-PROPOSE.md](HOW-TO-PROPOSE.md) |
| Understand how decisions get made | [GOVERNANCE.md](GOVERNANCE.md) |
| See what each site has implemented | [sites/conformance.csv](sites/conformance.csv) |
| Edit pages (editor's guide) | [HOW-TO-EDIT.md](HOW-TO-EDIT.md) |

### Folder structure

```
rules/
  GEN/                  cross-cutting conventions (nulls, dates, IDs...)
  PERSON/               one folder per OMOP table the group has rules for
  OBSERVATION_PERIOD/
  VISIT_OCCURRENCE/
  VOCAB/                vocabulary policy (not individual mappings)
  POP/                  population / scope rules
.github/ISSUE_TEMPLATE/ forms: propose a rule, propose a change, ask a question
sites/                  per-site conformance and deviations
scripts/                catalog generator and consistency checks
TEMPLATE.md             blank rule page, copy this
```
- Rule IDs look like `PE01`. The number is permanent and never reused.
- Rules can refer to one or more OMOP CDM fields. The teams agreed to have at least one rule that coves every field, even if it is simply a reference to an existing CDM specification or Themis convention.

### Rule statuses

| Status | Meaning | Implementers should |
|:---|:---|:---|
| `draft` | New rule, not yet agreed | Not implement |
| `ratified` | Agreed, in force | Implement |
| `under-revision` | Ratified; a change is being decided. Still in force | Keep implementing the current text |
| `retired` | Was ratified, no longer in force | Stop; follow the replacement if any |
| `rejected` | Proposed and declined | Not implement |

### Rule structure

- Every rule page starts with a standard header (front matter) using a fixed
vocabulary ([ALLOWED-VALUES.md](ALLOWED-VALUES.md)).
- The page describes the context/setting in which the rule exists.
- The rule text uses MUST / SHOULD / MAY in the RFC 2119 sense.
- The page also documents the alternatives to the rule and the tradeoffs the teams accepted as a result of the rule.
- The change log at the bottom of each page is written by hand by the editor after each decision.
- Each page links to the issue it came from, other issues discussing the rule, and to forms for asking a question or proposing a change.

### What this repo is not

- Not a store of individual source-to-concept mappings (those live in mapping tables with their own review).
- Not a restatement of the OMOP CDM specification or OHDSI Themis conventions; link to them instead.
- Not a record of meeting minutes. Decisions are recorded in each page's change log and in the outcome comment on the issue.
