"""Rigidity rank (prereg_v10) — a clone-DERIVED charge: position on the idempotent-Taylor term hierarchy, read
from the polymorphism clone alone (never from terrain — anti-circularity).

Scale (most rigid wins): 4 Maltsev (affine) / 3 near-unanimity or majority / 2 semilattice or other idempotent
Taylor / 1 weak-NU only / 0 no idempotent Taylor term. The 0-/1-valid-only co-clones are tractable via a constant
(NOT an idempotent Taylor term) — recorded at the low end (rank 0, edge) and flagged.
"""

RANK_NAME = {4: "Maltsev (affine)", 3: "near-unanimity/majority (bijunctive)",
             2: "semilattice (Horn/dual-Horn)", 1: "weak-NU only", 0: "no idempotent Taylor term"}


def rigidity_rank(flags):
    """flags: an iterable of profile flags from {'0v','1v','horn','dhorn','bij','aff'}. Returns (rank, name, edge)
    where `edge` marks the 0/1-valid-only tractable-by-constant case."""
    f = set(flags)
    if "aff" in f:
        return 4, RANK_NAME[4], False
    if "bij" in f:
        return 3, RANK_NAME[3], False
    if "horn" in f or "dhorn" in f:
        return 2, RANK_NAME[2], False
    if f & {"0v", "1v"}:
        return 0, "tractable-by-constant, no idempotent Taylor term (edge)", True
    return 0, "no Taylor term (NP-hard)", False
