# A4 — The charge atlas: Move One, closed

**What Move One asked:** *Is hardness a vector?* Build the first quantitative charge atlas of
computational problems (rows = problems, columns = 8 literature-sourced hardness charges), then run
blind structure detection over it.

**What the atlas answers:**

> **Yes — and one piece of the vector's structure is load-bearing.** Hardness is multi-dimensional
> (H1: not scalar), and its empty regions separate cleanly into theorem-forbidden cells and a small,
> falsifiable **gap frontier** (H3). But the finding that **survived every adversarial check** (§8) is the
> **approximation⟷parameterized gradient** — harder-to-approximate tracks harder-to-parameterize — beyond a
> type-respecting null, beyond row-dedup, at p<0.001, and against the field's known violators. The single
> sharpest empirical yield is not a structure but a *hole*: the **counting-folklore gap** — for ~⅔ of
> well-studied problems the field assumes, but has never published, the #P-completeness of the counting
> version. **Honest riders, banked under prereg (§8):** part of H1's dimensionality is definitional (eight
> formal objects cannot collapse to one axis) — and Crucible's null model shows the dimension *count* is
> fully typing-driven; the multiplet *amplifications* likewise do not exceed typing. The load-bearing
> empirical claims are the **gradient**, the **folklore gap**, and the two gap-frontier facts — not the
> dimension count, and not the amplification magnitudes.

Instrument: [`atlas.jsonl`](../../eightfold/results/atlas/atlas.jsonl) — **118 problems × 8 charges**,
citation-gated, validator-clean, **zero uncited-folklore**. Verdict run:
[`A3-structure.md`](A3-structure.md) / [`a3_structure.json`](../../eightfold/results/atlas/a3_structure.json).
Prereg: [`prereg_v5.json`](../../eightfold/results/prereg/prereg_v5.json) (`committed_before_analysis: true`).
Sub-findings: [A1 pilot](A1-pilot.md) · [A2 setup](A2-setup.md) · [counting-folklore gap](counting-folklore-gap.md) · [I1–I4](I1-I4-investigation.md).

> **Crucible (v1.1) note.** §§1–7 report the A3 verdicts on the **frozen 118-row atlas**. **§8** records the
> adversarial self-review (prereg_v6) that hardened them: the approx⟷parameterized gradient survived every
> attack; H1's dimension count and the H2 amplifications were **resized** honestly. Read §2/§5 with §8.

---

## 1. What was built — the instrument, and why it can be trusted

An atlas is only as good as its discipline about *not knowing*. The build enforced, mechanically:

- **Unknown ≠ zero.** Every cell is a cited real value or an explicit sentinel (`open`/`unmeasured`/`n.a.`);
  sentinels are never imputed. Coverage is measured over *applicable* cells (R2).
- **Correct-and-cited beats plausible-but-uncited.** The A1 gate required **zero** `uncited-folklore`;
  the F-1 audit (below) enforced it retroactively, re-opening ~48 fabricated counting cells rather than
  shipping them.
- **One formal object per charge (R1).** decision measures a decision problem, counting the #-version,
  approximation the optimization version, landscape a random ensemble — pinned per cell, because the
  eight charges are *not* properties of the same object. This single discipline turns out to explain a
  large share of the structure (§5).
- **Blind analysis.** Coding, predicted signatures, and kill thresholds were locked in the prereg
  before any structure run; changed predictions became new prereg versions (v1→v5), never edits.

The result is a **map of what the field has and has not established**, not a map of what is plausibly
true. That distinction is the whole point.

---

## 2. The three verdicts

**H1 — hardness is a vector: SUPPORTED.** ≥3 effective MCA dimensions in the full table (16), the
sentinel-free complete-case block (5, n=19), *and* under every leave-one-charge-out (min 13); the
scalar-hardness kill-gate did not fire. (Honest anchor: the full-table 16 is inflated by sentinel
categories — the complete-case 5 carries the verdict.) **→ Crucible §8 resizes this: the dimension *count*
is typing-driven (inside the null envelope); "not scalar" holds, the count is not a discovery.**

