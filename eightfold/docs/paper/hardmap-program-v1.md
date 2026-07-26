# The hardmap program — a consolidated account

**Draft status: W1. Sections 2–4 only.** §§1, 5–7 are outlined but unwritten (see
[the outline](hardmap-program-v1-outline.md)). Every number below was extracted from its artifact during
drafting and carries a row in [the claims map](claims-map.md); none was transcribed from a prior note.

**One conditional, stated once and not repeated.** Every hardness label in this program is conditional on
the standard separation conjectures. An `NPC` cell means *hard if P ≠ NP*. Nothing below is unconditional,
and where a result is theorem-grade it is the *classification* that is proven, not the separation.

---

## 2. The artifacts

The program's claim to be checkable rests on frozen bytes, not on narrative. Five artifacts carry the
results, each frozen at a hash that is asserted by test and re-verified on every run.

| artifact | rows | sha256[:16] | what it holds |
|---|---:|---|---|
| `atlas.jsonl` | 118 | `6d53a4f1d0907f16` | the charge atlas, v1 — the founding canon |
| `atlas_v2.jsonl` | 118 | `784f4739360f1d7b` | v1 plus the Strata charge-applicability layer |
| `atlas_v3.jsonl` | 345 | `e62f3c284b408a26` | the broad expansion; the population most results run on |
| `anatomy_v1.jsonl` | 4,417 | `8ff11f8a33bbdce7` | the Structure Atlas — 345 natural rows, 4,072 Boolean |
| `anatomy_v2.jsonl` | 4,417 | `f802f2e50c73f2fe` | v1 plus closure columns on the 28 rows that admit them |

**Two tables, one law.** The charge atlas records *fate* — what the literature has proven about a problem,
cited per cell. The Structure Atlas records *what a problem is* — coordinates derived from the problem's
own statement. The founding law separates them: **structure never enters the charge table, and no charge
value ever informs a structure cell.** The bridge between the two tables is the research object, and the
law exists so that measuring it cannot be circular.

**The seal chain.** Forty-three preregistrations are sealed, each by the act of committing it, so the seal
*is* the commit that introduced the prereg. Consolidation from the predecessor monorepo rewrote commit
hashes; `docs/seal-chain.md` resolves every prereg end to end through `docs/hash-map.txt`, and
`atlas.jsonl` is preserved byte-identical across that migration, enforced by a round-trip test.

**Passports.** Every Structure Atlas column carries an epistemic passport before it may enter a sealed
bet: an invariance verdict (`invariant` / `encoding-relative` / `parameter-relative` / `corpus-relative`),
what the column is a property *of*, and a recorded variance census. Of v1's eleven columns, **three are
admissible as-is, four more through a sealed collapse, and two carry `invariant` verdicts.** Anatomy v2
adds three columns of which **one** is admissible for a sealed bet. A passport table is complete when it is
honest, not when it is green: `starved` and `encoding-relative` are legal verdicts, undeclared is not.

**Anatomy v2 is a new sealed version, not an additive revision.** The schema licenses purely additive fills
for reserved column names only; Marrow's columns are not reserved, so under the amendment rule a changed
rule requires a new sealed version. `anatomy_v1.jsonl` therefore keeps its hash permanently, and **v1's own
tests passing unchanged is the evidence that v2 is a new artifact rather than an edit** — the artifact does
not merely assert non-interference, it demonstrates it.

**Reproducibility.** `pip install hardmap && hardmap repro` regenerates every cited number from committed
artifacts and exits nonzero on any mismatch; the manifest carries **28 claims**, each mapping claim id →
entrypoint → expected value → tolerance → tier. `hardmap verify` runs an internal-coherence sweep of **ten
checks** — estimates inside their CIs, Cramér's V in [0,1], netted ≤ raw where a theorem forces it,
marginals summing to n, and two gates the program added after being caught by their absence (below).

---

## 3. The eight assertions

Each assertion carries an evidence class. **PROVEN** means the literature proves it and this program
verified the computation. **MEASURED** means this program measured it under a seal. **CITED** means the
program audited a claim it did not itself prove.

### 3.1 Hardness is a vector, not a scalar — MEASURED

Eight charges were recorded per problem, and they do not compress. The effective dimensionality estimator
returns **k\* = 1** with a verdict interval of `[1]` on the founding canon, **k\* = 1** again on the tripled
roster, and the same on the generated universe's low-rank arms. Three scales, one answer: there is no second
dimension to find.

The consequence is linguistic as much as statistical. *"How hard is this problem"* is malformed without
*"which way"* — a problem may be NP-complete to decide, tractable to approximate, and fixed-parameter
tractable at once, and no single ordering reproduces that.

### 3.2 The field's flagship regularity is roster-conditional — MEASURED

The coupling between approximability and parameterizability is the field's most-cited structural
regularity. It is real, and it is partly a portrait of which problems people chose to study.

Two separate results establish this, and they are different statistics on different populations.

**The sealed out-of-sample falsification.** Prediction B1 held that the gradient would survive on rows
recruited after the canon. On the v3-new population the corrected V is **0.0**, against the v2 confidence
interval of **[0.53, 0.92]**. The prediction was sealed before the rows existed and it was **falsified**.

