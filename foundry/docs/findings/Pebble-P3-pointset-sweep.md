# Sprint 6 "Pebble" — P3: the full point-to-set sweep

**The result is mixed and the record says so — three facts, not one letter** (the single-letter a/b/c scheme was a
design flaw: (a) and (b) are not exclusive, they are a ratio, and the ratio is the finding). Observable: the qualified
point-to-set instrument (`measure_pointset`, reach_score = signal at r=2). Roster: 4 affine/parity LONG anchors +
44 bounded-width SHORT reps across 12 co-clones (rich within-co-clone replication), size ladder n∈{12,15,18} at
constant density. prereg_v24.

## Gate — provenance + population, before any interpretation

- **139/144 cells measurable; 94% exact coset enumeration**, 6% sampled.
- **5 cells declared UNMEASURABLE and set aside (not averaged):** thin cosets at small n in two bounded-width
  co-clones (`1v+dhorn#2` n=12/15, `1v+dhorn#3` n=12, `0v+horn#3` n=12/15). A reading is scored only over measurable
  cells.

## Fact 1 — the dichotomy is REAL and ALGEBRAIC (a-dominant)

| class | n=12 | n=15 | n=18 | trend |
|---|---|---|---|---|
| **LONG** (affine / parity) | 0.254 | 0.320 | 0.337 | **+0.084 (grows)** |
| **SHORT** (bounded-width) | 0.113 | 0.110 | 0.116 | **+0.003 (flat)** |
| between-class gap | 0.141 | 0.211 | 0.221 | widens |

The LONG (affine) and SHORT (bounded-width) classes separate cleanly and the separation **strengthens with n**. Reach
tracks the Schaefer/algebraic dichotomy — the deflationary-but-expected reading is dominant.

## Fact 2 — a secondary relation-level RESIDUE (b-present-but-minority)

**within-co-clone SD / between-class gap = 0.0957 / 0.2107 = 0.45** (vs Sprint 4.6's *decisive* ~1.0). The
within-co-clone reach variation is real and concentrated in the bounded-width co-clones (`0v+1v+dhorn`,
`0v+1v+horn+dhorn+bij`, … max SD 0.096 at n=18): reach carries *some* relation-level structure the co-clone does not
fix. At ~45% of the gap it is **half of what made Sprint 4.6's terrain result decisive** — real, but a minority
component, not the headline.

## Fact 3 — the finite-size hypothesis: TWO SEPARATE ENTRIES (per owner ruling)

**Entry [1] — the sealed (c) trigger FIRED, on its literal stated terms.** prereg_v24's (c) signature ("the
between-class gap changes by ≥30% relative from smallest to largest n") is met: the gap changed 0.141 → 0.221, +57%.
Recorded as fired.

**Entry [2] — dated directional refutation (interpretive note).** The pre-registered directional reading — stated
*before the data landed* (while the sweep was running): "if the long class grows with n while the short class stays
flat, the gap *widens*, which argues against finite-size artifact and toward real dichotomy" — is met exactly: LONG
+0.084, SHORT +0.003. The gap change is **divergence, not the convergence/blurring that "finite-size artifact"
means.** So the artifact interpretation is refuted, on a reading dated before the data. A reader may disagree with
Entry [2] without touching Entry [1].

**Spec defect logged (for future prereg versions):** the (c) trigger is **direction-blind** — it fires on gap
*magnitude* regardless of whether the levels converge (artifact) or diverge (real). This is the **second
specification defect this sprint** (the first: the v22 "parity single-max" clause, withdrawn). Both are owner
specification errors, logged here as defects rather than smoothed into the verdict, so the literal outcome and the
reasoning stay separable and auditable.

## Consequence carried

The v23 phase-2 expectation holds and is now measured, not just predicted: the differential prediction (prereg_v12/v13,
a strong/moderate/weak/none **gradient**) should expect **two levels** on the point-to-set observable, with a minority
relation-level residue inside the bounded-width level. **P4 tests whether that residue is *terrain-relevant*** — the
only part of this result that could be news rather than confirmation.
