# Atlas v3 — V2 confirm-pass report (agent-run)

**Date:** 2026-07-23  **Gate:** V2  **Prereg:** `prereg_v9.json`  **Workload:** the 272-cell V2 program
from `dev/confirm_harness.py` (231 judgment-heavy + 14 dear, full; 27 reliable, sealed 15% sample,
seed 20260723). Verdicts: `scratchpad/confirm/verdicts{1..8}.json`.

> **Standing caveat — this is not the owner's Gate-4 promotion.** An agent verifying agent drafts is a
> real second-pass QC (it caught 60 issues below), but it is not *independent*. Schema Gate 4 reserves
> `confirmed` for the owner after reading the primary source. **No cell was flipped to `confirmed`;
> the drafted corpus remains `claimed`.** This pass substitutes for the owner's confirm in *workload*,
> not in *authority*.

## Headline

| | cells | share |
|---|---|---|
| **OK** — citation establishes the value | 212 | 77.9% |
| **CITE** — value right, citation does **not** establish it | 47 | 17.3% |
| **FIX** — value wrong | 9 | 3.3% |
| **OPEN** — cannot be established, downgrade | 4 | 1.5% |
| **non-OK total** | **60** | **22.1%** |

**The load-bearing split: value errors 4.8% (13 cells); citation errors 17.3% (47 cells).** The corpus
is in good *value* shape — 95.2% of drafted values stand — but its *citations* frequently fail Check-9
(the cited work is real and the value is right, but that work doesn't prove *that* value for *that*
object). This is the R20 gate doing exactly what it was designed to do.

## The measured confirm cost (previously unmeasured)

**~28.6 s per cell** of agent verification: **7,767 agent-seconds ≈ 2.16 agent-hours** for 272 cells,
run as 8 parallel batches → **~18 minutes wall-clock**. Per-batch rates were tight (18–32 s/cell),
so the estimate is stable. This is the first time this program has a measured confirm number rather
than an asserted one. It is an **agent-confirm** cost; a human reading primary sources at `confirmed`
standard is a different, unmeasured quantity — and remains the owner's to measure.

## Error by funnel — and a kill-criterion ambiguity that needs an owner ruling

| funnel | cells | FIX | OPEN | CITE | all-error % | **value-error %** |
|---|---|---|---|---|---|---|
| ck | 77 | 1 | 1 | 11 | 16.9% | 2.6% |
| df | 36 | 3 | 0 | 9 | 33.3% | 8.3% |
| dh | 28 | 1 | 3 | 6 | 35.7% | 14.3% |
| ghr | 6 | 0 | 0 | 1 | 16.7% | 0.0% |
| rn | 76 | 4 | 0 | 16 | 26.3% | 5.3% |
| su | 49 | 0 | 0 | 4 | 8.2% | 0.0% |

**Kill-criterion 1 (spec §7) says a funnel with error > 15% is quarantined. The outcome flips entirely
on what counts as an "error":**
- Counting **CITE as error** → **5 of 6 funnels quarantine** (everything but `su`). That would gut a
  broad expansion over citation *completeness*, not wrongness.
- Counting **only value errors (FIX+OPEN)** → **no funnel exceeds 15%** (worst is `dh` at 14.3%).

I am not going to pick for you — the spec doesn't define it and this is exactly the kind of unstated
constraint I've over-reached on before. **Owner ruling needed.** My read of intent: the kill-criterion
protects against a funnel supplying *wrong facts*, which is the value-error column; citation
completeness is a fixable debt, not poisoning. But that is a reading, not the spec.

## Error by charge — the cost model, empirically

| charge | cells | error % | FIX | OPEN | CITE |
|---|---|---|---|---|---|
| approximation | 93 | **31.2%** | 6 | 1 | 22 |
| counting | 14 | 21.4% | 0 | 0 | 3 |
| parameterized | 70 | 20.0% | 2 | 2 | 10 |
| decision | 92 | **14.1%** | 1 | 1 | 11 |
| parallelization | 3 | 33.3% | 0 | 0 | 1 |

**This confirms K1's per-column model with real numbers**: `decision` is the cheapest/cleanest column
(14.1%), `approximation` the dearest (31.2%). Notably `counting` produced **zero value errors** — the
F-1 per-problem bar was applied correctly at draft time, and the drafters left honest `open`s rather
than guessing. Tier rates were flat (reliable 22.2%, judgment-heavy 22.1%, dear 21.4%), which
undercuts the premise that the "reliable" tier needs only sampling — it errs at the same rate.

