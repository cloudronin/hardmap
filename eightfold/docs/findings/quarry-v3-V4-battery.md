# Atlas v3 — V4 battery: the six sealed bets, scored

**Date:** 2026-07-24 · **atlas:** `atlas_v3.jsonl` (sha `e62f3c28`, frozen) · **prereg:** `prereg_v9.json`
(committed before analysis) + clarifications 01–03 · **scorer:** `dev/score_bets_v4.py` (seed 20260724,
deterministic) · **result:** `results/atlas/atlas_v3_bets_v4.json`.

> **QC provenance (condition 3 on the freeze).** v3 cells are **agent-double-passed and owner-unconfirmed**;
> see `trust-labels.md`. Double-passed is not owner-confirmed, and no number below should be read as if it
> were. Populations: **v2** = frozen 118 kernel; **v3-new** = the 227 expansion rows (the out-of-sample
> population every bet is scored on); **v3-full** = 345.

## Scorecard — 5 of 6 hold; the miss is the informative one

| bet | verdict | headline |
|---|---|---|
| **B1** gradient robustness | ✗ **does not hold** | v3-new approx↔param V = **0.31 raw / 0.0 corrected**, below v2's CI **[0.53, 0.92]** |
| **B2** incompressibility | ✓ holds | k* = **1** on v3-new (held-out) |
| **B3** NPI calibration | ✓ holds | **0** mis-typed NPI rows — the row did not inflate |
| **B4** occupancy | ✓ holds | PH×FPT inhabited; **0/16** forbidden cells violated; **6/123** gap cells newly filled |
| **B5** folklore gap | ✓ holds | published-proof fraction **0.18** vs v2's 0.31 — gap widened |
| **B6** funnel homogeneity | ✓ holds (weak) | no rn outlier; rn-present **0.39** > rn-absent **0.10** |

## B1 — the gradient does not reproduce out-of-sample (the prereg's payoff)

> **Revised 2026-07-24 (owner ruling, post-commit).** The original section committed at `794c43d` read
> the falsification as roster-composition simpliciter ("not a universal law"). That reading survives but
> is under-determined: it is confounded with a *recruitment-composition* alternative, and both must sit on
> the record. The scorecard does not move — B1 is falsified either way. The interpretation gains the
> composition table and the three-population arc below.

The v2 hardness gradient — the approximation↔parameterized coupling at **Cramér's V = 0.73**, a headline
structural finding — **does not reproduce on the broad expansion.** On v3-new's 42 both-real pairs the
association is **V = 0.31 uncorrected, 0.0 after the Bergsma sparse-table correction** — both below v2's
95% bootstrap CI lower bound of 0.53, under both the v3 9-rung and v2-collapsed 8-rung codings
(clarification-02; identical here). The bet named this acceptable in advance: *"movement outside the CI ⇒
the v2 gradient was partly roster-composition, decomposed by funnel — a finding either way."* A sealed bet,
scored on rows drawn after it was committed, falsified a comfortable prior. **v3 is `roster-conditional`.**

### Two readings, both live

The drop admits two explanations, and the data does not yet separate them:

- **Roster-composition** — the expansion *problems* genuinely couple approximation and parameterized more
  weakly than the canonical core did. The gradient was a property of *which problems* v2 sampled.
- **Recruitment-composition** — the low V is (partly) an artifact of *which cells* happen to carry both a
  real approximation AND a real parameterized value. The both-real subset is not a random sample of the
  population; the expansion recruited a compositionally different 42.

The composition table shows the recruitment genuinely differs — this is not a tie-breaker for either
reading, it is the reason both stay live:

| | v2 both-real (n=47) | v3-new both-real (n=42) |
|---|---|---|
| top approx value | **APX-complete 49%** (tight) | poly-APX 31% (spread; no value > 31%) |
| top param value | **FPT 79%** (tight) | FPT 48% (spread) |
| param categories | FPT / W[1] / W[2]+ | **+ para-NP-hard (5)** — absent from v2's both-real |

v2's both-real is a concentrated APX-complete×FPT block, and a concentrated joint distribution *mechanically*
produces high Cramér's V; v3-new's is dispersed across the grid with a new para-NP-hard column. So "the
gradient washed out" is entangled with "the both-real recruitment de-concentrated." Separating them needs a
recruitment-controlled resample (v3.1 work), not another bet.

### The three-population arc — coupling concentrates with canon-proximity

Placing v2, v3-new's two rn strata, and the generated-universe baseline on one axis, the coupling tracks
**proximity to the canonical core**:

