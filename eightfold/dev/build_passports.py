#!/usr/bin/env python3
"""Anatomy — the COLUMN PASSPORT audit (SCHEMA §9). Every column earns its passport before S3 freezes.

THE PRIOR QUESTION. The program had census-before-seal (does it vary?) and the qualification bar (can it be
read?). Neither asks the question that came first: **is this column well-defined on its object at all?** A
column can pass coverage, pass variance, and still be measuring an artifact of presentation — which is what
`arity_class` turned out to be, by theorem rather than by accident.

THREE CHECKS PER COLUMN:
  1. INVARIANCE  — invariant / encoding-relative / parameter-relative / corpus-relative, each with the
                   reason pinned I3-style. AUTHORED in `anatomy.PASSPORT_INVARIANCE` (these are theorem
                   judgments, not computations) and audited, not inherited: two landed off-expectation.
  2. VARIANCE    — marginals computed here from the artifact; any cell under the Cochran floor is flagged
                   MACHINE-READABLY, so no future prereg can seal a bet on a starved cell without the
                   artifact itself objecting.
  3. READABILITY — for coded columns, measured kappa from anatomy-instruments.json, printed BESIDE the
                   invariance verdict. The adjacency is the point: low kappa on an encoding-relative column
                   is the theorems talking, not the coders.

CLEAN != ALL-GREEN. `encoding-relative` and `starved` are LEGAL statuses. UNDECLARED ones are not.
"""
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from eightfold import anatomy as AN     # noqa: E402

AT = ROOT / "eightfold" / "results" / "atlas"
OUT = AT / "anatomy-passports.json"

# Variance operationalization, stated so it can be argued with:
MIN_CELL = 5          # Cochran's expected-count floor, applied to observed category counts
MAX_SHARE = 0.90      # a marginal this lopsided supports no contrast even at full coverage
NON_CATEGORICAL = {"poly_fingerprint", "class_size", "reduction_out_degree", "decomposition_facts"}

# THE RESOLUTION LADDER, APPLIED TO COLUMNS. A column starved at full resolution may still carry a bet at a
# coarser one -- exactly how `locality_class` qualified at 3-class after failing at 5. Where a collapse is
# both meaningful and unstarved, it is recorded so the ladder is visible instead of the column reading as
# simply dead. The COLLAPSE must be sealed in a prereg before use, like any resolution choice.
ADMISSIBLE_COLLAPSES = {
    "engine_type": {
        "collapse": "bounded-width yes/no", "counts": {"yes": 3178, "no": 894},
        "starved": False,
        "note": ("the 4-way split is dead (few-subpowers-only = 4/4072) but the BINARY is healthy; grid "
                 "Flag 5 already binds G0 to pose the engine bet as a binary. few-subpowers yes/no is "
                 "77/3995 — thin but above the floor.")},
    "kernel_status": {
        "collapse": "poly-kernel vs no-poly-kernel, WITHIN FPT", "counts": {"poly": 24, "no-poly": 22},
        "starved": False,
        "note": ("the 5-way is starved, but the informative residual Mosaic P6 sealed -- poly vs no-poly "
                 "within FPT -- is 24/22 and healthy. Ledger §6's correction says exactly this: the "
                 "FPT<->kernel equivalence carries no efficiency content, so the binary IS the content.")},
}


def variance_for(column, values):
    """Returns the variance block. Sentinels are excluded from the contrast test but reported."""
    real = [v for v in values if not (isinstance(v, str) and v in AN.SENTINELS)]
    n = len(real)
    if column in NON_CATEGORICAL:
        return {"kind": "non-categorical", "n_cells": len(values), "n_real": n,
                "starved": None, "note": "record- or scalar-valued; no categorical contrast to census"}
    marg = Counter(v for v in real if isinstance(v, str))
    if not marg:
        return {"kind": "categorical", "n_cells": len(values), "n_real": 0, "marginal": {},
                "starved": True, "starved_note": "no real values"}
    thin = {k: c for k, c in marg.items() if c < MIN_CELL}
    top, topc = marg.most_common(1)[0]
    share = topc / n
    starved = bool(thin) or share > MAX_SHARE
    note = []
    if thin:
        note.append(f"cells below the Cochran floor (n<{MIN_CELL}): " +
                    ", ".join(f"{k}={c}" for k, c in sorted(thin.items())))
    if share > MAX_SHARE:
        note.append(f"modal category {top!r} holds {share:.0%} — no contrast posable")
    return {"kind": "categorical", "n_cells": len(values), "n_real": n,
            "marginal": dict(marg.most_common()), "modal_share": round(share, 3),
            "thin_cells": thin, "starved": starved,
            "starved_note": "; ".join(note) if note else None}


