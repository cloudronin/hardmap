"""The observatory catalog extractor — v1. THE ONLY PLACE A DESCRIPTOR IS COMPUTED.

Frames (raw dial panels) -> calibrated frames (controls attached) -> CATALOG (derived descriptors,
computed once, quoted everywhere). Analyses, contact sheets, seals and registry features read the catalog;
only this module touches raw values.

THE TEST-OF-A-COPY LAW, APPLIED AT BIRTH (methods 41). A conformance check that reimplements its subject
certifies the reimplementation. The same failure kills a descriptor layer: if a contact sheet recomputes
`overlap_slope` its own way, the catalog and the figure disagree and nobody knows which is the program's
number. So every descriptor is a pure function HERE, and consumers import or read — never reimplement.

VERSIONING IS THE F4 LAW. A changed extraction rule is a NEW CATALOG VERSION, never an in-place edit.
Sealed claims quote `descriptor@version` forever and old versions stay frozen.

═══ THE REFERENCE STEP, PINNED ═══════════════════════════════════════════════════════════════════════

`excess_ref` is taken at the MEDIAN ADMISSIBLE STEP: the median of the ramp positions that are neither
INSUFFICIENT nor GAP. The rule is positional and therefore OUTCOME-BLIND — it is computable without
seeing a single excess value.

The rejected candidates and why, recorded so the choice is not relitigated by taste:
  - "the hardest step" hits the INSUFFICIENT wall exactly where optimization rows go thin
  - "threshold-nearest" exists only for families with known thresholds
  - anything chosen by looking at excess values is selection on the outcome, forbidden by construction

The chosen step's ACTUAL RAMP VALUE ships beside every `excess_ref` cell, so a reader always knows where
on the dial the reference was taken, and `excess_min`/`excess_max` carry the envelope around it.
"""
from __future__ import annotations

import math
from itertools import combinations
from statistics import mean, pstdev, stdev

VERSION = "v2"
FLAT_MULTIPLIER = 2.0            # the trajectory rule, inherited unchanged from sounding_trajectories
BIMODALITY_FLAG = 0.555          # the conventional flag against a uniform reference
PAIR_CAP = 20000


# ── supply ───────────────────────────────────────────────────────────────────────────────────────────
def admissible_positions(steps):
    """Ramp positions that are neither INSUFFICIENT nor GAP. The basis of every positional rule."""
    return [s["ramp_position"] for s in steps
            if s.get("state") == "usable" and not s.get("insufficient")]


