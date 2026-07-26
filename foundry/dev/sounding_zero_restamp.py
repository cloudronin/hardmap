#!/usr/bin/env python3
"""Re-emit the zero-hunt's corrected flags IN PLACE. Metadata correction — readings untouched.

WHAT MOVES: each exact-zero reading gains `zero_hunt_verdict` and its Q1 consequence. THIN-SATURATION
readings gain `insufficient: "INSUFFICIENT-r"` where the pre-declared floor applies. HIDDEN-CLOSURE
readings gain `closure_explained: true` so a future discovery statistic can exclude them by schema rather
than by anyone remembering to.

WHAT MUST NOT MOVE: every measured value. This script PROVES that rather than promising it — it snapshots
the measured fields before writing and re-checks them after, and refuses to write if any moved. The
program has been bitten by "metadata-only" edits that weren't, so the claim gets a test rather than a
sentence.
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LAT = ROOT / "foundry" / "results" / "lattice"
HUNT = LAT / "sounding_zero_hunt.json"
MEASURED_FIELDS = ("measured_rate", "control_mean", "control_sd", "excess", "r", "ambient_n",
                   "ambient_size", "distinct_subsets_used", "n_instances", "standardized_excess_UNSCORED")


def fingerprint(doc):
    """Every measured value in the file, in order — the thing that must be identical afterwards."""
    return [[x.get("row"), x.get("region"), x.get("flavor"), x.get("ramp_position")]
            + [x.get(f) for f in MEASURED_FIELDS] for x in doc["readings"]]


def main() -> int:
    hunt = json.loads(HUNT.read_text())
    verdicts = {}
    for a in hunt["adjudications"]:
        verdicts[(a["src"], a["row"], a["region"], a["flavor"], a["ramp_position"])] = a

    total = 0
    for fname, tag in (("sounding_survey_readings.json", "v2"), ("sounding_v3_survey.json", "v3")):
        p = LAT / fname
        doc = json.loads(p.read_text())
        before = fingerprint(doc)
        n = 0
        for x in doc["readings"]:
            a = verdicts.get((tag, x["row"], x["region"], x["flavor"], x.get("ramp_position")))
            if a is None:
                continue
            x["zero_hunt_verdict"] = a["verdict"]
            x["zero_hunt_argument"] = a["argument"]
            x["zero_hunt_q1_consequence"] = a["q1_consequence"]
            if a["verdict"] == "HIDDEN-CLOSURE":
                x["closure_explained"] = True
            if a["verdict"] == "THIN-SATURATION" and x["r"] < 10:
                x["insufficient"] = "INSUFFICIENT-r"
            n += 1
        after = fingerprint(doc)
        if before != after:                      # PROVEN, not promised
            print(f"FAIL — {fname}: a measured value moved during a metadata-only correction.",
                  file=sys.stderr)
            for b, a2 in zip(before, after):
                if b != a2:
                    print(f"    {b}\n -> {a2}", file=sys.stderr)
            return 1
        doc.setdefault("changelog", []).append({
            "date": "2026-07-26", "kind": "FLAG CORRECTION — NOT A RE-MEASUREMENT",
            "what": ("the zero-hunt's verdicts stamped onto every unforced exact-zero reading: "
                     "`zero_hunt_verdict`, its argument, its Q1 consequence; `closure_explained` on "
                     "HIDDEN-CLOSURE; `INSUFFICIENT-r` on THIN-SATURATION under the pre-declared floor."),
            "why": ("an unforced zero is not an unexplained one. 29 of 43 are explained by a closure the "
                    "template route cannot see, and leaving them unflagged would let a future discovery "
                    "statistic count them as findings."),
            "proof_readings_untouched": ("every measured field was fingerprinted before and after this "
                                         "edit and compared; the script refuses to write on any change."),
            "n_readings_stamped": n})
        doc["zero_hunt"] = {
            "artifact": "sounding_zero_hunt.json",
            "sha256": hashlib.sha256(HUNT.read_bytes()).hexdigest()[:16],
            "verdict_counts": hunt["verdict_counts"],
            "note": ("adjudication of every exact-zero reading not flagged theorem-forced. Closure claims "
                     "were TESTED by brute force, not asserted; one claim was falsified by its own test "
                     "and reversed.")}
        p.write_text(json.dumps(doc, indent=1) + "\n")
        print(f"  {fname:<34}stamped {n:>3}  sha256 {hashlib.sha256(p.read_bytes()).hexdigest()[:16]}")
        total += n

    print(f"\n  total readings stamped: {total}")
    print("  measured values verified identical in both files (fingerprint compare, not assertion)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
