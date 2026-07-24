# Absorption (arity-4) — does bounded-width structural tractability absorb the approx⟷param coupling?

> **⚠️ SUPERSEDED (2026-07-23) by [`Prism-v2-arity4-spec.md`](Prism-v2-arity4-spec.md) (sealed `prereg_v33`).** Review of
> the successor spec found this draft's central premise — that arity 4 makes the I6 localization-absorption test
> *askable* — **provably false**: on the param-real rows, unbounded-width-tractable = purely-affine (Schaefer), which the
> affine bridge nets out, so absorption is either untestable (one stratum) or non-independent (= the affine netting).
> This draft shared that blind spot with the owner's independently-drafted Prism v2, and its 4 h charging timebox +
> sampled fallback over-specced a cost that is actually seconds. The arity-4 experiment survives, **re-scoped** to the
> anti-canon Min-Ones replication (its sole sealed prize). Kept for provenance; do not execute from this file.

**Codename:** Absorption
**Status:** **SUPERSEDED** by Prism v2 — see banner above. (Originally: BANKED 2026-07-23, owner Q2 ruling.) Predictions
seal in a dedicated prereg (`prereg_v33`) **after owner review**, before any charge is computed on the roster. Nothing
runs without owner greenlight.
**Owner:** Vishnu
**Relation:** the arity-4 continuation of **Prism** (`Prism-v1-findings.md`, prereg_v32). Prism found the Foundry **I6
localization-absorption** headline **untestable at arity ≤3** because *bounded-width ⟺ tractability* there (the affine
obstruction to bounded width is vacuous below arity 4). This experiment goes to the smallest arity where a genuinely
**unbounded-width but tractable** relation exists — 4-ary parity `x₁⊕x₂⊕x₃⊕x₄=0` (affine ⇒ poly-time, yet not of
bounded width) — so that bounded-width finally *varies* on the param-real subset and absorption becomes measurable.

---

## 1. The one question

The atlas's most durable finding is the **approx⟷param coupling**. Prism decomposed the natural-population version of it
(v3's V=0.256) into a **theorem-forced part** (the affine off-diagonal, `affine ⟹ weakly-separable ⟹ FPT`, Marx Ex 2.4)
and a **non-affine residual** (pooled V 0.286, Min-Ones 0.459) that survives netting. **I6 asks a different, mechanistic
question:** is the coupling *carried by localness structure* — i.e. does conditioning on **bounded width** (the
Barto–Kozik structural-tractability charge) shrink it? If bounded-width absorbs the coupling, the coupling is (partly) a
re-expression of a relation's local consistency structure; if it does not, the coupling is orthogonal to localness. This
is the first **mechanism** test the program can run on the gradient, and arity 4 is the smallest roster on which it is
not vacuous.

**Why arity 4 and not more.** The absorption test needs bounded-width to vary *within the param-real rows*. At arity ≤3
every param-real relation is bounded-width (Prism §2), so there is exactly one stratum and nothing to condition on.
Arity 4 is where the affine unbounded-width-tractable class first appears. Going higher buys resolution at rapidly
growing charging cost; arity 4 is the **minimal decisive** roster and is specced as such.

## 2. Population and the enumeration lift (settled numbers)

- **Roster:** arity-4 Boolean relations = subsets of `{0,1}⁴` (16 tuples) ⇒ **2¹⁶ = 65 536 relations**. Symmetry-dedup
  by **S₄ coordinate permutation** (charges are permutation-invariant) ⇒ **exactly 3 984 symmetry classes** (Burnside
  over the 24 permutations; verified — `dev/prism_direction_check.py`-style one-off already run, cycle histogram
  `{6:6, 8:8, 10:3, 12:6, 16:1}`). The full natural population is **arity ≤4** = Prism's 90 (arity ≤3) **+ 3 984**
  (arity 4) = **4 074 classes**; the arity-4 tranche is what carries the bounded-width variation.
- **The lift is charging, not enumeration.** Enumerating + canonicalizing all 65 536 subsets is instant (≈1.5 M ops).
  The cost is **per-class oracle evaluation × 3 984** — ≈44× Prism's 90. The expensive oracle is the **general
  weak-separability** param check (Marx Def 2.1 guarded union), whose cost grows with arity; KSTW Max/Min-Ones and the
  bounded-width predicate are cheap. **This is exactly why I0 (below) is a hard gate.**

## 3. I-phase (verification + the sizing gate) — R0, before any prereg prediction is scored

**I0 — the sizing gate (owner-mandated).** Before committing to full charging: (a) compute the exact class count
(done: 3 984); (b) enumerate the classes and **micro-benchmark the per-class cost of every oracle** (especially
`is_weakly_separable_general` at arity 4) on a 100-class sample; (c) project `3 984 × per-class cost` against a **4-hour
charging timebox**. **Decision, logged before proceeding:**
  - projected ≤ timebox ⇒ **full-population charging** (all 3 984 classes);
  - projected > timebox ⇒ **sampled fallback**: draw a uniform-random sample of relations, symmetry-dedup, charge a
    bounded number of classes sized to the **effective-n floor** (below), report with sampling caveats and a
    per-stratum inhabitation table so no stratum is silently missed. The full-vs-sampled choice is a **recorded I0
    verdict**, not an in-flight improvisation.

**I-A — the make-or-break gate: bounded-width must actually vary.** Verify that at arity 4 **bounded-width ≠
tractability** — exhibit the affine 4-parity witness (`x₁⊕x₂⊕x₃⊕x₄=0`: affine ⇒ poly-time ⇒ decision P, param FPT, yet
**unbounded width**) and confirm the bounded-width marginal has **both values populated on the param-real subset**. If
bounded-width still collapses to tractability at arity 4 (marginal degeneracy again), the experiment is **UNTESTABLE and
halts** — declared on the marginal, exactly as Prism §2 did, never forced. This is promoted to a **sealed prediction**
(pred 2 below) because the whole experiment rides on it.

**I-B — oracle validity at arity 4.** The KSTW Max-Ones/Min-Ones approximation oracle and the Marx general
weak-separability param oracle were built and CI-locked at arity ≤3. Re-verify at arity 4: the guarded-union weak-sep
check must handle 4-ary relations correctly; the KSTW priority lists are arity-independent but each predicate check
(`is_width2affine`, `is_strongly_0valid`, `is_IHSB`) must be validated on 4-ary inputs. **Witness gate:** vertex-cover
and independent-set (as 4-ary gadgets or carried from arity ≤3) still land on opposite corners of both axes. Any oracle
that cannot be validated at arity 4 **drops to `open`** (its column is omitted, documented, not silently degraded).

**I-C — bounded-width characterization at arity 4.** Pin the Boolean bounded-width predicate at arity 4 before the
column fills, using Prism's corrected form (`(0-valid ∨ 1-valid)` trivial-satisfiability **first**, then
`horn ∨ dual-horn ∨ bijunctive`, **affine excluded**). At arity 4 the new unbounded-width-tractable class is exactly
**affine relations not also captured by horn/dual-horn/bijunctive** (4-parity and its cosets). Confirm the
characterization names them unbounded-width and names the trivially-satisfiable relations bounded-width (the same guard
that mattered at arity 3).

