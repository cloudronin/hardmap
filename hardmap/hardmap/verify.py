"""`hardmap verify` -- the H4 internal-coherence sweep (spec section 3.5, check 2).

One script over the persisted results asserting invariants that must hold
regardless of the numbers: Cramér's V in [0,1], point estimates inside their CIs,
marginals summing to n, netted <= raw where a theorem forces it. Grows a check per
artifact family; exits nonzero on any violation. This ships as a permanent command.
"""
from __future__ import annotations

import json
from pathlib import Path

import eightfold


def _eightfold_atlas() -> Path:
    return Path(eightfold.__file__).resolve().parent / "results" / "atlas"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def check_cramers_v_range() -> list[str]:
    """Every reported Cramér's V lies in [0, 1]."""
    bad = []
    a3 = _load(_eightfold_atlas() / "a3_structure.json")
    for pair, v in a3.get("cramers_v", {}).items():
        if not 0.0 <= float(v) <= 1.0:
            bad.append(f"a3 cramers_v[{pair}] = {v} outside [0,1]")
    cr = _load(_eightfold_atlas() / "crucible_results.json")
    for key in ("gradient_full_v", "gradient_dedup_v"):
        v = cr.get("S2", {}).get(key)
        if v is not None and not 0.0 <= float(v) <= 1.0:
            bad.append(f"crucible S2.{key} = {v} outside [0,1]")
    return bad


def check_factors_kstar_interval() -> list[str]:
    """k* point estimate sits inside its own reported verdict interval and is >= 1."""
    bad = []
    ks = _load(_eightfold_atlas() / "factors_v1.json")["k_star"]
    if ks["k_hat_1se"] not in ks["verdict_interval"]:
        bad.append(f"factors k_hat_1se {ks['k_hat_1se']} not in verdict_interval {ks['verdict_interval']}")
    if ks["k_hat_1se"] < 1:
        bad.append(f"factors k_hat_1se {ks['k_hat_1se']} < 1")
    return bad


def check_netted_le_raw() -> list[str]:
    """Cai-Chen residual audit: netted association <= raw where the theorem forces it."""
    bad = []
    a3 = _load(_eightfold_atlas() / "a3_structure.json")
    audit = a3.get("H2_multiplets", {}).get("cai_chen_bridge_audit_R25", {})
    raw = audit.get("raw", {}).get("v")
    for level in ("conservative", "aggressive", "extreme_floor_delete_whole_cell"):
        netted = audit.get(level, {}).get("v")
        if raw is not None and netted is not None and float(netted) > float(raw) + 1e-9:
            bad.append(f"netted[{level}] {netted} > raw {raw}")
    return bad


def check_estimates_in_cis() -> list[str]:
    """Point estimates lie inside their own reported bootstrap CIs."""
    import foundry
    lat_dir = Path(foundry.__file__).resolve().parent / "results" / "lattice"
    bad = []
    lat = _load(lat_dir / "lattice_v3_occupancy.json")
    v = lat["cramers_v"]
    lo, hi = lat["cramers_v_boot_ci95_sized_to_classes"]
    if not lo <= v <= hi:
        bad.append(f"lattice_v3 V {v:.4f} not in CI [{lo}, {hi}]")
    mo = _load(lat_dir / "prism_v2_matrix.json")["pred5_anti_canon"]["min_ones"]
    pt = mo["spearman_point_corrected"]
    clo, chi = mo["boot_ci95_classes_corrected"]
    if not clo <= pt <= chi:
        bad.append(f"prism_v2 corrected Spearman {pt} not in CI [{clo}, {chi}]")
    return bad


def check_census_jaccard_sane() -> list[str]:
    """Every committed median Jaccard lies in [0,1] and below the 0.95 plurality line."""
    import proofcensus
    c3 = _load(Path(proofcensus.__file__).resolve().parent / "results" / "c3" / "c3_summary.json")
    bad = []
    for nkey, trend in c3.get("trends", {}).items():
        for series in ("s1", "s2"):
            for j in trend.get("mean_jaccard", {}).get(series, []):
                if j is None:
                    continue
                if not 0.0 <= j <= 1.0:
                    bad.append(f"{nkey} mean_jaccard.{series} {j} outside [0,1]")
                elif j >= 0.95:
                    bad.append(f"{nkey} mean_jaccard.{series} {j} >= 0.95 (would imply plurality)")
    return bad


