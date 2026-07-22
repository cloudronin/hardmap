# Sprint 4 · domain-confound check — the anomaly withdrawn, the metric validated

**The domain-confound check (owner-mandated, Task 3 hold) dissolved the domain-3 anomaly and refuted H_I6b's
polymorphism reading — while validating the instrument.** The headline result of Sprint 4 is deflationary and
honest: **complexity factors through the algebraic classification; solution geometry does not.** Measured
ruggedness varies at the *relation* level — across families sharing width, sharing polymorphism class, and across
domains.

Sealed verdicts (prereg_v8, no rescue): **H_I6a SUPPORTED (internally valid) / external validity BROKEN**;
**H_I6b REFUTED as law**; **anomaly WITHDRAWN**; **theory-forced tier CONFIRMED**; **instrument QUALIFIED**.

---

## 1. The metric is not domain-biased (owner #1, #2)

`ruggedness = 1 − clustering`, `clustering = max(0, (mean_q − q_random)/(1 − q_random))`, `q_random = 2/|D| − 1`
(Boolean 0; |D|=3 −1/3). So it **corrects for the domain-dependent baseline overlap**. Validation:

- **Known-smooth |D|=3 pole:** the 0-attractor (`{(a,b): a=0 ∨ b=0}`, min-closed, 0-valid) reads **0.53–0.60
  normalized** — well under the 0.8 domain-bias threshold. A |D|=3 family *can* read smooth. (Equality
  `{(0,0),(1,1),(2,2)}` was a bad pole — it is coloring-like/spread, reads ~1.0; noted, not used.)
- **Rugged |D|=3 pole:** lin-eq-z3 (affine) reads **1.0**. The metric separates the |D|=3 poles cleanly.
- **Same-relation isolator (the decisive one):** the ≤ relation across domains — Boolean implication vs |D|=3
  order — has a **raw gap of ~0.20 that collapses to ~0.05 under normalization** (implication norm 0.72–0.79,
  order-3 norm 0.80–0.84). Normalization removes the domain baseline as intended.

## 2. Ruggedness is relation-specific — the real driver (owner #3)

| relation | domain | class | **normalized** | raw |
|---|---|---|---|---|
| **implication (x→y = ≤)** | \|D\|=2 | Horn/bounded | **0.72–0.79 (rugged)** | 0.40–0.42 |
| NAND-Horn | \|D\|=2 | Horn/bounded | 0.48–0.52 (smooth) | 0.18–0.24 |
| **order-3 (≤)** | \|D\|=3 | semilattice | **0.80–0.84 (rugged)** | 0.60 |
| 0-attractor | \|D\|=3 | min/bounded | 0.53–0.60 (smooth) | 0.39–0.43 |
| lin-eq-z3 | \|D\|=3 | affine | 1.00 (rugged) | 0.66–0.67 |

Three facts, together:

1. **Boolean implication (≤ over |D|=2) is itself rugged (0.79)** — and GKMP *covers* it (tight/Schaefer). So the
   order relation is intrinsically rugged **in any domain**; order-3 is rugged because it *is* ≤, not because it
   is |D|=3. → the anomaly is **Boolean-visible, inside GKMP's jurisdiction → WITHDRAWN** (no theory-silent
   novelty). The tier system worked: the theory-silent tier emptied itself under scrutiny.
2. **Implication and NAND-Horn are both Boolean bounded-width, yet read oppositely** (0.79 vs 0.48) → ruggedness is
   **not** a function of the polymorphism class → **H_I6b REFUTED as a law**; the census ordering was
   representative selection.
3. **Two |D|=3 min-closed families read oppositely** (0-attractor 0.55 vs order-3 0.82) → it is the relation, not
   the domain — reconfirming the metric is unbiased.

## 3. H_I6a rechecked under a rank test (owner #4, #5)

The median-cut used for Cramér's V was **not** pre-sealed, so the primary test is replaced by Mann-Whitney U (no
binning) on the raw ruggedness values, affine vs bounded; V is demoted to sensitivity.

| density | U (affine>bounded) | rank-biserial | permutation p |
|---|---|---|---|
| 0.7·α_struct | **45 / 45** | 1.00 | **0.0005** |
| 0.9·α_struct | **43 / 45** | 0.91 | **0.002** |

So H_I6a stays **SUPPORTED internally** — but its external validity is **broken**: affine reps are uniformly,
coset-*forced* rugged; "bounded-width → smooth" is **false as a law** (implication is a bounded-width
counterexample). The licensed claim is *"these affine reps are uniformly rugged and these bounded reps mostly are
not,"* never *"width predicts terrain."*

## 4. Structural consequence (stated plainly)

The census's **one-representative-per-co-clone roster is valid for the oracle columns** (charges constant within a
co-clone by theorem — Task 0 residual = 0) and **invalid for the measured columns** (ruggedness is demonstrably
not constant within a loose class). Every measured-column result inherits its representative choice. Whether it
inherits it *coarsely* (co-clones cluster) or *fatally* (co-clones scatter) is the **Sprint 4.5** question, run
next, before the findings doc is written.

Reproduce: the pole/isolator probes and the Mann-Whitney are in the confound-check run
([`results/landscape/confound_check.json`](../../foundry/results/landscape/confound_check.json)); the confirmation
raw cells are [`confirm_v7.json`](../../foundry/results/landscape/confirm_v7.json). Instrument:
[`solscape.py`](../../foundry/solscape.py). Sampled-population provenance throughout (R-d).
