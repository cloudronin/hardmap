"""Mosaic v3 grid — the gates that must fail LOUDLY, not silently.

These lock the two rules that make the arms mean anything: the algebra is excluded from Arm A's features,
and prediction files stay outside the research agents' input surface for the prospective registry.
"""
import json
import pathlib
import sys

import pytest

FOUNDRY = pathlib.Path(__file__).resolve().parent.parent
LAT = FOUNDRY / "foundry" / "results" / "lattice"
ATLAS = FOUNDRY.parent / "eightfold" / "eightfold" / "results" / "atlas"
sys.path.insert(0, str(FOUNDRY.parent / "eightfold" / "dev"))

SURF = LAT / "grid_surface_features.json"
FOLDS = LAT / "grid_folds_and_strata.json"
skip_no_surf = pytest.mark.skipif(not SURF.exists(), reason="surface features not built (G1)")


@skip_no_surf
def test_no_algebra_leaks_into_arm_a_features():
    """THE load-bearing gate. Arm A asks whether the algebra is recoverable from surface combinatorics;
    if a Post flag or a flag-derivative is in the feature matrix, the question is not being asked."""
    doc = json.loads(SURF.read_text())
    banned = set(doc["excluded_algebra"]) | set(doc["excluded_derived"])
    for name in doc["feature_names"]:
        assert name not in banned, f"EXCLUDED feature {name!r} present in Arm A's matrix"
    for row in doc["rows"][:200]:
        assert not (set(row["features"]) & banned), f"{row['row_key']}: excluded feature present"


@skip_no_surf
def test_weight_histogram_omits_the_0valid_and_1valid_bins():
    """w0 and w{arity} ARE 0valid/1valid. A naive weight histogram hands back 2 of the 10 flags."""
    doc = json.loads(SURF.read_text())
    assert "w0" not in doc["feature_names"], "w0 is the 0-valid flag in disguise"
    assert "w4" not in doc["feature_names"], "w{arity} is the 1-valid flag in disguise"


@skip_no_surf
def test_starved_features_are_flagged_not_silently_shipped():
    doc = json.loads(SURF.read_text())
    assert doc["starved_features"], "census found nothing starved — suspicious, verify the census ran"
    for k in doc["starved_features"]:
        assert doc["census"][k]["starved"] is True


@pytest.mark.skipif(not FOLDS.exists(), reason="folds not built (G1)")
def test_fold_key_is_the_46_fingerprint_groups_and_boundary_is_stratification_only():
    doc = json.loads(FOLDS.read_text())
    assert doc["fold_key"]["n_groups"] == 46
    assert "STRATIFICATION ONLY" in doc["boundary_distance"]["role"]
    assert doc["boundary_distance"]["starved"] is False


def test_prediction_files_are_outside_the_research_input_surface():
    """prereg_v12 G1 addendum rule 2: enforced BY CONSTRUCTION, not by convention."""
    import grid_registry as R
    bad = R.assert_research_surface_clean([
        ATLAS / "quarry-v2-fill-inventory.json", ATLAS / "quarry-v2-funnel-query.json"])
    assert bad == [], f"research inputs must not include prediction files: {bad}"
    leaked = R.assert_research_surface_clean([ATLAS / "grid-predictions" / "wave-1.json"])
    assert leaked, "the guard must FIRE when a prediction file reaches the research surface"


def test_registry_declares_insufficient_until_its_floor_is_cleared():
    """Tests the DURABLE invariant, not a transient state. The first version asserted
    'UNPINNED' in threshold_status and went red the moment the threshold was correctly pinned —
    it encoded a moment rather than a rule. What must always hold: no cell enters the scored n
    before a wave is sealed predict-then-fill, the floor is monotone once grading starts, and the
    21 pre-registry cells stay descriptive-only."""
    import grid_registry as R
    reg = R.load()
    ta = reg.get("threshold_arithmetic")
    if ta is not None:                                   # once pinned, the floor must be a real number
        assert isinstance(ta["FLOOR_scored"]["n"], int) and ta["FLOOR_scored"]["n"] > 0
        assert "MONOTONE" in ta["UPDATE_RULE"], "the floor must never be relaxable after grading"
    scored = [e for e in reg["entries"] if e.get("counts_in_scored_n")]
    assert scored == [], "no cell may enter the scored n before a wave is sealed predict-then-fill"
    pre = [e for e in reg["entries"] if e.get("temporal_class") == "clean-but-pre-registry"]
    assert len(pre) == 21 and all(e["counts_in_descriptive"] for e in pre)


