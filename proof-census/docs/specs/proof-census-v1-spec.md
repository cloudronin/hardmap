# Proof Census v1 — Spec

**Codename:** Census
**Status:** Draft for review
**Owner:** Vishnu
**Relation to Desert Map:** successor with a different instrument, not a continuation. Desert Map asked "can local search navigate a relaxed proof landscape" and died at kill 6.1 with the answer no. Census asks "what does the population of valid proofs itself look like," using the method that scored 100% in Desert Map's probe table as the sampler. No relaxation, no gradients, no gradable almost-ness required.

---

## 1. Objective and hypotheses

**Objective.** First empirical map of the geometry of the *refutation set* of random unsat 3-SAT: sample many valid Resolution refutations per instance via randomized constructive search, and compute population statistics on the sampled proofs directly.

**H1 (diversity).** The refutation set is genuinely plural: independent sampler runs produce structurally distinct refutations, and diversity varies systematically with α.

**H2 (geometry).** Population statistics shift as α decreases toward threshold (hard direction, per Desert Map correction): proofs lengthen, pairwise overlap distribution changes shape, and a "proof backbone" (clauses/resolutions appearing in nearly all sampled refutations) emerges or strengthens.

**H3 (sampler-independence).** Geometry findings replicate across two structurally different randomized constructors. Statistics that fail this replication are sampler artifacts, not terrain.

**Non-goal.** Uniform sampling of the refutation set. Known-hard problem, out of scope; Census maps sampler-reachable proof populations and says so. All claims are stated relative to the sampler pair.

## 2. Scope

| In scope (v1) | Out of scope (v1) |
|---|---|
| Resolution refutations, random 3-SAT unsat, existing fixtures | Other proof systems; structured instances |
| Two randomized constructive samplers | Uniform proof sampling; learned/policy samplers |
| Population metrics: overlap P(q), length distributions, backbone frequency, shard regularity | Any search-landscape claim (that program is closed) |
| CPU compute, local + cheap batch | GPU spend |

## 3. Design

### 3.1 Samplers (the instrument pair, H3 is the point)

- **S1 — randomized saturation:** the Desert Map constructive prover with randomized clause-selection order and random tie-breaking; extract the used sub-DAG of the derivation as the sampled refutation.
- **S2 — randomized DPLL/CDCL trace:** run a solver with randomized branching (pysat, randomized polarity/branching seeds), extract the refutation from the DRUP proof log, converting to Resolution per the Desert Map I6 pipeline (drat2er path; never quote raw DRAT counts).
- K = 200 sampled refutations per instance per sampler; all verified by the exact M1 verifier before entering any statistic (unverified sample = discarded and counted).

### 3.2 Fixtures

Reuse Desert Map M1 fixtures unchanged (50 instances per (n, α), n ∈ {20, 30, 40, 60}, α ∈ {4.5, 5.0, 6.0, 8.0, 10.0}), same hashes, same versioning. Hard direction: α decreasing toward 4.267.

### 3.3 Metrics (population statistics on verified proofs)

| Metric | What it measures | H2 prediction (as α → threshold) |
|---|---|---|
| Proof length distribution per cell | Cost of refutation | Lengthens, variance grows |
| Pairwise overlap P(q) on proofs-as-clause-sets (Jaccard → q=2s−1, per Desert Map I2) | Plurality vs concentration of the proof set | Distribution shifts; possible multi-modal structure |
| Backbone frequency: per original clause and per derived resolvent, fraction of sampled proofs containing it | Mandatory vs optional proof content | Backbone strengthens (contradiction localizes) |
| Shard regularity (second-order): are inter-proof differences systematic (symmetry-related) or unstructured | Crystal vs rubble in the proof set | Exploratory, no committed prediction |
| Sampler agreement: all above computed per-sampler and compared | Artifact vs terrain (H3) | Agreement on direction and shape |

### 3.4 Controls

