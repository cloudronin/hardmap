# H4 — Sealed verification pass

Checklist sealed before running; every check scored; triage rule fixed in advance:

- **cosmetic** — fix and log.
- **material** — dated correction through the artifacts (the established protocol).
- **invalidating** — the claim leaves the preprint until resolved (pauses H5, not the consolidation).

Run against the public candidate at the H3 state (`hardmap repro --all` 8/8, `hardmap verify` green).

## Scorecard

| # | check | status | re-run |
|---|---|---|---|
| 1 | Statistic-implementation audit | **PASS** | `pytest hardmap/tests/test_audit.py` |
| 2 | Internal-coherence sweep | **PASS (6/6)** | `hardmap verify` |
| 3 | Oracle spot-check | **SET UP** (owner manual pass pending) | `python scripts/oracle_spotcheck_draw.py` |
| 4 | Pipeline determinism | **PASS** | fresh clone → `pip install -e .` → `hardmap repro --all` |
| 5 | Cross-artifact consistency | **PASS (8/8)** | `python scripts/cross_artifact_consistency.py` |

## 1. Statistic-implementation audit
Every helper computing a published number checked against an *independent* reference plus a hand toy
(the defect-#5 method, generalized):

- **Cramér's V** (`eightfold.structure.cramers_v`) vs a fully hand-computed 2×2 toy — bias-corrected
  V = 0.45934, matched. ✓
- **Corrected Spearman** (`foundry/dev/prism_v2_matrix.py:_spearman`) vs `scipy.stats.spearmanr` on
  tie-heavy toys: the corrected form matches scipy; the sealed buggy form (`_spearman_legacy`,
  `argsort∘argsort`) fabricates ~0.71 correlation from ties whose true rank-correlation is 0. This
  confirms the −0.564 / −0.140 direction numbers come from the corrected estimator and the buggy value
  is retained only as the on-record fork. ✓
- Bootstrap CIs and Cai–Chen netting are covered transitively: `repro` reproduces the committed seeded
  CIs exactly, and the coherence sweep asserts *netted ≤ raw* and *point ∈ CI*.

## 2. Internal-coherence sweep → `hardmap verify`
Six invariants over all persisted results, all PASS: Cramér's V ∈ [0,1]; Factors k* inside its verdict
interval; netted ≤ raw (Cai–Chen); point estimates inside their CIs (lattice V, corrected Spearman);
census Jaccard ∈ [0,1] and below the 0.95 plurality line; contingency marginals sum to n. Shipped as
the permanent `hardmap verify` command.

## 3. Oracle spot-check (owner manual pass)
`scripts/oracle_spotcheck_draw.py` draws, under **sealed seed 20260724**, 10 cited-filled classes per
charge column (79 rows) into [`H4-oracle-spotcheck-worksheet.md`](H4-oracle-spotcheck-worksheet.md). The
condition on each drawn class must be re-derived **by hand** against the cited theorem — the one check
that needs human judgment, not code. Sealing the seed fixes the sample before the manual audit begins.
**Pending.**

## 4. Pipeline determinism
Genuinely fresh clone of the candidate → clean venv → `pip install -e .` → `hardmap repro --all` 8/8 and
`hardmap verify` 6/6, both exit 0. The strongest determinism check; doubles as the install test.

## 5. Cross-artifact consistency
`scripts/cross_artifact_consistency.py`: all 8 headline numbers cited in the findings prose match
`results/`. One nuance logged (**cosmetic**): prose uses the unicode minus (U+2212) for negative
directions (−0.564, −0.140) while code and the manifest use ASCII; the values are identical and the
script normalizes the glyph.

## Findings & triage
- **cosmetic (logged):** unicode vs ASCII minus in prose for negative directions. No correctness impact.
- **material:** none.
- **invalidating:** none.

No finding pauses H5. The oracle spot-check (check 3) remains as an owner manual pass; completing it
closes H4 fully.
