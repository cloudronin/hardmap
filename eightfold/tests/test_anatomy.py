"""Anatomy — the frozen-artifact guard. Models tests/test_atlas_v3.py.

Tests lock RULES and DATA INVARIANTS, never verdicts: the passport table's *contents* may change as
columns are added, but the artifact's bytes, its schema-validity, and the completeness of its passports
are pinned. `skipif` keeps the suite green before the artifact is built.
"""
import hashlib
import json
import pathlib

import pytest

from eightfold import anatomy, atlas

AT = pathlib.Path(atlas.__file__).resolve().parent / "results" / "atlas"
ART = AT / "anatomy_v1.jsonl"
PASS = AT / "anatomy-passports.json"
INST = AT / "anatomy-instruments.json"
ANATOMY_SHA256 = "8ff11f8a33bbdce7c6fbd3cf2607aad48462240720b90fa511c2350d9dcb5182"

skip_no_art = pytest.mark.skipif(not ART.exists(), reason="anatomy_v1.jsonl not built yet (S2)")


def _rows():
    return [json.loads(l) for l in ART.read_text().splitlines() if l.strip()]


def test_charge_atlases_untouched():
    """The founding law at the byte level: Anatomy reads the charge atlases, never writes them."""
    for name, want in (("atlas.jsonl", "6d53a4f1"), ("atlas_v2.jsonl", "784f4739"),
                       ("atlas_v3.jsonl", "e62f3c28")):
        got = hashlib.sha256((AT / name).read_bytes()).hexdigest()
        assert got.startswith(want), f"{name} drifted: {got[:8]} != {want}"


@skip_no_art
def test_anatomy_byte_frozen():
    assert hashlib.sha256(ART.read_bytes()).hexdigest() == ANATOMY_SHA256


@skip_no_art
def test_anatomy_validates_clean_and_keys_are_unique():
    rows = _rows()
    assert anatomy.validate_level_registry() == []
    keys = [r["row_key"] for r in rows]
    assert len(keys) == len(set(keys)), "row_key must be unique"
    errs = []
    for r in rows:
        errs.extend(anatomy.validate_anatomy_row(r))
    assert errs == [], errs[:5]


@skip_no_art
def test_both_universes_present_at_expected_counts():
    from collections import Counter
    c = Counter(r["universe"] for r in _rows())
    assert c[anatomy.NATURAL] == 345, c
    assert c[anatomy.BOOLEAN] == 4072, c


@skip_no_art
def test_no_column_appears_outside_its_declared_universe():
    """Column-level typing (SCHEMA §1.1) is the whole reason the artifact is not 90% ceremonial n.a."""
    for r in _rows():
        for cell in r["features"]:
            assert anatomy.COLUMNS[cell["feature"]]["universe"] == r["universe"], \
                f"{cell['feature']} on a {r['universe']} row"


@skip_no_art
def test_na_cells_carry_a_mandatory_reason():
    """R1 typing, enforced for real rather than by canonical_task non-emptiness."""
    for r in _rows():
        for cell in r["features"]:
            if cell.get("value") == "n.a.":
                assert cell.get("reason"), f"{r['row_key']}.{cell['feature']}: n.a. without a reason"


@skip_no_art
def test_coded_cells_resolve_to_a_real_instrument_record():
    insts = json.loads(INST.read_text())["instruments"] if INST.exists() else {}
    for r in _rows():
        for cell in r["features"]:
            if cell.get("provenance_status") == anatomy.PROV_CODED:
                assert cell.get("instrument_ref") in insts, \
                    f"{r['row_key']}.{cell['feature']}: instrument_ref does not resolve"


@skip_no_art
def test_bridge_citations_are_pinned_only():
    """Pin-before-net (SCHEMA §3.6): an UNPINNED ledger row may not be borrowed as a warrant."""
    for r in _rows():
        for cell in r["features"]:
            b = cell.get("bridge_citation")
            if b:
                assert b in anatomy.PINNED_BRIDGES, f"{r['row_key']}.{cell['feature']}: {b} not PINNED"
                assert b not in anatomy.UNPINNED_BRIDGES


@pytest.mark.skipif(not PASS.exists(), reason="passport table not built yet (S2)")
def test_passport_table_is_complete():
    """S3 freeze gate: every shipped column carries verdicts. COMPLETE, not all-green."""
    doc = json.loads(PASS.read_text())
    cols = doc["columns"]
    for c in anatomy.COLUMNS:
        assert c in cols, f"shipped column {c} has no passport"
        assert cols[c]["invariance"] in anatomy.INVARIANCE_VERDICTS
        assert "variance" in cols[c], f"{c}: variance flags not recorded"
        if cols[c]["invariance"] != anatomy.INVARIANT:
            assert cols[c].get("property_of"), f"{c}: relative column must say what it is a property of"


def test_duplicate_bridges_collapse_to_one_calibration_point():
    """§1.decision and §1.parameterized-tw are the SAME Courcelle theorem (ledger §9.2)."""
    assert anatomy.independent_bridge_count({"§1.decision", "§1.parameterized-tw"}) == 1
    assert anatomy.independent_bridge_count({"§1.decision", "§3.decision"}) == 2


def test_typing_sentinel_registered():
    """A row that keeps catching drift is an instrument, and instruments get registered."""
    s = anatomy.TYPING_SENTINELS["graph-3-coloring"]
    assert len(s["forced_corrections"]) >= 3
