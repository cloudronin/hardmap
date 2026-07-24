#!/usr/bin/env python3
"""Quarry K3 — build the 10 pilot ProblemEntry drafts (schema-valid) at `claimed` status.

These are AGENT DRAFTS: status `claimed` (a resolvable citation, owner-confirm pending) — never
`confirmed` (the owner's call after reading the primary source). NOT ingested: emitted to a file
BESIDE the frozen atlas.jsonl, which is never touched. Every charge is typed (real value + citation,
or a sentinel with an R1/R2 reason). Where a value cannot be established at Check-9 (R20) standard it
is `open` + note — never pattern-matched (the F-1 lesson). Validated by `eightfold.atlas validate`.

Helpers mirror dev/build_atlas.py's DSL exactly so the output matches the atlas schema.
"""
import json, os

DATE = "2026-07-23"
REVIEWER = "Claude Code (Quarry K3 draft; claimed — owner confirm pending)"
OUT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "..", "eightfold", "results", "atlas", "quarry-pilot-rows.jsonl"))

def cell(charge, value, task, cite=None, status="claimed", perspective=None, note=None, contested=None):
    prov = {}
    if cite: prov["citation"] = cite
    if note: prov["note"] = note
    return {"charge": charge, "value": value, "canonical_task": task, "status": status,
            "provenance": prov, "perspective": perspective, "contested_note": contested}

def na(charge, why):  # R2 sentinel: charge structurally does not apply
    return cell(charge, "n.a.", why, status="structural")

def op(charge, task, note=None):  # R2 sentinel: applies, value unknown/uncurated
    return cell(charge, "open", task, status="structural", note=note)

def entry(pid, name, family, enc, cells, notes=None):
    return {"problem_id": pid, "problem_name": name, "problem_family": family, "canonical_encoding": enc,
            "charges": cells, "last_reviewed": DATE, "reviewer": REVIEWER, "notes": notes}

# citation shorthands (resolvable; `claimed` standard)
KARP72 = "Karp, Reducibility among combinatorial problems, in Complexity of Computer Computations (1972) 85-103"
GJ = "Garey & Johnson, Computers and Intractability (1979)"
JVW90 = "Jaeger, Vertigan & Welsh, On the computational complexity of the Jones and Tutte polynomials, Math. Proc. Camb. Phil. Soc. 108 (1990) 35-53"
ZUCK07 = "Zuckerman, Linear degree extractors and the inapproximability of max clique and chromatic number, Theory of Computing 3 (2007) 103-128"
DF99 = "Downey & Fellows, Parameterized Complexity (1999)"
VAL79 = "Valiant, The complexity of computing the permanent / of enumeration and reliability problems, TCS 8 & SIAM J. Comput. 8 (1979)"
FAS_APX = "Even, Naor, Schieber & Sudan, Approximating minimum feedback sets and multicuts in directed graphs, Algorithmica 20 (1998) 151-174"
FAS_UGC = "Guruswami, Hastad, Manokaran, Raghavendra & Charikar, Beating the random ordering is hard: every ordering CSP is approximation resistant, SIAM J. Comput. 40 (2011)"
FAS_FPT = "Chen, Liu, Lu, O'Sullivan & Razgon, A fixed-parameter algorithm for the directed feedback vertex set problem, JACM 55 (2008)"
HN13 = "Hartung & Nichterlein, On the parameterized and approximation hardness of metric dimension, CCC 2013 (arXiv:1211.1636)"
KRR96 = "Khuller, Raghavachari & Rosenfeld, Landmarks in graphs, Discrete Appl. Math. 70 (1996) 217-229"
COOK85 = "Cook, A taxonomy of problems with fast parallel algorithms, Information and Control 64 (1985); via Greenlaw, Hoover & Ruzzo, Limits to Parallel Computation (1995)"
GHR95 = "Greenlaw, Hoover & Ruzzo, Limits to Parallel Computation: P-Completeness Theory (1995)"
COOK74 = "Cook, An observation on time-storage trade-off, STOC 1973 / JCSS 9 (1974) [Path System Accessibility: first P-complete problem]; catalogued in Greenlaw-Hoover-Ruzzo (1995)"
DBC02 = "Dunne & Bench-Capon, Coherence in finite argument systems, Artificial Intelligence 141 (2002) 187-203 [skeptical acceptance under preferred semantics is Pi_2^p-complete]"
DSW12 = "Dvorak, Szeider & Woltran, Abstract argumentation via monadic second order logic, SUM 2012 / Dvorak et al., Complexity of abstract argumentation under bounded treewidth (fixed-parameter tractable by treewidth)"
SCHAEFER78 = "Schaefer, On the complexity of some two-person perfect-information games, JCSS 16 (1978) 185-225 [Generalized Geography PSPACE-complete]"
KL83 = "Karp & Luby, Monte-Carlo algorithms for enumeration and reliability problems, FOCS 1983 [FPRAS for #DNF]"
CCLW14 = "Caprara, Carvalho, Lodi & Woeginger, A study on the computational complexity of the bilevel knapsack problem, SIAM J. Optim. 24(2) (2014) 823-838"

