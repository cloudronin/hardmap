"""The archive on the read surface — tested where it could stop being reachable, or stop being derived.

THE BUG THIS WHOLE SURFACE CLOSES. The queryable database is the product and a `pip install hardmap`
user could not reach it even in principle: it is derived and therefore unshipped, its only builder lived
behind a repo-only binary. The read/write split correctly stopped strangers writing and accidentally
stopped them reading.

THE FAILURES GUARDED HERE.

  1. THE TWO BUILDERS DIVERGING. `hardmap db build` and `foundry db compile` must produce the same
     bytes from the same sources, or the read surface is showing readers a different archive.
  2. BUILDING BECOMING WRITING. Building is derivation: it must touch nothing in the archive, reserve
     nothing, and emit no trail event. The moment it writes, the split it was designed not to weaken is
     weakened.
  3. THE REFUSAL LOSING ITS REMEDY. A reader with no database must be told the one command that fixes
     it, in the terms the freshness law already uses everywhere else.
"""
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent.parent
for p in ("hardmap", "eightfold", "foundry", "desert-map", "proof-census"):
    sys.path.insert(0, str(ROOT / p))

from foundry.catalog import queries as Q     # noqa: E402
from hardmap import archive                  # noqa: E402

LAT = ROOT / "foundry" / "foundry" / "results" / "lattice"


def test_the_frozen_artifacts_resolve_from_the_installed_package():
    """The build reads package data. If this resolves to nothing, a wheel user gets an empty archive."""
    assert archive.lattice_dir().exists(), archive.lattice_dir()
    assert archive.atlas_file().exists(), archive.atlas_file()


def test_both_builders_produce_byte_identical_databases(tmp_path):
    """`hardmap db build` and `foundry db compile` call the same loader on the same sources, so within
    one environment they must produce identical bytes. If they diverge, the read surface is quietly
    serving a different archive than the one operators see.

    BOTH SIDES ARE BUILT HERE, DELIBERATELY. The first version of this test compared a fresh build
    against the `db_sha256` committed in the manifest, which is not the same claim: it asserts that
    THIS machine's sqlite matches the machine that last ran `foundry db compile`. CI failed on it, and
    CI was right — see `test_the_db_header_stamps_the_writing_sqlite_version` for why.
    """
    from foundry.catalog import loader
    mine, theirs = tmp_path / "reader.db", tmp_path / "operator.db"
    a = archive.build(mine)
    b = loader.compile_db(archive.lattice_dir(), archive.atlas_file(), theirs)
    assert a["db_sha256"] == b["db_sha256"], "the two builders disagree"
    assert mine.read_bytes() == theirs.read_bytes()


def test_the_db_header_stamps_the_writing_sqlite_version(tmp_path):
    """WHY `db_sha256` IS NOT PORTABLE, pinned as an executable fact rather than left as a mystery.

    SQLite writes SQLITE_VERSION_NUMBER of the library that last modified the file into the header at
    byte offset 96. So two logically identical databases built by different sqlite builds differ in
    their bytes and therefore in their hash, and no amount of `PRAGMA page_size` or a final `VACUUM`
    changes that. The loader's determinism guarantee is real and is scoped to one environment.

    A future reader who sees a cross-machine hash mismatch should land here instead of hunting a
    nondeterminism that is not there.
    """
    import sqlite3
    import struct
    db = tmp_path / "x.db"
    archive.build(db)
    stamped = struct.unpack(">I", db.read_bytes()[96:100])[0]
    running = sqlite3.sqlite_version_info
    assert stamped == running[0] * 1_000_000 + running[1] * 1_000 + running[2], \
        "the header no longer records the writing library's version — re-derive what is portable"


def test_the_portable_content_matches_the_committed_manifest(tmp_path):
    """What DOES travel between machines: the source hashes and the row counts. The sources are hashes
    of the JSONL, which is the record; the counts are the logical content. Those are the fields a
    reader can check against ours, and the ones the freshness registry actually consumes."""
    info = archive.build(tmp_path / "x.db")
    canonical = json.loads((LAT / "observatory_db_manifest.json").read_text())
    assert info["sources"] == canonical["sources"], "the reader compiled from different artifacts"
    assert info["counts"] == canonical["counts"], "the reader's archive has different content"


