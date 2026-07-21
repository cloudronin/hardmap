# M2 / E0 risk-front — investigation & calibration

Record of the M2 differentiable-relaxation risk front (spec §6.1 kill criterion) and the discrete-search
calibration. All at n=20 planted controls unless noted; L=12 budget (planted chain k=5); R=40–128 seeds.

## What works (representation is sound)
- **Init AT planted proof → decode → verify: 100%.** The soft operator represents a Resolution refutation
  exactly (product-t-norm soft-OR + pivot removal; verifier fix: stop at first empty clause).
- **Near-planted init (bias≈6, noise≈0.3): 100%.** The valid basin exists and gradient descent reaches it
  *from near it*.

## What fails — random-init E0 (the gate), across every variant
| Attempt | n6 bare core | n20 full |
|---|---|---|
| #1 pure-soft | 0% | 0% |
| #2 straight-through (STE) | 0% | 0% |
| loss-schedule fix: decoupled-β (soft loss → **0.013**) | 0% (rounding gap) | 0% |
| entropy-anneal sweep w3∈{0.1,0.3,0.6} × {soft,STE} | 0% | 0% |

Two operator-redesign attempts (soft, STE) spent; both <50%. The decoupled-β fix drove the *soft* loss to
~0.01 but the argmax decode still didn't verify (soft→hard rounding gap); the entropy anneal (spec's
designated "main tunable") did not close it.

## Calibration (discrete-search baseline, spec §3.5) — the decisive result
| Method | Parameterization | n6-core | n20 | n40 |
|---|---|---|---|---|
| Gradient descent (soft & STE) | fixed per-step parent+pivot selection | 0% | 0% | — |
| Array WalkSAT (discrete local search, 96k moves) | **same** fixed-selection | 0% | 0% | — |
| **Constructive search** (grow bank by resolvable pairs) | order-free | **100% (4 steps)** | **100% (5)** | **100% (9)** |

`desertmap/discrete_search.py`: `walksat_proof_search` (array/fixed-selection) and `constructive_search`
(order-free). Energy verified to agree with the exact verifier (`energy(planted)=0, verifies=True`).

## Diagnosis
The barrier is **the fixed-per-step parent+pivot selection parameterization**, not the instances and not
gradient descent specifically:
- Instances are trivially refutable (constructive search: 100%, <0.5s) → **not** instance hardness.
- A *discrete* local search on the same fixed-selection parameterization fails identically to GD → **not**
  GD-specific; it is a property of the parameterization's landscape.
- Mechanism: the proof is a length-L sequence where each step's validity depends on the previous derived
  clause. Local moves (a gradient step, or a single-component discrete edit) at step t invalidate step t+1,
  so neither local method can assemble the coupled chain. An order-free constructive search sidesteps this
  entirely.

## Redesign attempt #3 — order-free direct relaxation (the chosen final attempt)
Per the decision to spend the last redesign on an order-free direct relaxation (skipping Gumbel/bilinear),
tested in BOTH faithful forms:
| Order-free form | n6-core | n20 |
|---|---|---|
| Order-free *objective* (dense saturation: mean-validity + shrink-to-unit + soft-min mass) on the ordered operator, STE, w_mass/w_shrink swept | 0% | 0% |
| Order-free *parameterization* (layered parallel soft-resolution DAG: slots attend the whole prior bank; D∈{6,8}, W∈{4,6}; STE & soft) | 0% | 0% |

Both land at 0% (< 50%). This is the third of three operator-redesign attempts.

## Implication for the remaining redesign budget
The two remaining operator-redesign axes (Gumbel-softmax; bilinear/expectation-placement) all **keep the
fixed-selection parameterization**. Since a discrete local search on that same parameterization already
fails (0%), a different *gradient estimator* is unlikely to cross the ≥50% kill threshold — the landscape is
search-hostile to local methods regardless of gradient vs discrete. Escaping it requires an order-free /
constructive parameterization, which edges toward the autoregressive policy approach the spec explicitly
puts **out of scope** (§2). This is the spec §6.1 kill juncture, now with a sharp, evidence-backed verdict.
