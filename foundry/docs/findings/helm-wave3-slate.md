# Helm wave 3 — the slate opens with one candidate

**Status:** AWAITING OWNER RULING. Nothing here is sealed, nothing is a claim.
**Artifacts:** `helm_wave3_slate.json` · `helm_wave3_candidates.jsonl` · `wave_trail.jsonl`
**Swept:** `observatory.db` `919f3a6258052809` under `sweep/v2`

```
393 candidates enumerated
 ├─ 103 REJECTED  (netting 35 · null-missing 68)
 ├─ 289 HELD      (power-fail 260 · null-missing 29)
 └─   1 SLATED
```

The frontier reached **8 reserved rows** with batch 6, which is the size the hold queue had been naming
since wave 1. One candidate cleared.

## The slate

| | |
|---|---|
| statistic | Spearman ρ(`overlap_ref`, `bimodality_max`) over `number-theoretic` trajectories |
| disclosed | **+0.9025** |
| frontier MDE | 0.8491 (8 clusters, Fisher z, α 0.05 / power 0.80) |
| sealed bet | on the reserved rows, the cluster-level rank correlation is **positive** |
| null | cluster permutation over the frontier's cells, problem-level |
| family | size 1 — Holm threshold 0.05 |
| novelty | 1.0 against the standing bank |

This is the same candidate that topped the hold queue in waves 1 and 2 at ρ = 0.866. It rose to 0.9025
as batches 4–6 added `number-theoretic` cells, and the frontier grew past its recorded gap. Nothing was
tuned to make it clear: the gap was written down at wave 1 and the frontier walked to it.

## One thing to weigh before ruling, flagged at wave 1 and unchanged

`overlap_ref` and `bimodality_max` are **computed from the same overlap distribution** — BC is a function
of its skew and kurtosis, `overlap_ref` of its mean. There is no identity linking them, which is why the
netting screen does not fire and should not. But overlaps are bounded in [0, 1], and a mean near 0.5
admits more spread than a mean near either endpoint, so part of the association may be boundary-induced
rather than structural.

That is a question for a seal to settle, not a screen to pre-empt — but it means a confirmed result would
support "these two move together" more strongly than it supports any mechanism behind it. The bet as
stated does not claim a mechanism.

## What the frontier is

Eight rows, none captured: `balanced-vertex-separator`, `bin-packing`, `capacitated-vertex-cover`,
`k-set-packing`, `maximum-minimal-vertex-cover`, `nearest-codeword`, `planar-dominating-set`,
`weighted-interval-scheduling`. Their frames do not exist. Under Helm §0.1 the predictions would be
hashed before any of them is built, so blindness here is physics rather than discipline.

**Note the stratum composition.** Of the eight, only `nearest-codeword` is `algebraic` and none is
`number-theoretic` — the family this candidate's statistic is computed over. The bet is cluster-level and
pooled across the frontier, so it remains adjudicable, but a reader should know that the frontier does not
contain the family the disclosed prior came from. Whether that makes the test stronger (a genuine
out-of-family transfer) or weaker (a different population) is a matter for the ruling.

## The hold queue moved too

Four candidates now sit **one reserved row** from adjudication, all `bimodality_max` and `r_ref` pairings
on `graph` and `optimization`. Batch 7's reservation clears them.

## Helm stops here

No prereg was minted. No prediction was hashed. The wave ends at the slate and waits, per §0.2.
