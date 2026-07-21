# Proof-Space Cartography v1 — Spec

**Codename:** Desert Map
**Status:** Draft for review
**Owner:** Vishnu
**Mode:** Spec-driven build, paired with Claude Code

---

## 1. Objective and hypothesis

**Objective.** Build the first empirical map of the loss landscape of continuous (gradient-descent) proof search, on the simplest proof system where proofs are fully verifiable: Resolution refutations of small unsatisfiable random 3-SAT instances.

**Hypothesis (H1).** As instance hardness increases, the landscape of the relaxed proof-search objective exhibits the shattering signature known from solution-space physics: independent gradient-descent runs converge to increasingly distant optima (bimodal overlap distribution), and success rate collapses at a sharp boundary rather than degrading smoothly. **Hardness direction (correction):** for Resolution refutations, hardness peaks just above the sat threshold and falls as α rises (Ben-Sasson–Wigderson width bound: refutation size shrinks with density). The hard cells are α=4.5–5.0; α=8–10 are the easy cells. All shattering signatures are predicted as α *decreases toward threshold*, opposite the solution-space convention.

**Non-goal.** v1 proves nothing. It produces plots. The theorem (a proof-space overlap-gap property) is a later phase gated on v1 showing the predicted signature.

## 2. Scope

| In scope (v1) | Out of scope (v1) |
|---|---|
| Resolution proof system only | Frege, extended Frege, any strong system |
| Random 3-SAT, unsat instances, n ≤ 60 vars | Structured/industrial instances |
| Direct continuous relaxation of the proof object | Policy/RL provers (AlphaProof-style) |
| Landscape metrics: overlap, success rate, Hessian spectra | Any lower-bound theorem |
| Single-GPU experiments | Distributed training |

Rationale for direct relaxation over a learned policy: the object of study is the geometry of proof space itself. A policy net puts the geometry in policy-weight space, one indirection away from the thing we want to map. v1 maps the proof embedding directly.

## 3. Design

### 3.1 Instance family

- Random 3-SAT at clause densities α ∈ {4.5, 5.0, 6.0, 8.0, 10.0} (all above the ~4.267 sat threshold, so unsat w.h.p.; verify each instance with a SAT solver before use).
- Sizes n ∈ {20, 30, 40, 60}. Discard satisfiable draws.
- 50 instances per (n, α) cell, fixed and versioned as test fixtures.

### 3.2 Proof representation (continuous relaxation)

A Resolution refutation of length L is a sequence of derived clauses, each obtained by resolving two earlier clauses on a pivot variable, terminating in the empty clause.

Relaxation, v1:

- Fix proof budget L (start L = 4n, sweep later).
- Each derived step t has three soft-selection tensors: parent-1 distribution over rows < t (softmax), parent-2 distribution, pivot distribution over variables.
- Each clause is represented as a soft literal-membership vector in [0,1]^(2n); derived clauses are computed differentiably from soft parents (union minus pivot literals).
- **Loss** = w1·(validity residual: mass of pivot-literal violations per step) + w2·(termination: distance of final clause from empty) + w3·(sharpness: entropy penalty, annealed).
- **Decode**: round selections to argmax, check the discrete proof with an exact verifier. A run "succeeds" iff the decoded proof verifies.

### 3.3 Training / probing protocol

- Optimizer: Adam, cosine schedule; R = 100 independent seeds per instance.
- Anneal entropy weight w3 from soft to hard (temperature schedule) — the continuous-to-discrete rounding is the known failure mode; the schedule is the main tunable.
- Record full weight trajectories at checkpoints for geometry analysis. To bound artifact size, compute trajectory summaries in-container (step-norm series, cosine of successive update directions, sampled pairwise seed divergence at checkpoints) and push those as parquet; raw trajectory tensors only for a small designated subset of cells.

### 3.4 Metrics (the map)

| Metric | What it measures | Shattering signature |
|---|---|---|
| Success rate vs (n, α) | Where gradient search fails | Sharp boundary, not smooth decay |
| Pairwise overlap of converged proofs (per instance, across seeds) | Clustering of optima | Overlap distribution splits bimodal as α decreases toward threshold |
| Distance between decoded discrete proofs (normalized edit/set distance) | Discrete-level clustering | Same split, discrete side |
| Hessian top-k spectrum at convergence (Lanczos) | Local terrain sharpness | Minima sharpen/isolate with hardness |
| Loss at failure vs success | Whether failures are "close misses" | Failures plateau far from valid (needle, no shadow) |
| Trajectory statistics (step-size decay, direction change/curvature along path, inter-trajectory divergence over time) | Structure the paths never reach, detected by deflection ("lensing") | Deceleration zones and scattering increase as α decreases toward threshold; trajectories on easy (high-α) instances flow smooth and parallel |

### 3.5 Controls

- Positive control: planted short refutations (instances constructed with known small proofs) — relaxation must recover these or it is broken.
- Negative control: satisfiable instances (no refutation exists) — loss must not decode to a "verifying" proof; verifier is the backstop.
- Baseline: random restarts + local discrete search (WalkSAT-style over proof space) at matched compute, to show any boundary is not an artifact of gradient methods alone. *(v1.1 if time-boxed out.)*
- Instrument-noise run (glitch catalog): apply the full pipeline, identical annealing schedule included, to easy instances (high α, small n — short refutations exist) where terrain is expected smooth. Any clustering or bimodality appearing there is instrument artifact (e.g., premature freezing from the temperature schedule), catalogued and subtracted from interpretation everywhere else.