# ── Terroir v1 (prereg_v14) ───────────────────────────────────────────────────────────────────────────

def _terroir(name):
    import json
    return json.loads((ATLAS / name).read_text(encoding="utf-8"))


def test_a4_within_family_decomposition_is_pinned_to_its_integer_counts():
    """A4 IS the verdict, so it is pinned to the counts that produce it rather than to a rounded float.
    The pooled +-0 is a difference of two small integers; if any of them moves, FAMILY-BORNE has to be
    re-argued rather than silently inherited."""
    d = _terroir("terroir_v1_results.json")["A4_within_family_residual"]
    pf = d["per_family"]
    for fam, modal, model, n in (("graph", 106, 112, 148), ("logic-proof", 17, 10, 49),
                                 ("optimization", 47, 48, 58)):
        assert pf[fam]["admissible"], f"{fam} must clear the n>=30 / modal<0.90 screen"
        assert (pf[fam]["n"], pf[fam]["modal_correct"], pf[fam]["model_correct"]) == (n, modal, model)
    pool = d["pooled_admissible_only"]
    assert pool["n"] == 255 and pool["modal_correct"] == pool["model_correct"] == 170
    assert pool["within_family_lift"] == 0.0
    assert d["verdict"] == "FAMILY-BORNE"
    # the anti-signal edge: logic-proof is significantly WORSE than its own modal
    assert pf["logic-proof"]["delta"] < 0 and pf["logic-proof"]["exact_binomial_p"] < 0.05


def test_a4_declares_insufficient_rather_than_arguing_past_the_power_floor():
    d = _terroir("terroir_v1_results.json")["A4_within_family_residual"]
    ins = [f for f, r in d["per_family"].items() if not r["admissible"]]
    assert len(ins) == 7, "seven families fail the screen and must each be declared, not pooled in"
    assert all("INSUFFICIENT" in d["per_family"][f]["status"] for f in ins)


def test_a4_asserts_the_seal_and_the_fold_warrant():
    """A4 is arithmetic on FROZEN predictions. If the prediction file ever moves, or the fold key stops
    being problem_family, the analysis is not the one that was reported."""
    import subprocess, sys, os
    d = _terroir("terroir_v1_results.json")["A4_within_family_residual"]
    assert d["predictions_sha256_asserted"] == "cc5bb3895a44a043"
    assert "problem_family" in d["fold_key_warrant"]
    env = dict(os.environ, PYTHONPATH="eightfold:foundry:hardmap:proof-census:desert-map")
    r = subprocess.run([sys.executable, "eightfold/dev/terroir_a4.py"], capture_output=True,
                       cwd=str(ATLAS.parents[3]), env=env)
    assert r.returncode == 0, f"A4 re-run failed its own seal assertions:\n{r.stderr.decode()[-2000:]}"


def test_a2_strips_every_absence_marker_not_just_the_named_one():
    """THE LOAD-BEARING CHECK. Exclusion must be closed under the CONCEPT, not under the name: `open` is
    absence just as much as `__missing__` is, and -1.0 is an exact missingness test under a threshold
    split. A2 that stripped only `__missing__` would still be reading coverage."""
    import sys
    sys.path.insert(0, "eightfold/dev"); sys.path.insert(0, "foundry/dev")
    import terroir_ablate as T
    from eightfold.anatomy import COVERAGE_ABSENCE_MARKERS
    assert set(COVERAGE_ABSENCE_MARKERS) == {"__missing__", "open", -1.0}
    v3, an, pids, fam, folds = T.load()
    enc, levels = T.make_encoder(an, pids, T.FEATS, impute_folds=True, folds=folds)
    for f, lv in levels.items():
        assert not (set(lv) & T.ABSENCE_STRINGS), f"{f} still carries an absence level: {lv}"
    import numpy as np
    X = np.array([enc(p, 0) for p in pids], dtype=float)
    assert not (X == T.ABSENCE_NUMERIC).any(), "the -1.0 sentinel survived into A2's matrix"


