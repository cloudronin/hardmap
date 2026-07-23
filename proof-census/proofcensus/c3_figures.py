"""Render C3 figures from c3_summary.json — one figure per §3.3 metric, S1 vs S2 series across α, per size.

Reads the aggregated summary (not the raw checkpoint), so it's cheap and re-runnable. α axis oriented
hard→easy (low α = toward threshold = left). S1 solid, S2 dashed; one color per n.
"""
from __future__ import annotations

import json
from pathlib import Path

OUT = Path(__file__).parent / "results" / "c3"
COLORS = {"n20": "#1f77b4", "n30": "#2ca02c", "n40": "#ff7f0e", "n60": "#d62728"}


def _plot(metric: str, ylabel: str, title: str, logy: bool = False):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    s = json.loads((OUT / "c3_summary.json").read_text())
    alphas = s["grid"]["alphas"]
    x = list(range(len(alphas)))
    fig, ax = plt.subplots(figsize=(8, 5))
    for nkey in ["n20", "n30", "n40", "n60"]:
        m = s["trends"][nkey][metric]
        c = COLORS[nkey]
        ax.plot(x, m["s1"], "o-", color=c, label=f"{nkey} S1")
        ax.plot(x, m["s2"], "s--", color=c, alpha=0.7, label=f"{nkey} S2")
    ax.set_xticks(x); ax.set_xticklabels([f"α={a}" for a in alphas])
    ax.set_xlabel("← harder (toward threshold)          easier →")
    ax.set_ylabel(ylabel)
    if logy:
        ax.set_yscale("log")
    ax.set_title(title)
    ax.legend(ncol=4, fontsize=8)
    fig.tight_layout()
    path = OUT / f"c3_{metric}.png"
    fig.savefig(path, dpi=120); plt.close(fig)
    return path


def main():
    figs = [
        _plot("mean_backbone", "mean backbone size (clause-ids ≥0.95)",
              "C3 — Backbone strengthens toward threshold (S1 solid, S2 dashed)", logy=True),
        _plot("median_length", "median proof length (resolution steps)",
              "C3 — Proof length lengthens toward threshold", logy=True),
        _plot("mean_jaccard", "mean median pairwise Jaccard",
              "C3 — Proof overlap vs α"),
    ]
    for p in figs:
        print("wrote", p)


if __name__ == "__main__":
    main()
