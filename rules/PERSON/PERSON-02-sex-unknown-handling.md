---
id: PERSON-02
title: Sex unknown and non-binary values
type: field
status: draft
home_table: person
fields: [person.gender_concept_id, person.gender_source_value]
also_tables: []
depends_on: [GEN-01, PERSON-01]
affects: []
supersedes: []
superseded_by: []
ratified_on:
proposed_by: EXAMPLE
discussion: ""
---

# PERSON-02: Sex unknown and non-binary values

> **EXAMPLE PAGE.** Illustrative only, to show how one field can be governed
> by several rules and how an open question is shown. Not agreed.
>
> **Status:** draft · [Ask a question](../../../../issues/new?template=question.yml&title=%5BPERSON-02%5D+&rule_id=PERSON-02) · [Propose a change](../../../../issues/new?template=change-request.yml&title=%5BPERSON-02%5D+&rule_id=PERSON-02) · [Past discussion](../../../../issues?q=is%3Aissue+%22PERSON-02%22) · **Last changed:** 2026-11-04

## Rule

1. A source value that is missing, blank, or explicitly "unknown" MUST
   result in `gender_concept_id = 0` (per GEN-01).
2. A source value that is not male or female (for example "other",
   "non-binary", "indeterminate") MUST also result in `gender_concept_id = 0`
   in the shared dataset, and the original value MUST be kept in
   `gender_source_value`.
3. Persons MUST NOT be dropped from `person` because of their sex value.

## Examples

| Source `sex` | `gender_concept_id` | `gender_source_value` |
|---|---|---|
| `NULL` | 0 | `NULL` |
| `""` | 0 | `NULL` |
| `"Unknown"` | 0 | `Unknown` |
| `"Other"` | 0 | `Other` |

## Edge cases and out of scope

- When several source systems give different sex values for one person, the
  precedence is decided in a separate rule (to be proposed). Until then,
  each site documents its own approach as a deviation.
- Small cell counts for rare values are a disclosure-control matter, not an
  ETL matter.

## Rationale

Forcing "other" values into male or female would misrepresent the data;
dropping persons would bias denominators. Mapping to `0` and keeping the
source value is the least lossy option that stays within the standard
concept set.

### Alternatives considered

- **Map "other" values to a Gender-domain concept for them, where one
  exists:** more informative, but the set of available concepts and their
  acceptability is itself an open question for the group.
- **Drop persons with unknown sex:** rejected, would bias populations.

### Trade-offs accepted

Non-binary persons become indistinguishable from unknown in the standard
field; the distinction survives only in `gender_source_value`.

## Impact on sites

Sites currently mapping "other" to a concept must switch to `0`.

## References

GEN-01; PERSON-01.

## Change log

| Date (meeting) | Change | Reason | Alternatives rejected / trade-off accepted |
|---|---|---|---|
| 2026-11-04 | Example draft | Demonstrates the template | n/a |
