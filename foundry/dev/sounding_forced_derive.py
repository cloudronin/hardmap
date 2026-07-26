#!/usr/bin/env python3
"""Derive theorem-forcedness from Marrow's pinned templates, replacing the hand-written FORCED list.

THE DEFECT THIS CLOSES. Design law 3 excludes theorem-forced flavours from any discovery statistic BY
SCHEMA — enforced in code against a hand-written dictionary. A hand-maintained list of forced pairings is
RULES-THAT-LIVE-IN-RECALL WEARING THE COSTUME OF THE FIX FOR IT, and the survey proved it: ten readings
returned exactly 0.0 while not flagged forced, and several were plainly forced and simply missing.

THE JOIN, which both artifacts already computed and nobody connected:
    Marrow pins a template Gamma per row and derives its closure flags.
    A polymorphism of Gamma is closed on EVERY instance's solution set — that is what a polymorphism IS.
    So:  bijunctive => majority forced ·  affine => minority forced
         horn       => min forced      ·  dualhorn => max forced
Forcedness becomes DERIVED provenance instead of REMEMBERED provenance.

TWO BOUNDARIES THAT MATTER, and collapsing either would just replace one wrong flag with another:

  1. REGION KIND. The guarantee covers the SOLUTION SET of CSP(Gamma) — so `solutions` and `feasible`
     regions inherit it. An `optimal` region is a SUB-LEVEL SET of an objective over that solution set and
     carries NO closure guarantee. Optimal regions are never forced.
  2. TEMPLATE COVERAGE. Only 11 of the survey's 20 rows have a pinned template. For the other 9 forcedness
     is UNDERIVABLE, which is NOT the same as "not forced". Three states, never two.

This is a FLAG CORRECTION, not a re-measurement: identical readings, corrected metadata.
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AT = ROOT.parent / "eightfold" / "eightfold" / "results" / "atlas"
SURVEY = ROOT / "foundry" / "results" / "lattice" / "sounding_survey_readings.json"

# DERIVED FORCEDNESS IS A LOWER BOUND, and the survey proved it in the same run that fixed the list.
# `matching`/feasible/min reads exactly 0.0 and the derivation calls it UNDERIVABLE — but matchings ARE
# subset-closed by a one-line argument (a subset of a matching is a matching), and no finite template is
# involved. The old hand list had that entry and it was TRUE.
# So the fix is not derived-INSTEAD-OF-asserted, it is derived UNION asserted-with-its-argument. What the
# hand list may no longer contain is an entry without a stated reason; every ASSERTED entry below ships
# the argument that justifies it, and is auditable as prose the way a derived one is auditable as code.
ASSERTED = {
    ("matching", "feasible", "min"):
        "a subset of a matching is a matching — the feasible set is closed downward under intersection. "
        "No finite bounded-arity template exists for this row, so the template route cannot see it.",
    ("dominating-set", "feasible", "max"):
        "a superset of a dominating set is a dominating set — closed upward under union. Unbounded-arity "
        "neighbourhood scopes put it outside the template route.",
    ("three-dimensional-matching", "feasible", "min"):
        "a subset of a 3D matching is a 3D matching — closed downward, same argument as `matching`.",
}

# the join: a closure flag on the pinned template forces the matching blend flavour
BOOL_MAP = {"bijunctive": "majority", "affine": "minority", "horn": "min", "dualhorn": "max"}
D3_MAP = {"semilattice_or_majority": "median", "maltsev_affine": "maltsev3"}
REGIONS_INHERITING = {"solutions", "feasible"}


def load_marrow():
    der = {}
    p = AT / "marrow-derived.jsonl"
    for line in p.read_text().splitlines():
        if line.strip():
            r = json.loads(line)
            der[r["problem_id"]] = r
    return der


def forced_flavours(row, der):
    """Flavours the row's PINNED TEMPLATE is closed under. None => no template => underivable."""
    rec = der.get(row)
    if rec is None:
        return None
    fp = rec.get("poly_fingerprint_natural")
    if not isinstance(fp, dict):
        return None
    out = set()
    if rec.get("domain_size") == 2:
        for flag, flavour in BOOL_MAP.items():
            if fp.get(flag) is True:
                out.add(flavour)
    else:
        for flag, flavour in D3_MAP.items():
            if fp.get(flag) is True:
                out.add(flavour)
        for flag, flavour in (("min", "min"), ("max", "max")):
            pass
    return out


