#!/usr/bin/env python3
"""N6-R Phase 1 — the tranche declaration. OUTCOME-BLIND, HASHED.

WHAT THIS FIXES AND WHEN. The tranche is declared BEFORE any hull is computed and before any excess
exists. Nothing about a hull, an inflation ratio, or an outcome is consulted — enforced by
test_census_minimalism.py, which runs this module with file reads instrumented.

THE ADMISSION RULE, and most of it was sealed before this study existed:

  1. BLENDING FLOOR — |R| >= m. A region smaller than the blend's arity cannot be blended at all.
  2. prereg_v16's INSUFFICIENT FLOOR — |R|^m >= 20. Sealed in the qualification study: below it the
     violation rate is quantised coarser than 0.05, so the reading has no usable resolution. NOT invented
     here; inherited from the seal that qualified this instrument on this roster.
  3. CP FREEDOM >= 2 — declared now, and the only new criterion. Freedom is prod_k C(C(n,k), count_k),
     the exact number of distinct CP-admissible controls, in closed form. A class with freedom 1 has
     exactly one admissible control: the region itself, so its excess is identically zero by construction.
     52 of 4,072 classes are forced this way.
  4. CLOSED pairs go to CALIBRATION, not discovery — the derived join's forced direction. They are not
     discarded: every one must return infl == 1.0, a battery 1,149 checks wide.

WHY THE ADMISSION RULE ADMITS ALMOST EVERYTHING, AND WHY IT IS STATED ANYWAY. The roster's ambient is at
most 16, so the worst closure round is C(16,3) = 560 tuples and EVERY class is affordable. The affordability
rule is vacuous. That is the whole point: the defect that killed N6's in-sample census was selection on the
predictor axis, and it cannot occur where the rule admits the universe. The rule is written down so the
record shows the selection was DESIGNED rather than lucky.

STRATIFICATION is by CLOSURE FINGERPRINT x r-band. The fingerprint is which flavours the class is closed
under — structural, computed from the relation, and deliberately NOT a charge: the F2 law holds that
nothing here reads or writes a charge, and a charge-stratified tranche would smuggle one in through the
sampling frame.
"""
import hashlib
import json
import sys
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "dev"))
LAT = ROOT / "foundry" / "results" / "lattice"
ROSTER = LAT / "prism_v2_charges.json"
OUT = LAT / "n6r_tranche.json"
from n6r_control_census import cp_freedom                              # noqa: E402

FLAVOURS = {
    "majority": (lambda ts: tuple(1 if sum(c) >= 2 else 0 for c in zip(*ts)), 3),
    "minority": (lambda ts: tuple(c[0] ^ c[1] ^ c[2] for c in zip(*ts)), 3),
    "min":      (lambda ts: tuple(min(c) for c in zip(*ts)), 2),
    "max":      (lambda ts: tuple(max(c) for c in zip(*ts)), 2),
}
INSUFFICIENT_FLOOR = 20        # prereg_v16, sealed — |R|^m < 20 means the rate is quantised too coarsely
MIN_CP_FREEDOM = 2             # declared here; freedom 1 means the only control is the region itself


def is_closed(rel, op, m):
    R = set(rel)
    return all(op(ts) in R for ts in product(R, repeat=m))


def r_band(r):
    return "r<=4" if r <= 4 else ("5<=r<=8" if r <= 8 else ("9<=r<=12" if r <= 12 else "r>=13"))


