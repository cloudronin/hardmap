"""Atlas builder — the authoritative source for results/atlas/atlas.jsonl.

The atlas is curated HERE (Python is far less error-prone than hand-editing nested JSONL) and generated with
`python dev/build_atlas.py`; atlas.jsonl is the loadable generated artifact (both committed). Every real cell
is `claimed` with a stable citation (books / primary papers — no url, so no R10 snapshot burden); `confirmed`
promotion is the owner's job (R8). The Census C2 backbone is the single `measured` cell (R9). Values are
agent-drafted from standard references; correct-and-partial beats complete-and-unverified — genuinely
unknown-to-me cells are `open`, inapplicable ones `n.a.` per the R15 boundary (n.a. only when the charge's
object cannot be constructed).
"""
import json
import pathlib

# eightfold/dev/build_atlas.py -> parents[1] = the product dir (eightfold/); the JSONL is one level in.
ATLAS = pathlib.Path(__file__).resolve().parents[1] / "eightfold" / "results" / "atlas" / "atlas.jsonl"

REVIEWER = "Claude Code (agent draft; claimed — owner review/confirm pending)"
DATE = "2026-07-21"

# ── citation shorthands (stable anchors: books + primary papers, no url) ──────────────────────────────────
GJ = "Garey & Johnson, Computers and Intractability (1979)"
AB = "Arora & Barak, Computational Complexity: A Modern Approach (2009)"
AK = "Ausiello, Crescenzi, Gambosi, Kann, Marchetti-Spaccamela & Protasi, Complexity and Approximation (1999)"
DF99 = "Downey & Fellows, Parameterized Complexity (1999)"
CYG = "Cygan et al., Parameterized Algorithms (2015)"
GHR = "Greenlaw, Hoover & Ruzzo, Limits to Parallel Computation (1995)"
KARP = "Karp, Reducibility among combinatorial problems (1972)"
VAL_PERM = "Valiant, The complexity of computing the permanent, TCS 8 (1979) 189-201"
VAL_ENUM = "Valiant, The complexity of enumeration and reliability problems, SIAM J. Comput. 8 (1979) 410-421"
CREIG = "Creignou & Hermann, Complexity of generalized satisfiability counting problems, Inf. Comput. 125 (1996)"
HAKEN = "Haken, The intractability of resolution, TCS 39 (1985) 297-308"
URQ = "Urquhart, Hard examples for resolution, JACM 34 (1987) 209-219"
CS88 = "Chvatal & Szemeredi, Many hard examples for resolution, JACM 35 (1988) 759-768"
HAST99 = "Hastad, Clique is hard to approximate within n^(1-eps), Acta Math. 182 (1999) 105-142"
ZUCK = "Zuckerman, Linear degree extractors and inapproximability of Max Clique and Chromatic Number, Theory of Computing 3 (2007)"
DS05 = "Dinur & Safra, On the hardness of approximating minimum vertex cover, Ann. of Math. 162 (2005) 439-485"
DF95 = "Downey & Fellows, Fixed-parameter tractability and completeness II (W[1]), TCS 141 (1995)"
IK75 = "Ibarra & Kim, Fast approximation algorithms for the knapsack..., JACM 22 (1975) 463-468"
FEIGE = "Feige, A threshold of ln n for approximating set cover, JACM 45 (1998) 634-652"
DINUR_ST = "Dinur & Steurer, Analytical approach to parallel repetition, STOC 2014"
GW95 = "Goemans & Williamson, Improved approximation algorithms for max cut and satisfiability, JACM 42 (1995)"
PY91 = "Papadimitriou & Yannakakis, Optimization, approximation, and complexity classes, JCSS 43 (1991) 425-440"
KHACH = "Khachiyan, A polynomial algorithm in linear programming, Soviet Math. Dokl. 20 (1979)"
BABAI16 = "Babai, Graph isomorphism in quasipolynomial time, STOC 2016"
CSANKY = "Csanky, Fast parallel matrix inversion algorithms, SIAM J. Comput. 5 (1976) 618-623"
MVV = "Mulmuley, Vazirani & Vazirani, Matching is as easy as matrix inversion, Combinatorica 7 (1987)"
KUW = "Karp, Upfal & Wigderson, Constructing a perfect matching is in Random NC, Combinatorica 6 (1986)"
HAST01 = "Hastad, Some optimal inapproximability results, JACM 48 (2001) 798-859"
DUBOIS = "Dubois & Mandler, The 3-XORSAT threshold, FOCS 2002"
IKKM = "Ibrahimi, Kanoria, Kraning & Montanari, The set of solutions of random XORSAT formulae, Ann. Appl. Probab. 25 (2015)"
MMZ05 = "Mezard, Mora & Zecchina, Clustering of solutions in the random satisfiability problem, PRL 94 (2005)"
ACO08 = "Achlioptas & Coja-Oghlan, Algorithmic barriers from phase transitions, FOCS 2008"
DSS15 = "Ding, Sly & Sun, Proof of the satisfiability conjecture for large k, STOC 2015"
FRIED = "Friedgut, Sharp thresholds of graph properties, and the k-SAT problem, JAMS 12 (1999)"
GS14 = "Gamarnik & Sudan, Limits of local algorithms over sparse random graphs, ITCS 2014"
APT79 = "Aspvall, Plass & Tarjan, A linear-time algorithm for testing certain QBFs (2-SAT), IPL 8 (1979)"
CR92 = "Chvatal & Reed, Mick gets some (the odds are on his side) [random 2-SAT], FOCS 1992"
DG84 = "Dowling & Gallier, Linear-time algorithms for testing satisfiability of Horn formulae, J. Logic Prog. 1 (1984)"
BGH82 = "Borodin, von zur Gathen & Hopcroft, Fast parallel matrix and GCD computations, Inf. Control 52 (1982)"
EDM65 = "Edmonds, Paths, trees, and flowers, Canad. J. Math. 17 (1965) 449-467"
ST04 = "Spielman & Teng, Smoothed analysis: why the simplex algorithm usually takes polynomial time, JACM 51 (2004)"
BES80 = "Babai, Erdos & Selkow, Random graph isomorphism, SIAM J. Comput. 9 (1980)"
LUKS82 = "Luks, Isomorphism of graphs of bounded valence can be tested in polynomial time, JCSS 25 (1982)"
STOCK73 = "Stockmeyer & Meyer, Word problems requiring exponential time, STOC 1973 [PSPACE-completeness]"
BCJ15 = "Beyersdorff, Chew & Janota, Proof complexity of resolution-based QBF calculi, STACS 2015"
LINIAL = "Linial, Hard enumeration problems in geometry and combinatorics, SIAM J. Alg. Disc. Meth. 7 (1986)"
AN05 = "Achlioptas & Naor, The two possible values of the chromatic number of a random graph, STOC 2004/Ann. Math. 2005"
KMRTZ = "Krzakala, Montanari, Ricci-Tersenghi, Semerjian & Zdeborova, Gibbs states and the set of solutions of random CSPs, PNAS 104 (2007)"
PB83 = "Provan & Ball, The complexity of counting cuts and of computing the probability that a graph is connected, SIAM J. Comput. 12 (1983)"
MERTENS = "Mertens, Phase transition in the number partitioning problem, PRL 81 (1998)"
BCP01 = "Borgs, Chayes & Pittel, Phase transition and finite-size scaling for the integer partitioning problem, RSA 19 (2001)"
DMS17 = "Dembo, Montanari & Sen, Extremal cuts of sparse random graphs, Ann. Probab. 45 (2017)"
SG76 = "Sahni & Gonzalez, P-complete approximation problems [general TSP inapprox], JACM 23 (1976)"
BHH59 = "Beardwood, Halton & Hammersley, The shortest path through many points, Proc. Camb. Phil. Soc. 55 (1959)"
RSA78 = "Rivest, Shamir & Adleman, A method for obtaining digital signatures..., CACM 21 (1978) [factoring assumption]"
DYER03 = "Dyer, Approximate counting by dynamic programming [#knapsack FPRAS], STOC 2003"
# R11-R16 additions
LIPTON91 = "Lipton, New directions in testing, DIMACS Ser. Discrete Math. 2 (1991) [permanent random self-reducibility]"
KARP_SIPSER = "Karp & Sipser, Maximum matchings in sparse random graphs, FOCS 1981"
BEIER_VOCKING = "Beier & Vocking, Random knapsack in expected polynomial time, JCSS 69 (2004) 306-329"
WEIGT_HARTMANN = "Weigt & Hartmann, Number of guards needed by a museum: phase transition in vertex covering of random graphs, PRL 84 (2000) 6118"
ISTRATE = "Istrate, The phase transition in random Horn satisfiability, Random Struct. Alg. 20 (2002)"
PLANTED = "planted-clique conjecture; Alon, Krivelevich & Sudakov, Finding a large hidden clique in a random graph, RSA 13 (1998); Barak et al., SOS lower bounds (2019)"
KSTW = "Khanna, Sudan, Trevisan & Williamson, The approximability of constraint satisfaction problems, SICOMP 30 (2001) [MAX-CSP dichotomy]; Guruswami & Zhou tight UGC bounds for almost-sat Horn SAT"
DF_KSUM = "Downey & Fellows, Parameterized Complexity (1999) [k-subset-sum W[1]-hardness]"
GENT_WALSH = "Gent & Walsh, Beyond NP: the QSAT phase transition, AAAI 1999"
# A2 batch-1 citations
SCHAEFER = "Schaefer, The complexity of satisfiability problems, STOC 1978"
BAFNA = "Bafna, Berman & Fujito, A 2-approximation for undirected feedback vertex set, SIAM J. Discrete Math. 12 (1999)"
DREYFUS = "Dreyfus & Wagner, The Steiner problem in graphs, Networks 1 (1971) [FPT by #terminals]"
BYRKA = "Byrka, Grandoni, Rothvoss & Sanita, Steiner tree approximation via iterative randomized rounding, JACM 60 (2013)"
AYZ = "Alon, Yuster & Zwick, Color-coding, JACM 42 (1995) [longest-path FPT]"
LENSTRA = "H.W. Lenstra Jr., Integer programming with a fixed number of variables, Math. Oper. Res. 8 (1983)"
AKS = "Agrawal, Kayal & Saxena, PRIMES is in P, Ann. of Math. 160 (2004)"
AJTAI = "Ajtai, Generating hard instances of lattice problems, STOC 1996 [worst-case to average-case]"
MICC = "Micciancio, The shortest vector problem is NP-hard to approximate to within some constant, SIAM J. Comput. 30 (2001)"
GSS = "Goldschlager, Shaw & Staples, The maximum flow problem is log-space complete for P, TCS 21 (1982)"
BODL = "Bodlaender, A linear-time algorithm for finding tree-decompositions of small treewidth, SIAM J. Comput. 25 (1996)"
FHL = "Feige, Hajiaghayi & Lee, Improved approximation algorithms for minimum-weight vertex separators, SIAM J. Comput. 38 (2008) [treewidth approx]"
HOCH_SHM = "Hochbaum & Shmoys, Using dual approximation algorithms for scheduling, JACM 34 (1987) [makespan PTAS; k-center 2-approx]"
CHRIST = "Christofides, Worst-case analysis of a new heuristic for the TSP (1976) [metric 3/2]"
JVW = "Jaeger, Vertigan & Welsh, Computational complexity of the Jones and Tutte polynomials, Math. Proc. Camb. Phil. Soc. 108 (1990)"
KK82 = "Karmarkar & Karp, An efficient approximation scheme for one-dimensional bin-packing, FOCS 1982 [AFPTAS]"
KMR_GCD = "Kannan, Miller & Rudolph, Sublinear parallel algorithm for computing the GCD, SIAM J. Comput. 16 (1987)"
KIRCHHOFF = "Kirchhoff matrix-tree theorem: #spanning-trees is a determinant (FP)"
LADNER = "Ladner, The circuit value problem is log-space complete for P, SIGACT News 7 (1975)"
# batch-1 review (R18/R19/R20 + fills)
LY94 = "Lund & Yannakakis, On the hardness of approximating minimization problems, JACM 41 (1994) [FVS APX-hard]"
BERN_PLASSMANN = "Bern & Plassmann, The Steiner problem with edge lengths 1 and 2, IPL 32 (1989) [Steiner APX-hard]"
PY93 = "Papadimitriou & Yannakakis, The TSP with distances one and two, Math. Oper. Res. 18 (1993) [metric-TSP APX-hard]"
NWF78 = "Nemhauser, Wolsey & Fisher, An analysis of approximations for maximizing submodular set functions, Math. Prog. 14 (1978)"
BFF = "Bollobas, Fenner & Frieze, An algorithm for finding Hamilton paths and cycles in random graphs, Combinatorica 7 (1987)"
APW = "Austrin, Pitassi & Wu, Inapproximability of treewidth and related problems, JAIR 49 (2014) [SSE-conjectural]"
KMR97 = "Karger, Motwani & Ramkumar, On approximating the longest path in a graph, Algorithmica 18 (1997)"
ACP87 = "Arnborg, Corneil & Proskurowski, Complexity of finding embeddings in a k-tree, SIAM J. Alg. Disc. Meth. 8 (1987)"
AM06 = "Achlioptas & Moore, Random k-SAT: two moments suffice to cross a sharp threshold, SIAM J. Comput. 36 (2006) [NAE-SAT]"
# batch 2 citations
HOLYER = "Holyer, The NP-completeness of edge-coloring, SIAM J. Comput. 10 (1981)"
VIZING = "Vizing, On an estimate of the chromatic class of a p-graph (1964) [Delta+1 edge-coloring]"
DAHLHAUS = "Dahlhaus, Johnson, Papadimitriou, Seymour & Yannakakis, The complexity of multiterminal cuts, SIAM J. Comput. 23 (1994)"
CLLOR = "Chen, Liu, Lu, O'Sullivan & Razgon, A fixed-parameter algorithm for directed feedback vertex set, JACM 55 (2008)"
VEB81 = "van Emde Boas, Another NP-complete problem and the complexity of computing short vectors in a lattice (1981) [CVP NP-hard]"
DKRS = "Dinur, Kindler, Raz & Safra, Approximating CVP to within almost-polynomial factors is NP-hard, Combinatorica 23 (2003)"
MARX06 = "Marx, Parameterized graph separation problems, TCS 351 (2006) [multiway cut FPT]"
KHOT02 = "Khot, On the power of unique 2-prover 1-round games, STOC 2002 [UGC]"
# batch 3 citations
REGEV = "Regev, On lattices, learning with errors, random linear codes, and cryptography, JACM 56 (2009)"
KABANETS_CAI = "Kabanets & Cai, Circuit minimization problem, STOC 2000 [MCSP]"
HOPTAR = "Hopcroft & Tarjan, Efficient planarity testing, JACM 21 (1974)"
KASTELEYN = "Kasteleyn (1961) / FKT: perfect matchings of a PLANAR graph counted in poly time"
UMANS = "Umans, The minimum equivalent DNF problem is Sigma_2^p-complete, FOCS 1998"
PY86 = "Papadimitriou & Yannakakis, A note on the succinct representation of graphs, Inf. Control 71 (1986) [succinct => NEXP]"
REED_OCT = "Reed, Smith & Vetta, Finding odd cycle transversals, Oper. Res. Lett. 32 (2004) [FPT]"
GRAMM_CE = "Gramm, Guo, Huffner & Niedermeier, FPT algorithms for cluster editing, Theory Comput. Syst. 38 (2005)"
GJS76 = "Garey, Johnson & Stockmeyer, Some simplified NP-complete graph problems, TCS 1 (1976) [planar 3-coloring]"
AKR95 = "Agrawal, Klein & Ravi, When trees collide: 2-approximation for generalized Steiner problems, SIAM J. Comput. 24 (1995)"
VARDI82 = "Vardi, The complexity of relational query languages, STOC 1982 [FO model checking]"
# batch 4 citations
KENYON_MATHIEU = "Kenyon-Mathieu & Schudy, How to rank with few errors, STOC 2007 [feedback-arc / Kemeny PTAS]"
RS95 = "Robertson & Seymour, Graph minors XIII: the disjoint paths problem, JCTB 63 (1995) [FPT]"
# batch 5 citations
BAKER94 = "Baker, Approximation algorithms for NP-complete problems on planar graphs, JACM 41 (1994) [planar PTAS]"
JAIN01 = "Jain, A factor 2 approximation for the generalized Steiner network problem, Combinatorica 21 (2001)"
GALE_SHAPLEY = "Gale & Shapley, College admissions and the stability of marriage, Amer. Math. Monthly 69 (1962)"
IRVING_LEATHER = "Irving & Leather, The complexity of counting stable marriages, SIAM J. Comput. 15 (1986) [#P-complete]"
BI15 = "Backurs & Indyk, Edit distance cannot be computed in strongly subquadratic time unless SETH is false, STOC 2015"
GO95 = "Gajentaan & Overmars, On a class of O(n^2) problems in computational geometry, Comput. Geom. 5 (1995) [3SUM]"
VADHAN01 = "Vadhan, The complexity of counting in sparse, regular, and planar graphs, SIAM J. Comput. 31 (2001) [#IS/#VC/#matchings #P-complete even planar bipartite bounded-degree]"
# R24 landscape evidence-grade citations
GAMARNIK_ZADIK = "Gamarnik & Zadik, The landscape of the planted clique problem: dense subgraphs and the overlap gap property (2019)"
GAMARNIK_KIZILDAG = "Gamarnik & Kizildag, Algorithmic obstructions in the random number partitioning problem, Ann. Appl. Probab. 33 (2023)"
CGPR = "Chen, Gamarnik, Panchenko & Rahman, Suboptimality of local algorithms for a class of max-cut problems, Ann. Probab. 47 (2019) [spin-glass OGP]"
MRT_ACO = "rigorous clustering for random k-SAT holds at K>=8 (Mezard-Ricci-Tersenghi; Achlioptas-Coja-Oghlan); k=3 is cavity-method physics"

