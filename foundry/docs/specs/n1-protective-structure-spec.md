# N1 — the protective-structure seal, re-posed

**Status: DRAFT AWAITING SEAL. Design ruled 2026-07-26; prereg number reserved `prereg_v20`, minted at seal.**
**Supersedes:** the queue note's N1 as written, which was ruled not losable.
**Inherits:** Terrain (`prereg_v19`, CONTROL-MISMATCH@1.5) · N2 (qualified CP control) · N4 (property schema)

---

## 0. Why the original N1 could not lose, and what replaced it

The queue note's N1 bet that fair-null excess is **negative**. Its population is 98.0 % negative *at tier
0*, before any fairer control, mean −0.2603 — and Terrain measured the tier-1→tier-1.5 shift as further
negative. The bet was decided by disclosed data.

**Ruled: option 3 becomes the primary.** The genuinely open question is the one the review isolated:

> Terrain's absorption was measured on readings **selected for positive excess**. Applying it to the
> negative majority crosses a selection boundary. The same cardinality mismatch that manufactured
> *positive* excess on 34 readings could be manufacturing *negative* excess everywhere else.

That is losable, and the arithmetic below shows it is losable by a margin thinner than the effect already
measured twice.

**Option 1 (a magnitude threshold) is dropped** — arbitrary where option 3 is principled.

---

## 1. The sealed primary

**On the scored population, mean FAIR-NULL excess remains NEGATIVE with a 95 % CI clear of zero.**

Fair null per coverage: **tier 1.5** where its mixing floor `max(50, r/4)` is cleared, **CP** (N2's
qualified conditional-Poisson control) otherwise. Both were qualified against each other at 18/18
agreement, mean |difference| 0.0228.

### Why this is losable — the arithmetic, stated before scoring

| | |
|---|---:|
| disclosed tier-0 mean, at the primary unit | **−0.2053** |
| its 95 % CI | [−0.2416, −0.1690] |
| the primary FAILS if fair-null absorption reaches | **+0.1690** |
| absorption measured by Terrain (sparse, positive-excess readings) | **+0.1297** |
| absorption measured by N2 (dense, positive-excess readings) | **+0.1586** |

**The larger of the two measured absorptions is within 0.011 of flipping this bet.** The seal is not a
formality; it sits on a knife edge, and which side it lands on turns on whether absorption behaves the same
on negative-excess readings as on the positive-excess ones where it was measured. That is the question.

## 2. The named secondary — the easy–hard contrast

Same family, declared now: **within each declared region kind, the easy–hard contrast in fair-null excess.**
This is the actual two-pole claim rather than a proxy for it.

**Q5's warrant, corrected.** Q5 was cited as showing "the sign is not stable across region kinds." All six
of its cells are negative. What is unstable is the **contrast**:

| region | NPC | P | contrast direction |
|---|---:|---:|---|
| `feasible` | −0.2895 | −0.2702 | hard more negative |
| `optimal` | −0.2105 | −0.2028 | hard more negative |
| `solutions` | −0.2021 | −0.3137 | **easy more negative** |

`solutions` runs opposite to the other two. **Region kinds are declared before looking**, and the
stratification stands — on the corrected warrant.

## 3. Population and coverage

| | n |
|---|---:|
| eligible: unforced, unsaturated, admissible, binary | 305 |
| − v2 readings with no per-reading seed (`INSUFFICIENT-replay`) | −56 |
| **scored population** | **249** |
| — sparse, tier-1.5 route | 143 |
| — dense, CP route | 106 |

**N2's qualification is load-bearing.** Without it the dense 106 are unreachable and the population is 143.
This is the first study whose scope depends on an instrument qualified in a previous one, and it is stated
rather than absorbed.

Composition: `feasible` 145 · `solutions` 76 · `optimal` 28 · four families · all four flavours.

## 4. Power, pre-declared

From the **disclosed tier-0 spread**, never the sealed fair-null statistic.

| unit | n | tier-0 SD | MDE (α .05, power .80) |
|---|---:|---:|---:|
| reading | 249 | 0.2634 | +0.0471 |
| **(row, region, step)** — primary | **86** | **0.1718** | **+0.0531** |
| row-clustered — robustness | 16 | 0.1157 | +0.0918 |

**INSUFFICIENT is not evidence of absence.**

## 5. Multiple-comparisons ledger — continues

Terrain's family closed at 5. **This seal opens its own family and names its predecessor.**

| | |
|---|---:|
| primary (pooled) | 1 |
| primary per-family | 4 |
| secondary: easy–hard contrast per declared region kind | 3 |
| **family size** | **8** |

Holm–Bonferroni at FWER 0.05; smallest threshold 0.05/8 = 0.00625. The eventual flagship (N5) closes over
both this family and Terrain's.

## 6. Verdicts

**PROTECTIVE-STRUCTURE-REAL** (primary holds — negative survives the fair null) ·
**ABSORBED** (the fair null removes the negativity too; the tier-0 negative was the same artifact as the
tier-0 positive, in the other direction) · **MIXED-BY-REGION-KIND** · **INSUFFICIENT**.

`ABSORBED` is new and is the point of re-posing: it names the outcome where the anomaly and its mirror turn
out to be one control defect.

## 7. Box, stated before building

**3–6 h compute.** Terrain took 75 min for 27 readings across 16 ramp steps; N1 covers 249 readings across
**72** steps. Naive scaling gives 5.6 h. CP is cheaper than a frozen 30-sweep chain, but tier-1 rejection
sampling on the 20 readings with r > 3000 (`knapsack`, `set-cover`) was Terrain's other bottleneck and is
unchanged. **This is the largest compute item the program has run and it is stated before sealing, not
discovered during.**

## 8. Not authorised

No new rows, no new readings, no re-measurement of any frozen rate. Terrain's verdict and its 18-of-27
scope are permanent and are not revisited by this study.
