# Sprint 6 "Pebble" — findings (P6 synthesis)

The substrate hypothesis proposes the charges are projections of one quantity: **reach** — how far information about a
partial solution propagates through the constraint structure. Sprint 6 built and tested reach's first instrument on
the synthetic census. The result is honest and mixed, and the discipline that produced it is as much the finding as
the numbers. **Physics note (bridge hunt, `Pebble-bridge-hunt.md`, 2026-07-22): reach = the literature's point-to-set
correlation length = reconstruction = clustering α_d. Every phenomenon sentence below cites an owned object; the
contribution is the instrument and the census measurement, never the object.**

## Headline

1. The pairwise instruments (`corr`, `forcing`) were **DISQUALIFIED** for reach — they measure point-to-point
   correlation, and reach is point-to-**set**; parity is invisible to them.
2. A **point-to-set instrument was built and QUALIFIED** (boundary-shell bucketing), after one redesign.
3. Reach on the Boolean census is a **real, algebraic dichotomy** — affine long / bounded-width short, tracking the
   Schaefer split — that **strengthens with n** (not finite-size), with a **minority relation-level residue** (0.45 of
   the class gap, vs Sprint 4.6 terrain's decisive ~1.0).
4. Reach is **terrain-relevant** (predicts `landscape` incrementally, +0.096 held-out) — but a **free relation-level
   scalar (`tuple_dispersion`) is a cheap proxy** for it (corr 0.78, T1.2), carrying most of its terrain content.
5. **Reach factors *without* the geometry term** (T1.4/T1.3): the scalarization hypothesis *reach ≈ f(geometry,
   scalar)* collapses to **reach ≈ f(`tuple_dispersion`)** — a pure relation-level property needing no graph, no
   instances, no sampling, no solution sets. The expensive instrument earns a **characterization, not a keep**; the
   cheap probe that scales is **one relation feature**. **Deflationary about the instrument, expansionary about what's
   now reachable** (the canon rows, where every prior deferral was parked, are now cheaply measurable).
6. The substrate hypothesis's actual test — the **differential pattern across the charges** — remains **untested at
   v1 scale**, structurally (the discriminating charges are clone-constant; v1 has ~13 strata).

## The arc, in order (each step a sealed prereg + a scored verdict)

| step | prereg | verdict |
|---|---|---|
| Pilot: does `tuple_dispersion` decay with size? | v12 | INCONCLUSIVE underpowered → replicated at +0.7 on 16-fold roster (P1) |
| `corr`/`forcing` reach instrument, three-pole calibration | v17 | QUALIFIED `corr` (pairwise) |
| **Parity diagnostic** — reach is point-to-set, not pairwise | v20 | **`corr` DISQUALIFIED** (parity reads 0.03 at maximal propagation) |
| Point-to-set instrument + hand-count gate | v21 | built; sensitivity + specificity locked |
| Point-to-set calibration | v22/v23 | **QUALIFIED** (parity inverted to the top group; strict-single-max clause withdrawn) |
| Full sweep — dichotomy, within-class replication, size ladder | v24 | dichotomy REAL + algebraic + 0.45 residue |
| **T1.1/P4** — is the residue terrain-relevant? | v25 | **INCREMENTAL** (+0.096, p≈0) |
| **T1.2** — are reach and `tuple_dispersion` the same property? | (map) | **PROXY** (corr 0.78) |
| **T1.4/T1.3** — does *geometry + scalar* reproduce reach? does geometry add anything? | v14/v13/v26 | ceiling reached **by the scalar alone**; geometry superfluous (Δ +0.003…0.023); structural race a MISS |

## What earns its keep, and what carries forward

- **The expensive instrument earns a modest keep.** Reach adds a real +0.096 held-out increment over the free scalar
  for terrain (P4) — from the ~22% of reach's variance the scalar does not share (T1.2). **Correctly-attributed
  caveat:** reach and `ruggedness` are both solution-set-geometry summaries of the *same ensemble* (measured on
  different draws — seeds 980000+i vs 981000+i — so an ensemble-level relationship, not a same-sample tautology), so
  the contest against the *constraint-level* `tuple_dispersion` was **structurally uneven**, not a fair fight reach
  won on merit. The un-circular test — reach vs a **non-geometry** charge — is phase-2.
- **The free scalar is not just a proxy — it is sufficient.** T1.4/T1.3 (below) shows the geometry term is
  unnecessary: reach ≈ f(`tuple_dispersion`), a pure relation-level property. **Tier-1 net verdict:** the expensive
  instrument earns a *characterization*, not a keep — everything it buys for prediction, one free relation feature
  already carries, and that feature needs no graph, no instances, no sampling. **Deflationary about the instrument,
  expansionary about what's now reachable.**

## T1.4/T1.3 — the scalarization collapses to the scalar (prereg_v14/v13/v26)

The sealed test: does *graph geometry + a per-relation scalar* reproduce reach at its self-reliability ceiling
(ρ ≥ 0.90)? The added reported number (owner rider, before the run): does graph geometry improve on the scalar's
standalone ~0.78 **at all**? Held out by co-clone, R* = ensemble split-half, density-resolved.

| density | R* | scalar-only | +geometry | **increment** | struct-only (T1.3) | ρ vs 0.90 | **sealed verdict (literal)** |
|---|---|---|---|---|---|---|---|
| 0.5·α | 0.898 | 0.800 | 0.823 | **+0.023** | −0.006 | 0.917 | SCALARIZABLE |
| 0.7·α | 0.939 | 0.809 | 0.812 | **+0.003** | 0.114 | 0.865 | PARTIAL |

**Literal firing, then reading, kept separate** (the same discipline as the direction-blind (c) trigger): the sealed
verdicts are recorded as computed — SCALARIZABLE at 0.5, PARTIAL at 0.7. **The difference between them is not
scientifically meaningful.** The scalar alone sits at ρ ≈ 0.86–0.89 — just under the threshold — at both densities;
the geometry increment (+0.003 to +0.023) is within noise at 0.5 and vanishes at 0.7. A verdict tipped over the line
by a within-noise increment at one density and not the other is a coin landing on its edge, not a result. **The
result is: the geometry term is superfluous at both densities; reach ≈ f(`tuple_dispersion`).** The structural race
(T1.3) confirms it from the other side — geometry *alone* predicts reach at −0.006 to 0.114 held-out, i.e. essentially
nothing (its class-level information is redundant with what the scalar already carries).

**Stronger than the hypothesis it tested.** T1.4 asked whether reach *factors* as geometry × relation-scalar. It does
not need to: the relation-scalar suffices. That is a **simpler and more portable probe** than the one specced —
computable on any problem with identifiable constraint relations, including the canon's gradient-carrying rows
(vertex cover, clique, Steiner) where every previous deferral has been parked. The canon-unblock payoff is collected,
and by a cheaper route than sealed (no graph at all).

**Owner odds scored (35% scalarizable):** the *mechanism* call was right — "geometry adds little beyond the scalar"
is exactly what happened (Δ ≈ 0). The 35% hedged on the threshold axis; the sealed verdict came out borderline, so the
threshold call was luck and the mechanism call was the content. **Bridge-hunt rider NOT triggered** — geometry does
not weigh, so there is no "constraint geometry predicts propagation" claim to hunt.

## Methods chapter — two specification defects and one construct-validity error, one of each species

This sprint produced one instance of each of two distinct failure species; a methods chapter that names them (with
dates and owners) is more useful than one that anonymizes them.

- **Owner specification defect #1 — the "parity single-max" clause** (prereg_v22, `cc8bc14`, 2026-07-22). The pass
  criterion demanded parity outrank its own affine class-mate (2-affine), which no physics produces; caught by the
  measurement (co-top within noise), **withdrawn post-result, dated and flagged**.
- **Owner specification defect #2 — the direction-blind (c) trigger** (prereg_v24, `7daba39`, 2026-07-22). The
  finite-size trigger fired on gap *magnitude*, blind to whether the levels converge (artifact) or diverge (real
  dichotomy); caught by the measurement (divergence), refuted by a *pre-data* directional reading.
- **Builder construct-validity error — the pairwise blindness** encoded in `test_parity_blind_but_2affine_visible`
  (`166eec4`, 2026-07-22). The test recorded that pure parity reads zero on the pairwise observable; it survived P2
  qualification and the start of the P3 harness build **filed as a pole-selection technicality, not a construct-
  validity failure** — until a parallel investigation (I-SP) read it correctly.

**The lesson:** *specification errors* (the criterion was worded wrong) and *construct-validity errors* (the
instrument doesn't measure the target construct) are different species. The first is caught by disagreeing with the
measurement's verdict; the second is caught by asking whether the measurement measures the thing at all — and the
program's own tests can encode the second before anyone reads it. Both were caught by measurement, neither by review.

**Running thread — post-Pebble additions.**
- **Owner specification defect #3 — the `is_2monotone` predicate-list error** (Lattice / G2, L1 sourcing memo
  `3773b6f`, 2026-07-23). The G2 build plan's predicate list named `is_2monotone` as "the single most load-bearing new
  classifier," but 2-monotone is the PO condition for **Max-CSP / Min-CSP** (KSTW Thm 2.11 / 2.13), *not* for the
  **Max-Ones / Min-Ones** objectives Lattice actually uses (Thm 2.12 / 2.14). Building it would have produced a
  classifier that **never fires** on this roster; the predicates the theorems require are `is_width2affine`,
  `is_strongly_0valid`, and `is_IHSB`. **This one was caught by the L1 R20 sourcing gate — pinning the classification
  from the primary source before writing a line of oracle — and so is the first of the three caught by *review* rather
  than by measurement.** It amends the lesson above ("neither by review"): the I-phase sourcing gate the program now
  runs before every build made its first catch, at zero measurement cost, before the wrong predicate was written. A
  specification error is cheapest when the source that refutes it is consulted before the build, not after the run.
- **Owner specification defect #4 — the `affine ⇒ weakly-separable` bridge the per-pair netting didn't consult**
  (Prism / R2, prereg_v32, `0a9bf31`, 2026-07-23). The prereg's structural headline asserted that general
  weak-separability (the *parameterized* charge's determinant) is **orthogonal** to the classical Schaefer fingerprint,
  and its per-pair netting conditioned on the **literal** predicate each oracle reads. Both missed **affine ⇒
  weakly-separable ⇒ FPT** (Marx Ex 2.4): `counting` and `approx_counting` read `affine`, so `affine=FP` *forces*
  `param=FPT` — a theorem-identity. Because the two predicates carry different names (`affine` vs `general_wsep`), the
  literal-intersection netting never conditioned on `affine`, so the identity survived as a spurious **0.74 "residual"**,
  making prediction 5 a spurious MISS and refuting the sealed orthogonality claim. **The metadata was already in the
  entailment catalog** — `affine⇒FPT` is the *same affine off-diagonal* that broke the tautology blocker (G1) and
  flattened v3's trend — the inference simply wasn't drawn by a netting keyed on predicate *names* rather than logical
  content: **metadata recorded, inference not drawn**, the program's characteristic failure mode once more. **Caught by
  the R2 gate** (the spurious survivors) *before anything shipped* — the third of the four now caught by a gate rather
  than by a downstream surprise. Completed per the sealed named-bridge layer (the bridge belongs to a layer the prereg
  already defined); both residual sets reported permanently; the orthogonality claim scored as a dated sealed-claim miss.
- **Owner specification defect #5 — a prediction framed as "the gate that makes I6 askable" when the question is
  unaskable in the domain** (Prism v2 review, prereg_v33, 2026-07-23). Prism v2 carried the I6 localization-absorption
  test to arity 4 on the premise that bounded-width — *constant* on the param-real rows at arity ≤3, which is exactly why
  v1 scored absorption UNTESTABLE — would *vary* at arity 4 and thereby make absorption measurable; pred 2 was drafted as
  precisely that enabling gate. The inference not drawn: in the Boolean single-relation domain, unbounded-width-tractable
  = **purely-affine** (Schaefer), and the affine-implies-weakly-separable-implies-FPT bridge (the *same off-diagonal* as
  defect #4) **nets affine out** — so conditioning the bridge-completed residual on bounded-width is conditioning on a
  *constant* (one stratum, UNTESTABLE again), and conditioning the raw residual is *re-deriving the bridge*. Arity 4 does
  not make I6 askable; it relocates v1's degeneracy into an affine **confound**. **Metadata recorded, inference not
  drawn** — Schaefer's classification and the bridge were both on the table — the characteristic failure mode once more,
  now at the level of *which question the design can answer at all*. **Caught at the plan stage by review of the
  successor spec, before `prereg_v33` sealed and before any oracle or roster: the cheapest catch point in the ledger.**
  The sharper fact the owner named: the confound sat *independently* in **two** drafts — the owner's Prism v2 and
  Claude's own banked `Absorption-arity4-spec.md` — caught by **neither author**, only by the review pass over the
  successor. The corpus-question check is a property of *review*, not of care at drafting time, and cannot be delegated
  to the drafting party — either of them. Resolution: preds 3 & 4 dropped from the seal; the arity-4 experiment
  re-scoped to its one clean prize (the anti-canon Min-Ones replication, pred 5); the sharpened statement — I6 is
  unaskable in the Boolean single-relation domain at *any* arity, domain ≥3 its smallest well-posed home — banked, not
  specced.
- **Construct-validity error #2 — the tie-ignoring Spearman** (Prism v2 run, prereg_v33, 2026-07-23). The sealed
  direction statistic `_spearman` computed `argsort(argsort(·))`, assigning tied values *consecutive* ranks by array
  position — not Spearman's ρ on tied data. On the heavily-tied (approx-class × binary-param) roster it partly measured
  array order; the tell was that the arity-4 point estimate fell **outside its own bootstrap CI** (and the buggy
  Max-Ones arity-4 value was +0.750 where the correct value is +0.023). Corrected to tie-averaged ranks (verified vs
  `scipy.stats.spearmanr`). **This is the second member of the construct-validity species** — the first was the pairwise
  blindness above; same shape, *the machinery named the right concept and computed a different one*. The pairwise
  blindness sat inside a **qualified instrument**; this sat inside a **sealed metric**. The class now has **two members,
  which upgrades it from incident to pattern.** The new information this instance adds: **the defect propagated into an
  owner ruling before it was caught** — the "monotonicity did not return / direction does not come back" decomposition
  sentence was ruled on the buggy value (dated-corrected in `Prism-v1-findings.md` §5, the four-wall note, and the
  preprint-bound statement). *Instrument defects contaminate downstream **judgment**, not just downstream numbers* — the
  cost that makes catching them at the scoring gate worth the interruption. It flipped two scored verdicts on
  re-computation: Prism v2 pred 5 (buggy REFUTED → corrected REPLICATES-attenuated) and v1 pred 6 (buggy MISS → corrected
  HIT); both numbers kept permanently wherever scored (owner ruling — the seal said "Spearman"; tie-corrected is its
  faithful implementation).
- **Delegation protocol, recorded (2026-07-23).** The ripple from this correction stopped being mechanical the moment it
  flipped a scored verdict. The execution distinguished *"recompute the numbers per the ruling"* (mechanical, proceed)
  from *"revise narrative substance"* (a scored MISS→HIT, and the withdrawal of an owner sentence) and **escalated the
  second to the owner before writing it into any doc.** That boundary — recompute silently, but surface anything that
  reverses a verdict or an owner ruling — is the delegation protocol working, and earns its line here.

## Program status (against the test map)

- **Tier 1 (does the expensive instrument earn its existence?)** — **answered.** Qualified and characterized; earns a
  *characterization, not a keep* (P4/T1.2/T1.4). The cheap probe that carries forward is `tuple_dispersion` **alone**
  (T1.4: geometry superfluous) — a relation feature needing no graph, no sampling, no solution sets.
- **Tier 3 (scale-out) is now CHEAP for the reach content** — because the probe is a relation feature, the canon
  extension (`tuple_dispersion` on the gradient-carrying rows: vertex cover, clique, Steiner) needs **no sampling and
  no solution sets**. Sealed as the next step in `prereg_v27` — **sealed and UNAUTHORIZED, not started**: it is a
  Tier-3 item requiring its own prereg, its own known-answer check (the six canon∩census anchors, where both a canon
  charge and a census reading exist, are the natural calibration), and an explicit license statement.
- **Tier 2 (does the measure predict the charges differentially — the actual hypothesis?)** — **UNTESTED at v1
  scale.** The within-co-clone regime reaches only `landscape` (+ thinly `average_case`); the discriminating charges
  are clone-constant, so the between regime has ~13 strata and v1 structurally cannot adjudicate the uniform null.
  This is the honest end-state: **instrument built and characterized, hypothesis untested at scale** — and now with a
  *cheap route* (Tier 3) to the scale that would test it.
- **Two-level not gradient (T2.3, prereg_v23):** now measured, not just predicted — the phase-2 differential should
  expect two levels with a minority residue, not a strong/moderate/weak/none gradient.

## Standing discipline (honored across v12–v26)

Prereg before measurement; known-answer calibration before unknown sky; population/provenance gates before
interpretation (the P3 sweep declared 5 unmeasurable cells, not averaged); beat your own nulls (P4 permutation p≈0);
bridge hunt before novelty language (physics cited, not claimed); sealed predictions scored as they land including
the misses (the pilot's INCONCLUSIVE, the parity DISQUALIFICATION); **no metric substituted after seeing results —
the sealed threshold was never moved** (the T1.4 SCALARIZABLE/PARTIAL straddle recorded as literally computed, with
the reading — "coin on its edge, geometry superfluous" — stated separately, the same literal-firing-then-reading
discipline as the direction-blind (c) trigger); specification errors recorded as dated owner errors, never as
threshold adjustments.
