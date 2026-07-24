# Quarry K2 — Intersection build + screen

**Date:** 2026-07-23  **Gate:** K2  **Spec:** sealed `hardmap@f74023ac4`.  **Depends on:** K1 verdicts.
**Data:** [`results/atlas/quarry-candidates.jsonl`](../../eightfold/results/atlas/quarry-candidates.jsonl)
(+ `.csv`), built by [`dev/build_quarry.py`](../../dev/build_quarry.py).

## Method (and its honest limits)

The candidate universe is drawn from the six K1 sources and screened against the atlas's own
admission criteria (spec §3). Two limits are stated up front because they bound the deliverable:

1. **reductions.network is not live-enumerated.** Per K1, the live site + RWTH GitLab are unreachable
   from this environment. Its *coverage and citation model* are known (structured Markdown, cited
   vertices+edges, networks `classic`/`parameterized`/`approximation`), and its problem set is drawn
   from the same canonical NP/#P/W/gap-preserving literature this curation already spans — so
   membership in `rn` is marked from documented coverage, **not** a file-level join. A future pass
   with repo access (`git clone reductioncompendium/data` + a Markdown parser) upgrades `rn`
   membership to exact and is the single highest-value K2 refinement.
2. **This is the high-priority *head*, not the full pool.** 37 curated candidates is a deliberately
   ranked front, not an enumeration of the ~hundreds of un-mined problems in GHR (~150 P-complete),
   Crescenzi–Kann (~200+ NP-opt), Downey–Fellows, de Haan, and Schaefer–Umans. The head is sized to
   (a) clear the kill-criterion-1 bar with margin, (b) span the priority spectrum for K3 selection,
   and (c) exercise the screen end-to-end. **All per-charge values are PROVISIONAL screening hints,
   not R20-verified** — that is exactly what K3 does, on 10 of these.

## Aliasing table (representative — the "same problem, 3–4 names" issue)

The full alias set is the `aliases` field per candidate. A representative slice showing why
normalization is needed before a membership matrix is meaningful:

| Quarry id | reductions.network | Crescenzi–Kann | GHR | Downey–Fellows | de Haan / Schaefer–Umans |
|---|---|---|---|---|---|
| `chromatic-number` | Graph Coloring | Minimum Graph Coloring | — | Coloring (by treewidth) | — |
| `feedback-arc-set` | Feedback Arc Set | Min Feedback Arc Set (also Max Acyclic Subgraph, its complement) | — | FAS (by solution size) | — |
| `subgraph-isomorphism` | Subgraph Isomorphism | — | — | Subgraph Iso (W[1] by pattern) | — |
| `lex-first-maximal-independent-set` | — | — | LFMIS / Lex-First Maximal Ind. Set | — | — |
| `independent-dominating-set` | — | Minimum Maximal Independent Set | — | Independent Domination | — |
| `abstract-argumentation` | — | — | — | Acceptance (treewidth) | Credulous Acceptance (Σ₂ᵖ) |
| `sharp-dnf` | #DNF | — | — | — | — |
| `path-system-accessibility` | — | — | Solvable Path System / Cook's problem | — | — |
| `bilevel-knapsack` | — | — | — | — | Stackelberg Knapsack (Σ₂ᵖ) |

Complementation is the sharp S2 case: **Maximum Acyclic Subgraph** normalizes onto `feedback-arc-set`
(S2 merges complements) rather than becoming its own row.

## Membership matrix (problem × source)

Encoded per candidate as the `sources` object (`rn,ck,ghr,df,dh,su` booleans). Source → charge
mapping, confirming the intersection logic: `rn` pre-charges decision/counting/approximation/
parameterized; `ck` → approximation; `ghr` → parallelization; `df` → parameterized; `dh`/`su` →
beyond-NP decision (+ `dh` parameterized). Multi-source candidates are the intersection engine — e.g.
`chromatic-number` ∈ {rn, ck, df} yields a 4-charge row; `abstract-argumentation` ∈ {dh, su} yields a
beyond-NP-decision × parameterized row in two thin columns at once.

## The screen (spec §3, all five criteria)

1. **Problem, not class (I3):** every candidate is a natural problem with one canonical encoding
   fixable at draft time (pinned per row in K3).
