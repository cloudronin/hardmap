"""R25 — net the theorem-forced component out of the census P2/P3 statistics (Sprint 4, Task 0).

The standing R25 procedure (`eightfold.structure.cai_chen_residual_audit`) nets the theorem-forced *members*
out of an association and asks whether it SURVIVES. On the CANON it survives (approx|parameterized Cramér's V
stays >= 0.5 even after deleting the entire APX-complete x FPT cell) — the multiplet is genuine empirical
structure, not a bridge-theorem artifact. On the CENSUS the same procedure must return the OPPOSITE, and it must
return it at the floor: every oracle charge is a *total deterministic function of the co-clone's polymorphism
profile* (`approximation` tracks 0/1-validity, `parameterized` tracks affine-ness — both are functions of
Pol(Γ)). Conditioning on the profile therefore removes ALL of the approx|parameterized association and ALL of the
census's latent dimensionality. The predicted residual is **exactly zero**.

This module is a SELFTEST of the netting machinery, not a discovery run (Sprint 4 re-uses the same residual
plumbing on the MEASURED instrument columns, where a non-zero residual is the whole point). It confirms the
residual is zero three independent ways and STOPs (raises) if any of them is non-zero:

  1. PROVENANCE NETTING (mirrors cai_chen): a both-real (approx,parameterized) row is theorem-forced iff BOTH
     cells carry evidential status `derived` — the kernel already verified (gate 6b) that a *named* dichotomy
     theorem forces that exact value. Net out every derived row; the residual association is over what remains.
     For the oracle-only census nothing remains -> V undefined -> 0, `survives = False`.
  2. WITHIN-STRATUM ASSOCIATION: stratify the both-real rows by polymorphism profile and pool the *within*-
     stratum contingency (the Cochran–Mantel–Haenszel move that removes the between-stratum/confounded signal).
     Functional determination makes every stratum charge-constant, so the pooled within-stratum V = 0.
  3. FUNCTIONAL DETERMINATION (falsifiable): group ALL both-real rows by polymorphism profile and assert every
     group is charge-constant. This is a genuine cross-implementation check — the N1 co-clone oracle
     (`oracles.classify`) and the finer-tier oracle (`finer.classify_boolean`) are *different code paths*; if
     they disagreed on two languages that share a profile, the group would split and the audit would STOP.

If the residual is non-zero, do not proceed: either the netting is buggy or an oracle cell is not actually
polymorphism-forced (a hand-edited value, a mis-statused cell). Diagnose before anything downstream runs.
"""
from eightfold import atlas
from eightfold import structure as S
from foundry import domain3 as D3
from foundry import finer as FN
from foundry import postlattice as PL
from foundry.analysis import CA, CB, full_census

# the oracle (theorem-derived) charge columns — the ones an atlas theorem assigns from Pol(Γ)
ORACLE_CHARGES = ("decision", "counting", "approximation", "parameterized", "localization")


# ── polymorphism profiles: the ORACLE INPUT (the stratum). Same profile ⟹ identical oracle charges. ──────────
def _bool_profile(rels):
    """The Boolean stratum: which CKZ operations (+ 0/1-validity + weak separability) preserve Γ. This is the
    exact set of predicates the Boolean oracles read; two Boolean languages agreeing on all of them are the same
    co-clone as far as every dichotomy theorem is concerned."""
    flags = (("0valid", PL.is_0valid(rels)), ("1valid", PL.is_1valid(rels)),
             ("horn", PL.has_polymorphism(rels, PL.HORN)), ("dual-horn", PL.has_polymorphism(rels, PL.DUAL_HORN)),
             ("bijunctive", PL.has_polymorphism(rels, PL.BIJUNCTIVE)), ("affine", PL.has_polymorphism(rels, PL.AFFINE)),
             ("weakly-separable", PL.is_weakly_separable(rels)))
    return ("bool", frozenset(name for name, ok in flags if ok))


def _d3_profile(rels):
    """The domain-3 stratum: the tractable-op profile + the extra predicates the general-domain oracles read
    (constant-validity, semilattice-closure, bounded width). A Boolean and a domain-3 language can never share a
    stratum (different domain), so residuals are pooled within tier — the comparable unit."""
    return ("d3", D3.polymorphism_profile(rels), D3._const_valid(rels),
            D3._semilattice_closed(rels), D3.is_bounded_width(rels))


