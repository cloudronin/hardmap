#!/usr/bin/env python3
"""Terroir v1 T1 — A4: the within-family residual, and the A3 retirement record.

WHAT THIS IS. Mosaic v3 Arm B scored `decision` at +0.0684 over its fold-weighted null (p = 0.0033) and
could not separate two readings: a weak anatomy->fate bridge, or family-level regularity riding the feature
matrix. A4 decomposes that lift. It is ARITHMETIC ON FROZEN PREDICTIONS -- nothing is refit here, and the
sealed prediction file's sha256 is ASSERTED before a single number is computed.

WHY THE FOLD STRUCTURE MAKES THIS SHARP, stated because it is the load-bearing fact:
  Arm B's fold key IS `problem_family`, so every family sits ENTIRELY INSIDE ONE FOLD. The model NEVER
  trains on a family it predicts. It cannot memorise "graph -> NPC"; it must INFER a family's base rate
  from anatomy features alone. So A4 is not asking the easy question ("did the model learn family labels?")
  -- it is asking the hardest one: having inferred the base rate, did the model add ANYTHING on top of it?

DISCLOSURE (prereg_v14): this analysis was COMPUTED AT GROUNDING, BEFORE the seal. It carries no predictive
credit and is recorded as a DISCLOSED FINDING. A1/A2 are the sealed arm.

DENOMINATOR DISCIPLINE: the pooled statistic uses THE SAME ROW SET for accuracy and for null -- admissible
families only. An earlier pass mixed an admissible-only null with an all-rows accuracy and got +0.0060
where the matched statistic is exactly 0. That class of error is now a `hardmap verify` gate.
"""
import hashlib
import json
import sys
from collections import Counter
from math import comb
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "dev"))
from eightfold import atlas as A                                     # noqa: E402
import quarry_v3_spec as V3                                          # noqa: E402

AT = ROOT / "eightfold" / "results" / "atlas"
OUT = AT / "terroir_v1_results.json"
SPEC = V3.V3_SPEC
SEED, NFOLD, CHARGE = 20260725, 5, "decision"

# prereg_v14 anchors — asserted, not trusted
SEALED_PRED_SHA = "cc5bb3895a44a043"
SEALED_LIFT, SEALED_ACC, SEALED_NULL = 0.0684, 0.6607, 0.5923

# prereg_v14 admissibility screen. NOT a new choice: n>=30 is the binomial power floor A4 already invokes,
# modal<0.90 is the census-before-seal starvation line sealed at Anatomy-SCHEMA §3.3/§3.3b.
MIN_N, MAX_MODAL = 30, 0.90


def load():
    """Reconstruct Arm B's fit population deterministically. Same sort, same filter, same fold hash."""
    v3 = {e.problem_id: e for e in A.load_atlas(str(AT / "atlas_v3.jsonl"))}
    an = set()
    for line in (AT / "anatomy_v1.jsonl").read_text().splitlines():
        if line.strip():
            r = json.loads(line)
            if r["universe"] == "natural":
                an.add(r["problem_id"])
    pids = sorted(p for p in v3 if p in an)
    fam = {p: v3[p].problem_family for p in pids}
    ufam = sorted(set(fam.values()))
    order = sorted(ufam, key=lambda g: hashlib.sha256((g + str(SEED)).encode()).hexdigest())
    ffold = {g: i % NFOLD for i, g in enumerate(order)}
    folds = np.array([ffold[fam[p]] for p in pids])
    return v3, pids, fam, folds


def charge_value(entry, ch):
    for c in entry.charges:
        if c.charge == ch:
            return c.value
    return "n.a."


def exact_binomial_two_sided(k, n, p):
    """P(as-or-more-extreme than k successes) under Binomial(n, p). Used INSTEAD of a normal approximation
    because the admissible families are small enough (49-148) for the tails to matter."""
    probs = [comb(n, j) * p ** j * (1 - p) ** (n - j) for j in range(n + 1)]
    return float(min(1.0, sum(q for q in probs if q <= probs[k] + 1e-15)))


