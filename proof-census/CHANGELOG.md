# Changelog — proof-census

## 0.1.0 (unreleased)

- Phase 0: scaffold the product (pyproject depending on the frozen `desert-map`, README, AGENTS.md
  invariants, `.gitignore`), commit the v1 spec, record I1–I3 investigation (both samplers self-implemented;
  S2 = DPLL→tree-resolution, no drat2er; canonical clause identity; novel vs Sidorov 2024 / MUS counting).
- **C1 done-gate MET:** `refutation.py` (canonical clause identity), `sampler_s1.py` (constructive
  saturation + provenance + sub-DAG extraction), `sampler_s2.py` (randomized DPLL → tree-resolution with
  unit-propagation regression, R3), `sample.py` (K-sampling driver, three-way accounting), `controls.py`
  (planted-core backbone calibration + glitch), `metrics.py`, `cli.py`. 200/200 verified per instance for
  both samplers on n=20 (0 discard, 0 budget); planted-core backbone at frequency 1.0 (both samplers).
  **H1 supported early:** median pairwise Jaccard 0.10 (S1) / 0.16 (S2), far below the 0.95 no-plurality
  kill line. **Province separation (R1):** S2 tree proofs ~9× longer than S1 DAG proofs (median 138 vs 17),
  backbone 19 vs 1. 19 tests green.
- C2 scaffolded: `plots.py` (one figure per §3.3 row), `results/prereg/prereg_v1.json` (predictions locked
  before the sweep). CI leg added (proof-census + desert-map co-install, torch-free).
- **S1 throughput:** the win is process parallelism over independent samples (`sweep.py`
  `sample_k_parallel`), not algorithmic — sampled/undirected or literal-index variants explored more before
  closing and were *slower*; the directed smallest-resolvent loop stays. ~4× on 10 cores at the default
  batch (K=200 n=20: 70s → ~18s), tuned toward ~need-per-wave. Full C3 sweep ≈ a few hours unattended,
  within the $20 / 12 h box. 20 tests green.
- **C2 done-gate MET** (`c2.py`, `sweep.py`): n=20 α-mini-sweep (3 instances/cell, K=80), S1-vs-S1 glitch
  bounds, 6 figures (length/P(q)/backbone per sampler + province). **Backbone strengthens** and **overlap
  concentrates** toward threshold in BOTH samplers (trend agreement, far above the glitch noise floor:
  backbone gap 0, Jaccard gap ≤0.011) — a real geometry finding. **Length lengthens in S2 only** →
  correctly flagged a sampler artifact per H3/R1. Province separation grows toward threshold (0.05→0.11).
  Neither kill criterion fires. Findings: `docs/findings/C2-mini-sweep.md`. Fixed an α-orientation sign bug
  in the trend/plot helpers (hard = low α = left). 20 tests green.
- Remaining: **C3** full parallel sweep (all n, 50 instances/cell, K=200) + the firm H1–H3 verdict.
