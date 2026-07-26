# Terrain v1 — the anti-blendability seal, scored

**Status: SCORED ONCE against the frozen column. `prereg_v19`, sealed 2026-07-26 before this ran.**
**Artifact:** `terrain_v1_results.json` (sha256 `092c7e88`) · **Spec:** `terrain-v1-anti-blendability-spec.md`

---

## The verdict

# CONTROL-MISMATCH@1.5

**The primary bet FAILED, in the direction it was made.**

| sealed primary (tier 1.5 where it clears its floor, else tier 1) | mean | 95 % CI | n |
|---|---:|---|---:|
| **pooled** | **−0.0142** | **[−0.0613, +0.0329]** | 26 |
| `graph` | +0.0063 | [−0.0732, +0.0859] | 13 |
| `number-theoretic` | +0.1123 | [+0.0003, +0.2244] | 3 |
| `optimization` | **−0.0754** | **[−0.0872, −0.0636]** | 9 |
| `sat-csp` | — | INSUFFICIENT (n < 2) | 1 |

The bet was *positive excess with a CI clear of zero*. The pooled result is **negative and its interval
contains zero**.

**Holm–Bonferroni, family of 5, FWER 0.05:** only `optimization` rejects (p < 0.00001 against a 0.01000
threshold) — **and it rejects in the NEGATIVE direction.** Those regions blend *better* than a matched
control. Reported as measured, against the sealed direction.

## The mechanism is named, and it is not the one the ladder was expected to catch

**The excess does not die at tier 1.** Matched-marginal controls leave it intact — pooled tier-1 excess
**+0.0706, CI [+0.0347, +0.1066]**, comfortably clear of zero.

**It dies at tier 1.5**, and the within-reading comparison is decisive:

| on the 17 units measurable at both tiers | mean | 95 % CI |
|---|---:|---|
| tier-1 excess | +0.0433 | [+0.0081, +0.0784] |
| tier-1.5 excess | −0.0864 | [−0.1050, −0.0678] |
| **within-reading Δ (1.5 − 1)** | **−0.1297** | **[−0.1699, −0.0895]** |

The single step from tier 1 to tier 1.5 **absorbs the entire anomaly and overshoots into negative
territory.** That step adds exactly one thing: the control preserves **every member's cardinality**, not
just the per-coordinate marginals.

So the unfair feature of the original control is identified precisely. It is not that the null ignored
correlation in general. It is that **a uniform random subset has Binomial(n, ½) cardinality while these
regions do not** — and matched marginals fix the *mean* cardinality while leaving its *distribution*
wrong. Tier 1.5 fixes the distribution, and the anomaly disappears.

**H-artifact is supported. H-real is not supported on the readings this design could test.**
`ANTI-BLENDABILITY-UNREFUTED` goes unused — the verdict required surviving tier 1.5, and nothing did.

### The motivating intuition was right about the feature and wrong about the example

H-artifact was argued from spanning trees, *"correlated by construction."* The I-phase showed
`min-spanning-tree` contributes nothing to the anomaly — both its readings are theorem-saturated. But the
mechanism the scoring found **is** cardinality structure, and a spanning tree is the paradigm
fixed-cardinality object. The intuition pointed at the right property through a row that turned out to
carry no evidence for it.

## The limitation, and it is worse in kind than the one the seal declared

The seal declared a **power** limitation: underpowered to distinguish partial from total absorption. What
actually bit is a **coverage** limitation, and no amount of *n* fixes it.

| | n | mean tier-1 excess |
|---|---:|---:|
| tier-1.5 **usable** | 18 | **+0.0430** |
| tier-1.5 **frozen** (below the mixing floor) | 9 | **+0.1222** |

**The readings tier 1.5 cannot test are exactly the dense ones, and they carry nearly three times the
tier-1 excess.** At high density a distinctness-preserving swap chain cannot move at all — `knapsack`'s
region is 10,316 of 16,384 vectors, and its chain accepts nothing.

So the verdict covers **18 of 27 readings**. The other 9 are `INSUFFICIENT-degenerate` at tier 1.5 and
**the verdict does not extend to them.** The part of the anomaly that looked largest is the part that
remains untested.

## What the seal disarmed before it ran

Two things were removed by the I-phase, and both would have moved the result:

- **58 of 92 readings were theorem-saturated** — violation forced to 1.0 by construction, carrying 45.5 %
  of the total positive excess. Had they stayed, the anomaly would have looked far larger and would have
  been an artifact of the join's blindness rather than of the control.
- **A sibling-instance tier-2 control** would have made the H-real bar reachable everywhere and was
  barred: the measured rate is already a mean over instances of that generator, so such a control's excess
  is zero by construction.

The first was inflating the anomaly; the second would have rigged the test against it. Disarming both
before scoring is why the failure recorded above is informative rather than merely negative.

## Counts

| | |
|---|---:|
| admissible positive-excess readings | 92 |
| − theorem-saturated (`forced_saturated`) | −58 |
| residual anomaly set | 34 |
| − `INSUFFICIENT-encoding` (non-binary; power-dead at +0.026 against a +0.062 MDE) | −5 |
| scored set | 29 |
| − `INSUFFICIENT-replay` (v2, no per-reading seed) | −2 |
| **readings in the ladder** | **27** |
| — of those, measurable at tier 1.5 | 18 |

Region replay was verified exact: every regenerated region reproduced its frozen rate to within 5 × 10⁻⁴,
and a mismatch would have dropped the reading rather than substituting a region. Two v2 readings had no
per-reading seed and dropped.

## What this does not say

It does not say anti-blendability is not real. It says **the excess that motivated the question is
explained by a control that failed to match cardinality**, on the 18 readings where a cardinality-matched
control could be built. Nine readings — the densest, with the largest excess — have no fair control that
this program currently knows how to construct, and that gap is definitional rather than budgetary.

The `min` skew (28 of 34 residual readings) is untouched by this seal and stays banked.
