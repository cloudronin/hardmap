# Factors v1 — the effective dimensionality of the charge atlas, by held-out prediction

**Verdict: k\* = 1.** By the pre-registered held-out-prediction estimator, the post-Crucible canon atlas is
**effectively one-dimensional** — a latent class model with k ≥ 2 does **not** predict masked charge cells better
than the per-charge marginals; it predicts them *worse* (overfitting at n≈114). The on-file prediction
**k\* ∈ {3,4} MISSES.**

> Read through a marginal-robust instrument, the atlas's apparent multi-dimensionality does not survive. This is
> the quantitative successor to Crucible **S1**, which already RESIZED the MCA dimensionality claim as "explained
> by typing + marginals." Held-out prediction now supplies the positive estimate S1 implied: **k\* = 1.** The one
> structure that survived S1 — the approximation⟷parameterized gradient — is a real *local* pairwise association,
> not a *global* predictive dimension, and both readings coexist.

**Provenance.** Pre-registered in [`prereg_v7.json`](../../eightfold/results/prereg/prereg_v7.json)
(`committed_before_analysis: true`, locked at commit `fff8a32` **before** this run; sha `3184827e…`). Data:
[`atlas.jsonl`](../../eightfold/results/atlas/atlas.jsonl) (sha `6d53a4f1…`), dedup'd to the 114-class S2 roster
(`crucible._S2_DROP`). Full machine output:
[`factors_v1.json`](../../eightfold/results/atlas/factors_v1.json) (sha `55bf628a…`,
`python -m eightfold.factors --factors`). Additive to the frozen kernel — `a3_structure.json` (sha `9a5ec8e0…`)
regenerates byte-identical; no existing module was touched. The **F-1 selftest is green** (planted k=3 recovered
0.42→0.74→**0.95**; pure null quiet, k\*=1), so the estimator class is validated and the interval claim is
**not** deferred.

---

## Setup — what was locked, and the rule

| Element | Locked in prereg_v7 |
|---|---|
| Primary estimator | held-out masked-cell predictive **accuracy** of a k-latent-factor categorical model (LCM by EM), k=1..6 |
| Maskable set | **real-valued cells only** (open/unmeasured/n.a. marginalized, never imputed) |
| Selection rule | k\*_hat = **smallest k within 1 SE** of the best mean accuracy (parsimonious 1-SE); the **claim is the interval** |
| Model ladder | LCM first; escalate to low-rank categorical PCA **only if the selftest fails** (it passed — no escalation) |
| Disqualified | MCA eigenvalue counts — S1-inflated by marginals+typing; a reported sensitivity, never the claim |
| On-file prediction | k\* ∈ {3,4}; loadings ≈ core-intractability / structural-tamability / statistical-geometric (scored, not gated) |

## The k\* curve (dedup-114 primary; full prereg budget)

| k | mean held-out accuracy | ±1 SE | verdict |
|---|---|---|---|
| **1** | **0.6656** | 0.0161 | **best — the whole interval** |
| 2 | 0.6065 | 0.0150 | worse than k=1 by >1 SE |
| 3 | 0.6172 | 0.0154 | worse than k=1 by >1 SE |
| 4 | 0.6183 | 0.0151 | worse than k=1 by >1 SE |
| 5 | 0.6344 | 0.0143 | worse than k=1 by >1 SE |
| 6 | 0.6333 | 0.0143 | worse than k=1 by >1 SE |

**k\* interval = [1]** (k=1 wins decisively — every k ≥ 2 sits more than 1 SE *below* it). n=114 rows, **72
distinct charge profiles**. Adding latent classes strictly *worsens* held-out accuracy — the signature of
fitting structure that does not generalize.

## The on-file prediction is scored a MISS

k\* ∈ {3,4} is **not** in the interval [1] — a **MISS**, reported at size (prereg: scored, not gated). The F1
note's intuition of 3–4 nameable factors is not borne out by held-out prediction on the canon. Because k\*=1,
the "loadings" degenerate to the single global marginal profile — there are **no multiple factors to name**, so
the loadings half of the on-file prediction (P_loadings) is moot at v1. (The one class's modal profile — decision
NPC, counting #P-complete, parameterized FPT, proof_size exp, … — is just the atlas marginals; it is recorded in
`factors_v1.json` for completeness, not as a factor identity.)

## Ablations & robustness (R-fac1) — k\*=1 is stable