def main() -> int:
    roster = json.loads(ROSTER.read_text())["charge_table"]
    discovery, calibration, excluded = [], [], []
    strata = {}

    for idx, c in enumerate(roster):
        rel = [tuple(t) for t in c["relation"]]
        r, n = len(rel), c["arity"]
        freedom = cp_freedom(rel, n)
        fp = []
        for fl, (op, m) in FLAVOURS.items():
            if r >= m and is_closed(rel, op, m):
                fp.append(fl)
        fingerprint = "+".join(fp) if fp else "none"
        for fl, (op, m) in FLAVOURS.items():
            rec = {"class_index": idx, "arity": n, "r": r, "ambient": 2 ** n,
                   "flavour": fl, "cp_freedom": freedom,
                   "fingerprint": fingerprint, "r_band": r_band(r)}
            if r < m:
                excluded.append({**rec, "why": "below blending floor (|R| < m)"}); continue
            if r ** m < INSUFFICIENT_FLOOR:
                excluded.append({**rec, "why": "prereg_v16 INSUFFICIENT floor (|R|^m < 20)"}); continue
            if freedom < MIN_CP_FREEDOM:
                excluded.append({**rec, "why": "CP freedom == 1 — the only admissible control is the "
                                               "region itself; excess would be identically zero"})
                continue
            if fl in fp:
                calibration.append({**rec, "role": "CALIBRATION",
                                    "expect": "infl == 1.0 (closed under this flavour)"})
                continue
            discovery.append(rec)
            key = f"{fingerprint}|{rec['r_band']}|{fl}"
            strata[key] = strata.get(key, 0) + 1

    payload = {"discovery": discovery, "calibration": calibration}
    tranche_hash = hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

    from collections import Counter
    doc = {"schema": "n6r-tranche/v1",
           "STATUS": "PHASE 1 — declared OUTCOME-BLIND, before any hull or excess exists",
           "what_was_not_consulted": ("no hull, no inflation ratio, no violation rate, no excess, no "
                                      "charge. The admission rule sees |R|, arity, closure fingerprint "
                                      "and CP freedom — all computable from the relation alone."),
           "admission_rule": {
               "1_blending_floor": "|R| >= m",
               "2_prereg_v16_insufficient_floor": f"|R|^m >= {INSUFFICIENT_FLOOR} — SEALED in the "
                                                  f"qualification study, not invented here",
               "3_cp_freedom": f">= {MIN_CP_FREEDOM} — declared here; freedom 1 means the only admissible "
                               f"control is the region itself",
               "4_closed_pairs": "routed to CALIBRATION, not discarded",
               "why_it_admits_nearly_everything": (
                   "ambient <= 16 makes every class affordable, so the affordability rule is VACUOUS. "
                   "That is the point: selection on the predictor axis cannot occur where the rule admits "
                   "the universe. The rule is written down so the record shows the selection was designed "
                   "rather than lucky.")},
           "stratification": ("closure fingerprint x r-band x flavour. The fingerprint is structural, "
                              "computed from the relation. Deliberately NOT a charge — the F2 law holds "
                              "that nothing here reads or writes one, and a charge-stratified frame would "
                              "smuggle one in through the sampling."),
           "n_discovery": len(discovery), "n_calibration": len(calibration), "n_excluded": len(excluded),
           "exclusion_reasons": dict(Counter(e["why"] for e in excluded)),
           "discovery_by_flavour": dict(Counter(d["flavour"] for d in discovery)),
           "discovery_by_fingerprint": dict(Counter(d["fingerprint"] for d in discovery)),
           "discovery_by_r_band": dict(Counter(d["r_band"] for d in discovery)),
           "n_strata": len(strata),
           "TRANCHE_HASH": tranche_hash,
           "hash_covers": "the discovery and calibration member lists, sorted-key canonical JSON",
           "discovery": discovery, "calibration": calibration, "excluded": excluded}
    OUT.write_text(json.dumps(doc, indent=1) + "\n")

    print("N6-R PHASE 1 — TRANCHE DECLARED (outcome-blind)\n")
    print(f"  discovery   : {len(discovery)}")
    print(f"  calibration : {len(calibration)}   <- infl must read exactly 1.0 on every one")
    print(f"  excluded    : {len(excluded)}")
    for k, v in sorted(doc["exclusion_reasons"].items(), key=lambda kv: -kv[1]):
        print(f"      {v:>5}  {k}")
    print(f"\n  discovery by flavour    : {doc['discovery_by_flavour']}")
    print(f"  discovery by r-band     : {doc['discovery_by_r_band']}")
    print(f"  distinct fingerprints   : {len(doc['discovery_by_fingerprint'])}")
    print(f"  strata (fp x band x fl) : {len(strata)}")
    print(f"\n  TRANCHE HASH: {tranche_hash}")
    print(f"\nwrote {OUT.name}  sha256 {hashlib.sha256(OUT.read_bytes()).hexdigest()[:16]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
