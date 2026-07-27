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
OUT = LAT / "observatory_batch3_census.json"
LEDGER = LAT / "observatory_reservation.jsonl"
BATCH = 3

# family → (declared census ramp, the values this batch walks)
FAMILY_RAMP = {
    "optimization":     ("constraint-to-ground-set ratio", (0.5, 1.0, 1.5, 2.0, 3.0)),
    "number-theoretic": ("capacity fraction or value range", (0.2, 0.35, 0.5, 0.65, 0.8)),
    "algebraic":        ("system density (equations per unknown)", (1.2, 1.5, 2.0, 2.5, 3.0)),
}

# row → (family, what this row instantiates the family ramp AS, declared structural expectation)
ROSTER = {
    "d-hitting-set":                ("optimization", "sets-to-hit per ground element", "upward_closed"),
    "minimum-test-cover":           ("optimization", "item-pairs to separate per test", "upward_closed"),
    "max-coverage":                 ("optimization", "universe elements per candidate set",
                                     "fixed_cardinality"),
    "weighted-interval-scheduling": ("optimization", "intervals per time slot", "downward_closed"),
    "subset-product":               ("number-theoretic", "capacity fraction of the full product",
                                     "downward_closed"),
    "generalized-subset-sum":       ("number-theoretic", "value range", None),
    "minimum-distance-code":        ("algebraic", "code length per message bit", None),
    "nearest-codeword":             ("algebraic", "code length per message bit", None),
}

# A census defect found at first use, carried in the artifact rather than reported in prose.
FLAGGED = {
    "problem": "minimum-common-string-partition",
    "family": "string",
    "the_census_declared": "pattern/text length ratio (precedent: none yet — declared here, "
                           "first use at build)",
    "why_it_does_not_apply": (
        "MCSP takes TWO STRINGS OF EQUAL LENGTH and asks for a common partition. There is no pattern and "
        "no text, so the declared ratio has no referent in the row — it is not a hard dial or an "
        "expensive one, it is undefined. This is the only reachable `string` row in the atlas, so the "
        "family's declared ramp has no row it fits."),
    "what_was_NOT_done": (
        "no substitute ramp was invented. Alphabet size over string length would move the row's "
        "tightness, but swapping in an undeclared dial silently would make the census's family "
        "declarations unfalsifiable — the first time one failed, it would be quietly repaired instead "
        "of recorded."),
    "disposition": "EXCLUDED from batch 3, RAISED FOR RULING",
    "the_ruling_needed": (
        "either (a) amend the `string` family ramp to a dial that fits its one reachable row, which is a "
        "census erratum under the F4 versioning law, or (b) type the row "
        "`no-natural-dial-at-fixed-encoding` and let the string family carry zero ramped rows."),
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
            "batches 1 and 2 were both `graph`. Three census-declared family ramps have never been used, "
            "two of them recorded in the census with 'precedent: none yet'. Batch 3 tests those "
            "declarations, because they govern 222 queued rows."),
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
        "flagged_for_ruling": FLAGGED,
    }
    OUT.write_text(json.dumps(doc, indent=1) + "\n")

    print(f"BATCH 3 CENSUS — roster {len(ROSTER)}, reserved {len(reserved)}, published {len(published)}\n")
    for r, (f, i, e) in ROSTER.items():
        mark = "RESERVED " if r in reserved else "  publish "
        print(f"  {mark}{r:<30} {f:<17} {e or '—'}")
    print(f"\n  roster sha256   {rec['roster_sha256'][:16]}")
    print(f"  reserved        {', '.join(rec['reserved'])}")
    print(f"  ledger          {LEDGER.name}  ({len(RES.read_ledger(LEDGER))} record(s))")
    print(f"\n  FLAGGED FOR RULING: {FLAGGED['problem']} — {FLAGGED['disposition']}")
    print(f"  wrote {OUT.name}  sha256 {hashlib.sha256(OUT.read_bytes()).hexdigest()[:16]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
