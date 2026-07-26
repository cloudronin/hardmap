#!/usr/bin/env python3
"""Geometry Probe A — the repeat-triple deflator check, run BEFORE Score 3 is quoted anywhere.

THE CONCERN. The blend operations are idempotent in the relevant sense: for any m-tuple containing a
repeat, the blend returns a tuple already in R.
    majority(a,a,b) = a          minority(a,a,b) = b          min(a,a) = a          max(a,a) = a
So A TUPLE WITH A REPEAT CAN NEVER VIOLATE. Violations live exclusively on all-distinct tuples.

`exhaustive_rate` iterated `product(rel, repeat=m)` — the full Cartesian product, repeats INCLUDED. The
denominator therefore contains a large block of tuples that are incapable of violating, and the reported
rate is mechanically capped at the all-distinct fraction:

    cap(r, m) = r(r-1)...(r-m+1) / r^m

At this roster's sizes that cap is severe: r=4, m=3 caps at 0.375; r=6 at 0.556; r=15 at 0.813. A "middle
band" of rates in 0.05-0.50 and a ceiling of "nothing above 0.50" could therefore be TUPLE-COUNT ARITHMETIC
wearing a geometry finding's clothes.

THE TYPED NULL for a violation rate is the rate conditioned on tuples that COULD violate. Because
violations occur only on distinct tuples, the arithmetic is exact and needs no re-enumeration:

    bad_raw == bad_distinct   =>   rate_distinct = rate_raw / cap(r, m)

Scores 1 and 2 are untouched by this and do not depend on the distribution's shape: the battery is a
binary (rate == 0 iff closed) that repeats cannot flip, and sensitivity asks only whether ANY violation was
found. The licence stands regardless. This is about what the free question actually found.
"""
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "dev"))
from geometry_probe_a import FLAVORS, exhaustive_rate, MIDDLE_BAND      # noqa: E402

LAT = ROOT / "foundry" / "results" / "lattice"
OUT = LAT / "geometry_probe_deflator_results.json"
BANDS = [("zero", 0.0, 0.0), ("0_to_005", 0.0, 0.05), ("005_to_015", 0.05, 0.15),
         ("015_to_030", 0.15, 0.30), ("030_to_050", 0.30, 0.50), ("050_to_075", 0.50, 0.75),
         ("075_to_1", 0.75, 1.0001)]


def cap(r, m):
    """Fraction of m-tuples that are all-distinct — the mechanical ceiling on any uniform-tuple rate."""
    num = 1
    for i in range(m):
        num *= (r - i)
    return max(0, num) / (r ** m)


def band_of(v):
    if v == 0.0:
        return "zero"
    for name, lo, hi in BANDS[1:]:
        if lo < v < hi:
            return name
    return "075_to_1"


