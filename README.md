# Social media age limits by app and country

An open dataset of:

- **apps**: the minimum age each major social media, messaging and gaming app states in its own terms or help pages, including the country and regional exceptions it publishes (58 rows, 16 apps and account systems);
- **countries**: laws and official rules that set an age for children online: US COPPA, the GDPR Article 8 digital consent age in each EU/EEA country and the UK, the UK Online Safety Act and Children's code, Australia's under-16 social media minimum age, and other national and US state rules (74 rows).

Every row has a `source_url` pointing to a primary source (the app's own page, an official legislation portal, a gazette, a regulator or a court) and a `checked_on` date. Where a source does not state an age, or a value could not be confirmed there, the field is blank and the note says why. Nothing is filled in from memory or from secondary reporting.

Browse and filter the tables: **https://imakarov.github.io/social-media-age-limits/**

For a plain-language guide to what these ages mean for parents, see [Social Media Age Limits: The Main Apps, Laws and Countries](https://teachkidshabits.com/blog/social-media-age-limits.html) on Teach Kids Habits.

## Files

| File | Contents |
|---|---|
| `data/apps.csv`, `data/apps.json` | Minimum ages stated by apps |
| `data/countries.csv`, `data/countries.json` | Laws and national rules |
| `SCHEMA.md` | Column definitions and allowed values |
| `validate.py` | Checks columns, ages, dates, URLs and that JSON matches CSV |
| `scripts/build_json.py` | Regenerates the JSON files from the CSV files |
| `index.html` | The searchable table published on GitHub Pages |

The CSV files are the source of truth. The JSON files are generated from them.

## How to use

Python:

```python
import csv
with open("data/apps.csv", newline="", encoding="utf-8") as f:
    apps = list(csv.DictReader(f))
print([r for r in apps if r["app"] == "TikTok"])
```

JavaScript:

```js
const laws = await fetch("https://imakarov.github.io/social-media-age-limits/data/countries.json").then(r => r.json());
const bans = laws.filter(r => r.rule_type === "account_ban" && r.status === "in_force");
```

Things to keep in mind when reading the data:

- **An app's age and a law's age are different things.** The app row is what the company says in its terms. The law row is what a country requires. Where they differ, the stricter one applies to the user.
- **`data_consent` is not a ban.** COPPA and GDPR Article 8 are about consent to data processing. Below that age a parent has to consent; the child is not barred from the service by that rule alone.
- **`age` means "applies to children under this age".** For example, Australia's row has `age = 16`: under-16s may not hold accounts on age-restricted platforms.
- **`verified = partial`** (countries table) means the source is primary but part of the row, usually a court status or a date, could not be confirmed on it. The note says which part.

## Method

1. Each app's current terms of service and help pages were read on the check date. Where an app publishes a different version by country (for example YouTube's EEA terms, or Google's per-country account ages), each version is a separate row.
2. For laws, the text was read on the official legislation portal or gazette, or on the regulator's page. News articles and law-firm summaries were used only to find the primary source, never as the source.
3. If a value could not be confirmed on the primary source, it was left blank and explained in `note`.
4. `python3 validate.py` checks every release; `python3 validate.py --online` also requests every source URL (some government sites block scripts, so a warning there needs a manual check in a browser).

This is a reference, not legal advice. Terms and laws change often, so check the linked source before relying on a value.

## Contributing

Corrections are welcome. Please open an issue or pull request with the primary source URL for the change. Update `checked_on`, run `python3 scripts/build_json.py` and `python3 validate.py`, and add a line to the changelog below.

## License

- Data (`data/`): [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). See `LICENSE-DATA`.
- Scripts and page (`validate.py`, `scripts/`, `index.html`): MIT. See `LICENSE`.

Short excerpts of terms and statutes are quoted only so that each value can be checked against its source.

## Citation

```
Teach Kids Habits, social-media-age-limits dataset, 2026.
https://github.com/imakarov/social-media-age-limits (CC BY 4.0)
```

BibTeX:

```bibtex
@misc{teachkidshabits_social_media_age_limits_2026,
  author       = {{Teach Kids Habits}},
  title        = {social-media-age-limits dataset},
  year         = {2026},
  howpublished = {\url{https://github.com/imakarov/social-media-age-limits}},
  note         = {Version 1.0.0, checked 2026-10-14. CC BY 4.0}
}
```

GitHub also reads `CITATION.cff` and shows a "Cite this repository" button.

## Changelog

### 1.0.0 (2026-10-14)

- First release: 58 app rows and 74 law rows, all checked on 2026-10-14.
- Notable findings at release: Denmark's digital consent age is 15 (since 1 Jan 2024, previously 13); Telegram's terms set 18 for EU users; YouTube's EEA terms state 16 even where the Google Account age is lower; TikTok's US terms set 14 in Florida; France's 2023 under-15 parental-consent law was never applied, and the 2026 under-15 ban was struck down by the Conseil constitutionnel; Malaysia requires age checks and bars accounts for those 15 and under from 1 June 2026.
