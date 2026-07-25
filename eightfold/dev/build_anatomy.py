#!/usr/bin/env python3
"""Anatomy S1 — consolidate every EXISTING structure column into `anatomy_v1.jsonl`.

CONSOLIDATION MOVES CELLS; IT NEVER EDITS THEM (Anatomy-SCHEMA §3.1, kill 1). Run with `--verify` to
diff every consolidated cell against its source sidecar; any changed value halts the milestone. An edit
is an errata event on the SOURCE, handled on that source's own track — never here.

S1 scope = columns that already exist somewhere on disk:
  natural  : locality_class (coded) · kernel_status (cited) · self_reducibility (pre-law exception,
             read-only from the R17/R18 charge fields) · reduction_out_degree (oracle) · sociology
  boolean  : class_size · poly_fingerprint  (both already persisted by the Prism build)

NOT S1: engine_type, arity_class, encoding_type, objective_type, decomposition_facts — those are DERIVED
or CITED work and belong to S2, under the rules sealed in Anatomy-SCHEMA §2.

A column emits a cell ONLY where source data exists. Absence here is honest: S2 fills the gaps with
`open`/`n.a.` and their mandatory reasons. Emitting a speculative sentinel now would be a derivation
wearing consolidation's clothes.
"""
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT.parent / "foundry"))

from eightfold import atlas as A, anatomy as AN     # noqa: E402

AT = ROOT / "eightfold" / "results" / "atlas"
LAT = ROOT.parent / "foundry" / "foundry" / "results" / "lattice"
OUT = AT / "anatomy_v1.jsonl"


def jsonl(p):
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()]


def cell(feature, value, prov, *, reason=None, citation=None, instrument_ref=None,
         bridge=None, source=None, note=None):
    c = {"feature": feature, "value": value, "provenance_status": prov}
    for k, v in (("reason", reason), ("citation", citation), ("instrument_ref", instrument_ref),
                 ("bridge_citation", bridge), ("source_artifact", source), ("note", note)):
        if v is not None:
            c[k] = v
    return c


# ── S2 derivation rules — applied VERBATIM from the sealed contract ───────────────────────────────────
import re  # noqa: E402

# §2.4 encoding_type: fixed order, first match wins (the order is outcome-relevant)
ENCODING_ORDER = [
    ("cnf-circuit", r"\bcnf\b|clause|literal|formula|circuit|qbf"),
    ("graph", r"\bgraph\b|vertex|vertices|edge|digraph|hypergraph|tree|adjacency"),
    ("geometric", r"point|plane|geometric|euclidean|disk|rectangle|polygon|coordinate"),
    ("matrix-vector", r"matrix|matrices|lattice basis|vector"),
    ("string", r"string|sequence|permutation|alphabet|word"),
    ("numeric-set", r"integer|number|set of.*(items|numbers)|weights"),
]

# §2.2a arity_class: five rules, fixed order, first match wins. Fallthrough -> `open`, never a guess.
ARITY_GLOBAL = (r"tour|cycle cover|spanning|connected|flow|cut(?!width)|chromatic|colou?ring|makespan|"
                r"completion time|latency|diameter|bandwidth|bisection|arrangement|embedding|"
                r"triangulation|packing|routing|scheduling|total (weight|cost|length)")
ARITY_UNBOUNDED = (r"set cover|hitting set|dominating|hypergraph|clause of arbitrary|"
                   r"unbounded (width|arity|degree)|subset of arbitrary|family of sets|covering all|hits every")
ARITY_LOCAL = (r"edge|pair(wise)?|adjacent|incident|neighbou?r|2-|binary constraint|degree at most|"
               r"arity (2|3|at most)|clause of (size|width) (2|3)|triangle")

# §2.3 objective_type: the Strata Cat-3 lexicon, sealed 2026-07-23, applied verbatim.
# `weighted` is checked LAST and narrowed: a recognised numeric objective wins.
OBJ_MAXCSP = r"max-(sat|2sat|3sat|horn-sat|nae-sat|cut|dicut|3-lin|1-in-3-sat|circuit-sat|k-sat)"
OBJ_MINONES = (r"min-(vc|vertex cover|dominating|set cover|hitting set|fvs|feedback vertex|"
               r"connected-vc|eds|edge dominating|odd-cycle-transversal|independent-dominating)")
OBJ_MAXONES = r"max-(clique|is\b|independent-set|independent set|leaf|k-set-packing|set packing|coverage)"
OBJ_GLOBALNUM = (r"tsp|tour|chromatic|steiner|discrepancy|bandwidth|makespan|bin-packing|bin packing|"
                 r"k-center|treewidth|treedepth|bisection|multiway-cut|longest-path|latency|"
                 r"completion time|cutwidth|minimum-fill-in|arrangement|triangulation")
