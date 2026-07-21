# A3 — Structure detection over the charge atlas

**Verdict:** **H1 SUPPORTED · H2 SUPPORTED · H3 SUPPORTED.**

> Hardness is a **vector, not a scalar** — at least 5 effective dimensions survive the most
> conservative reading, and the ≈1-dimension kill-gate (§5.2) did not fire. The two canonical
> **multiplets** (permanent/determinant, vertex-cover/clique) re-separate in their predicted
> subspaces. The frozen **entailment layer is consistent with the data** — all 16 theorem-forbidden
> cells are empty — and the run emits a falsifiable **gap list** (123 raw candidate cells, triaging to
> a small interpretable residual). This is the payload Move One was built to deliver.

Prereg: [`prereg_v5.json`](../../eightfold/results/prereg/prereg_v5.json) (`committed_before_analysis: true`).
Data: [`atlas.jsonl`](../../eightfold/results/atlas/atlas.jsonl), n=118 problems, sha256 `6d53a4f1d0907f16…`.
Full machine output: [`a3_structure.json`](../../eightfold/results/atlas/a3_structure.json)
(`python -m eightfold.structure --a3`). Battery: Cramér's V matrix · dual-missingness MCA (R4) ·
subspace clustering (R11) · marginal occupancy + entailment triage (R3/R5) · gap list · `--drop-measured`
(R9) and leave-one-charge-out ablations.

---

## Setup — what was locked, and the rule for each verdict

The coding, predicted signatures, missingness policy (R4), and kill thresholds were locked in the prereg
before this run; a changed prediction is a new prereg version, never an edit. The three verdicts each
resolve a **pre-registered boolean rule**, not a judgement call:

| Hyp. | Claim | Pre-registered SUPPORTED rule |
|---|---|---|
| **H1** | hardness is multi-dimensional | ≥3 effective dims in **both** full-table and complete-case MCA (R4) **and** ≥3 under **every** leave-one-charge-out |
| **H2** | multiplets exist (charge-decoupling families) | both canonical witness pairs (permanent/determinant, vertex-cover/clique) **amplify** in their predicted subspaces (in-subspace distance > full-8 distance) |
| **H3** | forbidden regions are theorem-forbidden, empty cells are gaps | **zero** data cells contradict the entailment layer (every theorem-forbidden cell empty), and the residual empty cells are enumerated as falsifiable gaps |

Kill-gates carried from the spec: **§5.2** — effective dimensionality ≈ 1 ⇒ hardness is scalar ⇒ write the
negative note. It did not fire.

---

## H1 — Dimensionality: **SUPPORTED** (hardness is a vector)

| Reading | Effective dims (inertia > 1/8) | n | Note |
|---|---|---|---|
| Full table (sentinels as categories) | **16** | 118 | 46 categories; inflated by sentinel levels — see caveat |
| **Complete-case** (core charges, no sentinels) | **5** | 19 | the honest anchor (R4): still ≥3 |
| Leave-one-charge-out (min over the 8 drops) | **13** | 118 | dropping *any* single charge keeps ≥13 |
| `--drop-measured` ablation (R9) | **16** | 118 | identical to full → no `measured` cell is load-bearing |

The pre-registered rule requires ≥3 in **both** the full and complete-case blocks **and** under every LOCO.
All three clauses hold — and hold with margin. The **kill-gate (dimensionality ≈ 1) did not fire**: even
the most conservative reading (complete-case, four core charges only, n=19) yields **5** effective
dimensions. Hardness does not collapse to a scalar at this resolution.

**Honest caveat.** The full-table 16 is *not* the headline number: sentinel levels (`open`/`n.a.`/`unmeasured`)
enter MCA as their own categories, and a sparse frontier manufactures low-occupancy axes. R4 exists precisely
to guard this — the complete-case sub-block (which drops every sentinel) is the number that carries the
verdict, and it is 5. That block is small (n=19) and coarse (its eigenvalues include three mechanical 0.25s
from the near-binary indicator structure), so "5" should be read as "comfortably more than 1," not as a
precise count. The claim H1 licenses is the qualitative one — **multi-dimensional, not scalar** — which is
robust across all four readings.

---

## H2 — Multiplets: **SUPPORTED** (2 of 3 witnesses, plus a dominant empirical cluster)

**Subspace amplification** (R11 — a family is a multiplet if its members, close in full-8 charge space,
*separate* in the subspace the decoupling lives in):

