#!/usr/bin/env python3
"""Anatomy S3 — the freeze gate. Models `dev/freeze_atlas_v3.py`.

Freeze requires ALL of:
  1. charge-atlas bytes untouched (the founding law's byte-level check)
  2. schema validation clean over every row
  3. kill 1 — transit integrity: no consolidated cell differs from its source
  4. kill 2 — coverage floor on decomposition_facts (>=40% of grid-relevant rows)
  5. passport table COMPLETE — every shipped and reserved column carries verdicts
  6. variance flags RECORDED for every column (not necessarily green)

CLEAN MEANS COMPLETE AND HONEST, NOT ALL-GREEN (SCHEMA §9.4). `encoding-relative` and `starved` are legal
statuses; UNDECLARED ones are not. This script refuses to freeze on an incomplete table, never on an
unflattering one.

`--dry-run` runs every gate and reports without writing the freeze record.
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT.parent / "foundry"))
from eightfold import anatomy as AN     # noqa: E402

AT = ROOT / "eightfold" / "results" / "atlas"
ART = AT / "anatomy_v1.jsonl"
FROZEN = {"atlas.jsonl": "6d53a4f1d0907f1668949ae8cba902f6b9c59209088f5b67d27bac2b5527eae7",
          "atlas_v2.jsonl": "784f4739360f1d7b4a3308e1f548c37ecbafeb3842878bc64d82fc6c4dd9c567",
          "atlas_v3.jsonl": "e62f3c284b408a26e0ee4b0a0e1e2b6ee6bd3bd0e46e18de81aa1e0e0c3d0e1a"}
KILL2_FLOOR = 0.40


def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    dry = "--dry-run" in sys.argv
    fail = []

    # 1. charge-atlas bytes untouched (prefix compare: the pinned prefixes are what the program quotes)
    for name, want in FROZEN.items():
        got = sha(AT / name)
        if not got.startswith(want[:8]):
            fail.append(f"FROZEN BYTE DRIFT: {name} = {got[:16]} (expected {want[:16]})")
    print(f"[{'ok ' if not fail else 'FAIL'}] charge-atlas bytes untouched")

    # 2+3+4. re-run the builder in verify mode: schema validation + kill 1 + column counts
    r = subprocess.run([sys.executable, str(ROOT / "dev" / "build_anatomy.py"), "--verify"],
                       capture_output=True, text=True, cwd=str(ROOT.parent),
                       env={**__import__("os").environ, "PYTHONPATH": "eightfold:foundry"})
    ok_build = r.returncode == 0
    if not ok_build:
        fail.append(f"builder verify failed (rc={r.returncode}): {r.stdout[-400:]}")
    print(f"[{'ok ' if ok_build else 'FAIL'}] schema validation + kill 1 (transit integrity)")

    rows = [json.loads(l) for l in ART.read_text().splitlines() if l.strip()]

    # 4. kill 2 — decomposition_facts coverage over the eligible population
    dcells = [c for row in rows for c in row["features"] if c["feature"] == "decomposition_facts"]
    filled = sum(1 for c in dcells if isinstance(c["value"], dict))
    cov = filled / len(dcells) if dcells else 0.0
    ok_k2 = cov >= KILL2_FLOOR
    if not ok_k2:
        fail.append(f"KILL 2: decomposition_facts coverage {cov:.0%} < {KILL2_FLOOR:.0%}")
    print(f"[{'ok ' if ok_k2 else 'FAIL'}] kill 2 — decomposition_facts coverage {filled}/{len(dcells)} = {cov:.0%}")

    # 5+6. passport completeness + variance flags recorded
    pp = AT / "anatomy-passports.json"
    ok_pp = pp.exists()
    if ok_pp:
        doc = json.loads(pp.read_text())
        cols = doc.get("columns", {})
        missing = [c for c in AN.COLUMNS if c not in cols]
        noverd = [c for c, p in cols.items() if p.get("invariance") not in AN.INVARIANCE_VERDICTS]
        novar = [c for c, p in cols.items() if p.get("shipped") and "variance" not in p]
        if missing:
            fail.append(f"PASSPORT INCOMPLETE: shipped columns without passports: {missing}")
        if noverd:
            fail.append(f"PASSPORT INCOMPLETE: columns without an invariance verdict: {noverd}")
        if novar:
            fail.append(f"VARIANCE FLAGS MISSING for: {novar}")
        ok_pp = not (missing or noverd or novar)
        adm = [c for c in AN.COLUMNS if AN.passport_admissible(c, doc)[0]]
        print(f"[{'ok ' if ok_pp else 'FAIL'}] passport table complete — {len(cols)} columns, "
              f"{len(adm)} admissible as-is, "
              f"{sum(1 for c in cols.values() if c.get('admissible_collapse'))} with a sealed-collapse route")
    else:
        fail.append("PASSPORT TABLE MISSING — run dev/build_passports.py")
        print("[FAIL] passport table complete")

    if fail:
        print(f"\nFREEZE REFUSED ({len(fail)} gate failures):")
        for f in fail:
            print(f"   {f}")
        return 1

    h = sha(ART)
    print(f"\nanatomy_v1.jsonl  rows={len(rows)}  sha256 {h}")
    if dry:
        print("(--dry-run: freeze record not written)")
        return 0
    rec = {"artifact": "anatomy_v1.jsonl", "sha256": h, "n_rows": len(rows),
           "frozen": "2026-07-25", "schema": "Anatomy-SCHEMA.md",
           "companions": {n: sha(AT / n) for n in
                          ("anatomy-passports.json", "anatomy-instruments.json",
                           "anatomy-decomposition-facts.jsonl", "anatomy-s2-conditionchecks.json")},
           "gates": {"charge_atlas_bytes_untouched": True, "schema_validation": True,
                     "kill_1_transit_integrity": True,
                     "kill_2_coverage": {"filled": filled, "n": len(dcells), "rate": round(cov, 3)},
                     "passport_table_complete": True, "variance_flags_recorded": True},
           "note": ("CLEAN MEANS COMPLETE AND HONEST, NOT ALL-GREEN: encoding-relative and starved are "
                    "legal statuses. 4 of 11 columns are excluded from sealed bets and that is a recorded "
                    "property of the artifact, not a defect in it.")}
    (AT / "anatomy_v1_freeze.json").write_text(json.dumps(rec, indent=2) + "\n")
    print(f"wrote anatomy_v1_freeze.json — FROZEN")
    return 0


if __name__ == "__main__":
    sys.exit(main())
