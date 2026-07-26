# Terroir v1 — the anatomy-vs-sociology probe

**Prereg:** `prereg_v14` · **Date:** 2026-07-25 · **Verdict: FAMILY-BORNE**

Mosaic v3 Arm B left one honestly-unresolved number: `decision` lifted **+0.0684** over its fold-weighted
null (permutation p = 0.0033, Bonferroni-passing), and the run could not separate a genuine weak
anatomy→fate bridge from family-level regularity riding the feature matrix. Terroir decomposes that lift.

It makes **no new headline bet** — it attributes an already-scored statistic. Nothing here rescores Arm B;
the sealed `+0.0684 / p = 0.0033` is frozen and quoted, never rewritten.

---

## 0. What was sealed and what was disclosed

Two of the four planned analyses were **computed during grounding, before the seal**. A prereg claiming all
four were pre-committed would have been false, and undetectably so from the artifact. So `prereg_v14`
splits them:

| analysis | status | predictive credit |
|---|---|---|
| **A4** within-family residual | DISCLOSED — computed pre-seal | none |
| **A3** sociology hierarchy | DISCLOSED — disqualified pre-seal | none |
| **A1** encoding ablation | SEALED — unrun | full |
| **A2** indicator-free refit | SEALED — unrun | full |

One further piece of hygiene, recorded because it was a deliberate choice: the association between
`encoding_type` and `problem_family` was **not measured** during grounding, specifically so A1 would stay
sealable. A2's *premise* (missingness is family-patterned) was measured; A2's *outcome* was not. **Where
knowing a thing would have destroyed the only remaining sealable content, the grounding pass chose not to
know it.**

---

## 1. A4 — the verdict

Arm B's fold key **is `problem_family`**, so every family sits entirely inside one fold. The model never
trains on a family it predicts; it cannot memorise "graph → NPC" and must *infer* each family's base rate
from anatomy features alone. A4 therefore asks the hardest available version of the question: **having
inferred the base rate, did the model add anything on top of it?**

| family | n | modal-correct | model-correct | Δ | exact binomial p |
|---|---:|---:|---:|---:|---:|
| graph | 148 | 106 | 112 | +6 | 0.3158 |
| logic-proof | 49 | 17 | 10 | **−7** | **0.0359** |
| optimization | 58 | 47 | 48 | +1 | 0.8674 |
| **pooled (admissible)** | **255** | **170** | **170** | **±0** | — |

**Within-family lift = +0.0000.** Seven of ten families fail the power screen (n ≥ 30, modal < 0.90) and
are declared INSUFFICIENT rather than argued past. Against the headline **+0.0685**, family composition
accounts for **the entire scored lift**.

**The sharpest edge is not the zero — it is `logic-proof`.** On the one admissible family whose label
genuinely varies, the model scores **significantly worse than its own modal** (10/49 vs 17/49, p = 0.0359).
It imports a cross-family rule that is *actively wrong* there. That is **anti-signal, not absence of
signal**: a model carrying real anatomy information would not degrade below the base rate precisely where
the base rate is weakest.

The ±0 is exactly equal to its own null and trips the tidy-number gate. It is **discharged, not waived**,
by a complete integer identity: **+6 − 7 + 1 = 0**, each term printed above and checkable by hand.

---

## 2. A3 — retired, and the trap is worth more than the analysis

A3 would have regressed `decision` on the quarantined sociology sidecar. It cannot run, for one shallow
reason and one disqualifying one.

**Shallow:** sociology covers 227 of 345 natural rows (v3-new only). The `decision` fit ∩ sociology is
**225, not 336**, with null 0.5644 vs 0.5923 — the increment would not be commensurable with the statistic
it claims to decompose.

**Disqualifying: the atlas was expanded in charge-stratified waves, so admission bookkeeping encodes the
charge.**

| wave | n | composition |
|---|---:|---|
| W1 | 25 | P 21, NPC 4 |
| W2 | 67 | PH-complete 42, PSPACE 15, beyond-PSPACE 9, coNP 1 |
| **W3** | **123** | **NPC 123 — 100%** |
| **W4** | **10** | **P 10 — 100%** |

`admission_wave` alone scores **0.8711 against a 0.5644 null — a +0.31 "sociology lift" that is pure
recruitment artifact.** Published, it would have looked like the most decisive result the program has
produced.

