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
≥ 0.9997. Majority is the hardest flavour and the reason is visible in score 3: its violations are rarest,
mean nonzero rate 0.1207.

Specificity is **1.0 and forced**, reported as such and claimed as nothing.

## Score 3 — the distribution shape: the question answers one way, decisively

Pre-registered as a question with no predicted direction: is blendability **bimodal** — mass at zero and
mass near the maximum, matching the dichotomy's binary — or is there a populated **"almost-closed" middle**?

**It is not bimodal. The middle is where almost everything lives.**

| flavour | exactly zero | nonzero in the 0.05–0.50 band | mean nonzero rate | above 0.50 |
|---|---:|---:|---:|---:|
| majority | 320 | **85.4%** | 0.1207 | **0** |
| minority | 33 | **99.2%** | 0.3669 | 33 |
| min | 317 | **87.4%** | 0.2457 | 110 |
| max | 317 | **87.4%** | 0.2457 | 110 |

Between 85% and 99% of all nonzero violation rates fall in the middle band, and the upper region is nearly
empty — **not one** of the 4,028 admissible classes violates majority at a rate above 0.50. The typical
not-closed relation is not wildly unblendable; it is *slightly* unblendable. The dichotomy's binary is
carving a continuum near its bottom end.

That is a finding about the geometry the theorems binarise, and it cost nothing extra — which is what the
note predicted the freebie would be worth, without predicting which way it would fall.

**A consistency check that came free.** `min` and `max` have byte-identical distributions. That is forced:
the roster is closed under complementation, which exchanges horn and dual-horn, so the two flavours are in
bijection. The numbers agreeing exactly is evidence the computation is coherent, not a coincidence.

## Census before seal, on the probe's own quantity

The standing law applies to instruments too. All four flavours pass at **both** ends of starvation —
138–170 distinct values, modal share 9–13%, nothing over-concentrated and nothing over-dispersed.

## Verdict — QUALIFIED

The battery is exact and the sampled sensitivity is characterised per flavour per budget. The probe is
**licensed for natural-row ensembles with its accuracy characterised.**

**Natural-row deployment is explicitly not authorised by this run** and needs its own spec. What the licence
buys is the possibility: a measured closure-proxy needing only an instance generator would reach the 311
rows the closure admission bar excluded — the mechanism programme's entire missing population. This study
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