def test_a2_imputation_is_fold_local():
    """A global modal would let a test row inform its own imputation. The fill value must depend only on
    the TRAIN fold — so the encoding of the same row must be allowed to differ across folds."""
    import sys
    sys.path.insert(0, "eightfold/dev"); sys.path.insert(0, "foundry/dev")
    import terroir_ablate as T
    import numpy as np
    v3, an, pids, fam, folds = T.load()
    enc, _ = T.make_encoder(an, pids, T.FEATS, impute_folds=True, folds=folds)
    mats = [np.array([enc(p, f) for p in pids], dtype=float) for f in range(T.NFOLD)]
    assert any(not np.array_equal(mats[0], m) for m in mats[1:]), \
        "A2's encoding is identical across folds — the imputation is not fold-local"


def test_terroir_reports_its_miss():
    """A1's sealed prediction FAILED. The artifact must say so; a seal that only records its hits is a
    press release."""
    s = _terroir("terroir_v1_ablations.json")["sealed_prediction_scoring"]
    assert s["A1_encoding_ablation"]["verdict"] == "MISS"
    assert s["A1_encoding_ablation"]["observed"] > 0.0342
    assert "specification_weakness_declared" in s["A2_indicator_free_primary"]


def test_ablations_reproduce_the_sealed_baseline_exactly():
    """Every delta is measured against a matched re-run. If the baseline stops reproducing the sealed
    accuracy, the deltas mean nothing and the run must fail rather than report them."""
    b = _terroir("terroir_v1_ablations.json")["runs"]["baseline"]
    assert b["acc"] == 0.6607 and b["null"] == 0.5923
    assert b["reproduces_sealed"]["lift_as_sealed"] == 0.0684


def test_denominator_gate_catches_a_mismatched_lift():
    """The gate promoted at T4 after three instances. It must FIRE on a planted mismatch, not merely
    pass on clean files — a check that has never been seen to fail is not known to work."""
    import json, tempfile, pathlib
    from hardmap import verify
    assert verify.check_lift_denominators_match() == []
    bad = {"block": {"n": 100, "acc": 0.90, "null": 0.50, "lift": 0.10}}   # 0.90-0.50 != 0.10
    p = ATLAS / "_tmp_denominator_probe_results.json"
    try:
        p.write_text(json.dumps(bad), encoding="utf-8")
        out = verify.check_lift_denominators_match()
        assert any("_tmp_denominator_probe" in m for m in out), "the denominator gate failed to fire"
    finally:
        p.unlink(missing_ok=True)


# ── Marrow v1 M0 (prereg_v15) ─────────────────────────────────────────────────────────────────────────

def _marrow(name):
    import json
    return json.loads((ATLAS / name).read_text(encoding="utf-8"))


def test_census_covers_every_natural_row_exactly_once():
    """345 rows, one stratum each, and every non-presentable row carries a REASON — the typing law."""
    import json
    rows = [json.loads(l) for l in (ATLAS / "marrow-i0-census.jsonl").read_text().splitlines() if l.strip()]
    assert len(rows) == 345
    assert len({r["problem_id"] for r in rows}) == 345
    for r in rows:
        assert r["stratum"] in ("direct-csp", "vcsp-shaped", "promise", "no-presentation")
        if r["stratum"] == "no-presentation":
            assert r["presentation"] == "n.a." and r.get("reason"), f"{r['problem_id']} lacks a reason"
        else:
            assert r.get("source_hint"), f"{r['problem_id']} lacks a source hint for M1"


def test_kill_1_fired_and_the_band_is_recorded():
    """The verdict is not robust to the admission reading, so the BAND must be in the artifact — a single
    reading reported alone would hide that a different one clears the floor."""
    d = _marrow("marrow-i0-census.json")
    assert d["kill_1"]["verdict"] == "FIRES"
    readings = d["readings"]
    assert len(readings) >= 3, "the band must be recorded, not just the chosen reading"
    verdicts = {r["kill_1"] for r in readings.values()}
    assert verdicts == {"FIRES", "CLEARS"}, "the band should show the verdict actually flipping"
    rec = [k for k, v in readings.items() if v.get("recommended")]
    assert len(rec) == 1 and readings[rec[0]]["kill_1"] == "FIRES", \
        "the recommended reading is the one that FIRES — recording that the clearing reading was available"


