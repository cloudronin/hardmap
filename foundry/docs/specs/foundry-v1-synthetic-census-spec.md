# Foundry v1 — Synthetic Census Spec (F1 hand-off)

<!-- In-repo canonical copy of ~/Downloads/foundry-v1-synthetic-census-spec.md. Build plan (Phase K kernel,
     N0-N5, owner riders A/B/C) tracked in the plan file; the F1 predictions are committed separately at
     docs/findings/F1-canon-or-computation-note.md (Rider C). This file is the frozen spec of record. -->


**Codename:** Foundry
**Status:** Draft for review — banked now, executed post-Crucible, post-defense (Oct 2026)
**Owner:** Vishnu
**Relation:** executes F1 (`F1-canon-or-computation-note.md`) tiers 1–2. Fifth project in the line: Desert Map (killed, banked) → Proof Census (instrument, C3 pending) → Eightfold (canon atlas, Move One closed) → Crucible (hardening, in flight) → Foundry. Answers the canon-vs-computation question and builds the tall/wide/diverse/replicated table the latent-factor question requires. F1 travels with this spec; its framing and predictions are normative.

---

## 1. Objective and pre-registered predictions

**Objective.** Build the first multi-charge atlas over a roster no human chose: constraint languages, generated and stratified, with charges assigned by classification theorems (oracle columns) and by the qualified instrument line (measured columns); then test whether the canon's structure reproduces.

Predictions inherited from F1 §4, to be locked in this project's prereg before any analysis:

1. **NPI calibration (known-answer):** the census's NPI row is empty by dichotomy theorem. Violation = pipeline failure, not discovery.
2. **Gradient persistence:** the approx⟷param gradient appears in tier-1 CSP-land with direction intact. Failure is the canon's-world finding, acceptable and stated in advance.
3. **Factor reproduction:** canon-fitted loadings (k = 3–4 prediction on file) reproduce within stated tolerance. **Gated on Factors v1 existing**; if Foundry runs first, this prediction is reported untested, never approximated.
4. **Tier-2 inhabitation:** ≥1 gap-list cell inhabited by construction within the box; average-case × landscape attempted first.

## 2. Scope

| In scope | Out of scope |
|---|---|
| Tier 1: Boolean census (exhaustive/stratified) + general-domain sampled tier | Tier 3 (arbitrary invention — undecidability boundary, F1 §2) |
| Oracle columns: decision, counting, approximation, proof-size(random), parameterized*, parallelization* (*pending I-phase verification) | New classification theorems |
| Instrument columns: landscape (+ average-case where measurable) via the Census apparatus, phase-gated | GPU spend; uniform sampling of anything |
| Tier 2: construction module for gap cells, `constructed` flag | Claiming constructed specimens as natural rows |
| Canon-comparison analysis (Crucible-hardened battery) | Move Two symmetry theory |

## 3. Design

### 3.1 Roster (tall, diverse, replicated — F1 requirements are binding)

- **Boolean tier:** enumerate relations to arity ≤ a (a set at I-phase; 3 minimum), languages as relation-sets, **one representative per co-clone** via the Post's-lattice structure; class sizes recorded. Deterministic → generations exempt (calibration property).
- **General-domain tier:** domains 3–4, languages sampled uniform-random, deduplicated to polymorphism-equivalence where the oracle makes that checkable; **one representative per realized class**, class sizes recorded.
- **Generations:** G = 3 independent generations of the sampled tier (and of every instrument-measured ensemble). Between-generation variance is computed first and is the noise floor all findings must exceed (glitch-check discipline, promoted to atlases). Self-averaging report: which statistics concentrate across generations, which don't (the latter is itself a finding).
- **Effective-n accounting:** every analysis reports distinct-charge-profile count alongside row count; factor-question power claims cite the former.

### 3.2 Oracle columns (statuses and provenance)

