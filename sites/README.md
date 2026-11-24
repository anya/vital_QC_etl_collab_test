# Site conformance

`conformance.csv` has one row per rule per site/province. It is the answer to "are we
actually harmonized?". Each site representative updates their own rows (can be done directly in the browser editor). 
The CSV format is used so changes show clearly in the History view; 

Rows are added when a rule is ratified (status `not-started` for each site).
When a rule is retired, its rows become `not-applicable`.

Columns:

| Column | Values |
|---|---|
| `rule_id` | A rule ID such as `PERSON-01` |
| `site` | (Need a complete list of participating teams: sites or provinces) |
| `status` | `not-started`, `in-progress`, `implemented`, `deviation`, `not-applicable` |
| `deviation_reason` | Required when status is `deviation` |
| `ruleset_version` | The release tag the site implements, e.g. `ruleset-v0.1` |
| `last_updated` | YYYY-MM-DD |

The catalog script checks that every `rule_id` exists and every status is
valid. A `deviation` without a reason is reported as an error, and a retired
rule whose rows are not `not-applicable` is reported as a warning.
