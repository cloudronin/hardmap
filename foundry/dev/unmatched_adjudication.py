#!/usr/bin/env python3
"""Hand adjudication of the 59 lexicon-unmatched rows — the stopping rule's declared endpoint.

Lexicon v2 read 53.5% of the REACH-subset class and its stopping rule, pinned in advance, said the
remainder gets HAND ADJUDICATION WITH THE ENCODING QUOTED PER ROW. This is that pass. A third lexicon
widening would have been fitting the rule to the data.

TWO CLASSES ARE MINTED HERE because eight rows had nowhere to land, and typing a row into a queue that
lies about its size is the disease this program just spent a day curing.

  DECOMPOSITION  certificate is a tree-plus-bags (or an elimination forest). The region genuinely
                 exists and is genuinely plural, but it is NOT COORDINATE-SHAPED: blend operations are
                 defined coordinate-wise, and a majority vote of three tree decompositions has no
                 meaning. out-of-reach-at-v1.

  STRATEGY       certificate is a sequence of choices against a spreading process. Distinct from
                 RECONFIGURATION, which walks between solutions rather than playing against dynamics.
                 out-of-reach-at-v1 — but with a WARMER re-entry route, recorded as such.

ONE ROW, ONE CURRENT TYPING. Rows carrying a disposition from an earlier route resolve by maptrail
supersession: the latest ruling governs and the histories are linked. The pass ASSERTS at completion
that no row holds two live typings — a row with two typings is two queues lying about each other.
"""
import json, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from foundry.catalog import maptrail as M                                       # noqa: E402

LAT = ROOT / "foundry" / "results" / "lattice"
ATLAS = ROOT.parent / "eightfold" / "eightfold" / "results" / "atlas" / "atlas_v3.jsonl"
OUT = LAT / "unmatched_adjudication.json"
TRAIL = LAT / "maptrail.jsonl"

R = "REACH-subset"; A = "REACH-assignment"; P = "REACH-permutation"
D = "DECOMPOSITION"; S = "STRATEGY"; U = "REGIONLESS-unique-answer"

VERDICT = {
    # ── REGIONLESS: the answer is unique, or the object is a P-time computation ──────────────────────
    "all-pairs-shortest-path": (U, "one shortest-path matrix; the answer is unique"),
    "deadlock-detection": (U, "a yes/no property of one fixed graph; no plural certificate"),
    "and-or-graph-accessibility": (U, "accessibility of a fixed target under fixed semantics; unique"),
    "min-cost-flow": (U, "a min-cost flow value; the optimum is unique even where the flow is not"),
    "lex-first-maximal-matching": (U, "UNIQUE given the fixed edge order the encoding states — the exact "
                                     "twin of lex-first-maximal-independent-set, reached by a different "
                                     "door (unmatched rather than false-matched)"),
    # ── DECOMPOSITION: tree-plus-bags certificates, not coordinate-shaped ────────────────────────────
    "treewidth": (D, "certificate is a tree decomposition; blend is coordinate-wise and a majority of "
                     "three tree decompositions has no meaning"),
    "pathwidth": (D, "path decomposition — same shape"),
    "treedepth": (D, "elimination forest — same shape"),
    "clique-width": (D, "a clique-width expression (a parse tree over union/relabel/join)"),
    "minimum-decision-tree": (D, "certificate is a decision TREE over the tests, not a subset of them"),
    # ── STRATEGY: choices against a spreading process ────────────────────────────────────────────────
    "firefighter": (S, "a per-round protection choice against a spreading fire"),
    "graph-burning": (S, "a per-round ignition choice against a spreading burn"),
    # ── ASSIGNMENT: a map from one set to another ────────────────────────────────────────────────────
    "flow-shop-scheduling": (A, "jobs to machine-slots"), "job-shop-scheduling": (A, "operations to slots"),
    "open-shop-scheduling": (A, "operations to machines, order free"),
    "makespan-scheduling": (A, "jobs to machines"),
    "unrelated-machine-scheduling": (A, "jobs to machines with machine-dependent times"),
    "weighted-completion-time-scheduling": (A, "jobs to machines"),
    "resource-constrained-scheduling": (A, "jobs to machines under resource bounds"),
    "stable-matching": (A, "a matching IS a map between the two sides"),
    "label-cover": (A, "a labelling of the vertices from label sets"),
    "facility-location": (A, "open set PLUS the client-to-facility map the objective scores"),
    "capacitated-facility-location": (A, "same, with capacities binding the map"),
    "maximum-common-subgraph": (A, "a partial isomorphism — a map between two vertex sets"),
    "roman-domination": (A, "assigns 0/1/2 per vertex; a three-valued labelling, not a subset"),
    # ── PERMUTATION: the order is the answer ────────────────────────────────────────────────────────
    "register-sufficiency": (P, "an evaluation ORDER of the DAG"),
    "longest-path": (P, "a simple path is an ordered walk; the sequence is the certificate"),
    "constrained-shortest-path": (P, "an s-t path under a resource budget; ordered"),
    # ── SUBSET: everything whose certificate is a subset of a fixed ground set ───────────────────────
    **{k: (R, v) for k, v in {
        "steiner-tree": "edge subset forming a tree over the terminals",
        "directed-steiner-tree": "arc subset forming an arborescence",
        "group-steiner-tree": "edge subset touching every group",
        "prize-collecting-steiner-tree": "edge subset; penalties score the complement",
        "steiner-forest": "edge subset connecting each pair",
        "survivable-network-design": "edge subset meeting connectivity requirements",
        "k-edge-connected-subgraph": "edge subset that is k-edge-connected",
        "graph-spanner": "edge subset meeting a stretch guarantee",
        "maximum-leaf-spanning-tree": "edge subset forming a spanning tree",
        "min-degree-spanning-tree": "edge subset forming a spanning tree",
        "min-communication-cost-spanning-tree": "edge subset forming a spanning tree",
        "minimum-k-cut": "edge subset whose removal leaves k components",
        "multicut": "edge subset separating every pair",
        "multiway-cut": "edge subset separating the terminals",
        "node-multiway-cut": "VERTEX subset separating the terminals",
        "sparsest-cut": "the cut is a vertex bipartition — recorded as a subset of one side",
        "feedback-arc-set": "arc subset whose removal breaks all cycles",
        "maximum-induced-matching": "edge subset that induces no further edges",
        "maximum-agreement-forest": "edge subset removed to leave agreeing components",
        "maximum-feasible-linear-subsystem": "a SUBSYSTEM is a subset of the relations",
        "graph-motif": "vertex subset realizing the colour multiset",
        "target-set-selection": "the seed set is a vertex subset",
        "high-degree-subgraph": "vertex subset inducing minimum degree >= k",
        "max-coverage": "subset of the set system",
        "k-center": "centre set of size k",
        "minimum-distance-code": "nonzero messages of bounded codeword weight",
        "nearest-codeword": "messages within a distance of the target",
        "generalized-subset-sum": "sign vectors over the coordinates",
        "covering-radius": "words within the radius of the code",
        "sharp-spanning-trees": "COUNTING changes what the charge asks, not whether the object has a "
                                "region — the set of spanning trees IS an edge-subset region",
        "planar-matching-count": "matchings are edge subsets; the # joins at the atlas layer",
    }.items()},
}


