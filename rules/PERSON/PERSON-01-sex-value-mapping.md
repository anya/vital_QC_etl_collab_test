---
id: PERSON-01
title: Sex value mapping
type: field
status: draft
home_table: person
fields: [person.gender_concept_id, person.gender_source_value, person.gender_source_concept_id]
also_tables: []
depends_on: [GEN-01]
affects: [PERSON-02]
supersedes: []
superseded_by: []
ratified_on:
proposed_by: EXAMPLE
discussion: ""
---

# PERSON-01: Sex value mapping

> **EXAMPLE PAGE.** The wording and the choice made here are illustrative,
> to show the template in use. They have not been discussed or agreed.
> Verify the concept IDs against the agreed vocabulary version.
>
> **Status:** draft · [Ask a question](../../../../issues/new?template=question.yml&title=%5BPERSON-01%5D+&rule_id=PERSON-01) · [Propose a change](../../../../issues/new?template=change-request.yml&title=%5BPERSON-01%5D+&rule_id=PERSON-01) · [Past discussion](../../../../issues?q=is%3Aissue+%22PERSON-01%22) · **Last changed:** 2026-11-04

## Rule

1. `person.gender_concept_id` MUST be populated from the sex recorded in the
   source, using only these standard concepts from the Gender domain:

   | Meaning | `gender_concept_id` | Concept name |
   |---|---|---|
   | Male | 8507 | MALE |
   | Female | 8532 | FEMALE |

2. The field records **sex as recorded in the source system**, whatever the
   source calls it ("sex", "gender", "sex at birth"). This rule does not
   distinguish between them. If sites hold both, see PERSON-02.
3. `person.gender_source_value` MUST contain the original source value
   (trimmed), as required by GEN-01.
4. `person.gender_source_concept_id` MUST be `0` unless the site has a
   source vocabulary loaded in which that value is a concept; then it is
   that concept's ID.
5. Values that cannot be mapped to the two concepts above are handled by
   PERSON-02.

## Examples

| Source `sex` | `gender_concept_id` | `gender_source_value` | `gender_source_concept_id` |
|---|---|---|---|
| `"M"` | 8507 | `M` | 0 |
| `"Female"` | 8532 | `Female` | 0 |
| `"f "` | 8532 | `f` | 0 |
| `"U"` | see PERSON-02 | `U` | 0 |

## Edge cases and out of scope

- Case and whitespace variants of the same code map to the same concept.
- What to do with values other than male/female is decided in PERSON-02,
  not here.
- This rule does not cover gender identity, which OMOP stores elsewhere if
  at all.

## Rationale

The CDM expects one value from the Gender domain, and cross-site
cohort definitions depend on every site using the same two concepts for the
same meaning. Fixing the concept IDs removes the risk of sites choosing
different (but equivalent-looking) concepts.

### Alternatives considered

- **Leave mapping to each site:** simplest, but cohort definitions then need
  per-site adjustments.
- **Use a wider set of concepts from the Gender domain:** may be appropriate
  later, but see PERSON-02.

### Trade-offs accepted

We accept a coarse representation: whatever the source holds is forced into
two categories plus unknown.

## Impact on sites

Sites already using only 8507 and 8532 need no change. Sites using other
concepts, or populating `gender_source_concept_id` differently, must adapt.

## References

OMOP CDM v5.4, PERSON table, `gender_concept_id`.

## Change log

| Date (meeting) | Change | Reason | Alternatives rejected / trade-off accepted |
|---|---|---|---|
| 2026-11-04 | Example draft | Demonstrates the template | n/a |
