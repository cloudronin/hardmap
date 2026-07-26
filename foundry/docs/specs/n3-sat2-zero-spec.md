# N3 — the sat-2 zero

**Status: DRAFT AWAITING SEAL. Ruled "go" 2026-07-26; prereg number reserved `prereg_v21`, minted at seal.**
**Closes:** one of the two GENUINE-READING zeros the zero-hunt left standing (Q10).

---

## 1. The reading

`sat-2 · solutions · min`, ramp position 4, clause/variable ratio **1.6**, seed `20265280`, 3 instances.

| | |
|---|---:|
| measured violation rate | **0.0000** |
| tier-0 excess | −0.9455 |
| r | 22 |
| distinct 2-subsets used | 354 |
| zero-hunt verdict | **GENUINE-READING** |

2-SAT is bijunctive, so `majority` is forced and the join flags it correctly. **`min` is not forced** — a
general 2-CNF is not Horn. The reading clears the pre-declared r floor and the subset floor, so thinness
does not explain it and no closure argument covers it.

## 2. The question, and the sealed split

Two explanations, declared before running:

- **CHANCE-COMPOSITION** — the sampled formulas happened to draw Horn-like, and Horn ⟹ min-closed.
- **PREVALENCE** — solution sets of general 2-CNF at this size are min-closed far more often than the
  Horn route alone would predict.

**Sealed decision rule.** Over *N* seeded re-draws at ratio 1.6, measure per formula (a) whether the
formula is Horn (every clause has ≤ 1 positive literal), and (b) whether its solution set is min-closed:

| observed | verdict |
|---|---|
| min-closed rate ≈ Horn rate, and min-closed formulas are predominantly Horn | **CHANCE-COMPOSITION** |
| min-closed rate ≫ Horn rate, with min-closed **non-Horn** formulas common | **PREVALENCE** |
| min-closed rate ≈ 0 across re-draws | **CHANCE-COMPOSITION**, and the original reading is a rare draw |
| neither pattern separates at the declared *N* | **INSUFFICIENT** |

## 3. The prior, computed rather than assumed

At ratio 1.6 with n = 12 the generator emits **m = 19** clauses. A 2-clause is Horn iff at most one of its
two literals is positive — 3 of the 4 sign patterns — so:

> **P(the whole formula is Horn) = 0.75¹⁹ = 0.00423, i.e. 0.42 %.**

**A chance-Horn draw is a priori rare.** If re-draws show min-closure materially more often than 0.42 %,
CHANCE-COMPOSITION cannot carry the explanation and PREVALENCE is what is left — which is the interesting
branch, and it is the one the arithmetic favours before any data is collected. **Stated now so it cannot
be presented as a surprise afterwards.**

Note the asymmetry the prior does *not* resolve: Horn ⟹ min-closed, but min-closed does **not** ⟹ Horn.
A small solution set (r = 22 of 4096) can be min-closed by accident. Separating "accidentally closed
because small" from "closed for a structural reason" is why (b) is measured directly rather than inferred
from (a).

## 4. Design

- **N = 300** seeded re-draws at ratio 1.6, n = 12, same generator, seeds derived from a declared base.
- Per formula: Horn indicator, |solution set|, min-closure (exhaustive over all distinct pairs — r is
  small enough that no sampling cap is needed, and an exhaustive check removes a source of doubt).
- Report the joint table (Horn × min-closed), not just the margins — the decision rule reads the joint.
- **Region-size control:** min-closure rate is reported *conditioned on r*, because a set of 22 members is
  more easily closed than one of 1216, and the original reading sits at the small end of its own ramp.

## 5. Box and scope

**One evening.** ~300 × 4096 membership evaluations plus pair checks — seconds of compute.
No new rows, no new encodings, no re-measurement of any frozen rate. The original reading keeps its
recorded value whatever this returns; what is being decided is its *explanation*.

## 6. Multiple-comparisons ledger

One test, one family of one. Named alongside Terrain (family 5) and N1 (family 8); the flagship closes over
all three.
