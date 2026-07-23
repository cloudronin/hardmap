# G1 — Can the approx⟷param gradient be tested on a *generated* roster? (I-phase memo)

**Status:** Investigation memo. Literature + feasibility only. No roster, no measurement, no prereg was produced,
and none is authorized by this memo. A BUILDABLE verdict authorizes a *spec*, not a roster.
**Discipline:** R20 — every classification is pinned to a primary source and the load-bearing cross-tabulation
(§I-G1) is reader-checkable. Timebox 3h; the two load-bearing items (I-G1, I-G2) resolved well inside 2h, so the
verdict is on the merits, not by timebox.

---

## The three possible verdicts (declared before investigating)

| Verdict | Meaning | Consequence |
|---|---|---|
| **BUILDABLE** | both charges assignable to generated optimization problems from independent sources; witness test passes | a roster spec follows, with its own prereg + known-answer calibration |
| **PARTIAL** | one axis has an oracle, the other is `open` | no gradient test; report which axis is missing |
| **NOT BUILDABLE** | charges share a source, or no oracle exists for optimization objectives | gradient testable only on curated rosters — a permanent scope limit, itself a finding |

## Verdict: **BUILDABLE**, scoped to CSP-style optimization objectives (Max-CSP / Max-Ones / Min-Ones).

The object the program needs *is* buildable, on one specific route, with one honest boundary. In one paragraph:

- Both charges are assignable to **generated** optimization problems from **independent** theoretical sources —
  approximation from the KSTW gap/PCP line, parameterization from the Marx / Bulatov–Marx W[1] line.
- The two sources are **different partitions** of the same Boolean languages, not one wearing two hats — proven by
  an **off-diagonal cell already in the program's own census oracle** (affine: approximation `inapprox`,
  parameterized `FPT`). That off-diagonal cell is exactly what was missing when Task-0 netting gave residual zero.
- The **witness test passes**: vertex-cover and independent-set — same constraint relation, complementary
  objectives — take **opposite values on both axes**, and a random-graph generator produces the pair.
- **The boundary (I-G3):** only *CSP-shaped* objectives (count satisfied constraints / count ones) are classified
  this way. The canon's 31 global-numeric rows (Steiner, TSP, knapsack, set-cover, feedback sets) have objectives
  that **no classification assigns charges to from independent sources** — they are out of reach of *any* generated
  roster, permanently. BUILDABLE buys a test on a population no human chose, but inside the CSP-objective universe,
  not the whole canon.

The rest of this memo is the four investigation items that land this verdict.

---

## Why every previous roster failed — and the escape, stated in the program's own oracle

The census's charges are functions of the constraint language Γ under **fixed** objectives. Read straight off
`foundry/foundry/oracles.py` (the pinned dichotomy oracle):

| Boolean class | decision (Schaefer 1978) | Max-CSP approximation (KSTW 2001 / Håstad 2001) | Exact-Ones parameterized (Marx 2005) |
|---|---|---|---|
| **affine** (XOR / linear) | **P** | **inapprox** (Max-3Lin, Håstad) | **FPT** (weakly separable) |
| bijunctive (2-SAT) | P | APX-complete | W[1] |
| Horn | P | APX-complete | W[1] |
| dual-Horn | P | APX-complete | W[1] |
| NP-hard (3-SAT, 1-in-3, …) | NP-complete | APX-complete | W[1] |

Task 0 found that netting the theorem-forced component of the approx⟷param association leaves residual **exactly
zero**. This table is *why*: with objectives fixed, both charge columns are (nearly) the single bit *affine-or-not*,
so any association between them is that one bit re-expressing itself. There is no residual variation to correlate.

**But look at the affine row.** Approximation reads `inapprox` (the hardest end); parameterized reads `FPT` (the
easiest end). The two charges **disagree** there. That single off-diagonal cell is the whole escape: it proves the
approximation partition and the parameterization partition are **not the same partition**. The reason the census
tautology bit is that the roster had only one bit of algebraic freedom (Schaefer class) *and a fixed objective*. Add
the **objective as a second generated dimension** and the two partitions come apart — which is precisely what the
canon's vertex-cover / independent-set pair does (§I-G4). That is the whole design requirement, and it is met.

---

