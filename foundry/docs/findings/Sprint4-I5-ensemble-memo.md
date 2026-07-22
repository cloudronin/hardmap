# Sprint 4 · I5 — per-family ensemble memo  [OWNER-REVIEW CHECKPOINT — before any generation]

**Purpose.** Log the per-family random-CSP ensemble decisions *before* generating a single instance (I5 discipline).
This memo is a STOP-for-owner-review item: it surfaces one load-bearing instrument finding, a build-scope decision,
and a prereg amendment that all need a ruling before Task 1b (generation) runs. Nothing below has been generated
or measured.

---

## §1. The load-bearing finding: the named apparatus measures the TRANSPOSE of the landscape charge

The plan's Task 1 names `sampler_s1`/`sampler_s2` (+ the Proof-Census metric suite) as "reuse unchanged" for the
measured columns. A thorough read of the apparatus (reuse map archived) establishes:

> **`sampler_s1`/`sampler_s2` are PROOF-space samplers, not solution-space samplers.** They sample valid
> **Resolution refutations of UNSAT CNFs** (they derive the empty clause); they never produce satisfying
> assignments. Every metric — `backbone`, `province_separation`, overlap `P(q)`, proof `lengths` — measures
> **refutation-set geometry**. Proof-Census states this explicitly: solution-space clustering/OGP is "the
> satisfiable-side analog Census transposes to the *refutation* side."

But the FOUNDRY_SPEC **`landscape`** charge — `{clustering-OGP-refuted, clustering-physics, clustering-proven,
freezing-measured}` — is **solution-space** geometry (the geometry of the *satisfying assignments*). And I6
(prereg_v4) is defined over `landscape`. So the apparatus, as-is, measures a **different charge** (`proof_size` /
refutation geometry) than the one I6 needs. This is exactly the split your Task 1 text already drew — "P-side
languages need the solution-side instruments instead — landscape of the solution set, *not refutations*" — now
confirmed at the code level: **the solution-side instrument the plan calls for does not exist in the apparatus.**

## §2. The good news: your hybrid split DECONFOUNDS I6

Assigning instruments by language class (your Task 1 design) turns out to remove a confound I flagged in the
interim note. The census rows split as:

| localization | decision | # rows | which |
|---|---|---|---|
| **bounded-width** | **P (all)** | 9 | horn-sat, dual-horn, 2-sat, zerovalid-horn, zerovalid-bijunctive, onevalid-dualhorn, onevalid-bijunctive, order-3, median-3 |
| **unbounded-width** | **P (affine)** | 5 | xor-sat, zerovalid-affine, onevalid-affine, lin-eq-z3, lin-eq-z3-b |
| **unbounded-width** | **NPC** | 5 | 3-sat, nae-sat, one-in-three-sat, 3-coloring, nae-3dom |

If the `landscape` (solution-side) instrument is applied to the **P-decision** languages (rows 1–2 above), the I6
landscape contrast becomes **9 bounded-width-P vs 5 affine-unbounded-P — every row decision-P.** The confound
between width and decision-complexity vanishes *by construction*: I6 becomes a clean test of whether **width**
(not decision-hardness) predicts solution-space ruggedness, among uniformly-easy-to-decide languages. The affine
block is not a side-control here — it **is** the unbounded-width arm of the contrast, and it is the classic
decision-easy-yet-solution-rugged case (random k-XOR solutions provably shatter/OGP). The 5 NP-hard rows go to the
**proof-side** instrument (`proof_size` + refutation geometry) — a separate, apparatus-native deliverable.

**This is the strongest available I6 design**, and it is *more* empirical (less theorem-forced) than the
alternative of measuring everything proof-side (see §3, Option A) — where "bounded-width ⟹ short refutation" is a
proof-complexity theorem (Ben-Sasson–Wigderson), which would re-import exactly the R25-forcing that Task 0 just
closed out. The solution-side width→clustering link is genuinely empirical.

## §3. Instrument options + build scope

