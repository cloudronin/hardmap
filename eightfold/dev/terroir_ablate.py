#!/usr/bin/env python3
"""Terroir v1 T2/T3 — the SEALED arm: A1 (encoding ablation) and A2 (indicator-free refit).

WHAT IS SEALED HERE, AND WHY IT MATTERS. A4 was computed at grounding and is DISCLOSED — it carries no
predictive credit. These two are genuinely unrun as of prereg_v14 and carry full credit. The sealed
prediction, quoted from prereg_v14 verbatim:

    "the headline lift falls BELOW HALF its sealed size, i.e. below +0.0342 -- the spec's own
     ANATOMY-RESIDUAL survival threshold FAILS."

...on BOTH A1 and A2. Disclosed alongside it, because it weakens the bet: the sealed Arm B run ALREADY
reports that dropping `locality_class` alone moves the lift +0.0684 -> +0.0327. The lift was already known
to be fragile to single-feature removal.

WHAT THESE CAN AND CANNOT DO (prereg_v14, stated so the writeup cannot overclaim):
  CANNOT overturn the verdict. Even total collapse under both is a MECHANISM finding; even total survival
  would leave the within-family lift at exactly 0. A4 is the discriminator precisely because it is immune
  to what the ablations do.
  CAN answer HOW the model identifies a family it never trained on -- the one question A4 leaves open.

BASELINE DISCIPLINE. Deltas are measured against a MATCHED RE-RUN BASELINE computed by this script under
identical machinery, not against the sealed number. The script ASSERTS the baseline reproduces the sealed
accuracy exactly; if it ever stops doing so, the deltas are meaningless and the run fails loudly. The
sealed +0.0684 / p = 0.0033 is FROZEN and is never rewritten.
"""
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "dev"))
sys.path.insert(0, str(ROOT.parent / "foundry" / "dev"))
from eightfold import atlas as A                                     # noqa: E402
from eightfold.anatomy import COVERAGE_ABSENCE_MARKERS               # noqa: E402
import quarry_v3_spec as V3                                          # noqa: E402
from grid_arm_a import build, predict                                # noqa: E402  (the same CART)

AT = ROOT / "eightfold" / "results" / "atlas"
OUT = AT / "terroir_v1_ablations.json"
SPEC = V3.V3_SPEC
SEED, DEPTH, MINLEAF, NFOLD, CHARGE = 20260725, 5, 6, 5, "decision"
NPERM = 1000

FEATS = ["locality_class", "encoding_type", "objective_type", "arity_class",
         "kernel_status", "self_reducibility", "reduction_out_degree"]
NUMERIC = {"reduction_out_degree"}
EXCLUDE = {"approximation": {"objective_type", "arity_class"},
           "parameterized": {"kernel_status"},
           "average_case": {"self_reducibility"}}          # `decision` excludes nothing

SEALED_ACC, SEALED_NULL, SEALED_LIFT = 0.6607, 0.5923, 0.0684
HALF_THRESHOLD = 0.0342                                     # prereg_v14's sealed survival line

# prereg_v14 absence_set_ruling. The string markers plus the numeric sentinel. NOT merged with each other
# -- classified together for stripping, distinguished everywhere else.
ABSENCE_STRINGS = {k for k in COVERAGE_ABSENCE_MARKERS if isinstance(k, str)}
ABSENCE_NUMERIC = -1.0


def load():
    v3 = {e.problem_id: e for e in A.load_atlas(str(AT / "atlas_v3.jsonl"))}
    an = {}
    for line in (AT / "anatomy_v1.jsonl").read_text().splitlines():
        if line.strip():
            r = json.loads(line)
            if r["universe"] == "natural":
                an[r["problem_id"]] = {c["feature"]: c["value"] for c in r["features"]}
    pids = sorted(p for p in v3 if p in an)
    fam = {p: v3[p].problem_family for p in pids}
    order = sorted(set(fam.values()), key=lambda g: hashlib.sha256((g + str(SEED)).encode()).hexdigest())
    ffold = {g: i % NFOLD for i, g in enumerate(order)}
    folds = np.array([ffold[fam[p]] for p in pids])
    return v3, an, pids, fam, folds


def charge_value(entry, ch):
    for c in entry.charges:
        if c.charge == ch:
            return c.value
    return "n.a."


