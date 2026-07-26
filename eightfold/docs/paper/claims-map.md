# Claims-to-artifacts map — skeleton (W0)

Every number in the consolidation draft resolves here: **claim → artifact → hash → field**. W2 is the
mechanical audit of this map; an orphan number is a halt, not a footnote.

**Status column.** `SOURCED` — artifact and field both identified, value to be extracted at W1.
`NEEDS-EXTRACTION` — artifact identified, exact field not yet pinned. `UNSOURCED` — no artifact found;
**blocks the claim, not just the citation.**

**Hashes below are sha256 prefixes verified 2026-07-26.** W1 re-verifies rather than trusting this table;
W2 diffs prose against artifact values.

---

## Frozen artifacts (the anchor set)

| artifact | sha256[:16] | role |
|---|---|---|
| `atlas.jsonl` | `6d53a4f1d0907f16` | charge atlas v1, byte-preserved through consolidation |
| `atlas_v2.jsonl` | `784f4739360f1d7b` | + Strata applicability layer |
| `atlas_v3.jsonl` | `e62f3c284b408a26` | broad expansion; the population most results run on |
| `anatomy_v1.jsonl` | `8ff11f8a33bbdce7` | Structure Atlas, 4417 rows (345 natural + 4072 boolean) |
| `anatomy_v2.jsonl` | `f802f2e50c73f2fe` | + Marrow closure columns on 28 rows |
| `mosaic-locality.jsonl` | `4c7ef94c1e85390f` | blind-coded locality instrument |
| `quarry-v2-fills.jsonl` | `c2f81f3b0d79551e` | 22 verified Channel-B fills |
| `grid_arm_b_predictions.json` | `cc5bb3895a44a043` | sealed Arm B predictions (Terroir re-analyses these) |
| `prism_v2_charges.json` | `52236fe2aede9f8b` | Boolean universe charge table |

Seal chain: `docs/seal-chain.md` — **43 sealed preregistrations**, each resolved to its introducing commit
through `docs/hash-map.txt`. Preregs on disk: `prereg_v1` … `prereg_v15` plus clarifications/addenda.

---

## §2 — The artifacts

| claim | artifact | status |
|---|---|---|
| atlas v1 byte-preserved through consolidation | `atlas.jsonl` + round-trip test | SOURCED |
| Anatomy v1 row counts and column registry | `anatomy_v1_freeze.json`, `anatomy.py::COLUMNS` | SOURCED |
| passport verdicts: 3 admissible as-is / 4 via collapse / 2 invariant | `anatomy-passports.json`; repro `anatomy.passports.verdicts` | SOURCED — **note the §9.1 erratum (2026-07-25)**; the sealed table's prior 4/2 is corrected in place |
| Anatomy v2 is a new sealed version, v1 unmoved | `anatomy_v2_freeze.json`; repro `marrow.build.v2_without_moving_v1` | SOURCED |
| reproducibility: N claims, `hardmap verify` 10/10 | `repro/manifest.yaml` (**28 claims**), `hardmap/verify.py` | SOURCED — **README's "eight" is stale; do not quote it** |
| 43 sealed preregistrations | `docs/seal-chain.md` | SOURCED |

## §3 — The assertions — **enumeration BLOCKED**

Mapped against what the directive names, so the owner can see which of the nine already have receipts.

