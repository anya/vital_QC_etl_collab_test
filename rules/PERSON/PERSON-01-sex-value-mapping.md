---
id: PE01
title: Sex value mapping
type: field
status: draft
home_table: person
fields: [person.gender_concept_id, person.gender_source_value, person.gender_source_concept_id]
also_tables: []
depends_on: [GEN01]
affects: [PE02]
ratified_on:
discussion: ""
---

## PE01: Sex value mapping

- [Ask a question](../../../../issues/new?template=question.yml&title=%5BPERSON-01%5D+&rule_id=PE01) 
- [Propose a change](../../../../issues/new?template=change-request.yml&title=%5BPERSON-01%5D+&rule_id=PE01)
- [Past discussion](../../../../issues?q=is%3Aissue+%22PE01%22)

### Context

`person.gender_concept_id` is a required field in OMOP CDM 5.4 and MUST be populated using only the following standard concepts from the Gender domain: 8507 (MALE) and 8532 (FEMALE). The CDM 5.4 documentation says the field "is meant to capture the biological sex at birth", not gender identity. 

### Rule

- Use the source system field capturing **sex at birth** regardless of how the source calls it ("sex", "gender", "sex at birth").
- Map source values that can be clearly identified as either Male or Female onto corresponding standard concept IDs to populate `person.gender_concept_id`; map all other values to 0.
- `person.gender_source_concept_id` MUST be `0` unless the site has a source vocabulary loaded in which that value is a concept; then it is that concept's ID.
- `person.gender_source_value` MUST contain the original source value (trimmed), as required by GEN01.

Examples:
| Source `sex` | `gender_concept_id` | `gender_source_value` | `gender_source_concept_id` |
|---|---|---|---|
| `"Male"` | 8507 | `Male` | 0 |
| `"f "` | 8532 | `f` | 0 |
| `"U"` | see PE02 | `U` | 0 |
| `"O"` | see PE02 | `U` | 0 |

### Rationale

The CDM expects one value from the Gender domain, and cross-site
cohort definitions depend on every site using the same two concepts for the
same meaning. Fixing the concept IDs removes the risk of sites choosing
different (but equivalent-looking) concepts.

### Alternatives considered

- Use a wider set of concepts from the Gender domain: may be appropriate later, but see PE02.

### Trade-offs accepted

We accept a coarse standard representation: whatever the source holds is forced into two categories plus unknown. The source variability is preserved in `gender_source_value` field.

## References

[OMOP CDM v5.4, PERSON table](https://ohdsi.github.io/CommonDataModel/cdm60.html#person), `gender_concept_id`.

#### Change log

| Date&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | Decision record (consider ARD Y-statement format) |
|:---|:---|
| 2026-11-04 | To comply with the CDM 5.4 specification, decided to use sex at birth and capture only 2 sexes as standard concepts in `gender_concept_id` and the rest as unknown, retaining source variety in `gender_source_value` |
