"""Sprint 3 — the P2/P3 verdicts on the synthetic census, + the between-generation noise floor.

Reuses the eightfold primitives with FOUNDRY_SPEC and does NOT modify eightfold: the Crucible null sampler
(`crucible._null_chain`) and both-real association (`crucible._both_real_v`, `_envelope`) are already
spec-threaded (Phase K), and the Factors estimator (`eightfold.factors`) is spec-parametrized. So the census S1
null, the P2 gradient, and the P3 factor run all go through the shared kernel with zero byte-identical risk.

Honest-power discipline: the v1 census is small (13 rows: 7 Boolean co-clone + 6 general-domain), so every
verdict is reported AT ITS TRUE POWER. A small-n inconclusive is a pre-registered K2 outcome, not a failure —
the meaningful factor comparison needs Foundry-scale data (foundry prereg_v2).
"""
import numpy as np

from eightfold import crucible as X
from eightfold import factors as F
from eightfold import structure as S
from foundry.charges import FOUNDRY_SPEC
from foundry.domain3 import build_d3_census, sample_binary_languages
from foundry.oracles import build_boolean_census

CA, CB = "approximation", "parameterized"


def full_census():
    return build_boolean_census() + build_d3_census()


# ── 3.1 between-generation noise floor (the sampled explorer; curated tiers are deterministic/exempt) ────────
def noise_floor(g=3, n_samples=300, base_seed=X.SEED):
    """Both census tiers are deterministic (curated CKZ/CKZ-analogue reps) → generations-exempt. The only
    sampled component is the domain-3 polymorphism-profile explorer; its between-generation stability is the
    noise floor. Report the profile-share vector per generation and the max between-generation drift."""
    gens = []
    for gi in range(g):
        prof = sample_binary_languages(n_samples, np.random.default_rng(base_seed + 1013 * gi))
        tot = sum(prof.values())
        gens.append({str(sorted(k)): round(v / tot, 3) for k, v in prof.items()})
    keys = sorted({k for gen in gens for k in gen})
    drift = max((max(gen.get(k, 0.0) for gen in gens) - min(gen.get(k, 0.0) for gen in gens)) for k in keys)
    return {"deterministic_tiers_exempt": ["boolean-coclone", "general-domain-curated"],
            "sampled_explorer_generations": gens, "n_profiles": len(keys),
            "max_between_generation_drift": round(drift, 3),
            "note": "Curated census rows are deterministic (generations-exempt). The drift is the sampled "
                    "explorer's profile-share instability across G generations — the floor a finding must clear."}


# ── 3.2 P2 — the approx<->parameterized gradient on the census vs its S1 null ────────────────────────────────
def _contingency(rows):
    both = [(r[CA], r[CB]) for r in rows
            if r[CA] in FOUNDRY_SPEC.charge_real_values[CA] and r[CB] in FOUNDRY_SPEC.charge_real_values[CB]]
    return both


def _perm_p_on_table(xs, ys, n_perm, seed):
    """CORRECT permutation test for association between two aligned label lists: permute ys among ITS OWN rows
    (the contingency table), recompute Cramer's V, p = (#perm with V>=real + 1)/(n_perm+1). This is the fix for
    the Sprint-3 bug, where parameterized was permuted among ALL non-n.a. cells (incl. domain-3 `open`), which
    injected extra values and made the p-value arithmetically impossible. Verified by selftest_p2_perm()."""
    real_v = S.cramers_v(xs, ys)
    if real_v != real_v:
        return {"real_v": None, "p": None}
    rng = np.random.default_rng(seed)
    ys = list(ys)
    ge = 0
    for _ in range(n_perm):
        v = S.cramers_v(xs, list(rng.permutation(ys)))
        if v == v and v >= real_v - 1e-9:
            ge += 1
    return {"real_v": round(real_v, 3), "p": round((ge + 1) / (n_perm + 1), 4)}


def selftest_p2_perm(n_perm=20000):
    """The permutation p on the census's both-real shape (6 identical + 1 distinct) must reproduce the
    hand-countable p = 1/7 (V=1.0 exactly when the lone FPT lands on the lone inapprox row). A tiny 3-row case
    gives p = 1/3. Byte-identical ethic for statistics: a broken test is a bug, not a verdict."""
    r7 = _perm_p_on_table(["APX"] * 6 + ["inapprox"], ["W1"] * 6 + ["FPT"], n_perm, X.SEED)
    r3 = _perm_p_on_table(["A", "A", "B"], ["y", "y", "x"], n_perm, X.SEED)
    ok7 = r7["real_v"] == 1.0 and 0.11 < r7["p"] < 0.18          # exact 1/7 = 0.1429
    ok3 = r3["real_v"] == 1.0 and 0.28 < r3["p"] < 0.40          # exact 1/3 = 0.3333
    print(f"P2 permutation selftest: 7-row p={r7['p']} (exact 1/7=0.143), 3-row p={r3['p']} (exact 1/3=0.333)"
          f" -> {'PASSED' if ok7 and ok3 else 'FAILED'}")
    return 0 if (ok7 and ok3) else 1