| assertion (directive wording) | candidate artifact | status |
|---|---|---|
| the vector result | `A4-charge-atlas-move-one.md`, `I1-I4-investigation.md`, `A2-setup.md` | NEEDS-EXTRACTION — three candidate docs, claim not yet pinned |
| roster-conditionality | `absorption-closeout.md`, `quarry-v3-V4-battery.md` | NEEDS-EXTRACTION |
| the two-property split | `mosaic-findings.md`, `mosaic-L1-findings.md`; `anatomy.py::BET_HISTORY["locality_class"]` records *V = 0.56 approx / 0.14 param* | SOURCED |
| theorem-determinism on the Boolean universe | `mosaic-v3-findings.md`; `prereg_v12` C3 (46 flag-vectors → 46 profiles, zero ambiguity) | SOURCED |
| surface-invisibility of closure | `arm-a-surface-vs-closure.md` | SOURCED |
| FAMILY-BORNE + the unaskable closure retest | `terroir_v1_results.json`, `marrow-terroir-c-power.json`; repro `terroir.a4.*`, `marrow.census.*` | SOURCED |
| **two-pole certificates (blending / pairwise-independence)** | — | **UNSOURCED** |
| census localization | ambiguous: Mosaic `localization` vs proof-census `census.backbone` / `census.plurality` | **AMBIGUOUS — needs disambiguation** |
| literature audit: errata · folklore gap · **unwritten theorem** · proven-here cell | `errata.md`; `counting-folklore-gap.md`; — ; `quarry-v2-gate4-promotions.jsonl` | 3 of 4 SOURCED; **"unwritten theorem" UNSOURCED** |

## §4 — The negative results

| result | artifact | status |
|---|---|---|
| Pebble's absorption | `absorption-closeout.md` | NEEDS-EXTRACTION |
| the unaskable conditioning | `absorption-closeout.md`, `mosaic-L3-L4-findings.md` | NEEDS-EXTRACTION |
| powered locality MISS (3-class INSUFFICIENT → 2-class powered MISS) | `quarry_v2_results.json`; repro `mosaic.absorption.2class`, `mosaic.power.3class` | SOURCED |
| the circular P4 | `prereg_v12` (C3/C4), methods instance 21 | SOURCED |
| Terroir — FAMILY-BORNE | `terroir_v1_results.json` (within-family lift **+0.0000**, 170/255 both ways) | SOURCED |
| Terroir — A1 reported as a MISS | `terroir_v1_ablations.json::sealed_prediction_scoring` | SOURCED |
| Marrow — closure retest unaskable | `marrow-terroir-c-power.json` (0 admissible families, every reading) | SOURCED |
| Marrow — Kill 1 fires | `marrow-i0-census.json` (34 principled; band 34/41/45) | SOURCED |

## §5 — The methods contribution

| claim | artifact | status |
|---|---|---|
| ledger size | `methods-thread.md` — **26 numbered entries, 6–31; 1–5 predate the file; 15 absent; 6 appears twice** | SOURCED — **the directive's "~28" is unsupported; use the derived form** |
| the tidy-number gate | `verify.py::check_suspicious_cleanliness` + `_watched` | SOURCED |
| the denominator gate | `verify.py::check_lift_denominators_match` | SOURCED |
| census-before-seal | `Anatomy-SCHEMA` §3.3/§3.3b | SOURCED |
| expression-not-artifact | methods 26, 28 (corrected), 31 | SOURCED |
| "it pointed the unflattering way" | methods 31 | SOURCED |
| gates run in CI, 10/10 | `hardmap verify` | SOURCED |

## §6 — Open instruments

| claim | artifact | status |
|---|---|---|
| registry at 0/57, mechanism-attribution rules | `grid-prospective-registry.json`, `grid_registry.py` | SOURCED |
| the two-verdict stack | `terroir-v1-findings.md` §6, `marrow-i0-census.md` §7 | SOURCED |
| frontier map | `arm-a-surface-vs-closure.md` | NEEDS-EXTRACTION |
| **geometry probes** | — | **UNSOURCED** |

## §7 — Related work — **fully UNSOURCED**

| obligation | status |
|---|---|
| meta-problem line · ISGCI · ISA/EHM · CoRCoD · dichotomy-program lineage · "the dated hunts" | **UNSOURCED — zero matches for every term** |

---

## Audit rules carried into W2

1. Every numeric literal in the prose has a row here, or the draft halts.
2. Values are **extracted from artifacts at draft time**, never transcribed from a findings note that
   might itself be stale — the §9.1 erratum and the README's "eight" are both live examples of a document
   drifting from its own gate.
3. A hash quoted in prose is re-verified in the same pass that quotes it.
4. PROVEN / MEASURED / CITED is carried per claim, not per section.
5. `UNSOURCED` blocks the claim, not merely its citation.
