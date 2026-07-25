# Mosaic — findings

**Date:** 2026-07-24. The mechanism test B1 demanded. Consolidates L0–L4 (memory-cites, L1 qualification,
L3/L4 scorecard); prereg `prereg_v10` + clarification-01 (resolution ladder) + addendum-01 (89-row re-run).
All numbers 3-class; locality is an approximate blind-coded variable (κ=0.646). Estimator:
`structure.stratified_cramers_v`, gated by `hardmap verify`'s known-answer test (defect #15).

## Headline — the gradient's constituent is a SPLIT, not a single locality

The approximation↔parameterized coupling (B1) is not driven by one latent "locality" variable. It is driven
by **at least two partially-independent structural properties**: *decomposition-locality*, which the blind
label captures and which predicts the **approximation** side of the gradient (V = 0.56, CI [0.48, 0.70]),
and a second property the label does **not** capture, which governs the **parameterized** side (V = 0.14,
CI [0.00, 0.34] — the whole interval below the 0.35 bar). The single locality label carries one half of the
mechanism and is silent on the other. The knapsack dissociation — decomposable structure, W-hard coordinate
— generalized to the corpus, measured with power.

## The spine — five independent lines converge on two properties

The split is not one statistic; it is where five separate measurements, taken different ways, agree:

1. **P2 asymmetry (powered):** locality ‖ approximation (0.56), locality ⊥ parameterized (0.14). On 89
   rows the parameterized column finally varies (FPT 57 / W[1] 17 / W[2]+ 10 / para-NP-hard 5), so the null
   is genuine, not variance-starved.
2. **P5 violator fingerprint (holds):** the off-diagonal gradient-benders code `delocalized` 4/5 vs the
   on-diagonal controls' 6/13 — and `subset-sum` codes `decomposable`, the dissociation exhibit landing as
   sealed (decomposable *structure*, off-diagonal *coordinate* — the two properties pulling apart in one row).
3. **P6 weak independence:** `kernel_status` (poly- vs no-poly-kernel), the natural certificate-locality
   proxy, is only V = 0.28 with locality — a partially distinct second axis, poly ↔ local-covering /
   no-poly ↔ delocalized in direction.
4. **L1 instrument strain:** two blind coders qualify at 3-class but cannot reliably split the
   `entangled`/`mixed` seam (specific-agreement 0.16). The single label strains exactly where the two
   properties overlap — the hard end of the spectrum.
5. **The originating dissociation:** knapsack, the row that motivated the two-property hypothesis before any
   coding, is the same object the analysis recovers.

One line could be noise. Five, taken blind and by different instruments, converging on the same
two-dimensional shape, is the finding.

## The null, with its price tag — absorption is unmeasurable, and why

P3 (does conditioning on locality *absorb* the coupling) and its composition companion P4 are **INSUFFICIENT
RESOLUTION**, declared per the pre-sealed power check (addendum-01), not scored. No population shows
absorption descriptively (canon 0.751 → 0.644, 14%; pooled-89 0.366 → 0.447, negative — small-sample
inflation); the smallest locality stratum has 9–13 both-real rows, below the floor.

**The price tag is one recurring bottleneck, and it names the next experiment.** The canon's parameterized
column is *nearly constant* — mostly FPT — and that single variance starvation killed **three** tests
tonight: P3's within-locality strata (too thin once split), P6's kernel↔param test (untestable — kernels
exist only on FPT rows, where param does not vary), and canon-only P2 (param unmeasurable until v3-new's
W-hard mass was pooled in). The gradient can only be decomposed where **both** charges vary, and the canon
supplies approximation variation richly and parameterized variation barely. The v4 recruitment target
therefore is not "more rows" but **more parameterized-varied both-real rows** — W-hard problems that also
carry a real approximation value. The collapsed-3 power check reached 78% at 89 rows; a targeted recruitment
of W-hard both-real rows is the specific, justified next step, not a vague "expand more."

## The methods contribution — instance 14, the ledger's best single exhibit

The program's flagship mechanism bet was scored under the most tempting possible conditions, and the seal
held in both directions across **three rulings in one night, each correcting the last, each dated**:

- **HIT-ish** — a buggy averaged-per-class V (0.797) read alongside a hopeful frame.
- **MISS** — my over-correction to a mis-normalized 0.911 and a declared clean miss, over-invoking "don't
  move the metric" to refuse a legitimate pre-sealed evaluation.
- **INSUFFICIENT** — the owner's denominator challenge surfaced the real defect (**averaging per-class V's
  is not a conditional association**, defect #15), and the correct pooled-within-stratum-χ² estimator plus a
  pre-sealed power check gave the only honest verdict: the sample is below the floor.

Optimism would have scored it HIT (0.31 conflated from the B1 endpoint); conservatism scored it a wrong
MISS; the seal scored it INSUFFICIENT. The permanent fix is a **gate, not a number**: `hardmap verify` now
runs a known-answer test on the conditional estimator (conditional-independence → 0, Simpson marginal-0.33 /
conditional-0.00 → 0, perfect → 1) before it touches real data — the mechanical check instances 6 and 10
lacked. The arc under pressure, on the flagship bet, is the methods ledger's best single exhibit.

## What Mosaic established

The gradient's mechanism is **at least two-dimensional**, one dimension measured with power and named
(decomposition-locality → approximation), the other localized and partially isolated (certificate-locality →
parameterized) but blocked from clean measurement by the canon's parameterized variance starvation. The
absorption question is no longer an open conjecture — it is a **powered experiment waiting for the right
rows**, with a specific recruitment target. Fourteen methods-instances in, the question got sharper even
though the bet did not land — which is what this program's progress has looked like since Pebble.

*Errata candidates surfaced in passing — `bin-packing`, `bin-covering`, `firefighter` (parameterized cells
overstating the literature) — proceed on the E-track, independent of these findings.*