ROWS = []

# ---- 1. chromatic-number (multi-compendium graph/opt) ----
ROWS.append(entry("chromatic-number", "Chromatic Number (Vertex Coloring, optimization)", "graph",
  "simple undirected graph, adjacency-list (sparse), size (n,m); objective = minimum #colors in a proper vertex coloring", [
  cell("decision", "NPC", "k-Colorability decision (chi(G) <= k)", KARP72, note="one of Karp's 21; 3-COL (graph-3-coloring) is the k=3 restriction, a separate row (S2)"),
  cell("counting", "#P-complete", "#proper k-colorings (k>=3) / chromatic-polynomial evaluation P(G,k)", JVW90, note="per-problem #P-hardness of evaluating the chromatic polynomial at k>=3 (not a folklore stamp) [F-1]"),
  cell("approximation", "inapprox", "approximate chi(G); n^(1-eps) inapprox unless P=NP", ZUCK07,
       contested="coded `inapprox` to MATCH the atlas clique precedent (identical n^(1-eps) status); under a strict F-2 reading both are poly-APX (trivial n-coloring). Known vocab tension (cf. directed-steiner-tree)."),
  cell("parameterized", "para-NP-hard", "chi(G) parameterized by number of colors k; NP-hard at fixed k=3", GJ, perspective="number of colors k", note="para-NP-hard by the natural parameter; FPT by treewidth (k^{tw} DP) is the alternative perspective"),
  na("parallelization", "NPC => not in P unless P=NP; within-P charge n.a. (E2)"),
  na("proof_size", "not a propositional refutation problem"),
  op("average_case", "chromatic number of G(n,p): concentration is studied (Bollobas; Achlioptas-Naor) but algorithmic average-case hardness is not cleanly established; ensemble exists => open not n.a. (R15)"),
  na("landscape", "no curated random-ensemble solution-space clustering result (physics results on coloring exist but are uncurated here)")]))

# ---- 2. subgraph-isomorphism (multi-compendium graph) ----
ROWS.append(entry("subgraph-isomorphism", "Subgraph Isomorphism (non-induced)", "graph",
  "two simple graphs: pattern H on k vertices, host G on n; decision: does G contain H as a (non-induced) subgraph?", [
  cell("decision", "NPC", "Subgraph Isomorphism decision (H a subgraph of G)", GJ, note="GJ [GT48]; generalizes CLIQUE and HAMILTONIAN-CYCLE. Distinct from induced-subgraph-isomorphism (induced) and graph-isomorphism (S2)"),
  op("counting", "#copies of H in G: #P-hard in general (generalizes #k-cliques, #Hamiltonian-paths), but a clean per-problem #P-completeness cite for the GENERAL non-induced version needs owner confirmation",
     note="F-1 DOWNGRADE: plausible #P-complete but not established at Check-9 here -> open, not a pattern-matched value"),
  na("approximation", "decision problem; no standard optimization version (Maximum Common Subgraph is the separate opt row)"),
  cell("parameterized", "W[1]", "k-Subgraph Isomorphism parameterized by pattern size k: W[1]-complete", DF99, perspective="pattern size k", note="CLIQUE (special case) is W[1]-complete; canonical"),
  na("parallelization", "NPC => within-P charge n.a. (E2)"),
  na("proof_size", "not a propositional refutation problem"),
  op("average_case", "subgraph appearance thresholds in G(n,p) are studied; algorithmic average-case detection hardness not curated"),
  na("landscape", "no curated random-ensemble solution-geometry result")]))

