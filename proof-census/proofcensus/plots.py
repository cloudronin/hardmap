"""Figures — one per spec §3.3 metric row (C2). matplotlib is lazy-imported (the `viz` extra).

Each function takes ``by_alpha``: an ordered dict/list of ``(alpha, [Refutation, ...])`` for a fixed n and
sampler, and writes a figure. α axis is oriented hard-toward-threshold (α descending → left-to-right harder;
Desert Map correction). Comparison across samplers is by TREND, not level (R1) — plot samplers as separate
series, never subtract their levels.
"""
from __future__ import annotations

from proofcensus import metrics


def _sorted_hard_first(by_alpha):
    """Return (alphas, ref_lists) ordered α ascending — hardest (lowest α, nearest threshold) first, so the
    x-axis reads left=harder → right=easier."""
    items = sorted(by_alpha.items(), key=lambda kv: kv[0])
    return [a for a, _ in items], [r for _, r in items]


def plot_length_distributions(by_alpha: dict, out: str, title: str = ""):
    """§3.3 row 1 — proof-length distribution per α (violin; wider/longer toward threshold = H2)."""
    import matplotlib.pyplot as plt
    alphas, refs = _sorted_hard_first(by_alpha)
    data = [metrics.lengths(r) for r in refs]
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.violinplot(data, showmedians=True)
    ax.set_xticks(range(1, len(alphas) + 1))
    ax.set_xticklabels([f"α={a}" for a in alphas])
    ax.set_xlabel("← harder (toward threshold)      easier →")
    ax.set_ylabel("proof length (resolution steps)")
    ax.set_title(title or "Proof-length distribution")
    fig.tight_layout(); fig.savefig(out, dpi=120); plt.close(fig)


def plot_overlap_pq(by_alpha: dict, out: str, title: str = ""):
    """§3.3 row 2 — pairwise overlap P(q) per α (overlaid histograms)."""
    import matplotlib.pyplot as plt
    alphas, refs = _sorted_hard_first(by_alpha)
    fig, ax = plt.subplots(figsize=(7, 4))
    for a, r in zip(alphas, refs):
        qs = metrics.overlap_qs(r)
        if qs:
            ax.hist(qs, bins=30, range=(-1, 1), histtype="step", density=True, label=f"α={a}")
    ax.set_xlabel("overlap q = 2·Jaccard − 1"); ax.set_ylabel("density")
    ax.set_title(title or "Pairwise proof overlap P(q)"); ax.legend()
    fig.tight_layout(); fig.savefig(out, dpi=120); plt.close(fig)


def plot_backbone_strength(by_alpha: dict, out: str, thresh: float = 0.95, title: str = ""):
    """§3.3 row 3 — backbone size vs α (count of clause-ids at frequency ≥ thresh; strengthens = H2)."""
    import matplotlib.pyplot as plt
    alphas, refs = _sorted_hard_first(by_alpha)
    sizes = [metrics.backbone_size(r, thresh) for r in refs]
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(range(len(alphas)), sizes, "o-")
    ax.set_xticks(range(len(alphas))); ax.set_xticklabels([f"α={a}" for a in alphas])
    ax.set_xlabel("← harder (toward threshold)      easier →")
    ax.set_ylabel(f"backbone size (clause-ids ≥ {thresh})")
    ax.set_title(title or "Backbone strength")
    fig.tight_layout(); fig.savefig(out, dpi=120); plt.close(fig)


def plot_province_separation(by_alpha_s1: dict, by_alpha_s2: dict, out: str, title: str = ""):
    """§3.3 row 5 — inter- vs intra-sampler overlap per α (province separation, R1 exploratory finding)."""
    import matplotlib.pyplot as plt
    alphas = sorted(set(by_alpha_s1) & set(by_alpha_s2), key=lambda a: -a)
    intra_a, intra_b, inter = [], [], []
    for a in alphas:
        ps = metrics.province_separation(by_alpha_s1[a], by_alpha_s2[a])
        intra_a.append(ps["intra_a"]); intra_b.append(ps["intra_b"]); inter.append(ps["inter"])
    fig, ax = plt.subplots(figsize=(7, 4))
    xs = range(len(alphas))
    ax.plot(xs, intra_a, "o-", label="intra S1"); ax.plot(xs, intra_b, "s-", label="intra S2")
    ax.plot(xs, inter, "^--", label="inter S1–S2")
    ax.set_xticks(list(xs)); ax.set_xticklabels([f"α={a}" for a in alphas])
    ax.set_ylabel("mean Jaccard"); ax.set_title(title or "Province separation (S1 vs S2)"); ax.legend()
    fig.tight_layout(); fig.savefig(out, dpi=120); plt.close(fig)
