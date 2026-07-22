"""Crucible (Eightfold v1.1) — adversarial self-review harness.

Runs the five referee attacks (S1–S5) on the frozen charge atlas. Each resolves a pre-registered
boolean — SURVIVES (hardens the claim) or RESIZED (amends A4 honestly) — whose criterion is locked in
`prereg_v6.json` BEFORE any real-data run. This module adds no new statistics of its own: it reuses the
`structure.py` primitives (`mca`, `complete_case`, `cramers_v`, `cluster_subspaces`) and only supplies
the resamplers (null model, permutation, bootstrap) and the roster surgery (dedup, violator additions).

Behind the `[analysis]` extra (numpy at module top, like structure.py). Core stays stdlib-only.

V1 status: S1 (null model) + toy self-test are implemented and validated. S2–S5 land in V2–V3 once
prereg_v6 is committed.
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np

from eightfold import charges as C
from eightfold import structure as S

SEED = 20260721            # fixed for reproducibility (prereg discipline; no wall-clock/entropy)
S1_M = 1000               # number of null atlases
S1_BURN = 5000            # swap-chain burn-in steps
S1_THIN = 500             # swap steps between recorded samples


# ── entailment-valid, marginal-preserving null (S1) ──────────────────────────────────────────────────────
def _row_valid(row):
    """A row is entailment-valid iff its real-valued cells trip no column-forbidding rule (E1, E2)."""
    assign = {c: v for c, v in row.items() if c in C.CHARGES and v not in C.SENTINELS}
    return not C.theorem_forbidden_by(assign)


def _null_chain(base_rows, rng, burn, thin, m):
    """Swap-chain MCMC over the space of entailment-valid tables that PRESERVE every per-charge marginal
    exactly and hold each row's `n.a.` typing fixed (R1). A proposal swaps two applicable cells within one
    charge and is accepted iff both affected rows stay valid — so marginals never change and E1/E2 always
    hold. Rejection sampling of whole tables would be ~100% here (E1 couples counting↔decision densely),
    which is why the spec's I1 fallback — per-charge swap-chains — is the primary sampler. Yields m tables.
    """
    state = [dict(r) for r in base_rows]
    applic = {ch: [i for i, r in enumerate(state) if r[ch] != "n.a."] for ch in C.CHARGES}
    swappable = [ch for ch in C.CHARGES if len(applic[ch]) >= 2]

    def step():
        ch = swappable[int(rng.integers(len(swappable)))]
        a, b = (int(x) for x in rng.choice(applic[ch], 2, replace=False))
        if state[a][ch] == state[b][ch]:
            return
        state[a][ch], state[b][ch] = state[b][ch], state[a][ch]
        if not (_row_valid(state[a]) and _row_valid(state[b])):
            state[a][ch], state[b][ch] = state[b][ch], state[a][ch]  # reject → revert

    for _ in range(burn):
        step()
    for _ in range(m):
        for _ in range(thin):
            step()
        yield [dict(r) for r in state]


# ── the battery (identical stats on the real atlas and each null) ────────────────────────────────────────
def _both_real_v(rows, ca, cb):
    """Cramér's V over rows where BOTH charges carry a real value (the R25 both-real convention)."""
    xs = [(r[ca], r[cb]) for r in rows
          if r[ca] in C.CHARGE_REAL_VALUES[ca] and r[cb] in C.CHARGE_REAL_VALUES[cb]]
    if len(xs) < 4:
        return float("nan")
    return S.cramers_v([x for x, _ in xs], [y for _, y in xs])


def _battery(ids, families, rows):
    """The structural statistics S1 compares real-vs-null: effective dims (full + complete-case), the
    approx⟷param gradient, and the two witness amplifications (Δ = in-subspace − full-8 distance)."""
    full = S.mca(rows, C.CHARGES)["dims_above_threshold"]
    cc_rows, cc_charges = S.complete_case(rows)
    cc = S.mca(cc_rows, cc_charges)["dims_above_threshold"]
    v = _both_real_v(rows, "approximation", "parameterized")
    try:
        amp = S.cluster_subspaces(ids, families, rows)
    except Exception:
        amp = {}

    def delta(key):
        p = amp.get(key) or {}
        ds, df = p.get("dist_subspace"), p.get("dist_full8")
        return (ds - df) if (ds is not None and df is not None) else None

    return {
        "mca_full_dims": full, "mca_cc_dims": cc, "cc_n": len(cc_rows),
        "approx_param_v": (v if v == v else None),   # nan → None
        "amp_permdet": delta("permanent|determinant"),
        "amp_vcclique": delta("vertex-cover|clique"),
    }


