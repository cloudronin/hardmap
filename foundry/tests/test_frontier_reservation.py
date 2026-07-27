"""The frontier reservation, tested where it can actually fail (Helm §5, Kill 2).

THE PROPERTY UNDER TEST is not "the batch script meant well". It is that a reserved row is ABSENT from
every disclosed artifact — the catalog, the database, the frames — and that the machinery raises rather
than quietly proceeding if one ever appears. Kill 2 says a detected leak halts all open waves, so the
detection has to be real.

A GUARD THAT CANNOT FAIL IS NOT A GUARD. `test_the_guard_can_actually_fail` feeds `assert_absent` a
reserved row and asserts it raises. Without that test, every other assertion here would pass just as
happily against a function whose body was `pass`.
"""
import json
import sqlite3
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "dev"))

from foundry.catalog import reservation as RES  # noqa: E402

LAT = ROOT / "foundry" / "results" / "lattice"
LEDGER = LAT / "observatory_reservation.jsonl"


def _reserved():
    if not LEDGER.exists():
        pytest.skip("no reservation ledger yet")
    return RES.reserved_rows(LEDGER)


# ── the rule ────────────────────────────────────────────────────────────────────────────────────────
def test_selection_is_deterministic():
    roster = ["alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta", "theta"]
    assert RES.select(3, roster) == RES.select(3, roster)


def test_selection_depends_only_on_batch_and_roster():
    """Outcome-blindness, tested rather than asserted. The rule sees a batch number and row names —
    there is nothing else in its signature for an outcome to enter through."""
    roster = ["alpha", "beta", "gamma", "delta"]
    assert RES.select(3, roster) != RES.select(4, roster) or len(roster) <= 1
    assert RES.select(3, roster) == RES.select(3, list(reversed(roster)))


def test_fraction_is_honoured_and_rounds_up():
    """ceil, so a non-empty batch always contributes frontier. 25% of 8 is 2; of 9 is 3."""
    assert len(RES.select(3, [f"r{i}" for i in range(8)])) == 2
    assert len(RES.select(3, [f"r{i}" for i in range(9)])) == 3
    assert len(RES.select(3, ["only"])) == 1


def test_roster_hash_is_order_independent():
    a = RES.roster_hash(["b", "a", "c"])
    assert a == RES.roster_hash(["a", "b", "c"])


# ── the enforcement ─────────────────────────────────────────────────────────────────────────────────
def test_the_guard_can_actually_fail():
    """Feed the guard a reserved row. If it does not raise, every other test in this file is theatre."""
    reserved = _reserved()
    if not reserved:
        pytest.skip("nothing currently reserved")
    with pytest.raises(RuntimeError, match="FRONTIER LEAK"):
        RES.assert_absent("a deliberately leaking artifact", sorted(reserved), LEDGER)


def test_guard_passes_on_clean_input():
    RES.assert_absent("clean", ["definitely-not-a-reserved-row"], LEDGER)


def test_reserved_rows_have_no_frames_in_any_panel():
    """The strongest form of the reservation: the frames DO NOT EXIST. Reserved rows are declared and
    uncaptured, so blindness is physics rather than a guard anyone must be trusted to respect."""
    reserved = _reserved()
    for p in sorted(LAT.glob("observatory_batch*_panels.json")):
        d = json.loads(p.read_text())
        rows = {r["row"] for r in d["rows"]} | {e["row"] for e in d.get("excluded_at_birth", [])}
        leak = rows & reserved
        assert not leak, f"{p.name} carries frames for reserved row(s) {sorted(leak)}"


def test_reserved_rows_have_no_catalog_cells():
    cat = LAT / "catalog_v1.jsonl"
    if not cat.exists():
        pytest.skip("no catalog")
    reserved = _reserved()
    seen = {json.loads(x)["problem_id"] for x in cat.read_text().splitlines()
            if x.strip() and json.loads(x).get("problem_id")}
    leak = seen & reserved
    assert not leak, f"catalog carries descriptor cells for reserved row(s) {sorted(leak)}"


