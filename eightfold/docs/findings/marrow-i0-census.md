# Marrow v1 — the I0 census note

**Prereg:** `prereg_v15` · **Date:** 2026-07-25 · **Kill 1: FIRES** · **Marrow ships as a census note, not
a build**

Terroir closed the natural-side bridge claim at *surface* resolution (FAMILY-BORNE), and Arm A had already
closed the synthetic side at the same grade — *surfaces see membership, not closure*. Marrow was to make
**closure-grade** invariants exist for natural rows, so the one legitimately-open retrospective question
could be asked of the anatomy the dichotomy theorems say is real.

The census says there is not enough of it. **34 of 345 natural rows carry a citable standard relational
presentation over a fixed finite bounded-arity template**, against a floor of 40. The spec named this
outcome in advance as legitimate: *"the natural atlas is presentation-poor" is itself a statement about
where closure anatomy can exist.*

---

## 1. The census

| stratum | n | |
|---|---:|---|
| direct-csp | 22 | CSP(Γ) for a fixed finite Γ of bounded arity |
| vcsp-shaped | 18 | Min-Ones / Max-Ones / Max-CSP over such a Γ (KSTW) |
| promise | 1 | PCSP theory (BBKO) — `robust-csp` |
| no-presentation | 304 | `n.a.` with a stated reason |
| **total** | **345** | |

**Presentable (strata 1+2) = 34 under the recommended reading. Kill 1 floor = 40. FIRES.**

The planning estimate was **82**, from a regex over problem names; the spec's own estimate was 60–120. The
strict test removes what a name-pattern happily accepts, and **57 near-misses are excluded with
individually stated reasons**:

- **unbounded arity** — `dominating-set` is Min-Ones over (x_v ∨ *its whole neighbourhood*), outside KSTW's
  finite Γ. Same for the domination family, `set-cover`, `hitting-set`, `max-coverage`.
- **global side constraints** — `equitable-coloring` (balance), `acyclic-coloring` (no bichromatic cycle),
  `harmonious-coloring` (global injectivity), `connected-vertex-cover` (connectivity), `min-bisection`
  (balance), `feedback-vertex-set` (acyclicity). Each has a colouring or Min-Ones *core* plus a condition
  no finite-arity Γ expresses.
- **quantification** — `choosability` (∀ lists ∃ colouring, Π₂ᵖ), `qcsp`, `tqbf`, `stochastic-sat`.
- **infinite domains** — `betweenness`, `cyclic-ordering` are ordering CSPs (Bodirsky), a different theory.

## 2. What the census surfaced that the spec did not settle

**Polymorphisms are computed *of a template*.** So the admission question is not "is this row CSP-shaped?"
but "**is there a fixed finite template whose Pol we can compute?**" Where the template is part of the
*input* — H in `graph-homomorphism`, Γ in `maximum-csp`, k in `chromatic-number` — there is no fixed Γ and
`poly_fingerprint_natural` is **undefined on that row**. That is a computability fact, not a preference,
and it decides Kill 1.

It cuts both ways, which is why it is recorded rather than folded silently into a number: it **removes 7**
varying-template rows and **adds 4** fixed-template rows the first pass had omitted (`d-hitting-set`,
`k-set-packing`, `three-dimensional-matching`, `3-dimensional-assignment` — self-caught).

| reading | n | Kill 1 |
|---|---:|---|
| **principled** — fixed template required, omissions corrected | **34** | **FIRES** |
| as-censused — CSP-shaped, template-fixedness not applied | 41 | CLEARS |
| permissive — also admits varying-template and unpinned-field rows | 45 | CLEARS |

**The reading that clears the floor was available and was not taken.** Choosing an admission rule after
seeing which one clears a kill criterion is the failure this record exists to prevent, so the band is
reported and the ruling is flagged as pending rather than made quietly. **It changes Kill 1 and nothing
else** — see §3.

## 3. Terroir-C cannot run, and that verdict *is* robust

M0b was a separate gate by design, because **supply is not viability**. At the planning estimate the two
disagreed: 82 rows would have cleared Kill 1 while the minimum detectable effect sat at +0.10.

Three independent structural blockers, all firing:

1. **Zero admissible families, under *every* reading.** Principled: sat-csp 15, graph 13, optimization 3,
   geometric 1, logic-proof 1. As-censused: graph 19, sat-csp 16, rest ≤ 3. Nothing reaches n = 30.
2. **Stratum 2 is constant.** The 18 vcsp-shaped rows are **18/18 NPC — modal share exactly 1.000**. Not
   merely starved: *constant*. Half the presentable population cannot support a `decision` contrast under
   any statistic. (The plan carried 90.6% from the regex set; the stricter census made it worse.)
3. **The fold structure is infeasible.** Terroir-C inherits family-grouped 5-fold CV, and only **2**
   families have ≥ 5 rows.

Even discarding the screen entirely, the pooled MDE is **+0.1212**. For scale, Terroir's headline lift was
+0.0685 and its within-family residual was exactly **+0.0000** — and a within-family residual is by
construction smaller than the headline it decomposes.

