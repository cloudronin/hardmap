# Mosaic L3/L4 — the corrected scorecard, and the reversal arc as the methods contribution

**Date:** 2026-07-24. Prereg `prereg_v10` + clarification-01 (resolution ladder) + addendum-01 (89-row
absorption re-run). All numbers 3-class; locality is an approximate LLM-coded variable (κ=0.646). The
estimator for conditional association is `structure.stratified_cramers_v`, gated by the `hardmap verify`
known-answer test (defect #15).

## The corrected scorecard

| bet | verdict | evidence |
|---|---|---|
| **P1** instrument | **QUALIFIED at 3-class** | κ=0.646, anchors 7/7 both coders, separability clear |
| **P2** separate association | **two-property SPLIT, powered** | V(loc,approx)=**0.56** [0.48,0.70] clears; V(loc,param)=**0.14** [0.00,0.34] misses |
| **P3** absorption | **INSUFFICIENT RESOLUTION** | canon-47 9/19-per-class, pooled-89 min-class 13 — all below floor; descriptively no absorption |
| **P4** composition (B1 payoff) | **INSUFFICIENT RESOLUTION** | uses the same underpowered within-class tables as P3 |
| **P5** violator fingerprint | **HOLDS** | off-diagonal delocalized 4/5 vs on-diagonal 6/13; `subset-sum` the dissociation exhibit |
| **P6** kernel netting | **partial / structurally blocked** | V(kernel, locality)=0.28 (weakly independent); kernel↔param untestable (param constant on FPT rows) |
| **P7** expressiveness | exploratory only | P3 is INSUFFICIENT (not a clean partial), so the trigger is ambiguous; runs at its 31-row floor as exploratory |

## The positive finding: the two-property split, adequately powered

Locality — the blind structural label — **predicts the approximation charge (V=0.56, CI [0.48, 0.70],
clears 0.35) but not the parameterized charge (V=0.14, CI [0.00, 0.34], the whole interval below 0.35).**
On the 89-row population the parameterized column finally *has* variation (FPT 57 / W[1] 17 / W[2]+ 10 /
para-NP-hard 5), so the 0.14 is a genuine null, not a no-variation artifact. The single locality label is
**decomposition-locality**: it carries the approximation side of the gradient and leaves the parameterized
side essentially unexplained. That is the two-property split, measured directly and with power — the
knapsack dissociation (decomposable structure, W-hard coordinate) generalized to the corpus.

P6 corroborates weakly: `kernel_status` (poly- vs no-poly-kernel), the natural *certificate-locality*
proxy, is only V=0.28 with locality — a partially independent second property, poly↔local-covering /
no-poly↔delocalized in direction. The clean confirmation (does certificate-locality drive the parameterized
side?) is **structurally blocked**: kernelization is FPT-only, so the rows that *have* a kernel_status all
have parameterized=FPT (constant), and the param variation lives in the W-hard rows that have no kernel.
That is a real limit of the instrument, recorded as such.

## The null that is honest, not disappointing: absorption is unmeasurable at this n

P3 asked whether conditioning on locality *absorbs* the approx↔param coupling. It does not, and — more
precisely — it **cannot be measured** at n=47 or n=89 split three ways. The pre-sealed power check
(addendum-01) declared INSUFFICIENT RESOLUTION: locality×approx clears only 29% of cells at full granularity
and 78% collapsed-to-3 (one cell short of the 80% Cochran floor); the smallest locality stratum has 9
(canon) / 13 (pooled) both-real rows. Descriptively, no population shows absorption — canon 0.751→0.644
(14% shrinkage), pooled-89 0.366→0.447 (negative, small-sample inflation). The bet is **declared
INSUFFICIENT, not scored**, and the finding is: *the within-locality absorption test waits for the next
expansion's both-real recruitment.* The collapsed-3 result at 78% says 89 rows is close; a modest further
expansion may cross the floor.

## The reversal arc — the methods contribution demonstrating itself

Tonight's scoring of the program's **first mechanism bet** reversed three times, and the sequence is the
point, recorded dated and in order:

1. **First pass (buggy, optimistic):** an averaged-per-class V of 0.797, mis-read alongside a hopeful frame
   → looked like *no absorption but a real signal*.
2. **My over-correction (MISS, then wrong):** I recomputed a mis-normalized stratified V of 0.911 and
   declared a clean MISS / near-NOT-QUALIFIED — over-invoking "don't move the metric" to refuse a legitimate
   pre-sealed evaluation. (The owner caught the parallel L1 mis-call.)
3. **The owner's denominator challenge → INSUFFICIENT:** pressed on which denominator the scorer used,
   the bug surfaced — **averaging per-class V's is not a conditional association at all** (defect #15) — and
   the correct pooled-within-stratum-χ² estimator, plus a power check, showed the real verdict is
   INSUFFICIENT RESOLUTION: the sample is below the floor for the within-class test, in both directions
   (the point estimate shows no absorption *and* it is untrustworthy).

The permanent fix is not the number, it is the gate: `hardmap verify` now runs a **known-answer test** on
the conditional estimator before it touches real data — conditional independence → ~0, a Simpson
construction (marginal V=0.33, conditional=0.00) → ~0, perfect within-stratum → ~1. A mechanism bet was
saved from being scored HIT and then MISS on a broken estimator by the oldest rule — *the seal decides, in
both directions, against wishful passes and reflexive conservatism alike* — applied here to a denominator.

## Side track (own protocol, not gating): atlas errata candidates

The kernel-status pass surfaced three frozen-atlas parameterized cells that overstate the literature:
`bin-packing` and `bin-covering` (FPT-in-#distinct-sizes claimed; only XP known — Goemans–Rothvoß), and
`firefighter` (parameterized=FPT, but W[1]-hard by #saved-vertices — Bazgan–Chopin–Fellows). These proceed
on the errata track (E-protocol, v3.1), independent of Mosaic.

## What the program has, after Mosaic

The gradient's *constituent* is not one "locality" that absorbs the coupling — that is unmeasurable at
current both-real n. What is measured, with power, is the **split**: a blind structural property predicts
the approximation side of the hardness gradient and not the parameterized side, and a second property
(kernelization) is partially independent of the first. The mechanism is at least two-dimensional, and the
absorption question is now a *powered-experiment-waiting-for-rows* rather than an open conjecture — which is
a sharper place than the line has stood since Pebble.
