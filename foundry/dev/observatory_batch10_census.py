#!/usr/bin/env python3
"""Batch 3's census — the roster and its frontier reservation, declared and hashed BEFORE capture.

THIS IS THE FIRST BATCH WITH A FRONTIER. Helm §5 reserves a declared fraction of every fan-out batch as
standing out-of-sample ground. The reservation has to be fixed before the batch is built, because a
fraction chosen after the readings exist is not a reservation, it is a selection. So the census runs
first, declares the roster, applies the declared rule, and hashes the result. Only then does a generator
run — and only on the published complement.

WHY THESE ROWS. Batches 1 and 2 were both `graph`, which means every dial captured so far has moved along
one family's ramp. Three families carry ramps the census DECLARED and nothing has ever used
(`optimization`, `number-theoretic`, `algebraic` — the last two with "precedent: none yet" written into
the census itself). A declared-but-unused ramp is an untested assumption sitting in the artifact that
governs 222 future rows. Batch 3 spends itself on exactly that risk.

THE ROSTER IS CHECKED, NOT ASSERTED. Every row is verified unbuilt and REACH-subset against the census and
the existing panels. A roster that quietly re-lists a built row would double-count it in the catalog and
nothing downstream would notice.
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from foundry.catalog import reservation as RES                                  # noqa: E402

LAT = ROOT / "foundry" / "results" / "lattice"
OUT = LAT / "observatory_batch10_census.json"
LEDGER = LAT / "observatory_reservation.jsonl"
BATCH = 10

# family → (declared census ramp, the values this batch walks)
#
# The `optimization` family ramp — constraint-to-ground-set ratio — is ALREADY the Q21-corrected form
# for these rows: terminals, pairs or requirements per candidate edge is a within-instance parameter at
# a fixed ground set. No erratum was needed here; the declaration happened to be right.
FAMILY_RAMP = {
    "optimization": ("constraint-to-ground-set ratio", (0.5, 1.0, 1.5, 2.0, 3.0)),
}

# OPTIMIZATION-WEIGHTED BY RULING. The voided prereg_v34's successor needs 10 reserved optimization
# clusters and the frontier holds 3; optimization rows are ordinary build priority until it clears.
# These are every vetted, unbuilt, unreserved, not-capture-blocked optimization row that exists — six.
ROSTER = {
    "steiner-forest":                    ("optimization", "terminal pairs per candidate edge", "upward_closed"),
    "group-steiner-tree":                ("optimization", "groups per candidate edge", "upward_closed"),
    "directed-steiner-tree":             ("optimization", "terminals per candidate arc", "upward_closed"),
    "survivable-network-design":         ("optimization", "connectivity requirement per candidate edge", "upward_closed"),
    "prize-collecting-steiner-tree":     ("optimization", "penalty level per candidate edge", "downward_closed"),
    "maximum-feasible-linear-subsystem": ("optimization", "relations per variable", "downward_closed"),
}
CAPTURE_MODE = {}
FLAGGED = {}


def main() -> int:
    census = json.loads((LAT / "observatory_reach_census.json").read_text())
    adj = {a["problem_id"]: a for a in
           json.loads((LAT / "observatory_untyped_adjudication.json").read_text())["adjudications"]}
    built = set()
    for p in sorted(LAT.glob("observatory_batch*_panels.json")):
        d = json.loads(p.read_text())
        built |= {r["row"] for r in d["rows"]} | {e["row"] for e in d.get("excluded_at_birth", [])}
    built |= {x["row"] for x in
              json.loads((LAT / "sounding_v3_survey.json").read_text())["readings"] if x.get("row")}
    cls = {}
    for r in census["rows"]:
        a = adj.get(r["problem_id"])
        cls[r["problem_id"]] = (a["now"] if a else r["reach_class"], r.get("family"))

    # ── the roster is CHECKED ───────────────────────────────────────────────────────────────────────
    problems = []
    for row, (fam, _instantiates, _exp) in ROSTER.items():
        if row not in cls:
            problems.append(f"{row}: not in the reach census at all")
            continue
        c, cfam = cls[row]
        if c != "REACH-subset":
            problems.append(f"{row}: reach class is {c}, not REACH-subset")
        if row in built:
            problems.append(f"{row}: ALREADY BUILT — a re-listed row double-counts in the catalog")
        if cfam != fam:
            problems.append(f"{row}: census family is {cfam!r}, roster says {fam!r}")
    if problems:
        print("ROSTER REJECTED:")
        for p in problems:
            print("   " + p)
        return 1

    rec = RES.declare(LEDGER, BATCH, list(ROSTER), RES.DEFAULT_FRACTION)
    reserved = set(rec["reserved"])
    published = [r for r in ROSTER if r not in reserved]

    doc = {
        "schema": "observatory-batch-census/v1",
        "STATUS": "DECLARATION — no reading exists for any row here",
        "batch": BATCH,
        "why_this_batch": (
            "OPTIMIZATION-WEIGHTED by ruling. prereg_v34 was voided for clearing power "
            "against clusters its statistic could never read; its successor needs 10 reserved "
            "optimization clusters and the frontier holds 3. These are every vetted, unbuilt, "
            "unreserved, not-capture-blocked optimization row in the atlas — six. Each runs on a "
            "within-instance dial at a fixed candidate-edge ground set."),
        "families": {f: {"census_ramp": r, "ramp_values": list(v)} for f, (r, v) in FAMILY_RAMP.items()},
        "roster": {r: {"family": f, "instantiates_the_family_ramp_as": i,
                       "structural_expectation": e,
                       "capture_mode": CAPTURE_MODE.get(r, "RAMPED")}
                   for r, (f, i, e) in ROSTER.items()},
        "n_roster": len(ROSTER),
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
        "published": sorted(published),
        "carried_forward": FLAGGED,
    }
    OUT.write_text(json.dumps(doc, indent=1) + "\n")

    print(f"BATCH {BATCH} CENSUS — roster {len(ROSTER)}, reserved {len(reserved)}, published {len(published)}\n")
    for r, (f, i, e) in ROSTER.items():
        mark = "RESERVED " if r in reserved else "  publish "
        print(f"  {mark}{r:<30} {f:<17} {e or '—'}")
    print(f"\n  roster sha256   {rec['roster_sha256'][:16]}")
    print(f"  reserved        {', '.join(rec['reserved'])}")
    print(f"  ledger          {LEDGER.name}  ({len(RES.read_ledger(LEDGER))} record(s))")
    for k, v in FLAGGED.items():
        print(f"  CARRIED FORWARD: {k} — {v['disposition']}")
    print(f"  wrote {OUT.name}  sha256 {hashlib.sha256(OUT.read_bytes()).hexdigest()[:16]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
