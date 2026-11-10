---
id: OBSERVATION_PERIOD-01
title: Number of observation periods per person
type: table
status: draft
home_table: observation_period
fields: [observation_period.observation_period_start_date, observation_period.observation_period_end_date]
also_tables: [person]
depends_on: []
affects: []
supersedes: []
superseded_by: []
ratified_on:
proposed_by: EXAMPLE
discussion: ""
---

# OBSERVATION_PERIOD-01: Number of observation periods per person

> **EXAMPLE PAGE.** This page shows how a genuinely open design question
> can be laid out for the group. The "proposed rule" is a placeholder for
> discussion, not a recommendation or an agreed position.
>
> **Status:** draft · [Ask a question](../../../../issues/new?template=question.yml&title=%5BOBSERVATION_PERIOD-01%5D+&rule_id=OBSERVATION_PERIOD-01) · [Propose a change](../../../../issues/new?template=change-request.yml&title=%5BOBSERVATION_PERIOD-01%5D+&rule_id=OBSERVATION_PERIOD-01) · [Past discussion](../../../../issues?q=is%3Aissue+%22OBSERVATION_PERIOD-01%22) · **Last changed:** 2026-11-04

## Rule (proposed wording, to be decided)

1. Each person in `person` MUST have at least one row in
   `observation_period`.
2. A person MAY have more than one observation period only if two
   consecutive periods are separated by a gap of more than **G days**, where
   G is [to be decided; see Alternatives].
3. Observation periods of one person MUST NOT overlap, and
   `observation_period_start_date` MUST be on or before
   `observation_period_end_date`.
4. Where the source records no gap longer than G days, the person has
   exactly one period.

## Examples

G = 548 days (illustration only).

| Source activity dates for one person | Result |
|---|---|
| 2018-03-01, 2018-09-10, 2019-02-02 | 1 period: 2018-03-01 to 2019-02-02 |
| 2015-01-10, 2015-06-01, then 2019-03-05 | 2 periods: 2015-01-10 to 2015-06-01, and 2019-03-05 onward (gap of 1,373 days) |
| One single encounter on 2020-05-05 | 1 period: 2020-05-05 to 2020-05-05 |

## Edge cases and out of scope

- How the start and end dates are derived (first and last event? first and
  last visit? enrolment dates?) is a separate rule.
- What to do with events outside the observation period is a separate rule.
- Persons with no events at all: whether they get a period is a population
  question (see `POP`).

## Rationale

Observation periods are the denominator for incidence and prevalence
calculations. If a person had no contact with the system for years, treating
those years as observed would overstate follow-up and understate event
rates. Conversely, splitting too eagerly creates many short periods and
discards legitimate follow-up between sparse visits.

### Alternatives considered

- **A. Exactly one period per person (first to last event):** simplest to
  implement and explain; overstates observation time for people with long
  gaps.
- **B. Multiple periods split at a gap of G days:** more faithful to real
  observation; depends on choosing G and on how complete the source is.
  Candidate values for G need to be compared on each site's data (for
  example, how many persons would get more than one period at G = 365,
  548 or 730).
- **C. Period defined by enrolment or registration records:** most accurate
  when such records exist, but not all sites have them.

### Trade-offs accepted

To be filled in when decided.

## Impact on sites

Each site should report, for the candidate values of G, the share of persons
that would receive more than one period, before the decision is made. This
turns the discussion from opinion into numbers.

## References

OMOP CDM v5.4, OBSERVATION_PERIOD table; Book of OHDSI chapter on ETL.

## Change log

| Date (meeting) | Change | Reason | Alternatives rejected / trade-off accepted |
|---|---|---|---|
| 2026-11-04 | Example draft | Demonstrates how an open design question is laid out | n/a |
