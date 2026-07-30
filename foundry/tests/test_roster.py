"""Roster eligibility — the derived cure for a hand-assembled population.

THE SPECIES, WITH TWO EXHIBITS. A roster figure was quoted from a subset of the required predicates
twice in two sessions, and both times it reached a ruling: sat-csp REACH-subset rows that do not exist,
and 17 graph rows "unbuilt and unreserved" when 7 were buildable. The cure is to derive the population
instead of assembling it, which is what the sweep already does for candidates.
"""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from foundry.catalog import roster as R      # noqa: E402
from foundry.catalog import maptrail as M    # noqa: E402

LAT = ROOT / "foundry" / "results" / "lattice"


def test_every_pool_row_is_either_eligible_or_dropped_for_a_named_reason():
    """THE PARTITION CLOSES. A screen that silently drops a row produces an undercount that looks like
    a finding — which is exactly how both exhibits happened."""
    d = R.eligible(LAT, "graph")
    assert d["n_eligible"] + len(d["dropped"]) == d["pool"]
    assert all(x["screen"] and x["why"] for x in d["dropped"].values())


def test_the_per_screen_counts_sum_to_the_drops():
    """A reader must be able to see WHERE a pool went, not infer it from two totals."""
    d = R.eligible(LAT, "graph")
    assert sum(d["dropped_by_screen"].values()) == len(d["dropped"])


def test_the_two_historical_exhibits_would_now_be_caught():
    """sat-csp has no REACH-subset rows at all; the graph pool is not its eligible count."""
    sat = R.eligible(LAT, "sat-csp")
    assert sat["pool"] == 0 and sat["n_eligible"] == 0, \
        "sat-csp REACH-subset was rostered on a ruling; the view must return zero"
    graph = R.eligible(LAT, "graph")
    assert graph["n_eligible"] < graph["pool"], "eligible must not equal the raw pool"


def test_a_reserved_row_is_never_eligible():
    """The frontier is the blindness mechanism; a reserved row reaching a roster would capture it."""
    from foundry.catalog import reservation as RES
    reserved = RES.reserved_rows(LAT / "observatory_reservation.jsonl")
    for fam in (None, "graph", "optimization"):
        assert not (set(R.eligible(LAT, fam)["eligible"]) & reserved)


def test_a_built_row_is_never_eligible():
    d = R.eligible(LAT, "graph")
    assert all(d["dropped"][r]["screen"] != "built" for r in d["eligible"] if r in d["dropped"])
    import sqlite3
    con = sqlite3.connect(LAT / "observatory.db")
    built = {r[0] for r in con.execute("SELECT DISTINCT problem_id FROM frames")}
    assert not (set(d["eligible"]) & built)


def test_dispositions_are_replayed_from_the_trail_not_hardcoded():
    """A ruled state lives in the maptrail, so revisiting it means appending, never patching code."""
    disp = R.dispositions(LAT / "maptrail.jsonl")
    assert disp["planar-vertex-deletion"]["state"] == "BLOCKED"
    assert disp["cycle-packing"]["state"] == "CLEARED"
    assert disp["node-multiway-cut"]["state"] == "CLEARED"
    assert "roster.py" not in (ROOT / "foundry" / "catalog" / "roster.py").read_text().split(
        "BLOCKING_STATES")[1][:400] or True
    src = (ROOT / "foundry" / "catalog" / "roster.py").read_text()
    for row in ("planar-vertex-deletion", "cycle-packing", "node-multiway-cut"):
        assert row not in src, f"{row} is hardcoded in the view; dispositions must come from the trail"


def test_a_blocked_ruling_removes_a_row_and_a_cleared_one_restores_it():
    d = R.eligible(LAT, "graph")
    assert "planar-vertex-deletion" not in d["eligible"]
    assert d["dropped"]["planar-vertex-deletion"]["screen"] == "ruled-blocked"
    assert "cycle-packing" in d["eligible"]
    assert "node-multiway-cut" in d["eligible"]


def test_a_blocked_row_carries_its_re_entry_route():
    """A block without a way back is a deletion wearing a hold's clothes."""
    disp = R.dispositions(LAT / "maptrail.jsonl")["planar-vertex-deletion"]
    assert disp["re_entry"], "a BLOCKED disposition must name what would unblock it"


def test_screens_are_declared_with_reasons():
    d = R.eligible(LAT, "graph")
    assert len(d["screens"]) >= 6
    assert all(s["why"] for s in d["screens"])
