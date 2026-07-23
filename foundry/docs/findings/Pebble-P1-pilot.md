# Sprint 6 "Pebble" — P1 pilot: does `tuple_dispersion`'s predictive power decay with size?

**Two-stage P1.** An initial arity-3, 8-fold run was **underpowered** (INCONCLUSIVE with held-out CIs spanning
zero) and exposed a power problem; it also caught a verdict-logic bug. The roster was then expanded to the full
Sprint 4.6 16-fold roster (arity 3+4) and the pilot re-run — **that expanded run is P1's real result** (owner ruling;
prereg_v15 sealed the roster + ladder change before its verdict was seen).

## Headline (the honest, bounded claim)

> Local relation geometry (`tuple_dispersion`) predicts global solution geometry (`ruggedness`) **out-of-sample,
> strongly (~0.64–0.74) and stably across n=8–20**, **replicating Sprint 4.6 on an independent arity-4 roster**.
> **Whether that relationship attenuates with size — the propagation signature — remains unresolved: a 30% decline
> is not excluded.**

**What this is, and is not.** The *predictor* is strong and stable; that is **not** the same as the substrate
hypothesis getting its first datum, and the two come apart:

- Sprint 4.6 experiment B already established that `tuple_dispersion` predicts terrain out-of-sample at **+0.74**.
  The expanded pilot **replicates that on a new roster** (16 arity-4 co-clones — real, independent corroboration)
  and adds that it **holds across the size ladder**.
- It does **not** add evidence of **propagation**. Propagation was supposed to appear as *attenuation with
  distance/size*; the whole point of the decay diagnostic is that **a static predictor holding flat is compatible
  with plain compositional inheritance**. A flat, strong predictor does not distinguish the two.
- Therefore the **substrate hypothesis is neither supported nor damaged by this pilot — it is untested.** The
  pilot's real contributions are (a) the **replication** on an independent arity-4 roster and (b) the **exclusion of
  the arity-3 negative as a few-folds artifact**.

## The question and the two formulas, side by side (mandatory disclosure)

The pilot asks whether a **local, relation-level** geometry statistic predicts a **global, solution-set** geometry
statistic, and whether that prediction survives as instances grow. The two are computed from **different objects by
structurally similar means**, so the reader can judge the resemblance directly:

| | `tuple_dispersion(R)` — the predictor | `ruggedness(sols).score` — the target |
|---|---|---|
| object | the relation's **satisfying tuples** (a handful) | **sampled solutions** of a random CSP instance (many) |
| core stat | mean pairwise **Hamming distance**, normalized by arity | mean pairwise **spin-overlap** `q = 2·agree−1` |
| formula | `mean_{i<j} Hamming(t_i,t_j)/arity` | `1 − max(0, (mean_q − q_rand)/(1 − q_rand))`, `q_rand = 2/|D|−1` |
| direction | higher = tuples more spread | higher = solutions spread like random draws (rugged) |

Both are mean-pairwise-spread measures; the sealed sign of the relationship is POSITIVE (prereg_v11).

## Expanded run — P1's real result (16 folds, ladder [8,12,16,20])

| n | held-out power (leave-one-co-clone-out, 16 folds) | bootstrap 95% CI |
|---|---|---|
| 8 | +0.692 | (0.538, 0.784) |
| 12 | +0.664 | — |
| 16 | +0.736 | — |
| 20 | +0.637 | (0.405, 0.768) |

first→last relative drop = **7.9%** (< 30% threshold); `within_noise = true`.

**Verdict (sealed R-1, ladder-agnostic first→last band): INCONCLUSIVE** — on the specific decay question. The drop is
within the bootstrap noise band and a ≥30% attenuation is **not excluded**: a 30% decline from 0.692 → 0.484 lies
inside the n=20 CI (0.41–0.77). So neither *attenuating* nor *undiminished* is earned.

But this INCONCLUSIVE is unlike the arity-3 one: the held-out power is **strong and significant** (measured-band CIs
0.54–0.78 and 0.41–0.77, both well above zero) and **flat** across sizes. What is unresolved is narrow — not "is
there signal?" (yes, firmly, and it replicates +0.74) but "does that signal *additionally* attenuate with size?"

### Operationalization note (flagged, routed to phase-2 — deliberately NOT acted on now)

The `within_noise` test is CI-overlap between first/last bands, which routes a *flat / no-measurable-attenuation*
result to INCONCLUSIVE rather than UNDIMINISHED (undiminished-as-coded requires a *resolved small decline*). So this
verdict reflects both genuine CI width and that quirk. It is **left unchanged**: the sealed code returns INCONCLUSIVE
faithfully, and changing the test after seeing an unsatisfying label would be exactly the metric-swap the discipline
forbids. Phase-2 fix (recorded, not applied): a direct bootstrap CI on the *drop itself* to cleanly separate
flat-undiminished from unresolved-inconclusive.

## Initial arity-3 run (the underpowered probe) + the bug it caught

8 folds, ladder [12,18,24,30]: held-out power +0.226 / +0.124 / −0.366 / −0.604, with the n=12 CI (−0.44, +0.55)
already spanning zero → INCONCLUSIVE. The negative large-n values were a **few-folds instability artifact** (the
expanded 16-fold run replaces them with a stable ~0.7). Per prereg_v15, the two runs differ in **both** roster and
ladder, so **no cross-run size comparison is valid**.

Verdict-logic bug caught here and fixed (`decide_verdict`): the code had ANDed an extra `drop<30%` onto the
INCONCLUSIVE branch, absent from the sealed rule, mislabelling a within-noise large-drop case as UNDIMINISHED.
Corrected from the same numbers → INCONCLUSIVE (the *more conservative* label; fixing broken logic is not arguing a
verdict back).

## Consequence for P2/P4

`tuple_dispersion` is now the **baseline to beat**. Because a strong, stable static local→global predictor is already
established, ξ's within-co-clone test at P4 must show **incremental predictive power over `tuple_dispersion`**, not
merely predictive power on its own — otherwise ξ could look successful while measuring exactly what the free scalar
already captures (the scalarization question arriving early). Sealed in the prereg before P2 is built.