2. **Distinct from existing rows (S2):** checked by id-collision (0 found) **and** token/semantic
   overlap vs all 118 names. Every near-match resolved: restrictions (planar/tournament/monotone
   variants), different objects (arcs vs vertices, induced vs non-induced, per-vertex lists), and
   different constraint languages stay **separate** per S2; complements **merge** (Max Acyclic
   Subgraph → FAS). **Two flagged `REVISIT-S2`** for owner ruling: `min-equivalent-expression` (vs
   `dnf-minimization` — general-formula vs DNF minimization) and `sharp-monotone-2sat` (its counting
   may be better modeled as `sat-2`'s counting *cell* than a new row).
3. **≥2 charges citable at R20 (screen for priority):** 31 of 37 are multi-charge PASS; 4 are
   single-charge beyond-NP/decision fillers (logged, not prioritized per §3).
4. **R1 typing:** each candidate's charges are typed or `n.a.`-able with a reason (finalized in K3).
5. **Currency:** 6 candidates carry a `staleness_check_required` flag (approximation values sourced
   through the 2000-era Crescenzi–Kann layer — `bandwidth`, `min-linear-arrangement`, `set-splitting`,
   `sparsest-cut`, `feedback-arc-set`, plus `max-*` cross-checks); their inapprox values are
   re-verified against post-2000 literature in K3 (several already resolve to current results —
   Håstad 7/8, Zuckerman n^{1-ε}, ARV √log n).

## Priority scoring (spec §3)

`score = (#R20-citable charges) × (2 if it fills a thin column {counting, parallelization, beyond-NP
decision} else 1)`, and **a candidate inhabiting an empty occupancy cell outranks everything**
(encoded as +100; the six gap-cell hits are provisional and verified against the real `gap_list` in
K3). W-hardness is a tie-break note, not a multiplier (faithful to §3's exact wording).

**View 1 — gap-cell candidates (provisional; outrank everything, pending K3 gap verification):**

| id | charges | gap-cell hint |
|---|---|---|
| `lex-first-maximal-independent-set` | decision=P, parallelization=P-complete, counting=FP | counting=FP × parallelization=P-complete |
| `abstract-argumentation` | decision=Σ₂ᵖ-complete, parameterized=FPT | decision=PH-complete × parameterized |
| `sharp-dnf` | decision=P, counting=#P-complete | **decision=P × counting=#P-complete** (decoupling witness) |
| `sharp-eulerian-circuits` | decision=P, counting=#P-complete | decision=P × counting=#P-complete |
| `sharp-linear-extensions` | decision=P, counting=#P-complete | decision=P × counting=#P-complete |
| `sharp-monotone-2sat` (REVISIT-S2) | decision=P, counting=#P-complete | decision=P × counting=#P-complete |

**View 2 — charge×thin score (non-gap head):** `chromatic-number` (8; 4 charges, counting) >
`max-2sat`, `max-e3-sat`, `subgraph-isomorphism` (6; 3 charges, counting) > `judgment-aggregation`,
and the five GHR parallelization pairs `path-system-accessibility` / `and-or-graph-accessibility` /
`context-free-membership` / `unification` / `dfs-lexicographic-ordering` (4; parallelization) >
the well-covered 3-charge graph/approximation candidates (`bandwidth`, `metric-dimension`,
`multicut`, `closest-string/-substring`, `feedback-arc-set`, `independent-dominating-set`,
`list-coloring`, `maximum-induced-matching`, `target-set-selection`; score 3) > 2-charge and
single-charge fillers.

## K2 done-gate

- **Aliasing table committed** ✓ (per-candidate `aliases`; the complementation S2 case called out).
- **Every candidate scored against §3** ✓ (37 rows; screen + priority in the data + `.csv`).
- **Existing-row dedup applied (S2)** ✓ (0 id collisions; all semantic near-matches resolved; 2
  `REVISIT-S2` referred to the owner).
- **Pool ≫ 30 multi-charge** ✓ (31 in the curated head alone; the un-mined tail is far larger) →
  independently confirms K1's no-kill determination.

## Feeds K3 (pilot pre-selection, spanning the priority spectrum, per §4.3)

- **~4 multi-compendium graph/optimization:** `chromatic-number`, `subgraph-isomorphism`,
  `feedback-arc-set`, `metric-dimension` (or `bandwidth`).
- **~2 parallelization-led:** `lex-first-maximal-independent-set`, `path-system-accessibility`.
- **~2 beyond-NP:** `abstract-argumentation`, `generalized-geography` (or `competitive-facility-location`).
- **~2 single-source / cell-filling:** `sharp-dnf` (counting decoupling), `bilevel-knapsack` (beyond-NP single).

This set is **not** the 10 easiest — it deliberately includes the columns K1 predicts are *dear*
(counting F-1, parameterized/beyond-NP membership) so the K3 cost number is representative, not rosy.
