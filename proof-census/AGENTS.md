# proof-census — agent/contributor rules

Load-bearing invariants for anyone (human or agent) working in this product. Each encodes a decision from
the spec (`docs/specs/proof-census-v1-spec.md`) and the approved plan.

## What this is (one paragraph)

Proof Census maps the **population of valid Resolution refutations** of unsat random 3-SAT: sample many
proofs per instance with two structurally-different randomized samplers, then compute population statistics
(length, overlap P(q), backbone, shard regularity) on the verifier-passing proofs. Successor to Desert Map
(which asked "can local search navigate a relaxed proof landscape" and died at kill 6.1 with "no"); Census
uses the constructive sampler that scored 100% in Desert Map's calibration. Depends one-way on the frozen
`desert-map` product for the M1 verifier/fixtures.

## THE INVARIANTS (do not break)

1. **Verifier-gate everything.** Every sampled refutation is checked by `desertmap.verify.verify` BEFORE it
   enters any statistic. Unverified samples are discarded and **counted** (three-way accounting: verified /
   verify-discard / budget-exceeded). A statistic computed over an unverified proof is invalid.

2. **All claims are sampler-relative.** Census maps *sampler-reachable* proof populations (S1, S2), never
   "the refutation set" absolutely — uniform proof sampling is out of scope and known hard. Say "under
   sampler S" every time.

3. **H3/replication is TRENDS, not LEVELS (R1).** S2 (tree-resolution) and S1 (saturation DAG) differ in
   metric *levels* by construction (trees repeat work → longer proofs, different clause profiles). Judge
   replication on **agreement of direction/shape across the α sweep**, beyond the S1-vs-S1 glitch bound.
   The inter-sampler level gap is a **finding** (province separation), never an artifact. Kill-2 fires only
   if trend agreement fails on *every* metric.

4. **S2 tree-resolution extraction MUST regress through unit propagations (R3).** At a conflict, regress the
   falsified clause against the antecedent clauses of propagated literals until only decision literals
   remain, THEN resolve at decision nodes. Skipping this leaves propagated variables in the resolvents and
   the whole proof fails verification. Implement regression explicitly — the verifier is not the place to
   catch a design bug.

5. **S2 runs under a node budget (R2).** Budget-exceeded runs are counted separately from verify-discards
   and abandoned. If n=60 hard cells are impractical, S2 covers n ≤ 40 there and the **coverage asymmetry
   is documented in the writeup** — never silently drop a cell.

6. **Canonical resolvent identity is the single source of clause equality (I3).** A derived resolvent is
   identified by its canonical sorted-literal tuple; originals get stable IDs. Overlap/backbone compare
   these identity sets. Do not compare proofs by step index or derivation order.

7. **Pre-register before the sweep, kill honestly.** Predictions (H1–H3 directions, kill thresholds) commit
   to `results/prereg/` before C3. No-plurality and trend-level sampler-dominance are pre-registered
   outcomes, not failures — report them.

## Dependency

One-way: `proofcensus` imports `desertmap` (verify/instance/fixtures/discrete_search). Never modify
desert-map to suit Census (it is frozen at its M2 kill). Install both editable in one venv.

Run tests from inside this product dir: `python -m pytest tests -q`.
