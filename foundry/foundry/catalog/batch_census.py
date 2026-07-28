"""The batch census — ONE procedure, per-batch declarations as data, ONE version string.

WHY THIS MODULE EXISTS, STATED AS THE DEFECT IT CLOSES. Batches 3 through 10 each got their own census
script, copied from the last one and edited. All eight copies of `main` diverged, and two of those
divergences were schema changes that never moved the schema string:

    b3      roster rows {family, ramp, expectation}         flagged_for_ruling   declared v1
    b4      roster rows {family, ramp, expectation}         carried_forward      declared v1   <- key renamed
    b5-b10  roster rows {..., capture_mode}                 carried_forward      declared v1   <- field added

Three shapes, one version string. F4 says a changed rule is a new version, and F4 could not bind here
because there was no single place for it to bind: the version was a literal inside eight files, so no
change to it was ever a change to anything. The catalog moved v1->v7 under the same law in the same
period, because the catalog's version lives in one module. That contrast is the whole argument.

(The prose drifted too, and more visibly: every one of the eight docstrings still says "Batch 3's
census", including batch 10's. Nobody was careless — copy-and-edit simply has no place for a rule to
live.)

WHAT IS PROCEDURE AND WHAT IS DECLARATION. The procedure is identical across every batch and lives here,
once. The roster, the family ramps, and the rationale are genuine per-batch content and live in a
declaration file. The relationship is exact and worth stating, because it is what makes the split
non-arbitrary:

    census = declaration + reservation + status

The declaration is authored before anything is read. The census is what the machinery compiles from it.
Batch generators stay as code, because region builders are code.

THE PAST IS RETRO-LABELLED, NEVER RE-EMITTED (ruled 2026-07-28). The eight historical censuses are
declarations made before reading. Re-emitting b3 under b10's shape after b3's readings exist would be
editing a pre-reading declaration to agree with what came after — the contamination direction, and the
fact that these files are not in the frozen manifest does not make it any less so. PRE-READING
DECLARATIONS ARE EPISTEMICALLY FROZEN EVEN WHERE THEY ARE NOT MECHANICALLY FROZEN. So the historical
bytes stand exactly as written, the three shapes are named in the maptrail as the schema history they
actually are, and `read()` below tolerates all of them.

TRAIL EMISSION IS INSIDE THE PROCEDURE, NOT BESIDE IT. Helm Kill 3: trail records come from the machinery
performing the act. A census that reaches disk without its maptrail record is a build failure, and
`assert_trailed` makes that mechanical rather than remembered. This is the unification's largest quiet
win — event-time emission stops being eight scripts' discipline and becomes one module's property.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from . import maptrail as M
from . import reservation as RES

# ── THE SINGLE SITE. F4 can finally see this move. ──────────────────────────────────────────────────
SCHEMA = "observatory-batch-census/v2"

# The dead string, owned here too. It is a historical citation rather than a rule — but a literal is a
# literal, and the invariant "one module owns this schema's identity" is worth more than the distinction.
# Anything naming the old version (the retro-label migration, chiefly) cites this rather than typing it.
LEGACY_SCHEMA = "observatory-batch-census/v1"

# The shapes that actually existed, named after the fact rather than pretended away. `read()` dispatches
# on structure (not on the declared string, which was v1 for all three and is therefore no evidence).
SCHEMA_HISTORY = {
    "v1-a": "b3. `flagged_for_ruling` holding ONE defect dict keyed by its own 'problem' field; "
            "roster rows carry no capture_mode.",
    "v1-b": "b4. `flagged_for_ruling` renamed to `carried_forward` and widened to a mapping of "
            "row -> disposition; roster rows still carry no capture_mode.",
    "v1-c": "b5-b10. `capture_mode` added to every roster row when the contrast-capture path was built.",
    "v2":   "batch 11 onward. Same content, one procedure, one version string, trail emitted at "
            "event time by the machinery that writes it.",
}

DECLARATION_REQUIRED = ("batch", "why_this_batch", "families", "roster")


# ── typing precedence: ONE SITE, pending the supersession walk ──────────────────────────────────────
# NOT SOLVED HERE, DELIBERATELY. This is the hardcoded two-artifact precedence the eight scripts each
# carried a copy of, and it is the same staleness NEXT.md items 1 and 2 exist to close: the reach census
# is overridden by the untyped adjudication and nothing else is consulted, so the three later typing
# passes are invisible to it. Unifying it does not fix it. What unification buys is that when the
# declared-`supersedes` walk lands there is ONE call site to change instead of eight, and the eight
# cannot drift apart in the meantime.
def resolve_typing(reach_census: dict, untyped_adjudication: dict) -> dict:
    """row -> (current reach_class, census family). Precedence as the batch scripts have always had it."""
    adj = {a["problem_id"]: a for a in untyped_adjudication["adjudications"]}
    out = {}
    for r in reach_census["rows"]:
        a = adj.get(r["problem_id"])
        out[r["problem_id"]] = ((a["now"] if a else r["reach_class"]), r.get("family"))
    return out


def built_rows(lat: Path, before_batch: int | None = None) -> set:
    """Every row that already has frames. A roster re-listing one would double-count it in the catalog.

    `before_batch` asks the historical form of the question — what was built BEFORE batch N — which is
    what re-derivation needs and what a live declaration does not. A census declared at batch N was
    checked against the world as it stood then; checking it against the world now would reject it for
    the rows it went on to build itself. Production passes nothing; verification passes the batch.
    """
    built = set()
    for p in sorted(lat.glob("observatory_batch*_panels.json")):
        n = int("".join(c for c in p.stem.split("batch")[1] if c.isdigit()))
        if before_batch is not None and n >= before_batch:
            continue
        d = json.loads(p.read_text())
        built |= {r["row"] for r in d["rows"]} | {e["row"] for e in d.get("excluded_at_birth", [])}
    built |= {x["row"] for x in
              json.loads((lat / "sounding_v3_survey.json").read_text())["readings"] if x.get("row")}
    return built


def check_roster(roster: dict, typing: dict, built: set) -> list:
    """THE ROSTER IS CHECKED, NOT ASSERTED. Returns the problems; empty means it passes."""
    problems = []
    for row, spec in roster.items():
        fam = spec["family"]
        if row not in typing:
            problems.append(f"{row}: not in the reach census at all")
            continue
        cls, census_fam = typing[row]
        if cls != "REACH-subset":
            problems.append(f"{row}: reach class is {cls}, not REACH-subset")
        if row in built:
            problems.append(f"{row}: ALREADY BUILT — a re-listed row double-counts in the catalog")
        if census_fam != fam:
            problems.append(f"{row}: census family is {census_fam!r}, roster says {fam!r}")
    return problems


def load_declaration(path: Path) -> dict:
    d = json.loads(path.read_text())
    missing = [k for k in DECLARATION_REQUIRED if k not in d]
    if missing:
        raise ValueError(f"{path.name}: declaration is missing {missing}")
    for row, spec in d["roster"].items():
        if "family" not in spec:
            raise ValueError(f"{path.name}: roster row {row!r} declares no family")
        spec.setdefault("structural_expectation", None)
        spec.setdefault("capture_mode", "RAMPED")
        spec.setdefault("instantiates_the_family_ramp_as", None)
    for fam in {s["family"] for s in d["roster"].values()}:
        if fam not in d["families"]:
            raise ValueError(f"{path.name}: roster uses family {fam!r} with no declared ramp")
    d.setdefault("carried_forward", {})
    return d


def declaration_from_census(path: Path) -> dict:
    """Recover the declaration a census was compiled from — `census - reservation - status`.

    This makes the module's central claim executable instead of merely asserted, and it has an ordinary
    working use: batch N+1's declaration legitimately starts life as batch N's, edited. Recovering it
    mechanically beats copying a file, which is precisely the habit that produced three shapes.
    """
    d = read(path)
    return {"batch": d["batch"], "why_this_batch": d["why_this_batch"], "families": d["families"],
            "roster": d["roster"], "carried_forward": d["carried_forward"]}


def declare(declaration: Path, lat: Path, ledger: Path, trail: Path, out: Path | None = None,
            fraction: float = RES.DEFAULT_FRACTION, before_batch: int | None = None) -> tuple:
    """Compile a declaration into a census: check the roster, reserve, EMIT, write. Returns (doc, rec).

    Order is emit-then-write and both are idempotent on their keys, so a run interrupted between them is
    recoverable by re-running rather than by repair. The invariant `assert_trailed` enforces is the one
    that matters: when this returns, the artifact and its trail record both exist.

    One honest limit: this is re-runnable up to the point of capture, not past it. Once a batch's rows
    are built, re-declaring it is correctly rejected — the roster check is doing its job. Re-derivation
    after the fact is a verification, and says so by passing `before_batch`.
    """
    decl = load_declaration(declaration)
    batch, roster = decl["batch"], decl["roster"]
    out = out or (lat / f"observatory_batch{batch}_census.json")

    typing = resolve_typing(
        json.loads((lat / "observatory_reach_census.json").read_text()),
        json.loads((lat / "observatory_untyped_adjudication.json").read_text()))
    problems = check_roster(roster, typing, built_rows(lat, before_batch))
    if problems:
        raise ValueError("ROSTER REJECTED:\n   " + "\n   ".join(problems))

    rec = RES.declare(ledger, batch, list(roster), fraction)
    reserved = set(rec["reserved"])
    published = sorted(r for r in roster if r not in reserved)

    doc = {
        "schema": SCHEMA,
        "STATUS": "DECLARATION — no reading exists for any row here",
        "batch": batch,
        "why_this_batch": decl["why_this_batch"],
        "families": decl["families"],
        "roster": roster,
        "n_roster": len(roster),
        "reservation": {
            "authority": "Helm v1 §5 — a declared fraction of every fan-out batch is reserved",
            "fraction": rec["fraction"], "rule": rec["rule"],
            "roster_sha256": rec["roster_sha256"], "reserved": rec["reserved"],
            "n_reserved": len(rec["reserved"]), "n_published": len(published),
            "declared_at": rec["declared_at"],
            "frames_do_not_exist": (
                "reserved rows are NOT CAPTURED. Helm §0.1 requires predictions hashed before their "
                "frames exist, which is strictly stronger than withholding frames that already exist: "
                "under it, blindness is physics rather than a guard anyone has to be trusted to respect. "
                "§5's 'captured last in the batch' is honoured maximally — last means after the wave's "
                "predictions are sealed."),
        },
        "published": published,
        "carried_forward": decl["carried_forward"],
    }

    # EVENT TIME. The machinery that performs the act emits the record for it — Kill 3, and the reason
    # this lives here rather than in a caller. `annotation` is the right kind by the census's own claim
    # about itself: it touches no measured value, because no reading exists for any row in it.
    M.emit(trail, "annotation", key=f"census:batch-{batch}",
           declares_batch=batch, schema=SCHEMA,
           n_roster=len(roster), n_reserved=len(rec["reserved"]), n_published=len(published),
           roster_sha256=rec["roster_sha256"], reserved=rec["reserved"],
           why=decl["why_this_batch"], touches_no_measured_value=True)

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(doc, indent=1) + "\n")
    return doc, rec


# ── the tolerant reader ─────────────────────────────────────────────────────────────────────────────
# DISPATCH ON STRUCTURE, NOT ON THE DECLARED STRING. All three historical shapes declare v1, so the
# string is no evidence about which one a file is. That is the defect; a reader that trusted it would be
# reproducing the defect in the code meant to survive it.

def shape_of(doc: dict) -> str:
    if doc.get("schema") == SCHEMA:
        return "v2"
    if "flagged_for_ruling" in doc:
        return "v1-a"
    rows = doc.get("roster") or {}
    if any("capture_mode" in s for s in rows.values()):
        return "v1-c"
    return "v1-b"


def read(path: Path) -> dict:
    """Normalise any census, of any shape, to one view. `shape` names which one it was on disk."""
    doc = json.loads(path.read_text())
    shape = shape_of(doc)

    carried = doc.get("carried_forward")
    if carried is None:
        flagged = doc.get("flagged_for_ruling") or {}
        # v1-a held ONE defect as a flat dict keyed by its own 'problem' field.
        carried = {flagged["problem"]: {k: v for k, v in flagged.items() if k != "problem"}} if flagged else {}

    roster = {r: {**s, "capture_mode": s.get("capture_mode", "RAMPED")}
              for r, s in (doc.get("roster") or {}).items()}

    return {"shape": shape, "declared_schema": doc.get("schema"), "batch": doc["batch"],
            "why_this_batch": doc.get("why_this_batch", ""), "families": doc.get("families", {}),
            "roster": roster, "n_roster": doc.get("n_roster", len(roster)),
            "reservation": doc.get("reservation", {}), "published": doc.get("published", []),
            "carried_forward": carried, "path": path}


def read_all(lat: Path) -> list:
    return sorted((read(p) for p in lat.glob("observatory_batch*_census.json")),
                  key=lambda d: d["batch"])


def assert_trailed(lat: Path, trail: Path, since: int) -> None:
    """Every census from `since` forward must have its maptrail record. A write that reached disk
    without one is a build failure, not a lint. `since` exists because the historical censuses predate
    event-time emission and are retro-labelled instead — never back-emitted as if contemporaneous."""
    have = {r.get("declares_batch") for r in M.read(trail) if r.get("declares_batch") is not None}
    missing = sorted(d["batch"] for d in read_all(lat) if d["batch"] >= since and d["batch"] not in have)
    if missing:
        raise RuntimeError(
            f"UNTRAILED CENSUS — batches {missing} are on disk with no maptrail record. A census that "
            f"reaches disk without its trail record is a build failure (Kill 3, event-time emission).")


def sha16(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]
