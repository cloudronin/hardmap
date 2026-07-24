# Quarry K2b — Full screened enumeration (the hard number)

**Date:** 2026-07-23  **Extends:** K2 (which delivered a 37-candidate curated *head*).
**Data:** [`results/atlas/quarry-candidates-full.jsonl`](../../eightfold/results/atlas/quarry-candidates-full.jsonl)
(+ `.csv`), 227 rows.

## Why this exists

K2's 37 candidates were explicitly a high-priority *head*, and K4 leaned on a soft "~150" estimate of
the full pool. This pass converts that estimate into a hard, reproducible count: four parallel miners
enumerated every §3-qualifying expansion candidate from the actual compendia, then the lists were
merged, de-duplicated against the 118 atlas rows + the 37 curated candidates + each other, and
S2-screened.

## The number

**227 screened candidates beyond the 118 — 161 multi-charge (≥2 R20-citable charges), 66
single-charge.**

| origin (miner / source) | candidates | multi-charge |
|---|---|---|
| curated head (K2's 37) | 37 | 32 |
| **A** — NP-opt / graph (Crescenzi–Kann, Garey–Johnson, reductions.network, Downey–Fellows) | 107 | 100 |
| **B** — beyond-NP decision (de Haan–Szeider, Schaefer–Umans, PSPACE games/logics) | 62 | 8 |
| **C** — parallelization / P-complete (Greenlaw–Hoover–Ruzzo) | 15 | 15 |
| **D** — counting-primary (#P-complete / FP, not counting-cells) | 6 | 6 |
| **TOTAL** | **227** | **161** |

The soft "~150" was well-calibrated on the **multi-charge** count (161); it under-weighted the
**single-charge beyond-NP tail** (66 — almost all decision-only games, logics, and Σ₂ᵖ/Π₂ᵖ problems
whose only applicable charge is `decision`).

**Where the qualifying supply lands, by thin column** (the columns expansion actually sharpens):
`parallelization = P-complete` → **21** rows; `beyond-NP decision` (PH/PSPACE/beyond-PSPACE/coNP) →
**68** rows; `counting` (real #P-complete/FP) → **15** rows. The bulk of the 161 multi-charge is the
NP-opt/graph tail (mostly `NPC × APX × FPT` rows that qualify but do not fill a thin column).

## How it was screened (and what that bounds)

Each miner applied the §3 screen: natural problem; **S2-distinct** from the 118 + 37 (complements and
trivial re-encodings merge; restrictions and different constraint languages/objects stay separate);
≥2 citable charges for MULTI. The miners returned their own S2-exclusion blocks — e.g. bucket A
dropped `maximum-acyclic-subgraph` (= complement of feedback-arc-set), `hamiltonian-path` (=
hamiltonian-cycle), `clique-cover` (= chromatic-number of the complement); bucket D dropped
`#stable-matchings`, `#knapsack`, `#2SAT` (counting *cells* of existing rows); bucket C dropped
`lex-first-maximal-clique` (complement-merges with LFMIS) and `one-player-pebble-game` (PSPACE, not
P). On merge, one further cell-overlap was cut: **`max-sat`** (= the `sat` row's approximation cell,
`canonical_task="MAX-SAT"`). Beyond-NP dropped the Θ₂ᵖ voting rows (Dodgson/Young — outside the atlas
decision vocab) and ~28 esoteric/uncertain entries (pomset/semilinear/WS1S/…).

**Four honesty bounds on the 227:**
1. **Provisional, not R20-verified.** These are *screening* classifications (K2-level). The K3 pilot
   measured a **~1/3 error rate** on hand-checked charge values — so the R20-*surviving* count is
   materially below 161 multi-charge (how far below is the confirm-pass's to measure).
2. **S2-restriction variants inflate it.** Geometric/planar restrictions (`euclidean-tsp`,
   `rectilinear-steiner-tree`, `planar-3sat`, `geometric-bin-packing`, …) are legitimately separate
   under S2 (like the atlas's deliberate planar trio), but a stricter "canonical-only" bar would trim
   ~15–25.
3. **The single-charge beyond-NP tail (66) is admission-dependent.** How many PSPACE games / logics /
   Σ₂ᵖ graph problems the atlas wants as one-cell `decision` rows is a judgment call; the literature
   holds more than the 62 kept here.
4. **reductions.network is not live-enumerated** (inaccessible from this environment, per K1) — its
   distinct contribution beyond the classical compendia is approximated from documented coverage.

## Bottom line

The atlas's compendia support roughly a **tripling** of the row count at this standard (~161
multi-charge + ~66 single-charge new rows vs the 118). **Supply is not, and never was, the binding
constraint** — R20 verification is. The full list is the input to any Atlas v3 mine; the count is a
*screened* ceiling, and the R20-confirmed number is smaller by the pilot's attrition.