# ---- 3. feedback-arc-set (multi-compendium graph; currency-check charge) ----
ROWS.append(entry("feedback-arc-set", "Minimum Feedback Arc Set (general directed)", "graph",
  "simple directed graph, adjacency-list; objective = minimum arc set whose removal makes G acyclic", [
  cell("decision", "NPC", "FAS decision: acyclic after removing <= k arcs?", KARP72, note="one of Karp's 21. Distinct from feedback-arc-set-tournament (restriction, S2) and directed-feedback-vertex-set (arcs vs vertices, S2); Maximum Acyclic Subgraph is the complement -> MERGES here (S2)"),
  op("counting", "#minimum feedback arc sets: not curated"),
  cell("approximation", "log-APX", "MIN-FAS: O(log n log log n)-approx; no constant-factor under UGC", FAS_APX, note="currency (post-2000): O(log n loglog n) upper (Even-Naor-Schieber-Sudan 1998); UGC-hardness of any constant factor (Guruswami-Hastad-Manokaran-Raghavendra-Charikar 2011). See "+FAS_UGC,
       contested="log-APX is the closest vocab rung; the loglog factor and UGC-conditional (not unconditional) hardness make this an F-2 vocab-boundary case (cf. directed-steiner-tree)"),
  cell("parameterized", "FPT", "FAS parameterized by solution size k", FAS_FPT, perspective="solution size k", note="O*(4^k) via the DFVS technique"),
  na("parallelization", "NPC => within-P charge n.a. (E2)"),
  na("proof_size", "not a propositional refutation problem"),
  op("average_case", "FAS on random tournaments/digraphs is studied; algorithmic average-case hardness not curated"),
  na("landscape", "no curated random-ensemble solution-geometry result")]))

# ---- 4. metric-dimension (multi-compendium graph; fills W[2]) ----
ROWS.append(entry("metric-dimension", "Metric Dimension", "graph",
  "simple undirected connected graph, adjacency-list; a resolving set S separates every vertex pair by distance; objective = minimum |S|", [
  cell("decision", "NPC", "Metric Dimension decision: resolving set of size <= k?", GJ, note="GJ [GT61]; Khuller-Raghavachari-Rosenfeld 1996 ("+KRR96+")"),
  na("counting", "not a natural solution-counting problem"),
  cell("approximation", "log-APX", "MIN resolving set: Theta(log n)-approx; o(log n)-inapprox unless P=NP", HN13, note="inapproximable within o(log n) even on max-degree-3 graphs (Hartung-Nichterlein 2013); set-cover-like"),
  cell("parameterized", "W[2]+", "Metric Dimension parameterized by solution size k: W[2]-complete", HN13, perspective="solution size k", note="W[2]-complete even on max-degree-3 graphs (Hartung-Nichterlein 2013); fills the sparse W[2]+ end"),
  na("parallelization", "NPC => within-P charge n.a. (E2)"),
  na("proof_size", "not a propositional refutation problem"),
  op("average_case", "metric dimension of random graphs studied (Bollobas-Mitsche-Pralat) but algorithmic average-case hardness not curated"),
  na("landscape", "no curated random-ensemble solution-geometry result")]))