def main() -> int:
    ct = json.loads((LAT / "prism_v2_charges.json").read_text())["charge_table"]
    per_flavor = {}
    for fl, (op, m, flag) in FLAVORS.items():
        raw_hist, dis_hist = Counter(), Counter()
        raw_nz, dis_nz, undef = [], [], 0
        by_r = {}
        for row in ct:
            rel = [tuple(int(b) for b in t) for t in row["relation"]]
            r = len(rel)
            c = cap(r, m)
            raw, tot = exhaustive_rate(rel, op, m)
            raw_hist[band_of(raw)] += 1
            if raw > 0:
                raw_nz.append(raw)
            if c == 0:                                   # no distinct m-tuple exists -> undefined
                undef += 1
                continue
            dis = raw / c                                # exact: violations live only on distinct tuples
            dis = min(dis, 1.0)
            dis_hist[band_of(dis)] += 1
            if dis > 0:
                dis_nz.append(dis)
            b = by_r.setdefault(r, {"n": 0, "cap": round(c, 4), "max_raw": 0.0, "max_distinct": 0.0})
            b["n"] += 1
            b["max_raw"] = max(b["max_raw"], round(raw, 4))
            b["max_distinct"] = max(b["max_distinct"], round(dis, 4))

        def mid(vals):
            return (round(sum(1 for v in vals if MIDDLE_BAND[0] <= v <= MIDDLE_BAND[1]) / len(vals), 4)
                    if vals else None)
        per_flavor[fl] = {
            "m": m,
            "undefined_no_distinct_tuple": undef,
            "raw": {"histogram": {k: raw_hist.get(k, 0) for k, _, _ in BANDS},
                    "n_nonzero": len(raw_nz),
                    "middle_band_fraction_of_nonzero": mid(raw_nz),
                    "mean_nonzero": round(sum(raw_nz) / len(raw_nz), 4) if raw_nz else None,
                    "max": round(max(raw_nz), 4) if raw_nz else None},
            "distinct_conditioned": {"histogram": {k: dis_hist.get(k, 0) for k, _, _ in BANDS},
                                     "n_nonzero": len(dis_nz),
                                     "middle_band_fraction_of_nonzero": mid(dis_nz),
                                     "mean_nonzero": round(sum(dis_nz) / len(dis_nz), 4) if dis_nz else None,
                                     "max": round(max(dis_nz), 4) if dis_nz else None},
            "by_relation_size": {str(k): by_r[k] for k in sorted(by_r)},
        }

    doc = {"schema": "geometry-probe-deflator/v1", "prereg": "prereg_v16 (pre-claim check)",
           "concern": ("blend operations are idempotent on repeats, so a tuple containing a repeat CANNOT "
                       "violate. exhaustive_rate iterated product(rel, repeat=m) — repeats INCLUDED — so "
                       "every reported rate is mechanically capped at the all-distinct fraction "
                       "r(r-1)...(r-m+1)/r^m."),
           "expression_read_first": ("geometry_probe_a.exhaustive_rate: `for ts in product(rel, repeat=m)`. "
                                     "The Cartesian product. Repeats are included, so the concern is LIVE "
                                     "and part 2 is a correction, not a confirmation."),
           "arithmetic": ("violations occur only on distinct tuples, so bad_raw == bad_distinct and "
                          "rate_distinct = rate_raw / cap(r, m) exactly. No re-enumeration needed."),
           "scores_1_and_2_unaffected": ("the battery is a binary (rate==0 iff closed) that repeats cannot "
                                         "flip; sensitivity asks only whether ANY violation was found. "
                                         "The QUALIFIED verdict and the licence stand regardless."),
           "per_flavor": per_flavor}
    ack = []
    for fl, v in per_flavor.items():
        if v["distinct_conditioned"]["max"] == 1.0:
            ack.append({"stat": f"per_flavor.{fl}.distinct_conditioned.max", "value": 1.0,
                        "why_the_exactness_is_expected": (
                            "THIS 1.0 IS THE RETRACTION'S EVIDENCE. Some relations violate on EVERY "
                            "distinct tuple, so conditioned on the tuples that could violate their rate is "
                            "exactly 1. The raw statistic hid them below the mechanical cap — which is "
                            "precisely why the 'almost-closed middle' reading failed.")})
        for r, b in v["by_relation_size"].items():
            if b["max_distinct"] == 1.0:
                ack.append({"stat": f"per_flavor.{fl}.by_relation_size.{r}.max_distinct", "value": 1.0,
                            "why_the_exactness_is_expected": (
                                f"at r={r} the maximum RAW rate equals the mechanical cap "
                                f"({b['cap']}) exactly, so the distinct-conditioned rate is 1.0 by "
                                f"arithmetic. A relation violating on every distinct tuple is the opposite "
                                f"of 'almost closed', and it was invisible in the raw statistic.")})
    doc["extremal_acknowledged"] = ack
    OUT.write_text(json.dumps(doc, indent=1) + "\n")

    print("GEOMETRY PROBE A — REPEAT-TRIPLE DEFLATOR CHECK\n")
    print("mechanical cap by relation size (fraction of m-tuples that are all-distinct):")
    print(f"    {'r':>4}" + "".join(f"{('m='+str(m)):>10}" for m in (2, 3)))
    for r in (2, 3, 4, 6, 8, 10, 15):
        print(f"    {r:>4}" + "".join(f"{cap(r, m):>10.4f}" for m in (2, 3)))
    print()
    for fl, v in per_flavor.items():
        rw, dc = v["raw"], v["distinct_conditioned"]
        print(f"--- {fl}  (m={v['m']}, {v['undefined_no_distinct_tuple']} classes have NO distinct tuple)")
        print(f"      {'':<22}{'RAW':>12}{'DISTINCT-COND':>16}")
        print(f"      {'middle-band frac':<22}{rw['middle_band_fraction_of_nonzero']:>12}"
              f"{dc['middle_band_fraction_of_nonzero']:>16}")
        print(f"      {'mean nonzero':<22}{rw['mean_nonzero']:>12}{dc['mean_nonzero']:>16}")
        print(f"      {'max':<22}{rw['max']:>12}{dc['max']:>16}")
        print(f"      raw  hist {rw['histogram']}")
        print(f"      dist hist {dc['histogram']}")
    print("\nCEILING STRATIFIED BY r (the 'nothing above 0.50' claim), majority:")
    mj = per_flavor["majority"]["by_relation_size"]
    print(f"    {'r':>4}{'n':>7}{'cap':>9}{'max raw':>10}{'max distinct':>14}")
    for r in sorted(mj, key=int):
        b = mj[r]
        print(f"    {r:>4}{b['n']:>7}{b['cap']:>9.4f}{b['max_raw']:>10.4f}{b['max_distinct']:>14.4f}")
    print(f"\nwrote {OUT.name}  sha256 {hashlib.sha256(OUT.read_bytes()).hexdigest()[:16]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