def main() -> int:
    der = load_marrow()
    doc = json.loads(SURVEY.read_text())
    changed, resid = [], []
    for x in doc["readings"]:
        ff = forced_flavours(x["row"], der)
        was = x.get("theorem_forced")
        if ff is None:
            now, prov = None, "underivable — no pinned template for this row"
        elif x["region"] not in REGIONS_INHERITING:
            now, prov = False, ("not applicable — an optimal region is a sub-level set and carries no "
                                "closure guarantee")
        else:
            now = x["flavor"] in ff
            prov = ("derived from the pinned template's closure flags (Marrow M2)" if now
                    else "derived: the pinned template is not closed under this flavour")
        key = (x["row"], x["region"], x["flavor"])
        if key in ASSERTED:                       # union, not override: asserted-with-argument counts
            now = True
            prov = "ASSERTED with argument (no template route): " + ASSERTED[key]
        x["theorem_forced"] = now
        x["forced_provenance"] = prov
        if bool(was) != bool(now) or now is None:
            changed.append({"row": x["row"], "region": x["region"], "flavor": x["flavor"],
                            "was": was, "now": now, "provenance": prov})
        if x["measured_rate"] == 0.0 and now is not True:
            resid.append({"row": x["row"], "region": x["region"], "flavor": x["flavor"],
                          "excess": x["excess"], "forced": now, "provenance": prov})

    doc["forced_flag_provenance"] = {
        "method": ("DERIVED from Marrow's pinned templates, not listed. bijunctive=>majority, "
                   "affine=>minority, horn=>min, dualhorn=>max; a polymorphism of Gamma holds on every "
                   "instance's solution set."),
        "region_rule": ("`solutions` and `feasible` inherit the template's guarantee; `optimal` regions "
                        "are sub-level sets and are never forced"),
        "three_states": ("true = forced · false = derived not forced · null = UNDERIVABLE by the template "
                         "route and not asserted. `null` is not `false`."),
        "derived_is_a_lower_bound": ("the template route sees only template-expressible closure. Regions "
                                     "can be provably closed for reasons no finite template carries — "
                                     "matchings under intersection, dominating sets under union. Those "
                                     "ship as ASSERTED entries CARRYING THEIR ARGUMENT. The rule the "
                                     "survey earned is not 'derive instead of assert', it is 'no entry "
                                     "without a reason, derived or written'."),
        "template_coverage": f"{len({r for r in {x['row'] for x in doc['readings']} if r in der})} of "
                             f"{len({x['row'] for x in doc['readings']})} survey rows have a pinned template",
        "n_flags_changed": len(changed), "changed": changed}
    doc.setdefault("changelog", []).append({
        "date": "2026-07-26", "kind": "FLAG CORRECTION — NOT A RE-MEASUREMENT",
        "what": ("`theorem_forced` recomputed from Marrow's pinned templates. Readings, seeds, controls "
                 "and every measured value are byte-identical; only the forced metadata changed."),
        "why": ("the hand-written FORCED list was incomplete — the survey found ten exact-zero readings "
                "unflagged, several plainly forced. A hand-maintained list of theorem-forced pairings is "
                "rules-that-live-in-recall wearing the costume of the fix for it.")})
    doc["residual_unforced_exact_zeros"] = {
        "n": len(resid),
        "note": ("exact-zero readings that are NOT derived-forced, AFTER the flag correction. These are "
                 "the genuinely interesting ones — which is exactly why the flag hygiene had to come "
                 "first. Not interpreted here; banked."),
        "readings": resid}
    SURVEY.write_text(json.dumps(doc, indent=1) + "\n")

    print("FORCEDNESS DERIVED FROM PINNED TEMPLATES (flag correction, not re-measurement)\n")
    print(f"  flags changed: {len(changed)}")
    for c in changed[:14]:
        print(f"    {c['row']:<27}{c['region']:<10}{c['flavor']:<10}{str(c['was']):<7}-> {c['now']}")
    if len(changed) > 14:
        print(f"    ... and {len(changed)-14} more")
    print(f"\n  residual unforced exact-zeros: {len(resid)}")
    for r in resid:
        print(f"    {r['row']:<27}{r['region']:<10}{r['flavor']:<10}excess {r['excess']:+.4f}  "
              f"forced={r['forced']}")
    print(f"\n  sha256 {hashlib.sha256(SURVEY.read_bytes()).hexdigest()[:16]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
