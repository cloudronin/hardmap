"""Relation-level features (prereg_v11, Sprint 4.6) — properties of the SPECIFIC relation that the polymorphism
clone discards, and that (unlike clone invariants) vary within a co-clone. `tuple_dispersion` is the feature that
carried experiment B (relation-level terrain prediction): a relation whose allowed tuples sit far apart in Hamming
space propagates that spread to its instances' solution sets.
"""
import statistics as st


def density(R):
    """|R| / |D|^arity — the fraction of the cube the relation allows. (Sealed sign NEGATIVE in prereg_v11; it
    FAILED — the physics density->clustering mechanism does not transpose to relation-density here.)"""
    a = len(next(iter(R)))
    dom = len({v for t in R for v in t}) or 2
    return round(len(R) / dom ** a, 3)


def tuple_dispersion(R):
    """Mean pairwise Hamming distance among R's tuples, normalized by arity. Sealed sign POSITIVE (prereg_v11) —
    matched; the relation-level predictor of measured ruggedness (held-out marginal +0.74)."""
    ts = list(R)
    a = len(ts[0])
    if len(ts) < 2:
        return 0.0
    ds = [sum(1 for x, y in zip(ts[i], ts[j]) if x != y) / a
          for i in range(len(ts)) for j in range(i + 1, len(ts))]
    return round(st.mean(ds), 3)


# ── the B evaluation harness: linear-fit R2 + permutation null (fixed; hand-count selftest in CI) ─────────────
def fit_r2(X, y):
    import numpy as np
    X1 = np.column_stack([np.ones(len(y)), X])
    beta, *_ = np.linalg.lstsq(X1, y, rcond=None)
    pred = X1 @ beta
    ss_res = float(np.sum((y - pred) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    return (1 - ss_res / ss_tot if ss_tot else 0.0), beta


def perm_null_p(X, y, n_perm=5000, seed=42):
    """p = fraction of feature<->outcome shuffles whose refit R2 reaches the real R2 (fixed harness)."""
    import numpy as np
    r2, _ = fit_r2(X, y)
    rng = np.random.default_rng(seed)
    ge = sum(1 for _ in range(n_perm) if fit_r2(X, rng.permutation(y))[0] >= r2 - 1e-12)
    return round((ge + 1) / (n_perm + 1), 4)


def selftest_perm(n_perm=5000):
    """Hand-count: a PERFECT linear predictor gives R2=1; a permuted refit essentially never reaches it, so
    perm_p ~ 1/(n_perm+1) (<0.01). This is the CI guard on the B null harness."""
    import numpy as np
    X = np.array([[i] for i in range(8)], float)
    y = np.array([float(i) for i in range(8)])
    r2, _ = fit_r2(X, y)
    p = perm_null_p(X, y, n_perm=n_perm, seed=1)
    ok = r2 > 0.999 and p < 0.01
    print(f"B perm selftest: perfect-linear R2={round(r2, 3)} perm_p={p} -> {'PASSED' if ok else 'FAILED'}")
    return 0 if ok else 1
