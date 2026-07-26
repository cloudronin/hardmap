# The post-Terrain queue — review, and the two items that needed no ruling

**Status: N2 and N4 RUN (instruments, no bets). N1 and N3 return for ruling. N5 correctly gated.**
**Date:** 2026-07-26 · **Queue note reviewed:** `next-questions-queue-note.md`

---

## Part 1 — the review, and it blocks N1

### N1's sealed direction is not losable as written

N1 bets that under tier-1.5 controls, structured regions blend **better** than the null — sealed direction
**negative** — on a population of *all* survey readings with usable tier-1.5 controls.

That population, built to N1's own stated exclusions (forced, saturated, INSUFFICIENT, non-binary, dense),
is **196 readings**. Of those:

| | n | mean tier-0 excess |
|---|---:|---:|
| `feasible` | 67 (66 negative) | −0.2864 |
| `optimal` | 40 (39 negative) | −0.2093 |
| `solutions` | 89 (87 negative) | −0.2635 |
| **total** | **196 — 192 negative (98.0 %)** | **−0.2603** |

**98 % of the population is already negative before any fairer control is applied**, and Terrain measured
the tier-1→tier-1.5 shift as a *further* −0.1297. For N1 to lose, tier 1.5 would have to move the mean by
more than **+0.26** — roughly twice Terrain's measured magnitude, in the opposite direction.

This program already has the language for it: *a null the bet could not win is the mirror image of a null
the bet could not lose.* N1 as written is the second kind. It would return a confident confirmation that
was visible in disclosed data before the seal was drafted.

**What is actually uncertain**, and would make N1 a real test — any of:

1. **A magnitude threshold**, not a sign. "More negative than −0.10 under tier 1.5" is losable; "negative"
   is not.
2. **The easy–hard contrast within region kind** — genuinely unstable (see below), and it is the actual
   two-pole claim rather than a proxy for it.
3. **Whether the negative excess survives *at all* on the already-negative majority.** Terrain's −0.1297
   delta was measured on readings *selected for positive tier-0 excess*. Applying it to the negative
   majority is extrapolation across a selection boundary — regression toward the mean would push those
   readings **up**, not down. That direction is untested and is the one genuinely open question here.

**N1 does not run until this is ruled.**

### Q5 does not say what N1 cites it as saying

N1's mandatory region-kind stratification is justified by *"Q5's banked warning: the sign is not stable
across region kinds."*

All six of Q5's cells are **negative**. What varies is the **easy–hard ordering** — `solutions` has P more
negative than NPC, `feasible` has NPC more negative than P. Recomputed on N1's own population:

| region | NPC | P |
|---|---:|---:|
| `feasible` | −0.2895 | −0.2702 |
| `optimal` | −0.2105 | −0.2028 |
| `solutions` | −0.2021 | −0.3137 |

The sign is stable; the *contrast* is not. Q5's own sentence is loose and N1 inherited the looseness. The
stratification requirement survives — for the contrast, which is what actually flips — but its stated
reason should be corrected before it is sealed, because a seal that cites its warrant incorrectly invites
the next reader to check nothing.

### The rest of the queue reviews clean

Terrain's `optimization` at −0.0754 as the sole Holm survivor ✓ · the 9 frozen readings at ~3× the tier-1
excess ✓ (measured +0.1222 against +0.0430) · `sat-2 · solutions · min` at r = 22, unforced ✓ · 29
constructively-adjudicated closure flags ✓ · bank references Q1–Q14 ✓ · N5's gating argument is correct and
N3/N4's independence is correct.

---

## Part 2 — N4, property-derived forcedness (hygiene, no bet)

**Artifact:** `n4_property_forcedness.json` · **All 15 declarations verified. 0 dropped. 0 contradictions.
0 derived flags disagreeing with observation.**

The zero-hunt's 29 HIDDEN-CLOSURE adjudications lived in prose. They are now a **standing schema**: a region
declares a structural property, and its forced flavours derive from the property mechanically — in **both**
directions, since the join now has two.

