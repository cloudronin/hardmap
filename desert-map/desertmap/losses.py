"""Loss terms + annealing schedules for the soft-resolution relaxation (M2).

Total loss (minimized independently per seed): ``w1·validity + w2·termination + w3(s)·entropy``, with a
temperature ``tau`` annealed geometrically and the entropy weight ``w3`` ramped in after the validity /
termination terms have had time to dominate.
"""
from __future__ import annotations

import torch

from desertmap.relax import Aux


def _softmin(stacked: torch.Tensor, beta: float, dim: int) -> torch.Tensor:
    """Differentiable soft-min: ``-1/beta · logsumexp(-beta · x)`` along ``dim`` (→ min as beta→∞)."""
    return -torch.logsumexp(-beta * stacked, dim=dim) / beta


def validity_residual(aux: Aux, n: int, beta: float) -> torch.Tensor:
    """Per-seed mean over steps of the pivot-orientation violation (soft-min over the two orientations).

    For pivot distribution q and soft parents P1, P2: orientation A wants ``+pivot`` in P1 and ``-pivot`` in
    P2; orientation B is the mirror. Residual = soft-min of the two orientations' total missing mass.
    """
    res = []
    for P1, P2, q in zip(aux.P1, aux.P2, aux.q):
        a = (q * P1[:, :n]).sum(-1)          # +pivot mass in parent 1
        b = (q * P2[:, n:]).sum(-1)          # -pivot mass in parent 2
        c = (q * P1[:, n:]).sum(-1)          # -pivot mass in parent 1 (other orientation)
        d = (q * P2[:, :n]).sum(-1)          # +pivot mass in parent 2
        orient = torch.stack([(1 - a) + (1 - b), (1 - c) + (1 - d)], dim=-1)  # [R, 2]
        res.append(_softmin(orient, beta, dim=-1))
    return torch.stack(res, dim=-1).mean(-1)  # [R]


def termination_distance(aux: Aux, beta: float) -> torch.Tensor:
    """Per-seed soft-min over steps of the derived clause's total mass (empty clause = all-zeros).

    Soft-min-over-steps decouples proof length from the budget L: the decoder reads the first near-empty
    row, so any step reaching the empty clause suffices.
    """
    masses = torch.stack([D.sum(-1) for D in aux.D], dim=-1)  # [R, L]
    return _softmin(masses, beta, dim=-1)                     # [R]


def entropy_penalty(aux: Aux, eps: float = 1e-9) -> torch.Tensor:
    """Per-seed mean over steps of ``H(p1)+H(p2)+H(q)`` (drives selections toward one-hot)."""
    def H(p):
        return -(p * (p + eps).log()).sum(-1)
    terms = [H(p1) + H(p2) + H(q) for p1, p2, q in zip(aux.p1, aux.p2, aux.q)]
    return torch.stack(terms, dim=-1).mean(-1)  # [R]


def total_loss(aux: Aux, n: int, w1: float, w2: float, w3: float, beta: float) -> torch.Tensor:
    """Per-seed total loss [R]. Backward uses ``.sum()`` since seeds optimize independently."""
    return (w1 * validity_residual(aux, n, beta)
            + w2 * termination_distance(aux, beta)
            + w3 * entropy_penalty(aux))


def tau_schedule(step: int, S: int, tau0: float = 1.0, tau_min: float = 0.05) -> float:
    """Geometric temperature anneal ``tau0 → tau_min`` over ``S`` steps (the primary sharpening lever)."""
    if S <= 1:
        return tau_min
    frac = step / (S - 1)
    return max(tau_min, tau0 * (tau_min / tau0) ** frac)


def w3_schedule(step: int, S: int, w3_max: float, s0_frac: float = 0.3) -> float:
    """Linear entropy-weight ramp: 0 until ``s0_frac·S``, then up to ``w3_max`` by the end."""
    s0 = s0_frac * S
    if step <= s0 or S <= 1:
        return 0.0 if step <= s0 else w3_max
    return w3_max * min(1.0, (step - s0) / max(1.0, (S - 1) - s0))