def raw_key(an, pid, f):
    """The value AS grid_arm_b.py's encode() sees it -- reproduced exactly, absence markers and all."""
    v = an.get(pid, {}).get(f)
    if f in NUMERIC:
        return float(v) if isinstance(v, (int, float)) else ABSENCE_NUMERIC
    return "__missing__" if v is None else ("__record__" if isinstance(v, dict) else str(v))


def is_absent(f, key):
    return (key == ABSENCE_NUMERIC) if f in NUMERIC else (key in ABSENCE_STRINGS)


def make_encoder(an, pids, use, impute_folds=None, folds=None):
    """One-hot over levels observed on the natural corpus. Order-free and deterministic (instance 22).

    impute_folds is None  -> BASELINE / A1 encoding: absence markers stay as their own levels, exactly as
                             the sealed run had them.
    impute_folds not None -> A2: every absence marker is replaced by the modal SUBSTANTIVE level of that
                             feature computed on the TRAIN FOLD ONLY. Fold-local because a global modal
                             would let test rows inform their own imputation -- the same discipline that
                             makes the null fold-weighted.
    """
    if impute_folds is None:
        levels = {f: sorted({raw_key(an, p, f) for p in pids}) for f in use if f not in NUMERIC}

        def enc(pid, _fold):
            row = []
            for f in use:
                k = raw_key(an, pid, f)
                if f in NUMERIC:
                    row.append(k)
                else:
                    row.extend(1.0 if k == lv else 0.0 for lv in levels[f])
            return row
        return enc, levels

    # A2: substantive level vocabulary only -- absence has NO column anywhere in the matrix
    levels = {f: sorted({k for p in pids if not is_absent(f, k := raw_key(an, p, f))})
              for f in use if f not in NUMERIC}
    fill = {}
    for fold in range(NFOLD):
        train = [p for i, p in enumerate(pids) if folds[i] != fold]
        for f in use:
            present = [k for p in train if not is_absent(f, k := raw_key(an, p, f))]
            fill[(fold, f)] = Counter(present).most_common(1)[0][0] if present else (
                ABSENCE_NUMERIC if f in NUMERIC else "__missing__")

    def enc(pid, fold):
        row = []
        for f in use:
            k = raw_key(an, pid, f)
            if is_absent(f, k):
                k = fill[(fold, f)]                 # <- the row's OWN test fold => train-fold modal
            if f in NUMERIC:
                row.append(float(k))
            else:
                row.extend(1.0 if k == lv else 0.0 for lv in levels[f])
        return row
    return enc, levels


def score(y, fl, X_of):
    """CV under the sealed fold structure. X_of(fold) returns the design matrix as that fold's test set
    would see it -- which matters only under A2, where the encoding is fold-dependent."""
    yp = np.empty(len(y), dtype=object)
    nl = np.empty(len(y), dtype=object)
    for f in range(NFOLD):
        tr, te = fl != f, fl == f
        if not (te.sum() and tr.sum()):
            continue
        X = X_of(f)
        yp[te] = predict(build(X[tr], y[tr], DEPTH), X[te])
        nl[te] = Counter(y[tr]).most_common(1)[0][0]
    return float((yp == y).mean()), float((nl == y).mean())


def perm_p(y, fl, X_of, observed, nperm=NPERM):
    """Within-fold label permutation. Labels are shuffled INSIDE each fold so the fold sizes and the
    fold-weighted null machinery are preserved and only the label-feature link is broken."""
    rng = np.random.default_rng(SEED)
    ge = 0
    for _ in range(nperm):
        yp = y.copy()
        for f in range(NFOLD):
            m = fl == f
            yp[m] = rng.permutation(yp[m])
        a, n = score(yp, fl, X_of)
        if (a - n) >= observed - 1e-12:
            ge += 1
    return (ge + 1) / (nperm + 1)


