"""Strata S2 — the derivation pass. Reads the FROZEN atlas.jsonl (read-only), derives the three additions under the
rules SEALED in results/atlas/Strata-SCHEMA.md, writes atlas_v2.jsonl + strata_judged.jsonl, validates every v2 row
through the composing validator, and reports the derived/judged split (R-2: a LOW judged fraction is a red flag).

Crisp rules only derive; anything not crisply extractable from the per-cell prose goes to `judged` for owner review
(S3). No value is ever changed (a wrong v1 value is an S3 v2.1 candidate, not touched here).

Run: PYTHONPATH=<eightfold-dir> python dev/build_strata.py
"""
import hashlib
import json
import re
from collections import Counter

from eightfold import atlas, strata

SENTINELS = {"open", "unmeasured", "n.a."}

# crisp objective lexicon from the approximation canonical_task lead (only the unambiguous cases derive)
_MAX_CSP = re.compile(r"^\s*MAX-(SAT|2SAT|3SAT|HORN-SAT|NAE-SAT|DICUT|CUT|3-LIN|1-IN-3-SAT|CIRCUIT-SAT|K-SAT)\b", re.I)
_MIN_ONES = re.compile(r"^\s*MIN-VC\b", re.I)                              # minimise the vertex set = Min-Ones
_MAX_ONES = re.compile(r"^\s*MAX-(CLIQUE|IS|INDEPENDENT-SET)\b", re.I)     # maximise the selected set = Max-Ones
_DEGENERACY = re.compile(r"\b(trivial|degenerate|0-valid|1-valid|vacuous)\b", re.I)


def _cell(row, ch):
    return next(c for c in row["charges"] if c["charge"] == ch)


def _object_witness(row, charge):
    """R-1 witness — faithful to 'a sibling whose reality establishes the object exists', NOT merely same-level. The
    structural object-existence relations: counting's #-version is well-defined once the decision problem is (that IS
    counting's definition — count the decision witnesses); parallelization's within-P question exists once decision
    does (an `open`, not `n.a.`, cell already implies decision∈P by E2); the two objective-level charges witness each
    other (R-1's own example); landscape's ensemble exists once average_case does (samplability is the residual
    judgment). `average_case` and `proof_size` have NO such structural sibling → they stay judged."""
    real = lambda c: _cell(row, c)["value"] not in SENTINELS
    if charge in ("counting", "parallelization") and real("decision"):
        return "decision"
    if charge == "approximation" and real("parameterized"):
        return "parameterized"
    if charge == "parameterized" and real("approximation"):
        return "approximation"
    if charge == "landscape" and real("average_case"):
        return "average_case"
    return None


def derive_applicability(row, cell):
    """-> (applicability, reason, provenance). Sealed rules; judged where not crisp."""
    ch, v, t, p = cell["charge"], cell["value"], cell.get("canonical_task") or "", cell.get("perspective")
    fam = row.get("problem_family")
    if v == "n.a.":
        return "n.a.", t, "derived"
    if v in ("open", "unmeasured"):
        sib = _object_witness(row, ch)
        if sib:
            return "defined-informative", f"object existence witnessed by populated {sib!r} (R-1 structural sibling); value {v}", "derived"
        return "defined-informative", f"value {v}; no structural sibling witnesses the object — owner confirm (R-1)", "judged"
    # real value
    if _DEGENERACY.search(t):
        return "defined-trivial", f"degeneracy signal in canonical_task: {t[:60]!r}", "judged"
    if ch == "parameterized" and fam == "graph":
        return "ambiguous", f"graph-family parameterization (treewidth vs solution-size competes); perspective={p!r}", "judged"
    if p and (";" in p or " vs " in p.lower()):
        return "ambiguous", f"perspective names competing framings: {p!r}", "judged"
    return "defined-informative", f"real value {v}; single natural framing", "derived"


def derive_objective(row):
    """-> (objective, reason, provenance) from the approximation canonical_task lead. Only crisp cases derive."""
    ap = _cell(row, "approximation")
    if ap["value"] == "n.a.":
        return "none", ap.get("canonical_task") or "approximation n.a.", "derived"
    t = ap.get("canonical_task") or ""
    if _MAX_CSP.search(t):
        return "Max-CSP", f"MAX-CSP objective from {t[:40]!r}", "derived"
    if _MIN_ONES.search(t):
        return "Min-Ones", f"MIN-VC = minimise selected set from {t[:40]!r}", "derived"
    if _MAX_ONES.search(t):
        return "Max-Ones", f"MAX-CLIQUE/IS = maximise selected set from {t[:40]!r}", "derived"
    return None, f"objective not crisply extractable from prose lead: {t[:60]!r}", "judged"


