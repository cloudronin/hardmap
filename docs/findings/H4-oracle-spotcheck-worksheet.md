# H4 oracle spot-check -- worksheet (sealed draw)

Sealed seed **20260724**, 10 cited-filled classes per charge column, drawn from the frozen atlas (118 problems). For each row, re-derive the charge value BY HAND from the cited theorem and mark it. Cosmetic / material / invalidating per the H4 triage rule.

| charge | problem_id | value | citation | hand-verified? |
|---|---|---|---|---|
| decision | one-in-three-sat | NPC | Schaefer, The complexity of satisfiability problems, STOC 1978 | |
| decision | stable-matching | P | Gale & Shapley, College admissions and the stability of marriage, Amer | |
| decision | planar-3-coloring | NPC | Garey, Johnson & Stockmeyer, Some simplified NP-complete graph problem | |
| decision | sat-2 | P | Aspvall, Plass & Tarjan, A linear-time algorithm for testing certain Q | |
| decision | group-steiner-tree | NPC | Karp, Reducibility among combinatorial problems (1972) | |
| decision | directed-feedback-vertex-set | NPC | Karp, Reducibility among combinatorial problems (1972) | |
| decision | tautology | coNP-complete | Arora & Barak, Computational Complexity: A Modern Approach (2009) | |
| decision | steiner-tree | NPC | Karp, Reducibility among combinatorial problems (1972) | |
| decision | max-directed-cut | NPC | Karp, Reducibility among combinatorial problems (1972) | |
| decision | max-2lin | NPC | Garey & Johnson, Computers and Intractability (1979) | |
| counting | number-partitioning | #P-complete | Valiant, The complexity of enumeration and reliability problems, SIAM  | |
| counting | longest-path | #P-complete | Valiant, The complexity of enumeration and reliability problems, SIAM  | |
| counting | sat-3 | #P-complete | Creignou & Hermann, Complexity of generalized satisfiability counting  | |
| counting | knapsack | #P-complete | Dyer, Approximate counting by dynamic programming [#knapsack FPRAS], S | |
| counting | weighted-interval-scheduling | FP | Arora & Barak, Computational Complexity: A Modern Approach (2009) | |
| counting | bipartiteness | FP | Arora & Barak, Computational Complexity: A Modern Approach (2009) | |
| counting | subset-sum | #P-complete | Valiant, The complexity of enumeration and reliability problems, SIAM  | |
| counting | tutte-polynomial | #P-complete | Jaeger, Vertigan & Welsh, Computational complexity of the Jones and Tu | |
| counting | determinant | FP | Arora & Barak, Computational Complexity: A Modern Approach (2009) | |
| counting | permanent | #P-complete | Valiant, The complexity of computing the permanent, TCS 8 (1979) 189-2 | |
| approximation | set-cover | log-APX | Feige, A threshold of ln n for approximating set cover, JACM 45 (1998) | |
| approximation | planar-vertex-cover | PTAS | Baker, Approximation algorithms for NP-complete problems on planar gra | |
| approximation | k-set-packing | APX-complete | Ausiello, Crescenzi, Gambosi, Kann, Marchetti-Spaccamela & Protasi, Co | |
| approximation | kemeny-rank-aggregation | PTAS | Kenyon-Mathieu & Schudy, How to rank with few errors, STOC 2007 [feedb | |
| approximation | bin-packing | APX | Karmarkar & Karp, An efficient approximation scheme for one-dimensiona | |
| approximation | hitting-set | log-APX | Feige, A threshold of ln n for approximating set cover, JACM 45 (1998) | |
| approximation | knapsack | FPTAS | Ibarra & Kim, Fast approximation algorithms for the knapsack..., JACM  | |
| approximation | dominating-set | log-APX | Feige, A threshold of ln n for approximating set cover, JACM 45 (1998) | |
| approximation | edge-coloring | APX | Vizing, On an estimate of the chromatic class of a p-graph (1964) [Del | |
| approximation | longest-path | poly-APX | Karger, Motwani & Ramkumar, On approximating the longest path in a gra | |
| parameterized | maximum-common-subgraph | W[1] | Downey & Fellows, Fixed-parameter tractability and completeness II (W[ | |
| parameterized | set-cover | W[2]+ | Downey & Fellows, Parameterized Complexity (1999) | |
| parameterized | integer-programming | FPT | H.W. Lenstra Jr., Integer programming with a fixed number of variables | |
| parameterized | prize-collecting-steiner-tree | FPT | Cygan et al., Parameterized Algorithms (2015) | |
| parameterized | max-cut | FPT | Cygan et al., Parameterized Algorithms (2015) | |
| parameterized | tsp | FPT | Cygan et al., Parameterized Algorithms (2015) | |
| parameterized | kemeny-rank-aggregation | FPT | Cygan et al., Parameterized Algorithms (2015) | |
| parameterized | cluster-editing | FPT | Gramm, Guo, Huffner & Niedermeier, FPT algorithms for cluster editing, | |
| parameterized | vertex-cover | FPT | Downey & Fellows, Parameterized Complexity (1999) | |
| parameterized | induced-subgraph-isomorphism | W[1] | Downey & Fellows, Fixed-parameter tractability and completeness II (W[ | |
| parallelization | circuit-value-problem | P-complete | Ladner, The circuit value problem is log-space complete for P, SIGACT  | |
| parallelization | bipartiteness | NC | Arora & Barak, Computational Complexity: A Modern Approach (2009) | |
| parallelization | min-spanning-tree | NC | Arora & Barak, Computational Complexity: A Modern Approach (2009) | |
| parallelization | max-flow | P-complete | Goldschlager, Shaw & Staples, The maximum flow problem is log-space co | |
| parallelization | monotone-circuit-value | P-complete | Greenlaw, Hoover & Ruzzo, Limits to Parallel Computation (1995) | |
| parallelization | sat-2 | NC | Arora & Barak, Computational Complexity: A Modern Approach (2009) | |
| parallelization | xor-sat | NC | Borodin, von zur Gathen & Hopcroft, Fast parallel matrix and GCD compu | |
| parallelization | reachability-stcon | NC | Arora & Barak, Computational Complexity: A Modern Approach (2009) | |
| parallelization | all-pairs-shortest-path | NC | Arora & Barak, Computational Complexity: A Modern Approach (2009) | |
| parallelization | planarity | NC | Arora & Barak, Computational Complexity: A Modern Approach (2009) | |
| proof_size | tautology | exp | Haken, The intractability of resolution, TCS 39 (1985) 297-308 | |
| proof_size | sat-3 | exp | Chvatal & Szemeredi, Many hard examples for resolution, JACM 35 (1988) | |
| proof_size | tseitin | exp | Urquhart, Hard examples for resolution, JACM 34 (1987) 209-219 | |
| proof_size | sat-2 | poly | Aspvall, Plass & Tarjan, A linear-time algorithm for testing certain Q | |
| proof_size | random-3sat-refutation | exp | Chvatal & Szemeredi, Many hard examples for resolution, JACM 35 (1988) | |
| proof_size | tqbf | exp | Beyersdorff, Chew & Janota, Proof complexity of resolution-based QBF c | |
| proof_size | xor-sat | exp | Urquhart, Hard examples for resolution, JACM 34 (1987) 209-219 | |
| proof_size | horn-sat | poly | Dowling & Gallier, Linear-time algorithms for testing satisfiability o | |
| proof_size | sat | exp | Haken, The intractability of resolution, TCS 39 (1985) 297-308 | |
| proof_size | php | exp | Haken, The intractability of resolution, TCS 39 (1985) 297-308 | |
| average_case | sat-3 | hard-on-average-conjectured | Achlioptas & Coja-Oghlan, Algorithmic barriers from phase transitions, | |
| average_case | tsp | easy-on-average | Beardwood, Halton & Hammersley, The shortest path through many points, | |
| average_case | sis | hard-on-average-provable | Ajtai, Generating hard instances of lattice problems, STOC 1996 [worst | |
| average_case | matching | easy-on-average | Karp & Sipser, Maximum matchings in sparse random graphs, FOCS 1981 | |
| average_case | primality | easy-on-average | Agrawal, Kayal & Saxena, PRIMES is in P, Ann. of Math. 160 (2004) | |
| average_case | graph-isomorphism | easy-on-average | Babai, Erdos & Selkow, Random graph isomorphism, SIAM J. Comput. 9 (19 | |
| average_case | hamiltonian-cycle | easy-on-average | Bollobas, Fenner & Frieze, An algorithm for finding Hamilton paths and | |
| average_case | xor-sat | easy-on-average | Dubois & Mandler, The 3-XORSAT threshold, FOCS 2002 | |
| average_case | lwe | hard-on-average-provable | Regev, On lattices, learning with errors, random linear codes, and cry | |
| average_case | factoring | hard-on-average-crypto | Rivest, Shamir & Adleman, A method for obtaining digital signatures... | |
| landscape | nae-sat | clustering-physics | Achlioptas & Moore, Random k-SAT: two moments suffice to cross a sharp | |
| landscape | graph-3-coloring | clustering-physics | Krzakala, Montanari, Ricci-Tersenghi, Semerjian & Zdeborova, Gibbs sta | |
| landscape | vertex-cover | clustering-proven | Gamarnik & Sudan, Limits of local algorithms over sparse random graphs | |
| landscape | sat-3 | clustering-physics | Mezard, Mora & Zecchina, Clustering of solutions in the random satisfi | |
| landscape | random-3sat-refutation | freezing-measured |  | |
| landscape | number-partitioning | clustering-proven | Gamarnik & Kizildag, Algorithmic obstructions in the random number par | |
| landscape | xor-sat | clustering-proven | Ibrahimi, Kanoria, Kraning & Montanari, The set of solutions of random | |
| landscape | max-cut | clustering-proven | Chen, Gamarnik, Panchenko & Rahman, Suboptimality of local algorithms  | |
| landscape | independent-set | clustering-proven | Gamarnik & Sudan, Limits of local algorithms over sparse random graphs | |
| landscape | clique | clustering-proven | Gamarnik & Zadik, The landscape of the planted clique problem: dense s | |
