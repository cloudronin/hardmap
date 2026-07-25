#!/usr/bin/env python3
"""Anatomy S1 — extract the coded instrument's qualification record into machine-readable form.

WHY THIS EXISTS. `Anatomy-SCHEMA.md` §2.5 requires a `coded` column's instrument record (rubric hash, kappa,
anchors, trap-row outcomes) to ride with the column PERMANENTLY. Today that requirement is satisfied only by
`dev/mosaic_code.py`'s stdout: it computes the resolution ladder, Cohen's kappa, Gwet's AC1, per-class
specific agreement, the P1 anchor check, the forbidden-vocabulary audit and the separability gate — and
persists exactly one of them (`mosaic-disagreements.json`). Everything else lives in a terminal that scrolled
away, plus prose in `mosaic-L1-findings.md`. That is instance-9's shape one more time: a provenance
requirement met by prose nobody can consume.

WHAT THIS DOES. Recomputes the SAME quantities from the SAME inputs using `mosaic_code`'s own functions
(imported read-only; the module is never modified), and writes `results/atlas/anatomy-instruments.json`.

TRANSIT INTEGRITY (kill 1). This script MOVES a record; it never edits one. The 3-class kappa it recomputes
is asserted equal to the value already sealed in `mosaic_L3_results.json` (0.646). Any drift is a hard
failure — it would mean the instrument record and the scored results disagree about the same instrument.
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent          # eightfold/
sys.path.insert(0, str(ROOT))                          # eightfold package
sys.path.insert(0, str(ROOT / "dev"))                  # mosaic_code

import mosaic_code as MC                                # noqa: E402  (read-only; __main__-guarded)
from eightfold import atlas as A, structure as S        # noqa: E402

                                                        # mosaic_code.AT is relative to ITS run dir; anchor it
AT = ROOT / "eightfold" / "results" / "atlas"
MC.AT = AT                                              # so any internal use resolves too
OUT = AT / "anatomy-instruments.json"
SEALED_KAPPA_3CLASS = 0.646        # mosaic_L3_results.json -> meta.kappa_3class
TOL = 0.0005                        # the sealed value is quoted to 3 dp


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def build() -> dict:
    a = MC.load(AT / "mosaic-coding-A.jsonl")
    b = MC.load(AT / "mosaic-coding-B.jsonl")
    keys = sorted(set(a) & set(b))

    # --- the resolution ladder (prereg_v10-clarification-01) ---
    ladder = {}
    for lvl in ("5-class", "3-class", "2-class"):
        aa, bb = MC._collapse(a, MC.COLLAPSE[lvl]), MC._collapse(b, MC.COLLAPSE[lvl])
        k, raw = MC.cohen_kappa(aa, bb, keys)
        ladder[lvl] = {"cohen_kappa": round(float(k), 4),
                       "raw_agreement": round(float(raw), 4),
                       "gwet_ac1": round(float(MC.gwet_ac1(aa, bb, keys)), 4),
                       "reliable_at_0.6": bool(k >= 0.6)}
    demonstrated = next((l for l in ("5-class", "3-class", "2-class")
                         if ladder[l]["cohen_kappa"] >= 0.6), None)

    # --- 5-class disagreement shape (the entangled<->mixed seam) ---
    dis5 = [(a[k]["locality_class"], b[k]["locality_class"])
            for k in keys if a[k]["locality_class"] != b[k]["locality_class"]]
    em = sum(1 for x, y in dis5 if {x, y} == {"entangled", "mixed"})

    # --- per-class specific agreement (5-class) ---
    pca = MC.per_class_agreement(a, b, keys)
    per_class = {c: {"both": pca[c][0], "either": pca[c][1], "rate": pca[c][2]}
                 for c in ("decomposable", "local-covering", "entangled", "mixed", "uncodable")}

    # --- P1 anchors ---
    anchors, p1_ok = {}, True
    for pid, want in MC.ANCHORS.items():
        ga = a.get(pid, {}).get("locality_class")
        gb = b.get(pid, {}).get("locality_class")
        ok = (ga == want) and (gb == want)
        p1_ok &= ok
        anchors[pid] = {"expected": want, "coder_A": ga, "coder_B": gb, "pass": bool(ok)}

    # --- forbidden-vocabulary audit (the blindness trap check) ---
    forb = {name: MC.forbidden_audit(c) for name, c in (("A", a), ("B", b))}

    # --- separability gate (PINNED, prereg_v10) on the AGREED rows joined to charges ---
    agreed = {k: a[k]["locality_class"] for k in keys if a[k]["locality_class"] == b[k]["locality_class"]}
    v3 = {e.problem_id: {c.charge: c.value for c in e.charges}
          for e in A.load_atlas(str(AT / "atlas_v3.jsonl"))}
    def real(v): return v not in ("open", "n.a.", "unmeasured")

    loc, ap = [], []
    for k, cls in agreed.items():
        cv = v3.get(k, {})
        if real(cv.get("approximation", "n.a.")):
            loc.append(cls); ap.append(cv["approximation"])
    v_ap = S.cramers_v(loc, ap) if len(loc) >= 4 else float("nan")

    loc2, pa2 = [], []
    for k, cls in agreed.items():
        cv = v3.get(k, {})
        if real(cv.get("parameterized", "n.a.")):
            loc2.append(cls); pa2.append(cv["parameterized"])
    v_pa = S.cramers_v(loc2, pa2) if len(loc2) >= 4 else float("nan")

    dz = [k for k in MC.DISSOCIATION if k in a and k in b]
    acc = (sum(a[k]["locality_class"] == "decomposable" and b[k]["locality_class"] == "decomposable"
               for k in dz) / len(dz)) if dz else float("nan")
    fires = bool((v_ap > acc) or (v_pa > acc))

    return {
        "schema": "anatomy-instruments/v1",
        "note": ("Machine-readable qualification records for Anatomy's `coded` columns. Every cell with "
                 "provenance_status 'coded' must carry an instrument_ref resolving here (Anatomy-SCHEMA §1.3). "
                 "Extracted from dev/mosaic_code.py's computation, which previously persisted only to stdout."),
        "instruments": {
            "mosaic-3class-v1": {
                "instrument_id": "mosaic-3class-v1",
                "column": "locality_class",
                "kind": "blind dual-coder structural judgment, resolution-laddered",
                "seals": ["prereg_v10", "prereg_v10-clarification-01"],
                "blindness": ("coders received problem_id + problem_name + canonical_encoding ONLY; no charge "
                              "value and no per-charge task text. Codings were hashed BEFORE the charge join."),
                "rubric": {"file": "mosaic-rubric.md", "sha256": sha(AT / "mosaic-rubric.md")},
                "codings": {
                    "A": {"file": "mosaic-coding-A.jsonl", "sha256": sha(AT / "mosaic-coding-A.jsonl"),
                          "n": len(a)},
                    "B": {"file": "mosaic-coding-B.jsonl", "sha256": sha(AT / "mosaic-coding-B.jsonl"),
                          "n": len(b)},
                    "C_tiebreak": {"file": "mosaic-coding-C.jsonl",
                                   "sha256": sha(AT / "mosaic-coding-C.jsonl"),
                                   "note": "blind third pass on disagreements only; never consulted charges"},
                },
                "n_shared_rows": len(keys),
                "qualification_threshold": 0.6,
                "resolution_ladder": ladder,
                "demonstrated_resolution": demonstrated,
                "disagreement_shape_5class": {
                    "n_disagreements": len(dis5),
                    "entangled_mixed_seam": em,
                    "seam_share": round(em / len(dis5), 4) if dis5 else 0.0,
                    "reading": ("the instrument strains exactly where the two structural properties overlap; "
                                "banked as two-property-split evidence when the seam share is >= 0.5"),
                },
                "per_class_specific_agreement_5class": per_class,
                "anchors": anchors,
                "anchors_pass": bool(p1_ok),
                "forbidden_vocabulary_audit": {
                    "A_leaks": len(forb["A"]), "B_leaks": len(forb["B"]),
                    "A_rows": forb["A"][:10], "B_rows": forb["B"][:10],
                    "rule": "a rationale naming an outcome word (has a PTAS / is FPT / inapproximable) leaks",
                },
                "separability_gate": {
                    "status": "PINNED (prereg_v10)",
                    "V_locality_approx": round(float(v_ap), 4),
                    "V_locality_param": round(float(v_pa), 4),
                    "dissociation_structure_accuracy": round(float(acc), 4),
                    "dissociation_rows": dz,
                    "charge_reconstruction_fires": fires,
                    "reading": ("FIRES iff the label predicts a charge better than it codes the dissociation "
                                "set's structure — i.e. the label is charge-echo, not structure. ABSOLUTE gate."),
                },
                "coverage_conditioning": None,
                "caveat": ("locality is an APPROXIMATE blind-coded variable; associations built on it are "
                           "indicative, not precise. `uncodable` is a NON-CLASS and is dropped from "
                           "associations, never bucketed."),
            }
        },
    }


def main() -> int:
    rec = build()
    inst = rec["instruments"]["mosaic-3class-v1"]

    # --- KILL 1: transit integrity. The record must AGREE with the already-sealed scored value. ---
    got = inst["resolution_ladder"]["3-class"]["cohen_kappa"]
    if abs(got - SEALED_KAPPA_3CLASS) > TOL:
        print(f"TRANSIT-INTEGRITY FAILURE: recomputed 3-class kappa {got} != sealed "
              f"{SEALED_KAPPA_3CLASS} (mosaic_L3_results.json). Consolidation MOVES cells, never edits them.")
        return 1

    OUT.write_text(json.dumps(rec, indent=2) + "\n")
    print(f"wrote {OUT}  sha256 {sha(OUT)[:16]}")
    print(f"  ladder: " + " · ".join(
        f"{k} kappa={v['cohen_kappa']:.3f}/AC1={v['gwet_ac1']:.3f}"
        for k, v in inst["resolution_ladder"].items()))
    print(f"  demonstrated resolution: {inst['demonstrated_resolution']}  "
          f"(sealed 3-class kappa {SEALED_KAPPA_3CLASS} MATCHES recomputed {got})")
    print(f"  anchors: {sum(v['pass'] for v in inst['anchors'].values())}/{len(inst['anchors'])} "
          f"-> {'QUALIFIED' if inst['anchors_pass'] else 'MISS'}")
    print(f"  separability gate: V(loc,approx)={inst['separability_gate']['V_locality_approx']} "
          f"V(loc,param)={inst['separability_gate']['V_locality_param']} "
          f"diss-acc={inst['separability_gate']['dissociation_structure_accuracy']} -> "
          f"{'FIRES' if inst['separability_gate']['charge_reconstruction_fires'] else 'clear'}")
    print(f"  forbidden-vocab leaks: A={inst['forbidden_vocabulary_audit']['A_leaks']} "
          f"B={inst['forbidden_vocabulary_audit']['B_leaks']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