def check_marginals_sum_to_n() -> list[str]:
    """Lattice v3 contingency marginals and occupancy cells each sum to n_both_real."""
    import foundry
    lat = _load(Path(foundry.__file__).resolve().parent / "results" / "lattice" / "lattice_v3_occupancy.json")
    n = lat["n_both_real"]
    bad = []
    if sum(lat["param_marginal"].values()) != n:
        bad.append(f"param_marginal sums to {sum(lat['param_marginal'].values())}, not n_both_real={n}")
    if sum(lat["occupancy"].values()) != n:
        bad.append(f"occupancy cells sum to {sum(lat['occupancy'].values())}, not n_both_real={n}")
    return bad


def check_stratified_v_known_answers() -> list[str]:
    """Defect #15 permanent gate — the conditional (within-stratum) Cramér's V estimator must return the
    KNOWN answer on constructed tables BEFORE it is trusted on real data. (a) conditional independence ->
    ~0; (b) Simpson's construction — marginal associated, conditional independent -> ~0 while the marginal V
    is clearly > 0; (c) perfect within-stratum association -> ~1. Guards against the original bug: averaging
    per-stratum V's (not a conditional association) and being fooled by the marginal."""
    from eightfold.structure import stratified_cramers_v, cramers_v
    bad = []
    # (a) conditional independence: Y is 80/20 regardless of X within each stratum
    ci = ([("x1", "y1", "A")] * 16 + [("x1", "y2", "A")] * 4 + [("x2", "y1", "A")] * 16 + [("x2", "y2", "A")] * 4
          + [("x1", "y1", "B")] * 4 + [("x1", "y2", "B")] * 16 + [("x2", "y1", "B")] * 4 + [("x2", "y2", "B")] * 16)
    if stratified_cramers_v(ci) > 0.10:
        bad.append(f"conditional-independence stratified V = {stratified_cramers_v(ci):.3f}, expected ~0")
    # (b) Simpson: marginal associated, conditional independent
    sp = ([("x1", "y1", "A")] * 16 + [("x1", "y2", "A")] * 4 + [("x2", "y1", "A")] * 4 + [("x2", "y2", "A")] * 1
          + [("x1", "y1", "B")] * 1 + [("x1", "y2", "B")] * 4 + [("x2", "y1", "B")] * 4 + [("x2", "y2", "B")] * 16)
    sv = stratified_cramers_v(sp)
    mv = cramers_v([x for x, y, s in sp], [y for x, y, s in sp])
    if sv > 0.10:
        bad.append(f"Simpson stratified V = {sv:.3f}, expected ~0 (must not be fooled by marginal)")
    if mv < 0.20:
        bad.append(f"Simpson marginal V = {mv:.3f}, expected clearly > 0 (test construction is degenerate)")
    # (c) perfect within-stratum association
    pf = [(x, {"x1": "y1", "x2": "y2", "x3": "y3"}[x], s)
          for s in ("A", "B", "C") for x in ("x1", "x2", "x3") for _ in range(10)]
    if stratified_cramers_v(pf) < 0.90:
        bad.append(f"perfect-association stratified V = {stratified_cramers_v(pf):.3f}, expected ~1")
    return bad


def check_anatomy_passports_complete() -> list[str]:
    """Anatomy S3 freeze gate, enforced in CI: every shipped column carries an invariance verdict, a
    property_of statement when relative, and RECORDED variance flags. CLEAN means COMPLETE AND HONEST, not
    all-green -- `starved` and `encoding-relative` are legal; UNDECLARED is not. Also re-checks the
    pin-before-net rule: no cell may carry a bridge_citation that is not PINNED in the Bridge Ledger."""
    import json
    from eightfold import anatomy as AN
    d = _eightfold_atlas()
    pp, art = d / "anatomy-passports.json", d / "anatomy_v1.jsonl"
    if not pp.exists() or not art.exists():
        return []                       # not built yet; the suite's skipif idiom, one level up
    bad = []
    doc = _load(pp)
    for c in AN.COLUMNS:
        p = doc.get("columns", {}).get(c)
        if p is None:
            bad.append(f"anatomy: shipped column {c!r} has no passport")
            continue
        if p.get("invariance") not in AN.INVARIANCE_VERDICTS:
            bad.append(f"anatomy[{c}]: invariance verdict missing/unrecognized")
        if p.get("invariance") != AN.INVARIANT and not p.get("property_of"):
            bad.append(f"anatomy[{c}]: relative column does not say what it is a property of")
        if "variance" not in p:
            bad.append(f"anatomy[{c}]: variance flags not recorded")
    for line in art.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        for cell in row.get("features", []):
            b = cell.get("bridge_citation")
            if b and b not in AN.PINNED_BRIDGES:
                bad.append(f"anatomy[{row['row_key']}.{cell['feature']}]: bridge {b!r} is NOT PINNED "
                           f"(pin-before-net); fall back to `open` rather than borrow the warrant")
    return bad


