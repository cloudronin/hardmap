#!/usr/bin/env python3
"""Atlas v3 (Quarry broad expansion) builder — drafts full ProblemEntry rows at `claimed`.

Reuses build_atlas.py's DSL shape; writes WORKING per-wave files beside the frozen atlas (freeze is
V3, a separate finalizer). Every row is a full 8-cell ProblemEntry; the un-cited charges are typed
sentinels (R1/R2/E2) per the atlas convention. All real values are `claimed` (owner confirm pending).
Per-row provenance (funnel/wave/quarry_member/single_charge) goes to a SIDECAR, never in the row
(the frozen schema pins its bytes — Quarry-SCHEMA.md §0).
"""
import json, os

DATE = "2026-07-23"
REVIEWER = "Claude Code (Atlas v3 draft; claimed — owner confirm pending)"
ATLAS_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                          "..", "eightfold", "results", "atlas"))

# ---- DSL (mirrors dev/build_atlas.py) ----
def cell(charge, value, task, cite=None, status="claimed", perspective=None, note=None, contested=None):
    prov = {}
    if cite: prov["citation"] = cite
    if note: prov["note"] = note
    return {"charge": charge, "value": value, "canonical_task": task, "status": status,
            "provenance": prov, "perspective": perspective, "contested_note": contested}

def na(charge, why):
    return cell(charge, "n.a.", why, status="structural")

def op(charge, task, note=None):
    return cell(charge, "open", task, status="structural", note=note)

def entry(pid, name, family, enc, cells, notes=None):
    return {"problem_id": pid, "problem_name": name, "problem_family": family, "canonical_encoding": enc,
            "charges": cells, "last_reviewed": DATE, "reviewer": REVIEWER, "notes": notes}

ROWS = []       # (wave, funnel, quarry_member, entry_dict)

def add(wave, funnel, qmember, e):
    ROWS.append((wave, funnel, qmember, e))

# ---- archetype: a P-complete (within-P-hard) problem: decision=P + parallelization=P-complete ----
def p_complete(pid, name, family, enc, dec_task, dec_cite, par_task, par_cite,
               wave="W1", funnel="ghr", qmember=True, counting=None):
    cnt = (cell("counting", counting[0], counting[1], counting[2]) if counting
           else na("counting", "not a solution-counting problem in the NP sense"))
    add(wave, funnel, qmember, entry(pid, name, family, enc, [
        cell("decision", "P", dec_task, dec_cite),
        cnt,
        na("approximation", "decision is in P; not an NP-optimization problem"),
        na("parameterized", "decision is in P; no standard W-hierarchy parameterization"),
        cell("parallelization", "P-complete", par_task, par_cite),
        na("proof_size", "not a propositional refutation problem"),
        na("average_case", "not a random-ensemble hardness object (deterministic P-complete)"),
        na("landscape", "not a random-ensemble solution-geometry object"),
    ]))

# ========================= WAVE 1 — parallelization (GHR) =========================
GHR = "Greenlaw, Hoover & Ruzzo, Limits to Parallel Computation: P-Completeness Theory (1995)"

p_complete("and-or-graph-accessibility", "AND/OR Graph Accessibility (AGAP)", "graph",
  "an AND/OR graph with a source set; decision: is a target vertex accessible (AND-vertices need all in-neighbors, OR-vertices any)?",
  "alternating reachability closure, poly-time", "Immerman, Number of quantifiers is better than number of tape cells, JCSS 22 (1981); GHR (1995)",
  "AGAP is P-complete (canonical alternating-reachability)", GHR, funnel="ghr")

p_complete("context-free-membership", "Context-Free Grammar Membership (CFL recognition)", "logic-proof",
  "a context-free grammar G and a string w; decision: is w in L(G)?",
  "CYK recognition, O(n^3)", "Jones & Laaser, Complete problems for deterministic polynomial time, TCS 3 (1976)",
  "CFL membership is P-complete", "Jones & Laaser (1976); GHR (1995)", funnel="ghr")

p_complete("unification", "First-Order Term Unification", "logic-proof",
  "two first-order terms; decision: do they have a most-general unifier (is a given variable bound)?",
  "linear-time unification (Paterson-Wegman)", "Paterson & Wegman, Linear unification, JCSS 16 (1978)",
  "unification is P-complete (log-space complete for P)", "Dwork, Kanellakis & Mitchell, On the sequential nature of unification, J. Logic Prog. 1 (1984); GHR (1995)", funnel="ghr")

