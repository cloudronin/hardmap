#!/usr/bin/env python3
"""Generator conformance — does each templated generator EMIT what its pinned template says it does?

THE FOURTH OBJECT DRIFT, and the first caught at the generator level. `horn-sat`'s generator branch was
byte-identical to the plain branch, so the row emitted uniform random 3-CNF while Marrow's pinned Horn
template — and every flag derived from it — described something else. The derivation was sound; the
instances were not what the row said they were.

That defect was found BY ACCIDENT, while grounding an unrelated study. The same four-line copy-paste could
sit in any generator, so every templated generator is suspect until checked.

THE CHECK, and why this form rather than a syntactic one.

The tempting version reads clause shapes: Horn means at most one positive literal per clause, bijunctive
means width 2, affine means parity form. That works only for clausal generators and it tests a proxy.

THE UNIVERSAL FORM IS SEMANTIC: **if the pinned template is closed under operation f, then every emitted
instance's SOLUTION SET must be closed under f.** That is precisely what a polymorphism is, it holds for
any constraint shape, and it is the exact implication the forcedness join consumes. A generator whose
emissions fail it has drifted from its row's identity, whatever its source code looks like.

Both are run where both apply: the semantic check DETECTS drift, and the syntactic check LOCALISES it to
the emission rule. A row failing semantics with clean syntax means the template is wrong; failing both
means the generator is.

STANDING PRACTICE THIS INSTALLS. New machinery gets built to the current standard while old machinery
grandfathers in — `forced_saturated` was born with an observation-comparison check and its elder sibling
`theorem_forced` never had one. When a new check class is invented, ask which existing instruments predate
it. This file is that retrofit for the generator fleet.
"""
import hashlib
import json
import random
import sys
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "dev"))
LAT = ROOT / "foundry" / "results" / "lattice"
AT = ROOT.parent / "eightfold" / "eightfold" / "results" / "atlas"
OUT = LAT / "generator_conformance.json"
import sounding_v3_survey as S3                                        # noqa: E402
import sounding_v2 as S2                                               # noqa: E402

N_INSTANCES = 6
PAIR_CAP = 4000

# closure flag -> (operation, arity, human name)
FLAG_OP = {
    "bijunctive": (lambda ts: tuple(1 if sum(c) >= 2 else 0 for c in zip(*ts)), 3, "majority"),
    "affine":     (lambda ts: tuple(c[0] ^ c[1] ^ c[2] for c in zip(*ts)), 3, "minority"),
    "horn":       (lambda ts: tuple(min(c) for c in zip(*ts)), 2, "min"),
    "dualhorn":   (lambda ts: tuple(max(c) for c in zip(*ts)), 2, "max"),
}

# rows whose generator is CLAUSAL, so a syntactic emission rule also applies
SYNTACTIC = {
    "horn": ("at most one POSITIVE literal per clause",
             lambda cls: all(sum(sg) <= 1 for _vs, sg in cls)),
    "dualhorn": ("at most one NEGATIVE literal per clause",
                 lambda cls: all(sum(1 for s in sg if s == 0) <= 1 for _vs, sg in cls)),
    "bijunctive": ("every clause of width <= 2",
                   lambda cls: all(len(vs) <= 2 for vs, _sg in cls)),
}


def load_flags():
    der = {}
    for line in (AT / "marrow-derived.jsonl").read_text().splitlines():
        if line.strip():
            r = json.loads(line)
            fp = r.get("poly_fingerprint_natural")
            if isinstance(fp, dict) and r.get("domain_size") == 2:
                der[r["problem_id"]] = [k for k in FLAG_OP if fp.get(k) is True]
    return der


# row -> a builder returning (solution-set, clause-list-or-None)
def builders(rng):
    def clausal(k, mode, ratio):
        """Call the REAL generator and read the clauses it actually emitted.

        An earlier version of this function REIMPLEMENTED the generator so it could see the clause list.
        That is a conformance test of a copy, which certifies nothing about the thing in service — and it
        proved the point immediately by continuing to report `horn-sat` as drifted after the real
        generator had been fixed. The generator now publishes `LAST_CLAUSES`; this reads it."""
        d = dict(S3.sat(rng, ratio, k, mode) or [])
        return d.get("solutions"), list(S3.LAST_CLAUSES)

    def from_survey(row, kind, fn):
        d = dict(fn() or [])
        return d.get(kind), None

    return {
        "horn-sat": lambda: clausal(3, "horn", 2.0),
        "sat-2": lambda: clausal(2, "plain", 1.0),
        "sat-3": lambda: clausal(3, "plain", 3.5),
        "xor-sat": lambda: clausal(3, "xor", 0.7),
        "nae-sat": lambda: clausal(3, "nae", 1.5),
        "sharp-monotone-2sat": lambda: from_survey("sharp-monotone-2sat", "solutions",
                                                   lambda: S3.monotone2(rng, 1.3)),
        "vertex-cover": lambda: from_survey("vertex-cover", "feasible",
                                            lambda: S3.gsub(rng, 0.35, "vc")),
        "independent-set": lambda: from_survey("independent-set", "feasible",
                                               lambda: S3.gsub(rng, 0.35, "is")),
        "clique": lambda: from_survey("clique", "feasible",
                                      lambda: S2.regions_for("clique", rng)),
        "max-cut": lambda: from_survey("max-cut", "feasible",
                                       lambda: S2.regions_for("max-cut", rng)),
        "bipartiteness": lambda: from_survey("bipartiteness", "solutions",
                                             lambda: S2.regions_for("bipartiteness", rng)),
    }


