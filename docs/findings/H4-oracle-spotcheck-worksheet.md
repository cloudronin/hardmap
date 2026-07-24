# H4 oracle spot-check — worksheet (sealed draw)

Sealed seed **20260724**. 10 cited-filled cells per charge column, drawn from the frozen atlas
(`atlas.jsonl`, 118 problems, `6d53a4f1…`). For each row, re-derive the value BY HAND from the cited
theorem *against the canonical task as written*, and triage: **cosmetic** (fix and log) / **material**
(dated correction through the artifacts) / **invalidating** (claim leaves the preprint until resolved).

> **Two worksheet defects repaired 2026-07-24.** Citations were truncated at ~70 characters — useless for
> hand-verification — and are now full (longest is 142). One drawn cell, `random-3sat-refutation` /
> `landscape`, has **no citation**: it is `status: measured`, this program's own experiment, carrying an
> `experiment` provenance block instead. It is the only uncited real-value cell in the frozen 118, and it
> is correctly formed. The draw therefore filtered on *has a real value*, not *has a citation*. That row
> is checked against the experiment record, not a theorem — marked ⚑ below.

## decision

| problem_id | value | canonical task | citation | hand-verified? |
|---|---|---|---|---|
| `one-in-three-sat` | `NPC` | 1-in-3-SAT decision | Schaefer, The complexity of satisfiability problems, STOC 1978 |  |
| `stable-matching` | `P` | a stable matching always exists and is found by Gale-Shapley (poly-time) | Gale & Shapley, College admissions and the stability of marriage, Amer. Math. Monthly 69 (1962) |  |
| `planar-3-coloring` | `NPC` | planar 3-coloring is NP-complete | Garey, Johnson & Stockmeyer, Some simplified NP-complete graph problems, TCS 1 (1976) [planar 3-coloring] |  |
| `sat-2` | `P` | 2-SAT decision (NL-complete, in P) | Aspvall, Plass & Tarjan, A linear-time algorithm for testing certain QBFs (2-SAT), IPL 8 (1979) |  |
| `group-steiner-tree` | `NPC` | Group Steiner Tree decision | Karp, Reducibility among combinatorial problems (1972) |  |
| `directed-feedback-vertex-set` | `NPC` | directed FVS decision | Karp, Reducibility among combinatorial problems (1972) |  |
| `tautology` | `coNP-complete` | TAUT is coNP-complete -- a SIBLING of NPC, not above it (NP vs coNP open) | Arora & Barak, Computational Complexity: A Modern Approach (2009) |  |
| `steiner-tree` | `NPC` | STEINER-TREE decision | Karp, Reducibility among combinatorial problems (1972) |  |
| `max-directed-cut` | `NPC` | Maximum Directed Cut decision | Karp, Reducibility among combinatorial problems (1972) |  |
| `max-2lin` | `NPC` | MAX-2LIN gap decision | Garey & Johnson, Computers and Intractability (1979) |  |

## counting

| problem_id | value | canonical task | citation | hand-verified? |
|---|---|---|---|---|
| `number-partitioning` | `#P-complete` | #balanced partitions | Valiant, The complexity of enumeration and reliability problems, SIAM J. Comput. 8 (1979) 410-421 |  |
| `longest-path` | `#P-complete` | #long paths | Valiant, The complexity of enumeration and reliability problems, SIAM J. Comput. 8 (1979) 410-421 |  |
| `sat-3` | `#P-complete` | #3-SAT | Creignou & Hermann, Complexity of generalized satisfiability counting problems, Inf. Comput. 125 (1996) |  |
| `knapsack` | `#P-complete` | #knapsack solutions | Dyer, Approximate counting by dynamic programming [#knapsack FPRAS], STOC 2003 |  |
| `weighted-interval-scheduling` | `FP` | #optimal selections computable in poly time (DP) | Arora & Barak, Computational Complexity: A Modern Approach (2009) |  |
| `bipartiteness` | `FP` | #2-colorings = 2^(#connected components) if bipartite, else 0 | Arora & Barak, Computational Complexity: A Modern Approach (2009) |  |
| `subset-sum` | `#P-complete` | #subsets hitting the target | Valiant, The complexity of enumeration and reliability problems, SIAM J. Comput. 8 (1979) 410-421 |  |
| `tutte-polynomial` | `#P-complete` | evaluating the Tutte polynomial (most points) is #P-hard | Jaeger, Vertigan & Welsh, Computational complexity of the Jones and Tutte polynomials, Math. Proc. Camb. Phil. Soc. 108 (1990) |  |
| `determinant` | `FP` | evaluate the determinant (in FP / GapL) | Arora & Barak, Computational Complexity: A Modern Approach (2009) |  |
| `permanent` | `#P-complete` | compute the permanent (= count perfect matchings) | Valiant, The complexity of computing the permanent, TCS 8 (1979) 189-201 |  |

