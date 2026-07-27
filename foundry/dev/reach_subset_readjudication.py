#!/usr/bin/env python3
"""Re-adjudicate all 127 REACH-subset rows by CERTIFICATE OBJECT (Q22, ruled 2026-07-27).

WHY THE FIRST TYPING WAS WRONG, and it is derivable rather than remembered. The census fired
`R3-subset-selection` on `min-sum-set-cover`, `cutwidth` and `d-hitting-set` alike, attaching the same
boilerplate note to all three: "solutions are subsets of a ground set". But those rows' own
`canonical_encoding` in atlas_v3 says:

    min-sum-set-cover : "objective = A LINEAR ORDER on the sets minimizing the sum over elements ..."
    cutwidth          : "graph; LINEAR VERTEX ORDERING minimizing the maximum edge cut, <= k"
    d-hitting-set     : "family of sets each of size <= d; hit all with <= k elements"

The encoding field states the certificate object outright. **The census never read it.** So this pass is
not a second opinion — it is the first reading of a field that was already there.

THE LEXICON IS SEALED BELOW, BEFORE IT RUNS, and ORDER IS PART OF THE RULE. First match wins, exactly as
the anatomy's `arity_class` lexicon works (SCHEMA §2.2a). Ordering is tested before subset because
"a linear order on the sets" also contains "sets"; partition before subset because "partitioned into
dominating sets" does too. Getting that order wrong is how a lexicon quietly reproduces the bug it exists
to fix.

WHAT THIS PASS DOES NOT DO: guess. A row whose encoding matches no rule is reported UNMATCHED and left
for adjudication. An unmatched row is a fact about the lexicon's coverage, not a licence to fall back on
what the problem name suggests.

RETYPE, NEVER DROP. A mis-typed row is not unreachable — it is differently shaped. An ordering row is
permutation-encoded and belongs to a capture path the observatory has not built yet; a partition row may
need a class the census has not minted. Both get sized populations here so those paths start with honest
denominators instead of an estimate.
"""
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from foundry.catalog import maptrail as M                                       # noqa: E402

LAT = ROOT / "foundry" / "results" / "lattice"
ATLAS = ROOT.parent / "eightfold" / "eightfold" / "results" / "atlas" / "atlas_v3.jsonl"
OUT = LAT / "reach_subset_readjudication.json"
TRAIL = LAT / "maptrail.jsonl"

# ── THE SEALED LEXICON. Order is the rule; first match wins. ─────────────────────────────────────────
LEXICON = [
    ("REACH-permutation", "L1-ordering", [
        "linear order", "linear ordering", "linear vertex ordering", "linear arrangement",
        "vertex ordering", "ordering of", "permutation", "a tour", "hamiltonian",
        "sequence of jobs", "sequencing", "layout", "arrangement of", "topological order"]),
    ("REACH-partition", "L2-partition", [
        "partition", "partitioned", "partitioning", "colouring", "coloring", "colour the", "color the",
        "into k parts", "into at most k classes", "classes into which"]),
    ("REACH-assignment", "L3-assignment", [
        "assignment", "assign each", "assigns each", "mapping from", "map each", "truth assignment",
        "schedule assigning", "allocation of"]),
    ("REACH-subset", "L4-subset", [
        "subset", "sub-family", "subfamily", "select", "choose", "delete <=", "delete at most",
        "remove <=", "remove at most", "hit all", "cover all", "covering all", "of size <= k",
        "at most k vertices", "at most k edges", "<= k vertices", "<= k edges", "<= k elements",
        "set of size", "family of sets"]),
]


def classify(encoding: str):
    """Returns (class, rule, matched_phrase) or (None, 'L0-unmatched', None)."""
    if not encoding:
        return None, "L0-no-encoding", None
    low = encoding.lower()
    for klass, rule, phrases in LEXICON:
        for ph in phrases:
            if ph in low:
                return klass, rule, ph
    return None, "L0-unmatched", None


def selftest():
    """The lexicon must reproduce the three mis-typings we already know, and must NOT retype the rows
    we have already built as subsets. A lexicon that passes neither check is a lexicon nobody tested."""
    atlas = {json.loads(x)["problem_id"]: json.loads(x) for x in ATLAS.read_text().splitlines() if x.strip()}
    must_move = {"min-sum-set-cover": "REACH-permutation", "cutwidth": "REACH-permutation",
                 "domatic-number": "REACH-partition"}
    must_stay = ["d-hitting-set", "cluster-vertex-deletion", "subset-product", "max-coverage",
                 "minimum-test-cover", "connected-vertex-cover"]
    fails = []
    for p, want in must_move.items():
        got, rule, ph = classify(atlas.get(p, {}).get("canonical_encoding", ""))
        if got != want:
            fails.append(f"{p}: expected {want}, lexicon said {got} (rule {rule}, phrase {ph!r})")
    for p in must_stay:
        got, rule, ph = classify(atlas.get(p, {}).get("canonical_encoding", ""))
        if got not in ("REACH-subset", None):
            fails.append(f"{p}: a BUILT subset row was retyped to {got} (rule {rule}, phrase {ph!r})")
    return fails


