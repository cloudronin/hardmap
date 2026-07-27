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
OUT = LAT / "observatory_batch4_census.json"
LEDGER = LAT / "observatory_reservation.jsonl"
BATCH = 4

# family → (declared census ramp, the values this batch walks)
FAMILY_RAMP = {
    "graph":            ("edge density", (0.15, 0.25, 0.35, 0.45, 0.60)),
    "number-theoretic": ("capacity fraction or value range", (0.2, 0.35, 0.5, 0.65, 0.8)),
}

# row → (family, what this row instantiates the family ramp AS, declared structural expectation)
ROSTER = {
    "edge-dominating-set":       ("graph", "edge density of the ground graph", "upward_closed"),
    "cluster-vertex-deletion":   ("graph", "edge density of the ground graph", "upward_closed"),
    "feedback-arc-set":          ("graph", "arc density of the ground digraph", "upward_closed"),
    "capacitated-vertex-cover":  ("graph", "edge density of the ground graph", "upward_closed"),
    "connected-vertex-cover":    ("graph", "edge density of the ground graph", None),
    "balanced-vertex-separator": ("graph", "edge density of the ground graph", "upward_closed"),
    "3sum":                      ("number-theoretic", "value range", "fixed_cardinality"),
    "3-partition":               ("number-theoretic", "value range", "fixed_cardinality"),
}

# Carried forward rather than closed: two rows batch 4 does NOT take, each for a stated reason.
FLAGGED = {
    "minimum-common-string-partition": {
        "disposition": "DEFERRED to batch 5 under its new CONTRAST-DIAL typing",
        "why": ("ruled 2026-07-27: the amended alphabet ramp moves once (|Sigma| = 2) and is flat from "
                "3 to 8, so the row enters as a declared two-level factor rather than a trajectory. "
                "The contrast-capture path is built at batch 5; forcing it into batch 4's ramped "
                "pipeline would catalogue a threshold as a slope."),
    },
    "covering-radius": {
        "disposition": "HELD — needs a framing that keeps the ambient fixed",
        "why": ("the natural region (words within distance r of the code) lives in WORD space, so "
                "ramping the code length would grow the ambient 2^n along with the dial — a size knob "
                "smuggled in under a constraint-density ramp. minimum-distance-code avoided this by "
                "keeping its region in MESSAGE space with k fixed; covering-radius has no such framing "
                "yet, and inventing one under time pressure is how an encoding artifact enters. It is "
                "the algebraic family's last unbuilt row and can wait for the framing."),
    },
}


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
            "batch 3 opened three new families; batch 4 works the queue's bulk. Six graph rows keep "
            "the screen stack's closure directions in exercise, and the two remaining number-theoretic "
            "rows finish that family's reachable set. 3sum is deliberately included: it declares "
            "fixed_cardinality while its region stays instance-dependent, which is the case that "
            "narrowed the structurally-flat rule at descriptor@v3."),
        "families": {f: {"census_ramp": r, "ramp_values": list(v)} for f, (r, v) in FAMILY_RAMP.items()},
        "roster": {r: {"family": f, "instantiates_the_family_ramp_as": i,
                       "structural_expectation": e} for r, (f, i, e) in ROSTER.items()},
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
