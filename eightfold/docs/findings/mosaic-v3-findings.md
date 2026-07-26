# Mosaic v3 — the bridge grid: the program's first non-circular prediction run

**Date:** 2026-07-25. Seals: `prereg_v12` (G0) + its G1 registry addendum + its G2 membership/closure
amendment. Anchors by hash: `anatomy_v1` `8ff11f8a`, `atlas_v3` `e62f3c28`, ledger pins `b532c0d`.
Companion notes: `arm-a-surface-vs-closure.md`, `arm-b-natural-bridge.md`. Bridge table:
`bridge-table-v1.json`. Nothing rescores.

## What this run was, and what it replaced

Mosaic v3 rev-3 could not seal. Its flagship estimator was **circular by construction**: on the Boolean
universe the charges are *computed from* the Post flags by the dichotomy oracles, so predicting charges from
coordinates that include `poly_fingerprint` asked a model to recover a function from its own inputs — 46
flag-vectors → 46 profiles, zero ambiguity, a **100% lookup ceiling**. The spec's own netting rule
(*"headline accuracy is net-of-forced"*) zeroed its own headline when applied honestly. That is the
discipline catching its author (methods 21).

Re-posed against measured ground, the run asks two questions that are not theorems.

## Two findings that ship regardless of either arm

**1. The coverage wall.** Exactly **2** objectives have pinned oracle coverage (Min-Ones, Max-Ones) against a
floor of 3 — and more decisively, **only one of eight charges responds to the objective at all**. Seven of
eight charge×objective components are *definitionally* zero. A grid whose treatment is the objective has a
1-charge × 2-level design space on this universe.

**2. The determinism, and the re-centering it forces.** On the Boolean universe the dichotomy theorems
**are** the bridge, proven cell by cell. That universe therefore **cannot test the bridge hypothesis,
because there it is not a hypothesis.** The empirical question lives *entirely* on the natural side, where
charges are **cited facts about the literature** rather than computed functions of structure. Arm B was
rev-3's banked sideshow; it is the main event. **That inversion is a discovery about the question, not a
concession.**

## Arm A — the algebra is not surface-recoverable

> **Surfaces see what a problem *contains*, not what it is *closed under* — and hardness lives in the
> closure.**

Every genuine closure property sits at or below its fold-weighted null (worst: `dualhorn` −0.171). The three
nominal positives rest on nulls of 0.95–0.98, so their lifts are noise. Joint headline lands *at* the null
(exact-profile 0.217 vs 0.219).

**The positive control is what makes this a finding rather than a null:** the same pipeline, features and
folds recover single-tuple membership at **0.983 / 1.000**. It learns what surfaces show and not what they
don't. That is a **type boundary**, not a broken fit — the strongest shape a negative can take.

## Arm B — one charge moves, three do not

| charge | n | null | with locality | lift |
|---|---|---|---|---|
| **decision** | 336 | 0.5923 | **0.6607** | **+0.0684** (permutation p = 0.0033, passes Bonferroni) |
| approximation | 154 | 0.4221 | 0.4286 | +0.0065 |
| counting | 51 | 0.8627 | 0.8627 | 0.0000 |
| parameterized | 129 | 0.6434 | 0.5969 | −0.0465 |

**Channel 2 was a real test that could have gone the other way.** The blind coders received `problem_name`,
so `locality_class` might have encoded charge knowledge. Measured: dependence is **+0.026 to +0.036** — live
but minor — and **`decision` clears its null at +0.0327 with `locality_class` removed entirely.** The one
positive does not rest on the coded column. Reported with the same neutrality a damning result would have
received.

**The interpretation stays split, and the split is genuinely hard here.** `decision` is the coarsest charge;
its lift may be family-level regularity ("graph problems tend to be NP-complete") rather than anatomy. Folds
group by `problem_family`, but **`encoding_type` correlates with family by construction**, so this design
cannot isolate anatomy from sociology on this population. Notably, **that is exactly the regression the
Anatomy sociology sidecar was quarantined for.**

**Arm A constrains what the lift can be:** since closure leaves no surface fingerprint, `decision`'s
accuracy is **not** hidden algebra-recovery. The Boolean arm could not test the bridge — it told us what the
natural arm's result *cannot be*.

## The bridge table, v1

`bridge-table-v1.json` — 27 cells, with **PROVEN and MEASURED mechanically distinguished**: 8 PROVEN-NETTED,
4 PROVEN-ISLAND, 2 UNPINNABLE, 2 OPEN, 10 MEASURED.

> **A MEASURED cell is never upgraded to PROVEN by any accuracy, and a PROVEN cell is never "confirmed" by a
> measurement that agrees with it. They answer different questions.** A table that blurs them is the thing
> this program exists not to produce.

## Open, with the next probe named

- **The anatomy-vs-sociology probe (banked, cheap, designed):** add the canon-proximity covariates —
  `source_funnel`, compendium membership, rn membership — and ask whether `decision`'s lift **survives**
  them. That is the sidecar's stated purpose, and it is the probe that could split the two live readings.
  Banked here, not sealed now.
- **The engine-split bet** (Ledger §3, engine→approx / engine→param) remains **OPEN and unspent** — invariant
  by the Galois connection, variance-healthy at its sealed binary collapse, `bet_history` exposure NONE.
- **The prospective registry stands at 0/57** toward its pre-pinned floor. It is the honest instrument for
  what this run could not settle: **predict-then-fill grades against answers that do not exist yet**, family
  regularities and all, so it has no family-confound problem by construction.

## What the run cost and what it caught

Two bugs died before becoming findings, **both in the miss direction** — a hash encoder imposing arbitrary
order on unordered categories (the fix moved `decision` +0.009 → +0.068) and an encoder that broke seed
discipline below the model layer (592/475/278 across runs). With defect #15's fabricated hit and rev-3's
circular P4, **the ledger now contains errors caught in both directions** — which is when scoring honesty in
both directions stops being a slogan (methods 22).

**The program's first non-circular prediction run ends at its true size: one weak, real,
honestly-unresolved positive; two findings that ship regardless; and the endgame instrument standing ready.**
