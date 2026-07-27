# The ramp pilot protocol — what a declared family dial must survive before it is used

Minted 2026-07-27 from the MCSP pilot, which failed two of these and caught itself both times.

A family ramp declared at census is a **typing** — a falsifiable claim that the family's rows have a
structural dial of that kind. A typing used without test is an assumption that governs every row the
family will ever contribute. This protocol is what a first use must pass.

## The four checks

**1. The dial has a referent in the row.** Stated plainly, because this is where MCSP failed first: the
`string` family's declared ramp was "pattern/text length ratio" and MCSP has neither a pattern nor a text.
A ramp with no referent is not a hard dial or an expensive one — it is undefined, and the honest response
is a census erratum, not a silent substitution.

**2. Everything but the dial is held fixed.** The first MCSP pilot varied the planted block count per
instance while varying the alphabet. Block count drives the region size far harder than alphabet does, so
the measured trajectory was mostly noise about the wrong variable. *A ramp is not measured until
everything but the dial is held fixed.*

**3. The movement clears the catalog's own flat rule.** Excursion of the step means ≥ `FLAT_MULTIPLIER` ×
pooled within-step SD, using the same multiplier the extractor applies to every other trajectory. A pilot
that passed under a laxer standard than the descriptor layer would ship rows the catalog then calls FLAT.

**4. LEAVE-ONE-OUT: the movement survives dropping its most extreme step.** Recompute check 3 without the
step furthest from the mean. If the remainder is flat, the dial is a **threshold, not a ramp** — the
signal is one contrast and the rest of the range is silent.

## What each outcome types

| outcome | typing | captured as |
|---|---|---|
| passes 1–4 | `RAMPED` | full panels across the declared ramp |
| passes 1–3, fails 4 | **`CONTRAST-DIAL`** | two declared levels; contrast descriptors, no trajectory |
| fails 3 | `no-natural-dial-at-fixed-encoding` | point capture, or the row types out |
| fails 1 | census erratum first, then re-pilot | — |

`CONTRAST-DIAL` was minted because MCSP landed in a case the original ruling did not have: neither a
working graded dial nor an absent one. A row typed this way enters as a **declared two-level factor** —
full panels at each level — with trajectory descriptors reading `n.a.-contrast` and between-level deltas
in their place. Sweeps treat it as a factor and never as a trajectory, because a `slope_sign` computed on
two points is a direction with no shape under it.

## The direction is measured, never asserted

Which end of a ramp *hardens* is the sort of thing written down from memory and found backwards later. The
pilot reads it off the measurement, and — per check 4 — an endpoint comparison does not count as reading
it. *An endpoint comparison is an eyeball claim with arithmetic on it.*

## Scope

Required of every **new** family pilot from 2026-07-27. The five ramps already in use (`sat-csp`, `graph`,
`optimization`, `number-theoretic`, `algebraic`) were declared and used before check 4 existed. Applying
it to them retroactively is a **catalog v3 question**, and it goes through the rule-before-computation
channel: the rule is declared and sealed before it is run, so that the answer cannot pick the rule. It is
banked as Q20 and is **not** retrofitted here.

---

## Roster protocol — vet before hashing (added 2026-07-27)

A batch census declares its roster and hashes it before any generator is written. That ordering is what
makes the reservation blind, and it must not change. But batch 5 declared eight rows and then discovered
that three of them had no subset region at all — the objects were an ordering, a linear layout and a
partition. Declare-then-discover was the bug.

**Vet-then-declare is the fix**, and it sits beside conformance-at-birth as a standing check:

> Before a roster is hashed, every row's **region formulation** is checked against its own
> `canonical_encoding` in the atlas. A row whose encoding names an ordering, a partition or an assignment
> does not enter a subset roster, whatever its census class says.

The check costs one field read per row and is mechanical — `reach_subset_readjudication.py` does it for
the whole class. What it protects against is the expensive failure: a hashed roster that cannot be
honoured, whose exclusions then have to be explained one at a time.

**Note the order dependence.** Vetting happens *before* the hash, on the row's declared identity; it never
consults a reading, because no reading exists yet. The reservation stays outcome-blind.

### Amendment — what satisfies vet-before-hash (2026-07-27)

The rule as first written named `reach_subset_readjudication.py`, because at writing time that was the
only pass which read region formulations with receipts. Naming an implementation made the rule look like
a ceremony, and by batch 9 the audit-verified queue was exhausted while a *different* pass had read 59
rows to a stricter standard. Asking whether that qualified, rather than assuming it, is the rule working.

**The rule protects a question, not a procedure:**

> *Has a human read this row's `canonical_encoding` and verified its certificate shape, with the
> encoding quoted, before a roster commits to filming it?*

**Vet-before-hash is satisfied by any pass that reads the row's canonical encoding and assigns its region
formulation with the quoted receipt.** Currently the region-formulation audit and the 59-row unmatched
adjudication both qualify — the adjudication under a stricter standard than the audit, since it carried a
verdict per row, refused to complete if any row lacked one, and used the finer vocabulary.

**Lexicon-matching alone never qualifies.** `lex-first-maximal-independent-set` matched `L4-subset` on a
real phrase in a real encoding and is not a subset region. Matched is not verified, and no future pass
inherits qualification by resembling one that has it.

Keeping the rule about the *thing* rather than the *ceremony* is also what keeps the list maintainable:
a new pass qualifies by meeting the standard, not by being added to an enumeration someone must remember
to update.
