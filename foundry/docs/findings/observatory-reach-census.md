# The observatory reach census — all 345 natural rows

**Status: CENSUS.** Classification and ramp declaration. No readings, no dials, no outcome artifact read.
**Date:** 2026-07-26 · **Artifact:** `observatory_reach_census.json`

---

## What this asks, and why it is not Marrow's question

Marrow's I0 asked *can a relational template be pinned?* and found 34 presentable rows. **This asks whether
the observatory can generate instances and compute dials** — a strictly different question, and the survey
already proved they diverge: `set-cover`, `knapsack` and `dominating-set` are all Marrow-excluded and were
fully surveyed anyway, because the probe enumerates solutions directly and does not care whether a finite
template exists.

## The counts

| reach class | n |
|---|---:|
| **BUILT** — generator exists in the fleet | **27** |
| REACH-subset — solutions are subsets of a ground set | 90 |
| REACH-assignment — solutions are variable assignments | 38 |
| REACH-permutation — solutions are orderings (ambient n!, thin) | 17 |
| OUT-proof-object — the object is a derivation, not a solution set | 52 |
| OUT-continuous | 16 |
| **UNTYPED** | **105** |

**172 of 345 reachable. All 172 ramped — zero point-captures**, because every reachable family has a
declared dial.

## BUILT is a measurement; everything else is a typing

The distinction matters and the artifact records it per row. **BUILT** is measured — the generator is
imported from the fleet or it is not. Every other class is a **typing**: a declared rule over family and
identity, with the rule that fired recorded. A typing is a claim about *the observatory's reach*, not about
the problem, **and it is falsified the moment someone builds a generator for a row typed unreachable.**

Marrow's spec warned that a regex over problem names is not a census. So rows no rule types are `UNTYPED`
and reported as a first-class number rather than absorbed into a nearby class.

## The 105 untyped are not one thing, and the difference decides where adjudication pays

Reading the untyped list rather than counting it:

**Rule-too-narrow — probably reachable.** `min-bisection`, `densest-k-subgraph`, `cluster-editing`,
`k-center`, `k-median`, `maximum-common-subgraph` are subset-selection problems whose names simply missed
the declared pattern. Most of the 53 untyped `graph` rows look like this. **Adjudicating these is cheap and
would move them into REACH-subset.**

**Genuinely regionless — and this is the census's substantive finding.** `primality`, `gcd`, `factoring`,
`determinant`, `permanent`, `matrix-multiplication`, `gaussian-elimination-pivoting` have **no solution set
to measure**. A unique answer is not a region; an evaluation problem has no members to blend.

> **The observatory needs a problem to have *many* solutions. That is not a limitation of the instrument —
> it is a fact about which problems have the kind of object this program measures.**

`lattice` rows (SVP, CVP, SIS, LWE) are a third case: solutions exist in quantity but live in an unbounded
integer ambient, so there is no finite region at a fixed encoding.

**Adjudicating the 105 is the next census motion.** It is not done here and is not guessed at.

## Ramped by default — the parameters declared here, at census

Every reachable row is captured along a ramp. The parameter is declared **per family, before any row is
captured**, so no row's dial is chosen after seeing its readings.

| family | ramp parameter | precedent |
|---|---|---|
| `sat-csp` | clause/variable ratio | sat-2, sat-3, horn-sat, xor-sat, nae-sat in v3 |
| `graph` | edge density | vertex-cover, independent-set, dominating-set, fvs, oct in v3 |
| `optimization` | constraint-to-ground-set ratio | set-cover, hitting-set in v3 |
| `number-theoretic` | capacity fraction or value range | knapsack, subset-sum in v3 |
| `string` | pattern/text length ratio | none yet — declared here, first use at build |
| `algebraic` | system density (equations per unknown) | xor-sat's ratio ramp is the nearest analogue |
| `matrix` | fill density | none yet |
| `lattice` | dimension | none yet — **flagged: a size knob is not a constraint-tightness knob** |
| `geometric` | point density | none yet; most geometric rows are unreachable regardless |
| `logic-proof` | — | the object is a derivation; the proof census reads these rows |

**One caution recorded rather than discovered later:** `lattice`'s declared parameter is *dimension*, which
is a **size** knob, not a **constraint-tightness** knob. Every other family's dial tightens constraints at
fixed size. If lattice rows are ever built, that difference has to be handled explicitly or their
trajectories are not comparable to the rest.

## What the fleet already reaches — the 27

`bipartiteness` · `clique` · `dominating-set` · `exact-cover-x3c` · `feedback-vertex-set` ·
`graph-3-coloring` · `hitting-set` · `horn-sat` · `independent-dominating-set` · `independent-set` ·
`knapsack` · `matching` · `max-cut` · `max-flow` · `min-spanning-tree` · `nae-sat` ·
`number-partitioning` · `odd-cycle-transversal` · `reachability-stcon` · `sat-2` · `sat-3` · `set-cover` ·
`sharp-monotone-2sat` · `subset-sum` · `three-dimensional-matching` · `vertex-cover` · `xor-sat`

