# Quarry — Atlas v3 broad-expansion (sealed contract)

**Codename:** Quarry / Atlas v3. **Artifact:** `atlas_v3.jsonl` (own sha256, frozen at V3). **Builder:**
`eightfold/dev/build_atlas_v3.py`. **Sidecar:** `atlas_v3_provenance.jsonl`. **This file seals the
admission standard, the provenance vocabulary, the QC tiers, and the wave plan BEFORE any v3 cell is
drafted** (sealed-before-measured). Amendments follow the prereg convention (a changed rule is a new
sealed version, never an in-place edit). The sealed delta bets live in `results/prereg/prereg_v9.json`.

> **Broad expansion (owner ruling).** Every admissible row is ingested across ALL columns from all six
> sources plus the un-mined remainders; 300–450 rows is an *outcome, not a target*. K4's column cost
> model survives only as sequencing + QC intensity, never as a scope cap.

## 0. Why provenance is a sidecar, not a schema field — the frozen atlas defends itself

`tests/test_loader.py` pins `entry_to_dict(entry_from_dict(d)) == d`, and `entry_to_dict` is `asdict`.
Any field added to `ProblemEntry`/`ChargeCell` would make `asdict` emit it, change `atlas.jsonl`'s
bytes, and fail the suite (the Strata precedent, §0 of Strata-SCHEMA.md). So the v3 per-row provenance
(source funnel, admission wave, Quarry membership) and the `single_charge` flag live in a **separate
sidecar keyed by `problem_id`**, never in the row. **The frozen `atlas_v3.jsonl` is plain `ProblemEntry`
rows** — loadable by `atlas.load_atlas(path)` and clean under `atlas.validate_corpus` unchanged.

## 1. Admission standard (spec §2 — unchanged law, applied broadly)

A row enters v3 iff ALL hold:

1. **Natural problem, one pinned canonical encoding** (I3 discipline); deviations logged in cell
   `provenance.note`.
2. **Distinct from every existing row under S2** (complementation / trivial re-encoding merge;
   restrictions and different constraint languages stay separate; a `#X`/`MAX-X` of an existing row is
   that row's counting/approximation *cell*, not a new row).
3. **≥1 charge citable at R20 standard** — every cited cell passes the 9-check protocol
   (`CORPUS_PR_REVIEW_GUIDE.md`); **counting held to the per-problem F-1 bar**. (This is the broad-scope
   relaxation from Quarry's ≥2; single-charge rows are admitted.)
4. **R1 typing clean** — each of the 8 charge cells present (Gate 7); each is a real value or a sentinel
   with a mandatory reason (R2). "Single-charge" = 1 citable + 7 typed sentinels, **not** a short row.
5. **Currency** — any value sourced through a pre-2005 compendium (Crescenzi–Kann) re-verified vs
   post-2000 literature before it is trusted.

**Zero uncited-folklore, always** — a cell that cannot be established is `open` + note, never guessed.
All drafted cells enter at `status="claimed"`; only the owner promotes to `confirmed` (Gate 4).

## 2. The provenance sidecar — `atlas_v3_provenance.jsonl`

One JSON object per admitted v3 row, keyed by `problem_id`:

| Field | Type | Vocabulary / source |
|---|---|---|
| `problem_id` | str | matches the `atlas_v3.jsonl` row |
| `source_funnel` | str | ∈ `{rn, ck, ghr, df, dh, su}` (the six sources; multi-source rows list the primary + `also`) |
| `admission_wave` | str | ∈ `{W1, W2, W3, W4}` (see §4) |
| `quarry_member` | bool | true iff present in `quarry-candidates-full.jsonl` (vs a remainder-sweep row) |
| `single_charge` | bool | **derived** — true iff exactly one charge cell is a non-sentinel real value |

Sourced from `quarry-candidates-full.jsonl` (`origin`→wave, `sources`→funnel, `screen`/`multi_charge`→
single_charge). The battery reads this sidecar to decompose any v2→v3 statistical shift by funnel
(prereg bet B6, funnel homogeneity) — this is the whole reason provenance travels with every row.

## 3. QC tiers (spec §3 — the 1/3 pilot error rate handled inside broad scope)

All cells enter `claimed`. Before freeze, an **owner** tiered confirm-pass, sized to the measured
per-column error model:

| Tier | Columns | Confirm requirement before freeze |
|---|---|---|
| **Reliable** (0 corrections in the K3 pilot) | `decision` (NP-level), `parallelization` | **Sampled:** owner hand-checks a sealed random 15% per source funnel; if sample error > 5%, that funnel escalates to full confirm |
| **Judgment-heavy** | `approximation` (currency + UGC-conditional), beyond-NP `decision` (the Σ₂ᵖ↔Π₂ᵖ trap) | **Full owner confirm** of every cell |
| **Dear** | `counting` (F-1 per-problem bar) | **Full owner confirm**; `open` downgrades expected and unlamented |

Confirm **wall-clock logged per sitting** (the measurement K4 declined to invent, taken here on the
real work). Surviving cells flip to `confirmed`; failing cells are corrected or opened, the error
logged by funnel (the **funnel error table** is itself a deliverable). Freeze gate: the confirm program
complete per this table. Broad scope changes how much confirming there is, not whether it happens.

## 4. Wave plan (spec §4 — sequencing only; all four run continuously)

The agent drafts all four waves continuously (touches nothing frozen); the owner confirm-pass is the
only gate. Order = K4's column priority as sequencing, **not** a scope gate:

- **W1** — parallelization + decision-led (GHR remainder + reductions.network decision/approx join,
  seeded by the 10 K3 pilot rows).
- **W2** — beyond-NP decision (de Haan–Szeider, Schaefer–Umans; incl. the ~66 single-charge
  decision-only rows).
- **W3** — approximation currency sweep (Crescenzi–Kann remainder re-verified vs post-2000 literature).
- **W4** — counting attempts (F-1 per-problem bar; `open` downgrades expected).

**rn access:** the reductions.network GitLab is unreachable from the drafting environment (confirmed
all through Quarry K1); the decision/approx join uses the **arXiv:2511.04308 snapshot + manual citation
chase**, documented and flagged higher-cost per spec §4's fallback.

## 5. Discipline inherited

R20 (9-check) / F-1 (per-problem counting) / R1 (typing) / S2 (equivalence) / I3 (encoding) as law;
prereg-before-analysis; marginals-first occupancy (R3); both-values-always (v2 + v3 in every table);
provenance per row. The frozen `atlas.jsonl` and `atlas_v2.jsonl` remain the permanent, citable, frozen
objects they already are.
