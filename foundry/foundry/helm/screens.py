"""The mechanical screens — Helm §3. Run BEFORE any human sees the slate.

THE FLOORS ARE PINNED IN THIS FILE, not chosen when the numbers arrive. A power floor selected after
seeing which candidates clear it is not a screen, it is a preference. Every constant below is declared
with the reason it takes the value it does, and the values are mathematical minima wherever one exists
rather than taste dressed as rigour.

THE POWER SCREEN IS COMPUTED ON THE FRONTIER, NEVER ON THE SWEEP. A candidate's disclosed statistic came
from published ground and says nothing about whether the reserved tranche can adjudicate it. So the
effective n is the frontier's EXPECTED n — and it is counted in CLUSTERS (problems), not cells, because
cells within a row are dependent and this program has already been bitten once by the difference between
a cell-level and a class-level reading of the same relationship (Q15).

A CANDIDATE THAT FAILS POWER IS HELD, NEVER KILLED. Its MDE gap is recorded so the standing HOLD query
resurfaces it the moment the frontier's grown n clears it. "Revisit someday" becomes a SELECT.
"""
from __future__ import annotations

import math

ALPHA = 0.05                 # FWER target, per the standing family discipline
POWER = 0.80
Z_ALPHA_2 = 1.959964         # two-sided 0.05
Z_BETA = 0.841621            # power 0.80

# Fisher's z transform needs n - 3 > 0 for its standard error to exist at all. Four clusters is
# therefore the MATHEMATICAL minimum for a cluster-level correlation, not a chosen threshold.
MIN_FRONTIER_CLUSTERS = 4

# A chi-square association at df = 1 needs a noncentrality of ~7.85 for 80% power at alpha 0.05.
CHI2_NCP_DF1 = 7.85

# An extremal-reproduction question needs enough frontier cells for the descriptor to be observed at
# all. Two is the minimum at which "the extremal was or was not exceeded" has more than one outcome.
MIN_FRONTIER_CELLS = 2

# THE STRATUM FLOOR, derived rather than chosen. A one-sided permutation test over m cells can attain
# no p-value smaller than 1/(m+1) — with 19 cells the smallest possible p is exactly 0.05, so 19 is the
# point at which significance becomes attainable at all and 20 is the first size at which it is
# attainable with anything to spare. A stratum below it returns INSUFFICIENT rather than a number,
# which is the same distinction the sounding survey draws between silence and inadmissible speech.
MIN_STRATUM_CELLS = 20

DISPOSITIONS = ("SLATED", "HELD", "REJECTED")

# Ruling 2 (2026-07-27). The HOLD queue's standing promise — the frontier's grown n revives it BY
# CONSTRUCTION — is true only for holds whose gap closes through scheduled building. A family-scoped
# candidate whose family has no unbuilt reachable rows left cannot be revived by any reservation: its
# gap closes only if an unbuilt CAPTURE PATH lands. Those are different creatures and the trail must
# not conflate them.
#
#   HELD-power        revives on a COUNT          — the frontier grows and clears the MDE
#   HELD-path-gated   revives on a BUILD DECISION — re-reviewed at every capture-path ruling, and
#                     CLOSES as INSUFFICIENT-by-population if the queue completes without its path
#
# A hold that cannot name its revival mechanism is a zombie. This one names it, with an expiry.
HOLD_KINDS = ("HELD-power", "HELD-path-gated", "HELD-null-missing")

