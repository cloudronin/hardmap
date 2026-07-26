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

## §3 — The eight assertions (enumeration 2026-07-26; recut from nine, see below)

Every numeric literal below was **extracted from an artifact**, not transcribed from the enumeration.
Where wording and artifact differ, the artifact governs and the difference is recorded.

| # | assertion | artifact → value | class | status |
|---|---|---|---|---|
| 1 | hardness is a vector; k*=1 at three scales | `factors_v1.json::k_star` (**k_hat_1se 1, verdict_interval [1]**) · repro `bets.b2.kstar.v3new` (**k_star 1**, 3× roster) · `factors_v1_1.json` low-rank arms | MEASURED | **SOURCED** |
| 2 | the coupling is roster-conditional | two statistics — see the note below | MEASURED | **SOURCED, conflation hazard** |
| 3 | "locality" is two properties | repro `mosaic.split.pooled` → **n 111, V_loc_approx 0.547, V_loc_param 0.231** | MEASURED | **SOURCED** |
| 4 | where structure is fully readable it determines fate, **as theorems — and closure under blending operations is what characterizes the tractable side** | `prereg_v12` C3 (**46 flag-vectors → 46 profiles, zero ambiguity**) · Bridge Ledger pinned `§3.decision` (Bulatov–Zhuk / Barto–Kozik cells) · `postlattice.py` `_MAJ`/`_MINORITY`, anchors green at both domain sizes | PROVEN | **SOURCED — now carries the recut easy pole** |
| 5 | that structure is surface-invisible | `arm-a-surface-vs-closure.md` — positive control **0.983 / 1.000**, every closure ≤ its null | MEASURED | **SOURCED** |
| 6 | on natural rows, surface anatomy adds nothing to fame | `terroir_v1_results.json` (**+0.0685 headline; within-family +0.0000**, 170/255; logic-proof **−7, p 0.0359**) · `terroir_v1_ablations.json` (**+0.0188** within coverage) · `marrow-i0-census.json` (**34 of 345**) | MEASURED | **SOURCED** |
| 7 | **the census backbone** — refutation difficulty concentrates where hardness does | repro `census.backbone` → **over_constrained 1.0 → near_threshold 272.6**; two structurally different samplers agreeing; planted-core calibration passed | MEASURED | **SOURCED** |
| 8 | the literature's hardness bookkeeping fails audit | `errata-v1.json` / `errata.md` · `counting-folklore-gap.md` · **the unwritten theorem**, chain below · **#19** minimum-sum-of-squares, first original `proven-here` cell | CITED + one PROVEN-HERE | **SOURCED** |

### The recut: nine → eight

Old assertion 7 ("certified anatomy at both poles") is **withdrawn as a single claim** and split:

- **Easy pole — folded into assertion 4.** Closure under blending operations (majority, affine) as the
  characterization of tractability is the Bridge Ledger's *pinned* `§3` cells and the Post-lattice machinery
  this program computes and tests. It was already load-bearing inside assertion 4; a separate assertion
  double-counted one evidence base.
- **Hard pole — moved to §6 (banked), not §3.** Austrin–Mossel (pairwise-independent support ⇒
  approximation resistance) is a literature fact at **survey confidence, never pinned**, from a bridge hunt
  whose note is not in-repo. Under the governing law it cannot be a §3 claim.

**Why it was in the list:** it entered from chat synthesis rather than from an artifact. Recorded because
the recut is evidence the map works, not bookkeeping — see methods instance 32.

### #2 — two distinct statistics, which never share a sentence

- **Sealed out-of-sample falsification** — repro `bets.b1.gradient.v3new`: v3-new corrected **V = 0.0**
  against the v2 CI **[0.53, 0.92]**. Verdict FALSIFIED.
- **The four-population arc** — `quarry-v3-V4-battery.md`: canon core **0.73** (repro `canon.gradient.v`
  full_v **0.7293**) → in-network (rn-present) **0.39** → generated universe **0.26** (repro
  `natural.v3.v` v **0.2555**, CI [0.13, 0.398]) → periphery (rn-absent) **0.10**.

The arc's 0.10 is the rn-absent *stratum* of v3-new; the 0.0 is the *whole* v3-new population corrected.
Running them together reports one result twice.

