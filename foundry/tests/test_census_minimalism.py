"""Census minimalism, made mechanical (methods — minted from N6's contamination).

THE RULE: a census computes its kill's inputs and nothing else. Joining predictor to outcome before the
seal is contamination however natural the join.

N6's census violated it by hand — it computed `infl` (correctly, the kill's input) and then joined it to
`fair_null_excess` (not the kill's input) and correlated them, which disclosed the sealed relationship and
killed the seal. The rule was minted the same day. This is the rule compiled into machinery.

THE ENFORCEMENT IS DYNAMIC, NOT A SOURCE SCAN. A grep for forbidden filenames is defeated by any
indirection — a path built from parts, a variable, a loop over a directory. So the census is actually RUN
with `Path.read_text` instrumented, and every file it touches is recorded. A census that reads an outcome
artifact fails here even if the read is three layers of helper deep.
"""
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "dev")); sys.path.insert(0, str(ROOT))

# Artifacts carrying an OUTCOME. A census that reads any of these has joined predictor to outcome.
FORBIDDEN = {
    "n1_results.json",                 # fair-null excess, the outcome N6-R bets on
    "terrain_v1_results.json",         # excess ladder
    "n6_hull_census.json",             # carries excess alongside inflation — the contaminated artifact
    "sounding_trajectories.json",      # excess trajectories
    "n2_dense_control_qualification.json",   # CP excesses
}


def _run_instrumented(module_name, out_attrs=("OUT",), shrink=None):
    """Run a census module's main() with file reads recorded. Returns the set of filenames read."""
    import importlib
    mod = importlib.import_module(module_name)
    seen = set()
    orig = Path.read_text

    def spy(self, *a, **k):
        seen.add(self.name)
        return orig(self, *a, **k)

    saved = {}
    try:
        Path.read_text = spy
        for j, oa in enumerate(out_attrs):
            saved[oa] = getattr(mod, oa)
            setattr(mod, oa, ROOT / "foundry" / "results" / "lattice" / f"_test_{module_name}_{j}.json")
        for k, v in (shrink or {}).items():
            saved[k] = getattr(mod, k)
            setattr(mod, k, v)
        rc = mod.main()
    finally:
        Path.read_text = orig
        for j, oa in enumerate(out_attrs):
            t = ROOT / "foundry" / "results" / "lattice" / f"_test_{module_name}_{j}.json"
            if t.exists():
                t.unlink()
        for k, v in saved.items():
            setattr(mod, k, v)
    return seen, rc


def test_control_census_reads_no_outcome_artifact():
    """Phase 0's census must touch the roster and nothing carrying an outcome."""
    seen, rc = _run_instrumented("n6r_control_census",
                                 shrink={"SAMPLE_PER_CELL": 1, "K_DRAWS": 2})
    assert rc == 0, "census did not complete"
    leaked = seen & FORBIDDEN
    assert not leaked, (
        f"CENSUS MINIMALISM VIOLATED — the census read outcome artifact(s) {sorted(leaked)}. "
        f"A census computes its kill's inputs and nothing else; joining predictor to outcome before the "
        f"seal is contamination. Files read: {sorted(seen)}")


def test_tranche_declaration_reads_no_outcome_artifact():
    """Phase 1's tranche must be declared outcome-blind — the same rule, the same enforcement.

    A guard written for one script and never extended to its successors is how a rule decays into a
    story about a rule. Every outcome-blind phase is bound here."""
    seen, rc = _run_instrumented("n6r_tranche")
    assert rc == 0, "tranche declaration did not complete"
    leaked = seen & FORBIDDEN
    assert not leaked, (
        f"CENSUS MINIMALISM VIOLATED — the tranche declaration read outcome artifact(s) {sorted(leaked)}. "
        f"The tranche is fixed BEFORE any hull or excess exists. Files read: {sorted(seen)}")


def test_tranche_hash_is_stable():
    """The tranche hash is the object Phase 2's predictions will be sealed against. If it is not
    reproducible, the seal has nothing to bind to."""
    import importlib
    mod = importlib.import_module("n6r_tranche")
    doc = json.loads((ROOT / "foundry" / "results" / "lattice" / "n6r_tranche.json").read_text())
    import hashlib
    payload = {"discovery": doc["discovery"], "calibration": doc["calibration"]}
    recomputed = hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    assert recomputed == doc["TRANCHE_HASH"], (
        "the tranche hash does not reproduce from its own member lists — the seal would bind to nothing")


def test_hull_phase_reads_no_outcome_artifact():
    """Phase 2 computes the PREDICTOR. It must not touch an outcome — that is exactly the join whose
    absence makes the sealed prediction blind."""
    seen, rc = _run_instrumented("n6r_hulls", out_attrs=("OUT_INFL", "OUT_PRED"))
    assert rc == 0, "hull phase did not complete"
    leaked = seen & FORBIDDEN
    assert not leaked, (
        f"CENSUS MINIMALISM VIOLATED — the hull phase read outcome artifact(s) {sorted(leaked)}. "
        f"The predictor is frozen and the predictions hashed BEFORE any outcome exists. "
        f"Files read: {sorted(seen)}")


def test_the_guard_can_actually_fail():
    """A guard that cannot fail is not a guard. Prove the instrumentation sees a forbidden read."""
    seen = set()
    orig = Path.read_text

    def spy(self, *a, **k):
        seen.add(self.name)
        return orig(self, *a, **k)

    target = ROOT / "foundry" / "results" / "lattice" / "n1_results.json"
    if not target.exists():
        pytest.skip("n1_results.json absent")
    try:
        Path.read_text = spy
        json.loads(target.read_text())
    finally:
        Path.read_text = orig
    assert seen & FORBIDDEN, "the instrumentation failed to record a forbidden read"
