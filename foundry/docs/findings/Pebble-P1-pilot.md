# Sprint 6 "Pebble" — P1 pilot: does `tuple_dispersion`'s predictive power decay with size?

**Status:** INCONCLUSIVE on the initial arity-3 roster (this run). **This is not P1's final result** — the pilot
exposed a power problem that gates the whole sprint, so the roster is being expanded (arity-4, more folds) and the
pilot re-run; the expanded verdict stands as P1's real result (owner ruling). This run is recorded immutably first,
underpowered result and bug-catch included, before the roster is touched.

Prereg: `prereg_v12` (sealed R-1 rule). Data: Sprint 4.6 apparatus, 48 arity-3 relations across 8 co-clone profiles
(6 reps each), ruggedness re-measured across a size sweep.

## The question and the two formulas, side by side (mandatory disclosure)

The pilot asks whether a **local, relation-level** geometry statistic predicts a **global, solution-set** geometry
statistic, and whether that prediction survives as instances grow. The reader must be able to judge the resemblance
of the two quantities directly, because they are computed from **different objects by structurally similar means**:

| | `tuple_dispersion(R)` — the predictor | `ruggedness(sols).score` — the target |
|---|---|---|
| object | the relation's **satisfying tuples** (a handful) | **sampled solutions** of a random CSP instance (many) |
| core stat | mean pairwise **Hamming distance**, normalized by arity | mean pairwise **spin-overlap** `q = 2·agree−1` |
| formula | `mean_{i<j} Hamming(t_i,t_j)/arity` | `1 − max(0, (mean_q − q_rand)/(1 − q_rand))`, `q_rand = 2/|D|−1` |
| direction | higher = tuples more spread | higher = solutions spread like random draws (rugged) |

Both are **mean-pairwise-spread** measures; both increase with spread; the sealed sign of the relationship is
POSITIVE (prereg_v11, matched: spread tuples → rugged solution set). The pilot is whether that relation-level→
solution-level link, fit on some co-clones, **generalizes to held-out co-clones**, and how it behaves with size.

## Result (leave-one-co-clone-out, 8 folds; bootstrap 95% CI)

| n | held-out power (pooled corr of predicted vs actual ruggedness) | bootstrap 95% CI |
|---|---|---|
| 12 | +0.226 | (−0.44, +0.55) |
| 18 | +0.124 | — |
| 24 | −0.366 | — |
| 30 | −0.604 | (−0.78, −0.013) |

`within_noise_band = true` (the n=12 and n=30 CIs overlap on (−0.44, −0.013)).

## Verdict: **INCONCLUSIVE** (sealed R-1: "trend within the bootstrap noise band")

The point estimates **decline monotonically and flip sign** (anti-prediction at large n) — which *looks* like strong
attenuation. But the measurement cannot resolve it: the **n=12 CI (−0.44, +0.55) already spans zero and both
signs**, and the smallest/largest CIs overlap. Per the sealed rule, INCONCLUSIVE is declared on **measurement
quality**, not argued from the point estimates. With 8 co-clone folds and leave-one-out, the pilot is underpowered.

### Verdict-logic bug caught and corrected (toward the *more conservative* verdict)

The pilot code first printed **UNDIMINISHED**. That was a bug, disclosed here in full:

- The sealed R-1 rule makes INCONCLUSIVE depend on **one** condition — is the trend within the noise band? — with
  **no** drop-size qualifier. The code had ANDed an extra `drop < 30%` onto its INCONCLUSIVE branch, so a
  within-noise case with a **large** drop fell through to `else` → UNDIMINISHED.
- That label is also substantively wrong for this data: "undiminished / no measurable attenuation" describes power
  that *holds up*, but the point estimate **collapses** +0.23 → −0.60.
- Fix: `decide_verdict()` now applies the seal in priority order (within-noise → INCONCLUSIVE; else drop≥30% →
  ATTENUATING; else → UNDIMINISHED). Recomputed from the **same** measurement numbers → INCONCLUSIVE. The
  `pebble_pilot.json` carries the corrected verdict, the original code label, and a provenance note; the per-band
  numbers are unchanged. **Fixing broken verdict logic is not arguing a verdict back** — and the correction moves
  away from a cleaner-sounding claim toward the conservative one.

## Honest meaning

- **No "first datum" for the substrate hypothesis.** Neither the propagation framing (attenuating → finite range)
  nor the construction framing (undiminished → compositional inheritance) is earned. The pilot is a null **on
  measurement quality**.
- **§3.0 gate is satisfied** (verdict stated before the instrument): ξ (P2) will be built as a **fresh** instrument
  whose framing this pilot does *not* pre-decide.
- **The power problem is now the sprint's gate.** The same held-out-by-co-clone design (few folds, wide CIs) is what
  P4's within-co-clone ξ→terrain test relies on. Before P2, the roster is expanded (arity-4, more co-clones, more
  folds, wider leave-one-out) and the pilot re-run. **If the expanded pilot still cannot resolve attenuation, that
  is a genuine finding about the phenomenon's effect size — not a roster artifact.**
