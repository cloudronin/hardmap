# Helm wave 5 — two candidates, and every new screen fired

**Status:** AWAITING OWNER RULING. Nothing sealed, nothing claimed.
**Swept:** `observatory.db` `2399f397b9123139` under `sweep/v5`, `descriptor@v7`

```
468 candidates enumerated
 ├─ 125 REJECTED  netting 35 · null-missing 76 · size-marginal 7 · definitional-consumption 7
 ├─ 341 HELD      power-fail 306 · null-missing 31 · needs-r-conditioning 2 · path-gated 2
 └─   2 SLATED
```

The wave-4 sitting's rules are live and firing on real input: **7 definitional-consumption**, **7
size-marginal**, **2 needs-r-conditioning**, **2 path-gated**. None of these existed a day ago and all of
them reject or hold candidates that would previously have reached a slate.

## The slate

| # | statistic | disclosed | MDE | family cost |
|---|---|---:|---:|---|
| 1 | ρ(`overlap_ref`, `r_ref`) · optimization | **−0.792** | 0.732 | Holm 0.025 |
| 2 | Cramér's V(`bimodal_flag`, charge=`landscape`) | **0.407** | 0.404 | Holm 0.05 |

**Candidate 1 needs your eye before it is ruled.** It pairs `overlap_ref` with `r_ref` — and `r_ref` *is*
the size descriptor. The size rule did not fire because it requires **two** size-coupled descriptors, and
`overlap_ref` is not one. That is defensible: this is not two proxies for size correlated with each
other, it is a direct question — *does mean pairwise agreement track region size?* — in which size is a
variable of interest rather than a lurking confounder. But it is one screen-width away from the four
candidates the last sitting killed, and the distinction is mine, not the machine's. **Flagged rather than
decided.**

Candidate 2 clears its MDE by 0.0022. It is the first **association** candidate ever to reach a slate,
and it joins a charge — so it ran against `charge_joinable_catalog`, meaning no encoding-variant row
contributed to it.

## `bimodality_excess` is live and did not slate

260 cells carry it, range [−0.110, +0.184], mean **+0.0123**. It is enumerable by the sweep at
`descriptor@v7` and deliberately **exempt from the size rule** — subtracting the matched-r control mean
is what removes the size dependence, which is why the descriptor was built.

No candidate involving it reached the slate this wave. That is a result, not an absence: the raw
`bimodality_max` pairings that dominated wave 4's slate are now either rejected as size-marginals or held
for conditioning, and their excess-based replacements did not clear the frontier's MDE. **Whether the
coherence signal survives its own control is not yet answered** — it is now askable, which it was not.

## The hold queue reached zero gap

`ρ(bimodality_max, insufficient_share)` on optimization needs **0 more reserved rows** — it clears at the
current frontier and is held only by the `needs-r-conditioning` rule. It returns as an r-conditioned
partial at the next sweep, exactly as the wave-4 sitting specified.
