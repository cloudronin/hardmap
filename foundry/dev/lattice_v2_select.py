"""Lattice v2 (prereg_v30) — the SEALED, correlation-blind selection. Enumerate every non-empty, non-full
Boolean relation of arity <= 3 in canonical order (arity asc, then tuple-set bitmask asc); for each KSTW
approximation stratum x objective, pick the canonical-FIRST relation hitting it. Uses ONLY the approximation
charge. Writes the roster WITHOUT the parameterized charge — committed BEFORE lattice_v2_analyze.py runs, so
the roster's commit hash provably predates the joint computation (hash-checkable, prereg_v30).

Run: PYTHONPATH=... python foundry/dev/lattice_v2_select.py
"""
import json
from itertools import product

from foundry import objective_oracles as OO

STRATA = ("PO", "APX-complete", "poly-APX-complete", "Nearest-Codeword-complete",
          "Min-Horn-Deletion-complete", "decidable-not-approximable", "feasibility-hard")
KNOWN = {  # human names for recognisable relations (annotation only; not used in selection)
    frozenset({(0, 1), (1, 0), (1, 1)}): "OR2(x∨y)", frozenset({(0, 0), (0, 1), (1, 0)}): "NAND(¬x∨¬y)",
    frozenset({(0, 1), (1, 0)}): "x≠y", frozenset({(0, 0), (1, 1)}): "x=y",
    frozenset({(0, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 0)}): "XOR3(=0)",
    frozenset({(0, 0, 1), (0, 1, 0), (1, 0, 0), (1, 1, 1)}): "XOR3(=1)",
}


def canonical_relations(max_arity=3):
    """Non-empty, non-full Boolean relations arity 1..max_arity, canonical order (arity asc, bitmask asc)."""
    for a in range(1, max_arity + 1):
        universe = list(product((0, 1), repeat=a))     # ordered (0..0),(0..1),...,(1..1)
        m = 2 ** a
        for mask in range(1, 2 ** m - 1):              # exclude empty (0) and full (2^m - 1)
            yield a, mask, frozenset(universe[i] for i in range(m) if (mask >> i) & 1)


def main():
    selected = {}   # (stratum, objective) -> row dict
    for a, mask, rel in canonical_relations(3):
        for obj in (OO.MAX_ONES, OO.MIN_ONES):
            s = OO.approximation([rel], obj)
            key = (s, obj)
            if key not in selected:
                selected[key] = {"stratum": s, "objective": obj, "arity": a, "bitmask": mask,
                                 "relation": [list(t) for t in sorted(rel)],   # sort tuples lex; do NOT sort within
                                 "name": KNOWN.get(rel, f"rel_a{a}_m{mask}")}

    rows = [selected[(s, o)] for s in STRATA for o in (OO.MAX_ONES, OO.MIN_ONES) if (s, o) in selected]
    empty_cells = [f"{s} x {o}" for s in STRATA for o in (OO.MAX_ONES, OO.MIN_ONES) if (s, o) not in selected]

    out = {"prereg": "v30", "selection": "canonical-first per (KSTW approx stratum x objective); approximation-ONLY",
           "arity_bound": 3, "n_rows": len(rows), "n_empty_cells": len(empty_cells),
           "empty_cells_at_arity3": empty_cells, "rows": rows,
           "NOTE": "parameterized charge and joint occupancy are NOT here — computed by lattice_v2_analyze.py in a LATER commit."}

    print(f"selected rows={len(rows)}  empty (stratum x objective) cells at arity<=3: {len(empty_cells)}")
    for r in rows:
        print(f"  {r['objective']:9s} {r['stratum']:28s} <- {r['name']:14s} (arity {r['arity']}, mask {r['bitmask']})")
    if empty_cells:
        print("  EMPTY:", ", ".join(empty_cells))
    json.dump(out, open("foundry/foundry/results/lattice/lattice_v2_roster.json", "w"), indent=2)
    print("\nwrote lattice_v2_roster.json (roster fixed; parameterized charge NOT computed here)")


if __name__ == "__main__":
    main()