## 4. Pre-registered predictions (DRAFT — seal in `prereg_v33` after owner review, before charging)

1. **NPI calibration (known-answer):** the decision column contains no intermediate value (Schaefer). Violation ⇒
   pipeline failure, halt.
2. **Bounded-width marginal is non-degenerate on the param-real subset** (the I-A gate as a sealed bet): both
   bounded-width and unbounded-width param-real classes are populated, each ≥ a floor set at I0 on the class count.
   Failure ⇒ 3b/4 **UNTESTABLE**, declared on the marginal (not a discovery, a resolution limit).
3a. **Localization identity persists (raw, descriptive):** bounded-width⟷approximation is strong raw (KSTW encodes the
   localness determinants) and **nets to ≈0** — the entailment finding carries to arity 4.
3b. **Localization coupling (the real bet):** bounded-width⟷**parameterized** has a **nonzero netted residual** — now
   testable because bounded-width varies. Sealed direction: **positive** is *not* pre-committed; report the residual.
4. **The I6 headline — absorption:** conditioning approx⟷param on **bounded-width** shrinks V by **≥ half**
   (stratification, not netting; bounded-width now varies across the population, so this is legal as written). Findings
   note sealed now: because bounded-width is a function of KSTW's inputs, any absorption means *the coupling is carried
   by localness structure the approximation classification already encodes* — the entailment stated in the sentence, not
   left for a referee.
5. **Outlier persistence (carried from Prism pred 5):** no other charge pair's bridge-completed netted residual exceeds
   approx⟷param's, on the richer roster.
6. **Direction, the open question arity ≤3 left (sealed as a real bet):** the bridge-completed **non-affine residual**
   direction stays **non-positive** (Spearman < +0.1) — the canon's positive gradient does **not** emerge with more
   resolution; the arity-≤3 finding (pooled −0.142, Min-Ones −0.428 anti-canon) replicates. A **positive** result here
   would be the more interesting miss and is the reason to seal this rather than leave it descriptive. Report per
   objective (Max-Ones/Min-Ones) — Prism showed the objectives split.

