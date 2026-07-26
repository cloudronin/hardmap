# Sounding v3 — the excess statistic against a size-matched null

**Status: SPEC — DRAFT AWAITING SEAL. Nothing runs until this is sealed.**
**Date:** 2026-07-26 · **Supersedes:** nothing. Rounds 1–2 keep their verdicts and their measured profiles.

---

## Why the statistic changes

Round 2 filled the four-cell design and then failed its region-size floor: 6 of 17 rows in band, *r*
spanning 57× inside a single stratum. The diagnosis was not that tuning was done badly — it was that
**region size is semantics, not nuisance.** Minimality *means* few members; satisfiability *means* many.
Tuning them equal distorts the objects.

Which reframes the measurement problem: **comparing raw violation rates across rows was always comparing
sizes wearing geometry's clothes.**

The fix is not to model size or match it, but to give every row **its own size-matched control**. The
comparison stops being row-versus-row and becomes **region-versus-structureless-control**: how far does
this region's blend-survival deviate from what a featureless set *of identical size in an identical ambient
space* would show?

That is scale-free by construction, and it is the theoretically correct question rather than a clever
workaround. Closure structure means blending **better than random**. And the hard pole's signature — the
Austrin–Mossel line, that hard problems' solution sets impersonate randomness — predicts hard rows sit
**at** their random baseline while easy rows deviate **below** it. The statistic this design needs is
literally *distance from randomness*, which is what the two-pole picture said hardness was all along.

**Rounds 1–2's raw rates become inputs. The scored object becomes the excess.**

---

## 1. The control ensemble

For a row whose measured region is `R ⊆ D^n` with `|R| = r`:

- **Draw** `K` independent uniform random subsets `S ⊆ D^n` with `|S| = r`.
- **Matched on both** `r` (cardinality) **and** `n` (ambient dimension), with `D` the row's own domain.
  Both drive the combinatorics and matching only one would leave the other free to carry the confound.
- **Compute** each control's violation profile with the identical probe used on `R` — same flavours, same
  distinct-subsets-only rule, same subset cap.

**`K = 50` control draws per (row, region, flavour)**, each sampling up to **2,000 distinct m-subsets**.
Sized from the box below; the null needs more total work than the measurement, which is the correct
allocation.

## 2. The excess statistic — RAW DIFFERENCE, and the reason is measured not assumed

**Scored statistic: `excess = rate_measured − mean(rate_control)`.**

This was ruled *against* the prior expectation, after characterising the control empirically:

| n | N = 2ⁿ | r | null mean | null SD |
|---:|---:|---:|---:|---:|
| 11 | 2048 | 7 | 0.8700 | 0.1006 |
| 11 | 2048 | 20 | 0.8739 | 0.0331 |
| 12 | 4096 | 75 | 0.8908 | 0.0105 |
| 12 | 4096 | 120 | 0.8804 | 0.0087 |
| 13 | 8192 | 212 | 0.9056 | 0.0054 |
| 12 | 4096 | 443 | 0.8102 | 0.0081 |

- **A ratio is rejected**: the null sits near 0.87 for every row, so a ratio compresses all rows into a
  sliver near 1 and discards the resolution the statistic exists to provide.
- **A z-score is rejected**, and this is the non-obvious call. `(measured − null_mean) / null_SD` looks like
  the scale-free choice — but **the null SD varies 20× with r** (0.1006 at r=7 → 0.0054 at r=212) while
  **the null mean is stable within ~0.10 across a 60× range of r**. Standardising would divide by the one
  quantity that still tracks region size, **reintroducing the r-dependence through the denominator** —
  round 2's failure in a new hat.
- **The raw difference is therefore the comparable one**, and it is comparable *because the null mean is
  empirically flat*, not because differences are inherently comparable.

**Reported beside it, never scored:** the standardized excess `(measured − null_mean)/null_SD`, so a reader
can see what the rejected choice would have said.

## 3. F-scores restated in excess terms

- **X1 — calibration.** Theorem-forced pairings still return exactly 0.0 measured, so their excess is
  strongly negative and equals `−null_mean`. Forced; calibration only; excluded from every discovery
  statistic **by schema** (design law 3, already enforced in code).
- **X2 — the mechanism question.** *Direction sealed:* **decision-easy rows show MORE NEGATIVE excess**
  (their regions blend better than featureless sets of the same size); **decision-hard rows sit CLOSER TO
  ZERO** (their regions impersonate randomness). Tested within region kind and pooled across it — the
  excess is size-controlled, so pooling is legitimate here where it was not in round 2. **Both are
  reported.**
- **X3 — the within-family cut.** X2's separation, if any, inside families against within-family excess
  nulls. Terroir vocabulary verbatim: FAMILY-BORNE / GEOMETRY-RESIDUAL / MIXED / INSUFFICIENT.
- **X4 — registry.** Predictions filed before any literature contact. Standing.

## 4. INSUFFICIENT vocabulary

- **`INSUFFICIENT-r`** — `r < 10`. The control's SD is unstable there (0.1006 at r=7, a 19× inflation over
  r=212), so the excess is not estimable at usable precision. Counted, reported, excluded from scoring.
- **`INSUFFICIENT-degenerate`** — control SD ≈ 0, or the region is a single orbit with no distinct subsets.
- **`n.a.-encoding`** — continuous or permutation-structured regions, per design law 2.

Declared per row, never argued past.

## 5. Robustness only — option (a)

The 17-row regression of excess on `log r` **rides as a robustness check and is never primary**. If the
design works it should show **no residual r-dependence**; that is the check that the matched null did its
job, exactly as r-stratification was round 2's check that tuning did.

**And the denominator's own dependence is reported**: `corr(log r, null_SD)` ships in the artifact, because
the z-score was rejected on that ground and the evidence for the rejection must be visible.

## 6. Box, stated before building

- **Spec pass** (this document): judgment-bound, ~1–2 h. Done.
- **Build + run**: control machinery reuses the existing probe; ~50 × 17 × 4 × 2,000 ≈ 7M blend
  evaluations, **10–20 min compute**, ~2–3 h paired for the scoring and the artifact.
- **Total ≈ 3–5 h paired.** Inside a weekend, and stated before starting per standing rule.

## 7. What is not authorised

No new rows. No new encodings. No fleet expansion. **The seventeen rows keep their measured profiles and
those become this round's inputs.** W-review is untouched and remains open independently.