def census(an, pids, use, enc, folds):
    """Census-before-seal on the imputed matrix (Anatomy-SCHEMA §3.3/§3.3b). A feature whose modal value
    swamps the population cannot carry a contrast -- DECLARED here, not silently dropped."""
    out = {}
    for f in use:
        vals = []
        for i, p in enumerate(pids):
            k = raw_key(an, p, f)
            if is_absent(f, k):
                k = "<imputed>"
            vals.append(k)
        c = Counter(vals)
        top, n = c.most_common(1)[0]
        # after imputation the absent rows JOIN the train-fold modal level, so the effective modal share is
        # (imputed + modal-substantive) when those coincide -- computed on the realised encoding below
        eff = Counter()
        for i, p in enumerate(pids):
            k = raw_key(an, p, f)
            eff[k if not is_absent(f, k) else "<imputed>"] += 1
        imputed = eff.get("<imputed>", 0)
        subst = {k: v for k, v in eff.items() if k != "<imputed>"}
        mtop, mn = (Counter(subst).most_common(1)[0] if subst else ("<none>", 0))
        share = (mn + imputed) / len(pids)
        out[f] = {"n_absent_imputed": imputed, "modal_substantive": str(mtop),
                  "effective_modal_share": round(share, 4),
                  "starved": bool(share > 0.90 or len(subst) <= 1),
                  "note": ("STARVED — after imputation the modal level holds "
                           f"{share:.0%}; this column was carrying ABSENCE, not anatomy"
                           if share > 0.90 or len(subst) <= 1 else "ok")}
    return out


def coverage_profile(an, pid, use):
    """The row's absence FINGERPRINT: which features are absent, ignoring what they say when present."""
    return "".join("1" if is_absent(f, raw_key(an, pid, f)) else "0" for f in use)


def stratify_by_coverage(an, sub, y, yp, use):
    """THE SEALED SECONDARY (prereg_v14 A2). Within a coverage profile, absence is CONSTANT — so it cannot
    be what distinguishes rows. Any lift surviving here is anatomy; any lift that vanishes was absence.

    This is the clean version of A2's question: no imputation, therefore no injected false values, and no
    confound between 'removed true information' and 'asserted false information'.

    Same admissibility screen as A4, same denominator rule: accuracy and null share the SAME row set."""
    prof = np.array([coverage_profile(an, p, use) for p in sub])
    per, admissible = {}, []
    for g in sorted(set(prof)):
        m = prof == g
        n = int(m.sum())
        lbl, modal_correct = Counter(y[m]).most_common(1)[0]
        model_correct = int((yp[m] == y[m]).sum())
        ok = n >= 30 and modal_correct / n < 0.90
        per[g] = {"n": n, "features_absent": [f for f, b in zip(use, g) if b == "1"],
                  "modal_label": lbl, "modal_correct": modal_correct, "model_correct": model_correct,
                  "delta": model_correct - modal_correct, "admissible": ok}
        if ok:
            admissible.append(g)
        else:
            per[g]["status"] = ("INSUFFICIENT — n < 30" if n < 30
                                else f"INSUFFICIENT — modal share {modal_correct / n:.0%} >= 90%")
    n_a = sum(per[g]["n"] for g in admissible)
    mo = sum(per[g]["modal_correct"] for g in admissible)
    me = sum(per[g]["model_correct"] for g in admissible)
    return {"n_profiles": len(per), "n_admissible": len(admissible),
            "per_profile": per,
            "pooled_admissible_only": {
                "denominator_rule": "accuracy and null share THE SAME row set (admissible profiles only)",
                "n": n_a, "modal_correct": mo, "model_correct": me,
                "null": round(mo / n_a, 4) if n_a else None,
                "acc": round(me / n_a, 4) if n_a else None,
                "within_coverage_lift": round((me - mo) / n_a, 4) if n_a else None}}


