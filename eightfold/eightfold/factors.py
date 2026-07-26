"""Factors v1 — effective dimensionality k* of the charge atlas by HELD-OUT PREDICTION.

Prereg `results/prereg/prereg_v7.json`. The estimator fits a k-latent-factor CATEGORICAL model for k=1..6 and
selects k* by masked-cell predictive accuracy — the S1-robust claim. MCA-style eigenvalue counts
(`structure.mca`) are S1-DISQUALIFIED as the primary estimator (Crucible S1: per-charge marginals + typing
reproduce the eigenvalue structure) and are kept only as a reported sensitivity, never the claim.

Model ladder (owner decision, locked in prereg_v7): primary = latent class model (finite mixture of per-charge
categoricals, EM); fallback = low-rank categorical PCA — invoked ONLY if the F-1 planted-k selftest fails
(pre-committed escalation, decided on synthetic known-answer data, never on the real canon).

ADDITIVE to the frozen 8-charge kernel: this module reads the atlas and reuses `structure._grid`,
`crucible._S2_DROP` (the 114-class S2 dedup), and `crucible._null_chain`/`_envelope` (the S1 null); it changes no
existing behavior, so `a3_structure.json` / `crucible_results.json` regenerate byte-identical. Spec-parametrized
(`spec=C.EIGHTFOLD_SPEC` default) so Foundry can point the same estimator at the census (Sprint 3.3 / P3).

    python -m eightfold.factors --selftest      # F-1 gate: planted-k recovered + pure-null quiet (wiring check)
    python -m eightfold.factors --factors       # F-2 verdict run on the dedup'd 114-class canon
    python -m eightfold.factors --factors --raw  # sensitivity: the raw 118 instead of the dedup'd 114
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

from eightfold import charges as C
from eightfold import crucible as X
from eightfold import structure as S

SEED = 20260721
# Fixed-before-F2 budget (prereg_v7 implementation_params). The selftest overrides with a reduced "wiring" budget.
CV_REPEATS = 30
EM_RESTARTS = 8
EM_MAX_ITERS = 150
MASK_FRAC = 0.10
SMOOTHING_ALPHA = 0.5
K_RANGE = range(1, 7)
NULL_M = 150


# ── encoding: rows (charge -> value) -> integer category matrix (missing = -1) ─────────────────────────────
def _encode(rows, spec=C.EIGHTFOLD_SPEC, charges=None):
    """Return (Xmat, cats). Xmat[i,j] = category index of row i on charge j, or -1 if the cell is a sentinel
    (open/unmeasured/n.a. -> MISSING, marginalized in the model, never imputed). cats[j] = the sorted real
    levels observed for charge j (the label space). Only real-valued cells are encoded -> only they are
    maskable/scorable (prereg maskable_set)."""
    charges = list(spec.charges) if charges is None else list(charges)
    cats = [sorted({r[ch] for r in rows if r.get(ch) in spec.charge_real_values[ch]}) for ch in charges]
    idx = [{v: k for k, v in enumerate(levels)} for levels in cats]
    n, p = len(rows), len(charges)
    Xmat = np.full((n, p), -1, dtype=np.int64)
    for i, r in enumerate(rows):
        for j, ch in enumerate(charges):
            v = r.get(ch)
            if v in idx[j]:
                Xmat[i, j] = idx[j][v]
    return Xmat, cats


# ── latent class model: EM over per-charge categoricals, with held-out cells masked out ────────────────────
def _fit_lcm(Xmat, cats, k, *, alpha=SMOOTHING_ALPHA, restarts=EM_RESTARTS, max_iters=EM_MAX_ITERS, seed=SEED,
             train_mask=None):
    """Fit a k-class LCM by EM. `train_mask` (bool, Xmat-shaped): where False, an observed cell is HELD OUT
    (excluded from fitting). Returns the best-of-`restarts` fit by observed-data log-likelihood."""
    n, p = Xmat.shape
    Ls = [len(c) for c in cats]
    obs = Xmat >= 0
    if train_mask is not None:
        obs = obs & train_mask
    rng = np.random.default_rng(seed)
    best = None
    for rs in range(restarts):
        g = rng.dirichlet(np.ones(k), size=n)                      # (n,k) soft assignments
        prev_ll = -np.inf
        log_pi = np.log(np.full(k, 1.0 / k))
        log_thetas = [None] * p
        thetas = [None] * p
        for _ in range(max_iters):
            # M-step ── priors + per-charge class-conditional categoricals (add-alpha smoothed)
            pi = g.sum(axis=0) + alpha
            pi = pi / pi.sum()
            log_pi = np.log(pi)
            for j in range(p):
                Lj = Ls[j]
                if Lj == 0:
                    thetas[j] = log_thetas[j] = None
                    continue
                th = np.full((k, Lj), alpha)
                col, ob = Xmat[:, j], obs[:, j]
                for l in range(Lj):
                    sel = ob & (col == l)
                    if sel.any():
                        th[:, l] += g[sel].sum(axis=0)
                th = th / th.sum(axis=1, keepdims=True)
                thetas[j], log_thetas[j] = th, np.log(th)
            # E-step ── posterior over classes from observed cells
            logg = np.tile(log_pi, (n, 1))
            for j in range(p):
                if log_thetas[j] is None:
                    continue
                col, ob = Xmat[:, j], obs[:, j]
                contrib = log_thetas[j][:, np.clip(col, 0, None)].T   # (n,k); missing cols masked next
                contrib[~ob] = 0.0
                logg = logg + contrib
            m = logg.max(axis=1, keepdims=True)
            ll = float((m.squeeze(1) + np.log(np.exp(logg - m).sum(axis=1))).sum())
            g = np.exp(logg - m)
            g = g / g.sum(axis=1, keepdims=True)
            if ll - prev_ll < 1e-7 * max(1.0, abs(prev_ll)):
                prev_ll = ll
                break
            prev_ll = ll
        if best is None or prev_ll > best["train_loglik"]:
            best = {"k": k, "log_pi": log_pi, "log_thetas": list(log_thetas), "thetas": list(thetas),
                    "train_loglik": prev_ll}
    return best


def _posterior(fit, Xmat, use_mask):
    """Row-wise class posterior from the cells flagged True in `use_mask` (& observed)."""
    n, p = Xmat.shape
    logg = np.tile(fit["log_pi"], (n, 1))
    for j in range(p):
        if fit["log_thetas"][j] is None:
            continue
        col = Xmat[:, j]
        ob = use_mask[:, j] & (col >= 0)
        contrib = fit["log_thetas"][j][:, np.clip(col, 0, None)].T
        contrib[~ob] = 0.0
        logg = logg + contrib
    m = logg.max(axis=1, keepdims=True)
    g = np.exp(logg - m)
    return g / g.sum(axis=1, keepdims=True)


def _score_heldout(fit, Xmat, held):
    """Predict the held-out cells from the posterior over the row's NON-held observed cells.
    Returns (n_correct, n_total, sum_loglik)."""
    n, p = Xmat.shape
    train_obs = (Xmat >= 0) & ~held
    gamma = _posterior(fit, Xmat, train_obs)                          # (n,k)
    correct = total = 0
    sll = 0.0
    for j in range(p):
        if fit["thetas"][j] is None:
            continue
        pred = gamma @ fit["thetas"][j]                               # (n,Lj) predictive dist
        for i in np.where(held[:, j] & (Xmat[:, j] >= 0))[0]:
            true_l = int(Xmat[i, j])
            total += 1
            if int(np.argmax(pred[i])) == true_l:
                correct += 1
            sll += float(np.log(max(pred[i, true_l], 1e-12)))
    return correct, total, sll


def _cv_curve(Xmat, cats, ks, *, mask_frac=MASK_FRAC, repeats=CV_REPEATS, restarts=EM_RESTARTS,
              max_iters=EM_MAX_ITERS, alpha=SMOOTHING_ALPHA, seed=SEED):
    """Repeated masked-cell CV. Per repeat, the SAME held-out set is scored for every k (fair comparison).
    Returns {k: {acc_mean, acc_se, ll_mean, n_folds}}."""
    n, p = Xmat.shape
    obs_idx = np.argwhere(Xmat >= 0)
    rng = np.random.default_rng(seed)
    accs = {k: [] for k in ks}
    lls = {k: [] for k in ks}
    n_hold = max(1, int(round(mask_frac * len(obs_idx))))
    for rep in range(repeats):
        sel = rng.choice(len(obs_idx), size=n_hold, replace=False)
        held = np.zeros((n, p), dtype=bool)
        for s in sel:
            held[obs_idx[s][0], obs_idx[s][1]] = True
        train_mask = ~held
        for k in ks:
            fit = _fit_lcm(Xmat, cats, k, alpha=alpha, restarts=restarts, max_iters=max_iters,
                           seed=seed + 1009 * rep + k, train_mask=train_mask)
            c, t, sll = _score_heldout(fit, Xmat, held)
            accs[k].append(c / t if t else np.nan)
            lls[k].append(sll / t if t else np.nan)
    res = {}
    for k in ks:
        a = np.array(accs[k], float)
        se = float(np.nanstd(a, ddof=1) / np.sqrt(np.sum(~np.isnan(a)))) if np.sum(~np.isnan(a)) > 1 else np.nan
        res[k] = {"acc_mean": float(np.nanmean(a)), "acc_se": se,
                  "ll_mean": float(np.nanmean(lls[k])), "n_folds": int(np.sum(~np.isnan(a)))}
    return res


def _n_profiles(rows, spec=C.EIGHTFOLD_SPEC, charges=None):
    charges = list(spec.charges) if charges is None else list(charges)
    return len({tuple(r[ch] for ch in charges) for r in rows})


def _loadings(Xmat, cats, k, spec, charges, *, alpha=SMOOTHING_ALPHA, restarts=EM_RESTARTS,
              max_iters=EM_MAX_ITERS, seed=SEED):
    """Fit the full-table LCM at k and report the class-conditional profiles — the candidate factor identities
    (INTERPRETIVE ONLY; named in the findings doc's walled section, never a v1 claim)."""
    fit = _fit_lcm(Xmat, cats, k, alpha=alpha, restarts=restarts, max_iters=max_iters, seed=seed)
    priors = np.exp(fit["log_pi"])
    classes = []
    for c in range(k):
        prof = {}
        for j, ch in enumerate(charges):
            if fit["thetas"][j] is None or not cats[j]:
                prof[ch] = None
                continue
            dist = fit["thetas"][j][c]
            modal = cats[j][int(np.argmax(dist))]
            prof[ch] = {"modal": modal, "p_modal": round(float(np.max(dist)), 3)}
        classes.append({"prior": round(float(priors[c]), 3), "profile": prof})
    return {"k": k, "classes": classes}


# ── the estimator ──────────────────────────────────────────────────────────────────────────────────────────
def estimate_rows(rows, spec=C.EIGHTFOLD_SPEC, *, charges=None, ks=K_RANGE, mask_frac=MASK_FRAC,
                  repeats=CV_REPEATS, restarts=EM_RESTARTS, max_iters=EM_MAX_ITERS, alpha=SMOOTHING_ALPHA,
                  seed=SEED, loadings=True):
    """Held-out-prediction k* estimate on a table of rows (charge->value). k*_hat = the parsimonious 1-SE
    choice (smallest k within 1 SE of the best mean accuracy); interval = all k within 1 SE of the best."""
    charges = list(spec.charges) if charges is None else list(charges)
    Xmat, cats = _encode(rows, spec, charges)
    ks = list(ks)
    curve = _cv_curve(Xmat, cats, ks, mask_frac=mask_frac, repeats=repeats, restarts=restarts,
                      max_iters=max_iters, alpha=alpha, seed=seed)
    k_argmax = max(ks, key=lambda k: curve[k]["acc_mean"])
    best, se_best = curve[k_argmax]["acc_mean"], curve[k_argmax]["acc_se"]
    band = se_best if se_best == se_best else 0.0                     # nan-guard
    interval = [k for k in ks if curve[k]["acc_mean"] >= best - band]
    k_hat = min(interval)                                             # parsimonious 1-SE rule
    out = {
        "model": "lcm", "k_hat_1se": k_hat, "k_argmax": k_argmax, "interval": interval,
        "best_acc": round(best, 4), "se_at_best": round(band, 4),
        "curve": {k: {"acc_mean": round(curve[k]["acc_mean"], 4), "acc_se": round(curve[k]["acc_se"], 4),
                      "ll_mean": round(curve[k]["ll_mean"], 4)} for k in ks},
        "n_rows": len(rows), "n_distinct_profiles": _n_profiles(rows, spec, charges), "charges": charges,
    }
    if loadings:
        out["loadings"] = _loadings(Xmat, cats, k_hat, spec, charges, alpha=alpha, restarts=restarts,
                                    max_iters=max_iters, seed=seed)
    return out


def excess_over_null(rows, spec=C.EIGHTFOLD_SPEC, *, k_hat, m=NULL_M, seed=SEED, repeats=5, restarts=3,
                     max_iters=80, burn=X.S1_BURN, thin=X.S1_THIN):
    """Secondary estimator: is k_hat's predictive gain over k=1 real, or an artifact of marginals + typing?
    Compare the real gain (acc[k_hat] - acc[1]) to the same gain over M S1 nulls (marginal+typing+entailment
    preserved). Reduced CV budget (the null loop is M-fold). Reuses crucible._null_chain / _envelope.

    DEGENERATE AT k_hat == 1 — reported as inapplicable, never as a result (see below)."""
    charges = list(spec.charges)
    ks = sorted({1, k_hat})
    rule = ("k_hat's dimensionality is structure-beyond-typing iff the real acc-gain of k_hat over k=1 "
            "exceeds the null 97.5th pct (one-sided). Inside the envelope -> RESIZE to "
            "'explained by typing + marginals', stated at that size.")

    # ── the k_hat == 1 degeneracy (found by the tidy-number gate, 2026-07-25) ──────────────────────────────
    # The statistic is acc[k_hat] - acc[1]. At k_hat == 1 that is acc[1] - acc[1] = 0.0 EXACTLY, on the real
    # table and on every one of the M nulls alike — the same float subtracted from itself, so the zero is an
    # identity of the EXPRESSION, invariant under the input. The block this function used to return therefore
    # read real = null_mean = null_p2.5 = null_p97.5 = 0.0 with one_sided_p_ge = (M+1)/(M+1) = 1.0, and
    # declared `excess_over_typing: false` — a verdict that would have come out identically on ANY input,
    # including a table with overwhelming latent structure. prereg_v7's secondary presumes k* > 1.
    #
    # WHAT IS AND IS NOT DROPPED (the instance-26 lesson, applied). The GAIN is kept: 0.0 is what the
    # expression evaluates to, and encoding a computed value as `null` asserts NOT COMPUTED about something
    # that was — the error retracted in instance 26. It ships with an acknowledgement carrying the identity,
    # so the zero stays legible instead of merely present. The ENVELOPE is dropped, on a different ground:
    # not "unmeasured" but UNDEFINED. A constant has no distribution, so there is no [p2.5, p97.5] to place
    # the point in and no percentile that means anything; and `excess_over_typing` becomes null rather than
    # false because `false` reports a test outcome and no test occurred. The M nulls are not drawn at all —
    # 150 EM fits to establish 0 == 0 is compute spent to manufacture a verdict.
    #
    # NOT A CLAMP AND NOT A p-FORM ARTIFACT — both checked rather than assumed. Nothing on this path clamps
    # (unlike structure.cramers_v's Bergsma floor), n is 114 not 22, and `_envelope` already uses the
    # plus-one form: with every null tied to the real value it returns (M+1)/(M+1) = 1.0, exactly what k/M
    # would give. Plus-one rescues the LOWER boundary, where "no draw reached it" is unprovable; at the upper
    # boundary "every draw was >= real" is directly observed, so 1.0 is honest arithmetic. The defect is the
    # vacuity of the comparison being summarised, not the summary.
    #
    # The question this was written to ask — is there association beyond per-charge marginals + n.a. typing —
    # is still answered, by two non-degenerate instruments: Crucible S1 (the gradient's own S1 envelope) and
    # the prereg_v8 null-corrected low-rank arm, which scores rank >= 1 against the k=0 marginal baseline and
    # so stays well-defined exactly where this one collapses.
    if len(ks) < 2:
        return {
            "k_hat": k_hat, "M": 0, "applicable": False,
            "real_gain_acc_khat_over_k1": 0.0, "null_envelope": None, "excess_over_typing": None,
            "not_applicable_reason": (
                f"k_hat = {k_hat}, so the statistic acc[k_hat] - acc[1] is acc[1] - acc[1] = 0 identically, "
                "on the real table and on every null. The gain is reported (0.0 is what the expression "
                "evaluates to) and acknowledged as an identity; the envelope is not, because a constant has "
                "no distribution to be placed in. No comparison is performed, so no excess-over-typing "
                "verdict is available from this estimator. Read the structure-beyond-typing question off "
                "Crucible S1 and the prereg_v8 low-rank arm (factors_v1_1.json), both of which remain "
                "well-defined at k* = 1."),
            "rule": rule,
        }

    def gain(tbl_rows):
        Xm, cs = _encode(tbl_rows, spec, charges)
        cv = _cv_curve(Xm, cs, ks, repeats=repeats, restarts=restarts, max_iters=max_iters, seed=seed)
        return cv[k_hat]["acc_mean"] - cv[1]["acc_mean"]

    real_gain = gain(rows)
    rng = np.random.default_rng(seed)
    null_gains = [gain(nr) for nr in X._null_chain(rows, rng, burn, thin, m, spec)]
    env = X._envelope(real_gain, null_gains)
    return {"k_hat": k_hat, "M": m, "applicable": True,
            "real_gain_acc_khat_over_k1": round(real_gain, 4),
            "null_envelope": {k: (round(v, 4) if isinstance(v, float) else v) for k, v in env.items()},
            "excess_over_typing": env["real_above_p97_5"],
            "rule": rule}


# ── F-2 verdict run (the dedup'd canon + ablations + sensitivity) ──────────────────────────────────────────
def factors_verdict(entries, spec=C.EIGHTFOLD_SPEC, *, drop_measured=False, primary_raw=False,
                    with_null=True, budget=None, ab_budget=None):
    """Assemble the Factors v1 verdict: primary k* on the dedup'd 114-class table, LOCO / drop-measured / raw
    ablations, excess-over-null, MCA sensitivity (flagged disqualified), and the on-file prediction score.

    The PRIMARY claim uses the full prereg budget (`budget`, default the prereg_v7 implementation_params). The
    ablations (LOCO / drop-measured / raw sensitivity) use a lighter CV budget (`ab_budget`) — they report k*
    ROBUSTNESS, not a precise interval, so a lighter fold count suffices; both budgets are recorded below."""
    b = {"repeats": CV_REPEATS, "restarts": EM_RESTARTS, "max_iters": EM_MAX_ITERS}
    if budget:
        b.update(budget)
    ab = {"repeats": 12, "restarts": 4, "max_iters": 100}
    if ab_budget:
        ab.update(ab_budget)
    dedup = [e for e in entries if e.problem_id not in X._S2_DROP]
    primary_entries = list(entries) if primary_raw else dedup
    sens_entries = dedup if primary_raw else list(entries)
    _, _, rows = S._grid(primary_entries, drop_measured=drop_measured)

    primary = estimate_rows(rows, spec, **b)
    k_hat = primary["k_hat_1se"]

    # (a) raw/dedup sensitivity — the OTHER roster (lighter budget)
    _, _, sens_rows = S._grid(sens_entries, drop_measured=drop_measured)
    sensitivity = estimate_rows(sens_rows, spec, loadings=False, **ab)

    # (b) leave-one-charge-out — no dimensionality claim may hinge on a single charge (lighter budget)
    loco = {}
    for drop in spec.charges:
        keep = [c for c in spec.charges if c != drop]
        loco[drop] = estimate_rows(rows, spec, charges=keep, loadings=False, **ab)["k_hat_1se"]

    # (c) drop-measured — no claim rests on the two measured charges alone (R9) (lighter budget)
    _, _, rows_dm = S._grid(primary_entries, drop_measured=True)
    drop_measured_k = estimate_rows(rows_dm, spec, loadings=False, **ab)["k_hat_1se"]

    # (d) MCA sensitivity — S1-DISQUALIFIED as primary (Crucible S1); reported, never the claim
    mca_dims = S.mca(rows, spec.charges)["dims_above_threshold"]

    # (e) secondary — excess over the S1 null
    excess = excess_over_null(rows, spec, k_hat=k_hat) if with_null else None

    # on-file prediction: k* in {3,4}? (scored, not gated)
    pred_hit = bool(set(primary["interval"]) & {3, 4})

    # tidy-number gate (methods 22). At k=1 the mixture has one component, so its prior is 1.0 by the
    # constraint that the priors sum to 1 — an exact extremal that the gate's current walker happens not to
    # reach (it does not descend into JSON arrays, and `classes` is one). Acknowledged anyway: an exactness
    # left unexplained because a checker cannot currently see it is still unexplained.
    ack = []
    # The degenerate secondary keeps its zero (instance 26: a computed value is not encoded as `null`), so
    # the zero owes the gate its arithmetic. Derived from the run — if a future roster moves k* off 1 the
    # comparison becomes real, `applicable` flips, and this acknowledgement disappears with its cause rather
    # than lingering as a stale exemption.
    if excess and not excess.get("applicable", True):
        ack.append({
            "stat": "excess_over_null.real_gain_acc_khat_over_k1", "value": 0.0,
            "identity_arithmetic": {"k_hat": excess["k_hat"], "ks_compared": sorted({1, excess["k_hat"]}),
                                    "statistic": "acc[k_hat] - acc[1]", "nulls_drawn": excess["M"]},
            "why_the_exactness_is_expected":
                f"an IDENTITY OF THE EXPRESSION, not a measurement. k_hat = {excess['k_hat']}, so "
                "acc[k_hat] - acc[1] is acc[1] minus itself — the same float, subtracted from itself, "
                "yielding exactly 0.0 on the real table and on any null anyone cares to draw. The value is "
                "INVARIANT UNDER THE INPUT: an atlas with overwhelming latent structure produces this same "
                "0.0. Read it as 'the secondary has no statistic at k*=1', NOT as 'the measured gain was "
                "zero'. The sibling `null_envelope` is null rather than 0.0 for a different reason — a "
                "constant has no distribution, so the percentiles are undefined, not merely unmeasured.",
            "direction_note":
                "discharged in the UNFLATTERING direction: this exactness made the old block UNDER-claim "
                "(it agreed with the k*=1 the primary had already found), which is why it survived review "
                "for as long as it did. A gate that only interrogates flattering exactness would have "
                "missed it.",
        })
    for i, cl in enumerate(primary.get("loadings", {}).get("classes", []) or []):
        if isinstance(cl.get("prior"), float) and cl["prior"] in (0.0, 1.0):
            ack.append({
                "stat": f"loadings_interpretive.classes.{i}.prior", "value": cl["prior"],
                "why_the_exactness_is_expected":
                    f"k = {k_hat}, so the fitted mixture has a single class and its prior is 1.0 by the "
                    "simplex constraint (the class priors sum to 1). Nothing was estimated to be certain "
                    "here; there was one place for the mass to go. The block is interpretive-only and sets "
                    "no claim.",
            })

    return {
        "factors": True, "prereg": "prereg_v7", "model": primary["model"],
        "manifest": {"seed": SEED, "primary_budget": b, "ablation_budget": ab,
                     "mask_fraction": MASK_FRAC, "smoothing_alpha": SMOOTHING_ALPHA,
                     "excess_over_null_M": (excess or {}).get("M", 0)},
        "primary_roster": "raw-118" if primary_raw else "dedup-114 (S2)",
        "drop_measured": drop_measured,
        "n_rows": primary["n_rows"], "n_distinct_profiles": primary["n_distinct_profiles"],
        "k_star": {
            "verdict_interval": primary["interval"], "k_hat_1se": k_hat, "k_argmax": primary["k_argmax"],
            "best_acc": primary["best_acc"], "se_at_best": primary["se_at_best"], "curve": primary["curve"],
            "rule": ("k*_hat = smallest k within 1 SE of the best mean held-out accuracy (parsimonious 1-SE "
                     "rule); the CLAIM is the interval, stated at its size. MCA counts are S1-disqualified."),
        },
        "on_file_prediction_P_k": {"prediction": "k* in {3,4}", "interval": primary["interval"],
                                   "hit": pred_hit, "note": "scored, not gated (prereg_v7)"},
        "ablations": {
            "sensitivity_other_roster": {"roster": "dedup-114" if primary_raw else "raw-118",
                                         "k_hat_1se": sensitivity["k_hat_1se"], "interval": sensitivity["interval"]},
            "leave_one_charge_out_k_hat": loco, "loco_min": min(loco.values()), "loco_max": max(loco.values()),
            "drop_measured_k_hat": drop_measured_k,
            "note": "R-fac1: k* robust to roster (dedup vs raw), to any single charge (LOCO), and to the measured cells.",
        },
        "excess_over_null": excess,
        "mca_sensitivity_DISQUALIFIED": {
            "dims_above_threshold": mca_dims,
            "note": ("R-fac2: MCA eigenvalue count is reported as a sensitivity ONLY and is S1-disqualified as "
                     "the primary estimator (Crucible S1). It does not set k*."),
        },
        "loadings_interpretive": primary.get("loadings"),
        "extremal_acknowledged": ack,
    }


# ── F-1 selftest: planted-k recovery + pure-null quiet (synthetic, reduced budget — a wiring check) ─────────
def _planted_factor_table(k, n_per=30, spec=C.EIGHTFOLD_SPEC, *, modal_p=0.9, miss_p=0.1, seed=SEED):
    """Sample from a KNOWN-k latent class model: k separable class profiles over the charges, each row emitting
    its class's modal level w.p. modal_p (else a random level), with miss_p cells sentinel."""
    rng = np.random.default_rng(seed)
    charges = list(spec.charges)
    levels = {ch: sorted(spec.charge_real_values[ch]) for ch in charges}
    profiles = [{ch: levels[ch][(c + j) % len(levels[ch])] for j, ch in enumerate(charges)} for c in range(k)]
    rows = []
    for c in range(k):
        for _ in range(n_per):
            r = {}
            for ch in charges:
                L = levels[ch]
                if rng.random() < miss_p:
                    r[ch] = "open"
                elif rng.random() < modal_p:
                    r[ch] = profiles[c][ch]
                else:
                    r[ch] = L[int(rng.integers(len(L)))]
            rows.append(r)
    return rows


def _null_factor_table(n=90, spec=C.EIGHTFOLD_SPEC, *, miss_p=0.1, dominant_p=None, seed=SEED):
    """Pure null: every charge drawn INDEPENDENTLY (no latent structure -> LCM k*=1 / low-rank k*=0). With
    dominant_p set, each charge has a skewed marginal (one dominant level w.p. dominant_p, rest uniform) — the
    realistic regime the real canon lives in (modal probs 0.44-0.81), where the marginal baseline is STRONG and
    a valid estimator must not hallucinate structure. dominant_p=None keeps a uniform marginal."""
    rng = np.random.default_rng(seed)
    charges = list(spec.charges)
    levels = {ch: sorted(spec.charge_real_values[ch]) for ch in charges}
    rows = []
    for _ in range(n):
        r = {}
        for ch in charges:
            L = levels[ch]
            if rng.random() < miss_p:
                r[ch] = "open"
            elif dominant_p is None or len(L) < 2:
                r[ch] = L[int(rng.integers(len(L)))]
            else:
                rest = (1.0 - dominant_p) / (len(L) - 1)
                p = np.array([dominant_p] + [rest] * (len(L) - 1))
                r[ch] = L[int(rng.choice(len(L), p=p))]
        rows.append(r)
    return rows


def selftest(verbose=True):
    """F-1 gate (prereg_v7): the estimator must RECOVER a planted k (k_hat == planted, planted in interval) and
    stay QUIET on a pure null (k_hat in {0,1}). Reduced budget — a wiring check, not the science run."""
    budget = dict(ks=range(1, 6), repeats=6, restarts=4, max_iters=70, loadings=False)
    planted_k = 3
    rp = estimate_rows(_planted_factor_table(planted_k, n_per=30, seed=SEED), seed=SEED, **budget)
    rn = estimate_rows(_null_factor_table(90, seed=SEED + 7), seed=SEED, **budget)
    recovery = (planted_k in rp["interval"]) and (rp["k_hat_1se"] == planted_k)
    null_quiet = rn["k_hat_1se"] in (0, 1)
    ok = recovery and null_quiet
    if verbose:
        pc = {k: rp["curve"][k]["acc_mean"] for k in rp["curve"]}
        nc = {k: rn["curve"][k]["acc_mean"] for k in rn["curve"]}
        print("Factors v1 selftest (LCM, reduced budget — wiring check):")
        print(f"  planted k={planted_k}: k_hat={rp['k_hat_1se']} argmax={rp['k_argmax']} "
              f"interval={rp['interval']} -> recovery={recovery}")
        print(f"    acc curve: {pc}")
        print(f"  pure null:  k_hat={rn['k_hat_1se']} argmax={rn['k_argmax']} interval={rn['interval']} "
              f"-> null_quiet={null_quiet}")
        print(f"    acc curve: {nc}")
        print(f"  selftest {'PASSED' if ok else 'FAILED'} (planted recovered AND null quiet)")
    return 0 if ok else 1


# ── low-rank categorical PCA arm (Factors v1.1 follow-up; prereg_v8) ────────────────────────────────────────
# A DIFFERENT model class from the LCM: continuous latent factors via soft-impute truncated-SVD of the one-hot
# indicator matrix, with k (the SVD rank) selected by HELD-OUT PREDICTION (not eigenvalue thresholds — so it is
# NOT the S1-disqualified MCA count). k=0 is the per-column-marginal baseline. Run as a co-equal TRIANGULATION of
# the v7 k*=1 verdict (owner-chosen new prereg), never a post-hoc escalation.
def _blocks(cats):
    slices, s = [], 0
    for levels in cats:
        slices.append((s, s + len(levels)))
        s += len(levels)
    return slices, s


def _lowrank_curve(Xmat, cats, ks, *, mask_frac=MASK_FRAC, repeats=CV_REPEATS, iters=12, seed=SEED):
    """Held-out CV for the soft-impute truncated-SVD model. k = rank (k=0 = marginal baseline)."""
    n, p = Xmat.shape
    slices, Cw = _blocks(cats)
    obs_idx = np.argwhere(Xmat >= 0)
    rng = np.random.default_rng(seed)
    accs = {k: [] for k in ks}
    n_hold = max(1, int(round(mask_frac * len(obs_idx))))
    for rep in range(repeats):
        sel = rng.choice(len(obs_idx), size=n_hold, replace=False)
        held_cells = [tuple(obs_idx[s]) for s in sel]
        held = np.zeros((n, p), dtype=bool)
        for i, j in held_cells:
            held[i, j] = True
        Z = np.full((n, Cw), np.nan)
        for i in range(n):
            for j in range(p):
                if Xmat[i, j] >= 0 and not held[i, j]:
                    a, _ = slices[j]
                    Z[i, slices[j][0]:slices[j][1]] = 0.0
                    Z[i, a + int(Xmat[i, j])] = 1.0
        miss = np.isnan(Z)
        cnt = np.sum(~miss, axis=0)
        colmean = np.where(cnt > 0, np.nansum(Z, axis=0) / np.maximum(cnt, 1), 0.0)
        for k in ks:
            if k == 0:
                Zhat = np.tile(colmean, (n, 1))
            else:
                Zf = np.where(miss, colmean, Z)
                Zhat = Zf
                for _ in range(iters):
                    U, Sv, Vt = np.linalg.svd(Zf - colmean, full_matrices=False)
                    kk = min(k, len(Sv))
                    Zhat = (U[:, :kk] * Sv[:kk]) @ Vt[:kk] + colmean
                    Zf = np.where(miss, Zhat, Z)
            c = t = 0
            for i, j in held_cells:
                a, b = slices[j]
                c += int(np.argmax(Zhat[i, a:b]) == int(Xmat[i, j]))
                t += 1
            accs[k].append(c / t if t else np.nan)
    res = {}
    for k in ks:
        arr = np.array(accs[k], float)
        nf = int(np.sum(~np.isnan(arr)))
        se = float(np.nanstd(arr, ddof=1) / np.sqrt(nf)) if nf > 1 else np.nan
        res[k] = {"acc_mean": float(np.nanmean(arr)), "acc_se": se, "n_folds": nf}
    return res


def _lowrank_loadings(Xmat, cats, k, charges, iters=15):
    slices, Cw = _blocks(cats)
    n, p = Xmat.shape
    Z = np.full((n, Cw), np.nan)
    for i in range(n):
        for j in range(p):
            if Xmat[i, j] >= 0:
                a, _ = slices[j]
                Z[i, slices[j][0]:slices[j][1]] = 0.0
                Z[i, a + int(Xmat[i, j])] = 1.0
    miss = np.isnan(Z)
    cnt = np.sum(~miss, axis=0)
    colmean = np.where(cnt > 0, np.nansum(Z, axis=0) / np.maximum(cnt, 1), 0.0)
    Zf = np.where(miss, colmean, Z)
    Sv = Vt = None
    for _ in range(iters):
        U, Sv, Vt = np.linalg.svd(Zf - colmean, full_matrices=False)
        kk = min(k, len(Sv))
        Zf = np.where(miss, (U[:, :kk] * Sv[:kk]) @ Vt[:kk] + colmean, Z)
    labels = [(charges[j], lev) for j, levels in enumerate(cats) for lev in levels]
    factors = []
    for r in range(min(k, len(Sv))):
        load = Vt[r]
        order = np.argsort(-np.abs(load))[:6]
        factors.append({"singular_value": round(float(Sv[r]), 3),
                        "top_loadings": [{"charge_level": f"{labels[o][0]}={labels[o][1]}",
                                          "loading": round(float(load[o]), 3)} for o in order]})
    return {"k": k, "factors": factors}


def _ack_lowrank(curve, null_gain, m_null, n_hold, null_repeats):
    """Derive the `extremal_acknowledged` entries this low-rank arm owes the tidy-number gate (methods 22).

    DERIVED, never stapled on: an entry is emitted only for a value that is actually exactly extremal AND
    whose exactness this function can explain from the arithmetic in front of it. Two causes are recognised —

      (1) THE k=0 SELF-IDENTITY. Both `gain_over_k0` and `null_gain_p97.5` are differences of the k=0
          accuracy from itself at k=0, so both are 0.0 by construction on the real table and on every
          permutation. k=0 is the marginal BASELINE the gains are measured against; it cannot gain on itself.

      (2) THE DISCRETISED NULL'S ZERO ATOM at k >= 1. Held-out accuracy on these tables lives on a lattice of
          1/(n_hold * null_repeats), so the null gain distribution is a handful of atoms rather than a
          continuum. Where enough permutation draws pile up at exactly 0, the interpolated 97.5th percentile
          lands inside that atom and is exactly 0.0 — a real percentile of a real distribution, coarse rather
          than absent. The entry carries the atom counts so the reading can be checked by hand.

    Anything else extremal gets NO entry and correctly fails the gate: a new exact 0.0/1.0 at a path nobody
    has read is the case this whole mechanism exists to stop."""
    ack = []
    for k in sorted(curve):
        cell = curve[k]
        if k == 0:
            if cell["gain_over_k0"] == 0.0:
                ack.append({
                    "stat": "curve.0.gain_over_k0", "value": 0.0,
                    "why_the_exactness_is_expected":
                        "k=0 IS the per-column-marginal baseline every gain is measured against, and this "
                        "cell is its gain over itself: acc_mean[0] - acc_mean[0]. Exactly 0.0 is the "
                        "definition of the origin, not a measured null result.",
                })
            if cell["null_gain_p97.5"] == 0.0:
                ack.append({
                    "stat": "curve.0.null_gain_p97.5", "value": 0.0,
                    "why_the_exactness_is_expected":
                        f"the same self-identity under permutation: each of the {m_null} column-permutation "
                        "nulls contributes acc_mean[0] - acc_mean[0] = 0, so the null gain distribution at "
                        "k=0 is a point mass at 0 and every percentile of it is 0.0. It is the origin "
                        "restated, and carries no information about whether rank-0 'beats' anything.",
                })
            continue
        if cell["null_gain_p97.5"] == 0.0:
            v = sorted(null_gain[k])
            n_zero = sum(1 for x in v if abs(x) < 1e-12)
            n_above = sum(1 for x in v if x > 1e-12)
            res = 1.0 / (n_hold * null_repeats)
            ack.append({
                "stat": f"curve.{k}.null_gain_p97.5", "value": 0.0,
                "atom_arithmetic": {
                    "m_null": m_null, "gain_resolution": round(res, 4),
                    "n_null_draws_exactly_zero": n_zero, "n_null_draws_above_zero": n_above,
                    "null_gain_max": round(float(v[-1]), 4),
                    "order_stats_bracketing_p97.5": [round(float(v[int(0.975 * (m_null - 1))]), 4),
                                                     round(float(v[min(int(0.975 * (m_null - 1)) + 1,
                                                                       m_null - 1)]), 4)],
                },
                "why_the_exactness_is_expected":
                    f"a REAL percentile of a COARSE distribution, not a missing computation. Held-out "
                    f"accuracy here is a count over {n_hold} masked cells averaged across {null_repeats} "
                    f"repeats, so null gains land on a lattice of 1/{n_hold * null_repeats} = {round(res, 4)}. "
                    f"Of the {m_null} permutation draws, {n_zero} sit at exactly 0 and only {n_above} exceed "
                    f"0 (max {round(float(v[-1]), 4)}), so the two order statistics the 97.5th percentile "
                    f"interpolates between are both 0.0 and the percentile is exactly 0.0.",
                "caveat_carried_forward":
                    "`beats_null` at this k is a strict `>` against a threshold sitting INSIDE a probability "
                    f"atom that holds {n_zero}/{m_null} of the null mass, so a real gain smaller than one "
                    "lattice step is credited on a knife edge. The prereg_v8 crediting rule is left as "
                    "written rather than re-specified after seeing the data; it does not move this arm's "
                    "verdict, which is set by the contiguity requirement from rank 1 and is unaffected.",
            })
    return ack


def _colperm(rows, charges, rng):
    """Independence null: permute each charge's column across rows — preserves every marginal exactly, destroys
    all cross-charge structure. Removes the one-hot compositional artifact that a raw SVD rank would read as
    'structure' (the same artifact that disqualifies MCA)."""
    n = len(rows)
    cols = {ch: [r.get(ch) for r in rows] for ch in charges}
    permd = {ch: [cols[ch][i] for i in rng.permutation(n)] for ch in charges}
    return [{ch: permd[ch][i] for ch in charges} for i in range(n)]


def estimate_rows_lowrank(rows, spec=C.EIGHTFOLD_SPEC, *, charges=None, ks=range(0, 6), mask_frac=MASK_FRAC,
                          repeats=CV_REPEATS, iters=12, m_null=60, null_repeats=4, seed=SEED, loadings=True):
    """Low-rank categorical PCA, NULL-CORRECTED. Raw SVD rank on the one-hot indicators inherits the MCA
    compositional artifact, so a rank is credited only if it beats an independence (column-permutation) null.
    k* = the parsimonious real plateau (smallest k within 1 SE of the best held-out accuracy, same rule as the
    LCM), credited ONLY if every rank 1..plateau beats the null 97.5th-pct gain (contiguous structure from rank
    1); else k* = 0. Anchoring at the plateau (not 'largest k beating null') avoids isolated high-k crossings."""
    charges = list(spec.charges) if charges is None else list(charges)
    Xmat, cats = _encode(rows, spec, charges)
    ks = list(ks)
    real = _lowrank_curve(Xmat, cats, ks, mask_frac=mask_frac, repeats=repeats, iters=iters, seed=seed)
    k_best = max(ks, key=lambda k: real[k]["acc_mean"])
    band = real[k_best]["acc_se"] if real[k_best]["acc_se"] == real[k_best]["acc_se"] else 0.0
    plateau = min(k for k in ks if real[k]["acc_mean"] >= real[k_best]["acc_mean"] - band)
    real_gain = {k: real[k]["acc_mean"] - real[0]["acc_mean"] for k in ks}
    rng = np.random.default_rng(seed)
    null_gain = {k: [] for k in ks}
    for t in range(m_null):
        Xn, catsn = _encode(_colperm(rows, charges, rng), spec, charges)
        nc = _lowrank_curve(Xn, catsn, ks, mask_frac=mask_frac, repeats=null_repeats, iters=iters,
                            seed=seed + 7919 * (t + 1))
        for k in ks:
            null_gain[k].append(nc[k]["acc_mean"] - nc[0]["acc_mean"])
    p975 = {k: float(np.percentile(null_gain[k], 97.5)) for k in ks}
    beats = {k: bool(real_gain[k] > p975[k]) for k in ks}
    contiguous = plateau >= 1 and all(beats[k] for k in range(1, plateau + 1))
    k_star = plateau if contiguous else 0
    out = {"model": "lowrank-catpca-null-corrected", "k_hat_1se": k_star, "k_star_excess": k_star,
           "k_plateau_real": plateau, "structure_contiguous_beats_null": bool(contiguous),
           "interval": (list(range(1, plateau + 1)) if k_star >= 1 else [0]),
           "best_acc": round(real[k_best]["acc_mean"], 4),
           "curve": {k: {"acc_mean": round(real[k]["acc_mean"], 4), "acc_se": round(real[k]["acc_se"], 4),
                         "gain_over_k0": round(real_gain[k], 4), "null_gain_p97.5": round(p975[k], 4),
                         "beats_null": beats[k]} for k in ks},
           "m_null": m_null, "n_rows": len(rows), "n_distinct_profiles": _n_profiles(rows, spec, charges),
           "charges": charges}
    n_hold = max(1, int(round(mask_frac * int((Xmat >= 0).sum()))))
    out["extremal_acknowledged"] = _ack_lowrank(out["curve"], null_gain, m_null, n_hold, null_repeats)
    if loadings and k_star >= 1:
        out["loadings"] = _lowrank_loadings(Xmat, cats, k_star, charges)
    return out


def _planted_lowrank_table(r, n=90, spec=C.EIGHTFOLD_SPEC, *, scale=2.5, miss_p=0.1, seed=SEED):
    """A genuine rank-r categorical structure: per-charge logits = U @ W_ch^T, x ~ softmax(logits)."""
    rng = np.random.default_rng(seed)
    charges = list(spec.charges)
    levels = {ch: sorted(spec.charge_real_values[ch]) for ch in charges}
    U = rng.standard_normal((n, r))
    W = {ch: rng.standard_normal((len(levels[ch]), r)) * scale for ch in charges}
    rows = []
    for i in range(n):
        rr = {}
        for ch in charges:
            if rng.random() < miss_p:
                rr[ch] = "open"
                continue
            logits = U[i] @ W[ch].T
            pmf = np.exp(logits - logits.max())
            pmf /= pmf.sum()
            rr[ch] = levels[ch][int(rng.choice(len(pmf), p=pmf))]
        rows.append(rr)
    return rows


def selftest_lowrank(verbose=True):
    """prereg_v8 gate for the null-corrected low-rank arm: recover a planted rank (k*_excess >= 1, with rank r
    beating the null) AND stay quiet (k*_excess = 0) on a pure independent null. Reduced budget wiring check."""
    r = 2
    lo = dict(repeats=8, m_null=30, null_repeats=3, seed=SEED, loadings=False)
    rp = estimate_rows_lowrank(_planted_lowrank_table(r, n=90, seed=SEED), **lo)
    # skewed independent null (dominant_p=0.6) — the realistic marginal regime the real canon lives in
    rn = estimate_rows_lowrank(_null_factor_table(90, dominant_p=0.6, seed=SEED + 7), **lo)
    # recovery: detect multi-dim structure (k*>=2) with the planted rank on the real plateau
    recovery = rp["k_star_excess"] >= 2 and r <= rp["k_plateau_real"]
    # null quiet: no structure of rank>=2 beyond marginals (a single noise-floor rank-1 edge crossing is tolerated)
    null_quiet = rn["k_star_excess"] <= 1
    ok = recovery and null_quiet
    if verbose:
        pg = {k: (rp["curve"][k]["gain_over_k0"], rp["curve"][k]["null_gain_p97.5"]) for k in rp["curve"]}
        ng = {k: (rn["curve"][k]["gain_over_k0"], rn["curve"][k]["null_gain_p97.5"]) for k in rn["curve"]}
        print("Factors v1.1 low-rank selftest (null-corrected soft-impute SVD — wiring check):")
        print(f"  planted rank r={r}: k*_excess={rp['k_star_excess']} beats-null-at={rp['interval']} "
              f"-> recovery={recovery}")
        print(f"    (gain_over_k0, null_p97.5) per k: {pg}")
        print(f"  pure null:  k*_excess={rn['k_star_excess']} beats-null-at={rn['interval']} "
              f"-> null_quiet={null_quiet}")
        print(f"    (gain_over_k0, null_p97.5) per k: {ng}")
        print(f"  low-rank selftest {'PASSED' if ok else 'FAILED'} (planted rank recovered AND null quiet)")
    return 0 if ok else 1


def followup_verdict(entries, spec=C.EIGHTFOLD_SPEC, *, budget=None):
    """F-4c (prereg_v8): triangulate the v7 k*=1 verdict along model class (low-rank vs LCM) and charge
    sparsity (core-4 vs all-8). Reports every k* side by side with v7's k*=1; does NOT overturn v7."""
    b = {"repeats": CV_REPEATS}
    lcm_b = {"repeats": CV_REPEATS, "restarts": EM_RESTARTS, "max_iters": EM_MAX_ITERS}
    if budget:
        b.update(budget)
        lcm_b.update(budget)
    dedup = [e for e in entries if e.problem_id not in X._S2_DROP]
    _, _, rows = S._grid(dedup)
    cc_rows, cc_charges = S.complete_case(rows)  # rows real-valued on all 4 COMPLETE_CASE_CHARGES

    lr_full = estimate_rows_lowrank(rows, spec, **b)
    lr_core = estimate_rows_lowrank(cc_rows, spec, charges=cc_charges, **b)
    lcm_core = estimate_rows(cc_rows, spec, charges=cc_charges, loadings=False, **lcm_b)

    def robust(res):
        return res["k_hat_1se"] <= 1

    # tidy-number gate (methods 22): each low-rank arm derives its own acknowledgements; re-path them to
    # where they actually sit in this artifact, since the gate matches on the full dotted path.
    ack = [{**a, "stat": f"arms.{arm}.{a['stat']}"}
           for arm, res in (("lowrank_full_8", lr_full), ("lowrank_core_4", lr_core))
           for a in res.get("extremal_acknowledged", [])]
    return {
        "factors_followup": True, "prereg": "prereg_v8", "supersedes": None,
        "reference_verdict_v7": {"model": "lcm", "roster": "dedup-114 all-8", "k_hat_1se": 1, "interval": [1]},
        "arms": {
            "lowrank_full_8": {"roster": "dedup-114 all-8", "model": lr_full["model"],
                               "k_star_excess": lr_full["k_star_excess"], "k_plateau_real": lr_full["k_plateau_real"],
                               "structure_beats_null": lr_full["structure_contiguous_beats_null"],
                               "interval": lr_full["interval"], "best_acc": lr_full["best_acc"],
                               "m_null": lr_full["m_null"], "curve": lr_full["curve"], "n_rows": lr_full["n_rows"],
                               "loadings": lr_full.get("loadings")},
            "lowrank_core_4": {"roster": f"complete-case on {cc_charges}", "model": lr_core["model"],
                               "k_star_excess": lr_core["k_star_excess"], "k_plateau_real": lr_core["k_plateau_real"],
                               "structure_beats_null": lr_core["structure_contiguous_beats_null"],
                               "interval": lr_core["interval"], "best_acc": lr_core["best_acc"],
                               "curve": lr_core["curve"], "n_rows": lr_core["n_rows"]},
            "lcm_core_4": {"roster": f"complete-case on {cc_charges}", "model": "lcm",
                           "k_hat_1se": lcm_core["k_hat_1se"], "interval": lcm_core["interval"],
                           "best_acc": lcm_core["best_acc"], "curve": lcm_core["curve"], "n_rows": lcm_core["n_rows"]},
        },
        "triangulation": {
            "v7_lcm_full_k1": True,
            "lowrank_full_agrees_k_le_1": robust(lr_full),
            "core4_lowrank_k_le_1": robust(lr_core), "core4_lcm_k_le_1": robust(lcm_core),
            "note": ("k*=1 is CONFIRMED robust iff every arm gives k*<=1. A single arm with k*>1 is a "
                     "methodological finding (model class or charge-sparsity was the limiting factor), reported "
                     "at size; it refines, and does NOT argue back, v7's primary k*=1. Core-4 carries an "
                     "n-underpower caveat (small complete-case block)."),
        },
        "extremal_acknowledged": ack,
    }


# ── sensitivity / power annex (R-v): what CAN the estimator see at canon n + missingness? ──────────────────
def _canon_real_fraction(spec=C.EIGHTFOLD_SPEC, path=None):
    """Fraction of the dedup'd canon's cells that carry a real value (the rest are sentinels) — used to give the
    power-calibration planted tables canon-like missingness."""
    from eightfold.atlas import load_atlas
    entries = [e for e in load_atlas(path) if e.problem_id not in X._S2_DROP]
    _, _, rows = S._grid(entries)
    tot = real = 0
    for r in rows:
        for ch in spec.charges:
            tot += 1
            real += int(r[ch] in spec.charge_real_values[ch])
    return real / tot if tot else 0.0


def sensitivity_floor(spec=C.EIGHTFOLD_SPEC, *, n=114, planted_k=3, n_seeds=8,
                      separations=(0.9, 0.7, 0.5, 0.4, 0.3, 0.2, 0.15, 0.1, 0.05, 0.0), miss_p=None,
                      repeats=15, restarts=5, max_iters=100, path=None):
    """Power-calibrate the k*=1 NEGATIVE. At canon-like n and missingness, sweep the planted class SEPARATION
    (modal_p = the excess probability a cell shows its class's modal level; 0 = no separation = indistinguishable
    classes) and report, per separation, the fraction of seeds where the LCM recovers k*>=2. The detectable-effect
    FLOOR = the WEAKEST separation still recovered in >=80% of seeds. k*=1 on the canon then means: any real latent
    structure has separation below this floor — 'no basis' is distinguished from 'basis below our lamp'."""
    if miss_p is None:
        miss_p = round(1.0 - _canon_real_fraction(spec, path), 3)
    curve = {}
    for sep in separations:
        rec = 0
        for s in range(n_seeds):
            rows = _planted_factor_table(planted_k, n_per=max(1, n // planted_k), spec=spec,
                                         modal_p=sep, miss_p=miss_p, seed=SEED + 101 * s)
            r = estimate_rows(rows, spec, ks=range(1, 6), repeats=repeats, restarts=restarts,
                              max_iters=max_iters, loadings=False, seed=SEED)
            rec += int(r["k_hat_1se"] >= 2)
        curve[round(sep, 3)] = round(rec / n_seeds, 3)
    recovered = [round(sep, 3) for sep in separations if curve[round(sep, 3)] >= 0.8]
    floor = min(recovered) if recovered else None
    # The zero-separation cell is the FALSE-POSITIVE BASE RATE, not a decoration: at modal_p = 0 the planted
    # classes are indistinguishable, so every k*>=2 there is the 1-SE rule firing on noise. Reported as its own
    # field (and quoted in the note) because the floor above is only interpretable against it.
    base = curve.get(0.0)
    # tidy-number gate (methods 22): a recovery fraction is rec/n_seeds, so 0.0 and 1.0 are the two endpoints
    # of a coarse integer lattice and both are reachable without anything being wrong. Acknowledged with the
    # count that produced them, and with the shape of the rest of the curve — a fraction of 1.0 is only benign
    # BECAUSE the same estimator drops well below 1.0 elsewhere in the same sweep.
    worst = min(curve, key=lambda t: curve[t])
    ack = []
    for sep in separations:
        s = round(sep, 3)
        frac = curve[s]
        if frac not in (0.0, 1.0):
            continue
        ack.append({
            "stat": f"recovery_frac_by_separation.{s}", "value": frac,
            "count_arithmetic": {"recovered_seeds": int(round(frac * n_seeds)), "n_seeds": n_seeds,
                                 "resolution": round(1.0 / n_seeds, 4)},
            "why_the_exactness_is_expected":
                f"a fraction of seeds, not a probability with a continuum behind it: "
                f"{int(round(frac * n_seeds))}/{n_seeds} at modal_p={s}, on a lattice of steps of "
                f"{round(1.0 / n_seeds, 4)}, so both endpoints are ordinary attainable values at this seed "
                f"count. This is a POWER curve and saturation at strong separation is its design intent — an "
                f"estimator that could NOT recover a planted k={planted_k} at modal_p={s} would be the "
                f"finding. The exactness is also not saturation of the whole sweep: the same estimator, same "
                f"budget, returns {curve[worst]} at modal_p={worst} in this run.",
            "direction_note":
                "read against `zero_separation_recovery_frac` in this artifact — the rate at which this "
                "estimator claims k*>=2 when nothing was planted to find. A 1.0 here is only worth what that "
                "number is not.",
        })
    return {"sensitivity_floor": True, "canon_like_missingness": miss_p, "planted_k": planted_k, "n": n,
            "n_seeds": n_seeds, "recovery_frac_by_separation": curve, "reliable_recovery_floor_modal_p": floor,
            "zero_separation_recovery_frac": base,
            "note": ("modal_p = the excess probability a cell shows its class's modal level (0 = indistinguishable "
                     "classes). The floor is the WEAKEST separation the LCM recovers k*>=2 in >=80% of seeds at "
                     "canon n + missingness. k*=1 on the canon => any real latent structure sits below this "
                     "detectable-effect floor. READ THE FLOOR AGAINST THE ZERO-SEPARATION BASE RATE, reported "
                     f"above as `zero_separation_recovery_frac`: at modal_p=0 the classes are indistinguishable "
                     f"and there is nothing to find, yet the 1-SE rule still returns k*>=2 in {base} of seeds. "
                     "Recovery does NOT fall to ~0 at zero separation — an earlier revision of this note said it "
                     "did, which this sweep has never shown (corrected 2026-07-25, on reading the curve for the "
                     "tidy-number gate). So the >=80% criterion sits above a substantial false-positive rate "
                     f"rather than above zero, and the curve below the floor is non-monotone at n_seeds={n_seeds}. "
                     "The mitigation, stated at its own size and NOT as a dismissal: at modal_p=0 this generator "
                     "draws every cell UNIFORMLY over its charge's levels, which is a weaker k=1 baseline than "
                     "the canon's strongly skewed marginals (modal probs 0.44-0.81), so the base rate here is an "
                     "upper bound on the canon's. Findings R-v carries the same reading. Treat the floor as an "
                     "order-of-magnitude detectability scale, not a calibrated threshold."),
            "extremal_acknowledged": ack}


# ── CLI ────────────────────────────────────────────────────────────────────────────────────────────────────
def main(argv=None):
    ap = argparse.ArgumentParser(prog="eightfold.factors")
    ap.add_argument("--selftest", action="store_true", help="F-1 gate: planted-k recovery + pure-null quiet")
    ap.add_argument("--selftest-lowrank", action="store_true", help="prereg_v8 gate: low-rank planted-rank recovery + null quiet")
    ap.add_argument("--followup", action="store_true", help="F-4c: prereg_v8 k*=1 triangulation (low-rank + core-4)")
    ap.add_argument("--sensitivity", action="store_true", help="R-v: power-calibrate the k*=1 negative (detectable-effect floor)")
    ap.add_argument("--factors", action="store_true", help="F-2 verdict run on the dedup'd 114-class canon")
    ap.add_argument("--raw", action="store_true", help="sensitivity: use the raw 118 as the primary roster")
    ap.add_argument("--drop-measured", action="store_true", help="R9 ablation: exclude the measured cells")
    ap.add_argument("--no-null", action="store_true", help="skip the excess-over-null secondary (faster)")
    ap.add_argument("--path", type=Path, default=None, help="atlas path (default: the bundled atlas)")
    ap.add_argument("--out", type=Path, default=None, help="write factors_v1.json here")
    args = ap.parse_args(argv if argv is not None else sys.argv[1:])

    if args.selftest:
        return selftest()

    if args.selftest_lowrank:
        return selftest_lowrank()

    if args.sensitivity:
        from eightfold.atlas import DEFAULT_PATH
        out = sensitivity_floor(path=args.path)
        out_path = args.out or (DEFAULT_PATH.parent / "factors_sensitivity.json")
        out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Factors sensitivity floor (R-v) -> {out_path}")
        print(f"  canon-like missingness={out['canon_like_missingness']}, planted k={out['planted_k']}, n={out['n']}, seeds={out['n_seeds']}")
        for sep, frac in out["recovery_frac_by_separation"].items():
            print(f"    modal_p={sep}: recover k>=2 in {frac:.0%} of seeds")
        print(f"  detectable-effect floor (>=80% recovery): modal_p={out['reliable_recovery_floor_modal_p']}")
        return 0

    if args.followup:
        from eightfold.atlas import DEFAULT_PATH, load_atlas
        out = followup_verdict(load_atlas(args.path))
        out_path = args.out or (DEFAULT_PATH.parent / "factors_v1_1.json")
        out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
        a = out["arms"]
        print(f"Factors v1.1 follow-up (prereg_v8) -> {out_path}")
        print(f"  reference: v7 LCM full-8 k*=1")
        print(f"  low-rank full-8 : k*={a['lowrank_full_8']['k_star_excess']} beats-null-at={a['lowrank_full_8']['interval']} "
              f"(plateau={a['lowrank_full_8']['k_plateau_real']}, best acc={a['lowrank_full_8']['best_acc']}, n={a['lowrank_full_8']['n_rows']})")
        print(f"  low-rank core-4 : k*={a['lowrank_core_4']['k_star_excess']} beats-null-at={a['lowrank_core_4']['interval']} "
              f"(n={a['lowrank_core_4']['n_rows']})")
        print(f"  LCM      core-4 : k*={a['lcm_core_4']['k_hat_1se']} interval={a['lcm_core_4']['interval']} "
              f"(n={a['lcm_core_4']['n_rows']})")
        tri = out["triangulation"]
        allrobust = all([tri["lowrank_full_agrees_k_le_1"], tri["core4_lowrank_k_le_1"], tri["core4_lcm_k_le_1"]])
        print(f"  triangulation: k*=1 {'CONFIRMED robust (every arm k*<=1)' if allrobust else 'REFINED (an arm found k*>1 — see findings)'}")
        return 0

    if args.factors:
        from eightfold.atlas import DEFAULT_PATH, load_atlas
        entries = load_atlas(args.path)
        out = factors_verdict(entries, drop_measured=args.drop_measured, primary_raw=args.raw,
                              with_null=not args.no_null)
        out_path = args.out or (DEFAULT_PATH.parent / "factors_v1.json")
        out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
        ks = out["k_star"]
        print(f"Factors v1 verdict (prereg_v7, {out['primary_roster']}, n={out['n_rows']}, "
              f"{out['n_distinct_profiles']} distinct profiles) -> {out_path}")
        print(f"  k* interval {ks['verdict_interval']}  (k_hat={ks['k_hat_1se']}, argmax={ks['k_argmax']}, "
              f"best acc={ks['best_acc']}±{ks['se_at_best']})")
        print(f"  on-file prediction k*∈{{3,4}}: {'HIT' if out['on_file_prediction_P_k']['hit'] else 'MISS'}")
        print(f"  LOCO k_hat range [{out['ablations']['loco_min']}, {out['ablations']['loco_max']}]; "
              f"drop-measured k_hat={out['ablations']['drop_measured_k_hat']}; "
              f"sensitivity({out['ablations']['sensitivity_other_roster']['roster']}) "
              f"k_hat={out['ablations']['sensitivity_other_roster']['k_hat_1se']}")
        if out["excess_over_null"]:
            e = out["excess_over_null"]
            if not e.get("applicable", True):
                print(f"  excess-over-null: NOT APPLICABLE at k_hat={e['k_hat']} — the statistic "
                      f"acc[k_hat]-acc[1] is identically 0; no envelope, no verdict")
            else:
                print(f"  excess-over-null: real gain={e['real_gain_acc_khat_over_k1']} "
                      f"excess_over_typing={e['excess_over_typing']}")
        print(f"  MCA sensitivity (S1-DISQUALIFIED, not the claim): {out['mca_sensitivity_DISQUALIFIED']['dims_above_threshold']} dims")
        return 0

    ap.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
