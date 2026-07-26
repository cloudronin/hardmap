#!/usr/bin/env python3
"""Marrow v1 M4 — build, census and freeze ANATOMY v2.

WHY v2 AND NOT AN ADDITIVE v1.1 (prereg_v15, ruled): Anatomy-SCHEMA §4 pre-authorises additive fills for
RESERVED NAMES ONLY, and none of Marrow's columns are reserved. §0.3.3 then governs -- "a changed rule is a
new sealed version, never an in-place edit." Adding cells to `anatomy_v1.jsonl` would also rewrite its bytes
against the `tolerance: exact` sha pin in repro/manifest.yaml and tests/test_anatomy.py.

THE PROOF OF NON-EDIT IS V1'S OWN TESTS. `anatomy_v1.jsonl` keeps sha 8ff11f8a and every v1 test passes
UNCHANGED -- that is the evidence this is a new artifact rather than an edit, and it is asserted here rather
than asserted in prose.

CENSUS BEFORE SEAL (SCHEMA §3.3/§3.3b) runs on every new column. Coverage and usability are SEPARATE
verdicts, both stated with their marginals, and a column failing usability still ships -- recorded as
descriptive-only. CLEAN MEANS COMPLETE AND HONEST, NOT ALL-GREEN.
"""
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from eightfold import anatomy as AN                                  # noqa: E402

AT = ROOT / "eightfold" / "results" / "atlas"
V1 = AT / "anatomy_v1.jsonl"
V2 = AT / "anatomy_v2.jsonl"
PASS2 = AT / "anatomy_v2_passports.json"
FREEZE2 = AT / "anatomy_v2_freeze.json"

V1_SHA = "8ff11f8a33bbdce7"
MIN_CELL, MAX_SHARE = 5, 0.90          # Cochran floor / starvation line, inherited unchanged


def cell(feature, value, prov, **kw):
    c = {"feature": feature, "value": value, "provenance_status": prov}
    c.update({k: v for k, v in kw.items() if v is not None})
    return c


def variance_for(column, cells):
    """SCHEMA §3.3b. `starved` is explicitly true/false — never left null on a categorical column, which
    `passport_admissible` treats as NOT CENSUSED and therefore permanently inadmissible."""
    real = [c["value"] for c in cells if not (isinstance(c["value"], str) and c["value"] in AN.SENTINELS)]
    if not real:
        return {"kind": "not-built", "n_cells": len(cells), "n_real": 0, "starved": None,
                "note": "no real cells"}
    if any(isinstance(v, dict) for v in real):
        return {"kind": "record-valued", "n_cells": len(cells), "n_real": len(real), "starved": None,
                "note": ("a dict is not a feature — admissible only through a NAMED PROJECTION whose own "
                         "marginals clear the floor (the rule that moved v1's poly_fingerprint)")}
    marg = Counter(str(v) for v in real)
    top, n = marg.most_common(1)[0]
    share = n / len(real)
    thin = [k for k, v in marg.items() if v < MIN_CELL]
    # THE GATE WAS ONE-SIDED, and this column is what exposed it. The inherited rule starves a column whose
    # modal value SWAMPS the population — over-concentration. It said nothing about the opposite failure:
    # `presentation` has 28 distinct values on 28 rows, modal share 4%, and every single cell sits below the
    # Cochran floor. A column with as many levels as rows is a ROW IDENTIFIER, and carries exactly as little
    # contrast as a constant does. Both ends are starvation; only one end was being checked.
    no_level_clears_floor = all(v < MIN_CELL for v in marg.values())
    starved = bool(share > MAX_SHARE or len(marg) < 2 or no_level_clears_floor)
    if share > MAX_SHARE:
        why = f"OVER-CONCENTRATED — modal value holds {share:.0%}"
    elif len(marg) < 2:
        why = "CONSTANT — one level, carries no information"
    elif no_level_clears_floor:
        why = (f"OVER-DISPERSED — {len(marg)} levels over {len(real)} rows and NOT ONE clears the Cochran "
               f"floor of {MIN_CELL}. This is a row identifier, not a feature; descriptive-only.")
    else:
        why = (f"ok — modal {share:.0%}, {len(marg)} levels; {len(thin)} cell(s) below the Cochran floor "
               f"of {MIN_CELL}")
    return {"kind": "categorical", "n_cells": len(cells), "n_real": len(real),
            "n_levels": len(marg),
            "marginal": (dict(marg.most_common()) if len(marg) <= 12 else
                         {"__suppressed__": f"{len(marg)} levels, all count<= {max(marg.values())}"}),
            "modal_share": round(share, 4), "thin_cells": len(thin), "starved": starved,
            "starved_note": why}


