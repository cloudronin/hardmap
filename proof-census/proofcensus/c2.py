"""C2 — population metrics + glitch bounds + figures over an n-fixed α-sweep (spec §3.3, §3.4).

For a fixed n, sweeps α ∈ cells, samples K refutations per (sampler, instance), and computes per-cell
population statistics. Reports: H2 trends (length, backbone, overlap) across α with S1-vs-S2 trend agreement
(R1 — trends, not levels), the S1-vs-S1 glitch (noise) bound per metric, province separation, and one figure
per §3.3 row. Metrics that must be per-instance (overlap, backbone) are computed per instance and pooled;
length pools across instances.
"""
from __future__ import annotations

import json
from pathlib import Path

from desertmap import fixtures
from proofcensus import metrics
from proofcensus.sweep import sample_k_parallel

ALPHAS = (4.5, 5.0, 6.0, 8.0, 10.0)


def _median(xs):
    return metrics.median(xs)


def run_c2(n: int = 20, alphas=ALPHAS, n_instances: int = 3, K: int = 100,
           out_dir: str | None = None, n_workers: int | None = None) -> dict:
    out = Path(out_dir or (Path(__file__).parent / "results" / "figures"))
    out.mkdir(parents=True, exist_ok=True)

    # per (sampler, alpha): pooled lengths, per-instance backbone sizes + median-jaccards, pooled overlap qs
    cell: dict = {}
    province_refs: dict = {}   # alpha -> {sampler: refs from instance 0}
    for alpha in alphas:
        for inst in range(n_instances):
            cnf = fixtures.gen_unsat_3sat(n, alpha, fixtures._cell_seed(n, alpha, inst))
            for sampler in ("s1", "s2"):
                refs = sample_k_parallel(cnf, sampler, K, seed=1000 + inst, n_workers=n_workers).refutations
                d = cell.setdefault((sampler, alpha), {"lengths": [], "backbone": [], "jac": [], "qs": []})
                d["lengths"] += metrics.lengths(refs)
                d["backbone"].append(metrics.backbone_size(refs))
                d["jac"].append(_median(metrics.pairwise_jaccards(refs)))
                d["qs"] += metrics.overlap_qs(refs)
                if inst == 0:
                    province_refs.setdefault(alpha, {})[sampler] = refs

    def series(sampler, key, agg):
        return [agg(cell[(sampler, a)][key]) for a in alphas]

    summary = {"n": n, "alphas": list(alphas), "n_instances": n_instances, "K": K, "trends": {}, "glitch": {},
               "province": {}}

    # --- H2 trends + S1-vs-S2 trend agreement (R1) ---
    for key, agg, label in [("lengths", _median, "median_length"),
                            ("backbone", lambda xs: sum(xs) / len(xs), "mean_backbone_size"),
                            ("jac", lambda xs: sum(xs) / len(xs), "mean_median_jaccard")]:
        sa, sb = series("s1", key, agg), series("s2", key, agg)
        agree = metrics.sampler_agreement_trend(list(alphas), sa, sb)
        summary["trends"][label] = {"s1": [round(x, 3) for x in sa], "s2": [round(x, 3) for x in sb],
                                    "trend_s1": agree["trend_a"], "trend_s2": agree["trend_b"],
                                    "agree": agree["agree"]}

    # --- S1-vs-S1 glitch (noise) bound: two independent seed banks on instance 0 of each α (parallel) ---
    metric_fns = {"median_length": lambda r: _median(metrics.lengths(r)) or 0,
                  "backbone_size": lambda r: metrics.backbone_size(r),
                  "median_jaccard": lambda r: _median(metrics.pairwise_jaccards(r)) or 0}
    glitch_gaps = {label: [] for label in metric_fns}
    for alpha in alphas:
        cnf = fixtures.gen_unsat_3sat(n, alpha, fixtures._cell_seed(n, alpha, 0))
        bank_a = sample_k_parallel(cnf, "s1", K, seed=1_000_000, n_workers=n_workers).refutations
        bank_b = sample_k_parallel(cnf, "s1", K, seed=9_000_000, n_workers=n_workers).refutations
        for label, fn in metric_fns.items():
            glitch_gaps[label].append(abs(fn(bank_a) - fn(bank_b)))
    for label in metric_fns:
        summary["glitch"][label] = {"per_alpha_gap": [round(x, 3) for x in glitch_gaps[label]],
                                    "max_gap": round(max(glitch_gaps[label]), 3)}

    # --- province separation per α ---
    for alpha in alphas:
        ps = metrics.province_separation(province_refs[alpha]["s1"], province_refs[alpha]["s2"])
        summary["province"][str(alpha)] = {k: round(v, 3) for k, v in ps.items()}

    # --- figures (one per §3.3 row) ---
    from proofcensus import plots
    plots.plot_length_distributions({a: _mk_refs(cell[("s1", a)]) for a in alphas}, str(out / "length_s1.png"),
                                    title=f"S1 proof length (n={n})")
    plots.plot_length_distributions({a: _mk_refs(cell[("s2", a)]) for a in alphas}, str(out / "length_s2.png"),
                                    title=f"S2 proof length (n={n})")
    _plot_pq_pooled(cell, alphas, "s1", str(out / "pq_s1.png"), n)
    _plot_pq_pooled(cell, alphas, "s2", str(out / "pq_s2.png"), n)
    _plot_backbone(summary, alphas, str(out / "backbone.png"), n)
    plots.plot_province_separation(province_refs_by_alpha(province_refs, "s1"),
                                   province_refs_by_alpha(province_refs, "s2"),
                                   str(out / "province.png"), title=f"Province separation (n={n})")
    (out / "c2_summary.json").write_text(json.dumps(summary, indent=2))
    return summary


