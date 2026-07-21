# Desert Map v1 — Negative result (kill at M2, spec §6.1)

**Verdict:** Direct continuous relaxation of the Resolution-refutation object is the wrong probe for
proof-search *findability*. The M2 kill criterion (spec §6.1) is triggered — with a sharper diagnosis than
the criterion anticipated. The M2 line stops here; per the containment plan we do **not** escalate to policy
nets inside this project (spec §2/§6.1).

## What was tested
The E0 positive control (spec §3.5, §4): recover a *planted* short Resolution refutation of a small unsat
instance from **random initialization** (success = the decoded discrete proof verifies, C1). Done-gate:
≥80% at n=20. Instances have a hand-built implication-chain core (controlled length k=5) whose *filler is
satisfiable on its own* (certifiable), plus C2 hard negatives (PHP, Tseitin) as no-short-proof controls.

## Result
| Probe | Parameterization | n6-core | n20 | n40 |
|---|---|---|---|---|
| **Constructive search** (order-free, non-parameterized) | grow bank by resolvable pairs | **100%** | **100%** | **100%** |
| Gradient descent — pure-soft | fixed per-step parent+pivot selection | 0% | 0% | — |
| Gradient descent — straight-through (STE) | same | 0% | 0% | — |
| Discrete local search (array WalkSAT, 96k moves) | same | 0% | 0% | — |
| Order-free objective (dense saturation, STE) | ordered operator | 0% | 0% | — |
| Order-free parameterization (layered soft-DAG, STE & soft) | order-free DAG | 0% | 0% | — |
| — for reference — init AT/near the planted proof | any | 100% | 100% | — |

Three operator-redesign attempts (pure-soft, STE, order-free) all < 50%; a loss-schedule fix (decoupled-β)
drove the *soft* loss to ~0.01 but the argmax decode still did not verify (soft→hard gap), and the entropy
anneal (the spec's designated "main tunable") did not close it.

## Diagnosis (the refined verdict)
The barrier is neither the instances nor gradient descent specifically:
1. **Not instance hardness** — a constructive resolution search refutes every instance in <0.5s (100%).
2. **Not GD-specific** — a *discrete* local search on the same fixed-selection parameterization fails
   identically to gradient descent (0%).
3. **It is the direct proof-object parameterization.** A valid proof is a coupled chain: each step's
   validity depends on the previous derived clause, so any *local* move (a gradient step, or a single
   discrete edit) at step *t* invalidates step *t+1*. Local optimization — gradient or discrete — cannot
   assemble the chain; the valid basin is reachable only from near it (planted-init → 100%). An order-free
   *objective* and an order-free *parameterization* (layered soft-DAG) do not escape this, because any
   acyclic direct relaxation retains the same cross-slot coupling. Only the non-parameterized, order-free
   **constructive** search — which commits real small resolvents greedily, one at a time — succeeds, and it
   is precisely *not* a direct relaxation.

**Conclusion.** The valid-proof basins of every *direct* proof-object relaxation tried are unreachable by
local optimization from random init; the landscape is search-hostile by construction, independent of
instance hardness or the gradient estimator. Direct relaxation cannot serve as the probe, so the geometry it
would report (H1 overlap/Hessian/lensing) is confounded with this parameterization pathology and cannot
distinguish intrinsic proof-space shattering from the parameterization's universal search-hostility.
Escaping it requires an order-free constructive/autoregressive formulation, which is a policy-style prover —
explicitly out of scope for v1 (spec §2).

## What ships (the salvage)
- **M1** — instance generator, exact torch-free Resolution verifier (the trusted oracle), planted-refutation
  builder, C2 hard negatives, versioned fixtures. Gate passed (100 corrupted rejected / 100 valid accepted;
  SAT negative control; hard negatives unsat). Fully tested.
- **M2 operator** — `SoftResolutionProof` (product-t-norm soft-OR + pivot removal, soft & STE), losses,
  decode, `fit_instance` with E5 trajectory summaries. Represents planted proofs exactly (100%); the
  negative result above is about *findability from random init*, not representation.
- **Calibration harness** — `discrete_search.py` (`walksat_proof_search`, `constructive_search`), the tool
  that produced the refined verdict.
- **Pre-registration** — `results/prereg/prereg_v1.json` (predictions locked before any run).

Nothing shipped to a paid HF flavor (spec §8): the kill happened at the local M2 gate, before any sweep.
Budget spent against the $75 ceiling: **$0** (all local CPU).

## If revisited (v2, out of current scope)
An order-free constructive/autoregressive prover (NeuRes-style learned clause-pair selection, I1) is the
formulation the calibration shows is searchable — but that puts the geometry in policy-weight space, one
indirection from the proof space v1 set out to map (spec §2 rationale). That is a different project, not a
redesign of this one.
