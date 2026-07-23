# Lattice (G2) — L1 sourcing memo: the KSTW Max-Ones / Min-Ones stratifications

**For owner review BEFORE any oracle build (L3).** This is the load-bearing R20 step: it pins, from the primary source,
the exact approximation stratifications the Lattice oracle must encode, maps the 15 Boolean languages onto them, and
lists the predicates to build. It also surfaces one **material correction to the plan's build surface** and four
decisions for the `prereg_v29` seal (L2). No code is written and no measurement runs on this memo.

## 0. The correction the gate caught: the plan named the wrong predicate

The G2 plan called `is_2monotone` "the single most load-bearing new classifier." **It is not needed.** 2-monotone is
the PO condition for **Max-CSP / Min-CSP** (KSTW Thm 2.11 / 2.13), *not* for Max-Ones or Min-Ones — and Lattice's
objectives are Max-Ones and Min-Ones (ruling 2). The conditions the Max-Ones/Min-Ones theorems actually use are
`0-valid`, `1-valid`, `weakly positive` (dual-Horn), `weakly negative` (Horn), `affine`, **`width-2 affine`**,
**`strongly 0-valid`**, `2CNF` (bijunctive), and **`IHS-B`**. **The new predicates to build are `is_width2affine`,
`is_strongly_0valid`, and `is_IHSB` — not `is_2monotone`.** Building against the plan as written would have implemented
a classifier that never fires in this roster. This is exactly what the L1 gate exists to catch.

## 1. MAX-ONES(F) — the full stratification (KSTW Theorem 2.12, verbatim)

> For any constraint set `F`, (Weighted) Max Ones(`F`) is either in PO or APX-complete or poly-APX-complete or
> decidable-but-not-approximable or not-decidable. Furthermore, evaluated as a **strict priority list**:
> **(1)** If `F` is **1-valid or weakly positive or width-2 affine** → **PO**.
> **(2)** Else if `F` is **affine** → **APX-complete**.
> **(3)** Else if `F` is **strongly 0-valid or weakly negative or 2CNF** → **poly-APX-complete**.
> **(4)** Else if `F` is **0-valid** → Sat(`F`) ∈ P but finding a positive-value solution is NP-hard (**decidable,
> not approximable to any factor**).
> **(5)** Else → finding a feasible solution is **NP-hard** (**not decidable**).

The clauses are **priority-ordered**: a language is classified by the *first* line it matches. (So an affine 0-valid
language is APX-complete by (2), never reaching (4).) Five distinct classes; the 0-valid case (4) is a genuine fifth
class, not a synonym for feasibility-hardness.

## 2. MIN-ONES(F) — the full stratification (KSTW Theorem 2.14, verbatim)

> For any constraint set `F`, (Weighted) Min Ones(`F`) is either in PO or APX-complete or Nearest-Codeword-complete or
> Min-Horn-Deletion-complete or poly-APX-complete or inapproximable-to-any-factor or not-decidable. As a strict
> priority list:
> **(1)** If `F` is **0-valid or weakly negative or width-2 affine** → **PO**.
> **(2)** Else if `F` is **2CNF or IHS-B** → **APX-complete**. *(Vertex Cover lives here.)*
> **(3)** Else if `F` is **affine** → **Nearest-Codeword-complete**. *(Nearest Codeword lives here.)*
> **(4)** Else if `F` is **weakly positive** → **Min-Horn-Deletion-complete**.
> **(5)** Else if `F` is **1-valid** → **poly-APX-complete** (unweighted) / inapproximable-to-any-factor (weighted).
> **(6)** Else → finding a feasible solution is **NP-hard**.

Six classes, two of which are named completeness classes with no standard-vocabulary synonym: **Nearest-Codeword-complete**
(affine; hard to approximate within `2^{log^{1−ε} n}`, Arora–Babai–Sweedyk–Stern) and **Min-Horn-Deletion-complete**
(weakly positive). Note the unweighted/weighted split in line (5).

## 3. Definitions (verbatim / precise, from KSTW §2.4, cross-checked)

- **0-valid / 1-valid:** `f(0,…,0)=1` / `f(1,…,1)=1`.
- **weakly negative = Horn:** expressible in CNF with ≤1 *unnegated* literal per clause (AND-closed).
- **weakly positive = anti-Horn = dual-Horn:** ≤1 *negated* literal per clause (OR-closed).
- **affine:** a conjunction of linear equations over Z₂.
- **width-2 affine (NEW predicate):** affine with **≤2 variables per equation** — i.e. expressible by `(x=y)`, `(x≠y)`,
  and unit constraints `(x)`,`(¬x)`. *This is the PO condition on both axes; it must be computed.*