**H2 — multiplets exist: SUPPORTED, and bridge-audited.** The two canonical witnesses re-separate in
their predicted subspaces (permanent/determinant; vertex-cover/clique). The atlas's densest multiplet is
the **APX-complete × FPT** cluster (22 problems — the textbook NP-hard combinatorial-optimization
signature). The headline check was **R25**: does that cluster survive subtraction of the *wide*
approximability→FPT bridge (Cai–Chen, MAX SNP / MIN F⁺Π₁ membership ⟹ FPT), not just the narrow
EPTAS↔FPT one? It does — netting out the theorem-forced members moves the approx⟷param association
**0.73 → 0.72 → 0.70 → 0.68** even when the *entire* cluster is deleted, because the coupling is the full
monotone gradient (`inapprox`→W-hard, `PTAS`/`APX`→FPT), not one cell. **→ Crucible §8 resizes the multiplet
*amplifications*: under a type-respecting null they do not exceed typing (the R11 metric has a positive
bias). The pairs separate as predicted, but the earned finding is the *gradient* — which survives S1, S2,
S3, and S5.**

**H3 — forbidden regions & gaps: SUPPORTED.** All 16 theorem-forbidden cells (E1: counting-FP⟹decision-P;
E2: parallelization only within P) are empty in the data — the entailment layer is consistent with the
corpus. The run emits 123 raw candidate gaps, triaging to the frontier of §4.

**One approving word on method.** `family_separation` came out **low** (0.15): the coarse `problem_family`
labels do *not* cluster in charge space. That is the healthy outcome — the analysis was deliberately
structured so textbook families *could* fail to cluster, and they did, which means the multiplets that
*did* form (§H2) were earned by the charges, not smuggled in by the row labels.

---

## 3. The headline finding — the counting-folklore gap

The sharpest single entry in the atlas is a measured absence. Counting is the charge where the field's
practice and the field's published record diverge most:

> Of 118 problems, **86 have an applicable counting version, and only 37 carry a published per-problem
> #P-completeness (or FP) result — 43%.** The other **49 applicable cells are open**: the community
> *assumes*, by default, that the counting version of an NP-hard problem is #P-complete — this is the
> standard working assumption, and it is exactly the pattern the atlas's own builder fell into (the F-1
> audit caught ~48 auto-stamped counting cells and re-opened them) — yet for roughly two-thirds of
> well-studied problems **no one has published the proof.** This is not sparse curation; it is a
> measured gap in what counting-complexity theory has actually established. Every decision-vs-counting
> decoupling witness the atlas relies on (permanent/determinant, 2-SAT, matching, reachability) sits in
> the *cited* 37 — the classical results are real; it is the long tail that is folklore.

Written up in full at [counting-folklore-gap.md](counting-folklore-gap.md). It is the clearest
demonstration that a citation-gated atlas surfaces *unasked questions* a plausibility-filled table would
have hidden.

---

## 4. The gap frontier — two facts, not 56 cells

The gap list's value is not its 123 raw cells (67 are R1 object-mismatch: exotic decision classes crossed
with optimization/ensemble charges whose object barely exists there). After triage, the interesting
residual collapses to **two structural facts**:

1. **The NP-intermediate bestiary is thin.** The entire `NPI-candidate` decision row is 6 problems —
   `factoring`, `discrete-log`, `quadratic-residuosity`, `graph-isomorphism`, `group-isomorphism`,
   `mcsp` — all cryptographic/algebraic or meta-complexity, and each under-characterized on the other
   seven charges. Most `NPI × X` cells are empty not because a natural inhabitant is hiding but because
   *natural NP-intermediate problems themselves are rare*. That is a crisp, citable observation about the
   shape of the complexity universe, and it falls out of the atlas in one line.

2. **The rigorous average-case × landscape frontier is uninhabited.** No problem in the atlas is *both*
   provably hard-on-average *and* has a proven clustering/OGP geometry: `hard-on-average-provable` =
   {permanent, SIS, LWE} (lattice/algebraic) and `clustering-proven` = {xor-sat, vertex-cover, clique,
   independent-set, number-partitioning, max-cut} (random combinatorial) **share no row.** This is the
   sharpest "should an inhabitant exist?" question the atlas raises: is there a random ensemble that is at
   once provably hard-on-average and provably clustered? And it is notably one **our own instrument line
   is equipped to attack** — the Census freezing/clustering measurement backbone can measure the
   solution-space geometry of candidate ensembles directly, turning this gap from a question into an
   experiment.

---

## 5. What it means — deep, or the R1 partition?

The intellectually honest question about H1 is whether the multi-dimensionality is *deep* or merely the
type-of-object partition that R1 builds in. The answer is **both, and the split is the finding**:

- **Definitional (not a discovery):** the eight charges attach to eight different formal objects, which
  *cannot* collapse onto one axis in any faithfully-typed atlas. Some of H1's dimension count is the price
  of taking R1 seriously — it would appear whether or not hardness "really" factors. **Crucible now puts a
  number on "some" (§8): statistically it is essentially *all* — the real dimension count sits inside a
  type-respecting null envelope, so the count is a consequence of typing, not a discovery.** Reporting it as
  a discovery would over-claim.
- **Empirical (the real yield):** *which* charges co-vary is not forced by object-type. The **approx⟷param
  gradient** — which survived both the Cai–Chen bridge subtraction (R25) *and* every Crucible attack (§8:
  null model, dedup, p<0.001, adversarial roster) — is the earned structure. The permanent/determinant and
  vertex-cover/clique **multiplets** separate as predicted, but their *amplification* does not exceed typing
  under the S1 null (§8) — so the earned claim there is "the pairs decouple where theory says," not "the
  decoupling is beyond chance." The counting-folklore gap and the two frontier facts of §4 are also earned.

**Bottom line for Move One:** hardness is a vector (not scalar); its one load-bearing empirical axis is the
approx⟷param gradient, which survived adversarial self-review; and the atlas's most valuable outputs are the
*holes* it makes visible — the counting-folklore gap and the average-case/landscape frontier — precisely
because the citation gate refused to paper them over.

---

## 6. Move-Two prerequisites

Move Two (predict-and-populate: use the structure to place bets on uninhabited cells) needs, in order:

1. **Build the object-existence predicate first — before any v2 roster work.** The gap list's biggest
   weakness is that 67/123 cells are R1 object-mismatch, separated here by a hand rule. Move Two needs a
   first-class predicate — *does the optimization/ensemble version of this problem exist at all?* — so
   gaps auto-partition into "no such object" vs "object exists, uninhabited." Without it, every
   gap-ranking is contaminated by type-mismatch noise; with it, the gap list becomes a ranked research
   agenda. This is the first investment, ahead of adding problems or charges.
2. **Attack the average-case × landscape frontier with the instrument line (§4.2).** It is the one gap
   the existing Census measurement backbone can address empirically — spec candidate ensembles, measure
   clustering geometry, and check the provable-hardness side against the crypto/lattice literature.
3. **Net the entailed component out of the whole Cramér's V matrix, R25-style.** The headline pair is now
   fully audited (EPTAS↔FPT + Cai–Chen); the same identify-theorem → pin-scope-from-sources →
   classify-members → net-out → report-range procedure should run on every association before it is
   called surprising.
4. **Backfill counting (the folklore gap).** Every counting-involving gap inherits the 49-open sparsity;
   resolving even part of the folklore gap re-populates that slice and sharpens the decision-vs-counting
   multiplet.
5. **A candidate v2 charge 9 — fine-grained complexity** (SETH/3SUM/APSP). Recorded for the record; it is
   the natural next column once the object-existence predicate exists to type it.

---

## 7. Provenance & honest caveats

- **Verdicts:** [`a3_structure.json`](../../eightfold/results/atlas/a3_structure.json) via
  `python -m eightfold.structure --a3`; in-house MCA / Cramér's V / subspace clustering / R25 audit
  (numpy+scipy only). Prereg_v5, `committed_before_analysis: true`.
- **Corpus:** 118 problems, validator exit 0, zero `uncited-folklore`, core per-charge A2 gate PASS
  (decision 97 / approximation 89 / parameterized 90); counting reported as a frontier column (43% cited)
  per the measured-density reclassification (prereg_v5, with the core-gate FAIL preserved on the record).
- **Tests:** 61 green (A3 harness + the Crucible S1–S5 harness + `derived`-status gates), locking the
  harness and the verdict *rules* (not the outcomes).
- **Caveats — three of A4's original caveats are now *tested*, not open (Crucible §8, prereg_v6):**
  row-independence (→ S2 dedup), the absence of p-values (→ S3, permutation p=0.0001), and
  sociology-of-study (→ S5 adversarial roster). The n=19 anchor was *not* grown (S4 deferred — S1 showed the
  count is typing-driven regardless of n). Remaining caveats: `family_separation` is a coarse-label
  diagnostic; the gap-list object-mismatch triage is a hand rule pending prerequisite #1; the R25
  problem-level syntactic-class classification is my reading of the class definitions (Π₁-definability),
  source-verified for the *theorem scope* but not per-problem-cited; measured cells (Census backbone) are
  load-bearing for no structural claim (`--drop-measured` unchanged, and now `--drop-derived` likewise).

---

## 8. Crucible results — adversarial self-review (v1.1)

