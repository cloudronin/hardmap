# Quarry v1 — Atlas Row-Expansion Investigation Spec

**Codename:** Quarry
**Status:** Draft for review — investigation box, runs now; does not block consolidation or preprint
**Owner:** Vishnu
**Relation:** feeds a future Atlas v3. Eightfold A2 stopped at 118 rows with R20 verification cost as
the binding constraint, not row supply. The July 2026 source landscape has changed — most notably
reductions.network (Grüne–Pfaue, Nov 2025), a multi-class reduction database covering NP, #P,
SSP-NP, W[1]/W[2], and gap-preserving reductions. Quarry investigates whether the available sources
yield expansion candidates that meet the atlas's admission criteria, and produces verified citations
for those that do. **Quarry's output is a vetted, citation-attached candidate table plus a verified
pilot batch — not an ingested atlas.** Ingestion (Atlas v3) is a separate, later decision with its
own spec.

---

## 1. Objective

Determine, at the atlas's own standard, which problems from the six identified sources qualify as
expansion rows: screen against the admission criteria, prioritize by multi-charge citation
availability (the intersection strategy), and run full R20 verification on a pilot batch to measure
true per-row cost — the number that sizes any Atlas v3 decision.

**Framing honesty, carried into every output:** expansion sharpens canon statistics (tighter V,
fatter complete-case block, better-populated occupancy cells). It does not touch the
canon-vs-computation question — more famous rows deepen the canon bias (F1). Quarry's value claim
is precision, never de-biasing.

## 2. Sources under investigation

| Source | Pre-cited charge(s) | Investigation question |
|---|---|---|
| reductions.network (arXiv 2511.04308) | decision, counting, parameterized, approximation (gap-preserving) | **Q1 (the lead):** does the database export machine-readably; do its per-edge/per-vertex entries carry literature citations at a quality the R20 audit can consume, or only reduction assertions? |
| Crescenzi–Kann compendium (~200+ problems) | approximation | un-mined remainder vs the 118; **staleness check** — last updated 2000, every value needs currency verification against the modern inapproximability literature |
| Greenlaw–Hoover–Ruzzo | parallelization (P-completeness) | candidate list for the atlas's thinnest column; overlap with existing rows vs genuinely new rows |
| Downey–Fellows compendia (DF99/DF13) | parameterized | delta vs what A2 already mined |
| de Haan higher-PH compendium (ECCC 2014-143) | parameterized, beyond-NP decision | doubles as the beyond-NP decision-value extension the atlas barely populates |
| Umans–Schaeffer PH compendium | decision (PH levels) | same beyond-NP role; access/format check |

Noted for the record: **no #P compendium exists** — independent corroboration of the folklore-gap
finding. Counting remains the expensive column for every candidate regardless of source.

## 3. Admission criteria (the screen, fixed before any candidate list is read)

A candidate row passes only if all of the following hold, per the Eightfold schema rules:

1. **Problem, not class** — a natural computational problem under a standard encoding; one
   canonical encoding fixed per problem, deviations logged (Eightfold I3 discipline).
2. **Distinct from existing rows** under the Crucible S2 equivalence rule (complementation /
   trivial re-encoding merges; restrictions and different constraint languages stay separate).
3. **≥2 charges citable at R20 standard** — the citation *establishes the value* (statement, not
   survey hand-wave), encoding matches, standard parameter noted for the parameterized column.
   Single-charge candidates are logged but not prioritized; they add rows without adding
   complete-case mass.
4. **R1 typing clean** — each charge either applies or is `n.a.` with a mandatory reason
   (Strata v2 standard); objective/parameterization pinning resolvable.
5. **Currency** — for values sourced from pre-2005 compendia, a modern-literature check confirms
   the value hasn't been superseded (the Crescenzi–Kann staleness risk, applied everywhere).

**Priority scoring:** candidates ranked by (number of R20-citable charges) × (fills a thin column
or empty occupancy cell). Parallelization, counting, and beyond-NP decision values outrank another
NPC×APX-complete graph problem; a candidate inhabiting a currently-empty occupancy cell outranks
everything (it is a gap-list datum for free).

