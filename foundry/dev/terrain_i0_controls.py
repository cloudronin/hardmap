#!/usr/bin/env python3
"""Terrain I0 — ground the control hierarchy BEFORE the prereg text fixes. No scoring, no bet.

WHAT THIS SETTLES, and every answer here is measured rather than argued:
  1. Is each control tier COMPUTABLE for each anomaly reading?
  2. Does each tier's control family VARY? (census-before-seal: a tier-2 family that cannot vary is
     unusable, and that has to be discovered before the bet fixes, not after it fails.)
  3. Does the kill condition fire — is tier 2 computable for a MAJORITY of anomaly readings?

THE TIERS, in increasing fairness:
  tier 0  uniform random sets of size r from the ambient space          (the survey's current control)
  tier 1  matched-marginal: size r, per-coordinate inclusion frequencies matched to the region
  tier 2  matched-object: r random members of the region's own containing SPECIES

THE STRUCTURAL FINDING THAT SHAPES EVERYTHING, stated here because it is not obvious and it decides the
seal's scope. "The same combinatorial family" is only a LARGER set than the region for some region kinds:

  optimal    region = the optimising subfamily; species = the FEASIBLE family. Strictly larger. Tier 2 is
             well-defined and asks a real question: does the optimal subfamily blend worse than a generic
             size-matched subfamily of the same feasible family?
  feasible   region = every object satisfying the constraint. The species IS the region. A control drawn
             from the species at matched r is the region itself. Tier 2 DEGENERATE.
  solutions  region = the instance's solution set. The only natural containing family is the ambient
             space, which is tier 0. Tier 2 COLLAPSES to tier 0.

There is a tempting escape for `feasible` — draw the control from a DIFFERENT instance of the same
generator. It is a trap and the prereg must say so. The survey's measured rate is ALREADY a mean over
several instances of that generator, so a sibling-instance control estimates the same quantity as the
measurement and its excess is zero by construction. That is not a conservative null, it is a RIGGED one:
the bet could not win however real the effect. It is kept below as a CALIBRATION diagnostic (it should
read ~0, and a nonzero reading indicts the pipeline) and is explicitly barred from the primary statistic.
"""
import json
import random
import sys
from collections import defaultdict
from itertools import combinations
from pathlib import Path
from statistics import mean, pstdev

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "dev"))
LAT = ROOT / "foundry" / "results" / "lattice"
OUT = LAT / "terrain_i0_control_census.json"
import sounding_v3_survey as S3                                        # noqa: E402
from sounding_v1 import violation                                      # noqa: E402

K_CENSUS = 12          # control draws per tier for the variance census
SUB_CAP = 3000
OPS = {"majority": (lambda ts: tuple(1 if sum(c) >= 2 else 0 for c in zip(*ts)), 3),
       "minority": (lambda ts: tuple(sum(c) % 2 for c in zip(*ts)), 3),
       "min": (lambda ts: tuple(min(c) for c in zip(*ts)), 2),
       "max": (lambda ts: tuple(max(c) for c in zip(*ts)), 2)}


def tier0(r, n, rng):
    """Uniform random subset of {0,1}^n at size r — the survey's existing control."""
    N = 1 << n
    if r >= N:
        return None
    return [tuple((x >> (n - 1 - i)) & 1 for i in range(n)) for x in rng.sample(range(N), r)]


def tier1(region, rng):
    """Matched-marginal: size r, per-coordinate inclusion frequency matched to the region.

    Coordinates are drawn INDEPENDENTLY at the region's own marginals, so the control keeps the region's
    per-coordinate bias and discards its correlation structure. That is exactly the comparison H-artifact
    asks for at this tier: spanning trees hit some edges far more often than others, and if that alone
    explains the excess it should die here."""
    r, n = len(region), len(region[0])
    p = [sum(s[i] for s in region) / r for i in range(n)]
    out, seen, guard = [], set(), 0
    while len(out) < r and guard < 40 * r:
        guard += 1
        v = tuple(1 if rng.random() < p[i] else 0 for i in range(n))
        if v not in seen:
            seen.add(v); out.append(v)
    return out if len(out) == r else None


def tier2_from_species(species, r, rng):
    """Matched-object: r random members of the region's own containing species."""
    if species is None or len(species) < r:
        return None
    return [tuple(s) for s in rng.sample(list(species), r)]


def rate(S, flavour, rng):
    op, m = OPS[flavour]
    v, _, _, _ = violation(S, op, m, rng)
    return v


