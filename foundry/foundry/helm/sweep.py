"""Candidate generation — Helm §2. Mechanical enumeration over the catalog and its joins.

EVERY CANDIDATE IS BORN `disclosed-prior`. The database is published ground, so nothing found in it is
ever a finding (Helm §0.1). What a sweep produces is a QUESTION with a direction attached, and the
direction is worth something only because the ground it will be scored on does not exist yet.

THE EYEBALL BAN (Helm §8): no candidate enters because something looked interesting. A candidate enters
by enumeration or by bank import, and nothing else. That is why this file enumerates every descriptor
pair rather than the promising ones — the denominator is the product, and a denominator chosen after
looking is not a denominator.

THE FORKING-PATHS COUNT IS RECORDED AT BIRTH. Each candidate carries how many siblings the sweep
enumerated alongside it. A multiple-comparisons correction computed later from a number someone
remembers is the thing this replaces.

THE TYPING BOUNDARY (F2) HOLDS HERE BY CONSTRUCTION. Charges enter only through `JOIN charges USING
(problem_id)` — as FIXED ROW LABELS. There is no query in this file in which a charge varies along a
ramp, because a charge is a property of a problem and a ramp position is a property of a reading.
"""
from __future__ import annotations

import hashlib
import json
from itertools import combinations

GENERATOR_VERSION = "sweep/v1"

# The descriptors a co-movement candidate may pair. `kink_sharpness` is deliberately INCLUDED so that
# screen 1 can visibly reject it: the catalog stamps it seal-prohibited for want of a typed null, and a
# screen that never fires on real input is a screen nobody has tested.
NUMERIC = ["excess_ref", "excess_min", "excess_max", "max_excursion_sd", "overlap_ref",
           "overlap_slope", "bimodality_max", "r_ref", "insufficient_share", "kink_sharpness"]
CATEGORICAL = ["traj_class", "slope_sign", "bimodal_flag"]

MIN_N = 8            # below this a rank correlation is not a statistic, it is a rumour
MIN_LEVELS = 2       # an association needs at least two levels on each axis

# A NULL FOR THE DISCLOSED STATISTIC IS NOT A NULL FOR THE SEALED BET, and conflating the two is the
# subtlest way a screen stops screening. An extremal's in-sample null answers "is this cell unusual
# among the cells we have?"; the bet it would become answers "does the frontier reproduce it?", and
# that second question needs an exchangeability model over frontier cells that v1 has not pinned.
# The catalog's transition group sets the precedent exactly: no candidate until its null is pinned.
NO_EXTREMAL_NULL = (
    "the declared null types the DISCLOSED extremal's position among published cells, not a frontier "
    "prediction. Typing the reproduction bet needs an exchangeability model over frontier cells that "
    "v1 has not pinned — and inventing one inside the sweep would be the change-point precedent "
    "(Helm §3.1) broken by the component that exists to enforce it.")


# ── statistics, pure ────────────────────────────────────────────────────────────────────────────────
def _ranks(v):
    order = sorted(range(len(v)), key=lambda i: v[i])
    r = [0.0] * len(v)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
            j += 1
        avg = (i + j) / 2 + 1
        for k in range(i, j + 1):
            r[order[k]] = avg
        i = j + 1
    return r


def spearman(xs, ys):
    """Rank correlation with average ranks for ties. Returns None where it is undefined."""
    if len(xs) < 3:
        return None
    a, b = _ranks(xs), _ranks(ys)
    n = len(a)
    ma, mb = sum(a) / n, sum(b) / n
    num = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    da = sum((x - ma) ** 2 for x in a) ** 0.5
    db = sum((y - mb) ** 2 for y in b) ** 0.5
    return None if da == 0 or db == 0 else num / (da * db)


