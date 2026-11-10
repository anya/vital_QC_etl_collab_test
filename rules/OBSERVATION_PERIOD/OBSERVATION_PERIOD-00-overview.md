---
id: OBSERVATION_PERIOD-00
title: OBSERVATION_PERIOD table overview
type: hub
home_table: observation_period
---

# OBSERVATION_PERIOD: overview

> This page is a guide, not a rule. It needs no ratification.

## Purpose of the table in this network

`observation_period` states when a person's events can be assumed to be
recorded in the source. Analyses rely on it as the denominator window: an
absence of an event only means something inside an observation period.
Decisions here therefore affect almost every downstream analysis.

## Rules for this table

See the generated [INDEX.md](../../INDEX.md) and
[FIELD-VIEW.md](../../FIELD-VIEW.md).

| Rule | Title |
|---|---|
| [OBSERVATION_PERIOD-01](OBSERVATION_PERIOD-01-periods-per-person.md) | Number of observation periods per person |

## Related rules to be proposed

- How `observation_period_start_date` and `_end_date` are derived.
- Handling of events that fall outside any observation period.
- `period_type_concept_id` value to use.

## Dependencies on other tables

Depends on `person`. Visit and event rules assume observation periods exist.
