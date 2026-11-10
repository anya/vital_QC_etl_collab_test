<!--
HOW TO USE THIS TEMPLATE
1. Copy this file to rules/<TABLE>/<TABLE>-NN-short-slug.md (next free number; never reuse one).
2. Replace every TABLE-NN with the real ID, in the header AND in the three links below the title.
   The links assume the file sits two folders deep (rules/<TABLE>/). The catalog script reports
   any placeholder or wrong ID you leave behind.
3. Delete this comment block.

WHEN THE STATUS IS under-revision, add this line under the status line (replace #31):
> **Under revision:** a change is being decided in [#31](../../../../issues/31). The text below stays in force until a change is ratified.
-->
---
id: TABLE-NN                 # e.g. PERSON-01. Number is permanent, never reused.
title: Short descriptive title
type: field                  # field | table | relationship | global | vocabulary | population
status: draft                # draft | ratified | under-revision | retired | rejected
home_table: person           # lowercase OMOP table, or: gen | vocab | pop
fields: []                   # qualified and lowercase, e.g. [person.gender_concept_id]
also_tables: []              # other tables touched (mainly for relationship rules)
depends_on: []               # rule IDs this rule relies on, e.g. [GEN-01]
affects: []                  # rule IDs that must be reviewed if this one changes
supersedes: []               # rule IDs this rule replaces (informational)
superseded_by: []            # only when status = retired and another rule replaces this one
ratified_on:                 # YYYY-MM-DD of the meeting that ratified it; empty for draft/rejected
revision_issue: ""           # required while status = under-revision, in quotes, e.g. "#31"
proposed_by:                 # name
discussion: ""               # the proposal issue this rule came from, in quotes, e.g. "#12"
---

# TABLE-NN: Title

> **Status:** draft · **Origin:** [#12](../../../../issues/12) · [Ask a question](../../../../issues/new?template=question.yml&title=%5BTABLE-NN%5D+&rule_id=TABLE-NN) · [Propose a change](../../../../issues/new?template=change-request.yml&title=%5BTABLE-NN%5D+&rule_id=TABLE-NN) · [Past discussion](../../../../issues?q=is%3Aissue+%22TABLE-NN%22) · **Last changed:** YYYY-MM-DD

## Rule

State the rule in precise terms. Use MUST / SHOULD / MAY as in RFC 2119.
Someone who has never seen your source system should be able to implement
this without asking a question.

1. ...
2. ...

## Examples

At least two worked examples: a small synthetic source input and the exact
OMOP output it must produce. Include at least one edge case.

| Source | Result in OMOP |
|---|---|
| ... | ... |

## Edge cases and out of scope

- What happens when the source value is missing, conflicting or unexpected?
- What this rule deliberately does NOT decide (and where that is decided).

## Rationale

Why this rule exists, in a few lines. Which problem does it solve for the
network?

### Alternatives considered

- **Alternative A:** why not.
- **Alternative B:** why not.

### Trade-offs accepted

What do we knowingly give up with this rule?

## Impact on sites

Who has to change what compared with a plain reading of the CDM spec or with
the previous version of this rule? Per-site status lives in
[sites/conformance.csv](../../sites/conformance.csv), not here.

## References

CDM spec section, Themis convention, forum thread, paper.

## Change log

Newest first. One row per decision (not per typo). The first row records the
original choice and the alternatives that lost. Rejection, retirement and
dissent are recorded here too, with the reason.

| Date (meeting) | Change | Reason | Alternatives rejected / trade-off accepted |
|---|---|---|---|
| YYYY-MM-DD | Initial rule | ... | ... |
