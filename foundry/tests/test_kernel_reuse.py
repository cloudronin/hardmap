"""Foundry ↔ Eightfold kernel reuse — the Phase-K payoff: one validator + harness, two vocabularies.

Proves the shared kernel (eightfold.atlas.validate + the Crucible-hardened harness) accepts Foundry's census
rows under FOUNDRY_SPEC, with no eightfold modification. Tests the machinery + the pre-registered NPI
calibration RULE (prediction 1), not science verdicts (the real census is N1+).
"""
import pytest

from eightfold import atlas
from eightfold.atlas import ChargeCell
from eightfold.charges import EIGHTFOLD_SPEC
from foundry.charges import FOUNDRY_SPEC
from foundry.census import derived, language, toy_census


def test_foundry_spec_entailment_layer_consistent():
    assert FOUNDRY_SPEC.validate_entailment_layer() == []
    assert FOUNDRY_SPEC.name == "foundry" and len(FOUNDRY_SPEC.charges) == 9
    assert "localization" in FOUNDRY_SPEC.charges


def test_shared_validator_accepts_foundry_rows():
    # the eightfold validator, driven by FOUNDRY_SPEC, validates census rows CLEAN — the Phase-K payoff
    for row in toy_census():
        assert atlas.validate(row, FOUNDRY_SPEC) == [], (row.problem_id, atlas.validate(row, FOUNDRY_SPEC))


def test_foundry_derived_gate_side_must_equal_value():
    # gate 6b (Crucible S4) fires under FOUNDRY_SPEC: derived condition_check.side must equal the value
    cells = [ChargeCell("decision", "NPC", "x", "derived",
                        {"citation": "c", "condition_check": {"theorem": "T", "condition": "c", "side": "P"}})]
    cells += [ChargeCell(ch, "n.a.", "n/a", "structural") for ch in FOUNDRY_SPEC.charges if ch != "decision"]
    errs = atlas.validate(language("bad", "bad", "affine", "enc", cells), FOUNDRY_SPEC)
    assert any("side" in e and "must equal" in e for e in errs)


def test_derived_allowed_broadened_to_oracle_columns():
    # Foundry allows `derived` on oracle columns beyond eightfold's {counting}; measured stays on instruments
    assert {"decision", "approximation", "localization"} <= FOUNDRY_SPEC.derived_allowed
    assert FOUNDRY_SPEC.measured_allowed == frozenset({"average_case", "landscape"})


def test_wrong_spec_rejects_foundry_row():
    # a census row (9 charges incl. localization) validated against EIGHTFOLD_SPEC fails — the spec matters
    assert atlas.validate(toy_census()[0], EIGHTFOLD_SPEC)


def test_harness_composes_with_foundry_spec():
    pytest.importorskip("numpy")  # the harness primitives are behind eightfold's [analysis] extra
    import numpy as np
    from eightfold import crucible as X
    from eightfold import structure as S
    rows = toy_census()
    triples = [["decision", "counting", "parallelization"],
               ["decision", "approximation", "parameterized"],
               ["localization", "approximation", "parameterized"]]
    gl = S.gap_list(rows, spec=FOUNDRY_SPEC, triples=triples)
    assert set(gl) >= {"gaps", "forbidden", "n_gaps", "n_forbidden"}
    _, _, base = S._grid(rows)
    rng = np.random.default_rng(0)
    seen = 0
    for null in X._null_chain(base, rng, burn=50, thin=10, m=2, spec=FOUNDRY_SPEC):
        seen += 1
        assert all(X._row_valid(r, FOUNDRY_SPEC) for r in null)  # entailment-valid under FOUNDRY_SPEC
    assert seen == 2


def test_prediction1_npi_calibration_toy():
    # prediction 1 (known-answer): the dichotomy makes the NPI row empty; a non-empty NPI row = pipeline bug
    npi = [r.problem_id for r in toy_census()
           for c in r.charges if c.charge == "decision" and c.value == "NPI-candidate"]
    assert npi == []
