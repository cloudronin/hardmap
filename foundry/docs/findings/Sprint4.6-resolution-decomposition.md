# Sprint 4.6 — the hardness vector at two resolutions: complexity is clone-level, terrain is relation-level

**The measured line resolves into a two-sided structural result, now empirically supported.** On one expanded
roster (arity-3 full + arity-4 sampled, 77 relations, prereg_v11), two sealed experiments bracket the question the
connectivity and rigidity results opened:

- **A (rigidity middle-rank retest): PARTIAL.** The Sprint-4.5 3≈2 tie resolves, at ≥5 reps per stratum, into a
  **weak ordering in the predicted direction** — rank 3 spread 0.274 < rank 2 spread 0.353, corr(rank, spread) =
  −0.389 — not a hard tie. The rigidity envelope *weakly* orders through the middle of the hierarchy (and rank 4
  Maltsev stays firmly smallest). So the algebra predicts *how much* freedom it leaves, monotonically but loosely.
- **B (relation-level terrain prediction): SUPPORTED.** A relation-level feature predicts terrain where clone
  invariants provably cannot, and it generalizes to **unseen co-clones** (held-out, the primary test).

**The headline:** complexity is a **clone-level** property (constant on the co-clone, by the impossibility);
terrain is a **relation-level** property (carried by the representative the clone discards). Two components of the
hardness vector living at **different resolutions of the same object** — a sharper structural claim than the basis
hypothesis this program already retired, and here it is measured, not assumed.

Reproduce: [dev/sprint46_roster.py](../../dev/sprint46_roster.py) (build+measure) →
[dev/sprint46_analyze.py](../../dev/sprint46_analyze.py) (A+B) →
[sprint46_analysis.json](../../foundry/results/landscape/sprint46_analysis.json). prereg_v11 sealed before any
terrain was measured. 53 foundry + 72 eightfold tests green; no oracle cell touched; eightfold byte-identical.

---

## A — rigidity middle-rank retest (PARTIAL)

| rank | term | strata (≥5 reps) | mean spread | strata spreads |
|---|---|---|---|---|
| 4 | Maltsev (affine) | (rare, <5 reps — separate) | ~0.039 (Sprint 4.5, firm) | — |
| **3** | majority (bijunctive) | 4 | **0.274** | 0.181, 0.35, 0.402, 0.161 |
| **2** | semilattice (Horn/dual-Horn) | 4 | **0.353** | 0.285, 0.309, 0.493, 0.324 |

corr(rank, spread) = **−0.389** (negative = predicted direction). The 3≈2 tie of Sprint 4.5 (0.140 ≈ 0.138) was
**thin-strata resolution, not a real absence of ordering**: with ≥5 reps the middle ranks separate in the
predicted direction (rank 3 < rank 2), though weakly and with overlapping strata — hence PARTIAL, not CONFIRMED.
The **0/1-valid strata were excluded as a pre-registered principle** (trivial-satisfiability, non-Taylor — they
ride the lattice; prereg_v11); rank 1 is empty by Post's lattice. (Spread magnitudes are larger than Sprint 4.5's
because more reps per stratum → larger observed max−min; only the *ordering* is comparable.)

## B — relation-level terrain prediction (SUPPORTED, and honestly)

Three closed, sealed features (prereg_v11). Fit predicts ruggedness with **in-sample R² = 0.59**; it **beats the
permutation null** (p = 0.0002); and — the primary test — **held-out by co-clone beats the marginal baseline**
(MSE 0.102 vs 0.226, ≈2×). So relation-level features predict terrain on **co-clones never seen in the fit**.

| feature | sealed sign | marginal corr | verdict |
|---|---|---|---|
| density (\|R\|/2^arity) | **NEGATIVE** | **+0.255** | **sealed sign FAILED** |
| arity | two-sided | −0.16 | weak, no committed sign |
| **tuple_dispersion** (mean pairwise Hamming among R's tuples) | **POSITIVE** | **+0.742** | **matches — carries B** |

**SUPPORTED rests entirely on `tuple_dispersion`, not density.** The sealed density mechanism (sparse → rugged)
is **wrong**: density's marginal correlation is *positive* (+0.255), the opposite of the seal. The statistical-
physics density→clustering mechanism (prior art — cavity-method RS/1RSB clustering, condensation, freezing vs
constraint density) **does not transpose to relation-density in the sealed direction**. What carries the result is
the relation's own **tuple geometry**: a relation whose allowed tuples sit far apart in Hamming space propagates
that spread to its instances' solution sets (marginal +0.742). Crucially, tuple_dispersion **varies within a
co-clone**, so it is genuinely relation-level — exactly the information the clone discards, and exactly where the
clone-invariant impossibility said terrain must live.

The sealed decision rule allowed *either* signed feature to carry the verdict; tuple_dispersion did, so SUPPORTED
stands with no rescue — but the density failure is recorded in full, not buried.

## Bridge hunt (before any novelty language)

The **density mechanism is prior art** (statistical physics of random-CSP ensembles: the cavity method's clustering,
condensation, and freezing transitions as functions of constraint density — k-SAT / k-XOR / NAE-SAT / coloring;
and the solution-space geometry of random linear equations). It is *also* the feature that failed here. The
contribution that survives the bridge hunt is therefore **not** a density law but **the resolution decomposition**:
that solution-space terrain is a relation-level property predictable from relation tuple-geometry, sitting one
resolution below the clone-level complexity classification — two components of the hardness vector on the same
object. Whether *that* framing is itself anticipated is a question for the writeup's related-work pass, but the
density half is credited to the physics literature outright.

Sources: Montanari et al., *Reconstruction and Clustering in Random CSP*; *The solution space geometry of random
linear equations* (arXiv 1107.5550); *Widely distributed clusters of the d-k-CSP model* (arXiv 1812.07358).

## Where Sprint 4 (incl. 4.5, 4.6) now stands

1. **Clone invariants cannot predict within-co-clone terrain values** — the impossibility, proved (connectivity
   NOT_PREDICTIVE was one instance).
2. **The envelope (spread) is partially clone-predictable** — rigidity rank 4 pins it (0.039, named Maltsev
   mechanism); the middle weakly orders it (A, PARTIAL, corr −0.389).
3. **Terrain itself is relation-predictable** — tuple-geometry predicts ruggedness held-out (B, SUPPORTED).

Complexity factors through the algebraic classification; terrain factors through the *relation* one resolution
below. The measured-column line closes not on a negative but on a **decomposition**.