- Where the Post's-lattice literature *directly states* the classification (Boolean tier, most charges): `claimed` with citation — the prior-art finding (F1: "the columns exist; the table does not") makes this the default path.
- Where a dichotomy is *applied* (general domains; any cell requiring a condition-check): `derived` — dichotomy citation + logged condition-check, inheriting Crucible S4's validator gates and the R20 citation-establishes-the-value audit applied to condition-checks.
- Conditional results (Raghavendra/UGC) carry the atlas's standard conditional flag.
- Charge sources: decision (Schaefer / Bulatov–Zhuk), counting (Creignou–Hermann / Dyer–Richerby; DGJ approximate-counting trichotomy as refinement), approximation (KSTW; Raghavendra flagged), proof-size-random (Molloy), parameterized (Marx weight-parameter dichotomy — **I1 verification required**), parallelization (ABISV within-P refinement — **I1 verification required**).

### 3.3 Instrument columns (phase-gated)

Landscape (and average-case components where the instrument reaches) measured by the Proof-Census-qualified apparatus pointed at random CSP ensembles drawn per-language from the generated roster: sampler pair, verifier gating, S1-vs-S1 glitch bounds per ensemble, trend-based cross-sampler concordance, per-generation replication. Cells enter as `measured` with full experiment manifests (prereg, seeds, hashes, commit). The C3 caveat discipline (budget-binding disclosure) carries over verbatim.

### 3.4 Analysis (Crucible-hardened battery only)

- Null model adapted from Crucible S1 (typing + marginals + entailment preserved; values shuffled) — run on the census *before* any structure claim; the census's own claims must beat its own nulls.
- Covariation with entailment netting matrix-wide (the R25 procedure as standard, not exception).
- Gradient test per prediction 2; NPI row check per prediction 1 (first analysis run, as pipeline validation).
- Factor comparison per prediction 3 iff Factors v1 exists: held-out-prediction estimator primary (S1 disqualified MCA-style counts), canon-fitted loadings tested against census loadings at pre-stated tolerance.
- **Registration anchors:** the canon∩census overlap (3-SAT, 2-SAT, XOR-SAT, Horn-SAT, NAE-SAT, 1-in-3-SAT — Boolean languages present in both tables) is flagged and used to register the two coordinate systems before the loading comparison is read.
- **Control strata + projection rule:** known-different populations validate the fit by *projection, never inclusion* — fitting on a mixture recovers mixture axes. The census's built-in controls: the tractable co-clones as the easy stratum, and the affine (XOR) class specifically as the deceptive-terrain control (easy decision, hard measured landscape — the model must place it distinctively; failure is a pre-registered negative). Out-of-NP injections (QCSP tier) are a v2 extension, out of this box.
- Both weightings reported: per-class (problem-space structure) and class-size-weighted (typical-random-problem structure).

### 3.5 Tier 2 — construction module

Gap-list cells (imported from Eightfold A3, post-Crucible resize) treated as construction requests: padding, Ladner-style diagonalization, ensemble design. Constructed specimens enter flagged `constructed`, excluded from natural-population analyses by default, included in occupancy analyses explicitly labeled. Priority: average-case × landscape (the instrument line measures the landscape half of any candidate directly). A cell that resists construction under standard techniques gets a documented failed-attempt log — evidence of an unproven selection rule, reported as such.

## 4. Milestones and done-gates

| M | Deliverable | Done-gate |
|---|---|---|
| N0 | I-phase (below) + prereg (predictions 1–4, roster policy, generations, analysis battery, tolerances) | I1–I5 written up; prereg committed before any census build reaches analysis |
| N1 | Boolean census built + validated | All oracle columns filled at `claimed`/`derived` standard; validator clean; distinct-profile count reported |
| N2 | Oracle-column analysis: predictions 1–2 verdicts | NPI calibration passes (or pipeline halt); gradient verdict resolved per prereg rule; null-model envelope computed |
| N3 | General-domain tier + generations | G=3 built; between-generation noise floor computed; profile count re-reported |
| N4 | Instrument columns on selected ensembles | Glitch bounds + concordance per C3 discipline; `measured` cells validator-clean; prediction 3 verdict iff Factors exists, else "untested" recorded |
| N5 | Tier-2 attempts + full writeup | ≥1 construction attempt on the priority cell (inhabited or failed-with-log); F1 predictions ledger complete; canon-vs-computation verdict stated |

