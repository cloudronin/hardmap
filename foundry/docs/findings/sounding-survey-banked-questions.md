# Sounding survey — banked questions

**Status: BANKED QUESTIONS. Not findings, not claims, not scored.**
Source: `sounding_survey_readings.json` — 114 matched-null excess readings over 20 rows, exploratory, no
sealed prediction. Anything below caught the eye during a descriptive pass and is written down so a later
design can pose it properly. **Nothing here may be cited as a result.**

---

## Q1 — RESOLVED 2026-07-26: forcedness is now derived, and the fix had a second half

**Closed by ruling.** `theorem_forced` is no longer a hand-written list. It is **derived from Marrow's
pinned templates** — bijunctive ⇒ majority-forced, affine ⇒ minority, horn ⇒ min, dualhorn ⇒ max — the
join both artifacts already computed and nobody had made. **62 flags changed**; the four plainly-forced
readings (`bipartiteness`, `vertex-cover`, `independent-set`, `clique`, all majority) now carry the right
flag with derived provenance.

Two boundaries were needed, and collapsing either would have replaced one wrong flag with another:

- **Region kind.** `solutions` and `feasible` inherit the template's guarantee; an **`optimal` region is a
  sub-level set and carries none**. Optimal regions are never forced.
- **Three states, not two.** Only **11 of 20** rows have a pinned template. For the rest forcedness is
  `null` — **UNDERIVABLE, which is not `false`.**

### The second half, which the same run exposed

**Derived forcedness is a LOWER BOUND.** `matching`/feasible/min reads exactly 0.0, the template route
calls it underivable — and matchings *are* subset-closed by a one-line argument (a subset of a matching is
a matching), with no finite template involved. **The old hand list had that entry and it was true.**

So the fix is not derive-*instead-of*-assert. It is **derive ∪ assert-with-its-argument**. Three asserted
entries now ship carrying the proof sketch that justifies them (`matching` and `three-dimensional-matching`
under intersection, `dominating-set` under union). The rule the survey actually earned:

> **No entry without a reason — derived in code, or written as an argument. What is banned is the
> unjustified entry, not the human one.**

### Residual, banked rather than adjudicated

Four exact-zero readings remain neither derived-forced nor asserted: `matching`/feasible/majority,
`max-flow`/feasible/minority, `max-flow`/optimal/minority, `three-dimensional-matching`/feasible/majority.
Each looks adjudicable by a short argument — flow conservation is a parity condition, for instance, and XOR
preserves parity. **They are not adjudicated here.** Asserting them would be doing the analysis a survey is
not entitled to do, and the point of the flag hygiene was to make a residual meaningful, not to keep
shrinking it until it vanished.

## Q2 — some regions are *anti*-blendable relative to random sets of their own size

30 of 114 readings have **positive** excess: the measured region violates *more* than a uniform random
subset of identical size in an identical space. The largest are structural rather than scattered —
spanning trees under union and intersection (+0.11 both), minimum-weight partitions (+0.12), dominating
sets under intersection (+0.18).

The shape is legible: a spanning tree is defined by a *global* constraint (connected and acyclic) that both
union and intersection destroy immediately, whereas a random set of the same size has no such structure to
break. **Being highly structured can make a region less blend-stable than being unstructured.**

If that survives a proper design, "distance from randomness" is **signed**, and the two-pole picture would
need a third position — not *blends better than random* versus *indistinguishable from random*, but a
region whose structure is actively hostile to blending. Banked, not claimed; n is small and no prediction
was made.

## Q3 — the probe reads rows closure anatomy cannot, and this is the first demonstration

`dominating-set`, `exact-cover-x3c` and `three-dimensional-matching` are **excluded from Marrow's closure
columns** — their constraint scopes are unbounded-arity, so no fixed finite template exists to take
polymorphisms of. The probe does not care: it enumerates solutions directly and read all three.

That is the geometry note's original argument, now demonstrated on three rows rather than asserted: an
instrument that measures the region reaches a population the instrument that derives from the template
cannot. **Whether those readings mean anything is a separate question and is not answered here.**

