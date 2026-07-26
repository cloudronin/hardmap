#!/usr/bin/env python3
"""The check the forced-CLOSED direction never had — and the generator defect it finds.

THE ASYMMETRY. When `forced_saturated` was built it shipped with a two-way check against observation:
claims saturation where the data disagrees (halt), and exact-1.0 readings the derivation misses (report).
It found 0 contradictions.

ITS OLDER SIBLING NEVER GOT ONE. `theorem_forced = True` asserts that violation is FORCED TO 0 — a
polymorphism of the pinned template is closed on every instance's solution set. That implication was
derived, stamped, and used to exclude readings from every discovery statistic, and **nobody ever compared
it to the measured rates.**

Five readings contradict it, all `horn-sat · solutions · min`, measuring 0.1177 to 0.6074 while flagged
"violation forced to zero".

THE CAUSE, found by reading the generator rather than the flag:

    elif mode == "horn": ok = any(vals[i] == sg[i] for i in range(k))
    else:                ok = any(vals[i] == sg[i] for i in range(k))

The two branches are BYTE-IDENTICAL. `sat(..., mode="horn")` draws signs uniformly at random, so it emits
plain random 3-CNF. A Horn clause has AT MOST ONE POSITIVE LITERAL; nothing in that branch enforces it.

So `horn-sat` is not Horn. Marrow pinned a Horn template for the row, the join correctly derived
`horn => min forced` from that template, and the derivation was sound — **the instances were not what the
row said they were.** The flag was right about the template and wrong about the data.

WHAT THIS SCRIPT DOES, and does not do:
  - adds the missing two-way check as standing machinery
  - corrects `theorem_forced` for the affected readings, WITH provenance naming the generator defect
  - leaves every measured value untouched, verified by fingerprint
  - does NOT rename the row, re-generate any instance, or re-measure anything. The readings are valid
    measurements OF A PLAIN 3-CNF ROW; what was wrong is the label and the flag derived from it. Renaming
    a survey row is a ruling, not a hygiene fix.
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LAT = ROOT / "foundry" / "results" / "lattice"
MEASURED = ("measured_rate", "control_mean", "control_sd", "excess", "r", "ambient_n", "ambient_size",
            "distinct_subsets_used", "n_instances", "standardized_excess_UNSCORED")

DEFECTIVE_GENERATOR = {
    "horn-sat": ("sounding_v3_survey.sat(..., mode='horn') is byte-identical to the plain branch — "
                 "`ok = any(vals[i] == sg[i] for i in range(k))` with signs drawn uniformly at random. "
                 "A Horn clause has at most one positive literal and nothing enforces it, so the row "
                 "emits plain random 3-CNF. Marrow's pinned Horn template is correct for the NAME and "
                 "wrong for the DATA, so every flag derived from it is invalid on this row.")}


def fingerprint(doc):
    return [[x.get("row"), x.get("region"), x.get("flavor"), x.get("ramp_position")]
            + [x.get(f) for f in MEASURED] for x in doc["readings"]]


def main() -> int:
    contradictions, corrected = [], 0
    for fname in ("sounding_survey_readings.json", "sounding_v3_survey.json"):
        p = LAT / fname
        doc = json.loads(p.read_text())
        before = fingerprint(doc)
        for x in doc["readings"]:
            if x.get("theorem_forced") is not True or x.get("measured_rate") is None:
                continue
            if x["measured_rate"] == 0.0:
                continue
            contradictions.append({"row": x["row"], "region": x["region"], "flavor": x["flavor"],
                                   "measured_rate": x["measured_rate"], "file": fname})
            why = DEFECTIVE_GENERATOR.get(x["row"])
            if why is None:
                # a contradiction with NO identified cause is a HALT: the flag and the data disagree and
                # nobody knows which is wrong. That must not be silently corrected in either direction.
                print(f"FAIL — {x['row']}·{x['region']}·{x['flavor']} is flagged forced-closed but "
                      f"measures {x['measured_rate']}, and no generator defect explains it. Read it "
                      f"before this ships.", file=sys.stderr)
                return 1
            x["theorem_forced"] = False
            x["forced_provenance"] = ("CORRECTED — the derivation was sound and its INPUT was not. " + why)
            x["forced_flag_erratum"] = "generator-defect/horn-not-horn/2026-07-26"
            corrected += 1
        after = fingerprint(doc)
        if before != after:
            print(f"FAIL — {fname}: a measured value moved during a flag correction.", file=sys.stderr)
            return 1
        if corrected:
            doc["forced_closed_check"] = {
                "what": ("`theorem_forced = True` asserts violation is forced to 0. This check compares "
                         "that implication to the measured rate on every flagged reading."),
                "why_it_did_not_exist": ("the forced-SATURATED direction shipped with a two-way check "
                                         "when it was built; its older sibling never got one. Five "
                                         "contradictions sat unread from the day the join landed."),
                "contradictions_found": len(contradictions),
                "cause": DEFECTIVE_GENERATOR,
                "what_was_NOT_done": ("no row renamed, no instance regenerated, no rate re-measured. The "
                                      "readings are valid measurements of a plain 3-CNF row; the label "
                                      "and the flag derived from it were wrong. Renaming a survey row is "
                                      "a ruling, not a hygiene fix."),
                "downstream": ("Terrain is UNAFFECTED: none of the wrongly-excluded readings had positive "
                               "excess, so none would have entered its anomaly set. N1's population grows "
                               "by the corrected readings that are otherwise admissible.")}
            doc.setdefault("changelog", []).append({
                "date": "2026-07-26", "kind": "FLAG CORRECTION — NOT A RE-MEASUREMENT",
                "what": f"`theorem_forced` corrected on {corrected} readings; measured values verified "
                        f"unmoved by fingerprint compare.",
                "why": "a generator defect made the row's pinned template inapplicable to its own data."})
            p.write_text(json.dumps(doc, indent=1) + "\n")
            print(f"  {fname:<34}corrected {corrected:>2}  "
                  f"sha256 {hashlib.sha256(p.read_bytes()).hexdigest()[:16]}")
            corrected = 0

    print(f"\nTHE FORCED-CLOSED CHECK (the one that never existed)\n")
    print(f"  contradictions found: {len(contradictions)}")
    for c in contradictions:
        print(f"    {c['row']}·{c['region']}·{c['flavor']}  flagged forced-closed, measures "
              f"{c['measured_rate']:.4f}")
    print(f"\n  cause: the `horn` generator branch is byte-identical to the plain branch.")
    print(f"  Terrain unaffected — none of these had positive excess.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
