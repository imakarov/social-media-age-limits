#!/usr/bin/env python3
"""Regenerate data/*.json from data/*.csv (the CSV files are the source of truth)."""
import csv, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
INT_FIELDS = {"apps": ["min_age"], "countries": ["age"]}


def convert(name):
    with open(ROOT / "data" / f"{name}.csv", newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        for k in INT_FIELDS[name]:
            row[k] = int(row[k]) if row[k] != "" else None
    out = ROOT / "data" / f"{name}.json"
    out.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{out.relative_to(ROOT)}: {len(rows)} rows")


if __name__ == "__main__":
    for n in INT_FIELDS:
        convert(n)
