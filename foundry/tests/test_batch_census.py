"""The unified batch census — tested at the seam where the drift got in.

THE FAILURE THIS GUARDS is not a wrong roster. It is a schema change that does not move the schema
string. That happened twice (b3->b4 renamed a key, b4->b5 added a field, both silently) and it happened
because the version was a literal inside eight copied files, so there was no single place for F4 to
bind. These tests hold the version to one site, hold the reader to all three shapes it must survive, and
prove the unified procedure reproduces the historical one exactly.
"""
import json
import shutil
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from foundry.catalog import batch_census as BC  # noqa: E402
from foundry.catalog import maptrail as M       # noqa: E402
from foundry.catalog import reservation as RES  # noqa: E402

LAT = ROOT / "foundry" / "results" / "lattice"
LEDGER = LAT / "observatory_reservation.jsonl"

HISTORICAL = sorted(LAT.glob("observatory_batch*_census.json"),
                    key=lambda p: int("".join(c for c in p.stem.split("batch")[1] if c.isdigit())))


# ── the reader survives the history it was built for ────────────────────────────────────────────────

def test_every_historical_census_reads():
    """All eight, whatever shape they are on disk. A reader that only handled the newest shape would
    make the old declarations unreadable, which is the same loss as rewriting them."""
    assert len(HISTORICAL) >= 8
    for p in HISTORICAL:
        d = BC.read(p)
        assert d["batch"] and d["roster"], p.name


def test_the_three_shapes_are_all_present_and_correctly_identified():
    """The drift, asserted as fact. If this ever reads differently, the history has been rewritten."""
    shapes = {BC.read(p)["batch"]: BC.read(p)["shape"] for p in HISTORICAL}
    assert shapes[3] == "v1-a", "b3 held ONE defect dict under `flagged_for_ruling`"
    assert shapes[4] == "v1-b", "b4 renamed the key and widened it to a mapping"
    assert all(shapes[b] == "v1-c" for b in range(5, 11)), "b5+ added capture_mode to roster rows"


def test_shape_is_read_off_structure_not_off_the_declared_string():
    """All three historical shapes DECLARE v1, so the string is no evidence. A reader that trusted it
    would reproduce the defect in the code written to survive it."""
    declared = {BC.read(p)["declared_schema"] for p in HISTORICAL}
    assert declared == {"observatory-batch-census/v1"}, "the whole point: one string, three shapes"
    assert len({BC.read(p)["shape"] for p in HISTORICAL}) == 3


def test_normalisation_is_total():
    """After reading, every row has a capture_mode and every carried_forward is a mapping — regardless
    of which shape it came from. Consumers get one contract, not three."""
    for p in HISTORICAL:
        d = BC.read(p)
        assert all("capture_mode" in s for s in d["roster"].values()), p.name
        assert isinstance(d["carried_forward"], dict), p.name


def test_b3s_single_defect_dict_becomes_a_mapping():
    """v1-a keyed its one defect by its own 'problem' field. The normalised form must not lose it."""
    d = BC.read(LAT / "observatory_batch3_census.json")
    assert "minimum-common-string-partition" in d["carried_forward"]
    assert "problem" not in d["carried_forward"]["minimum-common-string-partition"]


# ── the version has exactly one site ────────────────────────────────────────────────────────────────

def test_the_version_string_lives_in_one_place():
    """F4's precondition. If the literal reappears in a second module, the law stops binding again."""
    sites = []
    for p in (ROOT / "foundry").rglob("*.py"):
        if "observatory-batch-census/v" in p.read_text():
            sites.append(p.relative_to(ROOT))
    assert sites == [Path("foundry/catalog/batch_census.py")], f"version literal escaped to {sites}"


def test_no_ninth_copy_of_the_census_procedure():
    """The drift's mechanism was copy-and-edit. The eight historical scripts stand as the record of how
    their censuses were made; a NINTH would mean the unification was advisory. Batch 11 has a
    declaration file to start from and `declaration_from_census` to build it with."""
    copies = sorted(p.name for p in (ROOT / "dev").glob("observatory_batch*_census.py"))
    assert len(copies) == 8, f"a new census script appeared: {copies}"


# ── the unified procedure reproduces the historical one ─────────────────────────────────────────────

