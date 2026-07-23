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
| 6 | Cai–Chen netting raises monotonicity, V in CI (v3 addendum) | **MISS → HIT** (re-scored 2026-07-23, corrected metric) — V=0.255 in CI ✓; Spearman rose **0.128 → 0.261** (sealed-buggy: 0.019 → −0.005). See correction note. |
| — | *sealed structural claim:* general weak-separability is orthogonal to the classical fingerprint | **MISS (dated 2026-07-23)** — see §3 |

Gates: NPI passed; the **v3-reproduction sanity gate passed** (approx⟷param V = **0.2555** on the 166 both-real rows,
reproducing v3 exactly — Prism reads the identical roster).

> **⚠️ Dated correction (2026-07-23) — construct-validity error #2 (methods thread), all Spearman/direction numbers.**
> Every Spearman in §3–§5 was computed with a defective statistic (`argsort(argsort(·))`, which gives tied values
> consecutive ranks by array position — not Spearman's ρ on tied data; caught at Prism v2's arity-4 scoring, where the
> point estimate fell outside its own CI). Corrected to a tie-corrected Spearman (verified vs `scipy`). **The
> conclusions mostly strengthen, but two things change substantively: (i) prediction 6 re-scores MISS → HIT** (raw
> 0.128, netted 0.261 — monotonicity *does* rise under Cai–Chen netting); **(ii) the pooled direction is revealed to be
> cut-dependent** (§5). Corrected values, this note's authority: Min-Ones non-affine residual **−0.428 → −0.564**,
> pooled **−0.142 → −0.184**, Max-Ones **+0.331 → +0.098**. Both numbers (sealed-buggy + corrected) are kept
> everywhere, per the owner ruling; the seal said "Spearman" and the tie-corrected form is its faithful implementation.
> Full re-analysis: `Prism-v2-findings.md` §3.

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

**Prediction 6 (Cai–Chen) — originally scored MISS, re-scored HIT on 2026-07-23 (corrected metric; see the correction
note above).** Removing the 11 forced `(APX-complete, FPT)` rows leaves V = 0.255 (within CI (0.148, 0.38) ✓); under the
**tie-corrected** Spearman the pooled monotonicity **rises 0.128 → 0.261** — netting the affine off-diagonal *does* raise
monotonicity, the sealed bet's HIT condition. The original MISS was an artifact of the defective statistic (sealed-buggy
Spearman 0.019 → −0.005). This does **not** mean "the gradient reproduces": the rise is a *pooled, cut-specific* result
(remove these 11 rows and monotonicity goes up; remove *all* affine and it goes anti-canon — §5), and it coexists with
the anti-canon Min-Ones residual (§4). Both numbers kept, per the owner ruling.

## 4. The affine trace — and the sharpest number Prism produced