Two sealed rules already forbade the exit, and both were written before anyone could have anticipated this
particular regression: `Anatomy-SCHEMA` §3.4 (*"a sociology column never enters a structural claim"*), and
the sidecar's `provenance_note`, which permits stratifying on `rn_membership` but not `source_funnel` —
and `rn_membership` is the one blessed field with exactly zero lift (16 rows, all NPC). **A rule that only
forbids what its author foresaw is a preference; a rule that blocks a case its author never imagined is a
law.**

**The general form, which is the finding:**

> **Any covariate correlated with how the corpus was built is a label proxy to the exact degree the
> building was outcome-stratified.**

That binds every future use of provenance fields on every wave-built artifact. It is the recruitment-design
sibling of the theorem-forced-credit trap: the study's construction, not the world, guaranteeing the
answer.

---

## 3. A1 and A2 — the sealed arm, scored honestly

The sealed prediction, on both: *the lift falls below half its size (< +0.0342) — the ANATOMY-RESIDUAL
survival threshold fails.* Disclosed in the prereg as weakening the bet: the sealed Arm B run **already**
showed that dropping `locality_class` alone moves the lift +0.0684 → +0.0327.

| run | acc | null | lift | Δ vs baseline | perm p | prediction |
|---|---:|---:|---:|---:|---:|---|
| baseline (matched re-run) | 0.6607 | 0.5923 | +0.0685 | — | — | reproduces the seal exactly |
| **A1** — drop `encoding_type` | 0.6399 | 0.5923 | **+0.0476** | −0.0208 | 0.0010 | **MISS** |
| **A2 primary** — impute absence | 0.4583 | 0.5923 | −0.1339 | −0.2024 | 0.9321 | HIT (nominally) |
| **A2 secondary** — coverage-stratified | 0.5902 | 0.5714 | **+0.0188** | −0.0497 | — | **HIT** |
| *post-hoc control* — drop absence columns | 0.5685 | 0.5923 | −0.0238 | −0.0923 | — | *diagnostic* |

**A1 is a miss and is reported as one.** `encoding_type` carries about 30% of the lift, not the majority,
and what remains is still significant at p = 0.0010. The bluntest family channel is *not* the carrier.

**A2's primary hit is worth less than it looks, and the artifact says so.** Imputation at a ~50% absence
rate does two things at once: it removes absence information (the hypothesis) *and* asserts a false
substantive value on 166/345 `arity_class` rows and 126/345 `objective_type` rows (not the hypothesis). A
manipulation that degrades the matrix by construction makes the prediction nearly unfalsifiable, so passing
it is weak evidence. The post-hoc control quantifies the split: dropping the absence-bearing columns costs
−0.0923, imputing them costs −0.2024, so **roughly half the primary's dramatic collapse is injected false
values rather than removed absence.**

**The informative number is the sealed secondary: +0.0188.** Within a coverage profile — where absence is
constant and nothing is imputed — the lift falls from +0.0685 to +0.0188, about 73% of it gone, across four
admissible profiles and 266 rows. Per-profile deltas: **+3, +1, +1, +0.**

Absence is not hypothetical here. It is a live model input four ways: `kernel_status.__missing__` (288/345),
`self_reducibility` as a *pure* absence flag (342 missing / 3 positives), `reduction_out_degree = −1.0`
(314/345), and a level literally named `open` that is the **plurality value of `arity_class` (166/345)** and
the second-largest of `objective_type` (126/345). Under indicator-free imputation, three of seven features
starve outright — they were carrying absence, not anatomy.

---

## 4. The converging picture

Two independent stratifications each dissolve the lift, and neither leaves a residual:

| stratification | n | lift |
|---|---:|---:|
| none (headline) | 336 | +0.0685 |
| within `problem_family` (A4) | 255 | **+0.0000** |
| within coverage profile (A2 secondary) | 266 | **+0.0188** |

The two strata are themselves correlated (V = 0.2924, p = 0.0002), so these are less two explanations than
two views of one fact: **the model is reading which literature recorded the row, not what the problem is.**

**Verdict: FAMILY-BORNE.** The natural-side bridge claim closes at this resolution. The prospective registry
(0/57, confound-free by construction) is the instrument that inherits the question — the close `prereg_v14`
and the Terroir spec §5 both pre-declared.

The program's sentence, in its current form:

> **Anatomy predicts fate on the synthetic side by theorem, shows no within-family signal on the natural
> side at this resolution, and the confound-free prospective test is armed and accumulating.**

---

## 5. What the gates caught, in both directions

**A ruling corrected by measuring it first.** The instruction was "route `open` to `__missing__` before any
refit." Measured before executing: on `arity_class`, `objective_type` and `locality_class` there is *no*
`__missing__` level at all, so the routing is a **pure relabel** — identical one-hot partition, identical
fit — and on `kernel_status` it would have **merged two different facts** (`open` = the literature has no
answer; `__missing__` = the row was not coded). Ruling updated to classify all three absence forms in the
analysis layer, preserving the distinction. *Logged against the owner.*

**The denominator gate, promoted after a third instance.** A lift is `acc − null`, and the subtraction is
only meaningful if both terms were computed on the same rows. Three times: Quarry v2's conditional
shrinkage; A3's 225-vs-336; and **A4's own first pass**, which mixed an admissible-only null with an
all-rows accuracy and reported **+0.0060 where the matched statistic is exactly 0**. Three is a class, not
an anecdote series — it is now `check_lift_denominators_match()` in `hardmap verify`, with a test that
plants a mismatch and asserts the gate fires.

**A gate scoped to one project's filenames has an expiry date.** The tidy-number gate's glob was
`grid_*results*.json`, so `terroir_v1_results.json` was invisible to it. Widened — and it immediately found
seven unacknowledged extremals in *older* artifacts. Two are real defects:

- `crucible_results.json`: a permutation p reported as **exactly 0**. With N permutations the honest form is
  `< 1/N`; 0 asserts an impossibility. (S1's verdict is unaffected — the real V is far outside the envelope
  either way.)
- `quarry_v2_results.json`: the absorption block never ran (`governed_by: power_check.cleared`,
  INSUFFICIENT-terminal), yet `unconditional_V` and `averaged_per_class_wrong` sit at **0.0** — uninitialised
  placeholders that read as measured values. The same block writes `shrinkage_fraction: null`, the correct
  idiom, so **the file's own author knew it and applied it inconsistently.**

These are itemised in the gate's `LEGACY` table rather than waived, each with its reading, and the gate stays
live on those files for anything new. Their verdicts are unaffected and their bytes are not rewritten here.

**And the seal produced a miss.** A1's prediction failed. A bet that only ever records its hits is a press
release, and the ledger now carries a Terroir miss beside its hits.

---

## Artifacts

`prereg_v14.json` · `terroir_v1_results.json` (A4 + A3 record) · `terroir_v1_ablations.json` (A1 + A2 +
secondary + control) · `terroir_a4.py` · `terroir_ablate.py` · 8 tests in `foundry/tests/test_grid.py` ·
`check_lift_denominators_match()` in `hardmap/verify.py`.

**Frozen and untouched:** `grid_arm_b_predictions.json` `cc5bb389` (asserted at every A4 run),
`atlas_v3.jsonl` `e62f3c28`, `anatomy_v1.jsonl` `8ff11f8a`.

---

## 6. Where this leaves the program

Terroir answers what Mosaic v3 could not: **the natural-side lift was fame all the way down.** On every
stratification available to these features — by family, by coverage profile — it dissolves, and nothing
worth the name survives.

The convergence with Arm A is worth stating, because neither arm knew about the other when it was sealed.
Arm A asked whether the algebraic classification is recoverable from raw combinatorics and **answered no:
surfaces see membership, not closure.** Terroir now closes the natural side at *exactly that resolution*.
Both arms failed at the same boundary, from opposite directions — one on a universe where the bridge is a
theorem, one on a universe where the charges are cited facts. **The retrospective route is closed at
surface grade, and the reason is the same reason both times.**

What that leaves open is correspondingly sharp, and it is genuinely open rather than merely unrun:
**whether closure-grade invariants — computed from pinned presentations rather than read off surface
descriptions — carry within-family signal.** Nothing measured here bears on that question. Terroir tested
surface-grade coordinates and found them to be sociology; it did not test, and could not have tested, the
anatomy the dichotomy theorems say is real. That is the shape of the next instrument, and no artifact in
this repository pre-registers it yet.

The one confound-free instrument already armed is the prospective registry (0/57, predict-then-fill,
clean by construction). It inherits the retrospective question. It does not answer the closure-grade one.