| stratum | approx↔param V | canon-proximity |
|---|---|---|
| canon core (v2 full) | **0.73** | highest |
| in-network (v3-new, rn-present) | **0.39** | high |
| natural universe (`natural.v3.v`, generated) | **0.26** | baseline |
| periphery (v3-new, rn-absent) | **0.10** | lowest |

The periphery sits *below* the natural-universe baseline: the broad expansion's non-canonical rows couple
these two charges less than a randomly generated universe does. This is a gradient-of-the-gradient — the
coupling is not absent from the landscape, it **concentrates as you approach the canonical core**. That is
a stronger and more specific statement than "roster-conditional," and it is what the falsification buys:
"hardness charges couple" was never a universal law; it is a canon-proximity effect, measured on four
populations. **"Not a universal law" now sits next to its confound, not in front of it.**

## B2 — incompressibility survives at scale

k* = 1 on v3-new (held-out LCM 1-SE estimator, the v7 battery, V3_SPEC coding). The atlas remains
effectively one-dimensional: no second latent basis emerged as the roster nearly tripled. The bet flagged
k* ≥ 2 as "the biggest positive surprise" and genuinely possible — it did **not** occur. This does not
touch the banked v2 k*=1 verdict; it independently reproduces it on new rows.

## B3 — the NPI row did not inflate

**Zero** v3-new rows carry `decision = NPI-candidate`. The thin, delicate NP-intermediate row was not
grown by the expansion, so no CSP-shaped / dichotomy-decidable NPC could be mis-slotted into it — the
calibration the bet guards holds vacuously and informatively. (The two Garden NPI admits — ring-isomorphism,
simple-stochastic-games — are v3.1, each resting on an established NP∩coAM / NP∩coNP membership theorem,
not conjecture.)

## B4 — occupancy grew where structure permitted, nowhere it forbade

- **PH-complete × FPT stays inhabited** (pre-called INHABITED): 7 rows — abduction, disjunctive-ASP, and
  the semi-stable/stage argumentation family (Π₂ᵖ × FPT-by-treewidth, verified at Quarry K3).
- **0 of 16 theorem-forbidden cells violated** — a real check (all 16 parsed and tested against every v3
  row). No v3 row sits in a cell a theorem forbids; the data does not violate the entailment layer.
- **6 of 123 v2 gap cells newly inhabited by a v3-new row**, 117 still empty. Beyond PH×FPT, the expansion
  filled: APX × W[1] (`minimum-k-cut`), APX-complete × W[2]+ (`precedence-constrained-scheduling`),
  PTAS × W[1] (`closest-substring`, `geometric-independent-set`), log-APX × W[1] (`art-gallery`),
  poly-APX × W[2]+ (`bandwidth`, `independent-dominating-set`, `target-set-selection`).

## B5 — the folklore gap is the field's, not our effort's

Of v3-new's **77 applicable** counting cells (real #P + open, excluding n.a.), only **14 = 0.18** carry a
per-problem published proof; **63 resolved to `open`** under the F-1 per-problem bar. Against v2's ~0.31,
the published-proof fraction did **not** improve at scale — it widened. Tripling the roster did not close
the counting-provenance gap, because the gap is in the literature, not in the mining effort. Confirmed
out-of-sample.

## B6 — no funnel outlier, but little structure to be homogeneous about

Scored on **rn_membership** (binary, source-derived) per clarification-03; the six-way `source_funnel`
split is **withheld** — five of its six labels are miner-attributed, not source-verified, and reporting a
six-way table would repeat the instance-9 defect. Neither rn stratum is an outlier: rn-present V = 0.39,
rn-absent V = 0.10, both inside the pooled band [0.00, 0.44]. But the band is wide precisely because the
pooled association is weak (B1), so the "homogeneity" holds over not-much-signal. The one nameable signal
— rn-present carrying more gradient than the rest — is B1's decomposition seen from the other side, and on
16 in-network rows it is suggestive, not conclusive.

## What V4 establishes

The expansion **held four structural findings** (incompressibility, NPI calibration, forbidden-cell
integrity, the folklore gap) and **falsified one** (the approx↔param gradient is a canon-proximity effect,
not a universal law — with the roster-vs-recruitment confound and the four-population arc kept live on the
record, per the 2026-07-24 revision). One bet (B6) holds only weakly, as a consequence of the one that
failed. That is a healthy out-of-sample result: the atlas's *invariants* (k*=1, the entailment layer, the
folklore gap) are robust to a 3× roster change, while its *contingent* structure (the approx↔param
gradient) is correctly exposed as concentrating with canonical-proximity rather than holding universally. Every number is reproducible via `hardmap repro` (manifest claims `canon.*.v3new`);
none is owner-confirmed, and the trust-label line travels with each.