# ---- 5. lex-first-maximal-independent-set (parallelization-led) ----
ROWS.append(entry("lex-first-maximal-independent-set", "Lexicographically-First Maximal Independent Set (LFMIS)", "graph",
  "simple undirected graph with a fixed vertex order; decision: is vertex v in the lexicographically-first maximal independent set (greedy in order)?", [
  cell("decision", "P", "LFMIS membership: computable greedily in polynomial time", COOK85, note="in P (sequential greedy). Distinct from independent-set (lex-first selection object, S2)"),
  na("counting", "the lex-first MIS is UNIQUE by definition; counting it is degenerate (exactly one) -> no natural counting version. NOTE: this FALSIFIES the K2 provisional gap-hint 'counting=FP x parallelization=P-complete' for LFMIS"),
  na("approximation", "decision is in P; exactly determined, no optimization ratio"),
  na("parameterized", "decision is in P; no standard W-hierarchy parameterization"),
  cell("parallelization", "P-complete", "LFMIS is P-complete (hard to parallelize)", COOK85, note="canonical P-complete problem (Cook 1985; GHR 1995)"),
  na("proof_size", "not a propositional refutation problem"),
  na("average_case", "not a random-ensemble hardness object (deterministic P-complete)"),
  na("landscape", "not a random-ensemble solution-geometry object")]))

# ---- 6. path-system-accessibility (parallelization-led) ----
ROWS.append(entry("path-system-accessibility", "Path System Accessibility", "logic-proof",
  "a path system (set of rules (x,y,z): x accessible if y and z are) with source set; decision: is a target vertex accessible?", [
  cell("decision", "P", "Path System Accessibility: computable in polynomial time (closure)", COOK74),
  na("counting", "not a solution-counting problem in the NP sense"),
  na("approximation", "decision in P; not an optimization problem"),
  na("parameterized", "decision in P; no standard parameterization"),
  cell("parallelization", "P-complete", "Path System Accessibility is P-complete", COOK74, note="Cook's original P-complete problem (1974); the historic anchor of P-completeness theory (GHR 1995)"),
  na("proof_size", "not a propositional refutation problem"),
  na("average_case", "not a random-ensemble hardness object"),
  na("landscape", "not a random-ensemble solution-geometry object")]))

# ---- 7. abstract-argumentation (beyond-NP decision + parameterized) ----
# K3 HAND-CHECK CORRECTION: credulous+preferred is only NP-complete; the beyond-NP value requires
# SKEPTICAL+preferred (Pi_2^p) or credulous+semi-stable (Sigma_2^p). Retyped to skeptical+preferred.
ROWS.append(entry("abstract-argumentation", "Skeptical Acceptance in Abstract Argumentation (preferred semantics)", "logic-proof",
  "a Dung argumentation framework (directed graph of arguments + attacks); decision: is a given argument skeptically accepted — in EVERY preferred extension?", [
  cell("decision", "PH-complete", "skeptical acceptance under preferred semantics (argument in all preferred extensions): Pi_2^p-complete", DBC02, perspective="Pi_2^p", note="beyond-NP. K3 HAND-CHECK CORRECTION (Check 2/9 object/semantics mismatch): credulous+preferred is only NP-complete; skeptical+preferred is Pi_2^p-complete (Dunne-Bench-Capon 2002), credulous+semi-stable is Sigma_2^p-complete (Dvorak-Woltran 2010). The original claimed value was wrong."),
  na("counting", "counting preferred extensions is #.coNP-style, not an #P-witness-counting version"),
  na("approximation", "a decision (acceptance) problem; no standard optimization version"),
  cell("parameterized", "FPT", "skeptical acceptance parameterized by treewidth of the framework: fixed-parameter tractable", DSW12, perspective="treewidth", note="acceptance under the main semantics is FPT by treewidth via MSO / Courcelle (Dvorak-Szeider-Woltran)"),
  na("parallelization", "Pi_2^p-complete => not in P unless PH collapses; within-P charge n.a."),
  na("proof_size", "not a propositional refutation problem"),
  op("average_case", "random argumentation frameworks are studied empirically; algorithmic average-case hardness not curated"),
  na("landscape", "no curated random-ensemble solution-geometry result")]))

