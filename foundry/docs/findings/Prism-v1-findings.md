# Prism v1 (G2, prereg_v32) — findings: the multi-charge matrix, and what nets to zero

Prism charged the natural arity-≤3 Boolean roster (Lattice v3's **90 symmetry classes**) with every oracle-derivable
charge — decision, counting, localization (bounded-width), parallelization, approx-counting, approximation (Max/Min-Ones),
parameterized — and asked whether any pattern beyond the approx⟷param coupling survives netting what the theorems force.
$0 compute; the theorems are the instrument; **only netted residuals are findings.** The result is a clean separation
of theorem-identity from residual, one untestable headline, and one methods catch.

## Predictions ledger (all 7 scored, including misses)

| # | prediction | verdict |
|---|---|---|
| 1 | NPI calibration — decision ∈ {P, NPC}, no intermediate | **PASS** (83 P / 7 NPC) |
| 2 | decision⟷counting nets to ≈ 0 (identity) | **HIT** — netted 0 |
| 3a | bounded-width⟷approximation raw ≥ 0.4, netted 0 (entailment finding) | **HIT** — raw **0.983** → netted **0** |
| 3b | bounded-width⟷parameterized nonzero netted residual | **UNTESTABLE** — see §2 |
| 4 | conditioning approx⟷param on bounded-width shrinks V ≥ half (the I6 headline) | **UNTESTABLE** — see §2 |
| 5 | approx⟷param is the outlier survivor | **MISS (literal) → HIT (bridge-completed)** — see §3 |
| 6 | Cai–Chen netting raises monotonicity, V in CI (v3 addendum) | **MISS** — V in CI (0.255), but Spearman 0.019 → **−0.005** |
| — | *sealed structural claim:* general weak-separability is orthogonal to the classical fingerprint | **MISS (dated 2026-07-23)** — see §3 |

Gates: NPI passed; the **v3-reproduction sanity gate passed** (approx⟷param V = **0.2555** on the 166 both-real rows,
reproducing v3 exactly — Prism reads the identical roster).

## 1. What the netting cleanly zeroes — the theorem-identities

On a single-relation Boolean roster the charges are functions of the polymorphism fingerprint, so raw couplings are
theorem-identities. The per-pair shared-input netting confirms it: every **classical × classical** pair
(decision⟷counting 0.165→0, decision⟷localization **1.0**→0) and every **classical × approximation** pair
(localization⟷approx **0.983**→0, counting⟷approx-counting **0.994**→0) nets to exactly 0. **Prediction 2 and
prediction 3a are the confirmations** — 3a is an *entailment finding*, not a coupling: bounded-width⟷approximation is
strong raw (0.983, driven by unbounded-width ⟺ feasibility-hard) but nets to 0 because **KSTW's inputs already contain
bounded-width's determinants {horn, dual-horn, bijunctive}** — the approximation classification *encodes* the localness
structure, so there is nothing left once you condition on it.

## 2. The I6 localization headline is untestable at arity ≤3 (and why that is the correct answer)

The corrected I3 bounded-width predicate — `(0-valid ∨ 1-valid) ∨ Horn ∨ dual-Horn ∨ bijunctive`, trivial-satisfiability
first — revealed that **bounded-width ⟺ tractability** on this roster: the only unbounded-width classes are the 7 NP-hard
ones, because the affine obstruction (the sole tractable-but-unbounded case) is *vacuous at arity ≤3 single relations*
(smallest witness is arity 4). So every param-defined (both-real) row is bounded-width, and **bounded-width has zero
variation on the rows carrying the coupling.** Consequently:
- **3b** (bounded-width⟷param): constant on the 83 param-real classes → **UNTESTABLE**.
- **4** (absorption): one bounded-width stratum among both-real rows → **UNTESTABLE**.

This is declared on the **marginal**, before any association is read — the discipline working, and the *corrected*
predicate is what exposed it (the naive `horn∨dual-horn∨bijunctive` would have manufactured spurious variation among the
0/1-valid relations). The I6 mechanism-test needs **arity ≥ 4**, where genuinely unbounded-width tractable relations
exist. Deferred to a separate experiment (Prism's sealed scope excludes roster extension).

## 3. The netting was completed mid-run, per its sealed design — and it changed prediction 5

**The sequence, honestly:** the prereg's per-pair netting was *sealed*, *executed* on the literal predicate each oracle
reads, *found incomplete* at the R2 gate, *completed* per the sealed named-bridge layer, with **both numbers shown**.

The literal netting left two large "survivors" — `counting⟷param` **0.736** and `approx_counting⟷param` **0.745**. These
are **not residuals**: `counting` and `approx_counting` read `affine`, and **affine ⟹ weakly-separable ⟹ FPT** (Marx
Ex 2.4), so `affine=FP` *forces* `param=FPT`. The literal-intersection netting missed it because `affine` and
`general_wsep` carry different names (spec-defect #4, methods thread). Completing the named-bridge layer with
`affine⟹weakly-separable` nets them out. Both residual sets, permanent:

| pair | raw | netted (literal, sealed-as-first-run) | netted (bridge-completed) |
|---|---|---|---|
| counting × param | 0.736 | 0.736 | **0.0** |
| approx_maxones × param | 0.314 | 0.314 | **0.0** |
| approx_counting × param | 0.745 | 0.745 | **0.127** |
| parallelization × param | 0.311 | 0.311 | **0.071** |
| approx_minones × param | 0.192 | 0.192 | **0.459** |
| approx⟷param (166-row headline) | 0.256 | 0.256 | **0.286** |

**Prediction 5: MISS (literal) → HIT (bridge-completed).** After the bridge, the approx⟷param coupling *is* the outlier
survivor (its non-affine Min-Ones residual is **0.459**, the largest of any pair; the headline residual is 0.286; the
largest non-approx pair is 0.165). But **not for the sealed reason.** The prereg's structural claim — parameterized is
the *only* charge with a determinant orthogonal to the classical fingerprint — is **refuted** (`affine` is a determinant
of param via the theorem), scored as a dated sealed-claim miss with the same standing as v3's direction miss. The
approx⟷param coupling survives because its *non-affine residual* is strongest, not because param is orthogonal.

**Prediction 6 (Cai–Chen)** is a genuine, contamination-disclosed miss: removing the 11 forced `(APX-complete, FPT)`
rows left V = 0.255 (within CI (0.148, 0.38) ✓) but Spearman went 0.019 → **−0.005** — netting the affine Max-Ones
off-diagonal did *not* raise monotonicity. The other off-diagonal cells (poly-APX/FPT, Nearest-Codeword/FPT) remain.

## 4. The affine trace — and the sharpest number Prism produced

The affine class is the throughline: **affine → counting=FP, param=FPT** (the off-diagonal — approx-hard/param-easy that
broke the tautology blocker in G1 and flattened v3's trend), with approx = APX-complete (Max-Ones) / Nearest-Codeword-
complete (Min-Ones). It is exactly this cell that (a) *is* the theorem-forced `affine⟹FPT` link the literal netting
missed (§3), and (b) when netted, *unmasks* the strongest coupling in the whole roster. The same cell, load-bearing a
third time.

**The Min-Ones residual is the sharpest single number Prism produced.** Netting the affine off-diagonal raises the
`approx_minones⟷param` residual to **V = 0.459** pooled (**0.692** within the non-affine stratum alone) — *higher* than
the raw approx⟷param (0.256) — and its direction (post-hoc descriptive, computed on the bridge-completed residual set,
not sealed; effective-n = 55 non-affine param-real classes) is **Spearman −0.428**. The cross-tab is explicit:
Min-Ones-**APX-complete** relations are mostly **FPT** (10:4), Min-Ones-**PO** relations mostly **W[1]** (1:35) —
*harder to approximate ⟷ easier to parameterize*, the **opposite** of the canon's positive gradient. So the affine
off-diagonal was not merely *inflating* the signal; it was **distorting its shape**: underneath it sits a moderately
strong, *anti-canon* coupling. The theorem-forced structure hid both a stronger magnitude and the opposite sign.

**All three Spearmans in this section are post-hoc descriptive** — computed *after* seeing the bridge-completed table,
carrying **no prereg standing** (the sealed direction bet, prediction 6, already missed). With that caveat, the split
between the objectives is **not a tension — it is strong-vs-empty.** The Min-Ones residual carries a strong anti-canon
coupling; the **Max-Ones** residual carries **essentially nothing** — within-stratum V ≈ 0, so its Spearman +0.331 is a
direction reading on a near-degenerate association (noise on nothing), **not** canon-aligned evidence to be set against
Min-Ones. Pooling the two gives Spearman −0.142, which is why the *aggregate* direction reads as unresolved. The honest
one-line summary is not "the objectives disagree" but: **one objective carries a strong anti-canon residual, the other
carries essentially nothing.**

## 5. Implications — the decomposition (owner-ruled 2026-07-23), and the direction it does *not* recover

**The decomposition, adopted.** The natural approx⟷param coupling splits into a **theorem-forced part** — the affine
off-diagonal (`affine ⟹ weakly-separable ⟹ FPT`, Marx Ex 2.4), netted away — and a **non-affine residual** (pooled
V **0.286**, Min-Ones V **0.459**) that survives netting everything the theorems force. The residual is *stronger* than
the raw number (0.256) suggested; **the affine off-diagonal was masking it, not producing it.** There is no
direction-match clause: the earlier careful phrasing ("matches the canon's direction after removing what theorems
force") is **contradicted by the one direction test that ran.** Prediction 6 missed — removing the theorem-forced
affine rows left Spearman at −0.005, monotonicity did not return — and the post-hoc bridge-completed direction (§4)
confirms it: pooled Spearman **−0.142**, and the load-bearing Min-Ones side runs *anti-canon* at **−0.428**. The
residual does not recover the canon's positive gradient; if anything its strong side runs against it. **Direction stays
an open question, not a recovered claim.** The honest gloss for v3's "weak, non-monotonic coupling": *partly
theorem-forced; the non-affine residual is the real object, magnitude 0.286 (Min-Ones 0.459), direction unresolved —
anti-canon on the load-bearing Min-Ones side.*

**What this does to the canon-vs-computation verdict — register it, it is not small.** The decomposition is no longer
"a faint version of the canon's positive pattern plus theorem-forced noise." The structure is sharper and stranger:
*the theorems force one anti-gradient structure* — the affine off-diagonal, approx-hard/param-easy — *and underneath
it the free (non-affine) residual is also anti-canon on its strong side* (Min-Ones −0.428). So **the strongest netted
coupling in the natural Boolean universe runs opposite the canon's direction.** Hedged to this population (arity ≤3
Boolean single relations) and this objective (Min-Ones), the reading moves from *"the natural universe carries a faint
version of the gradient"* to *"the natural universe carries an **anti**-gradient where it carries anything at all"*:
whatever produces the canon's clean positive approx⟷param gradient, the natural universe not only fails to reproduce it,
its residual leans the other way. **This is the single most surprising number the program now owns, and the preprint's
decomposition section should carry it as a sentence, with the hedge.**

**Open, parked (one line, no commitment).** The Min-Ones anti-canon pattern — *inapproximability co-occurring with
FPT* — is a mechanism question Pebble had closed and the canon never posed (the canon never showed the pattern): why, in
nature, would hard-to-approximate Min-Ones relations tend to be *easier* to parameterize? Reopened here, left open.

**The arity-4 experiment, authorized.** The I6 localization headline (3b/4) is untestable at arity ≤3 because
bounded-width ⟺ tractability there (the affine obstruction is vacuous below arity 4). An arity-4 roster is where a
genuinely unbounded-width tractable relation first exists, so localization-absorption becomes testable. The spec is
written — `docs/specs/Absorption-arity4-spec.md` — and **runs after the preprint** (owner ruling: spec now, execute
later). Its I-phase must bound the symmetry-class count before committing to full charging (2^16 relations is a real
enumeration lift), with a sampled fallback if enumeration exceeds its timebox.

## Discipline honored

Prereg (`prereg_v32`) sealed before any column computed; NPI + v3-reproduction gates before the matrix; marginals-first
(the I6 untestability declared on the marginal); effective-n (V's CI sized to the 90 classes / per-stratum counts, not
the 270 rows); **both residual sets reported permanently**; the netting completed *per its sealed design* (the bridge
belongs to a layer the prereg defined), the sequence stated (sealed → executed → incomplete → completed); the refuted
structural claim scored as a dated miss; spec-defect #4 logged; `is_weakly_separable` / `oracles.py` / eightfold
untouched; `finer.classify_boolean` imported read-only. Artifacts: `results/lattice/prism_charges.json`,
`prism_matrix.json`.
