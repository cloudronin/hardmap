# The zero-hunt — adjudicating the survey's unforced exact-zeros

**Status: INSTRUMENT HYGIENE.** No prereg, no scored prediction, no verdict on the survey's substance.
**Date:** 2026-07-26 · **Artifact:** `sounding_zero_hunt.json` · **Input:** the re-stamped v2 column + v3.

---

## What was adjudicated

**43 exact-zero readings**, in **21 (row, region, flavour) units**, that the derived forcedness join does
*not* flag theorem-forced. Every one gets an entry, expression-first: the producing code path and the
region's construction are quoted **before** any verdict is stated.

| verdict | readings |
|---|---:|
| **HIDDEN-CLOSURE** | 29 |
| **THIN-SATURATION** | 12 |
| **GENUINE-READING** | 2 |
| ENCODING-ARTIFACT | 0 |

**Unadjudicated units: 0.**

## Why "unforced" was never "unexplained"

Q8 predicted the shape of this before it ran, and was right. On Marrow-excluded rows there is **no pinned
template**, so `forced = null` means *underivable*, not unexplained. Closure there has to be argued from
the region's construction directly, and **each argument is the artifact** — no join will ever supply these
flags mechanically.

That class dominates, as expected. And the arguments turn out to be **three structural ones**, not
twenty-one incidental ones:

- **(A) Pairwise-exclusion families are majority-closed.** Matchings, independent sets, 3D matchings. For
  the majority of three members to contain a conflicting pair, each element must lie in ≥2 of the 3 sets —
  so by pigeonhole some single member contains both, contradicting its own membership. *This is the
  2-clause/bijunctive argument arriving on rows Marrow could not pin,* because their scopes are
  unbounded-arity.
- **(B) Upward-closed families are max-closed.** Set covers, hitting sets, feedback vertex sets, odd-cycle
  transversals. Adding elements never destroys membership, so the union of two members is a member.
- **(C) Downward-closed families are min-closed.** Knapsack feasibility. Dropping items only decreases
  weight, so the intersection of two feasible packings is feasible.

`max-flow` is a fourth, narrower case: conservation is a **parity** condition on internal-node degree and
minority is coordinatewise XOR, so the blend preserves it. The affine argument, again reaching a row with
no pinned template.

**Encodings matter and are quoted for that reason.** In `fvs` and `oct_`, `s[v] = 1` means v is *removed* —
the closure is on the deleted set, not the retained one. Reading the flag without reading the encoding
would invert the argument.

## The closure claims were tested, not asserted

Each verdict rests on a structural premise that is checkable, so it was checked: premises verified
exhaustively on freshly built regions, implied closure verified by brute force over m-subsets. **A claim
that failed its own test was reversed by the test, not defended.**

One did. `independent-set · optimal · majority` was argued HIDDEN-CLOSURE with an explicit caveat that the
majority of three *maximum* independent sets is independent but need not be *maximum*. The brute-force
test found exactly that failure. **The verdict reversed to GENUINE-READING.** The prior argument is kept
in the artifact rather than deleted, since the reversal is the useful part.

Two defects in the test itself were caught before it was believed, and both are worth recording because
each would have produced a *confident wrong answer*:

1. **The test initially tested nothing.** All ten closure claims returned `NOT TESTED` — wrong builder
   signatures — and the run still printed a clean adjudication table. That is the silent gate again, one
   level down: an absent check reads as a passed one. Fixed by making an untested claim a **hard failure**
   of the script, so the artifact cannot be written while asserting a check that did not run.
2. **Truncation manufactured two false falsifications.** Regions were capped at 600 members before testing
   union-closure — but a truncated set is not the set, since the union of two members can be an element the
   truncation removed. `feedback-vertex-set` and `odd-cycle-transversal` "failed". The tell was that every
   failing region was *exactly* 600. With the full region as the membership set and only the enumerated
   subsets capped (and sampled at random rather than taken as a lexicographic prefix, since the front of
   `product((0,1),…)` is all leading zeros), both pass.

## THIN-SATURATION is adjudicated against a *pre-declared* floor

The v3 spec declared `INSUFFICIENT-r` (r < 10) **before any of these readings existed**. That floor
governs here, and it governs *first* — ahead of any closure argument. Inventing a thinness threshold at
adjudication time would be discovering the rule at scoring time, which is the exact move this program is
built against.

A first pass did invent one, and it changed answers: `nae-sat`, `sat-3` and two `independent-set` readings
were briefly promoted to GENUINE-READING by a floor written after seeing them. Under the pre-declared
floor they are THIN-SATURATION — below r=10 the control SD is unstable (0.1006 at r=7 against 0.0054 at
r=212), so the zero is not distinguishable from chance **in either direction**. It is not evidence of
closure and not evidence against it.

A secondary distinct-subset floor of 10 applies only *above* the pre-declared one.

## The residue — 2 readings

| row | region | flavour | r | subsets | why it survives |
|---|---|---|---:|---:|---|
| `sat-2` | solutions | min | 22 | 354 | 2-SAT is bijunctive, so *majority* is forced and the join flags it. **min is not**: a general 2-CNF is not Horn. 231 distinct pairs available. Either the sampled formula drew Horn-like, or min on 2-CNF solution sets at this size is unaccounted for. |
| `independent-set` | optimal | majority | 10 | 282 | closure argued, then **falsified by brute force**. The feasible family is majority-closed; the optimal region is not, and the test found the counterexample. Why the measurement still read 0.0 at this r is open. |

These stay as measurements and stay in the bank.

## The Q1 consequence, per entry

Recorded on every adjudication and re-stamped into both survey artifacts:

- **HIDDEN-CLOSURE (29)** → **leaves** the future scored set as calibration. The closure is real, so a
  discovery statistic must not count it. Flagged `closure_explained: true` so exclusion happens **by
  schema** rather than by anyone remembering to.
- **THIN-SATURATION (12)** → **leaves** as uninformative; migrates to `INSUFFICIENT-r`.
- **GENUINE-READING (2)** → **stays** as a measurement.

## The re-stamp

43 readings stamped across both files (4 in v2, 39 in v3). Metadata only — and that is **proven, not
promised**: every measured field is fingerprinted before and after the edit and compared, and the script
refuses to write on any change. The program has been bitten by "metadata-only" edits that weren't, so the
claim gets a test rather than a sentence.

## What this does not say

Nothing here scores anything. That 29 of 43 unforced zeros turn out to be closure the template route
cannot see is a statement about **the derivation's reach**, not about geometry, hardness, or the survey's
substance. Whether the reach can be extended — whether (A), (B) and (C) should become derived flags rather
than adjudicated ones — is a design question, and it is banked, not answered.