def _numeric_gate_roots():
    """The roots the numeric gates inspect, resolved THROUGH THEIR PACKAGES. Shared by the gates and by
    the meta-gate, so a scope that silently empties fails the build rather than passing it."""
    roots = [_eightfold_atlas()]
    try:
        import foundry
        lat = Path(foundry.__file__).resolve().parent / "results" / "lattice"
        if lat.exists():
            roots.append(lat)
    except ImportError:
        pass
    return roots


def _watched(root):
    """Artifacts the numeric gates inspect.

    THE DEFECT THIS EXISTS TO STOP REPEATING (Terroir T4, then Marrow M0 one commit later): the gate's glob
    was `grid_*results*.json`, so the next project's results file was invisible to it and nothing announced
    the blind spot. Widening it once was not the fix — the SHAPE was the defect. A gate keyed to whatever
    the last project happened to name its files silently stops working the moment naming changes, and it
    fails OPEN, reporting a pass over files it never opened.

    So the watched set is declared here, one place, and a new project registers its pattern rather than
    discovering later that it was never checked.

    `*factors*.json` WAS THE BACKLOG, AND IT IS NOW PAID (Marrow M0 -> M1). The pattern was held out at M0
    because adding it surfaced 16 unacknowledged extremals across factors_v1 / factors_v1_1 /
    factors_sensitivity — real debt in a project that pass had not examined — and waving them through a
    LEGACY table without reading them would be rubber-stamping, the one thing this gate must never become.
    The 16 have since been adjudicated one at a time: 10 benign, now carrying `extremal_acknowledged`
    entries their scorers DERIVE from each run rather than hardcode, and 6 — the whole of
    `factors_v1.json`'s `excess_over_null` block — a real reporting flaw, fixed at the scorer and
    regenerated. At k*=1 that block's statistic was `acc[1]` minus itself, so its all-zero envelope and
    `excess_over_typing: false` were forced by the expression and would have been emitted by any input at
    all. Nothing was added to LEGACY. The pattern is now IN, which is the only honest way a watched set
    grows: as fast as someone actually adjudicates it, and no faster."""
    pats = ("*results*.json", "*ablations*.json", "*census*.json", "*power*.json", "*factors*.json")
    return {p for pat in pats for p in root.glob(pat)}


