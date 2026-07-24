#!/usr/bin/env python3
"""Quarry K2 — serialize the curated candidate table -> quarry-candidates.jsonl + .csv.

The intellectual content (aliasing, source membership, per-charge complexity hints, S2
distinctness vs the 118) is hand-curated from the six sources per the K1 verdicts and is
documented in quarry-K2-intersection.md. Value hints are PROVISIONAL screening pointers,
NOT R20-verified (that is K3). Sources: rn=reductions.network, ck=Crescenzi-Kann,
ghr=Greenlaw-Hoover-Ruzzo, df=Downey-Fellows, dh=de Haan-Szeider, su=Schaefer-Umans.
"""
import json, csv, os

# portable: this script lives at eightfold/dev/build_quarry.py; data lands beside the frozen atlas.
OUT_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                        "..", "eightfold", "results", "atlas"))
SRC_KEYS = ["rn", "ck", "ghr", "df", "dh", "su"]
# thin columns (compendium-addressable) from the K2 atlas survey (2026-07-23):
#   counting 43.0%, parallelization 45.9%, beyond-NP decision (7 rows), parameterized W[2]+ (4 rows)
THIN_DECISION_VALUES = {"PH-complete", "PSPACE-complete", "beyond-PSPACE", "coNP-complete"}

def C(charge, value, src, note=""):
    return {"charge": charge, "value_hint": value, "source": src, "note": note}