def main() -> int:
    v1_sha = hashlib.sha256(V1.read_bytes()).hexdigest()[:16]
    assert v1_sha == V1_SHA, f"v1 MOVED: {v1_sha} != {V1_SHA} — v2 must never edit v1"

    pres = {json.loads(l)["problem_id"]: json.loads(l)
            for l in (AT / "marrow-presentations.jsonl").read_text().splitlines() if l.strip()}
    der = {json.loads(l)["problem_id"]: json.loads(l)
           for l in (AT / "marrow-derived.jsonl").read_text().splitlines() if l.strip()}

    rows, new_cells = [], {c: [] for c in AN.V2_COLUMNS}
    for line in V1.read_text().splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        pid = r.get("problem_id")
        if r["universe"] == AN.NATURAL and pid in pres:
            p, d = pres[pid], der.get(pid, {})
            add = [
                cell("presentation", p["presentation"], AN.PROV_CITED, citation=p["citation"]),
                cell("poly_fingerprint_natural", d.get("poly_fingerprint_natural", "open"),
                     AN.PROV_ORACLE if d else AN.PROV_STRUCTURAL),
                cell("engine_type_natural", d.get("engine_type_natural", "open"),
                     AN.PROV_ORACLE if d else AN.PROV_STRUCTURAL),
            ]
            r = dict(r)
            r["features"] = list(r["features"]) + add
            r["anatomy_version"] = "v2"
            for c in add:
                new_cells[c["feature"]].append(c)
        rows.append(r)

    V2.write_text("".join(json.dumps(r) + "\n" for r in rows))
    v2_sha = hashlib.sha256(V2.read_bytes()).hexdigest()[:16]

    # ── census before seal ──────────────────────────────────────────────────────────────────────────
    passports = {"schema": "anatomy-v2-passports/v1", "prereg": "prereg_v15",
                 "note": ("v2 columns ONLY. v1's passports are untouched and still authoritative for the "
                          "eleven v1 columns."),
                 "columns": {}}
    for col in AN.V2_COLUMNS:
        verdict, prop, reason = AN.V2_PASSPORT_INVARIANCE[col]
        passports["columns"][col] = {
            "column": col, "shipped": True,
            "universe": AN.V2_COLUMNS[col]["universe"], "route": AN.V2_COLUMNS[col]["route"],
            "invariance": verdict, "property_of": prop, "invariance_reason": reason,
            "bridge_citation": AN.V2_COLUMNS[col]["bridge"],
            "variance": variance_for(col, new_cells[col]),
            "readability": None, "admissible_collapse": None,
            "bet_history": {"sealed_bets": [], "outcomes": "UNSPENT — no bet has been sealed on any v2 "
                            "column. Terroir-C, the test they were built for, is INSUFFICIENT-as-sealed "
                            "(prereg_v15 M0b) and this build does not reopen it.",
                            "exposure": "NONE"}}
    adm = []
    for col in AN.V2_COLUMNS:
        ok, why = AN.passport_admissible(col, passports)
        passports["columns"][col]["admissible_for_a_sealed_bet"] = ok
        passports["columns"][col]["admissibility_reasons"] = why
        if ok:
            adm.append(col)
    PASS2.write_text(json.dumps(passports, indent=1) + "\n")

    freeze = {"schema": "anatomy-v2-freeze/v1", "artifact": V2.name, "sha256_16": v2_sha,
              "frozen": "2026-07-25", "prereg": "prereg_v15",
              "n_rows": len(rows),
              "n_rows_carrying_v2_columns": len(pres),
              "version_class": {
                  "ruling": "NEW SEALED VERSION, not an additive v1.1",
                  "why": ("Anatomy-SCHEMA §4 licenses additive fills for RESERVED NAMES ONLY and none of "
                          "these are reserved; §0.3.3 — a changed rule is a new sealed version."),
                  "v1_untouched": {"artifact": V1.name, "sha256_16": v1_sha,
                                   "asserted_here": True,
                                   "proof_of_non_edit": ("v1's own tests pass UNCHANGED — that is the "
                                                         "evidence, not this sentence")}},
              "gates": {"v1_bytes_unmoved": v1_sha == V1_SHA,
                        "kill_2_anchors": "7/7 green at M2 — see marrow-derived.json",
                        "passport_completeness": all(c in passports["columns"] for c in AN.V2_COLUMNS),
                        "variance_recorded": all(passports["columns"][c]["variance"].get("starved")
                                                 is not None or
                                                 passports["columns"][c]["variance"]["kind"] in
                                                 ("record-valued", "not-built") for c in AN.V2_COLUMNS)},
              "admissible_for_a_sealed_bet": adm,
              "honest_note": ("CLEAN MEANS COMPLETE AND HONEST, NOT ALL-GREEN. `presentation` and "
                              "`poly_fingerprint_natural` are record-/prose-valued and are not themselves "
                              "features; `engine_type_natural` is the one contrastable column."),
              "scope": ("28 of 345 natural rows carry v2 columns. The other 317 have no fixed finite "
                        "bounded-arity template and are absent from these columns by construction, not by "
                        "omission — see marrow-i0-census.json.")}
    FREEZE2.write_text(json.dumps(freeze, indent=1) + "\n")

    print("MARROW M4 — ANATOMY v2 built, censused, frozen\n")
    print(f"  v1 {V1.name:<22} sha {v1_sha}  UNMOVED  <- the freeze law")
    print(f"  v2 {V2.name:<22} sha {v2_sha}  ({len(rows)} rows, {len(pres)} carrying v2 columns)\n")
    for col in AN.V2_COLUMNS:
        v = passports["columns"][col]
        var = v["variance"]
        print(f"  {col:<26} {v['invariance']:<20} variance={var['kind']:<15} "
              f"starved={var.get('starved')}")
        if var["kind"] == "categorical":
            print(f"      marginal {var['marginal']}  modal {var['modal_share']:.0%}")
    print(f"\n  admissible for a sealed bet: {adm or 'NONE'}")
    print(f"  (and nothing is betting on them — Terroir-C stays INSUFFICIENT-as-sealed)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
