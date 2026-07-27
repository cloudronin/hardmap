# Helm wave 1 — the slate is empty, and the emptiness is the result

**Status:** EXPLORATORY. Nothing here is a finding about complexity. Every number below describes the
*engine*, not the atlas.
**Artifacts:** `helm_wave1_slate.json` · `helm_wave1_candidates.jsonl` · `wave_trail.jsonl`
**Swept:** `observatory.db` `6be2cfc816857ddb`

---

## What the wave did

```
344 candidates enumerated
 ├─  87 REJECTED   (30 netting · 57 null-missing)
 ├─ 257 HELD       (210 power-fail · 47 null-missing)
 └─   0 SLATED
```

Helm ran its full cycle — sweep, screens, rank — and produced **nothing for the owner to rule on**. That
is not a failure of the engine. It is the engine's first measurement, and the spec named it in advance:
Helm Kill 1 anticipates slates "dominated by untestable candidates (frontier power failing en masse)",
with the finding pre-stated as *the frontier's capture rate bounds the program's question rate*.

**The kill is not triggered.** Kill 1 requires the first **two** waves to fail this way. This is one.

## The number that matters

The frontier is **2 reserved rows**, projecting ~8 cells. A cluster-level rank correlation needs at least
**4 clusters** before its standard error exists at all — Fisher's z divides by `sqrt(n-3)`. So the
frontier cannot currently adjudicate any co-movement candidate, whatever its effect size.

The nearest candidate in the HOLD queue needs **6 more reserved rows**:

| gap | disclosed \|ρ\| | needs | candidate |
|---:|---:|---:|---|
| +6 | 0.866 | 8 clusters | `rho(overlap_ref, bimodality_max)` · number-theoretic |
| +7 | 0.843 | 9 clusters | `rho(overlap_ref, r_ref)` · optimization |
| +7 | 0.833 | 9 clusters | `rho(bimodality_max, r_ref)` · optimization |
| +7 | 0.833 | 9 clusters | `rho(r_ref, insufficient_share)` · optimization |
| +8 | 0.813 | 10 clusters | `rho(bimodality_max, insufficient_share)` · optimization |

At 25% of ~8 rows per batch — 2 reserved rows a batch — **six more rows is three more batches.** Wave 1's
slate opens at batch 6. That converts "when should we run a wave?" from a judgement call into a count.

## The shape of the hold queue is worth noticing

The five nearest-adjudicable candidates are all **coherence** descriptors — `overlap_ref`,
`bimodality_max`, `r_ref`, `insufficient_share`. Helm §4 names the live mechanism question as *coherence
vs unknown* and breaks ranking ties toward candidates that discriminate between them. Without any ranking
having run, the frontier's first affordable questions are already the ones the program most wants
answered.

Two of these deserve a flag before anyone rules on them, because they are *substantively* suspect in a
way the netting screen deliberately does not catch:

- **`overlap_ref × bimodality_max`** — BC is computed from the same overlap distribution whose mean is
  `overlap_ref`. It is location- and scale-invariant, so there is no identity linking them, but overlaps
  are bounded in [0,1] and a mean near 0.5 admits more spread than a mean near an endpoint. The
  relationship may be partly boundary-induced. That is a question for a seal to settle, not for a screen
  to pre-empt.
- **`r_ref × insufficient_share`** — `insufficient_share` counts steps failing the r floor, and `r_ref` is
  r at an admissible step. No identity, but both track region size, and the bank already carries a
  STANDING CAUTION that closure prevalence is size-driven.

## Two screens were wrong on the first run, and the second one is the more interesting

**The null screen was accepting the wrong null.** Every candidate carried a `null` field, and screen 1
checked it was non-empty. But an in-sample null *always* exists — the disclosed number was computed with
it. What a seal needs is a null for **the bet it would become**, on ground that does not exist yet. The
first run slated 20 anomaly candidates whose declared null typed the *disclosed extremal's position among
published cells* and said nothing about a frontier prediction. Candidates now carry `frontier_null`
separately, and the extremals are HELD because v1 has not pinned an exchangeability model over frontier
cells. This follows the catalog's own precedent exactly: no change-point candidate until the kink null is
pinned.

**Thirty candidates were correlating arithmetic with itself.** The first hold queue was topped by
`rho(excess_ref, excess_max) = 0.976`. Reading `foundry/catalog/extract.py`: `level()` builds one value
set per trajectory, returns a member of it as `excess_ref` beside its order statistics `excess_min` and
`excess_max`, and `shape()` computes `max_excursion_sd` from `excess_max - excess_min`. So `excess_ref ≤
excess_max` holds always, and the excursion is a difference containing both endpoints. Five descriptor
pairs are linked by identity or forced order; they now REJECT under a `netting` rule read off the
extractor rather than guessed.

**They are still enumerated.** All 30 coupled candidates appear in the sweep and in the count of 344,
rejected with the rule named. A forking-paths denominator that quietly omits the questions we already
knew were bad is a denominator we chose — and choosing it is the thing the enumeration exists to prevent.

## What the wave leaves behind

- **`wave_trail.jsonl`** — 3 events (`sweep`, `screen`, `slate`), each emitted by the stage that
  performed it. Kill 3 is checked before the wave opens.
- **`candidates` table** — all 344, rejections included, each with its verbatim SQL, its disclosed
  statistic, and the sibling count recorded at birth.
- **`hold_queue` view** — 257 held candidates, 155 carrying a numeric gap. The moment the frontier
  reaches 8 clusters, the first of them resurfaces by `SELECT`.
- **`family_ledger` view** — computed from the sweep and ruling records, never hand-maintained.

## Nothing here is a claim

No prereg was minted. No prediction was hashed. No reserved row was read — the reserved rows have no
frames to read, because they are declared and uncaptured. The wave awaits no ruling, because there is
nothing on the slate to rule on.