def census_strata():
    """{row_id: (profile, tier)} for every census row, by re-deriving the polymorphism profile from each row's
    generating relations (walking the SAME builders the census is built from)."""
    reg = {}
    for cc in PL.BOOLEAN_COCLONES:
        reg[cc.id] = (_bool_profile(cc.relations), "boolean-N1")
    for cid, _name, _enc, rels in FN._CANDIDATES:
        reg[cid] = (_bool_profile(rels), "boolean-finer")
    for lang in D3.CURATED_D3:
        reg[lang.id] = (_d3_profile(lang.relations), "domain-3")
    return reg


def _cramers_v(xs, ys):
    if len(xs) < 2 or len(set(xs)) < 2 or len(set(ys)) < 2:
        return None            # undefined — no marginal variation on at least one axis
    v = S.cramers_v(xs, ys)
    return round(float(v), 3) if v == v else None


# ── anchor cross-validation: the census∩canon overlap, compared against the ACTUAL Eightfold canon atlas ──────
# Each registration anchor is a canonical Boolean CSP present in BOTH worlds. Comparison is PERSPECTIVE-AWARE:
#   * decision / counting / approximation are perspective-free (or perspective-matched) — the census oracle and
#     the independently-curated canon MUST agree here (a disagreement is an R20 contradiction → STOP).
#   * parameterized is perspective-DIVERGENT: the canon parameterizes by treewidth (every CSP is FPT), the census
#     by Exact-Ones solution weight (Marx). Different parameter ⟹ not comparable — the concrete face of
#     "incomparable elsewhere," not a mismatch.
#   * localization is canon-absent (a foundry charge) → not comparable.
_ANCHOR_CANON_ID = {"xor-sat": "xor-sat", "horn-sat": "horn-sat", "2-sat": "sat-2",
                    "3-sat": "sat-3", "nae-sat": "nae-sat", "one-in-three-sat": "one-in-three-sat"}
_PERSPECTIVE_FREE = ("decision", "counting", "approximation")   # commensurable across the two worlds


