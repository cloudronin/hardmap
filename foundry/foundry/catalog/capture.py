"""The observatory's frame-capture pipeline — one implementation, every batch.

BATCH 1 CARRIED ITS OWN COPY OF THIS and that was fine for one batch. A second copy would be the
test-of-a-copy law arriving in the fan-out: two batches computing `overlap_mean` slightly differently
produce a catalog whose cells are not comparable, and nothing in the artifact would say so. So the
pipeline lives here and a batch is nothing but a table of generators.

WHAT A BATCH SUPPLIES: `{row: (builder, structural_expectation)}` where `builder(rng, ramp_value)`
returns `[(region_kind, region), ...]`. Everything else — conformance at birth, the ramp, the dial panel,
the three absence states — is this module's job.

CONFORMANCE AT BIRTH IS DERIVED CONSEQUENCES, NEVER THE FILTER. Checking that a region's members satisfy
the predicate the generator filtered by is circular. So a declared structural expectation is checked as a
CONSEQUENCE the definition implies but the filter does not state, and a generator that cannot reproduce
its own consequence does not ship — while its exclusion does not discard the batch.
"""
from __future__ import annotations

import random
from itertools import combinations, islice
from statistics import mean, pstdev

from . import extract as X

R_FLOOR = 10
K_CTRL = 20
SUBSET_CAP = 20000
HULL_MAX_N = 12                     # m=2 only, per the standing scope


def violation_rate(region, op, m):
    """Distinct m-subsets, LAZILY capped. A cap applied after the work is not a cap (methods)."""
    R = set(region)
    subs = list(islice(combinations(region, m), SUBSET_CAP))
    return (sum(1 for s in subs if op(s) not in R) / len(subs)) if subs else None


def hull_inflation(region, op, m):
    if m != 2 or len(region[0]) > HULL_MAX_N:
        return None
    cur = set(region)
    while True:
        new = {op(t) for t in combinations(cur, 2)} - cur
        if not new:
            return len(cur) / len(region)
        cur |= new
        if len(cur) > 60000:
            return None


def ambient_stability(build, ramp, rng, n_probe=3):
    """Does the row's GROUND SET stay the same object as the dial moves? (minted 2026-07-27)

    A blend statistic compares a region against an ambient of 2^w, where w is the tuple width. If w
    changes along the ramp, the trajectory confounds "the constraint tightened" with "the space got
    bigger", and no descriptor downstream can separate them. Vertex-subset rows hold w = n at every
    step; EDGE-subset rows do not, because the edge set is both the ground set and the thing edge
    density ramps.

    EQUALITY, NOT SIMILARITY. The requirement is that w be identical at every step, because the ambient
    must be the same object for the readings to be comparable at all — a tolerance here would be a
    threshold invented to let something through.

    Returns (stable, widths). `stable` is None when too few steps produced a region to judge."""
    widths = []
    for v in ramp:
        for _ in range(n_probe):
            try:
                d = dict(build(rng, v) or [])
            except Exception:
                continue
            r = d.get("feasible") or d.get("solutions")
            if r:
                widths.append(len(r[0]))
                break
    if len(widths) < 2:
        return None, widths
    return len(set(widths)) == 1, widths


def conformance_at_birth(build, expect, rng, probe_ramp=0.30, n_probe=4):
    """Derived consequences of the definition, checked independently of the generator's own filter."""
    checks, fails, regs = [], [], []
    for _ in range(n_probe):
        try:
            d = dict(build(rng, probe_ramp) or [])
        except Exception as e:                       # a raising builder is a failure, not a skip
            return [{"check": "buildable", "pass": False, "detail": f"builder raised: {e}"}], \
                   [f"builder raised: {e}"]
        r = d.get("feasible") or d.get("solutions")
        if r and 2 <= len(r) <= 4000:
            regs.append(r)
    if not regs:
        return ([{"check": "buildable", "pass": False,
                  "detail": "no region of usable size at the probe ramp value"}],
                ["no region built"])
    checks.append({"check": "buildable", "pass": True, "sizes": [len(x) for x in regs]})

    if expect in ("downward_closed", "upward_closed"):
        bit = 1 if expect == "downward_closed" else 0
        to = 0 if expect == "downward_closed" else 1
        ok = True
        for r in regs:
            S = set(r)
            for s in r:
                for i, v in enumerate(s):
                    if v == bit and tuple(to if j == i else s[j] for j in range(len(s))) not in S:
                        ok = False
                        break
                if not ok:
                    break
            if not ok:
                break
        checks.append({"check": f"derived: {expect} (single-bit move stays inside)", "pass": ok,
                       "why_not_the_filter": ("monotone closure is a CONSEQUENCE of the row's predicate, "
                                              "not a restatement of it")})
        if not ok:
            fails.append(f"not {expect}")
    if expect == "fixed_cardinality":
        w = {len({sum(s) for s in r}) for r in regs}
        ok = w == {1}
        checks.append({"check": "derived: exactly one distinct member weight", "pass": ok,
                       "observed": sorted(w)})
        if not ok:
            fails.append("not fixed-cardinality")
    return checks, fails