- **strongly 0-valid (NEW predicate):** satisfied by **all** assignments of weight ≤1 (all-zeros and every single-1).
  *Max-Ones only.*
- **2CNF = bijunctive:** expressible as a 2-CNF (majority-closed) — already available via the bijunctive polymorphism.
- **IHS-B (NEW predicate):** "implicative hitting-set bounded." **IHS-B+** = clauses of the form `(x₁∨…∨x_k)`, `k≤B`
  (bounded *positive* clauses), or `(¬x∨y)` (implications), or `(¬x)` (units). **IHS-B−** = the literal-complement dual
  (bounded *negative* clauses, implications, units). A finite family is IHS-B iff it is IHS-B+ or IHS-B−, with `B` the
  max arity. *Min-Ones only; this is where Vertex Cover's `OR₂` lands.*
- **2-monotone (NOT used here):** DNF `(∧positive)∨(∧negative)` — the Max-CSP/Min-CSP PO condition. Recorded only to
  document its exclusion.

## 4. The 15-language occupancy map — the objective flips the charge (the good news)

Applying the two priority lists to the roster's language types. The striking fact: **for the same language, Max-Ones and
Min-Ones usually land in *different* strata**, because the two theorems are near-duals (Horn drives Min-easy/Max-hard;
dual-Horn the reverse; 0-valid vs 1-valid swap roles). The objective dimension therefore spreads the approximation
charge across the whole stratification — exactly what ruling 3 (no flattening) protects, and a strong signal that the
occupancy grid will be well-populated despite ~30 rows.

| language type | Max-Ones stratum | Min-Ones stratum |
|---|---|---|
| **affine** (xor-sat) | **APX-complete** (2) | **Nearest-Codeword-complete** (3) |
| **Horn / weakly-negative** (horn-sat) | **poly-APX-complete** (3) | **PO** (1) |
| **dual-Horn / weakly-positive** | **PO** (1) | **Min-Horn-Deletion-complete** (4) |
| **bijunctive / 2CNF** (2-sat) | **poly-APX-complete** (3) | **APX-complete** (2) |
| **NP-hard** (3-sat, nae-sat, 1-in-3-sat) | **feasibility-NP-hard** (5) | **feasibility-NP-hard** (6) |
| **0-valid finer** (zerovalid-affine / -horn / -bijunctive / -dualhorn) | affine→APX-c; Horn/2CNF→poly-APX-c; else decidable-not-approx (4) | **PO** (1, 0-valid) |
| **1-valid finer** (onevalid-affine / -dualhorn / -bijunctive / -horn) | **PO** (1, 1-valid) | 1-valid→poly-APX-c (5), unless Horn/width-2-affine caught at (1) |

Distinct approximation values appearing across the roster: **PO, APX-complete, poly-APX-complete,
Nearest-Codeword-complete, Min-Horn-Deletion-complete, decidable-not-approximable, feasibility-NP-hard** — up to seven,
which with the two parameterized values gives a large profile ceiling. The exact per-representative placement is computed
by the oracle from each CKZ plain-basis relation (the finer-tier 0-/1-valid languages resolve by the priority order);
this table is the *expected* occupancy the L4 witness gate and L5 build will confirm or correct. **Empty strata will be
reported as facts (ruling 3), not merged.**

## 5. The witness / anchors (calibration, L4)

Pinned from KSTW §2.3 + the hardness lemmas:

| problem | as a Ones-problem | approximation charge | parameterized charge |
|---|---|---|---|
| **Vertex Cover** | **Min-Ones(`OR₂`)**, `OR₂={01,10,11}` | **APX-complete** (Min-Ones line 2; `OR₂` is 2CNF & IHS-B+) | **FPT** (Bulatov–Marx) |
| **Independent Set / Clique** | **Max-Ones(`NAND`)**, `NAND={00,01,10}` | **poly-APX-complete** (Max-Ones line 3; `NAND` is 2CNF, weakly-negative, strongly-0-valid; hard within Ω(n^{1−ε})) | **W[1]** (Bulatov–Marx) |
| Max-Cut | Max-**CSP**(`XOR`) | APX-complete — **excluded**: a Max-CSP, not a Ones-problem (ruling 2) | n/a |

So the L4 witness gate asserts exactly **VC = (APX-complete, FPT)** and **IS = (poly-APX-complete, W[1])** — opposite on
both axes, from complementary relations (`OR₂` vs `NAND`), both generatable. Max-Cut is recorded as an excluded anchor
(different objective), consistent with the Max-Ones/Min-Ones-only scope.

## 6. Predicates to build (corrected list) + the parameterized side

**New predicates (`postlattice.py`), each with a hand-value `selftest_* == 0`:**
- `is_width2affine(rels)` — affine *and* every equation ≤2 variables. (Reuse the existing affine machinery; add the
  arity bound.)