**The measured four-population arc.** Ordered from the canon's core outward, the coupling reads **0.73** on
the canon (full-roster V = 0.7293), **0.39** on in-network v3-new rows, **0.26** on the generated universe
(V = 0.2555, CI [0.13, 0.398]), and **0.10** on the periphery. The periphery sits below the generated
universe's baseline.

A third measurement sharpens rather than softens this. On the generated universe the one robust directional
residual runs the *other way*: corrected Spearman **−0.564** at the v1 anchor and **−0.140** at arity 4,
CI (−0.166, −0.114), excluding zero at both. Whatever produces the canon's clean positive gradient, the
generated universe's surviving directional signal leans against it.

### 3.3 What was called "locality" is two properties — MEASURED

A single blind-coded coordinate was expected to carry both approximation and parameterization. It carries
one. On the pooled 111-row population, locality's association with **approximation is V = 0.547** and with
**parameterization is V = 0.231**, with the two intervals separated. The pattern replicates across three
populations, approximation in the 0.55–0.58 band and parameterization in the 0.14–0.23 band.

One word had been naming two mechanisms. This is the program's one robust positive structural association,
and it is half the size of the thing it was originally believed to be.

### 3.4 Where structure is fully readable, it determines fate — and blending closure is what makes the tractable side tractable — PROVEN

On the Boolean universe, **46 distinct closure fingerprints map to 46 charge profiles with zero
ambiguity.** A lookup table built from arity ≤ 3 alone scores **93.87% exact** on the 3,982-class arity-4
holdout.

Neither half of this assertion is the program's discovery, and the section says so plainly. The
determinism is the dichotomy theorems — Schaefer, Bulatov–Zhuk, Barto–Kozik, and the KSTW line — proven
cell by cell. What characterizes the tractable side is closure under *blending* operations: a solution set
closed under majority, or under an affine combination, or under a semilattice meet, is tractable, and the
classification says these are the only ways it can be. The program computed these conditions, tested them
against known answers at two domain sizes, and confirmed them. It did not prove them.

The contribution here was negative and is recorded in §4: the program discovered that its own experiment
could not test what was already proven.

### 3.5 That determining structure is invisible from the surface — MEASURED

If closure decides fate where it is readable, the question is whether it can be read off a problem's
surface description. It cannot. Surface-combinatorial features recover *membership* facts nearly perfectly
— **0.983 and 1.000** on the positive control — and recover *closure* properties not at all: **every
closure target scored at or below its null.**

The positive control is what makes this a type boundary rather than a broken pipeline. The same features,
the same fits, the same folds recover one class of fact and not the other. What decides hardness cannot be
read off the problem's face.

### 3.6 On natural problems, surface anatomy predicts nothing that fame did not already — MEASURED

The one apparent positive on natural rows was a **+0.0685** lift on the decision charge, significant
against a fold-weighted null. It does not survive stratification.

Within problem families the model recovers **exactly zero** — 170 correct of 255 against a within-family
baseline of 170 of 255, across the three families that clear the power floor. Within coverage profiles it
recovers **+0.0188**. Two independent stratifications, no residual.

The sharpest evidence is not the zero. On `logic-proof`, the one admissible family whose label genuinely
varies, the model scores **significantly worse than its own baseline** — 10 correct of 49 against 17 of 49,
exact binomial p = 0.0359. That is anti-signal: a model carrying real structural information would not
degrade below the base rate precisely where the base rate is weakest. The model was reading which
literature recorded the row.

The closure-grade retest is unaskable. Only **34 of 345** natural rows possess a citable standard
relational presentation over a fixed finite bounded-arity template — and a closer pass pinning those
templates as explicit tuple-sets reduced it further, to **28**.

### 3.7 The census backbone — refutation difficulty concentrates where hardness concentrates — MEASURED

Proof contradictions localize toward the satisfiability threshold. Mean forced-core contradictions at
n = 60 run from **1.0** on over-constrained instances to **272.6** approaching the threshold, with two
structurally different samplers agreeing and planted-core calibration passed.

### 3.8 The literature's hardness bookkeeping fails audit — CITED, plus one proven-here cell

A sweep of published inapproximability cells found **8 of 9 defective**, all from one repeated unchecked
inference. Per-problem counting-hardness proofs exist for **31% of the canon and 18% of the expansion**;
the rest of the field's counting claims rest on a generic stamp.

And at least one universally-cited theorem appears never to have been written. The atlas's
`geometric-disk-cover` row is **free-placement** — unit disks with free centres. Marx (ESA 2005, Thm 5)
proves the result for **squares**; the disk-specific line (Marx–Pilipczuk; IWPEC 2006) covers only the
**discrete-centres** form. The free-placement statement the literature cites has no located proof. The cell
was **retracted to `open`** at a dated owner sitting — 21 cells promoted, that one retracted — and it stands
at `open` in `atlas_v3.jsonl` today, absent from the 21-cell promotions artifact.

