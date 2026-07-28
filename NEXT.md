# NEXT — what is open, compiled from the artifacts

**This file is DERIVED. Do not edit it.** Regenerate with `python3 foundry/dev/build_next.py`.

It duplicates no fact: the maptrail owns rulings, the methods thread owns reasoning, commits
own sequence. If this page disagrees with its sources, **the sources are right.** Nothing may
be recorded here that lives nowhere else — a hand-edit would make it a place where rulings
hide, which is the failure it exists to prevent.

This page carries no timestamp and no commit id: it is a pure function of its sources, so
two compiles from the same artifacts are byte-identical. Provenance belongs to the commit
that carries the file, not to a line inside it.

---

## Open work, in declared order

### 1. Backfill `supersedes` + `written_at` on the four typing artifacts

precedence must travel IN the artifact, declared by the pass that supersedes; inferring it from maptrail mentions inverted the order and invented an UNTYPED class for 105 rows

- key: `typing-precedence-backfill`
- see: `annotation:typing-precedence-ruled`
- see: `commit 4bb7fb1`
- *(opened by backfill — this item predates the openness signal)*

### 2. Loader walks the declared supersession chain; completeness guard; negative-space staleness test

the db answers the PRE-adjudication question for 51 rows — two typing passes wrote artifacts the loader never consumed. Shape-discovery already works; only the ordering signal was wrong.

- key: `loader-typing-walk`
- see: `annotation:typing-precedence-ruled`
- *(opened by backfill — this item predates the openness signal)*

### 3. Re-run the optimization supply census on the corrected column

the previous census read a reach_class column since proven stale; no supply number should be quoted from it

- key: `optimization-supply-census`
- *(opened by backfill — this item predates the openness signal)*

### 4. Recompute the successor bet's revival condition and disposition

prereg_v34 was voided for clearing power against clusters its statistic could never read. Its successor needs 10 reserved OPTIMIZATION SUBSET clusters; bin-packing sits on the frontier as an optimization reservation but was adjudicated REACH-partition, so the count may be 4 not 5. HELD-power vs HELD-path-gated falls out of the corrected census.

- key: `successor-bet-disposition`
- see: `retraction:prereg-v34`
- see: `wave-5:ruling:void-prereg-v34`
- *(opened by backfill — this item predates the openness signal)*

### 5. Contact sheet for steiner-forest's dual-motion trajectory

the first row in the archive where both regions move along one dial — feasible 1420 -> 691 while optimal grows 2 -> 21

- key: `steiner-forest-contact-sheet`
- see: `expansion:batch10`
- *(opened by backfill — this item predates the openness signal)*

### 6. Decide the REACH-assignment capture path

13 rows now type REACH-assignment after the 59-row adjudication, and the HELD-path-gated number-theoretic candidate revives only if this path lands

- key: `assignment-capture-path`
- see: `annotation:assignment-path-constituency`
- *(opened by backfill — this item predates the openness signal)*

### 7. Find an ambient-stable framing for covering-radius, or let the exclusion stand

held across batches 4-6 then typed out as deferred-no-ambient-stable-framing; the candidate framing (fixed ambient at declared n, ramp on code rate) is recorded

- key: `covering-radius-framing`
- see: `exclusion:covering-radius`
- *(opened by backfill — this item predates the openness signal)*

### 8. Whether the five in-use family ramps are secretly thresholds (Q20)

the leave-one-out flatness check that caught MCSP has never been run on the ramps already in use; applying it retroactively goes through rule-before-computation

- key: `lexicon-v3-question`
- *(opened by backfill — this item predates the openness signal)*

---

## State

- **problems**: 346
- **catalog cells**: 446
- **frames**: 2032
- **frontier (reserved)**: 16
- **waves**: 5
- **candidates enumerated**: 1942
- **maptrail records**: 75
- **descriptor version**: v7

- **reserved rows** (16): `balanced-vertex-separator`, `bin-packing`, `capacitated-vertex-cover`, `cluster-editing`, `directed-steiner-tree`, `group-steiner-tree`, `k-minimum-spanning-tree`, `k-set-packing`, `maximum-minimal-vertex-cover`, `minimum-fill-in`, `minimum-k-cut`, `multiway-cut`, `nearest-codeword`, `planar-dominating-set`, `power-dominating-set`, `weighted-interval-scheduling`

---

## How to close an item

Discharge is a NEW maptrail record pointing at the original, never an edit — the same shape
as the reservation ledger's reserve/release, so replay is the state:

```python
from foundry.catalog import maptrail as M
M.discharge(TRAIL, "<item-key>", by="<commit or artifact>", note="...")
```

Then regenerate this file. An item vanishes from the page because the trail says it closed,
never because someone deleted a line here.

