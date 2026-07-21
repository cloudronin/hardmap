# Finding: the counting-#P-completeness folklore gap

**Status:** measured in the A2 F-1 audit; **A4 headline finding** (prereg_v5, Rider 2). The atlas was built to
surface exactly this kind of thing — and the first instance it found is in its own audit trail.

## Claim

For natural NP-hard problems, the community treats *"the counting version is #P-complete"* as the default
assumption. Yet across the 118-problem atlas, that #P-completeness has a **published, per-problem** proof for
only ~37 problems; for roughly two-thirds of the well-studied optimization/graph problems here, **no one has
published the counting-hardness result.** The gap is in the literature, not the atlas.

## How it was measured

The A2 curation helper (`_npc_opt`) auto-stamped `counting = #P-complete` on every NP-complete optimization
problem, with a *generic* "counting the solutions of an NP-complete problem is #P-complete (Arora–Barak
Ch.17)" citation — the seductive default. The 118-row review (F-1) flagged this as pattern-matching, and an
R20 Check-9 audit over the whole column asked, per cell: *does a specific published result establish
#P-hardness for THIS problem?* Result:

- **37 cited** (specific citation): the classic canon — Valiant 1979 (independent sets, vertex covers,
  cliques, Hamiltonian cycles, matchings, #SAT), Creignou–Hermann (the SAT counting dichotomy), Provan–Ball
  (cuts/reliability), Linial (colorings), Jaeger–Vertigan–Welsh (Tutte), Dyer (knapsack), Irving–Leather
  (stable matchings), Kasteleyn/FKT + Kirchhoff (planar matchings, spanning trees — FP), Vadhan 2001 (planar
  VC/IS).
- **~49 open**: web-verification (two searches) confirmed the counting-hardness of these specific problems is
  **not published** — the literature proves their NP-completeness and parameterized complexity, but leaves
  the counting version as folklore.

Counting fell 97% → **43%** under the honest recoding. It was moved to the frontier tier (prereg_v5), where
its open-rate is a first-class deliverable rather than a gate failure.

## Why it is a finding, not a curation gap

No paper says "the number of minimum connected vertex covers / cluster edit sets / Kemeny rankings is
#P-complete." The result is *believed* (it follows the pattern, and a parsimonious reduction very likely
exists), but believed-and-unproven is precisely the atlas's target: each folklore-open cell is a falsifiable
gap-list entry — *"#{problem} is presumably #P-complete; no published proof is known."*

## The 37 established (counting is genuine here)

Every **decision-vs-counting decoupling witness** lives in this set, which is why A3 loses nothing: permanent
(#P-c) vs determinant (FP); 2-SAT / Horn-SAT / matching / reachability / stable-matching (decision-easy,
counting-hard); planar-matching-count (FP by FKT) as the structured foil. Full list: sat, sat-2, sat-3,
xor-sat (FP), horn-sat, nae-sat, one-in-three-sat, vertex-cover, clique, independent-set, dominating-set,
feedback-vertex-set, graph-3-coloring, hamiltonian-cycle, longest-path, tsp, metric-tsp, reachability-stcon,
three-dimensional-matching, exact-cover-x3c, circuit-sat, permanent, matching, determinant (FP),
min-spanning-tree (FP), planar-matching-count (FP), bipartiteness (FP), weighted-interval-scheduling (FP),
knapsack, subset-sum, number-partitioning, max-cut, network-reliability, tutte-polynomial, stable-matching,
planar-vertex-cover, planar-independent-set.

## The ~49 folklore-open (the gap)

bin-covering, bin-packing, capacitated-vertex-cover, cluster-editing, cluster-vertex-deletion,
connected-vertex-cover, cutwidth, d-hitting-set, densest-k-subgraph, directed-feedback-vertex-set,
directed-steiner-tree, disjoint-paths, edge-coloring, edge-dominating-set, feedback-arc-set-tournament,
graph-motif, group-steiner-tree, hitting-set, induced-subgraph-isomorphism, integer-programming, job-shop,
k-center, k-median, k-set-packing, kemeny-rank-aggregation, makespan, max-2lin, max-coverage, max-directed-cut,
maximum-common-subgraph, maximum-leaf-spanning-tree, min-bisection, minimum-fill-in, multiway-cut,
odd-cycle-transversal, partial-vertex-cover, planar-3-coloring, planar-dominating-set,
prize-collecting-steiner-tree, quadratic-assignment, set-cover, shortest-common-superstring, steiner-forest,
steiner-tree, survivable-network-design, treedepth, treewidth.

**Two non-folklore exceptions** in that list, open for a *different* reason (kept honest): graph-isomorphism
and group-isomorphism — their counting versions are polynomial-time equivalent to the (NPI-candidate)
decision, so they are neither FP nor #P-hard under standard assumptions.

## Caveats

Some of the ~49 may have published results not recalled here; the honest coding is `open` (R20), and any that
gain a citation move to `#P-complete`. The claim is about the **density** of published results and is robust
to a handful of missed citations. The owner promotion pass (R8) will spot-check two of the 37 survivors
(checking-the-checker) to bound false-positives in the *kept* set — the set-cover/Provan–Ball mis-citation was
already caught this way.
