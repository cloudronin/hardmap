"""Terroir v1 (prereg_v14) repro claims — the attribution of Arm B's `decision` lift.

These pin the DECOMPOSITION, not the headline. Arm B's +0.0684 belongs to mosaic claims and is untouched.
"""
import json
from pathlib import Path

_AT = Path(__file__).resolve().parents[3] / "eightfold" / "eightfold" / "results" / "atlas"


def _load(name: str) -> dict:
    return json.loads((_AT / name).read_text(encoding="utf-8"))


def within_family_residual() -> dict:
    """A4: the verdict. Pinned to INTEGER COUNTS, because the +-0 is a difference of two small integers
    and a rounded float would let it drift without anyone noticing."""
    d = _load("terroir_v1_results.json")["A4_within_family_residual"]
    pool, pf = d["pooled_admissible_only"], d["per_family"]
    return {"n_admissible_families": d["screen"]["n_admissible_families"],
            "n_insufficient_families": d["screen"]["n_insufficient_families"],
            "pooled_n": pool["n"], "modal_correct": pool["modal_correct"],
            "model_correct": pool["model_correct"],
            "within_family_lift": pool["within_family_lift"],
            "logic_proof_delta": pf["logic-proof"]["delta"],
            "logic_proof_p": pf["logic-proof"]["exact_binomial_p"],
            "verdict": d["verdict"]}


def sociology_is_a_recruitment_artifact() -> dict:
    """A3's retirement record: admission_wave is a label proxy because the corpus was built
    charge-stratified. The two 100%-pure waves are the exhibit."""
    d = _load("terroir_v1_results.json")["A3_retirement_record"]
    w = d["reason_2_THE_DISQUALIFIER"]
    return {"sociology_n": d["reason_1_different_population"]["decision_fit_intersect_sociology_n"],
            "headline_n": d["reason_1_different_population"]["decision_fit_n"],
            "admission_wave_lift": w["admission_wave_alone"]["lift"],
            "W3_purity": w["admission_wave_x_decision"]["W3"]["purity"],
            "W4_purity": w["admission_wave_x_decision"]["W4"]["purity"]}


def ablation_scoring() -> dict:
    """A1 + A2, scored against the seal INCLUDING THE MISS. The baseline must reproduce the sealed Arm B
    accuracy exactly or every delta below is meaningless."""
    d = _load("terroir_v1_ablations.json")
    r, s = d["runs"], d["sealed_prediction_scoring"]
    return {"baseline_acc": r["baseline"]["acc"], "baseline_null": r["baseline"]["null"],
            "a1_lift": r["A1_encoding_ablation"]["lift"],
            "a1_verdict": s["A1_encoding_ablation"]["verdict"],
            "a2_secondary_lift": (r["A2_secondary_coverage_stratified"]["pooled_admissible_only"]
                                  ["within_coverage_lift"]),
            "a2_secondary_n": r["A2_secondary_coverage_stratified"]["pooled_admissible_only"]["n"],
            "n_starved_under_imputation": len(r["A2_indicator_free"]["starved_under_imputation"])}


# ── Marrow v1 ─────────────────────────────────────────────────────────────────────────────────────────

def marrow_census() -> dict:
    """I0: the natural atlas is presentation-poor at closure grade. Kill 1 fires on the principled read."""
    d = _load("marrow-i0-census.json")
    return {"n_rows": d["n_rows"],
            "principled": d["readings"]["PRINCIPLED — fixed template required, omissions corrected"]["n"],
            "as_censused": d["readings"]["AS-CENSUSED — CSP-shaped, template-fixedness not applied"]["n"],
            "kill_1": d["kill_1"]["verdict"],
            "direct_csp": d["by_stratum"]["direct-csp"],
            "vcsp_shaped": d["by_stratum"]["vcsp-shaped"]}


def marrow_build() -> dict:
    """M1 corrected the census downward; M2's anchors gated; M4 froze v2 without moving v1."""
    p = _load("marrow-presentations.json")
    d = _load("marrow-derived.json")
    f = _load("anatomy_v2_freeze.json")
    return {"pinned": p["n_pinned"], "census_principled": p["census_principled_count"],
            "anchors_pass": d["kill_2_anchors"]["all_pass"], "n_anchors": d["kill_2_anchors"]["n"],
            "v1_sha_unmoved": f["version_class"]["v1_untouched"]["sha256_16"],
            "admissible_v2_columns": f["admissible_for_a_sealed_bet"]}


def marrow_audit() -> dict:
    """The presentation audit: posable only where the oracle matches the objective."""
    d = _load("marrow-presentation-audit.json")
    return {"pinned": d["scope"]["pinned_rows"], "posable": d["scope"]["posable"],
            "not_posable": d["scope"]["not_posable"],
            "agree": d["result"]["agree"], "disagree": d["result"]["disagree"],
            "errata_candidates": len(d["the_one_candidate"])}