def test_terroir_c_cannot_run_under_either_reading():
    """The viability verdict must be ROBUST to the admission ambiguity, unlike Kill 1. If this ever passes
    under one reading and fails under another, the seal's headline is reading-dependent and must say so."""
    d = _marrow("marrow-terroir-c-power.json")
    for reading, rec in d["readings"].items():
        assert rec["n_admissible_families"] == 0, f"{reading} unexpectedly has an admissible family"
        assert "CANNOT RUN" in rec["verdict"]
    assert "INSUFFICIENT IS NOT EVIDENCE OF ABSENCE" in d["SEALED_SENTENCE"]


def test_stratum_2_is_constant_on_decision():
    """The owner-ruled artifact-level variance flag. If a resumption ever draws a `decision` bet from the
    vcsp-shaped stratum alone it would be scoring a constant, and this asserts the flag stays true."""
    import json, sys
    sys.path.insert(0, "eightfold"); sys.path.insert(0, "eightfold/dev")
    from collections import Counter
    from eightfold import atlas as A
    import quarry_v3_spec as V3
    v3 = {e.problem_id: e for e in A.load_atlas(str(ATLAS / "atlas_v3.jsonl"))}
    rows = [json.loads(l) for l in (ATLAS / "marrow-i0-census.jsonl").read_text().splitlines() if l.strip()]
    real = V3.V3_SPEC.charge_real_values["decision"]

    def cv(e):
        return next((c.value for c in e.charges if c.charge == "decision"), "n.a.")
    s2 = [r["problem_id"] for r in rows if r["stratum"] == "vcsp-shaped" and cv(v3[r["problem_id"]]) in real]
    labels = Counter(cv(v3[p]) for p in s2)
    assert len(labels) == 1, f"stratum 2 is no longer constant: {dict(labels)} — the sealed flag is stale"


def test_tidy_number_watch_set_is_declared_not_globbed_per_project():
    """The defect this asserts against appeared TWICE: the gate's file pattern was scoped to whatever the
    last project named its files, so the next project's artifacts were silently unwatched and the gate
    failed OPEN. The watched set must be a declared tuple, and it must actually cover this project."""
    from hardmap import verify
    watched = {p.name for p in verify._watched(ATLAS)}
    for required in ("terroir_v1_results.json", "terroir_v1_ablations.json",
                     "marrow-i0-census.json", "marrow-terroir-c-power.json"):
        assert required in watched, f"{required} is not watched by the numeric gates"


# ── Marrow v1 M1–M4 (Anatomy v2) ──────────────────────────────────────────────────────────────────────

def test_anatomy_v1_is_untouched_by_v2():
    """THE PROOF OF NON-EDIT. v2 is a new sealed version, not an additive v1.1, so v1's bytes and v1's
    registry must both be exactly what they were. v1's OWN tests passing unchanged is the other half of
    this evidence and lives in eightfold/tests/test_anatomy.py."""
    import hashlib, sys
    sys.path.insert(0, "eightfold")
    from eightfold import anatomy as AN
    assert hashlib.sha256((ATLAS / "anatomy_v1.jsonl").read_bytes()).hexdigest()[:16] == "8ff11f8a33bbdce7"
    assert len(AN.COLUMNS) == 11, "v2 leaked into v1's registry"
    assert not (set(AN.V2_COLUMNS) & set(AN.COLUMNS)), "a v2 column shadows a v1 column"


def test_v2_passports_are_not_invariant():
    """The arity_class lesson applied BEFORE the failure. The Marrow spec expected `invariant` on all
    shipped columns; a fingerprint computed from a HUMAN-PINNED presentation cannot earn it."""
    import sys
    sys.path.insert(0, "eightfold")
    from eightfold import anatomy as AN
    assert AN.V2_PASSPORT_INVARIANCE["presentation"][0] == AN.ENCODING_RELATIVE
    for c in ("poly_fingerprint_natural", "engine_type_natural"):
        assert AN.V2_PASSPORT_INVARIANCE[c][0] == AN.PARAMETER_RELATIVE
        assert "PINNED" in AN.V2_PASSPORT_INVARIANCE[c][1].upper() or \
               "inherits" in AN.V2_PASSPORT_INVARIANCE[c][1]


