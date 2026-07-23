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

# Cat-3 objective-TYPE lexicon (sealed in Strata-SCHEMA.md §4); match the FULL canonical_task — the MIN-/MAX- lead
# names the PROBLEM, not the objective TYPE. Order matters (Max-CSP before the numeric CUT-family).
# Order matters: a recognised numeric/structural objective wins over `weighted` — S3 fix, weighted requires the
# OBJECTIVE to be a weight sum (knapsack: maximise value), not merely weighted INPUT (partitioning: min discrepancy,
# a derived numeric imbalance → global-numeric). So `weighted` is last and narrowed to KNAPSACK/SUBSET-SUM.
_OBJ_RULES = [
    ("Max-CSP",        re.compile(r"\bMAX-(SAT|2SAT|3SAT|HORN-SAT|NAE-SAT|DICUT|CUT|3-LIN|1-IN-3-SAT|CIRCUIT-SAT|K-SAT)\b", re.I)),
    ("Min-Ones",       re.compile(r"\bMIN-(VC|DOMINATING-SET|SET-COVER|HITTING-SET|FVS|CONNECTED-VC|EDS|ODD-CYCLE-TRANSVERSAL|INDEPENDENT-DOMINATING)\b", re.I)),
    ("Max-Ones",       re.compile(r"\bMAX-(CLIQUE|IS|INDEPENDENT-SET|LEAF|K-SET-PACKING)\b", re.I)),
    ("global-numeric", re.compile(r"\b(TSP|CHROMATIC|STEINER|DISCREPANCY|BANDWIDTH|MAKESPAN|BIN-PACKING|K-CENTER|TREEWIDTH|TREEDEPTH|BISECTION|MULTIWAY-CUT|LONGEST-PATH)\b", re.I)),
    ("weighted",       re.compile(r"\b(KNAPSACK|SUBSET-SUM)\b", re.I)),
]

# S3 Cat-3 owner assignments for the rows the lexicon flagged (never defaulted). Reasons recorded per the owner ruling.
_OBJ_OWNER = {
    "capacitated-vertex-cover": "Min-Ones", "partial-vertex-cover": "Min-Ones", "planar-vertex-cover": "Min-Ones",
    "d-hitting-set": "Min-Ones", "odd-cycle-transversal": "Min-Ones", "directed-feedback-vertex-set": "Min-Ones",
    "cluster-vertex-deletion": "Min-Ones", "cluster-editing": "Min-Ones", "planar-dominating-set": "Min-Ones",
    "multiway-cut": "global-numeric", "group-steiner-tree": "global-numeric", "directed-steiner-tree": "global-numeric",
    "k-median": "global-numeric", "job-shop-scheduling": "global-numeric", "quadratic-assignment": "global-numeric",
    "kemeny-rank-aggregation": "global-numeric", "feedback-arc-set-tournament": "global-numeric",
    "shortest-common-superstring": "global-numeric", "dnf-minimization": "global-numeric", "bin-covering": "global-numeric",
    "shortest-vector-svp": "global-numeric", "closest-vector-cvp": "global-numeric", "edge-coloring": "global-numeric",
    "treewidth": "global-numeric", "cutwidth": "global-numeric", "minimum-fill-in": "global-numeric", "min-bisection": "global-numeric",
    "three-dimensional-matching": "Max-Ones", "max-coverage": "Max-Ones", "densest-k-subgraph": "Max-Ones",
}
_OBJ_OWNER_REASON = {
    "treewidth": "structural-parameter objective", "cutwidth": "structural-parameter objective", "min-bisection": "structural-parameter objective",
    "minimum-fill-in": "structural-parameter objective (minimises added fill edges, but the quantity is a property of the decomposition, not a selected set)",
    "edge-coloring": "chromatic quantity (# colors), parallel to chromatic",
    "max-coverage": "constrained-cardinality variant (maximise coverage s.t. |S|<=k)",
    "densest-k-subgraph": "constrained-cardinality variant (maximise density s.t. |S|=k)",
}
_DEGENERACY = re.compile(r"\b(trivial|degenerate|0-valid|1-valid|vacuous)\b", re.I)

