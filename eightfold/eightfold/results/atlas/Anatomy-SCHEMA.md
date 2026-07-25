# Anatomy — the Structure Atlas (sealed contract)

**Codename:** Anatomy. **Artifact:** `anatomy_v1.jsonl` (own sha256). **Module:** `eightfold/anatomy.py`.
**CLI:** `hardmap anatomy`. **Spec:** "Strata v2 — The Structure Atlas" (owner, 2026-07-24).
**This file seals the vocabularies, the typing rules, and the derivation rules BEFORE any derivation runs**
(S0), so the S2 pass is rule-based, not outcome-shopped. Amendments follow the prereg convention: a changed
rule is a new sealed version, never an in-place edit.

> **Naming disambiguation — read first.** The spec's codename was *"Strata v2"*, which **collides with a
> shipped layer**: `eightfold/strata.py` (artifact `atlas_v2.jsonl`, contract `Strata-SCHEMA.md`, whose §8
> already reads *"Strata v2 = this additive metadata layer"*). That layer is not a competitor — it is a
> **source** (its `objective` pin is the only real objective-type data in the repo) — but it *merges into
> the charge table*, which is the exact thing this project's founding law forbids. Reusing its name would
> brand the new law with the old design's violation. **Ruled (owner, 2026-07-24): codename Anatomy.**
> "Strata" continues to mean the charge-applicability layer, unchanged.

---

## §0. Why a separate artifact, and where the founding law's edges are

### 0.1 The founding law

> **Structure never enters the charge table, and no charge value ever informs a structure cell.**

The bridge between the two tables is the program's product; circularity is its one mortal enemy.

### 0.2 Why a separate file (the mechanical reason, stated correctly)

`atlas.entry_from_dict` builds `ChargeCell(**c)` / `ProblemEntry(**d)` by `**`-splat, so **any unknown key
raises `TypeError`**, surfaced by `load_atlas` as `ValueError`. That is the real, structural enforcement of
additive-only: a structure field cannot be added to a frozen row without breaking the loader.

> **Correction to an inherited claim (do not copy the old wording).** `strata.py:8-11` and
> `Quarry-SCHEMA.md:15-17` both state that `tests/test_loader.py`'s round-trip pins `atlas.jsonl`'s
> **bytes**. It does not. That test asserts `entry_to_dict(entry_from_dict(d)) == d` where `d` is already
> `asdict` output — i.e. **asdict-stability**, not file fidelity. Verified: `asdict(entry_from_dict(raw))`
> ≠ `raw`, because it emits `transition_known` and `worst_to_average_self_reduction` as `null` on all 944
> cells while only 13 and 5 carry them in the file. **Byte-identity is pinned by the explicit sha256
> assertions** (`freeze_atlas_v3.py:201`, `tests/test_atlas_v3.py:50-53`), not by the round-trip test.
> Anatomy pins its own bytes the same explicit way and makes no round-trip byte claim.

### 0.3 The circularity carve-out (the law's operational edges)

The law needs edges, because three columns brush against it. Each is legal for a stated reason, and each
carries a machine-readable marker so no downstream analysis can launder it.

1. **Task *text* vs charge *value*.** Reading a charge cell's `canonical_task` prose to identify **which
   object** a row is about is R1 typing, and is **legal**. Reading a charge cell's `value` to set a
   structure value is **contamination**, and is **forbidden**. The sealed `objective_type` lexicon
   (`Strata-SCHEMA.md` Cat-3) reads task prose only. Every column derived this way carries
   `provenance_status: derived:from-verified-field`, never plain `derived`.

2. **Charge-conditioned *coverage* is not a charge-informed *value*.** `kernel_status` exists only on rows
   whose `parameterized == FPT` (kernelization is an FPT-only notion). That is legal — but the conditioning
   **must be recorded on the column**, because a downstream analysis that reads the coverage pattern as a
   structural fact recovers Mosaic P6's "structurally blocked" result as if it were a finding. See §6, the
   coverage-conditioning register, which is **mandatory and machine-readable**.

3. **Pre-law leakage is consolidated read-only, not restated.** `worst_to_average_self_reduction` (R18) and
   `transition_known` (R17) are structure facts that already live *inside* the charge table, from before
   this law existed. Anatomy's `self_reducibility` column **consolidates them read-only and names them as a
   known pre-law exception**. It does not re-derive them, and it does not present them as new structure.

