#!/usr/bin/env python3
"""Mosaic v3 G1 — SURFACE-COMBINATORIAL features for Arm A, with the algebra excluded by sealed rule.

THE QUESTION ARM A POSES: is the algebraic classification recoverable from RAW COMBINATORICS? So every
feature here is a property of the relation AS A SET OF TUPLES. The 10 Post's-lattice flags and everything
derived from them (engine_type, localization) are EXCLUDED — prereg_v12 A1.

THE LEAK THAT HAD TO BE DESIGNED AROUND, stated because it is not obvious:
  `0valid` and `1valid` ARE two of the ten flags, and they are ALSO trivially readable off a Hamming-weight
  histogram (the weight-0 and weight-arity bins). A naive "surface" weight histogram therefore hands back
  2 of the 10 flags for free and quietly breaks the exclusion.
  RESOLUTION (sealed here, before any fit): the STRICT feature set OMITS the weight-0 and weight-arity bins.
  A `relaxed` set including them is ALSO computed and stored, so the cost of the exclusion is measurable
  rather than assumed — but ONLY the strict set is scored. Reported either way.

Also excluded, per the Anatomy passport: `class_size` is admissible "as a weight, never as a feature"
(SCHEMA §9.2, encoding-relative — an orbit size AT THE DECLARED ARITY).

Every feature emitted here is a NEW DERIVED QUANTITY and gets census-before-seal (marginals + a starvation
verdict) before it may enter a fit.
"""
import hashlib
import json
import sys
from collections import Counter
from itertools import permutations
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

LAT = ROOT / "foundry" / "results" / "lattice"
OUT = LAT / "grid_surface_features.json"

# the ten flags, named here ONLY so the exclusion is explicit and testable
EXCLUDED_ALGEBRA = ("0valid", "1valid", "horn", "dualhorn", "bijunctive", "affine",
                    "width2affine", "strongly0valid", "IHSB", "general_wsep")
EXCLUDED_DERIVED = ("engine_type", "localization", "class_size")