## approximation

| problem_id | value | canonical task | citation | hand-verified? |
|---|---|---|---|---|
| `set-cover` | `log-APX` | MIN-SET-COVER: (1-o(1)) ln n tight | Feige, A threshold of ln n for approximating set cover, JACM 45 (1998) 634-652 |  |
| `planar-vertex-cover` | `PTAS` | planar VC: PTAS (Baker's technique) | Baker, Approximation algorithms for NP-complete problems on planar graphs, JACM 41 (1994) [planar PTAS] |  |
| `k-set-packing` | `APX-complete` | MAX-k-SET-PACKING: constant-factor + APX-hard (for fixed k) | Ausiello, Crescenzi, Gambosi, Kann, Marchetti-Spaccamela & Protasi, Complexity and Approximation (1999) |  |
| `kemeny-rank-aggregation` | `PTAS` | Kemeny consensus: PTAS (Kenyon-Mathieu-Schudy) | Kenyon-Mathieu & Schudy, How to rank with few errors, STOC 2007 [feedback-arc / Kemeny PTAS] |  |
| `bin-packing` | `APX` | bin-packing: 3/2 ABSOLUTE-ratio hardness (from PARTITION) but an asymptotic FPTAS (AFPTAS); APX membership, not completeness (R19) | Karmarkar & Karp, An efficient approximation scheme for one-dimensional bin-packing, FOCS 1982 [AFPTAS] |  |
| `hitting-set` | `log-APX` | MIN-HITTING-SET: ln n greedy + hardness (set-cover dual) | Feige, A threshold of ln n for approximating set cover, JACM 45 (1998) 634-652 |  |
| `knapsack` | `FPTAS` | MAX-KNAPSACK: FPTAS | Ibarra & Kim, Fast approximation algorithms for the knapsack..., JACM 22 (1975) 463-468 |  |
| `dominating-set` | `log-APX` | MIN-DOMINATING-SET: ln n greedy + (1-o(1)) ln n hardness (set-cover equivalent) | Feige, A threshold of ln n for approximating set cover, JACM 45 (1998) 634-652 |  |
| `edge-coloring` | `APX` | edge-coloring: constant-factor (Vizing's Delta+1 <= 4/3 Delta) but NP-hard to beat 4/3 on cubic graphs (Holyer) | Vizing, On an estimate of the chromatic class of a p-graph (1964) [Delta+1 edge-coloring] |  |
| `longest-path` | `poly-APX` | MAX-LONGEST-PATH: no constant-factor approx (n^(1-eps) hard); poly-factor approximable | Karger, Motwani & Ramkumar, On approximating the longest path in a graph, Algorithmica 18 (1997) |  |

## parameterized

| problem_id | value | canonical task | citation | hand-verified? |
|---|---|---|---|---|
| `maximum-common-subgraph` | `W[1]` | W[1]-hard (contains subgraph isomorphism by pattern size) | Downey & Fellows, Fixed-parameter tractability and completeness II (W[1]), TCS 141 (1995) |  |
| `set-cover` | `W[2]+` | k-SET-COVER: W[2]-complete | Downey & Fellows, Parameterized Complexity (1999) |  |
| `integer-programming` | `FPT` | ILP is FPT in the number of variables (Lenstra) | H.W. Lenstra Jr., Integer programming with a fixed number of variables, Math. Oper. Res. 8 (1983) |  |
| `prize-collecting-steiner-tree` | `FPT` | FPT in number of terminals | Cygan et al., Parameterized Algorithms (2015) |  |
| `max-cut` | `FPT` | MAX-CUT above the m/2 guarantee: FPT | Cygan et al., Parameterized Algorithms (2015) |  |
| `tsp` | `FPT` | TSP parameterized by treewidth | Cygan et al., Parameterized Algorithms (2015) |  |
| `kemeny-rank-aggregation` | `FPT` | FPT in the optimal Kemeny score | Cygan et al., Parameterized Algorithms (2015) |  |
| `cluster-editing` | `FPT` | cluster editing is FPT in the edit budget | Gramm, Guo, Huffner & Niedermeier, FPT algorithms for cluster editing, Theory Comput. Syst. 38 (2005) |  |
| `vertex-cover` | `FPT` | VC parameterized by solution size k | Downey & Fellows, Parameterized Complexity (1999) |  |
| `induced-subgraph-isomorphism` | `W[1]` | W[1]-hard in pattern size (contains k-CLIQUE) | Downey & Fellows, Fixed-parameter tractability and completeness II (W[1]), TCS 141 (1995) |  |

## parallelization

| problem_id | value | canonical task | citation | hand-verified? |
|---|---|---|---|---|
| `circuit-value-problem` | `P-complete` | CVP is the canonical P-complete problem | Ladner, The circuit value problem is log-space complete for P, SIGACT News 7 (1975) |  |
| `bipartiteness` | `NC` | 2-coloring / connectivity in NC (in fact SL=L) | Arora & Barak, Computational Complexity: A Modern Approach (2009) |  |
| `min-spanning-tree` | `NC` | MST in NC (Boruvka-style parallel contraction) | Arora & Barak, Computational Complexity: A Modern Approach (2009) |  |
| `max-flow` | `P-complete` | MAX-FLOW is P-complete | Goldschlager, Shaw & Staples, The maximum flow problem is log-space complete for P, TCS 21 (1982) |  |
| `monotone-circuit-value` | `P-complete` | monotone CVP is P-complete | Greenlaw, Hoover & Ruzzo, Limits to Parallel Computation (1995) |  |
| `sat-2` | `NC` | 2-SAT is NL-complete, and NL subset of NC^2 | Arora & Barak, Computational Complexity: A Modern Approach (2009) |  |
| `xor-sat` | `NC` | linear algebra over GF(2) in NC^2 | Borodin, von zur Gathen & Hopcroft, Fast parallel matrix and GCD computations, Inf. Control 52 (1982) |  |
| `reachability-stcon` | `NC` | STCON is NL-complete and NL subset of NC^2 | Arora & Barak, Computational Complexity: A Modern Approach (2009) |  |
| `all-pairs-shortest-path` | `NC` | APSP via O(log n) rounds of min-plus (tropical) matrix squaring | Arora & Barak, Computational Complexity: A Modern Approach (2009) |  |
| `planarity` | `NC` | planarity testing is in NC (AC^1) | Arora & Barak, Computational Complexity: A Modern Approach (2009) |  |

## proof_size

| problem_id | value | canonical task | citation | hand-verified? |
|---|---|---|---|---|
| `tautology` | `exp` | the canonical proof-complexity object; hard tautologies (PHP/Tseitin) are Resolution-exponential | Haken, The intractability of resolution, TCS 39 (1985) 297-308 |  |
| `sat-3` | `exp` | random unsat 3-SAT Resolution refutation size | Chvatal & Szemeredi, Many hard examples for resolution, JACM 35 (1988) 759-768 |  |
| `tseitin` | `exp` | Tseitin on bounded-degree expanders: Resolution size 2^Omega(n) | Urquhart, Hard examples for resolution, JACM 34 (1987) 209-219 |  |
| `sat-2` | `poly` | 2-UNSAT: poly Resolution refutation via the implication graph | Aspvall, Plass & Tarjan, A linear-time algorithm for testing certain QBFs (2-SAT), IPL 8 (1979) |  |
| `random-3sat-refutation` | `exp` | random unsat 3-SAT Resolution refutation size: exponential | Chvatal & Szemeredi, Many hard examples for resolution, JACM 35 (1988) 759-768 |  |
| `tqbf` | `exp` | false-QBF refutation in Q-resolution: exp lower bounds | Beyersdorff, Chew & Janota, Proof complexity of resolution-based QBF calculi, STACS 2015 |  |
| `xor-sat` | `exp` | Tseitin/XOR formulas on expanders: Resolution size 2^Omega(n) | Urquhart, Hard examples for resolution, JACM 34 (1987) 209-219 |  |
| `horn-sat` | `poly` | Horn-UNSAT: poly unit-resolution refutation | Dowling & Gallier, Linear-time algorithms for testing satisfiability of Horn formulae, J. Logic Prog. 1 (1984) |  |
| `sat` | `exp` | hardest unsat CNF families (PHP/Tseitin) refuted in Resolution | Haken, The intractability of resolution, TCS 39 (1985) 297-308 |  |
| `php` | `exp` | PHP^{n+1}_n Resolution refutation: 2^Omega(n) lower bound | Haken, The intractability of resolution, TCS 39 (1985) 297-308 |  |

## average_case

| problem_id | value | canonical task | citation | hand-verified? |
|---|---|---|---|---|
| `sat-3` | `hard-on-average-conjectured` | random 3-SAT near threshold: conjectured hard in the clustered regime | Achlioptas & Coja-Oghlan, Algorithmic barriers from phase transitions, FOCS 2008 |  |
| `tsp` | `easy-on-average` | random Euclidean TSP: BHH concentration; PTAS (Arora) | Beardwood, Halton & Hammersley, The shortest path through many points, Proc. Camb. Phil. Soc. 55 (1959) |  |
| `sis` | `hard-on-average-provable` | average-case SIS is provably hard from worst-case approx lattice problems (Ajtai) | Ajtai, Generating hard instances of lattice problems, STOC 1996 [worst-case to average-case] |  |
| `matching` | `easy-on-average` | maximum matching on sparse random graphs: Karp-Sipser greedy near-optimal | Karp & Sipser, Maximum matchings in sparse random graphs, FOCS 1981 |  |
| `primality` | `easy-on-average` | primality is in P, hence easy on average | Agrawal, Kayal & Saxena, PRIMES is in P, Ann. of Math. 160 (2004) |  |
| `graph-isomorphism` | `easy-on-average` | random graphs G(n,1/2) canonizable in linear expected time | Babai, Erdos & Selkow, Random graph isomorphism, SIAM J. Comput. 9 (1980) |  |
| `hamiltonian-cycle` | `easy-on-average` | Hamilton cycles found a.a.s. at the Komlos-Szemeredi threshold | Bollobas, Fenner & Frieze, An algorithm for finding Hamilton paths and cycles in random graphs, Combinatorica 7 (1987) |  |
| `xor-sat` | `easy-on-average` | random k-XORSAT: in P (Gaussian elimination), easy on average | Dubois & Mandler, The 3-XORSAT threshold, FOCS 2002 |  |
| `lwe` | `hard-on-average-provable` | average-case LWE provably hard from worst-case lattice problems (Regev) | Regev, On lattices, learning with errors, random linear codes, and cryptography, JACM 56 (2009) |  |
| `factoring` | `hard-on-average-crypto` | random RSA semiprimes: factoring assumption | Rivest, Shamir & Adleman, A method for obtaining digital signatures..., CACM 21 (1978) [factoring assumption] |  |

## landscape

| problem_id | value | canonical task | citation | hand-verified? |
|---|---|---|---|---|
| `nae-sat` | `clustering-physics` | random NAE-SAT solution space: clustering (cavity; symmetric CSP) | Achlioptas & Moore, Random k-SAT: two moments suffice to cross a sharp threshold, SIAM J. Comput. 36 (2006) [NAE-SAT] |  |
| `graph-3-coloring` | `clustering-physics` | random graph colorings: clustering/freezing (cavity/replica, Zdeborova-Krzakala) | Krzakala, Montanari, Ricci-Tersenghi, Semerjian & Zdeborova, Gibbs states and the set of solutions of random CSPs, PNAS 104 (2007) |  |
| `vertex-cover` | `clustering-proven` | max-independent-set (VC complement) on sparse G(n,c/n): OGP (rigorous, via IS complementation) | Gamarnik & Sudan, Limits of local algorithms over sparse random graphs, ITCS 2014 |  |
| `sat-3` | `clustering-physics` | random 3-SAT solution space: clustering/condensation near threshold (cavity/replica prediction) | Mezard, Mora & Zecchina, Clustering of solutions in the random satisfiability problem, PRL 94 (2005) |  |
| `random-3sat-refutation` ⚑ | `freezing-measured` | refutation-SET backbone/freezing of random unsat 3-SAT near threshold (proof-space landscape; R1: proofs, not solutions) | **experiment record** — `proof-census` prereg_v1 / c2_summary.json / uofa-lab@55c7df5 |  |
| `number-partitioning` | `clustering-proven` | random number partitioning: OGP / algorithmic obstruction (rigorous) | Gamarnik & Kizildag, Algorithmic obstructions in the random number partitioning problem, Ann. Appl. Probab. 33 (2023) |  |
| `xor-sat` | `clustering-proven` | random k-XORSAT solution space: frozen 1RSB clusters (rigorous) | Ibrahimi, Kanoria, Kraning & Montanari, The set of solutions of random XORSAT formulae, Ann. Appl. Probab. 25 (2015) |  |
| `max-cut` | `clustering-proven` | max-cut on random graphs: OGP (rigorous, spin-glass line) | Chen, Gamarnik, Panchenko & Rahman, Suboptimality of local algorithms for a class of max-cut problems, Ann. Probab. 47 (2019) [spin-glass OGP] |  |
| `independent-set` | `clustering-proven` | max-independent-set on sparse random graphs: OGP (rigorous, Gamarnik-Sudan) | Gamarnik & Sudan, Limits of local algorithms over sparse random graphs, ITCS 2014 |  |
| `clique` | `clustering-proven` | planted-clique landscape: dense-subgraph overlap-gap property (rigorous) | Gamarnik & Zadik, The landscape of the planted clique problem: dense subgraphs and the overlap gap property (2019) |  |
