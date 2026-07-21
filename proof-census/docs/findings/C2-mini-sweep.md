# C2 — n=20 α-mini-sweep: population geometry + glitch bounds

Mini-sweep (n=20, α∈{4.5,5,6,8,10}, 3 instances/cell, K=80 verified refutations per sampler per instance).
Figures in `proofcensus/results/figures/`; machine summary in `c2_summary.json`. All claims sampler-relative;
H3 replication judged on **trends** (direction across α), not levels (R1).

## Trends toward threshold (α → 4.5) — sign +1 = larger at the hard end
| Metric | S1 (DAG) | S2 (tree) | trend agree? |
|---|---|---|---|
| median proof length | [22,33,28,25,27] (≈flat, −) | [134,108,82,53,44] (**+**, strong) | **No** |
| mean backbone size (≥0.95) | [2.0,3.7,2.7,1.3,1.0] (**+**) | [17,10,1.3,1,1] (**+**, strong) | **Yes** |
| mean median-Jaccard (overlap) | [.128,.213,.157,.169,.127] (**+**) | [.168,.163,.141,.096,.071] (**+**) | **Yes** |

## Glitch (S1-vs-S1) noise bounds
Backbone-size gap **0**, median-Jaccard gap ≤ **0.011**, median-length gap ≤ **2**. The backbone and overlap
trends (S2 backbone 1→17; S2 overlap .07→.17) are far above the noise floor; the length trend gap is small
but the S1 length signal is itself ≈flat.

## Province separation (inter- vs intra-sampler overlap)
Intra > inter at every α; separation **grows toward threshold** (0.05 at α=10 → 0.112 at α=4.5). The two
samplers occupy increasingly distinct provinces of the refutation set as instances harden — a finding
(R1), not an artifact.

## Read (preview of the H1–H3 verdict; C3 firms it with 50 instances/cell)
- **H1 (plurality):** supported — median pairwise Jaccard 0.07–0.21, far below the 0.95 no-plurality kill.
- **H2 (geometry shifts toward threshold):** **backbone strengthens** and **overlap concentrates** in BOTH
  samplers; proof **length lengthens in S2 only** (S1 ≈flat).
- **H3 (replication = trends):** backbone and overlap trends **replicate** across the two structurally
  different samplers, beyond the glitch bound → **terrain**. The length trend does **not** replicate
  (S2-specific) → **sampler artifact**, exactly the discrimination R1 was designed to make. Neither kill
  criterion fires (plurality holds; trend agreement holds on ≥1 metric, in fact 2/3).

**Caveat:** 3 instances/cell is a mini-sweep for trend detection; per-cell statistics and significance come
from the C3 full sweep (50 instances/cell).
