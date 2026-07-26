# The hardmap program — a consolidated account

**Draft status: W3 — complete draft, pre-review.** Every number was extracted from its artifact during
drafting and carries a row in [the claims map](claims-map.md); none was transcribed from a prior note. The
number audit (`dev/audit_writeup.py`) passes with zero orphans and is itself probe-tested against
fabricated values.

---

## 1. The question and the object

**What this work cannot do, stated first.** Every hardness label here is conditional on the standard
separation conjectures: an `NPC` cell means *hard if P ≠ NP*. A model fitted on conditional labels
interpolates the assumption; it cannot out-know its training labels, and no amount of resolution turns an
interpolation into a separation proof. P versus NP is a single universally quantified statement about all
algorithms — the class of fact that only a theorem reaches. Nothing in this program bears on it, and where a
result below is theorem-grade it is the *classification* that is proven, never the separation. This
paragraph is not a disclaimer appended to the work; it is a boundary the work was designed inside.

**The question.** Complexity theory classifies problems by proving theorems about them one at a time. The
resulting body of knowledge is enormous, precise, and almost entirely unexamined *as a body*. Ask what
hardness is made of — whether the many ways a problem can be hard are one thing or several, whether they
can be predicted from what a problem *is* — and the field has no assembled object to answer from. This
program builds one and measures it.

**Two campaigns.** The **two-table program** asks the question of problems: it records what the literature
has proven about each problem's fate, records separately what each problem structurally *is*, and measures
the bridge between. The **proof census** asks the same question of refutation space: how plural the ways of
refuting an unsatisfiable instance are, and whether the ways converge as instances get hard. Different
objects, different instruments, one method. The paper's subject is the pair.

**The object.** Two tables and a law. The charge atlas records *fate* — eight charges per problem, each a
cited fact about the literature. The Structure Atlas records *what a problem is* — coordinates derived from
the problem's own statement, never from its fate. The founding law is the separation itself: **structure
never enters the charge table, and no charge value ever informs a structure cell.** The bridge between them
is the research object, and the law exists so that measuring it cannot be circular. Nearly every negative
result in §4 is the law refusing to let a question be asked the easy way.

**A frame, offered as exposition and carrying no claim.** Closure analysis is feasible-region analysis.
Convexity is itself a closure property — stability of a region under blending its points — and the
classification theorems that decide tractability are statements about which blends a solution set survives.
Read that way, this program's negatives say something geometric: the region's shape is what decides
hardness, and that shape is not visible from the syntax of the problem's statement. The frame is a teaching
device, sourced to a dated note; no result below depends on it.

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

### 3.7 The proof census — freedom in the large, compulsion in the core — MEASURED

*This is the program's second empirical campaign, and it is structurally unlike the six assertions above.*
Its object is refutation space rather than problem hardness; its instrument is a pair of structurally
different proof samplers, one building DAG refutations and one building tree refutations; it carries its
own sealed hypotheses (H1 diversity, H2 geometry, H3 sampler-independence), its own kill criteria, and its
own compute campaign. It is also **the program's one fully-positive result — both scored hypotheses
confirmed, neither kill criterion fired.** It is included here as the existence proof that the method
produces positives and not only well-characterised negatives.

The sweep covers n ∈ {20, 30, 40, 60} against clause-to-variable ratios α ∈ {4.5, 5.0, 6.0, 8.0, 10.0}, 50
instances per cell, 200 verified refutations per sampler per instance — **400,000 verified proofs** across
1,000 records.

**Freedom in the large.** Refutation sets are genuinely plural. Median pairwise Jaccard overlap between
independently sampled refutations of the *same* instance spans **0.044 to 0.165** across every cell and
both samplers — nowhere near the 0.95 line at which the plurality hypothesis would have been killed. There
is no single canonical proof waiting to be found; there are many, and they are mostly different.

**Compulsion in the core.** A forced core nevertheless emerges as instances approach the satisfiability
threshold. At n = 60 the mean backbone — clauses appearing in nearly all sampled refutations — runs from
**1.0** on over-constrained instances to **272.6** near the threshold, peaking at **283.28**. Over the same
range, median proof length grows from 315 to 6,976, a **22.1×** lengthening.

Both effects are real at once, and that is the finding: the proofs get long and various, and yet they are
increasingly compelled to share a core. **Freedom in the large, compulsion in the core.**

