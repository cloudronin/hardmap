# A1 — Pilot atlas (22 problems): population viable, gate MET

**Verdict:** The literature supports a multi-charge atlas at the required standard. Pilot cited coverage is
**83.3%** of applicable cells (90/108), **zero uncited-folklore**, verification-pass structure in place — the
A1 done-gate is **MET** and the population-failure kill (spec §5.1 / prereg) does **not** fire. Proceed to A2
(full ~120-problem atlas). $0 compute; literature + analysis only.

## What shipped

- **Product** `eightfold/` (fifth monorepo sibling): README, AGENTS.md (invariants), CHANGELOG, pyproject
  (stdlib-only core + `[analysis]` extra = numpy/scipy), CI leg.
- **Schema + validator** `atlas.py` (retargets a sibling project's corpus validator): `ProblemEntry`/`ChargeCell`
  dataclasses, 8 QC gates, loader, coverage accounting, `validate`/`summary` CLI. `charges.py`: the eight
  charge vocabularies + the entailment layer. `SCHEMA.md`, `CORPUS_PR_REVIEW_GUIDE.md`.
- **Pilot atlas** `results/atlas/atlas.jsonl` — 22 problems × 8 charges (176 cells), every real value a
  `claimed` citation to a stable anchor (Garey–Johnson 1979, Ausiello et al. 1999, primary papers — no `url`,
  so no R10 snapshot debt). Includes all decoupling witnesses: VC/CLIQUE (approx+param), permanent/determinant
  (counting+parallel), 2-SAT/Horn/XOR-SAT (counting+parallel), PHP (proof-size), LP/matching (parallel).
- **The Census backbone entered** as the single `measured` cell (R9): `random-3sat-refutation`'s landscape,
  citing the banked Census C2 experiment (prereg + c2_summary + seeds + code commit).
- **Structure harness** `structure.py` (Cramér's V, in-house MCA, hierarchical clustering, marginal occupancy
  + entailment triage, `--drop-measured` ablation) + `results/atlas/pilot_structure.json`.
- **28 tests** green (gates incl. R9/R10, loader, coverage/R2, entailment/R6, light-core import).

## Coverage (applicable = value ≠ n.a.; cited = claimed/confirmed/measured with a citation)

| charge | cited/applicable | open | n.a. |
|---|---|---|---|
| decision | 20/20 | 0 | 2 |
| counting | 16/17 | 1 | 5 |
| approximation | 12/13 | 1 | 9 |
| parameterized | 10/11 | 1 | 11 |
| parallelization | 5/9 | 4 | 13 |
| proof_size | 8/8 | 0 | 14 |
| average_case | 10/17 | 7 | 5 |
| landscape | 9/13 | 4 | 9 |
| **total** | **90/108 (83.3%)** | 18 | 68 |

The n.a. mass is real, not laziness (R2): parallelization is n.a. for the 13 NPC/PSPACE rows (E2); proof_size
applies only to the 8 refutation-family rows. The open cells (avg-case/landscape of worst-case-only problems)
are honest gaps to fill in A2 or leave as `open`.

## A finding from the build: two entailment rules were wrong (R6 earned its keep)

Rules **E6** (`inapprox ⟹ decision≠P`) and **E7** (`decision=P ⟹ no approx-hardness`) were drafted as
column-forbidding, then found **invalid for this atlas**: under R1 the approximation charge attaches to the
optimization object and the decision charge to the decision object, which can differ. **XOR-SAT is the
counterexample** — decision=P (GF(2) feasibility) yet MAX-3LIN is inapprox (Håstad 2001), so the cell
`(decision=P, approximation=inapprox)` is **occupied, not forbidden**. Leaving E6/E7 in would have converted
the atlas's most interesting decoupling into a false "theorem-forbidden" verdict — exactly the failure R6
guards against. They were demoted to informational (preconditions retained); the surviving column-forbidding
rules are **E1** (counting-FP ⟹ decision-P) and **E2** (parallel within P). Because H3's predicted forbidden
cells changed, the prereg was versioned **v1 → v2** (a changed prediction is a new version, not an edit — the
correction came from building the layer, before any analysis run).

## Structure preview (harness sanity-check — NOT the H1–H3 verdict)

N=22 is far too small to conclude; A3 on the full atlas is the verdict. What the harness shows it runs:

- **Occupancy respects the theorems:** every E1/E2-forbidden cell is empty in the data.
- **Clustering** recovers the CLIQUE≡Independent-Set multiplet, but plain 8-charge Hamming distance does *not*
  isolate the single-charge decouplings (permanent≡determinant cluster together) — a note for A3: use
  charge-weighted / subspace clustering.
- **Cramér's V** strongest pair is `approximation|parameterized` (0.747) — a *surprising* (non-entailed)
  association, the kind of signal H2 is after.
- **R4 tension is visible and healthy:** full-table MCA reports 10 dims > 1/Q but the complete-case block
  (n=9) reports 2 — the pilot is underpowered and missingness inflates the full-table count, which is exactly
  why H1 requires both analyses to agree (they can't at this N).
- **R9 ablation:** dropping the measured cell changes nothing (MCA 10→10, separation 0.160→0.167).

## Owner to-dos at review (R8)

- Promote ~2 cells/charge (≈16, decoupling-witness rows first) from `claimed` → `confirmed` after reading the
  primary source. Full-table confirmation is **not** an A1 requirement.
- Spot-check the honest `open` cells (avg-case/landscape) — fill or leave open for A2.

## Caveats

- All cells are agent-drafted `claimed`; none are owner-`confirmed` yet (by design, R8).
- The Census datum enters from **C2** (banked, done-gate MET); **C3** will refine it (spec sequencing).
- The structure numbers are a harness check at N=22, not evidence for or against H1–H3.
