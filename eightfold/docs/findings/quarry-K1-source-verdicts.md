# Quarry K1 — Source verdicts + Q1 fork resolution

**Date:** 2026-07-23  **Gate:** K1  **Spec:** sealed `hardmap@f74023ac4` (`docs/seal-chain.md`).
**Inherits:** R20 (the 9-check per-cell pass, `CORPUS_PR_REVIEW_GUIDE.md`), R1 typing, S2 equivalence,
I3 encoding discipline, R10 source snapshots, dated search trails, verdict-before-ingestion.

**Framing honesty (carried per §1 of the spec):** everything below sizes an expansion that *sharpens
canon statistics* — tighter Cramér's V, fatter complete-case block, better-populated occupancy cells.
It does **not** touch the canon-vs-computation question; more famous rows deepen the canon bias (F1,
`foundry/docs/findings/F1-canon-or-computation-note.md`). Quarry's value claim is precision, never
de-biasing.

---

## Q1 — reductions.network deep-dive (the lead; it shapes everything else)

### Access (dated 2026-07-23)

| surface | reductions.network / RWTH GitLab | control (arxiv.org) |
|---|---|---|
| Bash egress (`curl`) | **HTTP 000, timeout** (no route) | — |
| WebFetch | **60 s timeout** (JS SPA + no route) | OK |
| in-app Browser `navigate` | **"denied or failed"** | **OK** (paper rendered) |

**Verdict — live data inaccessible from this investigation environment.** The site and both RWTH
GitLab repos (`git.rwth-aachen.de/reductioncompendium/{code,data}`) are unreachable from here while
arxiv.org is reachable — a host-specific egress limit, not a global offline. **Consequence:** the
database's *format and citation model* are fully resolved (from the paper, below), but a *live
enumeration* of its problem/reduction set is not possible from this box. The join specified in §4.2
is therefore **specified here and executed at K2 from documented coverage + classical-compendium
knowledge**, with full machine enumeration deferred to when egress to RWTH GitLab is opened **or**
the owner clones `reductioncompendium/data` locally and points Quarry at it (≈ a `git clone` + a
Markdown parser — see format below).

