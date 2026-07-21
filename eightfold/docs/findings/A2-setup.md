# A2 setup — R11–R16 applied (23 problems, 86.4% cited)

**Verdict:** The six post-A1 refinements are applied and the atlas is A2-ready. Coverage rose to **86.4%**
(102/118 applicable cells) at 23 problems, zero uncited-folklore; the `n.a.`/`open` boundary is pinned and the
schema + analysis method are locked in `prereg_v3.json` **before** any A2 analysis. Remaining A2 work is the
expansion to ~120 problems.

## What each item did

- **R11 (prereg-gated method).** The pilot lesson — plain 8-charge Hamming washes out single-charge
  decouplings — is fixed by **subspace clustering** (`structure.cluster_subspaces`) and locked in
  `prereg_v3.json` (labeled *pilot-informed*). Confirmed: permanent/determinant and VC/CLIQUE decouplings are
  **amplified** in their carrying triples (Hamming 0.375 → 0.667) though full-vector clustering merges them.
- **R12 (approx|param bridges).** EPTAS ⟹ FPT (Cesati–Trevisan) and W[1]-hardness ⟹ no-EPTAS (Marx) added as
  informational entailment rules. The raw approximation|parameterized association (Cramér's V ≈ 0.66) is now
  reported as *partly theorem-forced*; only the residual is H2-grade (A3 computes it).
- **R13 (no borrowed cells).** **number-partitioning** is now its own row (a REM-like-landscape witness in its
  own right); knapsack/landscape reverted to `open`, and knapsack/average-case recoded `easy-on-average`
  (Beier–Vöcking, knapsack-specific) instead of the borrowed Mertens number-partitioning cite.
- **R14 (strictest standard for our datum).** The Census cell is **`freezing-measured`** (a new value), not
  `clustering-OGP-known`. Novelty recorded (I3): no OGP theorem exists for proof space.
- **R15 (`n.a.`/`open` pinned).** Full-atlas sweep: matching/average-case → `easy-on-average` (Karp–Sipser);
  horn-sat/landscape → `open` (Istrate); determinant / tqbf average-case → `open`. `n.a.` now marks only
  genuinely inapplicable charges — average-case `n.a.` dropped 5 → 2.
- **R16 (new average_case values).** `worst-case-to-average-equiv` (permanent, via Lipton 1991 random
  self-reducibility) and `hard-on-average-conjectured` (planted clique, for clique/IS).
- **R17 (average_case split).** `value` is now *algorithmic difficulty only*; the ensemble fact "a phase
  transition is known" moved to a separate boolean `transition_known` sub-field (11 cells carry it). Mixing
  the two statement types in one value manufactured sociology-driven associations. Schema clarification (not a
  prediction change), noted in `prereg_v3` coding scheme; `transition_known` enters A3 as its own binary
  feature.

Ordinary fills (no schema change): knapsack/parameterized → W[1] (k-subset-sum, Downey–Fellows);
vertex-cover/average-case → `transition-known` (Weigt–Hartmann 2000); horn-sat/approximation → APX-complete
(MAX-CSP dichotomy, Khanna–Sudan–Trevisan–Williamson; UGC-tight Guruswami–Zhou).

## Owner promotion pass (R8), reordered by review findings

1. **`sat-3`/landscape first** — a `contested_note` now flags that rigorous OGP is large-k while the k=3 story
   is physics-grade (Mézard–Mora–Zecchina); verify the citation supports OGP at k=3, or keep the caveat.
   (`graph-3-coloring`/landscape carries the same physics-grade note for a later rigor audit.)
2. The corrected **Census cell** (`freezing-measured`) once R14 is reviewed.
3. Witness rows as originally planned (VC/CLIQUE, permanent/determinant, 2-SAT/XOR-SAT, PHP).

## Remaining for A2

Expand 23 → ~120 problems at the same standard, with a per-charge coverage report; then A3 (structure analysis
under `prereg_v3`) is the H1–H3 verdict. The `n.a.`/`open` sweep rule (R15) and the no-borrowed-cells rule
(R13) apply to every new row.
