"""Entailment layer: R6 consistency, the E6/E7 object-mismatch demotion, and triage behavior."""
from eightfold import charges as C


def test_layer_consistent_R6():
    assert C.validate_entailment_layer() == []


def test_every_rule_states_preconditions_and_citation_R6():
    for r in C.ENTAILMENT_LAYER:
        assert r.preconditions and len(r.preconditions.strip()) >= 20, r.name
        assert r.citation and len(r.citation.strip()) >= 5, r.name


def test_E1_E2_forbid():
    assert "counting_FP_implies_decision_P" in C.theorem_forbidden_by({"counting": "FP", "decision": "NPC"})
    assert "parallel_defined_only_within_P" in C.theorem_forbidden_by({"decision": "NPC", "parallelization": "NC"})
    assert "parallel_defined_only_within_P" in C.theorem_forbidden_by({"decision": "PSPACE-complete", "parallelization": "P-complete"})


def test_counting_FP_with_decision_P_is_fine():
    assert C.theorem_forbidden_by({"counting": "FP", "decision": "P"}) == []


def test_object_mismatch_rules_demoted_R6():
    # E6/E7 must NOT forbid (decision=P, approximation=inapprox) — the XOR-SAT counterexample.
    assert C.theorem_forbidden_by({"decision": "P", "approximation": "inapprox"}) == []


def test_only_E1_E2_are_column_forbidding():
    forbidding = {r.name for r in C.ENTAILMENT_LAYER if r.forbids}
    assert forbidding == {"counting_FP_implies_decision_P", "parallel_defined_only_within_P"}


def test_layer_rejects_rule_missing_preconditions():
    bad = [C.EntailmentRule(name="x", antecedent={"decision": frozenset({"P"})},
                            preconditions="", citation="")]
    assert C.validate_entailment_layer(bad)


def test_layer_rejects_out_of_vocab_value():
    bad = [C.EntailmentRule(name="x", antecedent={"decision": frozenset({"NOT-A-VALUE"})},
                            preconditions="a" * 30, citation="cite here")]
    assert any("not in its vocab" in e for e in C.validate_entailment_layer(bad))


def test_R22_decision_partial_order():
    vals = set(C.CHARGE_REAL_VALUES["decision"])
    edges = {(a, b) for a, b in C.DECISION_PARTIAL_ORDER}
    for a, b in edges:
        assert a in vals and b in vals, (a, b)

    def below(a, b):
        # is a strictly below b in the transitive closure?
        frontier, seen = [a], set()
        while frontier:
            x = frontier.pop()
            for u, v in edges:
                if u == x:
                    if v == b:
                        return True
                    if v not in seen:
                        seen.add(v)
                        frontier.append(v)
        return False

    # NPC and coNP-complete are SIBLINGS — neither below the other (NP vs coNP is open)
    assert not below("NPC", "coNP-complete")
    assert not below("coNP-complete", "NPC")
    # but both are below PH-complete, and P is below NPC
    assert below("NPC", "PH-complete") and below("coNP-complete", "PH-complete")
    assert below("P", "NPC") and below("PSPACE-complete", "beyond-PSPACE")
    # decision is deliberately NOT in the linear ORDINAL (it is only partially ordered)
    assert "decision" not in C.ORDINAL


def test_R12_bridges_present_and_informational():
    names = {r.name for r in C.ENTAILMENT_LAYER}
    assert {"eptas_implies_fpt_SAME_PARAMETER", "w1_hardness_rules_out_eptas_MARX"} <= names
    # informational (R12): they document the approx<->parameterized bridge but forbid no column cell.
    assert C.theorem_forbidden_by({"approximation": "EPTAS"}) == []
    assert C.theorem_forbidden_by({"parameterized": "W[1]"}) == []


def test_R25_cai_chen_bridge_present_and_does_not_overreach():
    names = {r.name for r in C.ENTAILMENT_LAYER}
    assert "max_snp_or_min_f_pi1_membership_implies_fpt_CAI_CHEN" in names
    # It is CLASS MEMBERSHIP (off-column) that entails FPT, so the rule must forbid NO column cell — encoding
    # "APX-complete => FPT" would be the over-broad R6 error (Independent Set is APX-ish and W[1]-hard).
    rule = next(r for r in C.ENTAILMENT_LAYER if r.name.endswith("CAI_CHEN"))
    assert rule.forbids is None
    assert C.theorem_forbidden_by({"approximation": "APX-complete"}) == []
    assert C.theorem_forbidden_by({"approximation": "APX-complete", "parameterized": "W[1]"}) == []