def _envelope(real_val, null_vals):
    """Where the real statistic sits vs the null distribution: the 95% envelope [p2.5, p97.5], a one-sided
    high flag (structure ABOVE typing — for the gradient), and a two-sided flag (for the dims)."""
    vals = [x for x in null_vals if x is not None and x == x]
    if real_val is None or real_val != real_val or len(vals) < 2:
        return {"real": real_val, "null_mean": None, "null_p2.5": None, "null_p97.5": None,
                "real_above_p97_5": None, "real_outside_95": None, "one_sided_p_ge": None}
    p2, p97 = float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))
    return {
        "real": real_val, "null_mean": float(np.mean(vals)), "null_p2.5": p2, "null_p97.5": p97,
        "real_above_p97_5": bool(real_val > p97),
        "real_outside_95": bool(real_val < p2 or real_val > p97),
        "one_sided_p_ge": float(np.mean([1.0 if x >= real_val else 0.0 for x in vals])),
    }


def s1_null_model(entries, m=S1_M, seed=SEED, burn=S1_BURN, thin=S1_THIN):
    """S1 — the load-bearing attack. Compare the real atlas's structure to M type-respecting,
    marginal-preserving, entailment-valid nulls. SURVIVES iff the gradient exceeds the null envelope
    (one-sided) AND the complete-case dims fall outside it (two-sided): structure in excess of typing."""
    ids, families, base = S._grid(entries)
    real = _battery(ids, families, base)
    rng = np.random.default_rng(seed)
    nulls = [_battery(ids, families, rows) for rows in _null_chain(base, rng, burn, thin, m)]

    stats = ["mca_full_dims", "mca_cc_dims", "approx_param_v", "amp_permdet", "amp_vcclique"]
    env = {s: _envelope(real[s], [n[s] for n in nulls]) for s in stats}
    gradient_excess = env["approx_param_v"]["real_above_p97_5"]
    dims_excess = env["mca_cc_dims"]["real_outside_95"]
    survives = bool(gradient_excess and dims_excess)
    return {
        "attack": "S1_null_model", "M": m, "seed": seed,
        "rule": ("SURVIVES iff the real approx|param V exceeds the null 97.5th pct (one-sided) AND the "
                 "real complete-case dims fall outside the null 95% envelope — structure beyond typing."),
        "verdict": "SURVIVES" if survives else "RESIZED",
        "gradient_excess_over_typing": gradient_excess,
        "dims_excess_over_typing": dims_excess,
        "envelope": env, "real": real,
    }


# ── S2: reduction-equivalence dedup (read gradient-first — Rider 2) ──────────────────────────────────────
# Non-representative members of the prereg_v6 merge classes, dropped to form the 114-class deduped roster.
_S2_DROP = frozenset({"independent-set", "vertex-cover", "planar-vertex-cover", "set-cover"})


def _perm_p_gradient(rows, n_perm, rng):
    """Permutation p for the approx|param gradient. FREE shuffle of the parameterized column among applicable
    cells (Rider B: no forbidding rule touches `parameterized`, so no permutation can forge a forbidden
    table). p = (#perms with V >= real + 1)/(n_perm + 1)."""
    real = _both_real_v(rows, "approximation", "parameterized")
    idx = [i for i, r in enumerate(rows) if r["parameterized"] != "n.a."]
    vals = [rows[i]["parameterized"] for i in idx]
    arr = [dict(r) for r in rows]
    ge = 0
    for _ in range(n_perm):
        perm = rng.permutation(vals)
        for k, i in enumerate(idx):
            arr[i]["parameterized"] = perm[k]
        if _both_real_v(arr, "approximation", "parameterized") >= real:
            ge += 1
    return {"real_v": float(real), "p": (ge + 1) / (n_perm + 1), "n_perm": n_perm}


def _amp_deltas(ids, families, rows, keys=("permanent|determinant", "vertex-cover|clique")):
    out = {}
    try:
        cs = S.cluster_subspaces(ids, families, rows)
    except Exception:
        cs = {}
    for k in keys:
        p = cs.get(k) or {}
        ds, df = p.get("dist_subspace"), p.get("dist_full8")
        out[k] = (ds - df) if (ds is not None and df is not None) else None
    return out


