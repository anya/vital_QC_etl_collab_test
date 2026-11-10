# Governance: how rules are proposed, discussed, ratified and tracked

> Items marked **[DECIDE]** are open questions the workgroup needs to settle
> once, at the start. Defaults are suggested so the process can run meanwhile.

## 1. Roles

| Role | Responsibility |
|---|---|
| **Proposer** | Anyone in the workgroup. Opens an issue; may suggest wording. |
| **Editor** | Writes and edits pages, maintains the change log, prepares the agenda, records outcomes. A scribe, not a decider. |
| **Deputy editor** | Same permissions as the editor; covers absences. **[DECIDE: name]** |
| **Site representative** | One per site. Speaks for the site in decisions; reports implementation status. |
| **Chair** | Runs the meeting and declares the outcome. |

## 2. Where things live

| What | Where |
|---|---|
| The current rule | The rule page in `rules/` |
| Debate, questions, proposals | GitHub issues, opened through the three issue forms |
| The record of what was decided and why | The page's **change log**, plus the **outcome comment** the editor posts in the issue |
| Who has implemented what | `sites/conformance.csv` |

Meeting minutes are not kept in this repository. The change log row and the
outcome comment are the record.

Issue labels: `proposal`, `change-request`, `question`, `on-agenda`, `rejected`.

## 3. Rule statuses

| Status | Meaning | Implementers should |
|---|---|---|
| `draft` | New rule, not yet agreed | Not implement |
| `ratified` | Agreed, in force | Implement |
| `under-revision` | Ratified rule with a change being decided. **Still in force.** | Keep implementing the current text |
| `retired` | Was ratified, no longer in force | Stop; follow the replacement if any |
| `rejected` | Proposed and declined | Not implement |

```
proposal issue -> draft -> ratified <-> under-revision
                    |         |             |
                    v         v             v
                 rejected   retired <-------+
```

Who changes the status, and when:

| Change | Trigger | Done by |
|---|---|---|
| (issue) -> `draft` | The editor judges the proposal concrete enough to review as a page, or a meeting discussed it without agreeing | Editor |
| `draft` -> `ratified` | Accepted at a meeting | Editor, after the meeting |
| `draft` -> `rejected` | The group declines | Editor, after the meeting |
| `ratified` -> `under-revision` | A change request is **accepted onto the agenda** | Editor |
| `under-revision` -> `ratified` | The change is accepted (new text) or declined (old text stays) | Editor, after the meeting |
| `ratified` / `under-revision` -> `retired` | The group decides to remove the rule | Editor, after the meeting |

A question never changes the status. A change request changes it only once
the editor has accepted it for decision; this avoids the status flipping on
every comment.

## 4. Proposing a new rule

1. The proposer opens an issue with the **Propose a new rule** form
   ([HOW-TO-PROPOSE.md](HOW-TO-PROPOSE.md)). One issue = one question.
2. Discussion happens in that issue, not on a page.
3. When the proposal has concrete wording worth reviewing as a page, or after
   a meeting that discussed it without agreeing, the editor creates the page
   with `status: draft` and links the issue in the `discussion` field.
   Before that, the proposal lives only in its issue.
4. If the proposer abandons it, the editor deletes the draft page (if one
   exists) and closes the issue as "not planned".

## 5. Questions and change requests on an existing rule

Every rule page has three links at the top: **Ask a question**,
**Propose a change** and **Past discussion** (all issues that mention the
rule ID, open or closed).

- A **question** ("how do I apply this to my data?") is answered in the issue
  and closed. If the answer shows the rule is ambiguous, the editor converts
  it to a change request.
- A **change request** follows the same path as a proposal: discussion,
  agenda, decision. While the group decides, the rule stays in force and the
  page shows the current text. The proposed new wording lives in the issue,
  never in the page.

## 6. Getting on the agenda

- An item can be put to a decision only if it was announced **at least 7 days**
  before the meeting, with its page (if any) and issue linked. **[DECIDE: 7 days?]**
- The editor labels the issue `on-agenda` and, for a change request, sets the
  page to `under-revision` (editor's checklist below).
- Aim for 3 to 5 items per meeting so each gets real discussion. **[DECIDE]**

## 7. Ratification

- **Quorum** (suggested): at least 3 of the 4 sites represented, including
  the rule's main affected sites. **[DECIDE]**
- **Decision rule** (suggested): consensus, with each site holding one
  voice. If consensus fails, a vote with a majority of the sites present, and
  the dissent recorded in the change log. **[DECIDE]**
- **Absent sites** may comment in the issue beforehand, or object within
  3 working days of the outcome comment being posted. An objection reopens the
  item at the next meeting. **[DECIDE]**
- Possible outcomes: **accepted**, **accepted with changes** (the agreed
  changes are stated in the outcome comment, and the editor applies them),
  **deferred** (with a stated reason and what is needed), **rejected**.

## 8. After the meeting (editor's checklist)

For every item, post a short **outcome comment** in the issue: the decision,
and any agreed wording changes. Two lines are enough. Then:

| Outcome | Page edits | Other |
|---|---|---|
| **New rule accepted** | `status: ratified`, `ratified_on`, status line, first change log row (original choice, alternatives, trade-offs, dissent) | Add the rule's rows to `sites/conformance.csv` as `not-started`; close the issue |
| **New rule accepted with changes** | Apply the changes first, then as above | |
| **New rule not agreed / deferred** | Keep `draft`; update wording if the meeting agreed any | Leave the issue open and say what is needed |
| **New rule rejected** | If a draft page exists: `status: rejected`, change log row with the reason. If only an issue exists: no page | Close the issue with the label `rejected` |
| **Change accepted** | New text; `status: ratified`; new `ratified_on`; remove `revision_issue` and the "under revision" line; change log row | If ETL output changes, set affected sites' rows to `not-started`; check `depends_on` / `affects`; close the issue |
| **Change declined** | `status: ratified`; remove `revision_issue` and the "under revision" line; change log row only if the decision is worth recording | Close the issue with the reason |
| **Rule retired** | `status: retired`; `superseded_by` if another rule replaces it; change log row with the reason | Set the rule's conformance rows to `not-applicable`; fix pages that depend on it (the script warns); close the issue |

Finally, run the catalog script (or confirm it ran) and fix any errors.

## 9. Site deviations

A site that cannot implement a ratified rule (for example, the source data
does not contain the needed field) records a deviation in
`sites/conformance.csv` with status `deviation` and a reason, and tells the
workgroup. Deviations are reviewed at the next meeting. Silent divergence is
the failure this process is meant to prevent.

## 10. Releases

Periodically (suggested: after any meeting that ratifies rules, or at least
quarterly) the editor tags the repository as `ruleset-vMAJOR.MINOR`
(for example `ruleset-v0.3`). Sites cite the release they implement.
Breaking changes (a ratified rule changes in a way that alters ETL output)
increment MAJOR; additions and clarifications increment MINOR.
**[DECIDE]**

## 11. Urgent changes

If a rule is found to be wrong in a way that corrupts data, the chair may
approve an interim fix by email to all site representatives, with
ratification at the next meeting. The change log notes "interim".
**[DECIDE: allow this?]**

## 12. Relationship to existing standards

Rules here must not contradict the OMOP CDM specification. If a rule
restates an OHDSI Themis convention, link to it rather than copying. Rules
that go beyond or tighten those conventions are the ones that need
ratification here.
