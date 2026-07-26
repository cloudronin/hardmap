# The trajectory report — how excess moves along the ramp

**Status: DESCRIPTIVE BY DECLARATION.** No verdict, no score, no prediction. The classification at the end
is a mechanical label applied by a rule pinned before it ran — **it is not a finding.**
**Date:** 2026-07-26 · **Artifact:** `sounding_trajectories.json` · **Plots:** `plots/trajectory-*.svg`

---

## The classification rule — pinned before it ran

Stated in the script header and in the artifact, **before any classification executed**:

```
excursion      = max(excess) − min(excess)      over usable steps
pooled_ctrl_sd = mean(control_sd)               over those same steps

FLAT          iff  excursion < 2.0 × pooled_ctrl_sd
MONOTONE      iff  not FLAT, and the sequence is weakly non-increasing OR weakly non-decreasing
NON-MONOTONE  otherwise
UNCLASSIFIED  iff  fewer than 3 usable steps
usable step   =  a declared step with a reading whose r ≥ 10 (the pre-declared floor)
```

**The 2.0 is a convention, not a derived threshold.** Nothing about the excess statistic makes 2σ the
boundary between "flat" and "moving". It is the ordinary default, chosen in advance because choosing in
advance is worth more than choosing well.

To keep that arbitrariness **visible rather than merely confessed**, the whole table is recomputed at 1.0×
and 3.0×:

| multiplier | trajectories relabelled |
|---|---:|
| 1.0× | **4** of 108 |
| 3.0× | **7** of 108 |

So the labels are not especially sensitive to the choice — which is worth knowing, and would have been
worth knowing just as much if the answer had been 40.

## Coverage

**108 trajectories · 18 rows · 91 declared ramp steps.**

| classification | count |
|---|---:|
| MONOTONE | 41 |
| NON-MONOTONE | 24 |
| FLAT | 7 |
| UNCLASSIFIED | 36 |

UNCLASSIFIED is a third of the table. That is the ramp meeting the floor: many steps produced readings
below r=10, and short trajectories do not get a shape assigned to them.

## Controls were re-drawn per step — verified, not asserted

The directive asked for an assertion, and **an assertion that cannot fail is not one**. Controls are
matched on *r*, and *r* moves along the ramp — so a reused control would show an **identical
(mean, sd) pair at two different r**. That signature is detectable, so it was detected for.

**No such pair exists among non-degenerate controls.**

The check first fired on 37 readings, all with the profile `(1.0, 0.0)` — and that turned out to be a
false-positive mode, not a finding. A control saturated at rate 1.0 has **zero variance and no signature to
compare**; two steps matching there is a physical fact about small *r* under `minority`, not reuse. These
are `INSUFFICIENT-degenerate` in the v3 spec's **own pre-declared vocabulary** (control SD ≈ 0), so they
are counted and reported under that label rather than quietly skipped or wrongly flagged.

## Gaps are drawn as gaps

An absent reading is a claim of continuity unless the absence is itself recorded. So absences are held as
explicit nulls, never interpolated across, and **plot lines break at them**.

Two kinds are distinguished, because collapsing them would repeat the error the report exists to avoid:

| kind | cells | has a recorded reason? |
|---|---:|---|
| **GAP-no-region** — the declared step produced no region at all | 8 | **yes**, in the survey artifact |
| **combination-level absence** — the step produced a region, but not for this (region, flavour) | 10 | **no** |
| **INSUFFICIENT** — a reading exists but falls below the pre-declared floor | 160 | yes, by rule |

The second class is named separately *precisely because it is the undocumented one*.

And the third is not the same as the first two: an INSUFFICIENT step is **speech ruled inadmissible**, not
silence. The plots mark it `○` where a true gap is `×`. One glyph for both would misreport which occurred.

## The plots

One per family, drawn as **small multiples** — a mini-panel per (row, region), one line per flavour.

This replaced a single overlaid axis, which needed an 8-trajectory cap to stay legible and was therefore
**silently dropping 28 of `graph`'s 36 trajectories**. A capped plot reads as complete coverage. Small
multiples show all of it: **4 plots, 84 trajectories, nothing omitted.**

| plot | trajectories |
|---|---:|
| `trajectory-graph.svg` | 36 of 36 |
| `trajectory-sat-csp.svg` | 24 of 24 |
| `trajectory-number-theoretic.svg` | 12 of 12 |
| `trajectory-optimization.svg` | 12 of 12 |

(Trajectories with fewer than 2 usable steps have nothing to draw and are in the artifact only.)

## What the table shows, without interpretation

Stated as description, since that is all this report is licensed to do:

- The largest excursions sit on **`knapsack · feasible`** (0.59–0.63 across three flavours),
  **`dominating-set · feasible`** (0.70 majority, 0.71 max) and **`set-cover · feasible`** (0.43–0.62).
- The FLAT set is small and mostly `optimal`-region or coloring: `knapsack · optimal · majority` (0.0087
  against a pooled control SD of 0.0059), `graph-3-coloring · solutions · max` and `· min`,
  `hitting-set · feasible · min`.
- 24 trajectories are NON-MONOTONE, including `graph-3-coloring · solutions · maltsev3` with an excursion
  of 0.4991 against a pooled control SD of 0.0020.
- **`sudoku`** — the survey's only |D|=4 object and its only ramp on *constraint removal* — has 2 usable
  steps of 6 declared and is UNCLASSIFIED. Its readings are `max` +0.0008 / +0.0010 and `min` +0.0013 /
  +0.0012 at 2 and 0 clues, with `median` and `maltsev4` at −0.09/−0.02 and −0.03/−0.05.

No claim is made about why any of these move as they do. Three went to the bank as shape-specific entries.

## Scope

This report describes the v3 column only. It does not compare rows, does not relate trajectory shape to
any charge value, and does not license the Q2 fork — which the owner rules with both deliverables on the
table.