# ── the Census C2 banked experiment artifact (R9) ─────────────────────────────────────────────────────────
CENSUS_C2 = {
    "prereg": "proof-census/proofcensus/results/prereg/prereg_v1.json",
    "manifest": "proof-census/proofcensus/results/figures/c2_summary.json",
    "seeds": "c2.py S1/S2 seed banks; n=20 alpha-mini-sweep (3 instances/cell, K=80)",
    "code_commit": "uofa-lab@55c7df5 (proofcensus/c2.py, sweep.py, metrics.py)",
}


def cell(charge, value, task, cite=None, status="claimed", perspective=None, note=None, contested=None,
         experiment=None, transition_known=None, worst_to_average_self_reduction=None, primary_source=False):
    prov = {}
    if cite:
        prov["citation"] = cite
    if note:
        prov["note"] = note
    if experiment:
        prov["experiment"] = experiment
    if primary_source:                 # owner promotion (claimed -> confirmed): primary source read
        prov["primary_source"] = True
    d = {"charge": charge, "value": value, "canonical_task": task, "status": status,
         "provenance": prov, "perspective": perspective, "contested_note": contested}
    if transition_known is not None:                       # R17: average_case-only ensemble sub-field
        d["transition_known"] = transition_known
    if worst_to_average_self_reduction is not None:        # R18: average_case-only self-reduction sub-field
        d["worst_to_average_self_reduction"] = worst_to_average_self_reduction
    return d


def na(charge, why):
    return cell(charge, "n.a.", why, status="structural")


def op(charge, task, note=None, value="open", cite=None, transition_known=None):
    return cell(charge, value, task, cite=cite, status="structural", note=note, transition_known=transition_known)


def entry(pid, name, family, enc, cells, notes=None):
    return {"problem_id": pid, "problem_name": name, "problem_family": family, "canonical_encoding": enc,
            "charges": cells, "last_reviewed": DATE, "reviewer": REVIEWER, "notes": notes}


ROWS = []

# 1. SAT
ROWS.append(entry("sat", "Boolean Satisfiability (CNF-SAT)", "sat-csp",
    "CNF over n vars; clauses as literal-lists; unbounded width", [
    cell("decision", "NPC", "SAT decision", AB, note="Cook-Levin"),
    cell("counting", "#P-complete", "#SAT: count satisfying assignments", VAL_ENUM),
    cell("approximation", "APX-complete", "MAX-SAT (max satisfied clauses)", AK),
    cell("parameterized", "FPT", "SAT parameterized by treewidth of the primal graph", CYG, perspective="treewidth"),
    na("parallelization", "NPC => not in P unless P=NP; within-P charge n.a. (E2)"),
    cell("proof_size", "exp", "hardest unsat CNF families (PHP/Tseitin) refuted in Resolution", HAKEN, perspective="Resolution", note="also Urquhart 1987"),
    op("average_case", "random CNF: ensemble depends on clause width; no single canonical threshold for unbounded-width SAT"),
    op("landscape", "solution-space geometry is ensemble-dependent for general SAT"),
    ]))

# 2. 3-SAT
ROWS.append(entry("sat-3", "3-SAT", "sat-csp",
    "CNF with exactly-3-literal clauses; random ensemble at clause density alpha", [
    cell("decision", "NPC", "3-SAT decision", GJ, note="GJ [LO1]"),
    cell("counting", "#P-complete", "#3-SAT", CREIG),
    cell("approximation", "APX-complete", "MAX-3SAT; 7/8 tight", HAST01, note="Hastad optimal inapprox; APX-complete"),
    cell("parameterized", "FPT", "3-SAT parameterized by treewidth", CYG, perspective="treewidth"),
    na("parallelization", "NPC => within-P charge n.a. (E2)"),
    cell("proof_size", "exp", "random unsat 3-SAT Resolution refutation size", CS88, perspective="Resolution"),
    cell("average_case", "hard-on-average-conjectured", "random 3-SAT near threshold: conjectured hard in the clustered regime", ACO08, note="threshold ~4.267 (Friedgut; Ding-Sly-Sun 2015)", transition_known=True),
    cell("landscape", "clustering-physics", "random 3-SAT solution space: clustering/condensation near threshold (cavity/replica prediction)", MMZ05, note="R24: physics-grade at k=3 (Mezard-Mora-Zecchina); rigorous clustering starts at K>=8 (Mezard-Ricci-Tersenghi; Achlioptas-Coja-Oghlan) -- demoted from clustering-OGP-known at owner promotion"),
    ]))

# 3. 2-SAT
ROWS.append(entry("sat-2", "2-SAT", "sat-csp",
    "CNF with exactly-2-literal clauses; implication-graph view", [
    cell("decision", "P", "2-SAT decision (NL-complete, in P)", APT79),
    cell("counting", "#P-complete", "#2-SAT", VAL_ENUM),
    cell("approximation", "APX-complete", "MAX-2SAT", AK, note="GW 0.940; PY MAX-SNP-complete"),
    na("parameterized", "decision in P; no standard W-hierarchy parameterization for 2-SAT itself"),
    cell("parallelization", "NC", "2-SAT is NL-complete, and NL subset of NC^2", AB, note="NL-completeness Papadimitriou"),
    cell("proof_size", "poly", "2-UNSAT: poly Resolution refutation via the implication graph", APT79, perspective="Resolution", note="folklore; implication-graph certificate"),
    cell("average_case", "easy-on-average", "random 2-SAT: in P (linear-time), easy on average", APT79, note="sharp threshold at density 1 (Chvatal-Reed 1992)", transition_known=True),
    op("landscape", "random 2-SAT solution-space geometry less studied than 3-SAT/XORSAT"),
    ]))

# 4. XOR-SAT  (star decoupling witness)
ROWS.append(entry("xor-sat", "XOR-SAT (linear equations over GF(2))", "sat-csp",
    "system of GF(2) linear equations (k-XOR clauses); random k-XORSAT ensemble", [
    cell("decision", "P", "XOR-feasibility via Gaussian elimination over GF(2)", AB),
    cell("counting", "FP", "#solutions = 2^(n-rank); Gaussian elimination (affine => FP)", CREIG),
    cell("approximation", "inapprox", "MAX-3-LIN over GF(2): no (1/2+eps)-approx unless P=NP (a DIFFERENT object than XOR-feasibility, R1)", HAST01),
    na("parameterized", "decision in P"),
    cell("parallelization", "NC", "linear algebra over GF(2) in NC^2", BGH82),
    cell("proof_size", "exp", "Tseitin/XOR formulas on expanders: Resolution size 2^Omega(n)", URQ, perspective="Resolution"),
    cell("average_case", "easy-on-average", "random k-XORSAT: in P (Gaussian elimination), easy on average", DUBOIS, note="sharp SAT/clustering threshold (Dubois-Mandler 2002)", transition_known=True),
    cell("landscape", "clustering-proven", "random k-XORSAT solution space: frozen 1RSB clusters (rigorous)", IKKM),
    ], notes="Maximal decoupling: decision/counting trivial (P/FP) yet MAX-3LIN inapprox, Tseitin proof exp, solutions frozen. The R1 different-object witness."))

# 5. Horn-SAT
ROWS.append(entry("horn-sat", "Horn-SAT", "sat-csp",
    "CNF with <=1 positive literal per clause (Horn); unit-propagation view", [
    cell("decision", "P", "Horn satisfiability; linear-time unit propagation", DG84),
    cell("counting", "#P-complete", "#Horn-SAT (Horn is not affine => #P-complete)", CREIG),
    cell("approximation", "APX-complete", "MAX-Horn-SAT (maximize satisfied Horn clauses)", KSTW, note="APX-complete via MAX-CSP dichotomy; UGC-tight"),
    na("parameterized", "decision in P"),
    cell("parallelization", "P-complete", "Horn-SAT is P-complete", GHR),
    cell("proof_size", "poly", "Horn-UNSAT: poly unit-resolution refutation", DG84, perspective="Resolution", note="unit resolution complete for Horn"),
    cell("average_case", "easy-on-average", "random Horn-SAT: in P (linear-time), easy on average", ISTRATE, note="satisfiability phase transition (Istrate 2002)", transition_known=True),
    op("landscape", "random Horn solution-space geometry: ensemble exists (Istrate) but OGP not established (R15 open, not n.a.)"),
    ], notes="Decision-easy/counting-hard like 2-SAT, but P-complete parallel (vs 2-SAT/XORSAT NC)."))

# 6. Vertex Cover
ROWS.append(entry("vertex-cover", "Vertex Cover (decision)", "graph",
    "simple undirected graph, adjacency-list (sparse); size = (n vertices, m edges)", [
    cell("decision", "NPC", "VC decision: cover of size <= k?", GJ, note="GJ [GT1]; Karp 1972"),
    cell("counting", "#P-complete", "#vertex covers", VAL_ENUM, note="Provan-Ball 1983"),
    cell("approximation", "APX-complete", "MIN-VC: 2-approx, no PTAS unless P=NP (1.36 hardness)", DS05, note="APX-complete; Ausiello et al."),
    cell("parameterized", "FPT", "VC parameterized by solution size k", DF99, perspective="solution size k"),
    na("parallelization", "NPC => within-P charge n.a. (E2)"),
    na("proof_size", "not a propositional refutation problem"),
    cell("average_case", "hard-on-average-conjectured", "min-VC on random graphs: typical-case search-complexity peak near the transition", WEIGT_HARTMANN, transition_known=True),
    cell("landscape", "clustering-proven", "max-independent-set (VC complement) on sparse G(n,c/n): OGP (rigorous, via IS complementation)", GS14),
    ]))

# 7. Clique
ROWS.append(entry("clique", "Clique (decision)", "graph",
    "simple undirected graph, adjacency-list (sparse)", [
    cell("decision", "NPC", "CLIQUE decision: clique of size >= k?", KARP),
    cell("counting", "#P-complete", "#cliques", VAL_ENUM),
    cell("approximation", "inapprox", "MAX-CLIQUE: n^(1-eps) inapprox unless P=NP", HAST99, note="Zuckerman 2007 derandomized"),
    cell("parameterized", "W[1]", "k-CLIQUE: W[1]-complete", DF95, perspective="solution size k"),
    na("parallelization", "NPC => within-P charge n.a. (E2)"),
    na("proof_size", "not a propositional refutation problem"),
    cell("average_case", "hard-on-average-conjectured", "planted-clique detection at clique size o(sqrt n): conjectured hard on average", PLANTED, transition_known=True),
    cell("landscape", "clustering-proven", "planted-clique landscape: dense-subgraph overlap-gap property (rigorous)", GAMARNIK_ZADIK),
    ], notes="VC/CLIQUE decoupling: same decision NPC, opposite approximation and parameterized."))