# --- helpers: the length figure needs Refutation objects; we only kept lengths, so wrap them minimally ---
class _LenRef:
    __slots__ = ("length",)

    def __init__(self, length):
        self.length = length


def _mk_refs(d):
    return [_LenRef(x) for x in d["lengths"]]


def province_refs_by_alpha(province_refs, sampler):
    return {a: province_refs[a][sampler] for a in province_refs}


def _plot_pq_pooled(cell, alphas, sampler, path, n):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(7, 4))
    for a in sorted(alphas):                              # hard (low α) first in legend
        qs = cell[(sampler, a)]["qs"]
        if qs:
            ax.hist(qs, bins=30, range=(-1, 1), histtype="step", density=True, label=f"α={a}")
    ax.set_xlabel("overlap q = 2·Jaccard − 1"); ax.set_ylabel("density")
    ax.set_title(f"{sampler.upper()} pairwise proof overlap P(q) (n={n})"); ax.legend()
    fig.tight_layout(); fig.savefig(path, dpi=120); plt.close(fig)


def _plot_backbone(summary, alphas, path, n):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    order = sorted(range(len(alphas)), key=lambda i: alphas[i])   # hard (low α) first
    xs = [alphas[i] for i in order]
    s1 = [summary["trends"]["mean_backbone_size"]["s1"][i] for i in order]
    s2 = [summary["trends"]["mean_backbone_size"]["s2"][i] for i in order]
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(range(len(xs)), s1, "o-", label="S1"); ax.plot(range(len(xs)), s2, "s-", label="S2")
    ax.set_xticks(range(len(xs))); ax.set_xticklabels([f"α={a}" for a in xs])
    ax.set_xlabel("← harder (toward threshold)      easier →")
    ax.set_ylabel("mean backbone size (≥0.95)"); ax.set_title(f"Backbone strength (n={n})"); ax.legend()
    fig.tight_layout(); fig.savefig(path, dpi=120); plt.close(fig)


if __name__ == "__main__":
    import sys
    kw = {}
    if len(sys.argv) > 1:
        kw["K"] = int(sys.argv[1])
    if len(sys.argv) > 2:
        kw["n_instances"] = int(sys.argv[2])
    s = run_c2(**kw)
    print(json.dumps(s, indent=2))
