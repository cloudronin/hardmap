"""The typing chain — tested at the seam where 51 rows once answered a superseded question.

WHAT WENT WRONG. Four passes typed the same rows on the reach_class axis; the loader read the first
two. The database was well-formed, every join worked, and 51 rows carried the PRE-adjudication answer.
Nothing in the artifacts said which came after which, so nothing could have caught it.

THE THREE FAILURES GUARDED HERE.

  1. ORDER BEING INFERRED AGAIN. The ruling is that precedence travels IN the artifact. The failed
     attempt inferred it from maptrail mentions, and since the census is mentioned by later errata
     about it, the census scored newest and overwrote all three adjudications — 105 rows invented into
     an UNTYPED class, staleness 51 -> 60. Mention is not authorship.
  2. AN ARTIFACT PRODUCED AND NEVER CONSUMED. Invisible from outside; the db looks identical.
  3. THE NEGATIVE SPACE — zero rows whose stored class disagrees with the latest typing that names
     them. This is the test that would have failed for a month.
"""
import json
import sqlite3
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from foundry.catalog import typing_chain as TC  # noqa: E402

LAT = ROOT / "foundry" / "results" / "lattice"
DB = LAT / "observatory.db"


# ── the chain is declared, and complete ─────────────────────────────────────────────────────────────

def test_every_typing_artifact_declares_its_precedence():
    """Including the base, whose `supersedes: []` is a claim and not an omission."""
    decls = TC.load_declarations(LAT)
    assert len(decls) == 5
    TC.assert_declared(decls)


def test_the_reach_class_chain_is_the_declared_order():
    chain = [d["name"] for d in TC.chain_for(TC.load_declarations(LAT), "reach_class")]
    assert chain == ["observatory_reach_census.json",
                     "observatory_untyped_adjudication.json",
                     "reach_subset_readjudication.json",
                     "unmatched_adjudication.json"]


def test_written_at_agrees_with_the_declared_chain():
    """THE BACKSTOP. The chain fixes the order; the dates only check it. A pass claiming to supersede
    something written after it is a contradiction, not a tie to break."""
    chain = TC.chain_for(TC.load_declarations(LAT), "reach_class")
    dates = [d["written_at"] for d in chain]
    assert dates == sorted(dates), f"the chain disagrees with the dates: {dates}"


def test_the_region_audit_is_a_different_axis_and_says_so():
    """One row, one current typing PER AXIS. A region formulation and a reach class answer different
    questions, so neither supersedes the other — and the artifact declares which it is rather than
    leaving a reader to infer it from the filename."""
    d = [x for x in TC.load_declarations(LAT) if x["name"] == "region_formulation_audit.json"][0]
    assert d["axis"] == "region_formulation"
    assert d["consumed"] is False and d["not_consumed_because"]
    assert "schema change" in d["not_consumed_because"], \
        "the abstention must name why, or it is indistinguishable from an oversight"


# ── the chain refuses what it cannot order ──────────────────────────────────────────────────────────

def _decl(name, axis="reach_class", when="2026-01-01T00:00:00Z", supersedes=()):
    return {"name": name, "axis": axis, "written_at": when, "supersedes": list(supersedes),
            "consumed": True, "not_consumed_because": None, "row_typing": {"rows_at": "rows",
            "class_field": "now"}, "doc": {"rows": []}}


def test_a_supersedes_claim_pointing_at_a_later_artifact_is_a_build_failure():
    """The motivating backstop case, stated in the directive."""
    decls = [_decl("a.json", when="2026-01-02T00:00:00Z"),
             _decl("b.json", when="2026-01-01T00:00:00Z", supersedes=["a.json"])]
    with pytest.raises(RuntimeError, match="PRECEDENCE CONTRADICTION"):
        TC.chain_for(decls, "reach_class")


def test_a_dangling_supersedes_is_refused():
    decls = [_decl("a.json", supersedes=["ghost.json"])]
    with pytest.raises(RuntimeError, match="DANGLING SUPERSEDES"):
        TC.chain_for(decls, "reach_class")


def test_two_passes_claiming_the_same_predecessor_is_refused():
    """A fork is an ambiguity, not an ordering — and picking one would be the inference the ruling
    removed, reintroduced at a different layer."""
    decls = [_decl("a.json", when="2026-01-01T00:00:00Z"),
             _decl("b.json", when="2026-01-02T00:00:00Z", supersedes=["a.json"]),
             _decl("c.json", when="2026-01-03T00:00:00Z", supersedes=["a.json"])]
    with pytest.raises(RuntimeError, match="FORKED CHAIN"):
        TC.chain_for(decls, "reach_class")