def reference_step(steps):
    """The MEDIAN ADMISSIBLE position. Outcome-blind by construction: computed from states, never values.

    Returns (position, ramp_value) or (None, None) when nothing is admissible.
    """
    adm = admissible_positions(steps)
    if not adm:
        return None, None
    pos = sorted(adm)[len(adm) // 2]
    val = next((s.get("ramp_value") for s in steps if s["ramp_position"] == pos), None)
    return pos, val


def supply(steps):
    r = [s.get("r") for s in steps if s.get("r") is not None]
    pos, _ = reference_step(steps)
    return {
        "r_ref": next((s.get("r") for s in steps if s["ramp_position"] == pos), None),
        "r_range": [min(r), max(r)] if r else None,
        "insufficient_share": (round(sum(1 for s in steps if s.get("insufficient")) / len(steps), 4)
                               if steps else None),
        "gap_count": sum(1 for s in steps if s.get("state") == "GAP-no-region"),
    }


# ── level ────────────────────────────────────────────────────────────────────────────────────────────
def level(steps, key="blend_excess"):
    pos, val = reference_step(steps)
    vals = [(s["ramp_position"], s.get(key)) for s in steps
            if s.get(key) is not None and s.get("state") == "usable" and not s.get("insufficient")]
    if not vals:
        return {"excess_ref": None, "excess_ref_position": pos, "excess_ref_ramp_value": val,
                "excess_min": None, "excess_max": None,
                "note": "no admissible step carries this value"}
    at_ref = next((v for p, v in vals if p == pos), None)
    return {"excess_ref": round(at_ref, 6) if at_ref is not None else None,
            "excess_ref_position": pos, "excess_ref_ramp_value": val,
            "excess_min": round(min(v for _, v in vals), 6),
            "excess_max": round(max(v for _, v in vals), 6),
            "n_admissible": len(vals)}


# ── shape ────────────────────────────────────────────────────────────────────────────────────────────
def shape(steps, key="blend_excess", sd_key="control_sd"):
    """FLAT / MONOTONE / NON-MONOTONE under the pinned rule, with the sensitivity band shipped."""
    seq = [(s["ramp_position"], s.get(key), s.get(sd_key)) for s in steps
           if s.get(key) is not None and s.get("state") == "usable" and not s.get("insufficient")]
    seq.sort()
    v = [x[1] for x in seq]
    sds = [x[2] for x in seq if x[2] is not None]
    if len(v) < 3:
        return {"traj_class": "UNCLASSIFIED", "why": "fewer than 3 admissible steps",
                "slope_sign": None, "max_excursion_sd": None, "n_admissible": len(v)}
    exc = max(v) - min(v)
    psd = mean(sds) if sds else 0.0
    def klass(mult):
        if psd and exc < mult * psd:
            return "FLAT"
        nondec = all(b >= a for a, b in zip(v, v[1:]))
        noninc = all(b <= a for a, b in zip(v, v[1:]))
        return "MONOTONE" if (nondec or noninc) else "NON-MONOTONE"
    return {"traj_class": klass(FLAT_MULTIPLIER),
            "classification_rule": f"FLAT iff excursion < {FLAT_MULTIPLIER} x pooled control SD",
            "sensitivity_band": {"1.0x": klass(1.0), "3.0x": klass(3.0)},
            "slope_sign": (0 if v[-1] == v[0] else (1 if v[-1] > v[0] else -1)),
            "excursion": round(exc, 6),
            "pooled_control_sd": round(psd, 6) if psd else None,
            "max_excursion_sd": round(exc / psd, 4) if psd else None,
            "n_admissible": len(v)}


# ── coherence ────────────────────────────────────────────────────────────────────────────────────────
def overlaps(region, rng=None, cap=PAIR_CAP):
    """Normalised pairwise agreement. Capped LAZILY — a cap applied after the work is not a cap.

    THE SELF-PAIR FILTER APPLIES ONLY TO THE SAMPLED PATH. `combinations` already yields pairs of
    DISTINCT POSITIONS, so filtering `a != b` there discards legitimate pairs whose values coincide —
    it conflates "the same member drawn twice" with "two members holding equal values". Only the
    with-replacement sampler can draw a member against itself, so only it needs the guard.
    """
    n = len(region[0])
    total = len(region) * (len(region) - 1) // 2
    if total <= cap:
        return [sum(1 for x, y in zip(a, b) if x == y) / n for a, b in combinations(region, 2)]
    out = []
    for _ in range(cap):
        i, j = rng.randrange(len(region)), rng.randrange(len(region))
        if i == j:                      # the same member drawn twice — a sampling artifact, not a pair
            continue
        a, b = region[i], region[j]
        out.append(sum(1 for x, y in zip(a, b) if x == y) / n)
    return out


def bimodality_coefficient(o):
    """BC = (skew^2 + 1) / (kurt + 3(n-1)^2/((n-2)(n-3))). Measured, never eyeballed (methods 42)."""
    n = len(o)
    if n < 4:
        return None
    m = mean(o)
    sd = stdev(o)
    if sd == 0:
        return None
    sk = sum((x - m) ** 3 for x in o) / n / sd ** 3
    ku = sum((x - m) ** 4 for x in o) / n / sd ** 4 - 3
    den = ku + 3 * (n - 1) ** 2 / ((n - 2) * (n - 3))
    return (sk ** 2 + 1) / den if den else None


def coherence(steps):
    pos, _ = reference_step(steps)
    seq = [(s["ramp_position"], s.get("overlap_mean")) for s in steps
           if s.get("overlap_mean") is not None]
    seq.sort()
    bcs = [s.get("bimodality_coefficient") for s in steps
           if s.get("bimodality_coefficient") is not None]
    slope = None
    if len(seq) >= 2:
        xs = [p for p, _ in seq]; ys = [v for _, v in seq]
        mx, my = mean(xs), mean(ys)
        den = sum((x - mx) ** 2 for x in xs)
        slope = (sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / den) if den else None
    bmax = max(bcs) if bcs else None
    return {"overlap_ref": next((v for p, v in seq if p == pos), None),
            "overlap_slope": round(slope, 6) if slope is not None else None,
            "bimodality_max": round(bmax, 4) if bmax is not None else None,
            "bimodal_flag": (bmax > BIMODALITY_FLAG) if bmax is not None else None,
            "bimodality_flag_threshold": BIMODALITY_FLAG,
            "n_steps_with_overlap": len(seq)}


# ── transition — DESCRIPTIVE ONLY AT v1 ──────────────────────────────────────────────────────────────
def transition(steps, key="blend_excess"):
    """Change-point location and sharpness.

    FLAGGED: these are estimates WITHOUT TYPED NULLS. No seal may consume them at v1. The flag ships in
    the cell so a consumer cannot acquire the number without the caveat — a warning that lives only in a
    schema document is a warning nobody reads.
    """
    seq = [(s["ramp_position"], s.get(key)) for s in steps
           if s.get(key) is not None and s.get("state") == "usable" and not s.get("insufficient")]
    seq.sort()
    v = [x[1] for x in seq]
    if len(v) < 4:
        return {"kink_step": None, "kink_sharpness": None,
                "SEAL_PROHIBITED_AT_V1": True,
                "why": "fewer than 4 admissible steps; no change point estimable"}
    best, bpos = None, None
    for i in range(1, len(v)):
        a, b = v[:i], v[i:]
        if len(a) < 1 or len(b) < 1:
            continue
        d = abs(mean(b) - mean(a))
        if best is None or d > best:
            best, bpos = d, seq[i][0]
    return {"kink_step": bpos, "kink_sharpness": round(best, 6) if best is not None else None,
            "SEAL_PROHIBITED_AT_V1": True,
            "why_prohibited": ("a change-point estimate without a typed null is descriptive. The null "
                               "has not been pinned, so no sealed claim may consume this at v1.")}


# ── the row-level assembly ───────────────────────────────────────────────────────────────────────────
# ── structure — NEW AT v2 ────────────────────────────────────────────────────────────────────────────
def structure(steps, region=None, structural_expectation=None):
    """Is this trajectory flat BY CONSTRUCTION rather than by measurement?

    A fixed-cardinality row's FEASIBLE region is every size-k subset of the ground set. That set does not
    depend on the instance, so it is byte-identical at every ramp position — `max-coverage` reads r=120,
    overlap 0.5765, BC 0.4696 at all five steps of its ramp, and would read the same at any other.

    THE FLATNESS IS A PROPERTY OF THE ROW'S DEFINITION, NOT A READING. Correlating such a trajectory
    against anything is correlating a constant, and letting it stand as an extremal is reporting the
    definition back as a discovery. The flag exists so Helm can foreclose that whole candidate species
    instead of screening its members one at a time.

    DECLARED AND OBSERVED ARE KEPT SEPARATE. `structurally_flat` is derived from the row's DECLARED
    structural expectation and costs no reading; `region_size_invariant` is what the frames actually
    show. Collapsing them into one field would hide the case where they disagree — and a fixed-
    cardinality row whose region size moves is a conformance failure worth seeing, not a flag to fix."""
    flat_by_definition = bool(structural_expectation == "fixed_cardinality" and region == "feasible")
    rs = [s.get("r") for s in steps
          if s.get("state") == "usable" and s.get("r") is not None]
    invariant = (len(set(rs)) == 1) if len(rs) >= 2 else None
    return {"structurally_flat": flat_by_definition,
            "region_size_invariant": invariant,
            "declared_expectation": structural_expectation,
            "agree": None if invariant is None else (flat_by_definition == invariant),
            "rule": ("structurally_flat iff the row DECLARES fixed_cardinality and this is its feasible "
                     "region — the region is then every size-k subset, identical at every ramp value"),
            "why_it_matters": ("a structurally-flat trajectory is excluded from Helm's sweep: its "
                               "flatness is definitional, so enumerating it as a candidate correlates "
                               "a constant with things")}


def descriptors(steps, region=None, structural_expectation=None):
    """Every v2 descriptor for one (problem, region, flavour) trajectory. A pure function of frames
    plus the row's DECLARED structural expectation, which is not a reading."""
    return {"level": level(steps), "shape": shape(steps), "coherence": coherence(steps),
            "supply": supply(steps), "transition": transition(steps),
            "structure": structure(steps, region, structural_expectation),
            "scaling": {"kink_drift_n": None, "sharpening_ratio": None,
                        "RESERVED": "fills when the size axis lands; reserved per the additive licence"},
            "descriptor_version": VERSION}