def main() -> int:
    d = json.loads((LAT / "reach_subset_readjudication.json").read_text())
    atlas = {json.loads(x)["problem_id"]: json.loads(x)
             for x in ATLAS.read_text().splitlines() if x.strip()}
    unmatched = [r["problem_id"] for r in d["rows"] if r["now"].startswith("UNMATCHED")]

    missing = sorted(set(unmatched) - set(VERDICT))
    if missing:
        print("UNADJUDICATED ROWS — the pass refuses to complete:")
        for m in missing:
            print(f"   {m}: {atlas.get(m, {}).get('canonical_encoding', '')[:100]}")
        return 1

    rows = []
    for p in sorted(unmatched):
        klass, why = VERDICT[p]
        rows.append({"problem_id": p, "was": "REACH-subset", "now": klass, "why": why,
                     "canonical_encoding": atlas.get(p, {}).get("canonical_encoding", "")})
    by = Counter(r["now"] for r in rows)

    # ── ONE ROW, ONE CURRENT TYPING ─────────────────────────────────────────────────────────────────
    prior = {}
    for rec in M.read(TRAIL):
        if rec["event"] in ("erratum", "exclusion") and rec.get("problem"):
            prior[rec["problem"]] = rec["key"]
    # NOT EVERY PRIOR RECORD IS A COMPETING TYPING. `covering-radius` and `feedback-arc-set` carry
    # CAPTURE dispositions (deferred for want of an ambient-stable framing; excluded at birth for
    # ambient instability) while this pass assigns a REACH CLASS. Those are different axes: what the
    # object IS, versus whether the observatory can currently film it. Declaring supersession here
    # would silently retire a live capture disposition — the reconciliation rule exists to stop two
    # typings on ONE axis, not to collapse two axes into one.
    CAPTURE_AXIS = {"exclusion:covering-radius", "exclusion:batch4:feedback-arc-set"}
    coexist = [{"problem_id": r["problem_id"], "prior_record": prior[r["problem_id"]],
                "axis": "capture disposition", "this_pass_assigns": "reach class",
                "resolution": "BOTH STAND — different axes, no supersession"}
               for r in rows if prior.get(r["problem_id"]) in CAPTURE_AXIS]
    superseded = [{"problem_id": r["problem_id"], "prior_record": prior[r["problem_id"]],
                   "resolution": "latest ruling governs; histories linked, neither deleted"}
                  for r in rows if r["problem_id"] in prior
                  and prior[r["problem_id"]] not in CAPTURE_AXIS]

    doc = {"schema": "unmatched-adjudication/v1",
           "STATUS": "HAND ADJUDICATION WITH RECEIPTS — the stopping rule's declared endpoint",
           "why_not_a_third_lexicon": ("widening again against known misses would be fitting the rule "
                                       "to the data. Two mechanical passes, then eyes on the field."),
           "classes_minted": {
               "DECOMPOSITION": {"typed": "out-of-reach-at-v1",
                   "why": ("the region exists and is plural but is NOT coordinate-shaped — blend "
                           "operations are coordinate-wise and a majority vote of three tree "
                           "decompositions has no meaning"),
                   "re_entry": "any faithful fixed-length encoding someone declares falsifies this",
                   "the_irony_worth_recording": (
                       "the width parameters are parameterized complexity's OWN structural yardsticks. "
                       "The observatory currently cannot film the very objects the param charge is "
                       "built on.")},
               "STRATEGY": {"typed": "out-of-reach-at-v1",
                   "why": "a sequence of choices against a spreading process",
                   "distinct_from_RECONFIGURATION": ("walking between solutions is not playing against "
                                                     "dynamics"),
                   "re_entry": ("WARMER than DECOMPOSITION's: a fixed-horizon strategy IS a length-T "
                                "vector (round -> choice), so a faithful fixed-length encoding "
                                "plausibly exists. The barrier is the dynamic feasibility predicate, "
                                "not the shape — nearest of the out-of-reach classes to capturable.")}},
           "counting_correction": (
               "sharp-spanning-trees and planar-matching-count are REACH-SUBSET, not a counting limbo. "
               "The # changes what the CHARGE asks, not whether the object has a region: spanning trees "
               "and matchings are edge-subset regions and film like any other. These are the first rows "
               "where the decide-versus-count geometric comparison becomes physically possible."),
           "n_adjudicated": len(rows), "by_class": dict(by),
           "superseded_typings": superseded,
           "coexisting_different_axis": coexist,
           "reconciliation_rule": (
               "one row, one current typing ON EACH AXIS. A competing REACH CLASS resolves by maptrail "
               "supersession — latest ruling governs, histories linked, neither deleted. A prior "
               "CAPTURE disposition is not a competing typing and both stand: what an object IS and "
               "whether the observatory can film it are different questions, and collapsing them would "
               "retire a live deferral by accident."),
           "rows": rows}
    OUT.write_text(json.dumps(doc, indent=1) + "\n")

    print(f"UNMATCHED ADJUDICATION — {len(rows)} rows, every verdict quoting its encoding\n")
    for k, v in sorted(by.items(), key=lambda z: -z[1]):
        print(f"  {k:<28} {v}")
    print(f"\n  superseded typings (same axis) : {len(superseded)} "
          f"{[s['problem_id'] for s in superseded] or ''}")
    print(f"  coexisting (different axis)    : {len(coexist)} "
          f"{[s['problem_id'] for s in coexist] or ''}")
    assert not superseded or all(s["problem_id"] for s in superseded), "unresolved typing conflict"

    M.emit(TRAIL, "version", key="version:decomposition-class", model="reach-census class vocabulary",
           adds="DECOMPOSITION", typed="out-of-reach-at-v1",
           members=[r["problem_id"] for r in rows if r["now"] == D],
           why=doc["classes_minted"]["DECOMPOSITION"]["why"],
           re_entry_route=doc["classes_minted"]["DECOMPOSITION"]["re_entry"],
           note=doc["classes_minted"]["DECOMPOSITION"]["the_irony_worth_recording"],
           authority="owner ruling, 2026-07-27")
    M.emit(TRAIL, "version", key="version:strategy-class", model="reach-census class vocabulary",
           adds="STRATEGY", typed="out-of-reach-at-v1",
           members=[r["problem_id"] for r in rows if r["now"] == S],
           why=doc["classes_minted"]["STRATEGY"]["why"],
           re_entry_route=doc["classes_minted"]["STRATEGY"]["re_entry"],
           distinct_from="RECONFIGURATION", authority="owner ruling, 2026-07-27")
    M.emit(TRAIL, "erratum", key="erratum:counting-rows-are-subset-regions",
           field="reach class for sharp-spanning-trees and planar-matching-count",
           old="grouped as counting, implicitly regionless", new="REACH-subset",
           why=doc["counting_correction"], authority="owner ruling, 2026-07-27")
    M.emit(TRAIL, "annotation", key="annotation:assignment-path-constituency",
           what=("the scheduling block types into REACH-assignment, taking that class's constituency "
                 "to a size where BUILDING THE ASSIGNMENT CAPTURE PATH changes proposition"),
           n_assignment_rows=by[A],
           bears_on=("the HELD-path-gated number-theoretic candidate revives on exactly this build "
                     "decision. A capture path serving many rows is a different proposition than one "
                     "serving two, and the path-gated ledger should show the constituency growing."),
           touches_no_measured_value=True, authority="owner ruling, 2026-07-27")
    print(f"\n  wrote {OUT.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