| Ablation | Result |
|---|---|
| **Leave-one-charge-out** (drop each of the 8) | k\*_hat = **1 for every drop** — no single charge carries the verdict |
| **--drop-measured** (R9) | k\*_hat = **1** — the verdict does not rest on the measured cells |
| **Raw-118 sensitivity** | k\*_hat = **1** (interval [1,4,5,6] — flatter on the raw roster, but k=1 still wins) |
| **Excess-over-null** (M=150 S1 nulls) | real acc-gain of k\* over k=1 = **0.0**, inside the null envelope → **no structure beyond typing** (degenerate once k\*=1: the primary already found none) |
| **MCA sensitivity (DISQUALIFIED)** | 16 dims — the S1-inflated count Factors was built to replace. **MCA 16 vs held-out prediction 1** is the headline contrast. |

## The secondary estimator (excess-over-null) — and the one thing that DOES beat a null

The prereg_v7 secondary places k\*'s predictive gain over k=1 against the S1 null envelope. **The number: real
gain = 0.000, inside the null envelope (one-sided p = 1.0).** At k\*=1 this is degenerate by construction (the
gain of k\* over k=1 is zero), so on its own it is uninformative — but the **low-rank v1.1 null-correction is the
non-degenerate version**, and it is unambiguous: **no rank beats the independence null** (every rank's held-out
gain sits inside the column-permutation envelope; k\*=0). So the apparent dimensional "compression" that MCA and
Crucible S1 surfaced **does not replicate as held-out predictive gain** — no latent dimension pays its way.

This does not contradict Crucible S1; it sharpens it. S1's surviving result was the **approx⟷parameterized
pairwise gradient**, a Cramér's V that *did* exceed its null, and it is still there. What Factors adds is that
**no k captures it**: a single pairwise coupling does not lift the *global* predictive dimensionality above the
marginals. The one-sentence synthesis — *the atlas's real structure is pairwise and local (the gradient), not a
global latent basis; the predictive-dimensionality excess-over-null is zero even though the pairwise
excess-over-null (S1) is not.*

## Power calibration — what the estimator CAN see (R-v)

