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

## Caveats index

power-at-n114 · low-rank-arm-not-triggered-no-post-hoc-swap · prediction-is-a-demanding-instrument ·
does-not-overturn-A3/Crucible · excess-over-null-degenerate-once-k\*=1 · MCA-16-disqualified.
