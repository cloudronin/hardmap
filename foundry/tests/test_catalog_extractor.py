"""Known-answer battery for the catalog extractor (Observatory Catalog v1, guard rail 5).

THE RULE THIS ENFORCES: an extractor change that moves a fixture value WITHOUT A VERSION BUMP is a hard
failure. Sealed claims quote `descriptor@version` forever; if v1 silently starts meaning something else,
every claim quoting it becomes wrong at a distance with no diff to point at.

The fixtures are HAND-COMPUTED on tiny synthetic trajectories, not snapshots of extractor output. A
snapshot test only proves the extractor still does what it did; a hand-computed fixture proves it does
what it SHOULD. The difference is the whole point of a known-answer battery.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from foundry.catalog import extract as X  # noqa: E402


def _steps(vals, states=None, sds=None, ramp=None):
    """Build a synthetic trajectory. vals[i] is None where the step carries no value."""
    n = len(vals)
    states = states or ["usable"] * n
    sds = sds or [0.01] * n
    ramp = ramp or [0.1 * (i + 1) for i in range(n)]
    out = []
    for i, v in enumerate(vals):
        s = {"ramp_position": i, "ramp_value": ramp[i], "state": states[i],
             "blend_excess": v, "control_sd": sds[i], "r": 100 + i}
        if states[i] == "INSUFFICIENT":
            s["state"] = "usable"; s["insufficient"] = "INSUFFICIENT-r"
        out.append(s)
    return out


# ── the reference-step rule: positional, outcome-blind ──────────────────────────────────────────────
def test_reference_step_is_median_admissible_position():
    """5 admissible steps 0..4 -> median position 2. Hand-computed."""
    st = _steps([-0.1, -0.2, -0.3, -0.4, -0.5])
    pos, val = X.reference_step(st)
    assert pos == 2, f"expected median admissible position 2, got {pos}"
    assert abs(val - 0.3) < 1e-12, f"expected ramp value 0.3 at position 2, got {val}"


def test_reference_step_skips_insufficient_and_gap():
    """positions 0 and 4 inadmissible -> admissible {1,2,3} -> median 2."""
    st = _steps([None, -0.2, -0.3, -0.4, -0.5],
                states=["GAP-no-region", "usable", "usable", "usable", "INSUFFICIENT"])
    st[0]["state"] = "GAP-no-region"
    pos, _ = X.reference_step(st)
    assert pos == 2, f"expected 2 from admissible {{1,2,3}}, got {pos}"


def test_reference_step_never_reads_a_value():
    """THE OUTCOME-BLINDNESS PROPERTY, tested rather than asserted: the same states with wildly
    different values must select the same position."""
    a = X.reference_step(_steps([-0.1, -0.2, -0.3, -0.4, -0.5]))
    b = X.reference_step(_steps([+9.9, -0.2, +5.0, -0.4, -9.9]))
    assert a[0] == b[0] == 2, "the reference step moved when only the VALUES changed"


# ── level ───────────────────────────────────────────────────────────────────────────────────────────
def test_level_envelope_and_reference():
    st = _steps([-0.1, -0.2, -0.3, -0.4, -0.5])
    L = X.level(st)
    assert L["excess_ref"] == -0.3, L
    assert L["excess_min"] == -0.5 and L["excess_max"] == -0.1, L
    assert abs(L["excess_ref_ramp_value"] - 0.3) < 1e-9, L   # float build, tolerance


def test_level_ignores_inadmissible_steps_in_the_envelope():
    """an INSUFFICIENT step's value must not set excess_min — inadmissible is inadmissible everywhere."""
    st = _steps([-0.1, -0.2, -0.3, -0.4, -9.0], states=["usable"] * 4 + ["INSUFFICIENT"])
    assert X.level(st)["excess_min"] == -0.4


# ── shape ───────────────────────────────────────────────────────────────────────────────────────────
def test_shape_flat_when_excursion_below_two_sd():
    """excursion 0.02, pooled SD 0.05 -> 0.02 < 2*0.05 -> FLAT. Hand-computed."""
    st = _steps([-0.10, -0.11, -0.12, -0.11, -0.10], sds=[0.05] * 5)
    assert X.shape(st)["traj_class"] == "FLAT"


def test_shape_monotone_and_slope_sign():
    st = _steps([-0.5, -0.4, -0.3, -0.2, -0.1], sds=[0.001] * 5)
    S = X.shape(st)
    assert S["traj_class"] == "MONOTONE", S
    assert S["slope_sign"] == 1, S


def test_shape_non_monotone():
    st = _steps([-0.5, -0.1, -0.5, -0.1, -0.5], sds=[0.001] * 5)
    assert X.shape(st)["traj_class"] == "NON-MONOTONE"


def test_shape_unclassified_below_three_steps():
    st = _steps([-0.5, -0.4, None, None, None],
                states=["usable", "usable", "GAP-no-region", "GAP-no-region", "GAP-no-region"])
    assert X.shape(st)["traj_class"] == "UNCLASSIFIED"


# ── coherence ───────────────────────────────────────────────────────────────────────────────────────
def test_overlap_exhaustive_path_keeps_every_distinct_pair():
    """A region is a SET, so it cannot hold duplicate members — but the exhaustive path must not drop
    pairs merely because their values coincide. This pins the filter to the sampled path only.

    Four members, C(4,2) = 6 pairs, and all six must be returned."""
    r = [(1, 1, 0, 0), (1, 0, 1, 0), (0, 1, 1, 0), (1, 1, 1, 0)]
    assert len(X.overlaps(r)) == 6


