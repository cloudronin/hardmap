# N3 — the sat-2 zero, scored

**Status: SCORED ONCE. `prereg_v21`, sealed 2026-07-26 before this ran.**
**Artifact:** `n3_sat2_zero.json` (sha256 `29cc654d`) · **Closes:** Q10, one of the zero-hunt's two GENUINE readings

---

## Verdict: PREVALENCE

| | |
|---|---:|
| P(formula is Horn), **computed before any data** | **0.00423** (0.42 %) |
| observed Horn rate | **0.0085** (2 / 236) |
| observed **min-closed** rate | **0.5169** (122 / 236) |
| min-closed **and NOT Horn** | **120 of 122** |

The prior called it: a chance-Horn draw is rare, and it was — 2 formulas in 236, right at the computed
0.42 %. **Min-closure is 60× more common than Horn-ness**, and essentially none of it comes from the Horn
route.

**CHANCE-COMPOSITION is refuted.** The original zero was not a lucky Horn draw.

## But the size table is the actual finding

The design conditioned min-closure on region size, because a small solution set can be closed by accident
and Horn ⟹ min-closed does not run backwards. That conditioning is what turned a verdict into an
explanation:

| region size | n | min-closed | rate |
|---|---:|---:|---:|
| **r < 25** | 169 | 109 | **64.5 %** |
| 25 ≤ r < 100 | 66 | 13 | 19.7 % |
| r ≥ 100 | 1 | 0 | 0 % |

**The original reading sits at r = 22, squarely in the bucket where 64.5 % of random 2-CNF solution sets
are min-closed.**

So PREVALENCE is the right verdict and it is **size-driven, not structural**. Min-closure is not a hidden
property of 2-CNF; it is what happens when a solution set is small enough that the intersection of two
members is very likely to already be a member. At r ≥ 100 it vanishes.

## What this retires, and what it does not

**Retired:** the sat-2 zero as a mystery. It reads 0.0 because at r = 22 that is the *ordinary* outcome,
not a rare one. The zero-hunt was right to call it GENUINE (no closure argument covered it, and thinness
by the pre-declared floor did not explain it) — and the explanation turns out to be a **third thing**
neither branch of the zero-hunt's vocabulary named: *common by size, without being thin by the floor's
definition*.

That gap is worth stating plainly. `THIN-SATURATION` tests whether too few subsets exist for a nonzero
rate to be **observable**. This is different: 231 distinct pairs were available and a nonzero rate was
perfectly observable — it just did not occur, because small solution sets are usually min-closed. **A
reading can clear every thinness floor and still be unremarkable.**

**Not retired:** the other GENUINE zero. `independent-set · optimal · majority` at r = 10 stands, with its
closure claim falsified by brute force and nothing else covering it.

## Method note

300 draws at the sealed ratio 1.6, n = 12, seeds derived from a declared base; 236 usable (64 produced
fewer than 2 solutions). Min-closure checked **exhaustively** over all distinct pairs — r is small enough
that no sampling cap was needed, which removes a source of doubt rather than bounding it.

The generator was certified by the conformance sweep before this ran: `sat-2` conforms to its bijunctive
template at 6/6 semantic and 6/6 syntactic.
