# I1–I3 Investigation — findings & build decisions

Confirm-before-build items (spec §6). Web-sourced; negative results stated as "we found no prior work."

## I1 — Sampler tooling (randomized branching, DRUP, DRUP→Resolution)

**Findings.**
- PySAT emits **DRUP only** via `Solver(..., with_proof=True)` → `get_proof()`; **CaDiCaL has no Python
  randomization knob** — only **Glucose42** exposes `set_rnd_seed` / `set_rnd_pol` / `set_rnd_first_descent`.
- **drat2er** (DRUP→ordinary resolution) is **C++ build-from-source**, not pip-installable. DRAT-trim is a
  checker/trimmer, not a resolution emitter. RUP-expansion (each DRUP addition justified by reverse unit
  propagation → a resolution chain) is a standard, tractable self-implementation at n≤60.
- **DPLL ≡ tree resolution** is textbook (Beame/Pitassi; Buss; Beyersdorff et al.): a DPLL decision tree
  unfolds into a tree-resolution refutation. Extracting it directly (no DRAT, no drat2er) is sound and
  well-known.

**Decisions.**
- **Both samplers self-implemented; zero external proof tooling.** S1 = randomized constructive saturation
  (reuse Desert Map's `constructive_search`, instrumented with provenance + sub-DAG extraction). **S2 =
  self-written randomized DPLL→tree-resolution** — dependency-light, and structurally distinct from S1 (tree
  vs DAG), which is exactly what H3 needs. The pysat-Glucose42-DRUP + self-written RUP-expander path is a
  documented **v1.1 cross-check**, not built now.
- **R3 (soundness):** S2's extraction regresses conflict clauses through unit propagations (resolving out
  propagated literals against their antecedents, reverse trail order, at every level) before per-node
  resolution — implemented explicitly, not left for the verifier to catch. Confirmed: both samplers verify
  100% on random unsat n=20 (real propagation).

## I2 — Prior art: sampling the PROOF SET

We found **no prior empirical study** that samples the population of refutations of one instance and
characterizes it statistically. Nearest neighbors (adjacent, different):
- **Shortest-proof optimization** — Sidorov et al. 2024 (arXiv:2411.07955): branch-and-bound for *one*
  minimal-length resolution proof. Optimization, not population sampling.
- **MUS enumeration/counting** — Bendík & Meel (CAV 2020/21): enumerates/counts minimal unsatisfiable
  *cores*, a coarser object than the refutation set.
- **Operational proof diversity via seeding** — proof-minimization pipelines randomize solver seeds "for
  more diverse exploration of the space of valid proofs," but do not statistically characterize the
  population.
- **Solution-space geometry** — Achlioptas–Coja-Oghlan clustering/OGP is the satisfiable-side analog Census
  transposes to the refutation side.

**Decision.** Frame the population-statistics angle as the novel contribution; position against Sidorov 2024
and MUS counting as adjacent-but-different. State novelty as "we are not aware of prior work," not "none
exists" (thinly-indexed niche; a web negative is not literature-complete).

## I3 — Clause identity for overlap

**Decision.** Original clauses get stable IDs; every derived resolvent is identified by its **canonical
sorted-literal tuple** (`refutation.clause_id`), so identical resolvents match across proofs. A proof's
identity set = canonical ids of every clause node in its DAG (parents used + resolvents). Overlap = **Jaccard
on these sets → q = 2s−1** (Desert Map I2 convention for sparse sets). This is the single source of clause
equality (AGENTS.md invariant 6) — never compare by step index or derivation order.

## Early empirical confirmation (C1)
Both samplers verify 100% on random unsat n=20; median pairwise Jaccard 0.10 (S1) / 0.16 (S2) — far below
the 0.95 no-plurality kill line (**H1 supported**). S2 tree proofs are ~9× longer (median 153 vs 15) with a
17-clause backbone vs S1's 1 — a stark **province separation** that empirically vindicates the R1 decision to
judge H3 on trends, not levels.
