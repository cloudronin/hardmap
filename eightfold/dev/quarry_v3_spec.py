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

_v3_real = dict(C.EIGHTFOLD_SPEC.charge_real_values)
_v3_real["approximation"] = frozenset(_v3_real["approximation"] | {SUPERPOLY})

#: v3 instrument — EIGHTFOLD_SPEC with the approximation column extended by one rung.
V3_SPEC = dataclasses.replace(C.EIGHTFOLD_SPEC, charge_real_values=_v3_real)

#: v3 ordinal coding for the approximation column (9 rungs). The kernel/v2 scale stays at 8.
V3_APPROX_ORDER = ["FPTAS", "EPTAS", "PTAS", "APX", "APX-complete", "log-APX", "poly-APX",
                   SUPERPOLY, "inapprox"]

#: Collapse a v3 value to its nearest v2 rung, for the dual-coded re-run clarification-02 requires.
#: `superpoly-APX` collapses to `inapprox` (its v1 mis-coding), so the re-run reproduces the v2 scale.
def to_v2_coding(value: str) -> str:
    return "inapprox" if value == SUPERPOLY else value


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
    assert SUPERPOLY not in C.EIGHTFOLD_SPEC.charge_real_values["approximation"], \
        "kernel vocabulary must remain untouched — v2's instrument is frozen"
    assert to_v2_coding(SUPERPOLY) == "inapprox" and to_v2_coding("PTAS") == "PTAS"
    print(f"V3_SPEC ok — approximation rungs: v3={len(V3_SPEC.charge_real_values['approximation'])}, "
          f"kernel/v2={len(C.EIGHTFOLD_SPEC.charge_real_values['approximation'])} (unchanged)")