# 8. Independent Set
ROWS.append(entry("independent-set", "Independent Set (decision)", "graph",
    "simple undirected graph, adjacency-list (sparse)", [
    cell("decision", "NPC", "IS decision: independent set of size >= k?", KARP),
    cell("counting", "#P-complete", "#independent sets", VAL_ENUM),
    cell("approximation", "inapprox", "MAX-IS: n^(1-eps) inapprox unless P=NP", HAST99, note="complement of clique"),
    cell("parameterized", "W[1]", "k-IS: W[1]-complete", DF95, perspective="solution size k"),
    na("parallelization", "NPC => within-P charge n.a. (E2)"),
    na("proof_size", "not a propositional refutation problem"),
    cell("average_case", "hard-on-average-conjectured", "planted independent set (complement of planted clique): conjectured hard", PLANTED, transition_known=True),
    cell("landscape", "clustering-proven", "max-independent-set on sparse random graphs: OGP (rigorous, Gamarnik-Sudan)", GS14),
    ], notes="Same charge signature as CLIQUE (complement) -- an H2 multiplet check."))

# 9. Graph 3-Coloring
ROWS.append(entry("graph-3-coloring", "Graph 3-Coloring", "graph",
    "simple undirected graph, adjacency-list; random G(n,m) ensemble", [
    cell("decision", "NPC", "3-COLORING decision", GJ, note="Karp/Stockmeyer"),
    cell("counting", "#P-complete", "#proper 3-colorings (chromatic-polynomial eval)", LINIAL),
    cell("approximation", "inapprox", "CHROMATIC NUMBER: n^(1-eps) inapprox", ZUCK, note="Feige-Kilian"),
    cell("parameterized", "FPT", "coloring parameterized by treewidth", CYG, perspective="treewidth"),
    na("parallelization", "NPC => within-P charge n.a. (E2)"),
    na("proof_size", "not a propositional refutation problem"),
    cell("average_case", "hard-on-average-conjectured", "random graph coloring near threshold: conjectured hard (clustered)", AN05, note="k-colorability threshold (Achlioptas-Naor)", transition_known=True),
    cell("landscape", "clustering-physics", "random graph colorings: clustering/freezing (cavity/replica, Zdeborova-Krzakala)", KMRTZ, note="R24: cavity-method physics; rigorous coloring-clustering is a separate large-k line (Molloy / Achlioptas-Coja-Oghlan)"),
    ]))

# 10. TSP
ROWS.append(entry("tsp", "Traveling Salesman (general, decision)", "optimization",
    "complete graph with arbitrary nonnegative edge weights; decision: tour <= B", [
    cell("decision", "NPC", "TSP decision (Hamiltonicity special case)", GJ),
    cell("counting", "#P-complete", "#Hamiltonian tours", VAL_ENUM),
    cell("approximation", "inapprox", "general TSP: no poly alpha-approx unless P=NP", SG76, note="metric TSP is APX (Christofides 3/2) -- a different, restricted object"),
    cell("parameterized", "FPT", "TSP parameterized by treewidth", CYG, perspective="treewidth"),
    na("parallelization", "NPC => within-P charge n.a. (E2)"),
    na("proof_size", "not a propositional refutation problem"),
    cell("average_case", "easy-on-average", "random Euclidean TSP: BHH concentration; PTAS (Arora)", BHH59, note="Arora 1998 PTAS for Euclidean"),
    op("landscape", "TSP tour landscape not a standard OGP object"),
    ]))

# 11. Permanent
ROWS.append(entry("permanent", "Permanent (0/1 and integer matrices)", "algebraic",
    "n x n matrix, entries in binary; 0/1 case = bipartite adjacency", [
    cell("decision", "P", "0/1-permanent nonzero <=> bipartite perfect matching exists", EDM65),
    cell("counting", "#P-complete", "compute the permanent (= count perfect matchings)", VAL_PERM),
    na("approximation", "not an NP-optimization problem; approximate-COUNTING (FPRAS, JSV 2004) is a different axis than charge 3"),
    na("parameterized", "not a standard parameterized decision problem"),
    op("parallelization", "the decision (matching) is in RNC; NC-membership open", note="MVV 1987; KUW 1986"),
    na("proof_size", "not a propositional refutation problem"),
    cell("average_case", "hard-on-average-provable", "permanent over a large field: provably hard on average (random self-reduction + #P-hardness)", LIPTON91, note="RSR (Lipton 1991) + #P-hardness (Valiant 1979)", worst_to_average_self_reduction=True),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ], notes="Permanent vs determinant: same algebraic surface, counting #P-complete vs FP, parallel open vs NC."))

# 12. Determinant
ROWS.append(entry("determinant", "Determinant", "algebraic",
    "n x n integer matrix, entries in binary", [
    cell("decision", "P", "singularity (det = 0?), poly-time / in NC", AB),
    cell("counting", "FP", "evaluate the determinant (in FP / GapL)", AB),
    na("approximation", "exactly-computable algebraic function; no optimization/approx axis"),
    na("parameterized", "not a parameterized decision problem"),
    cell("parallelization", "NC", "determinant in NC^2 (Csanky)", CSANKY),
    na("proof_size", "not a propositional refutation problem"),
    op("average_case", "determinant of random matrices: ensemble definable, computed exactly (in P); not a studied hardness question (R15 open, not n.a.)"),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ], notes="Determinant half of the permanent/determinant witness: counting FP, parallel NC."))

# 13. Factoring
ROWS.append(entry("factoring", "Integer Factoring (decision)", "number-theoretic",
    "integer N in binary; decision: does N have a factor in [2, k]?", [
    cell("decision", "NPI-candidate", "FACTOR decision; in NP intersect coNP, not known NPC", AB),
    na("counting", "not a solution-counting problem"),
    na("approximation", "not an optimization problem"),
    na("parameterized", "no standard parameterization"),
    op("parallelization", "not known in NC; in BQP (Shor)"),
    na("proof_size", "not a propositional refutation problem"),
    cell("average_case", "hard-on-average-crypto", "random RSA semiprimes: factoring assumption", RSA78),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ]))

# 14. Graph Isomorphism
ROWS.append(entry("graph-isomorphism", "Graph Isomorphism (decision)", "graph",
    "two simple undirected graphs, adjacency-list", [
    cell("decision", "NPI-candidate", "GI decision; NP, not known NPC; quasipolynomial", BABAI16),
    op("counting", "#isomorphisms is poly-time equivalent to GI decision (Mathon 1979); not #P-hard unless GI is easy", note="Mathon 1979"),
    na("approximation", "GI is a decision problem; robust/approximate GI is out of scope"),
    cell("parameterized", "FPT", "GI FPT for bounded color-class size / bounded degree", LUKS82, perspective="bounded degree (Luks)"),
    op("parallelization", "GI not known in NC"),
    na("proof_size", "not a propositional refutation problem"),
    cell("average_case", "easy-on-average", "random graphs G(n,1/2) canonizable in linear expected time", BES80),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ]))

# 15. Linear Programming
ROWS.append(entry("linear-programming", "Linear Programming", "optimization",
    "rational constraint matrix + objective, entries in binary; feasibility/optimization", [
    cell("decision", "P", "LP feasibility/optimization; poly-time (ellipsoid)", KHACH),
    na("counting", "continuous optimization; no discrete solution count"),
    na("approximation", "solved exactly in poly time; no approx-hardness for its own objective"),
    na("parameterized", "no standard parameterization"),
    cell("parallelization", "P-complete", "Linear Programming is P-complete", GHR),
    na("proof_size", "not a propositional refutation problem"),
    cell("average_case", "easy-on-average", "simplex: polynomial smoothed complexity", ST04),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ], notes="LP (P-complete parallel) vs matching (open parallel): the charge-5 decoupling witness."))

# 16. Matching
ROWS.append(entry("matching", "Maximum Matching", "graph",
    "simple undirected graph, adjacency-list; perfect/maximum matching", [
    cell("decision", "P", "max/perfect matching; Edmonds' blossom algorithm", EDM65),
    cell("counting", "#P-complete", "count perfect matchings (= permanent for bipartite)", VAL_PERM),
    na("approximation", "solved exactly in poly time"),
    na("parameterized", "decision in P"),
    op("parallelization", "perfect matching in RNC (KUW/MVV); NC-membership famously open", note="MVV 1987"),
    na("proof_size", "not a propositional refutation problem"),
    cell("average_case", "easy-on-average", "maximum matching on sparse random graphs: Karp-Sipser greedy near-optimal", KARP_SIPSER),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ], notes="Decision-easy/counting-hard; parallel open (contrast LP P-complete, determinant NC)."))

# 17. Knapsack
ROWS.append(entry("knapsack", "0/1 Knapsack (decision)", "number-theoretic",
    "n items with integer weights/values in binary; capacity W; decision: value >= V?", [
    cell("decision", "NPC", "0/1-KNAPSACK decision; weakly NP-complete (binary encoding)", GJ, note="GJ [MP9]; pseudo-poly DP"),
    cell("counting", "#P-complete", "#knapsack solutions", DYER03, note="#P-hard; FPRAS Dyer 2003"),
    cell("approximation", "FPTAS", "MAX-KNAPSACK: FPTAS", IK75),
    cell("parameterized", "W[1]", "k-subset-sum (exactly k items hitting the target): W[1]-hard", DF_KSUM, perspective="solution size k"),
    na("parallelization", "NPC => within-P charge n.a. (E2)"),
    na("proof_size", "not a propositional refutation problem"),
    cell("average_case", "easy-on-average", "random knapsack: expected polynomial time (poly # Pareto-optimal points)", BEIER_VOCKING),
    op("landscape", "knapsack solution-space geometry: the REM-like landscape lives on the number-partitioning row, not borrowed here (R13)"),
    ], notes="FPTAS witness (weakly NP-hard, poly-unbounded objective under binary encoding -- see R6/E5)."))

# 17b. Number Partitioning  (R13: first-class specimen; REM-like landscape witness)
ROWS.append(entry("number-partitioning", "Number Partitioning (PARTITION)", "number-theoretic",
    "n integers in binary; decision: split into two subsets of equal sum", [
    cell("decision", "NPC", "PARTITION decision; weakly NP-complete", GJ, note="GJ [SP12]"),
    cell("counting", "#P-complete", "#balanced partitions", VAL_ENUM),
    cell("approximation", "FPTAS", "min-discrepancy partition: FPTAS (subset-sum DP)", IK75),
    op("parameterized", "no standard W-hierarchy parameter curated"),
    na("parallelization", "NPC => within-P charge n.a. (E2)"),
    na("proof_size", "not a propositional refutation problem"),
    cell("average_case", "hard-on-average-conjectured", "random number partitioning hard phase: no efficient algorithm known", MERTENS, note="sharp solvability transition (Mertens 1998)", transition_known=True),
    cell("landscape", "clustering-proven", "random number partitioning: OGP / algorithmic obstruction (rigorous)", GAMARNIK_KIZILDAG, note="REM-like shattering; Borgs-Chayes-Pittel for the transition"),
    ], notes="R13: the REM-like landscape makes number partitioning a witness in its own right; the cell previously mis-attributed to knapsack now lives here."))

# 18. Set Cover
ROWS.append(entry("set-cover", "Set Cover (decision)", "optimization",
    "ground set + set system (incidence lists); decision: cover of size <= k?", [
    cell("decision", "NPC", "SET-COVER decision", KARP),
    op("counting", "#set-covers is #P-complete, but PB83 (cuts/reliability) was MIS-cited here; specific citation to verify (F-1 audit of the kept set)"),
    cell("approximation", "log-APX", "MIN-SET-COVER: (1-o(1)) ln n tight", FEIGE, note="Dinur-Steurer 2014 tight"),
    cell("parameterized", "W[2]+", "k-SET-COVER: W[2]-complete", DF99, perspective="solution size k"),
    na("parallelization", "NPC => within-P charge n.a. (E2)"),
    na("proof_size", "not a propositional refutation problem"),
    op("average_case", "random set-cover ensembles not curated in pilot"),
    op("landscape", "not curated in pilot"),
    ], notes="log-APX and W[2] populate distinct approximation/parameterized values."))

# 19. Max-Cut
ROWS.append(entry("max-cut", "Maximum Cut", "graph",
    "simple undirected graph, adjacency-list; random G(n,c/n) ensemble", [
    cell("decision", "NPC", "MAX-CUT decision: cut >= B?", KARP),
    cell("counting", "#P-complete", "#maximum cuts / #cuts", PB83),
    cell("approximation", "APX-complete", "MAX-CUT: 0.878 (GW); APX-complete; UGC-optimal", GW95, note="Papadimitriou-Yannakakis MAX-SNP"),
    cell("parameterized", "FPT", "MAX-CUT above the m/2 guarantee: FPT", CYG, perspective="above-guarantee (m/2 + k)"),
    na("parallelization", "NPC => within-P charge n.a. (E2)"),
    na("proof_size", "not a propositional refutation problem"),
    cell("average_case", "hard-on-average-conjectured", "max-cut of sparse random graphs: conjectured hard near the spin-glass value (OGP barrier)", DMS17, note="extremal-cut value known (Dembo-Montanari-Sen 2017)", transition_known=True),
    cell("landscape", "clustering-proven", "max-cut on random graphs: OGP (rigorous, spin-glass line)", CGPR, note="Chen-Gamarnik-Panchenko-Rahman; Dembo-Montanari-Sen for the extremal-cut value"),
    ]))

# 20. PHP (pigeonhole family)
ROWS.append(entry("php", "Pigeonhole Principle PHP^{n+1}_n (family)", "logic-proof",
    "fixed unsatisfiable CNF encoding n+1 pigeons into n holes; parameterized by n", [
    na("decision", "PHP_n is a fixed unsatisfiable CNF family, not a decision problem with varying input (R1)"),
    na("counting", "not a solution-counting problem (unsatisfiable)"),
    na("approximation", "not an optimization problem"),
    na("parameterized", "not a parameterized decision problem"),
    na("parallelization", "not a within-P decision problem"),
    cell("proof_size", "exp", "PHP^{n+1}_n Resolution refutation: 2^Omega(n) lower bound", HAKEN, perspective="Resolution"),
    na("average_case", "a deterministic family, not a random ensemble"),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ], notes="Charge-6 witness (human-trivial, Resolution-exponential); 7 n.a. cells illustrate R1/R2."))