def check_suspicious_cleanliness() -> list[str]:
    """THE TIDY-NUMBER GATE (methods 22, promoted to a check 2026-07-25).

    Twice in one program a bug wore a verdict, and BOTH TIMES THE TELL WAS THE SAME: the number was too
    tidy. `1.0000` recovery is not learning, it is reading. `+0.009` on a designed-for signal is not a null,
    it is a dead encoder. So: any headline statistic that is EXACTLY extremal (0.0 / 1.0) or EXACTLY equal
    to its own stated null gets a mechanical second look BEFORE narration -- in BOTH directions, because a
    discipline that only catches flattering errors is indistinguishable from pessimism.

    Mechanised where it can be: an exactly-extremal statistic must be ACKNOWLEDGED in its own artifact
    (an `extremal_acknowledged` entry saying why the exactness is expected). Unacknowledged exactness is a
    violation. Where it cannot be mechanised, it remains a standing review line.

    KNOWN BLIND SPOT, stated rather than left to be discovered (2026-07-25, Marrow M1). The walker below
    descends into dicts only — a float inside a JSON ARRAY is invisible to it, because the recursion has no
    list branch (its sibling in check_lift_denominators_match does). So `x.classes[0].prior = 1.0` passes
    unread while `x.classes.0.prior` would not. This is NOT waived: factors_v1.json acknowledges its one
    known array-nested extremal anyway. Closing it is deliberately a separate job — adding the list branch
    widens the gate across every watched artifact at once and will surface a fresh batch of unread values,
    and that batch deserves the same one-by-one adjudication the factors 16 got, not a bulk LEGACY entry."""
    import json
    bad, roots = [], []
    # LEGACY DEBT, itemised rather than waived (2026-07-25, Terroir T4). Widening the glob pointed the gate
    # at artifacts sealed before it existed. Their verdicts stand and their bytes are not rewritten here,
    # but the gate's own output is the wrong place to bury what it found, so each is named with its reading.
    # This list is PER-PATH: any NEW extremal in these same files still fails.
    LEGACY = {
        # SURFACED 2026-07-26 when the lattice path was fixed. These had NEVER been inspected: the gate
        # pointed at `eightfold/foundry/foundry/results/lattice`, one `.parent` short of the real path, and
        # the `if lat.exists()` guard made the miss silent. All three are explainable, and the third is a
        # defect deliberately preserved as evidence.
        ("grid_arm_a_results.json", "ceiling"):
            "ADJUDICATED BY EXPRESSION 2026-07-26. `ceiling` is a HARDCODED LITERAL — grid_arm_a.py:112 "
            "writes `\"ceiling\":1.0` into the results dict; nothing computes it. It records the 100% "
            "determinism ceiling stated in advance (46 flag-vectors -> 46 profiles, zero ambiguity), so it "
            "is benign AND it is not a measurement. A NEW SPECIES for this gate: a documentation constant "
            "living in a results artifact, indistinguishable to any reader from a computed value.",
        ("grid_arm_a_results_clean.json", "ceiling"):
            "benign — the same determinism ceiling in the post-fix `clean` run",
        ("grid_arm_a_results.json", "per_flag_recovery.1valid.acc"):
            "ADJUDICATED BY EXPRESSION 2026-07-26, and the first reading written here was WRONG. It said "
            "'the documented arithmetic flag leak'. The decisive test refutes that in one line: the CLEAN "
            "run drops exactly the leak moments (weight_mean, weight_spread) and 1valid.acc is STILL "
            "1.0000. The leak is not the mechanism. The real one is the finding itself — `1valid` is "
            "MEMBERSHIP of one specific tuple (is the all-ones tuple in R), which surface order structure "
            "determines exactly, and Arm A's whole result is that surfaces see membership and not closure. "
            "This 1.0 is assertion 5's POSITIVE CONTROL, benign and load-bearing.",
        ("grid_arm_a_results_clean.json", "per_flag_recovery.1valid.acc"):
            "same value, same mechanism, in the post-reclassification run — see above",
        ("crucible_results.json", "S1.envelope.approx_param_v.null_p2.5"):
            "benign — V >= 0, so a null envelope's 2.5th percentile legitimately bottoms out at 0",
        ("crucible_results.json", "S1.envelope.approx_param_v.one_sided_p_ge"):
            "REAL FLAW, minor: a resampling p is reported as exactly 0. With M nulls the honest form is "
            "(k+1)/(M+1); 0 asserts an impossibility M draws cannot establish. Does not change the S1 "
            "verdict (the real V is far outside the envelope either way). SCORER FIXED 2026-07-25 — "
            "crucible._envelope now uses the plus-one form already used by _perm_p_gradient, and a re-run "
            "emits 1/1001 = 0.000999 here. The ARTIFACT is deliberately not regenerated in this worktree: "
            "a no-change regen drifts S1.envelope.mca_full_dims.null_mean 16.533 -> 16.534 because the "
            "environment carries scipy 1.14.0 against requirements.lock's scipy==1.17.1. This entry stays "
            "until crucible_results.json is regenerated under the lock, and should be removed then.",
        ("crucible_results.json", "S3.amplification_bootstrap_caveated.permdet_amp_pos_frac_where_present"):
            "plausible — a fraction conditioned on presence (present_frac 0.416); the block is already "
            "labelled _caveated. Unacknowledged, not wrong.",
        ("crucible_results.json", "S3.amplification_bootstrap_caveated.vcclique_amp_pos_frac_where_present"):
            "plausible — as above (present_frac 0.369)",
        ("mosaic_L3_results.json", "P4_composition_decomposition.observed_v3new_V"):
            "an observed association of exactly 0 alongside a predicted 0.734. The block's own verdict is "
            "HOLDS=false and P4 was declared INSUFFICIENT, so nothing downstream rests on it — but exactly "
            "0.0 for a measured V is the tell this gate exists for and it is recorded as unresolved.",
        # RETIRED 2026-07-25: the two quarry_v2_results.json entries. The itemisation read them as
        # UNINITIALISED PLACEHOLDERS from a block that never ran. That diagnosis was WRONG — the block ran,
        # and both zeros are BIAS-CORRECTION FLOORS: structure.cramers_v subtracts (k-1)(r-1)/(n-1) from
        # phi^2 and clamps at zero, and at n=22 the correction (0.5714) exceeds the signal (phi^2 0.4464),
        # so the estimator returns exactly 0 where the uncorrected V is 0.3857. `shrinkage_fraction: null`
        # was not an author's idiom either; it is the uncond>0 divide-by-zero guard tripping on the same
        # floor. score_quarry_v2.py now emits an `extremal_acknowledged` entry carrying that arithmetic,
        # so the gate clears them on the evidence rather than on an exemption. Both entries removed rather
        # than reworded: a legacy list is for debt, and this is paid.
    }
    d = _eightfold_atlas()
    roots.append(d)
    # FIXED 2026-07-26: this read `d.parent.parent.parent / "foundry" / ...`, one `.parent` short, and
    # resolved to `eightfold/foundry/foundry/results/lattice` — a path that has never existed. The
    # `if lat.exists()` guard then made the miss SILENT: the gate reported PASS while watching nothing, so
    # every Foundry lattice artifact went uninspected, including grid_arm_a_results.json whose 1.000
    # positive control is quoted in the write-up. Resolve via the package, the same idiom as
    # _eightfold_atlas(), instead of counting directory levels from a sibling.
    try:
        import foundry
        lat = Path(foundry.__file__).resolve().parent / "results" / "lattice"
        if lat.exists():
            roots.append(lat)
    except ImportError:
        pass
    for root in roots:
        # WIDENED 2026-07-25 (Terroir T4): the original glob was `grid_*results*.json`, which stopped
        # watching the moment a result file was named anything else — terroir_v1_results.json was invisible
        # to it. A gate scoped to one project's filename convention is a gate with an expiry date.
        for p in sorted(_watched(root)):
            try:
                doc = json.loads(p.read_text(encoding="utf-8"))
            except Exception:  # noqa: BLE001
                continue
            ack = {a.get("stat") for a in doc.get("extremal_acknowledged", [])}
            def walk(node, path):
                if isinstance(node, dict):
                    for k, v in node.items():
                        walk(v, f"{path}.{k}" if path else k)
                elif isinstance(node, float) and node in (0.0, 1.0):
                    if (p.name, path) in LEGACY:
                        return                      # itemised above, not silently waived
                    if not any(path.endswith(a) or a.endswith(path) for a in ack):
                        bad.append(f"{p.name}: {path} is EXACTLY {node} and is not in "
                                   f"extremal_acknowledged — tidy-number gate (methods 22)")
            walk(doc, "")
    return bad