## I-G1 — MAX-CSP: does the approximation classification cut across Schaefer's? **YES.**

Attach the standard objective (maximize satisfied constraints) to a generated Boolean constraint language. The
approximability of Max-CSP(Γ) is classified by KSTW, on **its own line**, not by Schaefer.

**The KSTW Max-CSP dichotomy (pinned):** Max-CSP(Γ) is in **PO** iff every relation in Γ is 0-valid, *or* every
relation is 1-valid, *or* every relation is 2-monotone; **otherwise APX-complete** (Khanna–Sudan–Trevisan–Williamson,
*SICOMP* 30(6):1863–1920, 2001; this is the exact condition the census oracle cites at `oracles.py:51`). Affine sits
outside PO and Max over affine is **inapproximable** to any constant factor unless P=NP (Håstad, *JACM* 48 (2001)).

**The cross-tabulation (the load-bearing, reader-checkable object):**

- Schaefer's tractable region is **0-valid ∪ 1-valid ∪ Horn ∪ dual-Horn ∪ affine ∪ bijunctive**.
- KSTW's Max-CSP-tractable region is **0-valid ∪ 1-valid ∪ 2-monotone** — strictly smaller.
- Therefore **affine, Horn, dual-Horn, and bijunctive all flip** from decision-`P` to Max-CSP-`APX-complete` (or
  worse, for affine). Decision-easy, approximation-hard. **The partitions cut across.**

The single cleanest witness a reader can check in ten seconds: **CSP(affine) ∈ P** (Gaussian elimination, Schaefer)
while **Max-CSP(affine) is inapproximable** (Håstad). Approximation is not a function of the decision class.

And the classification is not merely *shifted* — it is **richer**. Max-Ones and Min-Ones each stratify Γ into
**several** approximability classes (PO / APX-complete / poly-APX-complete / decision-hard), not two, and along
axes different from Schaefer's (the KSTW unified treatment covers Max-CSP, Min-CSP, Max-Ones, Min-Ones separately;
confirmed against the survey framing in arXiv:1109.3651). The extra classes are exactly the room the *objective*
buys.

**Bridge-hunt (R20, flagged in the spec):** the Schaefer-vs-optimization cross-tabulation is **a known published
object** — the Creignou–Khanna–Sudan monograph *Complexity Classifications of Boolean Constraint Satisfaction
Problems* (SIAM Monographs on Discrete Mathematics and Applications, vol. 7, 2001) tabulates decision, Max-CSP,
Max-Ones, Min-Ones, Min-CSP and counting side by side. This memo claims **no novelty** for the cross-tabulation; it
reads a fact off the published tables. What is new is only its *use* — as the tautology diagnostic for a generated
roster.

**I-G1 verdict:** cuts across. The tautology blocker does **not** apply to a Max-CSP roster; approximation has an
independent source (gap/PCP hardness) whose partition disagrees with the decision algebra.

## I-G2 — the parameterized oracle for generated optimization problems. **Exists, and carries the objective.**

The gradient needs both axes on the *same generated* problems.

**Marx 2005 (pinned):** for every finite Boolean constraint language Γ, Exact-Ones-SAT(Γ) — a satisfying assignment
of weight exactly *k*, parameterized by *k* — is **FPT iff Γ is weakly separable, W[1]-complete otherwise**. This is
an explicit *parameterized analog of Schaefer's dichotomy* (Marx, *Comput. Complexity* 14 (2005) 153–183). It is
the oracle the census already uses for its parameterized column (`oracles.py:76–93`).

**Bulatov–Marx 2014 (the successor that carries the objective, pinned):** *Constraint Satisfaction Parameterized by
Solution Size* (arXiv:1206.4854; *SICOMP* 43 (2014) 573–616) classifies CSP parameterized by **solution size / the
number of ones** — FPT vs W[1]-hard — for constraint languages closed under constant substitution, and states that
its FPT/W[1] cases have **"Independent Set, Vertex Cover, d-Hitting Set, Biclique"** as *special cases*. That is the
objective-carrying parameterized oracle: it distinguishes **vertex-cover (FPT)** from **independent-set (W[1]-hard)**
over generated relations, from **parameterized-reduction machinery** — a source independent of both Schaefer's
polymorphisms and KSTW's gaps.

