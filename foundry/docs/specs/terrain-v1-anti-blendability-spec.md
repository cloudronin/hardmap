# Terrain v1 — the anti-blendability seal

**Status: SEALED as `prereg_v19`, 2026-07-26. All six open items ruled; scored once against the frozen column.**
**Date:** 2026-07-26 · **Prereg:** `eightfold/eightfold/results/prereg/prereg_v19.json`
**Rulings applied:** THEOREM-SATURATED screen approved with the instrument fix · single-arm design approved ·
tier 1.5 admitted with its `max(50, r/4)` mixing floor · the non-binary readings ship `INSUFFICIENT-encoding`
with the domain-general tier 1 banked · §0.2 confirmed (the seal proceeds on the anomaly as measured) ·
`ANTI-BLENDABILITY-UNREFUTED` approved, its definition naming what an upgrade would require.
**Supersedes:** nothing. The survey column keeps its readings and its exploratory status.
**I-phase artifact:** `terrain_i0_control_census.json` · **I-phase code:** `foundry/dev/terrain_i0_controls.py`

---

## 0. What the I-phase changed, before any text fixed

The directive ordered grounding first, and grounding moved five things. All five are stated here rather
than absorbed silently, because each changes what the seal can honestly bet. **§0.3 is the one that
matters most** — it removes 63 % of the anomaly before any control tier is argued about, and it found a
one-sided defect in a standing instrument.

### 0.1 The admissible positive-excess set is 92 readings

| slice | n |
|---|---:|
| readings carrying an excess | 640 |
| **positive excess (any)** | **179** |
| — of those, theorem-forced | 0 |
| — of those, INSUFFICIENT by a pre-declared floor | 87 |
| **admissible positive-excess — the anomaly set** | **92** |
| distinct (row, region, flavour) units within it | 39 |

This is the set *before* the screen §0.3 introduces. **It is not the set that gets scored** — §0.3 removes
58 of these as theorem-saturated, leaving 34. The table is kept because the 92 is what "positive excess"
means in the frozen column, and the seal should show what it discarded and why.

### 0.2 The stated concentration does not hold

The directive attributes the anomaly to *spanning trees and dominating sets*. Measured:

All 18 rows, complete — not a selection, since a truncated table here would let the tree rows look larger
by omission of what outranks them:

| row | n | | row | n |
|---|---:|---|---|---:|
| `knapsack` | 13 | | `dominating-set` | 4 |
| `subset-sum` | 12 | | `sudoku` | 4 |
| `set-cover` | 10 | | `number-partitioning` | 2 |
| `independent-dominating-set` | 8 | | **`min-spanning-tree`** | **2** |
| `feedback-vertex-set` | 7 | | `matching` | 2 |
| `odd-cycle-transversal` | 7 | | `reachability-stcon` | 2 |
| `hitting-set` | 7 | | `three-dimensional-matching` | 2 |
| `graph-3-coloring` | 5 | | `nae-sat` | 2 |
| | | | `independent-set` | 2 |
| | | | `max-flow` | 1 |

`min-spanning-tree` contributes **2 of 92**. The dominating-set pair contributes 12. The mass sits in
**knapsack, subset-sum and set-cover** — packing and covering rows, not tree rows.

This matters beyond bookkeeping: the H-artifact story was *"objects like spanning trees are correlated by
construction."* That intuition is about a **fixed-cardinality, highly structured support**. The rows
actually carrying the anomaly are mostly **threshold/covering families whose members vary in cardinality**,
so the mechanism H-artifact proposes may not be the mechanism present. **The hypothesis is not thereby
refuted** — it is un-anchored from the example that motivated it, and the ladder in §2 is what settles it.

After §0.3's screen the point sharpens: `min-spanning-tree` leaves the anomaly set **entirely**, because
both its readings are theorem-saturated. The tree rows are not weak evidence for the anomaly; they are
**not evidence at all**.

### 0.3 THE DECISIVE FINDING — the forcedness join is one-sided, and 58 of the 92 are forced

