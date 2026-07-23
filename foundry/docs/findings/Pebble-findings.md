# Sprint 6 "Pebble" — findings (P6 synthesis)

The substrate hypothesis proposes the charges are projections of one quantity: **reach** — how far information about a
partial solution propagates through the constraint structure. Sprint 6 built and tested reach's first instrument on
the synthetic census. The result is honest and mixed, and the discipline that produced it is as much the finding as
the numbers. **Physics note (bridge hunt, `Pebble-bridge-hunt.md`, 2026-07-22): reach = the literature's point-to-set
correlation length = reconstruction = clustering α_d. Every phenomenon sentence below cites an owned object; the
contribution is the instrument and the census measurement, never the object.**

## Headline

1. The pairwise instruments (`corr`, `forcing`) were **DISQUALIFIED** for reach — they measure point-to-point
   correlation, and reach is point-to-**set**; parity is invisible to them.
2. A **point-to-set instrument was built and QUALIFIED** (boundary-shell bucketing), after one redesign.
3. Reach on the Boolean census is a **real, algebraic dichotomy** — affine long / bounded-width short, tracking the
   Schaefer split — that **strengthens with n** (not finite-size), with a **minority relation-level residue** (0.45 of
   the class gap, vs Sprint 4.6 terrain's decisive ~1.0).
4. Reach is **terrain-relevant** (predicts `landscape` incrementally, +0.096 held-out) — but a **free relation-level
   scalar (`tuple_dispersion`) is a cheap proxy** for it (corr 0.78), carrying most of its terrain content.
5. The substrate hypothesis's actual test — the **differential pattern across the charges** — remains **untested at
   v1 scale**, structurally (the discriminating charges are clone-constant; v1 has ~13 strata).

## The arc, in order (each step a sealed prereg + a scored verdict)

| step | prereg | verdict |
|---|---|---|
| Pilot: does `tuple_dispersion` decay with size? | v12 | INCONCLUSIVE underpowered → replicated at +0.7 on 16-fold roster (P1) |
| `corr`/`forcing` reach instrument, three-pole calibration | v17 | QUALIFIED `corr` (pairwise) |
| **Parity diagnostic** — reach is point-to-set, not pairwise | v20 | **`corr` DISQUALIFIED** (parity reads 0.03 at maximal propagation) |
| Point-to-set instrument + hand-count gate | v21 | built; sensitivity + specificity locked |
| Point-to-set calibration | v22/v23 | **QUALIFIED** (parity inverted to the top group; strict-single-max clause withdrawn) |
| Full sweep — dichotomy, within-class replication, size ladder | v24 | dichotomy REAL + algebraic + 0.45 residue |
| **T1.1/P4** — is the residue terrain-relevant? | v25 | **INCREMENTAL** (+0.096, p≈0) |
| **T1.2** — are reach and `tuple_dispersion` the same property? | (map) | **PROXY** (corr 0.78) |

## What earns its keep, and what carries forward

- **The expensive instrument earns a modest keep.** Reach adds a real +0.096 held-out increment over the free scalar
  for terrain (P4) — from the ~22% of reach's variance the scalar does not share (T1.2). **Correctly-attributed
  caveat:** reach and `ruggedness` are both solution-set-geometry summaries of the *same ensemble* (measured on
  different draws — seeds 980000+i vs 981000+i — so an ensemble-level relationship, not a same-sample tautology), so
  the contest against the *constraint-level* `tuple_dispersion` was **structurally uneven**, not a fair fight reach
  won on merit. The un-circular test — reach vs a **non-geometry** charge — is phase-2.
- **The free scalar carries forward at scale.** `tuple_dispersion` is a cheap proxy for reach (0.78), computable on
  anything with identifiable constraint relations — including the canon rows where sampling cannot reach. This is the
  T1.4-direction payoff, established here for free: at scale, the cheap number substitutes for the expensive
  instrument with modest loss.

## Methods chapter — two specification defects and one construct-validity error, one of each species

This sprint produced one instance of each of two distinct failure species; a methods chapter that names them (with
dates and owners) is more useful than one that anonymizes them.

- **Owner specification defect #1 — the "parity single-max" clause** (prereg_v22, `cc8bc14`, 2026-07-22). The pass
  criterion demanded parity outrank its own affine class-mate (2-affine), which no physics produces; caught by the
  measurement (co-top within noise), **withdrawn post-result, dated and flagged**.
- **Owner specification defect #2 — the direction-blind (c) trigger** (prereg_v24, `7daba39`, 2026-07-22). The
  finite-size trigger fired on gap *magnitude*, blind to whether the levels converge (artifact) or diverge (real
  dichotomy); caught by the measurement (divergence), refuted by a *pre-data* directional reading.
- **Builder construct-validity error — the pairwise blindness** encoded in `test_parity_blind_but_2affine_visible`
  (`166eec4`, 2026-07-22). The test recorded that pure parity reads zero on the pairwise observable; it survived P2
  qualification and the start of the P3 harness build **filed as a pole-selection technicality, not a construct-
  validity failure** — until a parallel investigation (I-SP) read it correctly.

**The lesson:** *specification errors* (the criterion was worded wrong) and *construct-validity errors* (the
instrument doesn't measure the target construct) are different species. The first is caught by disagreeing with the
measurement's verdict; the second is caught by asking whether the measurement measures the thing at all — and the
program's own tests can encode the second before anyone reads it. Both were caught by measurement, neither by review.

## Program status (against the test map)

- **Tier 1 (does the expensive instrument earn its existence?)** — substantially answered: qualified, characterized,
  earns a modest keep; the free scalar is a proxy that carries forward. T1.3 (structural race, v13) and T1.4
  (scalarization, v14) remain sealed-and-unrun; T1.2-PROXY is evidence the T1.4 ceiling is approachable.
- **Tier 2 (does the measure predict the charges differentially — the actual hypothesis?)** — **UNTESTED at v1
  scale.** The within-co-clone regime reaches only `landscape` (+ thinly `average_case`); the discriminating charges
  are clone-constant, so the between regime has ~13 strata and v1 structurally cannot adjudicate the uniform null.
  This is the honest end-state: **instrument built and characterized, hypothesis untested at scale.**
- **Two-level not gradient (T2.3, prereg_v23):** now measured, not just predicted — the phase-2 differential should
  expect two levels with a minority residue, not a strong/moderate/weak/none gradient.

## Standing discipline (honored across v12–v25)

Prereg before measurement; known-answer calibration before unknown sky; population/provenance gates before
interpretation (the P3 sweep declared 5 unmeasurable cells, not averaged); beat your own nulls (P4 permutation p≈0);
bridge hunt before novelty language (physics cited, not claimed); sealed predictions scored as they land including
the misses (the pilot's INCONCLUSIVE, the parity DISQUALIFICATION); **no metric substituted after seeing results —
specification errors recorded as dated owner errors, never as threshold adjustments.**
