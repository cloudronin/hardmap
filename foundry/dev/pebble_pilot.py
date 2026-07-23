"""Sprint 6 Pebble P1 — the pilot (prereg_v12, R-1 sealed rule). Data (relations + tuple_dispersion) in hand from
Sprint 4.6; ruggedness re-measured across a SIZE sweep. Question: does tuple_dispersion's HELD-OUT-by-co-clone
predictive power for ruggedness DECAY as instance size grows (local geometry propagates with finite range) or hold
(compositional inheritance)? Scored by the sealed numeric rule.

Run: PYTHONPATH=... python foundry/dev/pebble_pilot.py
"""
import json
import random
from collections import Counter
from itertools import combinations, product

import numpy as np

from foundry import postlattice as PL
from foundry import relfeatures as RF
from foundry import solscape as S
from foundry.landscape_run import locate_alpha_struct

T3 = list(product((0, 1), repeat=3))


def _profile(R):
    return tuple(n for n, ok in (("0v", PL.is_0valid((R,))), ("1v", PL.is_1valid((R,))),
                                 ("horn", PL.has_polymorphism((R,), PL.HORN)),
                                 ("dhorn", PL.has_polymorphism((R,), PL.DUAL_HORN)),
                                 ("bij", PL.has_polymorphism((R,), PL.BIJUNCTIVE)),
                                 ("aff", PL.has_polymorphism((R,), PL.AFFINE))) if ok)


def _select_arity3(reps_per=6):
    """Re-enumerate arity-3 relations (like Sprint 4.6), grouped by 6-flag profile; keep tractable co-clones with
    >= reps_per representatives; take reps_per each (fixed seed). Same-arity -> no R-2 arity confound in the pilot."""
    groups = {}
    for k in (4, 5, 6, 7):
        for combo in combinations(T3, k):
            R = frozenset(combo)
            key = _profile(R)
            if key:
                groups.setdefault(key, []).append(R)
    rng = random.Random("pebble-pilot")
    sel = []
    for key, Rs in groups.items():
        if len(Rs) < reps_per:
            continue
        for R in rng.sample(Rs, reps_per):
            sel.append({"profile": "+".join(key), "relation": sorted(tuple(t) for t in R),
                        "tuple_dispersion": RF.tuple_dispersion(R)})
    return sel

SIZE_BANDS = [12, 18, 24, 30]                     # smallest .. largest; bands fixed here (prereg_v12 R-1)
COARSE = [round(0.3 + 0.3 * i, 2) for i in range(14)]
DROP_THRESHOLD = 0.30                             # sealed: attenuating iff held-out power drops >= 30% (relative)


def measure_rug(R, n):
    a_struct, _ = locate_alpha_struct((R,), (0, 1), n, 500000, K=35, grid=COARSE)
    r = S.landscape_reading((R,), (0, 1), n, round(0.9 * a_struct, 3), base_seed=501000, K=35, n_instances=4)
    return r["pooled_score"]


def heldout_power(rows):
    """Leave-one-co-clone-out; predict held reps' ruggedness from [tuple_dispersion]; pooled corr(pred, actual)."""
    coclones = sorted({r["coclone"] for r in rows})
    preds, acts = [], []
    for cc in coclones:
        tr = [r for r in rows if r["coclone"] != cc]
        te = [r for r in rows if r["coclone"] == cc]
        if len(tr) < 5 or not te:
            continue
        X = np.array([[r["tuple_dispersion"]] for r in tr])
        y = np.array([r["ruggedness"] for r in tr])
        _, beta = RF.fit_r2(X, y)
        for r in te:
            preds.append(beta[0] + beta[1] * r["tuple_dispersion"])
            acts.append(r["ruggedness"])
    if len(set(preds)) < 2 or len(set(acts)) < 2:
        return None
    return round(float(np.corrcoef(preds, acts)[0, 1]), 3)