**58 of the 92 admissible positive-excess readings sit at `measured_rate` EXACTLY 1.0.** Not near it —
*at* it. Zero readings fall in [0.99, 1.0).

They are perfectly symmetric — **29 `min` and 29 `max`, and not one `majority` or `minority`** — and they
arrive in pairs on the same (row, region). That is the signature of a region whose defining constraint is
broken by **both** union and intersection:

| row · region | why every blend leaves, by construction |
|---|---|
| any `optimal` region | min of two optima is smaller, max is larger; neither is optimal |
| `subset-sum`, `number-partitioning` | membership is an **exact-sum equality**; both directions break it |
| `independent-dominating-set · feasible` | an intersection of an upward-closed property (dominating) and a downward-closed one (independent); union kills independence, intersection kills domination |
| `min-spanning-tree · feasible` | every member has exactly *n*−1 edges; neither blend preserves the count |
| `reachability-stcon · feasible` | a blend of two s–t paths is not a path |

**Their violation rate is a theorem, not a measurement.** Excess is then `1.0 − control_mean`, which is
positive for any control that is not itself saturated — so these readings are guaranteed positive excess
regardless of whether anti-blendability exists. **They carry 45.5 % of the anomaly set's total positive
excess.**

#### The instrument defect underneath

This program has netted the **theorem-forced-credit trap at four scales**, every time for forced *zero*.
The derived join excludes flavours a region is **closed under** — violation forced to 0. It has no
corresponding exclusion for flavours a region is forced to **leave** — violation forced to 1.

**The join is one-sided.** It was built to stop a theorem manufacturing a *null*, and the same theorem can
manufacture a *hit*. A discipline that only catches flattering errors is indistinguishable from pessimism,
and this is the same asymmetry wearing the other face.

**Required before scoring, and it is a fix to a standing instrument rather than to this study:** the
forcedness derivation gains a second direction — `forced_saturated` — derived from the region's
construction the same way `theorem_forced` is, and excluded from discovery statistics by the same schema.
Until it exists, the screen is applied here by the exact-1.0 test, which is a *sufficient* detector and not
a complete one: a region forced to leave on 99 % of blends would pass it.

#### What remains — and it is the directive's "~30", reached from the data

**Residual anomaly set: 34 readings.**

| row | n | excess range |
|---|---:|---|
| `graph-3-coloring` | 5 | +0.0006 .. +0.0260 |
| `feedback-vertex-set` | 5 | +0.1364 .. +0.2331 |
| `odd-cycle-transversal` | 5 | +0.0388 .. +0.2003 |
| `hitting-set` | 5 | +0.1295 .. +0.1575 |
| `dominating-set` | 4 | +0.1254 .. +0.3698 |
| `set-cover` | 4 | +0.0159 .. +0.3951 |
| `knapsack` | 3 | +0.1025 .. +0.4825 |
| `nae-sat` | 2 | +0.0257 .. +0.0316 |
| `max-flow` | 1 | +0.0087 |

Composition: **26 `feasible`, 7 `solutions`, 1 `optimal`** — and **28 of 34 are `min`**, 5 `max`, 1
`majority`. The flavour skew is stark and is **banked, not interpreted**: this seal tests whether the
excess survives fairer controls, not why intersection is special.

### 0.4 THE KILL FIRES — tier 2 is available for a minority

**On the 92-reading set, tier 2 is computable for 31 = 33.7 %. On the residual 34-reading set of §0.3 it
is computable for 1 = 2.9 %.** Per the directive's kill clause, the prereg comes back saying so and
re-scopes, never silently.

The second number is the operative one, and it is far worse than the first for a reason worth stating: the
forced-saturated readings removed in §0.3 were disproportionately `optimal`-region — which is precisely
where tier 2 *was* available. **Stripping the theorem-forced readings strips almost all of the tier-2
coverage with them.** The real anomaly lives in `feasible` regions, where tier 2 does not exist.

And the reason is **definitional, not computational** — no amount of compute fixes it:

| region kind | n | containing species | tier 2 |
|---|---:|---|---|
| `optimal` | **31** | the **feasible** family — strictly larger | **available** |
| `feasible` | 38 | the region *is* the species | **degenerate**: a species-drawn control at matched r is the region |
| `solutions` | 23 | only natural container is the ambient space | **collapses to tier 0** |

Confirmed empirically in the I-phase census across 24 (row, region, flavour) combinations: tier 2
computable on 8, all `optimal`; unavailable on all 12 `feasible` and all 4 `solutions`.

### 0.5 The escape from 0.4 is a rigged null, and is barred

There is an obvious way to make tier 2 available everywhere: draw the control from a **different instance
of the same generator**. The seal must refuse it, and the reason should be in the record.

The survey's `measured_rate` is **already a mean over several instances of that generator**. A
sibling-instance control therefore estimates *the same quantity as the measurement*, so its excess is
**zero by construction**. That is not a conservative null — it is one the bet could not win however real
the effect, which is the mirror image of a null the bet could not lose.

It is retained as a **calibration diagnostic** (it should read ≈ 0; a materially nonzero reading indicts
the pipeline) and is **excluded from every primary and secondary statistic by schema**.

---

## 1. The control ladder, as grounded

Each tier's computability *and its variance* were measured before this text fixed, per the
census-before-seal law. A control family that cannot vary is unusable, and one of them cannot.

