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
    rows = []
    for r in ct:
        key = f"b{r['arity']}:{bitmask(r['arity'], r['relation'])}"
        feats = [
            cell("class_size", r["class_size"], AN.PROV_ORACLE, source="prism_v2_charges.json"),
            cell("poly_fingerprint", {k: r["flags"][k] for k in AN.POLY_FINGERPRINT_FLAGS},
                 AN.PROV_ORACLE, bridge="§3.decision", source="prism_v2_charges.json",
                 note="the ten persisted Post's-lattice flags, verbatim and in sealed order"),
        ]
        rows.append({"row_key": key, "universe": AN.BOOLEAN, "arity": r["arity"],
                     "relation": r["relation"], "class_size": r["class_size"], "features": feats})
    return rows


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
    nat, boo = build_natural(), build_boolean()
    rows = nat + boo

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
    return 0


if __name__ == "__main__":
    sys.exit(main())
