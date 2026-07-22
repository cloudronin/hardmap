"""QC-gate unit tests for atlas.validate (retargets physmap's corpus-validator tests)."""
from eightfold import atlas, charges as C


def _cells(overrides=None):
    overrides = overrides or {}
    out = []
    for ch in C.CHARGES:
        out.append(overrides.get(ch, atlas.ChargeCell(ch, "n.a.", "not applicable here", "structural")))
    return out


def _entry(overrides=None, **kw):
    d = dict(problem_id="p", problem_name="P", problem_family="graph", canonical_encoding="enc",
             charges=_cells(overrides), last_reviewed="2026-07-21", reviewer="t")
    d.update(kw)
    return atlas.ProblemEntry(**d)


def _cell(charge, value, status="claimed", prov=None, perspective=None):
    return atlas.ChargeCell(charge, value, "canonical task", status, prov or {}, perspective)


def test_valid_entry_passes():
    e = _entry({"decision": _cell("decision", "NPC", prov={"citation": "GJ 1979"})})
    assert atlas.validate(e) == []


def test_bad_value_rejected():
    e = _entry({"decision": _cell("decision", "P-ish", prov={"citation": "x"})})
    assert any("not in vocab" in s for s in atlas.validate(e))


def test_missing_canonical_task_rejected():
    bad = atlas.ChargeCell("decision", "NPC", "", "claimed", {"citation": "x"})
    assert any("canonical_task" in s for s in atlas.validate(_entry({"decision": bad})))


def test_real_value_needs_citation_or_folklore():
    e = _entry({"decision": _cell("decision", "NPC", prov={})})
    assert any("gate 3" in s for s in atlas.validate(e))
    ok = _entry({"decision": _cell("decision", "NPC", status="uncited-folklore", prov={"note": "folklore"})})
    assert atlas.validate(ok) == []


def test_confirmed_requires_primary_source():
    e = _entry({"decision": _cell("decision", "NPC", status="confirmed", prov={"citation": "x"})})
    assert any("primary_source" in s for s in atlas.validate(e))


def test_perspective_required_for_proof_size():
    e = _entry({"proof_size": _cell("proof_size", "exp", prov={"citation": "Haken"})})
    assert any("perspective" in s for s in atlas.validate(e))
    ok = _entry({"proof_size": _cell("proof_size", "exp", prov={"citation": "Haken"}, perspective="Resolution")})
    assert atlas.validate(ok) == []


def test_measured_rejected_on_decision_R9():
    exp = {"prereg": "p", "manifest": "m", "seeds": "s", "code_commit": "c"}
    e = _entry({"decision": _cell("decision", "NPC", status="measured", prov={"experiment": exp})})
    assert any("R9" in s for s in atlas.validate(e))


def test_measured_allowed_on_landscape_with_experiment_R9():
    exp = {"prereg": "p", "manifest": "m", "seeds": "s", "code_commit": "c"}
    ok = _entry({"landscape": _cell("landscape", "freezing-measured", status="measured",
                                    prov={"experiment": exp})})
    assert atlas.validate(ok) == []
    bad = _entry({"landscape": _cell("landscape", "freezing-measured", status="measured", prov={})})
    assert any("R9" in s for s in atlas.validate(bad))


def test_derived_rejected_off_counting_crucible_S4():
    cc = {"theorem": "T", "condition": "hard-side", "side": "NPC"}
    e = _entry({"decision": _cell("decision", "NPC", status="derived",
                                  prov={"citation": "x", "condition_check": cc})})
    assert any("derived" in s and "counting" in s for s in atlas.validate(e))


def test_derived_allowed_on_counting_with_condition_check_S4():
    cc = {"theorem": "Dyer-Greenhill 2000", "condition": "H neither complete nor complete-bipartite",
          "side": "#P-complete"}
    ok = _entry({"counting": _cell("counting", "#P-complete", status="derived",
                                   prov={"citation": "DyerGreenhill2000", "condition_check": cc})})
    assert atlas.validate(ok) == []
    # missing condition_check → rejected
    bad = _entry({"counting": _cell("counting", "#P-complete", status="derived",
                                    prov={"citation": "DyerGreenhill2000"})})
    assert any("condition_check" in s for s in atlas.validate(bad))


