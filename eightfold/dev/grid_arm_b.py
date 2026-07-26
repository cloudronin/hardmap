#!/usr/bin/env python3
"""Mosaic v3 G3 — ARM B: do Anatomy coordinates predict CITED charges out-of-sample?

THE MAIN EVENT. Arm A established that the Boolean universe cannot test the bridge (there it is a theorem),
so the empirical question lives here, where charges are CITED FACTS ABOUT THE LITERATURE rather than
computed functions of structure.

CONTAMINATION PROTOCOL (prereg_v12, all three channels):
  1 TARGET LEAKAGE VIA TASK TEXT — per-charge feature-exclusion map, ENFORCED HERE and asserted by a
    loudly-failing test. The circularity carve-out authorised these derivations as TYPING; it never
    authorised them as PREDICTION FEATURES.
  2 NAME-KNOWLEDGE — the blind coders received problem_name, so locality_class may encode charge knowledge.
    MEASURED, not assumed: every charge is scored WITH and WITHOUT locality_class. If accuracy depends on
    it, THE LEAK IS THE FINDING.
  3 PREDICTOR-SIDE — no LLM in the predictor. Fitted CART only. Closed by construction.

Nulls are FOLD-WEIGHTED (train-fold mode -> test fold), the achievable baseline, per the G2 correction.
Folds group by problem_family so near-duplicate problems cannot straddle train/test.
"""
import hashlib, json, sys
from collections import Counter
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "dev"))
from eightfold import atlas as A                                    # noqa: E402
import quarry_v3_spec as V3                                          # noqa: E402
sys.path.insert(0, str(ROOT.parent / "foundry" / "dev"))
from grid_arm_a import build, predict                                # noqa: E402  (same CART)

AT = ROOT / "eightfold" / "results" / "atlas"
OUT = AT / "grid_arm_b_results.json"
PRED = AT / "grid_arm_b_predictions.json"
SEED, DEPTH, MINLEAF, NFOLD = 20260725, 5, 6, 5
SPEC = V3.V3_SPEC

# prereg_v12 contamination_protocol channel 1 — sealed map, enforced not trusted
EXCLUDE = {"approximation": {"objective_type", "arity_class"},
           "parameterized": {"kernel_status"},
           "average_case": {"self_reducibility"}}
CHARGES = ("decision", "counting", "approximation", "parameterized", "average_case")