def capture_row(row, build, expect, ramp, ops, seed, control_fn, n_inst=3):
    """Conformance, then the full dial panel across the declared ramp. Returns (record, excluded).

    `control_fn(region, rng) -> control_region` is INJECTED rather than imported. The library must not
    reach into dev scripts for its fair null — a library whose behaviour depends on who imported it is
    not a library. The caller passes the ladder rung it wants."""
    rng = random.Random(seed)
    stable, widths = ambient_stability(build, ramp, rng)
    if stable is False:
        return None, {"row": row,
                      "reason": [f"ambient is dial-dependent: ground-set width varies {sorted(set(widths))} "
                                 f"across the declared ramp, so a trajectory would confound tightening "
                                 f"with a growing space"],
                      "ground_set_widths": widths}
    checks, fails = conformance_at_birth(build, expect, rng)
    if fails:
        return None, {"row": row, "reason": fails, "conformance": checks}

    steps = []
    for pos, val in enumerate(ramp):
        srng = random.Random(seed + 1000 * pos + abs(hash(row)) % 997)
        acc = {}
        for _ in range(n_inst):
            for kind, region in (build(srng, val) or []):
                if region and len(region) >= 2:
                    acc.setdefault(kind, []).append(region)
        if not acc:
            steps.append({"ramp_position": pos, "ramp_value": val, "state": "GAP-no-region",
                          "reason": "no instance at this step produced a region"})
            continue
        for kind, regs in sorted(acc.items()):
            ov = [X.overlaps(r, rng=srng) for r in regs]
            flat = [x for o in ov for x in o]
            b = X.bimodality_coefficient(flat) if flat else None
            dials = {"r_per_instance": [len(r) for r in regs],
                     "r_mean": round(mean(len(r) for r in regs), 2),
                     "overlap_mean": round(mean(mean(o) for o in ov if o), 4) if any(ov) else None,
                     "bimodality_coefficient": round(b, 4) if b is not None else None,
                     "bimodal_flag": (b > X.BIMODALITY_FLAG) if b is not None else None,
                     "flavours": {}}
            for fl, (op, m) in ops.items():
                rs = [x for x in (violation_rate(r, op, m) for r in regs) if x is not None]
                if not rs:
                    continue
                ctrl = []
                for r in regs:
                    for _ in range(max(1, K_CTRL // len(regs))):
                        c = control_fn(r, srng)
                        v = violation_rate(c, op, m) if c else None
                        if v is not None:
                            ctrl.append(v)
                hi = [x for x in (hull_inflation(r, op, m) for r in regs) if x is not None]
                r_mean = dials["r_mean"]
                dials["flavours"][fl] = {
                    "measured_rate": round(mean(rs), 4),
                    "control_mean": round(mean(ctrl), 4) if ctrl else None,
                    "control_sd": round(pstdev(ctrl), 5) if len(ctrl) > 1 else None,
                    "blend_excess": round(mean(rs) - mean(ctrl), 4) if ctrl else None,
                    "control_route": "CP",
                    "hull_inflation": round(mean(hi), 4) if hi else None,
                    "hull_note": None if hi else "unaffordable (m=2 and n<=12 only)",
                    "insufficient": ("INSUFFICIENT-r" if r_mean < R_FLOOR else
                                     ("INSUFFICIENT-degenerate"
                                      if len(ctrl) < 2 or pstdev(ctrl) == 0 else None))}
            steps.append({"ramp_position": pos, "ramp_value": val, "region": kind,
                          "state": "usable", "dials": dials})
    return {"row": row, "ramp_values": list(ramp), "structural_expectation": expect,
            "conformance": {"checks": checks, "passed": True}, "steps": steps}, None