p_complete("dfs-lexicographic-ordering", "Lexicographic Depth-First Search Ordering", "graph",
  "a graph with a fixed vertex order and vertices u,v; decision: does u precede v in the lexicographic DFS numbering?",
  "computable in P by ordered DFS", "Reif, Depth-first search is inherently sequential, Inf. Proc. Lett. 20 (1985)",
  "lexicographic DFS ordering is P-complete", "Reif (1985); GHR (1995)", funnel="ghr")

p_complete("lex-first-maximal-matching", "Lexicographically-First Maximal Matching", "graph",
  "a graph with a fixed edge order and an edge e; decision: is e in the lexicographically-first maximal matching (greedy in order)?",
  "computable in P by greedy edge selection", "Miyano, The lexicographically first maximal subgraph problems, Int. J. Found. Comput. Sci. 1 (1990)",
  "LFMM is P-complete (edge object, distinct from LFMIS)", "Miyano (1990); GHR (1995)", funnel="ghr")

p_complete("high-degree-subgraph", "High-Degree Subgraph", "graph",
  "a graph G and integer k>=3; decision: does G have a nonempty induced subgraph of minimum degree >= k (does a given vertex survive the k-core-style peeling)?",
  "computable in P by iterated low-degree deletion", "Anderson & Mayr, A P-complete problem and approximations to it (1984)",
  "k-HDS is P-complete for k>=3 (in NC for k<=2)", "Anderson & Mayr (1984); GHR (1995)", funnel="ghr")

p_complete("generability", "Generability (GEN)", "logic-proof",
  "a finite set X, a binary operation table on X, a seed subset S, a target t; decision: is t in the closure of S under the operation?",
  "closure computation, poly-time", "Jones & Laaser, Complete problems for deterministic polynomial time, TCS 3 (1976)",
  "GEN is P-complete (canonical monotone-closure problem)", "Jones & Laaser (1976); GHR (1995)", funnel="ghr")

p_complete("unit-resolution", "Unit Resolution", "sat-csp",
  "a CNF formula; decision: can the empty clause be derived by unit resolution (unit-clause propagation)?",
  "unit propagation to fixpoint, poly-time", GHR,
  "unit resolution / unit-clause propagation is P-complete", "GHR (1995); cf. Jones & Laaser (1976)", funnel="ghr")

p_complete("datalog-evaluation", "Datalog Evaluation (data complexity)", "logic-proof",
  "a fixed Datalog program and an input database (EDB) + a target fact; decision: is the fact in the least fixpoint? (data complexity, program fixed)",
  "bottom-up fixpoint evaluation, poly-time in the data", "Dantsin, Eiter, Gottlob & Voronkov, Complexity and expressive power of logic programming, ACM Comput. Surv. 33 (2001)",
  "Datalog data complexity is P-complete", "Immerman/Vardi; Dantsin-Eiter-Gottlob-Voronkov (2001)", funnel="ghr")

p_complete("cellular-automaton-prediction", "Cellular Automaton / Game of Life Prediction", "logic-proof",
  "a cellular automaton, an initial configuration, a cell c, and a step count t in unary; decision: is c alive at step t?",
  "simulate t steps, poly-time in (t, size)", "GHR (1995); Berlekamp, Conway & Guy, Winning Ways (Game of Life universality)",
  "CA t-step prediction is P-complete", GHR, funnel="ghr")

p_complete("chip-firing-stabilization", "Abelian Sandpile / Chip-Firing Stabilization", "graph",
  "a graph with a chip configuration; decision: after stabilization (fire any vertex with chips >= degree), does a given vertex fire / hold >= k chips?",
  "abelian stabilization is order-independent, poly-time", "Bjorner, Lovasz & Shor, Chip-firing games on graphs, Eur. J. Combin. 12 (1991)",
  "sandpile prediction is P-complete in dimension >= 3", "Moore & Nilsson, The computational complexity of sandpiles, J. Stat. Phys. 96 (1999)", funnel="ghr")

p_complete("gaussian-elimination-pivoting", "Gaussian Elimination with Partial Pivoting", "matrix",
  "a rational matrix and a target pivot position; decision: is a given entry the pivot at a given step under partial-pivoting Gaussian elimination?",
  "run GE with partial pivoting, poly-time", "Vavasis, Gaussian elimination with pivoting is P-complete, SIAM J. Discrete Math. 2 (1989)",
  "GE with partial pivoting is P-complete (unlike determinant/linear-equations, which are in NC)", "Vavasis (1989)", funnel="ghr")

