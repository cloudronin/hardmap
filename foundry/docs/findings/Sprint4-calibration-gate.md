# Sprint 4 · Task 1c — calibration gate  [OWNER-REVIEW CHECKPOINT — before the long runs]

**Verdict: the solution-side instrument QUALIFIES (two-pole Vega passes), but calibration surfaces a genuine
scientific finding that reshapes I6 — bounded-width is NOT a uniform "smooth" class.** The instrument is built,
its two structurally-different samplers concord tightly, and the affine-exact ground truth confirms near-zero
sampler bias. But the census's bounded-width families split: the Horn/semilattice sub-family reads smooth while
the majority (2-SAT) and the domain-3 order/median families read nearly as rugged as affine. The I6 direction is
weakly consistent (+0.11) but is a *gradient tracking the specific polymorphism*, not the binary width dichotomy.
This is a real, measured result; it needs an owner ruling before the (cheap) full measurement + scoring runs.

Reproduce: `python foundry/dev/calibration_gate.py` (numbers below). Instrument: [`solscape.py`](../../foundry/solscape.py),
[`ensemble.py`](../../foundry/ensemble.py); tests [`test_solscape.py`](../../tests/test_solscape.py). 44 foundry +
72 eightfold tests green. No oracle cell touched; eightfold byte-identical.

---

## 1. The instrument (net-new, pure-Python, no SAT-solver dependency)

Native domain-general random-CSP instances (Boolean and |D|=3, no CNF encoding needed on the solution side).
Two **structurally-different** samplers (R-c): `sample_dpll` (systematic randomized backtracking) and
`sample_walksat` (stochastic local search). `sample_affine_exact` samples the linear solution coset **uniformly**
via Gaussian elimination over GF(p) — unbiased ground truth on the affine arm. Provenance is `sampled-population`
throughout (R-d). Metric (after two redesigns, R-e budget): the density sweep showed solution-graph
**fragmentation is a solution-COUNT artifact** (it tracks sample density, not geometry — discarded from the
score); the robust, domain-comparable signal is **excess mean overlap above the random-agreement baseline**
(`q_random = 2/|D|-1`): clustered solutions (consensus) = smooth; solutions spread like random draws = rugged.

## 2. Two-pole Vega (R-b) — PASSES, and the smooth pole is instructive

| pole | family | pooled ruggedness | reads |
|---|---|---|---|
| known-rugged | k-XOR (affine) | **0.998** | rugged ✓ |
| known-smooth | Horn | **0.829** | smooth ✓ |
| (invalid smooth) | 2-SAT | 0.885 | **rugged** — 2-SAT is NOT a valid smooth pole |

Separation XOR↔Horn = **0.169 ≥ 0.12 → PASS**. The instrument is calibrated at both poles (not "only ever reads
rugged"). But note: had we used the 2-SAT-class as the smooth pole (as R-b offered as an option), Vega would
**fail** (separation 0.113) — because 2-SAT's random solution space is itself spread. **Horn is the valid smooth
pole; 2-SAT is not.** That is the first face of the finding below.

## 3. Sampler concordance + the affine-exact bias deliverable (R-c)

- **Concordance:** across all 14 families, the max dpll↔walksat ruggedness gap is **0.037** — the two
  structurally-different samplers agree tightly. No reading rests on one sampler.
- **Sampler bias, measured directly (the R-c bonus):** on the affine arm, exact-vs-biased gap = **dpll 0.005,
  walksat 0.005**. The restart/local-search samplers are near-unbiased where we can check them against ground
  truth — the only place in the program sampler bias is directly measurable, and it is negligible.

## 4. The 14-family landscape table — the finding

Pooled ruggedness (dpll+walksat, 4 instances each), all decision-P, at per-family satisfiable-regime densities:

| arm | family | ruggedness | |
|---|---|---|---|
| **affine (unbounded-width)** | zerovalid-affine, onevalid-affine, lin-eq-z3 | 0.998–0.999 | rugged |
| | lin-eq-z3-b, **xor-sat** | 0.978, 0.956 | rugged |
| **bounded-width** | **horn-sat, dual-horn, 0/1-valid-horn** | **0.829–0.841** | **smooth** |
| | 2-sat, 0/1-valid-bijunctive | 0.885–0.900 | mid |
| | **order-3, median-3** | **0.927** | **nearly rugged** |

- affine mean **0.986**, bounded mean **0.875**, separation **+0.111** (I6-consistent direction).
- **But the bounded arm spans 0.83–0.93**, and the separation is carried almost entirely by the Horn/semilattice
  sub-family. Ruggedness tracks the **specific polymorphism**: semilattice (Horn, min/max) → clustered/smooth;
  majority (2-SAT) → mid; the domain-3 order/median → nearly as spread as affine. The oracle's **binary**
  `localization` charge (bounded vs unbounded) does **not** capture this gradient.

**What this means for I6.** As a clean "bounded-width ⇒ smooth" dichotomy, I6 is **weak** — a permutation test
will likely find the direction but the binary predictor is a poor fit. As a *refined* claim — "solution-space
ruggedness tracks the tractability-giving polymorphism, and it is NOT reducible to the width bit" — this is a
genuine measured cross-structure the theorems don't hand you (the interesting outcome for a measured column).

## 5. Honest caveats

1. **Density-sensitivity.** Ruggedness depends on α (solutions spread at low density, cluster near threshold).
   I measured each family in its satisfiable regime, but "matched density" (prereg_v5) needs a principled
   definition — e.g. matched fraction-of-threshold or matched solution-entropy — before the numbers above are
   treated as final rather than indicative.
2. **Partial theorem-adjacency.** The qualitative direction (affine solution spaces are linear-algebraically
   spread; Horn solution sets are lattices that concentrate on the least model) is *theory-anticipated*, akin to
   how R-e frames the proof-side as BSW-consistency-grade. The genuinely-measured content is the **quantitative
   gradient across bounded-width polymorphisms** and the fact that width alone does not predict it.
3. **Small n.** n = 12–16 (fast, pure-Python). Larger n is cheap to add if the design is confirmed.

## 6. Owner decisions (before Task 2 measurement + Task 3 scoring)

1. **Proceed to score I6 as specified** (bounded vs affine, the +0.11 direction), reporting it honestly as
   weak-but-directional — OR **refine the I6 response** to the measured polymorphism gradient (semilattice <
   majority < affine ruggedness), which is the more faithful and more interesting reading? (Either is a
   pre-measurement choice; the raw verdict still comes to you before findings.)
2. **Density protocol:** fix "matched density" as matched fraction-of-threshold per family (my recommendation),
   or matched solution-count, before the measurement run?
3. **Given partial theorem-adjacency**, is I6 worth the full run as a genuine-but-modest measured finding, or
   should it be reframed (like the proof-side) as consistency-grade, with the *gradient* as the headline?
4. **Proof-side `proof_size` (Task 1d)** on the 5 NP rows still proceeds in parallel regardless — confirm.
