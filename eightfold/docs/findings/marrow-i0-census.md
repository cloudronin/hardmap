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