# 21. TQBF
ROWS.append(entry("tqbf", "True Quantified Boolean Formula (TQBF)", "logic-proof",
    "fully-quantified Boolean formula; decision: is it true?", [
    cell("decision", "PSPACE-complete", "TQBF: PSPACE-complete", STOCK73),
    na("counting", "not a solution-counting problem in the NP sense"),
    na("approximation", "not an NP-optimization problem"),
    na("parameterized", "no standard W-hierarchy parameterization curated"),
    na("parallelization", "PSPACE-complete => not in P unless P=PSPACE; within-P charge n.a."),
    cell("proof_size", "exp", "false-QBF refutation in Q-resolution: exp lower bounds", BCJ15, perspective="Q-resolution"),
    op("average_case", "random QBF: algorithmic difficulty uncurated; QSAT phase transition known", cite=GENT_WALSH, transition_known=True),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ], notes="Populates PSPACE-complete on the decision partial order, plus a non-Resolution proof system."))

# 22. Random unsat 3-SAT refutation set  (the Census measured cell, R9)
ROWS.append(entry("random-3sat-refutation", "Random unsat 3-SAT: refutation set", "logic-proof",
    "random unsat 3-SAT near density 4.267; the SET of Resolution refutations (proof-space object)", [
    na("decision", "the object is the refutation SET / proof landscape, not a decision problem (see sat-3 for the decision charge)"),
    na("counting", "not a solution-counting problem"),
    na("approximation", "not an optimization problem"),
    na("parameterized", "not a parameterized decision problem"),
    na("parallelization", "not a within-P decision problem"),
    cell("proof_size", "exp", "random unsat 3-SAT Resolution refutation size: exponential", CS88, perspective="Resolution"),
    na("average_case", "the ensemble average-case decision charge lives on sat-3"),
    cell("landscape", "freezing-measured",
         "refutation-SET backbone/freezing of random unsat 3-SAT near threshold (proof-space landscape; R1: proofs, not solutions)",
         status="measured", experiment=CENSUS_C2,
         note="R14: value is freezing-measured, NOT clustering-OGP-known. Census C2 measured backbone STRENGTHENING and overlap CONCENTRATION (freezing-style evidence), not a proven overlap gap; no OGP theorem exists for proof space -- that absence is our own I3 novelty. C2 banked (done-gate MET); C3 will refine. Distinct object from the sat-3 solution-space OGP cell."),
    ], notes="R9 measured cell: the Census backbone datum enters charge 8's ledger as a self-generated, reproducible measurement (R14: freezing-measured, strictest standard for our own datum)."))


# ========================= A2 batch 1 (graph / logic / number / counting / optimization) =========================

# --- graph ---
ROWS.append(entry("dominating-set", "Dominating Set (decision)", "graph",
    "simple undirected graph, adjacency-list; decision: dominating set of size <= k?", [
    cell("decision", "NPC", "DOMINATING-SET decision", GJ, note="GJ [GT2]"),
    cell("counting", "#P-complete", "#dominating sets", VAL_ENUM),
    cell("approximation", "log-APX", "MIN-DOMINATING-SET: ln n greedy + (1-o(1)) ln n hardness (set-cover equivalent)", FEIGE, note="greedy ln n; hardness Feige 1998 via approx-preserving set-cover equivalence (R20)"),
    cell("parameterized", "W[2]+", "k-DOMINATING-SET: W[2]-complete", DF99, perspective="solution size k"),
    na("parallelization", "NPC => within-P charge n.a. (E2)"),
    na("proof_size", "not a propositional refutation problem"),
    op("average_case", "random-graph domination not curated"),
    op("landscape", "not curated"),
    ]))
ROWS.append(entry("feedback-vertex-set", "Feedback Vertex Set (decision)", "graph",
    "simple undirected graph, adjacency-list; delete <= k vertices to make acyclic", [
    cell("decision", "NPC", "FVS decision", KARP),
    cell("counting", "#P-complete", "#feedback vertex sets", VAL_ENUM),
    cell("approximation", "APX-complete", "MIN-FVS: 2-approximation (membership) + APX-hard", BAFNA, note="2-approx Bafna et al. 1999; APX-hardness Lund-Yannakakis 1994 (R20 both sides)"),
    cell("parameterized", "FPT", "k-FVS: FPT (iterative compression)", CYG, perspective="solution size k"),
    na("parallelization", "NPC => within-P charge n.a. (E2)"),
    na("proof_size", "not a propositional refutation problem"),
    op("average_case", "not curated"),
    op("landscape", "not curated"),
    ]))
ROWS.append(entry("steiner-tree", "Steiner Tree (decision)", "graph",
    "edge-weighted graph + terminal set; decision: Steiner tree of weight <= B?", [
    cell("decision", "NPC", "STEINER-TREE decision", KARP),
    op("counting", "#Steiner trees of weight <= B: per-problem #P-hardness not curated (F-1/R20)"),
    cell("approximation", "APX-complete", "MIN-STEINER-TREE: ~1.39 membership + APX-hard", BYRKA, note="1.39 upper Byrka et al. 2013; APX-hardness Bern-Plassmann 1989 (R20 both sides)"),
    cell("parameterized", "FPT", "Steiner tree parameterized by number of terminals", DREYFUS, perspective="#terminals"),
    na("parallelization", "NPC => within-P charge n.a. (E2)"),
    na("proof_size", "not a propositional refutation problem"),
    op("average_case", "not curated"),
    op("landscape", "not curated"),
    ]))
ROWS.append(entry("hamiltonian-cycle", "Hamiltonian Cycle", "graph",
    "simple undirected graph, adjacency-list; decision: does a Hamiltonian cycle exist?", [
    cell("decision", "NPC", "HAM-CYCLE decision", KARP),
    cell("counting", "#P-complete", "#Hamiltonian cycles", VAL_ENUM),
    na("approximation", "decision problem; the optimization version is TSP (separate row)"),
    cell("parameterized", "FPT", "Hamiltonicity parameterized by treewidth", CYG, perspective="treewidth"),
    na("parallelization", "NPC => within-P charge n.a. (E2)"),
    na("proof_size", "not a propositional refutation problem"),
    cell("average_case", "easy-on-average", "Hamilton cycles found a.a.s. at the Komlos-Szemeredi threshold", BFF, transition_known=True),
    op("landscape", "not curated"),
    ]))
ROWS.append(entry("longest-path", "Longest Path", "graph",
    "simple undirected graph, adjacency-list; decision: simple path of length >= k?", [
    cell("decision", "NPC", "LONGEST-PATH decision", GJ),
    cell("counting", "#P-complete", "#long paths", VAL_ENUM),
    cell("approximation", "poly-APX", "MAX-LONGEST-PATH: no constant-factor approx (n^(1-eps) hard); poly-factor approximable", KMR97),
    cell("parameterized", "FPT", "k-PATH: FPT via color-coding", AYZ, perspective="path length k"),
    na("parallelization", "NPC => within-P charge n.a. (E2)"),
    na("proof_size", "not a propositional refutation problem"),
    op("average_case", "not curated"),
    op("landscape", "not curated"),
    ], notes="FPT witness: 'hard' problem, but k-PATH is FPT by path length (color-coding)."))
ROWS.append(entry("reachability-stcon", "s-t Reachability (STCON)", "graph",
    "directed graph, adjacency-list; decision: is t reachable from s?", [
    cell("decision", "P", "STCON: NL-complete, in P", AB),
    cell("counting", "#P-complete", "#s-t paths in a DAG", VAL_ENUM),
    na("approximation", "decision problem, exactly solved"),
    na("parameterized", "decision in P"),
    cell("parallelization", "NC", "STCON is NL-complete and NL subset of NC^2", AB),
    na("proof_size", "not a propositional refutation problem"),
    na("average_case", "not a random-ensemble hardness object"),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ], notes="Decision-easy/counting-hard (#paths #P-c); NC parallel."))
ROWS.append(entry("max-flow", "Maximum Flow", "graph",
    "directed graph with integer capacities in binary; s-t max flow", [
    cell("decision", "P", "max-flow value >= v? poly-time (Edmonds-Karp)", AB),
    na("counting", "not a solution-counting problem"),
    na("approximation", "solved exactly in poly time"),
    na("parameterized", "decision in P"),
    cell("parallelization", "P-complete", "MAX-FLOW is P-complete", GSS),
    na("proof_size", "not a propositional refutation problem"),
    op("average_case", "not curated"),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ], notes="P-complete parallel (like LP), contrast matching (open) / MST (NC)."))
ROWS.append(entry("min-spanning-tree", "Minimum Spanning Tree", "graph",
    "edge-weighted undirected graph, adjacency-list", [
    cell("decision", "P", "MST weight <= B? poly-time (Kruskal/Prim)", AB),
    cell("counting", "FP", "#spanning trees = a determinant (Matrix-Tree theorem)", KIRCHHOFF),
    na("approximation", "solved exactly in poly time"),
    na("parameterized", "decision in P"),
    cell("parallelization", "NC", "MST in NC (Boruvka-style parallel contraction)", AB),
    na("proof_size", "not a propositional refutation problem"),
    na("average_case", "not a random-ensemble hardness object"),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ], notes="Counting FP (Matrix-Tree) + NC parallel: a determinant-like easy row."))
ROWS.append(entry("treewidth", "Treewidth (compute)", "graph",
    "simple undirected graph, adjacency-list; decision: treewidth <= k?", [
    cell("decision", "NPC", "TREEWIDTH <= k decision", ACP87),
    op("counting", "not curated"),
    op("approximation", "no constant-factor approximation known: Feige-Hajiaghayi-Lee is O(sqrt(log tw))-factor (not O(1)); constant-factor hardness only under the Small Set Expansion conjecture (Austrin-Pitassi-Wu) -- APX membership unproven (E-2/R20)"),
    cell("parameterized", "FPT", "treewidth <= k is FPT (linear-time, Bodlaender)", BODL, perspective="treewidth k"),
    na("parallelization", "NPC => within-P charge n.a. (E2)"),
    na("proof_size", "not a propositional refutation problem"),
    na("average_case", "not a random-ensemble hardness object"),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ], notes="FPT witness (Bodlaender linear-time FPT)."))
ROWS.append(entry("k-center", "k-Center", "optimization",
    "metric on n points (distance matrix); decision: cover with k radius-r balls?", [
    cell("decision", "NPC", "k-CENTER decision", GJ),
    op("counting", "#feasible k-center covers: per-problem #P-hardness not curated (F-1/R20)"),
    cell("approximation", "APX-complete", "k-CENTER: 2-approx and NP-hard to beat 2 (both established by Hochbaum-Shmoys)", HOCH_SHM),
    op("parameterized", "not curated"),
    na("parallelization", "NPC => within-P charge n.a. (E2)"),
    na("proof_size", "not a propositional refutation problem"),
    op("average_case", "not curated"),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ]))

# --- logic / CSP ---
ROWS.append(entry("nae-sat", "Not-All-Equal SAT", "sat-csp",
    "CNF; a clause is satisfied iff its literals are not all equal", [
    cell("decision", "NPC", "NAE-3SAT decision", SCHAEFER),
    cell("counting", "#P-complete", "#NAE-SAT (not affine => #P-complete)", CREIG),
    cell("approximation", "APX-complete", "MAX-NAE-SAT (MAX-SNP-complete)", AK),
    cell("parameterized", "FPT", "NAE-SAT parameterized by treewidth (same convention as sat-3)", CYG, perspective="treewidth"),
    na("parallelization", "NPC => within-P charge n.a. (E2)"),
    op("proof_size", "random NAE-SAT refutation size not curated"),
    cell("average_case", "hard-on-average-conjectured", "random NAE-SAT near threshold: conjectured hard (symmetric CSP, clustered)", AM06, note="clustering as in random k-SAT/coloring", transition_known=True),
    cell("landscape", "clustering-physics", "random NAE-SAT solution space: clustering (cavity; symmetric CSP)", AM06, note="R24: coded physics-grade for the curated small-k regime; rigorous NAE-clustering is a large-k result"),
    ]))
ROWS.append(entry("exact-cover-x3c", "Exact Cover by 3-Sets (X3C)", "sat-csp",
    "universe of 3n elements + triples; decision: exact cover?", [
    cell("decision", "NPC", "X3C decision", KARP),
    cell("counting", "#P-complete", "#exact covers", VAL_ENUM),
    na("approximation", "decision problem (perfect cover)"),
    op("parameterized", "not curated"),
    na("parallelization", "NPC => within-P charge n.a. (E2)"),
    na("proof_size", "not a propositional refutation problem"),
    op("average_case", "not curated"),
    op("landscape", "not curated"),
    ]))
ROWS.append(entry("circuit-sat", "Circuit SAT", "sat-csp",
    "Boolean circuit; decision: is there a satisfying input?", [
    cell("decision", "NPC", "CIRCUIT-SAT decision", AB),
    cell("counting", "#P-complete", "#satisfying assignments of a circuit", VAL_ENUM),
    cell("approximation", "APX-complete", "MAX-CIRCUIT-SAT (maximize satisfied outputs)", AK, note="generalizes MAX-SAT (APX-hard) and in APX by a random assignment"),
    na("parameterized", "no standard parameterization curated"),
    na("parallelization", "NPC => within-P charge n.a. (E2)"),
    op("proof_size", "not curated"),
    op("average_case", "not curated"),
    op("landscape", "not curated"),
    ]))
ROWS.append(entry("circuit-value-problem", "Circuit Value Problem (CVP)", "logic-proof",
    "Boolean circuit + input; decision: circuit output value", [
    cell("decision", "P", "CVP: evaluate the circuit, poly-time", AB),
    na("counting", "an evaluation problem, not solution-counting"),
    na("approximation", "exactly computed"),
    na("parameterized", "decision in P"),
    cell("parallelization", "P-complete", "CVP is the canonical P-complete problem", LADNER),
    na("proof_size", "not a propositional refutation problem"),
    na("average_case", "not a random-ensemble hardness object"),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ], notes="The canonical P-complete problem (parallelization witness)."))