- `is_strongly_0valid(rels)` — every weight-≤1 assignment satisfies. (Direct enumeration over ≤1-one assignments.)
- `is_IHSB(rels)` — IHS-B+ or IHS-B−: expressible with bounded positive (resp. negative) clauses + implications + units.
  (The subtlest; hand-check `OR₂`→IHS-B+, `NAND`→IHS-B−.)

**Reused predicates (exist):** `is_0valid`, `is_1valid`, `has_polymorphism`(Horn / dual-Horn / affine / bijunctive),
`any_tractable_polymorphism`. **`is_2monotone` is NOT built.**

**Parameterized axis (unchanged, reuse):** `paramd3.parameterized_d3` / `postlattice.is_weakly_separable` give FPT/W[1]
by solution size (number of ones). One pin to carry into L3: for a fixed language `F`, Min-Ones parameterizes by
"≤k ones" and Max-Ones by "≥k ones"; complementation (0↔1) maps one direction to the other, so the oracle must apply the
solution-size dichotomy **with the objective's direction** (Min: `F`; Max: `F` complemented), *not* as a single
direction-blind value per language. The witness (VC via Min-Ones-`OR₂`→FPT; IS via Max-Ones-`NAND`→W[1]) is the exact
calibration that this direction handling is correct.

## 7. Decisions for the `prereg_v29` seal (L2) — owner review

1. **Approximation vocabulary — use the KSTW-native classes, not eightfold's 8-value set.** The faithful values are
   `PO, APX-complete, poly-APX-complete, Nearest-Codeword-complete, Min-Horn-Deletion-complete, decidable-not-approximable,
   feasibility-hard`. (The G2 plan said "adopt eightfold's `FPTAS…inapprox` vocab"; that vocab cannot name
   Nearest-Codeword-complete or Min-Horn-Deletion-complete, and forcing a map would be the hand-judgment ruling 3
   forbids.) **Comparability to the canon's 0.73 is preserved:** Cramér's V is nominal and normalized, so the statistic
   is comparable across different label sets — the roster does not need the canon's exact vocabulary. *Recommend:
   KSTW-native vocab.*
2. **Ordinalization (only for a secondary rank statistic; the primary occupancy object needs none).** A defensible
   easy→hard order is `PO < APX-complete < Min-Horn-Deletion-complete < Nearest-Codeword-complete < poly-APX-complete <
   decidable-not-approximable < feasibility-hard`, but the placement of the two named completeness classes relative to
   poly-APX is a judgment (their hardness thresholds are `~log`-ish and `2^{log^{1−ε}n}` respectively). *Recommend:
   seal this order in the prereg with the caveat, and lead all analysis with the nominal occupancy grid so nothing rests
   on it.*
3. **Netting under the KSTW-native vocab.** The rule-based bridges (ruling 1) fire where their antecedent matches:
   Cai–Chen's antecedent `approximation ∈ {FPTAS,EPTAS,PTAS,APX,APX-complete}` matches only the roster's `APX-complete`
   rows; EPTAS↔FPT never fires (no EPTAS rows). So netting will remove only the theorem-forced implications on the
   `APX-complete` cells, leaving most of the table intact — a light touch, as ruling 1 intends. *Recommend: seal this
   applicability map; the fallback (raw + acknowledged gap) remains available if the adaptation proves heavier than
   expected.*
4. **`feasibility-hard` rows and the co-variation.** The three NP-hard languages read `feasibility-hard` on *both*
   objectives — the optimization problem has no findable feasible solution, so its parameterized charge is arguably
   `open` (you cannot parameterize a search you cannot perform). *Recommend: record `feasibility-hard` as the
   approximation value and `open` (n.a.-by-typing) as the parameterized value for these rows, so they enter the
   occupancy grid as a documented corner but not the both-real association — mirroring the canon's both-real convention.*

## 8. Sources (R20 — primary, reader-checkable)

- **PRIMARY:** S. Khanna, M. Sudan, L. Trevisan, D. P. Williamson, *The Approximability of Constraint Satisfaction
  Problems*, SIAM J. Comput. 30(6):1863–1920, 2001 — **Thm 2.12 (Max Ones), Thm 2.14 (Min Ones)**, §2.4 (definitions),
  §2.3 (problem placements). Full-text: `people.csail.mit.edu/madhu/papers/2001/kstw.pdf`;
  `epubs.siam.org/doi/10.1137/S0097539799349948`.
- **Restatement (Max Ones PO boundary):** S. Kratsch, D. Marx, M. Wahlström, *Parameterized Complexity and
  Kernelizability of Max Ones and Exact Ones Problems*, ACM TOCT 8(1), 2016 — Thm 3.1 (confirms the 1-valid / weakly
  positive / width-2 affine PO boundary; APX-hard otherwise).