| Witness pair | subspace | dist (full-8) | dist (subspace) | amplified? |
|---|---|---|---|---|
| permanent / determinant | decision+counting+parallelization | 0.375 | **0.667** | ✅ |
| vertex-cover / clique | decision+approximation+parameterized | 0.250 | **0.667** | ✅ |
| 2-SAT / XOR-SAT | decision+counting+parallelization | 0.500 | 0.333 | ❌ |

Both **canonical** witnesses — the permanent/determinant counting split and the VC/CLIQUE
approximation-and-parameterized split — separate exactly where theory says they should, satisfying the
pre-registered rule. The third pair (2-SAT/XOR-SAT) **did not** amplify: their differences (2-SAT counting is
#P-complete, XOR-SAT counting is FP) live as much *outside* the chosen subspace as inside it, so the subspace
does not concentrate them. Reported, not hidden — it is a witness that behaved off-prediction, and the verdict
does not lean on it.

**The surprising residual (R12 deliverable).** The strongest non-entailment-forced association is
**approximation ⟷ parameterized**. The two pairs the harness flags as *entailment-forced* — decision⟷parallelization
(V=0.59, forced by E2: parallelization is only defined within P) and counting⟷decision (V=0.46, forced by E1) —
are set aside first. What remains at the top is approx⟷param:

- harness matrix, all 118 rows with sentinels as categories: **V = 0.52**
- restricted to the n=47 problems where **both** charges carry a real value: **V = 0.73**
- after removing the one known theorem bridge (EPTAS↔FPT, Cesati–Trevisan; W[1]-hard rules out EPTAS, Marx —
  drop the FPTAS/EPTAS rows): **V = 0.69** (n=45)

The residual barely moves when the bridge is removed, so this coupling is **not** an artifact of the single
known theorem — it is a genuine multiplet. Its engine is visible in the contingency table: **22 of 47**
both-real problems sit at **APX-complete × FPT** — the textbook NP-hard combinatorial-optimization signature
(vertex cover and its relatives: constant-factor approximable, no PTAS, yet fixed-parameter tractable). That
cluster is the atlas's single densest multiplet, and neither of its two charges forces the other.

**Family separation = 0.15** (intra-vs-inter, low). The coarse `problem_family` labels do *not* form tight
clusters in charge space — exactly as intended: families were required to *emerge* as multiplets (H2), not be
imposed as an analysis input (SCHEMA.md). A low number here is the healthy outcome.

---

## H3 — Forbidden regions & gaps: **SUPPORTED**

**Forbidden cells (theorem-forbidden by the entailment layer):** **16 cells, all empty in the data.** No
row contradicts a frozen theorem — the corpus-wide entailment invariant holds. The 16 are:

- **6** from `counting_FP_implies_decision_P` (E1): decision ∈ {NPC, NPI-candidate, PH-complete,
  PSPACE-complete, beyond-PSPACE, coNP-complete} × counting=FP — an FP counting version would force decision
  into P, contradiction.
- **10** from `parallel_defined_only_within_P` (E2): decision ∈ {NPC, PH-complete, PSPACE-complete,
  beyond-PSPACE, coNP-complete} × parallelization ∈ {NC, P-complete} — parallelization is a within-P question.

**Gap list — 123 raw candidate cells** (empty, non-forbidden, in an examined 2-D marginal; each stated as a
falsifiable claim "a natural problem with charges (…) should exist; none is in the atlas"). This is the
falsifiable deliverable — but **123 is a raw enumeration, not 123 discoveries**, and the honest reading is its
composition:

| Bucket | Count | What it is |
|---|---|---|
| Object-mismatch-suspect | **67** | an *exotic* decision class (PSPACE-complete / beyond-PSPACE / PH-complete / coNP-complete) crossed with an optimization/ensemble charge (approximation, parameterized, landscape, average_case). These are near-`n.a.` by R1 object-type: a PSPACE-complete decision problem rarely has a natural constant-factor-optimization or random-ensemble version at all. Not empirical gaps. |
| Candidate genuine gap | **56** | everything else — the cells worth curating against |

Within the 56, two structural facts dominate (so even these are not 56 independent discoveries):

1. **The NPI-candidate row is nearly empty.** ~17 gaps are `decision=NPI-candidate × (something)`. Natural
   NP-intermediate *candidates* are rare (graph isomorphism, factoring, a handful more) and under-characterized
   on every other charge — so almost every NPI × X cell is empty. This is one interpretable fact about the
   literature, surfacing as many cells.
2. **The rigorous average-case ⟷ landscape frontier.** The 9 `average_case × landscape` gaps and several
   `decision=P × landscape` cells are the genuinely interesting residual: combinations like
   *hard-on-average-provable × clustering-proven* (a problem both provably hard-on-average **and** with a proven
   clustering transition) are real open cells — the sharpest "should an inhabitant exist?" questions the atlas
   raises.

The full 123-entry list (with per-cell marginal pair) is in
[`a3_structure.json`](../../eightfold/results/atlas/a3_structure.json) under `H3_forbidden_and_gaps.gap_list`.

---

## Ablations & robustness

- **`--drop-measured` (R9):** full-table dimensionality is **16 with and 16 without** the self-generated
  `measured`/`measured-scaling` cells. No structural claim rests on a value the project measured itself.
- **Leave-one-charge-out:** dimensionality stays ≥13 dropping any single charge (min 13, dropping
  `approximation`). H1 is not the artifact of one column.
- **Dual-missingness (R4):** H1 required agreement between the sentinel-inclusive and sentinel-free readings;
  both clear the bar. The sociology-of-study confound (axes driven by *which* problems were studied for *which*
  charges) is what the complete-case block controls for, and the verdict survives it.

---

## What it means — and the Move-Two prerequisites

**Is the multi-dimensionality deep, or is it the R1 type-of-object partition?** Honestly, **partly the
latter** — and this must be said plainly. The eight charges attach to eight *different formal objects* (R1):
decision measures a decision problem, counting the #-version, approximation the optimization version, landscape
a random ensemble. Objects that different *cannot* collapse onto one axis, so some of H1's dimensionality is
**definitional, not empirical** — it would appear in any faithfully-typed atlas regardless of whether hardness
"really" factors.

What is **not** definitional, and is the real Move-One yield:

- The **multiplet amplification** (permanent/determinant, VC/CLIQUE) is empirical — object-type alone does not
  predict that these specific pairs separate in these specific subspaces.
- The **approx⟷param residual** (0.69 bridge-free, the APX-complete×FPT cluster) is empirical — nothing forces
  those two charges to co-vary once the one known bridge is removed.
- The **gap list**, once triaged past the R1 object-mismatch bucket, is empirical — the NPI-row emptiness and
  the rigorous average-case/landscape frontier are facts about what the field has and has not characterized.

**Move-Two prerequisites** (carried into A4):

1. **Build the object-existence predicate.** The gap list's biggest weakness is that 67/123 cells are R1
   object-mismatch, triaged here by a hand rule ("exotic decision × opt/ensemble"). Move Two needs a
   first-class predicate — *does the optimization/ensemble version of this problem exist at all?* — so gaps
   auto-separate into "no such object" vs "object exists, uninhabited." That converts the gap list from a
   candidate pile into a ranked research agenda.
2. **Net the entailed component out of every association, not just approx⟷param.** R12 was honored for the
   headline pair; the same bridge-subtraction should run across the whole Cramér's V matrix so "surprising"
   is a computed residual everywhere, not a per-pair argument.
3. **The counting-folklore backfill.** The counting column is a measured frontier (49/86 applicable cells
   open) because per-problem #P-hardness is largely unpublished — the [A4 headline
   finding](counting-folklore-gap.md). Every counting-involving gap above inherits that sparsity; resolving
   the folklore gap would re-populate that slice of the atlas.

