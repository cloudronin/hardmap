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
- **Counting citation pass (choice A):** verified the kept canon is solid (Valiant 1979 covers
  IS/VC/clique/Hamiltonian/matching/#SAT — web-checked); recovered 2 cells (planar-VC, planar-IS → Vadhan
  2001, #P-complete even for planar graphs); reverted 1 mis-citation caught *in the kept set* (set-cover cited
  Provan–Ball, which is cuts/reliability, not set cover). **Result: counting = 37/86 cited = 43%.**
  Web-verification confirms the ~49 open counting cells **genuinely lack published per-problem #P-hardness
  results** — the literature establishes NP-completeness and parameterized complexity for optimization
  problems but rarely proves their *counting* versions. **Finding:** the counting charge is intrinsically
  sparse (established for ~37 of 118 problems), so an 85% core gate on counting is unachievable *honestly* —
  which argues counting belongs in **frontier** (reported, not gated), not core. That is a prereg decision
  (prereg_v5) for the owner; the 37 cited cells still carry every decision-vs-counting decoupling witness
  (permanent/determinant, 2-SAT, stable-matching, reachability, …).
- **prereg_v5 (R23 — counting → frontier; A2 gate now PASSES):** the F-1 audit *measured* counting's density
  (37/118, frontier-level), so `counting` moved core → frontier — correcting a mistaken density *prediction*,
  not lowering a bar. **A2 core gate = decision / approximation / parameterized, all ≥85% (97 / 89 / 90) →
  PASSES.** *Rider 1:* the FAIL-under-core stays on record (this entry + the F-1 entries; prereg_v4 still
  gates counting). *Rider 2:* the 43% is an **A4 headline finding** — a measured *folklore gap* (the field
  assumes #P-completeness of counting NP-hard problems but has not published it for ~⅔ of well-studied ones);
  written up in `docs/findings/counting-folklore-gap.md`. **Next: owner promotion pass (R8, incl. two
  counting-survivor draws — checking-the-checker), then A3.** 35 tests, 0 folklore.
- **Owner promotion pass (R8) + R24:** two checking-the-checker draws — (1) **confirmed** planar-VC & planar-IS
  counting (Vadhan 2001 says exactly this — #VC/#IS #P-complete even for planar bipartite bounded-degree
  graphs; the counting audit's kept set passes its draw, now 2 `confirmed` cells); (2) **demoted**
  sat-3/landscape — k=3 clustering is cavity-method physics, rigorous OGP is K≥8. The demotion forced **R24**:
  split `clustering-OGP-known` by **evidence grade** into `clustering-proven` (rigorous) and
  `clustering-physics` (cavity/replica). Recodes — physics: sat-3, graph-3-coloring, NAE-SAT; proven: xor-sat,
  IS (Gamarnik–Sudan), clique (Gamarnik–Zadik), number-partitioning (Gamarnik–Kızıldağ), max-cut
  (Chen–Gamarnik–Panchenko–Rahman), VC (via IS complementation). A coding change to the frontier (ungated)
  landscape column, logged in prereg_v5 (like R17). Gate still PASSES; 35 tests. **Next: A3.**
- **A3 — structure detection: H1 ✅ · H2 ✅ · H3 ✅** (`docs/findings/A3-structure.md`,
  `results/atlas/a3_structure.json`; `structure.py --a3` — new `a3()`, `leave_one_charge_out()`, `gap_list()`).
  Full battery under prereg_v5 (`committed_before_analysis: true`): Cramér's V, dual-missingness MCA (R4),
  subspace clustering (R11), marginal occupancy + entailment triage (R3/R5), gap list, `--drop-measured` (R9)
  and leave-one-charge-out ablations. **H1 — hardness is a vector:** ≥3 effective dims in full-table (16),
  complete-case (5, n=19) *and* every leave-one-charge-out (min 13); the ≈1-dim kill-gate (§5.2) did **not**
  fire (honest caveat: full-table dims are sentinel-inflated — the complete-case block, which drops sentinels,
  is the anchor). **H2 — multiplets:** both canonical witnesses amplify in-subspace (permanent/determinant,
  vertex-cover/clique); 2-SAT/XOR-SAT did **not** (reported, not gated). The surprising residual approx⟷param
  survives netting out the EPTAS↔FPT bridge (raw 0.52 harness / 0.73 both-real / 0.69 bridge-free), driven by
  the APX-complete×FPT cluster (22 problems); family_separation 0.15 (low → families emerge, not imposed).
  **H3 — forbidden & gaps:** all **16** theorem-forbidden cells (E1×6, E2×10) empty in the data (entailment
  invariant holds); **123** raw candidate gaps triaging honestly to 67 object-mismatch-suspect (exotic decision
  × opt/ensemble, an R1 type effect) + 56 candidate genuine (dominated by the near-empty NPI-candidate row and
  the rigorous average-case×landscape frontier). Ablations: `--drop-measured` leaves dimensionality unchanged
  (16→16 — no measured cell load-bearing). Move-Two prerequisites recorded (object-existence predicate for gap
  triage; matrix-wide bridge subtraction; counting-folklore backfill). **44 tests** (+9 `test_structure.py`,
  locking the harness + verdict *rules*, not the outcomes), 0 folklore, validate exit 0.
- **R25 — audit the H2 headline (APX-complete × FPT) against the *wide* approximability→FPT bridge.** The A3
  writeup subtracted only the narrow EPTAS↔FPT bridge; R25 pulls the broader **Cai–Chen (JCSS 1997)** result —
  *membership* in syntactic **MAX SNP / MIN F⁺Π₁** entails FPT for the standard parameterization (extended by
  Kratsch, STACS 2009) — the older bridge the layer lacked. Source-verified two load-bearing facts: it is class
  *membership*, **not** MAX-SNP-*hardness*, that transfers FPT (L-reductions don't carry it), and MIN F⁺Π₁'s Π₁
  feasibility **excludes connectivity/modification problems** (acyclicity/connectivity aren't FO-definable — so
  feedback-vertex-set, multiway-cut, connected-VC, Steiner, cluster-edit/-delete are FPT by *separate*
  techniques). Of the 22 cluster members only 4 are unambiguous syntactic members under the recorded standard
  parameter; 6 more are MAX SNP under a structural parameter; 12 are independent. New reproducible harness
  `cai_chen_residual_audit()` (surfaced in `a3_structure.json`): netting out the bridge moves approx⟷param V
  **0.73 → 0.72 (−4) → 0.70 (−10) → 0.68 (delete the whole cell)** — it **SURVIVES** even the unfair floor,
  because the coupling is the full monotone gradient (inapprox→W-hard, PTAS/APX→FPT), not one cell. **The
  multiplet is genuine; A4 leads with it.** Cai–Chen added to `ENTAILMENT_LAYER` as *informational* (R6,
  forbids nothing — "APX-complete ⟹ FPT" is false: Independent Set is APX-ish and W[1]-hard). **47 tests** (+3),
  0 folklore, validate exit 0. **Next: A4 closes the box.**
- **A4 — Move One CLOSED** (`docs/findings/A4-charge-atlas-move-one.md`). The capstone synthesis: *is hardness
  a vector?* — **yes, with earned internal structure.** Leads with the R25-audited multiplet; names the
  **counting-folklore gap** as the headline finding (37/86 applicable counting cells cited = 43%; the field
  assumes but has not published #P-completeness for ~⅔ of well-studied problems); frames the gap frontier as
  **two facts, not 56 cells** — the thin 6-problem NP-intermediate bestiary, and the uninhabited rigorous
  average-case × landscape cell (`hard-on-average-provable` {permanent,SIS,LWE} ∩ `clustering-proven`
  {xor-sat,VC,clique,IS,number-partitioning,max-cut} = ∅), the sharpest "should an inhabitant exist" question
  and one the Census instrument line can attack empirically. Honest deep-vs-definitional split: part of H1's
  dimensionality is the R1 type-of-object partition (definitional), the multiplets + folklore gap + frontier
  are the empirical yield; one approving line on family_separation reading low (families could fail to cluster,
  and did — the multiplets were earned). **Move-Two prerequisites** ordered: object-existence predicate FIRST
  (before any v2 roster), then the frontier attack, matrix-wide R25 bridge subtraction, counting backfill, and
  a candidate v2 charge 9 (fine-grained). **Move One is closed: the atlas exists, is honest about its holes,
  and its structure survives the checks brought against it.**

## 0.1.1 (unreleased) — Crucible v1.1 (adversarial self-review)

- **V1 gate MET** — the harness + prereg are locked BEFORE any real-data attack run (spec copied to
  `docs/specs/eightfold-v1-1-crucible-spec.md`). New **`derived`** evidential status (Crucible S4): a value
  entailed by a published counting dichotomy, confined to `counting`, **citation-required** (unlike
  `measured`) with a logged `provenance.condition_check = {theorem, condition, side}` whose `side` must equal
  the cell value (gate 6b). `structure.py --drop-derived` reverts derived cells to `open` so no H1 claim rests
  on the S4 backfill (surfaced in `a3()` beside `--drop-measured`). New **`crucible.py`** (behind `[analysis]`)
  with the **S1 null model**: a per-charge swap-chain MCMC preserving every marginal exactly, holding each
  row's n.a. typing fixed (R1), rejecting E1/E2-forbidden swaps — validated on a planted-structure toy
  (detected) and a pure-null toy (quiet). **`prereg_v6.json`** locks all five attack criteria + the S2 dedup
  classification (114 classes; {clique,IS,VC} merged — collapsing the VC/clique multiplet, so S2's multiplet
  test rests on permanent/determinant) + the S5 prediction (gradient weakens-but-persists) + Rider B (S3's free
  parameterized shuffle needs no rejection — no forbidding rule touches that charge — with the break condition
  recorded); `committed_before_analysis: true`. 57 tests (+10 crucible/derived), validate clean. **Next: V2
  (run S1–S3 on the real atlas).**
- **V2 — S1–S3 run (`crucible_results.json`).** The **approx⟷parameterized gradient is the flagship and it
  SURVIVES all three attacks:** **S1** null model (M=1000) — real V=0.73 sits far outside the type-respecting
  null envelope (p97.5=0.38); **S2** dedup (114 classes) — V=0.73→0.68, permutation p=0.0003; **S3** — the
  permutation **p=0.0001** (10k) the atlas never had. But S1 **RESIZES** two claims (banked honestly, not
  argued back): **H1's dimension count is typing-driven** — the real dims sit INSIDE the null envelope, at the
  *low* end (the atlas is more *correlated*, not more dimensional), quantifying A4 §5's unquantified "Some";
  "not scalar" itself still holds (dims≥3 in 96% of bootstraps). And the **H2 witness amplifications do not
  exceed typing** — permanent/determinant (0.29) is *below* the null mean (0.35), VC/clique inside the
  envelope; the R11 amplification metric carries a positive bias the null exposes (the pairs still separate
  replicably — 100% positive where present in bootstrap — but not beyond chance). Owner riders: **no metric
  redesign mid-Crucible** (a null-calibrated amplification is a labelled post-V4 re-analysis under a new
  prereg, never a quiet swap); **S2/S3 read gradient-first**. 59 tests. **Next: V3 (S4 derived backfill + S5
  violator hunt).**
- **V3 — S5 adversarial roster (S4 deferred).** Gradient-first hunt for violators of the approx⟷param
  gradient. The audit found the frozen roster ALREADY carries 7 (knapsack/subset-sum FPTAS×W[1], partial-VC
  APX-complete×W[1]; 3-coloring/TSP/longest-path/group-steiner hard-approx×FPT) — V=0.73 already survives them.
  The field's easy-approx×hard-param violators are dominated by clustering (k-center and k-median W[2]-hard-by-k
  via Dominating Set, already present but param-underspecified); **k-means** (APX-complete yet
  W[2]-hard by k, R20-cited) is the clean absent addition, kept in a separate `s5_violators.jsonl` so the
  frozen atlas stays 118 (Rider A). **S5 SURVIVES exactly as prereg'd:** adding k-means weakens the gradient
  0.73→0.66 but it persists at permutation **p=0.0001**. The gradient is NOT roster sociology. **S4 deferred**
  — S1 showed the dimension count is typing-driven regardless of n, so anchor-growth is no longer load-bearing;
  the `derived` machinery is built and tested for a later pass. 61 tests. **Next: V4 (amended A4).**
- **V4 — amended A4 (Crucible closed).** [`A4-charge-atlas-move-one.md`](docs/findings/A4-charge-atlas-move-one.md)
  §8 "Crucible results" appendix banks every verdict — the approx⟷param **gradient SURVIVES S1/S2/S3/S5**;
  **H1's dimension count + the H2 amplifications RESIZED** under the S1 null; S4 deferred — with a ledger
  line. The headline blockquote now leads with the *gradient* (the survivor), not the dimension count or the
  amplifications; §5's unquantified "Some" is quantified (statistically ~all of the dimension count is
  typing-driven); §2 H1/H2 carry resize pointers; §7 notes three original caveats (row-independence,
  no-p-values, sociology) are now *tested*, not open. **Rider A** provenance: §8 numbers labelled
  frozen-118 vs augmented-119, and A3-structure.md gets a header note pointing to §8 (frozen sha256). No
  RESIZED verdict argued back to SURVIVES. **Crucible v1.1 complete — nothing shipped until this existed.**

## 0.1.2 (unreleased) — atlas kernel (ChargeSpec); Foundry Phase K

- **Kernel extraction — the shared, spec-parametrized validator + harness (enables Foundry).** `charges.py`
  gains a frozen **`ChargeSpec`** (charges, real-value vocab, entailment layer, measured/derived-allowed,
  perspective-required, ordinal/partial-order, problem-families + methods `allowed_values` /
  `theorem_forbidden_by` / `validate_entailment_layer`) and **`EIGHTFOLD_SPEC`** built from the exact existing
  literals; every module-level name is unchanged. `atlas.validate` / `validate_corpus` and the reusable harness
  primitives (`crucible._row_valid` / `_null_chain` / `_both_real_v`, `structure.gap_list`) now take
  `spec=EIGHTFOLD_SPEC`, so one code path validates + analyses **any** charge atlas (Eightfold's eight hardness
  charges, or Foundry's CSP charges). The universal pieces (sentinels, the status ladder,
  experiment/condition-check/citation key sets) stay module-level. **Backward-compatibility gate MET:** 61
  tests pass unchanged, and `a3_structure.json` (sha `9a5ec8e0…`) + `crucible_results.json` (sha `5349b8bf…`)
  regenerate **byte-identical** — the science did not move. Eightfold now freezes as Foundry's library
  dependency; from here it is not modified to suit Foundry (Foundry Phase K, R-A).