---

## §1. Vocabularies

### 1.1 Universes (the row-type discriminator)

| universe | rows | `row_key` | key fields |
|---|---|---|---|
| `natural` | the frozen charge atlas's problems | `problem_id` | `problem_id` |
| `boolean` | Boolean constraint-language symmetry classes, arity ≤4 | `b<arity>:<canonical-form>` | `arity`, `relation`, `class_size` |

**Column-level applicability.** Every column declares its universe **once, here in the schema** — not per
cell. A column has **no cell at all** outside its universe; absence is typed by the schema. This is
deliberate: the alternative (a cell per column per row) would emit ~4072 ceremonial `n.a.` cells for every
natural-only column and ~345 for every Boolean-only column, drowning the mandatory-reason rule in noise
until it meant nothing. **Within** a column's universe, a defined-but-inapplicable cell is `n.a.` **with a
mandatory reason**, and that rule bites for real.

### 1.2 Columns

| column | universe | provenance route | value vocabulary | bridge (Ledger §) |
|---|---|---|---|---|
| `locality_class` | natural | `coded` | decomposable · local-covering · delocalized · `n.a.` | — (instrument record *is* the provenance) |
| `arity_class` | natural | `derived:from-verified-field` | bounded-local · unbounded-fanin · global-objective · `n.a.` | — (definitional) |
| `encoding_type` | natural | `derived:from-verified-field` | graph · cnf-circuit · geometric · matrix-vector · string · numeric-set · other | — (definitional) |
| `objective_type` | natural | `derived:from-verified-field` / `judged` | Min-Ones · Max-Ones · Max-CSP · weighted · global-numeric · none | — |
| `kernel_status` | natural | `cited` (R20) | poly-kernel · no-poly-unless-coNP⊆NP/poly · FPT-no-poly-known · no-kernel-W[1]-hard · `open` · `n.a.` | §6 |
| `decomposition_facts` | natural | `cited` (R20) | structured record (see 1.4) · `open` · `n.a.` | §1, §2 |
| `reduction_out_degree` | natural | `derived:from-oracle` | non-negative integer · `open` | — |
| `self_reducibility` | natural | `cited` | worst-to-average · random-self-reducible · none · `open` · `n.a.` | §7 |
| `engine_type` | boolean | `derived:from-oracle` | both · bounded-width · few-subpowers · neither | §3 |
| `poly_fingerprint` | boolean | `derived:from-oracle` | 10-flag record (see 1.5) | §3 |
| `class_size` | boolean | `derived:from-oracle` | positive integer | — |

**Sociology sidecar** (`natural`, quarantined section — see §3.4): `source_funnel`, `rn_membership`,
`rn_route`, `admission_wave`, compendium memberships. All `derived:from-oracle`.

### 1.3 Provenance statuses

| status | meaning | required companions |
|---|---|---|
| `derived:from-oracle` | a mechanical predicate over **structured** data (flags, edge lists, counts) | — |
| `derived:from-verified-field` | a sealed rule over **agent-drafted prose** that passed the atlas's own verification passes (`canonical_task`, `canonical_encoding`) | — |
| `cited` | an R20 literature citation | `citation` non-empty |
| `coded` | a qualified blind-coding instrument | `instrument_ref` resolving in `anatomy-instruments.json` |
| `structural` | the cell is a sentinel (`n.a.` / `open`) | `reason` non-empty when value is `n.a.` |
| `judged` | owner assignment where a sealed rule could not resolve | `reason` non-empty |

