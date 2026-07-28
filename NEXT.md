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
- **maptrail records**: 91
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

<!-- sources: {"maptrail.jsonl": "2bbeea23a98dfa31c53ad3fe654ef4b5d74a765f1baeb4adfc4b670c061f2e47", "observatory.db": "cca85ceced456594edb54b7fb3b0d25ad3490d0ee1d025cd53ef952b919b6eee", "observatory_reservation.jsonl": "b95df7abf9d7efc2d965652a76e4401ac0b4d3250e6162dd2167ea154e9581fc"} -->