def test_boolean_only_flags_are_na_on_non_boolean_rows():
    """Boolean BY THEOREM — KSTW/Marx do not transfer to |D|>2. This boundary must not erode silently."""
    import json, sys
    sys.path.insert(0, "eightfold")
    from eightfold import anatomy as AN
    rows = [json.loads(l) for l in (ATLAS / "marrow-derived.jsonl").read_text().splitlines() if l.strip()]
    nonbool = [r for r in rows if r.get("domain_size") not in (2, None)]
    assert nonbool, "no non-Boolean rows — the guard would be vacuous"
    for r in nonbool:
        fp = r["poly_fingerprint_natural"]
        for flag in AN.V2_BOOLEAN_ONLY_FLAGS:
            assert fp.get(flag) == "n.a.", f"{r['problem_id']}: {flag} must be n.a. at |D|>2, got {fp.get(flag)}"


def test_kill_2_anchors_gate_the_derivation():
    """Kill 2: anchors run FIRST and govern. A miss sends that domain to `open`, never to an approximation.
    Re-runs the script so the assertion is on live behaviour, not on a recorded claim."""
    import json, subprocess, sys, os
    d = json.loads((ATLAS / "marrow-derived.json").read_text())
    assert d["kill_2_anchors"]["all_pass"] and d["kill_2_anchors"]["n"] >= 7
    env = dict(os.environ, PYTHONPATH="eightfold:foundry:hardmap:proof-census:desert-map")
    r = subprocess.run([sys.executable, "eightfold/dev/marrow_derive.py"], capture_output=True,
                       cwd=str(ATLAS.parents[3]), env=env)
    assert r.returncode == 0, f"derivation failed its own anchors:\n{r.stderr.decode()[-1500:]}"


def test_starvation_gate_catches_over_dispersion_not_just_over_concentration():
    """The gate was one-sided for eleven columns: it starved a column whose modal value SWAMPED the
    population and said nothing about one with as many levels as rows. `presentation` has 28 distinct
    values on 28 rows and must read STARVED."""
    import json
    p = json.loads((ATLAS / "anatomy_v2_passports.json").read_text())["columns"]
    var = p["presentation"]["variance"]
    assert var["starved"] is True, "an all-singleton column must starve"
    assert "OVER-DISPERSED" in var["starved_note"]
    assert p["presentation"]["admissible_for_a_sealed_bet"] is False
    # and the gate must still catch the original direction
    assert p["engine_type_natural"]["variance"]["starved"] is False


def test_presentation_audit_is_posable_only_where_the_oracle_matches_the_objective():
    """Schaefer answers 'is CSP(Gamma) satisfiable in P'. For Min-Ones/Max-Ones that is the wrong question
    — CSP({OR2}) is trivially satisfiable while Min-Ones({OR2}) IS vertex cover. The vcsp rows must be
    declared NOT-POSABLE rather than scored as disagreements."""
    import json
    d = json.loads((ATLAS / "marrow-presentation-audit.json").read_text())
    assert d["scope"]["posable"] + d["scope"]["not_posable"] == d["scope"]["pinned_rows"]
    npos = [r for r in d["rows"] if r["verdict"] == "NOT-POSABLE"]
    assert npos and all(r["stratum"] == "vcsp-shaped" for r in npos)
    assert d["result"]["agree"] + d["result"]["disagree"] == d["scope"]["posable"]


# ── W2: the write-up number audit ─────────────────────────────────────────────────────────────────────

def _run_audit():
    import subprocess, sys, os
    env = dict(os.environ, PYTHONPATH="eightfold:foundry:hardmap:proof-census:desert-map")
    return subprocess.run([sys.executable, "eightfold/dev/audit_writeup.py"],
                          capture_output=True, env=env, text=True, cwd=str(ATLAS.parents[3]))


def test_writeup_number_audit_passes():
    """W2 gate: every numeral in the draft resolves to a value extracted live from an artifact.
    An orphan is a halt, not a footnote."""
    r = _run_audit()
    assert r.returncode == 0, f"W2 FAILS — orphan numerals in the draft:\n{r.stdout[-2000:]}"