## 4. Design

### 4.1 Q1 — reductions.network deep-dive (first, it shapes everything else)

Fetch the site and paper; determine: export format (JSON/API/scrape); per-problem metadata
richness; whether citations attach to problems, to reductions, or both; coverage counts per
network; license/attribution terms. **Fork:** if machine-readable with per-entry citations, the
intersection build (4.2) is a join; if assertions-only, it demotes to a candidate-name generator
and the citations come from the classical compendia + paper-by-paper work, which roughly doubles
per-row cost. Either way the verdict is written down with the access details, dated.

### 4.2 Intersection build

Normalize problem names across all six sources (aliasing table — the same problem appears under
3–4 names across compendia); compute the membership matrix (problem × source); emit the ranked
candidate table per §3's scoring. Existing-row overlap marked so the delta is explicit.

### 4.3 Pilot verification batch (the cost measurement)

Select 10 candidates spanning the priority spectrum (not the 10 easiest — the batch must estimate
*representative* cost): ~4 multi-compendium graph/optimization problems, ~2 parallelization-led,
~2 beyond-NP, ~2 single-source-but-cell-filling. Run full R20 verification on every citable charge:
citation retrieved, statement checked against the claimed value, encoding matched, parameter
pinned, provenance field drafted. Record wall-clock per row honestly. Output per candidate: an
atlas-ready row draft (not ingested) or a documented rejection with reason.

### 4.4 Outputs

1. `quarry-source-verdicts.md` — per-source access, format, citation quality, dated.
2. `quarry-candidates.parquet` + table — ranked candidates, membership matrix, screen results.
3. Ten verified pilot row drafts (or rejections with reasons) at full atlas standard.
4. **The cost number:** measured hours per verified row, by candidate type — the input any
   Atlas v3 spec sizes against.
5. One-paragraph Atlas v3 recommendation: expand / expand-narrow (specific columns only) / don't,
   with the row-target the cost number supports.

## 5. Milestones and done-gates

| M | Deliverable | Done-gate |
|---|---|---|
| K1 | Q1 verdict + source access for all six | Every source scored (machine-readable / transcribable / inaccessible), dated; fork resolved |
| K2 | Intersection table + screen | Aliasing table committed; every candidate scored against §3; existing-row dedup applied |
| K3 | Pilot batch verified | 10 candidates through full R20; per-row cost measured and reported by type |
| K4 | Verdict note | Outputs 1–5 delivered; Atlas v3 recommendation stated with the cost-supported row target |

## 6. Kill criteria

1. **Source failure (K1):** if reductions.network is assertions-only AND the classical compendia
   yield fewer than ~30 screened multi-charge candidates beyond the 118, the expansion pool is
   too thin — write the negative note (itself useful: the canon is near-saturated at this
   standard) and stop.
2. **Cost blowout (K3):** if pilot verification exceeds 1.5 h/row averaged, the K4 recommendation
   defaults to expand-narrow or don't; the pilot still completes (the cost number is the point).
3. **Box:** 10–14 h paired total (K1 2–3, K2 3–4, K3 4–5, K4 1). $0 compute. Source mining and
   table-building are spec-driven paired work; R20 verification is judgment-bound and does not
   compress — which is precisely why K3 measures it.

## 7. Placement and sequencing

Runs now, in parallel with the Hardmap consolidation — disjoint surfaces (Quarry touches no repo
code, produces documents and a parquet; consolidation touches no atlas content). Does not block
the preprint: the paper ships on the frozen 118-row atlas regardless of Quarry's verdict, and
Quarry's outputs feed Atlas v3, which post-dates publication by construction (frozen atlas is
frozen). One interaction worth noting: if K3's pilot surfaces a candidate inhabiting a
currently-empty occupancy cell, that is a gap-list update worth a dated line in the findings even
before v3 exists. Inherits: R20 as law, R1 typing, S2 equivalence rule, encoding discipline,
dated search trails, verdict-before-ingestion.
