# Sprint 4 results — the measured instrument columns: partial factoring with an identified boundary

**Lead finding: complexity factors through the algebraic classification everywhere; solution geometry factors
through it only where the algebra is rigid enough to force it.** Sprint 4 built the solution-side `landscape`
instrument (the Proof-Census apparatus measures the proof side; the landscape charge is the satisfiable side),
qualified it against two-pole calibration in both domains, and asked whether any oracle charge predicts measured
solution-space ruggedness. The answer, after a full domain-confound check and a within-co-clone replication, is a
**partial factoring with a sharp boundary**, not a uniform failure: **within the affine strata the algebra pins
terrain completely** (coset structure forces dispersion — every affine co-clone clusters at within-spread
0.002–0.075), while **everywhere else geometry is relation-specific** (non-affine co-clones scatter up to 0.327,
across families sharing width, sharing polymorphism class, and across domains). The tractability classification
carries the geometry exactly as far as its rigidity reaches, and no further. That boundary — algebraic where the
algebra is rigid, relation-specific otherwise — is the honest headline.

Provenance: preregs [v4](../../foundry/results/prereg/prereg_v4.json)–[v8](../../foundry/results/prereg/prereg_v8.json)
(each locked before its run; the GKMP netting column locked before fresh data); instrument
[solscape.py](../../foundry/solscape.py)/[ensemble.py](../../foundry/ensemble.py); raw cells + confound +
within-co-clone data under [results/landscape/](../../foundry/results/landscape/). Sampled-population provenance
throughout (R-d). 44 foundry + 72 eightfold tests green; **no oracle cell touched; eightfold byte-identical.**

---

## Verdicts at size (no rescue)

| object | verdict | basis |
|---|---|---|
| **Instrument** | **QUALIFIED** | two-pole Vega passes in |D|=2 and |D|=3; normalization validated against a known-smooth |D|=3 pole (0-attractor 0.53); same-relation cross-domain gap collapses 0.40 raw → 0.05 normalized; two samplers concord (≤0.037); affine-exact confirms sampler bias 0.005 |
| **H_I6a** (width→terrain) | **SUPPORTED internally, external validity BROKEN** | Mann-Whitney affine>bounded U=45/45 p=0.0005 @0.7, 43/45 p=0.002 @0.9 — but a bounded-width relation (implication) is as rugged (0.79) as affine, so **arm composition, not the width bit**, drives it |
| **H_I6b** (polymorphism ordering) | **REFUTED as a law** | implication vs NAND-Horn (both Boolean bounded-width): 0.79 vs 0.48. The census ordering was representative selection |
| **Anomaly** (|D|=3 order/median rugged) | **WITHDRAWN** | order-3's ruggedness is the ≤ relation's, Boolean-visible (implication 0.79), **inside GKMP's jurisdiction** — no theory-silent novelty. The pre-committed theory-silent tier emptied itself under scrutiny |
| **Theory-forced tier** | **CONFIRMED** (confirmation, not novelty) | affine coset dispersion + semilattice/absorbing consensus read as prior structure theory predicts |
| **Sprint 4.5** (within-co-clone) | **SCATTER** | max within-co-clone ruggedness spread **0.327** across genuine same-profile representatives |

The F1 predictions ledger records **H_I6a as a scored HIT that does not generalize** (internally-valid test;
downgraded on new evidence — legal; upgrading would not be). This sits beside the Factors k∈{3,4} miss.

## The one theory-forced solid: affine

Affine constraint languages are **uniformly, forcibly rugged** — a satisfiable affine system's solutions are a
coset of a linear subspace whose pairwise Hamming distances concentrate (a random linear code), forcing low
overlap = dispersion. This is the one place where geometry *does* factor through the algebra, and Sprint 4.5
confirms it: every affine co-clone clusters tightly (within-spread 0.002–0.075). GKMP-tight + coding geometry;
reported as **confirmation of known structure**, with no novelty language.

## Sprint 4.5 — why the census roster cannot carry measured columns

Measuring 3 genuine same-6-flag-profile representatives within each of 13 tractable arity-3 co-clones:

- **Affine co-clones CLUSTER** (coset-forced): spreads 0.002–0.075.
- **Non-affine co-clones are mixed to badly SCATTERED**: pure 0-valid ranges **0.44–0.77** across three
  same-profile representatives (spread **0.327**); several others 0.15–0.21. A single representative's measured
  value is *not* representative of its co-clone.

