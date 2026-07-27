"""The loader's contracts, tested rather than intended.

THE DB IS DERIVED. The hashed JSONL artifacts are the source of truth. These tests protect the three
properties that make a derived store trustworthy: it compiles deterministically, it enforces its own
foreign keys, and it is regenerated rather than mutated.
"""
import sqlite3
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from foundry.catalog import loader  # noqa: E402

LAT = ROOT / "foundry" / "results" / "lattice"
ATLAS = ROOT.parent / "eightfold" / "eightfold" / "results" / "atlas" / "atlas_v3.jsonl"
DB = LAT / "observatory.db"


def test_round_trip_is_byte_stable():
    """TWO BUILDS FROM IDENTICAL SOURCES MUST PRODUCE BYTE-IDENTICAL OUTPUT.

    Asserted against a real rebuild, not reasoned about. Determinism that is merely intended breaks the
    first time a dict iteration order shifts or an AUTOINCREMENT counter carries build state."""
    a, b = LAT / "_test_rt_a.db", LAT / "_test_rt_b.db"
    try:
        ia = loader.compile_db(LAT, ATLAS, a)
        ib = loader.compile_db(LAT, ATLAS, b)
        assert ia["db_sha256"] == ib["db_sha256"], "the raw db file is not byte-stable across rebuilds"
        assert loader.dump(a) == loader.dump(b), "the SQL dump is not stable across rebuilds"
    finally:
        for p in (a, b):
            if p.exists():
                p.unlink()


def test_compile_replaces_rather_than_mutates():
    """REGENERATED, NEVER MUTATED. A stale row left behind by a rebuild is silent drift between a number
    and its provenance — so compiling over an existing file must not preserve anything from it."""
    p = LAT / "_test_regen.db"
    try:
        loader.compile_db(LAT, ATLAS, p)
        con = sqlite3.connect(p)
        con.execute("INSERT INTO problems VALUES ('__ghost__',NULL,'FAKE',0,NULL,NULL,NULL,0)")
        con.commit(); con.close()
        loader.compile_db(LAT, ATLAS, p)
        con = sqlite3.connect(p)
        n = con.execute("SELECT COUNT(*) FROM problems WHERE problem_id='__ghost__'").fetchone()[0]
        con.close()
        assert n == 0, "a rebuild preserved a row from the previous db — it mutated instead of regenerating"
    finally:
        if p.exists():
            p.unlink()


def test_foreign_keys_are_enforced_not_decorative():
    """A schema declaring references that the engine does not check is documentation, not a constraint."""
    if not DB.exists():
        pytest.skip("observatory.db not built")
    con = sqlite3.connect(DB)
    try:
        con.execute("PRAGMA foreign_keys = ON")
        # THE ARITY IS READ OFF THE SCHEMA, not counted by hand. A hardcoded column count turns every
        # future descriptor addition into a spurious failure in a test that is not about arity — which
        # is how a real constraint check gets weakened to make an unrelated edit pass.
        ncols = len(con.execute("PRAGMA table_info(catalog)").fetchall())
        head = "'__nope__','feasible','min','v1'"           # 4 key columns
        tail = "0,0,0,0,'x','y','z'"                        # 4 NOT NULL flags + 3 provenance columns
        with pytest.raises(sqlite3.IntegrityError):
            con.execute(f"INSERT INTO catalog VALUES ({head},"
                        + ",".join(["NULL"] * (ncols - 11)) + f",{tail})")
        assert con.execute("PRAGMA foreign_key_check").fetchall() == []
    finally:
        con.rollback(); con.close()


def test_every_catalog_cell_names_a_real_problem():
    if not DB.exists():
        pytest.skip("observatory.db not built")
    con = sqlite3.connect(DB)
    try:
        orphans = con.execute(
            "SELECT c.problem_id FROM catalog c LEFT JOIN problems p USING(problem_id) "
            "WHERE p.problem_id IS NULL").fetchall()
        assert not orphans, f"catalog cells with no problem row: {orphans[:5]}"
    finally:
        con.close()


def test_seal_prohibition_survives_the_compile():
    """The transition group's no-seal flag must reach the db. A caveat lost in compilation is a caveat
    that stops existing exactly where people start querying."""
    if not DB.exists():
        pytest.skip("observatory.db not built")
    con = sqlite3.connect(DB)
    try:
        n_total, n_flagged = con.execute(
            "SELECT COUNT(*), SUM(seal_prohibited_at_v1) FROM catalog").fetchone()
        assert n_total > 0 and n_flagged == n_total, "not every catalog cell carries the v1 seal prohibition"
    finally:
        con.close()


def test_sources_table_records_every_input_hash():
    if not DB.exists():
        pytest.skip("observatory.db not built")
    con = sqlite3.connect(DB)
    try:
        rows = con.execute("SELECT artifact, sha256 FROM sources").fetchall()
        assert rows, "no sources recorded"
        for art, h in rows:
            assert len(h) == 64, f"{art} has a malformed sha256"
    finally:
        con.close()


def test_ambient_confounded_shape_columns_are_null_in_sql():
    """THE MARKER MUST NOT REACH SQL AS A VALUE. The JSONL keeps `n.a.-ambient-confounded` so a reader
    learns why the cell is empty; the column must be NULL so every `IS NOT NULL` filter excludes it
    without knowing the marker exists. A sentinel that reaches a column becomes a data value — and would
    show up in Helm's association candidates as a traj_class level."""
    if not DB.exists():
        pytest.skip("observatory.db not built")
    con = sqlite3.connect(DB)
    try:
        n = con.execute("SELECT COUNT(*) FROM catalog WHERE ambient_confounded = 1").fetchone()[0]
        if not n:
            pytest.skip("no confounded rows in this build")
        bad = con.execute(
            "SELECT COUNT(*) FROM catalog WHERE ambient_confounded = 1 AND ("
            "traj_class IS NOT NULL OR slope_sign IS NOT NULL OR max_excursion_sd IS NOT NULL "
            "OR kink_step IS NOT NULL OR overlap_slope IS NOT NULL)").fetchone()[0]
        assert bad == 0, f"{bad} confounded cell(s) leaked a shape/transition value into SQL"
        levels = con.execute(
            "SELECT COUNT(*) FROM catalog WHERE ambient_confounded = 1 "
            "AND excess_ref IS NOT NULL").fetchone()[0]
        assert levels > 0, "level descriptors must survive the confound, not be voided with the rest"
    finally:
        con.close()


def test_no_marker_string_survives_anywhere_in_the_catalog_table():
    if not DB.exists():
        pytest.skip("observatory.db not built")
    con = sqlite3.connect(DB)
    try:
        cols = [r[1] for r in con.execute("PRAGMA table_info(catalog)")]
        text_cols = [c for c in cols if c not in ("problem_id", "region", "flavour")]
        for c in text_cols:
            n = con.execute(f"SELECT COUNT(*) FROM catalog WHERE CAST({c} AS TEXT) LIKE 'n.a.%'").fetchone()[0]
            assert n == 0, f"column {c} carries {n} 'n.a.' marker string(s) as a value"
    finally:
        con.close()
