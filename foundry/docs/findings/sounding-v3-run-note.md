# Sounding v3 — widened and ramped survey (run note)

**STATUS: EXPLORATORY SURVEY. No scored predictions, no sealed bet, no verdicts, no shape claims.**
**Date:** 2026-07-26 · **Artifacts:** `sounding_v3_survey.json` · `sounding_v3_track1_census.json`

**528 readings · 18 rows · 91 declared ramp steps · 9 Marrow-excluded rows.**

## Track 1 — widen

Census attempted 10, **built 8, deferred 2**, and the census is the record either way.

Seven new rows entered; **six are Marrow-excluded** — unbounded-arity scopes, no fixed finite template,
closure anatomy underivable *by theorem*: `set-cover`, `hitting-set`, `feedback-vertex-set`,
`odd-cycle-transversal`, `independent-dominating-set`, `knapsack`. The probe's unique reach is exactly
there, and each is territory nothing else in the programme touches.

**Deferred at honest cost, not forced:** `one-in-three-sat` (the exact-one constraint over-constrained at
every density tried; r = 0) and `sudoku-9x9` (81 cells over 9 values; enumeration out of reach, low-clue
sampling not attempted inside the box).

**`sudoku` entered as the eighth row** — the survey's first |D| = 4 object, and its first ramp on
**constraint removal** rather than instance size. All 288 valid Shidoku grids are enumerated once and
**verified against the known count by an independent validator** before anything is built on them. It is
not an atlas row and carries no cited charge; recorded `in_atlas: false` with decision `n.a.` rather than
given a label it does not have.

## Track 2 — ramp

Every row is re-read across a declared ramp, 4–6 steps, the parameter named per family: clause/variable
ratio for SAT rows (through their thresholds where known), edge density for graph rows, set count or value
range for the combinatorial rows, and **descending clue count** for sudoku.

**Each step draws its own matched control.** Controls are never reused across steps, because *r* moves with
difficulty and a reused control would be matched to the wrong size — the size-confound this whole statistic
exists to remove, reintroduced through the back door. Per-step seeds are in the `ramp_manifest`.

## Coverage, stated as coverage

- **160 readings flagged `INSUFFICIENT-r`**, concentrated where round 2 predicted: optimal regions at the
  hard end of their ramps. Flagged, kept in the trajectory, **never interpolated over**.
- **2 steps produced no reading at all** and are recorded as explicit `GAP-no-region` entries —
  `sat-3` at ratio 5.5 and `sudoku` at 12 clues. A silently omitted step leaves a trajectory that *looks*
  continuous across a hole, which is the same interpolation the INSUFFICIENT discipline forbids, achieved
  by absence instead of by drawing.
- **39 unforced exact-zero readings** across the column. These are the zero-hunt's input and are **not**
  adjudicated here.

## Hygiene carried from v2

Forcedness is **derived** from Marrow's pinned templates from birth, with `ASSERTED` entries carrying their
arguments and `null` meaning *underivable*, which is not *false*. Sudoku carries an **asserted-not-forced**
entry with its argument — its template is CSP(K₄)-shaped, and like CSP(K₃) a complete-graph target admits
no nontrivial library polymorphism, so no flavour is forced to zero and every zero in that row is a genuine
reading rather than a definition.

Distinct m-subsets only; raw-difference excess with the standardized value shipped unscored beside every
reading; full per-reading provenance.

## What is not here

No verdicts. No trajectory shapes named. No mechanism language. The trajectory report and the zero-hunt are
separate deliverables and are not started in this run. Anything eye-catching goes to the banked-questions
file.

Frozen bytes untouched. W-review unaffected.