def main() -> int:
    art = AT / "anatomy_v1.jsonl"
    rows = [json.loads(l) for l in art.read_text().splitlines() if l.strip()] if art.exists() else []
    byc = {}
    for r in rows:
        for c in r["features"]:
            byc.setdefault(c["feature"], []).append(c["value"])

    inst = json.loads((AT / "anatomy-instruments.json").read_text()) if (AT / "anatomy-instruments.json").exists() else {}
    mos = inst.get("instruments", {}).get("mosaic-3class-v1", {})

    cols, problems = {}, []
    shipped = sorted(AN.COLUMNS)
    reserved = sorted(AN.RESERVED_COLUMNS)
    for col in shipped + ["channelness", "fo_form", "tuple_density", "row_relations"]:
        meta = AN.COLUMNS.get(col)
        inv = AN.PASSPORT_INVARIANCE.get(col)
        if inv is None:
            problems.append(f"{col}: NO INVARIANCE VERDICT — the passport table is incomplete")
            continue
        verdict, prop, why = inv
        p = {"column": col,
             "shipped": col in AN.COLUMNS,
             "universe": meta["universe"] if meta else None,
             "route": meta["route"] if meta else "(reserved — not shipped)",
             "invariance": verdict, "property_of": prop, "invariance_reason": why,
             "bridge_citation": (meta or {}).get("bridge"),
             "variance": variance_for(col, byc.get(col, [])) if col in byc else
                         {"kind": "not-built", "starved": None,
                          "note": "column not present in the artifact (reserved, or pending S2 citations)"},
             "readability": None,
             "admissible_collapse": ADMISSIBLE_COLLAPSES.get(col)}
        # readability: coded columns carry measured kappa; the derived twin of a coded column carries it too
        if col == "locality_class":
            lad = mos.get("resolution_ladder", {})
            p["readability"] = {"instrument": "mosaic-3class-v1",
                                "kappa": lad.get("3-class", {}).get("cohen_kappa"),
                                "demonstrated_resolution": mos.get("demonstrated_resolution"),
                                "bar": mos.get("qualification_threshold", 0.6),
                                "qualifies": bool(mos.get("demonstrated_resolution"))}
        elif col == "arity_class":
            rel = AN.COLUMNS[col].get("reliability", {})
            p["readability"] = {"instrument": "the same two blind coders (never resolved to a sidecar)",
                                "kappa": rel.get("inter_coder_kappa"), "bar": rel.get("qualification_bar"),
                                "qualifies": rel.get("qualifies"),
                                "reading": ("low kappa on an ENCODING-RELATIVE column is the theorems "
                                            "talking, not the coders — there is no invariant fact to read")}
        cols[col] = p

    # completeness gate
    for col in AN.COLUMNS:
        if col not in cols:
            problems.append(f"{col}: shipped column missing from the passport table")

    doc = {"schema": "anatomy-passports/v1",
           "note": ("One passport per column: invariance verdict (is it well-defined on its object?), "
                    "variance census (can it carry a contrast?), readability (can it be read reliably?). "
                    "CLEAN means COMPLETE AND HONEST, not all-green: `encoding-relative` and `starved` are "
                    "legal statuses; undeclared ones are not."),
           "variance_rule": {"min_cell": MIN_CELL, "max_modal_share": MAX_SHARE,
                             "note": "observed-count proxy for Cochran; sentinels excluded from the test"},
           "g0_binding": ("A sealed feature list may draw ONLY from columns whose passport reads "
                          "invariant-or-pinned-relative AND unstarved AND (if coded) qualified. Relativity "
                          "is not disqualifying; UNDECLARED relativity is."),
           "columns": cols}
    OUT.write_text(json.dumps(doc, indent=2) + "\n")

    print(f"wrote {OUT.name}  columns={len(cols)} (shipped {len(AN.COLUMNS)}, reserved {len(reserved)})")
    print(f"\n{'column':<22}{'invariance':<20}{'variance':<28}{'kappa':<8}")
    for col in shipped + ["channelness", "fo_form", "tuple_density", "row_relations"]:
        p = cols.get(col)
        if not p:
            continue
        v = p["variance"]
        vs = ("STARVED" if v.get("starved") else "ok" if v.get("starved") is False else v.get("kind"))
        if v.get("starved") and v.get("thin_cells"):
            vs += f" ({','.join(f'{k}={c}' for k, c in sorted(v['thin_cells'].items()))})"
        k = p["readability"]["kappa"] if p.get("readability") else ""
        mark = "" if p["shipped"] else "  [reserved]"
        print(f"{col:<22}{p['invariance']:<20}{vs:<28}{str(k):<8}{mark}")

    # G0 admissibility, computed from the passports themselves
    print("\nG0 feature-list admissibility (owner binding, 2026-07-25):")
    n_ok = 0
    for col in shipped:
        ok, why = AN.passport_admissible(col, doc)
        n_ok += ok
        line = f"  {'ADMISSIBLE ' if ok else 'EXCLUDED   '}{col}" + ("" if ok else f"  — {why[0].split(': ', 1)[1]}")
        c = cols[col].get("admissible_collapse")
        if not ok and c and not c["starved"]:
            line += f"\n               -> ADMISSIBLE AT A COLLAPSE: {c['collapse']} = {c['counts']}"
        print(line)
    print(f"\n  {n_ok}/{len(shipped)} columns admissible as-is; "
          f"{sum(1 for c in shipped if cols[c].get('admissible_collapse'))} more carry a sealed-collapse route.")

    if problems:
        print(f"\nPASSPORT TABLE INCOMPLETE ({len(problems)}):")
        for x in problems:
            print(f"   {x}")
        return 1
    print("\npassport table COMPLETE — every shipped and reserved column carries verdicts")
    return 0


if __name__ == "__main__":
    sys.exit(main())
