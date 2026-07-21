"""Decode: round soft selections to a discrete Resolution proof, then verify (M2).

The known failure mode is the soft→hard rounding gap: a near-zero soft loss can still argmax-decode to an
invalid proof. Decoding is deliberately independent of the loss — it argmaxes the selection distributions and
hands the result to the trusted verifier (:mod:`desertmap.verify`), which is the sole arbiter of success.
"""
from __future__ import annotations

import torch

from desertmap import verify
from desertmap.instance import CNF
from desertmap.relax import Aux, SoftResolutionProof

DiscreteProof = list  # list[(i1, i2, pivot)]


def decode_aux(aux: Aux) -> list[DiscreteProof]:
    """Argmax-decode a forward pass into one discrete proof per seed (len R).

    Per step: parent rows = argmax of the row-selection softmaxes; pivot variable = argmax of the pivot
    softmax (+1 to convert 0-indexed slot → 1-indexed variable, matching :mod:`desertmap.verify`).
    """
    L = len(aux.p1)
    R = aux.p1[0].shape[0]
    proofs: list[DiscreteProof] = [[] for _ in range(R)]
    for t in range(L):
        i1 = aux.p1[t].argmax(dim=-1)   # [R]
        i2 = aux.p2[t].argmax(dim=-1)
        piv = aux.q[t].argmax(dim=-1)   # [R], 0-indexed var
        for r in range(R):
            proofs[r].append((int(i1[r]), int(i2[r]), int(piv[r]) + 1))
    return proofs


@torch.no_grad()
def decode(module: SoftResolutionProof, tau: float) -> list[DiscreteProof]:
    """Run a hard-ish forward pass at temperature ``tau`` and argmax-decode to R discrete proofs."""
    return decode_aux(module(tau))


def verify_proofs(cnf: CNF, proofs: list[DiscreteProof]) -> list[bool]:
    """Verify each decoded proof against ``cnf`` with the trusted exact verifier. Returns per-seed bools."""
    clause_sets = cnf.clause_sets()
    return [verify.verify(clause_sets, p, n_vars=cnf.n_vars) for p in proofs]
