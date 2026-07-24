#!/usr/bin/env python3
"""H4 check 3 -- sealed oracle spot-check draw (setup for the manual pass).

Draws, with a SEALED seed, ~10 cited-filled classes per charge column from the frozen
atlas and writes a worksheet. The condition on each drawn class must then be re-derived
BY HAND against the cited theorem -- the one H4 check that needs human judgment, not code.
Sealing the seed here fixes the sample before the manual audit begins.

Run: python scripts/oracle_spotcheck_draw.py  ->  docs/findings/H4-oracle-spotcheck-worksheet.md
"""
from __future__ import annotations

import random
from pathlib import Path

from eightfold.atlas import get_charge, load_atlas
from eightfold import charges as C

SEED = 20260724          # sealed before drawing
PER_CHARGE = 10
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "findings" / "H4-oracle-spotcheck-worksheet.md"


def main() -> int:
    rng = random.Random(SEED)
    entries = load_atlas()
    lines = [
        "# H4 oracle spot-check -- worksheet (sealed draw)",
        "",
        f"Sealed seed **{SEED}**, {PER_CHARGE} cited-filled classes per charge column, drawn from the frozen "
        f"atlas ({len(entries)} problems). For each row, re-derive the charge value BY HAND from the cited "
        "theorem and mark it. Cosmetic / material / invalidating per the H4 triage rule.",
        "",
        "| charge | problem_id | value | citation | hand-verified? |",
        "|---|---|---|---|---|",
    ]
    for charge in C.EIGHTFOLD_SPEC.charges:
        pool = []
        for e in entries:
            cell = get_charge(e, charge)
            if cell and cell.value not in (None, "n.a.") and getattr(cell, "status", "") in ("claimed", "measured"):
                cite = (cell.provenance or {}).get("citation", "") if isinstance(getattr(cell, "provenance", None), dict) else ""
                pool.append((e.problem_id, cell.value, cite))
        drawn = rng.sample(pool, min(PER_CHARGE, len(pool)))
        for pid, val, cite in drawn:
            cite = (cite or "").replace("|", "/")[:70]
            lines.append(f"| {charge} | {pid} | {val} | {cite} | |")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({sum(1 for line in lines if line.startswith('| ') and 'problem_id' not in line) - 1} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