def a4(v3, pids, fam, folds):
    real = SPEC.charge_real_values[CHARGE]
    idx = [i for i, p in enumerate(pids) if charge_value(v3[p], CHARGE) in real]
    y = np.array([charge_value(v3[pids[i]], CHARGE) for i in idx])
    fl = folds[idx]
    fams = np.array([fam[pids[i]] for i in idx])

    pred_doc = json.loads((AT / "grid_arm_b_predictions.json").read_text())
    sha = hashlib.sha256((AT / "grid_arm_b_predictions.json").read_bytes()).hexdigest()[:16]
    assert sha == SEALED_PRED_SHA, f"SEAL BROKEN: predictions sha {sha} != {SEALED_PRED_SHA}"
    yp = np.array(pred_doc["predictions"][f"{CHARGE}:with_locality"])
    assert len(yp) == len(y), f"population drift: {len(yp)} predictions vs {len(y)} reconstructed rows"

    # the fold structure claim, ASSERTED rather than asserted-in-prose
    family_in_one_fold = all(len(set(fl[fams == g])) == 1 for g in set(fams))
    assert family_in_one_fold, "fold key is not problem_family — A4's warrant does not hold"

    # global fold-weighted null, recomputed to confirm we reproduce the sealed number
    gn = np.empty(len(y), dtype=object)
    for f in range(NFOLD):
        tr, te = fl != f, fl == f
        if te.sum() and tr.sum():
            gn[te] = Counter(y[tr]).most_common(1)[0][0]
    acc, null = float((yp == y).mean()), float((gn == y).mean())
    assert abs(round(acc, 4) - SEALED_ACC) < 1e-9, f"acc drift {acc} vs sealed {SEALED_ACC}"
    assert abs(round(null, 4) - SEALED_NULL) < 1e-9, f"null drift {null} vs sealed {SEALED_NULL}"

    per_family, admissible = {}, []
    for g in sorted(set(fams)):
        m = fams == g
        n = int(m.sum())
        lbl, modal_correct = Counter(y[m]).most_common(1)[0]
        model_correct = int((yp[m] == y[m]).sum())
        ok = n >= MIN_N and modal_correct / n < MAX_MODAL
        rec = {"n": n, "modal_label": lbl, "modal_correct": modal_correct,
               "modal_share": round(modal_correct / n, 4), "model_correct": model_correct,
               "delta": model_correct - modal_correct, "admissible": ok}
        if ok:
            rec["exact_binomial_p"] = round(
                exact_binomial_two_sided(model_correct, n, modal_correct / n), 4)
            admissible.append(g)
        else:
            rec["status"] = ("INSUFFICIENT — n < 30" if n < MIN_N
                             else f"INSUFFICIENT — modal share {modal_correct / n:.0%} >= 90%")
        per_family[g] = rec

    # POOLED: same row set for accuracy and null. This is the denominator rule made mechanical.
    n_adm = sum(per_family[g]["n"] for g in admissible)
    modal_adm = sum(per_family[g]["modal_correct"] for g in admissible)
    model_adm = sum(per_family[g]["model_correct"] for g in admissible)
    within_lift = (model_adm - modal_adm) / n_adm

    return {
        "status": "DISCLOSED — computed at grounding 2026-07-25, before prereg_v14 was sealed",
        "charge": CHARGE,
        "predictions_sha256_asserted": sha,
        "fold_key_warrant": ("problem_family — VERIFIED: every family sits entirely inside one fold, so "
                             "the model never trains on a family it predicts and must INFER that family's "
                             "base rate from anatomy features alone"),
        "headline_being_decomposed": {
            "n": len(y), "acc": round(acc, 4), "global_fold_weighted_null": round(null, 4),
            "lift_exact": round(acc - null, 4),
            "lift_as_sealed": SEALED_LIFT,
            "rounding_erratum": (
                f"the sealed artifact records {SEALED_LIFT}; the exact difference is 23/336 = 0.068452, "
                f"which rounds to {round(acc - null, 4)}. grid_arm_b.py computed the lift from the "
                f"ALREADY-ROUNDED accuracy (round(0.6607 - 0.5922619, 4) = 0.0684) rather than from the "
                f"exact values. A 0.0001 double-rounding artifact with no bearing on any verdict. Recorded "
                f"rather than silently reconciled; THE SEALED NUMBER IS NOT CHANGED. Terroir quotes the "
                f"sealed 0.0684 when referring to the Mosaic v3 result and the exact 0.0685 when doing "
                f"its own arithmetic, and says which is which."),
        },
        "screen": {"rule": f"n >= {MIN_N} AND modal_share < {MAX_MODAL}",
                   "admissible": admissible, "n_admissible_families": len(admissible),
                   "n_insufficient_families": len(per_family) - len(admissible)},
        "per_family": per_family,
        "pooled_admissible_only": {
            "denominator_rule": "accuracy and null share THE SAME ROW SET (admissible families only)",
            "n": n_adm, "modal_correct": modal_adm, "model_correct": model_adm,
            "null": round(modal_adm / n_adm, 4), "acc": round(model_adm / n_adm, 4),
            "within_family_lift": round(within_lift, 4)},
        "attribution": {
            "headline_lift": round(acc - null, 4),
            "within_family_lift": round(within_lift, 4),
            "share_of_lift_from_family_composition": round(1 - within_lift / (acc - null), 4),
            "reading": ("family composition accounts for the ENTIRE scored lift. Within admissible "
                        "families the model recovers exactly nothing.")},
        "sharpest_edge": {
            "family": "logic-proof",
            "finding": ("SIGNIFICANTLY WORSE than its own modal (10/49 vs 17/49, exact binomial "
                        "p = 0.0359). On the one admissible family with a genuinely spread label, the "
                        "model imports a cross-family rule that is ACTIVELY WRONG."),
            "why_it_matters": ("this is ANTI-SIGNAL, not absence of signal, and it is the strongest single "
                               "FAMILY-BORNE exhibit: a model with real anatomy signal would not degrade "
                               "below the base rate on the family where the label actually varies.")},
        "verdict": "FAMILY-BORNE",
    }


