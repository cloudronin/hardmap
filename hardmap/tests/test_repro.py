"""Smoke tests for the hardmap CLI layer: manifest, comparison, repro, verify."""
from hardmap import repro, verify
from hardmap.compare import compare
from hardmap.manifest import load_manifest

CLAIM_IDS = {
    "canon.gradient.v", "canon.crucible.verdicts", "factors.kstar",
    "natural.v3.v", "natural.prism.residuals", "natural.direction.corrected",
    "census.backbone", "census.plurality",
}
# Sub-second claims (skip the ~17s crucible recompute so the suite stays fast).
INSTANT = [
    "factors.kstar", "natural.v3.v", "natural.prism.residuals",
    "natural.direction.corrected", "census.backbone", "census.plurality",
]


def test_manifest_has_every_claim():
    ids = {c["id"] for c in load_manifest()}
    assert CLAIM_IDS <= ids


def test_instant_fast_claims_pass():
    assert repro.run(claim_ids=INSTANT) == 0


def test_verify_passes():
    assert verify.run() == 0


def test_repro_reports_unknown_claim():
    assert repro.run(claim_ids=["does.not.exist"]) == 2


def test_compare_semantics():
    assert compare(0.7293, 0.7293, {"abs": 0.001})[0]
    assert not compare(0.80, 0.7293, {"abs": 0.001})[0]
    assert compare(1.0e-4, 0.0001, {"max": 0.0005})[0]
    assert compare(-0.14, -0.14, {"range": [-0.166, -0.114]})[0]
    assert compare("SURVIVES", "SURVIVES", "exact")[0]
    assert not compare("RESIZED", "SURVIVES", "exact")[0]
