# C3 — full sweep + H1–H3 verdict

Full sweep: n∈{20,30,40,60} × α∈{4.5,5,6,8,10}, **50 instances/cell, K=200 verified refutations per sampler
per instance** (1000 instances, ~400k verified proofs). Checkpoint: `results/c3/checkpoint.jsonl`; aggregate:
`results/c3/c3_summary.json`; figures: `results/c3/c3_{mean_backbone,median_length,mean_jaccard}.png`. All
claims sampler-relative (S1 = constructive-saturation DAG, S2 = DPLL tree-resolution); H3 judged on **trends**
across α, not levels (R1).

## Verdict

**H1 (plurality) — CONFIRMED.** Median pairwise Jaccard 0.04–0.16 at every cell (both samplers) — far below
the 0.95 no-plurality kill line. The refutation set is plural everywhere.

**H2 (geometry shifts toward threshold) — CONFIRMED.**
- **Backbone strengthens toward threshold** (the headline), in both samplers at all four sizes. Mean
  backbone size (clause-ids in ≥95% of a cell's proofs) toward α=4.5:
  S2 — n20 1→15, n30 1→46, n40 1→126, **n60 1→273**; S1 — modest but monotone (≈1→1.5–2.6).
- **Proofs lengthen toward threshold**, both samplers, all sizes. S2 median length toward threshold:
  n20 43→130, n40 127→1070, **n60 315→6976** (22×). S1 length ≈flat (≈47 at n60) but still +1.
- **Overlap concentrates toward threshold** at n=20/30/40 (both samplers).

**H3 (replication = trends) — STRONGLY SUPPORTED.** Trend agreement in **11/12** (metric × size) cells:
length and backbone replicate (both +1) at every size; overlap replicates at n=20/30/40. The one divergence
— **n=60 overlap** (S1 +1, S2 −1) — is *mechanistically explained*, not artifact: near threshold at n=60,
S2 tree proofs are so large (~7000 clauses) that even a growing 273-clause backbone is a *shrinking
fraction* of the union, so pairwise Jaccard falls. That is the province-separation mechanism (tree vs DAG),
exactly what the R1 trend-not-level standard was designed to expose. **Neither kill criterion fires**
(plurality holds; trend agreement holds on ≥2/3 metrics at every size).

## Province separation (S1 DAG vs S2 tree)
The two samplers occupy very different provinces, and the gap grows with n and hardness: S2 tree proofs are
orders of magnitude longer and carry orders-of-magnitude larger backbones than S1 DAG proofs. This is a
*finding* (the refutation set is heterogeneous — different constructors reach different regions), not an
artifact — and it is why H3 must be read as trends, never levels.

## Coverage & robustness (honest caveats)
- **998/1000 instances fully covered** (S1 & S2 both reached K=200). **2 S1 instances** (n=60 α=5.0 and
  α=6.0) reached 49/50 — one instance each hit S1's max-attempts retry cap and returned <200; flagged in
  `c3_summary.json.coverage`, not hidden. S2 fully covered everywhere (the R2 n=60-hard fallback was never
  needed).
- **Budget caveat (methodological):** the S1 4000-resolution budget becomes binding at n=60 hard cells
  (budget-exceeded rate up to ~70%), so S1 there samples the subpopulation of refutations closeable within
  4000 resolutions. Consistent across all cells (same budget) — a documented filter, per AGENTS.md.
- **Run robustness:** the sweep survived a `BrokenProcessPool` (worker OOM) crash at instance 894; resumed
  from the checkpoint with zero data loss after adding an in-flight memory cap + self-healing executor
  recovery. Total wall-clock ≈ 44h + ~13h (resume).

## Bottom line
Proof Census delivers a positive, replicated empirical map of the refutation set: it is plural, and its
geometry — length, and especially a **proof backbone** — shifts systematically and strongly toward the
sat threshold, confirmed across two structurally different samplers and four sizes. The lone n=60-overlap
divergence is explained by tree-proof size explosion, not sampler noise.
