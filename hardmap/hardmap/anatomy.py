"""`hardmap anatomy` — dump / filter / join-key export for the Structure Atlas.

The charge atlas records what the algorithmic universe can do TO each problem; Anatomy records what each
problem IS. This command serves the second, including the passport table — because a consumer that reads a
column without reading its passport can seal a bet the column cannot carry.
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import eightfold
from eightfold import anatomy as AN


def _at() -> Path:
    return Path(eightfold.__file__).resolve().parent / "results" / "atlas"


def _rows():
    p = _at() / "anatomy_v1.jsonl"
    if not p.exists():
        print("anatomy_v1.jsonl not built (run dev/build_anatomy.py)", file=sys.stderr)
        return None
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def run(fmt: str = "jsonl", universe: str | None = None, column: str | None = None,
        passports: bool = False) -> int:
    if passports:
        p = _at() / "anatomy-passports.json"
        if not p.exists():
            print("anatomy-passports.json not built (run dev/build_passports.py)", file=sys.stderr)
            return 2
        doc = json.loads(p.read_text(encoding="utf-8"))
        if fmt == "jsonl":
            sys.stdout.write(json.dumps(doc, indent=2) + "\n")
            return 0
        w = csv.writer(sys.stdout)
        w.writerow(["column", "shipped", "universe", "invariance", "property_of",
                    "variance", "starved", "kappa", "admissible", "bets_spent"])
        for c, x in doc["columns"].items():
            ok, _ = AN.passport_admissible(c, doc)
            r = x.get("readability") or {}
            bh = x.get("bet_history") or {}
            w.writerow([c, x["shipped"], x["universe"] or "", x["invariance"], x["property_of"],
                        x["variance"].get("kind", ""), x["variance"].get("starved"),
                        r.get("kappa", ""), ok, len(bh.get("sealed_bets", []))])
        return 0

    rows = _rows()
    if rows is None:
        return 2
    if universe:
        if universe not in AN.UNIVERSES:
            print(f"unknown universe {universe!r}; expected one of {list(AN.UNIVERSES)}", file=sys.stderr)
            return 2
        rows = [r for r in rows if r["universe"] == universe]
    if column:
        if column not in AN.COLUMNS:
            print(f"unknown column {column!r}; expected one of {sorted(AN.COLUMNS)}", file=sys.stderr)
            return 2
        rows = [r for r in rows if any(c["feature"] == column for c in r["features"])]

    if fmt == "jsonl":
        for r in rows:
            sys.stdout.write(json.dumps(r, ensure_ascii=False) + "\n")
        return 0
    if fmt == "csv":
        # join-key export: one row per (row_key, column) so the atlas can be joined without unnesting
        w = csv.writer(sys.stdout)
        w.writerow(["row_key", "universe", "problem_id", "feature", "value", "provenance_status",
                    "instrument_ref", "bridge_citation", "source_artifact"])
        for r in rows:
            for c in r["features"]:
                if column and c["feature"] != column:
                    continue
                v = c["value"]
                w.writerow([r["row_key"], r["universe"], r.get("problem_id", ""), c["feature"],
                            json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v,
                            c.get("provenance_status", ""), c.get("instrument_ref", ""),
                            c.get("bridge_citation", ""), c.get("source_artifact", "")])
        return 0
    print(f"unknown format {fmt!r}", file=sys.stderr)
    return 2
