"""Freshness — a consumer older than its producers refuses to run.

THE MOTIVATING CASE is `wave run` against a stale db: the sweep enumerates candidates over the rows the
db knows about, so a db compiled before the newest census produces a slate over a world that no longer
exists — and produces it silently, with every number internally consistent. Nothing is wrong except
that the question was asked of last week's territory.

THE RULE IS ONE CHECK IN THE LIBRARY, NOT PER-VERB VIGILANCE. Staleness is not a species of bug to be
caught case by case; it is a STATE THE PIPELINE SHOULD NOT BE ABLE TO OCCUPY. So every compiled artifact
records the hashes of what it was compiled from, and every consumer compares that record against the
sources as they stand now. A verb inherits the check by naming what it consumes.

WHY HASHES AND NOT MTIMES. Mtimes move when nothing changed (a checkout, a copy, a sync) and stand still
when something did (a restore). This repository lives in a cloud-synced directory, so mtime is actively
misleading here. A hash answers the question actually being asked: is the byte-content this was compiled
from still the byte-content on disk?

THE DETERMINISM SPLIT THIS RESPECTS (ratified 2026-07-28). COMPILED artifacts — the db, the catalog,
NEXT.md — must regenerate byte-identically, so they carry no timestamps, no run ids, no commit ids.
Source hashes are safe to embed in them precisely because a hash is a pure function of its source: it
moves only when the source moves. APPEND-ONLY LOGS — the maptrail, the reservation ledger — legitimately
stamp `at`, because a log's whole subject is when things happened. The blanket rule "everything
regenerates byte-identically" would be false, and the natural place to notice that is here.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def current(names, resolve) -> dict:
    """The sources as they stand now. A named source that has vanished maps to None rather than raising —
    disappearance is a kind of staleness and the caller should hear about it in those terms.

    `resolve` maps a source NAME to a path, because not every source lives in the lattice directory: the
    charge atlas is an eightfold artifact and the db consumes it across the package boundary.
    """
    out = {}
    for n in names:
        p = resolve(n)
        out[n] = sha(p) if p is not None and p.exists() else None
    return out


def compare(recorded: dict, now: dict) -> dict:
    """What changed between compile time and now, in the three ways it can."""
    return {
        "changed": sorted(n for n, h in recorded.items()
                          if n in now and now[n] is not None and now[n] != h),
        "vanished": sorted(n for n, h in recorded.items() if now.get(n) is None),
        "new": sorted(n for n in now if n not in recorded and now[n] is not None),
    }


def is_stale(recorded: dict, now: dict) -> bool:
    d = compare(recorded, now)
    return bool(d["changed"] or d["vanished"] or d["new"])


def describe(label: str, d: dict) -> str:
    bits = []
    if d["changed"]:
        bits.append(f"{len(d['changed'])} source(s) changed since it was compiled: {d['changed'][:6]}")
    if d["vanished"]:
        bits.append(f"{len(d['vanished'])} source(s) no longer exist: {d['vanished'][:6]}")
    if d["new"]:
        bits.append(f"{len(d['new'])} source(s) appeared that it never saw: {d['new'][:6]}")
    return f"{label} is STALE — " + "; ".join(bits)


def assert_fresh(label: str, recorded: dict, now: dict, rebuild: str) -> None:
    """Refuse, and say what to run. A staleness error that does not name its own remedy just moves the
    reconstruction cost from the pipeline to the person reading the traceback."""
    d = compare(recorded, now)
    if d["changed"] or d["vanished"] or d["new"]:
        raise RuntimeError(describe(label, d) + f".\n  Rebuild it with:  {rebuild}")


# ── the registry of compiled artifacts ──────────────────────────────────────────────────────────────
# A verb declares WHAT IT CONSUMES; the check comes for free. Adding a compiled artifact is one entry,
# which is the property that keeps this from decaying back into per-verb vigilance.

def repo_root(lat: Path) -> Path:
    """`lat` is <repo>/foundry/foundry/results/lattice. Resolve first — this arithmetic is meaningless
    on a relative path, and a source that silently fails to resolve reads as `vanished`, which is a
    staleness verdict handed down on the strength of a path bug."""
    return lat.resolve().parent.parent.parent.parent


def atlas_path(lat: Path) -> Path:
    """The charge atlas is an eightfold artifact; the db consumes it across the package boundary."""
    return repo_root(lat) / "eightfold" / "eightfold" / "results" / "atlas" / "atlas_v3.jsonl"


def _resolver(lat: Path):
    def resolve(name: str):
        if name == "atlas_v3.jsonl":
            return atlas_path(lat)
        return lat / name
    return resolve


def _db_recorded(lat: Path) -> dict:
    p = lat / "observatory_db_manifest.json"
    return json.loads(p.read_text()).get("sources", {}) if p.exists() else {}


def _next_recorded(lat: Path) -> dict:
    """NEXT.md records its sources in an html comment. It did NOT before this: the page said in prose
    that it was a pure function of its sources and left a reader no way to check the claim."""
    p = next_path(lat)
    if not p.exists():
        return {}
    text = p.read_text()
    if SOURCES_MARKER not in text:
        return {}
    return json.loads(text.split(SOURCES_MARKER, 1)[1].split("-->", 1)[0].strip())


SOURCES_MARKER = "<!-- sources:"


def next_path(lat: Path) -> Path:
    return repo_root(lat) / "NEXT.md"


# DISCOVERY IS WHAT CATCHES A SOURCE THE ARTIFACT NEVER SAW. Comparing only the recorded names can
# detect a source that MOVED or VANISHED, never one that APPEARED — and "batch 11 was censused and the
# db does not know" is the motivating case, not an edge case. So each artifact declares the shape of
# its source set, and `test_freshness` asserts those globs actually cover what the compiler records.
REGISTRY = {
    "observatory.db": {
        "recorded": _db_recorded,
        "globs": ("observatory_batch*_panels.json", "helm_wave*_candidates.jsonl"),
        # A VERSIONED SINGLETON, not a glob: the loader consumes only the NEWEST catalog, selected by
        # parsed integer rather than lexicographically (which is why v10 will not sort under v9).
        # Globbing all of them would report the six superseded catalogs as sources the db never saw,
        # which is a staleness verdict on artifacts that are correctly ignored.
        "newest": ("catalog_v*.jsonl",),
        "singletons": ("observatory_reach_census.json", "observatory_untyped_adjudication.json",
                       "sounding_v3_survey.json", "maptrail.jsonl", "observatory_reservation.jsonl",
                       "wave_trail.jsonl", "atlas_v3.jsonl"),
        "rebuild": "foundry db compile",
        "why": "the sweep enumerates over the rows the db knows about; a stale db slates a world that "
               "no longer exists, silently and self-consistently",
    },
    "NEXT.md": {
        "recorded": _next_recorded,
        "globs": (),
        "singletons": ("maptrail.jsonl", "observatory_reservation.jsonl", "observatory.db"),
        "rebuild": "foundry next",
        "why": "a derived front page that lags its trail tells a stranger the wrong thing is open",
    },
}


def _version_of(name: str) -> int:
    digits = "".join(c for c in name if c.isdigit())
    return int(digits) if digits else -1


def discover(artifact: str, lat: Path) -> set:
    """The source set as it stands now, by the artifact's own declared shape."""
    spec = REGISTRY[artifact]
    found = {p.name for g in spec["globs"] for p in lat.glob(g)}
    for g in spec.get("newest", ()):
        matches = sorted(lat.glob(g), key=lambda p: _version_of(p.stem))
        if matches:
            found.add(matches[-1].name)
    resolve = _resolver(lat)
    return found | {n for n in spec["singletons"] if resolve(n).exists()}


def check(artifact: str, lat: Path) -> dict:
    """State of one compiled artifact: its recorded sources vs the world now."""
    spec = REGISTRY[artifact]
    recorded = spec["recorded"](lat)
    resolve = _resolver(lat)
    names = set(recorded) | discover(artifact, lat)
    now = current(names, resolve) if recorded else {}
    return {"artifact": artifact, "recorded": recorded, "now": now,
            "n_sources": len(recorded), "stale": bool(recorded) and is_stale(recorded, now),
            "unknown": not recorded, "diff": compare(recorded, now) if recorded else {},
            "rebuild": spec["rebuild"]}


def require(artifact: str, lat: Path) -> None:
    """The inherited check. A verb consuming a compiled artifact calls this and nothing else."""
    st = check(artifact, lat)
    if st["unknown"]:
        raise RuntimeError(
            f"{artifact} records no sources, so its freshness cannot be established. An artifact that "
            f"cannot be checked is not fresh by default — rebuild it with: {st['rebuild']}")
    assert_fresh(artifact, st["recorded"], st["now"], st["rebuild"])