def test_derived_side_must_equal_value_S4():
    cc = {"theorem": "T", "condition": "c", "side": "FP"}   # side disagrees with the cell value
    mism = _entry({"counting": _cell("counting", "#P-complete", status="derived",
                                     prov={"citation": "x", "condition_check": cc})})
    assert any("side" in s and "must equal" in s for s in atlas.validate(mism))


def test_derived_still_needs_citation_unlike_measured_S4():
    # Unlike `measured`, `derived` is NOT citation-exempt: the dichotomy theorem must be cited (gate 3).
    cc = {"theorem": "T", "condition": "c", "side": "#P-complete"}
    e = _entry({"counting": _cell("counting", "#P-complete", status="derived",
                                  prov={"condition_check": cc})})
    assert any("gate 3" in s for s in atlas.validate(e))


def test_snapshot_gate_R10():
    e = _entry({"decision": _cell("decision", "NPC", prov={"url": "http://x"})})
    errs = atlas.validate(e)
    assert any("R10" in s and "snapshot" in s for s in errs)
    ok = _entry({"decision": _cell("decision", "NPC",
                                   prov={"url": "http://x", "snapshot": "http://web.archive.org/y",
                                         "retrieved": "2026-07-21"})})
    assert atlas.validate(ok) == []


def test_data_violating_entailment_rejected():
    # counting=FP with decision=NPC violates E1 — must be flagged.
    e = _entry({"decision": _cell("decision", "NPC", prov={"citation": "x"}),
                "counting": _cell("counting", "FP", prov={"citation": "y"})})
    assert any("entailment rule" in s for s in atlas.validate(e))


def test_missing_charge_rejected():
    e = _entry()
    e.charges = e.charges[:-1]  # drop one charge
    assert any("one cell per charge" in s for s in atlas.validate(e))


def test_new_A2_vocab_values_valid():
    assert {"EPTAS", "APX"} <= C.allowed_values("approximation")   # R19 adds APX
    assert "freezing-measured" in C.allowed_values("landscape")
    assert {"hard-on-average-provable", "hard-on-average-conjectured"} <= C.allowed_values("average_case")  # R18
    # worst-case-to-average-equiv was a relation, not a difficulty value — removed (R18)
    assert "worst-case-to-average-equiv" not in C.allowed_values("average_case")


def test_self_reduction_gate_R18():
    e = _entry()
    avg = e.charges[[c.charge for c in e.charges].index("average_case")]
    avg.worst_to_average_self_reduction = True
    avg.provenance = {}
    assert any("worst_to_average_self_reduction=true needs a citation" in s for s in atlas.validate(e))
    bad = _entry({"decision": _cell("decision", "NPC", prov={"citation": "x"})})
    bad.charges[[c.charge for c in bad.charges].index("decision")].worst_to_average_self_reduction = True
    assert any("R18" in s for s in atlas.validate(bad))


def test_transition_known_gate_R17():
    # transition_known is average_case-only
    bad = _entry({"decision": _cell("decision", "NPC", prov={"citation": "x"})})
    bad.charges[[c.charge for c in bad.charges].index("decision")].transition_known = True
    assert any("R17" in s for s in atlas.validate(bad))
    # transition_known=true needs a citation for the transition
    e = _entry()
    avg = e.charges[[c.charge for c in e.charges].index("average_case")]
    avg.transition_known = True
    avg.provenance = {}
    assert any("transition_known=true needs a citation" in s for s in atlas.validate(e))


def test_freezing_measured_ok_as_measured_landscape():
    exp = {"prereg": "p", "manifest": "m", "seeds": "s", "code_commit": "c"}
    ok = _entry({"landscape": _cell("landscape", "freezing-measured", status="measured",
                                    prov={"experiment": exp})})
    assert atlas.validate(ok) == []
