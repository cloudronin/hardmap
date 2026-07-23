# Ferry (T3.1 canon extension) — I-phase memo

**For owner review BEFORE any canon-side measurement** (Ferry spec §7: "the I-phase memo reviewed before any
measurement"). The I-phase is the load-bearing, non-mechanical step, and it returns a **decisive definitional
finding at $0 measurement cost**: `tuple_dispersion` is *orthogonal* to the canon's approximation/parameterized
charges, so the cross-row prediction (F1–F4) is not well-posed. Recommendation and options at the end.

## I-F1 — what is "the relation" per gradient-carrying row (coverage)

47 gradient-carrying rows (real `approximation` AND real `parameterized`). Pinning the fixed-arity local constraint
relation under the atlas's canonical encoding:

- **16 rows have a defensible local relation** (Boolean/arity-2–3, or domain-3): the vertex-cover family → OR-2;
  independent-set / clique → NAND-2; max-cut / max-directed-cut → XOR-2; 3-coloring → ≠ over domain-3; 3-SAT → OR-3;
  NAE-SAT → NAE-3; 1-in-3-SAT → 1-in-3; MAX-2LIN → 2-affine.
- **31 rows are `n.a.` by typing** — no local relation, declared not forced (first-class outcome, Ferry §5): general
  SAT (unbounded width); the global graph problems (Steiner, feedback-vertex/arc-set, longest-path, spanning-tree,
  matching, editing, subgraph-iso, dominating-set [variable-arity], treedepth, densest-k-subgraph, …); and all the
  numeric/optimization rows (TSP, set-cover, knapsack, subset-sum, bin-packing, makespan, Kemeny, …). **This is the
  first substantive result: the canon's gradient-carrying rows are MOSTLY global/numeric problems whose hardness is
  not carried by any local constraint relation.**

Coverage artifact: `results/landscape/ferry_iphase_coverage.json`.

## I-F2 — is `tuple_dispersion` comparable AND discriminating across the rows? (the decisive item)

The 16 defensible-relation rows collapse to **five distinct dispersion values**. The charges present at each:

| disp | # rows | approximation charges present | parameterized |
|---|---|---|---|
| 0.571 | 1 | APX-complete | FPT |
| 0.600 | 1 | APX-complete | FPT |
| **0.667** | **9** | **APX-complete, PTAS, inapprox** | **FPT, W[1]** |
| 0.800 | 2 | APX, inapprox | FPT |
| 1.000 | 3 | APX-complete | FPT |

**The modal dispersion value (0.667, 9 of 16 rows) spans the ENTIRE approximability spectrum** — from PTAS
(polynomial-time approximation scheme, the easy end) through APX-complete to inapprox (the hardest end) — **and both
parameterized classes.** The scalar value 0.667 is charge-uninformative.

**Two measured counterexamples, both directions:**
- **Same relation-value, opposite charges:** vertex-cover (OR-2, disp 0.667) is APX-complete / FPT; independent-set
  (NAND-2, disp 0.667) is inapprox / W[1]. Their edge relations are complementary — identical dispersion — and their
  charges are opposite. `tuple_dispersion` cannot tell them apart.
- **Different relation-values, same charges:** 3-SAT (OR-3, 0.571), NAE-SAT (NAE-3, 0.600), 1-in-3-SAT (1-in-3,
  0.667) all read APX-complete / FPT. Dispersion varies; the charge does not.

**I-F2 verdict:** the values are arithmetically comparable but **orthogonal to the target.** A dispersion value that
does not track the charge cannot support a cross-row charge prediction (Ferry §1, I-F2). This is not a coverage gap
(that is I-F1's 31 `n.a.`); it is that even the covered rows carry no charge signal in the scalar.

## I-F3 — charge-object targeting

`tuple_dispersion` is computed from the *constraint relation*, which is **shared** across a problem's decision,
optimization (approximation), and parameterized objects. The counterexamples show the shared relation does not
determine the charge: the charge is fixed by the **global problem structure** — what is optimized, how it is
parameterized — not by the local relation. Vertex-cover and independent-set share the edge-relation *type* and
differ only in objective; that difference is exactly where their charges diverge, and it is invisible to the scalar.

## Anchor calibration (§2) — transports, but that is not the problem

Calibration 1 (canon-side disp = census-side disp) passes trivially for the unambiguous anchors (XOR-SAT, Horn-SAT,
NAE-SAT encode the *same* relation both sides → same value); Calibration 2 (XOR at the dispersion extreme) holds.
**The encoding transports fine.** The extension does not fail because the scalar mis-transports; it fails because the
scalar is orthogonal to the charges once transported.

## The finding, and why it was predictable

This is the **canon-scale confirmation of the program's own established result**: complexity is a *clone-level*
property and terrain is *relation-level* (Sprint 4.6). The canon's approximation/parameterized charges live at a
level **above** even the clone — the *global problem* (objective + parameterization) — and the relation-level scalar
(`tuple_dispersion`, the reach proxy from T1.4) cannot reach it. The reach line already showed reach ≈ f(relation);
Ferry shows the canon's charges ≠ f(relation). The cheap probe is **census-local**: it prices relation structure,
and the census varies relation structure meaningfully, but the canon's gradient is carried by global structure the
relation does not encode.

## Kill assessment (Ferry §6) and recommendation

- **Kill 2 (definitional collapse):** 16 rows → 5 dispersion values, the modal one charge-uninformative. Fires.
- **Kill 3 (incomparability→non-support):** the scalar's variance is orthogonal to the charge variation. Fires.
- **Kill 1 (anchor failure):** does NOT fire — the encoding transports.

**The F4 "real kill" is answerable at the I-phase, definitionally, at $0.** The substrate hypothesis, tested via the
`tuple_dispersion` proxy on the canon, is **NOT SUPPORTED** — not as a uniform generic-difficulty proxy, but as an
*orthogonal* one: the scalar carries no charge signal, with measured counterexamples that are the bulk of the data,
not edge cases.

**Options for your ruling (before any prereg is sealed):**
1. **Accept the I-phase definitional finding** — the cheap probe is census-local; the canon's charges are
   global-problem-level, orthogonal to the relation scalar. Honest, measured, and consistent with the program's
   clone-vs-relation thesis. The reach line's end-state stands: instrument characterized, hypothesis's real test
   answered NOT-SUPPORTED-via-this-proxy at the canon, with the counterexamples on the record.
2. **Seal the prereg and run F1–F4 anyway** ($0 compute) to convert the I-phase reasoning into a *formally scored*
   F4 verdict (held-out by family, entailment-netted, against the uniform/null) — putting a correlation number on
   the orthogonality rather than resting on the counterexamples. Rigorous, cheap, and closes it by measurement as
   well as by definition.

I lean to **(2)** — it is $0 and it scores the program's real kill formally rather than by argument — but the
finding itself is already decisive, so **(1)** is legitimate. Nothing is sealed or measured pending your review.