# candidate = (id, name, family, aliases, sources, [charge hints], distinct_note, tier, staleness, gap_hint, extra_note)
CANDS = [
 # ---------- TIER A: multi-charge, fills a thin column ----------
 ("chromatic-number", "Chromatic Number (Vertex Coloring, optimization)", "graph",
  ["Vertex Coloring","Graph Coloring","Minimum Colors","chi(G)"], ["rn","ck","df"],
  [C("decision","NPC","rn/Karp72"),
   C("counting","#P-complete","rn-parsimonious/JaegerVertiganWelsh90","chromatic polynomial evaluation"),
   C("approximation","inapprox","ck/Zuckerman07","n^{1-eps}; CURRENT (post-2000)"),
   C("parameterized","para-NP-hard","df","by #colors; FPT by treewidth (perspective-split)")],
  "distinct: k=3 restriction (graph-3-coloring) and edge-coloring stay separate (S2)", "A", False, None,
  "flagship counting-column filler with a modern tight inapprox"),

 ("subgraph-isomorphism", "Subgraph Isomorphism (non-induced)", "graph",
  ["Subgraph Matching","Pattern Matching (subgraph)"], ["rn","df"],
  [C("decision","NPC","rn/Cook71-via-clique"),
   C("parameterized","W[1]","df","by pattern size k; canonical"),
   C("counting","#W[1]-hard / #P-complete","rn","#subgraph-isomorphism")],
  "distinct from induced-subgraph-isomorphism (different YES-set) and graph-isomorphism (S2)", "A", False, None,
  "fills W[1] and counting; canonical parameterized anchor"),

 ("metric-dimension", "Metric Dimension", "graph",
  ["Resolving Set","Locating Set"], ["rn","df"],
  [C("decision","NPC","rn/GareyJohnson-GT61"),
   C("parameterized","W[2]","df/HartungNichterlein13","by solution size; W[2]-complete"),
   C("approximation","log-APX","ck","Theta(log n)")],
  "distinct new graph problem", "A", False, None,
  "canonical W[2]-complete; fills the sparse W[2]+ end (4 rows)"),

 ("bandwidth", "Graph Bandwidth", "graph",
  ["Bandwidth Minimization","Matrix Bandwidth"], ["rn","ck","df"],
  [C("decision","NPC","rn/Papadimitriou76"),
   C("parameterized","W-hard/XP","df","long-standing; no FPT known, hard for W[t]"),
   C("approximation","poly-log / inapprox-const","ck","O(log^{2.5} n); no constant-factor")],
  "distinct new graph problem", "A", True, None,
  "hard-to-parameterize canonical; staleness check on approx"),

 ("multicut", "Minimum Multicut (with terminal pairs)", "graph",
  ["Edge Multicut","Multi-commodity cut"], ["rn","df"],
  [C("decision","NPC","rn/DahlhausJPSY94"),
   C("parameterized","FPT","df/MarxRazgon14","by cutset size; landmark FPT result"),
   C("approximation","log-APX","ck","O(log k); APX-hard")],
  "distinct from multiway-cut (terminal pairs vs terminal set) (S2)", "A", False, None,
  "landmark FPT; multi-charge"),

 ("independent-dominating-set", "Independent Dominating Set (Minimum Maximal Independent Set)", "graph",
  ["Minimum Maximal Independent Set","Independent Domination"], ["rn","ck","df"],
  [C("decision","NPC","rn/GareyJohnson"),
   C("approximation","inapprox","ck/Halldorsson93","n^{1-eps}; hardest to approximate"),
   C("parameterized","W[2]","df","by solution size")],
  "distinct from dominating-set (adds independence) and independent-set (S2)", "A", False, None,
  "tight inapprox + W[2]"),

 ("list-coloring", "List Coloring", "graph",
  ["List Chromatic","Choosability (decision)"], ["rn","df"],
  [C("decision","NPC","rn"),
   C("parameterized","W[1]","df/FellowsEtAl11","by treewidth; canonical W[1]-by-treewidth"),
   C("approximation","inapprox","ck","inherits chromatic hardness")],
  "distinct from chromatic-number (per-vertex lists) (S2)", "A", False, None,
  "W[1]-hard-by-treewidth witness"),

 # ---------- TIER B: beyond-NP decision / higher-PH (thin decision + parameterized) ----------
 ("abstract-argumentation", "Credulous Acceptance in Abstract Argumentation (preferred semantics)", "logic-proof",
  ["Argumentation Acceptance","Dung framework acceptance","Credulous reasoning"], ["dh","su"],
  [C("decision","PH-complete","su/DimopoulosTorres96","Sigma_2^p-complete under preferred/semi-stable; perspective Sigma_2^p"),
   C("parameterized","FPT","dh/DvorakSzeiderWoltran12","by treewidth")],
  "distinct new problem", "B", False, "decision=PH-complete x parameterized",
  "fills beyond-NP decision AND parameterized; de Haan compendium core"),

 ("judgment-aggregation", "Judgment Aggregation (winner determination)", "logic-proof",
  ["Judgment aggregation consistency"], ["dh"],
  [C("decision","PH-complete","dh/EndrissEtAl","Theta_2^p / Sigma_2^p depending on rule; perspective noted"),
   C("parameterized","W[1]/FPT","dh","by agenda / treewidth")],
  "distinct new problem", "B", False, None,
  "beyond-NP decision + parameterized (de Haan)"),

 ("competitive-facility-location", "Competitive Facility Location (2-player)", "optimization",
  ["Voronoi game","Stackelberg facility location"], ["su"],
  [C("decision","PH-complete","su/Schaefer-Umans","Sigma_2^p-complete; perspective Sigma_2^p")],
  "distinct new problem", "B", False, None,
  "clean beyond-NP decision filler (Schaefer-Umans)"),

 ("generalized-geography", "Generalized Geography", "logic-proof",
  ["GEOGRAPHY","Vertex Geography","Edge Geography"], ["su"],
  [C("decision","PSPACE-complete","su/Schaefer78","perspective PSPACE")],
  "distinct from TQBF (different object, S2)", "B", False, None,
  "canonical PSPACE game; fills sparse PSPACE (2 rows)"),

 ("min-equivalent-expression", "Minimum Equivalent Expression (general formulas)", "logic-proof",
  ["MEE","Formula minimization"], ["su"],
  [C("decision","PH-complete","su/Umans01","Sigma_2^p-complete; perspective Sigma_2^p")],
  "REVISIT S2: superproblem of dnf-minimization (DNF restriction) — likely distinct (different formula class)", "B", False, None,
  "borderline vs dnf-minimization; owner S2 ruling needed"),

 # ---------- TIER C: parallelization-led (P-complete, thin column) ----------
 ("lex-first-maximal-independent-set", "Lexicographically-First Maximal Independent Set", "graph",
  ["LFMIS","Lex-first MIS"], ["ghr"],
  [C("decision","P","ghr/Cook85","greedily computable"),
   C("parallelization","P-complete","ghr/Cook85","canonical P-complete"),
   C("counting","FP","ghr","the lex-first MIS is unique -> count is 1")],
  "distinct from independent-set (lex-first selection object) (S2)", "C", False, "counting=FP x parallelization=P-complete",
  "parallelization anchor + candidate gap-cell occupant"),

 ("context-free-membership", "Context-Free Grammar Membership (CFL recognition)", "logic-proof",
  ["CFL recognition","CYK membership","CFG membership"], ["ghr"],
  [C("decision","P","ghr/CYK","O(n^3) recognition"),
   C("parallelization","P-complete","ghr/JonesLaaser76","canonical P-complete")],
  "distinct new problem", "C", False, None,
  "parallelization filler"),

 ("unification", "First-Order Term Unification", "logic-proof",
  ["Term unification","Robinson unification"], ["ghr"],
  [C("decision","P","ghr","linear-time unification"),
   C("parallelization","P-complete","ghr/DworkKanellakisMitchell84","canonical P-complete")],
  "distinct new problem", "C", False, None,
  "parallelization filler"),

 ("dfs-lexicographic-ordering", "Lexicographic Depth-First Search Ordering", "graph",
  ["Ordered DFS","Lex-DFS"], ["ghr"],
  [C("decision","P","ghr","computable in P"),
   C("parallelization","P-complete","ghr/Reif85","canonical P-complete")],
  "distinct new problem", "C", False, None,
  "parallelization filler"),

 # ---------- TIER D: counting-primary / decoupling witnesses (thin counting) ----------
 ("sharp-dnf", "#DNF (count satisfying assignments of a DNF)", "logic-proof",
  ["#DNF-SAT","DNF counting","#monotone-2-DNF"], ["rn"],
  [C("decision","P","rn","DNF satisfiability trivial"),
   C("counting","#P-complete","rn-parsimonious/Valiant79","hard even for monotone 2-DNF")],
  "distinct new problem (counting object; decision trivial)", "D", False, "decision=P x counting=#P-complete",
  "DECOUPLING WITNESS (decision easy, counting hard) + counting-column filler"),

 ("sharp-monotone-2sat", "#Monotone-2-SAT (count satisfying assignments)", "sat-csp",
  ["#2-monotone-CNF","monotone 2-SAT counting"], ["rn"],
  [C("decision","P","rn","monotone-2-SAT trivially satisfiable"),
   C("counting","#P-complete","rn-parsimonious/Valiant79")],
  "REVISIT S2: possible merge with sharp-dnf via complementation/re-encoding — owner ruling", "D", False, "decision=P x counting=#P-complete",
  "decoupling witness; check S2 vs sharp-dnf"),

 # ---------- TIER E: approximation-primary (well-covered column; lower priority) ----------
 ("min-linear-arrangement", "Minimum Linear Arrangement (Optimal Linear Arrangement)", "graph",
  ["MinLA","OLA","Optimal Linear Arrangement"], ["rn","ck"],
  [C("decision","NPC","rn/GareyJohnsonStockmeyer76"),
   C("approximation","poly-log-APX","ck/RaoRicha05","O(sqrt(log n) log log n)")],
  "distinct new problem", "E", True, None,
  "Crescenzi-Kann approximation problem; staleness check"),

 ("set-splitting", "Set Splitting (Hypergraph 2-Coloring / Max Set Splitting)", "sat-csp",
  ["Hypergraph 2-Coloring","Max-Set-Splitting","Not-All-Equal set system"], ["rn","ck"],
  [C("decision","NPC","rn/Lovasz73"),
   C("approximation","APX-complete","ck/Andersson-Engebretsen")],
  "distinct from nae-sat (set systems vs CNF) (S2 — different constraint language)", "E", True, None,
  "approx-primary; staleness"),

 ("feedback-arc-set", "Minimum Feedback Arc Set (general directed)", "graph",
  ["FAS","Minimum FAS","Maximum Acyclic Subgraph (complement)"], ["rn","ck","df"],
  [C("decision","NPC","rn/Karp72"),
   C("approximation","APX-hard","ck/GuruswamiEtAl11","O(log n log log n) upper; no PTAS under UGC — CURRENT"),
   C("parameterized","FPT","df/ChenLiuLuOSullivan08","O*(4^k)")],
  "distinct from feedback-arc-set-tournament (restriction, S2) and directed-feedback-vertex-set (arcs vs vertices, S2); NOTE Maximum Acyclic Subgraph merges by complementation (S2)", "E", True, None,
  "multi-charge but core columns already well-covered; S2 complementation note"),

 ("closest-string", "Closest String", "string",
  ["Center String","Hamming Center"], ["rn","ck","df"],
  [C("decision","NPC","rn/FrancesLitman97"),
   C("approximation","PTAS","ck/LiMaWang02"),
   C("parameterized","FPT","df/Gramm-Niedermeier-Rossmanith","by #strings or distance d")],
  "distinct new problem (string family, only 3 rows)", "E", False, None,
  "multi-charge; grows the thin string family"),

 ("betweenness", "Betweenness (Total Order)", "logic-proof",
  ["Total Ordering","Betweenness constraint"], ["rn"],
  [C("decision","NPC","rn/Opatrny79")],
  "distinct new problem", "F", False, None,
  "single-charge; low priority"),

 # ---------- batch 2: broaden the pool (clears the >=30 multi-charge bar) ----------
 ("max-e3-sat", "MAX-E3-SAT (maximize satisfied exact-3-clauses)", "sat-csp",
  ["MAX-3SAT","Max exact-3-SAT"], ["rn","ck"],
  [C("decision","NPC","rn/Cook71"),
   C("approximation","APX-complete","ck/Hastad01","7/8 tight inapprox; CURRENT (post-2000)"),
   C("counting","#P-complete","rn-parsimonious/Valiant79")],
  "distinct constraint language from sat / nae-sat / one-in-three-sat (S2)", "A", False, None,
  "tight modern inapprox + counting filler"),

 ("max-2sat", "MAX-2-SAT", "sat-csp",
  ["Maximum 2-Satisfiability"], ["rn","ck"],
  [C("decision","NPC","rn/GareyJohnsonStockmeyer76","NPC though 2-SAT decision is in P"),
   C("approximation","APX-complete","ck/AustrinUGC","~0.943 tight under UGC"),
   C("counting","#P-complete","rn-parsimonious/Valiant79","#2-SAT")],
  "distinct from sat-2 (max vs decision) and max-2lin (S2)", "A", False, None,
  "decoupling-flavored (2-SAT P, MAX-2-SAT NPC) + counting filler"),

 ("target-set-selection", "Target Set Selection", "graph",
  ["Influence threshold spread"], ["rn","df"],
  [C("decision","NPC","rn/Chen09"),
   C("parameterized","para-NP-hard","df/BenZwiHermelinLokshtanovNewman11","hard by treewidth"),
   C("approximation","inapprox","ck/Chen09","2^{log^{1-eps} n}")],
  "distinct new problem", "A", False, None,
  "hard everywhere; multi-charge"),

 ("maximum-induced-matching", "Maximum Induced Matching", "graph",
  ["Strong Matching","Dissociation matching"], ["rn","df"],
  [C("decision","NPC","rn/StockmeyerVazirani82"),
   C("parameterized","W[1]","df/MoserSikdar09","by solution size"),
   C("approximation","poly-APX","ck","APX-hard in bounded degree")],
  "distinct from matching (induced constraint) (S2)", "A", False, None,
  "W[1] + approx"),

 ("closest-substring", "Closest Substring", "string",
  ["Common Substring center"], ["rn","ck","df"],
  [C("decision","NPC","rn/FellowsGrammNiedermeier06"),
   C("parameterized","W[1]","df","by #strings and by length (double W[1]-hardness)"),
   C("approximation","PTAS","ck/Marx08")],
  "distinct from closest-string (substring vs whole string) (S2)", "A", False, None,
  "multi-charge; grows thin string family"),

 ("equitable-coloring", "Equitable Coloring", "graph",
  ["Balanced Coloring"], ["rn","df"],
  [C("decision","NPC","rn/Meyer73"),
   C("parameterized","W[1]","df/FellowsEtAl11","by treewidth + #colors")],
  "distinct from chromatic-number (balance constraint) (S2)", "A", False, None,
  "W[1]-by-treewidth witness"),

 ("capacitated-dominating-set", "Capacitated Dominating Set", "graph",
  ["Capacitated Domination"], ["rn","df"],
  [C("decision","NPC","rn"),
   C("parameterized","W[1]","df/DomLokshtanovSaurabhVillanger08","by solution size")],
  "distinct from dominating-set (capacities) and capacitated-vertex-cover (S2)", "A", False, None,
  "W[1] parameterized"),

 ("sparsest-cut", "Sparsest Cut (non-uniform)", "graph",
  ["Uniform Sparsest Cut","Conductance"], ["rn","ck"],
  [C("decision","NPC","rn/MatulaShahriari"),
   C("approximation","inapprox","ck/AroraRaoVazirani09","O(sqrt(log n)); no constant under UGC — CURRENT")],
  "distinct from min-bisection (balance) (S2)", "A", True, None,
  "approx-primary; currency-current"),

 ("facility-location", "Uncapacitated Facility Location (metric)", "optimization",
  ["Metric UFL","Warehouse location"], ["rn","ck"],
  [C("decision","NPC","rn/Cornuejols"),
   C("approximation","APX-complete","ck/Li13","1.488-approx; 1.463 APX-hard (Guha-Khuller)")],
  "distinct from k-median (opening costs vs cardinality) (S2)", "E", False, None,
  "canonical CK approx problem"),

 # counting-primary decoupling witnesses (thin counting) + candidate gap-cell occupants
 ("sharp-linear-extensions", "#Linear Extensions of a Poset", "logic-proof",
  ["Counting linear extensions","#LE"], ["rn"],
  [C("decision","P","rn","a linear extension always exists"),
   C("counting","#P-complete","rn-parsimonious/BrightwellWinkler91")],
  "distinct new problem (counting object)", "D", False, "decision=P x counting=#P-complete",
  "decoupling witness + counting filler"),

 ("sharp-eulerian-circuits", "#Eulerian Circuits", "graph",
  ["Counting Euler tours","#Euler"], ["rn"],
  [C("decision","P","rn/Euler","existence by degree parity"),
   C("counting","#P-complete","rn-parsimonious/BrightwellWinkler05")],
  "distinct new problem", "D", False, "decision=P x counting=#P-complete",
  "decoupling witness + counting filler"),

 # parallelization-led (P-complete, thin)
 ("path-system-accessibility", "Path System Accessibility", "logic-proof",
  ["Cook's path systems","Solvable Path System"], ["ghr"],
  [C("decision","P","ghr","in P"),
   C("parallelization","P-complete","ghr/Cook74","the first P-complete problem")],
  "distinct new problem", "C", False, None,
  "historic P-complete; parallelization filler"),

 ("and-or-graph-accessibility", "AND/OR Graph Accessibility (Alternating Graph Accessibility)", "graph",
  ["AGAP","Alternating reachability"], ["ghr"],
  [C("decision","P","ghr","in P"),
   C("parallelization","P-complete","ghr/Immerman","canonical P-complete")],
  "distinct from reachability-stcon (alternating vs plain, S2)", "C", False, None,
  "parallelization filler"),

 # beyond-NP decision filler (single, but grows the sparse column)
 ("bilevel-knapsack", "Bilevel Knapsack", "optimization",
  ["Stackelberg Knapsack","Min-max Knapsack"], ["su"],
  [C("decision","PH-complete","su/CapraraEtAl14","Sigma_2^p-complete; perspective Sigma_2^p")],
  "distinct new problem", "B", False, None,
  "clean beyond-NP decision filler"),
]

