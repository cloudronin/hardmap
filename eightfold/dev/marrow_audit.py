#!/usr/bin/env python3
"""Marrow v1 — the presentation audit, run as a DIAGNOSTIC.

STATUS: NOT A SCORED RESULT. The audit is Quarry v3's Z5 deliverable and seals under prereg_v16, which does
not exist yet. This runs it now because Marrow's build was authorised on the strength of two live consumers
and this is one of them — a demonstration that the consumer works, not a verdict.

WHAT IT DOES: for every row with a pinned presentation, derive the decision value FROM THE TEMPLATE and
compare it against the CITED cell. This is the first time the atlas's cited cells are checked against
computed ground truth rather than against other citations.

THE ORACLE MUST MATCH THE OBJECTIVE, and the first run of this got that wrong. Deriving "decision" from the
constraint language's SATISFIABILITY answers the right question for a plain CSP and the WRONG one for a
VCSP: CSP({OR2}) is trivially satisfiable (set every variable to 1), while Min-Ones({OR2}) IS VERTEX COVER.
Run naively, all thirteen stratum-2 rows came back as disagreements — a fabricated 50% error rate that was
entirely the auditor's own mis-specification. The repo's KSTW oracles (objective_oracles.py, Thm 2.12/2.14)
classify APPROXIMABILITY, not decision, so no pinned decision oracle exists for Min-Ones/Max-Ones and those
rows are `open` under the not-pinned-is-not-cited rule.

  => the audit is WELL-POSED ON THE DIRECT-CSP STRATUM ONLY.
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from eightfold import atlas as A                                     # noqa: E402

AT = ROOT / "eightfold" / "results" / "atlas"
OUT = AT / "marrow-presentation-audit.json"


def main() -> int:
    v3 = {e.problem_id: e for e in A.load_atlas(str(AT / "atlas_v3.jsonl"))}
    pres = {json.loads(l)["problem_id"]: json.loads(l)
            for l in (AT / "marrow-presentations.jsonl").read_text().splitlines() if l.strip()}
    der = {json.loads(l)["problem_id"]: json.loads(l)
           for l in (AT / "marrow-derived.jsonl").read_text().splitlines() if l.strip()}

    def cited(pid):
        return next((c.value for c in v3[pid].charges if c.charge == "decision"), "n.a.")

    posable, not_posable, rows = [], [], []
    for pid in sorted(pres):
        p, d = pres[pid], der.get(pid, {})
        if p["stratum"] != "direct-csp":
            not_posable.append(pid)
            rows.append({"problem_id": pid, "stratum": p["stratum"], "verdict": "NOT-POSABLE",
                         "reason": ("Min-Ones/Max-Ones decision has no pinned oracle in this repo; KSTW "
                                    "Thm 2.12/2.14 classify APPROXIMABILITY. `open` per "
                                    "not-pinned-is-not-cited.")})
            continue
        computed = "P" if d.get("engine_type_natural") in ("bounded-width", "few-subpowers", "both") \
            else "NPC"
        c = cited(pid)
        agree = (computed == c)
        posable.append(pid)
        rows.append({"problem_id": pid, "stratum": p["stratum"], "computed_decision": computed,
                     "cited_decision": c, "agree": agree,
                     "instance_restriction": p["instance_restriction"],
                     "verdict": "AGREE" if agree else "DISAGREE"})

    dis = [r for r in rows if r.get("verdict") == "DISAGREE"]
    doc = {
        "schema": "marrow-presentation-audit/v1", "milestone": "Marrow (diagnostic)",
        "status": ("DIAGNOSTIC, NOT SCORED. The scored instrument is Quarry v3 Z5 under prereg_v16, "
                   "which is not sealed. Run here to demonstrate the consumer works."),
        "scope": {"pinned_rows": len(pres), "posable": len(posable), "not_posable": len(not_posable),
                  "why_not_posable": ("the oracle must match the objective. Schaefer answers 'is CSP(Gamma) "
                                      "satisfiable in P'; for Min-Ones/Max-Ones that is the wrong question, "
                                      "and this repo pins no decision oracle for them.")},
        "auditor_error_caught_and_recorded": (
            "the first run derived decision from satisfiability for ALL rows and reported 14/28 "
            "disagreements. Thirteen of those were the auditor's mis-specification, not the atlas's error. "
            "Caught because a disagreement PREDICTION had been written down first (M1: 'disagreements "
            "should concentrate on instance-restricted rows') and the observed pattern did not match it — "
            "half the disagreements were on unrestricted rows, all of them VCSP-shaped."),
        "result": {"agree": len(posable) - len(dis), "disagree": len(dis), "n": len(posable)},
        "disagreements": [
            {**r, "reading": (
                "PREDICTED IN ADVANCE at M1 as a disagreement BY CONSTRUCTION: the template is K_3 exactly "
                "as plain 3-colouring, so closure derives NPC while the cited charge reflects the succinct "
                "input encoding the template cannot see. A scope limit of closure anatomy, not an errata "
                "candidate." if r["problem_id"] == "succinct-3-coloring" else
                "NOT A DISAGREEMENT: the cited decision cell is `n.a.`, so there is no value to disagree "
                "with. Comparing against a non-value." if r["cited_decision"] == "n.a." else
                "GENUINE ERRATA CANDIDATE — computed and cited differ with no encoding or restriction to "
                "explain the gap. Investigate to verdict per the F-2 sweep's logic, with the theorem-side "
                "derivation as second witness.")}
            for r in dis],
        "the_one_candidate": [r["problem_id"] for r in dis
                              if r["problem_id"] != "succinct-3-coloring"
                              and r["cited_decision"] != "n.a."],
        "rows": rows,
    }
    OUT.write_text(json.dumps(doc, indent=1) + "\n")

    print("MARROW — PRESENTATION AUDIT (diagnostic; scored version is Quarry v3 Z5)\n")
    print(f"  pinned {len(pres)}  posable {len(posable)}  not-posable {len(not_posable)}\n")
    print(f"  agree {doc['result']['agree']} / disagree {doc['result']['disagree']} "
          f"of {doc['result']['n']}\n")
    for r in dis:
        print(f"  DISAGREE  {r['problem_id']:<24} computed {r['computed_decision']:<5} "
              f"cited {r['cited_decision']}")
    print(f"\n  genuine errata candidates: {doc['the_one_candidate'] or 'none'}")
    print(f"\nwrote {OUT.name}  sha256 {hashlib.sha256(OUT.read_bytes()).hexdigest()[:16]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
