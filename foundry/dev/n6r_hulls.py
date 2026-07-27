#!/usr/bin/env python3
"""N6-R Phase 2 — exact hulls, the calibration battery, the degeneracy check, then PREDICTIONS HASHED.

ORDER IS THE WHOLE POINT and it is enforced by this file's control flow:
    1. verify the tranche hash — the predictions must bind to the declared population, not a drifted one
    2. exact hulls on every tranche member
    3. THE CALIBRATION BATTERY — all 963 closed pairs must return infl == 1.0, or this HALTS
    4. degeneracy check on infl's OWN distribution (census minimalism: no joins, no outcome)
    5. freeze inflation
    6. emit directional predictions and hash them — THE PREDICTION FILE IS THE SEAL

No excess is computed, read, or imported here. Phase 3 is the first moment an outcome exists, and by then
the predictions are hashed and committed. Blindness holds by construction rather than by discipline.

THE SEALED DIRECTION comes from N6's disclosed prior, and it is the OPPOSITE of what N6's original spec
guessed: on the contaminated 43% subsample, high inflation associated with MORE negative excess (partial
Spearman = -0.3684 controlling for measured rate). That prior is a fact about a biased subsample until this
replicates. Here it becomes a blind bet on a population whose outcomes do not exist yet.

WHY THE CALIBRATION BATTERY IS FREE AND WHY IT IS 963 WIDE. Pairs closed under their flavour are excluded
from discovery by the derived join — they carry no information about the relationship. But closure means
hull(R) == R exactly, so every one is a known-answer check on the machinery, at no extra cost. The natural
battery ran 17. If the hull routine has drifted, 963 simultaneous exact answers will say so.
"""
import hashlib
import json
import sys
from itertools import combinations, product
from pathlib import Path
from statistics import mean, pstdev

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "dev"))
LAT = ROOT / "foundry" / "results" / "lattice"
ROSTER = LAT / "prism_v2_charges.json"
TRANCHE = LAT / "n6r_tranche.json"
OUT_INFL = LAT / "n6r_inflation.json"
OUT_PRED = LAT / "n6r_predictions.json"

FLAVOURS = {
    "majority": (lambda ts: tuple(1 if sum(c) >= 2 else 0 for c in zip(*ts)), 3),
    "minority": (lambda ts: tuple(c[0] ^ c[1] ^ c[2] for c in zip(*ts)), 3),
    "min":      (lambda ts: tuple(min(c) for c in zip(*ts)), 2),
    "max":      (lambda ts: tuple(max(c) for c in zip(*ts)), 2),
}
SEALED_DIRECTION = "NEGATIVE"
DEGENERACY_SD_FLOOR = 0.05
DEGENERACY_DISTINCT_FLOOR = 5


def hull_profile(R, op, m):
    """EXACT closure by iteration. Ambient <= 16 here, so no budget guard is needed and none is used —
    a guard that never binds is a guard that hides whether it would have."""
    cur = set(R)
    rounds = []
    while True:
        new = {op(t) for t in combinations(cur, m)} - cur
        if not new:
            return len(cur), rounds
        cur |= new
        rounds.append(len(new))


