# Mosaic locality rubric (sealed with prereg_v10, 2026-07-24)

> **REVISION 1 — ATTEMPTED AND DISCARDED (2026-07-24).** After round-1's 5-class κ=0.521, the entangled/mixed
> boundary was sharpened from theory (total-vs-partial coupling + a "name the bounded channel" tiebreak) and
> the corpus recoded. The revision **regressed the instrument**: 3-class κ fell 0.646 → 0.523, the
> disagreement went diffuse (coder A over-routed to `mixed`, coder B's `uncodable` surged). Under
> prereg_v10-clarification-01 (κ measures resolution; sealed before the recode's number), round-1 was never
> NOT-QUALIFIED — it demonstrated **3-class resolution (κ=0.646)** on this original rubric. A revision that
> regresses a qualifying instrument is rejected, so the ORIGINAL criteria below are restored and govern the
> scored instrument. The revision and its recode are preserved (`-recode-r1`) and written up as a
> rubric-fragility finding, not merged. This is the instrument's rubric, at 3-class resolution.

The instrument. Coders classify each row's **structure** into one `locality_class`, from
`problem_id + problem_name + canonical_encoding` **only** — the eight charge columns and every per-charge
`canonical_task` are withheld (the per-charge task text states charge values verbatim, e.g. knapsack's
approximation task reads "MAX-KNAPSACK: FPTAS"; feeding it would build instance-9 circularity into the
instrument's own input). Every factual assertion below carries its source (instance-6/10 gate).

## Forbidden vocabulary (a coding that uses any of these is void)

The rubric classifies **structure**, never **algorithmic outcome**. These words and their synonyms are
banned from the coder's reasoning and must not appear in a coding rationale:
`PTAS / FPTAS / EPTAS / approximation scheme / APX / inapproximable / (1±ε) / FPT / W[1] / W[2] / kernel /
fixed-parameter / para-NP / NP-hard / #P / poly-time`. "Has a PTAS" is an *outcome*; "the objective sums
independent per-block contributions" is a *structure*. Only the latter is admissible. A rationale naming a
complexity class or an algorithm's existence is a rubric violation, scored as `uncodable` and flagged.

## The three structural axes the coder judges (definitional, from the encoding)

1. **Constraint binding** — do constraints couple solution elements *locally* (each constraint touches a
   bounded neighborhood, information does not have to traverse the whole instance) or *globally* (a
   constraint's satisfaction depends on far-apart elements)?
2. **Certificate boundedness** — can a yes-answer be certified by a *bounded-size local witness* (a small
   set of elements whose validity is checkable against a bounded neighborhood), or does the certificate
   require the whole configuration?
3. **Objective assembly** — is the objective a *sum/max of per-element or per-block terms* (separable), or
   does it *sum global interactions* (an entangled functional of the whole solution)?

## The five classes (structural criteria only)

- **`decomposable`** — the instance admits a *recursive/blockwise decomposition* under which the objective
  separates: solve blocks, combine by a bounded interface. Information about the optimum is *local to a
  block plus a bounded boundary*. Regime source: the one-decomposition mechanism (Baker's layerwise
  decomposition for planar problems, Baker, JACM 41 (1994); DP-over-a-linear-scaffold for scheduling/knapsack-
  shaped objects). *Anchor:* `planar-vertex-cover` (layerwise), and `knapsack` (1-D DP over capacity) —
  see the dissociation note below.
- **`local-covering`** — constraints are *local and coverage-shaped*: each element must be covered/hit by a
  bounded-degree constraint, certificates are per-constraint and bounded, but there is *no global
  decomposition* (the covering choices interact combinatorially). Regime source: the per-constraint-
  certificate mechanism. *Anchor:* `vertex-cover`, `max-2sat`.
- **`entangled`** — satisfying/optimizing requires *global agreement*: constraints couple far-apart
  elements, no bounded local witness certifies the optimum, the objective sums global interactions.
  Information about the optimum is *delocalized across the whole instance*. Regime source: the gadget-
  entanglement mechanism (label/agreement structure, dense global constraints). *Anchor:* `clique`,
  `independent-set`, `label-cover` (label-cover anchors on structure + its `decision`/`approximation`
  cells only — its `parameterized` cell is `open`, so the anchor never leans on a param value).
- **`mixed` / delocalized-covering** — *covering-shaped locally but delocalized globally*: bounded local
  constraints whose interaction has no bounded interface and no clean global agreement either — the
  structural signature the theory predicts on the gradient-bending rows.

> **3-class resolution (the instrument scored):** the instrument qualified at 3-class, where `entangled`
> and `mixed` collapse to **`delocalized`**. The two are distinguished only as diagnostic — the seam where
> blind coding strains, convergent with the two-property split — and are NOT separated in the scored
> analysis. The scored locality factor is `decomposable` / `local-covering` / `delocalized`.
- **`uncodable`** — the encoding does not determine the structure at this resolution, OR the coder could
  only reason via forbidden (outcome) vocabulary. A legal, informative outcome.

## `arity_class` (definitional, mechanical from the encoding where possible)

`bounded-local` (constraints of bounded arity over a bounded neighborhood) / `unbounded-fanin` (a
constraint may touch unboundedly many elements) / `global-objective` (the objective, not the constraints,
is the global object) / `n.a.` Spot-checked mechanical on 20 rows at I3; rows needing judgment are flagged.

## The dissociation note (sealed — knapsack and its kin)

`decomposable` and `local-covering` are **not** guarantees of joint tractability. `knapsack` is maximally
decomposable by structure (1-D DP is the FPTAS's own scaffold) yet its standard parameterization is hard —
locality feeds the two gradient charges through **two partially independent mechanisms**: *decomposition*
drives the approximation side (schemes), *certificate-boundedness* drives the parameterized side
(branching), and a row can carry one without the other. The coder still assigns the **structural** class
(`knapsack → decomposable`) — it must code by structure, not by coordinates. Rows where the two mechanisms
provably diverge form the **dissociation set** (prereg_v10 §dissociation); coding them by coordinates
rather than structure is the contamination the separability gate is built to catch.