- Planted-core instances: backbone metric must identify the planted core clauses at ~100% frequency (calibration standard).
- XOR-SAT/Tseitin cells (from Desert Map I6 hard negatives, now repurposed): S2 with XOR-aware preprocessing off vs on, checking whether crystal structure shows in shard regularity. Optional, v1.1.
- Glitch check: run the full metric suite comparing S1-vs-S1 (different seed banks) — any "disagreement" at that level bounds sampler noise before S1-vs-S2 comparisons are read.

## 4. Milestones and done-gates

| M | Deliverable | Done-gate |
|---|---|---|
| C1 | S1 + S2 samplers with verifier gating | 200 verified samples/instance on n=20 cells; discard rate reported; planted-core backbone calibration passes |
| C2 | Population metrics + plots (reuse metrics.py/plots.py) | Glitch check (S1-vs-S1) bounds computed; one figure per §3.3 row |
| C3 | Full sweep + writeup | H1–H3 verdicts stated; all claims sampler-relative; concordance discipline from Desert Map applied |

## 5. Kill criteria

1. **No plurality (kill at C1):** if both samplers produce near-identical refutations per instance (median pairwise Jaccard > 0.95 across cells), there is no population to map. Write it up as a finding (effective proof uniqueness under constructive sampling) and stop — that is a result, not a failure, but it ends v1.
2. **Sampler dominance (kill at C2):** if S1-vs-S2 disagreement exceeds S1-vs-S1 noise bounds on every metric, all geometry is artifact; stop and report.
3. **Time box:** C1 within one weekend block of paired attention; total attention ceiling 12 h. Compute is CPU; budget ceiling $20 (batch CPU jobs only if local wall-clock exceeds patience).

## 6. Investigation items

- **I1.** Randomized-branching support and DRUP logging in current pysat/CaDiCaL; confirm drat2er path works on n=20 outputs before building S2.
- **I2.** Prior art check: proof-set sampling / "space of all proofs of an instance" empirical studies. (Solution-space sampling literature exists; proof-set analog believed empty per Desert Map I3, confirm.)
- **I3.** Clause-identity convention for overlap: original clauses are stable IDs; derived resolvents need canonical form (sorted literal tuple) so identical resolvents match across proofs. Settle before metrics.

## 7. Engineering

Same monorepo pattern, new sibling `proof-census/` or subpackage decision at Claude Code's discretion; reuse M1 verifier, fixtures, metrics/plots harness, and reproducibility clause (seeds, pins, hashes, manifest) from Desert Map §8. Artifact store only if batch jobs run; local parquet otherwise.

## 8. Sizing

| Phase | Est. hours (paired) |
|---|---|
| I1–I3 | 1–2 |
| C1 | 3–4 |
| C2 | 3 |
| C3 | 2–3 |
| **Total** | **9–12 h** |

## 9. Placement

Independent hobby-research project. Reuses banked Desert Map assets; produces population maps or a documented reason none exist. No users, no support surface, kill criteria as above.

---

## Build addenda (approved refinements R1–R3, drat2er path dropped)

- **I1 resolution:** both samplers are self-implemented; **S2 = randomized DPLL→tree-resolution** (no drat2er, no external-solver randomization). The pysat-Glucose42-DRUP + self-written RUP-expander path is a deferred v1.1 cross-check.
- **R1 (H3 = trends, not levels):** S2 (tree) and S1 (DAG) differ in *levels* by construction; H3 replication is judged on **agreement of direction/shape across the α sweep**, beyond the S1-vs-S1 glitch bound. Kill 2 fires only if trend-level agreement fails on every metric. Inter-sampler level gap is reported as **province separation** (a finding, not an artifact).
- **R2 (S2 compute guard):** node budget per S2 run; budget-exceeded counted separately from verify-discards; S2 falls back to n ≤ 40 at hard cells if n=60 is impractical, with coverage asymmetry documented — never silently dropped.
- **R3 (S2 soundness):** tree-resolution extraction regresses conflict clauses through unit propagations (resolving against propagated literals' antecedents until only decision literals remain) before per-node resolution.
