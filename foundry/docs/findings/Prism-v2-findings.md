# Prism v2 (prereg_v33) — findings: the anti-canon residual replicates (attenuated), and the pooled direction is cut-dependent

Prism v2 charged the natural **arity-≤4** Boolean single-relation roster (**4072 symmetry classes** — 3982 arity-4 +
90 arity-≤3, permutation-only dedup) with the Prism v1 oracle set, and resolved **one** sealed question: does the
anti-canon Min-Ones residual (v1 post-hoc) replicate one size up? It does — **replicated but strongly attenuated**. The
run also surfaced a construct-validity defect in the sealed direction statistic that reaches back into v1, and, once
corrected, exposes a sharper pooled-level finding than v1 reported.

## Predictions ledger (sealed prereg_v33; 3 & 4 dropped at review, see the spec)

| # | prediction | verdict |
|---|---|---|
| 1 | reproduction gate — arity-≤3 subset reproduces V=0.256; NPI empty | **PASS** (V=0.2555, decision ∈ {P,NPC}) |
| 2 | bounded-width marginal (descriptive) | **confound confirmed** — every unbounded-width param-real class is affine (4/4) |
| 3 | localization⟷param survival | **DROPPED at review** (provably confounded) |
| 4 | localization absorption (I6) | **DROPPED at review** (provably confounded) |
| 5 | Min-Ones anti-canon residual replicates (Spearman<0, CI excludes 0) | **REPLICATES — strongly attenuated** — see §2 |
| 6 | approx⟷param the largest bridge-completed residual | **HIT** — pooled 0.352, Min-Ones 0.504, largest other 0.143 |

## 1. The gates, and the confound confirmed on the data (pred 1, 2)

The reproduction gate passed exactly: the arity-≤3 subset (90 classes) reproduces v1's approx⟷param **V = 0.2555**, and
the NPI row is empty (decision ∈ {P, NPC}). The pipeline reads the same roster v1 did.

