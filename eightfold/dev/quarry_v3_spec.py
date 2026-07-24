#!/usr/bin/env python3
"""V3_SPEC — the Atlas v3 instrument, scoped BESIDE the frozen kernel (never inside it).

THE VOCABULARY IS NOT METADATA, IT IS PART OF THE INSTRUMENT: the factors estimators size their
one-hot indicator matrix from the charge vocabulary, so a vocabulary edit IS an instrument edit.
Editing `charges.py` to add a rung broke the frozen suite (79 passed -> 3 failed, test_factors
planted-recovery / null-quiet) because it perturbed the v2 instrument itself — see
`results/prereg/prereg_v9-clarification-02.json`.

So v3 gets its own spec, composed from the kernel read-only (the Strata precedent):
  * v2's instrument stays frozen in the kernel (8 approximation rungs)
  * v3's instrument lives here (9 rungs: `superpoly-APX` between poly-APX and inapprox)
  * every v2-vs-v3 comparison is DUAL-CODED (clarification-02's separability requirement)

Nothing here mutates `eightfold.charges`; EIGHTFOLD_SPEC and all v1/v2 code paths are untouched.
"""
import dataclasses

from eightfold import charges as C

# the v3 rung: approximable only within a SUPERpolynomial factor (SVP 2^O(n loglog n/log n);
# CVP 2^(n/2), Babai). Neither poly-APX (no polynomial factor is achieved) nor inapprox (a factor
# IS achieved) is correct — v1 had no expressible value (errata-v1 E1, vocabulary-gap class).
SUPERPOLY = "superpoly-APX"

# the v3 decision rungs (owner ruling 2026-07-24, prereg_v9-clarification-04): the QUANTUM band. NP ⊆ QMA₁
# ⊆ QMA ⊆ PSPACE, so both completeness rungs sit ABOVE NPC and BELOW PSPACE-complete, INCOMPARABLE to the
# PH rungs (recorded here, not forced into the order — the superpoly-APX convention). Two rungs, not one:
# quantum-2-SAT ∈ P vs quantum-k-SAT QMA₁-complete is a permanent/determinant-style near-surface reversal,
# and QMA₁ (perfect completeness) is the class the cited theorem draws — collapsing it into QMA blurs a
# real distinction. `in-QMA` is a MEMBERSHIP value (group-non-membership, Watrous), the quantum analogue of
# `NPI-candidate`: admitted because the placement itself is the theorem, never dressed as completeness.
# ASCII spelling QMA1 = QMA₁. Frozen bytes untouched (no v1/v2/v3.0 row is quantum) — V3_SPEC-scoped.
QMA = "QMA-complete"
QMA1 = "QMA1-complete"
IN_QMA = "in-QMA"

_v3_real = dict(C.EIGHTFOLD_SPEC.charge_real_values)
_v3_real["approximation"] = frozenset(_v3_real["approximation"] | {SUPERPOLY})
_v3_real["decision"] = frozenset(_v3_real["decision"] | {QMA, QMA1, IN_QMA})

# decision partial order gains the quantum band: NPC ≤ QMA1-complete ≤ QMA-complete ≤ PSPACE-complete, and
# the membership value in-QMA ≤ QMA-complete (as NPI-candidate ≤ NPC). No edge to the PH rungs: QMA is not
# known in PH, so the incomparability stays a NON-edge, recorded in the spec note above.
_v3_dpo = list(C.EIGHTFOLD_SPEC.decision_partial_order) + [
    ("NPC", QMA1), (QMA1, QMA), (QMA, "PSPACE-complete"), (IN_QMA, QMA),
]

#: v3 instrument — EIGHTFOLD_SPEC with approximation (+1 rung) and decision (+ the quantum band) extended.
V3_SPEC = dataclasses.replace(C.EIGHTFOLD_SPEC, charge_real_values=_v3_real, decision_partial_order=_v3_dpo)

#: v3 ordinal coding for the approximation column (9 rungs). The kernel/v2 scale stays at 8.
V3_APPROX_ORDER = ["FPTAS", "EPTAS", "PTAS", "APX", "APX-complete", "log-APX", "poly-APX",
                   SUPERPOLY, "inapprox"]

#: Collapse a v3 value to its nearest v2 rung, for the dual-coded re-run clarifications 02 & 04 require.
#: `superpoly-APX` → `inapprox` (its v1 mis-coding); the quantum rungs → `PSPACE-complete` (their nearest
#: v2-expressible upper bound, QMA ⊆ PSPACE), so a v2-coded re-run reproduces the 7-rung decision scale.
def to_v2_coding(value: str) -> str:
    if value == SUPERPOLY:
        return "inapprox"
    if value in (QMA, QMA1, IN_QMA):
        return "PSPACE-complete"
    return value


def validate_v3(entries):
    """Validate v3 entries against the v3 instrument (kernel validator, v3 spec)."""
    from eightfold import atlas
    errs = {}
    for e in entries:
        v = atlas.validate(e, V3_SPEC)
        if v:
            errs[e.problem_id] = v
    return errs


if __name__ == "__main__":
    assert SUPERPOLY in V3_SPEC.charge_real_values["approximation"]
    assert {QMA, QMA1, IN_QMA} <= V3_SPEC.charge_real_values["decision"]
    # the kernel instrument must be untouched — v2's instrument is frozen
    assert SUPERPOLY not in C.EIGHTFOLD_SPEC.charge_real_values["approximation"]
    assert not ({QMA, QMA1, IN_QMA} & C.EIGHTFOLD_SPEC.charge_real_values["decision"]), \
        "kernel decision vocabulary must remain untouched"
    assert len(C.EIGHTFOLD_SPEC.decision_partial_order) == len(_v3_dpo) - 4
    assert to_v2_coding(SUPERPOLY) == "inapprox" and to_v2_coding("PTAS") == "PTAS"
    assert to_v2_coding(QMA) == "PSPACE-complete" and to_v2_coding(QMA1) == "PSPACE-complete"
    print(f"V3_SPEC ok — approximation rungs v3={len(V3_SPEC.charge_real_values['approximation'])} "
          f"(kernel {len(C.EIGHTFOLD_SPEC.charge_real_values['approximation'])}); "
          f"decision rungs v3={len(V3_SPEC.charge_real_values['decision'])} "
          f"(kernel {len(C.EIGHTFOLD_SPEC.charge_real_values['decision'])}, unchanged)")
