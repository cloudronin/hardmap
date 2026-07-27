#!/usr/bin/env python3
"""N6-R Phase 3 — excess, then SCORED ONCE. prereg-grade; the prediction file is the seal.

THE SCORER REFUSES TO RUN against anything but the sealed prediction hash. If the predictions changed
after being filed, the bet is not the bet that was made, and no result from this file would mean anything.

SEALED BET A (filed in n6r_predictions.json, hash ef18293d..., committed before this file first ran):
    partial Spearman of log-inflation against fair-null excess, controlling for measured violation rate,
    on the 14,555-member discovery population. DIRECTION: NEGATIVE. CI clear of zero, permutation null
    typed to the population.

TERRAIN'S SATURATION RIDER, declared in the prediction file before any rate existed: a reading whose
measured rate is EXACTLY 1.0 is flagged suspected-forced, and the statistic is reported WITH and WITHOUT
them. Declared in advance is what stops the screen being chosen after seeing which way it moves the answer.

MEASURED RATES ARE COMPUTED FRESH AND EXHAUSTIVELY. |R| <= 15 so C(15,3) = 455 — there is no sampling and
therefore no sampling question. The probe's stored rates are deliberately not read: recomputing costs
nothing and removes a provenance dependency from the scored path.
"""
import hashlib
import json
import math
import random
import sys
from itertools import combinations
from pathlib import Path
from statistics import mean, pstdev

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "dev"))
LAT = ROOT / "foundry" / "results" / "lattice"
ROSTER = LAT / "prism_v2_charges.json"
PRED = LAT / "n6r_predictions.json"
INFL = LAT / "n6r_inflation.json"
OUT = LAT / "n6r_results.json"
import terrain_score as T                                              # noqa: E402
import n2_dense_control as N2                                          # noqa: E402

SEALED_PRED_HASH = "ef18293da028c265945e5b6f7d1113253b1e27b1f6171cc1a4ae2df346a217de"
K_CTRL, N_PERM, Z = 30, 500, 1.959964
FLAVOURS = {
    "majority": (lambda ts: tuple(1 if sum(c) >= 2 else 0 for c in zip(*ts)), 3),
    "minority": (lambda ts: tuple(c[0] ^ c[1] ^ c[2] for c in zip(*ts)), 3),
    "min":      (lambda ts: tuple(min(c) for c in zip(*ts)), 2),
    "max":      (lambda ts: tuple(max(c) for c in zip(*ts)), 2),
}


def exact_rate(rel, op, m):
    R = set(rel)
    subs = list(combinations(rel, m))
    return (sum(1 for s in subs if op(s) not in R) / len(subs)) if subs else None


def ranks(v):
    order = sorted(range(len(v)), key=lambda i: v[i])
    r = [0.0] * len(v)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
            j += 1
        avg = (i + j) / 2.0
        for k in range(i, j + 1):
            r[order[k]] = avg
        i = j + 1
    return r


def pearson(a, b):
    n = len(a); ma, mb = sum(a) / n, sum(b) / n
    num = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    den = math.sqrt(sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b))
    return num / den if den else float("nan")


def partial(ra, rb, rc):
    """Partial correlation of a and b controlling for c, on pre-computed ranks -> partial Spearman."""
    rab, rac, rbc = pearson(ra, rb), pearson(ra, rc), pearson(rb, rc)
    d = math.sqrt((1 - rac ** 2) * (1 - rbc ** 2))
    return (rab - rac * rbc) / d if d else float("nan")


def score_block(infl, exc, rate, rng, label):
    li, le, lr = ranks([math.log(v) for v in infl]), ranks(exc), ranks(rate)
    obs = partial(li, le, lr)
    null = []
    idx = list(range(len(le)))
    for _ in range(N_PERM):
        rng.shuffle(idx)
        null.append(partial(li, [le[i] for i in idx], lr))
    null.sort()
    more_extreme = sum(1 for v in null if v <= obs)
    p = (more_extreme + 1) / (N_PERM + 1)
    lo, hi = null[int(0.025 * N_PERM)], null[int(0.975 * N_PERM)]
    return {"label": label, "n": len(exc), "partial_spearman": round(obs, 4),
            "permutation_null_95pct": [round(lo, 4), round(hi, 4)],
            "p_one_tailed_negative": round(p, 5),
            "clear_of_null": bool(obs < lo),
            "marginals": {"log_infl_vs_excess": round(pearson(li, le), 4),
                          "log_infl_vs_rate": round(pearson(li, lr), 4),
                          "rate_vs_excess": round(pearson(lr, le), 4)}}


