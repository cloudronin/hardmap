# H4 oracle spot-check (check 3) — findings

**Seed** 20260724 · **atlas** `6d53a4f1` (frozen 118) · **date** 2026-07-24 · verdicts in
`H4-oracle-check3-verdicts.json`, worksheet artifact relabeled agent-run.

## Provenance — read this first

**This is agent-run second-pass QC, not an owner-independent pass.** It carries the same standing caveat
as the V2 confirm: the adjudication leans on agent-gathered warrant evidence, so it does not meet the
owner-reads-every-primary-source bar that Gate 4 `confirmed` requires. **No cell is promoted to
`confirmed`.** The worksheet header (which read "owner manual pass") is corrected to match.

## Tally — 66 of 80 cells

| verdict | n | |
|---|---|---|
| HOLDS | 42 | citation establishes the value |
| COSMETIC | 3 | fix and log — a one-line derivation note |
| MATERIAL | 21 | dated correction through the artifacts |
| INVALIDATING | 0 | — |

**Material rate ~32%.** But the split is the finding, and it is the same anatomy as V2: **facts sound,
provenance sloppy.** Of the 21 MATERIAL, roughly **4 are genuine value/object defects** — `max-2lin`'s
gap object, `prize-collecting-steiner-tree`'s parameter, `longest-path`/counting's object, and possibly
`number-partitioning`/counting — and the other **~17 are warrant repair**: right value, wrong or
half-complete receipt. Zero cells invalidate. The atlas records the field's facts correctly; what fails
Check-9 is the citation, not the claim.

These are cells of the **frozen kernel**, so every correction is an **erratum against the frozen atlas**,
handled by the E1 protocol: v1 bytes stay frozen forever, dated entries in `errata-v1.json`, the v3
kernel copy carries the corrections tagged `erratum_v1`, and the v2→v3 delta books them as *erratum, not
drift*. The batch is being verified to primary-source precision before application (see below).

## Two systematic patterns — both root-cause, both getting an atlas-wide sweep

1. **The omnibus-textbook warrant.** Arora–Barak was cited on 8 of the drawn cells; on ~5 the book does
   not contain the claimed result. A textbook citation was used as a wildcard for "this is standard" —
   the same disease as the F-2 vocabulary error, but in provenance rather than value. **Atlas-wide there
   are 34 A&B-cited cells**, so the draw sampled a quarter of the exposure. A full sweep is running: for
   each, does the book actually establish that value for that object, and if not, the correct primary.
2. **Cygan-et-al-as-wildcard** — milder: 4 drawn cells, 2 unestablished. **Atlas-wide there are 36
   Cygan-cited cells.** Same sweep, larger surface than the draw showed.

Neither sweep reflexively replaces textbook cites — many standard results genuinely are in these books.
The defect is only where the book does not carry the specific claim.

## A framing correction — the landscape column is not "measured"

The pending 14 cells were expected to be a quick manifest audit on the premise that "landscape cells are
`measured`." **Checked against the atlas: false.** 9 of the 10 landscape cells are `status: claimed`
with literature citations (`clustering-physics` / `clustering-proven`) and need ordinary theorem
verification like any other cell; only `random-3sat-refutation` is `measured` and gets the
seeds/hashes/instrument-qualification audit. So of the 14 pending, **13 are theorem checks and 1 is a
manifest audit** — not a uniform quick pass. (This is the house failure mode one more time: a property
asserted of a column that its own per-cell data contradicts.)

## The MATERIAL set — disposition

Verified by a four-agent fan-out (full-text PDF reading) before anything is written to `errata-v1.json`,
because a wrong correction to a frozen cell is worse than the original defect. Grouping:

- **Counting (6)** — including the two the owner flagged conditional: whether `#PARTITION` and
  `#SUBSET-SUM` are actually in Valiant's SICOMP 8 (1979) enumeration list. **If either is absent, the
  frozen atlas's own counting column carries the folklore gap the atlas was built to measure, found
  against itself.** Verified against the paper's actual list, not reasoned about.
- **Decision + approximation (10)** — group-steiner (Karp → Group-Steiner origin), max-directed-cut
  (undirected-only warrant), max-2lin (gap object, repin-or-recite), set-cover/hitting-set/dominating-set
  (hardness-half-only; add the greedy membership co-cite), edge-coloring (add Holyer 1981),
  prize-collecting-steiner (parameter mismatch), sat-2/proof-size (decision-algo-not-proof-size), tsp
  average-case (concentration-not-algorithm).
- **A&B sweep (34)** and **Cygan sweep (36)** — atlas-wide, subsuming the draw's textbook misses.

**Two errata entries will be conditional on their paper check** (`subset-sum`, `max-cut`-above), per the
owner's flag that confidence in the warrant's absence is high but not certain. **COSMETIC (3)** are
one-line derivation notes: `longest-path`/approximation (any edge is a path ⇒ poly-APX membership),
`bipartiteness`/parallelization (double-cover reduction from undirected reachability), `tqbf`/proof-size
(verify the Q-resolution perspective tag is populated — a data check, not a theorem).

## Cross-links

- Two `decision`-column defects surfaced separately confirm the pattern this pass found in citations
  extends to values: `minimum-weight-triangulation` and `euclidean-tsp` (membership open, sum of
  radicals) and `shortest-vector-svp` (hard only under randomized reductions). See `errata.md` /
  `decision-membership-sweep.json`; those are a **vocabulary** gap, distinct from these **warrant** gaps.
- The infrastructure to apply this batch is in place: `freeze_atlas_v3.py`'s errata block is now
  charge-aware (it was approximation-rung-only and would have deferred every non-approximation citation
  fix).
