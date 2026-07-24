> Canonical in-repo copy of the driving spec.
> Body below is verbatim; approved refinements are recorded in the **Build addenda (R1–R8)** section
> appended at the end — never by editing the body above.

# Eightfold v1 — Charge Atlas Spec

**Codename:** Eightfold
**Status:** Draft for review
**Owner:** Vishnu
**Relation to prior work:** third project in the proof-space line. Desert Map (killed, banked) established that raw proof landscapes resist local search. Proof Census (running) is measuring one new charge, proof freezing. Eightfold executes Move One of the Gell-Mann sequence: plot the zoo along every measured charge and look for multiplet structure. Moves Two (generating symmetry) and Three (gap prediction as discipline) are phase-gated on Move One finding shape.

---

## 1. Objective and hypotheses

**Objective.** Build the first quantitative charge atlas of computational problems: a curated, fully-cited dataset assigning each problem a vector of independent hardness charges, and a structure analysis over that space looking for multiplets (recurring charge combinations), forbidden regions (combinations no known problem occupies), and gaps (combinations the structure predicts should be occupied but aren't).

**H1 (dimensionality).** Hardness is a vector, not a scalar: the charge dimensions are not reducible to one effective axis. Known decouplings (XOR-SAT, 2-SAT counting, P-complete vs NC) predict at least 3 effective dimensions.

**H2 (multiplets).** Problems cluster into recurring charge signatures, families occupying the same coordinates for structural reasons, not accidents of study.

**H3 (forbidden regions).** Some charge combinations are empty and provably or conjecturally *must* be: candidate selection rules.

**Non-goal for v1.** No new symmetry theory, no claimed periodic table. v1 is Mendeleev's card-sorting, done honestly: the table, the clusters, the holes. Interpretation is phase two, earned only if structure appears.

## 2. Scope

| In scope (v1) | Out of scope (v1) |
|---|---|
| Problems as the unit (like hadrons), not classes | Organizing the 500+ class zoo directly |
| 8 charge dimensions (below), literature-sourced, every value cited | Original proofs of any charge value |
| ~20 pilot → ~120 full atlas of well-studied problems | Exhaustive coverage |
| Structure detection: correlation, clustering, empty-cell analysis | The generating algebra (Move Two) |
| Falsifiable gap list as output | Claiming gaps are theorems |

## 3. Design

### 3.1 Unit of analysis

Natural computational problems under their standard encodings (SAT, 3-SAT, 2-SAT, XOR-SAT, VERTEX COVER, CLIQUE, TSP, GRAPH COLORING, PERMANENT, DETERMINANT, FACTORING, GRAPH ISOMORPHISM, LINEAR PROGRAMMING, HORN-SAT, PHP-as-family, etc.). Problems, not classes: charges attach cleanly to problems, and classes should *emerge* as multiplets if H2 holds. Variants with different charges (2-SAT vs 3-SAT) are distinct rows on purpose; those near-identical-surface, different-charge pairs are the most informative entries (the permanent/determinant pattern).

### 3.2 Charge schema (the eight, v1)

| # | Charge | Values (ordinal/categorical) | Canonical decoupling witness |
|---|---|---|---|
| 1 | Decision | P / NPC / NPI-candidate / harder | — (the classical axis) |
| 2 | Counting | FP / #P-complete / open | 2-SAT: decision-easy, counting-hard |
| 3 | Approximation | FPTAS / PTAS / APX-c / log / poly / inapprox / n.a. | VC vs CLIQUE: both NPC, opposite approximability |
| 4 | Parameterized | FPT / W[1] / W[2]+ / XP / n.a. (standard parameter noted) | VC vs CLIQUE again, opposite sides |
| 5 | Parallelization | NC / P-complete / open | LP vs matching |
| 6 | Proof-size (Resolution; multiplet-tagged by system) | poly / exp / open | PHP: human-trivial, Resolution-exponential |
| 7 | Average-case / phase structure | transition known / easy-on-average / hard-on-average (crypto) / unknown | random 3-SAT vs worst-case 3-SAT |
| 8 | Landscape/freezing | clustering-OGP known / refuted / unmeasured | XOR-SAT: max landscape charge, P |

Schema rules: **unknown ≠ zero** (explicit `open`/`unmeasured` values, never imputed); perspective-dependent charges (6) carry their perspective tag; every cell carries a citation or an explicit `uncited-folklore` flag that must be resolved or the cell reverts to open. Schema is extensible (space complexity, quantum, communication reserved as columns 9+ for v2).

### 3.3 Sources

Primary compendia to mine before paper-by-paper work: Garey & Johnson appendix (decision), Crescenzi–Kann compendium of NP optimization problems (approximation), parameterized complexity compendia (Downey–Fellows / Cygan et al. tables), Jukna and Krajíček for proof-size, the spin-glass/OGP literature already surveyed in Desert Map I2/I3 for charge 8. Census contributes the first backbone datum to charge 8's ledger.

### 3.4 Curation protocol

Claude Code drafts rows with citations; every pilot row gets a verification pass (citation actually states the claim, encoding matches, parameter noted). Disagreements and judgment calls logged per-cell in a `provenance` field. The atlas ships as versioned parquet + human-readable table.

### 3.5 Structure detection (C-phase)

- Association structure between charges (categorical: Cramér's V matrix, MCA for effective dimensionality) → H1 verdict.
- Clustering over charge vectors; clusters compared against textbook class boundaries — do known classes re-emerge, and does anything *cross-cut* them (the interesting case)?
- Occupancy grid: which charge combinations exist, which are empty. Empty cells triaged: provably forbidden (cite the theorem) / conjecturally forbidden / **gap** (no known obstruction, no known inhabitant).
- Deliverable: the gap list, each entry stated as a falsifiable claim: "a natural problem with charges (…) should exist; none is known."

## 4. Milestones and done-gates

| M | Deliverable | Done-gate |
|---|---|---|
| A1 | Schema + pilot atlas (20 problems, fully cited) | ≥70% of pilot cells filled with cited values; verification pass complete; zero uncited-folklore cells remaining |
| A2 | Full atlas (~120 problems) | Same citation standard; coverage report per charge |
| A3 | Structure analysis + occupancy grid | H1–H3 verdicts; gap list with ≥1 triaged entry per category |
| A4 | Writeup | Atlas + findings; explicit "Move Two prerequisites" section stating what structure was/wasn't found |

## 5. Kill criteria

1. **Population failure (kill/rescope at A1):** pilot coverage below 70% cited-fillable → the literature is too sparse for a charge table at this standard; rescope to fewer charges or kill.
2. **Degeneracy (kill at A3):** effective dimensionality ≈ 1 (all charges collapse onto the decision axis; Cramér's V near-uniform high) → hardness is a scalar after all at this resolution; write the negative note. (Prior says this won't fire, the witnesses in §3.2 already contradict it, but the analysis must be allowed to say it.)
3. **Time box:** A1 within two weekend blocks; total attention ceiling 25 h paired; $0 compute (this is a literature and analysis project).

## 6. Investigation items

- **I1.** Machine-readability of the Crescenzi–Kann compendium and any structured Complexity Zoo dumps; scrape-vs-transcribe decision before A1.
- **I2.** Prior art: has anyone built a quantitative multi-charge problem atlas? (Class-inclusion diagrams exist and are not this; confirm the charge-space framing is unclaimed. State as "not aware of prior work.")
- **I3.** Encoding discipline: charges can shift under re-encoding (sparse vs dense graphs). Fix one canonical encoding per problem in the schema; log deviations.
- **I4.** Sensitivity of clustering results to ordinal coding choices; pre-commit the coding before A3 (prereg discipline carried over).

## 7. Sizing

| Phase | Est. hours (paired) |
|---|---|
| I1–I4 | 2 |
| A1 pilot | 5–7 |
| A2 full atlas | 8–10 |
| A3 analysis | 4 |
| A4 writeup | 3 |
| **Total** | **22–26 h** |

## 8. Placement and sequencing

Independent hobby-research project. Starts after Census C3 writeup closes its box; Census's backbone result enters the atlas as charge 8's newest citation. No users, no support surface, $0 compute, kill criteria as above. Pre-registration discipline (I4) carried from the prior two projects.

---

## Build addenda (approved refinements R1–R10)

Approved during spec review (paired with Claude Code). These refine the design without changing scope; the
body above is unedited. R1–R5 are review findings; R6–R9 are owner-added.

- **R1 — Canonical task per charge.** The eight charges are not properties of the same formal object:
  decision/parallelization are worst-case *decision* properties; counting attaches to the #-version;
  approximation to the *optimization* version; parameterized needs a fixed parameter; proof-size (6) is a
  property of a family of *unsatisfiable* instances; average-case (7) and landscape/freezing (8) are
  properties of a *random ensemble*. A row is a constellation of related objects sharing a combinatorial core
  (the permanent/determinant point). Each charge cell carries an explicit `canonical_task` naming the object
  it measures for that problem.
- **R2 — `n.a.` ≠ `open`; coverage counts applicable cells.** `n.a.` = the charge structurally does not apply
  (e.g. landscape on a worst-case-only problem); `open` = it applies but the value is unknown. The A1 ≥70%
  gate and kill-criterion 1 measure *applicable-and-cited / applicable*, so ensemble-only or optimization-only
  problems do not falsely read as under-covered.
- **R3 — Occupancy over marginals, not the full grid.** The full 8-D grid has millions of cells and every
  occupant is a singleton, so "forbidden"/"gap" are vacuous there. Occupancy, forbidden-region, and gap
  analysis run over 2-D and 3-D charge marginals.
- **R4 — Pre-registered missingness policy (guards H1).** MCA over many `open`/`n.a.` cells can find axes
  driven by *which problems were studied for which charges* (sociology), not hardness. Run the dimensionality
  analysis twice — full table (sentinels as categories) and a complete-case sub-block — and return an H1
  "multi-dimensional" verdict only if both agree.
- **R5 — Known-entailment constraint layer.** Some empty cells are theorem-forbidden, not discoveries
  (counting-FP ⟹ decision-P; NC ⊆ P so charge 5 is `n.a.` outside P; strongly NP-hard **with a
  polynomially-bounded objective** ⟹ no FPTAS unless P=NP). A frozen table of these implications lets
  occupancy separate theorem-forbidden from empirically-empty, and reports H1's associations as
  entailment-forced vs surprising. (Fine-grained complexity — SETH/3SUM/APSP — is a natural v2 charge 9; the
  CSP dichotomy program is the closest existing forbidden-region work.)
- **R6 — Entailment rules carry exact preconditions (owner-added).** Every rule states the theorem's exact
  hypotheses (`preconditions`, with a citation); the consistency test rejects any rule without one. A wrong
  selection rule silently converts a genuine gap into a false "theorem-forbidden" cell — the exact category we
  mine — so a missing rule is safer than an over-broad one.
- **R7 — Prereg before the pilot preview (owner-added).** Commit `prereg_v1.json` (coding + predicted
  signatures + missingness policy + kill thresholds) immediately after the I4 coding decision and before any
  `structure.py` invocation on real data; harness debugging uses a synthetic toy table, never the pilot. A
  changed prediction is a new prereg version, not an edit.
- **R8 — Human promotion scoped inside the box (owner-added).** `claimed → confirmed` promotion is owner
  time. The A1 standard is spot-check promotion of ~2 cells per charge (16 total), decoupling-witness rows
  first; full-table promotion is not an A1 requirement. "Fully cited" is never inflated to "fully confirmed."
- **R9 — `measured` evidential status (owner-added).** Add `measured` to the status ladder alongside
  `claimed`/`confirmed`: a self-generated empirical value, permitted only for charges 7 and 8 (and as
  `measured-scaling` for charge 6), and **structurally rejected by the validator for charges 1–5**. A
  `measured` cell's provenance points to a reproducible experiment artifact (prereg, manifest, seeds, code
  commit) meeting the same standard as Census. v1 rule: only *already-banked* experiments fill cells (the
  Census backbone datum enters now); new measurements are not atlas work — they are separate mini-projects
  with their own boxes, queued from the atlas's blank cells. A3 runs the structure analysis **with and
  without** `measured` cells to confirm they do not single-handedly drive any structure claim.
- **R10 — Source snapshots (owner-added).** Both primary web sources rot: the Crescenzi–Kann pages are
  hand-maintained 1990s HTML (already cited via a third-party cache), and wiki content drifts. At
  transcription time, capture an archived snapshot (Wayback, or a local copy committed under `docs/sources/`)
  and record the `retrieved` date + `snapshot` pointer in the cell's provenance. The validator requires
  `snapshot` + `retrieved` on any provenance carrying a `url` (persistent identifiers — DOI, book + page —
  need none). A citation gate whose citations can go dark is not a gate; the atlas must still validate in five
  years.

### A2 refinements (approved after cell-by-cell A1 review; R11–R16, owner-added)

- **R11 — Method changes are prereg-gated.** Any analysis-method change prompted by a pilot preview (e.g.
  subspace clustering, after plain 8-charge Hamming washed out single-charge decouplings) is committed to a
  new prereg version labeled *pilot-informed*, before any structure run on the next milestone's data
  (`prereg_v3.json` carries the A2 method). The preview may teach us about the instrument; it must not quietly
  tune the analysis post-hoc.
- **R12 — Audit approx|parameterized against known bridges before calling it surprising.** The pilot's
  strongest association is partly theorem-forced: EPTAS ⟹ FPT (Cesati–Trevisan 1997), and W[1]-hardness rules
  out EPTAS (Marx 2008). Added as informational entailment rules with preconditions; only the *residual*
  association after known bridges is H2-grade signal.
- **R13 — No borrowed cells.** A cell whose `canonical_task` cites a different problem contaminates the row
  signature (H2 treats rows as atoms). The knapsack landscape cell (citing random number partitioning) is
  fixed: **number-partitioning becomes its own first-class row** (a REM-like-landscape witness in its own
  right); knapsack/landscape reverts to `open`.
- **R14 — Our own measured cell carries the strictest standard.** The Census proof-space datum is
  **`freezing-measured`** (a distinct new value), **not** `clustering-OGP-known`: Census measured backbone
  strengthening + overlap concentration (freezing-style), not a proven overlap gap, and *no OGP theorem exists
  for proof space* — an I3 novelty finding, recorded. A3 analyzes values, so the value field must be honest.
- **R15 — The `n.a.`/`open` boundary is pinned.** `n.a.` only when the charge's object *cannot be
  constructed* (no optimization version, no unsat family); if a random ensemble could be defined, the cell is
  `open` even if unstudied. Applied as a full-atlas sweep (matching/average-case → `easy-on-average`,
  Karp–Sipser; horn-sat/landscape → `open`, Istrate; etc.).
- **R16 — Two new `average_case` values.** `worst-case-to-average-equiv` (provable via random
  self-reducibility — permanent, Lipton 1991) and `hard-on-average-conjectured` (planted-distribution
  assumptions — planted clique), distinct from crypto-standard `hard-on-average-crypto` (factoring).
- **R17 — `average_case` splits difficulty from ensemble structure.** The value now states *algorithmic
  difficulty only* (`easy-on-average` / `hard-on-average-crypto` / `hard-on-average-conjectured` /
  `worst-case-to-average-equiv`); "a phase transition is known" moves to a separate boolean `transition_known`
  sub-field. These co-occur (random 3-SAT has a known transition **and** conjectured hardness near it), so a
  single-select value mixing the two statement types manufactures spurious A3 associations — problems coded by
  whichever fact their literature emphasized (sociology again). Schema clarification, not a prediction change;
  recorded in `prereg_v3`'s coding scheme.
- **R18 — Self-reduction semantics for average-case.** `worst-case-to-average-equiv` conflated a *relation*
  with a difficulty status; removed. The value now expresses difficulty — adding `hard-on-average-provable`
  (provably hard on average from an established worst-case hardness: permanent via random-self-reducibility +
  #P-hardness) — and the worst-case→average **self-reduction** is a separate boolean
  `worst_to_average_self_reduction` (true only for *same-problem* reductions; discrete-log stays
  `hard-on-average-crypto` with the boolean true). SVP's Ajtai reduction targets a *different* problem (SIS),
  so SVP/average_case is `open` and **SIS is its own row** carrying that celebrated reduction.
- **R19 — `APX` (membership) added; charge 3 is absolute-ratio.** `APX-complete` overclaimed completeness for
  bin-packing (asymptotic FPTAS / AFPTAS, yet 3/2 absolute-ratio hardness). `APX` = constant-factor
  approximable without a completeness claim; bin-packing recodes to `APX`.
- **R20 — Citation-establishes-the-value audit.** Before each new batch, one pass checks that every cited work
  *establishes* the charge value, not merely discusses the topic (an upper bound is not APX-completeness; a
  sublinear parallel algorithm is not NC). Failures get `open` + note or a complementary citation. Standing
  gate in the review guide (Check 9); it caught gcd/NC (E-1) and treewidth/APX (E-2).
- **R22 — Split `harder` into a decision *partial* order.** `harder` → `coNP-complete` · `PH-complete` (with
  the level, e.g. Σ₂ᵖ, in `perspective`) · `PSPACE-complete` · `beyond-PSPACE`. The order structure is the
  point: NPC and coNP-complete are **siblings**, not rungs (NP vs coNP is open), so `decision` is recorded as
  a **partial order** (`DECISION_PARTIAL_ORDER`, proven containments only) and is deliberately absent from the
  linear `ORDINAL` — linearizing it would inject a fake theorem (NP < coNP) into A3's ordinal-sensitivity
  check. Tautology sits *beside* SAT, not above it: the sibling structure is the NP-vs-coNP question rendered
  as schema. (Recoded tqbf → PSPACE-complete, tautology → coNP-complete, Σ₂-SAT → PH-complete/Σ₂ᵖ while only
  two rows were affected. Network-reliability's decision — PP-hard / #P-hard-threshold — has no clean rung
  yet; held `open`, a candidate future `counting-hard` value.)
- **R23 — `counting` moved core → frontier (prereg_v5).** The F-1 review found the counting column was
  ~⅔ pattern-matched (my `_npc_opt` helper auto-stamped `#P-complete` with a generic citation); the R20 audit
  *measured* counting's real citation density at **37/118** — published per-problem #P-hardness genuinely does
  not exist for most optimization/graph problems (web-verified). Since the core/frontier split was itself a
  *prediction* about literature density, reclassifying on the measured value corrects the prediction, not a
  bar (the FAIL-under-core stays on record — **Rider 1**). The A2 core gate is now
  decision/approximation/parameterized (each ≥85%, PASSES). **Rider 2:** the 43% is an **A4 headline finding**
  — a measured *folklore gap* (the field defaults to "counting an NP-hard problem is #P-complete" but has not
  proven it for ~⅔ of well-studied problems), written up in `docs/findings/counting-folklore-gap.md`. Every
  decision-vs-counting witness sits in the 37 cited cells, so A3 loses nothing.
- **R24 — split `landscape` clustering by evidence grade (owner promotion).** `clustering-OGP-known` conflated
  a *rigorous theorem* with a *cavity/replica physics prediction* → split into `clustering-proven` and
  `clustering-physics`. The owner promotion pass demoted sat-3/landscape: k=3 clustering is physics
  (Mézard–Mora–Zecchina); rigorous OGP is K≥8. Recodes — physics: sat-3, graph-3-coloring, NAE-SAT; proven:
  xor-sat, independent-set (Gamarnik–Sudan), clique (Gamarnik–Zadik), number-partitioning (Gamarnik–Kızıldağ),
  max-cut (Chen–Gamarnik–Panchenko–Rahman), vertex-cover (via IS complementation). A coding change to a
  frontier (ungated) column, logged in prereg_v5 like R17. Same pass **confirmed** planar-VC & planar-IS
  counting (Vadhan 2001).
- **R21 — Per-charge A2 gate (prereg_v4; committed before batch-2 curation).** As breadth grows, `open` is the
  truthful value in the frontier columns the literature is sparse on. So the A2 gate is fixed *prospectively*
  (before any number trips it — to avoid retroactive threshold-loosening, which the invariants forbid):
  **core** charges (decision / counting / approximation / parameterized) must **each** clear **85%**
  cited-of-applicable (the raised population-viability test); **frontier** charges (parallelization /
  proof-size / average-case / landscape) are **reported, not gated** — their open-rate is the "map of unasked
  questions" deliverable; aggregate coverage is reported for continuity, no longer load-bearing.