def test_an_artifact_off_the_chain_is_refused():
    """An artifact nothing links to is one whose typing silently does not apply."""
    decls = [_decl("a.json", when="2026-01-01T00:00:00Z"),
             _decl("b.json", when="2026-01-02T00:00:00Z", supersedes=["a.json"]),
             _decl("orphan.json", when="2026-01-03T00:00:00Z", supersedes=[])]
    with pytest.raises(RuntimeError, match="artifacts superseding nothing"):
        TC.chain_for(decls, "reach_class")


def test_an_artifact_missing_its_declaration_is_refused():
    with pytest.raises(RuntimeError, match="UNDECLARED TYPING ARTIFACT"):
        TC.assert_declared([{"name": "x.json", "axis": None, "written_at": None, "supersedes": None}])


# ── the completeness guard ──────────────────────────────────────────────────────────────────────────

def test_a_declared_but_unconsumed_artifact_fails_the_build():
    """The artifact-produced-but-unconsumed species, made structurally impossible."""
    with pytest.raises(RuntimeError, match="TYPING ARTIFACT NOT CONSUMED"):
        TC.assert_complete(LAT, consumed={"observatory_reach_census.json"})


def test_the_loader_actually_consumes_the_whole_chain():
    con = sqlite3.connect(DB)
    consumed = {a for (a,) in con.execute("SELECT artifact FROM sources")}
    for d in TC.load_declarations(LAT):
        if d["consumed"]:
            assert d["name"] in consumed, f"{d['name']} declares consumption but is not a db source"
    TC.assert_complete(LAT, consumed)


# ── THE NEGATIVE SPACE ──────────────────────────────────────────────────────────────────────────────

def test_no_row_carries_a_superseded_typing():
    """THE TEST THAT WOULD HAVE FAILED FOR A MONTH. Zero rows whose stored reach_class disagrees with
    the latest artifact on the chain that names them. Before the walk this stood at 51."""
    resolved = TC.resolve(LAT, "reach_class")
    con = sqlite3.connect(DB)
    stored = dict(con.execute("SELECT problem_id, reach_class FROM problems"))
    stale = {p: (stored[p], v["class"], v["source"])
             for p, v in resolved.items() if p in stored and stored[p] != v["class"]}
    assert not stale, (f"{len(stale)} row(s) carry a superseded typing, e.g. "
                       f"{list(stale.items())[:3]} — run `foundry db compile`")


def test_the_walk_actually_moved_rows():
    """The complement, so a resolver that silently returned nothing could not pass the test above.
    The two later passes must be visibly governing rows in the database."""
    resolved = TC.resolve(LAT, "reach_class")
    late = {p: v for p, v in resolved.items()
            if v["source"] in ("reach_subset_readjudication.json", "unmatched_adjudication.json")}
    assert len(late) == 127, f"expected 127 rows typed by the two late passes, got {len(late)}"
    con = sqlite3.connect(DB)
    stored = dict(con.execute("SELECT problem_id, reach_class FROM problems"))
    assert all(stored[p] == v["class"] for p, v in late.items() if p in stored)


def test_the_correction_narrowed_reach_subset_and_only_reach_subset():
    """THE DIRECTION OF THE CORRECTION, and the reason item 4 must re-run.

    Compared against WHAT THE OLD LOADER PRODUCED — census overridden by the untyped adjudication, the
    two links it actually read — the walk moves exactly 51 rows and every one is REACH-subset being
    narrowed to something more specific. So any supply count taken off the old column was an OVERCOUNT,
    not merely a different count.

    The comparison is against the old loader's resolution and not against the base census, because the
    base census conflates two different moves: rows that were UNTYPED and got typed at link 2 (correct
    and uninteresting) and rows that were REACH-subset and got narrowed at links 3-4 (the defect). An
    earlier version of this test compared against the base and failed on the first kind.
    """
    census = json.loads((LAT / "observatory_reach_census.json").read_text())["rows"]
    adj = {a["problem_id"]: a["now"] for a in
           json.loads((LAT / "observatory_untyped_adjudication.json").read_text())["adjudications"]}
    old = {r["problem_id"]: adj.get(r["problem_id"], r["reach_class"]) for r in census}

    resolved = TC.resolve(LAT, "reach_class")
    moved = [(p, old[p], v["class"]) for p, v in resolved.items()
             if p in old and old[p] != v["class"]]
    assert len(moved) == 51, f"expected the 51 rows NEXT.md recorded, got {len(moved)}"
    offenders = [m for m in moved if m[1] != "REACH-subset"]
    assert not offenders, f"a late pass moved something that was not REACH-subset: {offenders[:3]}"