**Verdict SCATTER, with a sharp boundary** (pre-registered rule: any co-clone ≥ 0.15). **Structural consequence
(F1 amended):** the census's one-representative-per-co-clone roster is **valid for the oracle columns** (charges
constant within a co-clone by theorem — Task 0 residual = 0), **valid for the measured columns *within the affine
strata*** (coset structure pins terrain — affine co-clones cluster at 0.002–0.075), and **invalid for the
measured columns elsewhere** (non-affine co-clones scatter up to 0.327). This is partial factoring with an
identified boundary — the algebra carries the geometry exactly where it is rigid enough (affine) and not beyond.
**Outside the affine strata the measured-column program requires relation-level sampling** — the correct, and
much stronger, next move (out of Sprint 4 scope).

## The clone-invariant impossibility — the structural result (prereg_v9 test)

The connectivity-class test (does the GKMP relation-level classification predict measured ruggedness where
tractability failed?) came back **NOT_PREDICTIVE** — and generalized into the strongest result of the measured
line, proof-shaped:

> **A co-clone is the set of relations sharing a polymorphism clone, so every language-level algebraic invariant —
> tractability class, connectivity class, rigidity rank, anything read off the polymorphisms — is constant on the
> co-clone by construction. No such invariant can explain within-co-clone terrain variation: it is carried by the
> choice of representative relation, the information the clone discards.**

Tractability failing (Sprint 4.5) and connectivity failing (here) are **one structural fact, not two
coincidences** — the connectivity features are near-constant within co-clones (vary in 2/13), and n_components = 1
for both rugged implication and smooth NAND-Horn. Framed correctly: *worst-case structural classification does not
reach typical-case sampled geometry* — not "the connectivity classes fail" (they succeed at their own diameter /
connectivity questions). **Convergent prior art** (Amendment 2): the GKMP–Schwerdtfeger line built finer
relation-level classes (tight, safely-tight, CPSS, constraint-projection separation) *because Schaefer's classes
cannot classify solution-space structure* — our headline was reached first from the worst-case side; we are less
novel, better supported, and extend it (even those classes stop at the co-clone boundary). Detail:
[Sprint4-connectivity-test.md](Sprint4-connectivity-test.md).

## Task 0 (the oracle-only closure) still stands

Independently of the measured columns, Sprint 4 opened by confirming the oracle-only census nets to **exactly
zero residual** (every oracle charge a total function of the polymorphism profile; canon-vs-computation over
oracle columns closed at its ceiling; cross-validated 18/18 at the anchors, perspective-divergent on
parameterized). See [Sprint4-Task0-R25-netting.md](Sprint4-Task0-R25-netting.md).

## Honest caveats

1. **The measured line ends negative.** No oracle × measured cross-structure was found; the instrument is sound
   and the negative is a *measurement*, not an instrument failure.
2. **Sampled-population, relation-level.** All ruggedness is a non-uniform sampled-population statistic (R-d) at
   n=15–24, K=35–40, at each family's α_struct regime (the density where the solution count first drops below the
   sampler cap — a builder-default anchor, since 10/14 census families are 0/1-valid and have no SAT threshold).
3. **Proof-side `proof_size` (5 NP rows) not run** — deferred (pysat absent in the dev venv; a pure-Python unsat
   path or the coverage gap is a follow-on). It would be a Ben-Sasson–Wigderson consistency check, not discovery.

## Budget ledger

All pure-Python CPU, local — **$0 of the $50 ceiling** consumed (no paid API/cloud). Wall-clock: calibration
seconds; confirmation 690 s; confound ~2 min; within-co-clone ~8 min. Kill-3 never triggered.

## Changelog / what's next

Sprint 4 delivered a **qualified instrument and a clean negative**: complexity factors through the algebra,
solution geometry does not. The measured-column program is **gated SCATTER** → the honest next move is a
**relation-level solution-geometry study** (sample many relations per co-clone; find the actual predictor of
ruggedness — order/dispersive structure is the leading hypothesis). Sprints 5–6 (construction + charge-9/Ω⁻) are
unaffected — they never depended on the measured columns.