def test_writeup_number_audit_actually_fires():
    """THE GATE MUST BE ABLE TO FAIL. The audit went from 17 orphans to 0 after its matching was
    loosened (headings exempted, prose artifacts scanned, rounding allowed) — which is the exact shape
    of narrowing a gate until it goes green. So: plant fabricated numerals of several shapes, including
    one sitting right beside a real value, and assert each is caught."""
    from pathlib import Path
    d = ATLAS.parents[3] / "eightfold" / "docs" / "paper" / "hardmap-program-v1.md"
    orig = d.read_text(encoding="utf-8")
    probes = ["The coupling reads **0.61** on the invented population.",
              "The model recovers **+0.0417** on the invented set.",
              "The census covers **7431** invented records.",
              "The lookup scores **88.12%** on the invented holdout.",
              "Jaccard spans **0.044 to 0.199** across all cells.",
              # THE ONE THAT SLIPPED: with a 500-value registry, a fabricated 2-decimal figure found a
              # genuine unrelated 0.6065 rounding to it. Rounding now counts only at >=3 decimals, so a
              # 2-decimal figure must appear literally in an artifact. This probe pins that fix.
              "The coupling reads **0.61** on the invented population, near a real 0.6065."]
    try:
        for line in probes:
            d.write_text(orig + "\n\n" + line + "\n", encoding="utf-8")
            r = _run_audit()
            assert r.returncode != 0, f"the audit did NOT fire on a fabricated numeral: {line}"
    finally:
        d.write_text(orig, encoding="utf-8")
    assert d.read_text(encoding="utf-8") == orig, "probe did not restore the draft"


# ── Geometry Probe A (prereg_v16) ─────────────────────────────────────────────────────────────────────

def _probe():
    import json
    from pathlib import Path
    import foundry
    p = Path(foundry.__file__).resolve().parent / "results" / "lattice" / "geometry_probe_a_results.json"
    return json.loads(p.read_text(encoding="utf-8"))


def test_probe_battery_is_exact_on_every_roster_class():
    """Score 1. Exhaustively computed, rate==0 IS the oracle flag by definition — so any disagreement is a
    probe bug, not noise. Pinned at zero."""
    d = _probe()
    for fl, v in d["score_1_known_answer_battery"]["result"].items():
        assert v["disagree"] == 0, f"{fl}: {v['disagree']} classes disagree with the oracle"
        assert v["agree"] == d["n_classes"]


def test_probe_forced_arms_are_labelled_forced():
    """The battery and specificity are theorem-forced. They must SAY so in the artifact — an unlabelled
    forced score is the theorem-forced-credit trap (methods 21) in an instrument's costume."""
    d = _probe()
    assert "FORCED" in d["score_1_known_answer_battery"]["status"].upper()
    assert d["score_2_sampled_sensitivity"]["specificity"]["value"] == 1.0
    assert "FORCED" in d["score_2_sampled_sensitivity"]["specificity"]["status"].upper()


def test_probe_sensitivity_has_live_dynamic_range():
    """The qualification is only meaningful if the measurement can move. Sensitivity at the smallest budget
    must be strictly below the largest — a statistic saturated at every budget would be measuring nothing."""
    d = _probe()
    b = [str(x) for x in d["budgets"]]
    for fl, v in d["score_2_sampled_sensitivity"]["result"].items():
        lo, hi = v[b[0]]["sensitivity"], v[b[-1]]["sensitivity"]
        assert lo < hi, f"{fl}: sensitivity flat at {lo} across all budgets"
        assert hi >= 0.99, f"{fl}: sensitivity only {hi} at the largest budget"


def test_probe_distribution_is_not_bimodal():
    """Score 3, the pre-registered question. Pinned because the answer is the finding: the middle band holds
    the overwhelming majority of nonzero rates, so the dichotomy's binary is carving a continuum."""
    d = _probe()
    for fl, v in d["score_3_distribution_shape"]["result"].items():
        assert v["middle_band_fraction_of_nonzero"] > 0.80, \
            f"{fl}: middle band holds only {v['middle_band_fraction_of_nonzero']} of nonzero rates"
    maj = d["score_3_distribution_shape"]["result"]["majority"]["histogram"]
    assert maj["050_to_075"] == 0 and maj["075_to_1"] == 0, \
        "majority violations above 0.50 would contradict the reported shape"


def test_min_max_distributions_match_by_complement_symmetry():
    """A free consistency check: the roster is closed under complementation, which exchanges horn and
    dual-horn, so min and max must have IDENTICAL distributions. If they ever diverge, the roster or the
    operation pair has changed underneath."""
    d = _probe()["score_3_distribution_shape"]["result"]
    assert d["min"]["histogram"] == d["max"]["histogram"]
    assert d["min"]["mean_nonzero"] == d["max"]["mean_nonzero"]