ROWS.append(entry("tseitin", "Tseitin Formulas (family)", "logic-proof",
    "unsatisfiable CNF from a graph with odd total charge; parameterized by an expander family", [
    na("decision", "a fixed unsatisfiable CNF family, not a decision problem with varying input (R1)"),
    na("counting", "unsatisfiable"),
    na("approximation", "not an optimization problem"),
    na("parameterized", "not a parameterized decision problem"),
    na("parallelization", "not a within-P decision problem"),
    cell("proof_size", "exp", "Tseitin on bounded-degree expanders: Resolution size 2^Omega(n)", URQ, perspective="Resolution"),
    na("average_case", "a deterministic family (given the graph), not a random-ensemble object"),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ], notes="Charge-6 witness alongside PHP; the XOR/parity hard instances for Resolution."))

# --- number / algebra ---
ROWS.append(entry("subset-sum", "Subset Sum (decision)", "number-theoretic",
    "n integers in binary + target; decision: subset summing to target?", [
    cell("decision", "NPC", "SUBSET-SUM decision; weakly NP-complete", KARP, note="pseudo-poly DP"),
    cell("counting", "#P-complete", "#subsets hitting the target", VAL_ENUM),
    cell("approximation", "FPTAS", "MAX-SUBSET-SUM (closest sum <= target): FPTAS", IK75),
    cell("parameterized", "W[1]", "k-subset-sum (exactly k items): W[1]-hard", DF_KSUM, perspective="solution size k"),
    na("parallelization", "NPC => within-P charge n.a. (E2)"),
    na("proof_size", "not a propositional refutation problem"),
    op("average_case", "random subset-sum (density regimes); not fully curated"),
    op("landscape", "see number-partitioning for the REM-like landscape"),
    ]))
ROWS.append(entry("integer-programming", "Integer Linear Programming (feasibility)", "optimization",
    "rational constraint matrix in binary; decision: integer point in the polytope?", [
    cell("decision", "NPC", "ILP feasibility decision", KARP),
    op("counting", "#integer feasible points of the ILP: per-problem #P-hardness not curated (F-1/R20)"),
    na("approximation", "feasibility problem"),
    cell("parameterized", "FPT", "ILP is FPT in the number of variables (Lenstra)", LENSTRA, perspective="#variables (dimension)"),
    na("parallelization", "NPC => within-P charge n.a. (E2)"),
    na("proof_size", "not a propositional refutation problem"),
    op("average_case", "not curated"),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ], notes="FPT witness: fixed-dimension ILP is FPT (Lenstra)."))
ROWS.append(entry("primality", "Primality Testing", "number-theoretic",
    "integer N in binary; decision: is N prime?", [
    cell("decision", "P", "PRIMES is in P (AKS 2002)", AKS),
    na("counting", "not a solution-counting problem"),
    na("approximation", "decision problem"),
    na("parameterized", "decision in P"),
    op("parallelization", "primality in P; NC-membership not curated"),
    na("proof_size", "not a propositional refutation problem"),
    cell("average_case", "easy-on-average", "primality is in P, hence easy on average", AKS, note="in P"),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ], notes="Primality in P (contrast factoring NPI-candidate) -- same input, decision-vs-search decoupling."))
ROWS.append(entry("discrete-log", "Discrete Logarithm", "number-theoretic",
    "cyclic group (prime modulus) in binary; find/verify the exponent", [
    cell("decision", "NPI-candidate", "DLOG decision; in NP, not known NPC", AB),
    na("counting", "not a solution-counting problem"),
    na("approximation", "not an optimization problem"),
    na("parameterized", "no standard parameterization"),
    op("parallelization", "not known in NC; in BQP (Shor)"),
    na("proof_size", "not a propositional refutation problem"),
    cell("average_case", "hard-on-average-crypto", "the discrete-log crypto assumption; random self-reducible (worst-case hardness itself conjectural)", AB, note="RSR over the group; the boolean records the self-reduction without overwriting the crypto-conjectural status (R18)", worst_to_average_self_reduction=True),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ], notes="Crypto average-case hardness (like factoring); random self-reducible."))
ROWS.append(entry("shortest-vector-svp", "Shortest Vector Problem (SVP)", "lattice",
    "lattice basis (integer matrix in binary); find/verify a shortest nonzero vector", [
    cell("decision", "NPC", "SVP is NP-hard (under randomized reductions)", MICC, note="Ajtai; exact/near-exact"),
    na("counting", "not a solution-counting problem"),
    cell("approximation", "inapprox", "NP-hard to approximate within some constant factor", MICC),
    na("parameterized", "no standard parameterization curated"),
    op("parallelization", "not curated"),
    na("proof_size", "not a propositional refutation problem"),
    op("average_case", "Ajtai maps worst-case approx-SVP to average-case SIS (a DIFFERENT problem); no SVP self-reduction -- see the sis row (R18)"),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ], notes="Lattice problem; the celebrated worst-case-to-average reduction goes to SIS (a different problem), not SVP itself -- see the sis row (R18)."))
ROWS.append(entry("sis", "Short Integer Solution (SIS)", "lattice",
    "random A in Z_q^{n x m}; find a short nonzero integer x with Ax = 0 mod q (average-case-defined)", [
    op("decision", "SIS is average-case-defined; a worst-case decision version is not standard"),
    na("counting", "not a solution-counting problem"),
    na("approximation", "not an NP-optimization problem"),
    na("parameterized", "no standard parameterization"),
    op("parallelization", "not curated"),
    na("proof_size", "not a propositional refutation problem"),
    cell("average_case", "hard-on-average-provable", "average-case SIS is provably hard from worst-case approx lattice problems (Ajtai)", AJTAI, note="worst-case approx-SVP/SIVP => average-case SIS (Ajtai 1996); an INTER-problem reduction, so NOT a self-reduction", worst_to_average_self_reduction=False),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ], notes="R18: carries Ajtai's celebrated worst-case-to-average-case reduction (worst-case lattice => average-case SIS); foundation of lattice cryptography."))
ROWS.append(entry("gcd", "Greatest Common Divisor", "number-theoretic",
    "two integers in binary", [
    cell("decision", "P", "GCD computable in poly-time (Euclid)", AB),
    na("counting", "not a solution-counting problem"),
    na("approximation", "exactly computed"),
    na("parameterized", "decision in P"),
    op("parallelization", "integer GCD in NC is a FAMOUS OPEN problem; Kannan-Miller-Rudolph (1987) give a sublinear-depth parallel algorithm, not polylog depth -- so the cited work does not establish NC (E-1/R20)"),
    na("proof_size", "not a propositional refutation problem"),
    na("average_case", "not a random-ensemble hardness object"),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ]))

# --- counting ---
ROWS.append(entry("network-reliability", "Network Reliability", "graph",
    "graph with edge-failure probabilities; probability that s and t stay connected", [
    op("decision", "deciding R(G,p) >= t is PP-hard / #P-hard-threshold (above PH by Toda, conjecturally below PSPACE); NO clean rung in the R22 decision vocab -- the counting charge carries the #P-completeness (E-3/R13/R22; candidate future 'counting-hard' value)"),
    cell("counting", "#P-complete", "two-terminal reliability / #operational subgraphs", PB83),
    na("approximation", "the counting object; FPRAS status is a different axis"),
    na("parameterized", "not a parameterized decision problem"),
    op("parallelization", "not curated"),
    na("proof_size", "not a propositional refutation problem"),
    na("average_case", "not a random-ensemble hardness object"),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ], notes="Decision-easy/counting-hard (#P-complete reliability)."))
ROWS.append(entry("tutte-polynomial", "Tutte Polynomial (evaluation)", "algebraic",
    "graph; evaluate the Tutte polynomial at a fixed point", [
    na("decision", "an evaluation/counting object, not a decision problem (R1)"),
    cell("counting", "#P-complete", "evaluating the Tutte polynomial (most points) is #P-hard", JVW),
    na("approximation", "counting object; FPRAS only at special points"),
    cell("parameterized", "FPT", "Tutte polynomial parameterized by treewidth", CYG, perspective="treewidth"),
    na("parallelization", "not a within-P decision problem"),
    na("proof_size", "not a propositional refutation problem"),
    na("average_case", "not a random-ensemble hardness object"),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ], notes="Generalizes chromatic/reliability polynomials; #P-hard almost everywhere."))

# --- optimization / scheduling ---
ROWS.append(entry("bin-packing", "Bin Packing", "optimization",
    "n item sizes in binary + bin capacity; decision: pack into <= k bins?", [
    cell("decision", "NPC", "BIN-PACKING decision", GJ, note="GJ [SR1]"),
    op("counting", "#packings into <= k bins: per-problem #P-hardness not curated (F-1/R20)"),
    cell("approximation", "APX", "bin-packing: 3/2 ABSOLUTE-ratio hardness (from PARTITION) but an asymptotic FPTAS (AFPTAS); APX membership, not completeness (R19)", KK82, note="absolute-ratio convention (R19): constant-factor absolutely, near-optimal asymptotically"),
    cell("parameterized", "FPT", "FPT in the number of distinct item sizes", CYG, perspective="#distinct sizes"),
    na("parallelization", "NPC => within-P charge n.a. (E2)"),
    na("proof_size", "not a propositional refutation problem"),
    op("average_case", "not curated"),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ]))
ROWS.append(entry("makespan-scheduling", "Makespan Scheduling (P||Cmax)", "optimization",
    "n job lengths in binary + m machines; decision: makespan <= T?", [
    cell("decision", "NPC", "P||Cmax decision", GJ),
    op("counting", "#schedules with makespan <= T: per-problem #P-hardness not curated (F-1/R20)"),
    cell("approximation", "PTAS", "makespan scheduling: PTAS (Hochbaum-Shmoys)", HOCH_SHM),
    cell("parameterized", "FPT", "FPT in the number of machines / job types", CYG, perspective="#machines"),
    na("parallelization", "NPC => within-P charge n.a. (E2)"),
    na("proof_size", "not a propositional refutation problem"),
    op("average_case", "not curated"),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ], notes="PTAS witness (approximation strictly between FPTAS and APX-complete)."))
ROWS.append(entry("metric-tsp", "Metric TSP (decision)", "optimization",
    "complete graph, edge weights obey the triangle inequality; tour <= B?", [
    cell("decision", "NPC", "metric-TSP decision", GJ),
    cell("counting", "#P-complete", "#tours of length <= B", VAL_ENUM, note="#Hamiltonian-tours is #P-complete"),
    cell("approximation", "APX-complete", "metric TSP: 3/2 (Christofides) membership + APX-hard", CHRIST, note="3/2 Christofides 1976; APX-hardness Papadimitriou-Yannakakis 1993; general TSP is inapprox -- same surface, different object (R1)"),
    cell("parameterized", "FPT", "TSP parameterized by treewidth", CYG, perspective="treewidth"),
    na("parallelization", "NPC => within-P charge n.a. (E2)"),
    na("proof_size", "not a propositional refutation problem"),
    op("average_case", "random metric/Euclidean TSP concentrates; not fully curated"),
    op("landscape", "not curated"),
    ], notes="Metric-TSP APX-complete vs general-TSP inapprox: the R1 restricted-object witness."))
ROWS.append(entry("max-coverage", "Maximum Coverage", "optimization",
    "set system + budget k; decision: k sets covering >= t elements?", [
    cell("decision", "NPC", "MAX-COVERAGE decision", KARP),
    op("counting", "#k-subsets covering >= t elements: per-problem #P-hardness not curated (F-1/R20)"),
    cell("approximation", "APX-complete", "MAX-COVERAGE: (1-1/e) greedy membership + (1-1/e) hardness", FEIGE, note="(1-1/e) greedy Nemhauser-Wolsey-Fisher 1978; (1-1/e) hardness Feige 1998 (R20 both sides)"),
    op("parameterized", "k-coverage parameterization not curated"),
    na("parallelization", "NPC => within-P charge n.a. (E2)"),
    na("proof_size", "not a propositional refutation problem"),
    op("average_case", "not curated"),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ]))


# ========================= A2 batch 2 =========================

# --- graph ---
ROWS.append(entry("edge-coloring", "Edge Coloring (Chromatic Index)", "graph",
    "simple undirected graph, adjacency-list; decision: edge-colorable with Delta colors?", [
    cell("decision", "NPC", "deciding chromatic index Delta vs Delta+1", HOLYER),
    op("counting", "#proper edge-colorings: per-problem #P-hardness not curated (F-1/R20)"),
    cell("approximation", "APX", "edge-coloring: constant-factor (Vizing's Delta+1 <= 4/3 Delta) but NP-hard to beat 4/3 on cubic graphs (Holyer)", VIZING, note="membership Vizing 1964 (Delta+1); 4/3 barrier from Holyer 1981; APX-completeness NOT established, and the additive +1 (ratio->1 as Delta grows) makes completeness the wrong description (R19/R20)"),
    cell("parameterized", "FPT", "edge-coloring parameterized by treewidth", CYG, perspective="treewidth"),
    na("parallelization", "NPC => within-P charge n.a. (E2)"),
    na("proof_size", "not a propositional refutation problem"),
    op("average_case", "not curated"),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ]))
ROWS.append(entry("min-bisection", "Minimum Bisection", "graph",
    "simple undirected graph, adjacency-list; split into two equal halves minimizing cut", [
    cell("decision", "NPC", "MIN-BISECTION decision", GJ),
    op("counting", "#minimum bisections: per-problem #P-hardness not curated (F-1/R20)"),
    op("approximation", "O(log n) approximation known (Racke); no APX-hardness/membership settled"),
    cell("parameterized", "FPT", "min-bisection is FPT parameterized by the cut size", CYG, perspective="cut size k"),
    na("parallelization", "NPC => within-P charge n.a. (E2)"),
    na("proof_size", "not a propositional refutation problem"),
    op("average_case", "planted-bisection has a detectability transition; not curated here"),
    op("landscape", "not curated"),
    ]))
