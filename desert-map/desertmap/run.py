"""Per-instance training over R independent seeds → RunResult (M2 + E5 trajectory summaries).

``fit_instance`` optimizes the soft-resolution parameters for R seeds jointly (they are independent — the
gradient never couples seeds), decodes at the final temperature, and verifies. E0 success is the
random-init verifier-pass rate (C1). Trajectory summaries (step-norm series, cosine of successive update
directions, sampled inter-seed divergence at checkpoints) are computed in-container and are the E5 artifact
(spec §3.3); raw parameter snapshots are kept only when ``keep_raw=True`` (the small designated subset).
"""
from __future__ import annotations

from dataclasses import dataclass, field

import torch

from desertmap import losses
from desertmap.decode import decode_aux, verify_proofs
from desertmap.instance import CNF
from desertmap.relax import SoftResolutionProof, cnf_to_membership


@dataclass
class RunResult:
    n_vars: int
    alpha: float
    L: int
    R: int
    steps: int
    success: list                      # per-seed bool (decoded proof verifies)
    success_rate: float
    final_loss: list                   # per-seed float
    soft_hard_gap: float               # (soft-success fraction) − (verify fraction) ≥ 0 signals rounding loss
    proofs: list                       # per-seed decoded DiscreteProof
    trajectory: dict                   # E5 summaries (checkpoints, step_norm, update_cosine, seed_divergence)
    fixture_hash: str = ""
    seed: int = 0
    init: str = "random"
    raw_snapshots: list = field(default_factory=list)  # optional [n_ckpt] of [R,P] param snapshots


def _flat_params(module: SoftResolutionProof) -> torch.Tensor:
    """Flatten all selection logits to ``[R, P]`` (per-seed parameter vector)."""
    return torch.cat([p.detach().reshape(module.R, -1) for p in module.parameters()], dim=1)


def _mean_pairwise_divergence(flat: torch.Tensor, n_pairs: int, gen: torch.Generator) -> float:
    """Mean L2 distance over ``n_pairs`` random seed pairs (inter-trajectory divergence proxy)."""
    R = flat.shape[0]
    if R < 2:
        return 0.0
    a = torch.randint(0, R, (n_pairs,), generator=gen)
    b = torch.randint(0, R, (n_pairs,), generator=gen)
    keep = a != b
    if keep.sum() == 0:
        return 0.0
    return (flat[a[keep]] - flat[b[keep]]).norm(dim=1).mean().item()


def fit_instance(cnf: CNF, L: int, R: int, S: int, *,
                 weights: tuple[float, float, float] = (1.0, 1.0, 0.1),
                 seed: int = 0, lr: float = 0.05, tau0: float = 1.0, tau_min: float = 0.05,
                 init: str = "random", planted_proof: list | None = None,
                 mode: str = "ste", checkpoint_every: int = 25, keep_raw: bool = False,
                 soft_tol: float = 0.05, device: str = "cpu") -> RunResult:
    """Fit R soft proofs on ``cnf`` and return a :class:`RunResult`. ``init='random'`` is the E0 gate;
    ``init='planted'`` (needs ``planted_proof``) is the diagnostic-only near-planted variant (not the gate).
    ``mode='ste'`` (straight-through, default) closes the soft→hard rounding gap; ``mode='soft'`` is the
    pure-soft baseline.
    """
    w1, w2, w3_max = weights
    C0 = cnf_to_membership(cnf).to(device)
    module = SoftResolutionProof(C0, L, R, mode=mode).to(device)
    if init == "planted":
        if planted_proof is None:
            raise ValueError("init='planted' requires planted_proof")
        module.init_near_proof(planted_proof, seed=seed)
    else:
        module.init_seeds(seed)

    opt = torch.optim.Adam(module.parameters(), lr=lr)
    gen = torch.Generator().manual_seed(seed)

    ckpts, step_norm, update_cos, seed_div, raw = [], [], [], [], []
    prev_flat = _flat_params(module)
    prev_delta = None

    for s in range(S):
        tau = losses.tau_schedule(s, S, tau0, tau_min)
        w3 = losses.w3_schedule(s, S, w3_max)
        beta = min(50.0, 1.0 / max(tau, 1e-3))
        aux = module(tau)
        loss_vec = losses.total_loss(aux, module.n, w1, w2, w3, beta)
        opt.zero_grad()
        loss_vec.sum().backward()
        opt.step()

        if (s % checkpoint_every == 0) or (s == S - 1):
            cur_flat = _flat_params(module)
            delta = cur_flat - prev_flat
            sn = delta.norm(dim=1)                                   # [R]
            if prev_delta is not None:
                cos = torch.nn.functional.cosine_similarity(delta, prev_delta, dim=1)  # [R]
            else:
                cos = torch.zeros(module.R)
            ckpts.append(s)
            step_norm.append(sn.tolist())
            update_cos.append(cos.tolist())
            seed_div.append(_mean_pairwise_divergence(cur_flat, n_pairs=min(200, module.R * 4), gen=gen))
            if keep_raw:
                raw.append(cur_flat.clone())
            prev_delta = delta
            prev_flat = cur_flat

    # --- decode + verify at the final (sharp) temperature ---
    with torch.no_grad():
        aux_final = module(tau_min)
        vr = losses.validity_residual(aux_final, module.n, beta=min(50.0, 1.0 / tau_min))
        td = losses.termination_distance(aux_final, beta=min(50.0, 1.0 / tau_min))
        final_loss = (w1 * vr + w2 * td).tolist()
        proofs = decode_aux(aux_final)
    success = verify_proofs(cnf, proofs)
    success_rate = sum(success) / len(success)

    soft_ok = ((vr < soft_tol) & (td < soft_tol)).float().mean().item()
    soft_hard_gap = soft_ok - success_rate

    trajectory = {"checkpoints": ckpts, "step_norm": step_norm,
                  "update_cosine": update_cos, "seed_divergence": seed_div}
    return RunResult(
        n_vars=cnf.n_vars, alpha=cnf.alpha, L=L, R=R, steps=S,
        success=success, success_rate=success_rate, final_loss=final_loss,
        soft_hard_gap=soft_hard_gap, proofs=proofs, trajectory=trajectory,
        fixture_hash=cnf.content_hash(), seed=seed, init=init,
        raw_snapshots=raw,
    )
