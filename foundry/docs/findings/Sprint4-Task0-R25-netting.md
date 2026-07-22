# Sprint 4 · Task 0 — R25-netting confirmation: the oracle-only comparison nets to exactly zero

**Predicted residual = 0. Confirmed, three independent ways.** Netting the theorem-forced component out of the
census P2/P3 statistics per the standing R25 procedure returns exactly zero residual — as it must, and this run
is a **selftest of the netting machinery**, not a discovery attempt. A non-zero residual would have been a
STOP-the-line bug; none appeared. This permanently closes the canon-vs-computation comparison **over the oracle
columns** and hands all remaining census science to the measured instrument columns (Task 1 onward).

> **R25 census residual → 0 (predicted, confirmed).** The both-real approx|parameterized table has raw
> Cramér's **V = 0.472** (n = 19; the live H_P2_scaled association). Netting the theorem-forced component
> collapses it to nothing: **residual V = undefined** (0 rows survive netting), **pooled within-stratum V = 0.0**
> (15 profile strata), **residual dimensionality = 0** (0 non-`derived` oracle cells). `survives = False` — the
> exact OPPOSITE of the canon, where the same procedure leaves V ≥ 0.5 even after deleting the entire
> APX-complete × FPT cell.

**Provenance.** Standing R25 procedure = [`eightfold.structure.cai_chen_residual_audit`](../../../eightfold/eightfold/structure.py).
Census-side implementation + CI selftest: [`foundry/r25.py`](../../foundry/r25.py),
[`tests/test_r25.py`](../../tests/test_r25.py). Run: `python -m foundry.cli --r25`. Census: 21 rows / 19 both-real
(unchanged from Sprint 3.5). No oracle cell was touched; eightfold byte-identical (r25 reads the canon atlas
read-only). 37 foundry + 72 eightfold tests green.

---

## The three netting views (all zero)

| View | What it removes | Residual | Reads |
|---|---|---|---|
| **Provenance netting** (mirrors cai_chen) | every row whose approx AND param cells are theorem-`derived` | **V undefined**, n_residual = **0**, `survives = False` | all 19 both-real rows are `derived` → the table empties |
| **Within-stratum association** (Cochran–Mantel–Haenszel) | the between-profile signal; pool the *within*-profile association | **pooled V = 0.0** over 15 strata | every stratum is charge-constant → zero within-variance |
| **Residual dimensionality** (P3) | the theorem-predicted value of every oracle cell | **residual k\* = 0** | 0 non-`derived` oracle cells; deviance from the theorem = 0 across all cells |

The raw signals these nets remove are real and non-trivial — V = 0.472 for the approx|param association, k\* = 3
for the census factor structure (Sprint 3.3). Netting takes both to zero because **every oracle charge is a total
deterministic function of the co-clone's polymorphism profile**: `approximation` tracks 0/1-validity,
`parameterized` tracks affine-ness, and both are functions of Pol(Γ). Conditioning on the profile therefore
removes all of the association and all of the dimensionality. This is the "within-stratum variation is zero by
construction" fact made numeric.

### The falsifiable check that gives the zero teeth

The residual could only be non-zero if some oracle cell were **not** polymorphism-forced (a hand-edited value, a
mis-statused cell, or an oracle that reads something outside the clone). Two guards make the zero a genuine test,
not a tautology:

- **Functional determination.** Grouping all both-real rows by polymorphism profile, every group is
  charge-constant — across **4 multi-row strata (max size 3)**. This spans the *two independent oracle code
  paths* (the N1 co-clone oracle `oracles.classify` and the finer-tier oracle `finer.classify_boolean`); if they
  disagreed on two languages that share a profile, the group would split and the audit would STOP. It doesn't.
- **Anchor cross-validation against the real canon** (below).

## Cross-validated at the anchors, incomparable elsewhere

The six registration anchors (`xor-sat`, `horn-sat`, `2-sat`, `3-sat`, `nae-sat`, `one-in-three-sat`) are the
canon ∩ census overlap — the only languages present in both worlds. Compared **perspective-aware** against the
actual Eightfold canon atlas:

- **Perspective-free charges** (`decision`, `counting`, `approximation`): **18 / 18 cells agree** across all six
  anchors. The census dichotomy oracles reproduce the independently-curated canon complexities exactly.
- **`parameterized` is perspective-divergent and thus incomparable:** the canon parameterizes by **treewidth**
  (every CSP is FPT — Courcelle), the census by **Exact-Ones solution weight** (Marx → W[1] off the
  weakly-separable class). Different parameter, different question; the anchors do *not* cross-validate here, by
  construction, and neither world is wrong.
- **`localization` is canon-absent** (a foundry-only charge).

---

## Closing paragraph — the oracle-only comparison is settled

**The canon-vs-computation question, asked over the oracle columns, is answered at its ceiling, and the answer is
a category difference rather than a measurement.** The census's oracle columns carry *no empirical content beyond
their own dichotomies*: every value is a total function of the polymorphism clone, so netting the theorem-forced
component leaves exactly zero residual association (V undefined) and zero residual dimensionality (k\* = 0) — the
mirror image of the canon, whose approx|parameterized multiplet *survives* the identical netting because it is
sourced from independent literature. The two atlases are commensurable only at the six shared anchors, and only
on the three perspective-free charges, where they agree 18/18; on the perspective-dependent `parameterized`
charge even the anchors are incomparable (treewidth vs Exact-Ones), and off the anchors the census has nothing
non-tautological to compare against the canon at all. There is therefore **no further oracle-column science to
extract**: any additional census row, at any n, can only re-express the dichotomies it was built from. The live
scientific question — does *hardness* (not the theorems) structure the synthetic world the way it structures the
human canon — now lives entirely in the **measured instrument columns** (`landscape`, `average_case`), which the
theorems do *not* assign. Sprint 4 builds and reads those columns; the flagship sealed test is I6 (does the
bounded-width oracle predict measured landscape ruggedness?). This closes the oracle-only comparison permanently.