def cramers_v(pairs):
    """Cramér's V on a contingency of (row_label, col_label) pairs."""
    rows = sorted({p[0] for p in pairs})
    cols = sorted({p[1] for p in pairs})
    if len(rows) < MIN_LEVELS or len(cols) < MIN_LEVELS:
        return None
    n = len(pairs)
    obs = {(r, c): 0 for r in rows for c in cols}
    for p in pairs:
        obs[p] += 1
    rt = {r: sum(obs[(r, c)] for c in cols) for r in rows}
    ct = {c: sum(obs[(r, c)] for r in rows) for c in cols}
    chi2 = 0.0
    for r in rows:
        for c in cols:
            e = rt[r] * ct[c] / n
            if e > 0:
                chi2 += (obs[(r, c)] - e) ** 2 / e
    return (chi2 / (n * min(len(rows) - 1, len(cols) - 1))) ** 0.5


def _cid(kind: str, *parts) -> str:
    return f"{kind}:" + hashlib.sha256("|".join(map(str, parts)).encode()).hexdigest()[:12]


# ── the sweep ───────────────────────────────────────────────────────────────────────────────────────
def _families(con):
    return [r[0] for r in con.execute(
        "SELECT DISTINCT p.family FROM problems p JOIN catalog c ON c.problem_id = p.problem_id "
        "WHERE p.family IS NOT NULL ORDER BY p.family")]


def co_movement(con):
    """Every dial-pair rank correlation across trajectories, per family and pooled."""
    out = []
    groups = [(None, "pooled")] + [(f, f) for f in _families(con)]
    for a, b in combinations(NUMERIC, 2):
        for fam, label in groups:
            sql = (f"SELECT c.problem_id, c.{a}, c.{b} FROM admissible_catalog c "
                   f"JOIN problems p ON p.problem_id = c.problem_id "
                   f"WHERE c.{a} IS NOT NULL AND c.{b} IS NOT NULL"
                   + (f" AND p.family = '{fam}'" if fam else "") + " ORDER BY 1,2,3")
            rows = con.execute(sql).fetchall()
            rho = spearman([r[1] for r in rows], [r[2] for r in rows]) if len(rows) >= MIN_N else None
            out.append({
                "kind": "co-movement", "candidate_id": _cid("comov", a, b, label),
                "statistic": f"Spearman rho({a}, {b}) over {label} trajectories",
                "descriptors": [a, b], "group": label,
                "generating_query": sql, "disclosed": rho,
                "n": len(rows), "n_clusters": len({r[0] for r in rows}),
                "null": ("cluster permutation: whole problems' descriptor vectors are shuffled, so "
                         "within-problem dependence between a row's cells is preserved under the null"),
                "frontier_null": ("the same cluster permutation, applied to the reserved rows' cells "
                                  "once they exist — the statistic and its null are the same object "
                                  "on the frontier as on published ground"),
                "stamp": "disclosed-prior"})
    return out


def association(con):
    """descriptor x charge-label associations. Charges join in as FIXED ROW LABELS (typing boundary)."""
    out = []
    charges = [r[0] for r in con.execute(
        "SELECT charge FROM charges GROUP BY charge HAVING COUNT(DISTINCT value) >= 2 ORDER BY charge")]
    for ch in charges:
        for d in CATEGORICAL:
            sql = (f"SELECT ch.value, c.{d} FROM admissible_catalog c "
                   f"JOIN charges ch ON ch.problem_id = c.problem_id "
                   f"WHERE ch.charge = '{ch}' AND c.{d} IS NOT NULL ORDER BY 1,2")
            rows = con.execute(sql).fetchall()
            v = cramers_v([(str(r[0]), str(r[1])) for r in rows]) if len(rows) >= MIN_N else None
            out.append({
                "kind": "association", "candidate_id": _cid("assoc", ch, d),
                "statistic": f"Cramer's V({d}, charge={ch})", "descriptors": [d],
                "charge": ch, "group": "pooled",
                "generating_query": sql, "disclosed": v,
                "n": len(rows), "n_clusters": len({r[0] for r in con.execute(
                    f"SELECT c.problem_id FROM admissible_catalog c JOIN charges ch "
                    f"ON ch.problem_id = c.problem_id WHERE ch.charge = '{ch}'").fetchall()}),
                "null": "label permutation within the charge column, clustered by problem",
                "frontier_null": ("the same label permutation on the reserved rows' cells, with the "
                                  "charge joining in as a fixed row label exactly as it does here"),
                "charge_is_a_fixed_row_label": True,
                "stamp": "disclosed-prior"})

    # flavour_order — derived in SQL rather than stored, since the loader keeps rollups out of the db
    sql = ("SELECT problem_id, region, flavour FROM admissible_catalog "
           "ORDER BY problem_id, region, excess_ref")
    order = {}
    for pid, reg, fl in con.execute(sql):
        order.setdefault((pid, reg), []).append(fl)
    for ch in charges:
        vals = dict(con.execute(f"SELECT problem_id, value FROM charges WHERE charge = '{ch}'"))
        pairs = [(str(vals[p]), "<".join(fl)) for (p, _r), fl in sorted(order.items())
                 if p in vals and len(fl) >= 2]
        v = cramers_v(pairs) if len(pairs) >= MIN_N else None
        out.append({
            "kind": "association", "candidate_id": _cid("assoc", ch, "flavour_order"),
            "statistic": f"Cramer's V(flavour_order, charge={ch})", "descriptors": ["flavour_order"],
            "charge": ch, "group": "pooled",
            "generating_query": sql + f"   -- joined to charges WHERE charge = '{ch}'",
            "disclosed": v, "n": len(pairs), "n_clusters": len({p for p, _ in order}),
            "null": "label permutation within the charge column, clustered by problem",
            "charge_is_a_fixed_row_label": True, "stamp": "disclosed-prior"})
    return out


