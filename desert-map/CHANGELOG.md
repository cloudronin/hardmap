# Changelog — desert-map

## 0.1.0 — v1 killed at M2 (spec §6.1); negative result shipped

**Outcome:** Direct continuous relaxation of the Resolution-refutation object is the wrong probe for
proof-search findability. E0 (random-init planted-proof recovery) stayed at 0% across three operator
redesigns (pure-soft, STE, order-free) — while a constructive resolution search recovers every instance at
100%, and a discrete local search on the same fixed-selection parameterization also fails at 0%. The barrier
is the direct proof-object parameterization, not the instances or gradient descent. Full write-up:
`docs/findings/NEGATIVE-RESULT.md`. No paid compute used ($0 vs the $75 ceiling); kill at the local gate.

**Shipped (the salvage):**
- Phase 0: product scaffold mirroring the raitune sibling layout; v1 spec committed under `docs/specs/`;
  I1–I6 investigation (`docs/findings/I1-I6-investigation.md`).
- M1 (gate passed): `instance.py` (random 3-SAT, planted refutations, C2 PHP/Tseitin hard negatives),
  `verify.py` (torch-free exact Resolution verifier — the trusted oracle), `fixtures.py` (versioned
  hash-manifest incl. A1 SAT negative control). 100 corrupted rejected / 100 valid accepted.
- M2 operator: `relax.py` (soft & straight-through), `losses.py`, `decode.py`, `run.py` (E5 trajectory
  summaries). Represents planted proofs exactly (100%); fails findability from random init (the result).
- Calibration harness: `discrete_search.py` (`walksat_proof_search`, `constructive_search`) — produced the
  refined verdict. `docs/findings/M2-e0-calibration.md`.
- Pre-registration `results/prereg/prereg_v1.json` (predictions locked before any run).

**Not built (moot after the kill):** M3 metrics/plots, HF Jobs launcher/entrypoint/mirror, and the E1–E5
paid sweep — all gated on M2 passing (spec §5: "M3–M4 are mechanical once M2 passes"). `hf/config.py` is the
only HF scaffolding present (env-config pattern). 39 tests green.