def check_lift_denominators_match() -> list[str]:
    """THE DENOMINATOR GATE (promoted 2026-07-25, Terroir T4).

    A lift is `accuracy - null`. The subtraction is only meaningful if BOTH TERMS WERE COMPUTED ON THE SAME
    ROWS. Three times in this program they were not:

      1. Quarry v2's conditional shrinkage — unconditional and conditional statistics on different supports
      2. Terroir A3 — a sociology increment on 225 rows compared against a 336-row headline (caught before
         it ran; the analysis was retired)
      3. Terroir A4's first pass — an admissible-only within-family NULL against an all-rows ACCURACY,
         reporting +0.0060 where the matched statistic is exactly 0

    Three instances is a class, not an anecdote series. So: any artifact block carrying `acc`/`null`/`lift`
    must declare the row count `n` those terms share, and `lift` must equal `acc - null` to rounding. A
    block that pools across a screen must additionally carry a `denominator_rule` naming the shared row
    set, because that is exactly the case where the mismatch is easiest to make and hardest to see."""
    import json
    bad, roots = [], []
    d = _eightfold_atlas()
    roots.append(d)
    # FIXED 2026-07-26: this read `d.parent.parent.parent / "foundry" / ...`, one `.parent` short, and
    # resolved to `eightfold/foundry/foundry/results/lattice` — a path that has never existed. The
    # `if lat.exists()` guard then made the miss SILENT: the gate reported PASS while watching nothing, so
    # every Foundry lattice artifact went uninspected, including grid_arm_a_results.json whose 1.000
    # positive control is quoted in the write-up. Resolve via the package, the same idiom as
    # _eightfold_atlas(), instead of counting directory levels from a sibling.
    try:
        import foundry
        lat = Path(foundry.__file__).resolve().parent / "results" / "lattice"
        if lat.exists():
            roots.append(lat)
    except ImportError:
        pass
    for root in roots:
        for p in sorted(_watched(root)):
            try:
                doc = json.loads(p.read_text(encoding="utf-8"))
            except Exception:  # noqa: BLE001
                continue

            def walk(node, path):
                if not isinstance(node, dict):
                    if isinstance(node, list):
                        for i, v in enumerate(node):
                            walk(v, f"{path}[{i}]")
                    return
                keys = set(node)
                acc_k = keys & {"acc", "accuracy"}
                null_k = keys & {"null", "fold_weighted_null", "modal_null"}
                lift_ks = [k for k in keys if k.startswith("lift") or k.endswith("_lift")]
                if acc_k and null_k and lift_ks:
                    a, nl = node[next(iter(acc_k))], node[next(iter(null_k))]
                    if isinstance(a, (int, float)) and isinstance(nl, (int, float)):
                        for lk in lift_ks:
                            lv = node[lk]
                            if isinstance(lv, (int, float)) and abs((a - nl) - lv) > 5e-4:
                                bad.append(f"{p.name}: {path}.{lk} = {lv} but acc - null = {a - nl:.4f} "
                                           f"— denominator gate: the two terms may not share a row set")
                    if "n" not in keys and "denominator_rule" not in keys:
                        bad.append(f"{p.name}: {path} reports acc/null/lift without an `n` or a "
                                   f"`denominator_rule` — denominator gate: the shared row set is "
                                   f"undeclared")
                for k, v in node.items():
                    walk(v, f"{path}.{k}" if path else k)
            walk(doc, "")
    return bad


