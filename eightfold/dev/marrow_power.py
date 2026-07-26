#!/usr/bin/env python3
"""Marrow v1 M0b — the Terroir-C power record. Computed from the ACTUAL census, printed before any verdict.

WHY THIS IS A SEPARATE GATE FROM KILL 1, stated because the separation is the point:
  Kill 1 asks "is there a POPULATION?" (>= 40 presentable rows).
  M0b asks   "can the test that JUSTIFIES the build SEE anything on it?"
Those are different questions and they can disagree. At the planning estimate they did: 82 rows would have
cleared Kill 1 comfortably while the minimum detectable effect sat at +0.10 against measured residuals of
+0.0000 and +0.0188. Supply is not viability. This is the coverage-vs-usability split (Anatomy-SCHEMA
§3.3b) applied PROSPECTIVELY for once, instead of discovered at scoring time.

WHAT TERROIR-C INHERITS (prereg_v14, unchanged): the admissibility screen n >= 30 AND modal < 0.90 per
family, the fold key `problem_family`, and the rule that a family failing the screen is DECLARED
INSUFFICIENT and never argued past.

THE SENTENCE THIS EXISTS TO SEAL: this instrument sees +X and up; below that it reports INSUFFICIENT, and
INSUFFICIENT IS NOT EVIDENCE OF ABSENCE. Written before a single presentation is pinned.
"""
import json
import sys
from collections import Counter
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "dev"))
from eightfold import atlas as A                                     # noqa: E402
import quarry_v3_spec as V3                                          # noqa: E402

AT = ROOT / "eightfold" / "results" / "atlas"
OUT = AT / "marrow-terroir-c-power.json"
SPEC = V3.V3_SPEC
MIN_N, MAX_MODAL, ALPHA = 30, 0.90, 0.05          # inherited from prereg_v14, not re-chosen here

# what Terroir actually measured, for scale
TERROIR = {"headline_lift": 0.0685, "within_family_residual": 0.0000, "within_coverage_residual": 0.0188}


def tail(k, n, p):
    return sum(comb(n, j) * p ** j * (1 - p) ** (n - j) for j in range(k, n + 1))


def mde(n, k_modal):
    """Smallest lift a one-sided exact binomial at ALPHA can distinguish from the modal null."""
    if n == 0:
        return None
    p0 = k_modal / n
    crit = next((k for k in range(n + 1) if tail(k, n, p0) <= ALPHA), None)
    return None if crit is None else round(crit / n - p0, 4)


