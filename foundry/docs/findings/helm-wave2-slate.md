# Helm wave 2 — the rulings applied, and the slate is still empty

**Status:** EXPLORATORY. Describes the engine, not the atlas.
**Artifacts:** `helm_wave2_slate.json` · `helm_wave2_candidates.jsonl` · `wave_trail.jsonl`
**Swept:** `observatory.db` `bcf27d60cdcadb65` under `sweep/v2`

Wave 1 is not re-run. Its trail is committed and stands as what the engine saw before the rulings
existed; the amended screens produce a **new wave**. The wave id is computed as the next unused one
rather than typed, so a future rule change cannot silently overwrite a recorded wave.

## What moved

```
                        wave 1        wave 2
enumerated                 344           344
REJECTED                    87            89     netting 30 · null-missing 57 → 59
HELD                       257           255     power-fail 210 → 230 · null-missing 47 → 25
SLATED                       0             0
```

Three rulings changed the machinery between them:

**The extremal null is pinned.** `stratified-exchangeability/v1` — permutation within the candidate's
own **(family × region-kind × flavour)** stratum, r-band as a matching covariate, floor 20 cells. The 22
anomaly candidates that wave 1 held for want of a model now clear screen 1 and fail on *supply* instead:
the 2-row frontier delivers at most 1 cell to any stratum against a floor of 20. That is a better kind of
holding — the gap is now a number that shrinks as the frontier fills, rather than a missing model.

The floor is derived: a one-sided permutation over *m* cells attains no p below 1/(m+1), so 19 is where
0.05 becomes reachable at all and 20 is the first size with anything to spare.

**Twenty cells left the swept population.** Five rows — `densest-k-subgraph`, `k-center`, `max-coverage`,
`max-dispersion`, `min-bisection` — declare fixed cardinality, so their *feasible* region is every size-k
subset: identical at every ramp value before an instance exists. `max-coverage` reads r=120, overlap
0.5765, BC 0.4696 at all five steps and would read the same at any other. They are now flagged
`structurally_flat` at descriptor@v2 and excluded via the `sweepable_catalog` view.

This was not cosmetic. Removing them moved real numbers — optimization's `overlap_ref × r_ref` fell from
0.843 to 0.810, `r_ref × insufficient_share` from 0.833 to 0.788. Constants were inflating those
correlations, and every one of them was headed for the hold queue as a candidate.

**The catalog is at v2.** Adding the `structure` group changed no v1 descriptor's value, but the version
bumped anyway: if `v1` sometimes carried the group and sometimes did not, `descriptor@v1` would stop
identifying a schema. `catalog_v1.jsonl` is left exactly as v1 last built it and is no longer regenerated.

## The count that matters is unchanged

The nearest adjudicable candidate still needs **6 more reserved rows** — `rho(overlap_ref,
bimodality_max)` on number-theoretic trajectories, disclosed 0.866, needing 8 clusters against the
frontier's 2. Three more batches.

The hold queue's top is still entirely **coherence** descriptors, and the flat-cell exclusion did not
change that. `overlap_ref`, `bimodality_max`, `r_ref`, `insufficient_share` — the frontier's first
affordable questions remain the ones the mechanism question needs.

## Kill 1 status

Two waves have now produced slates dominated by untestable candidates, which is Kill 1's stated
condition. **It should not fire, and the reason is recorded rather than assumed:** Kill 1 exists to
detect an engine whose questions the frontier can never adjudicate. Here the frontier is 2 rows old and
grows 2 rows per batch by construction, and every held candidate carries the exact size that revives it.
The diagnosis Kill 1 would deliver — "the frontier's capture rate bounds the program's question rate" —
is already the measured finding, and the bound is scheduled to lift at batch 6 rather than being a
standing property of the engine.

Firing the kill now would demote Helm for being correct about a frontier that is three batches from
useful. Recorded as a deliberate non-fire, for the owner to overturn if they read it otherwise.