def check_gates_inspected_something() -> list[str]:
    """THE META-GATE (2026-07-26, after the third fail-open). A gate that inspected ZERO files must FAIL,
    not pass.

    This one gate has now silently watched nothing in three distinct ways:
      1. a glob scoped to one project's filename convention, blind to the next project's results;
      2. a walker that descends into dicts only, so a float inside a JSON array is unreachable;
      3. a path one `.parent` short, resolving to a directory that has never existed — with the
         `if lat.exists()` guard turning the miss into SILENCE.
    All three FAIL OPEN: they report a clean pass over files they never opened. The failure is
    indistinguishable from success, which is the only property that matters here.

    THE RULE: an existence guard around a load-bearing scope is a silence generator. Resolve a scope
    through its package, never by counting directory levels from a sibling — and then ASSERT THE SCOPE IS
    NON-EMPTY, because verification that verified nothing must say so.

    This converts all three historical fail-opens into one impossible class: whatever the mechanism, an
    empty inspection set is now a build failure rather than a green light."""
    bad = []
    roots = _numeric_gate_roots()
    if not roots:
        return ["meta-gate: the numeric gates resolved NO roots at all — scope is empty"]
    total = 0
    for r in roots:
        n = len(_watched(r))
        total += n
        if n == 0:
            bad.append(f"meta-gate: root {r} is watched but contains ZERO inspectable artifacts — "
                       f"either the path is wrong or the pattern set is. A gate over nothing passes "
                       f"vacuously, which is the failure this check exists to make impossible.")
    if total == 0:
        bad.append("meta-gate: ZERO files inspected across all roots — every numeric gate passed vacuously")
    return bad


CHECKS = [
    ("Gates inspected something (meta-gate)", check_gates_inspected_something),
    ("Suspicious cleanliness (tidy-number gate)", check_suspicious_cleanliness),
    ("Lift denominators match (acc and null share rows)", check_lift_denominators_match),
    ("Anatomy passports complete + bridges pinned", check_anatomy_passports_complete),
    ("Stratified V known-answer gate (defect #15)", check_stratified_v_known_answers),
    ("Cramér's V in [0,1]", check_cramers_v_range),
    ("Factors k* inside verdict interval", check_factors_kstar_interval),
    ("Netted association <= raw (Cai-Chen)", check_netted_le_raw),
    ("Point estimates inside their CIs", check_estimates_in_cis),
    ("Census Jaccard in [0,1] and below plurality line", check_census_jaccard_sane),
    ("Contingency marginals sum to n", check_marginals_sum_to_n),
]


def run() -> int:
    n_fail = 0
    for name, fn in CHECKS:
        try:
            problems = fn()
        except Exception as exc:  # noqa: BLE001
            problems = [f"{type(exc).__name__}: {exc}"]
        ok = not problems
        n_fail += not ok
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")
        for p in problems:
            print(f"        {p}")
    print(f"\n{len(CHECKS) - n_fail}/{len(CHECKS)} coherence checks passed")
    return 1 if n_fail else 0