OBJ_WEIGHTED = r"knapsack|subset-sum|subset sum"


def derive_encoding_type(enc: str) -> str:
    s = (enc or "").lower()
    for name, pat in ENCODING_ORDER:
        if re.search(pat, s):
            return name
    return "other"


def derive_arity_class(enc: str, task_text: str):
    """Returns (value, reason_or_None). Reads task TEXT only -- never a charge VALUE (SCHEMA §0.3.1)."""
    s = f"{enc or ''} {task_text or ''}".lower()
    if not s.strip():
        return "n.a.", "the row pins no constraint or objective structure to classify"
    for value, pat in (("global-objective", ARITY_GLOBAL),
                       ("unbounded-fanin", ARITY_UNBOUNDED),
                       ("bounded-local", ARITY_LOCAL)):
        if re.search(pat, s):
            return value, None
    return "open", None          # fallthrough is reported, never bucketed


def derive_objective_type(approx_value: str, approx_task: str):
    """Cat-3 lexicon. approx_value is read ONLY for the sentinel test that the OBJECT exists (n.a. => the
    optimization version does not exist => `none`), which is a typing fact, not a value-informed structure
    claim. The CLASS is decided purely from task text."""
    if approx_value == "n.a.":
        return "none", None
    t = (approx_task or "").lower()
    for value, pat in ((("Max-CSP"), OBJ_MAXCSP), ("Min-Ones", OBJ_MINONES),
                       ("Max-Ones", OBJ_MAXONES), ("global-numeric", OBJ_GLOBALNUM)):
        if re.search(pat, t):
            return value, None
    if re.search(OBJ_WEIGHTED, t):
        return "weighted", None
    return "open", None          # flagged, never defaulted


def derive_engine_type(flags: dict):
    """§2.1. Uses the CORRECTED I3 bounded-width predicate ONLY (prism.py:66) -- the naive variants at
    finer.py:52 / r25.py miss the 0/1-valid rescue and would manufacture spurious variation."""
    from foundry import prism
    bw = prism.bounded_width(flags) == "bounded-width"
    fs = bool(flags["affine"])                    # Boolean domain: few subpowers <=> Maltsev <=> affine
    return ("both" if (bw and fs) else "bounded-width" if bw else "few-subpowers" if fs else "neither"), bw


