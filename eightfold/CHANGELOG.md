# Changelog — eightfold

## 0.1.0 (unreleased)

- Phase 0: scaffold the product (pyproject — stdlib-only core, `[analysis]` extra for
  pandas/prince/scipy/sklearn; README; AGENTS.md invariants; `.gitignore`), commit the v1 spec with Build
  addenda R1–R8, add the CI leg (`.github/workflows/tests.yml`).
- Phase I: record I1–I4 investigation (compendium machine-readability; prior-art check — "not aware of a
  quantitative multi-charge problem atlas"; canonical encoding fixed per problem; ordinal/categorical coding
  pre-committed).
- **A1 done-gate MET** (`docs/findings/A1-pilot.md`): `atlas.py` (schema + 8 QC gates + loader +
  validate/summary CLI, retargeting the physmap corpus validator), `charges.py` (the eight charge
  vocabularies + the entailment layer with per-rule `preconditions`, R6), `results/atlas/SCHEMA.md`,
  `docs/CORPUS_PR_REVIEW_GUIDE.md`, `structure.py` (Cramér's V + in-house MCA + clustering + marginal
  occupancy/entailment triage + `--drop-measured` ablation), the **22-problem pilot atlas**
  (`results/atlas/atlas.jsonl`), and the pilot structure preview. **Coverage 83.3%** (90/108 applicable cells
  cited), **zero uncited-folklore** → population-failure kill does not fire; proceed to A2. 28 tests green.
- Prereg locked before any analysis run (R7): `prereg_v1.json`, then **`prereg_v2.json`** after two entailment
  rules (E6/E7) were found invalid for the atlas (R1 object-mismatch; XOR-SAT counterexample) and demoted to
  informational — a changed prediction is a new version, not an edit. The Census C2 backbone entered as the
  single `measured` cell (R9).
- **A2 setup (R11–R16, after cell-by-cell A1 review; `docs/findings/A2-setup.md`):** subspace clustering +
  approx|param residual method locked in **`prereg_v3.json`** (pilot-informed, R11); EPTAS/Marx bridges added
  as informational entailment rules (R12); **number-partitioning** promoted to its own row and the borrowed
  knapsack landscape cell reverted to `open` (R13); the Census cell recoded **`freezing-measured`** with the
  no-proof-space-OGP-theorem novelty recorded (R14); the `n.a.`/`open` boundary pinned and swept (R15); two
  new `average_case` values — `worst-case-to-average-equiv` (permanent/Lipton), `hard-on-average-conjectured`
  (planted clique) (R16); plus ordinary fills (knapsack/param W[1], VC/avg Weigt–Hartmann, horn/approx
  APX-complete). Then **R17** split `average_case` into an algorithmic-difficulty `value` + a separate
  `transition_known` boolean sub-field (schema clarification; prevents sociology-driven A3 associations). The
  atlas builder is now committed at `dev/build_atlas.py` (authoritative source; `atlas.jsonl` is generated).
  **23 problems, 86.4% cited**, 32 tests green.
- **A2 expansion (batch 1):** +27 well-studied problems (graph / logic / number / counting / optimization) —
  dominating-set, feedback-vertex-set, steiner-tree, longest-path (color-coding FPT), reachability/STCON,
  max-flow (P-complete), MST (counting-FP via Matrix-Tree), treewidth (Bodlaender FPT), circuit-value
  (canonical P-complete), tseitin, subset-sum, integer-programming (Lenstra fixed-dim FPT), primality (AKS —
  contrast factoring), discrete-log, SVP (Ajtai worst-case-to-average), gcd, network-reliability,
  tutte-polynomial, bin-packing, makespan (PTAS), metric-TSP (APX vs general-TSP inapprox), max-coverage, …
  **50 problems, 74.2% cited**, 0 uncited-folklore, 32 tests green. Structure preview complete-case MCA now
  4 dims (up from 2 at N=23). Remaining: ~70 more toward ~120, then A3.