**Replication.** Twelve trend comparisons across four sizes and three metrics; **eleven agree** between the
two samplers. The single divergence is discussed in §5 — it is explained mechanistically rather than
excused, which is what the replication standard was written to force.

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

## 5. The methods contribution

The most transferable output of this program may not be any of its findings. It is a ledger of the ways
careful measurement went wrong, kept as a first-class artifact and converted into gates that now run in
continuous integration.

The ledger holds **27 numbered entries spanning 6–32**, with instances 1–5 predating the file. It is not
renumbered, because an instance number is a citation target. Every entry follows one shape: what happened,
why the disconfirming information was already present, and what rule now prevents it. The program's
characteristic failure mode has a name — **metadata already recorded, inference not drawn**. In almost every
case the fact needed to avoid the error was written down somewhere in the artifact and nobody joined it up.

**The taxonomy.**

*Errors in both directions.* A discipline that only catches flattering errors is indistinguishable from
pessimism. The ledger records bugs that would have manufactured hits — an averaged-per-class statistic
reading 0.797, a lookup with a 100% ceiling, an arithmetic leak recovering a flag at exactly 1.0000 — and
bugs that manufactured misses: a hash-coded categorical fed to a threshold-splitting model, whose repair
moved a result from +0.009 to +0.068. Only once both directions appeared could the ledger claim to be
measuring rather than merely doubting.

*The tidy-number tell.* Both directions had the same signature: the number was too tidy. A recovery of
exactly 1.0000 is not learning, it is reading; a null of exactly +0.009 on a designed-for signal is not a
result, it is a dead encoder. This became a mechanical gate — any headline statistic exactly extremal, or
exactly equal to its own null, must carry an acknowledgement in its own artifact explaining why the
exactness is expected. Unacknowledged exactness fails the build.

*Census before seal.* No column may carry a bet before its marginals are counted. The rule caught columns
too concentrated to support a contrast, and then — when a genuinely high-cardinality column arrived — caught
the opposite failure it had been blind to: a column with as many distinct values as rows is a row
identifier, and carries exactly as little contrast as a constant does. Both ends are starvation; the gate
had learned only the end it had been burned by.

*Denominator matching.* A lift is `accuracy − null`, and the subtraction means nothing unless both terms
were computed on the same rows. Three separate occurrences — a conditional shrinkage, a sociology increment
on a different population, and a within-family null paired with an all-rows accuracy — turned this from
anecdote into a gate that fails the build when a lift's terms do not share a declared row set.

*Expression, not artifact.* An exactly-extremal value has at least three causes that look identical in
serialized output: an estimator clamping at its boundary, a p-value at the limit of its own form, and a
statistic whose expression makes it constant regardless of input. They are separable only by reading the
code path. Two diagnoses made from the shape of the artifact were both wrong; two made by reading the
expression were both right.

*It pointed the unflattering way.* One defect survived review specifically because its output was
disappointing. A block computing `acc[k̂] − acc[1]` at k̂ = 1 was computing a value minus itself: identically
zero on the real data and on all 150 nulls it drew and discarded, and reporting a negative result that no
input could have changed. A bug that manufactures a null attracts less scrutiny than one that manufactures a
finding, and that asymmetry is itself a bias the ledger now names.

*Chat is not an artifact.* A claim whose only provenance is a conversation is unsourced by definition,
however confidently stated and whoever stated it. When this document's own claim list was assembled, three
of nine entries arrived from conversational synthesis rather than from a record. Building the
claims-to-artifacts map **before** writing prose caught all three; a map written afterwards would have
caught none of them, because each would have been handed a plausible-looking pointer by the same synthesis
that produced it.

**The census's methods exhibit.** The two proof samplers occupy regions of proof space separated by orders
of magnitude — tree refutations at n = 60 run to 6,976 median resolutions where DAG refutations run to 48.
The replication standard declares that gap **a finding, not an artifact**, and judges sampler agreement on
*trends* rather than levels. That standard then did real work: of twelve trend comparisons, the single
divergence was explained mechanistically rather than excused — proof size explodes 22.1× toward the
threshold, so a growing shared core becomes a shrinking *fraction* of a much longer proof, and the overlap
metric falls while the backbone rises. **Divergences are explained, or the verdict does not ship.**

