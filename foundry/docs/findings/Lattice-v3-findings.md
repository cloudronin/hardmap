# Lattice v3 (G2, prereg_v31) — findings: a weak coupling *is* present in the natural generated universe

The clean test. Neither the census representatives (v1, too coarse) nor a stratum-spanning selection (v2, FPT-biased)
could measure the approx⟷param coupling. v3 measures it on the **natural, unselected population**: every non-trivial
Boolean relation of arity ≤ 3, deduped up to coordinate permutation, × {Min-Ones, Max-Ones}. The answer is a **weak but
real coupling** — present, far below the canon's 0.73, and *not* a clean monotonic gradient.

## 1. The measurement

| quantity | value |
|---|---|
| raw relations (arity ≤ 3) | 270 |
| **symmetry classes** (effective population) | **90** |
| rows (classes × 2 objectives) | 180 |
| both-real rows | 166 |
| distinct profiles | 9 |
| parameterized marginal | **80 FPT : 86 W[1]** (balanced) |
| **Cramér's V** (canon statistic) | **0.256** |
| **bootstrap CI₉₅** (sized to the 166 class-rows) | **(0.13, 0.398)** |
| Spearman direction (ordinal) | **0.019** |

**The CI excludes 0: a coupling is present.** But it is **weak** — a quarter of the canon's 0.73 — and the **balanced
param marginal (80:86)** confirms the earlier scares were artifacts: v1's poverty was the census representatives, v2's
7:1 skew was the canonical-first selection. The natural population carries genuine variation on both axes.

## 2. What kind of coupling — nominal, not a gradient

The **Spearman is ~0**, so this is a *nominal association*, not the canon's monotonic gradient. The occupancy shows why:

| approximation (easy→hard) | FPT | W[1] | leans |
|---|---|---|---|
| PO | 64 | 62 | balanced (the dominant cell) |
| APX-complete | 11 | 4 | **FPT** — the affine off-diagonal |
| poly-APX-complete | 3 | 16 | **W[1]** — canon direction |
| decidable-not-approximable | 1 | 4 | W[1] — canon direction |
| Nearest-Codeword-complete | 1 | 0 | (thin) |

Two opposing effects produce a weak net V with no monotonic trend:
- **On-diagonal (canon direction):** the *hardest* approximation strata (poly-APX-complete, decidable-not-approximable)
  lean **W[1]** — harder-to-approximate co-occurs with harder-parameterized, exactly the canon's sign.
- **Off-diagonal (against it):** **APX-complete leans FPT** — this is the **affine cell**, precisely the
  `(approx-hard, param-easy)` off-diagonal that G1 identified as the tautology-breaker. Affine relations are
  APX-complete-ish on Max-Ones yet weakly separable (FPT). The same cell that proved the two charges are *independent
  partitions* is the one that **flattens the monotonic gradient** here.
- **The dominant PO cell is param-balanced (64:62)**, washing out the ordinal trend entirely.

So the natural generated universe contains **a real but weak, non-monotonic coupling**: the hard end tracks the canon's
direction, but the affine off-diagonal and the balanced easy end keep it from being a clean gradient.

## 3. Scoring the sealed prediction (prereg_v31)

Sealed before the parameterized column was computed on the 270 (with v2's 7:1 marginal disclosed as seen):

| clause | prediction | outcome |
|---|---|---|
| coupling present | yes | **HIT** — V=0.256, CI (0.13, 0.398) excludes 0 |
| magnitude | V ≈ 0.15–0.35, weaker than 0.73 | **HIT** — 0.256, CI within/around the band; ¼ of 0.73 |
| direction | positive, matching the canon | **PARTIAL** — positive in the hard strata, but Spearman ≈ 0 overall (the affine off-diagonal + balanced PO cancel the monotonic trend) |
| natural marginal less skewed than v2's 7:1 | yes | **HIT** — 80:86, balanced |

Net: **present + weak = hit; clean positive direction = miss.** The coupling is real but it is *not* the canon's gradient
in miniature — it is a weaker, non-monotonic nominal association, and the reason it is non-monotonic is the very
off-diagonal cell the program has been tracking since G1.

## 4. What this means — the coupling is *partly* computational, not purely curation

This is the finding the whole Lattice arc was built to reach, and it is genuinely two-sided:

- **Not purely a selection effect.** A coupling survives in the *unselected* generated Boolean population (V=0.256,
  CI excludes 0). Approximation-hardness and parameterization-hardness are **not independent** even with no human
  choosing the problems. Something computational is there.
- **But not the canon's gradient, either.** 0.256 is a quarter of 0.73, and it is non-monotonic. The canon's strong,
  clean gradient is **not reproduced** on the generated proxy. Its strength owes to something the generated Boolean
  universe lacks — the curated global-objective problems (Ferry's 31 `n.a.` rows), or the specific curated set.

The honest synthesis: **a weak, non-monotonic coupling exists in the natural generated universe** — not purely a
selection effect, and not the canon's gradient either. The 0.73-vs-0.256 gap is attributable to **curation** (humans
chose the canon's rows) and/or **population composition** (the canon contains global-objective problems no generated
roster reaches) — two confounded differences v3 **cannot separate**, so the gap is **not yet decomposed** (not "the
canon amplifies it 4×", which would assert a curation mechanism v3 did not isolate). And because v3's coupling is
*nominal* (Spearman ≈ 0) while the canon's is *monotonic*, what v3 found may be a **related-but-different coupling
shape**, not the same gradient at lower volume. Both the decomposition (curation vs population composition) and the
shape question (same gradient weaker, vs different coupling) stay **open**.

## 5. Scope (sealed, carried from the prereg)

v3's V is the natural coupling over the **reachable proxy universe** — single-relation Boolean, two objectives — **not
"the gradient outside the canon" full stop.** The generation-cannot-reach finding still stands: global-objective
problems remain unreachable, and this proxy is the *best* population generation can honestly produce, which is exactly
why measuring it is worth doing. Comparability to 0.73 is fair only on the **curated-vs-generated axis**; both numbers
stay population-scoped (0.73 = curated-not-stratified canon; 0.256 = generated-not-stratified Boolean proxy).

## The Lattice arc, closed

**v1** — the census *representatives* are too coarse (5 profiles, INSUFFICIENT RESOLUTION); the pipeline works (witness
gate passes). **v2** — the Boolean *universe spans* the strata (6 profiles), refuting Wall 3's coarseness claim; but a
stratum-spanning selection is FPT-biased and cannot measure the coupling. **v3** — on the *natural* population, a **weak,
non-monotonic coupling is present (V=0.256, CI (0.13, 0.398))** but far below the canon's 0.73. Not purely curation,
not the canon's gradient either; the 0.73-vs-0.256 gap (curation and/or population composition) and the shape question
(same gradient weaker, vs different coupling) stay open.

## Discipline honored

Prereg (`prereg_v31`) with a *sealed prediction* (not just procedure) committed before the parameterized column on the
270; v2's marginal disclosed as seen (mild contamination, stated); effective-n reported (raw 270 / 90 symmetry classes
/ 9 profiles) and the V's CI sized to the class count, not the raw rows; occupancy primary; V population-scoped, not
decontextualized against 0.73; sealed prediction scored including the direction miss; `is_weakly_separable` and
`oracles.py` untouched. Artifact: `results/lattice/lattice_v3_occupancy.json`.