def main() -> int:
    got = hashlib.sha256(PRED.read_bytes()).hexdigest()
    if got != SEALED_PRED_HASH:
        print(f"FAIL — prediction hash mismatch.\n  sealed {SEALED_PRED_HASH}\n  found  {got}\n"
              f"The bet filed is not the bet on disk. Refusing to score.", file=sys.stderr)
        return 1
    print(f"N6-R PHASE 3 — SCORING ONCE\n\n  prediction hash verified: {got[:32]}...\n")

    roster = json.loads(ROSTER.read_text())["charge_table"]
    rel_of = {i: [tuple(t) for t in c["relation"]] for i, c in enumerate(roster)}
    disc = json.loads(INFL.read_text())["readings"]
    rng = random.Random(20260731)

    rows, dropped = [], []
    for d in disc:
        rel = rel_of[d["class_index"]]
        op, m = FLAVOURS[d["flavour"]]
        rate = exact_rate(rel, op, m)
        if rate is None:
            dropped.append({**d, "why": "no m-subsets"}); continue
        # fair null per the standing ladder: tier 1.5 where its chain clears, CP otherwise
        vals, route = [], None
        c15, sw = T.tier15(rel, rng)
        if sw >= max(50, len(rel) // 4):
            route = "tier1.5"
            for _ in range(K_CTRL):
                cc, s2 = T.tier15(rel, rng)
                v = exact_rate(cc, op, m)
                if v is not None:
                    vals.append(v)
        else:
            route = "CP"
            for _ in range(K_CTRL):
                cc, _e, _u = N2.cp_control(rel, rng)
                v = exact_rate(cc, op, m)
                if v is not None:
                    vals.append(v)
        if len(vals) < 2 or pstdev(vals) == 0:
            dropped.append({**d, "why": f"INSUFFICIENT-degenerate ({route} control did not vary)"})
            continue
        rows.append({**{k: d[k] for k in ("class_index", "arity", "r", "flavour", "infl", "depth",
                                          "fingerprint", "r_band")},
                     "measured_rate": round(rate, 6), "control_mean": round(mean(vals), 6),
                     "control_sd": round(pstdev(vals), 6),
                     "excess": round(rate - mean(vals), 6), "route": route,
                     "suspected_forced_saturated": rate == 1.0})

    sat = [r for r in rows if r["suspected_forced_saturated"]]
    clean = [r for r in rows if not r["suspected_forced_saturated"]]
    blocks = [score_block([r["infl"] for r in rows], [r["excess"] for r in rows],
                          [r["measured_rate"] for r in rows], rng, "ALL (with suspected-forced)")]
    if clean:
        blocks.append(score_block([r["infl"] for r in clean], [r["excess"] for r in clean],
                                  [r["measured_rate"] for r in clean], rng,
                                  "SATURATION-SCREENED (rate == 1.0 removed)"))
    # class-clustered robustness: flavours inside one class share the region
    byc = {}
    for r in clean or rows:
        byc.setdefault(r["class_index"], []).append(r)
    if len(byc) > 30:
        blocks.append(score_block([mean(x["infl"] for x in v) for v in byc.values()],
                                  [mean(x["excess"] for x in v) for v in byc.values()],
                                  [mean(x["measured_rate"] for x in v) for v in byc.values()],
                                  rng, "CLASS-CLUSTERED (screened)"))

    primary = blocks[1] if len(blocks) > 1 else blocks[0]
    verdict = ("REPLICATES — the disclosed negative sign survives blind"
               if primary["clear_of_null"] and primary["partial_spearman"] < 0 else
               "DOES NOT REPLICATE — the disclosed prior was the biased subsample's artifact"
               if primary["partial_spearman"] >= 0 or primary["p_one_tailed_negative"] > 0.05 else
               "INSUFFICIENT")

    doc = {"schema": "n6r-results/v1", "scored_once": True,
           "sealed_prediction_hash": SEALED_PRED_HASH,
           "sealed_direction": "NEGATIVE",
           "n_discovery": len(disc), "n_scored": len(rows), "n_dropped": len(dropped),
           "dropped_reasons": {k: sum(1 for d in dropped if d["why"] == k)
                               for k in {d["why"] for d in dropped}},
           "saturation_screen": {"declared": "in the prediction file, before any rate existed",
                                 "n_flagged_rate_exactly_1": len(sat),
                                 "reported_both_ways": True},
           "route_counts": {r: sum(1 for x in rows if x["route"] == r) for r in {x["route"] for x in rows}},
           "BLOCKS": blocks, "VERDICT_A": verdict,
           "depth_descriptive": {"median": sorted(x["depth"] for x in rows)[len(rows) // 2],
                                 "max": max(x["depth"] for x in rows),
                                 "note": "descriptive everywhere; never sealed"},
           "readings": rows}
    OUT.write_text(json.dumps(doc, indent=1) + "\n")

    print(f"  scored {len(rows)}   dropped {len(dropped)}  {doc['dropped_reasons']}")
    print(f"  routes {doc['route_counts']}")
    print(f"  suspected-forced (rate == 1.0): {len(sat)}\n")
    for b in blocks:
        print(f"  {b['label']}")
        print(f"    n={b['n']}  partial Spearman {b['partial_spearman']:+.4f}   "
              f"perm-null 95% [{b['permutation_null_95pct'][0]:+.4f}, "
              f"{b['permutation_null_95pct'][1]:+.4f}]  p={b['p_one_tailed_negative']:.5f}  "
              f"{'CLEAR' if b['clear_of_null'] else 'not clear'}")
        print(f"    marginals {b['marginals']}")
    print(f"\n  VERDICT A: {verdict}")
    print(f"\n  sha256 {hashlib.sha256(OUT.read_bytes()).hexdigest()[:16]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
