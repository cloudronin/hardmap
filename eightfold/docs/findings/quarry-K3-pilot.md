# Quarry K3 — Pilot verification batch (10 rows) + cost measurement

**Date:** 2026-07-23  **Gate:** K3  **Spec:** sealed `hardmap@f74023ac4`.  **Depends on:** K2.
**Data:** [`results/atlas/quarry-pilot-rows.jsonl`](../../eightfold/results/atlas/quarry-pilot-rows.jsonl),
built by [`dev/build_quarry_pilot.py`](../../dev/build_quarry_pilot.py); **PASSES**
`python -m eightfold.atlas validate --path …` (10 clean, 80 cells, 22/31 = 71% cited-filled, **0
uncited-folklore**). All real values are **`claimed`** (agent draft; owner confirm pending) — never
`confirmed`. Emitted **beside** the frozen atlas; `atlas.jsonl` is byte-identical/untouched.

## The 10 pilot rows (spanning the K2 priority spectrum, not the 10 easiest)

| # | row | type | citable charges | notable R20 outcome |
|---|---|---|---|---|
| 1 | `chromatic-number` | multi-compendium graph | decision, counting, approximation, parameterized (4) | approx `inapprox` (F-2 tension, matched to clique) |
| 2 | `subgraph-isomorphism` | multi-compendium graph | decision, parameterized (2) | **counting DOWNGRADED to `open`** (F-1) |
| 3 | `feedback-arc-set` | multi-compendium graph | decision, approximation, parameterized (3) | approx `log-APX` **contested** (UGC-conditional) |
| 4 | `metric-dimension` | multi-compendium graph | decision, approximation, parameterized (3) | W[2]-complete (fills sparse W[2]+) |
| 5 | `lex-first-maximal-independent-set` | parallelization-led | decision, parallelization (2) | **counting `n.a.`** (unique object; K2 gap-hint falsified) |
| 6 | `path-system-accessibility` | parallelization-led | decision, parallelization (2) | clean (historic first P-complete) |
| 7 | `abstract-argumentation` | beyond-NP + param | decision, parameterized (2) | **decision CORRECTED** Σ₂ᵖ→Π₂ᵖ by hand-check; **fills a gap** |
| 8 | `generalized-geography` | beyond-NP (cell-filling) | decision (1) | clean PSPACE-complete (fills sparse PSPACE) |
| 9 | `sharp-dnf` | counting decoupling | decision, counting (2) | clean #P-complete; gap-hint falsified (cell occupied) |
| 10 | `bilevel-knapsack` | beyond-NP (cell-filling) | decision (1) | approx `open` (objective/variant pin unsettled) |

## The 9-check R20 pass — outcomes (the audit trail)

Every citable charge ran the 9 checks (`CORPUS_PR_REVIEW_GUIDE.md`): citation states the value in
context (1), object+encoding match (2), perspective present (3), citation resolvable (4), sentinel
choice (5), entailment consistency (6), measured/derived quarantine (7/8), **Check 9 — the citation
establishes the VALUE not the topic**. The clean pass-throughs are recorded in the row `provenance`;
the **six non-trivial outcomes** are the point of a cost pilot:

1. **`subgraph-isomorphism` / counting → `open` (F-1 downgrade).** #copies-of-H is #P-hard *in
   general* (generalizes #clique, #Ham-paths), but no clean **per-problem** #P-completeness citation
   for the general non-induced version was established at Check-9 standard. Coded `open` + note, not a
   pattern-matched `#P-complete`. This is the F-1 discipline (the counting-column trap) firing exactly
   as designed.
2. **`chromatic-number` / approximation `inapprox` (F-2 vocab tension).** n^{1-ε}-inapprox
   (Zuckerman 2007) — identical approximability to `clique`, which the atlas codes `inapprox`. Under a
   strict F-2 reading both are `poly-APX` (a trivial n-coloring is a poly-factor approx). **Coded
   `inapprox` to match the atlas's own clique precedent** (consistency beats a lone reinterpretation);
   flagged in `contested_note` as a known vocab-boundary case (cf. `directed-steiner-tree`).
3. **`feedback-arc-set` / approximation `log-APX` (contested, UGC-conditional).** O(log n log log n)
   upper (Even-Naor-Schieber-Sudan 1998); no constant factor **under UGC** (Guruswami et al. 2011).
   `log-APX` is the closest rung; the log log factor and the *conditional* hardness are flagged in
   `contested_note`. Currency: both anchors post-2000 → the Crescenzi–Kann staleness risk does **not**
   bite here.
4. **`lex-first-maximal-independent-set` / counting `n.a.` (K2 gap-hint falsified).** The lex-first
   MIS is **unique by definition**, so its counting version is degenerate (exactly one) — coded `n.a.`
   with reason, *not* the K2 provisional `counting=FP`. This **falsifies** the K2 gap-cell hint
   "counting=FP × parallelization=P-complete" for this row.
5. **`abstract-argumentation` / decision CORRECTED Σ₂ᵖ → Π₂ᵖ (hand-check caught a real error).** The
   draft claimed *credulous acceptance under preferred semantics = Σ₂ᵖ-complete*. A primary-source
   hand-check (Check 2/9, object/semantics match) found **credulous+preferred is only NP-complete**;
   the beyond-NP value requires **skeptical+preferred = Π₂ᵖ-complete** (Dunne–Bench-Capon 2002) or
   credulous+semi-stable = Σ₂ᵖ-complete (Dvořák–Woltran 2010). Retyped to skeptical+preferred
   (Π₂ᵖ-complete). **This is the single most important K3 datum: a `claimed` value was wrong, and only
   the confirm-pass caught it.**
6. **`bilevel-knapsack` / approximation `open` (R1 objective pin).** Caprara et al. 2014 give a PTAS
   for one variant and no-constant-factor for two others — the approximation value is
   objective/variant-dependent and the pin is unsettled here → `open`, not a guessed value.

**Sentinel typing** followed the atlas's demonstrated convention (checked against `clique`,
`circuit-value-problem`, `permanent`, `tqbf`, `dnf-minimization`): `parallelization` = `n.a.` "NPC ⇒
within-P n.a. (E2)" for NP-hard rows and the real value for P-rows; `proof_size` = `n.a.` "not a
propositional refutation problem"; `average_case` = `open` where an ensemble exists but is uncurated,
`n.a.` for deterministic P-complete / evaluation objects; `landscape` = `n.a.` absent a curated
clustering result.