p_complete("plane-sweep-triangulation", "Plane-Sweep Triangulation", "geometric",
  "a simple polygon (possibly with holes) and a diagonal; decision: is the diagonal in the top-to-bottom plane-sweep triangulation?",
  "sweepline triangulation, poly-time", "Atallah, Callahan & Goodrich, P-complete geometric problems, Int. J. Comput. Geom. Appl. 3 (1993)",
  "plane-sweep triangulation is P-complete", "Atallah-Callahan-Goodrich (1993); GHR (1995)", funnel="ghr")

p_complete("lz78-compression", "LZ78 / LZW Compression", "string",
  "a string s and a factor t; decision: does compressing s with the LZ78 greedy parse add t to the dictionary?",
  "greedy LZ78 dictionary parse, poly-time", "De Agostino & Storer, On-line versus off-line computation in dynamic text compression, Inf. Proc. Lett. 59 (1996)",
  "LZ78 dictionary membership is P-complete", "De Agostino & Storer (1996)", funnel="ghr")

p_complete("breadth-depth-search", "Breadth-Depth Search Ordering", "graph",
  "a graph with a fixed adjacency order and vertices u,v; decision: does u precede v in the breadth-depth search numbering?",
  "computable in P by breadth-depth search", "Greenlaw, Breadth-depth search is P-complete, Parallel Proc. Lett. 3 (1993)",
  "breadth-depth search ordering is P-complete", "Greenlaw (1993); GHR (1995)", funnel="ghr")

p_complete("deadlock-detection", "Deadlock Detection (single-unit resources)", "graph",
  "a single-unit resource-allocation graph; decision: is the system deadlocked (an unresolvable wait cycle)?",
  "resource-graph reduction, poly-time", "Spirakis, The parallel complexity of deadlock detection (1986); GHR (1995)",
  "single-unit deadlock detection is P-complete (log-space complete for P)", "Spirakis (1986); GHR (1995)", funnel="ghr")

p_complete("lex-first-delta-plus-one-coloring", "Lexicographically-First (Delta+1)-Coloring", "graph",
  "a graph with a fixed vertex order, a vertex v and a color c; decision: does v receive color c under greedy first-fit coloring in that order?",
  "greedy first-fit coloring, poly-time", "GHR (1995)",
  "lex-first greedy (Delta+1)-coloring is P-complete", GHR, funnel="ghr")

p_complete("context-free-emptiness", "Context-Free Grammar Emptiness", "logic-proof",
  "a context-free grammar G; decision: is L(G) empty (is the start symbol non-productive)?",
  "grammar productivity closure, poly-time", "Jones & Laaser, Complete problems for deterministic polynomial time, TCS 3 (1976)",
  "CFG emptiness/productivity is P-complete", "Jones & Laaser (1976); GHR (1995)", funnel="ghr")

p_complete("type-inference-typability", "Simple Type Inference / Typability", "logic-proof",
  "a lambda-term in the simply-typed calculus (or with partial types); decision: is the term typable?",
  "constraint-based type inference via unification, poly-time (simply-typed)", "O'Toole & Gifford; Dwork, Kanellakis & Mitchell (1984)",
  "simple-type typability is P-complete (log-space equiv. to unification; full ML let-polymorphism is DEXPTIME)", "Dwork-Kanellakis-Mitchell (1984); GHR (1995)", funnel="ghr")

# ---- write per-wave working files + provenance sidecar ----
def _derive_single_charge(e):
    reals = [c for c in e["charges"] if c["status"] != "structural"]
    return len(reals) == 1

def main():
    by_wave = {}
    prov = []
    for wave, funnel, qmember, e in ROWS:
        by_wave.setdefault(wave, []).append(e)
        prov.append({"problem_id": e["problem_id"], "source_funnel": funnel,
                     "admission_wave": wave, "quarry_member": qmember,
                     "single_charge": _derive_single_charge(e)})
    for wave, rows in by_wave.items():
        path = os.path.join(ATLAS_DIR, f"quarry-v3-{wave.lower()}.jsonl")
        with open(path, "w") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(f"{wave}: wrote {len(rows)} rows -> {os.path.basename(path)}")
    ppath = os.path.join(ATLAS_DIR, "quarry-v3-provenance.jsonl")
    with open(ppath, "w") as f:
        for p in prov:
            f.write(json.dumps(p, ensure_ascii=False) + "\n")
    print(f"provenance: wrote {len(prov)} rows -> {os.path.basename(ppath)}")
    print(f"single_charge rows: {sum(1 for p in prov if p['single_charge'])}")

if __name__ == "__main__":
    main()
