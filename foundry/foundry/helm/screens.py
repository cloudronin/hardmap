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

DISPOSITIONS = ("SLATED", "HELD", "REJECTED")

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
        "SELECT COUNT(*) FROM admissible_catalog GROUP BY problem_id ORDER BY 1")]
    med = per[len(per) // 2] if per else 0
    return {"n_clusters": len(reserved),
            "n_cells": len(reserved) * med,
            "median_cells_per_published_problem": med,
            "reserved": sorted(reserved),
            "projected_from": "the published population's cells-per-problem — no reserved row is read"}


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
    if len(ds) == 2 and frozenset(ds) in DEFINITIONAL_COUPLING:
        return ("REJECTED", "netting",
                f"definitionally coupled: {DEFINITIONAL_COUPLING[frozenset(ds)]}. The correlation is "
                f"partly forced by the extractor, so a frontier replication of it would confirm "
                f"arithmetic rather than structure.")
    if cand.get("charge") and not cand.get("charge_is_a_fixed_row_label"):
        return ("REJECTED", "F2-foreclosed",
                "a charge would have to vary along the ramp for this statistic to mean anything; "
                "cited charges are FIXED ROW LABELS")

    # ── 3. frontier power ───────────────────────────────────────────────────────────────────────────
    d = cand.get("disclosed")
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
    elif cand["kind"] == "association":
        mde = mde_association(frontier["n_cells"])
        if mde is None or d < mde:
            return ("HELD", "power-fail",
                    (f"disclosed V {d:.3f} is below the frontier's MDE {mde:.3f}" if mde
                     else "frontier too small to type an MDE"))
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
        if disp == "HELD" and rule == "power-fail":
            # The recorded gap. §7's standing HOLD query resurfaces this candidate the moment the
            # frontier's grown n clears the number written here.
            if c["kind"] == "co-movement":
                rec["required_clusters"] = required_clusters(c.get("disclosed"))
                rec["gap_in_reserved_rows"] = (
                    None if rec["required_clusters"] is None
                    else max(0, rec["required_clusters"] - frontier["n_clusters"]))
            elif c["kind"] == "association":
                rec["required_cells"] = required_cells(c.get("disclosed"))
        results.append(rec)
    slated = [r for r in results if r["screen_disposition"] == "SLATED"]
    if slated:
        # Screen 4: the wave declares its family size BEFORE ruling; Holm across the declared family.
        thr = holm([1.0] * len(slated))
        for r, t in zip(slated, thr):
            r["family_size"] = len(slated)
            r["holm_threshold_if_sealed"] = t
    return results