- **Batch-1 review corrections:** fixed 3 value errors — gcd/parallel NC→open (E-1: Kannan-Miller-Rudolph is
  sublinear, not NC), treewidth/approx APX-complete→open (E-2: no O(1)-factor known; SSE-conjectural
  hardness), network-reliability/decision P→harder (E-3: borrowed s-t connectivity; #P-hard via Turing
  reduction). **R18** split the worst-case→average *relation* out of the value (new
  `worst_to_average_self_reduction` boolean + `hard-on-average-provable` value; permanent/discrete-log
  recoded; **SIS** added as its own row for Ajtai's reduction; SVP/avg→open). **R19** added `APX`
  (absolute-ratio; bin-packing). **R20** added a citation-establishes-the-value audit gate (also caught
  longest-path/approx + treewidth/decision citation mismatches). Fills: hamiltonian-cycle/avg→easy-on-average
  (Bollobás–Fenner–Frieze), nae-sat/param→FPT. **51 problems, 73.0% cited**, 33 tests green.
- **Rider 1 (`prereg_v4`, committed before batch-2 curation):** the A2 gate is now **per-charge** — core
  (decision/counting/approximation/parameterized) must **each** reach ≥85% cited; frontier
  (parallelization/proof-size/average-case/landscape) is **reported, not gated** (open-rate = "map of unasked
  questions"); aggregate is reported, no longer load-bearing. Fixed prospectively before any number trips it
  (anti-threshold-loosening). `atlas.coverage_report` now emits `core_charge_ratios` + `a2_core_gate_pass`.
  At commit: decision 98% / counting 76% / approximation 93% / parameterized 86% — counting flags the
  batch-2 counting-cell backfill (rider 2).
- **Rider 2 (cheap-wins backfill, timeboxed):** filled the batch-1 counting gaps (#P-complete via parsimonious
  reduction — steiner-tree, ILP, metric-TSP, k-center, bin-packing, makespan, max-coverage) and the nae-sat
  frontier cells (avg `hard-on-average-conjectured`, landscape `clustering-OGP-known`). **Per-charge A2 gate
  now PASSES** (decision 98 / counting 95 / approximation 93 / parameterized 86); aggregate 76.8%, 34 tests.
  Stopped there — the remaining opens are genuine frontier (the map of unasked questions).
- **A2 batch 2:** +16 problems — edge-coloring, min-bisection, multiway-cut, directed-FVS (FPT, Chen et al.),
  3D-matching, bipartiteness (P/FP/NC easy row), matrix-multiplication, linear-equations, CVP, quadratic-
  residuosity, tautology (coNP-complete "harder" + the proof-complexity home problem), Σ₂-SAT (PH level 2),
  monotone-circuit-value (P-complete), 1-in-3-SAT, MAX-2LIN (Unique-Games canonical), job-shop. Counting
  filled for every NPC row (per the gate). **67 problems, 74.9% cited; per-charge A2 gate PASSES**
  (decision 98 / counting 96 / approximation 86 / parameterized 85), 34 tests. Genuinely-open approximability
  cells (edge-coloring / min-bisection / directed-FVS / job-shop) left `open` per R20 — not manufactured.
- **R22 (decision partial order) + edge-coloring fill:** split `harder` → `coNP-complete` / `PH-complete`
  (level in `perspective`) / `PSPACE-complete` / `beyond-PSPACE`. `decision` is now a **partial order**
  (`DECISION_PARTIAL_ORDER`, proven containments only; **NPC ∥ coNP-complete**), removed from the linear
  `ORDINAL` so A3's ordinal-sensitivity check can't assert NP<coNP. Recoded tqbf→PSPACE-complete,
  tautology→coNP-complete, Σ₂-SAT→PH-complete/Σ₂ᵖ; edge-coloring/approx→`APX` (Vizing membership + Holyer 4/3
  barrier, R19). Network-reliability decision (PP-hard) held `open` — a candidate future `counting-hard` value.
  35 tests; gate PASSES (decision 97 / counting 96 / approximation 89 / parameterized 85).
- **A2 batch 3:** +15 problems populating the R22 decision rungs + witnesses — LWE (lattice, avg
  `hard-on-average-provable` via Regev, beside SIS), MCSP + group-isomorphism (NPI-candidates), planarity
  (P/NC), planar-matching-count (counting **FP** via FKT — the structured foil to #P-complete #matchings),
  Π₂-SAT + dnf-minimization (PH-complete Π₂ᵖ/Σ₂ᵖ), succinct-3-coloring (**beyond-PSPACE**/NEXP-complete),
  odd-cycle-transversal + cluster-editing (FPT), quadratic-assignment, planar-3-coloring, steiner-forest,
  maximum-common-subgraph, first-order-model-checking (PSPACE-complete). Counting filled for all NPC rows.
  **82 problems, 72.9% cited.** Per-charge gate: decision 96 / counting 95 / **approximation 84 / parameterized
  82** — dipped just under 85% because batch 3 was PH/lattice-heavy with genuinely *open* approximability /
  parameterized cells (not lazy gaps); a mid-A2 transient (the gate is an A2-COMPLETION target per prereg_v4),
  **not** manufactured up. 35 tests. Remaining: ~38 toward ~120, expected to recover the gate as
  NP-optimization batches (clean approx/param) are added.
- **A2 batch 4:** +18 NP-optimization/graph problems with clean approximation + parameterized — connected-VC,
  edge-dominating-set, hitting-set, max-leaf-spanning-tree, prize-collecting-Steiner, feedback-arc-tournament
  (PTAS), Kemeny (PTAS), capacitated-VC, k-set-packing, partial-VC, group-Steiner, graph-motif,
  induced-subgraph-iso, disjoint-paths (Robertson–Seymour FPT), cutwidth, treedepth, min-fill-in,
  weighted-interval-scheduling (P/FP easy). **100 problems, 73.8% cited; per-charge gate PASSES again**
  (decision 97 / counting 96 / approximation 86 / parameterized 88) — recovered from the batch-3 dip as
  predicted (treedepth & planar-3-coloring approx recoded `APX` once the constant-factor bounds were
  confirmed; the rest stayed honestly `open`). 35 tests. Remaining: ~18–20 to ~120.
- **A2 batch 5 (curation to ~120):** +18 — densest-k-subgraph, cluster-vertex-deletion, max-directed-cut,
  d-hitting-set, bin-covering, survivable-network-design, shortest-common-superstring, directed-Steiner-tree,
  k-median, the **planar-PTAS trio** (VC / dominating-set / IS — structure lifts approximability to PTAS+FPT),
  **stable-matching** (decision-easy Gale–Shapley / counting-hard #P-complete Irving–Leather), min-cost-flow,
  and four **fine-grained P** problems (edit-distance, LCS, APSP, 3SUM — in P with conjectured time lower
  bounds, foreshadowing a v2 charge 9). **118 problems — A2 curation target (~120) reached; per-charge gate
  PASSES** (decision 97 / counting 97 / approximation 89 / parameterized 88), 0 folklore, 35 tests. Structure
  preview at N=118: full-table MCA 15 dims, complete-case (n=45) **6 dims** — both ≥3, so the R4 dual-analysis
  now *agrees* (the H1-support condition, in preview; A3 is the verdict). Frontier open-rates (the map of
  unasked questions): average-case 65/89, landscape 18/28 mostly open. **Ready for full cell-level review,
  then A3 under prereg_v4.**
- **118-row review corrections (F-1..F-4):**
  - **F-1 (systematic, serious):** the counting column was ~58% pattern-matched — the `_npc_opt` helper
    auto-stamped `counting=#P-complete` with a *generic* "Arora–Barak Ch.17" citation on every NPC
    optimization problem (the mirror of lazy-open, more dangerous because it hides). Ran R20 Check-9 over all
    counting cells: **reverted ~48** cells lacking a per-problem #P-hardness citation to `open`; **kept 30**
    with specific citations (Valiant, Provan–Ball, Creignou–Hermann, Linial, Dyer, JVW, Irving–Leather,
    Kasteleyn). **Counting drops 97% → 42%; the per-charge A2 gate now reads FAIL honestly** on counting —
    the correct outcome (a fabricated column would have poisoned A3's occupancy/multiplet analysis invisibly).
    Reverted cells are promotion-pass targets. `_npc_opt` no longer stamps counting; review-guide Check-9 now
    explicitly forbids the generic pattern.
  - **F-2:** pinned `inapprox` = no poly f(n)-approx for ANY poly f, *unconditionally* (SCHEMA). Recoded three
    overclaimers: group-Steiner & directed-Steiner → `log-APX` (contested: true status polylog, a v2 vocab
    candidate); densest-k-subgraph → `poly-APX` (conditional-hardness note).
  - **F-3:** APSP/parallelization n.a.→`NC` (min-plus matrix squaring); fine-grained average_case n.a.→`open`
    (R15 — random ensembles exist).
  - **F-4:** planar-matching-count/parallel→`NC` (Pfaffian = determinant, Csanky); FO-model-checking/param→
    `W[2]+` (AW[*]-complete); min-cost-flow/parallel→`P-complete`; one-in-3-SAT & MAX-2LIN param→`FPT`/treewidth.
  - Aggregate 64.8% (superseded A1 gate, reported only); 35 tests; 0 folklore. **A2 gate FAILS on counting
    (42%) — a per-problem counting-hardness citation pass is required before A3.**
