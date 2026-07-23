# Ferry (T3.1) — findings: the canon extension of the relation-level scalar

The reach line ended with a cheap probe — `tuple_dispersion`, a pure relation-level property (T1.4). Ferry carried
it to the canon's gradient-carrying rows to test the substrate hypothesis where the approx⟷param gradient actually
lives. The answer is decisive, and the most important part of it is not the kill.

## 1. The headline: the canon's gradient lives where no local relation exists

**31 of 47 gradient-carrying canon rows have no defensible local constraint relation at all.** Steiner tree, TSP,
knapsack, subset-sum, set-cover, feedback vertex/arc set, longest path, spanning-tree, matching, bin-packing,
makespan, Kemeny — their hardness is carried by **global structure** (an objective over the whole instance, a
connectivity or acyclicity or ordering requirement) or by **numeric magnitude**, not by any local constraint that a
relation could name. This is not a coverage gap to apologize for; it is a **structural fact about the canon**: the
interesting rows — the ones carrying the approximation⟷parameterized gradient the program set out to explain — are
precisely the ones a relation-level quantity cannot see.

That reframes the whole substrate program in one line: **it was reaching for something the canon's gradient-carrying
rows do not have.** A propagation quantity read from constraint structure can only price problems whose difficulty
lives in that structure; the canon's does not.

## 2. Where a relation does exist, the scalar is orthogonal to the charges

For the **16 rows that do admit a local relation**, `tuple_dispersion` carries no charge signal — established two
independent ways:

**Definitionally (I-phase, $0, by construction).** The 16 rows collapse to five dispersion values; the modal value
**0.667 (9 rows) spans PTAS → APX-complete → inapprox and both FPT/W[1]**. The cleanest possible witness:
**vertex-cover (edge relation, disp 0.667) is APX-complete / FPT; independent-set (complementary edge relation, same
disp 0.667) is inapprox / W[1]** — identical relation, opposite charges on both gradient axes. And in the other
direction, 3-SAT / NAE-SAT / 1-in-3-SAT carry different dispersions but identical charges.

**By confirmatory measurement (F1–F4, prereg_v28, held-out-by-family + permutation).** This did not *decide* anything
the definition had not already settled — it puts a scored number next to the counterexample table for a reader who
wants one:

| test | charge | Spearman(disp, charge) | perm-p | within-graph |
|---|---|---|---|---|
| F1 | landscape | −0.30 | 0.49 | −0.04 |
| **F2** | **approximation** | **0.035** | **0.93** | **−0.13** |
| **F2** | **parameterized** | **0.162** | **0.86** | **−0.20** |

**F3 (flagship):** conditioning on `tuple_dispersion` does **not** shrink the approx⟷param association (no
shrinkage) — the scalar explains none of the coupling. **F4 verdict: ORTHOGONAL** — not even a uniform
generic-difficulty proxy; the scalar's variance is simply perpendicular to the charges.

## 3. The kill

The substrate hypothesis, tested via the `tuple_dispersion` proxy on the canon, is **NOT SUPPORTED**. Propagation —
as read by this relation-level probe — does not explain the charges. (Kills 2 and 3 of the Ferry spec; kill 1, anchor
transport, did **not** fire — the encoding is fine, so this is a real orthogonality, not an artifact of a mis-encoded
scalar.)

## 4. What endures — a twice-measured structural claim

Sprint 4.6 established, in the **census**, that complexity is a clone-level property while terrain is relation-level —
a relation-level quantity cannot reach clone-level complexity. Ferry establishes the **same thing at canon scale**,
and the witnesses are not toy relations: **vertex-cover and independent-set are the pair that carry the atlas's
flagship approx⟷param gradient.** The claim — *hardness lives above the level a constraint relation can name* — is
now measured twice, in two independently-built worlds, with the canon's most load-bearing rows as the evidence. That
structural claim is **more durable than the substrate hypothesis it kills.**

## 5. The honest resting position

