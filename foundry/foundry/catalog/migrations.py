"""Migrations — history with a checksum, never a verb.

THE CATEGORY THIS EXISTS FOR. A third of `dev/` is neither a recurring operation nor a report: it is
one-time passes that ran once, under a ruling, and are now history. `void_prereg_v34` is the type
specimen — it asserts specific prereg bytes and voids a specific bet. Making it `foundry void-prereg`
would advertise it as re-runnable, and re-running it is not a no-op, it is a second void of something
already void. The same holds for the four typing adjudications: each was a judgement passed at a moment,
not a procedure anyone should invoke again.

So these get migration semantics rather than verb semantics: NAMED, ORDERED, APPLIED ONCE, and RECORDED
AS APPLIED. What you can do to a migration is see whether it ran. What you cannot do is run it again.

THE MAPTRAIL IS THE APPLIED-LEDGER. Not a second file beside it — the trail already is the append-only
record of what happened to this territory, and "migration 0001 was applied" is exactly that kind of
fact. Replay gives the state, so there is no mutable applied-flag for drift to hide in. This is the db's
no-UPDATE semantics carried up to the migration layer, and it is the same shape as the reservation
ledger's reserve/release.

THE CHECKSUM IS WHAT MAKES IT HISTORY RATHER THAN A CLAIM. Each applied record carries the sha of the
migration's own source. If a migration's definition changes after it was applied, the record on file
describes something that no longer exists, and `verify` says so loudly. A migration is not a place to
fix a mistake: to change what history did, you write the next migration.
"""
from __future__ import annotations

import hashlib
import inspect
from dataclasses import dataclass, field
from pathlib import Path

from . import maptrail as M


@dataclass(frozen=True)
class Migration:
    name: str                    # "0001-census-schema-history" — the leading number IS the order
    why: str
    apply: object                # (paths: dict) -> summary dict
    touches_measured_values: bool = False

    def source_sha(self) -> str:
        return hashlib.sha256(inspect.getsource(self.apply).encode()).hexdigest()[:16]


REGISTRY: list = []


def register(name: str, why: str, touches_measured_values: bool = False):
    def deco(fn):
        if any(m.name == name for m in REGISTRY):
            raise ValueError(f"migration {name!r} is already registered — names are unique and ordered")
        REGISTRY.append(Migration(name, why, fn, touches_measured_values))
        REGISTRY.sort(key=lambda m: m.name)
        return fn
    return deco


def applied(trail: Path) -> dict:
    """name -> the record of its application. Replayed from the trail, never stored."""
    return {r["migration"]: r for r in M.read(trail) if r.get("migration")}


def status(trail: Path) -> list:
    """Every known migration with its state. `drifted` means: applied, but its source has changed since
    — the record on file describes a migration that no longer exists."""
    done = applied(trail)
    out = []
    for m in REGISTRY:
        rec = done.get(m.name)
        state = "pending" if rec is None else (
            "applied" if rec.get("source_sha256") == m.source_sha() else "DRIFTED")
        out.append({"name": m.name, "state": state, "why": m.why,
                    "applied_at": (rec or {}).get("at"), "summary": (rec or {}).get("summary")})
    return out


def assert_no_drift(trail: Path) -> None:
    bad = [s["name"] for s in status(trail) if s["state"] == "DRIFTED"]
    if bad:
        raise RuntimeError(
            f"MIGRATION DRIFT — {bad} were applied, then their source changed. The applied record now "
            f"describes something that does not exist. A migration is history: to change what it did, "
            f"write the next one.")


def run(trail: Path, paths: dict, only: str | None = None, dry_run: bool = False) -> list:
    """Apply pending migrations in name order, once each. Returns what it did.

    Refuses outright if any applied migration has drifted — applying new history on top of a record that
    has stopped being true is how a ledger becomes decorative.
    """
    assert_no_drift(trail)
    done, results = applied(trail), []
    for m in REGISTRY:
        if only and m.name != only:
            continue
        if m.name in done:
            results.append({"name": m.name, "state": "already applied", "at": done[m.name]["at"]})
            continue
        if dry_run:
            results.append({"name": m.name, "state": "would apply"})
            continue
        summary = m.apply(paths)
        M.emit(trail, "annotation", key=f"migration:{m.name}",
               migration=m.name, why=m.why, source_sha256=m.source_sha(),
               summary=summary, touches_no_measured_value=not m.touches_measured_values)
        results.append({"name": m.name, "state": "applied", "summary": summary})
    return results