def anomaly(con):
    """Descriptor extremals, fingerprint outliers, residual unexplained zeros.

    EXPRESSION-FIRST (Helm §8): an extremal candidate carries the cell that produced it, so the first
    question asked of it is what expression generated the number — not whether the number is unusual."""
    out = []
    for d in NUMERIC:
        for direction, order in (("max", "DESC"), ("min", "ASC")):
            sql = (f"SELECT problem_id, region, flavour, {d} FROM admissible_catalog "
                   f"WHERE {d} IS NOT NULL ORDER BY {d} {order}, problem_id, region, flavour LIMIT 5")
            rows = con.execute(sql).fetchall()
            if not rows:
                continue
            allv = [r[0] for r in con.execute(
                f"SELECT {d} FROM admissible_catalog WHERE {d} IS NOT NULL")]
            if len(allv) < MIN_N:
                continue
            mu = sum(allv) / len(allv)
            sd = (sum((x - mu) ** 2 for x in allv) / len(allv)) ** 0.5
            top = rows[0]
            out.append({
                "kind": "anomaly", "candidate_id": _cid("anom", d, direction),
                "statistic": f"{direction} of {d}: {top[0]} / {top[1]} / {top[2]} = {top[3]}",
                "descriptors": [d], "group": "pooled",
                "generating_query": sql,
                "disclosed": (abs(top[3] - mu) / sd) if sd > 0 else None,
                "disclosed_units": "SD from the pooled mean",
                "cell": {"problem_id": top[0], "region": top[1], "flavour": top[2], "value": top[3]},
                "expression_first": ("adjudicate what expression produced this cell BEFORE asking "
                                     "whether the value is surprising"),
                "n": len(allv), "n_clusters": len({r[0] for r in con.execute(
                    f"SELECT problem_id FROM admissible_catalog WHERE {d} IS NOT NULL")}),
                "null": "pooled descriptor distribution; extremal position under cluster permutation",
                "frontier_null": None,
                "why_no_frontier_null": NO_EXTREMAL_NULL,
                "stamp": "disclosed-prior"})

    sql = ("SELECT problem_id, region, flavour, excess_ref FROM admissible_catalog "
           "WHERE excess_ref = 0.0 ORDER BY problem_id, region, flavour")
    zeros = con.execute(sql).fetchall()
    out.append({
        "kind": "anomaly", "candidate_id": _cid("anom", "residual-zeros"),
        "statistic": "count of cells reading excess_ref exactly 0.0",
        "descriptors": ["excess_ref"], "group": "pooled", "generating_query": sql,
        "disclosed": float(len(zeros)), "disclosed_units": "cells",
        "cells": [{"problem_id": z[0], "region": z[1], "flavour": z[2]} for z in zeros[:20]],
        "n": len(zeros), "n_clusters": len({z[0] for z in zeros}),
        "null": "the zero-hunt's adjudication vocabulary — every zero is forced, thin, or unexplained",
        "frontier_null": None, "why_no_frontier_null": NO_EXTREMAL_NULL,
        "expression_first": "each zero is adjudicated expression-first before it counts as a residual",
        "stamp": "disclosed-prior"})

    sql = ("SELECT traj_class, slope_sign, bimodal_flag, COUNT(*) AS n FROM admissible_catalog "
           "GROUP BY 1,2,3 ORDER BY n ASC, 1, 2, 3")
    fps = con.execute(sql).fetchall()
    rare = [f for f in fps if f[3] <= 2]
    out.append({
        "kind": "anomaly", "candidate_id": _cid("anom", "fingerprint-outliers"),
        "statistic": "(traj_class, slope_sign, bimodal_flag) combinations occurring at most twice",
        "descriptors": CATEGORICAL, "group": "pooled", "generating_query": sql,
        "disclosed": float(len(rare)), "disclosed_units": "rare combinations",
        "cells": [{"fingerprint": f[:3], "n": f[3]} for f in rare],
        "n": sum(f[3] for f in fps), "n_clusters": len({r[0] for r in con.execute(
            "SELECT problem_id FROM admissible_catalog")}),
        "null": "multinomial over observed fingerprint frequencies",
        "frontier_null": None, "why_no_frontier_null": NO_EXTREMAL_NULL,
        "stamp": "disclosed-prior"})
    return out


