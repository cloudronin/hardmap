"""Lattice v1 (prereg_v29) — occupancy of the SEALED roster: the distinct single relations in the Boolean
co-clone plain bases + the finer tier, each paired with {Min-Ones, Max-Ones}. Verdict declared on COMPOSITION
(profile count vs the pre-registered floor) BEFORE the association is read (ruling 4). $0, deterministic.

Run: PYTHONPATH=... python foundry/dev/lattice_v1.py
"""
import json

from eightfold import structure as S
from foundry import finer, objective_oracles as OO, postlattice as PL

FLOOR_PROFILES, FLOOR_ROWS = 6, 15


def distinct_relations():
    """The distinct single relations across BOOLEAN_COCLONES bases + finer-tier bases (deduped by frozenset)."""
    seen, out = set(), []
    def add(rel, name):
        if rel not in seen:
            seen.add(rel); out.append((name, rel))
    named = {PL.R_XOR3: "XOR3(x+y+z=0)", PL.R_XOR2: "XOR2(x!=y)", PL.R_NOR3: "NOR3(Horn)", PL.R_TRUE: "TRUE(x=1)",
             PL.R_OR3: "OR3(dualHorn)", PL.R_FALSE: "FALSE(x=0)", PL.R_POS2: "OR2(VC)", PL.R_NEG2: "NAND(IS)",
             PL.R_NAE3: "NAE3", PL.R_1IN3: "1in3", finer.R_XOR3_1: "XOR3_1(x+y+z=1)"}
    for cc in PL.BOOLEAN_COCLONES:
        for r in cc.relations:
            add(r, named.get(r, "?"))
    for _cid, _n, _e, rels in finer._CANDIDATES:
        for r in rels:
            add(r, named.get(r, "?"))
    return out


def main():
    rels = distinct_relations()
    rows = []
    for name, R in rels:
        for obj in (OO.MAX_ONES, OO.MIN_ONES):
            apx, par = OO.charges([R], obj)
            rows.append({"relation": name, "objective": obj, "approximation": apx, "parameterized": par})

    both_real = [r for r in rows if r["parameterized"] != "open"]
    profiles = sorted({(r["approximation"], r["parameterized"]) for r in both_real})
    n_rel, n_rows, n_both, n_prof = len(rels), len(rows), len(both_real), len(profiles)

    # secondary association — the canon's statistic (structure.cramers_v on the both-real label lists)
    xs = [r["approximation"] for r in both_real]
    ys = [r["parameterized"] for r in both_real]
    v = S.cramers_v(xs, ys)

    # occupancy grid
    from collections import Counter
    grid = Counter((r["approximation"], r["parameterized"]) for r in both_real)

    verdict = ("INSUFFICIENT RESOLUTION" if (n_prof < FLOOR_PROFILES or n_both < FLOOR_ROWS)
               else "RESOLVED — association readable")
    out = {"prereg": "v29", "roster": "co-clone representatives + finer tier (SEALED)",
           "n_distinct_relations": n_rel, "n_rows": n_rows, "n_both_real": n_both,
           "n_distinct_profiles": n_prof, "floor_profiles": FLOOR_PROFILES, "floor_rows": FLOOR_ROWS,
           "verdict_on_composition": verdict,
           "occupancy": {f"{a} x {p}": c for (a, p), c in sorted(grid.items())},
           "secondary_cramers_v": v,
           "empty_strata_note": "3 KSTW approx strata carry NO row from these representatives; see findings.",
           "feasibility_hard_rows": [r["relation"] for r in rows if r["approximation"] == "feasibility-hard"]}

    print(f"distinct relations={n_rel}  rows={n_rows}  both-real={n_both}  profiles={n_prof} (floor {FLOOR_PROFILES})")
    print(f"VERDICT ON COMPOSITION: {verdict}")
    print(f"secondary Cramer's V (resolution-limited) = {v}")
    print("occupancy:")
    for (a, p), c in sorted(grid.items()):
        print(f"  {a:28s} x {p:5s} : {c}")
    json.dump(out, open("foundry/foundry/results/lattice/lattice_v1_occupancy.json", "w"), indent=2)
    print("\nwrote lattice_v1_occupancy.json")


if __name__ == "__main__":
    main()
