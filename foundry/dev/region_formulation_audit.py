#!/usr/bin/env python3
"""The region-formulation audit over the lexicon-typed queue (Q24, ruled 2026-07-27).

WHY THIS IS HAND ADJUDICATION AND SAYS SO. Lexicon v2's stopping rule declared two mechanical passes and
then eyes-on-the-field with receipts. This is the eyes-on pass, run over the MATCHED portion — because
`lex-first-maximal-independent-set` matched `L4-subset` on the phrase "independent set" and is not a
subset region at all. Matched is not verified.

Every verdict quotes the row's own `canonical_encoding`. That is the receipt: a reader disagreeing with
a call can see exactly the text it was made from, without trusting the caller.

THE VOCABULARY IS DECLARED BEFORE THE ROWS ARE READ, and it inherits the distinction the rulings already
drew rather than rediscovering it:

  SUBSET-VERIFIED  the certificate IS a subset of a fixed instance-determined ground set, and
                   feasibility is a predicate on that subset. Enters a subset roster.

  VARIANT-REGION   a subset encoding EXISTS but loses information the canonical object carries — the
                   3-partition species. Declares a variant at birth, or waits for its canonical path.

  WRONG-REGION     the object is not a subset region under any encoding — a unique answer, or a
                   sequence whose order is the answer. Excludes; it belongs to another class.

The two route differently, which is why they are not one verdict: WRONG-REGION leaves the queue,
VARIANT-REGION stays with a declaration attached.
"""
import json, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from foundry.catalog import maptrail as M                                       # noqa: E402

LAT = ROOT / "foundry" / "results" / "lattice"
ATLAS = ROOT.parent / "eightfold" / "eightfold" / "results" / "atlas" / "atlas_v3.jsonl"
OUT = LAT / "region_formulation_audit.json"
TRAIL = LAT / "maptrail.jsonl"

VERDICTS = {
    "lex-first-maximal-independent-set": ("WRONG-REGION",
        "the lex-first maximal independent set is UNIQUE given the fixed vertex order the encoding "
        "states. There is one answer, not a region — the row belongs to REGIONLESS-unique-answer. This "
        "is the false positive that forced the audit: it matched L4-subset on 'independent set'."),
    "independent-set-reconfiguration": ("WRONG-REGION",
        "the certificate is a SEQUENCE of single-token moves transforming I_s into I_t. The answer is "
        "the transformation, and its order is the content — no subset of a fixed ground set encodes "
        "it. Belongs to the reconfiguration/sequence shape, which the census has no class for yet."),
    "disjoint-paths": ("VARIANT-REGION",
        "an edge-subset encoding exists — the union of the k paths is an edge set — but it LOSES the "
        "terminal-pair assignment, which is the whole question. A subset reading answers 'are these "
        "edges usable' rather than 'do k disjoint paths connect these pairs'. Subset encoding "
        "available, canonical object different: the 3-partition species."),
}
AFFORDABILITY_NOTE = {
    "bilevel-knapsack": "leader's choice IS a subset; the predicate requires solving the follower's "
                        "optimum, so this is an AFFORDABILITY question, not a typing one",
    "network-interdiction": "same bilevel shape — subset certificate, inner-optimization predicate",
}


def main() -> int:
    d = json.loads((LAT / "reach_subset_readjudication.json").read_text())
    atlas = {json.loads(x)["problem_id"]: json.loads(x)
             for x in ATLAS.read_text().splitlines() if x.strip()}
    queue = d["lexicon_typed_queue"]

    rows = []
    for p in queue:
        enc = atlas.get(p, {}).get("canonical_encoding") or ""
        verdict, why = VERDICTS.get(p, ("SUBSET-VERIFIED",
            "the certificate is a subset of a fixed instance-determined ground set and feasibility is "
            "a predicate on that subset"))
        rec = {"problem_id": p, "verdict": verdict, "why": why, "canonical_encoding": enc}
        if p in AFFORDABILITY_NOTE:
            rec["affordability_note"] = AFFORDABILITY_NOTE[p]
        rows.append(rec)

    by = Counter(r["verdict"] for r in rows)
    wrong = [r["problem_id"] for r in rows if r["verdict"] == "WRONG-REGION"]
    variant = [r["problem_id"] for r in rows if r["verdict"] == "VARIANT-REGION"]
    verified = [r["problem_id"] for r in rows if r["verdict"] == "SUBSET-VERIFIED"]

    doc = {
        "schema": "region-formulation-audit/v1",
        "STATUS": "HAND ADJUDICATION WITH RECEIPTS — the eyes-on pass lexicon v2's stopping rule "
                  "declared in advance. Every verdict quotes the encoding it was made from.",
        "scope": "the MATCHED portion of the lexicon-typed queue, because matched is not verified",
        "vocabulary": {
            "SUBSET-VERIFIED": "certificate is a subset of a fixed ground set; enters a subset roster",
            "VARIANT-REGION": "a subset encoding exists but loses what the canonical object carries; "
                              "declares a variant at birth or waits for its canonical path",
            "WRONG-REGION": "not a subset region under any encoding; leaves the queue"},
        "declared_before_reading": True,
        "n_audited": len(rows),
        "by_verdict": dict(by),
        "lexicon_false_positive_rate": {
            "wrong_region_only": round(len(wrong) / len(rows), 4),
            "wrong_or_variant": round((len(wrong) + len(variant)) / len(rows), 4),
            "what_it_measures": ("the rate at which an L4-subset MATCH is not a verified subset region. "
                                 "This is the honesty accounting lexicon v2's coverage number wanted: "
                                 "coverage says how much the lexicon read, this says how often what it "
                                 "read was right."),
            "denominator_caveat": ("23 matched rows, not a sample of anything wider. It is the rate on "
                                   "THIS queue and is not projected onto the 59 still unmatched.")},
        "verified_subset_queue": verified,
        "n_verified": len(verified),
        "wrong_region": wrong,
        "variant_region": variant,
        "rows": rows,
    }
    OUT.write_text(json.dumps(doc, indent=1) + "\n")

    print(f"REGION-FORMULATION AUDIT — {len(rows)} lexicon-typed rows\n")
    for k, v in sorted(by.items(), key=lambda z: -z[1]):
        print(f"  {k:<18} {v}")
    print(f"\n  lexicon false-positive rate (wrong-region only) : "
          f"{doc['lexicon_false_positive_rate']['wrong_region_only']:.1%}")
    print(f"  including variant-region                        : "
          f"{doc['lexicon_false_positive_rate']['wrong_or_variant']:.1%}")
    print(f"\n  VERIFIED subset queue: {len(verified)} rows — batch 8 rosters from here")
    for r in rows:
        if r["verdict"] != "SUBSET-VERIFIED":
            print(f"\n  [{r['verdict']}] {r['problem_id']}")
            print(f"      encoding: {r['canonical_encoding'][:110]}")
            print(f"      why     : {r['why'][:150]}")

    M.emit(TRAIL, "annotation", key="annotation:region-formulation-audit",
           what="the lexicon-typed queue audited row by row for region formulation",
           n_audited=len(rows), by_verdict=dict(by),
           wrong_region=wrong, variant_region=variant,
           false_positive_rate_wrong_only=doc["lexicon_false_positive_rate"]["wrong_region_only"],
           method="hand adjudication with the canonical_encoding quoted per row",
           touches_no_measured_value=True, authority="owner ruling on Q24, 2026-07-27")
    print(f"\n  wrote {OUT.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