| property | forces | direction |
|---|---|---|
| `upward_closed` | `max` | closed (violation 0) |
| `downward_closed` | `min` | closed |
| `pairwise_exclusion` | `majority` | closed |
| `parity` | `minority` | closed |
| `fixed_cardinality` | `min`, `max` | **saturated** (violation 1) |
| `exact_equality` | `min`, `max` | **saturated** |

**The disease-guard is what lets this ship.** A declared property is a hand-written entry wearing
derivation's clothes unless it is mechanically verified — so every declaration is brute-force checked on
freshly built regions, and **an unverified declaration is dropped, not downgraded**. `upward_closed` and
`downward_closed` are checked exhaustively (every single-bit raise/clear); `pairwise_exclusion` derives the
conflict set from the region and then confirms it *characterises* membership, so a region with any
non-pairwise constraint fails.

Contradictory implications on one flavour are a **hard error**, not a precedence rule: if a region were
declared both upward-closed and fixed-cardinality, one declaration is wrong and quietly preferring one
would hide it. None occurred.

Two declarations initially dropped for a reason that was mine, not theirs — `dominating-set` isn't in the
v2 fleet and `knapsack(0.45)` builds 5,959 members, outside the verification window. Corrected at the
builder; the properties themselves verified on the first attempt.

---

## Part 3 — N2, a fair control for dense regions (instrument, no bet)

**Artifact:** `n2_dense_control_qualification.json` · **QUALIFIED, then deployed.**

### The candidate

Conditional-Poisson-style sampling. Tier 1.5 *perturbs* the region, which is exactly what freezes on dense
input. This **constructs** a fresh control matching the same things: member cardinality taken exactly from
the region's multiset, coordinate marginals fitted by iterative proportional adjustment, distinctness by
rejection. Density cannot freeze it, because nothing has to move.

### Qualification — the criterion was pinned before any number was computed

A dense-region control that cannot reproduce the sparse answers is **a new instrument, not a wider one**.
So it had to agree with tier 1.5 on the 18 readings tier 1.5 already served:

| test | required | achieved |
|---|---|---|
| per reading, \|Δexcess\| ≤ 2·max(sd) | — | **18 / 18** |
| fraction agreeing | ≥ 80 % | **100 %** |
| mean \|difference\| | ≤ 0.05 | **0.0228** |
| variance census (sd = 0 disqualifies) | 0 degenerate | **0** |

**QUALIFIED.**

### Deployment — and it closes Q12

Run on the 9 readings Terrain could not test:

| | mean | 95 % CI |
|---|---:|---|
| their **tier-1** excess (the untested anomaly) | **+0.1222** | — |
| their **CP** excess | **−0.0364** | **[−0.0603, −0.0125]** |
| within-reading Δ (CP − tier 1) | **−0.1586** | **[−0.2289, −0.0883]** |

The shift is **statistically indistinguishable from the −0.1297 (CI [−0.1699, −0.0895]) Terrain measured on
the sparse half.** The part of the anomaly that looked largest behaves exactly like the part that was
testable: matching cardinality absorbs it and carries it slightly negative.

`knapsack` is the sharpest case — tier-0 excess +0.4825, tier-1 +0.2224, **CP −0.0014**.

### What this does not do

**It does not rewrite Terrain's verdict.** Terrain scored once, and its verdict is scoped to 18 of 27
readings, which is what it says. This is a follow-on measurement with its own provenance and its own
instrument. Whether `CONTROL-MISMATCH@1.5` now extends to full coverage is **a ruling, not an inference this
artifact makes** — and the honest reason to require the ruling is that a qualified instrument arriving after
a verdict is exactly the situation where a program talks itself into upgrading a result it already likes.

---

## Returning for ruling

| item | status |
|---|---|
| **N1** | **blocked on redesign** — the sealed direction is not losable (§Part 1). Three candidate re-posings offered; the third is the genuinely open one. |
| **N3** | prereg to draft — unaffected by the above, smallest seal, one evening |
| **N5** | correctly gated; N2 has now discharged half the gate |
| **Terrain's coverage** | does the N2 deployment extend `CONTROL-MISMATCH@1.5` to 27 of 27? |