def bitmask(arity, relation):
    """Canonical, stable key for a Boolean relation: a bitmask over the 2^arity possible tuples."""
    m = 0
    for t in relation:
        idx = 0
        for bit in t:
            idx = (idx << 1) | int(bit)
        m |= (1 << idx)
    width = max(1, (2 ** arity + 3) // 4)
    return f"{m:0{width}x}"


# ── natural universe ──────────────────────────────────────────────────────────────────────────────────
def build_natural():
    v3 = A.load_atlas(str(AT / "atlas_v3.jsonl"))
    loc = {r["problem_id"]: r for r in jsonl(AT / "mosaic-locality.jsonl")}
    ker = {r["problem_id"]: r for r in jsonl(AT / "mosaic-kernel-status.jsonl")}
    prov = {r["problem_id"]: r for r in jsonl(AT / "atlas_v3_provenance.jsonl")}
    rn = json.loads((AT / "reductions-network-edges.json").read_text())
    outdeg = rn.get("per_problem_outdegree", {})
    v2pins = {r["problem_id"]: r for r in jsonl(AT / "atlas_v2.jsonl") if r.get("objective") is not None}

    rows = []
    for e in v3:
        pid = e.problem_id
        feats = []

        # locality_class — CODED. `uncodable` is a NON-CLASS: it becomes `open`, never a bucket.
        if pid in loc:
            lv = loc[pid]["locality_3class"]
            if lv == "uncodable":
                feats.append(cell("locality_class", "open", AN.PROV_STRUCTURAL,
                                  reason=("blind instrument returned `uncodable` — the pinned encoding did "
                                          "not admit a structural call at 3-class resolution"),
                                  source="mosaic-locality.jsonl"))
            else:
                feats.append(cell("locality_class", lv, AN.PROV_CODED,
                                  instrument_ref="mosaic-3class-v1", source="mosaic-locality.jsonl",
                                  note=loc[pid].get("resolution")))

        # kernel_status — CITED (R20). Coverage is FPT-conditioned; see SCHEMA §6.
        if pid in ker:
            feats.append(cell("kernel_status", ker[pid]["kernel_status"], AN.PROV_CITED,
                              citation=ker[pid].get("citation"), bridge="§6.kernel",
                              source="mosaic-kernel-status.jsonl", note=ker[pid].get("note")))

        # self_reducibility — PRE-LAW EXCEPTION: consolidated READ-ONLY from the R18 charge field.
        for ch in e.charges:
            if getattr(ch, "worst_to_average_self_reduction", None) is True:
                feats.append(cell("self_reducibility", "worst-to-average", AN.PROV_CITED,
                                  citation=(ch.provenance or {}).get("citation"), bridge="§7.self_reducibility",
                                  source="atlas_v3.jsonl:charges.worst_to_average_self_reduction",
                                  note=("PRE-LAW EXCEPTION (SCHEMA §0.3.3): structure that already lived in "
                                        "the charge table before the founding law; consolidated read-only, "
                                        "never re-derived")))
                break

        # reduction_out_degree — ORACLE. Absent is NOT zero (SCHEMA §2.5); non-members emit no cell.
        if pid in outdeg:
            feats.append(cell("reduction_out_degree", outdeg[pid], AN.PROV_ORACLE,
                              source="reductions-network-edges.json",
                              note=f"pinned commit {rn.get('commit', '')[:8]}; rule: {rn.get('counting_rule', '')[:80]}"))

        # ── S2 DERIVED (natural) ──────────────────────────────────────────────────────────────────────
        ch = {c.charge: c for c in e.charges}
        enc = e.canonical_encoding or ""
        atask = (ch["approximation"].canonical_task if "approximation" in ch else "") or ""
        dtask = (ch["decision"].canonical_task if "decision" in ch else "") or ""

        feats.append(cell("encoding_type", derive_encoding_type(enc), AN.PROV_FIELD,
                          source="atlas_v3.jsonl:canonical_encoding",
                          note="sealed keyword order, first match wins (SCHEMA §2.4)"))

        av, ar = derive_arity_class(enc, f"{dtask} {atask}")
        feats.append(cell("arity_class", av,
                          AN.PROV_STRUCTURAL if av in ("n.a.", "open") else AN.PROV_FIELD,
                          reason=ar, source="atlas_v3.jsonl:canonical_encoding+canonical_task",
                          note="sealed five-rule lexicon, first match wins (SCHEMA §2.2a)"))

        # §2.3: INHERIT the 118 sealed atlas_v2 pins verbatim (with their own derived/judged provenance),
        # and only then extend to v3-new rows by the Cat-3 lexicon. Inheritance wins over re-derivation.
        if pid in v2pins:
            p = v2pins[pid]
            feats.append(cell("objective_type", p["objective"],
                              AN.PROV_JUDGED if p.get("pin_provenance") == "judged" else AN.PROV_FIELD,
                              reason=("owner-assigned at the Strata S3 sitting, 2026-07-23"
                                      if p.get("pin_provenance") == "judged" else None),
                              source="atlas_v2.jsonl:objective (sealed Strata pin, inherited verbatim)",
                              note=f"pin_theorem: {p.get('pin_theorem') or '—'}"))
        else:
            ov, orr = derive_objective_type(
                ch["approximation"].value if "approximation" in ch else "n.a.", atask)
            feats.append(cell("objective_type", ov,
                              AN.PROV_STRUCTURAL if ov == "open" else AN.PROV_FIELD,
                              reason=orr, source="atlas_v3.jsonl:canonical_task (Cat-3 lexicon)",
                              note="Strata Cat-3 lexicon, sealed 2026-07-23, extended to v3-new (SCHEMA §2.3)"))

        row = {"row_key": pid, "universe": AN.NATURAL, "problem_id": pid, "features": feats}

        # sociology sidecar — QUARANTINED (SCHEMA §3.4): control terms only, never a structural claim.
        if pid in prov:
            p = prov[pid]
            row["sociology"] = {k: p.get(k) for k in
                                ("source_funnel", "admission_wave", "rn_membership", "rn_route")
                                if p.get(k) is not None}
            row["sociology"]["_law"] = "control term only; never enters a structural claim"
        rows.append(row)
    return rows


# ── boolean universe ──────────────────────────────────────────────────────────────────────────────────
def build_boolean():
    ct = json.loads((LAT / "prism_v2_charges.json").read_text())["charge_table"]
    rows, eng_marg, bw_marg = [], Counter(), Counter()
    for r in ct:
        key = f"b{r['arity']}:{bitmask(r['arity'], r['relation'])}"
        engine, bw = derive_engine_type(r["flags"])
        eng_marg[engine] += 1
        bw_marg["bounded-width" if bw else "unbounded-width"] += 1
        feats = [
            cell("class_size", r["class_size"], AN.PROV_ORACLE, source="prism_v2_charges.json"),
            cell("poly_fingerprint", {k: r["flags"][k] for k in AN.POLY_FINGERPRINT_FLAGS},
                 AN.PROV_ORACLE, bridge="§3.decision", source="prism_v2_charges.json",
                 note="the ten persisted Post's-lattice flags, verbatim and in sealed order"),
            cell("engine_type", engine, AN.PROV_ORACLE, bridge="§3.decision",
                 source="prism_v2_charges.json:flags",
                 note=("corrected I3 bounded-width predicate (prism.py:66) + affine=few-subpowers; "
                       "cite §3.decision ONLY in its corrected form -- 'bounded-width <=> local "
                       "consistency' is Barto-Kozik's DEFINITION, the theorem is the SD(^) "
                       "characterization (necessity: Larose-Zadori 2007)")),
        ]
        rows.append({"row_key": key, "universe": AN.BOOLEAN, "arity": r["arity"],
                     "relation": r["relation"], "class_size": r["class_size"], "features": feats})
    return rows, eng_marg, bw_marg


def reconcile_engine(bw_marg):
    """SCHEMA §2.1(d): derived marginals MUST reconcile with the persisted Prism numbers, or the predicate
    in use is not the corrected one. Returns a list of violations."""
    p = json.loads((LAT / "prism_v2_charges.json").read_text())
    want = p.get("marginals", {}).get("localization", {})
    bad = []
    for k, v in want.items():
        if bw_marg.get(k, 0) != v:
            bad.append(f"engine reconciliation: derived {k}={bw_marg.get(k, 0)} != persisted {v}")
    pa = (p.get("pred2_bounded_width_marginal_descriptive", {})
           .get("purely_affine_unbounded_classes_total"))
    return bad, want, pa


def coder_cross_check(rows):
    """SCHEMA §2.2 ruling: the 345x2 blind codings are a VALIDATION SIGNAL, never a tiebreak. Rows where
    the derivation disagrees with BOTH coders are task-text ambiguity notes."""
    a = {r["problem_id"]: r.get("arity_class") for r in jsonl(AT / "mosaic-coding-A.jsonl")}
    b = {r["problem_id"]: r.get("arity_class") for r in jsonl(AT / "mosaic-coding-B.jsonl")}
    agree_a = agree_b = both = neither = n = 0
    ambiguous = []
    for row in rows:
        if row["universe"] != AN.NATURAL:
            continue
        got = next((c["value"] for c in row["features"] if c["feature"] == "arity_class"), None)
        pid = row["problem_id"]
        if got in (None, "open", "n.a.") or pid not in a or pid not in b:
            continue
        n += 1
        ha, hb = (got == a[pid]), (got == b[pid])
        agree_a += ha; agree_b += hb
        if ha and hb:
            both += 1
        elif not ha and not hb:
            neither += 1
            ambiguous.append({"problem_id": pid, "derived": got, "coder_A": a[pid], "coder_B": b[pid]})
    return {"n_compared": n, "agree_coder_A": agree_a, "agree_coder_B": agree_b,
            "agree_both": both, "agree_neither": neither,
            "rate_A": round(agree_a / n, 3) if n else None,
            "rate_B": round(agree_b / n, 3) if n else None,
            "task_text_ambiguities": ambiguous}


# ── kill 1: transit integrity ─────────────────────────────────────────────────────────────────────────
def verify(rows):
    """Every consolidated cell must equal its source cell. Returns a list of violations."""
    bad = []
    loc = {r["problem_id"]: r for r in jsonl(AT / "mosaic-locality.jsonl")}
    ker = {r["problem_id"]: r for r in jsonl(AT / "mosaic-kernel-status.jsonl")}
    rn = json.loads((AT / "reductions-network-edges.json").read_text()).get("per_problem_outdegree", {})
    ct = {f"b{r['arity']}:{bitmask(r['arity'], r['relation'])}": r
          for r in json.loads((LAT / "prism_v2_charges.json").read_text())["charge_table"]}

    for row in rows:
        cells = {c["feature"]: c for c in row["features"]}
        if row["universe"] == AN.NATURAL:
            pid = row["problem_id"]
            if "locality_class" in cells:
                src = loc[pid]["locality_3class"]
                got = cells["locality_class"]["value"]
                want = "open" if src == "uncodable" else src
                if got != want:
                    bad.append(f"{pid}.locality_class: {got!r} != source {src!r}")
            if "kernel_status" in cells and cells["kernel_status"]["value"] != ker[pid]["kernel_status"]:
                bad.append(f"{pid}.kernel_status: {cells['kernel_status']['value']!r} != source "
                           f"{ker[pid]['kernel_status']!r}")
            if "reduction_out_degree" in cells and cells["reduction_out_degree"]["value"] != rn[pid]:
                bad.append(f"{pid}.reduction_out_degree: {cells['reduction_out_degree']['value']} != {rn[pid]}")
        else:
            src = ct[row["row_key"]]
            if cells["class_size"]["value"] != src["class_size"]:
                bad.append(f"{row['row_key']}.class_size mismatch")
            if cells["poly_fingerprint"]["value"] != {k: src["flags"][k] for k in AN.POLY_FINGERPRINT_FLAGS}:
                bad.append(f"{row['row_key']}.poly_fingerprint mismatch")
    return bad


def main() -> int:
    nat = build_natural()
    boo, eng_marg, bw_marg = build_boolean()
    rows = nat + boo

    # --- SCHEMA §2.1(d): engine reconciliation gate, BEFORE anything is written ---
    rbad, want, pure_affine = reconcile_engine(bw_marg)
    if rbad:
        print("ENGINE RECONCILIATION FAILED — the predicate in use is not the corrected I3 one:")
        for x in rbad:
            print(f"   {x}")
        return 3

    # schema validation, before anything is written
    errs = AN.validate_level_registry()
    for r in rows:
        errs.extend(AN.validate_anatomy_row(r))
    if errs:
        print(f"SCHEMA VALIDATION FAILED ({len(errs)}):")
        for e in errs[:20]:
            print(f"   {e}")
        return 2

    bad = verify(rows)
    if bad:
        print(f"KILL 1 — TRANSIT INTEGRITY FAILURE ({len(bad)} cells changed in transit):")
        for b in bad[:20]:
            print(f"   {b}")
        return 1

    if "--verify" not in sys.argv:
        with OUT.open("w") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        import hashlib
        print(f"wrote {OUT.name}  rows={len(rows)}  sha256 {hashlib.sha256(OUT.read_bytes()).hexdigest()[:16]}")

    cnt = Counter(c["feature"] for r in rows for c in r["features"])
    print(f"natural rows {len(nat)} · boolean rows {len(boo)} · total {len(rows)}")
    print("cells per column: " + " · ".join(f"{k}={v}" for k, v in sorted(cnt.items())))
    print(f"schema validation: CLEAN · transit integrity (kill 1): CLEAN ({len(rows)} rows diffed)")

    # --- S2 condition-check log (SCHEMA §2.1 / §2.2a: the residual must be VISIBLE) ---
    print(f"\nengine reconciliation: derived bw-marginals {dict(bw_marg)} == persisted {want}  OK"
          f"  (purely-affine-unbounded persisted total: {pure_affine})")
    print(f"engine_type marginals: {dict(eng_marg)}")
    for col in ("encoding_type", "arity_class", "objective_type"):
        d = Counter(c["value"] for r in rows for c in r["features"] if c["feature"] == col)
        tot = sum(d.values())
        opens = d.get("open", 0)
        print(f"{col}: {dict(d.most_common())}   [residual `open` = {opens}/{tot} = {100*opens/tot:.0f}%]")

    x = coder_cross_check(rows)
    print(f"\narity_class coder cross-check (VALIDATION SIGNAL, not a tiebreak — SCHEMA §2.2):")
    print(f"  compared {x['n_compared']} rows · agree A {x['agree_coder_A']} ({x['rate_A']}) · "
          f"agree B {x['agree_coder_B']} ({x['rate_B']}) · both {x['agree_both']} · neither {x['agree_neither']}")
    print(f"  task-text ambiguities (derivation disagrees with BOTH coders): {len(x['task_text_ambiguities'])}"
          f" — recorded as typing notes, NOT resolved by a third pass")
    (AT / "anatomy-s2-conditionchecks.json").write_text(json.dumps({
        "engine_reconciliation": {"derived": dict(bw_marg), "persisted": want, "match": True,
                                  "purely_affine_unbounded_persisted": pure_affine},
        "engine_type_marginals": dict(eng_marg),
        "column_marginals": {col: dict(Counter(c["value"] for r in rows for c in r["features"]
                                               if c["feature"] == col))
                             for col in ("encoding_type", "arity_class", "objective_type")},
        "arity_class_coder_cross_check": x,
    }, indent=2, default=str) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