def census_residual_audit(entries=None):
    """Net the theorem-forced component out of the census approx|parameterized association (P2) and out of the
    census factor structure (P3). Returns the netted numbers; the predicted residual is zero everywhere."""
    entries = full_census() if entries is None else entries
    strata = census_strata()
    ids, _, rows = S._grid(entries)
    byid_row = {pid: r for pid, r in zip(ids, rows)}
    byid_cell = {e.problem_id: {c.charge: c for c in e.charges} for e in entries}
    byid_status = {pid: {ch: c.status for ch, c in cm.items()} for pid, cm in byid_cell.items()}
    from foundry.charges import FOUNDRY_SPEC
    spec_real = FOUNDRY_SPEC.charge_real_values

    # the both-real (approx, parameterized) rows — the P2 table
    both = [pid for pid in ids
            if byid_row[pid][CA] in spec_real[CA] and byid_row[pid][CB] in spec_real[CB]]
    xs_all = [byid_row[pid][CA] for pid in both]
    ys_all = [byid_row[pid][CB] for pid in both]

    # ── (1) provenance netting: drop rows whose BOTH cells are `derived` (theorem-forced), recompute V ────────
    forced = [pid for pid in both
              if byid_status[pid].get(CA) == "derived" and byid_status[pid].get(CB) == "derived"]
    residual_ids = [pid for pid in both if pid not in forced]
    p2_raw_v = _cramers_v(xs_all, ys_all)
    p2_residual_v = _cramers_v([byid_row[pid][CA] for pid in residual_ids],
                               [byid_row[pid][CB] for pid in residual_ids])
    provenance = {
        "level_raw": {"v": p2_raw_v, "n": len(both)},
        "level_net_theorem_forced": {"v": p2_residual_v, "n": len(residual_ids),
                                     "netted_out": len(forced)},
        "all_both_real_rows_are_derived": len(forced) == len(both),
        "survives": (p2_residual_v is not None and p2_residual_v >= 0.5),  # canon: True; census: False
    }

    # ── (2) within-stratum pooled association (condition on the polymorphism profile) ─────────────────────────
    # Cochran–Mantel–Haenszel move: pool the WITHIN-profile association, size-weighted. Every stratum is charge-
    # constant (functional determination), so each within-stratum V is 0 and the pooled statistic is 0.
    by_stratum = {}
    for pid in both:
        by_stratum.setdefault(strata[pid][0], []).append(pid)
    per_stratum_v = {}
    for prof, members in by_stratum.items():
        pv = _cramers_v([byid_row[pid][CA] for pid in members], [byid_row[pid][CB] for pid in members])
        per_stratum_v[str(sorted(prof[1]) if prof[0] == "bool" else prof)] = {"v": pv if pv is not None else 0.0,
                                                                              "n": len(members)}
    pooled_within = round(sum(v["v"] * v["n"] for v in per_stratum_v.values()) / max(1, len(both)), 3)

    # ── (3) functional determination: same profile ⟹ same oracle charges (falsifiable cross-check) ───────────
    determination = _functional_determination(entries, strata)

    # ── (P3) residual dimensionality: the theorem forces every oracle cell, so the residual table is null ─────
    oracle_cells = [(pid, ch) for pid in ids for ch in ORACLE_CHARGES
                    if byid_row[pid][ch] in spec_real.get(ch, ())]
    nonderived_oracle_cells = [(pid, ch) for pid, ch in oracle_cells
                               if byid_status[pid].get(ch) != "derived"]
    distinct_oracle_profiles = len({tuple(byid_row[pid][ch] for ch in ORACLE_CHARGES) for pid in ids})
    p3 = {
        "raw_distinct_oracle_profiles": distinct_oracle_profiles,
        "raw_census_k_hat_reference": 3,   # Factors v1 on the census (p3_factors); documented reference
        "n_oracle_cells": len(oracle_cells),
        "n_nonderived_oracle_cells": len(nonderived_oracle_cells),
        "residual_dimensionality": 0 if not nonderived_oracle_cells else None,
        "note": ("every filled oracle cell is theorem-`derived` (deviance from the theorem prediction = 0 over "
                 f"all {len(oracle_cells)} cells), so no latent structure survives netting: residual k* = 0. The "
                 "raw k*=3 is the census re-expressing its own dichotomies (the distinct polymorphism strata)."),
    }

    # ── anchor cross-validation (against the real canon atlas, perspective-aware) ─────────────────────────────
    anchors = _anchor_crossval(byid_cell)

    residual_is_zero = (
        provenance["level_net_theorem_forced"]["v"] is None and
        provenance["all_both_real_rows_are_derived"] and
        not provenance["survives"] and
        pooled_within == 0.0 and
        determination["all_strata_charge_constant"] and
        p3["residual_dimensionality"] == 0 and
        anchors["all_perspective_free_cells_agree"]
    )
    return {
        "audit": "census_R25_residual", "predicted_residual": 0, "residual_is_zero": residual_is_zero,
        "n_both_real": len(both),
        "P2_provenance_netting": provenance,
        "P2_within_stratum": {"pooled_within_stratum_v": pooled_within, "n_strata": len(by_stratum),
                              "per_stratum": per_stratum_v},
        "functional_determination": determination,
        "P3_dimensionality": p3,
        "anchor_crossvalidation": anchors,
        "rule": ("R25 (census): net out the theorem-`derived` component. Residual approx|param V is UNDEFINED "
                 "(no non-derived both-real rows), pooled within-stratum V = 0, residual k* = 0. `survives` = "
                 "False — the OPPOSITE of the canon, where the association survives deletion of the whole "
                 "APX-complete x FPT cell. The oracle-only census carries no empirical content beyond its "
                 "dichotomies; the canon-vs-computation comparison over oracle columns is closed here."),
    }


def _functional_determination(entries, strata):
    """Group all rows by polymorphism profile; every group must share one full oracle-charge profile."""
    ids, _, rows = S._grid(entries)
    byid_row = {pid: r for pid, r in zip(ids, rows)}
    groups = {}
    for pid in ids:
        groups.setdefault(strata[pid][0], []).append(pid)
    inconsistent = []
    multi = 0
    for prof, members in groups.items():
        if len(members) > 1:
            multi += 1
        profiles = {tuple(byid_row[pid].get(ch) for ch in ORACLE_CHARGES) for pid in members}
        if len(profiles) > 1:
            inconsistent.append({"profile": str(prof), "members": members,
                                 "distinct_charge_profiles": [list(p) for p in profiles]})
    return {"n_profile_groups": len(groups), "n_multi_row_groups": multi,
            "max_group_size": max((len(m) for m in groups.values()), default=0),
            "all_strata_charge_constant": not inconsistent, "inconsistent_groups": inconsistent}


