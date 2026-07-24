# desert-map — agent/contributor rules

> **Status: v1 killed at M2 (spec §6.1).** Direct relaxation of the proof object cannot recover planted
> refutations from random init (E0 = 0%); the barrier is the direct fixed-selection parameterization, not
> the instances or GD. See `docs/findings/NEGATIVE-RESULT.md`. M1 + the M2 operator + the calibration
> harness ship; M3/HF-sweep/E1–E5 were gated on M2 and are not built. The invariants below still govern any
> future work on this code.

Load-bearing invariants for anyone (human or agent) working in this product. Each encodes a
decision from the spec (`docs/specs/proof-space-mapping-v1-spec.md`) and the approved plan; breaking
one silently invalidates the science, not just the scaffolding.

## What this is (one paragraph)

Desert Map builds the first empirical map of the loss landscape of *continuous (gradient-descent)
proof search* for **Resolution refutations** of small unsat random 3-SAT instances, and tests **H1**
(shattering: independent GD runs converge to distant optima and success rate collapses at a sharp
boundary as instances get harder). v1 produces plots and a verdict on H1 — it proves no theorem.
A self-contained monorepo sibling product. Sweeps run on HF Jobs.

## THE INVARIANTS (do not break)

1. **The verifier is the trusted, torch-free oracle.** `verify.py` is a dependency-free exact
   Resolution checker. A run "succeeds" iff its *decoded discrete* proof verifies here — never
   because the soft loss is low. Keep `verify.py` (and `instance.py`, `fixtures.py`) importable with
   **no ML stack**; `tests/test_light_oracle_import.py` enforces it. Never weaken or bypass the
   verifier to make a run "succeed."

2. **E0 success = "decoded proof verifies," from RANDOM init.** The M2 done-gate is ≥80%
   **verifier-pass rate at n=20 from random initialization** (findability) — a run succeeds iff its
   decoded proof verifies, NOT if it recovers the *specific* planted proof (C1). The planted core only
   guarantees a refutation of length ≤ the chain length exists, which sets the proof budget `L`; any
   verifying refutation counts. A near-planted-init run is only a *diagnostic* (search-failure vs
   representation-failure) — it does NOT satisfy the gate and does NOT consume the 3-redesign kill
   budget (spec §6.1). The certifiable property of a planted instance is that its *filler is satisfiable
   on its own* (so every refutation engages the core); proof uniqueness is neither claimed nor required.

2a. **Hard-negative control category (C2, spec §3.5): failing is the correct reading.** PHP and
   Tseitin-on-expander are unsat instances with NO short Resolution proof. The relaxation is *expected*
   to fail to find a verifying refutation within budget `L` there — and that failure is pre-registered
   (`results/prereg`), not explained after the fact. Never use these as planted positives.

3. **Hardness increases TOWARD the threshold — never flip the dial.** For Resolution refutation
   hardness, **hard = α∈{4.5,5.0}** (near the ~4.267 sat threshold), **easy = α∈{8,10}**. All
   shattering signatures are predicted as **α decreases toward threshold** — opposite the
   solution-space convention. The glitch/instrument-noise control runs on the **easy** cells (high α,
   small n). The M3 sanity check uses the *standard* solution-space dial (sat instances below
   threshold) — do not conflate the two.

4. **Concordance rule — no single-channel shattering claims.** Shattering is claimed only if the
   overlap, Hessian, and failure-loss channels **independently agree, after subtracting the glitch
   catalog**. Any single-channel signal is reported as an *anomaly*, not a finding (spec §5).

5. **Pre-register before any paid run.** `results/prereg/*.json` commits the predicted signatures
   (H1 direction, overlap shape, trajectory-lensing direction, concordance rule) BEFORE E1 runs.
   Phase 5 does not launch until the prereg receipts are committed. This is what makes M4
   matched-filtering rather than post-hoc pattern reading.

6. **A job that computes but doesn't push is a failed job.** HF Jobs machines are ephemeral; every
   job pushes its cell's metrics (parquet) + tensors + a manifest (fixture hash, global seed,
   `pip freeze`, git commit) to the private HF dataset repo before exit (spec §8).

7. **Kill honestly.** If after 3 soft-resolution-operator redesigns random-init recovery stays <50%,
   stop — do not escalate to policy nets inside this project (§6.1). If E1 shows smooth decay +
   unimodal overlap + failure-loss hugging success-loss, write the negative result up and stop
   (§6.2). Do not widen the sweep or loosen a tolerance to manufacture a signal. Budget ceiling $75.

## Repo layout

```
desertmap/
  instance.py verify.py fixtures.py   # M1 oracle (torch-free)
  relax.py losses.py decode.py run.py # M2 relaxation (torch, [compute], lazy-imported)
  metrics.py hessian.py trajectories.py glitch.py plots.py  # M3 + E5 analysis
  hf/ launcher.py launch.py entrypoint.py mirror.py         # HF Jobs (sibling hf layout)
  config.py                           # env-overridable repo ids / flavors / image
  results/prereg/                     # committed pre-registration receipts
  fixtures/                           # versioned instances (data)
```

Run tests from inside this product dir: `python -m pytest tests -q` (monorepo namespace convention).