The affine class is the throughline: **affine → counting=FP, param=FPT** (the off-diagonal — approx-hard/param-easy that
broke the tautology blocker in G1 and flattened v3's trend), with approx = APX-complete (Max-Ones) / Nearest-Codeword-
complete (Min-Ones). It is exactly this cell that (a) *is* the theorem-forced `affine⟹FPT` link the literal netting
missed (§3), and (b) when netted, *unmasks* the strongest coupling in the whole roster. The same cell, load-bearing a
third time.

**The Min-Ones residual is the sharpest single number Prism produced.** Netting the affine off-diagonal raises the
`approx_minones⟷param` residual to **V = 0.459** pooled (**0.692** within the non-affine stratum alone) — *higher* than
the raw approx⟷param (0.256) — and its direction (post-hoc descriptive, computed on the bridge-completed residual set,
not sealed; effective-n = 55 non-affine param-real classes) is **Spearman −0.564** (tie-corrected; sealed-buggy value was
−0.428, corrected 2026-07-23 — see the correction note). The cross-tab is explicit:
Min-Ones-**APX-complete** relations are mostly **FPT** (10:4), Min-Ones-**PO** relations mostly **W[1]** (1:35) —
*harder to approximate ⟷ easier to parameterize*, the **opposite** of the canon's positive gradient. So the affine
off-diagonal was not merely *inflating* the signal; it was **distorting its shape**: underneath it sits a moderately
strong, *anti-canon* coupling. The theorem-forced structure hid both a stronger magnitude and the opposite sign.

**All three Spearmans in this section are post-hoc descriptive** — computed *after* seeing the bridge-completed table,
carrying **no prereg standing** — and all three are now the **tie-corrected** values (sealed-buggy −0.428 / +0.331 /
−0.142 kept in the correction note). With that caveat, the split between the objectives is **not a tension — it is
strong-vs-empty.** The Min-Ones residual carries a strong anti-canon coupling (**−0.564**); the **Max-Ones** residual
carries **essentially nothing** — within-stratum V ≈ 0, so its Spearman **+0.098** is a direction reading on a
near-degenerate association (noise on nothing), **not** canon-aligned evidence to be set against Min-Ones. Pooling the
two gives Spearman **−0.184** — but the pooled direction is **cut-dependent** (§5): remove a *different* theorem-forced
structure and its sign flips, so **no aggregate direction claim is made.** The honest one-line summary is not "the
objectives disagree" but: **one objective (Min-Ones) carries a strong anti-canon residual, the other carries essentially
nothing.**

## 5. Implications — the decomposition (owner-ruled 2026-07-23), and the direction it does *not* recover

**The decomposition, adopted.** The natural approx⟷param coupling splits into a **theorem-forced part** — the affine
off-diagonal (`affine ⟹ weakly-separable ⟹ FPT`, Marx Ex 2.4) — and a **non-affine residual** (pooled V **0.286**,
Min-Ones V **0.459**) that survives netting everything the theorems force. The residual is *stronger* than the raw
number (0.256) suggested; **the affine off-diagonal was masking it, not producing it.**

> **Dated correction (2026-07-23) — owner error, named as such.** This paragraph originally read *"Prediction 6 missed —
> removing the theorem-forced affine rows left Spearman at −0.005, monotonicity did not return … Direction stays an open
> question."* That was an owner sentence, **ruled into the decomposition on the sealed-implementation Spearman**
> (construct-validity error #2, the buggy `argsort` statistic). Revised on the corrected metric: **prediction 6
> re-scores HIT** — pooled monotonicity *rises* **0.128 → 0.261** under Cai–Chen netting. The "direction does not come
> back" framing built on that MISS is **withdrawn**, and replaced by the cut-dependence finding below. Owner errors are
> recorded as owner errors; that discipline does not bend because the error was downstream of an instrument bug.

**The pooled direction is cut-dependent — that is the pooled-level finding, not a nuisance.** On the same population,
two theorem-motivated subtractions give **opposite signs**: the **Cai–Chen cut** (remove the 11 forced (APX-complete,
FPT) rows) → **+0.261** (canon-positive); the **bridge cut** (remove *all* affine) → **−0.184** (anti-canon). The
aggregate direction is **not a stable property of the population — it is a property of which theorem-forced structure
you remove.** No aggregate direction claim is made.

**The one robust directional finding** — the only claim holding across **both arities, both cuts, with the CI excluding
zero everywhere** — is the **Min-Ones non-affine residual, anti-canon**: **−0.564** at v1 (arity ≤3), **−0.140** at
arity 4 (`Prism-v2-findings.md`; replicated but strongly attenuated). Gloss for v3's "weak, non-monotonic coupling":
*partly theorem-forced; the non-affine residual is the real object (Min-Ones V 0.459), its one robust directional signal
(Min-Ones) runs anti-canon; the pooled direction is sign-unstable under cut choice and is not identified.*

**What this does to the canon-vs-computation verdict — register it, it is not small.** The natural universe's **one
robust directional signal runs opposite the canon's** — on the **Min-Ones** objective, at **two sizes** (−0.564 at
arity ≤3, −0.140 at arity 4, both with the CI excluding zero). That is the sharp, referee-proof claim, and it is
deliberately **not** an aggregate one: the pooled direction is cut-dependent (above), so "the natural universe carries
an anti-gradient" holds specifically for the **Min-Ones residual**, not for the population in aggregate. Hedged that way
the reading still moves decisively past *"a faint version of the gradient survives outside the canon"* — whatever
produces the canon's clean positive approx⟷param gradient, the natural universe's one robust directional residual leans
the **other** way. **The preprint's decomposition section leads with this Min-Ones finding and demotes the pooled
direction to a cut-dependence exhibit** — both cuts (+0.261 Cai–Chen, −0.184 bridge) shown side by side, the pooled sign
explicitly *not identified*, no aggregate direction claim. The strong sentence the paper keeps: *the natural universe's
one robust directional signal runs opposite the canon's, on the Min-Ones objective, at two sizes.*

**Open, parked (one line, no commitment).** The Min-Ones anti-canon pattern — *inapproximability co-occurring with
FPT* — is a mechanism question Pebble had closed and the canon never posed (the canon never showed the pattern): why, in
nature, would hard-to-approximate Min-Ones relations tend to be *easier* to parameterize? Reopened here, left open.

**The arity-4 experiment — ran as Prism v2 (`Prism-v2-findings.md`, prereg_v33; update 2026-07-23).** The I6
localization headline (3b/4) is untestable at arity ≤3 because bounded-width ⟺ tractability there. At arity 4 a genuinely
unbounded-width tractable relation first exists — but on review the localization *absorption* test turned out **still not
askable**: on the param-real rows `unbounded-width = purely-affine` (Schaefer), which the affine bridge nets out, so the
arm was **dropped from the seal** (the Prism v2 spec supersedes the earlier `Absorption-arity4-spec.md`). Prism v2 was
re-scoped to the **anti-canon Min-Ones replication**, which is what the −0.140 arity-4 value above reports:
**REPLICATED but strongly attenuated.**

## Discipline honored

Prereg (`prereg_v32`) sealed before any column computed; NPI + v3-reproduction gates before the matrix; marginals-first
(the I6 untestability declared on the marginal); effective-n (V's CI sized to the 90 classes / per-stratum counts, not
the 270 rows); **both residual sets reported permanently**; the netting completed *per its sealed design* (the bridge
belongs to a layer the prereg defined), the sequence stated (sealed → executed → incomplete → completed); the refuted
structural claim scored as a dated miss; spec-defect #4 logged; `is_weakly_separable` / `oracles.py` / eightfold
untouched; `finer.classify_boolean` imported read-only. Artifacts: `results/lattice/prism_charges.json`,
`prism_matrix.json`.