def main():
    v3 = {e.problem_id: e for e in A.load_atlas(str(AT / "atlas_v3.jsonl"))}
    an = {}
    for l in (AT / "anatomy_v1.jsonl").read_text().splitlines():
        if not l.strip(): continue
        r = json.loads(l)
        if r["universe"] == "natural":
            an[r["problem_id"]] = {c["feature"]: c["value"] for c in r["features"]}

    # feature space: Anatomy's natural columns, categorical -> integer codes
    FEATS = ["locality_class", "encoding_type", "objective_type", "arity_class",
             "kernel_status", "self_reducibility", "reduction_out_degree"]
    # ONE-HOT ENCODING. The first version hash-coded categories to abs(hash(v))%997, which was wrong twice:
    # (a) a CART splits on x <= t, so a hash imposes an ARBITRARY TOTAL ORDER on unordered categories and
    #     every split is on noise; (b) Python's string hash is RANDOMIZED PER PROCESS, so the run was not
    #     reproducible at all (592 / 475 / 278 across three runs of the same value) -- the seed discipline
    #     was broken at the encoder. One-hot is order-free and deterministic.
    def levels_of(f):
        vs = set()
        for p in an:
            v = an[p].get(f)
            vs.add("__missing__" if v is None else ("__record__" if isinstance(v, dict) else str(v)))
        return sorted(vs)
    LEVELS = {f: levels_of(f) for f in FEATS}
    NUMERIC = {"reduction_out_degree"}
    def encode(pid, use):
        row = []
        for f in use:
            v = an.get(pid, {}).get(f)
            if f in NUMERIC:
                row.append(float(v) if isinstance(v, (int, float)) else -1.0)
                continue
            key = "__missing__" if v is None else ("__record__" if isinstance(v, dict) else str(v))
            row.extend(1.0 if key == lv else 0.0 for lv in LEVELS[f])
        return row
    pids = sorted(p for p in v3 if p in an)
    fam = {p: v3[p].problem_family for p in pids}
    rng = np.random.default_rng(SEED)
    ufam = sorted(set(fam.values()))
    order = sorted(ufam, key=lambda g: hashlib.sha256((g + str(SEED)).encode()).hexdigest())
    ffold = {g: i % NFOLD for i, g in enumerate(order)}
    folds = np.array([ffold[fam[p]] for p in pids])

    def fold_null(y, fl):
        yp = np.empty(len(y), dtype=object)
        for f in range(NFOLD):
            tr, te = fl != f, fl == f
            if te.sum() == 0 or tr.sum() == 0: continue
            yp[te] = Counter(y[tr]).most_common(1)[0][0]
        return float((yp == y).mean())

    res = {"seed": SEED, "model": f"CART depth<={DEPTH}", "n_rows_total": len(pids),
           "fold_key": "problem_family", "nulls": "fold-weighted (train-fold mode -> test fold)",
           "protocol": "prereg_v12 contamination_protocol_arm_B", "per_charge": {}}
    allpred = {}
    for ch in CHARGES:
        real = SPEC.charge_real_values[ch]
        idx = [i for i, p in enumerate(pids) if (g := _cv(v3[p], ch)) in real]
        if len(idx) < 40:
            res["per_charge"][ch] = {"status": "SKIPPED — too few real cells", "n": len(idx)}
            continue
        y = np.array([_cv(v3[pids[i]], ch) for i in idx])
        fl = folds[idx]
        for variant, drop_loc in (("with_locality", False), ("without_locality", True)):
            use = [f for f in FEATS if f not in EXCLUDE.get(ch, set())
                   and not (drop_loc and f == "locality_class")]
            # CHANNEL 1 ENFORCEMENT — assert, do not trust
            leaked = set(use) & EXCLUDE.get(ch, set())
            assert not leaked, f"LEAKAGE: {leaked} in {ch}'s matrix"
            X = np.array([encode(pids[i], use) for i in idx], dtype=float)
            yp = np.empty(len(y), dtype=object)
            for f in range(NFOLD):
                tr, te = fl != f, fl == f
                if te.sum() == 0 or tr.sum() == 0: continue
                yp[te] = predict(build(X[tr], y[tr], DEPTH), X[te])
            acc = float((yp == y).mean())
            res["per_charge"].setdefault(ch, {})[variant] = {
                "n": len(idx), "features": use, "acc": round(acc, 4)}
            allpred[f"{ch}:{variant}"] = [str(v) for v in yp]
        nul = fold_null(y, fl)
        w = res["per_charge"][ch]["with_locality"]["acc"]
        wo = res["per_charge"][ch]["without_locality"]["acc"]
        res["per_charge"][ch]["fold_weighted_null"] = round(nul, 4)
        res["per_charge"][ch]["lift_with"] = round(w - nul, 4)
        res["per_charge"][ch]["lift_without"] = round(wo - nul, 4)
        res["per_charge"][ch]["channel_2_locality_dependence"] = round(w - wo, 4)

    PRED.write_text(json.dumps({"seed": SEED, "predictions": allpred}, indent=1) + "\n")
    res["prediction_sha256"] = hashlib.sha256(PRED.read_bytes()).hexdigest()
    OUT.write_text(json.dumps(res, indent=1) + "\n")

    print(f"ARM B — natural atlas, folds=problem_family, nulls fold-weighted")
    print(f"predictions sealed sha {res['prediction_sha256'][:16]}\n")
    print(f"{'charge':<16}{'n':>5}{'null':>8}{'with':>8}{'lift':>8}{'without':>9}{'lift':>8}{'ch2 dep':>9}")
    for ch, v in res["per_charge"].items():
        if "with_locality" not in v:
            print(f"{ch:<16}{v.get('n',0):>5}  {v['status']}"); continue
        print(f"{ch:<16}{v['with_locality']['n']:>5}{v['fold_weighted_null']:>8.4f}"
              f"{v['with_locality']['acc']:>8.4f}{v['lift_with']:>+8.4f}"
              f"{v['without_locality']['acc']:>9.4f}{v['lift_without']:>+8.4f}"
              f"{v['channel_2_locality_dependence']:>+9.4f}")
    return 0


def _cv(entry, ch):
    for c in entry.charges:
        if c.charge == ch: return c.value
    return "n.a."


if __name__ == "__main__":
    sys.exit(main())