**Source-independence check (three hats, not one).** decision ← polymorphism algebra; approximation ← gap/PCP
hardness (KSTW/Håstad); parameterization ← W[1] solution-size reductions (Marx / Bulatov–Marx). The proof they are
not one source in disguise is the affine off-diagonal cell above: `2-monotone` (KSTW's tractability line) and
`weakly separable` (Marx's tractability line) are **different conditions that disagree on affine** — approx-hard,
param-easy. Different conditions ⇒ different partitions ⇒ a genuine, measurable joint distribution, not a forced
diagonal.

**Honesty item to hand the spec (does not block BUILDABLE).** The affine parameterized cell depends on the *exact*
parameterization. The census oracle's value (`Exact-Ones over the affine co-clone` = FPT) rests on affine being
weakly separable. A *different* affine optimization — minimum-weight codeword, i.e. min-weight *nonzero* solution
of a GF(2) system, parameterized by the target weight — is **W[1]-hard** (Downey–Fellows–Vardy–Wegener 1999). Same
algebra, different objective/parameterization, different charge. This is not a contradiction; it is the point of
the whole memo restated at the finest grain — **the objective is the free variable** — and it is a calibration the
future spec must pin **per problem** (which objective, which parameterization), exactly as the reach line pinned
the conditioning value. The witness test below is chosen to be immune to this subtlety.

**I-G2 verdict:** the parameterized axis has an oracle for generated optimization objectives, independent-sourced.

## I-G3 — the generated-*objective* route (the harder, better-matched option). **No oracle — expected, established.**

The canon's gradient rows are mostly global-numeric (Ferry: 31 of 47): minimize a total subject to a connectivity /
covering / ordering condition. The honest question is whether *those* objectives can be generated **and** classified.

They cannot, and it is worth stating why rather than assuming it. Constraint **languages** are classified because a
finite relational signature has a finite, lattice-structured space of polymorphisms — Schaefer, KSTW, Marx all
exploit that. An arbitrary global numeric **objective** (a weight vector, a connectivity requirement, a metric) has
**no such classifying structure**: there is no "Schaefer for objectives," no dichotomy that takes a generated
objective and returns its approximation and parameterized charges. The classifications that *do* exist — KSTW, Marx,
Bulatov–Marx — are for objectives of a **fixed CSP functional form** (count satisfied constraints; count ones)
*parameterized by the constraint language*. So:

- **Pure generated-objective route** (arbitrary global numeric objectives): **no oracle either axis** → cannot carry
  the gradient. This is the permanent scope limit; it is the same wall Ferry hit (the 31 `n.a.` rows) seen from the
  generation side.
- **CSP-objective route** (Max-CSP / Max-Ones / Min-Ones over a generated language): **both oracles exist** (I-G1,
  I-G2). This is the viable route, and the only one.

**I-G3 verdict:** the space of objectives is not classified the way constraint languages are; the generated-objective
route is closed, and the roster must live in the CSP-objective universe. That boundary is the honest limit on what
BUILDABLE buys (§ what-it-buys).

## I-G4 — the witness test (runs first). **PASSES.**

Before any roster is proposed: does the generation scheme produce vertex-cover / independent-set — same constraints,
complementary objectives, **opposite charges on both axes** — with *distinct* values? (A scheme that assigns the pair
identical values is structurally incapable of exhibiting the gradient — this is what killed `tuple_dispersion`, which
gave both 0.667.)

| problem | relation + objective | approximation | parameterized |
|---|---|---|---|
| **vertex cover** | edge, **Min-Ones** (cover all edges) | APX-complete — 2-approx, no PTAS (Dinur–Safra) | **FPT** (Bulatov–Marx special case) |
| **independent set** | complementary edge, **Max-Ones** (pack) | **inapprox** — no $n^{1-\epsilon}$ (Håstad/Zuckerman) | **W[1]** (Bulatov–Marx special case) |

Same relation type (edge), complementary objective (Min-Ones vs Max-Ones), **opposite on both axes**. A random-graph
generator paired with the two objectives produces both, with distinct values. Crucially this witness uses **only**
the Max/Min-Ones objectives and the solution-size parameterization — the parameterizations Bulatov–Marx pins
directly — so it is immune to the affine/codeword subtlety of I-G2. **Witness test passes.** The generation scheme
is structurally capable of exhibiting the gradient.

---

## What a BUILDABLE verdict buys (and what it does not)

The first test of the approx⟷param gradient on a population **no human chose** — generated languages × generated
CSP-objectives — with the two charges from partitions that **provably disagree** (the affine off-diagonal). This is
the one thing that could begin to separate *"approximability and parameterizability are coupled in computation"*
from *"they are coupled among the problems people found interesting enough to study."* Every one of the five attacks
that hardened the canon gradient (null model, dedup, permutation, adversarial violator hunt, two bridge hunts) was
an attack **from inside the canon**; this is the only route that measures the coupling outside it.

**Correctly scoped.** It gets outside *curation* but stays inside the **CSP-objective universe**. The canon's 31
global-numeric rows — where the gradient most vividly lives — remain out of reach of *any* generated roster, because
their objectives are not classifiable (I-G3). So a positive result would read: *the coupling persists in the
CSP-objective universe, not merely among curated problems* — evidence it is computational, over the reachable
sub-universe. A null would read: *the coupling is a selection effect, absent once curation is removed (at least in
the CSP-objective universe).* Both are informative; both are firsts; neither claims the whole canon. That boundary
is not a hedge — it is the same twice-measured structural fact (hardness lives above the relation level) seen a
third way: **the objective is a separate object from the constraints, and only where the objective has CSP shape can
a generator reach it.**

## What this memo does *not* authorize

No roster is built and no measurement runs on the strength of this memo. BUILDABLE authorizes a **spec** — which
must, before it runs anything: (1) pin the objective + parameterization **per problem** (the I-G2 codeword
subtlety); (2) pass the §I-G4 witness test *as its first calibration gate*, on its own generated instances, before
any sky; (3) state its population as *CSP-objective, not canon* up front (the I-G3 boundary); (4) carry a
known-answer calibration (the census anchors transport — vertex-cover/independent-set/Max-Cut have known charges);
and (5) declare what a positive vs null result can and cannot claim about the whole-canon gradient. The gradient
stays unexplained until such a spec is written, sealed, and run. **G1 rests at BUILDABLE.**

---

## Sources (R20 — primary, reader-checkable)

- T. J. Schaefer, *The complexity of satisfiability problems*, STOC 1978 — decision dichotomy.
- S. Khanna, M. Sudan, L. Trevisan, D. P. Williamson, *The approximability of constraint satisfaction problems*,
  *SIAM J. Comput.* 30(6):1863–1920, 2001 — Max-CSP / Max-Ones / Min-Ones / Min-CSP classification (the 2-monotone
  Max-CSP dichotomy).
- J. Håstad, *Some optimal inapproximability results*, *JACM* 48(4):798–859, 2001 — Max-3Lin (affine) inapprox.
- N. Creignou, S. Khanna, M. Sudan, *Complexity Classifications of Boolean Constraint Satisfaction Problems*, SIAM
  Monographs on Discrete Mathematics and Applications 7, 2001 — **the published cross-tabulation** (bridge-hunt).
- D. Marx, *Parameterized complexity of constraint satisfaction problems*, *Comput. Complexity* 14:153–183, 2005 —
  Exact-Ones FPT iff weakly separable (parameterized analog of Schaefer).
- A. Bulatov, D. Marx, *Constraint satisfaction parameterized by solution size*, arXiv:1206.4854; *SIAM J. Comput.*
  43(2):573–616, 2014 — solution-size FPT/W[1] dichotomy; Vertex Cover / Independent Set as special cases.
- R. Downey, M. Fellows, A. Vardy, G. Whittle/Wegener, *The parametrized complexity of some fundamental problems in
  coding theory*, *SIAM J. Comput.* 29(2):545–570, 1999 — minimum-weight codeword W[1]-hard (the I-G2 honesty item).
- In-repo grounding: `foundry/foundry/oracles.py` (the census dichotomy oracle — decision/approximation/
  parameterized columns and their pinned cites); Ferry findings `docs/findings/Ferry-findings.md` (the 31 `n.a.`
  global-numeric rows; the vertex-cover/independent-set calibration standard).