def a3_retirement(v3, pids, fam, folds):
    """A3 is RETIRED. This is not the analysis — it is the RECORD of why it cannot run, computed once and
    frozen so the retirement is auditable rather than asserted."""
    soc = {}
    for line in (AT / "atlas_v3_provenance.jsonl").read_text().splitlines():
        if line.strip():
            r = json.loads(line)
            soc[r["problem_id"]] = r
    real = SPEC.charge_real_values[CHARGE]
    fit = [p for p in pids if charge_value(v3[p], CHARGE) in real]
    fitsoc = [p for p in fit if p in soc]

    fl = np.array([folds[pids.index(p)] for p in fitsoc])
    y = np.array([charge_value(v3[p], CHARGE) for p in fitsoc])
    wave = np.array([soc[p]["admission_wave"] for p in fitsoc])

    # admission_wave ALONE, under Arm B's own fold structure and null convention
    yp, nl = np.empty(len(y), dtype=object), np.empty(len(y), dtype=object)
    for f in range(NFOLD):
        tr, te = fl != f, fl == f
        if not (te.sum() and tr.sum()):
            continue
        lut = {w: Counter(y[tr][wave[tr] == w]).most_common(1)[0][0] for w in set(wave[tr])}
        glob = Counter(y[tr]).most_common(1)[0][0]
        yp[te] = [lut.get(w, glob) for w in wave[te]]
        nl[te] = glob
    acc, null = float((yp == y).mean()), float((nl == y).mean())

    xt = {}
    for w in sorted(set(wave)):
        c = Counter(y[wave == w])
        lbl, k = c.most_common(1)[0]
        xt[w] = {"n": int((wave == w).sum()), "modal_label": lbl, "modal_correct": k,
                 "purity": round(k / int((wave == w).sum()), 4), "breakdown": dict(c.most_common())}

    rn = [p for p in fitsoc if str(soc[p].get("rn_membership")) == "present"]
    return {
        "status": "RETIRED — DISQUALIFIED at grounding, before prereg_v14 was sealed",
        "reason_1_different_population": {
            "sociology_coverage": f"{len(soc)} of 345 natural rows (v3-new only; the 118 legacy v2 rows "
                                  f"carry no provenance record)",
            "decision_fit_n": len(fit),
            "decision_fit_intersect_sociology_n": len(fitsoc),
            "note": ("the nested increment would be computed on 225 rows against a 0.5644 null and then "
                     "compared to a 336-row statistic against a 0.5923 null. Not commensurable.")},
        "reason_2_THE_DISQUALIFIER": {
            "mechanism": ("the atlas was expanded in CHARGE-STRATIFIED WAVES, so admission bookkeeping "
                          "ENCODES THE CHARGE"),
            "admission_wave_x_decision": xt,
            "admission_wave_alone": {"n": len(fitsoc),
                                     "denominator_rule": ("acc and null computed on the same 225 rows — "
                                                          "the decision-fit INTERSECT sociology "
                                                          "population, which is NOT the 336-row "
                                                          "population the headline lives on"),
                                     "acc": round(acc, 4), "fold_weighted_null": round(null, 4),
                                     "lift": round(acc - null, 4)},
            "reading": ("a +0.31 'sociology lift' that is PURE RECRUITMENT ARTIFACT. Published, it would "
                        "have looked like the most decisive result in the program.")},
        "reason_3_already_forbidden": {
            "Anatomy-SCHEMA §3.4": "a sociology column never enters a structural claim",
            "provenance_note": ("permits stratification on rn_membership; does NOT permit it on "
                                "source_funnel"),
            "rn_membership_is_degenerate": {
                "present": len(rn),
                "labels": dict(Counter(charge_value(v3[p], CHARGE) for p in rn)),
                "lift": 0.0,
                "note": ("the one blessed field is uniform on the global modal label, so stratifying on it "
                         "is arithmetically identical to not stratifying")},
            "quarry_member_is_constant": "True on all 225 fit-sociology rows — carries no information"},
        "the_finding_that_replaces_it": (
            "ANY COVARIATE CORRELATED WITH HOW THE CORPUS WAS BUILT IS A LABEL PROXY TO THE EXACT DEGREE "
            "THE BUILDING WAS OUTCOME-STRATIFIED. This binds every future use of provenance fields on "
            "every wave-built artifact, and it is the recruitment-design sibling of the theorem-forced-"
            "credit trap: the study's construction, not the world, guaranteeing the answer."),
        "quarantine_law_vindicated": (
            "the two rules that blocked this were written before anyone could have anticipated this "
            "specific regression. A rule that only forbids what its author foresaw is a preference; a rule "
            "that blocks a case its author never imagined is a law."),
    }


