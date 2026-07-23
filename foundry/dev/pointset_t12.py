"""Pebble T1.2 (substrate program map) — are point-to-set reach and tuple_dispersion the SAME property through two
channels, or genuinely DIFFERENT properties? Direct correlation across relations, with the qualified poles (affine
parity = known high reach; bounded-width = known low) as known-answer anchors. Data in hand / quick.

Licensing (per the map): high corr -> tuple_dispersion is a cheap PROXY for reach and inherits its interpretation.
Low corr (with P4 already positive) -> they are DIFFERENT properties and terrain reads both. Reported over the full
roster (with anchors) AND bounded-width-only (the honest within-class read).

Run: PYTHONPATH=... python foundry/dev/pointset_t12.py
"""
import json
import statistics as st

import numpy as np

from foundry import pointset as PS
from foundry import relfeatures as RF
import sys, os
sys.path.insert(0, os.path.join(os.getcwd(), "foundry", "dev"))
import pointset_sweep as SW    # reuse long_anchors + density_for + classify

N, NINST, RADIUS, DFRAC = 18, 4, 2, 0.6
BW = {"horn", "dhorn", "bij"}


def main():
    roster = json.load(open("foundry/foundry/results/landscape/sprint46_roster.json"))["rows"]
    bw = [{"profile": r["profile"], "class": "SHORT", "id": r["profile"], "relation": r["relation"],
           "alpha_struct": r["alpha_struct"]} for r in roster if set(r["profile"].split("+")) & BW]
    recs = SW.long_anchors() + bw      # affine anchors + all bounded-width relations

    rows = []
    for i, rec in enumerate(recs):
        R = frozenset(tuple(t) for t in rec["relation"])
        alpha = SW.density_for(rec, N)
        reach = PS.measure_pointset((R,), (0, 1), N, alpha, n_instances=NINST, base_seed=985000 + i, reach_radius=RADIUS)["reach_score"]
        if reach is None:
            continue
        rows.append({"class": rec["class"], "reach": reach, "tuple_dispersion": RF.tuple_dispersion(R)})
    print(f"T1.2: {len(rows)} relations (LONG {sum(r['class']=='LONG' for r in rows)}, "
          f"SHORT {sum(r['class']=='SHORT' for r in rows)})", flush=True)

    def corr(sub):
        x = [r["reach"] for r in sub]; y = [r["tuple_dispersion"] for r in sub]
        return round(float(np.corrcoef(x, y)[0, 1]), 3) if len(set(x)) > 1 and len(set(y)) > 1 else None

    full = corr(rows)
    bw_only = corr([r for r in rows if r["class"] == "SHORT"])
    long_mean = round(st.mean([r["reach"] for r in rows if r["class"] == "LONG"]), 3)
    long_td = round(st.mean([r["tuple_dispersion"] for r in rows if r["class"] == "LONG"]), 3)
    sh_reach = round(st.mean([r["reach"] for r in rows if r["class"] == "SHORT"]), 3)
    sh_td = round(st.mean([r["tuple_dispersion"] for r in rows if r["class"] == "SHORT"]), 3)

    reading = ("PROXY (high corr — tuple_dispersion is a cheap proxy for reach)" if full is not None and abs(full) >= 0.7
               else "DIFFERENT (low corr — reach and tuple_dispersion are different properties)" if full is not None and abs(full) < 0.4
               else "PARTIAL (moderate corr — related but not interchangeable)")
    out = {"map_row": "T1.2", "n_rows": len(rows),
           "corr_reach_vs_tupledisp_full_with_anchors": full, "corr_bounded_width_only": bw_only,
           "anchors": {"LONG_mean_reach": long_mean, "LONG_mean_tupledisp": long_td,
                       "SHORT_mean_reach": sh_reach, "SHORT_mean_tupledisp": sh_td},
           "READING": reading}
    json.dump(out, open("foundry/foundry/results/landscape/pointset_t12.json", "w"), indent=2)
    print(f"\ncorr(reach, tuple_dispersion): full(with anchors)={full}  bounded-width-only={bw_only}")
    print(f"anchors: LONG reach={long_mean}/td={long_td}   SHORT reach={sh_reach}/td={sh_td}")
    print(f"READING: {reading}")


if __name__ == "__main__":
    main()
