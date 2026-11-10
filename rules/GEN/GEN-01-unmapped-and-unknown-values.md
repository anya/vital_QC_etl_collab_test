---
id: GEN-01
title: Unmapped and unknown values
type: global
status: draft
home_table: gen
fields: []
also_tables: []
depends_on: []
affects: [PERSON-02]
supersedes: []
superseded_by: []
ratified_on:
proposed_by: EXAMPLE
discussion: ""
---

# GEN-01: Unmapped and unknown values

> **EXAMPLE PAGE.** Wording is illustrative, to show the template in use.
> It has not been discussed or agreed by the workgroup.
>
> **Status:** draft · [Ask a question](../../../../issues/new?template=question.yml&title=%5BGEN-01%5D+&rule_id=GEN-01) · [Propose a change](../../../../issues/new?template=change-request.yml&title=%5BGEN-01%5D+&rule_id=GEN-01) · [Past discussion](../../../../issues?q=is%3Aissue+%22GEN-01%22) · **Last changed:** 2026-11-04

## Rule

1. When a source value has no mapping to a standard concept, the `*_concept_id`
   field MUST be set to `0`.
2. The original source value MUST be preserved in the corresponding
   `*_source_value` field, without transformation other than trimming
   leading and trailing whitespace.
3. A `NULL` source value MUST be treated the same as an unmapped value: the
   `*_concept_id` is `0` and the `*_source_value` is `NULL`.
4. Sites MUST NOT use any other placeholder (for example `-1`, `999999`, or a
   site-specific concept) in a `*_concept_id` field.
5. Individual field rules MAY refine this behaviour for a specific field, but
   MUST name this rule in `depends_on` and say explicitly where they differ.

## Examples

| Source value | Mapping exists? | `*_concept_id` | `*_source_value` |
|---|---|---|---|
| `"F"` | yes | mapped concept | `F` |
| `"X"` | no | `0` | `X` |
| `NULL` | n/a | `0` | `NULL` |
| `"  X "` | no | `0` | `X` |

## Edge cases and out of scope

- Fields where `0` is not allowed by the CDM (for example required domain
  columns) are not covered; their own rules apply.
- This rule does not decide which values are considered "mapped"; that is the
  mapping tables' job.

## Rationale

Concept `0` is the CDM convention for "no matching concept", and keeping the
source value allows later remapping without re-extraction. Agreeing on a
single convention avoids sites using different sentinel values that break
cross-site queries.

### Alternatives considered

- **Drop rows with unmapped values:** loses data and biases counts.
- **Site-specific placeholder concepts:** not comparable across sites.

### Trade-offs accepted

Sites must retain source values, which may have privacy implications for
free-text fields. Free-text fields are out of scope for this rule.

## Impact on sites

Sites already using a different placeholder must change it. Expected to be
small.

## References

OMOP CDM specification, conventions on `*_concept_id = 0`.

## Change log

| Date (meeting) | Change | Reason | Alternatives rejected / trade-off accepted |
|---|---|---|---|
| 2026-11-04 | Example draft | Demonstrates the template | n/a |
