# Sprint 6 "Pebble" — P2b: the point-to-set reach instrument

**Verdict: QUALIFIED** (redesign #1), by owner criterion ruling recorded below. The point-to-set instrument recovers
the reach dichotomy that `corr` inverted. P3 re-opens on the point-to-set observable.

## The result — the `corr` inversion, demonstrated

Point-to-set signal at r=2 (the pinned reach_score, prereg_v22), n=16 exact coset enumeration:

| pole | class | reach_score @ r=2 | bootstrap interval |
|---|---|---|---|
| 2-affine (equality) | affine (long) | 0.375 | (0.336, 0.414) |
| **3-XOR (parity)** | affine (long) | **0.352** | (0.313, 0.391) |
| 2-SAT @1.6 | bounded-width (short) | 0.211 | (0.184, 0.242) |
| 2-SAT @0.9 | bounded-width (short) | 0.183 | (0.165, 0.202) |

**Groups separate cleanly:** affine/parity HIGH (floor 0.313) vs bounded-width LOW (ceiling 0.242), non-overlapping.
**Parity moved from the `corr` floor (0.03) to the top group.** That inversion is the whole point of the rebuild,
and it is unambiguous. (`corr`, rescoped, correctly ordered *pairwise* correlation and put parity at 0.03 — a real
quantity, not the one reach means.)

## Criterion withdrawal — dated after the result, flagged (owner ruling, 2026-07-22)

**This is a post-result change to a sealed criterion, disclosed as such so a reader can judge it.** It post-dates
the v22 run (commit `de64f4f`, 2026-07-22 19:56).

prereg_v22 sealed the pass criterion as group separation **and** "PARITY AT THE TOP", and the verdict code read the
latter as *parity the single maximum*. Parity (0.352) is co-top with 2-affine (0.375) — within heavily overlapping
intervals — but not the strict max, so the code returned NOT_QUALIFIED.

**The owner ruling (in the owner's framing):** the strict-single-max clause was a **specification error**, not a
result to be reinterpreted. "Parity at the top" was sealed as shorthand for *the instrument inverts `corr`* — parity
must move from the floor to the high end, the whole point of the rebuild. What went unnoticed when writing it: **2-affine
is *also* affine — globally rigid, point-to-set-long, the same physical class as parity — and was already placed in
the design as the *consistency reference* precisely because it is co-long.** So the criterion as literally written
demanded that parity outrank its own class-mate, which no physical mechanism produces; a 0.02 gap inside overlapping
intervals is exactly the noise expected between two members of one class. The distinction matters: this is *not*
"the data nearly met the bar, call it met" — the bar tests the inversion (which it does) plus an artifact (strict
rank within a class) it should not have.

**Dated pre-result evidence for this reading:** prereg_v22 (committed `cc8bc14`, *before* the run) designated
2-affine the consistency reference with the expected reading "reads HIGH, near parity (consistency)." It did exactly
that. The withdrawal is therefore correcting the criterion to what it was sealed to test, not to what the data showed.

**Recorded:** QUALIFIED on group separation. The strict-single-max clause is **withdrawn as an owner specification
error**, reason above, dated after the result and flagged. No redesign budget is spent on a non-physical target.

## The honest criterion form (sealed for any future re-run — prereg_v23)

> Affine-class HIGH vs bounded-width LOW, non-overlapping bootstrap intervals between the groups; **same-class
> co-top permitted** (a co-long class-mate reading at or above parity does not fail the instrument).

## Methods lesson (carried from prereg_v21)

`test_parity_blind_but_2affine_visible` entered the suite on 2026-07-22 (commit `166eec4`) and encoded the pairwise
blindness — it survived P2 QUALIFICATION and the start of the P3 harness build before the disqualifying conclusion
was drawn (via the parallel I-SP investigation). It was filed as a pole-**selection** technicality, not a
**construct-validity** failure. "Which media do I calibrate against" and "does this observable measure the target
construct" look adjacent and are not. The flaw sat in our own tests before we read it correctly.

## Scientific finding (not a calibration note): point-to-set reach on Boolean may be DICHOTOMOUS

The four poles land in **two** groups with a clean gap and nothing between: affine-class **long** (0.35–0.38),
bounded-width **short** (0.18–0.21). This is what the **algebraic dichotomy** would predict — affine vs bounded-width
is the Schaefer split, and point-to-set reach appears to track it with **no meaningful middle level**. Two bounded-width
densities (0.9, 1.6) both sit LOW; the affine and parity families both sit HIGH.

**If this holds up in P3, it is a real result about the phenomenon's structure**, and it has a consequence for
phase 2: the sealed differential prediction (prereg_v12/v13, framed as a strong/moderate/weak/none **gradient**)
should expect **two levels rather than a gradient** on the point-to-set observable. Recorded here; the sealed table
is not rewritten — the dichotomy is the *expectation to test*, sealed before P3 re-opens.
