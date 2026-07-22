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
    ap.add_argument("--s1", action="store_true", help="S1 null model on the real atlas (needs prereg_v6 locked)")
    ap.add_argument("--path", type=Path, default=None, help="atlas path (default: the bundled atlas)")
    ap.add_argument("--out", type=Path, default=None, help="write crucible_results.json here")
    args = ap.parse_args(argv if argv is not None else sys.argv[1:])

    if args.selftest:
        return selftest()

    if args.s1:
        from eightfold.atlas import DEFAULT_PATH, load_atlas
        out = {"crucible": True, "prereg": "prereg_v6", "S1": s1_null_model(load_atlas(args.path))}
        out_path = args.out or (DEFAULT_PATH.parent / "crucible_results.json")
        out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
        s1 = out["S1"]
        ap_env = s1["envelope"]["approx_param_v"]
        print(f"S1 null model (M={s1['M']}) → {s1['verdict']}  written to {out_path}")
        print(f"  gradient excess over typing: {s1['gradient_excess_over_typing']} "
              f"(real V={s1['real']['approx_param_v']}, null p97.5={ap_env['null_p97.5']})")
        print(f"  dims excess over typing:     {s1['dims_excess_over_typing']}")
        return 0

    ap.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
