# Charge Atlas — Schema

Per [the spec](../../../docs/specs/eightfold-v1-charge-atlas-spec.md) (§3.2–§3.4; Build addenda R1–R9). The
atlas lives as a single JSONL file at [`atlas.jsonl`](atlas.jsonl), one problem per line (line-diffable). The
schema is implemented as dataclasses in [`eightfold/atlas.py`](../../atlas.py) and the charge vocabularies +
entailment layer in [`eightfold/charges.py`](../../charges.py); the validator enforces the QC gates below plus
corpus-wide invariants.

## ProblemEntry (top-level, one per line)

| Field | Type | Notes |
|---|---|---|
| `problem_id` | string | Immutable lowercase slug (no spaces), unique across the atlas. |
| `problem_name` | string | Human-readable name, incl. the task sense (e.g. "Vertex Cover (decision)"). |
| `problem_family` | string | One of `PROBLEM_FAMILIES` — coarse traceability only. **Not** an analysis input: families should *emerge* as multiplets (H2), not be imposed. |
| `canonical_encoding` | string | The fixed encoding (I3). Deviations are logged per-cell in `provenance.note`. |
| `charges` | list[ChargeCell] | Exactly one cell per charge; `charge` names must match `CHARGES`. |
| `last_reviewed` | string | ISO date `YYYY-MM-DD`. |
| `reviewer` | string | Who curated. |
| `notes` | string \| null | Optional free text. |

## ChargeCell (per charge, nested in `charges`)

| Field | Type | Notes |
|---|---|---|
| `charge` | string | One of the eight `CHARGES`. |
| `value` | string | A real value from that charge's vocabulary, **or** a sentinel `open`/`unmeasured`/`n.a.` (R2). |
| `canonical_task` | string | **R1** — the formal object this charge measures for this problem (e.g. counting → "#VC: count vertex covers of size ≤ k"). For an `n.a.` cell, states why the charge does not apply. |
| `status` | string | Evidential status (real value) or `structural` (sentinel). See the ladder below. |
| `provenance` | dict | Citation dict; required for a real value unless flagged `uncited-folklore` (gate 3). For `measured*`, must carry an `experiment` sub-object (R9). A `url` citation must also carry `snapshot` + `retrieved` (R10). |
| `perspective` | string \| null | Required for `proof_size` (proof system) and `parameterized` (parameter) real values (gate 5). |
| `contested_note` | string \| null | If sources disagree; both sides must be in `provenance` (never silently averaged). |
| `transition_known` | bool \| null | **R17** — `average_case` only: is a phase transition known for the ensemble? Kept separate from `value` (which is algorithmic difficulty). If `true`, requires a citation. Absent/`null` elsewhere. |
| `worst_to_average_self_reduction` | bool \| null | **R18** — `average_case` only: is there a *same-problem* worst-case→average self-reduction (permanent, discrete-log)? A relation, kept out of `value`. If `true`, requires a citation. Absent/`null` elsewhere. |

## The eight charges & their real-value vocabularies (§3.2)

Each charge attaches to a **different formal object** (R1); the cell's `canonical_task` pins which.

| # | Charge | Canonical object (R1) | Real values |
|---|---|---|---|
| 1 | `decision` | the worst-case decision problem | `P` · `NPI-candidate` · `NPC` · `coNP-complete` · `PH-complete` (level in `perspective`) · `PSPACE-complete` · `beyond-PSPACE` (R22). **Partial order, not linear:** NPC and coNP-complete are *siblings* (NP vs coNP is open); `DECISION_PARTIAL_ORDER` records proven containments only. |
| 2 | `counting` | the #-version (count the decision witnesses) | `FP` · `#P-complete` |
| 3 | `approximation` | the optimization version (**absolute ratio**, R19) | `FPTAS` · `EPTAS` · `PTAS` · `APX` (constant-factor membership) · `APX-complete` (+ APX-hard) · `log-APX` · `poly-APX` · `inapprox` |
| 4 | `parameterized` | decision + a fixed parameter (`perspective`) | `FPT` · `W[1]` · `W[2]+` · `XP` · `para-NP-hard` |
| 5 | `parallelization` | the within-P question (needs decision ∈ P) | `NC` · `P-complete` |
| 6 | `proof_size` | an unsatisfiable instance family, in a system (`perspective`) | `poly` · `exp` |
| 7 | `average_case` | a random ensemble (density/model pinned in `canonical_task`) | **algorithmic difficulty only (R17):** `easy-on-average` · `hard-on-average-crypto` · `hard-on-average-provable` (R18) · `hard-on-average-conjectured`. The ensemble "a transition is known" fact and the worst-case→average self-reduction are separate sub-fields (`transition_known`, `worst_to_average_self_reduction`), not values. |
| 8 | `landscape` | a random ensemble's solution-space geometry | `clustering-OGP-known` · `clustering-OGP-refuted` · `freezing-measured` (R14) |

