# Sprint 4 · connectivity-class prediction test — NOT PREDICTIVE (and convergent prior art recorded)

**Do the connectivity literature's relation-level classes predict measured ruggedness where the tractability
labels failed? No.** Scored against the sealed prediction ([prereg_v9](../../foundry/results/prereg/prereg_v9.json),
committed before the classification was derived): **NOT_PREDICTIVE.** Typical-case *sampled* solution geometry
escapes even the classification purpose-built for *worst-case* geometry — solution geometry is finer than **both**
the algebraic (Schaefer) and the connectivity (GKMP) classifications. That dissociation is the finding.

R20-verified classes (Gopalan–Kolaitis–Maneva–Papadimitriou, SICOMP 38(6) 2009, arXiv cs/0609072, Def 5–6,
Thm 8–10): OR-free, NAND-free, componentwise-bijunctive, tight, and n_components(G(R)). Applied to the 39
Sprint-4.5 arity-3 Boolean relations already measured (no new sampling). Implementation
[connectivity.py](../../foundry/connectivity.py); run [dev/connectivity_test.py](../../dev/connectivity_test.py) →
[connectivity_test.json](../../foundry/results/landscape/connectivity_test.json).

---

## The general result — the clone-invariant impossibility (lead)

The connectivity features are near-constant within a co-clone (they vary in only **2 of 13**). This is **not
specific to the connectivity classes**, and it is the real result, proof-shaped:

> **A co-clone *is* the set of relations sharing a polymorphism clone. Therefore every language-level algebraic
> invariant — tractability class, connectivity class, rigidity rank, anything read off the polymorphisms — is
> *constant on the co-clone by construction*. No such invariant can explain within-co-clone terrain variation:
> the variation is carried by the *choice of representative relation*, precisely the information the clone
> discards.**

The two empirical negatives — tractability failed to predict within-co-clone ruggedness (Sprint 4.5), connectivity
failed here — are **two instances of one structural fact**, not two coincidences. Any future clone-derived charge
(including rigidity rank, below) inherits the same ceiling: it can speak to *between*-co-clone quantities, never to
*within*-co-clone terrain variation. That is why the surviving rigidity question (prereg_v10) is posed about the
between-stratum spread, not the within-stratum values.

**Framing discipline.** This is *"worst-case structural classification does not reach typical-case sampled
geometry,"* **not** "the connectivity classes do not work." They were built for a different question — the
diameter dichotomy and the st-connectivity trichotomy — and they succeed at it. Amendment 2's convergent-prior-art
credit stands in full: the GKMP–Schwerdtfeger line hit the same wall we did (coarse tractability labels cannot
classify solution-space structure) and answered it by building finer classes; our result only adds that even those
finer classes stop at the co-clone boundary, because they too are clone invariants.

---

## The result

The connectivity features are **near-constant within a co-clone** — they vary within only **2 of 13** co-clones —
because they are essentially *functions of the co-clone* (OR-free/NAND-free/componentwise-bijunctive are
polymorphism-facing). A classification that is constant where the ruggedness scatters **cannot explain that
scatter**: it lives at the same resolution as tractability, which already failed there (Sprint 4.5).

The overall correlations are weak *between*-co-clone effects, not a relation-level predictor:

| feature | overall corr with ruggedness | note |
|---|---|---|
| n_components | **+0.47** | but n_comp=1 group ranges **[0.34, 1.0]**; n_comp=2 ranges [0.44, 1.0] — huge overlap |
| componentwise-bijunctive | −0.33 | **wrong sign on the key contrast** (below) |
| balanced (OR-free & NAND-free) | +0.04 | no signal |

**The decisive diagnostic** (the confound-check contrast): implication (rugged 0.79) and NAND-Horn (smooth 0.48)
**both have n_components = 1** — the strongest feature cannot tell them apart. And componentwise-bijunctive is
`True` for rugged implication yet correlates −0.33 (→ smoother) overall: it points the *opposite* way on the very
contrast that motivated the test.

### Scored against the sealed prediction (owner, prereg_v9)

| sub-prediction | sealed | outcome |
|---|---|---|
| (a) separates affine from non-affine | yes | **WEAK** — the affine *flag* does not separate (0.69 vs 0.68); the geometric signal (n_components) is a between-co-clone effect the aff-flag already spans |
| (b) outperforms tractability on the remainder | yes | **FAILS** — features vary within only 2/13 co-clones, so they cannot explain the within-co-clone scatter where tractability failed |
| (c) leaves substantial within-class variance | yes | **HOLDS** — within-group ruggedness ranges span [0.34, 1.0] |

The owner's prediction anticipated PARTIAL (a,b,c all hold); the data is **weaker** — (b), the crux, fails. Scored
straight: **NOT_PREDICTIVE**. No rescue.

## Convergent prior art (Amendment 2)

The GKMP–Schwerdtfeger connectivity line developed its own finer *relation-level* classes — **tight, safely
tight, CPSS (constraint-projection-separating Schaefer), constraint-projection separation** — *precisely because
Schaefer's tractability classes could not classify solution-space structure* (the trichotomy P / coNP-complete /
PSPACE-complete for st-connectivity refines Schaefer's P/NP-complete SAT dichotomy). This is **convergent prior
art** for the Sprint-4 headline (complexity factors through the algebra, geometry does not, at the tractability
resolution): the neighbors reached "the tractability classes do not classify geometry" first, from the
*worst-case structural* side. Our result is **less novel and better supported for it**, and it **extends** the
convergence in a specific direction: even those purpose-built finer classes, evaluated as relation-level
predictors, do **not** reach the *typical-case sampled* geometry we measure — they remain co-clone functions.
Worst-case connectivity structure and typical-case sampled dispersion are distinct axes.

Sources: GKMP, *The Connectivity of Boolean Satisfiability: Computational and Structural Dichotomies*, SIAM J.
Comput. 38(6):2330–2355, 2009 (arXiv cs/0609072); K. Schwerdtfeger, *A Computational Trichotomy for Connectivity
of Boolean Satisfiability* (arXiv 1312.4524) and the thesis *Connectivity of Boolean Satisfiability*.

## What survives, precisely

Sprint 4's boundary sharpens to: **complexity factors through the algebraic classification; solution geometry
factors through it only within the affine strata (coset-forced) and is otherwise relation-specific below the
resolution of both the algebraic and the connectivity classifications.** The measured-column program's honest next
move — sampling geometry at the relation level and seeking a *typical-case* predictor (not a worst-case
structural class) — stands, now with the worst-case classes ruled out as the shortcut.
