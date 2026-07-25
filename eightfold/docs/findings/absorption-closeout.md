# The absorption arc, closed — and the two-property split, standing

**Date:** 2026-07-24. Consolidated close-out of the Mosaic locality hypothesis and the Quarry v2 recruitment
+ rerun. Seals of record: `prereg_v10` (+ clarification-01 resolution ladder, + addendum-01 the 89-row
re-run), `prereg_v11` (Mosaic v3 G0, strategic), `prereg_v13` (Quarry v2, the third and operational seal).
Estimator throughout: `structure.stratified_cramers_v` (defect #15 fix, gated by the `hardmap verify`
known-answer test). Locality is an approximate blind-coded variable (κ=0.646 at 3-class). **Nothing
rescores; every prior verdict stands as scored.** Frozen bytes byte-identical (`atlas` 6d53a4f1, `atlas_v2`
784f4739, `atlas_v3` e62f3c28, `mosaic-locality` 4c7ef94c).

**Headline.** The single-variable absorption hypothesis — *one latent "locality" absorbs the
approximation↔parameterized coupling* — is **closed with a powered MISS at the only resolution the natural
corpus can support**. It is not "locality refuted": the same blind label **carries the approximation charge
robustly and replicates out-of-sample** (V ≈ 0.5–0.6 across four independent draws). What died is the
one-variable claim; what stands is the **two-property split**. The mechanism burden passes to the
intervention grid (Mosaic v3 G0) with a clean conscience.

---

## §1 — Scorecard of record

Verbatim verdicts across all seals; no reinterpretation.

| Bet | Verdict | Evidence |
|---|---|---|
| **P1 instrument** | **QUALIFIED at 3-class** | κ=0.646, anchors 7/7 both coders, separability clear. The resolution-ladder arc — κ measures the finest *reliable* granularity (5→3→2), not a kill threshold — resolved the L1 qualification at 3-class (details: `prereg_v10-clarification-01`, `mosaic-L1-findings`). |
| **P2 / P4-split** | **two-property SPLIT — confirmed and replicated out-of-sample** | Locality predicts **approximation** (V ≈ 0.55) and **not parameterized** (V ≈ 0.14–0.23). The sealed *symmetric* form ("both ≥ 0.35") is a **MISS**; the **asymmetry is the finding**. Both statements stand side by side — the label carries one charge, is near-silent on the other. |
| **P3 absorption — 3-class (sharp)** | **INSUFFICIENT RESOLUTION, terminal — price paid** | Quarry v2 lifted the both-real population 89→111 and the decomposable stratum 13→21, yet 3-class power stalls at **7/9 (78%)**, min-exp **3.6** at `decomposable × scheme`. Channel B **exhausted** the citable decomposable-scheme supply; the cell is intrinsically thin in the natural corpus. Per `prereg_v13` kill-criterion 3: **absorption is not decidable from the natural-problem corpus at the resolution the two-property split lives at.** This is a finding *about the corpus*, and it stands regardless of §2's coarse verdict. |
| **P3 absorption — 2-class (coarse)** | **powered MISS — does not absorb** | Descended per the sealed resolution ladder (see the ruling note below), outcome-blind. Pooled n=111, uncond V **0.283** → conditional (local vs delocalized) **0.453**, shrinkage **−0.60**, bootstrap CI **[−1.15, −0.21]** — *wholly negative*: conditioning does not shrink the coupling; the within-stratum association is *higher* than the marginal. **Tagged everywhere: 2-class speaks to the coarse local-vs-delocalized property only and is silent on the decomposable distinction.** |
| **P5 mixture calibration** | **corpus census, not a breach** (funnel form deferred) | Channel B fills every charge-citable candidate → *no selection occurs*, so its decomposable-enriched mixture (36% vs v3-new's 10%) cannot be a blindness breach; it is a structural fact of the corpus (decomposable problems disproportionately carry `open` param cells that resolve in the literature). P5's sealed *funnel*-blindness form waits for Channel A, if Channel A ever runs. |
| **P1 supply** | **HOLDS (≥22), via Channel B alone** | 55 candidates researched blind on charge-citability → 23 fillable at R20 → **dual-pass independently verified → 22** (1 refuted: `maximum-feasible-linear-subsystem`, cited result parameterizes by dimension not the named parameter → open). 22 net-new both-real = the ≥22 bar exactly; Channel A not run (grounding I3: the blind funnel cannot reach the decomposable-scheme cell). |

*Prior-run verdicts stand and are referenced, not restated: canon-47 P3 INSUFFICIENT and the
HIT-ish→MISS→INSUFFICIENT reversal arc (`mosaic-L3-L4-findings`, `methods-thread` instance 14).*

**The resolution ruling, logged (owner, 2026-07-24).** Descending to 2-class is the ladder's *designed exit*,
not a reversal of addendum-01. At n=89 the sharp 3-class rung was **purchasable** — the price was named
(~25 rows) and a recruitment channel existed — so descending then would have been premature coarsening while
the sharp question was still buyable. Tonight the situation is **terminal**: Channel B exhausted the citable
decomposable-scheme supply, the starved cell is intrinsically thin in the natural corpus, and kill-criterion
3's terminus *is* the honest 3-class verdict. Descending when the finer rung is provably unreachable is
coarsening *because the sharp question has no population* — categorically different from coarsening *to
manufacture an answer*. The one wall that protects believability held: the descent was **outcome-blind** —
the 2-class statistic was uncomputed until the rung was ruled.

---

## §2 — Three-population tables (standing law)

Marginals and per-stratum n before any V. All CIs are seed-deterministic bootstrap (seed 20260724, 2000
resamples), sized to both-real counts. Estimator: `structure.stratified_cramers_v`; defect-#15 gate **green**
(`hardmap verify`: conditional-independence→~0, Simpson marginal-0.33/conditional-0.00→~0, perfect→~1).

**Split stability — V(locality, charge) across four independent draws** *(the out-of-sample replication)*:

| population | n | V(loc, **approx**) [95% CI] | V(loc, **param**) [95% CI] |
|---|---|---|---|
| canon-47 | 47 | **0.619** [0.54, 0.78] | 0.161 [0.00, 0.39] |
| v3-new-42 | 42 | **0.511** [0.28, 0.73] | 0.000 [0.00, 0.45] |
| recruited-22 | 22 | **0.488** [0.31, 0.80] | 0.325 [0.00, 0.73] |
| **pooled-111** | 111 | **0.547** [0.45, 0.67] | 0.231 [0.15, 0.38] |

The approximation column is stable and clears 0.35 in every draw; the parameterized column stays low
throughout. **The two V's CIs are disjoint on the pooled set (0.384 < 0.451).**

**P4 marginal honesty (rider 2).** V(loc, param)'s CI is *wholly* below 0.35 only on prior/canon draws (hi
0.333 on canon-47, 0.393 upper is the small v3-new sample). On the enlarged pooled set its upper bound is
**0.384 — crossing 0.35** — because the recruited W-hard-param rows carry a little more locality↔param
signal (recruited point 0.325). That small drift is worth one sentence: **it is the first hint that the
parameterized side is not fully inert to structure** — consistent with a *second, weaker* structural
property on the param channel, not with the single-locality claim.