**Sentinels (R2), allowed for every charge:** `open` (applies, value unknown) · `unmeasured` (applies, nobody
has measured) · `n.a.` (charge structurally does not apply). Unknown ≠ zero; sentinels are never imputed. A
sentinel cell carries `status = "structural"`. **The `n.a.`/`open` boundary (R15):** use `n.a.` **only** when
the charge's object cannot be constructed (no optimization version, no unsat family); if a random ensemble
could be defined, the cell is `open` even if unstudied — never `n.a.`.

## Status ladder (evidential)

- `confirmed` — primary source read; **owner-promoted** at review (gate 4: `primary_source: true` + a citation
  key). Never set by the agent.
- `claimed` — real citation, not independently confirmed. **The agent default.**
- `uncited-folklore` — asserted without a resolvable citation. A **debt**, not a value: resolve to a citation
  or revert the cell to `open`. The A1 gate requires **zero** of these.
- `measured` / `measured-scaling` — **R9**: a self-generated empirical value. `measured` only on charges 7/8;
  `measured-scaling` only on charge 6; validator-rejected on charges 1–5. Requires
  `provenance.experiment = {prereg, manifest, seeds, code_commit}` (Census standard). v1 fills these only from
  already-banked experiments.
- `structural` — the status of a sentinel-valued cell.

## The QC gates (enforced by `atlas.py::validate`)

1. **Vocab** — `charge ∈ CHARGES`; `value ∈ allowed_values(charge)`; status coherent with value type
   (sentinel ⇒ `structural`; real ⇒ an evidential status).
2. **Canonical task (R1)** — `canonical_task` non-empty on every cell.
3. **Citation-or-flag** — a real value carries a citation key, or `status = uncited-folklore`.
4. **Confirmed** — `confirmed` requires `provenance.primary_source = true` **and** a citation key.
5. **Perspective (R1/§3.2)** — `proof_size` / `parameterized` real values carry a `perspective`.
6. **Measured quarantine (R9)** — `measured` only on charges 7/8, `measured-scaling` only on 6; both require a
   full `provenance.experiment`.
7. **Shape** — exactly one cell per charge (names match `CHARGES`); slug/family/encoding/date/reviewer
   well-formed.
8. **Source snapshot (R10)** — any provenance carrying a `url` also carries a `snapshot` (Wayback capture or a
   local copy under `docs/sources/`) and a `retrieved` ISO date. Persistent identifiers (DOI, book + page)
   need no snapshot.

**Corpus-wide invariants:** unique `problem_id`; every entry's real charge values obey the entailment layer
(a theorem-forbidden combination in the *data* is a bug — fix or document); the entailment layer itself passes
its R6 consistency check (`__entailment__`).

## Coverage accounting (R2) & the A1 gate

Coverage is measured over **applicable** cells (`value ≠ n.a.`): `coverage = cited-filled / applicable`, where
*cited-filled* = a real value with status `claimed`/`confirmed`/`measured*` (not a sentinel, not folklore).
An `n.a.` cell is correctly filled, not missing. **A1 done-gate:** `coverage ≥ 70%` **and** zero
`uncited-folklore`.

## Entailment layer (R5/R6)

`charges.py::ENTAILMENT_LAYER` holds known theorems linking charge values, each with a mandatory
`preconditions` field and citation (R6). Column-expressible rules (`forbids` set) drive occupancy triage —
separating theorem-forbidden empty cells from genuine gaps; informational rules (e.g. the FPTAS rule, whose
hypothesis "strongly NP-hard with a poly-bounded objective" is not one of our columns) are kept for the record
and to document why preconditions are load-bearing. `validate_entailment_layer()` rejects any rule missing
preconditions/citation or naming an out-of-vocab value.

## CLI

```bash
python -m eightfold.atlas validate [--path atlas.jsonl]   # gates + invariants + entailment check; nonzero on any violation
python -m eightfold.atlas summary  [--path atlas.jsonl]   # per-charge / per-family coverage + A1 gate
```