## Q4 — optimal regions are systematically tiny, and 28 readings are INSUFFICIENT-r

28 of 114 readings sit below the r ≥ 10 floor, nearly all of them `optimal` regions —
`min-spanning-tree` optimal at r ≈ 2.7, `reachability-stcon` optimal at r ≈ 3.5. This is round 2's
entanglement finding appearing again from the other side: **minimality means few members**, and no ensemble
tuning changes that.

The question: is there a region definition between *feasible* and *optimal* — near-optimal within a
declared slack — that keeps optimisation semantics while carrying enough members to measure? That is a
design question about what an optimisation row's region *should* be, not a statistical one.

## Q5 — the descriptive table does not repeat round 2's pattern, which is itself worth noting

Mean excess by region kind × decision, forced and INSUFFICIENT readings excluded:

| region | easy | hard |
|---|---:|---:|
| solutions | −0.3555 (n=12) | −0.1834 (n=16) |
| feasible | −0.1795 (n=15) | −0.3658 (n=17) |
| optimal | −0.1402 (n=8) | −0.1167 (n=10) |

The `solutions` row runs one way and the `feasible` row runs the other, with `optimal` nearly flat. **No
direction is claimed** — these are means over unmatched readings with no prediction attached, exactly the
comparison a survey is not entitled to score. It is banked because a design that intends to score it should
know in advance that the sign is not stable across region kinds, and should say which region kind it means
before looking.

---

**None of the above is a result.** Each is a question with an artifact behind it, waiting for a design that
states its prediction first.

---

# Appended 2026-07-26 — from the v3 widened + ramped survey

## Q6 — the puzzle regime is unmeasurable, and that is a property of the object

`sudoku`'s ramp runs on **constraint removal**. At 12 clues the region collapses below blendability and the
step records `GAP-no-region`; at 6 clues r = 3 and every flavour reads exactly 1.0 against a control of
exactly 1.0 — **excess 0.0000, and both sides saturated**. Measurable readings begin only at 2 clues
(r = 28) and the blank board (r = 288).

The bankable observation is about the instrument, not the object: **a region small enough to be a puzzle is
too small to have measurable geometry.** Whether that is a limitation of this probe or a fact about
puzzle-shaped regions is not answered here and is not guessed at.

*Pre-emptive note, recorded per directive: the moderate-violation expectation from the colouring analysis
is a **prior, not a prediction**. The readings are what they are.*

## Q7 — 160 of 528 readings are INSUFFICIENT-r, and they are not randomly placed

They concentrate at the hard end of optimal-region ramps. This is round 2's entanglement finding appearing
a third time, now with a trajectory shape rather than a single cross-section: **as difficulty rises the
optimal set shrinks, and the statistic runs out of region before the ramp runs out of steps.**

The question for a later design: is there a region definition between *feasible* and *optimal* — near-
optimal within a declared slack — that preserves optimisation semantics while surviving the hard end of a
ramp? Not a statistical question; a question about what an optimisation row's region *should be*.

## Q8 — 39 unforced exact-zeros now, up from 4

The v2 column had 4 after flag correction. The widened column has **39**, because the new rows are almost
all Marrow-excluded and their forcedness is therefore `null` — underivable, not false.

**This is the zero-hunt's input and is deliberately not adjudicated here.** Recorded so the count's growth
is visible and attributable: it grew because coverage grew into territory where the derivation cannot see,
not because the instrument got noisier.

---

*Entries below are banked from the zero-hunt and the trajectory report (2026-07-26). Same posture:
descriptive, unscored, deliberately not answered.*

## Q9 — three closure arguments cover 29 of 43 unforced zeros, and none of them needs a template

The zero-hunt's HIDDEN-CLOSURE verdicts rest on exactly three structural facts —
pairwise-exclusion ⟹ majority-closed, upward-closed ⟹ max-closed, downward-closed ⟹ min-closed — plus
parity ⟹ minority-closed on one row. All four are one-line arguments about a region's *construction*, and
**none requires a finite bounded-arity template.**

