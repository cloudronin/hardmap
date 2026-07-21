"""M2 operator — what it provably does: it REPRESENTS a Resolution refutation exactly (init at a planted
proof decodes+verifies at 100%). The E0 negative result (findability from random init) is documented in
docs/findings/NEGATIVE-RESULT.md, not asserted here. torch-guarded so CI without [compute] skips cleanly."""
from __future__ import annotations

import pytest

pytest.importorskip("torch")
import torch  # noqa: E402

from desertmap import instance  # noqa: E402
from desertmap.relax import SoftResolutionProof, cnf_to_membership, _ste  # noqa: E402
from desertmap.decode import decode_aux, verify_proofs  # noqa: E402


def test_cnf_to_membership_slots():
    cnf = instance.CNF(3, ((1, -2), (3,)))       # (x1 ∨ ¬x2), (x3)
    M = cnf_to_membership(cnf)
    assert M.shape == (2, 6)
    assert M[0, 0] == 1 and M[0, 3 + 1] == 1     # +x1 at slot 0, ¬x2 at slot n+1=4
    assert M[1, 2] == 1 and M[1].sum() == 1      # +x3 at slot 2


def test_soft_or_is_expected_resolvent_on_hard_clauses():
    # product t-norm soft-OR of two hard clauses = exact union membership
    A = torch.tensor([1.0, 0, 0, 0]); B = torch.tensor([0.0, 1, 0, 0])
    assert torch.allclose(1 - (1 - A) * (1 - B), torch.tensor([1.0, 1, 0, 0]))


def test_ste_is_onehot_forward_identity_backward():
    soft = torch.tensor([[0.2, 0.7, 0.1]], requires_grad=True)
    h = _ste(soft)
    assert torch.allclose(h.detach(), torch.tensor([[0.0, 1.0, 0.0]]))   # forward = argmax one-hot
    h.sum().backward()
    assert soft.grad is not None                                          # gradient flows to soft


@pytest.mark.parametrize("n,k", [(20, 5), (30, 6)])
def test_operator_represents_planted_proof(n, k):
    cnf, proof = instance.gen_planted(n=n, k=k, seed=0)
    m = SoftResolutionProof(cnf_to_membership(cnf), L=4 * n, R=8)
    m.init_near_proof(proof, bias=12.0, noise=0.0, seed=0)
    succ = verify_proofs(cnf, decode_aux(m(tau=0.05)))
    assert sum(succ) / len(succ) == 1.0, "operator must represent a planted proof exactly"


def test_ste_bank_stays_discrete():
    cnf, proof = instance.gen_planted(n=20, k=5, seed=0)
    m = SoftResolutionProof(cnf_to_membership(cnf), L=12, R=4, mode="ste")
    m.init_near_proof(proof, bias=12.0, noise=0.0, seed=0)
    aux = m(tau=0.05)
    D = aux.D[0]                                     # first derived clause, [R, 2n]
    assert torch.all((D == 0) | (D == 1)), "STE forward must yield discrete 0/1 clauses"
