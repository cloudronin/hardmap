# Strata — Eightfold v2 additive metadata layer (sealed contract)

**Codename:** Strata. **Artifact:** `atlas_v2.jsonl` (own sha256). **Module:** `eightfold/strata.py`.
**This file seals the vocabularies, the level table, and the derivation rules BEFORE any derivation runs** (S1),
so the S2 pass is rule-based, not outcome-shopped. Amendments follow the prereg convention (a changed rule is a new
sealed version, never an in-place edit).

> **"v2" disambiguation.** *Strata v2* = this additive metadata layer. It is a **distinct axis** from the queued
> *charge-9 v2* (fine-grained complexity: SETH/3SUM/APSP). The two must never be conflated.

## 0. Why additive-only is structural, not a discipline choice — the frozen atlas defends itself

`tests/test_loader.py` pins `entry_to_dict(entry_from_dict(d)) == d`. Any field added to a v1 `ChargeCell` or
`ProblemEntry` would make `asdict` emit it, change `atlas.jsonl`'s bytes, and fail the suite. So "additive only" is
**enforced by the test suite**: the separate-layer design (import the kernel read-only, operate on raw dicts,
compose over `atlas.validate`) is the *only* design that can satisfy the spec. Strata makes **zero** edits to
`atlas.py`/`charges.py`; it is the `foundry/substrate.py` precedent, one axis over.

## 1. The three additions + their vocabularies

### 3.1 Charge levels — `CHARGE_LEVELS` (per charge, one table)
The object each charge attaches to (must stay consistent with `SCHEMA.md` §3.2 "Canonical object (R1)"):

| Charge | Level | Requires |
|---|---|---|
| decision | decision | the problem |
| counting | counting | the #-version |
| parallelization | decision | the problem (within P) |
| proof_size | refutation | an unsat instance family |
| **approximation** | **objective** | an objective function |
| **parameterized** | **objective** | an objective + a parameterization |
| average_case | ensemble | a random instance distribution |
| landscape | ensemble | ensemble + samplable solutions |

**Sealed finding:** the two `objective`-level charges (approximation, parameterized) are **exactly** the coupled
pair; every other level holds multiple charges with no strong coupling among them.
**Mechanical consequence:** `cross_level_flag(predictor_level, charge)` flags a level-X predictor aimed at a
level-Y charge as suspect *before anything runs* (would have caught tuple-dispersion-vs-approximation three sprints
early).

### 3.2 Charge applicability — per cell, mandatory reason + `derived`/`judged` provenance
Vocab: `defined-informative` (exists + non-degenerate; the only cells carrying analytical weight) · `defined-trivial`
(defined but degenerate, e.g. 0-valid Max-CSP trivially approximable because the *objective* degenerates) ·
`ambiguous` (defined but perspective-dependent with competing natural answers) · `n.a.` (the object does not exist).
**Gate (S1 done-gate):** an applicability value REQUIRES a non-empty `applicability_reason` and a `derived`/`judged`
`applicability_provenance`.

### 3.3 Objective + parameterization pinning — per row
`objective ∈ {Min-Ones, Max-Ones, Max-CSP, weighted, global-numeric, none}`;
`parameterization ∈ {solution size, treewidth, other, none}`; plus `pin_theorem` (the covering dichotomy where one
exists) and a `derived`/`judged` `pin_provenance` on any real (non-`none`) pin.

## 2. Derivation rules (SEALED — applied verbatim in S2; the `judged` set is the S3 owner-review list)

### Applicability (3.2)
1. sentinel `n.a.` (status `structural`) → **`n.a.` [derived]**; reason = the templated `canonical_task` "why"
   ("not an optimization problem", "decision in P", "NPC ⇒ within-P n.a.").
2. real value, non-degenerate, single natural framing → **`defined-informative` [derived]**.
3. degeneracy signal (objective degenerates: "trivially approximable", 0-/1-valid Max-CSP) →
   **`defined-trivial` [judged]**.
4. competing natural framings (`perspective` names an alternative; graph problems with treewidth *vs* solution-size)
   → **`ambiguous` [judged]**.
5. **(R-1, the rule most prone to misfire)** `open`/`unmeasured` → **`judged` by DEFAULT**. It is `defined-informative`
   **[derived]** ONLY when a *sibling cell in the same row* already establishes the object exists (e.g. approximation
   is populated ⇒ the optimization version demonstrably exists). **No cell is `derived` on the strength of a word
   like "plainly."** Anything without a sibling witness goes to the review list — a longer review list beats a
   category assigned by adjective.
   **Witness map** (the operationalization of "establishes the object", faithful to the rule — NOT merely same-level,
   which would over-judge `counting`): `counting` ← `decision` real (the #-version is well-defined once the decision
   problem is — that is counting's own definition); `parallelization` ← `decision` real (an `open` cell already
   implies decision∈P by E2); `approximation` ↔ `parameterized` (the objective pair, R-1's own example); `landscape`
   ← `average_case` real (the ensemble exists; samplability is the residual). `average_case` and `proof_size` have
   **no** structural sibling → they stay `judged`.

### Objective + parameterization (3.3)
- **objective** from the approximation `canonical_task` prefix: `MAX-<CSP>` (MAX-SAT/3SAT/2SAT/Horn/3-LIN)→`Max-CSP`;
  `MIN-<size>` (MIN-VC)→`Min-Ones`; `MAX-<set>` (MAX-CLIQUE/MAX-IS)→`Max-Ones`; TSP/chromatic→`global-numeric`;
  approximation `n.a.`→`none`. weighted variants or unclear → **[judged]**.
- **parameterization** from the `parameterized` cell's `perspective`: "solution size k"→`solution size`;
  "treewidth"→`treewidth`; named others ("bounded degree (Luks)", "#terminals", "above-guarantee")→`other`;
  `n.a.`→`none`; competing → **[judged]**. `pin_theorem` from provenance where a dichotomy pins it (Bulatov–Marx
  solution-size, Downey–Fellows) — the G1 codeword lesson: a parameterization outside the pinned dichotomies cannot
  carry a parameterized claim.

## 3. Build discipline (bind S2–S4)

- **(R-2) The derived/judged split is an S2 headline number.** A *low* judged fraction (<~10%) is a **RED FLAG**,
  not a success: `canonical_task` prose was written per-cell over months with no schema in mind, so the judged
  fraction is expected *higher* than the mechanical rules imply. A low number means the pass pattern-matched prose
  instead of reading it — re-examine, do not celebrate efficiency.
- **(R-3) The coverage report (S4) is a three-level drill-down, not a top number.** Report the *sequence*: 118 rows
  → both approximation & parameterized `defined-informative` → of those, how many carry a defensible local relation
  (Ferry's 16), each drop-off with its reasons. The shrinkage sequence is the structural fact (where hardness can be
  studied at all); a single count is a coverage statistic.
- **No value changes.** A v1 *value* that looks wrong is a **v2.1 candidate** (logged in
  `results/atlas/strata_v2_1_candidates.json`, prereg-amendment style), never fixed in place. A correction touching
  ONLY new metadata is applied and `atlas_v2.jsonl` re-hashed.
- **Every new field carries provenance** (`derived` from existing text vs `judged` by the owner), so the metadata
  layer is auditable to the same standard as the values.
- **Scope resistance:** no charge 9, no roster expansion, no cell fixes. Aggregation, not accumulation.