Propagation-via-this-proxy does not explain the charges. **The approx⟷param gradient remains unexplained** — the
program's central unexplained coupling is still unexplained. But the *reason* it remains unexplained is now better
characterized than before: it lives on **global and numeric structure that no local constraint relation encodes**,
and a relation-level probe is orthogonal to it by construction, not by bad luck. The program did not find the
substrate; it found, and measured twice, why a relation-level substrate cannot be it.

## Coverage (deliverable) + discipline

- **47 gradient rows → 16 CSP-local + 31 `n.a.`-by-typing** (`ferry_iphase_coverage.json`); the `n.a.` set is the
  headline, not a failure.
- **Discipline honored:** the F-phase was sealed (prereg_v28) as **confirmatory, not adjudicative** — the record
  states the I-phase settled orthogonality definitionally; anchors transport (calibration passed); held-out by
  family; permutation-tested; `n.a.`-by-typing first-class; $0 compute. The kill is scored by measurement *and* by
  definition, and the two agree.

## 6. The methodological lesson (the most useful sentence Ferry produced)

Why did three sprints go into relation-level instruments? Because the **census was chosen precisely because local
structure is decisive there.** Schaefer and Bulatov–Zhuk say it by theorem: on a fixed constraint language, the
constraint language *determines* the decision complexity. We picked that world for being bias-free and fully
classifiable — and **the very property that made it a good roster (local determinism) made it unrepresentative for
this question.** Generalizing from a domain *selected for local determinism* to a domain where the **objective is a
separate object** from the constraints is the actual methodological error.

And it was visible in our own oracle columns the whole time. The census's **approximation** charge did **not** fall
out of Schaefer — `oracles.py` derives it from **"KSTW 2001 / Håstad 2001"** (Max-CSP hardness-of-approximation),
and canon-side the same charge cites Håstad, Dinur–Safra, Goemans–Williamson, and Khot's UGC. The decision charge
comes from the algebraic dichotomy; the approximation charge needed an **entirely separate body of gap-based
machinery.** That divergence — one charge from the constraint algebra, another from PCP/UGC — was the tell that the
objective is not a function of the constraints, and we did not read it until Ferry forced it. This paragraph is
worth more to a future reader than the kill.

## 7. The cheapest calibration standard: vertex-cover / independent-set

The witness pair is now the program's **first gate on any future candidate measure.** Same constraints
(complementary edge relations), *complementary objectives*, **opposite charges on both axes** (APX-complete/FPT vs
inapprox/W[1]). **Any measure that assigns those two the same value is dead before implementation** — exactly as
`tuple_dispersion` was (both 0.667). It is a ten-second test that would have saved a spec cycle, and it should be run
on anything proposed next *before* it is built.

## 8. Where the search goes, if it continues (unauthorized — specs required)

The kill is specific: a *relation-only* or *objective-only* measure cannot work; what could is a measure of
**objective-and-constraints jointly.** Two candidates have real theory behind them and both **pass the §7 gate by
construction** (they see the objective, which is what separates the witness pair):

- **Objective decomposability over the constraint structure** — whether the objective is a separable sum through
  globally-coupled conditions, or is itself globally coupled. Distinguishes vertex-cover (cover-all-edges, a global
  covering objective) from a local-satisfaction objective.
- **Gap behavior under complementation** — the mechanism that *actually* separates the witness pair, and the reason
  the field needed **gap-preserving reductions as separate machinery** (§6's Håstad/UGC tell). This is the
  physically-right candidate.

Both are computable from definitions ($0), both have prior art in the **MAX-SNP / syntactic-approximation-class**
line (Papadimitriou–Yannakakis, Khanna–Motwani–Sudan–Vazirani) that a bridge hunt must clear *before* any novelty
language, and **both are unauthorized until specced.** Nothing here runs on the strength of this finding.

**Ferry rests.** The approx⟷param gradient stays unexplained — and for the first time we can say precisely what
*kind* of thing could explain it: not a property of the constraints, and not a property of the objective, but a
property of how the objective sits on the constraints.