> **Sealed sentence.** Terroir-C cannot run as a within-family residual test on this population: every
> family falls below n = 30, so the statistic A4 defined has no admissible stratum to be computed on.
> **Declared INSUFFICIENT in advance — and INSUFFICIENT IS NOT EVIDENCE OF ABSENCE.** The closure question
> is not answered here; it is *unasked for want of a population.*

## 4. Decisions sealed anyway, so a resumption inherits them

Marrow does not build, but `prereg_v15` pins what was decided, so a resumption starts from settled
questions:

- **Anatomy v2, not an additive v1.1.** §4's additive licence covers *reserved names only*, and none of
  Marrow's columns are reserved; §0.3.3 governs — *a changed rule is a new sealed version.* Adding columns
  would also rewrite `anatomy_v1.jsonl`'s bytes against its `tolerance: exact` pin.
- **Passports split.** `presentation` is **encoding-relative** (its declared object *is* the choice);
  `poly_fingerprint_natural` and `engine_type_natural` are **parameter-relative** — invariant *given the
  pin*. Boolean `poly_fingerprint` earns `invariant` because there the relation **is** the object with no
  choice to make. This is the `arity_class` lesson applied before the failure instead of after.
- **`fractional_poly_facts` reserved, not shipped** — VCSP was already ruled NOT BUILDABLE in this repo on
  classification-gap grounds. Reserving it now is what makes a later fill legal under §4.
- **Flags 7–10 are `n.a.` by theorem** on non-Boolean rows (KSTW and Marx do not transfer), and
  `derive_engine_type`'s `fs = bool(flags["affine"])` is quarantined as the build's chief correctness risk —
  that collapse breaks at k > 2.

**The good news, for whenever it resumes:** the machinery is largely built. `foundry/foundry/domain3.py`
already classifies |D| = 3 languages including CSP(K₃); `_closed_under` is domain-agnostic; nothing
enumerates f: Dⁿ → D anywhere — every check tests *named* operations. The anchor set is already green at
both domain sizes.

## 5. What survives

**Terroir-C does not.** The FAMILY-BORNE verdict's one legitimately-open retrospective question stays open,
and now has a *measured reason why* rather than a gap.

**The registry might, by owner ruling.** Spec §3.2's registry upgrade does not depend on Terroir-C — a
prospective predict-then-fill wave carrying closure-feature predictions is confound-free by construction
and accumulates regardless of retrospective population size. But it needs the columns, which need M1–M4,
which Kill 1 stops. **Building them for the registry alone is a live option and an owner decision, not a
consequence of this seal.**

The prospective registry at 0/57 remains the program's one armed confound-free instrument.

---

## 6. Two gate findings from this milestone

**The §9.1 erratum.** The sealed passport table read *"4 of 11 admissible as-is; 2 more via a sealed
collapse"*; the live gate says **3 and 4**. Two rows were overtaken: `decomposition_facts` was built at S2,
and the RECORD-VALUED rule was added afterwards — under it `poly_fingerprint`'s original **yes** was a pass
*by omission* (typed non-categorical) rather than by evidence. `repro/manifest.yaml` already carried the
corrected numbers; the sealed table was the stale copy. No rule changed and no cell moved, so per §0.3.3
this is an erratum corrected in place with its date.

**The watch-set defect, found twice in two commits.** Terroir widened the tidy-number gate's glob from
`grid_*results*.json` after finding it blind to its own results file. One commit later, Marrow's census and
power artifacts matched *neither* widened pattern — the same defect, immediately. The shape was wrong, not
the pattern: **a gate keyed to whatever the last project named its files fails OPEN, reporting a pass over
files it never opened.** The watched set is now a declared tuple in one place.

And the honest boundary on that fix: adding `*factors*.json` surfaced **16 unacknowledged extremals** in a
project this pass has not examined. Waving them through a LEGACY table without reading them would be
rubber-stamping — the one thing this gate must not become — and dropping the pattern silently would be
worse. So the pattern stays out, **the reason is recorded in the gate itself**, and the backlog is queued
as its own task. A watched set that grows only as fast as someone actually adjudicates it is the honest
kind.

---

## Artifacts

`prereg_v15.json` · `marrow-i0-census.jsonl` (345 rows) · `marrow-i0-census.json` ·
`marrow-terroir-c-power.json` · `marrow_census.py` · `marrow_power.py` · 5 tests in
`foundry/tests/test_grid.py` · `_watched()` in `hardmap/verify.py`.

**Frozen and untouched:** `anatomy_v1.jsonl` `8ff11f8a`, `atlas_v3.jsonl` `e62f3c28`,
`grid_arm_b_predictions.json` `cc5bb389`. Marrow built no column and moved no byte of the sealed atlas.

---

## 7. Rulings (2026-07-25) and the build they authorised

### Ruling 1 — the principled 34, and the question it answers

**This is answer-believability, not taxonomy.** Where the template is input, `poly_fingerprint_natural` is
not *hard to compute* — it is **undefined**, and a derived column carrying undefined values dressed as facts
would be the `arity_class` failure at derivation grade. The clearing reading (41) was available and would
have been wrong to take.