def s2_dedup(entries, n_perm=10000, seed=SEED):
    """S2 — rerun on one representative per reduction-equivalence class. Gradient-first: SURVIVES iff the
    deduped gradient stays present AND significant. Multiplet amplifications reported (bias-caveated)."""
    full_rows = S._grid(entries)[2]
    dedup = [e for e in entries if e.problem_id not in _S2_DROP]
    ids, families, rows = S._grid(dedup)
    rng = np.random.default_rng(seed)
    full_v = _both_real_v(full_rows, "approximation", "parameterized")
    ded = _perm_p_gradient(rows, n_perm, rng)
    gradient_survives = bool(ded["p"] < 0.05 and ded["real_v"] >= 0.5)
    return {
        "attack": "S2_dedup", "n_classes": len(dedup), "dropped": sorted(_S2_DROP),
        "rule": ("Read gradient-first (Rider 2). SURVIVES iff the deduped gradient stays present (V >= 0.5) "
                 "AND significant (permutation p < 0.05). vertex-cover/clique is merged away, so its "
                 "amplification cannot be tested here; permanent/determinant is reported but inherits the "
                 "S1 bias caveat (not gated)."),
        "verdict": "SURVIVES" if gradient_survives else "RESIZED",
        "gradient_full_v": float(full_v), "gradient_dedup_v": ded["real_v"], "gradient_dedup_p": ded["p"],
        "multiplet_amplifications_dedup_caveated": _amp_deltas(ids, families, rows),
    }


# ── S3: significance + stability (read gradient-first — Rider 2) ──────────────────────────────────────────
def _bootstrap(entries, n_boot, rng):
    ids, families, base = S._grid(entries)
    n = len(base)
    dims_ge3, dims_vals = 0, []
    pd_pos = pd_tot = vc_pos = vc_tot = 0
    for _ in range(n_boot):
        pick = [int(i) for i in rng.integers(0, n, n)]
        b = _battery([ids[i] for i in pick], [families[i] for i in pick], [base[i] for i in pick])
        dims_vals.append(b["mca_cc_dims"])
        dims_ge3 += (b["mca_cc_dims"] >= 3)
        if b["amp_permdet"] is not None:
            pd_tot += 1
            pd_pos += (b["amp_permdet"] > 0)
        if b["amp_vcclique"] is not None:
            vc_tot += 1
            vc_pos += (b["amp_vcclique"] > 0)
    return {
        "n_boot": n_boot, "cc_dims_ge3_frac": dims_ge3 / n_boot, "cc_dims_median": float(np.median(dims_vals)),
        "permdet_amp_pos_frac_where_present": (pd_pos / pd_tot if pd_tot else None),
        "permdet_present_frac": pd_tot / n_boot,
        "vcclique_amp_pos_frac_where_present": (vc_pos / vc_tot if vc_tot else None),
        "vcclique_present_frac": vc_tot / n_boot,
    }


def s3_significance(entries, n_perm=10000, n_boot=1000, seed=SEED):
    """S3 — the p-value the atlas never had, plus bootstrap stability. Gradient-first: the verdict gates on
    the gradient permutation p; dims stability documents the 'not scalar' claim; amplification bootstrap is
    reported with the S1 bias caveat (not gated)."""
    ids, families, rows = S._grid(entries)
    rng = np.random.default_rng(seed)
    grad = _perm_p_gradient(rows, n_perm, rng)
    boot = _bootstrap(entries, n_boot, rng)
    gradient_survives = bool(grad["p"] < 0.05)
    return {
        "attack": "S3_significance",
        "rule": ("Read gradient-first (Rider 2). GRADIENT SURVIVES iff permutation p < 0.05. Complete-case "
                 "dims >=3 bootstrap fraction documents the 'not scalar' claim. Amplification bootstrap is "
                 "reported with the S1 bias caveat (not gated)."),
        "verdict": "SURVIVES" if gradient_survives else "RESIZED",
        "gradient_perm_p": grad["p"], "gradient_real_v": grad["real_v"], "n_perm": n_perm,
        "dims_bootstrap": {"cc_dims_ge3_frac": boot["cc_dims_ge3_frac"], "cc_dims_median": boot["cc_dims_median"],
                           "stable_ge_95pct": bool(boot["cc_dims_ge3_frac"] >= 0.95)},
        "amplification_bootstrap_caveated": {k: v for k, v in boot.items() if "amp" in k or "present" in k},
    }


# ── toy atlases for the V1 self-test (planted structure vs pure null) ────────────────────────────────────
def _toy_entry(pid, dec, cnt, apx, par):
    from eightfold.atlas import ChargeCell, ProblemEntry
    def rc(ch, val, persp=None):
        return ChargeCell(ch, val, f"toy {ch}", "claimed", {"citation": "toy"}, persp)
    def na(ch):
        return ChargeCell(ch, "n.a.", "n/a", "structural")
    cells = [rc("decision", dec), rc("counting", cnt), rc("approximation", apx),
             rc("parameterized", par, "k"), na("parallelization"), na("proof_size"),
             na("average_case"), na("landscape")]
    return ProblemEntry(pid, pid, "graph", "enc", cells, "2026-07-21", "toy")


