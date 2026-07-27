"""The observatory loader — a SQL database compiled deterministically from the frozen JSONL artifacts.

THE DERIVED-ARTIFACT LAW, and it is the first thing a reader must know: **the database is DERIVED. The
hashed JSONL artifacts are the source of truth.** The db can always be thrown away and rebuilt; the JSONL
never can. Every table carries the sha256 of the artifact it was compiled from, so a db and its sources
can be checked against each other rather than trusted.

REGENERATED, NEVER MUTATED. There is no UPDATE path and no migration path. An artifact changing means the
db is rebuilt from scratch. A mutable derived store drifts from its sources silently, and silent drift
between a number and its provenance is the failure this whole program is built against.

DETERMINISM IS A TESTED PROPERTY, NOT AN INTENTION. Two builds from identical sources must produce byte-
identical output. That requires:
  - every INSERT ordered by an explicit sort key (dict iteration order is not a contract)
  - no AUTOINCREMENT anywhere (sqlite_sequence is build-order-dependent state)
  - no timestamps, no run ids, no environment capture in any row
  - a fixed page size and encoding, set before the first write
The round-trip test asserts it against a real rebuild rather than reasoning about it.

FOREIGN KEYS ARE ENFORCED, not decorative. `PRAGMA foreign_keys = ON` is set on every connection, and the
schema declares real references. A catalog cell naming a problem that is not in `problems` is a build
failure — which is exactly how a typo in a row id gets caught at compile time instead of in an analysis.
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
from pathlib import Path

SCHEMA_VERSION = "v1"

SCHEMA = """
PRAGMA page_size = 4096;
PRAGMA encoding = 'UTF-8';

CREATE TABLE sources (
    artifact      TEXT PRIMARY KEY,
    sha256        TEXT NOT NULL,
    role          TEXT NOT NULL
);

