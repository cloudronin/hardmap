# Sounding survey — matched-null excess readings

**Status: EXPLORATORY SURVEY. No scored predictions, no sealed bet, descriptive tables only.**
**Date:** 2026-07-26 · **Artifact:** `foundry/foundry/results/lattice/sounding_survey_readings.json`

Sounding v2 reframes as a survey. The matched-null excess reading is run on every row with a working
generator, shipped as a measured column with full provenance. **Nothing here is citable as a result** —
nothing was predicted in advance and nothing is scored. Anything of interest is banked in
[sounding-survey-banked-questions.md](sounding-survey-banked-questions.md).

## What was measured

**114 readings across 20 rows** — the 17 fleet rows plus three cheap additions taken while the tooling was
warm. Each reading is one (row, region, blend flavour) triple.

**The statistic.** `excess = measured rate − mean(size-matched control)`, where each control is a uniform
random subset of the **same ambient space at the same cardinality**. Every row carries its own control, so
the reading is scale-free by construction — which is what round 2's failure showed was needed, region size
having turned out to be semantics rather than nuisance.

**Raw difference, not z-score**, and the reason was measured rather than assumed: across a 60× range of *r*
the control **mean** is flat (0.81–0.91) while the control **SD** varies 20×. Standardising would divide by
the one quantity still tracking region size. The standardized value ships beside every reading, unscored,
so the rejected choice stays visible.

## Provenance carried per reading

`measured_rate` · `control_mean` · `control_sd` · `excess` · `standardized_excess_UNSCORED` · `r` ·
`ambient_n` · `ambient_size` · `distinct_subsets_used` · `uniform_tuple_cap_for_reference` ·
`n_instances` · `control_draws` · `theorem_forced` · `marrow_excluded_row` · `insufficient`.

Seed `20260726`; 8 instances per row; 40 control draws per reading; distinct subsets only throughout.

## Three cheap additions, chosen to test the instrument's reach

`dominating-set`, `exact-cover-x3c` and `three-dimensional-matching` are **excluded from Marrow's closure
columns** — unbounded-arity constraint scopes, so no fixed finite template exists to take polymorphisms of.
The probe enumerates solutions directly and read all three. That is the geometry note's founding argument
demonstrated rather than asserted.

## Coverage and its limits, stated plainly

- **28 of 114 readings are INSUFFICIENT-r** (r < 10), nearly all `optimal` regions. Minimality means few
  members; this is round 2's entanglement finding seen from the other side.
- **Ten readings return exactly 0.0 while not flagged theorem-forced**, which surfaced a real gap in the
  hand-maintained FORCED table — banked as Q1, with an operational consequence for design law 3.
- **Some regions read positive excess** — more violating than random sets of their own size. Banked as Q2.

## What this is for

The survey produces a measured column and a set of questions with artifacts behind them. It does not
produce a finding, and the descriptive tables in the banked-questions file are explicitly not scored: the
sign of the easy/hard contrast is not stable across region kinds, which a design intending to score it
should know **before** looking.

Frozen bytes untouched. W-review unaffected.