def _planted_toy(n_each=8):
    """approximation ⟷ parameterized in perfect lock-step → a strong gradient the null must destroy."""
    aligned = [("APX-complete", "FPT"), ("inapprox", "W[1]"), ("log-APX", "W[2]+")]
    decs = ["NPC", "coNP-complete", "PSPACE-complete"]  # counting=#P-complete keeps every row E1-valid
    return [_toy_entry(f"planted-{k}-{i}", decs[(k + i) % 3], "#P-complete", apx, par)
            for k, (apx, par) in enumerate(aligned) for i in range(n_each)]


def _null_toy(cycles=2):
    """approximation and parameterized varied INDEPENDENTLY (all 9 combos equally) → no real gradient."""
    apxs, pars = ["APX-complete", "inapprox", "log-APX"], ["FPT", "W[1]", "W[2]+"]
    decs = ["NPC", "coNP-complete", "PSPACE-complete"]
    return [_toy_entry(f"null-{c}-{i}", decs[i % 3], "#P-complete", apxs[i % 3], pars[(i // 3) % 3])
            for c in range(cycles) for i in range(9)]


def selftest():
    """V1 gate: the S1 harness must DETECT the planted gradient (real above the null envelope) and find
    NONE in the pure-null toy (real inside the envelope). Small M/burn/thin — this is a wiring check."""
    rp = s1_null_model(_planted_toy(), m=200, burn=800, thin=60)
    rn = s1_null_model(_null_toy(), m=200, burn=800, thin=60)
    planted_detected = rp["gradient_excess_over_typing"] is True
    null_quiet = rn["gradient_excess_over_typing"] is False
    print("S1 self-test:")
    print(f"  planted toy: real V={rp['real']['approx_param_v']:.2f} vs null p97.5="
          f"{rp['envelope']['approx_param_v']['null_p97.5']:.2f} → detected={planted_detected}")
    print(f"  null toy:    real V={rn['real']['approx_param_v']:.2f} vs null p97.5="
          f"{rn['envelope']['approx_param_v']['null_p97.5']:.2f} → detected="
          f"{rn['gradient_excess_over_typing']}")
    ok = planted_detected and null_quiet
    print(f"  self-test {'PASSED' if ok else 'FAILED'} (planted detected AND null quiet)")
    return 0 if ok else 1


# ── CLI ──────────────────────────────────────────────────────────────────────────────────────────────────
def main(argv=None):
    ap = argparse.ArgumentParser(prog="eightfold.crucible")
    ap.add_argument("--selftest", action="store_true", help="V1 gate: validate S1 on planted + null toys")
    ap.add_argument("--s1", action="store_true", help="S1 null model (needs prereg_v6 locked)")
    ap.add_argument("--s2", action="store_true", help="S2 reduction-equivalence dedup rerun")
    ap.add_argument("--s3", action="store_true", help="S3 permutation p-value + bootstrap stability")
    ap.add_argument("--path", type=Path, default=None, help="atlas path (default: the bundled atlas)")
    ap.add_argument("--out", type=Path, default=None, help="write crucible_results.json here")
    args = ap.parse_args(argv if argv is not None else sys.argv[1:])

    if args.selftest:
        return selftest()

    if args.s1 or args.s2 or args.s3:
        from eightfold.atlas import DEFAULT_PATH, load_atlas
        entries = load_atlas(args.path)
        out_path = args.out or (DEFAULT_PATH.parent / "crucible_results.json")
        out = json.loads(out_path.read_text(encoding="utf-8")) if out_path.exists() else {}
        out.update({"crucible": True, "prereg": "prereg_v6"})
        if args.s1:
            out["S1"] = s1_null_model(entries)
        if args.s2:
            out["S2"] = s2_dedup(entries)
        if args.s3:
            out["S3"] = s3_significance(entries)
        out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Crucible results written to {out_path}")
        if args.s1:
            s1 = out["S1"]
            print(f"  S1 null model (M={s1['M']}) → {s1['verdict']}  [gradient excess="
                  f"{s1['gradient_excess_over_typing']} (V={s1['real']['approx_param_v']:.2f} vs null p97.5="
                  f"{s1['envelope']['approx_param_v']['null_p97.5']:.2f}), dims excess={s1['dims_excess_over_typing']}]")
        if args.s2:
            s2 = out["S2"]
            print(f"  S2 dedup ({s2['n_classes']} classes) → {s2['verdict']}  [gradient full V="
                  f"{s2['gradient_full_v']:.2f} → dedup V={s2['gradient_dedup_v']:.2f}, p={s2['gradient_dedup_p']:.4f}]")
        if args.s3:
            s3 = out["S3"]
            print(f"  S3 significance → {s3['verdict']}  [gradient perm p={s3['gradient_perm_p']:.4f} "
                  f"(V={s3['gradient_real_v']:.2f}); dims>=3 in "
                  f"{s3['dims_bootstrap']['cc_dims_ge3_frac'] * 100:.0f}% of bootstraps]")
        return 0

    ap.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
