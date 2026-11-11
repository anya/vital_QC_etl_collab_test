# Allowed values for rule headers

> The catalog script rejects anything not on this list. 

### `status`

| Value | Meaning | An implementer should... |
|:---|:---|:---|
| `draft` | New rule, not yet agreed. Created by the editor from a proposal issue once there is wording to review, or after a meeting that discussed it without reaching agreement. Wording may change freely. | Not implement it. Read it to see where things are heading. |
| `ratified` | Agreed by the group and in force. | Implement it. |
| `under-revision` | A ratified rule for which a change is being decided. **The rule stays in force.** The page keeps showing the current text; the proposed change lives in the change-request issue named in `revision_issue`. | Keep implementing the current text, and expect it may change. |
| `retired` | Was ratified, no longer in force: duplicate of another rule, split into several, now covered by a standard, no longer wanted, or out of scope. The replacement (if any) is in `superseded_by`; the reason is in the change log. | Stop applying it. Follow the replacement, if any. |
| `rejected` | Proposed and declined by the group. Never ratified. Kept so the same idea is not proposed again unnoticed. | Not implement it. |

There is no "withdrawn" status. If a proposer abandons a draft, the editor
deletes the draft page (git keeps its history) and closes the issue as
"not planned". A proposal that never had a page and is declined needs no
page either: its issue is closed with the label `rejected`.

Allowed transitions:

```
proposal issue -> draft -> ratified <-> under-revision
                    |         |             |
                    v         v             v
                 rejected   retired <-------+
```

`rejected` and `retired` are final. A revived idea is a new proposal and
gets a new rule ID.

### Header fields that depend on status

| Status | Required | Must be empty |
|:---|:---|:---|
| `draft` | | `ratified_on`, `revision_issue`, `superseded_by` |
| `ratified` | `ratified_on` | `revision_issue`, `superseded_by` |
| `under-revision` | `ratified_on`, `revision_issue` | `superseded_by` |
| `retired` | (reason goes in the change log) | `revision_issue`. `superseded_by` is optional. |
| `rejected` | (reason goes in the change log) | `ratified_on`, `revision_issue`, `superseded_by` |

Always put issue numbers in quotes: `revision_issue: "#31"`. Without quotes,
the YAML format treats `#31` as a comment and the field looks empty.

### `type`

| Value | Use for |
|:---|:---|
| `field` | How one or more fields are derived |
| `table` | What a row is, and which source data creates rows |
| `relationship` | How rows in different tables link or depend on each other |
| `global` | Conventions that apply everywhere |
| `vocabulary` | Policy about concepts and mapping method, not individual mappings |
| `population` | Who and what is in scope at all |
| `hub` | Overview page of a table (not a rule, never ratified, has no status) |

### `home_table`

Lowercase OMOP table name (`person`, `observation_period`, `visit_occurrence`...),
or one of `gen`, `vocab`, `pop`. A relationship rule lives in the folder of its
driving table; list the others in `also_tables`.

### `fields`

Qualified, lowercase: `person.gender_concept_id`. Never a bare field name.

### `discussion`

The proposal issue this rule came from, in quotes: `"#12"`. Later questions
and change requests are found through the "Past discussion" link on the page.

### Rule IDs

`PREFIXNN`, where PREFIX is the two-letter table acronym or `GEN` | `VOCAB` |`POP`, and NN is a
two-digit number. `00` is reserved for the table overview page. Numbers are never reused.