# ══ 0001 ════════════════════════════════════════════════════════════════════════════════════════════

@register(
    "0001-census-schema-history",
    "Three batch-census shapes shipped under one version string because the string was a literal inside "
    "eight copied files. Retro-label the history; never re-emit the artifacts.",
)
def _census_schema_history(paths: dict) -> dict:
    """Name the three shapes that actually existed, plus the v2 that replaces them.

    RETRO-LABEL, NEVER REWRITE (ruled 2026-07-28). The eight historical censuses are declarations made
    before reading. Re-emitting b3 under b10's shape after b3's readings exist would be editing a
    pre-reading declaration to agree with what came after — the contamination direction, and the fact
    that these files are not in the frozen manifest does not make it less so. Pre-reading declarations
    are epistemically frozen even where they are not mechanically frozen.

    The three historical records carry `reconstructed: true` because they are history written late. The
    v2 record does not: it is being declared now, by the machinery that will emit it.
    """
    from . import batch_census as BC
    trail = paths["trail"]
    law = "F4 — a changed rule is a NEW version, never an in-place edit"
    legacy = BC.LEGACY_SCHEMA
    common = dict(model="observatory batch census, per-batch declaration schema", law=law,
                  authority="retro-label ruling, 2026-07-28",
                  never_rewritten="the historical census bytes stand exactly as written; a pre-reading "
                                  "declaration edited after its readings exist is the contamination "
                                  "direction, mechanically frozen or not")

    M.emit(trail, "version", key="version:batch-census-v1-a", reconstructed=True,
           schema=legacy, shape="v1-a", batches=[3],
           rule="`flagged_for_ruling` holds ONE defect dict keyed by its own 'problem' field; roster "
                "rows carry no capture_mode",
           note="the original shape. Nothing was wrong with it; what was wrong is that the two shapes "
                "after it also called themselves v1.", **common)

    M.emit(trail, "version", key="version:batch-census-v1-b", reconstructed=True,
           schema=legacy, shape="v1-b", batches=[4],
           old_rule="`flagged_for_ruling`: one defect dict, keyed by its own 'problem' field",
           new_rule="`carried_forward`: a mapping of row -> disposition, so more than one row can carry",
           why="batch 4 needed to carry two dispositions forward and one dict could hold one. The widening "
               "was right; the silence was the defect — a renamed key is a schema change and the version "
               "did not move.",
           detected="2026-07-28, by diffing the eight copies of `main` during the CLI design",
           consumers_affected="none — nothing downstream ever read either key, so no measured value is "
                              "wrong. This is provenance drift caught before consumption.", **common)

    M.emit(trail, "version", key="version:batch-census-v1-c", reconstructed=True,
           schema=legacy, shape="v1-c", batches=[5, 6, 7, 8, 9, 10],
           old_rule="roster rows: {family, instantiates_the_family_ramp_as, structural_expectation}",
           new_rule="...plus `capture_mode`, when the contrast-capture path was built at batch 5",
           why="the addition was correct and necessary. It shipped under the same version string as the "
               "shape without it, so a consumer reading the v1 string cannot know whether the field "
               "is absent or the batch is old.",
           consumers_affected="none — the capture_mode that reaches the loader comes from capture "
                              "records, not from the census.", **common)

    M.emit(trail, "version", key="version:batch-census-v2",
           schema=BC.SCHEMA, version="v2.0", shape="v2", batches="11 onward",
           extractor_sha256=hashlib.sha256(
               (Path(inspect.getfile(BC)).read_bytes())).hexdigest()[:16],
           adds="one procedure, per-batch declarations as data, and a version string with exactly one "
                "site in the source tree",
           supersedes=["v1-a", "v1-b", "v1-c"],
           why="F4 could not bind while the version was a literal inside eight copied files: no change "
               "to it was ever a change to anything. The catalog moved v1->v7 under the same law in the "
               "same period because the catalog's version lives in one module.",
           reader="foundry.catalog.batch_census.read tolerates all four shapes and dispatches on "
                  "structure, not on the declared string — which is no evidence, since all three "
                  "historical shapes declare v1", **common)

    return {"version_records": 4, "reconstructed": 3, "contemporaneous": 1,
            "artifacts_rewritten": 0}