The template route was built because polymorphisms of Γ transport to every instance. But these families
have no finite Γ and are closed anyway. The bankable question is whether the derivation's reach can be
*extended by kind rather than by row*: could a region carry a declared monotonicity/exclusion/parity
property, from which forced flavours are derived the way template flags derive them now?

That would convert 29 adjudicated flags into derived ones. It would also introduce a new place for a
hand-written property to hide, which is the failure the template derivation was built to end. **Not
resolved here** — it is a design question about whether the cure reintroduces the disease.

## Q10 — `sat-2 · solutions · min` reads exactly 0.0 at r = 22 and nothing explains it

2-SAT is bijunctive, so *majority* is forced and the join flags it correctly. **`min` is not forced**: a
general 2-CNF is not Horn. The reading has 354 distinct subsets, clears the pre-declared floor, and
survived the zero-hunt as one of only two GENUINE-READINGs.

Two candidate explanations, neither tested: the sampled formulas drew Horn-like by chance at this
clause/variable ratio, or min-closure on 2-CNF solution sets is more common at small *n* than the general
non-implication suggests. **A single seeded re-draw would separate these** and is deliberately not run
here — the survey does not score, and an unscored re-draw chasing a specific reading is exactly the
posture violation the banked-questions file exists to prevent.

## Q11 — `graph-3-coloring · solutions · maltsev3` swings 0.4991 against a control SD of 0.0020

The largest excursion-to-control-SD ratio in the trajectory table by a wide margin (~245×), and
**NON-MONOTONE** — it does not simply rise or fall along the ramp.

`maltsev3` is the |D|=3 affine flavour, and 3-colouring's solution sets are not affine, so nothing forces
this to any value. What makes it bankable is the *shape*: a non-monotone swing this large on a flavour the
row is not closed under, while the same row's `max` and `min` trajectories are both **FLAT** (0.0299 and
0.0541 excursions).

Whether that is the ramp parameter interacting with 3-colouring's phase behaviour, or an artefact of how
`maltsev3` behaves on regions of rapidly changing size, is not diagnosed. It is the most eye-catching
single shape in the report and is recorded as such, without a story attached.

---

*Banked from Terrain v1 (2026-07-26), after the seal scored.*

## Q12 — nine readings have no fair control anyone currently knows how to build

Terrain's verdict covers 18 of 27 scored readings. The other 9 froze at tier 1.5: at high density a
distinctness-preserving swap chain cannot move (knapsack's region is 10,316 of 16,384 vectors and accepts
zero swaps). **Those 9 carry a mean tier-1 excess of +0.1222 against +0.0430 for the testable ones** — the
part of the anomaly that looks largest is the part with no fair null.

Neither tier 2 (definitionally unavailable for feasible regions) nor tier 1.5 (frozen) reaches them. The
open question is whether a cardinality-and-marginal-matched control exists for dense regions at all —
conditional Poisson sampling and Ising-model fits are candidates, neither grounded here.

**This is a question about the instrument, not the objects**, and it is the honest residue of a seal that
otherwise resolved cleanly.

## Q13 — the domain-general tier 1, with its known-answer requirement

A |D| > 2 matched-marginal control, banked rather than built mid-seal. Ruled out of Terrain because the 5
`graph-3-coloring` readings top out at +0.0260 against a +0.0624 MDE — power-dead regardless of control.

**Requirement written into the bank entry:** on binary rows the general variant must **reproduce tier 1
exactly**. A generalisation that cannot recover its own special case is a new instrument, not a wider one.

## Q14 — `optimization` blends BETTER than a matched control, and that was not the direction bet

`optimization`'s sealed primary is **−0.0754, CI [−0.0872, −0.0636]**, the only family to survive
Holm–Bonferroni — in the **negative** direction. Against a control matched on size, coordinate marginals and
member cardinality, those regions violate *less* than the null.

