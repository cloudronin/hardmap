#!/usr/bin/env python3
"""Mosaic v3 G1 — the sealed FOLD PARTITION and the BOUNDARY-DISTANCE stratification variable.

FOLD KEY = the 46 poly-fingerprint groups. The warrant, recorded because it reads as a contradiction:
using flag-groups as the FOLD KEY while excluding flags as FEATURES is legal and correct — the key only
prevents identical-profile near-duplicates from straddling train/test, which makes the test STRICTLY
HARDER, NEVER EASIER. Nothing about the key enters the fit. (prereg_v12 fold_key.)

BOUNDARY DISTANCE = minimum tuple-edits (add or remove one tuple) to flip the bounded-width predicate.
It is FLAG-DERIVED, so prereg_v12 bars it as a FEATURE and permits it as a STRATIFICATION variable:
reporting accuracy BY boundary distance leaks nothing into the fit. Census-before-seal applies.
"""
import json, sys, hashlib
from collections import Counter
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from foundry import postlattice as PL, prism            # noqa: E402
LAT = ROOT / "foundry" / "results" / "lattice"
OUT = LAT / "grid_folds_and_strata.json"
MAX_D = 2

def bw(rels):
    return prism.bounded_width(prism._flags(rels)) == "bounded-width"

def boundary_distance(arity, rel):
    """min tuple-edits to flip bounded-width; capped at MAX_D, else >MAX_D."""
    base = [tuple(int(b) for b in t) for t in rel]
    cur = bw([frozenset(base)])
    universe = [tuple((i >> (arity - 1 - j)) & 1 for j in range(arity)) for i in range(2 ** arity)]
    s = set(base)
    # distance 1
    for t in universe:
        cand = (s - {t}) if t in s else (s | {t})
        if not cand:
            continue
        if bw([frozenset(cand)]) != cur:
            return 1
    if MAX_D < 2:
        return f">{MAX_D}"
    # distance 2
    for i, t1 in enumerate(universe):
        s1 = (s - {t1}) if t1 in s else (s | {t1})
        for t2 in universe[i + 1:]:
            cand = (s1 - {t2}) if t2 in s1 else (s1 | {t2})
            if not cand:
                continue
            if bw([frozenset(cand)]) != cur:
                return 2
    return f">{MAX_D}"

def main():
    ct = json.loads((LAT / "prism_v2_charges.json").read_text())["charge_table"]
    FLAGS = ("0valid","1valid","horn","dualhorn","bijunctive","affine",
             "width2affine","strongly0valid","IHSB","general_wsep")
    rows = []
    for r in ct:
        fp = "".join("1" if r["flags"][k] else "0" for k in FLAGS)
        rows.append({"row_key": f"b{r['arity']}:{_bm(r['arity'], r['relation'])}",
                     "arity": r["arity"], "fold_key": fp,
                     "boundary_distance": boundary_distance(r["arity"], r["relation"])})
    folds = Counter(r["fold_key"] for r in rows)
    bd = Counter(str(r["boundary_distance"]) for r in rows)
    top, topn = bd.most_common(1)[0]
    doc = {"schema": "grid-folds-strata/v1",
           "fold_key": {"name": "poly_fingerprint (10-flag bitstring)", "n_groups": len(folds),
                        "warrant": ("the key only prevents identical-profile near-duplicates from straddling "
                                    "train/test, which makes the test STRICTLY HARDER, never easier; nothing "
                                    "about the key enters the fit"),
                        "sizes_top10": folds.most_common(10),
                        "n_singleton_groups": sum(1 for v in folds.values() if v == 1)},
           "boundary_distance": {"role": "STRATIFICATION ONLY — flag-derived, barred as a feature",
                                 "cap": MAX_D, "marginal": dict(bd.most_common()),
                                 "modal_share": round(topn / len(rows), 4),
                                 "starved": bool(topn / len(rows) > 0.90),
                                 "note": ("a model accurate in the interiors and coin-flip at the line has "
                                          "learned geography, not the border")},
           "rows": rows}
    OUT.write_text(json.dumps(doc, indent=1) + "\n")
    print(f"wrote {OUT.name} sha {hashlib.sha256(OUT.read_bytes()).hexdigest()[:16]}")
    print(f"fold groups: {len(folds)}  singletons: {doc['fold_key']['n_singleton_groups']}  "
          f"largest: {folds.most_common(3)}")
    print(f"boundary distance marginal: {dict(bd.most_common())}  modal {topn/len(rows):.0%} -> "
          f"{'STARVED' if doc['boundary_distance']['starved'] else 'ok'}")
    return 0

def _bm(a, rel):
    m = 0
    for t in rel:
        i = 0
        for b in t: i = (i << 1) | int(b)
        m |= (1 << i)
    return f"{m:0{max(1,(2**a+3)//4)}x}"

if __name__ == "__main__":
    sys.exit(main())