| | measures | fills | reuse | I6 | R25 risk |
|---|---|---|---|---|---|
| **A. proof-side only** | refutation geometry of UNSAT instances | `proof_size` | apparatus **unchanged** | bounded→short/smooth proofs, but partly **theorem-forced** (BSW width–size) | HIGH (re-forces) |
| **B. solution-side only** | solution-space clustering of SAT instances | `landscape` | metric *concepts* only; **net-new sampler** | all rows, but NP-hard arm re-confounds with decision | low |
| **C. HYBRID (recommended)** | proof-side for NP-hard; **solution-side for P-side** | `proof_size` (NP) + `landscape` (P) | apparatus unchanged for proof-side; **net-new solution sampler** for P-side | **deconfounded** (bounded-P vs affine-P) | low |

**Net-new build for the solution-side instrument (Options B/C).** What transposes vs what is new:

- **Reuse unchanged (proof-side, for the 5 NP-hard `proof_size` rows):** `sample_k`, `sweep.sample_k_parallel`,
  `sampler_s1/s2`, `glitch_bound`, `province_separation`, `sampler_agreement_trend`, the M1 verifier gate — all
  genuinely CNF-general (verified: no width-3 assumption in any of them).
- **Net-new (solution-side, for the 14 P-side `landscape` rows):**
  1. a per-Γ random-instance generator + CNF encoding (needed regardless; domain-3 rows need a direct/log CNF
     encoding before any Boolean apparatus applies);
  2. a **satisfying-assignment sampler** — pysat/Cadical `get_model` + randomized polarity/restarts + blocking
     clauses for diversity (net-new; the apparatus has none). For **affine** languages this is *exact and
     unbiased* (uniform over the solution coset by linear algebra) — the best-calibrated deception control;
  3. **solution-space metrics** = the Census metric *concepts* re-pointed from clause-id sets to assignments:
     overlap `q = 2·Jaccard−1` (or normalized Hamming) between solutions, **backbone = frozen variables** (same
     value across all sampled solutions), **clustering = P(q) modality**. Structurally these reuse `glitch_bound`
     (feed a solution-metric `metric_fn`) and the trend logic; `backbone`/`province_separation` need a solution
     transpose.
- **Also needs adaptation even for pure reuse (per the map):** `planted_backbone_calibration` is hardwired to
  `gen_planted`'s core-index layout — a new planted-terrain generator + core convention is required; and
  `sampler_agreement_trend` bakes in "ascending α = harder," which must be re-checked per family.

**Honest scope statement:** Option C is *not* "reuse unchanged." It reuses the proof-side apparatus unchanged and
builds a bounded net-new solution-side instrument (generator + model-sampler + transposed metrics). Estimate: the
generator + affine-exact + Cadical-restart sampler + solution-overlap metrics are a focused build well inside the
Sprint-4 attention budget; the CPU cost lands in the measurement runs (Task 2), under the $50 ceiling with kill-3.

## §4. prereg_v4 amendment required (pre-measurement, legitimate)

prereg_v4 currently says the affine block is "reported separately, NOT averaged into the I6 contrast." Under the
recommended hybrid design that is **self-defeating**: the affine rows are the *only* unbounded-width landscape
rows, so excluding them leaves I6 with no unbounded arm. The amendment (still before any measured cell — pure
pre-analysis): **affine is the unbounded-width arm of the I6 landscape contrast** (the deconfounder), reported as
such; the NP-hard languages are the proof-side `proof_size` deliverable, not part of the landscape contrast; the
XOR deception-control role (must read rugged) is retained as a *calibration* gate on the affine rows. → OWNER
DECISION 1.

## §5. Per-family instrument assignment + α-grids

