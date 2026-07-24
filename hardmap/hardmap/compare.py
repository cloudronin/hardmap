"""Tolerance comparison for repro claims.

A claim's ``expected`` maps field -> expected value; its ``tolerance`` maps
field -> a spec (or the literal string ``"exact"`` for the whole claim). A field
passes per its spec:

    exact            actual == expected            (strings, ints, booleans)
    {abs: x}         |actual - expected| <= x
    {rel: x}         |actual - expected| <= x*|expected|
    {max: x}         actual <= x                    (upper bound, e.g. p-values)
    {min: x}         actual >= x
    {range: [lo,hi]} lo <= actual <= hi             (e.g. CI membership, Jaccard band)
"""
from __future__ import annotations


def compare(actual, expected, tol) -> tuple[bool, str]:
    """Return (ok, human-readable detail)."""
    if tol in (None, "exact"):
        ok = actual == expected
        return ok, f"{actual!r} {'==' if ok else '!='} {expected!r}"
    if not isinstance(tol, dict):
        raise ValueError(f"bad tolerance spec: {tol!r}")
    a = float(actual)
    if "max" in tol:
        return a <= tol["max"], f"{a:.6g} <= {tol['max']}"
    if "min" in tol:
        return a >= tol["min"], f"{a:.6g} >= {tol['min']}"
    if "range" in tol:
        lo, hi = tol["range"]
        return lo <= a <= hi, f"{lo} <= {a:.6g} <= {hi}"
    if "abs" in tol:
        e = float(expected)
        return abs(a - e) <= tol["abs"], f"|{a:.6g} - {e:.6g}| <= {tol['abs']}"
    if "rel" in tol:
        e = float(expected)
        return abs(a - e) <= tol["rel"] * abs(e), f"|{a:.6g} - {e:.6g}| <= {tol['rel']}*|{e:.6g}|"
    raise ValueError(f"unknown tolerance keys: {list(tol)}")


def check_claim(result: dict, expected: dict, tolerance) -> list[tuple[str, bool, str]]:
    """Compare every expected field against the adapter's result.

    Returns one (field, ok, detail) row per expected field. Missing fields fail.
    """
    rows = []
    for field, exp in expected.items():
        if field not in result:
            rows.append((field, False, f"missing from result (have {sorted(result)})"))
            continue
        tol = tolerance if tolerance in (None, "exact") else tolerance.get(field, "exact")
        ok, detail = compare(result[field], exp, tol)
        rows.append((field, ok, detail))
    return rows
