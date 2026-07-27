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

## Scope

Census minimalism governs: this reads the atlas and the fleet and no outcome artifact. It declares
classifications and ramp parameters. It measures nothing about geometry and makes no claim about any row's
behaviour.