| family | rows | instrument | ensemble regime | α-grid (proposed; fixed at calibration) |
|---|---|---|---|---|
| NP-hard Boolean | 3-sat, nae-sat, one-in-three-sat | **proof-side** (`proof_size`) | UNSAT above threshold | bracket the family threshold, decreasing-α = harder (3-SAT ≈4.27; NAE ≈2.1; 1-in-3 ≈0.62) — verify at calibration |
| NP-hard domain-3 | 3-coloring, nae-3dom | **proof-side** (`proof_size`) | UNSAT, CNF-encoded | bracket the 3-colorability / NAE-3 threshold (avg-degree grid) |
| affine (unbounded-P) | xor-sat, zerovalid-affine, onevalid-affine, lin-eq-z3, lin-eq-z3-b | **solution-side** (`landscape`) — deconfounder + deception control | SAT; solutions = linear coset (exact uniform sampling) | density where the coset dimension sweeps rich→sparse |
| bounded-width Boolean | horn-sat, dual-horn, 2-sat, zerovalid-horn, zerovalid-bijunctive, onevalid-dualhorn, onevalid-bijunctive | **solution-side** (`landscape`) | SAT; structured solution set (lattice / median-graph) | density in the richly-satisfiable regime |
| bounded-width domain-3 | order-3, median-3 | **solution-side** (`landscape`), CNF-encoded | SAT; monotone/median solution set | as above |
| constant co-clones | zerovalid-dualhorn {x=0}, onevalid-horn {x=1} | **n.a. (R15)** | solution set is a subcube — no geometry to measure; every instance trivially SAT with no clustering | — |

Notes: (i) `average_case` is *parameterized, not measured* in the apparatus (no difficulty scalar exists) — I
propose deriving it only where a genuine hardness scalar is reachable (e.g. sampler budget-rate on the NP-hard
proof-side), else `n.a.` with reason; it is **not** on the I6 critical path. (ii) `proof_size` for the affine
family is *also* reachable proof-side (random 3-XOR needs exponential resolution) — a bonus cross-charge, optional.

## §6. Coverage vs the I6 floor (≥12 both-real landscape rows)

Recommended-hybrid landscape both-real set = **9 bounded + 5 affine-unbounded = 14** ≥ 12 ✓, all decision-P
(deconfounded), spanning both localization classes. Honest asymmetries to document: 9 vs 5 imbalance; the 5 NP-hard
rows are absent from the landscape contrast (they are a separate proof-side deliverable); domain-3 rows depend on a
faithful CNF encoding passing calibration.

## §7. Calibration gate (Task 1c — before any long run, a second owner-review checkpoint)

- **Proof-side anchor:** the 3-SAT family must reproduce the known Proof-Census C2 signatures — **backbone
  strengthens toward threshold** (trend +1, both samplers agree above the glitch floor) and **province
  separation grows toward threshold** (0.05→0.11 range). If it doesn't, the generator/wiring is broken.
- **Solution-side deception control:** the affine/XOR family's measured **solution** landscape must return
  **rugged-while-decision-easy** (clustered/shattered solution overlaps, i.e. bimodal `P(q)` / large frozen
  backbone) despite P-time decision — or the solution instrument is declared broken and no landscape cell is
  emitted. Because affine sampling is *exact*, this is a clean, bias-free calibration.
- **Planted / known-terrain + glitch floor** per family before any cross-sampler read; noise floor committed
  before any finding.

## §8. Owner decisions (please rule before Task 1b generation)

1. **Instrument strategy** — adopt **Option C (hybrid)** as recommended (proof-side reuse for NP-hard `proof_size`;
   net-new solution-side sampler for the 14 P-side `landscape` rows, testing a deconfounded I6)? Or A (pure reuse,
   proof-side only, accept the theorem-forced weakening + I6 not on `landscape`) or B (solution-side only)?
2. **prereg_v4 amendment** — approve reclassifying affine as the *unbounded-width arm* of the I6 landscape contrast
   (deconfounder), with its deception-control role kept as a calibration gate (§4)?
3. **Build scope** — approve the bounded net-new solution-side instrument (per-Γ generator + CNF encoding +
   Cadical-restart / affine-exact model sampler + transposed solution-overlap metrics), reusing the proof-side
   apparatus unchanged?
4. **n.a. list** — confirm the two constant co-clones ({x=0}, {x=1}) are the only genuine `landscape` n.a.; and
   that `average_case` is filled only where a real hardness scalar is reachable, else n.a.-with-reason (R15)?