**27 built of 172 reachable.** The build queue is 145 rows deep before adjudicating the untyped.

## Scope — and the regionless class is a theorem about that scope, not a gap in it

> **The observatory measures solution-set geometry. It therefore applies to search-shaped problems and not
> to evaluation-shaped ones.**

`factoring`, `primality`, `determinant`, `permanent`, `gcd`, `matrix-multiplication` are not rows the
instrument failed to reach. They are rows with **no region to reach**: a unique answer is not a set, and an
evaluation problem has no members to blend. That is a fact about which problems have the kind of object
hardness-geometry attaches to.

**And the program already met this fact one scale down.** Q6 recorded that Shidoku's puzzle regime was
unmeasurable because a well-posed puzzle has r = 1 — uniqueness kills blending. That is the same
phenomenon: **uniqueness destroys the region, per instance in Q6 and per row here.** One fact, two scales,
and they are hereby recorded as one.

**And the unification runs one scale further out.** `factoring` lands in the regionless class because a
factorisation is *unique up to order* — r = 1, and uniqueness kills blending. So:

> **Uniqueness destroys the region — per instance in Sudoku's puzzle regime (Q6), per row in factoring,
> per field in cryptography.**

That last step has explanatory content rather than being a boundary note. **The observatory cannot film
cryptography because cryptography is built on problems whose answer-objects have no crowd to photograph.**
One-wayness lives precisely where the solution object degenerates to a point — the object of interest is a
*value*, and a value has no geometry. Those rows were never candidates for a geometry this instrument
could see, and now the reason is stated rather than observed.

## Census discipline

Census minimalism governs: this reads the atlas and the fleet and no outcome artifact. It declares
classifications and ramp parameters. It measures nothing about geometry and makes no claim about any row's
behaviour.

---

# Addendum — the 105 adjudicated

**Artifact:** `observatory_untyped_adjudication.json` · **Completeness asserted:** every untyped row is
adjudicated or the script halts. Adjudicating 105 means all 105.

| class | n |
|---|---:|
| REACH-subset | 37 |
| REACH-permutation | 22 |
| REACH-assignment | 18 |
| REGIONLESS-unique-answer | 9 |
| REGIONLESS-language-membership | 6 |
| OUT-continuous | 6 |
| no-natural-dial-at-fixed-encoding *(lattice)* | 4 |
| **STILL-UNTYPED** | **3** |

**Reachable: 172 → 249 of 345.** The build queue is **222 rows** beyond the 27 already built.

## Two refinements the reading produced, each moving a subclass

**A counting problem's region is the set being counted.** `sharp-acyclic-orientations` counts acyclic
orientations, and that *set* is exactly a region this instrument enumerates and blends. **The `#` changes
what the charge asks, not whether the object has a region.** Five graph rows plus `sharp-contingency-tables`
move from apparently-regionless to reachable on this alone.

**The regionless class is narrower than the first pass suggested, and sharper for it.** It is exactly the
rows whose answer is a single value with no set behind it — `primality` (a bit), `gcd` (one integer),
`discrete-log` (one exponent), `matrix-multiplication` (one matrix). **`factoring` belongs there**: the
factorisation is unique up to order, so its region has one member — **Q6's fact at row scale.**

A second regionless kind emerged that the first pass had no name for: **language membership**.
`dfa-intersection-emptiness`, `nfa-universality`, `regex-squaring-inequivalence`, `planarity` ask a yes/no
about an *object*, not for members of a set. No region, and for a different reason than uniqueness.

## The lattice ruling

Dimension was declared as lattice's ramp at census — **and dimension is the size axis.** Finite-size
scaling needs ramp and size as independent knobs, so a family whose only dial is size has **no ramp at
all**, not a strange one. A size axis must not impersonate a hardening axis.

Adjudicated: **at fixed dimension these rows do have candidate constraint dials** — the approximation
factor γ for SVP/CVP (the region `{v : |v| ≤ γ·λ₁}` widens as γ rises), and the noise-rate/modulus ratio
for LWE and SIS. Those are genuine tightness knobs.

**But the ambient is unbounded integer vectors, so no finite region exists until a coefficient bound is
pinned — an encoding choice this census has not made.** Typed `no-natural-dial-at-fixed-encoding`, with the
dial candidate *named* so a future build can pin it, and **dimension barred as the ramp regardless.**

## Three kept open

`network-reliability`, `permanent`, `tutte-polynomial` are recorded `STILL-UNTYPED`. `permanent` is the
interesting one — for 0/1 matrices it counts perfect matchings, whose set *is* a region, but the row as
carried is an evaluation. That ambiguity is left standing rather than resolved by preference.
