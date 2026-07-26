# Geometry Probe A — the Boolean qualification study

**Prereg:** `prereg_v16` (eightfold) · **Date:** 2026-07-26 · **Verdict: QUALIFIED**
**Spec:** `eightfold/docs/notes/geometry-probes-note.md` §4

The program proved the feasible region's geometry is invisible from constraint syntax, and that closure
anatomy exists for only 28 of 345 natural rows. Probe A measures blendability directly instead of deriving
it. This study grades the looking before it is trusted anywhere that matters — on the 4,072-class Boolean
roster, where true closure is oracle-known for every relation.

**F2 law, carried in the artifact's docstring:** probe values never impersonate worst-case charges. A low
violation rate is a measured geometric property that may *associate* with charges; the association is the
research object. No charge is read or written by this instrument.

---

## What the probe measures

For a region *R* and a blending operation *f* of arity *m*, the **violation rate** is the fraction of
*m*-tuples drawn from *R* whose coordinatewise blend lands outside *R*. Closure is the special case
rate = 0. The probe's point is the **degree** — the continuous scale the theorems binarise away.

Four flavours, each with an oracle counterpart: **majority** (↔ bijunctive), **minority** (↔ affine),
**min** (↔ horn), **max** (↔ dual-horn).

## The design problem, sealed before running

On this roster |R| ≤ 15 and arity ≤ 4, so the rate is computable **exhaustively**. Exhaustively computed,
`rate == 0` is *equivalent to the oracle flag by definition*. A known-answer battery scored on the
exhaustive probe therefore passes by construction, and separation against oracle labels is 100% by
construction. **That is the theorem-forced-credit trap wearing an instrument's costume**, and it was named
in the seal so it could not be discovered in the results.

The split it forces:

- **Exhaustive arm — calibration only.** Verifies the implementation computes what closure means. Forced,
  and reported as forced.
- **Sampled arm — the actual qualification.** The instrument that would deploy on natural rows cannot
  enumerate a region; it samples one. Its resolution at a declared budget is not forced by any theorem.
- **And one direction is *still* forced.** Specificity is 1.0 by construction: if *R* is closed then no
  *m*-tuple violates, so every sample returns 0 and a closed class can never be called open. Only
  **sensitivity** is measurable.

## Score 1 — known-answer battery: exact, and it caught the answer key

**4,072 of 4,072 classes agree on every flavour, zero disagreements.** The implementation computes closure.
Calibration credit only, as sealed.

**The battery's first run failed — and the fault was in the expectations, not the probe.** A hand-written
case asserted that `NEQ2 = {01,10}` is affine but *not* majority-closed. `NEQ2` is `x ≠ y`, which is
2-CNF-expressible as `(x∨y) ∧ (¬x∨¬y)` — therefore bijunctive, therefore majority-closed. It is closed
under minority *and* majority. The instrument was right and the answer key was wrong. Logged in the file
per the seal's "fix and rerun is legal at this gate."

## Score 2 — sampled sensitivity: the measured resolution

On classes the oracle marks **not** closed, the fraction detected at each budget:

| flavour | open classes | B = 10 | B = 30 | B = 100 | B = 300 |
|---|---:|---:|---:|---:|---:|
| majority | 3,708 | 0.6543 | 0.8981 | 0.9873 | 0.9997 |
| minority | 3,995 | 0.9782 | 0.9995 | 1.0000 | 1.0000 |
| min | 3,660 | 0.8276 | 0.9508 | 0.9937 | 1.0000 |
| max | 3,660 | 0.8208 | 0.9484 | 0.9943 | 1.0000 |

**One hundred sampled blends detect non-closure with ≥ 0.987 sensitivity on every flavour**, and 300 reach
≥ 0.9997. Majority is the hardest flavour — its violations are the rarest of the four, which is why it needs
the largest budget.

Specificity is **1.0 and forced**, reported as such and claimed as nothing.

## Score 3 — RETRACTED before first citation

**The finding this section originally reported does not survive its typed null, and was withdrawn the same
day it was written.** It is preserved here as the record.

**What it said.** 85–99% of nonzero violation rates fall in a 0.05–0.50 "almost-closed" middle band; not
one of 4,028 admissible classes violates majority-closure above 0.50; the typical not-closed relation is
*slightly* unblendable rather than shattered; the dichotomy's binary carves a continuum near its bottom end.

**What was wrong with it.** The blend operations are **idempotent on repeats** — `maj(a,a,b) = a`,
`minority(a,a,b) = b`, `min(a,a) = a` — so a tuple containing a repeat lands back inside the region *by
construction* and **cannot violate**. Rates were computed over `product(rel, repeat=m)`, the full Cartesian
product, so every denominator contained a large block of tuples incapable of violating. Each rate was
therefore capped at the all-distinct fraction:

| r | cap (m = 3) |
|---:|---:|
| 3 | 0.222 |
| 4 | 0.375 |
| 5 | 0.480 |
| 6 | 0.556 |
| 10 | 0.720 |
| 15 | 0.809 |

**The ceiling was the cap.** At r = 3, 4 and 5 the *maximum observed raw rate equals the cap exactly*
(0.2222, 0.3750, 0.4800) — meaning those relations violate on **every** distinct triple and their true rate
is **1.0**. 527 classes sit at r ≤ 5 and are capped below 0.50 by arithmetic alone. "Not one class above
0.50" was a statement about tuple counting, not geometry.

**Conditioned on the tuples that could actually violate** (exact: violations occur only on distinct tuples,
so `rate_distinct = rate_raw / cap`):

| flavour | middle-band fraction, raw → distinct | classes above 0.50, raw → distinct |
|---|---|---|
| majority | 0.854 → 0.898 | **0 → 341** |
| minority | 0.992 → **0.314** | 33 → **2,910** |
| min | 0.873 → 0.811 | 244 → 578 |
| max | 0.873 → 0.811 | 244 → 578 |

Both headline sentences fail. The band's range is 0.31–0.90, not 0.85–0.99, and minority — where the raw
figure was most striking — collapses hardest. The ceiling claim is simply false: **341 classes** violate
majority above 0.50 under the typed null.

**Disposition, per the rule sealed with the check:** retracted before first citation. The distinct-
conditioned distributions are reported as data in `geometry_probe_deflator_results.json`, **and no shape is
claimed for them.** Naming a replacement finding in the same breath as retracting one would be the
identical eagerness at half the interval.

**Scores 1 and 2 are untouched**, and were never in question: the battery is a binary that repeats cannot
flip, and sensitivity asks only whether *any* violation was found. The QUALIFIED verdict and the licence
stand exactly as issued.

## Census before seal, on the probe's own quantity

The standing law applies to instruments too. All four flavours pass at **both** ends of starvation —
138–170 distinct values, modal share 9–13%, nothing over-concentrated and nothing over-dispersed.

## Verdict — QUALIFIED

The battery is exact and the sampled sensitivity is characterised per flavour per budget. The probe is
**licensed for natural-row ensembles with its accuracy characterised.**

**Natural-row deployment is explicitly not authorised by this run** and needs its own spec. What the licence
buys is the possibility: a measured closure-proxy needing only an instance generator would reach the 317
rows the closure admission bar excludes — the mechanism programme's entire missing population. This study
establishes that the instrument works. It does not establish that the deployment is affordable.

---

## The gate defect this run surfaced

Running the probe put a new results file in `foundry/foundry/results/lattice/` — and the tidy-number gate
passed it while containing four sensitivities of exactly 1.0.

**The gate's lattice path was wrong, and had always been wrong.** It read
`d.parent.parent.parent / "foundry" / "foundry" / "results" / "lattice"` — one `.parent` short, resolving to
`eightfold/foundry/foundry/results/lattice`, a directory that has never existed. The `if lat.exists()` guard
then made the miss **silent**: the gate reported PASS while watching nothing.

**Every Foundry lattice artifact has therefore gone uninspected since the gate was written**, including
`grid_arm_a_results.json` — whose `1.000` positive control is quoted in the write-up as assertion 5.

Fixed by resolving through the package (`Path(foundry.__file__).parent / "results" / "lattice"`), the same
idiom `_eightfold_atlas()` already used, rather than counting directory levels from a sibling. The fix
immediately surfaced three previously-unseen extremals, all explainable and now itemised:

- **the 100% determinism ceiling** (×2 files) — benign, and load-bearing: exactly 1.0 *is* Arm A's finding.
- **`per_flag_recovery.1valid.acc = 1.0000`** — the documented arithmetic flag leak, retained deliberately
  as evidence in the pre-fix run.

**This is the third distinct way this one gate has silently not watched something**: a glob scoped to one
project's filenames, a walker that descends into dicts only, and now a path that resolves nowhere. The
common shape is that all three **fail open** — they report a pass over files they never opened. A gate that
cannot distinguish "inspected and clean" from "never looked" is not a gate.

---

## Artifacts

`prereg_v16.json` · `foundry/dev/geometry_probe_a.py` (with its selftest, real rows included) ·
`foundry/foundry/results/lattice/geometry_probe_a_results.json`.

**Frozen bytes untouched.** No natural row was read, no column shipped, no charge consulted.