def _anchor_crossval(byid_cell):
    """Compare each registration anchor's census oracle cells against the ACTUAL Eightfold canon atlas,
    perspective-aware. Perspective-free charges must agree; parameterized is logged as perspective-divergent."""
    from foundry.charges import FOUNDRY_SPEC
    real = FOUNDRY_SPEC.charge_real_values
    canon = {e.problem_id: {c.charge: c for c in e.charges} for e in atlas.load_atlas()}
    results, agree, disagree = {}, 0, 0
    for aid, kid in _ANCHOR_CANON_ID.items():
        cens_cells, canon_cells = byid_cell.get(aid, {}), canon.get(kid, {})
        row = {"canon_id": kid, "present_in_census": aid in byid_cell, "present_in_canon": kid in canon}
        cmp = {}
        for ch in _PERSPECTIVE_FREE:
            cv = cens_cells[ch].value if ch in cens_cells else None
            kv = canon_cells[ch].value if ch in canon_cells else None
            if cv in real.get(ch, ()) and kv in real.get(ch, ()):
                match = cv == kv
                agree += match
                disagree += not match
                cmp[ch] = {"census": cv, "canon": kv, "agree": match}
            else:
                cmp[ch] = {"census": cv, "canon": kv, "comparable": False}
        # parameterized: record the perspective divergence explicitly
        pc = cens_cells.get("parameterized")
        kc = canon_cells.get("parameterized")
        row["parameterized_perspective_divergent"] = {
            "census": {"value": pc.value if pc else None, "perspective": getattr(pc, "perspective", None)},
            "canon": {"value": kc.value if kc else None, "perspective": getattr(kc, "perspective", None)},
            "comparable": False}
        row["perspective_free"] = cmp
        results[aid] = row
    return {"all_perspective_free_cells_agree": disagree == 0, "n_agree": agree, "n_disagree": disagree,
            "n_anchors": len(_ANCHOR_CANON_ID), "perspective_free_charges": list(_PERSPECTIVE_FREE),
            "per_anchor": results,
            "note": ("decision/counting/approximation cross-validate census↔canon at every anchor; parameterized "
                     "is perspective-divergent (canon=treewidth → FPT, census=Exact-Ones weight → Marx W[1]); "
                     "localization is canon-absent. This is the 'cross-validated at the anchors, incomparable "
                     "elsewhere' locus.")}


# ── CI selftest: the residual MUST be zero; a non-zero residual is a STOP-the-line bug ────────────────────────
def census_r25_selftest(verbose=True):
    a = census_residual_audit()
    ok = a["residual_is_zero"]
    if verbose:
        pv = a["P2_provenance_netting"]
        print(f"R25 census residual selftest:")
        print(f"  P2 raw V (all both-real)         = {pv['level_raw']['v']}  (n={pv['level_raw']['n']})")
        print(f"  P2 residual V (net theorem-forced)= {pv['level_net_theorem_forced']['v']}  "
              f"(netted {pv['level_net_theorem_forced']['netted_out']}, n_residual="
              f"{pv['level_net_theorem_forced']['n']})  survives={pv['survives']}")
        print(f"  P2 pooled within-stratum V        = {a['P2_within_stratum']['pooled_within_stratum_v']}  "
              f"({a['P2_within_stratum']['n_strata']} strata)")
        fd = a["functional_determination"]
        print(f"  functional determination          = {fd['n_multi_row_groups']} multi-row strata, max size "
              f"{fd['max_group_size']}, all charge-constant={fd['all_strata_charge_constant']}")
        print(f"  P3 residual dimensionality        = {a['P3_dimensionality']['residual_dimensionality']}  "
              f"(non-derived oracle cells={a['P3_dimensionality']['n_nonderived_oracle_cells']})")
        ax = a["anchor_crossvalidation"]
        print(f"  anchors (canon↔census)            = {ax['n_agree']} agree / {ax['n_disagree']} disagree "
              f"on perspective-free charges over {ax['n_anchors']} anchors (param perspective-divergent)")
        print(f"  RESIDUAL IS ZERO (predicted)      = {ok}  -> {'PASSED' if ok else 'FAILED — STOP, diagnose'}")
    return 0 if ok else 1


if __name__ == "__main__":
    import sys
    sys.exit(census_r25_selftest())
