# The wall generation cannot cross — why the approx⟷param gradient can only be attacked from inside the canon

**A standalone finding, arrived at by four independent probes rather than by argument.**

The charge atlas's single most robust empirical finding is a coupling between two of the eight charges: a problem's
**approximability** and its **parameterized** complexity co-vary (Cramér's V ≈ 0.73 on the 47 both-real canon rows,
surviving a type-respecting null and entailment netting). Five separate attacks failed to dissolve it — the S1
type-respecting null model, deduplication, permutation, an adversarial violator hunt, and two bridge hunts. **Every one
of those five attacks was mounted from inside the canon.** This note reports why no attack could be mounted from
outside — and why that fact, once you see it, is itself a result.

## The thesis

> **The approx⟷param gradient lives in a population that generation cannot reach.** Its home is curated optimization
> problems with *global* objectives — Steiner tree, TSP, knapsack, set-cover, feedback sets — precisely the class for
> which no classification theory provides *both* an approximation charge and a parameterized charge from *independent*
> sources. Every bias-free generated alternative is, provably, one of: theorem-tautological, structurally mismatched,
> too coarse, or classification-less on one axis.

> **Amendment (2026-07-23) — the thesis is quantitatively corrected by the program's own next experiment; original
> kept visible.** Lattice v3 (`Lattice-v3-findings.md`, prereg_v31) did what this note said could not be done: it
> attacked the gradient **from outside the canon**, on the natural, unselected generated Boolean population (90
> symmetry classes, no selection at all). It found a **weak, non-monotonic coupling** — Cramér's V = **0.256**,
> bootstrap CI₉₅ **(0.13, 0.398)**, which **excludes 0**. So "cannot be attacked from outside" is **partly falsified**:
> it *can* be attacked, and a weak signal survives with no human choosing the problems — the gradient is therefore
> **not purely a selection effect.** But it is also **not the canon's gradient reproduced**: 0.256 is a quarter of the
> canon's 0.73, and v3's coupling is *nominal* (Spearman ≈ 0) whereas the canon's is *monotonic*, so what v3 found
> **may be a related-but-different coupling shape**, not the same gradient at lower volume — v3 cannot tell which. The
> 0.73-vs-0.256 gap is attributable to **curation** (humans chose the canon's rows) **and/or population composition**
> (the canon contains the global-objective problems no generated roster reaches) — two confounded differences v3
> **cannot separate; the gap is not yet decomposed.** (This note does *not* claim the canon "amplifies" the signal —
> that would assert a curation mechanism v3 did not isolate.) The Wall-3 "open question" from the earlier amendment is
> now answered: the single-relation Boolean *universe* is **not** too coarse — it spans the strata (v2) and carries a
> weak coupling (v3). **Net: three measured walls, plus a weak non-monotonic coupling that does survive outside the
> canon.** The original thesis is left standing above so the movement of this program-defining claim stays on record.

> **Amendment (2026-07-23, Prism) — the "weak, non-monotonic coupling" is now decomposed; the residual, not the raw
> number, is the object.** Prism (`Prism-v1-findings.md`, prereg_v32) charged the *same* 90-class roster with every
> oracle-derivable charge and netted each pair against what the theorems force. It splits v3's 0.256 into two parts.
> **(i) A theorem-forced part** — the affine off-diagonal, `affine ⟹ weakly-separable ⟹ FPT` (Marx Ex 2.4). **(ii) A
> non-affine residual** that survives netting everything the theorems force, and is **stronger than the raw number
> suggested**: pooled Cramér's V **0.286**, and on the **Min-Ones** objective **0.459** (0.692 within the non-affine
> stratum alone). The affine off-diagonal was **masking** this residual, not producing it — so the theorem-forced
> structure was not merely inflating the signal, it was **distorting its shape.** **Direction does not come back.** The
> sealed prediction that netting the affine rows would restore monotonicity (prereg_v32 pred 6) **missed** — netted
> Spearman went 0.019 → −0.005 — and the post-hoc bridge-completed residual runs *anti-canon* where it is strongest:
> pooled Spearman **−0.142**, Min-Ones **−0.428** (Min-Ones-APX-complete relations are mostly FPT, Min-Ones-PO mostly
> W[1] — *harder-approx ⟷ easier-param*, the reverse of the canon's positive gradient; Max-Ones is near-degenerate and
> weakly the other way, so the aggregate is unresolved). **There is no "matches the canon's direction after removing
> what theorems force" claim** — the one direction test that ran contradicts it. **Updated gloss for v3's "weak,
> non-monotonic coupling":** *partly theorem-forced; the non-affine residual is the real object, magnitude 0.286
> (Min-Ones 0.459), direction unresolved — anti-canon on the load-bearing Min-Ones side.* Prism also found the
> localization-absorption headline (does bounded-width absorb the coupling, Foundry I6) **untestable at arity ≤3**
> (bounded-width ⟺ tractability there); the arity-4 experiment that *can* test it is specced (`docs/specs/
> Absorption-arity4-spec.md`) and deferred behind the preprint.