**Absorption — three populations, 3-class (sharp) and 2-class (coarse)**:

| population | n | uncond V(approx,param) | 3-class cond (stratified) | 2-class cond (stratified) |
|---|---|---|---|---|
| prior-89 | 89 | 0.366 | 0.447 | 0.514 |
| recruited-22 | 22 | 0.000 | 0.430 | 0.478 |
| **pooled-111** | 111 | **0.283** | 0.385 *(INSUFFICIENT — not scored)* | **0.453 — MISS** |

**The three P3 estimators, labeled (rider: every P3 telling carries all three).** On the historical canon-47
(the reversal arc): averaged-per-class-V **0.797** *(the defect-#15 bug — not a conditional association)* ·
mis-normalized stratified **0.911** *(my over-correction)* · correct pooled-within-stratum **0.644**. On the
Quarry-v2 pooled-111: averaged-per-class **0.311** · correct 3-class stratified **0.385** · unconditional
**0.283**. All three of the pooled trio now point the same way — **no absorption** — but under the 3-class
floor the point is moot; the scored verdict is the 2-class **0.453 MISS**.

**Weak-coupling context (rider 1) — stated next to the 2-class number, not in a footnote.** The pooled
unconditional coupling is **0.283**. The coupling this whole hypothesis set out to explain was the
canon-core **0.73**, and it is **roster-conditional** (B1): 0.73 canon-core → 0.366 at 89 both-real → 0.283
at 111. So the 2-class MISS adjudicates a **modest object** — "does the coarse binary absorb a 0.28 coupling"
— and **must not be read as adjudicating the canon-core 0.73**. The strong coupling lives in the canon core;
on the broad both-real population there is little of it left to absorb.

---

## §3 — The split's wording, ruled

Carry both, in this structure, never fused:

**Primary (conservative, asserted):** *Structure-locality, as blind-coded, carries the approximation charge
and not the parameterized charge; the carrier of the approximation↔parameterized coupling is **not** this
label.* This is what four independent draws and a powered 2-class MISS support directly.

**Candidate (clearly marked, not asserted):** *The coupling may route through the **objective's relationship
to structure** — "objective-channelness" — a second property distinct from decomposition-locality.* Support
on the record: **P5's violator fingerprint** (off-diagonal gradient-benders code `delocalized` **4/5** vs the
on-diagonal controls' **6/13**; `subset-sum`, the dissociation exhibit, codes `decomposable` — decomposable
*structure*, off-diagonal *coordinate*), the **knapsack originating dissociation** (FPTAS × W[1] —
decomposable structure, off-diagonal parameterized coordinate), and the **§2 param-side drift** (V(loc,param)
rising to 0.23 with its CI now touching 0.35). This candidate is **not yet isolated by intervention** — that
is G0's job, and it is the only thing that can promote it from candidate to claim.

