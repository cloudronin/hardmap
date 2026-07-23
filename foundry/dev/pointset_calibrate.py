"""Pebble P2b B1+B2 — point-to-set calibration (prereg_v21). B1: the bucket-population report (the pre-fit
resolution gate). B2: the three-pole verdict — short < medium < LONG(parity), non-overlapping intervals, PARITY AT
THE TOP (the known-answer inversion of corr, which put parity at the floor).

Poles at n=16 (exact coset enumeration): short = 2-SAT low density (prereg_v18 nonzero short pole); medium = 2-SAT
moderate density; long = 3-XOR PARITY; consistency = 2-affine (globally rigid, reads high). Parity/affine are UNSAT
at high alpha, so densities are per-pole in their SAT regime — the ordering is what is sealed, not the values.

Run: PYTHONPATH=... python foundry/dev/pointset_calibrate.py
"""
import json
from itertools import product

from foundry import pointset as PS
from foundry import reach as X

R3_XOR = frozenset({(0, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 0)})
R4_XOR = frozenset(t for t in product((0, 1), repeat=4) if sum(t) % 2 == 0)

N, NINST = 16, 8
POLES = [
    ("short (2-SAT low-dens)", (X.R_IMP,), 0.4, 861000),
    ("medium (2-SAT mod-dens)", (X.R_IMP,), 0.9, 862000),
    ("long (3-XOR parity)", (R3_XOR,), 0.6, 863000),
    ("consistency (2-affine)", (X.R_EQ,), 0.6, 864000),
    ("aux (4-XOR parity)", (R4_XOR,), 0.6, 865000),
]


def main():
    out = {"prereg": "v21", "n": N, "n_instances": NINST, "poles": {}}
    print("=== B1 population report (pre-fit gate) ===")
    for name, rels, alpha, seed in POLES:
        m = PS.measure_pointset(rels, (0, 1), N, alpha, n_instances=NINST, base_seed=seed)
        iv = X.boot_interval(m["per_unit_reach"]) if len(m["per_unit_reach"]) >= 2 else (None, None)
        m["reach_interval"] = iv
        out["poles"][name] = m
        print(f"\n{name}  alpha={alpha}  coset~{m['median_coset']} exact_frac={m['exact_fraction']}")
        for r, c in m["radii"].items():
            print(f"   r={r}: signal={c['signal']} mean_buckets={c['mean_buckets']} "
                  f"min_pop={c['min_pop']} median_pop={c['median_pop']} measurable={c['measurable']} (n_obs={c['n_obs']})")
        print(f"   -> reach_score(@largest valid r={m['largest_valid_radius']})={m['reach_score']} interval={iv}")

    P = out["poles"]
    s = P["short (2-SAT low-dens)"]["reach_score"]
    md = P["medium (2-SAT mod-dens)"]["reach_score"]
    lg = P["long (3-XOR parity)"]["reach_score"]
    ref = P["consistency (2-affine)"]["reach_score"]
    ivs = {k: P[k]["reach_interval"] for k in P}
    ordered = (s is not None and md is not None and lg is not None and s < md < lg)
    parity_top = lg is not None and lg == max(x for x in (s, md, lg, ref) if x is not None)
    nonoverlap = (all(None not in ivs[k] for k in ("short (2-SAT low-dens)", "medium (2-SAT mod-dens)", "long (3-XOR parity)"))
                  and ivs["short (2-SAT low-dens)"][1] < ivs["medium (2-SAT mod-dens)"][0]
                  and ivs["medium (2-SAT mod-dens)"][1] < ivs["long (3-XOR parity)"][0])
    verdict = "QUALIFIED" if (ordered and parity_top and nonoverlap) else "NOT_QUALIFIED_see_report"
    out["verdict"] = {"reach_scores": {"short": s, "medium": md, "long_parity": lg, "reference_2affine": ref},
                      "ordered_short_lt_medium_lt_parity": bool(ordered), "parity_at_top": bool(parity_top),
                      "intervals_nonoverlapping": bool(nonoverlap), "VERDICT": verdict}
    json.dump(out, open("foundry/foundry/results/landscape/pointset_calibration.json", "w"), indent=2)
    print(f"\n=== B2 verdict ===\nreach: short={s} medium={md} long(parity)={lg} ref(2-affine)={ref}")
    print(f"ordered={ordered} parity_at_top={parity_top} nonoverlap={nonoverlap}\nVERDICT: {verdict}")


if __name__ == "__main__":
    main()
