"""Coverage accounting (R2) + the A1 done-gate on the bundled atlas."""
from eightfold import atlas, charges as C


def _mixed_entry():
    cells = [atlas.ChargeCell(ch, "n.a.", "n/a", "structural") for ch in C.CHARGES]
    by = {c.charge: i for i, c in enumerate(cells)}
    cells[by["decision"]] = atlas.ChargeCell("decision", "NPC", "d", "claimed", {"citation": "x"})
    cells[by["counting"]] = atlas.ChargeCell("counting", "#P-complete", "c", "uncited-folklore", {"note": "f"})
    cells[by["approximation"]] = atlas.ChargeCell("approximation", "open", "a", "structural")
    return atlas.ProblemEntry("p", "P", "graph", "enc", cells, "2026-07-21", "t")


def test_coverage_accounting_R2():
    rep = atlas.coverage_report([_mixed_entry()])
    # applicable: decision (NPC) + counting (folklore) + approximation (open) = 3; the 5 n.a. don't count.
    assert rep["applicable"] == 3
    # cited-filled: only the claimed decision cell.
    assert rep["cited_filled"] == 1
    assert rep["uncited_folklore"] == 1


def test_na_does_not_lower_coverage():
    # an entry with one cited cell and the rest n.a. -> 100% coverage (n.a. is correctly filled, not missing).
    cells = [atlas.ChargeCell(ch, "n.a.", "n/a", "structural") for ch in C.CHARGES]
    cells[0] = atlas.ChargeCell("decision", "NPC", "d", "claimed", {"citation": "x"})
    rep = atlas.coverage_report([atlas.ProblemEntry("p", "P", "graph", "e", cells, "2026-07-21", "t")])
    assert rep["applicable"] == 1 and rep["cited_filled"] == 1
    assert rep["coverage_ratio"] == 1.0


def test_real_atlas_meets_A1_gate():
    rep = atlas.coverage_report(atlas.load_atlas())
    assert rep["uncited_folklore"] == 0
    assert rep["coverage_ratio"] >= 0.70
    assert rep["a1_gate_pass"] is True


def test_a2_per_charge_gate_fields_R21():
    r = atlas.coverage_report(atlas.load_atlas())
    assert set(r["core_charge_ratios"]) == set(atlas.CORE_CHARGES)
    assert set(r["frontier_open_rates"]) == set(atlas.FRONTIER_CHARGES)
    # the gate is per-charge: passes iff every core charge clears 85% (and zero folklore)
    assert r["a2_core_gate_pass"] == (all(v >= 0.85 for v in r["core_charge_ratios"].values())
                                      and r["uncited_folklore"] == 0)
