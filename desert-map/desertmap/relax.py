"""Differentiable relaxation of a Resolution refutation — the risk front (M2).

The soft-resolvent operator is the product t-norm soft-OR ``1-(1-A)(1-B)`` with multiplicative pivot
removal, which is the EXACT expected literal-membership of the discrete resolvent under independent softmax
selection of the two parents and the pivot (I1 finding: the t-norm primitive is standard — cite Xu 2018 /
van Krieken 2020 — but assembling it into a refutation-search operator over a growing clause bank is the
contribution). Everything is batched over ``R`` independent seeds; only the step loop is sequential.

Literal slot convention (0-indexed): slot ``i∈[0,n)`` = positive literal ``x_{i+1}``; slot ``n+i`` =
negative literal ``¬x_{i+1}``. :mod:`desertmap.decode` bridges these slots back to signed-int literals for
:mod:`desertmap.verify`.
"""
from __future__ import annotations

from dataclasses import dataclass

import torch
import torch.nn as nn
import torch.nn.functional as F

from desertmap.instance import CNF


def cnf_to_membership(cnf: CNF) -> torch.Tensor:
    """Hard membership matrix ``C0 ∈ {0,1}^{m×2n}`` for the original clauses (slot convention above)."""
    n, m = cnf.n_vars, cnf.n_clauses
    C0 = torch.zeros(m, 2 * n)
    for j, clause in enumerate(cnf.clauses):
        for lit in clause:
            v = abs(lit)
            slot = (v - 1) if lit > 0 else n + (v - 1)
            C0[j, slot] = 1.0
    return C0


def _ste(soft: torch.Tensor) -> torch.Tensor:
    """Straight-through one-hot: forward value = argmax one-hot; backward = identity onto ``soft``.

    ``hard + (soft - soft.detach())`` equals ``hard`` numerically but carries ``soft``'s gradient.
    """
    idx = soft.argmax(dim=-1, keepdim=True)
    hard = torch.zeros_like(soft).scatter_(-1, idx, 1.0)
    return hard + (soft - soft.detach())


@dataclass
class Aux:
    """Per-step cached tensors from a forward pass (all leading dim ``R``)."""

    p1: list  # row-selection softmaxes, each [R, m+t]
    p2: list
    q: list   # pivot-variable softmaxes, each [R, n]
    P1: list  # soft parent-1 clause, each [R, 2n]
    P2: list
    D: list   # soft resolvent (derived clause) at each step, each [R, 2n]


class SoftResolutionProof(nn.Module):
    """A batch of ``R`` soft Resolution proofs of budget ``L`` over one instance.

    Learnable parameters are only the selection logits ``theta_p1, theta_p2 [R,L,m+L-1]`` and
    ``theta_q [R,L,n]``; clauses are *derived*, not learned. A causal mask forbids step ``t`` from selecting
    any bank row ``>= m+t`` (parents must be original or earlier-derived).
    """

    def __init__(self, C0: torch.Tensor, L: int, R: int, mode: str = "soft"):
        super().__init__()
        m, twon = C0.shape
        self.m, self.n, self.L, self.R = m, twon // 2, L, R
        self.max_rows = m + L - 1
        self.mode = mode                                                 # 'soft' | 'ste' (redesign axis 1)
        self.register_buffer("C0", C0)                                   # [m, 2n], not learned

        g = torch.Generator().manual_seed(0)  # param *shape* init; the real seed variety is set in fit()
        self.theta_p1 = nn.Parameter(torch.randn(R, L, self.max_rows, generator=g) * 0.01)
        self.theta_p2 = nn.Parameter(torch.randn(R, L, self.max_rows, generator=g) * 0.01)
        self.theta_q = nn.Parameter(torch.randn(R, L, self.n, generator=g) * 0.01)

        # Causal mask: mask[t, j] = 0 if row j selectable at step t (j < m+t) else -inf.
        mask = torch.full((L, self.max_rows), float("-inf"))
        for t in range(L):
            mask[t, : m + t] = 0.0
        self.register_buffer("causal_mask", mask)

    def forward(self, tau: float, mode: str | None = None) -> Aux:
        """Forward pass at temperature ``tau``. ``mode='soft'`` uses the soft selections directly;
        ``mode='ste'`` (straight-through, redesign axis 1) computes the resolvent from the HARD argmax
        selection in the forward pass — so the loss sees the actual decoded proof and the bank stays
        discrete — while gradients flow through the soft softmax Jacobian.
        """
        mode = mode or self.mode
        R, m, n, L = self.R, self.m, self.n, self.L
        static = self.C0.unsqueeze(0).expand(R, m, 2 * n)                # [R, m, 2n]
        derived: list[torch.Tensor] = []
        aux = Aux([], [], [], [], [], [])
        for t in range(L):
            k = m + t                                                    # #available rows at step t
            bank = static if not derived else torch.cat([static, torch.stack(derived, dim=1)], dim=1)
            logits1 = (self.theta_p1[:, t, :k] + self.causal_mask[t, :k]) / tau
            logits2 = (self.theta_p2[:, t, :k] + self.causal_mask[t, :k]) / tau
            p1 = F.softmax(logits1, dim=-1)                              # [R, k] (soft; used for entropy)
            p2 = F.softmax(logits2, dim=-1)
            q = F.softmax(self.theta_q[:, t] / tau, dim=-1)             # [R, n]
            s1, s2, sq = (_ste(p1), _ste(p2), _ste(q)) if mode == "ste" else (p1, p2, q)
            P1 = torch.einsum("rk,rkd->rd", s1, bank)                    # [R, 2n]
            P2 = torch.einsum("rk,rkd->rd", s2, bank)
            U = 1.0 - (1.0 - P1) * (1.0 - P2)                           # product t-norm soft-OR
            removal = torch.cat([sq, sq], dim=-1)                       # remove both polarities of pivot
            D = U * (1.0 - removal)                                      # resolvent [R, 2n]
            derived.append(D)
            aux.p1.append(p1); aux.p2.append(p2); aux.q.append(q)       # store SOFT dists (entropy/validity)
            aux.P1.append(P1); aux.P2.append(P2); aux.D.append(D)
        return aux

    @torch.no_grad()
    def init_seeds(self, seed: int, scale: float = 1.0):
        """Random-init all selection logits with per-seed variety (E0 is a from-random-init gate, C1)."""
        g = torch.Generator().manual_seed(seed)
        for p in (self.theta_p1, self.theta_p2, self.theta_q):
            p.copy_(torch.randn(p.shape, generator=g) * scale)

    @torch.no_grad()
    def init_near_proof(self, proof: list, bias: float = 6.0, noise: float = 0.3, seed: int = 0):
        """DIAGNOSTIC-only near-planted init (NOT the E0 gate, AGENTS.md invariant 2): bias logits toward a
        known proof's argmax so we can isolate search-failure from representation-failure."""
        g = torch.Generator().manual_seed(seed)
        self.init_seeds(seed, scale=noise)
        for t, (i1, i2, pivot) in enumerate(proof[: self.L]):
            self.theta_p1[:, t, i1] += bias
            self.theta_p2[:, t, i2] += bias
            self.theta_q[:, t, pivot - 1] += bias        # pivot var (1-indexed) -> slot (0-indexed)
