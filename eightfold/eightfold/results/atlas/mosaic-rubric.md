# Mosaic locality rubric (sealed with prereg_v10, 2026-07-24)

> **REVISION 1 — 2026-07-24 (the one permitted revision; prereg_v10 kill_criteria.instrument_L1).** Round-1
> coding qualified on the anchors (7/7, both coders) and passed the separability gate clean, but κ=0.521 <
> 0.6: the coders parted on the `entangled`/`mixed` boundary, with one coder systematically over-assigning
> `entangled`. This revision sharpens ONLY that boundary, and it is written from the THEORY side — the
> total-vs-partial-coupling criterion below — illustrated exclusively with the sealed anchor/dissociation
> rows. It was NOT written by inspecting the round-1 disagreement rows (tuning the rubric on its own test
> set is forbidden). All other class definitions stand verbatim. A second κ miss on the recode banks NOT
> QUALIFIED per the seal — no third attempt.

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
- **`entangled`** — global coupling is **TOTAL**: **every** solution element constrains **every** other,
  and the coupling does **not** factor through any bounded channel. The constraint graph on solution
  elements has no bounded separator — there is no small interface whose fixing decouples the two sides.
  A yes-answer requires simultaneous global agreement; no bounded local witness certifies the optimum.
  *Anchor:* `clique` (every pair of chosen vertices must be mutually adjacent — literally all-to-all),
  `independent-set` (its complement — every pair mutually non-adjacent), `label-cover` (a single global
  labeling must be consistent across the whole instance at once). (`label-cover` anchors on structure +
  its `decision`/`approximation` cells only — its `parameterized` cell is `open`.)
- **`mixed` / delocalized-covering** — global coupling is **PARTIAL / CHANNELED**: constraints are
  locally bounded (as in `local-covering`) and the instance is globally connected, BUT the coupling
  **factors through bounded interfaces** — there exist bounded separators / channels through which
  far-apart elements interact, rather than all-to-all. Locally covering, globally connected, but not
  totally entangled. *There is no anchor for `mixed` by design* — it is the intermediate class, pinned by
  CONTRAST: more coupled than `local-covering` (`vertex-cover`, whose certificate is per-edge and the
  covering choices interact only through shared vertices) yet less than `entangled` (`clique`, all-to-all).
- **THE OPERATIONAL TEST (entangled vs mixed), applied per row:** *Does every solution element constrain
  every other (→ `entangled`), or only through a bounded channel / a nameable bounded interface (→
  `mixed`)?* **Tiebreak (calibration):** `entangled` is the STRONGEST structural claim — reserve it for
  demonstrably TOTAL coupling. When you are unsure between `entangled` and `mixed`, ask "can I NAME the
  bounded channel the coupling passes through?" If yes → `mixed`. Only assign `entangled` when no such
  channel exists. (This tiebreak exists because `entangled` is the easy over-assignment; the default under
  genuine uncertainty at this boundary is `mixed`, not `entangled`.)
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