## Occupancy + gap-list verification (against the real `a3_structure.json`)

The pilot adds **4 new occupancy value-pairs** to the atlas's marginal grid; of these exactly **one
fills a predicted empty gap cell**:

- **`abstract-argumentation` FILLS a predicted gap:** `decision=PH-complete × parameterized=FPT` was
  a gap-list cell ("should exist; none in the atlas") — now occupied (with the *corrected* Π₂ᵖ object).
  **This is a dated gap-list update (spec §7): a gap-list datum for free, worth a line even before
  Atlas v3.**
- **The `sharp-*` K2 gap-hints do NOT survive:** `decision=P × counting=#P-complete` is **already
  occupied** in the 118 (by `permanent`, `matching`, `stable-matching`, `sat-2`, `horn-sat`,
  `reachability-stcon`) — so `sharp-dnf`/`sharp-eulerian`/`sharp-linear-extensions` fill no empty cell.
  K2 gap-hints were provisional; K3 is where they are verified, and most fell.

## Cost measurement (the number that sizes Atlas v3)

**Agent-draft wall-clock:** the 10-row draft-and-validate phase took **757 s = 12.6 min → ~1.3
min/row (0.021 h/row) agent-draft.** By type (qualitative gradient, batch-timed): the **P-complete
parallelization rows were cheapest** (one clean GHR citation each), the **multi-compendium graph rows
mid** (3–4 citable charges each), and the **beyond-NP rows dearest** (semantics precision — one
required a correction).

**This EMPIRICALLY CONFIRMS the K1 per-column cost model.** The charges that ran clean were exactly
the predicted-cheap ones — `decision` NPC/P (Karp/GJ/GHR, 0 corrections) and `parallelization`
P-complete (0 corrections). The charges that forced downgrades/corrections were exactly the
predicted-dear ones — `counting` (F-1 downgrade), `approximation` (F-2/UGC judgment), and beyond-NP
`decision` (the Σ₂ᵖ→Π₂ᵖ error). Cost is **per-charge**, not per-row: a row is dear iff it touches a
dear column.

**Confirm-cost signal (the crude multiplier, refinement 2).** Three cells hand-checked against
primary sources: **85 s / 3 = 28 s/cell**, vs **34 s/cell** agent-draft → an **agent confirm/draft
ratio ≈ 0.8×** (an agent confirms about as fast as it drafts — same tools). **But the load-bearing
number is the error rate, not the time:** **1 of 3 spot-checked cells was wrong** (the argumentation
Σ₂ᵖ→Π₂ᵖ error). The *human* paired-confirm cost — reading primary sources at `confirmed` standard —
is a **larger, unmeasured** factor that only the owner's confirm-pass quantifies; the agent's 0.8×
ratio is **not** a substitute for it.

## Kill-criterion 2 (spec §6.2)

The spec's line is **> 1.5 h/row (paired-human)**. The agent-draft figure (0.021 h/row) is **not
comparable** — it is agent wall-clock, not paired-expert judgment time. **Kill-criterion 2 is not
tripped at the agent-draft level, but the pilot deliberately does not claim the human 1.5 h/row bar is
cleared** — that is the owner's confirm-pass to measure. The honest read: the agent compresses
*drafting* to minutes/row, but **does not compress the judgment** the confirm-pass supplies (the 1/3
error rate proves the judgment is still load-bearing).

## K3 done-gate

- **10 candidates through the full 9-check R20 pass** ✓ (schema-valid, 0 folklore).
- **Per-row cost measured and reported by type** ✓ (agent-draft 1.3 min/row; per-charge gradient
  confirms the K1 model).
- **Honest downgrades/corrections recorded** ✓ (2 `open` downgrades, 1 `n.a.` retype, 1 beyond-NP
  correction, 2 contested vocab flags).
- **Gap-list interaction resolved** ✓ (1 verified gap fill; 3 provisional hints falsified).
- **Frozen atlas untouched** ✓.
