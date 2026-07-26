# Arm A — the algebra is not surface-recoverable: surfaces see membership, not closure

**Date:** 2026-07-25. Mosaic v3 G2, prereg_v12 A1/A2 + the G2 amendment. Population: 4072 arity-≤4 Boolean
symmetry classes. Model: depth-≤6 CART, 5 grouped folds on the 46 poly-fingerprint groups, seed 20260725.
Predictions hashed before scoring. Nothing rescores.

## The answer

> **No. Surface combinatorics do not recover the algebra. Surfaces see what a problem *contains*; they do
> not see what it is *closed under* — and hardness lives in the closure.**

| closure property | recovery | fold-weighted null | lift |
|---|---|---|---|
| dualhorn | 0.728 | 0.899 | **−0.171** |
| general_wsep | 0.767 | 0.929 | **−0.162** |
| IHSB | 0.782 | 0.922 | **−0.141** |
| horn | 0.812 | 0.899 | **−0.087** |
| bijunctive | 0.844 | 0.911 | **−0.067** |
| affine | 0.991 | 0.981 | +0.010 |
| width2affine | 0.995 | 0.984 | +0.011 |
| strongly0valid | 0.998 | 0.954 | +0.044 |

Every genuine closure property sits **at or below** its achievable baseline. The three nominal positives
rest on nulls of 0.95–0.98, so their lifts are noise. Joint headline: Hamming **0.831 vs 0.744**;
exact-profile **0.217 vs 0.219** — *at* the null. Ceiling, stated in advance: 1.00.

## The positive control is what makes this a finding rather than a null

`0valid` and `1valid` recover at **0.983 / 1.000**. They are *membership of one specific tuple* — not
closure properties. So the same pipeline, the same features, the same folds **learn membership essentially
perfectly and closure not at all.**

That is the difference between "the fit is broken" and "there is a type boundary here." **It is a type
boundary.**

## How we know the split is forced, not chosen — three acts

1. **An arithmetic leak.** The first design excluded the weight-histogram's `w0`/`w_arity` bins because those
   *are* 0valid/1valid. But `weight_mean × n_tuples = S(strict bins) + arity × w_arity` reconstructs them
   **exactly on 4070/4070 rows**. Excluding the bins did not exclude the information.
2. **A semantic channel.** Dropping `weight_mean` and `weight_spread` did not close it — `1valid` still
   recovered at exactly 1.0000. The channel runs through *order structure*: if all-ones ∈ R it is the unique
   maximum, so `n_maximal_tuples` collapses to 1 (98.5% concordance; symmetric for all-zeros). **Any faithful
   description of a tuple-set sees single-tuple membership.** No honest surface feature set can blind itself
   to it.
3. **Reclassification, not more cutting.** Deleting features until a genuinely surface-visible fact became
   invisible would manufacture blindness to preserve a mis-drawn line. The category error was named *before*
   these numbers existed, the mechanism forces it, and the verdict is unchanged either way — so it is typing,
   not negotiation. Sealed as the G2 amendment.

*Guard applied:* nulls are **fold-weighted** (train-fold mode → test fold), the achievable baseline. This
moved exact-profile from below-null to at-null — the earlier "actively below" reading was partly leak
artifact, and it died before it was narrated. The closure negatives survive fold-weighting because their
nulls are ~90/10 imbalanced and barely move.

## What this calibrates for Arm B — and it is load-bearing

**If closure structure leaves no surface fingerprint on the Boolean side, then Arm B's natural-side
prediction cannot be routing through hidden algebra-recovery.** Whatever accuracy Arm B achieves comes from
something else — citation-era regularities, problem-family structure, or the genuine bridge.

That sharpens what a hit there would mean, and it is the Boolean arm's real contribution: **it did not test
the bridge (it cannot — there the bridge is a theorem), but it calibrated the interpretation of the arm that
does.**

## Ceiling and honest limits

- The 100% ceiling is a property of the population (the profile is a deterministic function of the flags),
  stated before the fit, never a result.
- One model family (shallow CART) at one depth. A richer model could raise absolute accuracy; it could not
  make a closure property visible in features that provably do not encode it.
- The error geography by boundary distance is reported in `grid_arm_a_results_clean.json`; exact-profile is
  0.290 at distance 1 and 0.030 at distance 2, and that inversion is **not** interpreted here — it is
  recorded for the frontier map, which is where it belongs.
