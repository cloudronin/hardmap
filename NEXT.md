# NEXT — what is open, compiled from the artifacts

**This file is DERIVED. Do not edit it.** Regenerate with `foundry next`.

It duplicates no fact: the maptrail owns rulings, the methods thread owns reasoning, commits
own sequence. If this page disagrees with its sources, **the sources are right.** Nothing may
be recorded here that lives nowhere else — a hand-edit would make it a place where rulings
hide, which is the failure it exists to prevent.

This page carries no timestamp and no commit id: it is a pure function of its sources, so
two compiles from the same artifacts are byte-identical. Provenance belongs to the commit
that carries the file, not to a line inside it. The source hashes it was compiled from are
recorded at the foot of the page, so the claim can be checked with `foundry fresh` rather
than taken on trust.

---

## Open work, in declared order

### 1. Decide the REACH-assignment capture path

13 rows now type REACH-assignment after the 59-row adjudication, and the HELD-path-gated number-theoretic candidate revives only if this path lands

- key: `assignment-capture-path`
- see: `annotation:assignment-path-constituency`
- *(opened by backfill — this item predates the openness signal)*

### 2. Batch 11's roster needs three dispositions and per-row Q21-corrected ramps

The graph subset pool vets to 7 FRESH rows: cycle-packing and planar-vertex-deletion and node-multiway-cut were each ATTEMPTED AND EXCLUDED AT BIRTH in earlier batches, and each needs a disposition before it can be re-rostered.

  planar-vertex-deletion  batch 7, no-affordable-exact-test — no exact planarity test at enumeration scale. A hard blocker unless the region is reformulated.
  cycle-packing           batch 7, conformance: no usable region at probe 0.35. THE PROBE WAS THE OLD ONE. The corrected rule probes the MEDIAN declared level, which is 0.5 for the graph ramp — ~43% more edges. This is the same shape as the MCSP incident: a row excluded for a property of the probe and blamed on the row. Worth re-probing before it stands.
  node-multiway-cut       batch 9, 'not upward_closed'. It BUILT (sizes 28,16,16,16); only the declared structural expectation failed. That is a declaration error, not a build failure, and it is re-rosterable with the expectation corrected.

Separately, all 10 carry 'edge density' as their census ramp_parameter, which is exactly the dial Q21 ruled out where the ground set IS the edge set. Each needs a per-row within-instance parameter at fixed ground set declared before capture — the step that produced three declaration-implementation disagreements when done quickly.

- key: `batch-11-roster-composition`
- see: `batch11_roster_vetting.json`
- see: `observatory_batch7_panels.json excluded_at_birth`
- see: `observatory_batch9_panels.json excluded_at_birth`
- see: `foundry/batches/README.md — the declaration convention`

### 5. Contact sheet for steiner-forest's dual-motion trajectory

the first row in the archive where both regions move along one dial — feasible 1420 -> 691 while optimal grows 2 -> 21

- key: `steiner-forest-contact-sheet`
- see: `expansion:batch10`
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

### 9. Lift the six delegated verbs out of dev/ into the library

The `foundry` CLI is one dispatch surface now, but six recurring operations still hold their logic in dev/ and are reached by import: ambient-census, bimodality-fill, catalog, reach-census, wave, mint-prereg. Freshness is enforced for them at the boundary — `wave` against a stale db does refuse — but EVENT-TIME EMISSION is not, and cannot be: the dispatcher cannot make a dev script emit its maptrail record from inside the act it performs, and emitting on its behalf from outside is precisely the reconstruction Kill 3 forbids. So each lift buys one verb its own trail record. `test_cli.DELEGATED_CEILING` is 6 and only ever goes down; lower it as each lands.

- key: `lift-delegated-verbs`
- see: `foundry/foundry/cli.py DELEGATED`
- see: `foundry/tests/test_cli.py DELEGATED_CEILING`
- see: `foundry/foundry/catalog/next_page.py — the pattern, already lifted`

---

## State

- **problems**: 346
- **catalog cells**: 446
- **frames**: 2032
- **frontier (reserved)**: 16
- **waves**: 5
- **candidates enumerated**: 1942
- **maptrail records**: 97
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

<!-- sources: {"maptrail.jsonl": "15fb4a2fea38df451fa0eceea25e35b19b5ec84ce7315735f092b26fd42ec7dc", "observatory.db": "ec8a3d7a820ee128ad12f09ff2e7161546de0015f838c79767efae881d216dac", "observatory_reservation.jsonl": "b95df7abf9d7efc2d965652a76e4401ac0b4d3250e6162dd2167ea154e9581fc"} -->