def build():
    rows = []
    for (cid, name, fam, aliases, srcs, charges, distinct, tier, stale, gap, note) in CANDS:
        source_flags = {k: (k in srcs) for k in SRC_KEYS}
        precited = {c["charge"]: {"value_hint": c["value_hint"], "source": c["source"], "note": c["note"]} for c in charges}
        n_charges = len(charges)
        # thin columns per spec §3: "Parallelization, counting, and beyond-NP decision values
        # outrank another NPC x APX-complete graph problem." (W-hardness is a tie-break note, not a
        # multiplier — kept in `notes`, not scored.)
        fills_thin = sorted({
            *("counting" for c in charges if c["charge"]=="counting"),
            *("parallelization" for c in charges if c["charge"]=="parallelization"),
            *("decision(beyond-NP)" for c in charges if c["charge"]=="decision" and c["value_hint"] in THIN_DECISION_VALUES),
        })
        thin = bool(fills_thin) or (gap is not None)
        # priority per spec §3: (#R20-citable charges) x (fills thin column or empty occupancy cell)
        score = n_charges * (2 if thin else 1)
        if gap:  # a candidate inhabiting an empty occupancy cell outranks everything
            score += 100
        screen = "PASS-multi" if n_charges >= 2 else "PASS-single"
        if "REVISIT" in distinct:
            screen = "REVISIT-S2"
        rows.append({
            "candidate_id": cid, "name": name, "family": fam, "aliases": aliases,
            "sources": source_flags, "n_sources": sum(source_flags.values()),
            "precited_charges": precited, "n_citable_charges": n_charges,
            "fills_thin_columns": fills_thin, "gap_cell_hint": gap,
            "distinct_vs_118": distinct, "screen": screen,
            "staleness_check_required": stale, "tier": tier,
            "priority_score": score, "notes": note,
        })
    rows.sort(key=lambda r: (-r["priority_score"], r["tier"], r["candidate_id"]))
    return rows