ROWS.append(entry("multiway-cut", "Multiway Cut", "graph",
    "edge-weighted graph + terminal set; separate all terminals minimizing cut", [
    cell("decision", "NPC", "MULTIWAY-CUT (>= 3 terminals) decision", DAHLHAUS),
    op("counting", "#minimum multiway cuts: per-problem #P-hardness not curated (F-1/R20)"),
    cell("approximation", "APX-complete", "1.2965-approximation + APX-hard", DAHLHAUS, note="APX-hard for >= 3 terminals (Dahlhaus et al.)"),
    cell("parameterized", "FPT", "multiway cut FPT in the cutset size", MARX06, perspective="cutset size k"),
    na("parallelization", "NPC => within-P charge n.a. (E2)"),
    na("proof_size", "not a propositional refutation problem"),
    op("average_case", "not curated"),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ]))
ROWS.append(entry("directed-feedback-vertex-set", "Directed Feedback Vertex Set", "graph",
    "directed graph, adjacency-list; delete <= k vertices to make acyclic", [
    cell("decision", "NPC", "directed FVS decision", KARP),
    op("counting", "#directed feedback vertex sets: per-problem #P-hardness not curated (F-1/R20)"),
    op("approximation", "O(log n log log n) approximation; no constant-factor / clean APX status"),
    cell("parameterized", "FPT", "directed FVS is FPT (Chen et al. 2008)", CLLOR, perspective="solution size k"),
    na("parallelization", "NPC => within-P charge n.a. (E2)"),
    na("proof_size", "not a propositional refutation problem"),
    op("average_case", "not curated"),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ], notes="Directed FVS FPT (Chen et al.) resolved a long-open question -- an FPT witness."))
ROWS.append(entry("three-dimensional-matching", "3-Dimensional Matching (3DM)", "graph",
    "tripartite hypergraph (triples over X,Y,Z); decision: perfect matching?", [
    cell("decision", "NPC", "3DM decision", KARP),
    cell("counting", "#P-complete", "#3-dimensional matchings", VAL_ENUM),
    cell("approximation", "APX-complete", "MAX-3DM: constant-factor + APX-hard", AK),
    cell("parameterized", "FPT", "k-3DM (3-set packing) is FPT via color-coding", AYZ, perspective="solution size k"),
    na("parallelization", "NPC => within-P charge n.a. (E2)"),
    na("proof_size", "not a propositional refutation problem"),
    op("average_case", "not curated"),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ]))
ROWS.append(entry("bipartiteness", "Bipartiteness (2-Coloring)", "graph",
    "simple undirected graph, adjacency-list; decision: is the graph 2-colorable?", [
    cell("decision", "P", "bipartiteness by BFS/DFS 2-coloring", AB),
    cell("counting", "FP", "#2-colorings = 2^(#connected components) if bipartite, else 0", AB),
    na("approximation", "decision problem, exactly solved"),
    na("parameterized", "decision in P"),
    cell("parallelization", "NC", "2-coloring / connectivity in NC (in fact SL=L)", AB),
    na("proof_size", "not a propositional refutation problem"),
    na("average_case", "not a random-ensemble hardness object"),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ], notes="Decision P, counting FP, parallel NC -- an easy row (contrast 3-coloring NPC)."))

# --- matrix / algebra ---
ROWS.append(entry("matrix-multiplication", "Matrix Multiplication", "matrix",
    "two n x n integer matrices in binary", [
    cell("decision", "P", "compute the product; poly-time", AB),
    na("counting", "not a solution-counting problem"),
    na("approximation", "exactly computed"),
    na("parameterized", "decision in P"),
    cell("parallelization", "NC", "matrix multiplication in NC^1", AB),
    na("proof_size", "not a propositional refutation problem"),
    na("average_case", "not a random-ensemble hardness object"),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ]))
ROWS.append(entry("linear-equations", "Solving Linear Equations", "matrix",
    "rational linear system in binary", [
    cell("decision", "P", "Gaussian elimination, poly-time", AB),
    na("counting", "the solution set is an affine subspace, not a discrete count"),
    na("approximation", "exactly solved"),
    na("parameterized", "decision in P"),
    cell("parallelization", "NC", "linear algebra over a field is in NC (Csanky/Berkowitz)", BGH82),
    na("proof_size", "not a propositional refutation problem"),
    na("average_case", "not a random-ensemble hardness object"),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ]))

# --- lattice / number ---
ROWS.append(entry("closest-vector-cvp", "Closest Vector Problem (CVP)", "lattice",
    "lattice basis (integer matrix) + target; find/verify the closest lattice vector", [
    cell("decision", "NPC", "CVP is NP-complete", VEB81),
    na("counting", "not a solution-counting problem"),
    cell("approximation", "inapprox", "NP-hard to approximate within almost-polynomial factors", DKRS),
    na("parameterized", "no standard parameterization curated"),
    op("parallelization", "not curated"),
    na("proof_size", "not a propositional refutation problem"),
    op("average_case", "worst-case-hardness stronger than SVP; average-case via lattice reductions -- see sis"),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ]))
ROWS.append(entry("quadratic-residuosity", "Quadratic Residuosity", "number-theoretic",
    "integer N + a in Z_N (binary); is a a quadratic residue mod N?", [
    cell("decision", "NPI-candidate", "QR decision; in NP intersect coNP, not known NPC", AB),
    na("counting", "not a solution-counting problem"),
    na("approximation", "not an optimization problem"),
    na("parameterized", "no standard parameterization"),
    op("parallelization", "not curated"),
    na("proof_size", "not a propositional refutation problem"),
    cell("average_case", "hard-on-average-crypto", "the QR crypto assumption; random self-reducible", AB, note="RSR; boolean records the self-reduction (R18)", worst_to_average_self_reduction=True),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ]))

# --- logic / proof / PH ---
ROWS.append(entry("tautology", "Propositional Tautology (TAUT)", "logic-proof",
    "propositional formula; decision: is it a tautology?", [
    cell("decision", "coNP-complete", "TAUT is coNP-complete -- a SIBLING of NPC, not above it (NP vs coNP open)", AB),
    na("counting", "not an NP-solution-counting problem"),
    na("approximation", "not an optimization problem"),
    na("parameterized", "no standard parameterization curated"),
    na("parallelization", "not a within-P decision problem"),
    cell("proof_size", "exp", "the canonical proof-complexity object; hard tautologies (PHP/Tseitin) are Resolution-exponential", HAKEN, perspective="Resolution"),
    na("average_case", "not a random-ensemble hardness object"),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ], notes="coNP-complete decision -- SIBLING of NPC (NP-vs-coNP as schema); TAUT IS proof complexity, the charge-6 home problem."))
ROWS.append(entry("sigma2-sat", "Sigma_2-SAT (exists-forall QBF)", "logic-proof",
    "quantified Boolean formula with one alternation (exists x forall y phi)", [
    cell("decision", "PH-complete", "Sigma_2^p-complete (second level of PH)", STOCK73, perspective="Sigma_2^p"),
    na("counting", "not an NP-solution-counting problem"),
    na("approximation", "not an optimization problem"),
    na("parameterized", "no standard parameterization curated"),
    na("parallelization", "not a within-P decision problem"),
    op("proof_size", "QBF/Sigma_2 proof systems studied; not curated here"),
    na("average_case", "not a random-ensemble hardness object"),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ], notes="Populates PH level 2 between NPC and PSPACE (TQBF)."))
ROWS.append(entry("monotone-circuit-value", "Monotone Circuit Value", "logic-proof",
    "monotone Boolean circuit (AND/OR only) + input; output value", [
    cell("decision", "P", "evaluate the monotone circuit, poly-time", AB),
    na("counting", "an evaluation problem, not solution-counting"),
    na("approximation", "exactly computed"),
    na("parameterized", "decision in P"),
    cell("parallelization", "P-complete", "monotone CVP is P-complete", GHR),
    na("proof_size", "not a propositional refutation problem"),
    na("average_case", "not a random-ensemble hardness object"),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ], notes="Monotone CVP is P-complete (like general CVP) -- parallelization witness."))

# --- CSP / optimization ---
ROWS.append(entry("one-in-three-sat", "One-in-Three SAT", "sat-csp",
    "3-CNF; a clause is satisfied iff exactly one literal is true (positive version)", [
    cell("decision", "NPC", "1-in-3-SAT decision", SCHAEFER),
    cell("counting", "#P-complete", "#1-in-3 assignments (not affine)", CREIG),
    cell("approximation", "APX-complete", "MAX-1-in-3-SAT", AK),
    cell("parameterized", "FPT", "1-in-3-SAT parameterized by treewidth (SAT-family convention)", CYG, perspective="treewidth"),
    na("parallelization", "NPC => within-P charge n.a. (E2)"),
    op("proof_size", "not curated"),
    op("average_case", "not curated"),
    op("landscape", "not curated"),
    ]))
ROWS.append(entry("max-2lin", "MAX-2-LIN over Z_q", "sat-csp",
    "system of 2-variable linear equations mod q; maximize satisfied equations", [
    cell("decision", "NPC", "MAX-2LIN gap decision", GJ),
    op("counting", "#max-satisfying assignments: per-problem #P-hardness not curated (F-1/R20)"),
    cell("approximation", "APX-complete", "constant-factor + APX-hard; UGC-tight (generalizes MAX-CUT)", KHOT02),
    cell("parameterized", "FPT", "MAX-2LIN parameterized by treewidth (SAT-family convention)", CYG, perspective="treewidth"),
    na("parallelization", "NPC => within-P charge n.a. (E2)"),
    na("proof_size", "not a propositional refutation problem"),
    op("average_case", "not curated"),
    op("landscape", "not curated"),
    ], notes="The Unique-Games canonical CSP; MAX-CUT is a special case."))
ROWS.append(entry("job-shop-scheduling", "Job-Shop Scheduling", "optimization",
    "n jobs, m machines, operation orders + times in binary; minimize makespan", [
    cell("decision", "NPC", "job-shop makespan <= T decision; strongly NP-hard", GJ),
    op("counting", "#schedules with makespan <= T: per-problem #P-hardness not curated (F-1/R20)"),
    op("approximation", "O(log^2) approximation known; no PTAS (strongly NP-hard); clean APX status not curated"),
    op("parameterized", "not curated"),
    na("parallelization", "NPC => within-P charge n.a. (E2)"),
    na("proof_size", "not a propositional refutation problem"),
    op("average_case", "not curated"),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ]))


# ========================= A2 batch 3 (populate the R22 decision rungs + more witnesses) =========================

ROWS.append(entry("lwe", "Learning With Errors (LWE)", "lattice",
    "random noisy linear system mod q (average-case-defined); recover the secret", [
    op("decision", "LWE is average-case-defined; a worst-case decision version is not standard"),
    na("counting", "not a solution-counting problem"),
    na("approximation", "not an NP-optimization problem"),
    na("parameterized", "no standard parameterization"),
    op("parallelization", "not curated"),
    na("proof_size", "not a propositional refutation problem"),
    cell("average_case", "hard-on-average-provable", "average-case LWE provably hard from worst-case lattice problems (Regev)", REGEV, note="worst-case GapSVP/SIVP => average-case LWE; INTER-problem reduction (not a self-reduction)", worst_to_average_self_reduction=False),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ], notes="With SIS, the second Ajtai/Regev worst-case-to-average lattice witness; the basis of modern lattice crypto."))
ROWS.append(entry("mcsp", "Minimum Circuit Size Problem (MCSP)", "logic-proof",
    "truth table + size s; decision: is there a circuit of size <= s computing it?", [
    cell("decision", "NPI-candidate", "MCSP: in NP, famously not known NP-complete (nor in P)", KABANETS_CAI),
    na("counting", "not a standard solution-counting problem"),
    na("approximation", "not an NP-optimization problem in the standard sense"),
    na("parameterized", "no standard parameterization curated"),
    op("parallelization", "not curated"),
    na("proof_size", "not a propositional refutation problem"),
    op("average_case", "not curated"),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ], notes="A rare natural NPI-candidate (with factoring/GI); central to meta-complexity."))
ROWS.append(entry("planarity", "Planarity Testing", "graph",
    "simple undirected graph, adjacency-list; decision: is it planar?", [
    cell("decision", "P", "planarity testing in linear time (Hopcroft-Tarjan)", HOPTAR),
    na("counting", "a decision property, not solution-counting"),
    na("approximation", "decision problem, exactly solved"),
    na("parameterized", "decision in P"),
    cell("parallelization", "NC", "planarity testing is in NC (AC^1)", AB),
    na("proof_size", "not a propositional refutation problem"),
    na("average_case", "not a random-ensemble hardness object"),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ]))
ROWS.append(entry("planar-matching-count", "Counting Perfect Matchings (planar)", "graph",
    "planar graph, adjacency-list; count perfect matchings", [
    cell("decision", "P", "perfect matching existence in P (Edmonds)", EDM65),
    cell("counting", "FP", "#perfect matchings of a PLANAR graph in poly time (FKT/Pfaffian)", KASTELEYN),
    na("approximation", "exactly counted"),
    na("parameterized", "in P for planar"),
    cell("parallelization", "NC", "planar #perfect-matchings via the Pfaffian = a determinant (in NC, Csanky)", CSANKY, note="FKT/Pfaffian reduces to determinant (F-4)"),
    na("proof_size", "not a propositional refutation problem"),
    na("average_case", "not a random-ensemble hardness object"),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ], notes="Counting FP when PLANAR (FKT) -- the structured foil to the #P-complete general permanent/#matchings."))
ROWS.append(entry("pi2-sat", "Pi_2-SAT (forall-exists QBF)", "logic-proof",
    "QBF with one alternation (forall x exists y phi)", [
    cell("decision", "PH-complete", "Pi_2^p-complete (second level of PH, co-side)", STOCK73, perspective="Pi_2^p"),
    na("counting", "not an NP-solution-counting problem"),
    na("approximation", "not an optimization problem"),
    na("parameterized", "no standard parameterization curated"),
    na("parallelization", "not a within-P decision problem"),
    op("proof_size", "Pi_2-QBF proof systems studied; not curated"),
    na("average_case", "not a random-ensemble hardness object"),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ], notes="Pi_2^p-complete: the co-sibling of Sigma_2-SAT at PH level 2."))