def _rederive(batch, tmp_path):
    """Re-derive a historical census through the unified procedure, against a COPIED ledger so
    idempotency returns the original reservation rather than minting a new one."""
    shutil.copy(LEDGER, tmp_path / "ledger.jsonl")
    decl = BC.declaration_from_census(LAT / f"observatory_batch{batch}_census.json")
    (tmp_path / "decl.json").write_text(json.dumps(decl, indent=1))
    doc, rec = BC.declare(tmp_path / "decl.json", LAT, tmp_path / "ledger.jsonl",
                          tmp_path / "trail.jsonl", out=tmp_path / "out.json", before_batch=batch)
    return doc, json.loads((LAT / f"observatory_batch{batch}_census.json").read_text())


def test_batch10_rederives_identically_except_the_version(tmp_path):
    """The strongest available equivalence: the newest historical shape differs from the unified output
    in the schema string and NOTHING else. The unification loses nothing."""
    doc, orig = _rederive(10, tmp_path)
    differing = sorted(k for k in set(doc) | set(orig) if doc.get(k) != orig.get(k))
    assert differing == ["schema"], f"unexpected drift: {differing}"


@pytest.mark.parametrize("batch,expected", [
    (3, ["carried_forward", "flagged_for_ruling", "roster", "schema"]),
    (4, ["roster", "schema"]),
])
def test_older_shapes_differ_by_exactly_the_documented_transitions(batch, expected, tmp_path):
    """b3 and b4 differ from v2 by precisely the two shape changes named in SCHEMA_HISTORY — the key
    rename and the added field — and by nothing else. The drift is fully characterised, not approximated."""
    doc, orig = _rederive(batch, tmp_path)
    assert sorted(k for k in set(doc) | set(orig) if doc.get(k) != orig.get(k)) == expected


def test_rederivation_never_grows_the_ledger(tmp_path):
    """A reservation is declared once. If re-deriving a census could append a second record, the
    reservation would drift under the artifact it exists to fix."""
    before = len(RES.read_ledger(LEDGER))
    _rederive(10, tmp_path)
    assert len(RES.read_ledger(tmp_path / "ledger.jsonl")) == before


# ── event-time emission is a property of the procedure ──────────────────────────────────────────────

def test_declaring_emits_its_own_trail_record(tmp_path):
    """Kill 3: the machinery performing the act emits the record. Not a caller, not a later pass."""
    _rederive(10, tmp_path)
    recs = M.read(tmp_path / "trail.jsonl")
    assert len(recs) == 1 and recs[0]["declares_batch"] == 10
    assert recs[0]["touches_no_measured_value"] is True
    assert recs[0]["schema"] == BC.SCHEMA


def test_a_census_on_disk_without_its_trail_record_is_a_build_failure(tmp_path):
    """`assert_trailed` is the mechanical form of 'a write that reaches disk without its trail record
    is a build failure'. `since` keeps it off the historical censuses, which are retro-labelled rather
    than back-emitted as if they had been contemporaneous."""
    (tmp_path / "observatory_batch99_census.json").write_text(json.dumps(
        {"schema": BC.SCHEMA, "batch": 99, "roster": {}, "reservation": {}, "published": []}))
    with pytest.raises(RuntimeError, match="UNTRAILED CENSUS"):
        BC.assert_trailed(tmp_path, tmp_path / "empty.jsonl", since=99)
    BC.assert_trailed(tmp_path, tmp_path / "empty.jsonl", since=100)  # below the floor: silent


def test_historical_censuses_are_not_required_to_carry_trail_records():
    """They predate event-time emission. Back-emitting them would be history written late and presented
    as contemporaneous — the one thing the maptrail's `reconstructed` flag exists to prevent."""
    BC.assert_trailed(LAT, LAT / "maptrail.jsonl", since=11)


# ── the declaration/census relationship is executable ───────────────────────────────────────────────

def test_declaration_round_trips():
    """`census = declaration + reservation + status`, asserted by construction rather than in prose."""
    for p in HISTORICAL:
        d = BC.declaration_from_census(p)
        assert set(d) == {"batch", "why_this_batch", "families", "roster", "carried_forward"}
        assert set(d["roster"]) == set(BC.read(p)["roster"])


def test_a_declaration_using_an_undeclared_family_ramp_is_refused(tmp_path):
    """The check that stops a roster naming a family whose ramp nothing declared."""
    (tmp_path / "d.json").write_text(json.dumps({
        "batch": 99, "why_this_batch": "x", "families": {"graph": {"census_ramp": "r", "ramp_values": [1]}},
        "roster": {"row-a": {"family": "optimization"}}}))
    with pytest.raises(ValueError, match="no declared ramp"):
        BC.load_declaration(tmp_path / "d.json")