def main():
    rows = build()
    jl = os.path.join(OUT_DIR, "quarry-candidates.jsonl")
    with open(jl, "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    # flat CSV export (repo convention: hardmap atlas --format csv analog)
    cols = ["candidate_id","name","family","tier","priority_score","screen","n_sources","n_citable_charges",
            "fills_thin_columns","gap_cell_hint","staleness_check_required",
            "rn","ck","ghr","df","dh","su","precited_charges","distinct_vs_118","notes"]
    cv = os.path.join(OUT_DIR, "quarry-candidates.csv")
    with open(cv, "w", newline="") as f:
        w = csv.writer(f); w.writerow(cols)
        for r in rows:
            pc = "; ".join(f"{k}={v['value_hint']}" for k,v in r["precited_charges"].items())
            w.writerow([r["candidate_id"], r["name"], r["family"], r["tier"], r["priority_score"], r["screen"],
                        r["n_sources"], r["n_citable_charges"], "|".join(r["fills_thin_columns"]),
                        r["gap_cell_hint"] or "", r["staleness_check_required"],
                        r["sources"]["rn"], r["sources"]["ck"], r["sources"]["ghr"], r["sources"]["df"],
                        r["sources"]["dh"], r["sources"]["su"], pc, r["distinct_vs_118"], r["notes"]])
    # summary
    multi = [r for r in rows if r["n_citable_charges"] >= 2 and r["screen"] != "REVISIT-S2"]
    print(f"candidates: {len(rows)}  | multi-charge PASS: {len(multi)}  | REVISIT-S2: {sum(1 for r in rows if r['screen']=='REVISIT-S2')}")
    print(f"kill-criterion-1 bar (>=~30 multi-charge): {'CLEAR' if len(multi) >= 30 else 'CHECK — pool ' + str(len(multi))}")
    print("\nby tier:", {t: sum(1 for r in rows if r['tier']==t) for t in 'ABCDEF'})
    print("gap-cell candidates:", [r["candidate_id"] for r in rows if r["gap_cell_hint"]])
    print("\ntop 12 by priority:")
    for r in rows[:12]:
        print(f"  {r['priority_score']:4d}  {r['tier']}  {r['candidate_id']:34} charges={r['n_citable_charges']} thin={r['fills_thin_columns']}")
    print(f"\nwrote:\n  {jl}\n  {cv}")

if __name__ == "__main__":
    main()
