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

## 4. The affine trace

The affine class is the throughline: **affine → counting=FP, param=FPT** (the off-diagonal — approx-hard/param-easy that
broke the tautology blocker in G1 and flattened v3's trend), with approx = APX-complete (Max-Ones) / Nearest-Codeword-
complete (Min-Ones). It is exactly this cell that (a) *is* the theorem-forced `affine⟹FPT` link the literal netting
missed (§3), and (b) when netted, *raises* the Min-Ones residual to 0.459 — the affine off-diagonal was masking a real
non-affine coupling. The same cell, load-bearing a third time.

## 5. Implications — posed as questions for ruling, not rewrites

- **For the v3 decomposition / four-wall note:** the approx⟷param coupling now decomposes into a **theorem-forced part**
  (the affine off-diagonal, `affine⟹FPT`) and a **residual part** (the non-affine coupling, 0.286 pooled / 0.459
  Min-Ones) that survives netting what the theorems force. Does this update v3's "weak, non-monotonic coupling" claim to
  "a weak coupling that is *partly theorem-forced and partly residual*", with the residual matching the canon's
  direction only after the theorem-forced anti-gradient is removed? (This is the careful claim you flagged: "matches
  the canon's direction after removing what theorems force," not "the gradient reproduces.")
- **For the I6 program:** the localization headline is untestable at arity ≤3; an arity-4 roster is the natural next
  experiment. Authorize a spec, or leave localization-absorption as an open question?

Neither is rewritten here.

## Discipline honored

Prereg (`prereg_v32`) sealed before any column computed; NPI + v3-reproduction gates before the matrix; marginals-first
(the I6 untestability declared on the marginal); effective-n (V's CI sized to the 90 classes / per-stratum counts, not
the 270 rows); **both residual sets reported permanently**; the netting completed *per its sealed design* (the bridge
belongs to a layer the prereg defined), the sequence stated (sealed → executed → incomplete → completed); the refuted
structural claim scored as a dated miss; spec-defect #4 logged; `is_weakly_separable` / `oracles.py` / eightfold
untouched; `finer.classify_boolean` imported read-only. Artifacts: `results/lattice/prism_charges.json`,
`prism_matrix.json`.
