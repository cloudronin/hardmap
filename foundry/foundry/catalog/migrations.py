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


# ══ 0002 ════════════════════════════════════════════════════════════════════════════════════════════

@register(
    "0002-typing-precedence-backfill",
    "Four typing artifacts on the reach_class axis, and nothing in any of them said which came after "
    "which. Backfill `supersedes` + `written_at`, declared, never inferred.",
)
def _typing_precedence_backfill(paths: dict) -> dict:
    """Give each typing artifact the precedence it always had and never stated.

    THE RULING (2026-07-28): precedence travels IN the artifact, as an explicit `supersedes` field
    written by the pass that supersedes — the only party that authoritatively knows. Nothing downstream
    infers.

    THE APPROACH THAT FAILED, recorded here so it is not retried. An earlier attempt inferred precedence
    from the latest maptrail record MENTIONING each artifact. The reach census is mentioned by later
    errata *about* it, so it scored as newest, overwrote all three adjudications, and invented an
    UNTYPED class for 105 rows — taking staleness from 51 rows to 60. MENTION IS NOT AUTHORSHIP. A
    stale column answers an old question; an inverted one answers a question nobody asked.

    WHY THIS IS RECONSTRUCTION AND SAYS SO. These four passes ran before the field existed, so the order
    is recovered from git authorship dates rather than declared at the time. Every backfilled block
    carries `reconstructed: true`. History written late is fine; history written late and presented as
    contemporaneous is not.

    `written_at` IS THE BACKSTOP, not decoration: a `supersedes` claim pointing at an artifact written
    LATER than the claimant is a contradiction, and the loader treats it as a build failure.
    """
    import json
    lat = paths["lat"]

    # Write order, from `git log --diff-filter=A` / last-modification on each file. The chain is a
    # linked list — each pass names only what it DIRECTLY supersedes, and the loader walks it. Naming
    # every ancestor would be a second, redundant statement of an order the chain already fixes.
    CHAIN = [
        ("observatory_reach_census.json", "2026-07-26T18:44:52-07:00", [], "rows", "reach_class",
         "the base classification: 345 rows typed by rule from the atlas"),
        ("observatory_untyped_adjudication.json", "2026-07-26T18:54:57-07:00",
         ["observatory_reach_census.json"], "adjudications", "now",
         "105 rows the census left UNTYPED, adjudicated"),
        ("reach_subset_readjudication.json", "2026-07-27T11:05:36-07:00",
         ["observatory_untyped_adjudication.json"], "rows", "now",
         "127 REACH-subset rows re-typed against a sealed lexicon over canonical_encoding"),
        ("unmatched_adjudication.json", "2026-07-27T13:28:20-07:00",
         ["reach_subset_readjudication.json"], "rows", "now",
         "the 59 rows the lexicon did not match, hand-adjudicated with receipts"),
    ]

    written = []
    for i, (name, when, supersedes, rowkey, field, what) in enumerate(CHAIN):
        p = lat / name
        d = json.loads(p.read_text())
        d["typing_axis"] = "reach_class"
        d["written_at"] = when
        d["supersedes"] = supersedes
        d["row_typing"] = {"rows_at": rowkey, "class_field": field}
        d["consumed_by_loader"] = True
        d["precedence_backfill"] = {
            "reconstructed": True,
            "declared_by": "migration 0002-typing-precedence-backfill",
            "recovered_from": "git authorship dates; the field did not exist when these passes ran",
            "position": f"{i + 1} of {len(CHAIN)} on the reach_class axis",
            "what_this_pass_did": what,
            "rule": ("the superseding pass declares what it supersedes. Nothing downstream infers "
                     "order — not from filenames, not from mtimes, and not from maptrail mentions."),
            "the_approach_that_failed": (
                "inferring precedence from the latest maptrail record MENTIONING the artifact. The "
                "reach census is mentioned by later errata about it, so it scored newest and overwrote "
                "all three adjudications, inventing an UNTYPED class for 105 rows and taking staleness "
                "from 51 to 60. Mention is not authorship."),
            "backstop": ("`written_at` — a supersedes claim pointing at a later-written artifact is a "
                         "contradiction and the loader fails the build on it"),
        }
        p.write_text(json.dumps(d, indent=1) + "\n")
        written.append(name)

    # A DIFFERENT AXIS, MARKED AS ONE. The region audit's verdicts (SUBSET-VERIFIED / WRONG-REGION /
    # VARIANT-REGION) are region formulations, not reach classes — `unmatched_adjudication` already
    # carries a `coexisting_different_axis` block saying so. It is labelled here so the completeness
    # guard can tell "different axis" from "forgotten", which are the two things that look identical
    # from outside. Consuming it would add a column, and a column is a schema change: owner's call.
    p = lat / "region_formulation_audit.json"
    d = json.loads(p.read_text())
    d["typing_axis"] = "region_formulation"
    d["written_at"] = "2026-07-27T11:10:50-07:00"
    d["supersedes"] = []
    d["consumed_by_loader"] = False
    d["not_consumed_because"] = (
        "COEXISTS, does not supersede. Region formulation is a different axis from reach class, and the "
        "standing rule is one row, one current typing PER AXIS. Loading it would add a "
        "`region_disposition` column to `problems`, and a new column is a schema change under F4 — "
        "which is an owner ruling, not a build decision. Declared here so the guard reads this as a "
        "deliberate abstention rather than an artifact nobody consumed.")
    d["precedence_backfill"] = {
        "reconstructed": True,
        "declared_by": "migration 0002-typing-precedence-backfill",
        "recovered_from": "git authorship dates",
    }
    p.write_text(json.dumps(d, indent=1) + "\n")

    return {"chain_length": len(CHAIN), "backfilled": written + ["region_formulation_audit.json"],
            "axes": ["reach_class", "region_formulation"], "reconstructed": True}