def test_overlap_maximum_for_distinct_members():
    """Distinct members differ in at least one coordinate, so the ceiling is (n-1)/n, never 1.0."""
    o = X.overlaps([(1, 1, 1, 1), (1, 1, 1, 0)])
    assert len(o) == 1 and abs(o[0] - 0.75) < 1e-12


def test_overlap_of_complementary_pair_is_zero():
    o = X.overlaps([(1, 1, 1, 1), (0, 0, 0, 0)])
    assert len(o) == 1 and abs(o[0]) < 1e-12


def test_overlap_half_agreement():
    """(1,1,0,0) vs (1,0,1,0) agree on 2 of 4 coordinates -> 0.5. Hand-computed."""
    o = X.overlaps([(1, 1, 0, 0), (1, 0, 1, 0)])
    assert len(o) == 1 and abs(o[0] - 0.5) < 1e-12


def test_bimodality_none_below_four_samples():
    assert X.bimodality_coefficient([0.1, 0.2, 0.3]) is None


def test_bimodality_none_on_zero_variance():
    assert X.bimodality_coefficient([0.5] * 10) is None


def test_bimodality_flags_a_two_spike_distribution():
    """A clean two-spike distribution must exceed the flag; a unimodal one must not."""
    two = [0.1] * 20 + [0.9] * 20
    uni = [0.5 + 0.01 * ((i % 7) - 3) for i in range(40)]
    assert X.bimodality_coefficient(two) > X.BIMODALITY_FLAG
    assert X.bimodality_coefficient(uni) <= X.BIMODALITY_FLAG


# ── transition carries its own prohibition ──────────────────────────────────────────────────────────
def test_transition_ships_its_seal_prohibition_in_the_cell():
    """A caveat that lives only in a schema document is a caveat nobody reads. It must be in the cell."""
    st = _steps([-0.1, -0.1, -0.5, -0.5, -0.5], sds=[0.001] * 5)
    t = X.transition(st)
    assert t["SEAL_PROHIBITED_AT_V1"] is True
    assert t["kink_step"] == 2, t


# ── supply ──────────────────────────────────────────────────────────────────────────────────────────
def test_supply_counts_the_three_absence_states_separately():
    st = _steps([-0.1, None, -0.3, -0.4, -0.5],
                states=["usable", "GAP-no-region", "usable", "INSUFFICIENT", "usable"])
    s = X.supply(st)
    assert s["gap_count"] == 1, s
    assert abs(s["insufficient_share"] - 0.2) < 1e-12, s


# ── the version contract ────────────────────────────────────────────────────────────────────────────
def test_descriptors_stamp_their_version():
    st = _steps([-0.1, -0.2, -0.3, -0.4, -0.5])
    assert X.descriptors(st)["descriptor_version"] == X.VERSION


def test_scaling_group_is_reserved_not_absent():
    """A reserved column must be present-and-null, not missing — an absent key reads as an oversight."""
    st = _steps([-0.1, -0.2, -0.3, -0.4, -0.5])
    sc = X.descriptors(st)["scaling"]
    assert "kink_drift_n" in sc and sc["kink_drift_n"] is None
    assert "RESERVED" in sc


# ── structure — NEW AT v2 ───────────────────────────────────────────────────────────────────────────
def _rsteps(rs):
    return [{"ramp_position": i, "ramp_value": 0.1 * (i + 1), "state": "usable",
             "blend_excess": -0.1, "control_sd": 0.01, "r": r} for i, r in enumerate(rs)]


def test_structurally_flat_needs_declaration_region_AND_observed_invariance():
    """A fixed-cardinality row's OPTIMAL region depends on the instance, so only feasible can be flat —
    and even then only if the frames show the region standing still."""
    assert X.structure(_rsteps([120] * 5), "feasible", "fixed_cardinality")["structurally_flat"]
    assert not X.structure(_rsteps([46, 14, 5, 7, 6]), "optimal",
                           "fixed_cardinality")["structurally_flat"]


def test_declared_fixed_cardinality_whose_region_moves_is_not_flat():
    """THE v2 DEFECT, pinned. 3sum's members all have weight 3, so it declares fixed_cardinality
    honestly — but its region is the triples SUMMING TO ZERO, which moves with the instance. v2 would
    have flagged it flat and dropped a real trajectory from Helm's swept population."""
    s = X.structure(_rsteps([33, 18, 15, 10, 9]), "feasible", "fixed_cardinality")
    assert s["structurally_flat"] is False
    assert s["declared_flat_but_moves"] is True, "the disagreement must be surfaced, not resolved"


def test_structurally_flat_is_false_without_the_declaration():
    assert not X.structure(_rsteps([120] * 5), "feasible", "upward_closed")["structurally_flat"]
    assert not X.structure(_rsteps([120] * 5), "feasible", None)["structurally_flat"]


def test_region_size_invariance_is_measured_separately_from_the_declaration():
    """Declared and observed are kept apart on purpose, so the informative case stays visible."""
    s = X.structure(_rsteps([120] * 5), "feasible", "fixed_cardinality")
    assert s["region_size_invariant"] is True and s["declared_flat_but_moves"] is False
    s2 = X.structure(_rsteps([441, 273, 181, 156, 101]), "feasible", "fixed_cardinality")
    assert s2["region_size_invariant"] is False and s2["declared_flat_but_moves"] is True


def test_region_size_invariance_is_none_below_two_steps():
    assert X.structure(_rsteps([120]), "feasible", "fixed_cardinality")["region_size_invariant"] is None


def test_descriptors_carry_the_structure_group():
    d = X.descriptors(_rsteps([120] * 5), region="feasible",
                      structural_expectation="fixed_cardinality")
    assert d["descriptor_version"] == X.VERSION
    assert d["structure"]["structurally_flat"] is True