**Bottom line.** Move One's question was *is hardness a vector?* The atlas answers **yes** — decisively on the
qualitative claim, with the honest rider that part of the dimensionality is the R1 typing and the sharpest
empirical structure is the multiplet amplification, the approx/param cluster, and the triaged gap frontier.
The kill-gate did not fire; the map is real; the unasked questions are now enumerated.

---

## Provenance

- **Run:** `python -m eightfold.structure --a3` → `eightfold/results/atlas/a3_structure.json`; harness
  `eightfold/structure.py` (in-house MCA/Cramér's V/subspace clustering, numpy+scipy only).
- **Prereg:** `prereg_v5.json`, `committed_before_analysis: true` (counting→frontier tier amendment +
  R24 landscape evidence-grade split, both logged pre-analysis).
- **Data:** `atlas.jsonl`, 118 problems, validator-clean (exit 0), **zero `uncited-folklore`**, core per-charge
  A2 gate PASS (decision 97 / approximation 89 / parameterized 90).
- **Repo:** commit `e40ae78` (branch `cloudronin/charge-atlas-spec-review-55a58c`), 35 tests green.
- **Caveats index:** complete-case MCA is n=19 and coarse; family_separation is a coarse-label diagnostic;
  the gap-list object-mismatch triage is a hand rule pending the Move-Two object-existence predicate; the
  approx⟷param residual is bridge-subtracted only for the EPTAS↔FPT bridge.
