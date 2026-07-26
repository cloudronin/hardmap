# Sounding v2 — the fleet (prereg_v18)

**Date:** 2026-07-26 · **Verdict: four-cell design FILLED · region-size tuning FAILED · F2 NOT SCORED**

The pilot's design brief, executed. Two of its three prerequisites were met; the third was not, and the
sealed kill criterion for it fired.

## What worked: the recruitment wall was made of recruitment

The pilot's `easy × optimal` cell was empty, which made region kind a proxy for hardness and put no amount
of *n* in reach of separating them. **Four decision-easy optimisation rows were recruited from the atlas's
tractable canon and all four built cleanly**: `min-spanning-tree`, `matching`, `reachability-stcon`,
`max-flow` (unit capacity), all on edge-characteristic encoding.

| | decision-easy | decision-hard |
|---|---:|---:|
| **solutions** | 4 | 4 |
| **optimal** | **4** | 5 |

**All four cells occupied, 17 rows.** The generator census was right that this wall was recruitment rather
than mathematics — and the tractable canon paid out exactly as expected.

## What did not: region sizes would not tune

`prereg_v18` named ensemble tuning as the **primary** region-size control and r-stratification as the check
that it worked. It did not work.

- **6 of 17** rows landed in the declared band [25, 250].
- Residual **corr(log r, rate) = −0.2932**.
- Within the `solutions` stratum alone, *r* spans **8 → 459**, a **57×** ratio. Within `optimal`, **2.6 →
  99**, 38×.
- `reachability-stcon` came in at **r = 2.6** — a region with almost nothing to blend, and a discovery rate
  of exactly 1.0 for that reason alone.

The sealed floor reads: *"if ensemble tuning cannot bring region sizes into the target band, say so and
score nothing that depends on comparability."* The within-region-kind gap depends on precisely that
comparability. **F2 is not scored.** F3 depends on F2 and is not scored either.

## What is recorded but not claimed

The within-region-kind gaps exist in the artifact. Their **sign differs between region kinds**. That is the
comparison the four-cell design was built to make visible — and it is exactly the comparison the tuning
floor forbids scoring, because a 57× spread in region size inside a stratum is not a controlled contrast.

It is recorded as **data for round 2's design, not as a finding**, and it is not quoted anywhere else.
Reporting it as a result while declaring the statistic unscored would be having it both ways.

## What the fleet bought

**The design brief was correct and is now half-discharged.** Four-cell occupancy is achieved and permanent —
those four generators exist and will not need rebuilding. The remaining obstacle is isolated, named, and
measurable: region size.

**And the failure is more informative than a scored null would have been.** Region size is not a nuisance
parameter here; it is entangled with what the rows *are*. Optimal sets of small graph problems are tiny by
their nature (a minimum vertex cover set has a handful of members); solution sets of CNF formulas are large
by theirs. **Tuning cannot equalise them without distorting the instances past recognition** — which is
itself the finding this round produces.

Round 3's fork, stated so it can be ruled rather than drifted into:

1. **Model *r* explicitly** rather than matching it — accept the residual uncertainty a 17-row regression
   carries, and say so.
2. **Restrict to comparable region types** — score only within narrow *r* bands, accepting a much smaller
   scored *n* per band.
3. **Change the statistic** to one that is scale-free by construction, so region size cannot enter. This is
   the most promising and the least specified; it would need its own design pass.

No expansion is authorised by this run.

## Artifacts

`prereg_v18.json` · `foundry/dev/sounding_v2.py` (four new generators + the schema-enforced discovery
statistic) · `foundry/foundry/results/lattice/sounding_v2_results.json`.

**Design law 3 is now enforced in code**: `discovery_rate()` cannot see a theorem-forced flavour, so the
pilot's 42% leak is impossible at this schema rather than merely avoided. Frozen bytes untouched.
