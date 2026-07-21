# eightfold — agent/contributor rules

Load-bearing invariants for anyone (human or agent) working in this product. Each encodes a decision from the
spec (`docs/specs/eightfold-v1-charge-atlas-spec.md`, including Build addenda R1–R8) and the approved plan.

## What this is (one paragraph)

Eightfold builds the first quantitative **charge atlas** of computational problems: rows are natural problems
under fixed encodings, columns are eight literature-sourced hardness "charges" (decision, counting,
approximation, parameterized, parallelization, proof-size, average-case, landscape/freezing). Every cell
carries a value + a citation, or an explicit flag. Structure detection over the atlas looks for multiplets
(H2), forbidden regions (H3), and gaps. Third project in the proof-space line (Desert Map → Proof Census →
Eightfold); it executes "Move One" of the Gell-Mann sequence — Mendeleev card-sorting done honestly, no
claimed periodic table (that would be Move Two, phase-gated on Move One finding shape).

## THE INVARIANTS (do not break)

1. **Unknown ≠ zero.** Missing values are explicit sentinels — `open` (applies, value unknown), `unmeasured`
   (applies, nobody has measured it), `n.a.` (the charge structurally does not apply to this problem). Never
   impute; never leave a blank that reads as a value. **The `n.a.`/`open` boundary (R15):** `n.a.` only when
   the charge's object cannot be constructed (no optimization version, no unsat family); if a random ensemble
   could be defined, the cell is `open` even if unstudied — never `n.a.`.

2. **Every real value is cited, or flagged.** A cell with a real charge value carries a resolvable citation
   in `provenance`, or is marked `uncited-folklore` — a debt, not a value: it must be resolved to a citation
   or reverted to `open`. `confirmed` (primary-source read) is **owner-promoted** at review, never set by the
   agent; the agent fills `claimed` (real citation, not independently confirmed). "Fully cited" for the A1
   gate means `claimed`-or-better with **zero `uncited-folklore`** left — it is NOT "fully confirmed" (R8).

3. **Canonical task pinned per charge (R1); `n.a.` ≠ `open` (R2).** The eight charges attach to different
   formal objects (worst-case decision vs the #-version vs the optimization version vs a random ensemble vs
   an unsat family). Each cell names its `canonical_task`. Coverage is counted over **applicable** cells
   (`applicable-and-cited / applicable`): an `n.a.` cell is correctly filled, not missing.

4. **Occupancy over marginals, not the full grid (R3); dual-missingness for H1 (R4).** The full 8-D grid is
   vacuous (every occupant a singleton). Forbidden-region / gap analysis runs over 2-D and 3-D charge
   marginals. The H1 effective-dimensionality verdict requires agreement between the full-table and
   complete-case analyses — otherwise the leading axis is a sociology-of-study artifact, not hardness.

5. **Entailment rules carry exact preconditions (R6).** Every rule in the entailment layer states the
   theorem's exact hypotheses (`preconditions`) with a citation; the layer's consistency test rejects any
   rule without one. A wrong selection rule silently turns a genuine gap into a false "theorem-forbidden"
   cell — the exact category we mine for discoveries — so a missing rule is safer than an over-broad one.

6. **Pre-register before analysis; kill honestly.** The coding scheme + predicted signatures (H1–H3) + kill
   thresholds commit to `results/prereg/prereg_v1.json` **before any `structure.py` run on real data** (R7);
   harness debugging uses a synthetic toy table, never the pilot. A changed prediction is a new prereg
   version, not an edit. Do not loosen a threshold or widen a marginal to manufacture structure. The
   degeneracy verdict (effective dimensionality ≈ 1) and the population-failure verdict (<70% cited) are
   pre-registered **outcomes**, not failures — report them. **Method changes are prereg-gated too (R11):** a
   preview-prompted analysis change (e.g. subspace clustering) commits to a new prereg version labeled
   *pilot-informed* before the next milestone's structure run — the preview may teach us about the instrument,
   never tune the analysis post-hoc.

7. **`measured` is quarantined (R9).** A `measured` value (self-generated, not from the literature) is allowed
   only for charges 7 (average-case) and 8 (landscape), and as `measured-scaling` for charge 6 (proof-size);
   the validator **rejects** it for charges 1–5. Its provenance points to a reproducible experiment artifact
   (`experiment` = prereg + manifest + seeds + code commit), the same standard as Census. In v1 only
   already-banked experiments fill cells — the Census backbone datum enters now; new measurements are separate
   mini-projects queued from blank cells, not atlas work. A3 runs structure detection with and without
   `measured` cells; no structure claim may rest on them alone.

8. **Web citations are snapshotted (R10).** Any cell citing a `url` (the online Crescenzi–Kann compendium, the
   Complexity Zoo, any web page) also carries a `snapshot` (a Wayback capture or a local copy committed under
   `docs/sources/`) and a `retrieved` ISO date; the validator rejects a bare `url`. Persistent identifiers
   (DOI, book + page) need no snapshot. The gate must still pass when the live pages go dark — the atlas
   validates in five years.

## Storage & tiering

Canonical storage is versioned JSONL (`results/atlas/atlas.jsonl`, one problem per line, line-diffable) + a
the `results/atlas/SCHEMA.md` contract. The atlas is **curated in `dev/build_atlas.py`** (Python is far less
error-prone than hand-editing nested JSONL) and generated with `python dev/build_atlas.py`; atlas.jsonl is the
loadable generated artifact (both committed). Edit the builder, regenerate, then `validate`. The spec's
"parquet" is an optional export, not the source of truth (the repo standard is JSONL + a validator gate). Single-tier for v1;
`resolve_atlas_path` carries a documented no-op seam for a later physmap-style seed/premium firewall — do not
wire the premium branch until there is a reason to split.

Run tests from inside this product dir: `python -m pytest tests -q`.