def census_one(regions_by_kind, kind, flavour, rng):
    """Return per-tier {computable, mean, sd, n} for one (region kind, flavour) on one built instance."""
    region = regions_by_kind.get(kind)
    if not region or len(region) < 4:
        return None
    r, n = len(region), len(region[0])
    species = regions_by_kind.get("feasible") if kind == "optimal" else None
    out = {"r": r, "n": n, "measured": rate(region, flavour, rng)}
    for name, draw in (("tier0", lambda: tier0(r, n, rng)),
                       ("tier1", lambda: tier1(region, rng)),
                       ("tier2", lambda: tier2_from_species(species, r, rng))):
        vals = []
        for _ in range(K_CENSUS):
            S = draw()
            if S is None:
                break
            v = rate(S, flavour, rng)
            if v is not None:
                vals.append(v)
        if len(vals) < 3:
            out[name] = {"computable": False,
                         "why": ("no containing species larger than the region for this region kind"
                                 if name == "tier2" else "control could not be drawn at this r and n")}
        else:
            out[name] = {"computable": True, "mean": round(mean(vals), 4),
                         "sd": round(pstdev(vals), 5), "n_draws": len(vals),
                         "degenerate_zero_variance": pstdev(vals) == 0.0}
    return out


def main() -> int:
    rng = random.Random(20260726)
    # Rows carrying admissible positive-excess readings, with a builder and its v3 ramp argument.
    BUILD = {"knapsack": lambda: S3.knapsack(rng, 0.45),
             "set-cover": lambda: S3.set_cover(rng, 9),
             "hitting-set": lambda: S3.hitting_set(rng, 7),
             "feedback-vertex-set": lambda: S3.fvs(rng, 0.30),
             "odd-cycle-transversal": lambda: S3.oct_(rng, 0.30),
             "independent-dominating-set": lambda: S3.indep_dom(rng, 0.28),
             "subset-sum": lambda: S3.subsum(rng, 60),
             "graph-3-coloring": lambda: S3.col3(rng, 0.32)}
    rows_out, tally = {}, defaultdict(int)
    for row, build in BUILD.items():
        per_kind = defaultdict(list)
        for _ in range(3):
            try:
                regs = dict(build() or [])
            except Exception as e:
                rows_out[row] = {"build_error": str(e)}; break
            for kind in ("feasible", "optimal", "solutions"):
                if kind not in regs:
                    continue
                for fl in ("majority", "max"):
                    c = census_one(regs, kind, fl, rng)
                    if c:
                        per_kind[(kind, fl)].append(c)
        if row in rows_out:
            continue
        rows_out[row] = {}
        for (kind, fl), cs in per_kind.items():
            t2 = [c["tier2"] for c in cs]
            rows_out[row][f"{kind}·{fl}"] = {
                "r_range": [min(c["r"] for c in cs), max(c["r"] for c in cs)],
                "tier0_computable": all(c["tier0"]["computable"] for c in cs),
                "tier1_computable": all(c["tier1"]["computable"] for c in cs),
                "tier2_computable": all(t["computable"] for t in t2),
                "tier2_why": next((t.get("why") for t in t2 if not t["computable"]), None),
                "tier1_varies": all(c["tier1"].get("sd", 0) > 0 for c in cs if c["tier1"]["computable"]),
                "tier2_varies": all(t.get("sd", 0) > 0 for t in t2 if t["computable"]),
                "example": cs[0]}
            tally[(kind, "tier2_ok" if all(t["computable"] for t in t2) else "tier2_no")] += 1

    doc = {"schema": "terrain-i0-control-census/v1",
           "STATUS": "I-PHASE GROUNDING — no bet, no score, no prereg text fixed by this",
           "purpose": ("settle computability and variance of every control tier before the seal's text "
                       "fixes, and evaluate the kill condition on tier-2 coverage"),
           "tier_definitions": {
               "tier0": "uniform random subset of the ambient space at matched r",
               "tier1": "matched-marginal — size r, per-coordinate inclusion frequencies matched",
               "tier2": "matched-object — r random members of the region's own containing species"},
           "tier2_is_structurally_unavailable_for": {
               "feasible": "the region IS the species; a species-drawn control at matched r is the region",
               "solutions": "the only natural containing family is the ambient space, i.e. tier 0"},
           "sibling_instance_control_is_barred_from_the_primary": (
               "drawing the control from a different instance of the same generator would make tier 2 "
               "available everywhere, and it is a RIGGED null: the survey's measured rate is already a "
               "mean over several instances of that generator, so the control estimates the same "
               "quantity and the excess is zero by construction. Kept only as a calibration diagnostic."),
           "per_row": rows_out}
    # ── the tidy-number gate, satisfied by DERIVATION rather than by a blanket ───────────────────────
    # Exactly-extremal statistics must be acknowledged in their own artifact with a reason. The reasons
    # here are derived from each value's own path at run time, never hardcoded — and an extremal whose
    # path matches NO known-explicable pattern is a HARD FAILURE of this script, because an
    # acknowledgment block that accepts anything is a rubber stamp and the gate exists to prevent one.
    def explain(path: str, val: float):
        p = path.lower()
        if p.endswith(".sd") or ".sd" in p.rsplit(".", 1)[-1]:
            return ("control SD exactly 0 — every control draw returned the same rate. This is "
                    "INSUFFICIENT-degenerate in the v3 spec's pre-declared vocabulary, and it is a "
                    "reading about the control family's usability, not about the region.")
        if "feasible" in p and ("·max" in p or "·max" in p) and val == 0.0:
            return ("EXACT 0.0 IS FORCED BY THE CONSTRUCTION: these feasible families are upward-closed "
                    "(adding elements never destroys membership), so max = union stays inside and no "
                    "blend can violate. Independently established and brute-force tested in the "
                    "zero-hunt as HIDDEN-CLOSURE. An exact zero here is the expected value, not a tell.")
        if "optimal" in p and ("·max" in p or "·max" in p) and val == 1.0:
            return ("EXACT 1.0 IS FORCED BY THE CONSTRUCTION, and is the mirror of the case above: the "
                    "union of two optimal members is feasible but strictly larger, hence never optimal, "
                    "so EVERY blend leaves the optimal region. Saturation is the expected value.")
        # MAX SATURATES WHENEVER THE DEFINING CONSTRAINT IS NOT UPWARD-CLOSED. This is the mirror of the
        # feasible/max case above and it reaches rows whose constraint has a non-monotone conjunct. Named
        # per row rather than caught by a wildcard, so the acknowledgment stays auditable: a new row
        # arriving with a 1.0 still halts until someone reads its constraint.
        NOT_UPWARD_CLOSED = {
            "independent-dominating-set": (
                "the region is an INTERSECTION of an upward-closed property (dominating) and a "
                "downward-closed one (independent). Union preserves domination and destroys "
                "independence as soon as the two members differ, so max leaves the region."),
            "subset-sum": (
                "membership is an EXACT-SUM equality. The union of two distinct equal-sum subsets has a "
                "strictly larger sum, so it overshoots the target and max always leaves the region."),
            "number-partitioning": (
                "membership is an exact-balance equality, the same shape as subset-sum: union breaks the "
                "equality it is defined by."),
        }
        if "·max" in p and val == 1.0:
            for row, why in NOT_UPWARD_CLOSED.items():
                if f"per_row.{row}." in p:
                    return ("EXACT 1.0 IS FORCED BY THE CONSTRUCTION: " + why)
        if p.endswith(".measured") and val in (0.0, 1.0):
            return None                       # a measured extremal with no structural story -> HALT
        return None

    acks, unexplained = [], []
    def walk_ack(node, path):
        if isinstance(node, dict):
            for k, v in node.items():
                walk_ack(v, f"{path}.{k}" if path else k)
        elif isinstance(node, float) and node in (0.0, 1.0):
            why = explain(path, node)
            (acks if why else unexplained).append({"stat": path, "value": node, "why": why})
    walk_ack(doc, "")
    if unexplained:
        print("FAIL — exactly-extremal values with no structural explanation:", file=sys.stderr)
        for u in unexplained[:12]:
            print(f"    {u['stat']} = {u['value']}", file=sys.stderr)
        print("\nEach needs reading before this artifact ships. The tidy-number gate is not satisfied by "
              "acknowledging everything.", file=sys.stderr)
        return 1
    doc["extremal_acknowledged"] = acks
    doc["extremal_acknowledgment_is_derived"] = (
        "every entry above was produced by matching the value's own path against a small set of "
        "structurally-explicable patterns at run time. An extremal matching none of them halts this "
        "script rather than being waved through.")

    OUT.write_text(json.dumps(doc, indent=1) + "\n")

    print("TERRAIN I0 — CONTROL-TIER CENSUS (grounding; no bet)\n")
    print(f"  {'row':<28}{'region·flavour':<22}{'r':>10}  t0  t1  t2   t1var t2var")
    for row, kinds in sorted(rows_out.items()):
        if "build_error" in kinds:
            print(f"  {row:<28}BUILD ERROR: {kinds['build_error'][:50]}"); continue
        for k, v in sorted(kinds.items()):
            rr = f"{v['r_range'][0]}-{v['r_range'][1]}"
            y = lambda b: " Y" if b else " ."
            print(f"  {row:<28}{k:<22}{rr:>10} {y(v['tier0_computable'])}  {y(v['tier1_computable'])}"
                  f"  {y(v['tier2_computable'])}   {y(v['tier1_varies'])}   {y(v['tier2_varies'])}")
    print(f"\n  tier-2 availability by region kind: {dict(tally)}")
    print(f"\nwrote {OUT.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