def main() -> int:
    atlas = {json.loads(x)["problem_id"]: json.loads(x)
             for x in ATLAS.read_text().splitlines() if x.strip()}
    fails = selftest()
    if fails:
        print("LEXICON SELF-TEST FAILED — not run:")
        for f in fails:
            print("   " + f)
        return 1
    print("lexicon self-test passes: the three known mis-typings move, the six built rows stay\n")

    census = json.loads((LAT / "observatory_reach_census.json").read_text())
    adj = {a["problem_id"]: a for a in
           json.loads((LAT / "observatory_untyped_adjudication.json").read_text())["adjudications"]}
    subs = [r["problem_id"] for r in census["rows"]
            if (adj[r["problem_id"]]["now"] if r["problem_id"] in adj else r["reach_class"])
            == "REACH-subset"]

    built = set()
    for p in sorted(LAT.glob("observatory_batch*_panels.json")):
        d = json.loads(p.read_text())
        built |= {r["row"] for r in d["rows"]} | {e["row"] for e in d.get("excluded_at_birth", [])}
    built |= {x["row"] for x in
              json.loads((LAT / "sounding_v3_survey.json").read_text())["readings"] if x.get("row")}

    rows = []
    for pid in sorted(subs):
        enc = atlas.get(pid, {}).get("canonical_encoding", "") or ""
        klass, rule, ph = classify(enc)
        rows.append({"problem_id": pid, "was": "REACH-subset",
                     "now": klass or "UNMATCHED-needs-adjudication",
                     "rule_fired": rule, "matched_phrase": ph,
                     "retyped": bool(klass and klass != "REACH-subset"),
                     "already_built": pid in built,
                     "canonical_encoding": enc})

    by = Counter(r["now"] for r in rows)
    retyped = [r for r in rows if r["retyped"]]
    unmatched = [r for r in rows if r["now"].startswith("UNMATCHED")]
    clean = [r["problem_id"] for r in rows
             if r["now"] == "REACH-subset" and not r["already_built"]]
    built_but_retyped = [r["problem_id"] for r in retyped if r["already_built"]]

    doc = {
        "schema": "reach-subset-readjudication/v1",
        "STATUS": "TYPING — derived from each row's own canonical_encoding, not from judgement",
        "why": ("the census fired R3-subset-selection with identical boilerplate on rows whose own "
                "encoding says 'a linear order' and 'partitioned into'. The field was never read. This "
                "is the first reading of it, not a second opinion."),
        "method": ("sealed lexicon over atlas_v3.canonical_encoding, FIRST MATCH WINS, order part of "
                   "the rule — ordering before partition before assignment before subset, because the "
                   "later phrases occur inside the earlier ones"),
        "lexicon": [{"class": k, "rule": r, "phrases": p} for k, r, p in LEXICON],
        "selftest": "the three known mis-typings must move and six built subset rows must not",
        "n_examined": len(rows),
        "by_class": dict(by),
        "n_retyped": len(retyped),
        "n_unmatched": len(unmatched),
        "n_readable": len(rows) - len(unmatched),
        # THE DENOMINATOR IS THE WHOLE POINT, so it is stated three ways rather than once.
        "rate_among_readable": (round(len(retyped) / (len(rows) - len(unmatched)), 4)
                                if len(rows) > len(unmatched) else None),
        "rate_lower_bound_over_class": round(len(retyped) / len(rows), 4) if rows else None,
        "rate_caveat": (
            "THE CLASS RATE IS NOT KNOWN. The lexicon reads only the rows whose encoding contains one "
            "of its phrases; the rest are UNMATCHED, and an unmatched row is not a clean row. So "
            "`rate_among_readable` is a rate over a population selected by the instrument, and "
            "`rate_lower_bound_over_class` is a floor that assumes every unmatched row is correctly "
            "typed — which nothing supports. Reporting either alone as 'the misclassification rate' "
            "would be the denominator error this program has a gate against."),
        "coverage": round((len(rows) - len(unmatched)) / len(rows), 4) if rows else None,
        "coverage_note": ("the lexicon was sealed before it ran and is NOT tuned after seeing which "
                          "rows it missed. Broadening it is a v2 pass that declares its phrases first, "
                          "through the rule-before-computation channel."),
        "clean_subset_queue": clean,
        "n_clean_unbuilt": len(clean),
        "already_built_but_retyped": built_but_retyped,
        "built_but_retyped_note": ("frozen frames are NOT touched. A built row that retypes keeps its "
                                   "readings; what changes is which capture path future work uses."),
        "ENCODING_DISAGREES_WITH_CAPTURE": {
            "what": ("two rows were captured AS SUBSETS while the atlas encoding names a different "
                     "certificate object. The capture is not thereby wrong — a subset encoding of a "
                     "partition problem can be a faithful reformulation — but the two artifacts "
                     "disagree about what the row IS, and nothing currently records which governs."),
            "rows": {
                "3-partition": {
                    "atlas_encoding_says": "partition",
                    "captured_as": "size-3 subsets hitting the per-triple target (batch 4)",
                    "the_question": ("is the triple-subset region a faithful encoding of 3-partition, "
                                     "or a subset PROXY for it — the same move that made "
                                     "min-sum-set-cover look like set-cover?")},
                "minimum-common-string-partition": {
                    "atlas_encoding_says": "permutation",
                    "captured_as": "cut-position subsets of A that also partition B (batch 5)",
                    "the_question": ("the cut set determines the common partition, so the subset "
                                     "reading is arguably exact rather than a proxy — but that is an "
                                     "argument, and the atlas says otherwise")}},
            "disposition": "RAISED FOR RULING — not resolved here, and neither capture is withdrawn",
            "why_not_resolved_here": ("choosing between two artifacts that disagree about a row's "
                                      "identity is a typing ruling. Picking one silently is how the "
                                      "census's original error was made.")},
        "sized_populations": {
            "REACH-permutation": [r["problem_id"] for r in rows if r["now"] == "REACH-permutation"],
            "REACH-partition": [r["problem_id"] for r in rows if r["now"] == "REACH-partition"],
            "REACH-assignment": [r["problem_id"] for r in rows if r["now"] == "REACH-assignment"]},
        "partition_class_note": ("REACH-partition does not exist in the census vocabulary. It is minted "
                                 "here only if the population is non-empty — a class with no members is "
                                 "a category invented for tidiness."),
        "rows": rows,
    }
    OUT.write_text(json.dumps(doc, indent=1) + "\n")

    print(f"REACH-SUBSET RE-ADJUDICATION — {len(rows)} rows examined\n")
    for k, v in sorted(by.items(), key=lambda z: -z[1]):
        print(f"  {k:<32} {v}")
    print(f"\n  lexicon coverage       : {doc['coverage']:.1%}  ({doc['n_readable']} of {len(rows)} readable)")
    print(f"  retyped                : {len(retyped)}")
    print(f"    among readable       : {doc['rate_among_readable']:.1%}  (instrument-selected population)")
    print(f"    lower bound on class : {doc['rate_lower_bound_over_class']:.1%}  (assumes every "
          f"unmatched row is clean — nothing supports that)")
    print(f"  unmatched (needs human): {len(unmatched)}")
    print(f"  clean unbuilt queue    : {len(clean)}")
    if built_but_retyped:
        print(f"  ALREADY BUILT but retyped: {', '.join(built_but_retyped)}")
    print("\n  retyped rows:")
    for r in retyped[:40]:
        print(f"    {r['problem_id']:<34} -> {r['now']:<20} [{r['matched_phrase']}]")
    if unmatched:
        print("\n  unmatched (reported, never guessed):")
        for r in unmatched[:20]:
            print(f"    {r['problem_id']:<34} {r['canonical_encoding'][:70]}")

    M.emit(TRAIL, "annotation", key="annotation:reach-subset-readjudication",
           what=("all 127 REACH-subset rows re-typed by certificate object, derived from each row's own "
                 "canonical_encoding under a sealed lexicon"),
           n_examined=len(rows), n_retyped=len(retyped), n_unmatched=len(unmatched),
           rate_among_readable=doc["rate_among_readable"],
           rate_lower_bound_over_class=doc["rate_lower_bound_over_class"],
           lexicon_coverage=doc["coverage"],
           by_class=dict(by), touches_no_measured_value=True,
           frozen_frames_untouched=True,
           authority="owner ruling on Q22, 2026-07-27")
    print(f"\n  wrote {OUT.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
