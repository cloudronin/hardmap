"""The archive on the READ surface — `hardmap db build` and `hardmap query`.

THE BUG THIS CLOSES. The queryable database is the product, and a `pip install hardmap` user could not
reach it even in principle: `observatory.db` is derived and therefore not shipped, its only builder was
`foundry db compile`, and `foundry` is repo-only by design. The read/write split correctly stopped
strangers writing and accidentally stopped them reading. Sixty seconds from "heard about it" to "queried
it" is the entire distribution argument, and it did not exist.

BUILDING IS DERIVATION, NOT WRITING. This is why it belongs on the read surface without weakening the
split. `hardmap db build` compiles a *derived* artifact from frozen JSONL that ships in the wheel; it
adds nothing to the archive, reserves nothing, and emits no maptrail event — THE TRAIL RECORDS HISTORY,
NOT COMPILATION. Nothing here can advance the frontier, because nothing here writes anything the archive
counts as a fact.

SAME LOADER, SAME CONTRACT. It calls `foundry.catalog.loader.compile_db`, the identical function
`foundry db compile` calls, so the two builds are byte-identical from the same sources — asserted by a
test rather than assumed. The freshness machinery applies unchanged: the built db records the sha256 of
every source, so a reader can check it against the JSONL rather than trust it.

BYTE-IDENTITY IS SCOPED TO ONE SQLITE BUILD, AND THIS IS NOT A CAVEAT TO BURY. SQLite stamps
SQLITE_VERSION_NUMBER of the writing library into the file header at byte offset 96, so a database
compiled by a different sqlite is logically identical and byte-different. The loader's `PRAGMA
page_size` and closing `VACUUM` make the layout deterministic; they cannot un-stamp the header. CI
caught this by disagreeing with a hash committed from a developer laptop, and CI was right.

WHAT TRAVELS BETWEEN MACHINES is therefore the `sources` map and the `counts` — the hashes of the JSONL,
which is the record, and the logical content compiled from it. Those are what a reader should compare
against ours, what the freshness registry consumes, and what the tests assert across environments.
`db_sha256` is a within-environment fingerprint and is documented as one.

READ-ONLY BY CONSTRUCTION. Queries open the database in SQLite's immutable mode. A `--sql` that tried to
write fails on the connection rather than on our good intentions.
"""
from __future__ import annotations

import json
from pathlib import Path

DEFAULT_DB = Path("observatory.db")


def lattice_dir() -> Path:
    """The frozen JSONL, wherever this is installed from — a checkout or a wheel. Both work, because
    `foundry`'s package_data ships `results/**` and the lattice lives under it."""
    import foundry
    return Path(foundry.__file__).resolve().parent / "results" / "lattice"


def atlas_file() -> Path:
    import eightfold
    return Path(eightfold.__file__).resolve().parent / "results" / "atlas" / "atlas_v3.jsonl"


def build(out: Path = DEFAULT_DB) -> dict:
    """Compile the database. Same sources in, same database out — byte-identical on one sqlite build,
    logically identical across builds (the header carries the writer's version; see the module note)."""
    from foundry.catalog import loader
    lat, atlas = lattice_dir(), atlas_file()
    missing = [str(p) for p in (lat, atlas) if not p.exists()]
    if missing:
        raise RuntimeError(
            f"the frozen artifacts are not present at {missing}. This build needs the JSONL that ships "
            f"with the package; if you are running from a source tree, install it first (`pip install "
            f"-e .`) so the package data resolves.")
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    info = loader.compile_db(lat, atlas, out)
    (out.parent / f"{out.stem}_manifest.json").write_text(json.dumps({
        "schema": "observatory-db/v1",
        "SOURCE_OF_TRUTH": ("the hashed JSONL artifacts. This database is DERIVED — it can always be "
                            "thrown away and rebuilt; the JSONL never can."),
        "regenerated_never_mutated": ("there is no UPDATE path and no migration path. An artifact "
                                      "changing means a rebuild from scratch."),
        **info}, indent=1) + "\n")
    return info


def resolve_db(path: Path | None) -> Path:
    """Find the database, or refuse in the terms the freshness law uses: name the remedy."""
    p = Path(path) if path else DEFAULT_DB
    if p.exists():
        return p
    raise RuntimeError(f"no database at {p}. Build it first:\n\n    hardmap db build\n")


def run_build(out: str | None = None) -> int:
    info = build(Path(out) if out else DEFAULT_DB)
    where = Path(out) if out else DEFAULT_DB
    print("OBSERVATORY DB BUILT\n")
    for t, n in info["counts"].items():
        print(f"  {t:<12}{n:>6}")
    print(f"\n  {where}   sha256 {info['db_sha256'][:16]}   {len(info['sources'])} sources")
    print("\n  The database is DERIVED. The hashed JSONL it was compiled from is the record —")
    print("  delete this file and rebuild it any time. Every table carries its source's sha256.")
    print("\n  Try:  hardmap query --list")
    return 0


def run_query(name: str | None, sql: str | None, list_only: bool, db: str | None,
              limit: int = 40) -> int:
    from foundry.catalog import queries as Q

    if list_only:
        qs = Q.parse()
        print(f"{len(qs)} worked queries — `hardmap query <name>`\n")
        for q in qs:
            print(f"  {q['name']:<24} {q['title']}")
        print(f"\n  Full text, with the SQL and what each join is for:\n  {Q.path()}")
        return 0

    try:
        database = resolve_db(db)
    except RuntimeError as e:
        print(f"\n{e}", file=__import__("sys").stderr)
        return 2

    if sql:
        statement, title = sql, "(freeform)"
    else:
        try:
            q = Q.get(name)
        except KeyError:
            print(f"\nno query named {name!r}. `hardmap query --list` shows them all.\n",
                  file=__import__("sys").stderr)
            return 2
        statement, title = q["sql"], f"{q['id']} — {q['title']}"

    cols, rows = Q.run(database, statement)
    print(f"{title}\n")
    print(Q.tabulate(cols, rows, limit=limit))
    print(f"\n  {len(rows)} row(s)   from {database}")
    return 0