"Bias-free rostering" — generating problems from a formal scheme rather than curating the ones people happened to find
interesting — is the gold standard for ruling out a selection effect. The question the gradient has always faced is
whether it reflects computation or sociology: are approximability and parameterizability coupled *in the mathematics*,
or only *among the problems humans chose to study*? A generated roster is the only instrument that can separate those.
This note establishes that the instrument does not exist, and characterizes exactly why.

## The four walls

Four routes to a generated roster have now been probed, each hitting a distinct, named wall.

| # | Route | The object it generates | Wall | Type of result |
|---|---|---|---|---|
| 1 | **Census** | Boolean constraint *languages* (co-clones), fixed objective | Both charges read off **one polymorphism fingerprint** ⇒ their association is an *identity*, not a measurement | **Measured** (Task 0: entailment-netted residual = 0) |
| 2 | **Ferry** | (canon carried to a relation-level scalar) | The canon's gradient rows have **no local constraint relation** to generate from — 31 of 47 are global/numeric | **Measured** (`Ferry-findings.md`: 31/47 `n.a.`) |
| 3 | **Lattice** | (language, objective) pairs, crisp CSP | ~~the reachable population is ~30 rows and too coarse~~ **[DOWNGRADED 2026-07-23 — see amendment below]**: the census *representatives* gave 5 profiles < floor (INSUFFICIENT RESOLUTION), but the *universe* question is **open**, v2 pending | **Provisional** (v1 measured; v2 open) |
| 4 | **VCSP** | valued objectives (cost functions) | Population is vast, but the **parameterized axis has no classification** (open frontier) and the approximation axis only *dichotomizes* | **Feasibility-pinned** (G3 NOT BUILDABLE) |

Each wall is different, and that is the point — this is not one obstacle met four times, it is four independent
obstacles that happen to enclose the same region.

**Wall 1 — tautology (census).** Schaefer, KSTW, and Marx all read a Boolean language's charges from the *same*
algebraic object: its polymorphisms. When the objective is held fixed, the approximation and parameterized charges
become deterministic functions of that one fingerprint, so any correlation between them is the fingerprint
re-expressing itself. Netting the theorem-forced component leaves residual exactly zero. *The charges were never
independent to begin with.*

**Wall 2 — structural mismatch (Ferry).** Carrying a relation-level probe (`tuple_dispersion`) to the canon's
gradient-carrying rows revealed that **31 of 47 have no defensible local relation at all** — their hardness lives in a
global objective (a total to minimize, a connectivity or ordering condition), not in any local constraint a relation
could name. A generated constraint-language roster is made entirely of local relations. *The population where the
gradient lives and the population generation produces barely intersect.*

**Wall 3 — too coarse (Lattice).** G1 established that making the *objective* a second generated dimension (Min-Ones vs
Max-Ones over a generated language) does break the tautology — the two charges then come from partitions that provably
disagree, witnessed by the affine cell reading `(approximation: inapprox, parameterized: FPT)` in the program's own
oracle. This is real, and Lattice will run it. But the reachable universe is **~15 Boolean co-clones × 2 objectives**,
a deterministic table of ~30 rows — a *complete census of a small universe*, not a sample of a large one. It may simply
be too coarse to exhibit a gradient; if so, the honest verdict is "the reachable universe is too small," itself an
answer.