_ALGEBRAIC_NT = {"algebraic", "number-theoretic"}                 # Cat 1: no canonical random ensemble
_REFUTATION_FAMILIES = {"logic-proof", "sat-csp"}                 # Cat 5: rows that can be an unsat instance family
_GRADIENT_WITNESSES = {"vertex-cover", "clique", "independent-set"}   # Cat 2: charge flips with parameterization
_NOPERSP_PARAM = {"number-partitioning": "solution size", "exact-cover-x3c": "solution size",
                  "k-center": "solution size"}                   # Cat 4: owner-assigned (k-center: k = # centers)


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
    """-> (applicability, reason, provenance). Sealed S1 rules + S3 owner rulings (Strata-SCHEMA §4)."""
    ch, v, t, p = cell["charge"], cell["value"], cell.get("canonical_task") or "", cell.get("perspective")
    fam, pid = row.get("problem_family"), row["problem_id"]
    if v == "n.a.":
        return "n.a.", t, "derived"
    if v in ("open", "unmeasured"):
        if ch == "average_case" and fam in _ALGEBRAIC_NT:                                    # Cat 1 exception
            return "ambiguous", f"no canonical ensemble: a random {fam} instance is a distribution-over-integers modeling decision, not a given (S3 Cat 1)", "judged"
        if ch == "proof_size" and fam not in _REFUTATION_FAMILIES:                           # Cat 5: not a refutation object
            return "n.a.", f"not a propositional refutation object (family {fam!r}); proof_size requires an unsat instance family (S3 Cat 5)", "judged"
        sib = _object_witness(row, ch)
        if sib:
            return "defined-informative", f"object existence witnessed by populated {sib!r} (R-1 structural sibling); value {v}", "derived"
        return "defined-informative", f"value {v}; object exists (S3 owner default for average_case/landscape/proof_size)", "judged"
    # real value
    if _DEGENERACY.search(t):
        return "defined-trivial", f"degeneracy signal in canonical_task: {t[:60]!r}", "judged"
    if ch == "parameterized" and fam == "graph":                                            # Cat 2: all graph-param ambiguous
        if pid in _GRADIENT_WITNESSES:
            return "ambiguous", f"GRADIENT WITNESS — charge value flips with parameterization (solution-size vs treewidth); recorded not downgraded (S3 Cat 2); perspective={p!r}", "judged"
        return "ambiguous", f"graph-family parameterization: treewidth vs solution-size competes; perspective={p!r} (S3 Cat 2)", "judged"
    if p and (";" in p or " vs " in p.lower()):
        return "ambiguous", f"perspective names competing framings: {p!r}", "judged"
    return "defined-informative", f"real value {v}; single natural framing", "derived"


def derive_objective(row):
    """-> (objective, reason, provenance) from the FULL approximation canonical_task (Cat-3 lexicon; flag, never default)."""
    ap = _cell(row, "approximation")
    if ap["value"] == "n.a.":
        return "none", ap.get("canonical_task") or "approximation n.a.", "derived"
    t = ap.get("canonical_task") or ""
    for obj, rx in _OBJ_RULES:
        m = rx.search(t)
        if m:
            return obj, f"{obj} from {m.group(0)!r} in canonical_task", "derived"
    pid = row["problem_id"]
    if pid in _OBJ_OWNER:                                       # S3 Cat 3 owner assignment (lexicon flagged it)
        obj = _OBJ_OWNER[pid]
        return obj, f"owner-assigned (S3 Cat 3): {obj}" + (f" — {_OBJ_OWNER_REASON[pid]}" if pid in _OBJ_OWNER_REASON else ""), "judged"
    return None, f"objective type not resolvable by the sealed lexicon: {t[:60]!r} — owner assigns (S3 Cat 3)", "judged"


def derive_parameterization(row):
    """-> (parameterization, pin_theorem, reason, provenance) from the parameterized perspective (S1 rules + S3 Cat 4)."""
    pm = _cell(row, "parameterized")
    pid = row["problem_id"]
    if pm["value"] == "n.a.":
        return "none", None, pm.get("canonical_task") or "parameterized n.a.", "derived"
    p = pm.get("perspective")
    theorem = (pm.get("provenance") or {}).get("citation")
    if not p:
        if pid in _NOPERSP_PARAM:                                                            # Cat 4: owner-assigned
            return _NOPERSP_PARAM[pid], theorem, f"owner-assigned (S3 Cat 4): {_NOPERSP_PARAM[pid]}; perspective absent", "judged"
        return None, theorem, "parameterized value without a perspective — owner assigns", "judged"
    pl = p.lower()
    if ";" in p or " vs " in pl:
        return "other", theorem, f"competing parameterizations named: {p!r}", "judged"
    if "solution size" in pl:
        return "solution size", theorem, f"perspective={p!r}", "derived"
    if "treewidth" in pl:
        return "treewidth", theorem, f"perspective={p!r}", "derived"
    return "other", theorem, f"single named parameter {p!r} -> other (S3 Cat 4, owner-confirmed derived)", "derived"


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
