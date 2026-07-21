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