The seal bet on positive excess and this is its opposite, which is why it is reported rather than
interpreted. Whether it is the two-pole picture's "easy rows blend better than featureless sets" showing up
under a fairer control than the survey ever had is exactly the question a later design would pose.

---

## Q12 — CLOSED, 2026-07-26

The nine readings with no fair control now have one. N2's conditional-Poisson sampler qualified against
criteria pinned before any number was computed (18/18 agreement with tier 1.5 on shared ground, mean
|difference| 0.0228 against a 0.05 ceiling, zero degenerate controls), and was deployed once.

Those nine carried a mean tier-1 excess of **+0.1222** and read **−0.0364, CI [−0.0603, −0.0125]** under
the qualified control — a within-reading shift of −0.1586, statistically indistinguishable from the
−0.1297 Terrain measured on the sparse half.

**The question is answered: a cardinality-and-marginal-matched control does exist for dense regions, and
the untested remainder behaves like the tested part.** Terrain's verdict does not relabel; the retirement
is stated as a two-artifact conclusion in both artifacts.

---

## Q10 — CLOSED, 2026-07-26

**PREVALENCE**, and size-driven. At the sealed ratio, Horn formulas occur at 0.85 % (prior: 0.42 %) while
min-closed solution sets occur at **51.7 %**, of which **120 of 122 are not Horn**. Conditioned on size:
**64.5 % of solution sets with r < 25 are min-closed**, falling to 19.7 % at 25 ≤ r < 100 and 0 % above.

The original reading sits at r = 22. It reads 0.0 because that is the ordinary outcome at that size.

**A gap in the zero-hunt's vocabulary, recorded rather than patched:** `THIN-SATURATION` asks whether a
nonzero rate was *observable*. Here 231 distinct pairs were available and a nonzero rate was perfectly
observable — it simply did not occur. **A reading can clear every thinness floor and still be
unremarkable.** Whether that deserves its own verdict term is a design question, not answered here.

---

## STANDING CAUTION — closure prevalence is size-driven

**Measured, not conjectured (N3, `prereg_v21`):** 64.5 % of random 2-CNF solution sets with r < 25 are
min-closed, falling to 19.7 % at 25 ≤ r < 100 and 0 % at r ≥ 100. The same shape appears in the
independent-set base rate (24.5 % at r ≈ 10).

**Small solution sets are often accidentally closed. Closure at small r is the ordinary condition, not a
structural signal.**

This is a confounder with teeth. **Any future claim about closure rates must condition on region size, or
it is reading the base rate and calling it structure** — including anything the almost-closed-middle
question becomes, and any Marrow-adjacent prevalence statement.

---

## Q15 — the sign flips with aggregation level (N6-R Tier A)

The sealed statistic — reading-level partial Spearman of log-inflation against fair-null excess,
controlling for measured rate — came in at **+0.0023**, inside its permutation null. Aggregated to the
**class** level the same relationship reads **+0.1685 against a null of [−0.0325, +0.0349]**, decisively
outside it, and **opposite** the sealed negative sign.

**This is banked, never narrated as support.** It sits at a different aggregation level than the sealed
statistic and in the opposite direction to the bet, which makes it the Simpson-flavoured species:
*sign changes with aggregation* is a named phenomenon and it has three candidate explanations that this
study cannot separate.

1. **Clustering artifact.** Flavours inside one class share a region, so class-level means average away
   reading-level noise in a way that can manufacture an association from shared structure rather than from
   the relationship being measured.
2. **Size-weighted composition.** Classes contribute unequal numbers of readings, and |R| drives both
   inflation's ceiling (|hull| ≤ ambient) and the rate's resolution (C(r,m)). A class-level mean is a
   differently-weighted object, and the weighting is correlated with the predictor.
3. **A real class-level relationship** that reading-level noise buries — the interesting one, and the only
   one that would matter.

**Distinguishing them is a future sealed design's job, not a findings paragraph's.** A study that wanted
this would declare the aggregation level in advance, stratify on |R| explicitly, and separate
within-class from between-class variance before looking.