def derive_parameterization(row):
    """-> (parameterization, pin_theorem, reason, provenance) from the parameterized perspective. Crisp only."""
    pm = _cell(row, "parameterized")
    if pm["value"] == "n.a.":
        return "none", None, pm.get("canonical_task") or "parameterized n.a.", "derived"
    p = pm.get("perspective")
    theorem = (pm.get("provenance") or {}).get("citation")
    if not p:
        return None, theorem, "parameterized real value without a perspective", "judged"
    pl = p.lower()
    if ";" in p or " vs " in pl:
        return "other", theorem, f"competing parameterizations named: {p!r}", "judged"
    if "solution size" in pl:
        return "solution size", theorem, f"perspective={p!r}", "derived"
    if "treewidth" in pl:
        return "treewidth", theorem, f"perspective={p!r}", "derived"
    return "other", theorem, f"single named parameter {p!r} (mapping to 'other' — owner confirm)", "judged"


def main():
    rows = [json.loads(line) for line in atlas.resolve_atlas_path().read_text().splitlines() if line.strip()]
    strata_by_row, judged = {}, []
    prov_counter = Counter()

    for row in rows:
        pid = row["problem_id"]
        cell_meta = {}
        for cell in row["charges"]:
            ap, reason, prov = derive_applicability(row, cell)
            cell_meta[cell["charge"]] = {"applicability": ap, "applicability_reason": reason,
                                         "applicability_provenance": prov}
            prov_counter[("applicability", prov)] += 1
            if prov == "judged":
                judged.append({"problem_id": pid, "charge": cell["charge"], "field": "applicability",
                               "proposed": ap, "reason": reason, "value": cell["value"],
                               "canonical_task": cell.get("canonical_task"), "perspective": cell.get("perspective")})

        obj, obj_reason, obj_prov = derive_objective(row)
        par, theorem, par_reason, par_prov = derive_parameterization(row)
        pin_prov = "derived" if (obj_prov == "derived" and par_prov == "derived") else "judged"
        row_pins = {"objective": obj, "parameterization": par, "pin_theorem": theorem, "pin_provenance": pin_prov}
        prov_counter[("objective", obj_prov)] += 1
        prov_counter[("parameterization", par_prov)] += 1
        for field, val, rsn, pv in (("objective", obj, obj_reason, obj_prov), ("parameterization", par, par_reason, par_prov)):
            if pv == "judged":
                judged.append({"problem_id": pid, "field": field, "proposed": val, "reason": rsn})

        strata_by_row[pid] = {"row_pins": row_pins, "cell_meta": cell_meta}

    dest, merged = strata.write_atlas_v2(strata_by_row)

    # every v2 row must validate clean through the composing validator (v1 gates + strata gates)
    bad = [(r["problem_id"], strata.validate_entry_v2(r)) for r in merged]
    bad = [(pid, e) for pid, e in bad if e]

    judged_path = atlas.DEFAULT_PATH.parent / "strata_judged.jsonl"
    with judged_path.open("w") as f:
        for j in judged:
            f.write(json.dumps(j, ensure_ascii=False) + "\n")

    sha = hashlib.sha256(dest.read_bytes()).hexdigest()

    # ── report ──
    total_cells = sum(prov_counter[("applicability", p)] for p in ("derived", "judged"))
    ap_judged = prov_counter[("applicability", "judged")]
    print(f"atlas_v2.jsonl written: {len(merged)} rows  sha256={sha}")
    print(f"validation: {len(bad)} rows with errors (must be 0)")
    for pid, e in bad[:10]:
        print("   ", pid, e)
    print(f"\n=== derived/judged split (R-2: a LOW judged fraction is a RED FLAG) ===")
    for field in ("applicability", "objective", "parameterization"):
        d = prov_counter[(field, "derived")]
        j = prov_counter[(field, "judged")]
        tot = d + j
        print(f"  {field:16}: derived {d:3}  judged {j:3}  ({100*j/tot:.0f}% judged of {tot})")
    print(f"\n  applicability judged fraction = {100*ap_judged/total_cells:.0f}%  "
          f"({'OK — reading prose' if ap_judged/total_cells >= 0.10 else 'RED FLAG — likely pattern-matching, re-examine'})")
    print(f"  judged review list: {len(judged)} entries -> {judged_path.name}")


if __name__ == "__main__":
    main()
