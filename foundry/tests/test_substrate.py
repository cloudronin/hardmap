"""Substrate layer (Sprint 6 Pebble, prereg_v12) — the RULES.

Locks the schema: the sealed REACH_LAYER validates, R1 typing + measured-manifest are enforced, the composing
validator runs the frozen eightfold charge gates AND the one-way substrate->charge asymmetry (a substrate cell
may never be derived-from a charge; a rule's substrate may never be a charge). The reach VERDICTS live in the
findings, not here.
"""
from foundry import substrate as SUB
from foundry.census import toy_census
from foundry.charges import FOUNDRY_SPEC


def _good_cell(**kw):
    base = dict(quantity="reach", value="short-range", canonical_ensemble="random xor-3", density_anchor="0.9*a*",
                status="measured", measured={"decay_rate": 0.4},
                provenance={"experiment": {"prereg": "v12", "manifest": "m", "seeds": "s", "code_commit": "c"}})
    base.update(kw)
    return SUB.SubstrateCell(**base)


def test_reach_layer_valid_and_regime_split():
    assert SUB.validate_layer(SUB.REACH_LAYER, FOUNDRY_SPEC) == []
    regime = {c: r.regime for r in SUB.REACH_LAYER for c in r.predicts}
    # measured charges are within-co-clone; oracle charges are between-co-clone (the resolution split)
    assert regime["landscape"] == "within-co-clone" and regime["average_case"] == "within-co-clone"
    for oracle in ("approximation", "parameterized", "counting", "parallelization"):
        assert regime[oracle] == "between-co-clone"
    assert regime["parallelization"] and SUB.REACH_LAYER[-1].predicts["parallelization"] == "none"  # negative control


def test_substrate_cell_gates():
    assert SUB.validate_substrate_cell(_good_cell()) == []
    assert SUB.validate_substrate_cell(_good_cell(canonical_ensemble="", density_anchor="")) != []   # R1 typing
    assert SUB.validate_substrate_cell(_good_cell(provenance={})) != []                               # manifest
    # a sentinel value must carry structural status
    assert SUB.validate_substrate_cell(_good_cell(value="n.a.", status="measured")) != []


def test_one_way_asymmetry_is_enforced():
    # a substrate cell may never be derived-from a charge column
    bad = _good_cell(provenance={"experiment": {"prereg": "v12", "manifest": "m", "seeds": "s", "code_commit": "c"},
                                 "derived_from": "approximation"})
    errs = SUB.validate_entry_with_substrate(toy_census()[0], [bad], FOUNDRY_SPEC)
    assert any("derived-from" in e for e in errs)
    # a predictive rule whose substrate IS a charge is rejected (substrate predicts charges, never the reverse)
    badrule = SUB.PredictiveRule("x", "approximation", {"landscape": "strong"}, "within-co-clone",
                                 "a fully stated mechanism goes here", "cite")
    assert SUB.validate_predictive_rule(badrule, FOUNDRY_SPEC) != []


def test_composing_validator_runs_eightfold_charge_gates_unchanged():
    # the charge columns are validated by the frozen eightfold validator; a good toy row + good cell is clean
    assert SUB.validate_entry_with_substrate(toy_census()[0], [_good_cell()], FOUNDRY_SPEC) == []
