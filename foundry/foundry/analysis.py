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


def p2_gradient(entries=None, m=1000, seed=X.SEED, n_perm=20000):
    entries = full_census() if entries is None else entries
    _, _, base = S._grid(entries)
    both = _contingency(base)
    real_v = X._both_real_v(base, CA, CB, FOUNDRY_SPEC)
    # S1 null envelope (marginals + n.a. typing + entailment preserved; values swap-shuffled)
    rng = np.random.default_rng(seed)
    null_vs = [X._both_real_v(rows, CA, CB, FOUNDRY_SPEC)
               for rows in X._null_chain(base, rng, X.S1_BURN, X.S1_THIN, m, FOUNDRY_SPEC)]
    env = X._envelope(real_v, null_vs)
    # permutation p — free shuffle of the parameterized column among applicable cells
    idx = [i for i, r in enumerate(base) if r[CB] != "n.a."]
    vals = [base[i][CB] for i in idx]
    arr = [dict(r) for r in base]
    ge = 0
    rv = real_v if real_v == real_v else -1.0
    for _ in range(n_perm):
        perm = rng.permutation(vals)
        for k, i in enumerate(idx):
            arr[i][CB] = perm[k]
        v = X._both_real_v(arr, CA, CB, FOUNDRY_SPEC)
        if v == v and v >= rv:
            ge += 1
    perm_p = (ge + 1) / (n_perm + 1)
    # the affine/XOR deceptive-terrain decoupling witness (hard-approx + easy-param), reproduced from the canon
    xor = next((e for e in entries if e.problem_id == "xor-sat"), None)
    xor_cells = {c.charge: c.value for c in xor.charges} if xor else {}
    return {
        "attack": "P2_gradient_census", "n_both_real": len(both), "both_real_pairs": sorted(set(both)),
        "gradient_v": (round(real_v, 3) if real_v == real_v else None), "perm_p": round(perm_p, 4), "n_perm": n_perm,
        "s1_null_envelope": {k: (round(v, 3) if isinstance(v, float) else v) for k, v in env.items()},
        "beats_null": env["real_above_p97_5"],
        "decoupling_witness": {"xor-sat": {"approximation": xor_cells.get(CA), "parameterized": xor_cells.get(CB)}},
        "rule": ("SURVIVES iff the census approx|param V beats its S1 null (one-sided) AND permutation p<0.05. "
                 "At the v1 census n this is expected to be underpowered/inconclusive (a pre-registered K2 "
                 "outcome). The DIRECTION is the finding: the affine/XOR decoupling (hard-approx + easy-param) "
                 "runs opposite to the canon's positive gradient."),
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
        "attack": "P3_factors_census", "n_rows": len(rows), "n_distinct_profiles": lcm["n_distinct_profiles"],
        "census_k_hat_1se": lcm["k_hat_1se"], "census_interval": lcm["interval"], "census_curve": lcm["curve"],
        "reference_canon": {"k_hat_1se": 1, "note": "canon read k*=1 (Factors v1/v1.1)"},
        "same_world": lcm["k_hat_1se"] <= 1,
        "rule": ("prereg_v2 P3a: SAME-WORLD iff census k*_hat <= 1 (both universes carry no global latent "
                 "dimensionality beyond marginals). At n=13 this is underpowered — a small census is mechanically "
                 "low-dimensional; the meaningful comparison needs Foundry-scale data."),
    }


def run_all(m=1000):
    return {"census": "boolean-coclone(7) + general-domain-|D|=3(6) = 13 rows",
            "noise_floor": noise_floor(), "P2": p2_gradient(m=m), "P3": p3_factors()}
