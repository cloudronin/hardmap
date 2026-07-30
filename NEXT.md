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

### 2. Declare the nine within-instance dials for batch 11, one per row, at session start

All nine eligible graph rows carry 'edge density' as their census ramp_parameter, which is the dial Q21 ruled out wherever the ground set IS the edge set. Each needs a within-instance parameter at a fixed ground set, declared per row and put through the pilot protocol: dial isolated, ambient fixed by construction, derived-consequence check at the probe.

SCHEDULED, NOT BATCHED. Three declaration-implementation disagreements is the base rate speaking, and all three came from declaring dials quickly at the end of other work. Ruled to a fresh session at full context; the scheduling costs nothing and is the only thing that has reliably prevented the fourth.

Rows: cycle-packing, k-edge-connected-subgraph, maximum-leaf-spanning-tree, min-communication-cost-spanning-tree, min-degree-spanning-tree, multicut, node-multiway-cut (structural_expectation corrected to NOT upward_closed), sharp-spanning-trees, sparsest-cut.

- key: `batch-11-ramp-declarations`
- see: `foundry roster eligible --family graph`
- see: `foundry/batches/README.md`

### 3. An exclusion-at-birth cannot be re-derived — the record names no generator sha

cycle-packing's batch-7 exclusion does not reproduce: with batch 7's own seed and its declared median probe, the current generator builds regions of size [12, 12] and passes conformance. Neither the probe hypothesis nor a seed-sensitivity hypothesis survives; the honest answer is that the generator or its constants changed after batch 7 and the exclusion record describes code that no longer exists.

The record carries the row, the reason, the probe value and the conformance detail — but no sha of the generator that failed. So an exclusion can be read and cannot be CHECKED, which is the same provenance-without-a-receipt species the catalog already fixed for cells (frame_artifact + frame_sha256 + extractor_sha256 per row). Panels should carry the same.

Until they do, every standing exclusion-at-birth is a claim on trust rather than a reproducible verdict.

- key: `exclusion-records-carry-no-code-provenance`
- see: `maptrail disposition:cycle-packing`
- see: `foundry/catalog/capture.py conformance_at_birth`
- see: `observatory_batch7_panels.json excluded_at_birth`

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
- **maptrail records**: 103
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

<!-- sources: {"maptrail.jsonl": "ba1376419595c90c946f08b35118b3b1bd1283c9b25e6767030261b05b6cd6c7", "observatory.db": "43b7153123de9a9e0a7dfa13bc79e17a9a7e7cd5ea0f83c5e8ce4d89a60c89ad", "observatory_reservation.jsonl": "b95df7abf9d7efc2d965652a76e4401ac0b4d3250e6162dd2167ea154e9581fc"} -->