def test_tidy_number_gate_actually_watches_the_lattice_directory():
    """THE DEFECT THIS PINS. The gate's lattice path was one `.parent` short and resolved to a directory
    that never existed; `if lat.exists()` then made the miss silent, so every Foundry lattice artifact went
    uninspected — including the 1.000 the write-up quotes. A gate that cannot tell 'inspected and clean'
    from 'never looked' is not a gate."""
    from pathlib import Path
    import foundry
    from hardmap import verify as V
    lat = Path(foundry.__file__).resolve().parent / "results" / "lattice"
    assert lat.exists(), "the real lattice directory moved"
    watched = {p.name for p in V._watched(lat)}
    assert "geometry_probe_a_results.json" in watched
    assert "grid_arm_a_results.json" in watched


def test_meta_gate_fails_when_a_gate_inspected_nothing():
    """THE META-GATE, probe-tested. It exists because one gate silently watched nothing in three distinct
    ways, all of which FAIL OPEN. Verification that verified nothing must say so — so an empty scope must
    be a build failure, not a green light."""
    import tempfile
    from pathlib import Path
    from hardmap import verify as V
    orig = V._numeric_gate_roots
    try:
        with tempfile.TemporaryDirectory() as td:
            V._numeric_gate_roots = lambda: orig() + [Path(td)]
            assert V.check_gates_inspected_something(), "a root with zero artifacts did not fail the gate"
        V._numeric_gate_roots = lambda: []
        assert V.check_gates_inspected_something(), "resolving zero roots did not fail the gate"
    finally:
        V._numeric_gate_roots = orig
    assert V.check_gates_inspected_something() == [], "live scope should be clean"


def test_arm_a_extremals_are_adjudicated_by_expression():
    """The three Arm A extremals, verdicted 2026-07-26. Pinned because BOTH first readings were wrong and
    the decisive evidence is one comparison: if the arithmetic leak had caused 1valid's 1.0000, dropping
    the leak moments would have moved it. It does not move."""
    import json
    from pathlib import Path
    import foundry
    lat = Path(foundry.__file__).resolve().parent / "results" / "lattice"
    pre = json.loads((lat / "grid_arm_a_results.json").read_text(encoding="utf-8"))
    clean = json.loads((lat / "grid_arm_a_results_clean.json").read_text(encoding="utf-8"))
    # 1valid is MEMBERSHIP: unchanged by dropping the leak moments, so the leak is not the mechanism
    assert pre["per_flag_recovery"]["1valid"]["acc"] == 1.0
    assert clean["per_flag_recovery"]["1valid"]["acc"] == 1.0
    assert clean["arithmetic_closure"]["clean_run"] is True
    assert set(clean["arithmetic_closure"]["dropped_moments"]) == {"weight_mean", "weight_spread"}
    # and it is a positive control: its null is low, so the recovery is real signal not a constant flag
    assert clean["per_flag_recovery"]["1valid"]["modal_null_foldweighted"] < 0.20


def test_assertion_5_states_its_exceptions():
    """The draft first claimed EVERY closure target fell at or below its null. Three do not. The source
    note always said so; the draft had dropped the qualification. Pinned so it cannot drop again."""
    from pathlib import Path
    import json, foundry
    lat = Path(foundry.__file__).resolve().parent / "results" / "lattice"
    clean = json.loads((lat / "grid_arm_a_results_clean.json").read_text(encoding="utf-8"))
    above = [f for f, v in clean["per_flag_recovery"].items()
             if f not in ("0valid", "1valid") and v["acc"] > v["modal_null_foldweighted"]]
    assert len(above) == 3, f"expected 3 nominal positives, got {above}"
    for f in above:
        assert clean["per_flag_recovery"][f]["modal_null_foldweighted"] >= 0.95, \
            f"{f} is above null on a null below 0.95 — the 'noise' reading would no longer hold"
    draft = (Path(__file__).parents[2] / "eightfold" / "docs" / "paper"
             / "hardmap-program-v1.md").read_text(encoding="utf-8")
    assert "nominally above" in draft, "the draft must state the exceptions, not absorb them"