def bank_imports(bank_md):
    """Every banked question re-expressed as a candidate record, so the bank and the sweep merge into
    ONE ledger (Helm §2). A question living in a markdown file and a question living in the sweep are
    two ledgers that will disagree; this makes them one."""
    out = []
    if not bank_md.exists():
        return out
    for line in bank_md.read_text().splitlines():
        if not line.startswith("## Q"):
            continue
        head = line[3:].strip()
        qid = head.split(" ")[0].rstrip("—").strip()
        rest = head[len(qid):].strip(" —")
        closed = any(t in rest.upper() for t in ("CLOSED", "RESOLVED"))
        out.append({
            "kind": "bank-import", "candidate_id": _cid("bank", qid, rest[:40]),
            "statistic": f"Q{qid.lstrip('Q')}: {rest}", "descriptors": [], "group": "bank",
            "generating_query": f"-- bank import from {bank_md.name}, heading '## {head}'",
            "disclosed": None, "n": 0, "n_clusters": 0,
            "bank_status": "CLOSED" if closed else "OPEN",
            "null": None,
            "no_enumeration_denominator": ("a bank import was not enumerated by this sweep, so it "
                                           "carries no forking-paths denominator of its own"),
            "stamp": "disclosed-prior"})
    return out


def sweep(con, bank_md):
    """The full sweep. Returns (candidates, provenance)."""
    cands = co_movement(con) + association(con) + anomaly(con) + bank_imports(bank_md)
    by_kind = {}
    for c in cands:
        by_kind.setdefault((c["kind"], c["group"]), []).append(c)
    for (_k, _g), members in by_kind.items():
        for c in members:
            c["n_siblings"] = len(members)          # the forking-paths denominator, recorded AT BIRTH
    for c in cands:
        c["sweep_total"] = len(cands)
    prov = {"generator_version": GENERATOR_VERSION,
            "n_candidates": len(cands),
            "by_kind": {k: sum(1 for c in cands if c["kind"] == k)
                        for k in sorted({c["kind"] for c in cands})}}
    return cands, prov


def db_hashes(con, db_path):
    srcs = dict((r[0], r[1]) for r in con.execute("SELECT artifact, sha256 FROM sources"))
    return {"db_sha256": hashlib.sha256(db_path.read_bytes()).hexdigest(), "sources": srcs}


def canonical(cands):
    return json.dumps(sorted(cands, key=lambda c: c["candidate_id"]), sort_keys=True,
                      separators=(",", ":"))