# ── netting (Helm §3.2): descriptor pairs whose correlation is partly forced by their definitions ────
# Read off `foundry/catalog/extract.py`, not guessed. `level()` builds one value set per trajectory and
# returns a member of it (`excess_ref`) beside its order statistics (`excess_min`, `excess_max`), so
# ref <= max and ref >= min and min <= max hold ALWAYS. `shape()` computes the excursion as
# `max(v) - min(v)` over that same set, so `max_excursion_sd` is an arithmetic function of the two
# endpoints — correlating a difference against one of its own terms is the textbook spurious pair.
#
# These candidates are still ENUMERATED, because the forking-paths denominator has to count every
# question the sweep could have asked. They are rejected with the rule named, and the rejection is
# preserved. A denominator that quietly omits the questions we knew were bad is a denominator we chose.
# ── DEFINITIONAL CONSUMPTION (ruled 2026-07-27, wave-4 sitting) ──────────────────────────────────────
# The netting screen barred pairs linked by an IDENTITY or a forced order. That is too narrow. A flag
# derived from a quantity is coupled to it just as hard: INSUFFICIENT-r's trigger IS r below the floor,
# so correlating `r_ref` with the share of flags derived from r is a vacuous comparison in descriptor
# clothing. The flag-derivation graph is known, so the screen reads it instead of guessing.
#
# The rule generalises past this pair: any candidate where one descriptor's DEFINITION CONSUMES the
# other's underlying quantity is barred at sweep time — enumerated, killed, kept in the denominator.
CONSUMES = {
    "insufficient_share": {"r"},      # the INSUFFICIENT-r flag fires on r below R_FLOOR
    "gap_count":          set(),      # GAP is region absence, not an r threshold — NOT coupled to r
    "r_ref":              {"r"},
}

# ── SIZE-COUPLED DESCRIPTORS (ruled 2026-07-27) ──────────────────────────────────────────────────────
# Size is this program's most-convicted confounder: the deflator, the sixth species, N3's size-driven
# closure prevalence. Wave 4's slate came back four-for-four wearing its costumes. These descriptors all
# carry r in one hand:
#
#   r_ref              IS the region size at the reference step
#   insufficient_share fires on r-floors
#   bimodality_max     BC is a coefficient statistic; small overlap samples inflate it MECHANICALLY
#
# A marginal correlation between two of these has size in both hands. To reach a slate, such a candidate
# must present its r-CONDITIONED disclosed prior — and a pair containing `r_ref` itself cannot be
# conditioned on r at all, so it is barred rather than held.
# `bimodality_excess_ref` is deliberately NOT here. It is BC minus the matched-r control mean, so the
# size dependence is subtracted rather than conditioned away — which is exactly why it was built.
SIZE_COUPLED = {"r_ref", "insufficient_share", "bimodality_max"}

DEFINITIONAL_COUPLING = {
    frozenset({"excess_ref", "excess_min"}): "excess_ref >= excess_min by construction",
    frozenset({"excess_ref", "excess_max"}): "excess_ref <= excess_max by construction",
    frozenset({"excess_min", "excess_max"}): "order statistics of one value set; min <= max always",
    frozenset({"max_excursion_sd", "excess_min"}): "excursion = excess_max - excess_min",
    frozenset({"max_excursion_sd", "excess_max"}): "excursion = excess_max - excess_min",
}


