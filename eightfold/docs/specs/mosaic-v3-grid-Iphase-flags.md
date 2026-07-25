# Mosaic v3 grid (G0) — I-phase flags to pin before the prereg seals

**Status:** pre-I-phase flags, not a seal. Recorded 2026-07-24 from the Mosaic-v2 phantom-retirement incident
(methods-thread instance 16). To be pinned into the G0 prereg when it is written (after the owner's Strata v2
spec). Nothing here is sealed; it is the carry-forward the incident produced.

---

## Flag 1 (consequential) — parameterized is objective-INDEPENDENT by oracle construction; part of prediction 2 is definitional, not empirical

**The fact.** On the single-relation Boolean roster the grid uses, the parameterized charge is a *relation-level*
property: `objective_oracles.parameterized(rels)` (Marx / BM14 OCSP weak-separability) takes **no objective
argument**. Approximation is objective-dependent (KSTW Max-Ones vs Min-Ones); parameterized is not. Empirically
this is exact — **param-flip ≡ 0/83** across the both-real symmetry-class pairs (methods-thread instance 16).

**The trap it creates for G0's prediction 2.** The grid's prediction 2 (as specced) predicts *the coupling
loads weakly on the objective main effect*. For the **parameterized** charge on this roster, that main-effect
loading is **zero by construction, not weakly-by-measurement** — the oracle's type signature forces it. A
variance decomposition that reports "parameterized does not vary with objective" as a *finding* is claiming
**theorem-forced credit**: it is the defect-#15 / Cai–Chen netting trap appearing one level up, in the
instrument's own plumbing rather than in the data. A charge that is constant by an oracle's construction
cannot be an empirical result about that constant.

**What G0's prereg must do.** Split prediction 2 into its two arms and label each:
- **approximation × objective** — genuinely empirical (approx *is* objective-dependent; 37/83 classes flip).
  The main-effect loading here is a real measurement and a real bet.
- **parameterized × objective** — **definitional / oracle-forced to zero on this roster.** Not a bet; declared
  as a type-signature fact, netted out of the decomposition's "explained by objective" credit before any
  variance is attributed. If the grid ever swaps in an objective-dependent parameterized oracle, this arm
  becomes empirical again and must be re-opened.

Pin this distinction at I-phase or the decomposition will score a forced constant as a finding.

---

## Flag 2 (banked wording — declined as a one-off, reserved for the grid) — the objective-sensitivity × param-value sub-analysis

The Mosaic-v2 retirement surfaced the one *non-degenerate* paired statistic available on the frozen roster,
and the owner **declined to compute it as a one-off** (2026-07-24) precisely because it is a cell of the
grid's own sealed territory — running it outside G0's prereg would pre-compute a fragment of the grid and
contaminate G0's bets with a peeked answer. **Banked verbatim for the G0 prereg as a named sub-analysis:**

> Over the 83 both-real symmetry-class pairs, is a class's **approximation objective-sensitivity**
> (approx-flip: does Min-Ones vs Max-Ones change the approximation charge?) associated with its
> **parameterized value** (relation-level FPT vs W[1])? 2×2 = (approx-flip Y/N) × (param FPT/W[1]); exact OR
> with CI at effective-n = pairs. This tests whether *the objective mattering for approximability* co-occurs
> with *param-hardness* — a real, non-degenerate question, and a direct cell of the grid's
> approx-objective-sensitivity × relation-level-charge decomposition.

Census already in hand (do not recompute outside the seal): 83 pairs, 37 approx-flips, param marginal
FPT 80 / W[1] 86 over the 166 both-real rows. Compute **once, inside G0**, with the full decomposition around
it — never as a standalone.

---

---

## Flag 3 — the Bridge Ledger pinning pass (I3) ran; its results bind G0's calibration layer

I3 was specified as **one pass, two consumers** (Anatomy S0 + Mosaic v3 G0). It ran on 2026-07-24 and is
recorded in full at `docs/findings/bridge-ledger-v1.md` §9. **15 cells examined: 3 pinned clean, 9 pinned
only with correction, 3 unpinnable.** Four consequences bind G0 directly:

1. **A NETTED calibration cell asserted the opposite of a theorem.** Ledger §2.counting read "planar
   matchings/permanent in P and NC" — but *counting matchings in a planar graph is #P-complete* (Jerrum
   1987). The tractable object is planar **perfect** matchings. Per Ledger §8.1, NETTED cells are the grid's
   known-answer layer where "failures are pipeline bugs by definition" — so shipped as-is, a **correct**
   pipeline would have been flagged as buggy and the instrument "corrected" toward the error. **G0 must take
   its calibration values from §9's corrected wording, never from the §1–§7 tables as originally written.**

2. **§1.decision and §1.parameterized-tw are ONE theorem, not two.** Both are Courcelle 1990 Prop. (4.14).
   Counting them as independent calibration points inflates the known-answer layer with one theorem wearing
   two hats. `anatomy.independent_bridge_count()` collapses the pair mechanically; G0 should use it or
   replicate the rule.

3. **Expansion cannot be a per-row feature — this is Flag 1's failure mode a second time.** Ledger
   §5.approximation is **UNPINNED for a structural reason**: Dinur's Preprocessing Lemma manufactures the
   expansion hypothesis on *any* constraint graph, so no instance is excluded for lacking it or charged for
   having it. Like the objective-independent param oracle in Flag 1, this is a proposed feature that
   **cannot vary in the way a bet would need**. If G0 ever reaches for an expansion covariate, it must first
   pass the same census-before-seal gate.

4. **§6.kernel's correction vindicates Mosaic P6 as sealed.** "FPT ⟺ some kernel" holds only for
   **decidable, non-trivial** problems, and g(k) is an arbitrary computable function — so the equivalence
   "carries no efficiency content." The informative contrast really is **poly- vs no-poly kernel within
   FPT**, which is exactly what P6 measured. No change to P6; the ledger row is what needed fixing.

**Also carried:** `engine_type`'s bridge (§3.decision) may be cited only in its corrected form — the
algebraic characterization (SD(∧) sufficiency Barto–Kozik JACM 2014; necessity **Larose–Zádori 2007**) with
its **finite core + all-singletons** hypotheses. "Bounded width ⟺ local consistency" is Barto–Kozik's
*definition*, not a theorem, and must not be presented as an empirical bridge.

---

## Carry-forward summary

1. Prediction 2 splits: approx×objective empirical; **param×objective definitional (oracle-forced zero) —
   net it out, don't score it.**
2. The objective-sensitivity × param-value 2×2 is a **named G0 sub-analysis**, banked, computed once inside
   the seal.
3. Both trace to the same root — an outcome variable frozen by the instrument's construction — which is why
   **census-before-seal (confirm every outcome variable can vary) is now mandatory at every paired design's
   I-phase** (methods-thread instance 16).