| tier | definition | computable | varies |
|---|---|---|---|
| **0** | uniform random subset of the ambient space at matched *r* | 92/92 (already frozen in the column) | yes |
| **1** | **matched-marginal** — size *r*, per-coordinate inclusion frequencies matched, coordinates drawn independently | 29/34 binary; **5 need a domain-general variant** (`graph-3-coloring`, \|D\|=3 — `sudoku`'s 4 readings are all theorem-saturated and leave the set) | yes |
| **1.5** | **swap-randomised** — preserves every per-coordinate marginal **and** every member's cardinality **and** distinctness | **conditional — see 1.2** | conditional |
| **2** | **matched-object** — *r* random members of the region's own containing species | 31/92 on the pre-screen set; **1/34 on the scored set** | yes |

### 1.1 Why tier 1.5 exists — tier 1 has a flaw the ladder needs to cover

Tier 1 draws coordinates **independently**, so it does **not** preserve member cardinality. Measured in the
I-phase: `hitting-set · optimal` has cardinality SD **exactly 0** — every member the same size. Spanning
trees are the same shape (every spanning tree has *n*−1 edges). For such a region a tier-1 control is not a
fairer null but a **differently-shaped** one, and a "died at tier 1" verdict there would be uninterpretable.

Swap randomisation (Curveball-style) fixes it: verified in the I-phase to preserve **all** column marginals,
**all** member cardinalities, and — with a distinctness guard — **|set| = r** exactly, while varying across
draws.

### 1.2 And tier 1.5 has its own failure, found by measuring it

On dense regions the distinctness guard **freezes the chain**:

> `knapsack · feasible`, r = 6152 of 16384 (38 % density): **0 swaps accepted, 140 263 rejected.**
> The "control" was byte-identical to the region — excess 0 by construction.

Density across the anomaly set:

| r / \|ambient\| | readings |
|---|---:|
| < 2 % (mixes freely) | 51 |
| 2–10 % | 13 |
| 10–25 % | 3 |
| **≥ 25 % (freeze risk)** | **25** |

So tier 1.5 ships **with a declared mixing floor**: a control whose accepted-swap count falls below
`max(50, r/4)` is declared `INSUFFICIENT-degenerate` and the reading reports tier 1.5 as unavailable rather
than reporting a frozen control as a fair one. **This is the second control family the census caught before
the bet fixed, and it is exactly what census-before-seal is for.**

---

## 2. The sealed bet — single-armed, because the kill fired and the screen emptied the other arm

The directive's fallback is *"re-scope to tier 1 with the limitation stated."* **That fallback is what the
grounding lands on**, and this section says so plainly rather than dressing it up.

An earlier pass of this draft proposed a stronger stratified design — each stratum bet at the highest tier
its region kind admits, with `optimal` regions carrying a genuine tier-2 arm. **§0.3's screen emptied that
arm**: the theorem-saturated readings it removes are disproportionately `optimal`, leaving **33
non-optimal readings and 1 optimal one**. A two-armed design with one reading in the second arm is a
pretence, so the design is single-armed.

### The single arm — the residual 34, at tier 1 / tier 1.5

**Primary.** Mean **tier-1** excess (tier 1.5 wherever it clears the mixing floor of §1.2) is positive with
a 95 % CI clear of zero, per family and pooled at declared weights.

**The declared limitation, and it belongs in the seal rather than the write-up: this design cannot reach
the H-real bar.** Tier 2 is definitionally unavailable for 33 of 34 readings, so no result here can be
`ANTI-BLENDABILITY-REAL` in the sense the directive sealed. What it *can* do is decisive in one direction
and only suggestive in the other:

- **excess dies at tier 1 or 1.5 → `CONTROL-MISMATCH@1` / `@1.5`.** H-artifact wins, cleanly, and the
  sixth species is confirmed.
- **excess survives tier 1.5 → `ANTI-BLENDABILITY-UNREFUTED`** — a *new* verdict this draft proposes,
  because reusing `ANTI-BLENDABILITY-REAL` would claim a bar the design cannot clear. It says: not
  explained by coordinate marginals, cardinality, or size, and **not tested against species membership**.

Ruling item: **the added verdict**, or its rejection in favour of reporting survival as INSUFFICIENT.

### Secondary — the ladder is the mechanism

The full **tier 0 → 1 → 1.5 → 2** excess ladder is reported for **every** anomaly reading, with per-tier
provenance. The ladder's shape *is* the finding:

- dies at tier 1 → **coordinate marginals** explain it
- dies at tier 1.5 → **cardinality structure** explains it
- dies at tier 2 → **species membership** explains it *(reachable for 1 reading; reported, never pooled)*
- survives tier 2 → **H-real stands** *(not reachable by this design — see the limitation above)*

### Unit of analysis

Flavours inside one region are computed **on the same region** and are not independent. The unit is
therefore **(row, region, ramp-step)**; `row`-clustered results ship as the robustness check.

---

## 3. Verdict vocabulary — sealed

- **ANTI-BLENDABILITY-REAL** — survives tier 2. **Unreachable by this design** (1 of 34 readings has a
  tier-2 control) and retained in the vocabulary only so a later study can use it. Declared unreachable in
  advance rather than quietly unused.
- **ANTI-BLENDABILITY-UNREFUTED** *(proposed; §2)* — survives tier 1.5 with no tier-2 test available.
- **THEOREM-SATURATED** *(proposed; §0.3)* — violation forced to 1.0 by the region's construction. 58
  readings. Excluded from every statistic, reported with its argument, and the reason the anomaly set is
  34 rather than 92.
- **CONTROL-MISMATCH** — dies at a named tier. **The tier is part of the verdict** (`CONTROL-MISMATCH@1`,
  `@1.5`, `@2`).
- **MIXED** — family-dependent. The table is the finding.
- **INSUFFICIENT** — per the standing floors, declared per reading: `INSUFFICIENT-r`,
  `INSUFFICIENT-degenerate`, plus tier-specific unavailability.

---

## 4. Power, pre-declared

Computed from the **already-disclosed tier-0 excess spread** — the quantity that *defines* the anomaly set
and is visible in the frozen column. **Not** from the sealed tier-1/tier-2 statistic, which has not been
computed and must not be before ruling.

Computed on the **residual 34**, since that is what will be scored.

| unit of analysis | n | tier-0 excess SD | **MDE** (α .05, power .80) | mean tier-0 excess |
|---|---:|---:|---:|---:|
| reading | 34 | 0.1224 | +0.0624 | +0.1457 |
| **(row, region, step)** — primary | **32** | **0.1217** | **+0.0642** | +0.1537 |
| row-clustered — robustness | 9 | 0.1055 | +0.1232 | +0.1357 |

**The declaration that binds:** at the primary unit this instrument sees about **+0.064**; row-clustered,
about **+0.123**. Below that it reports INSUFFICIENT, **and INSUFFICIENT is not evidence of absence.**

**The honest reading of that table, stated now rather than after the result:** the disclosed tier-0 mean is
+0.154 and the row-clustered MDE is +0.123. So if fairer controls absorb even **20 % of the tier-0 excess**,
the row-clustered arm goes INSUFFICIENT rather than negative. The design is **well powered to detect
survival and poorly powered to distinguish partial absorption from total absorption** — which is a real
limitation of scoring 9 rows, not a defect to be fixed by choosing a friendlier unit.

---

## 5. Multiple-comparisons ledger — opened here

This is the sequence's **first true seal** (Q4 was hygiene, Q3 descriptive). The family-wise ledger opens
with this study.

| | |
|---|---:|
| primary test (single arm, pooled) | 1 |
| secondary per-family | 4 |
| **family-wise family size** | **5** |

**Correction: Holm–Bonferroni at FWER 0.05**, smallest threshold 0.05/5 = 0.01000. The ladder's per-tier
readings are **descriptive**, not tests, and do not enter the family — stated now so they cannot be
promoted to tests after the fact.

**Q1's eventual seal closes over this ledger** and inherits its count; noted here per directive so the
family cannot be silently reset between studies.

---

## 6. Standing laws, applied

- Distinct m-subsets only; the pre-declared `INSUFFICIENT-r` (r < 10) and `INSUFFICIENT-degenerate`
  vocabularies govern unchanged.
- Theorem-forced flavours excluded **by the derived join** — 0 of the 92 are forced, verified, so the
  exclusion binds vacuously here and is still enforced in code.
- Per-reading provenance ships **all** control tiers, including unavailable ones with their reason.
- Scoring runs **once**, against the **frozen** survey column. **No new readings.** Measured rates are
  inputs and do not move.
- Tidy-number, denominator, bound-claim and meta gates live throughout.
- Anything eye-catching outside the sealed statistics goes to the **bank**, not the findings.

### 6.1 One mechanical obstacle, disclosed

Computing any new control tier requires **regenerating the regions** — the artifact stores summaries, not
members. v3's 78 anomaly readings carry **per-reading seeds** and regenerate directly. **v2's 14 do not**;
they are recoverable only by replaying the entire v2 RNG stream in order. That replay is deterministic and
cheap, but it is a reproduction step with its own failure mode, so it ships with an assertion that each
replayed region's *r* matches the frozen reading's *r* — and any mismatch drops the reading to
INSUFFICIENT rather than silently substituting a different region.

---

## 7. What is not authorised

No new rows, no new encodings, no re-measurement of any frozen rate, no scoring before ruling. The Q2 fork
and Q1's seal are untouched. W-review remains open independently.

---

## 8. Box

- **I-phase + this draft:** ~2–3 h. **Done.**
- **Scoring run after ruling:** ~1–2 h. $0 compute (largest job is tier-1.5 chains on 51 sparse regions).

---

## 9. Open items — ALL RULED 2026-07-26

**All six approved.** Recorded as ruled rather than deleted, since the questions are what the seal answered.

1. **RULED: approved, with the instrument fix.** The `THEOREM-SATURATED` screen (§0.3) — it removes 58 of 92 readings and is the single largest
   judgement in this draft. It also implies a fix to a standing instrument: the forcedness join gains a
   `forced_saturated` direction. Ruling needed on both the screen and the instrument fix.
2. **The single-arm design.** The first draft proposed stratification; after the screen there is 1 optimal
   reading left and stratification is moot. §2.
3. **Tier 1.5's admission to the ladder.** It was not in the directive; the I-phase found tier 1 breaks
   fixed-cardinality regions, which is the very structure H-artifact is about. §1.1.
4. **The 9 non-binary readings** (`graph-3-coloring`, `sudoku`) need a domain-general tier 1, or they ship
   as `INSUFFICIENT-encoding`. §1.
5. **§0.2 — the concentration claim.** The tree-row premise does not hold in the data; the ruling should
   confirm the seal proceeds on the anomaly as measured rather than as described.
