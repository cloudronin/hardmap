# The hardening figure — a descriptive note

**Status: EXPLORATORY, ILLUSTRATION-GRADE. Not citable as a result.** No verdict, no prediction, no scored
statistic. Built entirely from assets already frozen.
**Date:** 2026-07-26 · **Figures:** `plots/hardening-sat2.svg`, `plots/hardening-shidoku.svg`
**Manifest:** `n7_hardening_manifest.json`

---

## What the row choice was, and why

The directive said to check the GAP records before choosing. `sat-3` has **2 usable steps of 5** —
positions 2 and 3 `INSUFFICIENT` (r = 9, 7), position 4 `GAP-no-region` — which is exactly the gap-ridden
condition its own fallback rule names. **`sat-2` has 5 usable of 5.** The fallback triggered on its stated
criterion rather than on preference.

## Panel set A — hardening

One declared instance per step, chosen by a seed and recorded, never chosen by looking at the data.

| clause/var | solutions | mean pairwise overlap |
|---:|---:|---:|
| 0.4 | 1,152 | 0.5398 |
| 0.7 | 672 | 0.5629 |
| 1.0 | 128 | 0.5801 |
| 1.3 | **16** | **0.8000** |
| 1.6 | 42 | 0.7111 |

The freedom dial falls by two orders of magnitude and the coherence dial rises. That is the phenomenon the
epigraph describes, drawn.

**One honesty note the figure cannot hide and should not.** The freedom dial is **not monotone**: 16 at
ratio 1.3, then 42 at 1.6. That is the declared-single-instance convention showing its cost — the step's
three instances had sizes [18, 16, 56] and [5, 20, 42], and the seed picked 16 and 42. The ladder's
*means* over three instances run 30 then 22, monotone. **A single seeded instance is a fair draw, not a
smooth one**, and the panel shows the draw rather than the mean because that is what was asked for.

## Panel set B — loosening

The same three panels run backwards on Shidoku's clue-removal ramp.

| clues | solutions | mean pairwise overlap | state |
|---:|---:|---:|---|
| 12 | — | — | **GAP-no-region** |
| 8 | 2 | 0.7500 | INSUFFICIENT |
| 6 | 1 | — *(no pairs exist)* | INSUFFICIENT |
| 4 | 6 | 0.6000 | INSUFFICIENT |
| 2 | 24 | 0.4293 | usable |
| 0 | **288** | **0.2480** | usable |

The cloud grows from a point to the full 288-grid space and the coherence dial falls monotonically,
0.75 → 0.25. Constraint-loosening is hardening run backwards, on the row whose endpoint is independently
known.

The 12-clue step is drawn as a **×**, never interpolated across. The 8/6/4-clue steps are drawn — their
regions exist — and flagged `‡`, because a reading ruled inadmissible is not the same as silence. At 6
clues the single solution admits **no pairs at all**, so the coherence dial is blank rather than zero.

## What the panels are and are not

The scatter panels are **projections capturing 24% (sat-2) and 35% (Shidoku) of variance in two
components**. That is a weak picture and the caption says so on the figure. They are illustration.

**The overlap-distribution panel is the projection-free signal** and is the only one any future claim could
rest on. Bimodality there would be honest evidence of clustering; a visually clumpy scatter would not be.

Bimodality was therefore **measured, not eyeballed** — bimodality coefficient per step, stored in the
manifest. **0 of 8 measurable steps exceed the 0.555 flag**, maximum 0.5271. See **Q17**.

## The two hooks, recorded as observations and banked

Per the directive, both are one-sentence descriptive glances with no mechanism language, banked rather
than narrated. See **Q16** and **Q17**.

## Provenance

Solution sets regenerated through `terrain_score.replay` from the frozen ramp-manifest seeds; every step's
replay reproduces its frozen reading. Instance choice seeded at `SEED + ramp_position` and recorded per
step alongside all instance sizes. Projection fit **once** on the pooled union across steps — a per-step
refit rotates the space and manufactures motion, which is the single most available way to make a figure
of this kind lie.