> **Why `derived` is split.** A column derived from agent-drafted prose is **two provenance hops**, not
> one. That is legitimate — the prose survived the atlas's verification passes — but it is not the same
> object as a predicate evaluated on a relation, and the battery's refuse-`inferred` rule needs to tell
> them apart when someone later asks how hard a column can be leaned on. `inferred` remains **forbidden
> everywhere** in both atlases (instance-9's fix, now schema law).

### 1.4 `decomposition_facts` record

```jsonc
{ "treewidth_bounded_on": "planar | bounded-degree | interval | …" | null,
  "planar_restriction": true | false | null,
  "minor_excluded": "K5 | K33 | apex | …" | null,
  "geometric_embedding": "unit-disk | rectangle | …" | null,
  "citation": "…", "note": "…" }
```
Any field with no R20 warrant is `null`; a record with all-null fields is the value `open`, never a
half-filled record. **Never inferred from "looks planar."**

### 1.5 `poly_fingerprint` record

The ten persisted Post's-lattice flags, verbatim and in this order:
`0valid, 1valid, horn, dualhorn, bijunctive, affine, width2affine, strongly0valid, IHSB, general_wsep`.

---

## §2. Derivation rules (SEALED — applied verbatim in S2)

### 2.1 `engine_type` (boolean)

```
bounded_width  := prism.bounded_width(flags) == "bounded-width"
                  # the CORRECTED I3 predicate: 0valid | 1valid | horn | dualhorn | bijunctive
                  # (trivial-satisfiability FIRST, then the semilattice/majority polymorphisms)
few_subpowers  := flags["affine"]
                  # on the Boolean domain: few subpowers <=> Maltsev term <=> affine
engine_type    := both | bounded-width | few-subpowers | neither
```
**Binding constraints.** (a) Use `foundry/foundry/prism.py:66` **only**; the variants at
`foundry/foundry/finer.py:52` and `foundry/foundry/r25.py` are the *naive* predicate and miss the
0/1-valid rescue — reusing them would manufacture spurious variation among 0/1-valid relations.
(b) Ledger §1 requires the bounded/unbounded-width distinction be carried explicitly or the
tw→parallelization cell mis-nets; `engine_type` is that carrier. (c) **Arity ≤4 is mandatory**: at
arity ≤3 the affine obstruction is vacuous, `engine_type` is constant, and Prism's predictions 3b/4 were
declared UNTESTABLE for exactly this reason. Variation exists only at arity 4.
(d) **Reconciliation gate (S3):** derived marginals must reconcile with the persisted
`marginals.localization` = `{bounded-width: 3178, unbounded-width: 894}` and with
`pred2_bounded_width_marginal_descriptive.purely_affine_unbounded_classes_total: 4`.

### 2.2 `arity_class` (natural)

Derived mechanically from the pinned task/encoding text into
`bounded-local | unbounded-fanin | global-objective | n.a.`, then **cross-checked against the two blind
coders' existing 345×2 `arity_class` codings** (`mosaic-coding-A/B.jsonl`), with agreement reported as an
instrument-grade validation signal.

> **Ruled (owner, 2026-07-24):** the cross-check is a *validation signal*, not a tiebreak. Where the
> mechanical derivation disagrees with **both** coders, that is a **task-text ambiguity worth a typing
> note** — recorded, not resolved by a third pass. No new judging is performed.

### 2.3 `objective_type` (natural)

Inherit the 118 sealed `atlas_v2` strata pins verbatim with their existing `derived`/`judged` provenance,
then extend to v3-new rows by the **sealed Cat-3 lexicon** (`Strata-SCHEMA.md` §4 Cat-3) applied to the
full `canonical_task` text. Anything the lexicon does not resolve is **flagged, never defaulted** — it is
`open`, or `judged` if the owner assigns it. `weighted` is checked **last** and narrowed to
KNAPSACK/SUBSET-SUM: a recognised numeric objective wins (number-partitioning minimises a derived numeric
imbalance → `global-numeric`, not `weighted`).

### 2.4 `encoding_type` (natural)

Keyword rule over `canonical_encoding`, evaluated in this fixed order (first match wins):
`cnf-circuit` → `graph` → `geometric` → `matrix-vector` → `string` → `numeric-set` → `other`.
The order is sealed here because it is outcome-relevant: several rows match more than one pattern.

### 2.5 `reduction_out_degree` (natural)

From `reductions-network-edges.json` at pinned commit `8089fb4f`, using the artifact's **own
`counting_rule` field** (already fixed in the artifact — the spec's I5 counting-rule item is pre-answered).
Coverage is **31 problems**, not the spec's ~48; 48 is rn's *total atlas-row membership*, a different
quantity. Rows outside the 31 are `open`, never 0 — **absence of an edge record is not an out-degree of
zero.**

### 2.6 Consolidated columns (`locality_class`, `kernel_status`, `self_reducibility`)

Moved verbatim from their source sidecars. **No value may change in transit** (kill 1). Each cell records
its `source_artifact`.

---

## §3. Build discipline

### 3.1 Kill 1 — transit integrity (S1)

Any consolidation diff showing a value changed from its source sidecar **halts the milestone**.
Consolidation moves cells; it never edits them. An edit is an **errata event on the source**, handled on
that source's own track.

### 3.2 Kill 2 — coverage floor (S2)

If `decomposition_facts` is citable for **< 40% of grid-relevant rows**, the column ships at whatever
coverage exists **with the gap stated** — never padded, never inferred.

**Pinned at S0 so the denominator cannot move after the result** (I2 census):
- grid-relevant population (both-real **and** locality-codable) = **111 rows**
- decomposition-**eligible** (encoding is graph or geometric) = **77/111 = 69%** — the hard ceiling
- therefore kill 2 requires a citable fact on **≥ 58% of eligible rows** (40/69)

### 3.3 Variance census (S3) — mandatory before freeze

One groupby per objective-keyed column, asking whether the value **actually varies** across objectives
within the rows it is keyed on, with the marginal **stated either way**. Instance-16's lesson at the
artifact layer: a column that *cannot* vary on its keyed population is discovered at **build**, with a
number beside it, not at G1 when a grid bet lands on it. For v1 this is near-trivial — Boolean rows' approx
values are known to vary; natural rows are degenerate single-objective by design and the census records
exactly that — which is precisely why it is cheap to institutionalize now.

### 3.4 Sociology quarantine

The sociology sidecar exists **solely** so bridge regressions can control for canon-proximity — the
covariate that lets the B1 arc (0.73 → 0.10) be decomposed into structural vs curatorial parts by testing
whether anatomy predicts charges *beyond fame*.

> **Law: a sociology column never enters a structural claim.** It may appear only as a control term. Any
> analysis reporting a sociology column as a structural finding is in violation.

**`first_classification_year` is CUT** (owner ruling, 2026-07-24): funnel provenance and compendium
membership carry the canon-proximity control adequately; year would be `cited`-at-best with fuzzy semantics
(classified *as what*, by whose first?) at real per-row research cost, and its marginal control value over
compendium membership is speculative. It earns a scoped follow-up only if a bridge regression shows the
fame covariates matter and year would sharpen them.

### 3.5 No value changes; frozen bytes untouched

`atlas.jsonl` (`6d53a4f1`), `atlas_v2.jsonl` (`784f4739`), `atlas_v3.jsonl` (`e62f3c28`) and every source
sidecar stay byte-identical. Anatomy reads them; it never writes them.

### 3.6 Bridge citations are pin-gated

A column may carry a `bridge_citation` **only if that Ledger row reads `PINNED`** in
`docs/findings/bridge-ledger-v1.md` §9. An `UNPINNED` row may not net anything, may not serve as a
known-answer calibration value, and the column citing it falls back to `open` rather than borrowing an
unverified warrant. This is the Ledger's own pin-before-net house rule, made mechanical.

---

## §4. Reserved names (not shipped in v1)

Named and typed here so a later fill is **purely additive** — no schema version bump, no re-freeze of
meaning.

| reserved column | universe | intended route | bridge | why not now |
|---|---|---|---|---|
| `channelness` | natural + objective-keyed | coded (new instrument) | — | unmeasured hypothesis; explicitly deferred to Mosaic v3 G0 (`prereg_v13`) |
| `fo_form` (X-positive / X-negative Gaifman-coverable) | natural | cited/derived | §4 | no data exists; requires new judging, barred by spec §3 |
| `tuple_density` | boolean | `derived:from-oracle` | — | trivially derivable later; reserved with the rest per owner ruling |
| **row-relations layer** (`dual_of`, `complement_of`, `restriction_of`, `objective_variant_of`) | natural | derived edges + cited edges | — | each edge **is a claim carrying a warrant** — R20 work at scale, which does not fit the v1 box. **v1.1's headline.** |

---

## §5. Owner rulings (dated 2026-07-24, sealed before derivation)

1. **Codename Anatomy** — the Strata collision is not cosmetic; the existing layer merges into the charge
   table, the opposite of the founding law.
2. **One artifact, two sections** — with column-level universe typing (§1.1) as the fix for the n.a.
   explosion a single artifact would otherwise produce.
3. **Boolean roster at arity ≤4 (4072 classes)** — the only depth at which `engine_type` varies, hence the
   only depth at which Ledger §3's engine→approx / engine→param bets are posable.
4. **Absent columns reserved in schema, not shipped as data** (§4).
5. **`arity_class`: mechanical derivation primary; coder codings as cross-check, not tiebreak** (§2.2).
6. **`first_classification_year` cut** (§3.4).
7. **Variance census institutionalized at S3** (§3.3).

---

## §6. Coverage-conditioning register (mandatory, machine-readable)

A column whose **coverage** is conditioned on something other than the column's own definition must
declare it here, and the declaration ships in the artifact. This exists because a coverage pattern read as
a structural fact is a real and already-realized failure mode (Mosaic P6).

| column | coverage conditioned on | consequence a consumer must respect |
|---|---|---|
| `kernel_status` | `parameterized == FPT` (kernelization is FPT-only) | The rows that *have* a kernel status all have `parameterized` constant. A kernel↔param association is **structurally blocked**, not merely unmeasured. Only the poly- vs no-poly residual **within** FPT is informative. |
| `decomposition_facts` | `encoding_type ∈ {graph, geometric}` — and that eligibility is **itself stratified by locality**: decomposable 52%, local-covering 62%, delocalized 81% (grid-relevant population, n=111) | Coverage is **not missing-at-random with respect to locality**. Any association between `decomposition_facts` and a locality-conditioned quantity must be reported against this gradient, or a coverage artifact will be read as structure. |
| `reduction_out_degree` | membership in the pinned reductions.network snapshot (31 of 345) | Absent ≠ zero. Non-members are `open`. |
| `objective_type` | 118 rows inherit sealed v2 pins; v3-new rows derive from the Cat-3 lexicon | Two provenance regimes in one column; consumers stratifying on it should check `provenance_status`. |

---

## §7. Typing edge cases (I4) — resolved with counts, sealed before derivation

**7.1 `objective_type = none` is a REAL value, not a sentinel — and it is the plurality.**
137 of 345 rows carry `approximation = n.a.`, i.e. no objective function exists (decision-only and
structural rows). Per the Cat-3 rule those take `objective_type = none`, which asserts *the object does not
exist* — a positive typing claim, distinct from `open` (exists, unknown) and requiring no reason. The
`objective_cells` sub-section is **absent** on these rows, not empty-with-placeholders.

Applicability cross-tab over the 345 (sealed here so later coverage talk has a fixed denominator):

| | `parameterized` real | `parameterized` n.a. |
|---|---|---|
| **`approximation` real** | 175 | 33 |
| **`approximation` n.a.** | 29 | 108 |

**7.2 Promise / gap-shaped rows — anatomy follows the pinned task, never the name.**
Seven rows carry promise/gap language in their task text: `graph-3-coloring`, `max-2lin`,
`lex-first-maximal-independent-set`, `generalized-subset-sum`, `3-coloring-extension`,
`min-degree-spanning-tree`, `minimum-test-cover`. These are exactly where **object-drift** (methods-thread
instances 9 and 17) has bitten twice: the id names one object and the pinned task defines another. **Rule:
every structure cell on these rows is typed from `canonical_task`/`canonical_encoding`, and where the task
pins a promise/gap version the cell records that in its `reason`.** `graph-3-coloring` is the standing
exemplar and is treated as a typing test case, not a routine row.

**7.3 `engine_type` on natural rows — no cell exists, by construction.**
The column is `boolean`-universe only (§1.1), so a natural row has **no `engine_type` cell at all** — not
an `n.a.` cell. This is the whole point of column-level typing: the 26 `sat-csp`-family rows are *not*
partial credit toward an engine column, because a problem family is not a constraint language.

The id-level overlap with `postlattice.REGISTRATION_ANCHORS` is a **cross-link, not a column**:

| co-clone | atlas `problem_id` | present |
|---|---|---|
| `xor-sat`, `horn-sat`, `nae-sat`, `one-in-three-sat` | same | yes (exact) |
| `2-sat`, `3-sat` | `sat-2`, `sat-3` | yes (via alias) |
| `dual-horn` | — | **no atlas row** |

Six anchors, one co-clone with no natural counterpart. They are recorded in the artifact as a registration
cross-link so the two universes can be *joined* at known points without either column leaking into the
other's universe.