### #8 — the unwritten theorem, full artifact chain

Three links, all verified 2026-07-26:

1. **The sitting record** — `quarry-v2-gate4-sitting.md`: *"21 promoted to `confirmed`, 1 retracted to
   `open`"*, the retraction named as **#11 geometric-disk-cover (object-drift; free-placement W[1] not
   pinned)**, dated with owner authority.
2. **The cell** — `atlas_v3.jsonl::geometric-disk-cover.parameterized` stands at **`open`**, and the row is
   **absent** from the 21-cell `quarry-v2-gate4-promotions.jsonl`.
3. **The rationale** — Marx ESA 2005 Thm 5 proves **squares**, not disks; the disk-specific line
   (Marx–Pilipczuk 2015 / IWPEC 2006) covers only the **discrete-centres** form. The free-placement
   statement the literature cites is **unwritten**.

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
| **hard-pole certificate** (Austrin–Mossel: pairwise-independent support ⇒ approximation resistance) | recut from assertion 7 | **BANKED — survey confidence, never pinned. PIN BEFORE ANY CLAIM LEANS ON IT.** Note not in-repo. |
| **geometry probes** · **frontier map** | chat-generated notes on the owner's side | **BANKED-IN-CONVERSATION** — §6 describes them as such until they land as dated commits, then cites them |

## §7 — Related work — sourced to the SPECS, not the repo

| obligation | source | status |
|---|---|---|
| meta-problem line (Bulatov; Creignou–Khanna–Sudan; AutCSP) — nearest claim + oracle supply | `mosaic-v3-objective-intervention-grid-spec.md` §7 "Related-work obligations (dated hunts; mandatory in the writeup)" | SOURCED to spec |
| ISA/EHM — the instance-level contrast | same | SOURCED to spec |
| ISGCI — the transposed structural cousin | same; plus `strata-v2-structure-atlas-spec.md` §I2 (graphclasses.org, Unknown⟷`open` alignment noted) | SOURCED to spec |
| CoRCoD + structure→dynamics ML — pattern precedents | same | SOURCED to spec |
| *"the two-table object with a measured, out-of-sample bridge remains unclaimed territory per the hunts"* | same | **SOURCED AS A POSITION, NOT AS EVIDENCE** — the hunts' results are not in the repo, so the claim is citable to the spec but its underlying search is not reproducible. State it as the program's position, dated, or re-run the hunt as declared new work. |

**Spec-to-repo gap:** none of §7 was ever copied into the repository. W1 should land these obligations as a
findings-side document so the writeup cites an in-repo artifact rather than a file in `~/Downloads`.

## Abstentions (the three, all sourced)

| abstention | artifact | status |
|---|---|---|
| no measured mechanism for the coupling on natural problems; the one live instrument is the registry at 0/57 | `grid-prospective-registry.json`; `terroir_v1_results.json` (FAMILY-BORNE) | SOURCED |
| no verdict on whether closure anatomy transfers — unaskable at current population | `marrow-terroir-c-power.json` (0 admissible families under every reading) | SOURCED |
| nothing unconditional — every hardness label rides the standard conjectures | schema-level; stated once per the tone constraint | SOURCED |

---

## Expository framing (not claims)

| item | disposition |
|---|---|
| the convex-analysis teaching frame (§1) | `framing (origin: owner exchange, 2026-07-25)` — **no artifact required, no claim rides on it.** The governing law binds claims and numbers; expository frames may be new prose. |

## Audit rules carried into W2

1. Every numeric literal in the prose has a row here, or the draft halts.
2. Values are **extracted from artifacts at draft time**, never transcribed from a findings note that
   might itself be stale — the §9.1 erratum and the README's "eight" are both live examples of a document
   drifting from its own gate.
3. A hash quoted in prose is re-verified in the same pass that quotes it.
4. PROVEN / MEASURED / CITED is carried per claim, not per section.
5. `UNSOURCED` blocks the claim, not merely its citation.
6. **Two statistics that answer different questions never share a sentence** — assertion 2's 0.0 and 0.10
   are the standing example.
7. **Chat is not an artifact.** A claim whose only provenance is a conversation summary is UNSOURCED by
   definition, however confidently stated and whoever stated it. Three of nine assertion-candidates entered
   that way and were caught here; see methods instance 32.