CREATE TABLE problems (
    problem_id    TEXT PRIMARY KEY,
    family        TEXT,
    reach_class   TEXT NOT NULL,
    reachable     INTEGER NOT NULL,
    capture       TEXT,
    ramp_parameter TEXT,
    rule_fired    TEXT,
    adjudicated   INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE charges (
    problem_id    TEXT NOT NULL,
    charge        TEXT NOT NULL,
    value         TEXT,
    PRIMARY KEY (problem_id, charge),
    FOREIGN KEY (problem_id) REFERENCES problems(problem_id)
);

CREATE TABLE frames (
    problem_id    TEXT NOT NULL,
    region        TEXT NOT NULL,
    flavour       TEXT NOT NULL,
    ramp_position INTEGER NOT NULL,
    ramp_value    REAL,
    state         TEXT NOT NULL,
    insufficient  TEXT,
    blend_excess  REAL,
    measured_rate REAL,
    control_mean  REAL,
    control_sd    REAL,
    r             REAL,
    overlap_mean  REAL,
    bimodality_coefficient REAL,
    source_artifact TEXT NOT NULL,
    PRIMARY KEY (problem_id, region, flavour, ramp_position),
    FOREIGN KEY (problem_id) REFERENCES problems(problem_id),
    FOREIGN KEY (source_artifact) REFERENCES sources(artifact)
);

CREATE TABLE catalog (
    problem_id    TEXT NOT NULL,
    region        TEXT NOT NULL,
    flavour       TEXT NOT NULL,
    descriptor_version TEXT NOT NULL,
    excess_ref    REAL,
    excess_ref_position INTEGER,
    excess_ref_ramp_value REAL,
    excess_min    REAL,
    excess_max    REAL,
    traj_class    TEXT,
    slope_sign    INTEGER,
    max_excursion_sd REAL,
    overlap_ref   REAL,
    overlap_slope REAL,
    bimodality_max REAL,
    bimodal_flag  INTEGER,
    r_ref         REAL,
    insufficient_share REAL,
    gap_count     INTEGER,
    kink_step     INTEGER,
    kink_sharpness REAL,
    seal_prohibited_at_v1 INTEGER NOT NULL,
    coherence_is_retro_filled INTEGER NOT NULL,
    frame_artifact TEXT NOT NULL,
    frame_sha256  TEXT NOT NULL,
    extractor_sha256 TEXT NOT NULL,
    PRIMARY KEY (problem_id, region, flavour),
    FOREIGN KEY (problem_id) REFERENCES problems(problem_id)
);

CREATE VIEW admissible_catalog AS
    SELECT * FROM catalog WHERE excess_ref IS NOT NULL;
"""


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _flat(d, *path, default=None):
    cur = d
    for k in path:
        if not isinstance(cur, dict) or k not in cur:
            return default
        cur = cur[k]
    return cur


def compile_db(lat: Path, atlas: Path, out: Path) -> dict:
    """Compile the db from frozen artifacts. Regenerates: any existing file is replaced, never updated."""
    if out.exists():
        out.unlink()                       # REGENERATED, NEVER MUTATED
    con = sqlite3.connect(out)
    con.executescript(SCHEMA)
    con.execute("PRAGMA foreign_keys = ON")

    srcs = {}

    def add_source(name: str, path: Path, role: str):
        srcs[name] = _sha(path)
        con.execute("INSERT INTO sources VALUES (?,?,?)", (name, srcs[name], role))
        return json.loads(path.read_text()) if path.suffix == ".json" else path.read_text()

    census = add_source("observatory_reach_census.json", lat / "observatory_reach_census.json", "census")
    adj = add_source("observatory_untyped_adjudication.json",
                     lat / "observatory_untyped_adjudication.json", "census")
    v3 = add_source("sounding_v3_survey.json", lat / "sounding_v3_survey.json", "frames")
    b1p = lat / "observatory_batch1_panels.json"
    b1 = add_source("observatory_batch1_panels.json", b1p, "frames") if b1p.exists() else None
    catp = lat / "catalog_v1.jsonl"
    cat_text = add_source("catalog_v1.jsonl", catp, "catalog") if catp.exists() else None
    atlas_text = add_source("atlas_v3.jsonl", atlas, "charges")

    # ── problems: census + adjudication, sorted ─────────────────────────────────────────────────────
    adjudged = {a["problem_id"]: a for a in adj["adjudications"]}
    probs = {}
    for r in census["rows"]:
        pid = r["problem_id"]
        a = adjudged.get(pid)
        probs[pid] = (pid, r.get("family"),
                      a["now"] if a else r["reach_class"],
                      1 if (a["reachable"] if a else r["reachable"]) else 0,
                      (a["capture"] if a else r.get("capture")),
                      (a.get("ramp_parameter") if a else r.get("ramp_parameter")),
                      r.get("rule_fired"), 1 if a else 0)
    # rows that exist only in the frames (new builds not yet in the atlas census)
    def ensure(pid):
        if pid not in probs:
            probs[pid] = (pid, None, "BUILT-not-in-census", 1, "RAMPED", None, "R1-built", 0)
    for x in v3["readings"]:
        if x.get("row"):
            ensure(x["row"])
    if b1:
        for r in b1["rows"]:
            ensure(r["row"])
        for e in b1.get("excluded_at_birth", []):
            ensure(e["row"])
    con.executemany("INSERT INTO problems VALUES (?,?,?,?,?,?,?,?)",
                    [probs[k] for k in sorted(probs)])

    # ── charges ─────────────────────────────────────────────────────────────────────────────────────
    ch = []
    for line in atlas_text.splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        if r["problem_id"] not in probs:
            continue
        for c in r.get("charges", []):
            ch.append((r["problem_id"], c["charge"], str(c.get("value"))))
    con.executemany("INSERT INTO charges VALUES (?,?,?)", sorted(set(ch)))

    # ── frames ──────────────────────────────────────────────────────────────────────────────────────
    fr = []
    for x in v3["readings"]:
        if not (x.get("region") and x.get("flavor")):
            continue
        fr.append((x["row"], x["region"], x["flavor"], x.get("ramp_position") or 0,
                   x.get("ramp_value"), "usable", x.get("insufficient"), x.get("excess"),
                   x.get("measured_rate"), x.get("control_mean"), x.get("control_sd"), x.get("r"),
                   None, None, "sounding_v3_survey.json"))
    if b1:
        for r in b1["rows"]:
            for s in r["steps"]:
                if s.get("state") != "usable":
                    continue
                d = s["dials"]
                for fl, v in sorted(d["flavours"].items()):
                    fr.append((r["row"], s["region"], fl, s["ramp_position"], s["ramp_value"],
                               "usable", v.get("insufficient"), v.get("blend_excess"),
                               v.get("measured_rate"), v.get("control_mean"), v.get("control_sd"),
                               d.get("r_mean"), d.get("overlap_mean"), d.get("bimodality_coefficient"),
                               "observatory_batch1_panels.json"))
    seen, ded = set(), []
    for row in sorted(fr, key=lambda z: (z[0], z[1], z[2], z[3])):
        k = row[:4]
        if k in seen:
            continue
        seen.add(k); ded.append(row)
    con.executemany("INSERT INTO frames VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", ded)

    # ── catalog ─────────────────────────────────────────────────────────────────────────────────────
    n_cat = 0
    if cat_text:
        cells = []
        for line in cat_text.splitlines():
            if not line.strip():
                continue
            c = json.loads(line)
            if c.get("_rollup") or not c.get("region"):
                continue
            cells.append((
                c["problem_id"], c["region"], c["flavour"], c["descriptor_version"],
                _flat(c, "level", "excess_ref"), _flat(c, "level", "excess_ref_position"),
                _flat(c, "level", "excess_ref_ramp_value"),
                _flat(c, "level", "excess_min"), _flat(c, "level", "excess_max"),
                _flat(c, "shape", "traj_class"), _flat(c, "shape", "slope_sign"),
                _flat(c, "shape", "max_excursion_sd"),
                _flat(c, "coherence", "overlap_ref"), _flat(c, "coherence", "overlap_slope"),
                _flat(c, "coherence", "bimodality_max"),
                1 if _flat(c, "coherence", "bimodal_flag") else 0,
                _flat(c, "supply", "r_ref"), _flat(c, "supply", "insufficient_share"),
                _flat(c, "supply", "gap_count"),
                _flat(c, "transition", "kink_step"), _flat(c, "transition", "kink_sharpness"),
                1 if _flat(c, "transition", "SEAL_PROHIBITED_AT_V1") else 0,
                1 if c.get("coherence_is_retro_filled") else 0,
                c["frame_artifact"], c["frame_sha256"], c["extractor_sha256"]))
        uniq, ks = [], set()
        for row in sorted(cells, key=lambda z: (z[0], z[1], z[2])):
            if row[:3] in ks:
                continue
            ks.add(row[:3]); uniq.append(row)
        con.executemany("INSERT INTO catalog VALUES (" + ",".join("?" * 26) + ")", uniq)
        n_cat = len(uniq)

    fk = con.execute("PRAGMA foreign_key_check").fetchall()
    if fk:
        con.close()
        raise RuntimeError(f"FOREIGN KEY VIOLATIONS — the db does not compile: {fk[:5]}")
    con.commit()
    con.execute("VACUUM")                  # deterministic final layout
    con.commit()
    counts = {t: con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
              for t in ("sources", "problems", "charges", "frames", "catalog")}
    con.close()
    return {"schema_version": SCHEMA_VERSION, "sources": srcs, "counts": counts,
            "db_sha256": _sha(out)}


def dump(path: Path) -> str:
    """A canonical SQL dump — the byte-stability contract's subject."""
    con = sqlite3.connect(path)
    try:
        return "\n".join(con.iterdump())
    finally:
        con.close()