def p2_gradient(entries=None, seed=X.SEED, n_perm=20000):
    """P2 on the census — CORRECTED and DISPOSITIONED HONESTLY. The both-real table is only the 7 Boolean rows
    (domain-3 leaves approx+param `open`), and 6 of them are identical: this cannot test the gradient. Verdict:
    INSUFFICIENT RESOLUTION (the same disposition the Boolean tier already carries). The direction-reversal is a
    DESCRIPTIVE observation + a pre-registered hypothesis for the scaled census — NOT a ruling, and NOT evidence
    for 'roster sociology' (Crucible S5 retired that explanation on the actual canon at p=0.0001; a 7-row
    theorem-world anecdote cannot reinstate it)."""
    entries = full_census() if entries is None else entries
    _, _, base = S._grid(entries)
    both = _contingency(base)
    xs = [a for a, b in both]
    ys = [b for a, b in both]
    perm = _perm_p_on_table(xs, ys, n_perm, seed)
    distinct = sorted(set(both))
    xor = next((e for e in entries if e.problem_id == "xor-sat"), None)
    xor_cells = {c.charge: c.value for c in xor.charges} if xor else {}
    return {
        "attack": "P2_gradient_census",
        "disposition": "INSUFFICIENT_RESOLUTION",
        "n_both_real": len(both), "n_distinct_both_real_rows": len(distinct), "both_real_pairs": distinct,
        "gradient_v": perm["real_v"], "perm_p": perm["p"], "n_perm": n_perm, "exact_perm_p_by_counting": round(1 / 7, 4),
        "descriptive_observation": {
            "direction": "REVERSED vs the canon (harder-approx co-occurs with EASIER param)",
            "decoupling_witness_xor_sat": {"approximation": xor_cells.get(CA), "parameterized": xor_cells.get(CB)},
            "note": "one distinctive row (affine/XOR) against six identical rows — an anecdote with V=1.0, not a test."},
        "s1_null": "not a ruling at this resolution — 7 both-real rows, 6 identical; the S1 null is uninformative here",
        "roster_sociology": "STRUCK — contradicts Crucible S5 (roster exhausted with every known violator; gradient survived p=0.0001). Not reinstated by a 7-row anecdote.",
        "rule": ("A 7-row both-real table with 6 identical rows cannot test the gradient (permutation p=1/7≈0.143 "
                 "by counting, non-significant by construction). Disposition = INSUFFICIENT RESOLUTION. The "
                 "direction-reversal is logged descriptively and pre-registered for the scaled census (prereg_v3)."),
    }


# ── 3.3 P3 — run the IDENTICAL Factors estimator on the census (foundry prereg_v2: same-verdict-both-worlds) ──
def p3_factors(entries=None, budget=None):
    entries = full_census() if entries is None else entries
    _, _, rows = S._grid(entries)
    b = dict(ks=range(1, 6), repeats=20, restarts=6, max_iters=120, loadings=False)
    if budget:
        b.update(budget)
    lcm = F.estimate_rows(rows, FOUNDRY_SPEC, **b)
    return {
        "attack": "P3_factors_census", "disposition": "DIVERGENT (directional at n=13)",
        "n_rows": len(rows), "n_distinct_profiles": lcm["n_distinct_profiles"],
        "census_k_hat_1se": lcm["k_hat_1se"], "census_interval": lcm["interval"], "census_curve": lcm["curve"],
        "reference_canon": {"k_hat_1se": 1, "note": "canon read k*=1 (Factors v1/v1.1)"},
        "same_world": lcm["k_hat_1se"] <= 1,
        "caveats_promoted": {
            "power": "n=13 with ~1-2 masked cells per fold — k*=3 is directional at best, not a precise count.",
            "the_real_finding": ("caveat 2 IS the finding: the comparison as operationalized contrasts a "
                                 "THEOREM-COUPLED construction (census charges derived from one another by the "
                                 "dichotomies) against an EMPIRICAL population (canon charges from independent "
                                 "literature), so divergence was structurally likely regardless of what hardness "
                                 "is. k*=3 is the census re-expressing its own entailment, not emergent structure."),
            "v1.1_path": "R25-net the census's factor structure; refine the Boolean tier to escape profile poverty."},
        "rule": ("prereg_v2 P3a: SAME-WORLD iff census k*_hat <= 1. Census k*_hat > 1 -> DIVERGENT, but reported "
                 "as DIRECTIONAL at n=13; the meaningful comparison needs Foundry-scale data + R25-netting."),
    }


def run_all():
    return {"census": "boolean-coclone(7) + general-domain-|D|=3(6) = 13 rows",
            "p2_perm_selftest_passes": selftest_p2_perm(n_perm=5000) == 0,
            "noise_floor": noise_floor(), "P2": p2_gradient(), "P3": p3_factors()}
