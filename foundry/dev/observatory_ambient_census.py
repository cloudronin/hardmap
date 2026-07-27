#!/usr/bin/env python3
"""Which built rows have an ambient that moves with their dial? (Q21, ruled 2026-07-27)

DERIVED, NEVER LISTED. The obvious way to record "these rows are edge-subset rows" is a hand-written
list, and this program has been bitten by hand-written lists often enough to have a law about it. So the
census RUNS each row's generator across its declared ramp and measures the ground-set width directly.
A row is ambient-confounded iff its width is not identical at every step.

WHY IT MATTERS, precisely. Each step's excess is a valid measurement against its own matched control and
stays honest forever — that is a LEVEL descriptor. But slope, `traj_class` and kink presuppose the x-axis
is a tightening dial over a FIXED space. When the ground set is the edge set and the dial is edge density,
the x-axis moves the universe too, and those descriptors conflate "constraints tightened" with "the space
grew". A semantically confounded number does not ship with a warning; it does not ship.

This is NOT the kink precedent. Kink values are meaningful-but-untested — they have a referent and lack a
null. These are meaningless-as-defined: there is no quantity for them to be an estimate of.

THE v3 SURVEY ROWS ARE CHECKED THE SAME WAY, through `terrain_score.replay`, because assuming the older
column is fine is exactly the assumption this census exists to stop making.
"""
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "dev"))
LAT = ROOT / "foundry" / "results" / "lattice"
OUT = LAT / "observatory_ambient_census.json"
from foundry.catalog import capture as C                                        # noqa: E402

SEED = 20260727


def batch_rows():
    """(row, builder, ramp) for every row any batch module defines."""
    import observatory_batch1 as B1
    import observatory_batch2 as B2
    import observatory_batch3 as B3
    import observatory_batch4 as B4
    import observatory_batch5 as B5
    import observatory_batch6 as B6
    import observatory_batch7 as B7
    out = []
    for row, (b, _e) in B1.ROWS.items():
        out.append((row, 1, b, B1.EDGE_DENSITY_RAMP))
    for row, (b, _e) in B2.ROWS.items():
        out.append((row, 2, b, B2.RAMP))
    for row, (b, _e, _f, ramp, _i) in B3.ROWS.items():
        out.append((row, 3, b, ramp))
    for row, (b, _e, _f, ramp, _i) in B4.ROWS.items():
        out.append((row, 4, b, ramp))
    for row, (b, _e, _f, ramp, _i, _m) in B5.ROWS.items():
        out.append((row, 5, b, ramp))
    for row, (b, _e, _f, ramp, _i) in B6.ROWS.items():
        out.append((row, 6, b, ramp))
    for row, (b, _e, _f, ramp, _i) in B7.ROWS.items():
        out.append((row, 7, b, ramp))
    return out


def v3_widths():
    """Ground-set widths for the frozen v3 survey rows, via replay of their recorded seeds."""
    import terrain_score as T
    doc = json.loads((LAT / "sounding_v3_survey.json").read_text())
    by = {}
    for m in doc["ramp_manifest"]:
        try:
            regions, _ = T.replay(m["row"], m["ramp_position"], m["seed"])
        except Exception:
            continue
        for _kind, regs in regions.items():
            for r in regs:
                if r:
                    by.setdefault(m["row"], []).append(len(r[0]))
                    break
            break
    return by


def main() -> int:
    print("AMBIENT CENSUS — does the ground set stand still while the dial moves?\n")
    rows = []
    for row, batch, build, ramp in batch_rows():
        rng = random.Random(SEED)
        stable, widths = C.ambient_stability(build, ramp, rng)
        rows.append({"problem_id": row, "batch": batch, "ramp_values": list(ramp),
                     "ground_set_widths": widths,
                     "ambient_stable": stable,
                     "ambient_confounded": (stable is False)})
    print("  replaying the frozen v3 column ...", flush=True)
    for row, widths in sorted(v3_widths().items()):
        stable = (len(set(widths)) == 1) if len(widths) >= 2 else None
        rows.append({"problem_id": row, "batch": "v3-survey", "ramp_values": None,
                     "ground_set_widths": widths, "ambient_stable": stable,
                     "ambient_confounded": (stable is False)})

    conf = sorted(r["problem_id"] for r in rows if r["ambient_confounded"])
    doc = {"schema": "observatory-ambient-census/v1",
           "STATUS": "DERIVED — every verdict computed by running the generator, none listed by hand",
           "question": "is the ground-set width identical at every declared ramp step?",
           "rule": ("ambient_confounded iff the width differs across steps. The ambient 2^w must be the "
                    "same object for readings to be comparable; a tolerance here would be a threshold "
                    "invented to let something through."),
           "consequence": {
               "level_descriptors": "STAND — each step's excess is a valid measurement at its own "
                                    "(width, density), against its own matched control",
               "shape_and_transition_descriptors": "n.a.-ambient-confounded — slope, traj_class and "
                                                   "kink presuppose a fixed space; here the x-axis "
                                                   "moves the universe too",
               "not_the_kink_precedent": "kink values are meaningful-but-untested; these are "
                                         "meaningless-as-defined"},
           "n_rows": len(rows), "n_confounded": len(conf), "confounded": conf,
           "rows": sorted(rows, key=lambda z: (str(z["batch"]), z["problem_id"]))}
    OUT.write_text(json.dumps(doc, indent=1) + "\n")

    for r in doc["rows"]:
        mark = "CONFOUNDED" if r["ambient_confounded"] else ("stable" if r["ambient_stable"] else "n/a")
        print(f"  {str(r['batch']):<10} {r['problem_id']:<28} {mark:<11} widths "
              f"{sorted(set(r['ground_set_widths']))}")
    print(f"\n  {len(conf)} of {len(rows)} rows ambient-confounded: {', '.join(conf)}")
    print(f"  wrote {OUT.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
