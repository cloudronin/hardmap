"""`hardmap verify` -- the H4 internal-coherence sweep (spec section 3.5, check 2).

One script over the persisted results asserting invariants that must hold
regardless of the numbers: Cramér's V in [0,1], point estimates inside their CIs,
marginals summing to n, netted <= raw where a theorem forces it. Grows a check per
artifact family; exits nonzero on any violation. This ships as a permanent command.
"""
from __future__ import annotations

import json
from pathlib import Path

import eightfold


def _eightfold_atlas() -> Path:
    return Path(eightfold.__file__).resolve().parent / "results" / "atlas"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def check_cramers_v_range() -> list[str]:
    """Every reported Cramér's V lies in [0, 1]."""
    bad = []
    a3 = _load(_eightfold_atlas() / "a3_structure.json")
    for pair, v in a3.get("cramers_v", {}).items():
        if not 0.0 <= float(v) <= 1.0:
            bad.append(f"a3 cramers_v[{pair}] = {v} outside [0,1]")
    cr = _load(_eightfold_atlas() / "crucible_results.json")
    for key in ("gradient_full_v", "gradient_dedup_v"):
        v = cr.get("S2", {}).get(key)
        if v is not None and not 0.0 <= float(v) <= 1.0:
            bad.append(f"crucible S2.{key} = {v} outside [0,1]")
    return bad


def check_factors_kstar_interval() -> list[str]:
    """k* point estimate sits inside its own reported verdict interval and is >= 1."""
    bad = []
    ks = _load(_eightfold_atlas() / "factors_v1.json")["k_star"]
    if ks["k_hat_1se"] not in ks["verdict_interval"]:
        bad.append(f"factors k_hat_1se {ks['k_hat_1se']} not in verdict_interval {ks['verdict_interval']}")
    if ks["k_hat_1se"] < 1:
        bad.append(f"factors k_hat_1se {ks['k_hat_1se']} < 1")
    return bad


def check_netted_le_raw() -> list[str]:
    """Cai-Chen residual audit: netted association <= raw where the theorem forces it."""
    bad = []
    a3 = _load(_eightfold_atlas() / "a3_structure.json")
    audit = a3.get("H2_multiplets", {}).get("cai_chen_bridge_audit_R25", {})
    raw = audit.get("raw", {}).get("v")
    for level in ("conservative", "aggressive", "extreme_floor_delete_whole_cell"):
        netted = audit.get(level, {}).get("v")
        if raw is not None and netted is not None and float(netted) > float(raw) + 1e-9:
            bad.append(f"netted[{level}] {netted} > raw {raw}")
    return bad


def check_estimates_in_cis() -> list[str]:
    """Point estimates lie inside their own reported bootstrap CIs."""
    import foundry
    lat_dir = Path(foundry.__file__).resolve().parent / "results" / "lattice"
    bad = []
    lat = _load(lat_dir / "lattice_v3_occupancy.json")
    v = lat["cramers_v"]
    lo, hi = lat["cramers_v_boot_ci95_sized_to_classes"]
    if not lo <= v <= hi:
        bad.append(f"lattice_v3 V {v:.4f} not in CI [{lo}, {hi}]")
    mo = _load(lat_dir / "prism_v2_matrix.json")["pred5_anti_canon"]["min_ones"]
    pt = mo["spearman_point_corrected"]
    clo, chi = mo["boot_ci95_classes_corrected"]
    if not clo <= pt <= chi:
        bad.append(f"prism_v2 corrected Spearman {pt} not in CI [{clo}, {chi}]")
    return bad


def check_census_jaccard_sane() -> list[str]:
    """Every committed median Jaccard lies in [0,1] and below the 0.95 plurality line."""
    import proofcensus
    c3 = _load(Path(proofcensus.__file__).resolve().parent / "results" / "c3" / "c3_summary.json")
    bad = []
    for nkey, trend in c3.get("trends", {}).items():
        for series in ("s1", "s2"):
            for j in trend.get("mean_jaccard", {}).get(series, []):
                if j is None:
                    continue
                if not 0.0 <= j <= 1.0:
                    bad.append(f"{nkey} mean_jaccard.{series} {j} outside [0,1]")
                elif j >= 0.95:
                    bad.append(f"{nkey} mean_jaccard.{series} {j} >= 0.95 (would imply plurality)")
    return bad


def check_marginals_sum_to_n() -> list[str]:
    """Lattice v3 contingency marginals and occupancy cells each sum to n_both_real."""
    import foundry
    lat = _load(Path(foundry.__file__).resolve().parent / "results" / "lattice" / "lattice_v3_occupancy.json")
    n = lat["n_both_real"]
    bad = []
    if sum(lat["param_marginal"].values()) != n:
        bad.append(f"param_marginal sums to {sum(lat['param_marginal'].values())}, not n_both_real={n}")
    if sum(lat["occupancy"].values()) != n:
        bad.append(f"occupancy cells sum to {sum(lat['occupancy'].values())}, not n_both_real={n}")
    return bad


CHECKS = [
    ("Cramér's V in [0,1]", check_cramers_v_range),
    ("Factors k* inside verdict interval", check_factors_kstar_interval),
    ("Netted association <= raw (Cai-Chen)", check_netted_le_raw),
    ("Point estimates inside their CIs", check_estimates_in_cis),
    ("Census Jaccard in [0,1] and below plurality line", check_census_jaccard_sane),
    ("Contingency marginals sum to n", check_marginals_sum_to_n),
]


def run() -> int:
    n_fail = 0
    for name, fn in CHECKS:
        try:
            problems = fn()
        except Exception as exc:  # noqa: BLE001
            problems = [f"{type(exc).__name__}: {exc}"]
        ok = not problems
        n_fail += not ok
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")
        for p in problems:
            print(f"        {p}")
    print(f"\n{len(CHECKS) - n_fail}/{len(CHECKS)} coherence checks passed")
    return 1 if n_fail else 0