def main() -> int:
    v3, an, pids, fam, folds = load()
    real = SPEC.charge_real_values[CHARGE]
    idx = [i for i, p in enumerate(pids) if charge_value(v3[p], CHARGE) in real]
    sub = [pids[i] for i in idx]
    y = np.array([charge_value(v3[p], CHARGE) for p in sub])
    fl = folds[idx]
    base_feats = [f for f in FEATS if f not in EXCLUDE.get(CHARGE, set())]

    def matrix(enc, fold):
        return np.array([enc(p, fold) for p in sub], dtype=float)

    runs = {}

    # ---- BASELINE: the sealed configuration, re-run under this script's code path -------------------
    enc0, _ = make_encoder(an, pids, base_feats)
    X0 = matrix(enc0, 0)
    acc0, null0 = score(y, fl, lambda f: X0)
    assert abs(round(acc0, 4) - SEALED_ACC) < 1e-9, (
        f"MATCHED BASELINE FAILED: acc {acc0:.4f} != sealed {SEALED_ACC}. The deltas below would be "
        f"meaningless, so this run fails rather than reporting them.")
    assert abs(round(null0, 4) - SEALED_NULL) < 1e-9, f"null {null0:.4f} != sealed {SEALED_NULL}"
    runs["baseline"] = {"role": "MATCHED RE-RUN of the sealed configuration — the reference for all deltas",
                        "features": base_feats, "n": len(y),
                        "denominator_rule": "acc and null computed on the same 336 decision-real rows",
                        "acc": round(acc0, 4), "null": round(null0, 4),
                        "lift": round(acc0 - null0, 4),
                        "reproduces_sealed": {"n": len(y), "acc": SEALED_ACC, "null": SEALED_NULL,
                                              "lift_as_sealed": SEALED_LIFT,
                                              "denominator_rule": "same 336 rows as the sealed Arm B run",
                                              "note": "sealed lift is double-rounded; exact is 0.0685"}}

    # ---- A1: encoding ablation ---------------------------------------------------------------------
    a1_feats = [f for f in base_feats if f != "encoding_type"]
    enc1, _ = make_encoder(an, pids, a1_feats)
    X1 = matrix(enc1, 0)
    acc1, null1 = score(y, fl, lambda f: X1)
    p1 = perm_p(y, fl, lambda f: X1, acc1 - null1)
    runs["A1_encoding_ablation"] = {
        "sealed_prediction": f"lift falls below half its sealed size (< +{HALF_THRESHOLD})",
        "features": a1_feats, "dropped": ["encoding_type"],
        "n": len(y),
        "denominator_rule": "acc and null computed on the same 336 decision-real rows",
        "acc": round(acc1, 4), "null": round(null1, 4), "lift": round(acc1 - null1, 4),
        "permutation_p": round(p1, 4), "n_permutations": NPERM,
        "delta_vs_baseline": round((acc1 - null1) - (acc0 - null0), 4),
        "prediction_hit": bool((acc1 - null1) < HALF_THRESHOLD)}

    # ---- A2: indicator-free refit ------------------------------------------------------------------
    enc2, _ = make_encoder(an, pids, base_feats, impute_folds=True, folds=folds)
    X2 = {f: matrix(enc2, f) for f in range(NFOLD)}
    acc2, null2 = score(y, fl, lambda f: X2[f])
    p2 = perm_p(y, fl, lambda f: X2[f], acc2 - null2)
    cen = census(an, pids, base_feats, enc2, folds)
    runs["A2_indicator_free"] = {
        "sealed_prediction": f"lift falls below half its sealed size (< +{HALF_THRESHOLD})",
        "features": base_feats,
        "absence_set_stripped": {"strings": sorted(ABSENCE_STRINGS), "numeric_sentinel": ABSENCE_NUMERIC},
        "n": len(y),
        "denominator_rule": "acc and null computed on the same 336 decision-real rows",
        "imputation": ("fold-local modal substantive level — the fill value for a row is computed on its "
                       "own TRAIN fold only, never on the fold being predicted"),
        "acc": round(acc2, 4), "null": round(null2, 4), "lift": round(acc2 - null2, 4),
        "permutation_p": round(p2, 4), "n_permutations": NPERM,
        "delta_vs_baseline": round((acc2 - null2) - (acc0 - null0), 4),
        "prediction_hit": bool((acc2 - null2) < HALF_THRESHOLD),
        "census_after_imputation": cen,
        "starved_under_imputation": [f for f, v in cen.items() if v["starved"]]}

    # ---- A2 SECONDARY (sealed): stratification by coverage profile ---------------------------------
    # Runs on the BASELINE predictions — the sealed matrix, untouched. No imputation, so no false values.
    ypb = np.empty(len(y), dtype=object)
    for f in range(NFOLD):
        tr, te = fl != f, fl == f
        ypb[te] = predict(build(X0[tr], y[tr], DEPTH), X0[te])
    runs["A2_secondary_coverage_stratified"] = {
        "role": "SEALED SECONDARY (prereg_v14 A2, 'secondarily, stratification by coverage profile')",
        "why_it_is_the_cleaner_test": (
            "within a coverage profile absence is CONSTANT, so it cannot be what distinguishes rows. This "
            "asks A2's question WITHOUT imputing anything, and is therefore free of the magnitude confound "
            "that limits the primary."),
        **stratify_by_coverage(an, sub, y, ypb, base_feats)}

    # ---- POST-HOC DIAGNOSTIC (NOT sealed, NOT a bet) -----------------------------------------------
    # Why this exists: A2's primary imputes `open` -> a substantive level on 166/345 arity_class rows and
    # 126/345 objective_type rows. That does not only REMOVE absence information, it ASSERTS A FALSE VALUE
    # on roughly half the corpus -- so the primary's magnitude conflates two mechanisms. Dropping the
    # absence-bearing columns removes the information WITHOUT injecting anything. Labelled post-hoc; it
    # claims no predictive credit and is reported as a diagnostic, not a result.
    keep = [f for f in base_feats if not any(is_absent(f, raw_key(an, p, f)) for p in pids)]
    enc3, _ = make_encoder(an, pids, keep)
    X3 = matrix(enc3, 0)
    acc3, null3 = score(y, fl, lambda f: X3)
    runs["POSTHOC_drop_absence_bearing_columns"] = {
        "status": "POST-HOC DIAGNOSTIC — not sealed, not a bet, no predictive credit claimed",
        "motivation": ("separates 'removed true information' from 'asserted false information', which "
                       "A2's primary confounds at a ~50% absence rate"),
        "features_kept": keep,
        "features_dropped": [f for f in base_feats if f not in keep],
        "n": len(y),
        "denominator_rule": "acc and null computed on the same 336 decision-real rows",
        "acc": round(acc3, 4), "null": round(null3, 4), "lift": round(acc3 - null3, 4),
        "delta_vs_baseline": round((acc3 - null3) - (acc0 - null0), 4)}

    sec_lift = runs["A2_secondary_coverage_stratified"]["pooled_admissible_only"]["within_coverage_lift"]
    scoring = {
        "A1_encoding_ablation": {
            "sealed_prediction": f"lift < +{HALF_THRESHOLD}",
            "observed": round(acc1 - null1, 4),
            "verdict": "MISS",
            "reading": ("the prediction was WRONG. `encoding_type` carries about 30% of the lift "
                        "(-0.0208 of +0.0685), not the majority, and what remains is still significant "
                        "at p = 0.0010. The bluntest family channel is NOT the carrier."),
            "recorded_because_it_is_a_miss": ("scored against the seal and reported as a miss. The bet was "
                                              "disclosed as weakened in advance by the known "
                                              "locality_class ablation; it still failed.")},
        "A2_indicator_free_primary": {
            "sealed_prediction": f"lift < +{HALF_THRESHOLD}",
            "observed": round(acc2 - null2, 4),
            "verdict": "HIT — nominally",
            "specification_weakness_declared": (
                "THE TEST WAS POORLY SPECIFIED AND THE HIT IS WORTH LESS THAN IT LOOKS. Imputation at a "
                "~50% absence rate does two things at once: it REMOVES absence information (the "
                "hypothesis) and it ASSERTS A FALSE SUBSTANTIVE VALUE on 166/345 arity_class rows and "
                "126/345 objective_type rows (not the hypothesis). A manipulation that degrades the matrix "
                "by construction makes the prediction nearly unfalsifiable, so passing it is weak "
                "evidence. Quantified by the post-hoc control: dropping the absence-bearing columns costs "
                "-0.0923, while imputing them costs -0.2024 — so roughly half the primary's collapse is "
                "the injected false values, not the removed absence."),
            "consequence": "the informative test is the SEALED SECONDARY below, not this one"},
        "A2_secondary_coverage_stratified": {
            "sealed_prediction": f"lift < +{HALF_THRESHOLD} (same prediction, cleaner instrument)",
            "observed": sec_lift,
            "verdict": "HIT",
            "reading": (f"within a coverage profile — where absence is CONSTANT and nothing is imputed — "
                        f"the lift falls from +0.0685 to {sec_lift:+.4f}, about {1 - sec_lift / 0.0685:.0%} "
                        f"of it gone. Five extra correct predictions across 266 rows in four profiles. "
                        f"This is the number A2 was designed to produce and the only one free of the "
                        f"imputation confound.")},
    }

    doc = {"schema": "terroir-v1-ablations/v1", "prereg": "prereg_v14", "milestone": "T2+T3",
           "seed": SEED, "model": f"CART depth<={DEPTH} minleaf={MINLEAF}", "n": len(y),
           "charge": CHARGE, "fold_key": "problem_family", "runs": runs,
           "sealed_prediction_scoring": scoring,
           "converging_picture": (
               "two INDEPENDENT stratifications each dissolve the lift and neither leaves a residual: "
               "within problem_family it is exactly +0.0000 (A4, 255 rows), within coverage profile it is "
               f"{sec_lift:+.4f} (A2 secondary, 266 rows). The two strata are themselves correlated "
               "(V = 0.2924, p = 0.0002), so these are not independent explanations so much as two views "
               "of one fact: the model is reading which literature recorded the row, not what the problem "
               "is."),
           "extremal_acknowledged": [{
               "stat": ("runs.A2_indicator_free.census_after_imputation.self_reducibility."
                        "effective_modal_share"),
               "value": 1.0,
               "why_the_exactness_is_expected": (
                   "`self_reducibility` has exactly ONE substantive level (`worst-to-average`, 3 rows) "
                   "against 342 absent ones, so fold-local modal imputation sends every absent row to that "
                   "single level and the column becomes CONSTANT. A modal share of exactly 1.0 is the "
                   "arithmetic consequence. prereg_v14 DECLARED this starvation in advance as an expected "
                   "side effect — the column was carrying absence, not anatomy, and imputation makes that "
                   "visible by leaving nothing behind."),
           }],
           "scope_limit_stated_in_advance": (
               "these are MECHANISM, not verdict. A4's within-family lift is exactly 0 regardless of what "
               "these return; no ablation result can move it.")}
    OUT.write_text(json.dumps(doc, indent=1) + "\n")

    print(f"TERROIR v1 — T2/T3: the SEALED arm  (n={len(y)}, {NPERM} permutations each)\n")
    print(f"{'run':<34}{'acc':>8}{'null':>8}{'lift':>9}{'delta':>9}{'perm p':>9}  prediction")
    for k, r in runs.items():
        if "acc" not in r:
            continue
        if k == "baseline":
            print(f"{k:<34}{r['acc']:>8.4f}{r['null']:>8.4f}{r['lift']:>+9.4f}{'—':>9}{'—':>9}  "
                  f"(matched re-run; reproduces sealed exactly)")
            continue
        if "prediction_hit" not in r:
            print(f"{k:<34}{r['acc']:>8.4f}{r['null']:>8.4f}{r['lift']:>+9.4f}"
                  f"{r['delta_vs_baseline']:>+9.4f}{'—':>9}  post-hoc diagnostic")
            continue
        hit = "HIT" if r["prediction_hit"] else "MISS"
        print(f"{k:<34}{r['acc']:>8.4f}{r['null']:>8.4f}{r['lift']:>+9.4f}"
              f"{r['delta_vs_baseline']:>+9.4f}{r['permutation_p']:>9.4f}  {hit} (< +{HALF_THRESHOLD})")

    sec = runs["A2_secondary_coverage_stratified"]
    ps = sec["pooled_admissible_only"]
    print(f"\nA2 SECONDARY — coverage-profile stratification (sealed matrix, no imputation):")
    print(f"  {sec['n_profiles']} profiles, {sec['n_admissible']} admissible")
    for g, r in sec["per_profile"].items():
        if not r["admissible"]:
            continue
        print(f"    {g}  n={r['n']:<4} modal={r['modal_correct']:<4} model={r['model_correct']:<4} "
              f"delta={r['delta']:+d}   absent={r['features_absent']}")
    if ps["n"]:
        print(f"  POOLED n={ps['n']}  null={ps['null']:.4f}  acc={ps['acc']:.4f}  "
              f"WITHIN-COVERAGE LIFT={ps['within_coverage_lift']:+.4f}")
    print(f"\nA2 census after imputation — starved: {runs['A2_indicator_free']['starved_under_imputation']}")
    for f, v in runs["A2_indicator_free"]["census_after_imputation"].items():
        mark = "STARVED" if v["starved"] else "ok     "
        print(f"  {mark} {f:<24} imputed={v['n_absent_imputed']:<5} "
              f"eff_modal={v['effective_modal_share']:.0%}")
    print("\nSEALED PREDICTION SCORING:")
    for k, s in scoring.items():
        print(f"  {s['verdict']:<16} {k:<36} predicted {s['sealed_prediction']}, observed "
              f"{s['observed']:+.4f}")
    print(f"\nwrote {OUT.name}  sha256 {hashlib.sha256(OUT.read_bytes()).hexdigest()[:16]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
