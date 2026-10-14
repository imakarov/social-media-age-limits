# Schema

Both tables are published as CSV (UTF-8, comma-separated, RFC 4180 quoting) and as JSON
(an array of objects with the same keys). The CSV files are the source of truth;
`scripts/build_json.py` regenerates the JSON. In JSON, an empty age is `null`; every
other field is a string.

## `data/apps.csv`: minimum ages stated by apps

One row per app and scope. A row with `scope_type = global` is the app's baseline;
other rows record an exception that the app itself publishes for a region, country
or US state.

| Column | Type | Meaning |
|---|---|---|
| `id` | string | Stable row id, `app-NNN`. |
| `app` | string | App or account system (e.g. `Google Account (used by YouTube)`). |
| `operator` | string | Company that publishes the terms. |
| `scope` | string | `global`, a region (`EEA`, `EU`), an ISO 3166-1 alpha-2 code, or an ISO 3166-2 subdivision such as `US-FL`. |
| `scope_type` | enum | `global`, `region`, `country`, `subdivision`. |
| `min_age` | integer or blank | Minimum age to use the app on one's own, as stated by the source. Blank when the source states no single age; `note` explains. |
| `rule` | string | What the source says, short quote or close paraphrase. |
| `under_min_option` | string | Official option for children below the minimum (e.g. YouTube Kids, Family Link), if the source names one. |
| `source_title` | string | Title of the source page. |
| `source_url` | https URL | The app's own terms or help page. |
| `checked_on` | date (YYYY-MM-DD) | Date the source was read. |
| `note` | string | Caveats. |

## `data/countries.csv`: laws and national rules

One row per law (or per country for the GDPR Article 8 digital consent age).

| Column | Type | Meaning |
|---|---|---|
| `id` | string | Stable row id, `law-NNN`. |
| `jurisdiction` | string | Country, or `European Union` for EU-wide rules. |
| `iso2` | string | ISO 3166-1 alpha-2 code (`EU` for the Union). |
| `subdivision` | string | ISO 3166-2 code for state laws (e.g. `US-UT`), else blank. |
| `law` | string | Official name and article. |
| `rule_type` | enum | `account_ban` (accounts below the age not allowed), `parental_consent` (allowed with a parent's consent), `data_consent` (age at which a child can consent alone to data processing), `age_assurance_duty` (platforms must check age or keep children from certain content), `design_code` (design duties for services likely used by children), `guidance` (official advice, not binding). |
| `age` | integer or blank | The age threshold: a rule applies to children *under* this age. Blank when the law has no single age; `note` explains. |
| `applies_to` | string | Which services are covered. |
| `status` | enum | `in_force`, `enacted_not_in_force`, `enjoined` (blocked by a court), `struck_down` (held unconstitutional), `proposed`, `lapsed` (bill expired without passing), `repealed`. |
| `effective_date` | date or blank | When the rule took or takes effect, if known. |
| `source_url` | URL | Official legislation portal, gazette, regulator or court page. |
| `checked_on` | date (YYYY-MM-DD) | Date the source was read. |
| `verified` | enum | `yes`: the age and status were read on the primary source. `partial`: the source is primary, but part of the row (usually court status or a date) could not be confirmed there; the note says which part. |
| `note` | string | Caveats. |

## Rules

- Only primary sources: the app's own terms and help pages; official legislation, gazettes, regulators, courts.
- No value is inferred. If it could not be confirmed, the age is blank and the note says why.
- `python3 validate.py` must pass before a change is merged.