def main() -> int:
    tr = json.loads(TRANCHE.read_text())
    payload = {"discovery": tr["discovery"], "calibration": tr["calibration"]}
    h = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    if h != tr["TRANCHE_HASH"]:
        print(f"FAIL — tranche hash mismatch. Declared {tr['TRANCHE_HASH']}, recomputed {h}. The "
              f"predictions would bind to a population that is not the declared one.", file=sys.stderr)
        return 1
    print(f"N6-R PHASE 2\n\n  tranche hash verified: {h[:32]}...\n")

    roster = json.loads(ROSTER.read_text())["charge_table"]
    rel_of = {i: [tuple(t) for t in c["relation"]] for i, c in enumerate(roster)}

    # ── 3. THE CALIBRATION BATTERY — runs BEFORE anything is frozen ─────────────────────────────────
    fails = []
    for rec in tr["calibration"]:
        rel = rel_of[rec["class_index"]]
        op, m = FLAVOURS[rec["flavour"]]
        size, rounds = hull_profile(rel, op, m)
        infl = size / len(rel)
        if abs(infl - 1.0) > 1e-12 or rounds:
            fails.append({**{k: rec[k] for k in ("class_index", "arity", "r", "flavour")},
                          "infl": infl, "rounds": rounds})
    print(f"  CALIBRATION BATTERY: {len(tr['calibration'])} closed pairs, "
          f"{len(tr['calibration']) - len(fails)} returned infl == 1.0 exactly")
    if fails:
        print(f"\nFAIL — {len(fails)} closed pairs did not return infl == 1.0. Closure means hull(R) == R "
              f"by definition, so the hull routine is not computing closure and nothing downstream is "
              f"trustworthy:", file=sys.stderr)
        for f in fails[:10]:
            print(f"    {f}", file=sys.stderr)
        return 1

    # ── 4. hulls on the discovery population ────────────────────────────────────────────────────────
    disc = []
    for rec in tr["discovery"]:
        rel = rel_of[rec["class_index"]]
        op, m = FLAVOURS[rec["flavour"]]
        size, rounds = hull_profile(rel, op, m)
        disc.append({**{k: rec[k] for k in ("class_index", "arity", "r", "ambient", "flavour",
                                            "cp_freedom", "fingerprint", "r_band")},
                     "hull": size, "infl": round(size / rec["r"], 6),
                     "depth": len(rounds), "round_additions": rounds})

    # ── 5. DEGENERACY CHECK on infl's OWN distribution. No joins. ───────────────────────────────────
    infl = [d["infl"] for d in disc]
    sd = pstdev(infl)
    distinct = len({round(v, 3) for v in infl})
    degenerate = sd < DEGENERACY_SD_FLOOR or distinct < DEGENERACY_DISTINCT_FLOOR
    per_fl = {}
    for fl in FLAVOURS:
        v = [d["infl"] for d in disc if d["flavour"] == fl]
        if v:
            per_fl[fl] = {"n": len(v), "min": round(min(v), 4), "max": round(max(v), 4),
                          "median": round(sorted(v)[len(v) // 2], 4), "sd": round(pstdev(v), 4),
                          "n_exactly_1": sum(1 for x in v if abs(x - 1.0) < 1e-12)}
    print(f"\n  DEGENERACY CHECK (infl's own distribution; no joins)")
    print(f"    {'flavour':<10}{'n':>6}{'median':>9}{'max':>9}{'sd':>9}{'infl==1':>9}")
    for fl, c in per_fl.items():
        print(f"    {fl:<10}{c['n']:>6}{c['median']:>9.3f}{c['max']:>9.2f}{c['sd']:>9.3f}"
              f"{c['n_exactly_1']:>9}")
    print(f"    pooled sd {sd:.4f}, {distinct} distinct values -> "
          f"{'DEGENERATE — seal re-scopes' if degenerate else 'varies; seal proceeds'}")
    if degenerate:
        print("\nFAIL — the predictor is degenerate on the declared tranche. The seal re-scopes rather "
              "than betting on a constant.", file=sys.stderr)
        return 1

    infl_doc = {"schema": "n6r-inflation/v1",
                "STATUS": "PHASE 2 — predictor FROZEN. No outcome computed, read or imported.",
                "tranche_hash": h,
                "calibration_battery": {"n": len(tr["calibration"]), "all_returned_infl_1": True,
                                        "note": ("closure means hull(R) == R by definition, so every "
                                                 "closed pair is a free known-answer check. The natural "
                                                 "battery ran 17; this one is 963 wide.")},
                "degeneracy_check": {"pooled_sd": round(sd, 5), "distinct_values": distinct,
                                     "degenerate": degenerate, "per_flavour": per_fl},
                "n_discovery": len(disc), "readings": disc}
    OUT_INFL.write_text(json.dumps(infl_doc, indent=1) + "\n")
    infl_hash = hashlib.sha256(OUT_INFL.read_bytes()).hexdigest()

    # ── 6. PREDICTIONS — hashed. THIS FILE IS THE SEAL. ────────────────────────────────────────────
    med = sorted(infl)[len(infl) // 2]
    per_reading = [{"class_index": d["class_index"], "flavour": d["flavour"],
                    "log_infl_rank_side": "high" if d["infl"] > med else "low",
                    "predicted_excess_side": "more negative" if d["infl"] > med else "less negative"}
                   for d in disc]
    pred = {"schema": "n6r-predictions/v1",
            "STATUS": "SEALED. Filed before any excess for this population exists.",
            "binds_to": {"tranche_hash": h, "inflation_artifact_sha256": infl_hash},
            "SEALED_BET_A": {
                "statistic": ("partial Spearman of log-inflation against fair-null excess, controlling "
                              "for measured violation rate, on the discovery population"),
                "direction": SEALED_DIRECTION,
                "meaning": "higher inflation associates with MORE negative excess",
                "provenance": ("N6's disclosed prior: partial = -0.3684 on the contaminated 43% "
                               "subsample. That is a fact about a biased subsample; this is the blind "
                               "test of whether it survives."),
                "and_it_is_the_opposite_of_the_original_guess": (
                    "N6's first spec sealed POSITIVE — regions near their hulls carrying the most "
                    "negative excess. The data disagreed. Betting on the direction the evidence points "
                    "rather than the one the theory suggested is the point of re-posing."),
                "decision": "CI clear of zero in the sealed direction, permutation null typed to the "
                            "population"},
            "depth_is_descriptive_everywhere": ("three usable levels on the natural side; reported, "
                                                "never sealed"),
            "saturation_screen_declared_now": (
                "Terrain's rider: any discovery reading whose measured rate is EXACTLY 1.0 is flagged "
                "suspected-forced, and the sealed statistic is reported WITH and WITHOUT them. Declared "
                "here, before any rate exists, so the screen cannot be chosen after seeing which way it "
                "moves the answer."),
            "median_inflation_at_seal_time": round(med, 6),
            "n_predictions": len(per_reading),
            "per_reading_predictions": per_reading}
    OUT_PRED.write_text(json.dumps(pred, indent=1) + "\n")
    pred_hash = hashlib.sha256(OUT_PRED.read_bytes()).hexdigest()

    print(f"\n  inflation frozen : {OUT_INFL.name}  sha256 {infl_hash[:16]}")
    print(f"  PREDICTIONS SEALED: {OUT_PRED.name}")
    print(f"    sha256 {pred_hash}")
    print(f"    direction {SEALED_DIRECTION}, {len(per_reading)} per-reading predictions")
    print(f"    median inflation at seal time {med:.4f}")
    print(f"\n  Phase 3 must assert this hash before scoring.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