One gap was filled rather than only recorded. `minimum-sum-of-squares` carried a citation that did not
establish its value; the disposition check produced a one-paragraph reduction from PARTITION, and the cell
entered as the program's first original **`proven-here`** result.

---

## 4. The negative results

These are the program's largest section by volume of sealed verdicts, and they are the reason the positives
above can be read as measurements rather than as hopes. Each is quoted at its sealed strength.

### 4.1 Pebble — the expensive instrument was absorbed by a free one

A point-to-set instrument (*reach*, ξ) was designed to measure how far information about a partial solution
propagates. Building it took a disqualification and a redesign: the pairwise instruments were
**DISQUALIFIED** when a parity diagnostic read **0.03** at maximal propagation, because reach is
point-to-set and they measure point-to-point.

Qualified, it produced a real result — reach on the Boolean census is an algebraic dichotomy tracking the
Schaefer split, strengthening with n. And it is terrain-relevant: **+0.096 held-out increment, p ≈ 0**.

Then a free relation-level scalar absorbed it. `tuple_dispersion` — a pure property of the relation,
needing no graph, no instances, no sampling, no solution sets — proxies reach at **corr 0.78**, and the
scalarization hypothesis *reach ≈ f(geometry, scalar)* collapsed to **reach ≈ f(tuple_dispersion)** with the
geometry term contributing **+0.003 to +0.023**, inside noise. The sealed verdict: **the expensive
instrument earns a characterization, not a keep.**

The finding's own caveat is recorded with it and is not a softening. Reach and the terrain charge it
predicted are both solution-set-geometry summaries of the *same ensemble*, measured on different draws — so
the contest against a *constraint-level* scalar was **structurally uneven, not a fair fight reach won on
merit.** The un-circular test, reach against a non-geometry charge, was deferred rather than claimed.

### 4.2 The conditioning that could not be asked

The program's central absorption question — does bounded width absorb the approximation↔parameterization
coupling — is **unaskable in the Boolean single-relation domain at any arity.** On the parameterization-real
rows, unbounded-width coincides exactly with purely-affine by Schaefer's classification, so the
conditioning variable and the outcome are the same fact wearing two names. The arm was **dropped from the
seal** at Prism v2 rather than deferred. Domain size ≥ 3 is its smallest well-posed home.

This is not an underpowered result. No sample size in that domain would answer it.

### 4.3 The powered locality miss

The absorption hypothesis was re-posed on natural rows, where it could be asked. At three classes it was
declared **INSUFFICIENT and terminal**: 7 of 9 cells reached expected count ≥ 5 on n = 111, and the power
floor was not cleared. Collapsed to two classes, where the floor *is* cleared, it was scored and **missed**:
unconditional V **0.283** rises to conditional V **0.453**, a shrinkage of **−0.60**. Conditioning on the
proposed absorber made the association *stronger*. It does not absorb.

The 3-class result was declared insufficient before the 2-class result was computed, and the declaration was
not revisited afterwards.

### 4.4 The circular prediction

The flagship estimator of the bridge grid was to predict a problem's full charge profile from its structural
coordinates, including its closure fingerprint. Grounding found the prediction **circular by construction**:
on the Boolean universe the charges are *computed from* those coordinates by the dichotomy oracles, so the
model would have been asked to recover a function from its own inputs — 46 fingerprints to 46 profiles, a
100% ceiling.

The spec's own netting rule zeroed its own headline. It had declared that theorem-forced coordinates earn
calibration credit only and that headline accuracy is net-of-forced; applied honestly, every point of the
prediction's accuracy was theorem-forced. **The discipline caught its author**, and the prediction was
retired before it was sealed.

### 4.5 Terroir — the natural-side lift was fame

Reported in full at §3.6. The verdict was **FAMILY-BORNE**, and the sealed arm produced a **miss**: the
prediction that dropping the encoding channel would collapse the lift below half its size failed — it landed
at **+0.0476**, still significant at p = 0.0010. The bet was wrong, and the residual is information: the
family signal rides several channels, not one blunt column.

A second sealed prediction hit and was **demoted by its own artifact**. Imputing away the absence markers
drove the lift to −0.1339, well past the threshold — but imputation at a ~50% absence rate does not only
remove absence information, it asserts a false substantive value on 166 rows. A manipulation that degrades
the matrix by construction makes its prediction nearly unfalsifiable, so passing it is weak evidence. The
informative number is the sealed secondary, which imputes nothing: **+0.0188** within coverage profile.

### 4.6 Marrow — the closure retest has no population

Reported at §3.6. Three independent structural blockers, each sufficient alone: no problem family reaches
the admissibility floor under any reading of the admission rule; the value-optimization stratum is
**constant** on the decision charge, 18 rows of 18 sharing one label; and only two families hold five or
more rows, so the fold structure the test inherits cannot be built.

The verdict is **INSUFFICIENT, declared in advance of any attempt** — and insufficient is not evidence of
absence. The closure question is not answered here. It is unasked for want of a population.

---

*Sections 1, 5–7 follow at W3. The number audit (W2) runs against this text before they are written.*
