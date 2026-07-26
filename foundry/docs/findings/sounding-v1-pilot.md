# Sounding v1 — the blend probe on natural rows (pilot S1)

**Prereg:** `prereg_v17` · **Date:** 2026-07-26
**S-1 PASS (7/7 exact) · S-2 INSUFFICIENT — confounded · S-3 INSUFFICIENT · S-4 not filed**

The qualified probe, taken to the population it was built for. Named plainly in the seal: this is the
legitimate revival of Terroir-C's question — *does measured solution-space geometry predict cited charges?*
— on a new instrument and a new population. Nothing sealed shut was reopened.

**13 rows carry a working generator and enumerator**, against a floor of 12. The probe's reach on the
natural corpus at current cost is 13 rows, and that number is itself a deliverable.

## S-1 — calibration: PASS, 7 of 7 exact

| row | region | flavour | rate |
|---|---|---|---|
| sat-2 | solutions | majority | 0.0 |
| horn-sat | solutions | min | 0.0 |
| xor-sat | solutions | minority | 0.0 |
| bipartiteness | solutions | minority | 0.0 |
| vertex-cover | feasible | max | 0.0 |
| independent-set | feasible | min | 0.0 |
| clique | feasible | min | 0.0 |

Generators, enumerators and encodings are correct. **Theorem-forced and sealed as such**: if Γ is closed
under *f*, every instance's solution set is closed under *f* — that is what a polymorphism is. A superset
of a vertex cover is a vertex cover; a subset of an independent set is independent. This arm earns
implementation confidence and nothing else.

## S-2 — the mechanism question: INSUFFICIENT, confounded three ways

The raw numbers point the sealed direction — decision-hard rows louder, **+0.3282**. They do not survive
their own controls.

**Confound 1 — S-1's calibration zeros leak into S-2's statistic.** Every decision-*easy* row in this pilot
is a CSP carrying exactly one theorem-forced zero, which drags its mean down. Excluding forced flavours the
gap falls to **+0.1908**: **42% of the apparent separation was the forced arm bleeding into the measured
one.**

**Confound 2 — region size.** Violation rate correlates **−0.39** with log *r*, and hard rows have
systematically smaller regions (mean *r* 89.5 vs 201.5). Stratified: the gap is **+0.3431** among large-*r*
rows and **+0.0319** among small-*r* rows — nearly all of it lives where region size differs most.

**Confound 3 — region kind, and this one is structural.** Every optimal-region row in the pilot is
decision-hard (5 of 5); every decision-easy row is a solutions-region row (4 of 4). **Region kind and
hardness are not separable in this sample**, so a comparison across them is not a comparison of geometry.

Not scored. Declared INSUFFICIENT, not argued past.

## S-3 — the within-family cut: INSUFFICIENT

Sealed from birth this time rather than bolted on. No family carries enough label-varying rows: `graph`
n=6 with one easy row, `sat-csp` n=5, `number-theoretic` n=2 with no label variation. The graph family's
single contrast is itself region-kind confounded. Terroir's vocabulary applies and returns INSUFFICIENT.

## S-4 — registry: not filed

No open cell was in scope. Every pilot row's decision charge is already cited, so there was nothing to
predict-then-fill.

## What the pilot actually bought

**The instrument deploys.** Thirteen natural rows now have measured solution-space geometry where they had
none — the first instrument reading on any of the 317 rows closure anatomy cannot reach. Rates ship with
*r*, the distinct-subset count and the uniform cap, so the deflator species cannot recur at this schema.

**And the pilot diagnosed its own design.** The three confounds are not noise; they are a specification for
the fleet:

1. **Recruit decision-easy optimisation rows** — minimum spanning tree, max-flow, 2-colouring — so region
   kind stops being a proxy for hardness. Without them no amount of *n* separates the two.
2. **Match region sizes across the contrast**, or model *r* explicitly. A statistic that moves with region
   size will read as a finding whenever region size correlates with the label.
3. **Score S-2 on forced-excluded flavours only.** The forced zeros belong to S-1 and must not enter the
   measured statistic — 42% of a headline came from that leak alone.

An expansion that does not fix all three would produce a larger version of this same uninterpretable gap.
**That is worth more than the gap would have been**, and it is what a pilot is for.

## Artifacts

`prereg_v17.json` · `foundry/dev/sounding_v1.py` (generators, enumerators, probe) ·
`foundry/foundry/results/lattice/sounding_v1_results.json` (profiles, four scores, 73 acknowledged
extremals). Frozen bytes untouched; no charge cell written.
