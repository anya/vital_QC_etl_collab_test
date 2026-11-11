---
id: PE00
title: PERSON table overview
type: hub
home_table: person
---

# PERSON: overview

> This page is a guide, not a rule. It needs no ratification.

## Purpose of the table in this network

One row per individual in the study population. What counts as "an
individual" and how persons from different source systems are linked is
decided in the population rules (see `POP`).

## Rules for this table

The authoritative, always-current list is generated:
see [INDEX.md](../../INDEX.md) (filter by table `person`) and
[FIELD-VIEW.md](../../FIELD-VIEW.md) (all `person.*` fields, with the rules
that govern each and the fields that have none).

| Rule | Title |
|---|---|
| [PE01](PE01-sex-value-mapping.md) | Sex: value mapping |

## Fields with no network rule

Fields not covered by a rule follow the OMOP CDM specification and OHDSI
Themis conventions as-is. That is a deliberate default, not an oversight;
FIELD-VIEW.md lists the fields concerned.

## Open questions

Add links to open issues about this table here.

## Dependencies on other tables

- `person.location_id` is governed by the LOCATION rules.
- `observation_period` rows require a `person` row; see OBSERVATION_PERIOD.