A negative is only as strong as the lamp it was read under. At **canon-like n=114 and 66% missingness**, a known
3-class structure was planted and its **separation** swept (modal_p = the excess probability a cell shows its
class's modal level), 8 seeds each. Machine output:
[`factors_sensitivity.json`](../../eightfold/results/atlas/factors_sensitivity.json).

| separation modal_p | recover k≥2 (8 seeds) |
|---|---|
| 0.9 / 0.7 / 0.5 | **100%** |
| 0.4 | 75% |
| 0.3 / 0.2 / 0.15 / 0.1 / 0.05 | 12–75% (noisy) |
| 0.0 (no separation) | 50% (uniform-marginal false-positive) |

**Detectable-effect floor: modal_p ≈ 0.5** — the LCM reliably (100%) recovers a planted 3-class structure down to
a *moderate* separation at canon n. So **k\*=1 on the canon means: no latent basis of separation ≥ 0.5 exists** —
the lamp reaches moderate structure and finds none.

Honest read of the low end: below 0.5 recovery degrades into noise, and at modal_p=0 the LCM spuriously reads
k≥2 in ~50% of seeds. That false-positive is an artifact of the **uniform** synthetic marginals at zero
separation (a weak k=1 baseline); the real canon's marginals are strongly skewed (modal probs 0.44–0.81), a
strong k=1 baseline where it does not arise — evidenced by the **decisive** real k\*=1 (k=1 beats every k≥2 by
>1 SE, not a borderline call) and by the uniform-null selftest reading k\*=1 at n=90. The canon verdict sits
comfortably outside the ambiguous regime: **"no basis," not "basis below the lamp."**

## Honest caveats (named, per the house standard)

1. **Power at n≈114 — the load-bearing caveat.** The selftest validated recovery of **strong, well-separated**
   planted structure (modal probability 0.9). Latent structure *weaker* than that could exist below this
   estimator's power at n=114; k\*=1 means "no structure strong enough to improve held-out prediction at this n,"
   **not** "provably no structure." The pre-registered forward path is more rows: **Foundry-scale data**
   sharpens (or overturns) this interval. This is the same n≈114 coarseness A3's complete-case block flagged.
2. **The low-rank arm was not triggered, and must not be reached for now.** Escalation to low-rank categorical
   PCA fires **only on selftest failure**, which did not occur. Switching models now because k\*=1 is unwelcome
   would be arguing a resized verdict back (forbidden). A continuous-factor / literal-loadings reading is a
   legitimate **new, separately pre-registered** analysis — not a post-hoc swap on this one.
3. **Held-out prediction is a demanding instrument.** It asks whether latent classes *improve masked-cell
   prediction*. An atlas can carry real pairwise *associations* (the surviving approx⟷param gradient) that a
   global predictive model does not turn into higher held-out accuracy — most charges are sparse frontier
   columns with weak cross-structure. "k\*=1 by prediction" and "a real gradient exists" are not in tension.
4. **This does not overturn A3 or Crucible.** A3's H1 (≥5 MCA dims) was already RESIZED by Crucible S1; the
   banked S1–S5 verdicts stand. Factors v1 is the marginal-robust estimator A3 lacked, and it makes the
   S1-resized dimensionality quantitative. No prior verdict is argued back.

## What it means

The charge atlas is, to the resolution of held-out prediction at n≈114, **predictively one-dimensional**:
knowing a problem's inferred latent class does not help predict its hardness on a held-out charge beyond that
charge's marginal frequency. The "hardness is a vector" intuition — true as a *statement about MCA variance
directions* — does **not** cash out as *predictive* multi-dimensionality. The single robust cross-charge signal
the program has found (the approx⟷param gradient, S1/S2/S3/S5-survived) is a local axis that does not lift the
global predictive dimensionality above 1.

## Forward

- **P3 (Foundry, Sprint 3.3) inherits a well-defined k\*=1 canon fit.** The census↔canon loading comparison must
  be operationalized in `foundry` prereg_v2 (rider R-i) against a **k=1** canon baseline — the anchor-registered
  comparison is now a comparison of *marginal* profiles unless the census itself shows k\* > 1. This is a real,
  usable P3 input, not a blocked one.
- **The pre-registered route to revise k\*=1 is scale, not model-switching:** Foundry-scale generated data (many
  more rows) is where a weak latent dimensionality, if real, becomes recoverable.
- The MCA-16 vs prediction-1 gap is itself a finding — a clean second data point (after S1) that eigenvalue
  dimensionality on a charge atlas is marginal-driven.

## Factors v1.1 follow-up (prereg_v8) — k\* = 1 is confirmed robust

The v7 verdict was triangulated along two axes — a **new** pre-registered analysis
([`prereg_v8.json`](../../eightfold/results/prereg/prereg_v8.json), owner-chosen, **not** a post-hoc swap; v7
stands as the primary). Machine output: [`factors_v1_1.json`](../../eightfold/results/atlas/factors_v1_1.json)
(sha `c96fb8a5…`, `python -m eightfold.factors --followup`).

| Arm | Axis tested | k\* | note |
|---|---|---|---|
| v7 LCM, all-8 | reference | **1** | marginal baseline 0.666; no k≥2 improves |
| **low-rank, all-8** (null-corrected) | model class | **0** | marginal 0.666 is best; *every* rank is worse and none beats the independence null |
| low-rank, core-4 | charge sparsity | **0** | n=16 complete-case; no structure |
| LCM, core-4 | charge sparsity | **1** | n=16, flat interval [1..6] — underpowered, consistent |

**Every arm gives k\* ≤ 1 → k\*=1 CONFIRMED ROBUST.** Two conclusions:

1. **Model class is not the reason.** A continuous-factor model (low-rank categorical PCA) finds k\*=0 — *more*
   decisive than the LCM: the marginal baseline is the single best predictor and adding any factor makes held-out
   accuracy worse. The k\*=1 verdict is not an artifact of the LCM's discrete classes.
2. **Charge sparsity is not masking it.** Restricting to the well-populated core-4 reveals no structure (low-rank
   k\*=0). The LCM core-4 gives k\*=1 but at n=16 with a flat interval — underpowered, so weak-but-consistent (the
   pre-registered caveat).

The low-rank arm needed a **null correction to be valid at all**: a raw SVD rank on the one-hot indicators
inherits the very compositional inflation that disqualifies MCA. Crediting a rank only when it beats an
independence (column-permutation) null removes the artifact — and once it does, the continuous-factor model finds
nothing. This is a **second, independent confirmation that the MCA-16 dimensionality is artifactual.** The forward
path is unchanged: revising k\*=1 requires Foundry-scale data, not model-switching.

## Caveats index

power-at-n114 · detectable-effect-floor-modal-p≈0.5 (R-v) · low-end-uniform-marginal-false-positive ·
low-rank-arm-not-triggered-no-post-hoc-swap · prediction-is-a-demanding-instrument · does-not-overturn-A3/Crucible ·
excess-over-null-degenerate-once-k\*=1-but-low-rank-null-correction-and-S1-pairwise-are-the-real-story (R-iv) ·
MCA-16-disqualified.