def main() -> int:
    v3, pids, fam, folds = load()
    res_a4 = a4(v3, pids, fam, folds)
    res_a3 = a3_retirement(v3, pids, fam, folds)

    pool = res_a4["pooled_admissible_only"]
    doc = {
        "schema": "terroir-v1-results/v1",
        "prereg": "prereg_v14",
        "milestone": "T1",
        "A4_within_family_residual": res_a4,
        "A3_retirement_record": res_a3,
        # THE TIDY-NUMBER GATE, discharged rather than waived. check_suspicious_cleanliness() flags any
        # headline exactly equal to its own null; the exactness here has a COMPLETE INTEGER EXPLANATION
        # and that arithmetic is the discharge.
        "extremal_acknowledged": [{
            "stat": "A4_within_family_residual.pooled_admissible_only.within_family_lift",
            "value": pool["within_family_lift"],
            "why_the_exactness_is_expected": (
                f"not a coincidence of rounding — an exact integer identity. Across the three admissible "
                f"families the model gets {pool['model_correct']} of {pool['n']} right and the "
                f"within-family modal baseline gets {pool['modal_correct']} of {pool['n']}: "
                f"graph +6, logic-proof -7, optimization +1, summing to 0. The statistic is a difference "
                f"of two small integers that happen to be equal, and each term is printed above so the "
                f"identity can be checked by hand."),
            "direction_note": ("flagged and discharged in the UNFLATTERING direction: this exactness makes "
                               "the result MORE decisive against the anatomy claim, and a gate that only "
                               "interrogates flattering numbers is indistinguishable from optimism."),
        }, {
            "stat": "A4_within_family_residual.attribution.share_of_lift_from_family_composition",
            "value": res_a4["attribution"]["share_of_lift_from_family_composition"],
            "why_the_exactness_is_expected": (
                "exactly 1.0 is FORCED BY the entry above, not independently remarkable: the share is "
                "1 - (within_family_lift / headline_lift), and the numerator is exactly 0. One extremal "
                "fact, reported twice — acknowledged separately so the gate is not satisfied by silence."),
        }, {
            "stat": "A4_within_family_residual.attribution.within_family_lift",
            "value": 0.0,
            "why_the_exactness_is_expected": (
                "the same statistic as the pooled entry above, restated in the attribution block. Flagged "
                "separately by design — the gate matches on path, so one number reported at two paths owes "
                "two acknowledgements rather than one."),
        }, {
            "stat": "A4_within_family_residual.per_family.lattice.modal_share",
            "value": 1.0,
            "why_the_exactness_is_expected": (
                "the `lattice` family has n=2 and both rows carry NPC, so its in-sample modal share is "
                "1.0 by arithmetic. This is WHY the family is declared INSUFFICIENT rather than scored — "
                "the modal<0.90 screen exists to catch exactly this. Same for `matrix` (n=4, all P)."),
        }, {
            "stat": "A4_within_family_residual.per_family.matrix.modal_share",
            "value": 1.0,
            "why_the_exactness_is_expected": "n=4, all P — see the `lattice` entry above",
        }, {
            "stat": "A3_retirement_record.reason_2_THE_DISQUALIFIER.admission_wave_x_decision.W3.purity",
            "value": 1.0,
            "why_the_exactness_is_expected": (
                "THIS EXACTNESS IS THE FINDING, not an artifact to explain away. Wave W3 is 123/123 NPC "
                "and W4 is 10/10 P because the atlas was expanded in CHARGE-STRATIFIED waves. A purity of "
                "exactly 1.0 is what a recruitment label proxy looks like, and it is why A3 is retired."),
        }, {
            "stat": "A3_retirement_record.reason_2_THE_DISQUALIFIER.admission_wave_x_decision.W4.purity",
            "value": 1.0,
            "why_the_exactness_is_expected": "10/10 P — see the W3 entry above",
        }, {
            "stat": "A3_retirement_record.reason_3_already_forbidden.rn_membership_is_degenerate.lift",
            "value": 0.0,
            "why_the_exactness_is_expected": (
                "rn_membership is `present` on 16 rows and ALL 16 carry the global modal label (NPC), so "
                "the within-stratum modal and the global modal are the same label on every row. "
                "Stratifying on it is arithmetically identical to not stratifying — the zero is a "
                "degeneracy of the covariate, not a measured null."),
        }],
    }
    OUT.write_text(json.dumps(doc, indent=1) + "\n")

    print("TERROIR v1 — T1: A4 within-family residual  (DISCLOSED, arithmetic on frozen predictions)")
    print(f"seal asserted: predictions sha {res_a4['predictions_sha256_asserted']}\n")
    h = res_a4["headline_being_decomposed"]
    print(f"decomposing: n={h['n']}  acc={h['acc']:.4f}  global null={h['global_fold_weighted_null']:.4f}"
          f"  lift={h['lift_exact']:+.4f} (sealed as {h['lift_as_sealed']}, double-rounded)\n")
    print(f"{'family':<18}{'n':>5}{'modal':>8}{'model':>8}{'delta':>8}{'p':>9}  screen")
    for g, r in res_a4["per_family"].items():
        p = f"{r['exact_binomial_p']:.4f}" if r["admissible"] else "—"
        mark = "ADMISSIBLE" if r["admissible"] else r["status"]
        print(f"{g:<18}{r['n']:>5}{r['modal_correct']:>8}{r['model_correct']:>8}{r['delta']:>+8}{p:>9}  {mark}")
    print(f"\n{'POOLED (admissible)':<18}{pool['n']:>5}{pool['modal_correct']:>8}"
          f"{pool['model_correct']:>8}{pool['model_correct'] - pool['modal_correct']:>+8}")
    print(f"\n  within-family null = {pool['null']:.4f}   acc = {pool['acc']:.4f}   "
          f"WITHIN-FAMILY LIFT = {pool['within_family_lift']:+.4f}")
    print(f"  headline lift      = {h['lift_exact']:+.4f}")
    print(f"  share of lift from family composition = "
          f"{res_a4['attribution']['share_of_lift_from_family_composition']:.1%}")
    print(f"\n  VERDICT: {res_a4['verdict']}")
    print(f"\nA3 RETIRED — admission_wave alone: "
          f"acc={res_a3['reason_2_THE_DISQUALIFIER']['admission_wave_alone']['acc']:.4f} "
          f"null={res_a3['reason_2_THE_DISQUALIFIER']['admission_wave_alone']['fold_weighted_null']:.4f} "
          f"lift={res_a3['reason_2_THE_DISQUALIFIER']['admission_wave_alone']['lift']:+.4f}  (artifact)")
    print(f"\nwrote {OUT.name}  sha256 {hashlib.sha256(OUT.read_bytes()).hexdigest()[:16]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