A fourth support arrived from the contamination-free synthetic roster — but as a *row-level* coupling, not
the paired-discordance figure that circulated: on the frozen Lattice-v3 Boolean roster (166 both-real
symmetry-class rows, no human curation) **V(approximation, parameterized) = 0.256, CI [0.13, 0.398],
"COUPLING PRESENT"** (prereg v31, sha `29c517e8`). See §4's sixth line and its caveats.

> **The phantom, retired (incident closed).** A figure "OR ≈ 4.6" from a *paired-discordance* design
> circulated in reviewer summaries; it had **no artifact, and could never have had one.** The design — over
> symmetry-class pairs, is Min-vs-Max approximation-discordance associated with parameterized-discordance —
> is **structurally degenerate on this roster**: the parameterized oracle is objective-*independent* by
> construction (`objective_oracles.parameterized` is a relation-level Marx/OCSP property, no objective
> argument), so **param-flip ≡ 0/83** across the usable pairs and the 2×2's param-flip column is empty — OR
> undefined, McNemar trivial. The ghost was not a lost result but an *impossible* one. Retired with its
> mechanical reason; the census that caught it and the design lesson are in the methods thread
> (2026-07-24). The candidate reading loses this leg and keeps the three real ones above plus §4's sixth.

---

## §4 — Convergence: independent designs, one hypothesis

The two-property split is not one statistic; it is where separate measurements, taken by different
instruments with independent failure modes, agree on the same shape.

| design | instrument | independent failure mode | result | direction |
|---|---|---|---|---|
| **Judged labels on the canon** | blind LLM coders, 3-class rubric, encoding-only input | coder bias / rubric leakage | V(loc,approx) **0.55**, V(loc,param) **0.14–0.23** | locality ‖ approx, ⊥ param |
| **Violator fingerprint (P5)** | mechanical off-diagonal cell query + blind labels | miscoded anchors | off-diagonal `delocalized` **4/5** vs on-diagonal **6/13** | gradient-benders are delocalized |
| **Kernel independence (P6)** | R20 kernel-status column, netted | kernel-theorem confound | V(kernel, locality) **0.28** (weak) | certificate-locality partially distinct |
| **Instrument strain (L1)** | inter-coder specific-agreement | — | coders split cleanly at 3-class, fail the `entangled/mixed` seam (spec-agr 0.16) | the label strains where two properties overlap |
| **Originating dissociation** | frozen atlas coordinates (pre-coding) | none (mechanical) | `knapsack` FPTAS × W[1]; `subset-sum` decomposable × off-diagonal | structure and coordinate come apart |
| **Natural-roster coupling (Lattice-v3)** | synthetic Boolean CSP roster, oracle charges, no human curation | proxy-universe validity | **V(approx, param) = 0.256, CI [0.13, 0.398]** — COUPLING PRESENT | coupling exists on an uncurated population |