## 5. Kill criteria

1. **Oracle timebox (kill/rescope at N0→N1):** if general-domain dichotomy-oracle implementation exceeds its I-phase-set timebox, scope collapses to the Boolean census; predictions 1–2 proceed; prediction 3 is **reported untested** (F1's corrected fallback — never quietly downgraded).
2. **Profile poverty (rescope at N1):** if the Boolean tier realizes fewer distinct charge profiles than the I-phase-set floor, factor-question claims leave scope for this version; bias-verdict work continues.
3. **Instrument wall-clock (bound at N4):** per-ensemble measurement exceeding 2× its estimate before first checkpoint gets cut per C3 precedent; coverage asymmetries documented, never silently dropped.
4. **Time box:** attention ceiling 40 h paired across N0–N5; compute ceiling $50 (CPU batch only). Phases N3–N5 are individually deferrable without killing N1–N2's standalone value.

## 6. Investigation items (N0; confirm before build)

- **I1.** Verify the two memory-cited oracles: Marx's Boolean weighted-CSP FPT/W[1] dichotomy; ABISV's within-P refinement of Schaefer. Pin exact statements, scopes, and decidable conditions. If either fails verification, the column drops to `open` for the census and the width claim adjusts.
- **I2.** Boolean enumeration bounds: relations to arity a, co-clone stratification mechanics, expected distinct-profile count (feeds kill 2's floor). Post's-lattice tooling availability vs hand-rolled.
- **I3.** General-domain oracle feasibility: polymorphism condition-checking cost at domain 3–4; this sets kill 1's timebox.
- **I4.** Deep prior-art re-check (the hand-off search was survey-confidence): anything in the Post's-lattice program that assembled cross-task tables; anything census-shaped in the random-CSP literature. Verdict phrasing per house convention.
- **I5.** Ensemble design for instrument columns: which per-language random-CSP ensembles are well-posed (density dial, unsat regime for the proof-side instrument), and which canon ensembles serve as calibration anchors.
- **I6.** Localization charge (hypothesis-bearing): bounded width — solvability by local consistency — is polymorphism-characterized (Barto–Kozik) and hence oracle-derivable per language. Add as a census column; pre-register the localization hypothesis: bounded-width status co-varies with both approximation and parameterized charges, and conditioning on it absorbs a substantial share of the approx⟷param gradient (candidate identity for the "structural tamability" factor; motivated by the kernelization-as-containment / Baker-locality / expander-delocalization triad). Verify the Barto–Kozik condition-check's implementability alongside I3.

## 7. Sizing

| Phase | Est. hours (paired) |
|---|---|
| N0 (I-phase + prereg) | 4–5 |
| N1 (Boolean census) | 6–8 |
| N2 (oracle analysis) | 3–4 |
| N3 (general tier + generations) | 6–8 |
| N4 (instrument columns) | 8–10 |
| N5 (tier 2 + writeup) | 4–6 |
| **Total** | **31–41 h** |

Largest project in the line; N1–N2 form a self-contained first campaign (~13–17 h) delivering predictions 1–2 on their own.

## 8. Placement and sequencing

Post-Crucible, post-defense (Oct 2026), per the standing pipeline: Crucible → Factors → **Foundry** → charge-9 test. Prediction 3 is the only Factors dependency; N1–N3 can run before Factors if calendar favors it, with prediction 3 held open. Inherits: Crucible S4 `derived` machinery, Eightfold schema/validator/R-series discipline, Proof-Census samplers and concordance protocol, prereg-before-analysis as law. Hobby bucket, subordinate to praxis until defense; nothing here decays by waiting.