> **Amendment (2026-07-23) — Wall 3 DOWNGRADED, and now partly measured.** Lattice v1 ran
> (`Lattice-v1-findings.md`, prereg_v29). The **witness gate passed** — the generate-and-charge pipeline reproduces
> vertex-cover and independent-set on opposite corners of both axes, so the instrument works. But the sealed roster
> (the census's Schaefer representatives) realized only **5 distinct profiles < the floor of 6 → INSUFFICIENT
> RESOLUTION.** Crucially, the honest verdict is **narrower** than this section first predicted: it is the census's
> *representatives* that are too coarse (they are 0-valid / 1-valid / width-2-affine / IHS-B, collapsing to PO), **not**
> the single-relation Boolean *universe* — whose empty strata are inhabited by relations the census never used
> (`x⊕y⊕z=1` → Nearest-Codeword-complete, the only reason the count was 5 not 4). So Wall 3 as written — "the reachable
> population is ~30 rows and too coarse" — **is not established.** Whether the generated Boolean universe is too coarse
> is now an **open question**, tested by v2 (`prereg_v30`), a purpose-built, stratum-spanning, correlation-blind roster.
> The wall may not be a wall; the representatives were. This finding's Wall-3 leg is therefore **provisional pending
> v2**, and a reader should treat the four-wall claim as three measured walls plus one open question, not four.

**Wall 4 — classification-less (VCSP).** Valued CSP looked like the census with room: the cost function *is* the
generated object, and the population is a continuum. But (G3) the approximation charge for valued languages only
**dichotomizes** — Thapper–Živný classify *exact* solvability (poly-time or NP-hard), with no PTAS/APX/poly-APX
stratification — and there is **no parameterized-by-solution-size classification for valued objectives at all** (the
FPT/W[1] borderline for VCSP is an open research frontier). A larger population bought nothing: distinct
(approx × param) profiles are bounded by charge *granularity*, not by row count, and VCSP's granularity is coarser than
Lattice's on one axis and absent on the other.

## The one conclusion

Approximation and parameterized status are each classifiable, from independent theory, only for two kinds of object:
**constraint languages** (Schaefer/KSTW/Marx — but there the objective is fixed, so the charges collapse to one source)
and **crisp CSP objectives** (Lattice — but the reachable population is ~30). The moment the objective becomes *global
and numeric* — the moment you reach the problems where the gradient is strongest — you leave the domain of every
classification theorem that assigns these charges. There is no Schaefer-for-objectives; there is no
Bulatov–Marx-for-valued-objectives. **The gradient's home is exactly the blind spot shared by all the classification
programs that could otherwise generate a bias-free roster.**

## Why it matters

1. **It explains a fact the program has circled for months.** The gradient survived five attacks from inside the canon
   and could not be attacked from outside — *not for lack of effort, but because the outside does not contain the right
   objects.* Four independent probes, four different walls, one enclosed region. The absence of a knockout from outside
   was never evidence the gradient is fragile; it is evidence the outside is empty of the objects needed to swing.
2. **It retroactively justifies curation.** The canon has always carried an implicit charge of arbitrariness — why
   these 118 problems? This finding answers it: for the coupling that most defines the atlas, **curation is not
   laziness, because the bias-free alternative provably cannot reach the population.** A hand-chosen roster of
   global-objective problems is, for this question, not a weaker instrument than a generated one — it is the *only*
   instrument.
3. **It converts an accumulation of disappointments into a single positive result.** Census, Ferry, Lattice, VCSP each
   read locally as "this route didn't work." Together they read as a characterization: *we now know precisely what kind
   of object could carry a bias-free test of this gradient, and that no current theory classifies it.*

## What this does *not* claim (honest scope)

- **Not a theorem, a state-of-classification result.** The wall is relative to the classification theory that exists
  today. If someone produces a classification of *global-objective* problems assigning approximation and parameterized
  charges from independent sources — a "Schaefer for objectives" — the wall moves and a bias-free test becomes possible.
  The finding is that no such classification currently exists, established by pinning the frontier (Thapper–Živný is
  exact-only; parameterized VCSP is open), not by proving one impossible.
- **Not a claim that the gradient is real-because-unattackable.** Unattackability from outside is not confirmation; it
  is a statement about instruments, not about the phenomenon. The gradient's within-canon support (V ≈ 0.73, surviving
  five attacks) is its evidence; this note only explains the *shape of the remaining uncertainty* — that it cannot, at
  present, be reduced by a generated roster.
- **Lattice has now run (v1), and moved Wall 3.** Update (2026-07-23): v1's witness gate passed (the pipeline works)
  but its sealed roster hit INSUFFICIENT RESOLUTION — *on the census representatives, not the universe*. That refined
  "too coarse" from a prediction about the population into a **measured fact about the representatives** and an **open
  question about the universe**. Wall 3 is now provisional; v2 (a stratum-spanning roster) is the actual test of whether
  the generated Boolean universe can exhibit the gradient. Until v2, read this finding as **three measured walls plus
  one open question.**

## Provenance

Established across: `docs/findings/Factors-v1.md` / `A3-structure.md` / `A4-*.md` (the V ≈ 0.73 coupling and its five
in-canon attacks); Task 0 R25-netting residual-zero selftest (`foundry/foundry/r25.py`); `docs/findings/Ferry-findings.md`
(the 31/47 `n.a.` structural fact); `docs/findings/G1-buildability.md` (Lattice BUILDABLE, ~15×2 reachable);
`docs/findings/G3-vcsp-buildability.md` (VCSP NOT BUILDABLE). Underlying classification sources are pinned R20 in the G1
and G3 memos (Schaefer 1978; KSTW SICOMP 2001; Marx 2005 / Bulatov–Marx 2014; Thapper–Živný JACM 2016; Kolmogorov–
Krokhin–Rolínek SICOMP 2017).