Band recorded with the ruling: **34 principled / 41 as-censused / 45 permissive.** And the verdict is
**per-corpus, not permanent** — the Zoo wave's tier-1 rows (QBF variants, succinct and counting SAT forms)
are largely fixed-template by construction, so the presentable population grows through ordinary
recruitment rather than through re-reading the rule.

### Ruling 2 — the two-verdict stack

> **Surface answered no, and closure cannot be asked: Terroir returned FAMILY-BORNE at surface grade, and
> Marrow's census shows the natural atlas has no population on which to pose the closure question — so the
> retrospective route to the mechanism question is closed at both grades, and the question now lives
> exclusively in the prospective registry.**

That is the measurement phase completing, not a defeat. The program's active posture is
**registry-plus-writeup**.

### Ruling 3 — M1–M4 built, scoped to the 34, for two consumers

Terroir-C stays INSUFFICIENT-as-sealed; nothing in the build reopens it. If the Zoo wave later grows the
fixed-template population past the floors, a Terroir-C revival is a **new seal on a new census**, not a
resurrection.

---

## 8. What the build produced

**M1 corrected the census downward, 34 → 28.** Writing the templates out as explicit tuple-sets made the
bounded-arity test *checkable* rather than asserted, and six admitted rows failed the same test that
excluded `set-cover`: `exact-cover-x3c`, `three-dimensional-matching`, `3-dimensional-assignment` and
`k-set-packing` all carry a per-element constraint over unboundedly many sets; `set-splitting` has one NAE
constraint per set and sets are unbounded; `minimum-sum-coloring` draws colours from an unbounded palette.

**Three of the four "self-caught omissions" the census *added* are in that list.** Only `d-hitting-set` was
correctly added. The census's additions were less reliable than its exclusions — worth knowing about the
next sizing pass. No verdict moves: Kill 1 had already fired at 34 against a floor of 40, and fires harder
at 28.

**M2 — all 7 Kill-2 anchors green** before a single natural row was derived (3-SAT → no tractable
polymorphism; Horn → semilattice; 2-SAT → majority; XOR → affine; CSP(K₃) → none; lin-eq-Z₃ → tractable but
unbounded width; order-on-3 → bounded width). `engine_type_natural` marginal: **neither 11 · bounded-width
11 · both 4 · few-subpowers 2.**

**M4 — Anatomy v2 frozen at `f802f2e5`, and `anatomy_v1.jsonl` still reads `8ff11f8a`.** v2 is a separate
registry (`V2_COLUMNS`), a separate passports file and a separate freeze record; v1's `COLUMNS` and
passports are untouched, and **v1's own tests passing unchanged is the evidence of non-edit.**

| column | passport | variance | admissible |
|---|---|---|---|
| `presentation` | encoding-relative | **STARVED — over-dispersed** | no (descriptive-only) |
| `poly_fingerprint_natural` | parameter-relative | record-valued | no (needs a named projection) |
| `engine_type_natural` | parameter-relative | categorical, modal 39% | **yes** |

**The starvation gate was one-sided, and `presentation` is what exposed it.** The inherited rule starves a
column whose modal value swamps the population. It said nothing about the opposite failure: `presentation`
has **28 distinct values on 28 rows**, modal share 4%, and not one cell clears the Cochran floor. A column
with as many levels as rows is a *row identifier* and carries exactly as little contrast as a constant does.
Both ends are starvation; only one was being checked. Fixed, and `presentation` correctly ships
descriptive-only.

## 9. The presentation audit — the second consumer, demonstrated

Run as a **diagnostic**; the scored instrument is Quarry v3 Z5 under `prereg_v16`.

**12 agree / 3 disagree, on the 15 rows where it is posable.** The three:

- `succinct-3-coloring` — **predicted at M1 before the derivation ran** as a disagreement *by
  construction*: the template is K₃ exactly as plain 3-colouring, so closure derives NPC while the cited
  charge reflects an input encoding the template cannot see. A scope limit, not an errata candidate.
- `tseitin` — the cited decision cell is `n.a.`, so there is no value to disagree with.
- **`3-coloring-extension` — the one genuine errata candidate**, computed NPC against a cited PH-complete
  with no restriction or encoding to explain the gap. For investigation to verdict.

**And the audit caught its own auditor first.** The initial run derived decision from satisfiability for
*all* rows and reported 14/28 disagreements. Thirteen were mis-specification: `CSP({OR2})` is trivially
satisfiable while `Min-Ones({OR2})` **is** vertex cover, so Schaefer answers the wrong question on every
VCSP row. It was caught because a disagreement *prediction* had been written down first — M1 said
disagreements should concentrate on instance-restricted rows, and the observed pattern didn't match, which
sent me back to the oracle instead of to the atlas. The 13 VCSP rows are `open`: this repo pins no decision
oracle for Min-Ones/Max-Ones, and KSTW Thm 2.12/2.14 classify approximability.