Before any external motion, the five strongest referee attacks were run *by us*, under
[`prereg_v6.json`](../../eightfold/results/prereg/prereg_v6.json) (`committed_before_analysis: true`, locked
before any real-data run). Machine output: [`crucible_results.json`](../../eightfold/results/atlas/crucible_results.json).
Every verdict is banked; a RESIZED verdict is stated at its new size, never argued back.

**Roster provenance (Rider A).** All numbers in §§1–7 describe the **frozen 118-row atlas** (`atlas.jsonl`,
sha256 `6d53a4f1…`). S5 adds one violator (`k-means`), kept in a separate
[`s5_violators.jsonl`](../../eightfold/results/atlas/s5_violators.jsonl); the **augmented** roster (119) is
used *only* where labelled "augmented" below.

**The flagship survived every attack.** The approximation⟷parameterized gradient:

| Attack | What it tests | Result | Verdict |
|---|---|---|---|
| **S1** null model (M=1000) | structure beyond typing | real V=**0.73** vs type-respecting null p97.5=**0.38** | **SURVIVES** |
| **S2** dedup (114 classes) | row-independence | V 0.73 → **0.68**, permutation p=**0.0003** | **SURVIVES** |
| **S3** significance | the p-value the atlas lacked | permutation **p=0.0001** (10k) | **SURVIVES** |
| **S5** adversarial roster (augmented 119) | sociology-of-study | +k-means: 0.73→**0.66**, p=**0.0001** | **SURVIVES** (weakens-but-persists, exactly as prereg'd) |

**Two claims RESIZED — honestly, and not argued back:**

- **H1 dimensionality → the dimension *count* is typing-driven.** S1's null preserves typing (the `n.a.`
  mask) + per-charge marginals and destroys cross-charge structure. The real complete-case dims (5) sit
  *inside* the null envelope [p2.5=5, mean=7.4, p97.5=10] — at the **low** end: the real atlas is *more
  correlated* (fewer effective axes) than typing predicts, not more dimensional. **This is the number §5's
  word "Some" was missing:** the dimension count is (statistically) a consequence of R1 typing, not of
  empirical structure in excess of it. "Not scalar" still holds — complete-case dims ≥3 in **96%** of
  bootstraps (S3) — but H1's *earned* content is the gradient, not the dimension count.
- **H2 witness amplifications → not beyond typing.** Under the S1 null, permanent/determinant amplifies
  *less* than a random pair (0.29 vs null mean 0.35) and vertex-cover/clique sits inside the envelope (0.42
  vs p97.5=0.50). The pairs *do* separate replicably in their predicted subspaces (100% positive where
  present in the S3 bootstrap), but the R11 amplification metric (in-subspace − full-8 distance) carries a
  **positive bias** the null exposes — so the amplification is not distinguishable from typing. **§2's "the
  multiplet is genuine" resizes to: the pairs separate as predicted, but the separation does not exceed what
  typing produces by chance.** *(Interpretation only, per owner rider: a bias-corrected, null-calibrated
  amplification metric is a labelled re-analysis under a new prereg, run only after this writeup exists —
  never a mid-Crucible instrument swap that would let RESIZED argue itself back to SURVIVES.)*

**What is now settled.** The gradient — harder-to-approximate ⟷ harder-to-parameterize — is the
load-bearing empirical finding: beyond typing (S1), robust to collapsing reduction-equivalent rows (S2),
p<0.001 (S3), and weakens-but-persists against the field's known violators (S5 — seven already in the
frozen roster + k-means; violators are not abundant, so the gradient is not roster sociology). The
counting-folklore gap (§3) is untouched by these attacks and stands. **S4 (grow the n=19 anchor) was
deferred:** S1 showed the dimension count is typing-driven regardless of n, so anchor-growth is no longer
load-bearing; the `derived`-status machinery is built and tested for a later pass.

**Crucible ledger.** S1 gradient **SURVIVES** / S1 H1-dims **RESIZED** / S1 H2-amplification **RESIZED** ·
S2 **SURVIVES** · S3 **SURVIVES** · S4 **deferred** · S5 **SURVIVES**.

---

**Move One is closed, and hardened.** The atlas exists, it is honest about its holes, and — Crucible now
shows — its *load-bearing* finding, the approx⟷parameterized gradient, survives every check brought against
it: the null model, dedup, a p<0.001, and an adversarial roster. Two claims resized honestly along the way
(§8) — the dimension count is typing-driven, and the multiplet amplifications do not exceed typing. Nothing
shipped until that was on the record.
