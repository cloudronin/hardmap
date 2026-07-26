"""Mosaic v3 grid — the gates that must fail LOUDLY, not silently.

These lock the two rules that make the arms mean anything: the algebra is excluded from Arm A's features,
and prediction files stay outside the research agents' input surface for the prospective registry.
"""
import json
import pathlib
import sys

import pytest

FOUNDRY = pathlib.Path(__file__).resolve().parent.parent
LAT = FOUNDRY / "foundry" / "results" / "lattice"
ATLAS = FOUNDRY.parent / "eightfold" / "eightfold" / "results" / "atlas"
sys.path.insert(0, str(FOUNDRY.parent / "eightfold" / "dev"))

SURF = LAT / "grid_surface_features.json"
FOLDS = LAT / "grid_folds_and_strata.json"
skip_no_surf = pytest.mark.skipif(not SURF.exists(), reason="surface features not built (G1)")


@skip_no_surf
def test_no_algebra_leaks_into_arm_a_features():
    """THE load-bearing gate. Arm A asks whether the algebra is recoverable from surface combinatorics;
    if a Post flag or a flag-derivative is in the feature matrix, the question is not being asked."""
    doc = json.loads(SURF.read_text())
    banned = set(doc["excluded_algebra"]) | set(doc["excluded_derived"])
    for name in doc["feature_names"]:
        assert name not in banned, f"EXCLUDED feature {name!r} present in Arm A's matrix"
    for row in doc["rows"][:200]:
        assert not (set(row["features"]) & banned), f"{row['row_key']}: excluded feature present"


@skip_no_surf
def test_weight_histogram_omits_the_0valid_and_1valid_bins():
    """w0 and w{arity} ARE 0valid/1valid. A naive weight histogram hands back 2 of the 10 flags."""
    doc = json.loads(SURF.read_text())
    assert "w0" not in doc["feature_names"], "w0 is the 0-valid flag in disguise"
    assert "w4" not in doc["feature_names"], "w{arity} is the 1-valid flag in disguise"


@skip_no_surf
def test_starved_features_are_flagged_not_silently_shipped():
    doc = json.loads(SURF.read_text())
    assert doc["starved_features"], "census found nothing starved — suspicious, verify the census ran"
    for k in doc["starved_features"]:
        assert doc["census"][k]["starved"] is True


@pytest.mark.skipif(not FOLDS.exists(), reason="folds not built (G1)")
def test_fold_key_is_the_46_fingerprint_groups_and_boundary_is_stratification_only():
    doc = json.loads(FOLDS.read_text())
    assert doc["fold_key"]["n_groups"] == 46
    assert "STRATIFICATION ONLY" in doc["boundary_distance"]["role"]
    assert doc["boundary_distance"]["starved"] is False


def test_prediction_files_are_outside_the_research_input_surface():
    """prereg_v12 G1 addendum rule 2: enforced BY CONSTRUCTION, not by convention."""
    import grid_registry as R
    bad = R.assert_research_surface_clean([
        ATLAS / "quarry-v2-fill-inventory.json", ATLAS / "quarry-v2-funnel-query.json"])
    assert bad == [], f"research inputs must not include prediction files: {bad}"
    leaked = R.assert_research_surface_clean([ATLAS / "grid-predictions" / "wave-1.json"])
    assert leaked, "the guard must FIRE when a prediction file reaches the research surface"


def test_registry_declares_insufficient_until_its_floor_is_pinned():
    import grid_registry as R
    reg = R.load()
    assert "UNPINNED" in reg["threshold_status"]
    scored = [e for e in reg["entries"] if e.get("counts_in_scored_n")]
    assert scored == [], "no cell may enter the scored n before a wave is sealed predict-then-fill"
    pre = [e for e in reg["entries"] if e.get("temporal_class") == "clean-but-pre-registry"]
    assert len(pre) == 21 and all(e["counts_in_descriptive"] for e in pre)