def bootstrap_ci(rows, n_boot=400, seed=7):
    rng = np.random.default_rng(seed)
    vals = []
    idx = list(range(len(rows)))
    for _ in range(n_boot):
        bs = [rows[i] for i in rng.choice(idx, len(idx), replace=True)]
        p = heldout_power(bs)
        if p is not None:
            vals.append(p)
    if not vals:
        return None
    return (round(np.percentile(vals, 2.5), 3), round(np.percentile(vals, 97.5), 3))


def decide_verdict(p_small, p_large, rel_drop, within_noise):
    """The SEALED R-1 rule (prereg_v12), applied in priority order — faithful to the prereg text:
      * within the bootstrap noise band            -> INCONCLUSIVE (declared on measurement quality)
      * resolved (outside noise) AND drop >= 30%    -> ATTENUATING (finite propagation range)
      * resolved (outside noise) AND drop <  30%    -> UNDIMINISHED (compositional inheritance)
    INCONCLUSIVE depends ONLY on 'within the noise band' — the prereg attaches no drop-size qualifier to it."""
    if p_small is None or p_large is None:
        return "INSUFFICIENT_RESOLUTION"
    if within_noise:
        return "INCONCLUSIVE (trend within bootstrap noise band)"
    if rel_drop is not None and rel_drop >= DROP_THRESHOLD:
        return "ATTENUATING (finite propagation range — genuine propagation, xi's pilot measurement)"
    return "UNDIMINISHED (compositional inheritance — reframe the reach instrument as construction)"


def main():
    sel = _select_arity3(reps_per=6)
    n_cc = len(set(r["profile"] for r in sel))
    print(f"pilot: {len(sel)} arity-3 relations across {n_cc} co-clones; size bands {SIZE_BANDS}")

    per_band = {}
    band_rows = {}
    for n in SIZE_BANDS:
        rows = []
        for r in sel:
            R = frozenset(tuple(t) for t in r["relation"])
            rug = measure_rug(R, n)
            if rug is not None:
                rows.append({"coclone": r["profile"], "tuple_dispersion": r["tuple_dispersion"], "ruggedness": rug})
        band_rows[n] = rows
        per_band[n] = {"held_out_power": heldout_power(rows), "n_rows": len(rows)}
        print(f"  n={n}: held_out_power={per_band[n]['held_out_power']} (rows={per_band[n]['n_rows']})")

    smallest, largest = SIZE_BANDS[0], SIZE_BANDS[-1]
    p_small = per_band[smallest]["held_out_power"]
    p_large = per_band[largest]["held_out_power"]
    ci_small = bootstrap_ci(band_rows[smallest])
    ci_large = bootstrap_ci(band_rows[largest])
    rel_drop = round((p_small - p_large) / p_small, 3) if (p_small and p_small > 0) else None
    # noise band: do the smallest/largest bootstrap CIs overlap? (INCONCLUSIVE if the trend is within noise)
    within_noise = (ci_small and ci_large and ci_large[1] >= ci_small[0])
    verdict = decide_verdict(p_small, p_large, rel_drop, bool(within_noise))

    out = {"prereg": "v12", "size_bands": SIZE_BANDS, "per_band": per_band,
           "held_out_power_smallest": p_small, "held_out_power_largest": p_large,
           "relative_drop": rel_drop, "drop_threshold": DROP_THRESHOLD,
           "bootstrap_ci_smallest": ci_small, "bootstrap_ci_largest": ci_large,
           "within_noise_band": bool(within_noise), "verdict": verdict}
    json.dump(out, open("foundry/foundry/results/landscape/pebble_pilot.json", "w"), indent=2)
    print(f"\nrelative drop {p_small}->{p_large} = {rel_drop} (threshold {DROP_THRESHOLD}); "
          f"CIs small={ci_small} large={ci_large} within_noise={within_noise}")
    print(f"VERDICT: {verdict}")


if __name__ == "__main__":
    main()