def frontier_expectation(con, reserved):
    """What the reserved tranche is expected to yield, projected from published rows.

    Reads NO reading from any reserved row — there are none, the rows are not captured. This projects
    from the published population's cells-per-problem, which is disclosed ground and legitimately so."""
    per = [r[0] for r in con.execute(
        "SELECT COUNT(*) FROM sweepable_catalog GROUP BY problem_id ORDER BY 1")]
    med = per[len(per) // 2] if per else 0
    return {"n_clusters": len(reserved),
            "n_cells": len(reserved) * med,
            "median_cells_per_published_problem": med,
            "reserved": sorted(reserved),
            "strata": frontier_strata(con, reserved),
            "projected_from": "the published population's cells-per-problem — no reserved row is read"}


def frontier_strata(con, reserved):
    """How many frontier cells each (family x region-kind x flavour) stratum is projected to receive.

    A reserved row contributes ONE cell to each stratum its family/region/flavour combination names, so
    a stratum's supply is the count of reserved rows in that family. Family is a census TYPING, not a
    reading — no reserved row is read here, and none could be: they have no frames."""
    if not reserved:
        return {}
    qs = ",".join("?" * len(reserved))
    fams = con.execute(f"SELECT family FROM problems WHERE problem_id IN ({qs})",
                       sorted(reserved)).fetchall()
    out = {}
    for (f,) in fams:
        out[f] = out.get(f, 0) + 1
    return out


def mde_correlation(n_clusters):
    """Minimum detectable |rho| at the declared alpha/power, via Fisher's z."""
    if n_clusters < MIN_FRONTIER_CLUSTERS:
        return None
    return math.tanh((Z_ALPHA_2 + Z_BETA) / math.sqrt(n_clusters - 3))


def mde_association(n_cells):
    """Minimum detectable Cramer's V at df = 1. Approximate, and labelled as such."""
    if n_cells < 2:
        return None
    return math.sqrt(CHI2_NCP_DF1 / n_cells)


def required_clusters(rho):
    """The frontier size at which a disclosed |rho| becomes detectable. Inverts the Fisher-z MDE.

    This is what makes the HOLD queue a queue rather than a graveyard: a candidate held today carries
    the number of reserved rows that would revive it, so growth in the frontier resurfaces it by
    SELECT rather than by anyone remembering it existed."""
    r = abs(rho or 0.0)
    if r <= 0 or r >= 1:
        return None
    return math.ceil(3 + ((Z_ALPHA_2 + Z_BETA) / math.atanh(r)) ** 2)


def required_cells(v):
    """The frontier cell count at which a disclosed Cramer's V becomes detectable at df = 1."""
    if not v or v <= 0:
        return None
    return math.ceil(CHI2_NCP_DF1 / v ** 2)


def screen(cand, con, frontier, seal_prohibited):
    """Apply the four screens in order. Returns (disposition, rule, detail).

    SCREEN 1 CHECKS THE NULL FOR THE BET, NOT FOR THE DISCLOSED STATISTIC. Those are different objects,
    and accepting the second in place of the first is how a screen keeps passing candidates it should
    stop — the in-sample null always exists, because the in-sample number was computed with it."""
    # ── 1. a typed null must exist FOR THE SEALED BET ───────────────────────────────────────────────
    if cand["kind"] != "bank-import" and not cand.get("frontier_null"):
        return ("HELD", "null-missing",
                cand.get("why_no_frontier_null") or "no typed null for the bet this would become")
    touched = set(cand.get("descriptors") or [])
    bad = touched & seal_prohibited
    if bad:
        return ("REJECTED", "null-missing",
                f"consumes {sorted(bad)}, which the catalog stamps SEAL_PROHIBITED_AT_V1 — the "
                f"transition group has no typed null at v1 and the cell says so itself")
    if cand["kind"] == "bank-import":
        if cand.get("bank_status") == "CLOSED":
            return "REJECTED", "null-missing", "bank question already closed; nothing left to seal"
        return ("HELD", "null-missing",
                "bank import carries prose, not a typed statistic — it needs a statistic and a null "
                "before it can be powered, and inventing one here would be the eyeball ban in reverse")

    # ── 2. F2 / netting / forced-flavour compliance ─────────────────────────────────────────────────
    ds = cand.get("descriptors") or []
    if len(ds) == 2:
        a, b = ds
        if (CONSUMES.get(a, set()) & CONSUMES.get(b, set())) and a != b:
            return ("REJECTED", "definitional-consumption",
                    f"`{a}` and `{b}` are both defined over {sorted(CONSUMES.get(a, set()) & CONSUMES.get(b, set()))}"
                    f" — one descriptor's definition consumes the other's underlying quantity, so the "
                    f"correlation is vacuous rather than structural. Enumerated, killed, kept in the "
                    f"denominator.")
    if len(ds) == 2 and frozenset(ds) in DEFINITIONAL_COUPLING:
        return ("REJECTED", "netting",
                f"definitionally coupled: {DEFINITIONAL_COUPLING[frozenset(ds)]}. The correlation is "
                f"partly forced by the extractor, so a frontier replication of it would confirm "
                f"arithmetic rather than structure.")
    if cand.get("charge") and not cand.get("charge_is_a_fixed_row_label"):
        return ("REJECTED", "F2-foreclosed",
                "a charge would have to vary along the ramp for this statistic to mean anything; "
                "cited charges are FIXED ROW LABELS")
    if cand.get("structurally_flat"):
        return ("REJECTED", "structurally-flat",
                "the cell's trajectory is flat BY CONSTRUCTION — a fixed-cardinality row's feasible "
                "region is every size-k subset, identical at every ramp value before any instance "
                "exists. Enumerating it correlates a constant, or reports a definition as a discovery.")

    # ── 2b. SIZE CONDITIONING (ruled 2026-07-27) ────────────────────────────────────────────────────
    # Marginals with size in both hands do not get a sitting.
    touched = set(ds)
    if len(touched & SIZE_COUPLED) >= 2:
        if "r_ref" in touched:
            return ("REJECTED", "size-marginal",
                    f"{sorted(touched)} are both size-coupled AND one of them IS the size descriptor, "
                    f"so the pair cannot be conditioned on r — there is no version of this question "
                    f"with size held out. Small samples inflate BC mechanically; this is that "
                    f"coupling, not a finding.")
        if cand.get("disclosed_partial_r") is None:
            return ("HELD", "needs-r-conditioning",
                    f"{sorted(touched)} are both size-coupled, with r behind both as common cause. "
                    f"This reaches a slate only as an r-CONDITIONED partial, with the conditioned "
                    f"prior disclosed — or it dies there.")

    # ── 3. frontier power ───────────────────────────────────────────────────────────────────────────
    d = cand.get("disclosed")
    if cand.get("disclosed_partial_r") is not None:
        d = cand["disclosed_partial_r"]      # the conditioned prior is the one that gets screened
    if d is None:
        return "HELD", "power-fail", "no disclosed statistic — the sweep found too few cells to compute it"
    if cand["kind"] == "co-movement":
        mde = mde_correlation(frontier["n_clusters"])
        if mde is None:
            return ("HELD", "power-fail",
                    f"the frontier has {frontier['n_clusters']} cluster(s); a cluster-level rank "
                    f"correlation needs at least {MIN_FRONTIER_CLUSTERS} for its standard error to "
                    f"exist. Gap: {MIN_FRONTIER_CLUSTERS - frontier['n_clusters']} more reserved rows.")
        if abs(d) < mde:
            return ("HELD", "power-fail",
                    f"disclosed |rho| {abs(d):.3f} is below the frontier's MDE {mde:.3f}")
        # POPULATION MATCH (Ruling 2). A family-scoped prior scored on a family-absent frontier is not
        # a test of the prior — it is a test of a broader cousin with the prior as decoration. This is
        # the lesson Terroir's strata and N6-R's tiers each paid for once.
        grp = cand.get("group")
        strata = frontier.get("strata") or {}
        supply = frontier.get("family_supply") or {}
        if grp and grp != "pooled" and strata.get(grp, 0) == 0:
            unbuilt = supply.get(grp, 0)
            if unbuilt > 0:
                return ("HELD", "population-mismatch",
                        f"the disclosed prior is {grp}-specific and the frontier holds ZERO {grp} "
                        f"rows. {unbuilt} unbuilt {grp} row(s) remain, so a future reservation can "
                        f"close this by construction.")
            return ("HELD", "path-gated",
                    f"the disclosed prior is {grp}-specific, the frontier holds ZERO {grp} rows, and "
                    f"the {grp} family has NO unbuilt reachable rows left. This gap cannot close "
                    f"through scheduled building — only through an unbuilt capture path. Re-review at "
                    f"the next capture-path ruling; closes as INSUFFICIENT-by-population if the build "
                    f"queue completes without one.")
    elif cand["kind"] == "association":
        mde = mde_association(frontier["n_cells"])
        if mde is None or d < mde:
            return ("HELD", "power-fail",
                    (f"disclosed V {d:.3f} is below the frontier's MDE {mde:.3f}" if mde
                     else "frontier too small to type an MDE"))
    elif cand["kind"] == "anomaly":
        # Stratified exchangeability (ruling, 2026-07-27): the bet is adjudicated WITHIN the
        # candidate's stratum, so what matters is that stratum's supply — not the frontier's total.
        strata = frontier.get("strata") or {}
        fam = (cand.get("stratum") or {}).get("family")
        if fam is None:
            supply = min(strata.values()) if strata else 0
            where = "the thinnest stratum it spans"
        else:
            supply = strata.get(fam, 0)
            where = f"stratum family={fam}"
        if supply < MIN_STRATUM_CELLS:
            return ("HELD", "power-fail",
                    f"{where} projects {supply} frontier cell(s); the stratified null needs "
                    f"{MIN_STRATUM_CELLS} before a permutation p-value below alpha is attainable "
                    f"at all. Gap: {MIN_STRATUM_CELLS - supply} more reserved rows in that family.")
    return "SLATED", None, None


def holm(pvals, alpha=ALPHA):
    """Holm-Bonferroni across the wave's declared family. Returns per-index thresholds."""
    idx = sorted(range(len(pvals)), key=lambda i: pvals[i])
    m = len(pvals)
    out = [None] * m
    for rank, i in enumerate(idx):
        out[i] = alpha / (m - rank)
    return out


def run(cands, con, frontier, seal_prohibited):
    """Screen every candidate. REJECTIONS ARE PRESERVED — they are what a future auditor needs to
    verify the correction was computed from an honest enumeration."""
    results = []
    for c in cands:
        disp, rule, detail = screen(c, con, frontier, seal_prohibited)
        rec = {**c, "screen_disposition": disp, "screen_rule": rule, "screen_detail": detail}
        if disp == "HELD" and rule in ("population-mismatch", "path-gated"):
            rec["hold_kind"] = ("HELD-power" if rule == "population-mismatch" else "HELD-path-gated")
            rec["revives_on"] = ("a reservation drawn from the family's unbuilt rows"
                                 if rule == "population-mismatch"
                                 else "a capture-path build decision — NOT on any frontier count")
            rec["closes_as"] = (None if rule == "population-mismatch"
                                else "INSUFFICIENT-by-population, if the build queue completes "
                                     "without the path")
        if disp == "HELD" and rule == "power-fail":
            rec["hold_kind"] = "HELD-power"
            rec["revives_on"] = "a frontier count — recorded below"
            # The recorded gap. §7's standing HOLD query resurfaces this candidate the moment the
            # frontier's grown n clears the number written here.
            if c["kind"] == "co-movement":
                rec["required_clusters"] = required_clusters(c.get("disclosed"))
                rec["gap_in_reserved_rows"] = (
                    None if rec["required_clusters"] is None
                    else max(0, rec["required_clusters"] - frontier["n_clusters"]))
            elif c["kind"] == "association":
                rec["required_cells"] = required_cells(c.get("disclosed"))
            elif c["kind"] == "anomaly":
                fam = (c.get("stratum") or {}).get("family")
                strata = frontier.get("strata") or {}
                supply = strata.get(fam, 0) if fam else (min(strata.values()) if strata else 0)
                rec["required_stratum_cells"] = MIN_STRATUM_CELLS
                rec["stratum_family"] = fam
                rec["gap_in_reserved_rows"] = max(0, MIN_STRATUM_CELLS - supply)
        results.append(rec)
    slated = [r for r in results if r["screen_disposition"] == "SLATED"]
    if slated:
        # Screen 4: the wave declares its family size BEFORE ruling; Holm across the declared family.
        thr = holm([1.0] * len(slated))
        for r, t in zip(slated, thr):
            r["family_size"] = len(slated)
            r["holm_threshold_if_sealed"] = t
    return results
