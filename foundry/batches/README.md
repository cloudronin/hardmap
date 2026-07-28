# Batch declarations

One file per batch, authored **before anything is read**. `foundry census declare --declaration
batches/<N>.json` compiles it into `observatory_batch<N>_census.json`.

```
census = declaration + reservation + status
```

The declaration is the part a person writes: which rows, which family ramps, and why this batch. The
reservation is applied mechanically by the declared rule, and the status is fixed —
`DECLARATION — no reading exists for any row here`.

## Shape

```json
{
  "batch": 11,
  "why_this_batch": "the reason this roster and not another, in a sentence a stranger can check",
  "families": {
    "optimization": {"census_ramp": "constraint-to-ground-set ratio",
                     "ramp_values": [0.5, 1.0, 1.5, 2.0, 3.0]}
  },
  "roster": {
    "some-row": {"family": "optimization",
                 "instantiates_the_family_ramp_as": "terminals per candidate edge",
                 "structural_expectation": "upward_closed",
                 "capture_mode": "RAMPED"}
  },
  "carried_forward": {}
}
```

`structural_expectation` and `capture_mode` default to `null` and `RAMPED`. A roster naming a family
with no declared ramp is refused, as is one listing a row that is already built, not REACH-subset, or
whose family disagrees with the reach census.

## Starting the next one

Do not copy a previous declaration file by hand — copy-and-edit is what produced three census schemas
wearing one version string. Recover the previous declaration mechanically instead:

```python
from foundry.catalog import batch_census as BC
BC.declaration_from_census(LAT / "observatory_batch10_census.json")   # -> the declaration, as a dict
```

## Why this directory starts empty

Batches 3–10 were declared before this mechanism existed, by eight separate scripts under `dev/`. Those
censuses are declarations made **before reading**, so they are never re-emitted under the current shape
— re-writing a pre-reading declaration to agree with what came after is the contamination direction,
whatever the frozen manifest formally binds. Their history is named in the maptrail
(`foundry migrate status`, migration `0001-census-schema-history`) and
`foundry.catalog.batch_census.read` tolerates every shape they are in.

So the first file here will be batch 11's. Backfilling the earlier ones would fabricate authorship for
declarations that were made another way.