**Persistent citable anchor:** **arXiv:2511.04308** (Grüne & Pfaue, "A Compendium of Reductions:
reductions.network", 6 Nov 2025). Held locally (761 KB PDF + rendered HTML full text). Per R10 this
persistent ID *is* the snapshot — no Wayback capture required for the source itself.

### Format & citation model (from arXiv:2511.04308 §2–§3, authoritative)

- **Machine-readable, structured.** Data live in the public Git repo `reductioncompendium/data`,
  **one Markdown file per problem and per reduction**, heading-structured (`# name` / `# ...`
  fields, inline `$…$` TeX), organized as top-level **network folders** `classic/`,
  `parameterized/`, `approximation/`, each split into `problems/` and `reductions/`. CI enforces the
  format on every PR. A MariaDB backend is *synchronized from* this repo (the repo, not the DB, is
  the contributable source of truth).
- **Citations attach to BOTH problems and reductions**, rendered from **BibTeX** via Citation-js.
  Problem files carry a formal description + references; reduction files carry the transformation +
  references (and sometimes small worked instances). This is *richer* than the pre-planning
  assumption of "per-edge only" — the vertices are cited too.
- **Networks & coverage (current state):** `classic` = NP [Garey–Johnson] + #P [Valiant '79] +
  **SSP-NP** [Grüne–Wulf, IPCO '25]; `parameterized` = W-hierarchy W[1], W[2] [Downey–Fellows];
  `approximation` = gap-preserving reductions under the **PCP theorem** [Arora et al.] and the
  **Unique Games Conjecture** [Khot]. A **"parsimonious" filter** shows exactly the reductions whose
  source problems have a **#P-complete counting version** — a genuine asset for the counting column.
  Vis.js was chosen for "thousands of entries" scale; the paper draws on theses by Pfaue
  (arXiv:2411.05796), Bartlett (arXiv:2506.12255), Faour, Verma, He, plus Grüne–Wulf.

### Fork resolution — **per column, not blanket** (the K1 refinement)

The reduction-graph structure means an edge is often *itself* a value citation, but only for the
columns where "hardness transfers along the edge + routine membership = the atlas value." Resolved
per charge:

| charge | what reductions.network supplies | R20 Check-9 consumability | fork verdict |
|---|---|---|---|
| **decision** | NP/PH-completeness vertices + reduction chains, refs on both | edge (A ≤ B, A complete) + routine membership **establishes** B's value | **STRONG — join.** Discovery *and* value-citation compress. |
| **approximation** | gap-preserving edges (PCP/UGC) + refs | a gap-preserving edge **is** an inapprox / APX-hard value citation | **STRONG — join.** |
| **counting** | #P network + **parsimonious filter** + refs | a *parsimonious* edge from a #P-complete problem establishes #P-completeness — but F-1 demands the per-problem parsimony be checked | **MODERATE — assisted leads.** The filter points at the right edges; F-1 judgment does not compress. |
| **parameterized** | W[1]/W[2] FPT-reduction edges + refs | W-hardness transfers along an FPT-reduction, but *completeness* needs the membership side too | **MODERATE — assisted leads.** |

**Net:** reductions.network is **not assertions-only** — it is machine-readable with cited vertices
and edges. The join compresses *candidate discovery + citation-lead* cost for all four columns, and
compresses *R20 verification* cost materially for **decision** and **approximation**; **counting**
and **parameterized** still carry F-1 / membership judgment (which is exactly the cost K3 measures,
and it will split by charge, per the plan).

---

## The other five sources (scored + dated)

| source | atlas role / charges | already a source? | access & anchor | format | staleness |
|---|---|---|---|---|---|
| **Crescenzi–Kann** — Ausiello et al., *Complexity and Approximation* (1999) + KTH web list | approximation (`AK`) | **yes, load-bearing** | book (ISBN, stable) + `nada.kth.se/~viggo/problemlist/` (rot; already Wayback-cached per `docs/sources`) | **transcribable** (~200+ NP-opt problems) | **HIGH — last web update ~2000.** Every value needs a currency check vs. post-2000 inapproximability (UGC-tight APX, improved log-APX/​inapprox). |
| **Greenlaw–Hoover–Ruzzo** — *Limits to Parallel Computation* (1995) | parallelization / P-completeness (`GHR`) — the atlas's thinnest column | **yes** | book (stable) | **transcribable** (Appendix A: ~150 P-complete problems) | **LOW** — P-completeness classifications are stable; delta is coverage, not currency. |
| **Downey–Fellows** — *Parameterized Complexity* (1999) + *Fundamentals of PC* (2013) | parameterized (`DF99`/`DF13`) | **yes** | books (stable) | **transcribable** (W-hierarchy compendium) | **LOW–MOD** — DF13 is current; check only for post-2013 reclassifications. |
| **de Haan–Szeider** — *Compendium of Parameterized Problems at Higher Levels of the PH*, **ECCC TR14-143** (Nov 2014) | parameterized **+ beyond-NP decision** (Σ₂ᵖ/Π₂ᵖ+) | **new** | ECCC report id (persistent) + PDF | **transcribable** | **LOW–MOD** (2014) — doubles as the beyond-NP decision-value source the atlas "barely populates." |
| **Schaefer–Umans** — *Completeness in the PH: A Compendium*, **SIGACT News 33(3):32–49 & 33(4):22–36** (2002) | beyond-NP decision — `PH-complete` values (`perspective` = the level) | **new** (only Umans's FOCS'98 primary cite present, on `dnf-minimization`) | SIGACT News (persistent) + DePaul PDF `ovid.cs.depaul.edu/documents/phcom.pdf` (rot → snapshot if URL-cited) | **transcribable** (Garey/Johnson-style PH-complete list + best-known approx hardness) | **MOD** (2002) — currency check for improved PH-approximation results. |

**Record fact (independent corroboration of the folklore-gap finding):** **no #P compendium exists.**
The nearest counting structure anywhere is reductions.network's parsimonious-filter sub-graph.
Counting therefore stays the **expensive column** for every candidate regardless of source — the same
finding `counting-folklore-gap.md` reached from inside the atlas.

**Delta reality (feeds K2 priority):** Crescenzi–Kann, GHR, and Downey–Fellows are *already* mined for
the 118, so Quarry's delta from them is the **un-mined remainder**. The genuinely **new supply** is
reductions.network (cross-class structure + SSP-NP + parsimonious sub-graph), de Haan–Szeider, and
Schaefer–Umans — and it is concentrated in exactly the atlas's thin/empty columns (beyond-NP
`decision`, higher-PH `parameterized`, `parallelization`).

---

## R10 snapshot status

Most cells the pilot drafts will cite **primary theorems by DOI/book+page** (the compendia are
*screening/discovery* tools, not the atlas citation) — so the snapshot burden is minimal and matches
the atlas convention. Anchors: reductions.network → arXiv:2511.04308 (persistent, held); de Haan →
ECCC TR14-143 (persistent); Schaefer–Umans → SIGACT News 2002 (persistent) + DePaul PDF (snapshot
only if a cell cites the URL); Crescenzi–Kann → book anchor (already handled in `docs/sources`); GHR
/ Downey–Fellows → books. No new web-only `url` provenance is anticipated; any that arises gets a
`docs/sources/<slug>.2026-07-23.pdf` capture + `retrieved` date per gate 8.

---

## K1 done-gate

- **Every source scored** (machine-readable / transcribable / inaccessible), **dated** ✓
- **Q1 fork resolved** — per-column, written down with access details ✓
- **Kill-criterion 1 (hard stop):** requires reductions.network *assertions-only* **AND** < ~30
  screened multi-charge candidates beyond the 118. The fork resolved to **machine-readable with cited
  vertices+edges** → the first conjunct is **false** → **no hard stop**, independent of pool size.
  The pool is separately and clearly **≫ 30** (GHR ~150 P-complete, Crescenzi–Kann ~200+ NP-opt,
  Downey–Fellows W-hierarchy, de Haan + Schaefer–Umans PH-complete lists, most beyond the 118).
- **Decision: PROCEED to K2.** No narrowing forced at K1.
