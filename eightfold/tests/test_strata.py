"""Strata (Eightfold v2 additive layer) — lock the schema, the composing validator, and the additive-only property.

The load-bearing test is `test_v1_untouched`: it proves the layer NEVER changes v1 — every frozen row validates
clean through the v2 validator, and merge→strip round-trips back to the exact v1 row. The frozen atlas defends
itself (test_loader's round-trip), and Strata stays outside it.
"""
import json

from eightfold import strata, atlas


def _rows():
    return [json.loads(line) for line in atlas.resolve_atlas_path().read_text().splitlines() if line.strip()]


def test_selftest_green():
    assert strata.selftest_strata(verbose=True) == 0


def test_level_table_valid_and_objective_coupling():
    assert strata.validate_level_table() == []
    # the sealed finding: exactly the two objective-level charges are the coupled pair
    assert strata.OBJECTIVE_LEVEL_CHARGES == {"approximation", "parameterized"}
    # cross-level flagging fires on a mismatch, stays silent on a match
    assert strata.cross_level_flag("ensemble", "approximation") is not None
    assert strata.cross_level_flag("objective", "parameterized") is None


def test_applicability_gate_requires_reason_and_provenance():
    good = {"charge": "approximation", "applicability": "defined-informative",
            "applicability_reason": "APX-complete objective is non-degenerate", "applicability_provenance": "derived"}
    assert strata.validate_applicability(good) == []
    assert strata.validate_applicability({**good, "applicability_reason": ""}) != []      # the S1 gate
    assert strata.validate_applicability({**good, "applicability": "bogus"}) != []         # out of vocab
    assert strata.validate_applicability({**good, "applicability_provenance": "guess"}) != []
    assert strata.validate_applicability({"charge": "decision"}) == []                     # v1-only cell: silent


def test_objective_pin_gate():
    assert strata.validate_objective_pin({"problem_id": "x", "objective": "Min-Ones",
                                          "parameterization": "solution size", "pin_provenance": "derived"}) == []
    assert strata.validate_objective_pin({"problem_id": "x", "objective": "bogus"}) != []            # out of vocab
    assert strata.validate_objective_pin({"problem_id": "x", "objective": "Max-CSP"}) != []          # real pin, no prov
    assert strata.validate_objective_pin({"problem_id": "x", "objective": "none",
                                          "parameterization": "none"}) == []                          # trivial: no prov needed


def test_v2_composes_over_frozen_validator():
    rows = _rows()
    vc = next(r for r in rows if r["problem_id"] == "vertex-cover")
    v2 = strata.merge_row(vc, {"row_pins": {"objective": "Min-Ones", "parameterization": "solution size",
                                            "pin_provenance": "derived"},
                               "cell_meta": {"approximation": {"applicability": "defined-informative",
                                             "applicability_reason": "APX-complete; non-degenerate",
                                             "applicability_provenance": "derived"}}})
    assert strata.validate_entry_v2(v2) == []
    # missing reason must surface through the composing validator
    bad = strata.merge_row(vc, {"cell_meta": {"approximation": {"applicability": "defined-informative",
                                              "applicability_provenance": "derived"}}})
    assert any("applicability_reason" in e for e in strata.validate_entry_v2(bad))


def test_v1_untouched():
    """Every frozen row validates clean through the v2 validator (strata absent), and merge→strip is the exact
    inverse — the additive-only property, structurally."""
    rows = _rows()
    assert len(rows) == 118
    for r in rows:
        assert strata.validate_entry_v2(r) == []                      # v1 rows pass the composing validator
        assert strata.strip_strata(r) == r                            # no strata keys on a v1 row → identity
        merged = strata.merge_row(r, {"row_pins": {"objective": "none"},
                                      "cell_meta": {"decision": {"applicability": "defined-informative",
                                                    "applicability_reason": "x", "applicability_provenance": "derived"}}})
        assert strata.strip_strata(merged) == r                       # stripping the additions recovers v1 exactly