**Pred 2 confirms the dropped-arm argument empirically.** At arity 4, bounded-width does vary (marginal
`{bounded-width: 3178, unbounded-width: 894}`), but among the **param-real** rows there are exactly **4** unbounded-width
classes and **all 4 are affine** (purely-affine, arity-4, param-FPT). So every unbounded-width param-real class is
netted out by the affine bridge → the localization-absorption test has one stratum on the bridge-completed residual.
The confound the review predicted from Schaefer's theorem is exactly what the roster shows: `unbounded-width ∩ param-real
= affine`. Preds 3 & 4 were correctly dropped; this is the marginal declaring it, as designed.

## 2. Pred 5 — the anti-canon Min-Ones residual replicates, strongly attenuated

**Scored on a tie-corrected Spearman** (the sealed implementation was a buggy argsort statistic — see §3; both numbers
permanent, per the owner ruling). On the arity-4 non-affine param-real rows, Min-Ones objective:

| | corrected Spearman | sealed-impl (buggy) | Cramér's V | CI₉₅ (classes) |
|---|---|---|---|---|
| **arity-4 Min-Ones** (n=3105) | **−0.140** | −0.071 | **0.516** | **(−0.165, −0.114)** ✓ excludes 0 |
| v1 arity-≤3 Min-Ones (n=55) | −0.564 | −0.428 | 0.692 (0.459 pooled) | (−0.795, −0.328) |

**Verdict: REPLICATED but STRONGLY ATTENUATED.** The direction holds — the CI (−0.165, −0.114) excludes zero
(p≈5×10⁻¹⁵) — so the anti-canon coupling (harder-to-approximate Min-Ones relations tending to be *easier* to
parameterize) is real on the natural arity-4 population, not an arity-≤3 artifact. But the magnitude fell hard, from
v1's corrected **−0.564** to **−0.140**. Notably the *association* strengthened (Cramér's V 0.459→**0.516**) while the
*monotone* component weakened: at arity 4 the harder `poly-APX-complete` cell swings back toward W[1], breaking the
clean PO→W[1] / APX-complete→FPT trend that drove v1. **Open (one line, no commitment):** whether the attenuation is a
size/arity trend is a new question, not answered here.

The Max-Ones residual is, again, essentially nothing (corrected Spearman **+0.023**, V 0.106) — the "strong-vs-empty"
split is cleaner than ever under the corrected metric.

## 3. The construct-validity defect, and the cut-dependence it exposed

The sealed `_spearman` helper computed `argsort(argsort(·))`, which gives tied values *consecutive* ranks by array
position instead of averaging them — not Spearman's ρ on tied data. On the heavily-tied (approx-class × binary-param)
roster it partly measured array order; the tell is that the arity-4 point estimate fell **outside its own bootstrap
CI**, and the buggy Max-Ones arity-4 value was **+0.750** where the correct value is **+0.023**. It is logged as the
program's **second construct-validity error** (methods thread; the first was Pebble's pairwise blindness — same species,
"the machinery named the right concept and computed a different one").

Correcting it (tie-averaged ranks; verified against `scipy.stats.spearmanr`) re-scored v1's shipped direction numbers
and **flipped v1's prediction 6 from MISS to HIT** — which exposed the real pooled-level finding:

**The pooled direction is cut-dependent — that is the finding, not a nuisance.** On the same v1 population, two
theorem-motivated subtractions give **opposite signs**:

| pooled approx⟷param, arity-≤3 | corrected Spearman |
|---|---|
| raw (all 166 both-real rows) | +0.128 |
| **Cai–Chen cut** (remove the 11 forced (APX-complete, FPT) affine rows) | **+0.261** (canon-positive) |
| **bridge cut** (remove *all* affine rows) | **−0.184** (anti-canon) |

Same population, two theorem-forced removals, opposite signs. **The aggregate direction is not a stable property of the
population — it is a property of which theorem-forced structure you remove.** The only direction claim that holds across
**both arities, both cuts, and with the CI excluding zero everywhere** is the **Min-Ones non-affine residual, anti-canon**
(−0.564 at v1, −0.140 at arity 4). That is the decomposition's spine: **one robust directional finding, surrounded by
pooled estimates that are sign-unstable under cut choice.** (This is the version that survives a referee, whose first
move is to try the other cut.)

## 4. What re-scores, and where (dated corrections)

- **v1 pred 6: MISS → HIT** (`Prism-v1-findings.md` ledger + §3), same ruling as pred 5 — the seal said "Spearman,"
  tie-corrected is the faithful implementation; both numbers permanent; original epistemic standing kept
  (contamination-disclosed at seal). Corrected: raw 0.019→**0.128**, netted −0.005→**0.261**, V 0.255 in CI → HIT.
- **v1 direction numbers** revised (dated) in the findings, the four-wall note, and the preprint-bound statement:
  Min-Ones −0.428→**−0.564**, pooled −0.142→**−0.184**, Max-Ones +0.331→**+0.098**.
- **The "monotonicity did not return" sentence** (owner wording, ruled into the v1 decomposition on the buggy value)
  gets a dated correction naming its cause — recorded as an owner error downstream of the instrument bug, not quietly
  re-issued.

## Discipline honored

Prereg (`prereg_v33`) sealed before any arity-4 column; reproduction gate + NPI before the matrix; marginals-first (the
confound declared on the marginal); effective-n (CIs sized to the 4072 classes); per-objective before pooled; the affine
class traced; **both metric numbers (sealed-buggy + corrected) reported permanently**; the construct-validity defect
logged with its downstream-judgment contamination; the localization arm dropped at review, not measured. Artifacts:
`results/lattice/prism_v2_charges.json`, `prism_v2_matrix.json`. `is_weakly_separable` / `oracles.py` / eightfold
untouched; `finer.classify_boolean` read-only.