def surface_features(arity, rel):
    """Every value here is a property of the tuple-set. Nothing consults a polymorphism."""
    tuples = [tuple(int(b) for b in t) for t in rel]
    n = len(tuples)
    total = 2 ** arity
    weights = [sum(t) for t in tuples]
    wc = Counter(weights)

    # weight histogram, STRICT: bins 0 and `arity` omitted (they are 0valid / 1valid)
    strict_bins = {f"w{w}": wc.get(w, 0) for w in range(1, arity)}
    relaxed_bins = {f"w{w}": wc.get(w, 0) for w in range(0, arity + 1)}

    # per-coordinate ones-rate, order-invariant summary (sorted, so it is a multiset statistic)
    col_ones = sorted(sum(t[i] for t in tuples) for i in range(arity)) if n else []
    # coordinate "fixedness": how many coordinates are constant across all tuples
    n_fixed = sum(1 for i in range(arity) if len({t[i] for t in tuples}) == 1) if n else arity

    # symmetry: orbit of the relation under coordinate permutation -> |Aut| = a! / orbit_size
    canon = {tuple(sorted(tuple(t[p[i]] for i in range(arity)) for t in tuples))
             for p in permutations(range(arity))}
    orbit = len(canon)
    aut = (_fact(arity) // orbit) if orbit else 1

    # closure under complement (a surface symmetry, NOT a Post flag)
    comp = {tuple(1 - x for x in t) for t in tuples}
    self_complementary = int(comp == set(tuples)) if n else 0

    # Hamming-order shape: minimal/maximal tuples, and whether R is an up-set / down-set
    ts = set(tuples)
    def leq(a, b): return all(x <= y for x, y in zip(a, b))
    minimal = sum(1 for t in ts if not any(u != t and leq(u, t) for u in ts))
    maximal = sum(1 for t in ts if not any(u != t and leq(t, u) for u in ts))

    f = {
        "arity": arity,
        "n_tuples": n,
        "tuple_density": round(n / total, 6),
        "weight_mean": round(sum(weights) / n, 4) if n else 0.0,
        "weight_spread": (max(weights) - min(weights)) if n else 0,
        "n_distinct_weights_strict": len([w for w in wc if 0 < w < arity]),
        "col_ones_min": col_ones[0] if col_ones else 0,
        "col_ones_max": col_ones[-1] if col_ones else 0,
        "col_ones_range": (col_ones[-1] - col_ones[0]) if col_ones else 0,
        "n_fixed_coords": n_fixed,
        "aut_group_size": aut,
        "self_complementary": self_complementary,
        "n_minimal_tuples": minimal,
        "n_maximal_tuples": maximal,
        **strict_bins,
    }
    return f, relaxed_bins


def _fact(k):
    r = 1
    for i in range(2, k + 1):
        r *= i
    return r


def census(rows, keys):
    """Census-before-seal on every new derived quantity (SCHEMA §3.3/§3.3b). A feature that cannot vary
    cannot carry a bet; a feature whose modal value swamps the population cannot carry a contrast."""
    out = {}
    for k in keys:
        vals = [r["features"].get(k) for r in rows]
        vals = [v for v in vals if v is not None]
        c = Counter(vals)
        top, topn = c.most_common(1)[0]
        share = topn / len(vals)
        out[k] = {"n_distinct": len(c), "modal_value": top, "modal_share": round(share, 4),
                  "constant": len(c) == 1,
                  "starved": bool(len(c) == 1 or share > 0.90),
                  "note": ("CONSTANT — carries no information" if len(c) == 1 else
                           f"modal value holds {share:.0%} — weak contrast" if share > 0.90 else "ok")}
    return out


def main() -> int:
    ct = json.loads((LAT / "prism_v2_charges.json").read_text())["charge_table"]
    rows, relaxed = [], {}
    for r in ct:
        key = f"b{r['arity']}:{_bitmask(r['arity'], r['relation'])}"
        f, rb = surface_features(r["arity"], r["relation"])
        rows.append({"row_key": key, "arity": r["arity"], "features": f})
        relaxed[key] = rb

    # BUG CAUGHT BY RUNNING IT: keys must be the UNION over all rows, not row 0's. Row 0 is arity 1,
    # whose strict weight bins are empty by construction (range(1,1)), so taking its key set silently
    # DROPPED every weight-histogram feature. Rows of different arity carry different bin counts, so the
    # matrix is ragged; missing bins are filled with 0 (the bin genuinely holds zero tuples at that arity).
    keys = sorted({k for r in rows for k in r["features"]})
    for r in rows:
        for k in keys:
            r["features"].setdefault(k, 0)
    cen = census(rows, keys)
    usable = [k for k, v in cen.items() if not v["starved"]]
    starved = [k for k, v in cen.items() if v["starved"]]

    doc = {"schema": "grid-surface-features/v1",
           "sealed_rule": ("SURFACE ONLY. The 10 Post flags and everything derived from them are excluded. "
                           "The weight histogram OMITS bins 0 and `arity` because those ARE 0valid/1valid."),
           "excluded_algebra": list(EXCLUDED_ALGEBRA),
           "excluded_derived": list(EXCLUDED_DERIVED),
           "n_rows": len(rows), "feature_names": keys,
           "census": cen, "usable_features": usable, "starved_features": starved,
           "relaxed_weight_bins_stored_not_scored": ("bins w0 and w{arity} are stored so the COST of the "
                                                     "exclusion is measurable; they are NOT scored"),
           "rows": rows}
    OUT.write_text(json.dumps(doc, indent=1) + "\n")
    (LAT / "grid_surface_relaxed_bins.json").write_text(json.dumps(relaxed, indent=1) + "\n")

    print(f"wrote {OUT.name}  rows={len(rows)}  features={len(keys)}  "
          f"sha256 {hashlib.sha256(OUT.read_bytes()).hexdigest()[:16]}")
    print(f"\ncensus-before-seal: {len(usable)} usable · {len(starved)} starved")
    for k in keys:
        v = cen[k]
        mark = "STARVED" if v["starved"] else "ok     "
        print(f"  {mark} {k:<26} distinct={v['n_distinct']:<5} modal={str(v['modal_value'])[:12]:<12} "
              f"{v['modal_share']:.0%}")
    return 0


def _bitmask(arity, relation):
    m = 0
    for t in relation:
        idx = 0
        for bit in t:
            idx = (idx << 1) | int(bit)
        m |= (1 << idx)
    width = max(1, (2 ** arity + 3) // 4)
    return f"{m:0{width}x}"


if __name__ == "__main__":
    sys.exit(main())