## 4. Experiment matrix

| Exp | Question | Cells | Est. GPU-h |
|---|---|---|---|
| E0 | Does the relaxation recover planted proofs? | 3 sizes × planted | 4 |
| E1 | Success-rate map over (n, α) | 4 × 5 × 50 × 100 seeds | 30–60 |
| E2 | Overlap distributions on E1 successes | reuse E1 artifacts | 2 |
| E3 | Hessian spectra at 20 sampled optima per cell | subset | 8 |
| E4 | Budget sweep L ∈ {2n, 4n, 8n} at one (n, α) | 3 | 10 |
| E5 | Trajectory-lensing analysis on E1 checkpoint trajectories | reuse E1 artifacts | 3 (CPU-heavy, analysis only) |

## 5. Milestones and done-gates

| M | Deliverable | Done-gate |
|---|---|---|
| M1 | Instance generator + exact Resolution verifier + fixtures | Verifier rejects 100 corrupted proofs, accepts 100 known-valid; fixtures versioned |
| M2 | Differentiable relaxation + decode | E0 passes: ≥80% planted-proof recovery at n=20 |
| M3 | Metrics harness (overlap, spectra, plots) | Reproduces a known solution-space shattering plot on plain 3-SAT solutions as a harness sanity check |
| M4 | E1–E3, E5 run + writeup of the map | One figure per metric row in §3.4, with a stated verdict on H1. Concordance rule: shattering is claimed only if overlap, Hessian, and failure-loss channels independently agree, after subtracting the glitch catalog; any single-channel signal is reported as anomaly, not finding |

M1–M2 are the risk front. M3–M4 are mechanical once M2 passes.

## 6. Kill criteria

1. **Relaxation dead (kill at M2):** after 3 redesign attempts of the soft-resolution operator, planted-proof recovery at n=20 stays below 50%. Verdict: direct relaxation is the wrong probe; stop, do not escalate to policy nets inside this project.
2. **No signal (kill at M4):** success rate degrades smoothly with α, overlap distributions stay unimodal, and failure losses hug the success losses. Verdict: no shattering visible at this scale; write the negative result up as a short note and stop.
3. **Compute blowout:** any single experiment exceeding 2× its GPU-h estimate before producing its first checkpoint plot gets re-scoped or cut.

## 7. Investigation items (confirm before build, do not assume settled)

- **I1.** Prior art on differentiable Resolution / continuous relaxations of refutation search — likely exists in some form (neuro-symbolic ITP literature, differentiable SAT). Execution agent: search before writing the M2 operator; adopt an existing formulation if one fits.
- **I2.** Standard overlap estimator used in the spin-glass 3-SAT literature (exact definition of m(q) as used by Mézard/Zdeborová school), so E2 matches published methodology.
- **I3.** Whether Gamarnik's OGP formalism has already been applied to any proof-search setting. If yes, v1 repositions as replication + extension, which changes the writeup, not the build.
- **I4.** Lanczos Hessian tooling that works out of the box on this parameterization (PyHessian or equivalent, current maintenance status).
- **I5.** Compute platform decided: HF Jobs. T4-small for E0/smoke, 1x L4 ($0.80/hr) for E1/E2/E4, L40S only if E4 L=8n OOMs, CPU Upgrade for M1 fixtures. Execution agent: confirm exact flavor strings via `hf jobs hardware` at build time; set explicit `--timeout` on every run (default is 30 min); shard E1 into per-(n,α) jobs so a failed cell doesn't burn the sweep. Budget ceiling: $75 total, tracked against kill criterion 3.
- **I6.** Planted-refutation construction for E0/M2 gate: how to build unsat instances with a known short Resolution refutation of controlled length. Candidate approaches to evaluate before building: (a) start from a small unsat core (e.g., the 2-variable complete contradiction from the dinner example generalized) padded with satisfiable filler clauses; (b) run a real solver (DRAT-producing) on small random instances and keep those with short extracted proofs. Do not build E0 until one of these is validated.

## 8. Engineering requirements

- **Stack:** Python + PyTorch. Exact SAT solver for fixture verification: agent's choice (PySAT/kissat class), pinned.
- **Artifact store:** HF Jobs machines are ephemeral. Every job pushes results to a private HF dataset repo before exit: one path per experiment cell, metrics as parquet, converged proof tensors and decoded proofs as versioned files. A job that computes but doesn't push counts as failed.
- **Reproducibility:** every run records instance fixture hash, global seed, library versions (pinned requirements), and git commit. Overlap statistics are only valid within a pinned environment; treat an environment change as a new experiment version.
- **Dev/run split:** develop and unit-test locally on CPU (n=20 runs in seconds); HF Jobs is for sweeps only. Nothing ships to a paid flavor before passing the local M1/M2 gates.

## 9. Sizing

Paired-with-Claude-Code mode, spec-driven:

| Phase | Est. hours (paired) |
|---|---|
| I1–I4 investigation | 2 |
| M1 | 2–3 |
| M2 (risk front, incl. redesign loops) | 6–10 |
| M3 | 3 |
| M4 (runs are wall-clock, attention is checkpointing) | 3 |
| E5 trajectory-lensing analysis | 2 |
| **Total attention** | **18–23 h** |

Fits in 2–3 weekend blocks plus weeknight checkpoint reviews. GPU wall-clock runs unattended.

## 10. Placement

Hobby-research bucket, subordinate to praxis work. Nothing here touches frozen praxis artifacts. Kill criteria above are the containment; no design partner, no users, no support surface.