ROWS.append(entry("dnf-minimization", "Minimum Equivalent DNF", "logic-proof",
    "DNF formula + size k; decision: is there an equivalent DNF of size <= k?", [
    cell("decision", "PH-complete", "minimum equivalent DNF is Sigma_2^p-complete", UMANS, perspective="Sigma_2^p"),
    na("counting", "not a standard solution-counting problem"),
    op("approximation", "hard to approximate; not curated"),
    na("parameterized", "no standard parameterization curated"),
    na("parallelization", "not a within-P decision problem"),
    na("proof_size", "not a propositional refutation problem"),
    na("average_case", "not a random-ensemble hardness object"),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ], notes="A natural Sigma_2^p-complete problem (Umans) -- not artificial QBF."))
ROWS.append(entry("succinct-3-coloring", "Succinct 3-Coloring", "logic-proof",
    "graph given by a circuit (succinct representation); decision: 3-colorable?", [
    cell("decision", "beyond-PSPACE", "succinct 3-coloring is NEXP-complete", PY86),
    na("counting", "not curated at this level"),
    na("approximation", "not curated"),
    na("parameterized", "not curated"),
    na("parallelization", "not a within-P decision problem"),
    na("proof_size", "not a propositional refutation problem"),
    na("average_case", "not a random-ensemble hardness object"),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ], notes="Populates beyond-PSPACE (NEXP-complete): succinctness lifts NPC to NEXP-complete."))
ROWS.append(entry("odd-cycle-transversal", "Odd Cycle Transversal", "graph",
    "simple undirected graph; delete <= k vertices to make bipartite", [
    cell("decision", "NPC", "OCT decision", GJ),
    op("counting", "#odd cycle transversals: per-problem #P-hardness not curated (F-1/R20)"),
    op("approximation", "O(sqrt(log n)) approximation; no constant-factor / clean APX status"),
    cell("parameterized", "FPT", "OCT is FPT via iterative compression (Reed-Smith-Vetta)", REED_OCT, perspective="solution size k"),
    na("parallelization", "NPC => within-P charge n.a. (E2)"),
    na("proof_size", "not a propositional refutation problem"),
    op("average_case", "not curated"),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ], notes="FPT witness: iterative compression (Reed-Smith-Vetta)."))
ROWS.append(entry("cluster-editing", "Cluster Editing", "graph",
    "simple undirected graph; edit <= k edges to make a disjoint union of cliques", [
    cell("decision", "NPC", "cluster editing decision", GJ),
    op("counting", "#minimum cluster edit sets: per-problem #P-hardness not curated (F-1/R20)"),
    cell("approximation", "APX-complete", "constant-factor approx + APX-hard", AK),
    cell("parameterized", "FPT", "cluster editing is FPT in the edit budget", GRAMM_CE, perspective="edits k"),
    na("parallelization", "NPC => within-P charge n.a. (E2)"),
    na("proof_size", "not a propositional refutation problem"),
    op("average_case", "not curated"),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ]))
ROWS.append(entry("quadratic-assignment", "Quadratic Assignment (QAP)", "optimization",
    "two n x n matrices (flow, distance); assign facilities to locations minimizing cost", [
    cell("decision", "NPC", "QAP decision; strongly NP-hard", SG76),
    op("counting", "#optimal assignments: per-problem #P-hardness not curated (F-1/R20)"),
    cell("approximation", "inapprox", "no constant-factor approximation unless P=NP", SG76),
    na("parameterized", "no standard parameterization curated"),
    na("parallelization", "NPC => within-P charge n.a. (E2)"),
    na("proof_size", "not a propositional refutation problem"),
    op("average_case", "not curated"),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ]))
ROWS.append(entry("planar-3-coloring", "Planar 3-Coloring", "graph",
    "planar graph, adjacency-list; decision: 3-colorable?", [
    cell("decision", "NPC", "planar 3-coloring is NP-complete", GJS76),
    op("counting", "#proper 3-colorings of a planar graph: per-problem #P-hardness not curated (F-1/R20)"),
    cell("approximation", "APX", "planar chromatic number: 4/3-approx (output 4 by 4CT, opt >= 3); NP-hard to beat 4/3", GJS76, note="membership from the 4-colour theorem; 4/3 barrier from 3-vs-4 NP-hardness"),
    cell("parameterized", "FPT", "planar 3-coloring parameterized by treewidth", CYG, perspective="treewidth"),
    na("parallelization", "NPC => within-P charge n.a. (E2)"),
    na("proof_size", "not a propositional refutation problem"),
    op("average_case", "not curated"),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ], notes="Planarity restriction keeps 3-coloring NPC (Garey-Johnson-Stockmeyer)."))
ROWS.append(entry("steiner-forest", "Steiner Forest", "optimization",
    "edge-weighted graph + terminal PAIRS; connect each pair minimizing total weight", [
    cell("decision", "NPC", "Steiner forest decision (generalizes Steiner tree)", KARP),
    op("counting", "#minimum Steiner forests: per-problem #P-hardness not curated (F-1/R20)"),
    cell("approximation", "APX-complete", "2-approximation (Agrawal-Klein-Ravi) + APX-hard (from Steiner tree)", AKR95, note="2-approx AKR 1995; APX-hardness Bern-Plassmann"),
    op("parameterized", "FPT status by #terminal-pairs is subtle; not curated"),
    na("parallelization", "NPC => within-P charge n.a. (E2)"),
    na("proof_size", "not a propositional refutation problem"),
    op("average_case", "not curated"),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ]))
ROWS.append(entry("group-isomorphism", "Group Isomorphism (Cayley table)", "algebraic",
    "two groups by multiplication table; decision: isomorphic?", [
    cell("decision", "NPI-candidate", "group iso; n^(log n) time, not known NPC (easier than graph iso)", BABAI16, note="n^{O(log n)}; between P and GI"),
    op("counting", "#automorphisms; polynomial-time-equivalent to the decision (like GI)"),
    na("approximation", "a decision problem"),
    na("parameterized", "no standard parameterization curated"),
    op("parallelization", "not curated"),
    na("proof_size", "not a propositional refutation problem"),
    op("average_case", "not curated"),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ], notes="Another NPI-candidate; conjectured easier than graph isomorphism."))
ROWS.append(entry("maximum-common-subgraph", "Maximum Common Subgraph", "graph",
    "two graphs; find the largest graph isomorphic to a subgraph of both", [
    cell("decision", "NPC", "MAX-COMMON-SUBGRAPH decision (contains CLIQUE / subgraph-iso)", GJ),
    op("counting", "#maximum common subgraphs: per-problem #P-hardness not curated (F-1/R20)"),
    cell("approximation", "inapprox", "as hard to approximate as MAX-CLIQUE (n^(1-eps))", HAST99),
    cell("parameterized", "W[1]", "W[1]-hard (contains subgraph isomorphism by pattern size)", DF95, perspective="pattern size k"),
    na("parallelization", "NPC => within-P charge n.a. (E2)"),
    na("proof_size", "not a propositional refutation problem"),
    op("average_case", "not curated"),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ]))
ROWS.append(entry("first-order-model-checking", "First-Order Model Checking (combined)", "logic-proof",
    "finite structure + first-order sentence; decision: does the structure satisfy it?", [
    cell("decision", "PSPACE-complete", "FO model checking is PSPACE-complete in combined complexity", VARDI82),
    na("counting", "not a standard solution-counting problem"),
    na("approximation", "not an optimization problem"),
    cell("parameterized", "W[2]+", "FO model-checking parameterized by formula: AW[*]-complete", DF99, perspective="formula size; AW[*]-complete (Downey-Fellows-Taylor); FPT on nowhere-dense classes (Grohe et al.)"),
    na("parallelization", "not a within-P decision problem"),
    na("proof_size", "not a propositional refutation problem"),
    na("average_case", "not a random-ensemble hardness object"),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ], notes="Populates PSPACE-complete (combined complexity), beyond TQBF."))


# ========================= A2 batch 4 (NP-optimization: clean approximation + parameterized) =========================

def _npc_opt(pid, name, family, enc, approx_val, approx_task, approx_cite, param_val, param_task, param_persp,
             param_cite, approx_note=None, notes=None, landscape=None, counting_cite=None, counting_confirmed=False):
    """Helper for an NP-complete optimization problem with clean core charges; frontier honest."""
    cells = [
        cell("decision", "NPC", f"{name} decision", KARP),
        # F-1/R20: NO generic 'counting solutions of NPC is #P-complete' stamp. A per-problem counting-hardness
        # result must be cited explicitly (pass counting_cite); otherwise the #-version is open.
        (cell("counting", "#P-complete", f"#-version of {name}", counting_cite,
              status=("confirmed" if counting_confirmed else "claimed"), primary_source=counting_confirmed)
         if counting_cite else
         op("counting", f"#-version of {name}: no per-problem counting-hardness result curated (F-1/R20)")),
        cell("approximation", approx_val, approx_task, approx_cite, note=approx_note),
        cell("parameterized", param_val, param_task, param_cite, perspective=param_persp),
        na("parallelization", "NPC => within-P charge n.a. (E2)"),
        na("proof_size", "not a propositional refutation problem"),
        op("average_case", "not curated"),
        (landscape if landscape else na("landscape", "not a random-ensemble solution-geometry object")),
    ]
    return entry(pid, name, family, enc, cells, notes=notes)

ROWS.append(_npc_opt("connected-vertex-cover", "Connected Vertex Cover", "graph",
    "simple undirected graph; a vertex cover that induces a connected subgraph, size <= k",
    "APX-complete", "MIN-connected-VC: 2-approximation + APX-hard", AK, "FPT", "FPT in solution size k", "solution size k", CYG))
ROWS.append(_npc_opt("edge-dominating-set", "Edge Dominating Set", "graph",
    "simple undirected graph; edge set dominating all edges, size <= k",
    "APX-complete", "MIN-EDS: 2-approximation + APX-hard", AK, "FPT", "FPT in solution size k", "solution size k", CYG))
ROWS.append(_npc_opt("hitting-set", "Hitting Set", "optimization",
    "ground set + set family; hit every set with <= k elements",
    "log-APX", "MIN-HITTING-SET: ln n greedy + hardness (set-cover dual)", FEIGE, "W[2]+", "k-HITTING-SET: W[2]-complete", "solution size k", DF99))
ROWS.append(_npc_opt("maximum-leaf-spanning-tree", "Maximum Leaf Spanning Tree", "graph",
    "simple undirected graph; spanning tree with >= k leaves",
    "APX-complete", "MAX-LEAF: 2-approximation + APX-hard", AK, "FPT", "FPT in number of leaves k", "leaves k", CYG))
ROWS.append(_npc_opt("prize-collecting-steiner-tree", "Prize-Collecting Steiner Tree", "optimization",
    "edge-weighted graph + vertex penalties; minimize tree weight + unconnected penalties",
    "APX-complete", "2-approximation + APX-hard (from Steiner tree)", AKR95, "FPT", "FPT in number of terminals", "#terminals", CYG))
ROWS.append(_npc_opt("feedback-arc-set-tournament", "Feedback Arc Set in Tournaments", "graph",
    "tournament (complete directed graph); delete <= k arcs to make acyclic",
    "PTAS", "FAST: PTAS on tournaments (Kenyon-Mathieu-Schudy)", KENYON_MATHIEU, "FPT", "FPT in solution size k", "solution size k", CYG))
ROWS.append(_npc_opt("kemeny-rank-aggregation", "Kemeny Rank Aggregation", "optimization",
    "set of permutations; find a consensus ranking minimizing total Kendall-tau distance",
    "PTAS", "Kemeny consensus: PTAS (Kenyon-Mathieu-Schudy)", KENYON_MATHIEU, "FPT", "FPT in the optimal Kemeny score", "Kemeny score k", CYG))
ROWS.append(_npc_opt("capacitated-vertex-cover", "Capacitated Vertex Cover", "graph",
    "graph with vertex capacities; cover all edges respecting capacities, size <= k",
    "APX-complete", "2-approximation + APX-hard", AK, "FPT", "FPT in solution size k", "solution size k", CYG))
ROWS.append(_npc_opt("k-set-packing", "k-Set Packing", "optimization",
    "family of sets each of size <= k; find a maximum disjoint subfamily",
    "APX-complete", "MAX-k-SET-PACKING: constant-factor + APX-hard (for fixed k)", AK, "FPT", "FPT in solution size via color-coding", "solution size", AYZ))
ROWS.append(_npc_opt("partial-vertex-cover", "Partial Vertex Cover", "graph",
    "graph; choose k vertices covering the maximum number of edges",
    "APX-complete", "constant-factor + APX-hard", AK, "W[1]", "k-PARTIAL-VC: W[1]-hard", "solution size k", DF95))
ROWS.append(_npc_opt("group-steiner-tree", "Group Steiner Tree", "optimization",
    "edge-weighted graph + vertex groups; minimum tree touching every group",
    "log-APX", "O(log^2 n) approximation; log^{2-eps} hardness (Halperin-Krauthgamer) -- a POLYLOG gap", AK, "FPT", "FPT in number of groups", "#groups", CYG,
    approx_note="coded log-APX (closest rung): true status is polylog (O(log^2) approx / log^{2-eps} hard), NOT inapprox -- vocab lacks a polylog rung (v2 candidate) (F-2)"))

# decision problems adding parameterized coverage (approximation n.a. -- not optimization objects)
ROWS.append(entry("graph-motif", "Graph Motif", "graph",
    "vertex-colored graph + multiset of colors; connected subgraph realizing the multiset", [
    cell("decision", "NPC", "GRAPH-MOTIF decision", GJ),
    op("counting", "#occurrences of the motif: per-problem #P-hardness not curated (F-1/R20)"),
    na("approximation", "a decision/pattern problem, not an optimization object"),
    cell("parameterized", "FPT", "FPT in motif size via color-coding", AYZ, perspective="motif size k"),
    na("parallelization", "NPC => within-P charge n.a. (E2)"),
    na("proof_size", "not a propositional refutation problem"),
    op("average_case", "not curated"),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ]))
ROWS.append(entry("induced-subgraph-isomorphism", "Induced Subgraph Isomorphism", "graph",
    "pattern graph H + host graph G; is there an induced copy of H in G?", [
    cell("decision", "NPC", "induced subgraph isomorphism decision (contains CLIQUE)", GJ),
    op("counting", "#induced copies of H: per-problem #P-hardness not curated (F-1/R20)"),
    na("approximation", "a decision problem"),
    cell("parameterized", "W[1]", "W[1]-hard in pattern size (contains k-CLIQUE)", DF95, perspective="pattern size k"),
    na("parallelization", "NPC => within-P charge n.a. (E2)"),
    na("proof_size", "not a propositional refutation problem"),
    op("average_case", "not curated"),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ]))