def closed_under(region, op, m, rng):
    R = set(region)
    if len(region) < m:
        return None, 0
    idx = list(range(len(region)))
    seen = 0
    if len(region) <= 60:
        subs = list(combinations(idx, m))
    else:
        subs = [tuple(rng.sample(idx, m)) for _ in range(PAIR_CAP)]
    for sub in subs:
        seen += 1
        if op([region[i] for i in sub]) not in R:
            return False, seen
    return True, seen


def main() -> int:
    rng = random.Random(20260726)
    flags = load_flags()
    B = builders(rng)
    rows_out, drifted = [], []

    for row in sorted(set(flags) & set(B)):
        want = flags[row]
        if not want:
            continue
        sem = {f: {"pass": 0, "fail": 0, "checked": 0} for f in want}
        syn = {f: {"pass": 0, "fail": 0} for f in want if f in SYNTACTIC}
        example = None
        for _ in range(N_INSTANCES):
            try:
                region, cls = B[row]()
            except Exception as e:
                rows_out.append({"row": row, "error": str(e)}); region = None
                break
            if not region or len(region) < 3:
                continue
            for f in want:
                op, m, _nm = FLAG_OP[f]
                ok, seen = closed_under(region, op, m, rng)
                if ok is None:
                    continue
                sem[f]["checked"] += seen
                sem[f]["pass" if ok else "fail"] += 1
                if not ok and example is None:
                    example = {"flag": f, "region_size": len(region)}
            if cls is not None:
                for f in want:
                    if f in SYNTACTIC:
                        _d, test = SYNTACTIC[f]
                        syn[f]["pass" if test(cls) else "fail"] += 1
        if not any(sem[f]["pass"] + sem[f]["fail"] for f in want):
            continue
        bad = [f for f in want if sem[f]["fail"] > 0]
        rec = {"row": row, "template_flags": want,
               "semantic": {f: sem[f] for f in want},
               "syntactic": {f: {**syn[f], "rule": SYNTACTIC[f][0]} for f in syn} or None,
               "CONFORMS": not bad, "failing_flags": bad, "example": example}
        if bad:
            syn_clean = all(syn.get(f, {}).get("fail", 0) == 0 for f in bad)
            rec["localisation"] = (
                "semantics FAIL with clean syntax — the emitted clauses satisfy the shape rule but the "
                "solution sets are not closed. Suspect the TEMPLATE." if syn_clean and syn else
                "semantics and syntax BOTH fail — the GENERATOR does not emit the declared object.")
            drifted.append(rec)
        rows_out.append(rec)

    doc = {"schema": "generator-conformance/v1",
           "STATUS": "INSTRUMENT HYGIENE — no bet, no prereg",
           "the_check": ("if a row's pinned template is closed under f, EVERY emitted instance's solution "
                         "set must be closed under f. That is what a polymorphism is, it holds for any "
                         "constraint shape, and it is the exact implication the forcedness join consumes."),
           "why_semantic_not_syntactic": ("a clause-shape rule tests a proxy and only works on clausal "
                                          "generators. Both run where both apply: semantics DETECT drift, "
                                          "syntax LOCALISES it to the emission rule."),
           "standing_practice": ("new machinery is built to the current standard while old machinery "
                                 "grandfathers in. When a new check class is invented, ask which existing "
                                 "instruments predate it. This is that retrofit for the generator fleet."),
           "n_rows_checked": len(rows_out), "n_drifted": len(drifted),
           "drifted": drifted, "rows": rows_out}
    OUT.write_text(json.dumps(doc, indent=1) + "\n")

    print("GENERATOR CONFORMANCE SWEEP — do templated generators emit what their templates say?\n")
    print(f"  {'row':<24}{'template flags':<26}{'semantic':<22}{'syntactic':<18}conforms")
    for r in rows_out:
        if "error" in r:
            print(f"  {r['row']:<24}BUILD ERROR: {r['error'][:50]}"); continue
        s = " ".join(f"{f}:{r['semantic'][f]['pass']}/{r['semantic'][f]['pass']+r['semantic'][f]['fail']}"
                     for f in r["template_flags"])
        # a syntactic check with zero observations never RAN (non-clausal generator). Printing 0/0
        # would read as "checked and passed nothing", which is the fail-open shape this program names.
        y = " ".join(f"{f}:{v['pass']}/{v['pass']+v['fail']}" for f, v in (r["syntactic"] or {}).items()
                     if v["pass"] + v["fail"] > 0) or "n/a (non-clausal)"
        print(f"  {r['row']:<24}{','.join(r['template_flags']):<26}{s:<22}{y:<18}"
              f"{'YES' if r['CONFORMS'] else 'NO — DRIFTED'}")
    if drifted:
        print(f"\n  DRIFTED GENERATORS: {len(drifted)}")
        for d in drifted:
            print(f"    {d['row']}: failing {d['failing_flags']}")
            print(f"      {d['localisation']}")
    else:
        print(f"\n  No drift found beyond what is already recorded.")
    print(f"\nwrote {OUT.name}  sha256 {hashlib.sha256(OUT.read_bytes()).hexdigest()[:16]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