## The 13 value changes

| verdict | row | charge | drafted → corrected |
|---|---|---|---|
| FIX | `chromatic-number` | approximation | `inapprox` → **`poly-APX`** |
| FIX | `independent-dominating-set` | approximation | `inapprox` → **`poly-APX`** |
| FIX | `red-blue-set-cover` | approximation | `inapprox` → **`poly-APX`** |
| FIX | `target-set-selection` | approximation | `inapprox` → **`poly-APX`** |
| FIX | `string-folding` | approximation | `APX-complete` → **`APX`** (hardness is a different alphabet/scoring object) |
| FIX | `firefighter` | parameterized | `W[1]` → **`FPT`** (row pins *trees*; W[1]-hardness is general graphs) |
| FIX | `precoloring-extension` | parameterized | `W[1]` → **`para-NP-hard`** as written (W[1] only if the task pins chordal/interval) |
| FIX | `judgment-aggregation` | decision | level wrong — Kemeny is **Θ₂ᵖ**; pin the task to the Ranked-agenda rule for Σ₂ᵖ |
| FIX | `boxicity` | approximation | value stands; task text must read O(n^{0.5−ε}), not n^{1−ε} |
| OPEN | `robust-csp` | decision | `PH-complete` → **`open`** (no verified classical Π₂ᵖ source) |
| OPEN | `robust-csp` | parameterized | `FPT` → **`open`** (no treewidth result; unbounded domain is XP) |
| OPEN | `3-coloring-extension` | parameterized | `FPT` → **`open`** (source never parameterizes by treewidth) |
| OPEN | `3-dimensional-assignment` | approximation | `APX-complete` → **`open`** (no per-problem APX-hardness located) |

## Four systematic patterns (each one root-cause, not a one-off)

1. **F-2 `inapprox` over-use — 4 of the 9 FIXes.** Every one is the same mistake: treating n^{1−ε} or
   2^{log^{1−ε}n} hardness as `inapprox` when a trivial polynomial-factor approximation exists. **This
   reaches the frozen atlas**: `chromatic-number`'s correction is the *same cell content* the frozen
   `atlas.jsonl` carries on `graph-3-coloring`. So either v3 diverges from v1 here, or **v1 has a
   pre-existing vocab error**. That is a frozen-artifact decision and is yours alone.
2. **`APX-complete` cited to the algorithm only** — the single largest CITE cause. Drafters cited the
   upper-bound paper and omitted the hardness side, which Check-9 explicitly forbids. Mechanically
   fixable: add the second citation.
3. **My own drafter-prompt hints seeded errors.** I asserted "argumentation, ASP, abduction,
   robust-csp, 3-coloring-extension are FPT by treewidth" — wrong for `robust-csp` and
   `3-coloring-extension` (both now `open`), and the argumentation FPT cells cite the wrong paper
   (Dvořák–Pichler–Woltran doesn't cover semi-stable/stage; Dvořák–Szeider–Woltran does). Four rows
   inherited one bad hint.
4. **A citation garble I introduced at K3 propagated.** The two 1979 Valiant papers were merged into
   one citation string in the pilot's `sharp-dnf`; it reappeared on `max-2sat`, `max-e3-sat`, and
   `sharp-dnf`. #SAT-family completeness is *Enumeration and reliability* (SICOMP 8), not *the
   permanent* (TCS 8).

## Limitations

Agent-not-independent (the standing caveat). Three verifiers exhausted their 200-call search budget
near the end of their batch and adjudicated the last few cells from gathered evidence. No local PDF
rendering (no poppler), so PDF-only sources were checked via HTML/abstract/snippet — except where a
verifier fetched full text directly (batch 8 read the GHR book and Jerrum's paper; batch 7 extracted
the Nayak–Sinclair–Zwick text).

## What I did not do

No cell was promoted to `confirmed`; no drafted value was edited. The 13 value corrections and 47
citation corrections are **recorded, not applied** — applying them is a mechanical follow-up once you
rule on (a) the kill-criterion error definition and (b) the frozen-atlas `inapprox` question.
