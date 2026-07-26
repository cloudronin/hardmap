#!/usr/bin/env python3
"""Marrow v1 M2 — the derived closure columns: poly_fingerprint_natural, engine_type_natural.

THE ANCHORS RUN FIRST AND GOVERN. Kill 2 (prereg_v15): any extended predicate failing its known-answer
anchors sends that domain's rows to `open`, never to an approximation. So this script computes the anchor
set BEFORE it computes a single natural row, and refuses to write if any anchor misses.

TWO CONSTRAINTS SEALED BEFORE THE CODE WAS WRITTEN (prereg_v15 derived_build_constraints):

  1. FLAGS 7-10 ARE `n.a.` BY THEOREM ON NON-BOOLEAN ROWS. `width2affine`, `strongly0valid`, `IHSB` and
     `general_wsep` are Boolean by THEOREM, not merely by implementation -- KSTW and Marx do not transfer
     to |D| > 2. They are emitted as `n.a.` with a reason, never ported and never approximated.

  2. `build_anatomy.derive_engine_type` IS NOT CALLED HERE. It computes `fs = bool(flags["affine"])`,
     encoding the Boolean collapse few-subpowers <=> Maltsev <=> affine. That equivalence BREAKS at k > 2:
     Maltsev implies few subpowers, but few subpowers needs a k-edge term. The D3 side is handled by
     domain3's own operations, exactly as domain3.py:207-212 already does.

WHAT THE COLUMNS ARE A PROPERTY OF (prereg_v15 passports): the constraint language AT THE PINNED
PRESENTATION -- PARAMETER-RELATIVE, not invariant. On the Boolean universe the relation IS the object and
`poly_fingerprint` earns `invariant`; here a human pinned the presentation, and the fingerprint is an
invariant of that pin.
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT.parent / "foundry"))
from eightfold import anatomy as AN                                  # noqa: E402
from foundry import prism as PRISM                                   # noqa: E402
from foundry import domain3 as D3                                    # noqa: E402

AT = ROOT / "eightfold" / "results" / "atlas"
OUT = AT / "marrow-derived.jsonl"
SUMMARY = AT / "marrow-derived.json"

# Boolean by theorem — KSTW / Marx do not transfer to |D| > 2 (prereg_v15, clause 1)
BOOLEAN_ONLY_FLAGS = ("width2affine", "strongly0valid", "IHSB", "general_wsep")

# Kill-2 anchors. Every one is a KNOWN answer from the literature, asserted before any natural row is read.
BOOLEAN_ANCHORS = {
    "3-SAT -> no tractable polymorphism": (
        [[list(t) for t in __import__("itertools").product((0, 1), repeat=3) if list(t) != list(a)]
         for a in __import__("itertools").product((0, 1), repeat=3)],
        lambda f: not (f["0valid"] or f["1valid"] or f["horn"] or f["dualhorn"] or f["bijunctive"]
                       or f["affine"])),
    "Horn-SAT -> semilattice (MIN)": (
        [[list(t) for t in __import__("itertools").product((0, 1), repeat=3) if list(t) != list(a)]
         for a in __import__("itertools").product((0, 1), repeat=3)
         if sum(1 for x in a if x == 0) <= 1],
        lambda f: f["horn"]),
    "2-SAT -> majority (bijunctive)": (
        [[list(t) for t in __import__("itertools").product((0, 1), repeat=2) if list(t) != list(a)]
         for a in __import__("itertools").product((0, 1), repeat=2)],
        lambda f: f["bijunctive"]),
    "XOR-SAT -> affine (minority)": (
        [[list(t) for t in __import__("itertools").product((0, 1), repeat=3) if sum(t) % 2 == b]
         for b in (0, 1)],
        lambda f: f["affine"]),
}

D3_ANCHORS = {
    "CSP(K_3) 3-colouring -> NO tractable polymorphism": (
        [[[a, b] for a in range(3) for b in range(3) if a != b]],
        lambda prof, bw: len(prof) == 0),
    "linear equations over Z_3 -> tractable but UNBOUNDED width (Maltsev only)": (
        [[[a, b, c] for a in range(3) for b in range(3) for c in range(3) if (a + b + c) % 3 == 0]],
        lambda prof, bw: len(prof) > 0 and not bw),
    "the order relation on {0,1,2} -> tractable AND bounded width (semilattice)": (
        [[[a, b] for a in range(3) for b in range(3) if a <= b]],
        lambda prof, bw: len(prof) > 0 and bw),
}


def run_anchors():
    """Kill 2: runs first, governs. Returns (all_pass, report)."""
    rep, ok = [], True
    for name, (rels, pred) in BOOLEAN_ANCHORS.items():
        f = PRISM._flags([[tuple(t) for t in r] for r in rels])
        p = bool(pred(f))
        ok &= p
        rep.append({"domain": 2, "anchor": name, "pass": p})
    for name, (rels, pred) in D3_ANCHORS.items():
        rr = [[tuple(t) for t in r] for r in rels]
        prof = D3.polymorphism_profile(rr)
        bw = D3.is_bounded_width(rr)
        p = bool(pred(prof, bw))
        ok &= p
        rep.append({"domain": 3, "anchor": name, "pass": p, "profile": sorted(prof),
                    "bounded_width": bool(bw)})
    return ok, rep


def derive_boolean(tmpl):
    rels = [[tuple(t) for t in r] for v in tmpl["relations"].values() for r in v]
    f = PRISM._flags(rels)
    fingerprint = {k: bool(v) for k, v in f.items()}
    engine_bw = PRISM.bounded_width(f) == "bounded-width"
    # |D| = 2 ONLY: few-subpowers <=> Maltsev <=> affine. Stated here because it is exactly the collapse
    # that must not travel to k > 2.
    engine_fs = bool(f["affine"])
    engine = ("both" if (engine_bw and engine_fs) else "bounded-width" if engine_bw
              else "few-subpowers" if engine_fs else "neither")
    return fingerprint, engine, {"basis": "Post's lattice, |D|=2", "collapse_used": "few-subpowers <=> affine"}


def derive_d3(tmpl):
    rels = [[tuple(t) for t in r] for v in tmpl["relations"].values() for r in v]
    prof = D3.polymorphism_profile(rels)
    bw = bool(D3.is_bounded_width(rels))
    tractable = len(prof) > 0
    # flags 7-10 are n.a. BY THEOREM; the rest are reported as the named-operation profile
    fingerprint = {k: "n.a." for k in BOOLEAN_ONLY_FLAGS}
    fingerprint.update({"const_valid": bool(D3._const_valid(rels)) if hasattr(D3, "_const_valid") else "n.a.",
                        "semilattice_or_majority": bw,
                        "maltsev_affine": bool("maltsev-z3" in prof or "affine-z3" in prof
                                               or any("maltsev" in p or "affine" in p for p in prof)),
                        "tractable_witness": sorted(prof)})
    # NOT derive_engine_type: the affine<=>few-subpowers collapse is |D|=2 only
    engine = ("bounded-width" if bw else "few-subpowers" if tractable else "neither")
    return fingerprint, engine, {"basis": "domain3 named-operation witnesses, |D|=3",
                                 "collapse_used": "NONE — the Boolean affine<=>few-subpowers collapse is "
                                                  "deliberately not applied at k>2",
                                 "sufficiency_caveat": ("named operations are a SUFFICIENT witness for "
                                                        "tractability, not a decision procedure; an empty "
                                                        "profile means 'no library witness', which for "
                                                        "CSP(K_3) coincides with the known NP-hardness")}


def main() -> int:
    ok, rep = run_anchors()
    print("MARROW M2 — KILL-2 ANCHORS (run first, govern)\n")
    for r in rep:
        print(f"  {'PASS' if r['pass'] else 'FAIL'}  |D|={r['domain']}  {r['anchor']}")
    if not ok:
        print("\nANCHOR FAILURE — per prereg_v15 Kill 2 that domain's rows go `open`, never approximated.")
        print("Refusing to write derived columns.")
        return 1
    print(f"\n  all {len(rep)} anchors green — derivation permitted\n")

    pres = [json.loads(l) for l in (AT / "marrow-presentations.jsonl").read_text().splitlines() if l.strip()]
    recs = []
    for p in pres:
        d = p["domain_size"]
        if d == 2:
            fp, engine, prov = derive_boolean(p["template"])
        elif d == 3:
            fp, engine, prov = derive_d3(p["template"])
        else:
            recs.append({"problem_id": p["problem_id"], "poly_fingerprint_natural": "open",
                         "engine_type_natural": "open",
                         "reason": f"|D|={d} has no qualified predicate set; `open`, never approximated"})
            continue
        recs.append({"problem_id": p["problem_id"], "domain_size": d,
                     "poly_fingerprint_natural": fp, "engine_type_natural": engine,
                     "derivation": prov, "provenance_status": "derived",
                     "instance_restriction": p["instance_restriction"],
                     "n_a_flags": list(BOOLEAN_ONLY_FLAGS) if d != 2 else [],
                     "n_a_reason": (None if d == 2 else
                                    "Boolean BY THEOREM — KSTW/Marx do not transfer to |D|>2")})
    OUT.write_text("".join(json.dumps(r) + "\n" for r in recs))

    from collections import Counter
    eng = Counter(r.get("engine_type_natural") for r in recs)
    doc = {"schema": "marrow-derived/v1", "prereg": "prereg_v15", "milestone": "M2",
           "kill_2_anchors": {"all_pass": ok, "n": len(rep), "detail": rep,
                              "rule": "anchors run FIRST and govern; a miss sends that domain to `open`"},
           "n_rows": len(recs), "by_domain": dict(Counter(r.get("domain_size") for r in recs)),
           "engine_type_marginal": dict(eng),
           "boolean_only_flags_na_on_non_boolean": list(BOOLEAN_ONLY_FLAGS),
           "derive_engine_type_not_reused": (
               "build_anatomy.derive_engine_type was NOT called. Its `fs = bool(flags['affine'])` encodes "
               "the |D|=2 collapse few-subpowers <=> Maltsev <=> affine, which breaks at k>2. The D3 path "
               "uses domain3's own operations."),
           "passport_note": ("PARAMETER-RELATIVE: an invariant of the constraint language AT THE PINNED "
                             "PRESENTATION. Boolean poly_fingerprint earns `invariant` because there the "
                             "relation IS the object; here a human pinned the presentation.")}
    SUMMARY.write_text(json.dumps(doc, indent=1) + "\n")

    print(f"{'row':<28}{'dom':>4}  engine_type_natural")
    for r in recs:
        print(f"{r['problem_id']:<28}{r.get('domain_size','—'):>4}  {r.get('engine_type_natural')}")
    print(f"\nengine marginal: {dict(eng)}")
    print(f"wrote {OUT.name} ({len(recs)} rows)  sha256 {hashlib.sha256(OUT.read_bytes()).hexdigest()[:16]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