def test_the_build_is_deterministic(tmp_path):
    a, b = tmp_path / "a.db", tmp_path / "b.db"
    assert archive.build(a)["db_sha256"] == archive.build(b)["db_sha256"]
    assert a.read_bytes() == b.read_bytes()


def test_building_touches_nothing_in_the_archive(tmp_path):
    """BUILDING IS DERIVATION, NOT WRITING — which is the entire reason this belongs on the read
    surface. It must not append to the trail, the ledger, or any artifact."""
    watched = {p: p.read_bytes() for p in LAT.iterdir() if p.suffix in (".jsonl", ".json")}
    archive.build(tmp_path / "x.db")
    changed = sorted(p.name for p, b in watched.items() if p.read_bytes() != b)
    assert not changed, f"the build wrote into the archive: {changed}"


def test_the_build_emits_no_maptrail_event(tmp_path):
    """The trail records HISTORY, not compilation. A derived artifact rebuilt on a reader's laptop is
    not an event in the territory's biography."""
    trail = LAT / "maptrail.jsonl"
    before = len(trail.read_text().splitlines())
    archive.build(tmp_path / "x.db")
    assert len(trail.read_text().splitlines()) == before


def test_a_missing_database_refuses_and_names_the_remedy(tmp_path):
    with pytest.raises(RuntimeError, match="hardmap db build"):
        archive.resolve_db(tmp_path / "nope.db")


def test_queries_are_read_only(tmp_path):
    """Opened immutable, so a `--sql` that tried to write fails on the connection rather than on our
    good intentions."""
    db = tmp_path / "x.db"
    archive.build(db)
    with pytest.raises(Exception):
        Q.run(db, "CREATE TABLE evil (x INT)")


# ── the queries file is one home, parsed by the CLI and rendered as documentation ───────────────────

def test_every_named_query_parses_and_executes(tmp_path):
    db = tmp_path / "x.db"
    archive.build(db)
    qs = Q.parse()
    assert len(qs) >= 8
    for q in qs:
        cols, rows = Q.run(db, q["sql"])
        assert cols, f"{q['name']} returned no columns"


def test_the_queries_file_ships_in_the_wheel():
    """Under foundry/docs/ it was excluded from the distribution, so a pip user could not have run a
    named query even once the runner existed — the same shape as the bug this unit exists to fix."""
    assert Q.path().exists()
    assert "queries" in Q.path().parts, "QUERIES.md must live inside the package to be shipped"
    setup_py = (ROOT / "setup.py").read_text()
    assert "queries/*.md" in setup_py, "the wheel no longer ships QUERIES.md"


def test_query_names_are_unique_and_slugged():
    names = [q["name"] for q in Q.parse()]
    assert len(names) == len(set(names))
    assert all(n.islower() and " " not in n for n in names)


def test_the_readme_quickstart_query_exists():
    """The README's sixty-second path names a query. If it is renamed, the front door breaks."""
    assert any(q["name"] == "rejected-candidates" for q in Q.parse())


def test_the_cli_exposes_db_and_query():
    from hardmap.cli import build_parser
    actions = [a for a in build_parser()._actions if hasattr(a, "choices") and a.choices]
    verbs = {v for a in actions for v in (a.choices or {})}
    assert {"db", "query"} <= verbs


def test_the_read_surface_still_has_no_write_verb():
    """Adding the archive must not have smuggled a writer onto the published binary."""
    from hardmap.cli import build_parser
    actions = [a for a in build_parser()._actions if hasattr(a, "choices") and a.choices]
    verbs = {v for a in actions for v in (a.choices or {})}
    forbidden = {"wave", "census", "migrate", "next", "agents", "frontier", "catalog", "mint-prereg"}
    assert not (verbs & forbidden), f"a write verb reached the read surface: {sorted(verbs & forbidden)}"