def main() -> int:
    census = {r["problem_id"]: r for r in
              (json.loads(l) for l in (AT / "marrow-i0-census.jsonl").read_text().splitlines() if l.strip())}
    summ = json.loads((AT / "marrow-i0-census.json").read_text())
    varying = set(summ["THE_FIXED_TEMPLATE_AMBIGUITY"]["varying_template_rows"])

    v3 = {e.problem_id: e for e in A.load_atlas(str(AT / "atlas_v3.jsonl"))}
    real = SPEC.charge_real_values["decision"]

    def population(reading):
        rows = [p for p, r in census.items()
                if r["stratum"] in ("direct-csp", "vcsp-shaped") and p in v3
                and _cv(v3[p]) in real]
        if reading == "principled":
            rows = [p for p in rows if p not in varying]
        return sorted(rows)

    def _cv(e):
        for c in e.charges:
            if c.charge == "decision":
                return c.value
        return "n.a."

    out = {"schema": "marrow-terroir-c-power/v1", "prereg": "prereg_v15", "milestone": "M0b",
           "screen_inherited_from": "prereg_v14 (n>=30 AND modal<0.90); not re-chosen here",
           "why_separate_from_kill_1": ("Kill 1 asks whether a POPULATION exists; this asks whether the "
                                        "test that justifies the build can SEE anything on it. Supply is "
                                        "not viability."),
           "terroir_measured_for_scale": TERROIR, "readings": {}}

    print("MARROW v1 — M0b: TERROIR-C POWER RECORD  (computed from the census, before any verdict)\n")
    for reading in ("principled", "as_censused"):
        rows = population(reading)
        fams = Counter(v3[p].problem_family for p in rows)
        per, admissible = {}, []
        for f, n in sorted(fams.items(), key=lambda kv: -kv[1]):
            labels = Counter(_cv(v3[p]) for p in rows if v3[p].problem_family == f)
            lbl, k = labels.most_common(1)[0]
            ok = n >= MIN_N and k / n < MAX_MODAL
            per[f] = {"n": n, "modal_label": lbl, "modal_correct": k,
                      "modal_share": round(k / n, 4), "admissible": ok,
                      "status": ("ADMISSIBLE" if ok else
                                 f"INSUFFICIENT — n < {MIN_N}" if n < MIN_N else
                                 f"INSUFFICIENT — modal {k / n:.0%} >= {MAX_MODAL:.0%}")}
            if ok:
                admissible.append(f)
        N = sum(per[f]["n"] for f in admissible)
        M = sum(per[f]["modal_correct"] for f in admissible)
        pooled_all_n = sum(v["n"] for v in per.values())
        pooled_all_m = sum(v["modal_correct"] for v in per.values())

        rec = {"n_rows": len(rows), "n_admissible_families": len(admissible),
               "admissible_families": admissible, "per_family": per,
               "mde_single_family": (mde(per[admissible[0]]["n"], per[admissible[0]]["modal_correct"])
                                     if admissible else None),
               "mde_pooled_admissible_only": mde(N, M) if N else None,
               "mde_pooled_all_families_ignoring_screen": mde(pooled_all_n, pooled_all_m),
               "verdict": ("CANNOT RUN — zero admissible families under the inherited screen"
                           if not admissible else "RUNNABLE on the admissible set")}
        out["readings"][reading] = rec

        print(f"--- reading: {reading.upper()}  ({len(rows)} decision-real presentable rows)")
        for f, v in per.items():
            print(f"      {f:<18}n={v['n']:<4} modal={v['modal_share']:.3f}  {v['status']}")
        print(f"    admissible families: {len(admissible)} {admissible}")
        if admissible:
            print(f"    MDE (pooled admissible) : {rec['mde_pooled_admissible_only']:+.4f}")
        print(f"    MDE (all families, screen ignored — NOT the sealed statistic): "
              f"{rec['mde_pooled_all_families_ignoring_screen']:+.4f}")
        print(f"    => {rec['verdict']}\n")

    p = out["readings"]["principled"]
    out["SEALED_SENTENCE"] = (
        "Terroir-C on the principled census population has "
        f"{p['n_admissible_families']} admissible families under the screen inherited from prereg_v14. "
        + ("It CANNOT RUN as a within-family residual test: every family falls below n=30, so the "
           "statistic A4 defined has no admissible stratum to be computed on. Declared INSUFFICIENT IN "
           "ADVANCE — and INSUFFICIENT IS NOT EVIDENCE OF ABSENCE."
           if p["n_admissible_families"] == 0 else
           f"Its minimum detectable lift is {p['mde_pooled_admissible_only']:+.4f}; below that it reports "
           "INSUFFICIENT, and INSUFFICIENT IS NOT EVIDENCE OF ABSENCE."))
    out["scale_note"] = (
        "for comparison, the effect Terroir-C would be looking for: Arm B's headline lift was +0.0685 and "
        "its within-family residual was exactly +0.0000. A within-family residual is by construction "
        "smaller than the headline it decomposes.")
    out["extremal_acknowledged"] = [
        {"stat": "terroir_measured_for_scale.within_family_residual", "value": 0.0,
         "why_the_exactness_is_expected": (
             "not measured here — QUOTED from Terroir's A4, where it is already discharged by its own "
             "integer identity (+6 -7 +1 = 0 across the three admissible families). Carried in this "
             "artifact only to give the MDE a scale to be compared against.")},
    ] + [
        {"stat": f"readings.{r}.per_family.{f}.modal_share", "value": 1.0,
         "why_the_exactness_is_expected": (
             f"the `{f}` family has n={out['readings'][r]['per_family'][f]['n']} presentable rows and all "
             f"of them carry the same decision label, so its in-sample modal share is 1.0 by arithmetic. "
             f"THIS IS WHY THE FAMILY IS DECLARED INSUFFICIENT rather than scored — the modal<0.90 screen "
             f"exists to catch exactly this degeneracy.")}
        for r in out["readings"] for f, v in out["readings"][r]["per_family"].items()
        if v["modal_share"] == 1.0]
    OUT.write_text(json.dumps(out, indent=1) + "\n")
    print("SEALED SENTENCE:\n  " + out["SEALED_SENTENCE"])
    print(f"\nwrote {OUT.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