Six filed lines, taken blind and by different instruments, converge on the same shape: one structural
property drives approximability, a second (certificate-/objective-side) property is partially independent of
it, and the approx↔param coupling is *present on a population no human curated*. **The sixth line carries two
caveats, verbatim:** it is a **row-level** association, **not** paired-discordance — the flip design that
would have been genuinely paired is structurally unavailable on this roster (parameterized is
objective-independent by oracle construction; see §3's retirement and the methods thread) — and its
**direction is unresolved** (Spearman ≈ 0.02: the coupling is present but not monotone). It is the
contamination-free arm the spine wanted from this roster — the coupling *existing at all* on an uncurated
population — and it was in the record under prereg v31 the whole time, which is its own small lesson about
reaching for a phantom when a filed number already answers the question.

---

## §5 — Methods entries

**Instance 14 — the flagship mechanism bet, scored honestly in both directions under maximum temptation,
now across the full arc:** HIT-ish (buggy averaged-V 0.797, hopeful frame) → MISS (my mis-normalized 0.911,
over-invoking "don't move the metric") → INSUFFICIENT (owner's denominator challenge surfaced defect #15;
correct estimator + pre-sealed power check) → **Quarry v2: 3-class INSUFFICIENT-terminal + 2-class powered
MISS**. Optimism would have scored it HIT; conservatism a wrong MISS; the seal scored it correctly at every
step. The reversal arc *is* the contribution, whether or not the bet ever landed.

**Defect #15, the permanent gate.** Averaging per-class V's is not a conditional association. The fix is the
correct pooled-within-stratum-χ² estimator **plus** a `hardmap verify` known-answer test that runs before
the estimator touches real data — the mechanical check instances 6 and 10 lacked. Green throughout Quarry v2.

**The delegation boundary, second instance (2026-07-24) — verdict-shaped numbers refused without a run.**
The consolidated-note directive itself arrived carrying specific verdict numbers (a "0.6% shrinkage, 94%
power" powered MISS; "11 param fills"). No completed run stood behind them. The refusal to write them into
the record — *against the owner's own directive* — is logged as the positive pattern: **the record is sealed
against expectation exactly as the estimator is, and the source of a number, including the owner, does not
change that.** The run then landed elsewhere than the directive's numbers (INSUFFICIENT-then-MISS on 22
verified fills, not a 94%-power MISS) — which is precisely why the refusal mattered.

*Three times now the seal decided against the strongest available pull: the reversal arc, the refusal, and
the outcome-blind descent ruling.*

---

## §6 — What's open, with owners

- **Objective-channelness isolation** → **Mosaic v3 grid, G0 next** (owner-sealed; Strata v2 spec pending
  from owner before G0 seals). The candidate mechanism (§3) is promotable only by intervention on a synthetic
  ground where structure and objective-channelness are varied independently.
- **The within-class residual at sharp (3-class) resolution** → future recruitment, **price now known and
  named**: the natural corpus cannot supply the `decomposable × scheme` cell (Channel B exhausted it; the
  three remaining candidates — euclidean-tsp, constrained-shortest-path, number-partitioning — are genuinely
  parameterized-open). Sharp absorption is a **synthetic-grid** question, not a natural-recruitment one.
- **Channel B's 22 param fills — Gate-4 sitting complete (2026-07-24):** **21 promoted to `confirmed`**
  (owner primary-source read, atlas-**v3.1**-track; the program's first owner-`confirmed` cohort since v1),
  **1 retracted to `open`** — `geometric-disk-cover`, object-drift caught at the gate (free-placement
  unit-disk-cover W[1] is unpinned; the fill rode a squares citation; methods-thread instance 17). Full
  record: `quarry-v2-gate4-sitting.md`; promotions: `quarry-v2-gate4-promotions.jsonl`.
  **Footnote to the sealed run (ruling: footnote, not rerun):** the absorption verdicts stand as scored on
  the 22-fill population at seal time; `#11` was retracted *after* the run through the designed gate, and no
  verdict's arithmetic turns on it — **verified**: 3-class 7/9 with or without it (INSUFFICIENT unchanged);
  the 2-class MISS's sealed CI [−1.15, −0.21] is far from the +0.5 bar (point −60% → −59%); the split CIs are
  unmoved at n=110 (V(loc,approx) 0.547 → 0.539, V(loc,param) 0.231 → 0.230). Not a defect in the run — a
  population member retracted through the gate, the system's normal metabolism. Several fills also *correct*
  frozen `open` cells the literature has since settled (`graph-burning` W[2]-complete, etc.).
- **Errata candidates** (`bin-packing`, `bin-covering`, `firefighter`) remain on the E-track, independent.

---

## §7 — Program position

The single-variable era of the mechanism program is over, ended not by fatigue but by a **powered kill at
the only resolution the natural corpus supports**: the coarse binary does not absorb the coupling, and the
sharp resolution has no population to test at. The two-property picture is now **the only one standing** —
one blind structural property carries approximability with a replicated V ≈ 0.55, a second property carries
whatever couples it to the parameterized side, and no single "locality" does both. The absorption arc closes
at three verdicts that belong together: **INSUFFICIENT** (sharp, terminal — a fact about the corpus),
**MISS** (coarse, powered — a fact about the coarse property), and **the split REPLICATES** (the finding
that outlived the question). The designed test of the candidate mechanism is the intervention grid, and it
inherits the burden clean.

**The mechanism sentence, in its conservative form, as the close:** *structure-locality, as blind-coded,
carries a problem's approximability and not its parameterized complexity; the coupling between the two is
carried by something this label does not capture — and isolating that something is an experiment, not a
correlation.*
