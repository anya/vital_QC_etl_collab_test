---
id: TABLENN                  # e.g. PE01. Use two letters for CDM tables, or: GEN | VOCAB | POP. Number is permanent, never reused.
title: Short descriptive title
type: field                  # field | table | relationship | global | vocabulary | population
status: draft                # draft | ratified | under-revision | retired | rejected
home_table: person           # lowercase OMOP table, or: gen | vocab | pop
fields: []                   # qualified and lowercase, e.g. [person.gender_concept_id]
also_tables: []              # other tables touched (mainly for relationship rules)
depends_on: []               # rule IDs this rule relies on, e.g. [GEN01]
affects: []                  # rule IDs that must be reviewed if this one changes
supersedes: []               # rule IDs this rule replaces (informational)
superseded_by: []            # only when status = retired and another rule replaces this one
ratified_on:                 # YYYY-MM-DD of the meeting that ratified it; empty for draft/rejected
revision_issue: ""           # required while status = under-revision, in quotes, e.g. "#31"
proposed_by:                 # name
discussion: ""               # the proposal issue this rule came from, in quotes, e.g. "#12"
---

<!-- 
Replace every TABLE-NN with the real ID, in the header AND in the three links below.
The links assume the file sits two folders deep (rules/<TABLE>/). The catalog script reports
any placeholder or wrong ID you leave behind.
-->

[Ask a question](../../../../issues/new?template=question.yml&title=%5BTABLE-NN%5D+&rule_id=TABLENN) | 
[Propose a change](../../../../issues/new?template=change-request.yml&title=%5BTABLE-NN%5D+&rule_id=TABLENN) |
[Past discussion](../../../../issues?q=is%3Aissue+%22TABLENN%22)

# TABLENN: Title

> **Status:** draft · **Origin:** [#12](../../../../issues/12) · **Last changed:** YYYY-MM-DD

<!-- 
WHEN THE STATUS IS under-revision, add this line under the status line (replace #31):
> **Under revision:** a change is being decided in [#31](../../../../issues/31). The text below stays in force until a change is ratified.
-->

### Context

Describe the context for creating this rule: use case, setting, task, ...

### Rule

State the rule in precise terms. Use MUST / SHOULD / MAY as in RFC 2119.
Someone who has never seen your source system should be able to implement
this without asking a question.

Describe handling of edge cases (what happens when the source value is missing, conflicting or unexpected) and
what's out of scope (what this rule deliberately does NOT decide and where that is decided instead).

Include examples: a small synthetic source input and the exact
OMOP output it must produce. Include at least one edge case.

| Source | Result in OMOP for a given field |
|---|---|
| ... | ... |

### Rationale

Why this rule exists, in a few lines. Which problem does it solve for the network?

### Alternatives considered

- **Alternative A:** why not.
- **Alternative B:** why not.

### Trade-offs accepted

What do we knowingly give up with this rule?

## References

CDM spec section, Themis convention, forum thread, paper.

### Change log

<!-- Remove the instructions below, keep only the table -->
Newest first. One row per decision (not per text changes on the page). The first row records the
original choice. Rejection, retirement and dissent are recorded here too, with the reason. 
Get insired by the [ADR Y-statements](https://adr.github.io/adr-templates/#y-statement) to consicely summarize the decision.

| Date&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | Decision record (consider ARD Y-statement format) |
|:---|:---|
| YYYY-MM-DD |  In the context of `use case/user story`, facing `concern` we decided for `option` to achieve `quality`, accepting `downside/tradeoff`. |
