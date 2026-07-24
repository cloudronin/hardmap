# Mosaic L0 — two memory-cite roster defects, corrected by the frozen coordinates

**Date:** 2026-07-24. Recorded spec-side at the owner's direction, before prereg_v10 seals. Both are the
**instance-9 shape** — a value held from memory and consumed as ground truth without checking it against
the artifact that defines it. The frozen charge coordinates are that artifact; the sealed off-diagonal
cell-pattern query (prereg_v10 P5) is the correction.

## Defect 1 — the S5 violator roster was a memory-cite

The Mosaic spec named prediction 5's violator set as `capacitated-vertex-cover, k-means, densest-k-subgraph,
group-steiner-tree`. Checked against code:
- Only **`k-means`** is a hardcoded S5 violator (`crucible._s5_violators`).
- **`group-steiner-tree`** is on the *frozen-audited* violator list (`existing_violators_audited_in_frozen`
  = knapsack, subset-sum, partial-vertex-cover, graph-3-coloring, tsp, longest-path, group-steiner-tree) —
  a roster of **audit-touched** rows, not gradient-benders. Audit-touched ≠ gradient-bending; conflating
  the two rosters is exactly the field-consumed-as-ground-truth failure.
- **`capacitated-vertex-cover`** and **`densest-k-subgraph`** appear in no S5 roster at all (only as
  objective-type tags in `build_strata.py`).

**Correction:** stop reconciling to any remembered or repurposed roster. Prediction 5's known-answer set is
derived **mechanically from the frozen (approximation, parameterized) coordinates** — off-diagonal
residence *is* gradient-bending, by definition, no roster required. The query yields
`{subset-sum, graph-3-coloring, group-steiner-tree, longest-path, tsp}` (5 non-anchor off-diagonal rows).
It recovers the genuinely off-diagonal members of the audited list and correctly drops the rest — the query
corrects the memory-cite.

## Defect 2 — `knapsack` was a memory-cite too, and the load-bearing one

The pred-5 reasoning that exposed defect 1 rested on "knapsack is FPTAS × FPT, the on-diagonal easy
corner." The frozen coordinates say **`FPTAS × W[1]`** — *off-diagonal* (approximation-easy × W-hard). Left
uncorrected, the off-diagonal query would have selected knapsack as a delocalized/mixed violator (P5) while
prediction 1 requires it to code `decomposable` — the prereg would contradict itself, the very failure the
mechanical query was adopted to avoid.

**Correction, and it is a gift:** knapsack is excluded from P5 (anchors are reserved instrument checks) and
promoted to **the exemplar of the dissociation set** — maximally decomposable by structure (1-D DP is the
FPTAS's own scaffold) yet W-hard on the standard parameter. It is the first concrete evidence that locality
feeds the two gradient charges through **two partially independent structural properties** (decomposition-
locality → schemes; certificate-locality → branching), which is now a named secondary observation in the
seal (prereg_v10 §two_property_split). A memory-cite, checked against the artifact, became the sharpest
test in the design.

## The general rule (already the methods thread's, applied to a fresh spec)

A roster or coordinate held from memory is a citation without a Check-9 gate. The frozen atlas is the gate;
query it before sealing a prediction on it. Both defects were caught at L0, before coding — the self-catch
latency the methods thread has been tracking, holding.