def test_reserved_rows_are_absent_from_the_database():
    db = LAT / "observatory.db"
    if not db.exists():
        pytest.skip("no db")
    reserved = _reserved()
    con = sqlite3.connect(db)
    try:
        for table in ("frames", "catalog"):
            rows = {r[0] for r in con.execute(f"SELECT DISTINCT problem_id FROM {table}")}
            leak = rows & reserved
            assert not leak, f"db table {table} carries reserved row(s) {sorted(leak)}"
    finally:
        con.close()


def test_reserved_rows_are_visible_as_frontier_not_as_readings():
    """A reserved row must still be KNOWABLE — the power screen needs to count the tranche. What must
    not leak is a reading, not a row id."""
    db = LAT / "observatory.db"
    if not db.exists():
        pytest.skip("no db")
    reserved = _reserved()
    con = sqlite3.connect(db)
    try:
        front = {r[0] for r in con.execute("SELECT problem_id FROM frontier WHERE released = 0")}
    finally:
        con.close()
    assert front == reserved, f"frontier table {sorted(front)} disagrees with the ledger {sorted(reserved)}"


def test_the_batch_defines_no_generator_for_a_reserved_row():
    """The batch cannot burn the ground because it never learned how to build it."""
    import observatory_batch3 as B
    leak = set(B.ROWS) & _reserved()
    assert not leak, f"batch 3 defines generators for reserved row(s) {sorted(leak)}"


def test_declaring_a_different_roster_for_a_declared_batch_is_refused(tmp_path):
    led = tmp_path / "led.jsonl"
    RES.declare(led, 9, ["a", "b", "c", "d"])
    RES.declare(led, 9, ["a", "b", "c", "d"])                 # idempotent: no second record
    assert len(RES.read_ledger(led)) == 1
    with pytest.raises(RuntimeError, match="DIFFERENT roster"):
        RES.declare(led, 9, ["a", "b", "c", "e"])


def test_release_is_an_append_not_an_edit(tmp_path):
    led = tmp_path / "led.jsonl"
    rec = RES.declare(led, 9, ["a", "b", "c", "d"])
    assert RES.reserved_rows(led) == set(rec["reserved"])
    RES.release(led, 9, "wave-1", "test")
    assert RES.reserved_rows(led) == set()
    assert len(RES.read_ledger(led)) == 2
    assert RES.read_ledger(led)[0]["reserved"] == rec["reserved"], "the reservation record was edited"


# ── the near-miss guards (minted 2026-07-27) ────────────────────────────────────────────────────────
def test_a_reserved_row_generator_cannot_exist_in_a_batch_module():
    """Batch 8 DEFINED minimum_fill_in while minimum-fill-in sat on the frontier, kept it out of ROWS,
    and passed every check. The standing rule was stated in every batch docstring and enforced by none."""
    reserved = _reserved()
    if not reserved:
        pytest.skip("nothing reserved")
    victim = sorted(reserved)[0].replace("-", "_")
    with pytest.raises(RuntimeError, match="RESERVED-ROW GENERATOR PRESENT"):
        RES.assert_no_reserved_generators({victim: lambda rng, v: []}, LEDGER)


def test_the_generator_guard_passes_on_a_clean_module():
    RES.assert_no_reserved_generators({"some_other_row": lambda rng, v: []}, LEDGER)


def test_two_generators_computing_the_same_region_halt_the_batch():
    """THE EXPENSIVE HALF. A region is reserved ground regardless of the label above it — every earlier
    guard checked row NAMES and none checked what was computed."""
    import random
    same = lambda rng, v: [("feasible", [(1, 0), (0, 1)])]
    with pytest.raises(RuntimeError, match="DUPLICATE REGION"):
        RES.assert_no_duplicate_regions({"a": same, "b": same}, 0.35, LEDGER,
                                        lambda: random.Random(0))


def test_distinct_generators_pass_the_duplicate_check():
    import random
    RES.assert_no_duplicate_regions(
        {"a": lambda rng, v: [("feasible", [(1, 0), (0, 1)])],
         "b": lambda rng, v: [("feasible", [(1, 1), (0, 0)])]},
        0.35, LEDGER, lambda: random.Random(0))