# ---- 8. generalized-geography (beyond-NP decision; fills sparse PSPACE) ----
ROWS.append(entry("generalized-geography", "Generalized Geography", "logic-proof",
  "a directed graph with a start vertex; two players alternately extend a simple path; a player unable to move loses; decision: does player 1 have a winning strategy?", [
  cell("decision", "PSPACE-complete", "Generalized Geography: deciding a winning strategy is PSPACE-complete", SCHAEFER78, note="canonical PSPACE game; distinct from TQBF (different object, S2). Fills the sparse PSPACE decision cell (2 rows)"),
  na("counting", "not a solution-counting problem in the NP sense"),
  na("approximation", "not an NP-optimization problem"),
  na("parameterized", "no standard W-hierarchy parameterization curated"),
  na("parallelization", "PSPACE-complete => not in P unless P=PSPACE; within-P charge n.a."),
  na("proof_size", "not a propositional refutation problem (a game, not a formula family)"),
  op("average_case", "random game instances not curated for algorithmic average-case hardness"),
  na("landscape", "not a random-ensemble solution-geometry object")]))

# ---- 9. sharp-dnf (#DNF; counting decoupling witness) ----
ROWS.append(entry("sharp-dnf", "#DNF (count satisfying assignments of a DNF formula)", "logic-proof",
  "a DNF formula over n Boolean variables; count the number of satisfying assignments", [
  cell("decision", "P", "DNF satisfiability is trivially in P (a DNF is satisfiable unless every term is contradictory)", GJ, note="the decision version is easy -> a decoupling witness against the hard counting version"),
  cell("counting", "#P-complete", "#DNF: count satisfying assignments; #P-complete even for monotone 2-DNF", VAL79, note="per-problem #P-completeness (Valiant 1979) [F-1]. NOTE: an FPRAS exists (Karp-Luby 1983, "+KL83+") but the `approximation` charge concerns the OPTIMIZATION version, not approximate counting"),
  na("approximation", "a counting problem, not an NP-optimization problem; approximate counting (FPRAS) is a separate question (cf. permanent)"),
  na("parameterized", "not a standard parameterized decision problem"),
  na("parallelization", "the decision (DNF-SAT) is trivial, not P-complete; within-P hardness charge n.a."),
  na("proof_size", "not a propositional refutation problem"),
  na("average_case", "not a random-ensemble hardness object (canonical)"),
  na("landscape", "not a random-ensemble solution-geometry object")]))

# ---- 10. bilevel-knapsack (beyond-NP decision filler) ----
ROWS.append(entry("bilevel-knapsack", "Bilevel Knapsack", "optimization",
  "a two-level (leader/follower) 0/1 knapsack with binary-encoded weights and profits; decision: can the leader guarantee objective >= t against the follower's optimal response?", [
  cell("decision", "PH-complete", "bilevel knapsack decision: Sigma_2^p-complete", CCLW14, perspective="Sigma_2^p", note="all three natural variants are Sigma_2^p-complete (Caprara-Carvalho-Lodi-Woeginger 2014). The bilevel (quantifier-alternation) lift makes it distinct from knapsack (S2)"),
  na("counting", "not a natural solution-counting problem"),
  op("approximation", "one variant admits a PTAS, two cannot be approximated within any constant (P!=NP) (Caprara et al. 2014); the objective/variant pinning is not settled here -> open pending R1 objective pin"),
  na("parameterized", "no standard W-hierarchy parameterization curated"),
  na("parallelization", "Sigma_2^p-complete => not in P unless PH collapses; within-P charge n.a."),
  na("proof_size", "not a propositional refutation problem"),
  na("average_case", "not a random-ensemble hardness object curated"),
  na("landscape", "not a random-ensemble solution-geometry object")]))

def main():
    with open(OUT, "w") as f:
        for r in ROWS:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"wrote {len(ROWS)} pilot rows -> {OUT}")
    # quick self-report: citable (real-value) charges per row
    for r in ROWS:
        real = [c["charge"] for c in r["charges"] if c["status"] != "structural"]
        print(f"  {r['problem_id']:34} citable={len(real)}: {','.join(real)}")

if __name__ == "__main__":
    main()