**The delegation protocol.** Several entries in the ledger record a directive being measured before it was
executed, and the measurement changing it. An instruction to merge two absence markers turned out to be a
no-op on three of four columns and destructive on the fourth. An instruction to seal a prediction was
refused because the prediction was circular by construction. The protocol that emerged is narrow and
specific: *execute the ruling, but measure the instruction first, and report when the measurement
contradicts it.*

**The gates.** `hardmap verify` runs **ten** coherence checks on every artifact set — including the two the
program added after being caught by their absence. Each was written to fail loudly, and the two newest were
probe-tested by planting a defect and confirming the gate fires, on the principle that **a check never
observed to fail is not known to work.**

---

## 6. Open instruments and the standing state

**The prospective registry.** One instrument remains live and is confound-free by construction. It records
predictions from fitted models *before* the corresponding literature research is done, hashed and committed
so the ordering is verifiable, and grades them as cells fill. Its floor is pinned at **n = 57** — the count
a one-sided binomial needs to detect a lift of +0.15 over the base rate at 80% power. It currently holds
**21 descriptive entries and zero scored cells**: the 21 predate the registry's sealing and are marked
descriptive-only, and no cell may enter the scored count before its wave is sealed predict-then-fill.

The registry also carries the rules that govern what an eventual hit may claim. A hit is
*foresight-certified* by the ordering alone; to be *mechanism-attributed* it must additionally survive the
within-family cut and the closure-versus-surface contrast. Those rules were written before any cell was
graded, precisely so that a positive result could not be re-interpreted into significance after arrival.

**The two-verdict stack.** Surface anatomy was measured on natural problems and answered no (§3.6). Closure
anatomy cannot be measured there at all, for want of a population (§3.6, §4.6). Retrospection is therefore
closed at both grades, and the mechanism question now lives **exclusively prospectively** — in the registry,
at zero of fifty-seven.

That is the measurement phase completing rather than a defeat. The question was asked at the resolution the
available evidence supports, answered where it could be, and declared unanswerable where it could not.

**Banked directions, none committed.** Three are named with their fill routes and their limits.
*Geometry probes* would measure feasible-region shape directly — blend-violation rates and relaxation
tightness — reaching the rows the closure admission bar excludes; their qualification study on the Boolean
roster, where true closure is oracle-known for every relation, is the one cheap executable thread.
*The relaxation-resistance certificate* would add a derived column for predicates whose solution sets
support a balanced pairwise-independent distribution; it is at survey confidence and **must be pinned before
any claim leans on it**. *The frontier map* would sample anatomy space to sketch the conditional
tractability boundary, gated behind a validated bridge model and inheriting the scope limit at the head of
§1.

**And the census is the natural seed of a separate paper**, if the backbone line extends to larger n, to
other proof systems, or to the width-lower-bound connection. Banked as an option, not committed here; this
document keeps it as one campaign of two.

---

## 7. Related work

The program positions against five lines, recorded as dated obligations in its own specifications.

The **meta-problem line** (Bulatov; Creignou–Khanna–Sudan; the AutCSP work) is the nearest existing claim
and the supplier of this program's oracles: it asks, given a constraint language, to decide its complexity —
the same bridge question, answered by theorem on the territory where theorems exist. **ISA/EHM** provides
the instance-level contrast: hardness measured per instance rather than per problem. **ISGCI** is the
transposed structural cousin — a curated graph-class catalogue with its own `Unknown` status, aligned here
with the `open` sentinel. **CoRCoD** and the structure-to-dynamics machine-learning literature are pattern
precedents for predicting behaviour from structural descriptors. And the **dichotomy program** itself —
Schaefer through Bulatov–Zhuk — is the lineage: it is what a complete answer looks like on the territory
where one is possible, and §3.4 is this program confirming its computation rather than extending its reach.

**The program's dated position, labelled as a position.** Its own specifications record that a two-table
object with a measured, out-of-sample bridge remains unclaimed territory, per literature hunts conducted
during design. That statement is offered as **the program's dated position and not as reproducible
evidence** — the hunts' results are not in the repository, and re-running them now would be new work
requiring its own seal rather than synthesis of existing records. A position honestly labelled is worth more
than a search theatrically repeated.

---

*Complete draft. The number audit passes at zero orphans; the claims map carries every value's artifact.*