ROWS.append(entry("disjoint-paths", "Vertex-Disjoint Paths", "graph",
    "graph + k terminal pairs; k vertex-disjoint paths connecting them", [
    cell("decision", "NPC", "k-DISJOINT-PATHS decision (NP-hard for variable k)", KARP),
    op("counting", "#disjoint-path systems: per-problem #P-hardness not curated (F-1/R20)"),
    na("approximation", "a decision problem"),
    cell("parameterized", "FPT", "FPT in the number of pairs k (Robertson-Seymour graph minors)", RS95, perspective="#pairs k"),
    na("parallelization", "NPC => within-P charge n.a. (E2)"),
    na("proof_size", "not a propositional refutation problem"),
    op("average_case", "not curated"),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ], notes="A celebrated FPT result (Robertson-Seymour graph minors)."))
ROWS.append(entry("cutwidth", "Cutwidth", "graph",
    "graph; linear vertex ordering minimizing the maximum edge cut, <= k", [
    cell("decision", "NPC", "CUTWIDTH decision", GJ),
    op("counting", "#optimal orderings: per-problem #P-hardness not curated (F-1/R20)"),
    op("approximation", "O(log^2 n) approximation; clean APX status not curated"),
    cell("parameterized", "FPT", "FPT in the cutwidth k", CYG, perspective="cutwidth k"),
    na("parallelization", "NPC => within-P charge n.a. (E2)"),
    na("proof_size", "not a propositional refutation problem"),
    op("average_case", "not curated"),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ]))
ROWS.append(entry("treedepth", "Treedepth", "graph",
    "graph; minimum height of an elimination forest, <= k", [
    cell("decision", "NPC", "TREEDEPTH decision", GJ),
    op("counting", "#optimal elimination forests: per-problem #P-hardness not curated (F-1/R20)"),
    cell("approximation", "APX", "treedepth: constant-factor approximation (membership); APX-hardness not established", CYG, note="constant-factor via CYG; completeness not claimed (R19/R20)"),
    cell("parameterized", "FPT", "FPT in treedepth k (and computable in linear FPT time)", CYG, perspective="treedepth k"),
    na("parallelization", "NPC => within-P charge n.a. (E2)"),
    na("proof_size", "not a propositional refutation problem"),
    op("average_case", "not curated"),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ]))
ROWS.append(entry("minimum-fill-in", "Minimum Fill-In", "graph",
    "graph; add <= k edges to make it chordal", [
    cell("decision", "NPC", "MIN-FILL-IN decision", GJ, note="Yannakakis 1981"),
    op("counting", "#minimum chordal completions: per-problem #P-hardness not curated (F-1/R20)"),
    op("approximation", "approximation studied; clean APX status not curated"),
    cell("parameterized", "FPT", "FPT in the number of added edges k", CYG, perspective="fill edges k"),
    na("parallelization", "NPC => within-P charge n.a. (E2)"),
    na("proof_size", "not a propositional refutation problem"),
    op("average_case", "not curated"),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ]))
ROWS.append(entry("weighted-interval-scheduling", "Weighted Interval Scheduling", "optimization",
    "weighted intervals on a line; select a max-weight non-overlapping subset", [
    cell("decision", "P", "solved exactly by DP (sort + longest-weighted chain)", AB),
    cell("counting", "FP", "#optimal selections computable in poly time (DP)", AB),
    na("approximation", "solved exactly in poly time"),
    na("parameterized", "decision in P"),
    op("parallelization", "not curated"),
    na("proof_size", "not a propositional refutation problem"),
    na("average_case", "not a random-ensemble hardness object"),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ], notes="Easy row (P/FP) -- the tractable interval-structured foil to NP-hard packing."))


# ========================= A2 batch 5 (final push to ~120) =========================

# clean NP-optimization (approx + param cited where clean, else n.a.)
ROWS.append(_npc_opt("densest-k-subgraph", "Densest k-Subgraph", "graph",
    "graph; choose k vertices maximizing induced edges",
    "poly-APX", "O(n^{1/4}) approximation (Bhaskara et al.); strong n^eps hardness is CONDITIONAL only", AK,
    "W[1]", "W[1]-hard in k", "solution size k", DF95,
    approx_note="poly-APX with CONDITIONAL hardness -- there is an n^{1/4} algorithm, so NOT unconditional inapprox (F-2)"))
ROWS.append(_npc_opt("cluster-vertex-deletion", "Cluster Vertex Deletion", "graph",
    "graph; delete <= k vertices to make a disjoint union of cliques",
    "APX-complete", "constant-factor + APX-hard", AK, "FPT", "FPT in solution size k", "solution size k", CYG))
ROWS.append(_npc_opt("max-directed-cut", "Maximum Directed Cut", "graph",
    "directed graph; partition maximizing arcs from left to right",
    "APX-complete", "MAX-DICUT: constant-factor + APX-hard", AK, "FPT", "FPT above the m/4 guarantee", "above-guarantee k", CYG))
ROWS.append(_npc_opt("d-hitting-set", "d-Hitting Set", "optimization",
    "family of sets each of size <= d; hit all with <= k elements",
    "APX-complete", "d-approximation + APX-hard (fixed d)", AK, "FPT", "FPT in k for fixed d (sunflower kernel)", "solution size k", CYG))
ROWS.append(_npc_opt("bin-covering", "Bin Covering", "optimization",
    "item sizes; maximize the number of bins filled to >= 1",
    "APX", "asymptotic FPTAS (AFPTAS) but constant absolute ratio -- APX, not completeness (R19)", KK82, "FPT", "FPT in the number of distinct sizes", "#distinct sizes", CYG,
    approx_note="absolute-ratio convention (R19)"))
ROWS.append(entry("survivable-network-design", "Survivable Network Design", "optimization",
    "edge-weighted graph + connectivity requirements r(u,v); min-cost subgraph meeting them", [
    cell("decision", "NPC", "SNDP decision (generalizes Steiner tree)", KARP),
    op("counting", "#min-cost survivable subgraphs: per-problem #P-hardness not curated (F-1/R20)"),
    cell("approximation", "APX-complete", "2-approximation (Jain) + APX-hard (from Steiner tree)", JAIN01),
    na("parameterized", "no standard single-parameter tractability curated"),
    na("parallelization", "NPC => within-P charge n.a. (E2)"),
    na("proof_size", "not a propositional refutation problem"),
    op("average_case", "not curated"),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ]))
ROWS.append(entry("shortest-common-superstring", "Shortest Common Superstring", "string",
    "set of strings; find the shortest string containing all as substrings", [
    cell("decision", "NPC", "SCS decision", GJ),
    op("counting", "#shortest common superstrings: per-problem #P-hardness not curated (F-1/R20)"),
    cell("approximation", "APX-complete", "constant-factor + APX-hard", AK),
    na("parameterized", "no standard parameterization curated"),
    na("parallelization", "NPC => within-P charge n.a. (E2)"),
    na("proof_size", "not a propositional refutation problem"),
    op("average_case", "not curated"),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ]))
ROWS.append(entry("directed-steiner-tree", "Directed Steiner Tree", "optimization",
    "directed edge-weighted graph + root + terminals; min-cost arborescence reaching terminals", [
    cell("decision", "NPC", "directed Steiner tree decision", KARP),
    op("counting", "#min-cost directed Steiner trees: per-problem #P-hardness not curated (F-1/R20)"),
    cell("approximation", "log-APX", "O(n^eps)-approx for every eps + polylog approx; log^{2-eps} hardness -- a POLYLOG gap", AK, contested="coded log-APX (closest rung): true status is polylog and n^eps-approx exists for every eps, so NOT inapprox -- v2 vocab candidate (F-2)"),
    op("parameterized", "FPT/XP in #terminals is subtle; not curated"),
    na("parallelization", "NPC => within-P charge n.a. (E2)"),
    na("proof_size", "not a propositional refutation problem"),
    op("average_case", "not curated"),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ]))
ROWS.append(entry("k-median", "k-Median", "optimization",
    "metric on n points; open k centers minimizing total assignment distance", [
    cell("decision", "NPC", "k-MEDIAN decision", GJ),
    op("counting", "#optimal center sets: per-problem #P-hardness not curated (F-1/R20)"),
    cell("approximation", "APX-complete", "constant-factor (~2.6) + APX-hard (1+2/e)", AK),
    na("parameterized", "no standard single-parameter tractability curated"),
    na("parallelization", "NPC => within-P charge n.a. (E2)"),
    na("proof_size", "not a propositional refutation problem"),
    op("average_case", "not curated"),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ]))

# planar-PTAS trio (structure improves approximability -- a clean structural finding)
ROWS.append(_npc_opt("planar-vertex-cover", "Vertex Cover (planar)", "graph",
    "planar graph; vertex cover of size <= k",
    "PTAS", "planar VC: PTAS (Baker's technique)", BAKER94, "FPT", "linear kernel / FPT in k", "solution size k", CYG,
    counting_cite=VADHAN01, counting_confirmed=True,
    notes="Planar restriction lifts VC from APX-complete to PTAS -- structure improves approximability. #VC #P-complete even planar (Vadhan) -- CONFIRMED at owner promotion (R8)."))
ROWS.append(_npc_opt("planar-dominating-set", "Dominating Set (planar)", "graph",
    "planar graph; dominating set of size <= k",
    "PTAS", "planar dominating set: PTAS (Baker/bidimensionality)", BAKER94, "FPT", "FPT (linear kernel; bidimensionality)", "solution size k", CYG,
    notes="Planar lifts dominating set from log-APX/W[2] to PTAS/FPT."))
ROWS.append(_npc_opt("planar-independent-set", "Independent Set (planar)", "graph",
    "planar graph; independent set of size >= k",
    "PTAS", "planar MAX-IS: PTAS (Lipton-Tarjan separators / Baker)", BAKER94, "FPT", "FPT (subexponential via separators)", "solution size k", CYG,
    counting_cite=VADHAN01, counting_confirmed=True,
    notes="Planar lifts IS from inapprox/W[1] to PTAS/FPT. #IS #P-complete even planar (Vadhan) -- CONFIRMED at owner promotion (R8)."))

# witnesses
ROWS.append(entry("stable-matching", "Stable Matching (Stable Marriage)", "optimization",
    "two sides with preference lists; find a stable matching", [
    cell("decision", "P", "a stable matching always exists and is found by Gale-Shapley (poly-time)", GALE_SHAPLEY),
    cell("counting", "#P-complete", "#stable matchings is #P-complete (Irving-Leather)", IRVING_LEATHER),
    na("approximation", "decision/search solved exactly (existence guaranteed)"),
    na("parameterized", "decision in P"),
    op("parallelization", "stable matching is CC-complete (comparator circuits); NC-membership open"),
    na("proof_size", "not a propositional refutation problem"),
    na("average_case", "not a random-ensemble hardness object"),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ], notes="Decision-easy (Gale-Shapley) / counting-hard (#P-complete, Irving-Leather) -- another such witness."))
ROWS.append(entry("min-cost-flow", "Minimum-Cost Flow", "graph",
    "directed graph with capacities + costs (binary); min-cost feasible flow", [
    cell("decision", "P", "min-cost flow in poly-time (e.g. network simplex / scaling)", AB),
    na("counting", "not a discrete solution-counting problem"),
    na("approximation", "solved exactly in poly time"),
    na("parameterized", "decision in P"),
    cell("parallelization", "P-complete", "min-cost flow generalizes max-flow (P-complete); logspace-hard", GSS),
    na("proof_size", "not a propositional refutation problem"),
    na("average_case", "not a random-ensemble hardness object"),
    na("landscape", "not a random-ensemble solution-geometry object"),
    ]))

# fine-grained P problems (populate P; foreshadow the v2 fine-grained charge -- SETH/3SUM/APSP)
def _finegrained_P(pid, name, family, enc, task, cite, note, parallel=None):
    return entry(pid, name, family, enc, [
        cell("decision", "P", task, cite, note=note),
        na("counting", "not a discrete solution-counting problem"),
        na("approximation", "solved exactly in poly time"),
        na("parameterized", "decision in P"),
        (parallel if parallel else op("parallelization", "not curated")),
        na("proof_size", "not a propositional refutation problem"),
        op("average_case", "random ensembles for this problem exist and are studied; algorithmic-difficulty value not curated (R15: open, not n.a. -- F-3)"),
        na("landscape", "not a random-ensemble solution-geometry object"),
    ], notes="Fine-grained: in P, but a conjectured time lower bound (candidate v2 charge 9).")

ROWS.append(_finegrained_P("edit-distance", "Edit Distance", "string",
    "two strings; minimum insert/delete/substitute operations",
    "O(n^2) dynamic programming", AB, "no strongly subquadratic algorithm unless SETH fails (Backurs-Indyk 2015)"))
ROWS.append(_finegrained_P("longest-common-subsequence", "Longest Common Subsequence", "string",
    "two strings; length of the longest common subsequence",
    "O(n^2) dynamic programming", AB, "SETH-hard for strongly subquadratic (Abboud-Backurs-Williams 2015)"))
ROWS.append(_finegrained_P("all-pairs-shortest-path", "All-Pairs Shortest Path (APSP)", "graph",
    "weighted graph; shortest path between every pair",
    "O(n^3) (Floyd-Warshall); truly-subcubic open", AB, "APSP conjecture: no truly subcubic algorithm",
    parallel=cell("parallelization", "NC", "APSP via O(log n) rounds of min-plus (tropical) matrix squaring", AB, note="min-plus repeated squaring => NC (F-3)")))
ROWS.append(_finegrained_P("3sum", "3SUM", "number-theoretic",
    "n integers; are there three summing to zero?",
    "O(n^2) (in P)", GO95, "3SUM conjecture: no truly subquadratic algorithm (Gajentaan-Overmars)"))


def main():
    with open(ATLAS, "w", encoding="utf-8") as f:
        for r in ROWS:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"wrote {len(ROWS)} problems to {ATLAS}")


if __name__ == "__main__":
    main()