**Standing rules inherited (binding):** marginals + distinct-profile counts read **before** any V; bootstrap CIs sized
to **symmetry classes / per-stratum class counts, never raw relations** (effective-n); per-pair shared-input netting +
the named-bridge layer (`affine⟹WS`), **both residual sets reported permanently**; NPI check first; no metric
substituted after seeing results; the **affine class traced** through every pairing (it is the tautology-breaker and the
new unbounded-width-tractable class — doubly load-bearing here).

## 5. Design (reuse Prism; the deltas are arity-4-specific)

- **Roster:** generalize `prism.build_roster` to arity 4 — `all_relations(4)` (subsets of `{0,1}⁴`), `canonical` under
  **S₄** (24 permutations, was S₃'s 6), `symmetry_classes`. Class sizes carried. Keep arity ≤3 available so the full
  arity-≤4 population (4 074 classes) can be assembled; the absorption analysis runs on the param-real subset of it.
- **Charges:** identical oracle set to Prism — decision/counting/localization/parallelization/approx-counting
  (classical) + approx_maxones/approx_minones (KSTW) + parameterized (Marx general weak-sep). All validated at arity 4
  in I-B before the columns fill.
- **Netting + matrix:** reuse `prism_matrix.py`'s `_netted` (per-pair shared-input) + `NETTING_INPUTS` (the `affine⟹WS`
  bridge). Both residual sets. Score predictions 2, 3a, 3b, 5, 6.
- **Conditioning analysis (prediction 4 — the new capability):** recompute approx⟷param **within bounded-width strata**;
  report stratified V per stratum, **pooled conditional V** (size-weighted), shrinkage fraction vs the roster's raw V,
  and CIs sized to per-stratum class counts. Thin strata (marginals-first will show it) ⇒ INSUFFICIENT RESOLUTION on
  prediction 4, declared on measurement quality.
- **Reporting:** both weightings (per-class; class-size-weighted); occupancy grids per charge pair; affine trace; raw
  **and** netted numbers always paired; the arity-4 unbounded-width-tractable classes named explicitly.

## 6. Milestones and done-gates

| M | Deliverable | Done-gate |
|---|---|---|
| **R0** | I0 sizing verdict + I-A/I-B/I-C verification + `prereg_v33` | I0 full-vs-sampled decision **logged**; I-A bounded-width variation **confirmed** (or halt UNTESTABLE); oracles validated at arity 4 (R20) or dropped to `open`; prereg sealed **after owner review**, before any column computed |
| **R1** | Charge columns (`prism.py` arity-4 path, `dev/absorption_build.py`) | NPI passes (pred 1) or halt; marginals + distinct-profile counts + **bounded-width marginal on param-real** (pred 2) persisted; class sizes carried |
| **R2** | Pairwise V matrix + netting (`dev/absorption_matrix.py`) | Every cell netted with logged derivation; preds 3a, 3b, 5, 6 scored; both residual sets paired |
| **R3** | Conditioning analysis (the I6 headline) | **Prediction 4 scored** (shrinkage fraction + CI) or INSUFFICIENT RESOLUTION declared |
| **R4** | Findings (`docs/findings/Absorption-findings.md`) + ledger | All predictions scored incl. misses; affine trace; the absorption verdict stated with its entailment caveat; four-wall / I6 implications posed **as questions for ruling, not rewrites** |

## 7. Kill criteria

1. **I-A fails (primary risk):** bounded-width still ⟺ tractability at arity 4 ⇒ **UNTESTABLE, halt** (same posture as
   Prism §2 at arity ≤3). The experiment's whole reason to exist is that this does *not* happen; verify it first.
2. **I0 underpowered:** if full charging exceeds the timebox **and** the sampled fallback cannot reach the effective-n
   floor for a legible absorption test ⇒ report underpowered, do not force a thin-strata verdict.
3. **Oracle validity (I-B):** any oracle uncheckable at arity 4 ⇒ its column drops to `open`, matrix proceeds without it
   (documented).
4. **Box:** $0 compute; 4-hour charging timebox (I0-enforced); no frozen-artifact contact; `is_weakly_separable`,
   `oracles.py`, eightfold untouched; `finer.classify_boolean` imported read-only.

## 8. Placement and sequencing

Independent hobby-research project; $0 compute; roster is generated, no curation contact. **Deferred behind the
preprint** (owner ruling 2026-07-23): the preprint is unambiguously next, and nothing in the queue — this included —
moves before it. Banked now while Prism context is hot so the arity-4 deltas (S₄ dedup, the 3 984 count, the arity-4
oracle-validity items, the absorption capability) are captured accurately. Inherits every standing discipline; nothing
decays by waiting. **On execution:** owner reviews the predictions and the I0 sizing verdict before `prereg_v33` seals;
the I-A gate is checked before any prediction is scored; the four-wall/I6 implications return to the owner as questions.
