#!/usr/bin/env python3
"""Validate the dataset.

Checks: exact column sets, unique ids, required fields, ages are whole numbers
in a sane range (or blank with a note), checked_on is an ISO date not in the
future, source_url is an absolute URL (https preferred), enumerated fields use allowed
values, and data/*.json matches data/*.csv.

Usage:
    python3 validate.py            # offline checks
    python3 validate.py --online   # also request every source_url
"""
import csv, datetime, json, pathlib, sys, urllib.parse, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent

SCHEMA = {
    "apps": {
        "columns": ["id", "app", "operator", "scope", "scope_type", "min_age", "rule",
                    "under_min_option", "source_title", "source_url", "checked_on", "note"],
        "required": ["id", "app", "operator", "scope", "scope_type", "rule",
                     "source_title", "source_url", "checked_on"],
        "age": "min_age",
        "enums": {"scope_type": {"global", "region", "country", "subdivision"}},
    },
    "countries": {
        "columns": ["id", "jurisdiction", "iso2", "subdivision", "law", "rule_type", "age",
                    "applies_to", "status", "effective_date", "source_url", "checked_on", "verified", "note"],
        "required": ["id", "jurisdiction", "law", "rule_type", "applies_to", "status",
                     "source_url", "checked_on", "verified"],
        "age": "age",
        "enums": {
            "rule_type": {"account_ban", "parental_consent", "data_consent",
                          "age_assurance_duty", "design_code", "guidance"},
            "status": {"in_force", "enacted_not_in_force", "enjoined", "struck_down",
                       "proposed", "lapsed", "repealed"},
            "verified": {"yes", "partial"},
        },
    },
}


def check_url(u):
    p = urllib.parse.urlparse(u)
    return p.scheme in ("https", "http") and bool(p.netloc) and " " not in u


def online(u):
    req = urllib.request.Request(u, method="GET", headers={
        "User-Agent": "Mozilla/5.0 (dataset link checker; +https://github.com/imakarov/social-media-age-limits)"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception as e:  # network error
        return str(e)


def main():
    errors, warnings, urls = [], [], set()
    today = datetime.date.today()
    for name, spec in SCHEMA.items():
        path = ROOT / "data" / f"{name}.csv"
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if reader.fieldnames != spec["columns"]:
                errors.append(f"{name}.csv: columns {reader.fieldnames} != {spec['columns']}")
                continue
            rows = list(reader)
        ids = set()
        for n, row in enumerate(rows, start=2):
            where = f"{name}.csv line {n} ({row.get('id')})"
            if row["id"] in ids:
                errors.append(f"{where}: duplicate id")
            ids.add(row["id"])
            for k in spec["required"]:
                if not row[k].strip():
                    errors.append(f"{where}: empty required field {k}")
            age = row[spec["age"]]
            if age == "":
                if not row["note"].strip():
                    errors.append(f"{where}: blank {spec['age']} needs a note explaining why")
            elif not age.isdigit() or not 0 < int(age) <= 21:
                errors.append(f"{where}: {spec['age']} must be a whole number 1-21, got {age!r}")
            for k, allowed in spec["enums"].items():
                if row[k] not in allowed:
                    errors.append(f"{where}: {k}={row[k]!r} not in {sorted(allowed)}")
            for k in ("checked_on", "effective_date"):
                if k in row and row[k]:
                    try:
                        d = datetime.date.fromisoformat(row[k])
                        if k == "checked_on" and d > today:
                            errors.append(f"{where}: checked_on {d} is in the future")
                    except ValueError:
                        errors.append(f"{where}: {k} is not YYYY-MM-DD: {row[k]!r}")
            if not check_url(row["source_url"]):
                errors.append(f"{where}: source_url is not an absolute URL: {row['source_url']!r}")
            elif row["source_url"].startswith("http://"):
                warnings.append(f"{where}: source_url uses http (site has no https version)")
            urls.add(row["source_url"])
        jpath = ROOT / "data" / f"{name}.json"
        data = json.loads(jpath.read_text(encoding="utf-8"))
        expected = [{k: (int(v) if k == spec["age"] and v != "" else (None if k == spec["age"] else v))
                     for k, v in r.items()} for r in rows]
        if data != expected:
            errors.append(f"{name}.json does not match {name}.csv (run scripts/build_json.py)")
        print(f"{name}: {len(rows)} rows")

    if "--online" in sys.argv:
        for u in sorted(urls):
            s = online(u)
            ok = isinstance(s, int) and s < 400
            print(f"  {'ok  ' if ok else 'WARN'} {s} {u}")
            if not ok:
                warnings.append(f"{u} -> {s} (some sites block scripts; check in a browser)")

    for w in warnings:
        print("warning:", w)
    for e in errors:
        print("error:", e)
    print("OK" if not errors else f"{len(errors)} error(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
