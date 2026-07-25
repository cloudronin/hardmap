# The codability spectrum — which anatomy is even askable

**Date:** 2026-07-25. Anatomy v1, milestone S2. Artifact: `anatomy_v1.jsonl` (4417 rows, 11 columns) with
`anatomy-passports.json`, `anatomy-instruments.json`, `anatomy-s2-conditionchecks.json`. Contract:
`Anatomy-SCHEMA.md`. Nothing here rescores any bet; every number is a property of the *instrument*, not of
the world.

## The finding

The program set out to record what each problem **is**, expecting the hard part to be *coverage* — finding
citations. Coverage turned out to be the easy half. **The hard part is that candidate structural features
differ enormously in whether they can be measured at all**, and nothing about a feature's appearance
predicts where it sits on that spectrum.

Eleven columns were built and each was put through three checks — **invariance** (is it well-defined on its
object?), **variance** (can it carry a contrast?), **readability** (can it be read reliably?). The result:

> **3 of 11 columns are admissible for a sealed bet as-is. 4 more only through a declared collapse.
> 4 are excluded outright. Eleven columns, eleven honest verdicts, zero passes by omission.**

That is the finding. Not "the atlas is 84% covered" — which is also true, and would have been the
misleading headline.

## The spectrum

| tier | columns | what limits them |
|---|---|---|
| **Invariant and usable** | `poly_fingerprint`* , `engine_type`* | the Galois connection makes polymorphism properties invariants of the constraint language; both need a declared projection/collapse (*see below) |
| **Relative but declared, usable** | `locality_class` (κ 0.646), `encoding_type`, `class_size` | properties of the pinned encoding — legitimate once *what they are properties of* is stated |
| **Usable only collapsed** | `kernel_status`, `decomposition_facts` | starved at full resolution; healthy at a coarser, sealed contrast |
| **Measurable but not readable** | `arity_class` (κ 0.360) | presentation-relative *by theorem* — there is no invariant fact to read |
| **Not a structural feature at all** | `reduction_out_degree` | corpus-relative: a fact about what someone recorded, movable by tomorrow's publication |
| **Too thin to contrast** | `objective_type`, `self_reducibility` | real values, starved marginals |

## Four things the spectrum taught that a coverage report cannot

### 1. Coverage and usability are different properties, and the field guards only one

`decomposition_facts` is the best-covered cited column in the atlas: **65 of 77 eligible rows (84%)** carry
a citable decomposition fact, against a kill-criterion floor of 45. It passes coverage handsomely. It is
also **unusable as a contrast variable**: its one boolean field is 48 True / 3 False (**94% modal**), and
its other three fields carry **46 distinct values across 48 fills** — cited prose wearing a column's
clothes.

> **Had the census not been extended to cited columns, this would have shipped looking like the best-covered
> column in the atlas.**

R20 guards coverage. The variance census guards usability. **The field's compendia have only ever had the
first guard.** The ladder then does what it was built for: the *record* stays as a reference resource, and
the *presence binaries* (has-citable-bounded-treewidth-class 48/17; has-citable-excluded-minor 31/34)
become the sealed contrast. Reference resource above, contrast variable below, both honest.

### 2. "Definitional-looking" predicts nothing

`arity_class` was specced **`derived (definitional)`** — it looked like the easiest column in the project.
Two blind coders agree at **κ = 0.360**; a mechanical lexicon agrees with neither. The reason is a theorem,
not carelessness: **arity is a property of the presentation, not of the problem.** 3-SAT as a ternary CSP is
`bounded-local`; the same instance as a hypergraph covering problem is `unbounded-fanin`; nothing about the
problem moved. There is no invariant fact in the pinned text, so **no reader — human, model, or regex — can
code it reliably.** κ = 0.360 *measures that absence.*

Against `locality_class` at **κ = 0.646** on the same corpus, by the same instrument, this is a genuine
spectrum: some anatomy is blind-readable and some is not, and the confident typing was wrong before the
instrument ran. The instrument is how we found out.

### 3. The failed column and the landing column are the same question, asked at two levels of invariance

The constructive half. The problem-invariant version of *"how wide are the interactions?"* is not an arity
label at all — it is a **width measure of the constraint hypergraph**: treewidth, hypertree width,
submodular width. Those survive re-encoding in exactly the way an arity label does not. **That is
`decomposition_facts`**, cited at R20 in the same milestone.

> `arity_class` and `decomposition_facts` are the same question asked at the wrong and the right level of
> invariance. The instrument strain did not merely flag a bad column — it re-derived a known theorem from
> the direction of measurement: **anatomy must be read from structure that survives re-encoding**, and the
> field settled fifty years ago which structures those are.

### 4. A row that keeps catching drift is an instrument

`graph-3-coloring` has now forced the same class of correction **three times** — methods instances 9 and 17,
and again here (its pinned encoding is a random G(n,m) ensemble, a.a.s. non-planar with treewidth Θ(n), so
general-problem planar facts describe a different object). Three is not coincidence. Its id names a classic
decision problem, its pinned task is a promise version, and its encoding is an ensemble: **three objects
reachable from one row**, so any rule that conflates them fails there first. It is now a **registered
typing sentinel** (`anatomy.TYPING_SENTINELS`), to be included in every future typing rule, validator
selftest, and coder qualification — the way `knapsack` became the dissociation exhibit.

## The gate qualified itself on its own artifact

The passport audit found **five defects in its own logic**, every one on first contact with real columns:
route-conditioned readability let κ = 0.36 pass; `starved: None` auto-passed an unbuilt column;
`corpus-relative` had no exclusion path; and record-valued columns (`decomposition_facts`,
`poly_fingerprint`) read admissible *by omission* — a dict cannot be contrasted on.

That count is the gate's certification, not its embarrassment: **a gate that finds five defects in itself on
first contact with real data is a gate that was actually run.** It is also the S1 validator-selftest rule
(*real rows, not synthetic constructions*) proving out one level up — **gates need real columns to debug
gates.**

## Closing exhibit — the discipline rediscovering its own result

`kernel_status` is starved at full resolution (5 values, two cells under the floor). Its **only** admissible
collapse, found from the variance side by a groupby with no knowledge of the prior work, is **poly-kernel vs
no-poly-kernel *within* FPT** — 24 / 22, healthy.

That is exactly the contrast **Mosaic P6 sealed** as its informative residual, and exactly what the **Bridge
Ledger §6 correction** independently established from the theorem side: the FPT ⟺ some-kernel equivalence
holds only for decidable problems and carries *no efficiency content*, so the poly/no-poly distinction
**is** the content.

Three instruments — a sealed prediction, a theorem-pinning pass, and a variance census — asking different
questions, arriving at the same design. **That is what it looks like when the rules encode real structure
rather than ritual**, and it is the reason to trust the other verdicts in the table.

---

*What the atlas can now say, and could not before: for every column, **what it is a property of**, **what it
can carry**, and **what it has already carried**.*
