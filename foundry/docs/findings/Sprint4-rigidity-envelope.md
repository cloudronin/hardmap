# Sprint 4 · rigidity-envelope test — PARTIAL, with a named mechanism for the affine boundary

**Does the algebra predict how much freedom it leaves?** At the rigid end, yes. Scored against the sealed
prediction ([prereg_v10](../../foundry/results/prereg/prereg_v10.json), committed before rigidity was derived):
**PARTIAL** — exactly the owner's predicted shape (holds at the rigid end, breaks at the low end).

This is the legitimate survivor of the clone-invariant impossibility: rigidity rank is a clone function, so it
**cannot** predict within-co-clone terrain *values* — but the *spread* (a between-stratum statistic) is a fair
clone-level target, and rigidity partially predicts it. Anti-circular by construction: rank is read from the
polymorphism flags alone; spread is measured from terrain alone. Reproduce:
[dev/rigidity_test.py](../../dev/rigidity_test.py) → [rigidity_test.json](../../foundry/results/landscape/rigidity_test.json);
rank function [rigidity.py](../../foundry/rigidity.py).

---

## The result

Rigidity rank (idempotent-Taylor hierarchy, most-rigid-wins: 4 Maltsev/affine · 3 majority · 2 semilattice ·
0 no-idempotent-Taylor) vs the Sprint-4.5 within-co-clone spread:

| rank | term | co-clones | mean spread | values |
|---|---|---|---|---|
| **4** | Maltsev (affine) | 4 | **0.039** | 0.006, 0.073, 0.075, 0.002 |
| 3 | majority (bijunctive) | 4 | 0.140 | 0.092, 0.214, 0.192, 0.062 |
| 2 | semilattice (Horn/dual-Horn) | 2 | 0.138 | 0.129, 0.147 |
| 0 (edge) | 0/1-valid only, no idempotent Taylor | 3 | 0.127 | **0.327**, 0.052, 0.003 |

- **corr(rank, spread) = −0.30** overall; **−0.63 excluding the 0/1-valid edge.** Negative = the predicted
  direction (more rigid → less freedom).
- **rigid end holds cleanly:** rank 4 (Maltsev) has the smallest spread by a wide margin (0.039 vs ~0.14).
- **not strictly monotone:** ranks 3 and 2 tie (0.140 ≈ 0.138); and the 0/1-valid edge co-clones — tractable by a
  constant, with *no idempotent Taylor term*, so "rigidity" is ill-defined for them — do not fit (a 0.327 outlier
  beside 0.003/0.052).

### Scored against the sealed prediction (owner, prereg_v10)

Prediction: spread decreases monotonically with rank; near-zero at 4, largest at 1–2, intermediate at 3.
Outcome: **PARTIAL** — the rigid end (rank 4 near-zero) holds exactly; the intermediate ranks are ordered below
rank 4 with a clean −0.63 correlation once the edge is excluded; but the strict monotone breaks (3≈2) and the
low-end "largest at 1–2" fails (the edge co-clones are inconsistent, not uniformly large). No rescue.

## The named mechanism (the positive)

**Maltsev rigidity forces near-zero within-co-clone spread.** This is the theory-grounded *mechanism* behind
Sprint 4's one solid: the affine strata are where geometry factors through the algebra (Amendment 1). Affine =
rank-4 Maltsev = the most rigid idempotent structure (few subpowers; solution sets are cosets of a linear
subspace), and that rigidity leaves essentially no representative-dependent freedom — hence spread 0.039. The
rigidity charge thus **names why** the affine boundary is a boundary, rather than merely observing it. Off the
Maltsev end, rigidity rank still trends with the spread (−0.63) but does not pin it — the residual freedom the
weaker-term co-clones leave is real and is where relation-level sampling (the honest next move) would go.

## Where this sits

Together with the connectivity test, Sprint 4 now has a clean two-sided result: a clone invariant **cannot**
predict within-co-clone terrain values (the impossibility, proved), but the strongest clone invariant
(Maltsev rigidity) **does** predict the *envelope* at the rigid end (partial, mechanism-grounded). The algebra
predicts how much freedom it leaves only where it leaves almost none.
