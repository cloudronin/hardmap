"""A3 harness: machinery + the pre-registered verdict RULES.

These lock the harness (it runs end-to-end, shapes are well-formed) and check that each verdict
correctly *applies its pre-registered rule* — deliberately NOT that the answer is "SUPPORTED".
Pinning the verdict value would manufacture the science; if the atlas changed and a hypothesis
flipped, these tests must still pass. The one data fact asserted outright — every theorem-forbidden
cell is empty — is an entailment invariant the validator already enforces on the corpus.
"""
import pytest

pytest.importorskip("numpy")  # structure.py is behind the [analysis] extra

from eightfold import charges as C  # noqa: E402
from eightfold.atlas import DEFAULT_PATH, load_atlas  # noqa: E402
from eightfold.structure import a3, gap_list, leave_one_charge_out, selftest  # noqa: E402


@pytest.fixture(scope="module")
def out():
    return a3(load_atlas(DEFAULT_PATH))


def test_a3_shape(out):
    assert out["a3"] is True and out["prereg"] == "prereg_v5"
    assert out["n_problems"] == 118
    for k in ("H1_dimensionality", "H2_multiplets", "H3_forbidden_and_gaps",
              "cramers_v", "mca_full_table", "mca_complete_case", "subspace_clustering"):
        assert k in out, k


def test_H1_rule_applied_correctly(out):
    h1 = out["H1_dimensionality"]
    supported = (h1["mca_full_dims"] >= 3 and h1["mca_complete_case_dims"] >= 3
                 and h1["loco_min_dims"] >= 3)
    assert h1["verdict"] == ("SUPPORTED" if supported else "NOT-SUPPORTED")
    # loco_min is the min over the per-charge drops
    assert h1["loco_min_dims"] == min(h1["loco_per_charge"].values())
    assert set(h1["loco_per_charge"]) == set(C.CHARGES)


def test_H2_rule_applied_correctly(out):
    h2 = out["H2_multiplets"]
    amp = h2["witness_amplified"]
    assert set(amp) == {"permanent|determinant", "vertex-cover|clique", "sat-2|xor-sat"}
    supported = amp["permanent|determinant"] and amp["vertex-cover|clique"]
    assert h2["verdict"] == ("SUPPORTED" if supported else "NOT-SUPPORTED")


def test_H3_forbidden_cells_all_empty_invariant(out):
    h3 = out["H3_forbidden_and_gaps"]
    # E1 (6 decision values x counting=FP) + E2 (5 decision values x {NC,P-complete}) = 16
    assert h3["n_theorem_forbidden_cells"] == 16
    assert h3["forbidden_cells_all_empty_in_data"] is True
    for cell in h3["theorem_forbidden"]:
        assert cell["rules"], cell


def test_gap_list_wellformed(out):
    h3 = out["H3_forbidden_and_gaps"]
    assert h3["n_gaps"] == len(h3["gap_list"])
    for g in h3["gap_list"]:
        assert g["pair"].count("|") == 1
        assert g["claim"].startswith("a natural problem with ")
        assert "should exist; none is in the atlas" in g["claim"]
    # a gap is never also theorem-forbidden (triage is a partition)
    forbidden = {c["cell"] for c in h3["theorem_forbidden"]}
    assert forbidden and not (forbidden & {g["claim"] for g in h3["gap_list"]})


def test_gap_list_standalone_matches_a3(out):
    gl = gap_list(load_atlas(DEFAULT_PATH))
    assert gl["n_gaps"] == out["H3_forbidden_and_gaps"]["n_gaps"]
    assert gl["n_forbidden"] == out["H3_forbidden_and_gaps"]["n_theorem_forbidden_cells"]


def test_leave_one_charge_out_one_dim_per_charge():
    loco = leave_one_charge_out(load_atlas(DEFAULT_PATH))
    assert set(loco) == set(C.CHARGES)
    assert all(isinstance(v, int) and v >= 0 for v in loco.values())


def test_drop_measured_ablation_present(out):
    # R9: the ablation number exists so no structure claim can rest on measured cells unnoticed
    assert isinstance(out["H1_dimensionality"]["drop_measured_full_dims"], int)


def test_selftest_green():
    assert selftest() == 0