- **Restatement (Min Ones PO boundary + Vertex Cover identity):** S. Kratsch, M. Wahlström, *Preprocessing of Min Ones
  Problems: A Dichotomy*, MFCS 2010 (arXiv:0910.4518) — Thm 1 (0-valid / Horn / width-2 affine PO boundary);
  `Min-Ones({01,10,11})` = Vertex Cover.
- **Context:** N. Creignou, S. Khanna, M. Sudan, *Complexity Classifications of Boolean Constraint Satisfaction
  Problems*, SIAM Monographs 7, 2001 (the tabulated cross-reference; not read interior — not cited as a pin).
- Parameterized side pins: Marx 2005 / Bulatov–Marx 2014 (arXiv:1206.4854), per `G1-buildability.md`.

## 9. Parameterized-axis sourcing (post-review) — the corrected relation-level oracle + the armed ground-truth rule

Sourcing that followed the owner's rulings (single-relation languages; **ground-truth rule: the implementation follows
the source's definition; the known values are a CHECK, never an input; a disagreement is a finding to stop-and-report,
not a predicate to tune**).

**The definition (Marx 2005, Definition 2.1 — general, no 0-validity):** *R is weakly separable if (1) [guarded union]
whenever x₁, x₂ are satisfying **such that their intersection is satisfying**, their union is satisfying; and (2)
[difference] whenever x₁ ⊊ x₂ ⊊ x₃ are satisfying, x₁ ⊕ x₂ ⊕ x₃ is satisfying.* The union condition is **guarded**, so
it does **not** require or imply 0-validity. The existing `postlattice.is_weakly_separable` implements the **0-valid
simplified form** (Marx Lemma 2.2 / Bulatov–Marx Def 3.2), whose *unconditional* disjoint-union test is valid **only on
0-valid relations** — correct for the census (class-level, 0-valid-normalized co-clones), wrong for Lattice's 0-invalid
single relations. Lattice adds a distinct `is_weakly_separable_general` (Def 2.1); the census's function is untouched.

**The armed ground-truth rule — OUTCOME: ARMED, DID NOT FIRE.** The definition was pinned from source *before* the check;
every ground-truth-checked single-relation verdict reproduced with **no tuning**. The `scope` column is load-bearing —
record it so a future reader does not re-derive the OR₃ confusion:

| relation | Exact-Ones({R}) | source | **scope of the source value** |
|---|---|---|---|
| OR₂ (pos-2-clause) | **FPT** | BM14 Ex 6.1 — VC = OCSP(OR₂) | single-relation |
| NAND (neg-2-clause) | **W[1]** | BM14 Ex 6.1 — IS = OCSP(NAND) | single-relation |
| x≠y (width-2 affine) | **FPT** | Marx Ex 2.4 — affine ⇒ weakly separable, *per-relation* | single-relation |
| x⊕y⊕z=0 (affine) | **FPT** | Marx Ex 2.4 | single-relation |
| OR₃ (pos-3-clause) | **FPT** | BM14 — d-Hitting-Set is FPT (d=3) | **single-relation** |
| dual-Horn *co-clone* | **W[1]** | census `oracles.py` — implication x→y in the co-clone fails Def 2.1 | **co-clone / class-level** |

**OR₃ / dual-Horn are compatible, not contradictory** (different objects): OR₃ *alone* is 3-Hitting-Set (FPT). The
dual-Horn *co-clone* additionally contains the implication x→y = {00,01,11}, which is **not** weakly separable —
the chain (00)⊊(01)⊊(11) gives (00)⊕(01)⊕(11) = (10) ∉ R, so the difference condition fails — making the co-clone
*language* W[1]. The census charges the co-clone (right for the census); Lattice charges the single relation (right for
Lattice). This is precisely the scope distinction that motivated the single-relation ruling.

**The guard is real (CI unit test, not just a passing run).** The union guard is the exact conditional the old code
dropped. Hand-constructed discriminator: on **x≠y**, guarded (Def 2.1) → weakly-separable = **True**, unguarded (0-valid
form) → **False** — they disagree, and the implementation returns the guarded value. Asserted in `test_lattice.py`, so
the new oracle cannot silently regress to the unconditional check.

**Parameterization: exactly-k ones** (BM14 OCSP); equivalent to the textbook ≤k / ≥k forms up to padding, so the
FPT/W[1] status is unaffected.

**Nothing roster-wide runs on this memo.** With §7's four decisions signed off and §9's oracle validated against ground
truth, L2 seals `prereg_v29` and L3 builds the predicates + both objective oracles + `is_weakly_separable_general`,
gated by the L4 witness test (VC and IS on opposite corners of **both** axes).
