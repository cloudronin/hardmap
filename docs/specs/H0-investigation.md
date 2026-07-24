# H0 — Investigation close-out (I1–I4)

Grounding facts that drove the consolidation, resolved against the actual repo
state before migration. These fix the strategy that H1–H5 execute.

## I1 — Repo topology  → filter-repo extraction, hash-map mandatory
The four folders lived in **one private monorepo** (`uofa-lab`, 449 commits);
none had its own `.git`. Extraction therefore used `git filter-repo` keeping the
four paths, which **rewrites commit hashes**. Because the seals are commit
hashes, this makes a hash-map mandatory:
[`docs/hash-map.txt`](../hash-map.txt) (full old→new map) and
[`docs/seal-chain.md`](../seal-chain.md) (every sealed prereg resolved). History
was not entangled with the unrelated `praxis` product; the monorepo's bulk
(~237 MB) was out-of-scope sibling projects dropped by the
filter — the extracted history is ~2 MB. The `foundry` branch (Prism) was
fast-forwarded onto `main` before extraction so all cited numbers share one
linear history.

## I2 — Shared-code inventory  → nothing to vendor; two internal edges
The four folders import **zero** code from outside themselves — every sibling-project
or `uofa` occurrence is prose or provenance, not an import. The only real
cross-tree edges are internal:
- `foundry` → `eightfold` (atlas, charges, crucible, factors, structure)
- `proof-census` → `desertmap` (instance, verify, fixtures)

`desert-map` and `eightfold` are standalone leaves. These edges are satisfied
today only by editable co-install (not declared deps), so the consolidation ships
all four in **one `hardmap` distribution** to resolve them by construction.
Those sibling projects remain private in `uofa-lab` and are not carried over.

## I3 — Paper-number inventory  → 8 claims mapped to code + artifact
Candidate claim-id set for `repro/manifest.yaml` (finalize against the draft):

| claim id | folder | notes |
|---|---|---|
| `canon.gradient.v` | eightfold | `crucible.py` + `structure.cramers_v`; artifact `results/atlas/crucible_results.json` |
| `canon.crucible.verdicts` | eightfold | S1/S2/S3/**S5** (S4 deferred) — represent what exists, manufacture nothing |
| `factors.kstar` | **eightfold** | `factors.py:excess_over_null` — Factors is owned by eightfold, not foundry |
| `natural.v3.v` | foundry | `dev/lattice_v3.py`; `results/lattice/lattice_v3_occupancy.json` |
| `natural.prism.residuals` | foundry | `prism.py` + `dev/prism_matrix.py`; on `main` after the FF merge |
| `natural.direction.corrected` | foundry | corrected Spearman `dev/prism_v2_matrix.py`; buggy sealed impl retained — an H4 audit surface |
| `census.backbone` | proof-census | `metrics.py:backbone`; `results/c3/c3_summary.json` |
| `census.plurality` | proof-census | `metrics.py:pairwise_jaccards`; `results/c3/c3_summary.json` |

Frozen atlas: `eightfold/eightfold/results/atlas/atlas.jsonl` (264,972 bytes,
118 rows), byte-identity enforced by `tests/test_loader.py`.

## I4 — Results-artifact completeness  → fast tier ~ready; no LFS
Each folder already commits small "receipts" (prereg JSONs, atlas jsonl,
`checkpoint.jsonl` 2.4 MB, summary JSONs) and gitignores bulky regenerable
output. Total committed results ≈ 4.4 MB; **no file exceeds 5 MB**, so no Git LFS
or release-asset convention is needed. The fast tier recomputes from these
committed artifacts.

## H0 gate
- PyPI `hardmap` (0.0.1 placeholder) reserved; `github.com/cloudronin/hardmap`
  reserved. ✅
- I1–I4 written up (this document). ✅
