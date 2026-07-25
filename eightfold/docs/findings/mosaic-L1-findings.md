# Mosaic L1 — instrument qualification: QUALIFIED at 3-class resolution

**Date:** 2026-07-24. Prereg: `prereg_v10` + `prereg_v10-clarification-01` (the resolution ladder, sealed
before the recode's number). The blind locality instrument **qualifies at 3-class resolution**; P2–P6 score
there, tagged on every number.

## The instrument that scores

Round-1 blind coding, two varied coders (opus + sonnet), the **original** rubric (5-class), coder input =
`problem_id + problem_name + canonical_encoding` only (leak-clean, verified per row). Gate:

| ladder level | κ | AC1 (context) | verdict |
|---|---|---|---|
| 5-class | 0.521 | 0.655 | not reliable |
| **3-class** (decomposable / local-covering / delocalized) | **0.646** | 0.796 | **RELIABLE — the demonstrated resolution** |
| 2-class (local / delocalized) | 0.627 | 0.788 | reliable |

- **P1 anchors: QUALIFIED**, 7/7 both coders (incl. `knapsack` → `decomposable` on structure despite its
  off-diagonal coordinates — the dissociation case landing exactly as sealed).
- **Separability gate: CLEAR** — V(locality, approx)=0.436, V(locality, param)=0.178, dissociation
  structure-accuracy 1.00. The labels code structure, not charge-echo; the contamination defense held.
- **Forbidden-vocabulary: clean**, both coders.

`κ` is not a pass/kill here (clarification-01): it **measures** the granularity at which the structural
property is blind-codable. The answer is **3 classes**. The property exists and is codable; the finest
5-drawer split is not reliably codable blind, the coarser 3-drawer split is.

## Finding 1 — a finer structural criterion coded LESS reliably (rubric fragility)

After round-1's 5-class κ=0.521, the one permitted revision sharpened the `entangled`/`mixed` boundary from
theory (total-vs-partial coupling + a "name the bounded channel" tiebreak), written without opening the
disputed rows, and the corpus was fully recoded. **The revision regressed the instrument:** 3-class κ fell
**0.646 → 0.523**. Coder A over-routed to `mixed` (199/345), coder B's `uncodable` surged (26, from ~9), and
the disagreement went *diffuse* — off the entangled/mixed seam and onto the decomposable/uncodable
frontiers, which the 3-class collapse cannot recover.

This is a real, slightly counter-intuitive result: **on this phenomenon, a more precise structural rubric
produced *less* inter-coder agreement than a coarser one.** The sharper the drawer labels, the more two
careful blind coders diverge on which drawer — because the fine structure at the spectrum's hard end is
genuinely fuzzy, not because the coders are careless. The original (coarser) rubric is the better
instrument; the revision and its recode are preserved (`-recode-r1`) as this finding, not merged.

*(Process note: under clarification-01, round-1 was never NOT-QUALIFIED — it demonstrated 3-class resolution
pre-result. The revision was triggered by the pre-clarification kill rule that clarification-01 retired. A
regression is rejected. The agent initially mis-called NOT QUALIFIED and over-invoked "don't move the
metric" to refuse a legitimate pre-sealed evaluation of the un-tampered instrument; the owner corrected it.
The metric — κ ≥ 0.6 — never moved.)*

## Finding 2 — the disagreement is concentrated on the two-property seam

Of the 101 five-class disagreements, **42% are `entangled` ↔ `mixed`** — the single most common dispute of
the ~10 possible class-pairs (4× uniform). Per-class specific-agreement makes it sharp: `entangled` 0.65,
`local-covering` 0.52, `decomposable` 0.58, but **`mixed` 0.16** — the coders can find `entangled` and the
covering classes, but rarely agree a row is *`mixed`*. The blind coder can see "delocalized" reliably; it
cannot reliably split delocalized into total-vs-partial coupling.

That is exactly the seam the **knapsack dissociation** and the prereg's **two-property split**
(decomposition-locality vs certificate-locality) predicted in advance: the locality spectrum's hard end is
where a *single* label strains, because there are two partially-independent structural properties there, not
one. The instrument qualifying at 3-class (where the seam is collapsed) and straining precisely on that seam
at 5-class is convergent evidence for the two-property structure — the finding the prereg named as the
designed follow-up, arriving here from the instrument side rather than the analysis side.

## What scores, and how

- The scored locality factor is **3-class**: `decomposable` / `local-covering` / `delocalized`
  (= entangled ∪ mixed), plus `uncodable` as a non-class. Final per-row label = 3-class coder agreement
  (286 rows) + blind third-pass resolution of the 59 residual disagreements (18 of them both-real).
- Every P2–P6 number carries its resolution tag ("3-class"). The blindness/separability gate re-runs at
  3-class (already clear).
- The `entangled`/`mixed` distinction is reported as **diagnostic only** (Finding 2), never as a scored
  factor level.
