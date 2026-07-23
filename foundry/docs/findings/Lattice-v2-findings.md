# Lattice v2 (G2, prereg_v30) — findings: the universe spans the strata; the selection confounds the coupling

**A banked verdict, at its own size, before v3's prereg exists** (owner ruling). v2 stands on two results that hold
regardless of what v3 finds: **Wall 3's "too-coarse universe" is refuted**, and **the stratum-spanning selection is
FPT-biased**, so v2 cannot measure the coupling. Both go on the record now.

## 1. The result that refutes Wall 3: the Boolean universe spans the strata

The purpose-built roster — one generated Boolean relation per KSTW approximation stratum × objective, selected by the
sealed mechanical rule (canonical-first, correlation-blind, committed before the parameterized charge) — reaches **6
distinct (approximation × parameterized) profiles across 8 both-real rows, with both parameterized values present.**
That clears the floor. **The single-relation Boolean *universe* is not too coarse to exhibit the gradient — it spans
the KSTW stratification.** Wall 3 as originally written in `generation-cannot-reach-the-gradient.md` ("the reachable
population is ~30 rows and too coarse") is **refuted, not merely downgraded**: v1's poverty was a property of the
census's Schaefer *representatives* (0-valid / 1-valid / width-2-affine / IHS-B → collapse to PO), not of the universe.

**Empty strata at arity ≤ 3 (reported, never back-filled):** `Min-Horn-Deletion-complete` is unreachable on *both*
objectives (no arity-≤3 relation lands there); `Nearest-Codeword-complete × Max-Ones` and
`decidable-not-approximable × Min-Ones` are also empty. These are facts about the arity-≤3 reachable universe, sealed as
scope limits, not gaps to fill by raising the arity after the count.

## 2. The result that keeps v2 from measuring the coupling: an FPT-biased selection

The secondary association is **Cramér's V = 0.0** — but this is **degenerate, not a coupling measurement.** The
parameterized marginal is **7 FPT : 1 W[1]**: the *canonical-first* (minimal-arity, lexicographically-first) relation in
each approximation stratum is *simple*, and simple relations are weakly separable (FPT). Only `NAND` (a negative
2-clause) breaks it. So the sealed selection rule — correctly correlation-blind and mechanical — is nonetheless
**FPT-biased**: it spans the approximation axis but flattens the parameterized one. V = 0.0 is a consequence of a
near-constant parameterized axis, not evidence about whether approximation-hardness and parameterization-hardness
co-vary. Combined with the sealed stratified-sampling caveat (association *given* uniform approximation coverage, not a
natural population), **v2 cannot answer "is the gradient present outside the canon."** It answers only "can the universe
span the strata" — yes.

| approximation | param FPT | param W[1] |
|---|---|---|
| PO | 2 | — |
| APX-complete | 2 | — |
| poly-APX-complete | 1 | 1 (`NAND`) |
| Nearest-Codeword-complete | 1 | — |
| decidable-not-approximable | 1 | — |

## 3. A serialization bug, caught the right way

The analysis first read `NAND → FPT`, which is *impossible* — `NAND` is the independent-set relation and must be W[1].
The compute-rather-than-trust check flagged it immediately. Cause: the roster's human-readable `relation` field was
written as `sorted(sorted(t) …)`, which sorts *within* each tuple, corrupting `(1,0) → (0,1)` and turning `NAND` into a
weakly-separable relation. The **authoritative arity + bitmask were always correct**, and the selection logic used the
in-memory relation, so the selected roster (and the hash-seal that it was fixed before the parameterized charge) is
intact; the fix reconstructs each relation from the authoritative bitmask. A serialization defect, caught before it
reached a verdict by a value that could not be true.

## 4. What v2 banks, and what it hands to v3

**Banked (holds regardless of v3):** the generated single-relation Boolean universe spans the KSTW strata (Wall 3's
universe-coarseness claim is refuted); and a stratum-spanning, correlation-blind selection is FPT-biased, so it cannot
measure the coupling. **Handed to v3:** the clean test is the *natural* population — the exhaustive arity-≤3 roster with
no selection at all (`prereg_v31`), whose association is the honest coupling over the reachable proxy universe. v2 proved
the universe is rich enough to test; v3 does the test.

## Discipline honored

Prereg (`prereg_v30`) sealed before selection; selection mechanical + correlation-blind + hash-sealed (roster committed
before the parameterized charge); occupancy primary; empty strata reported, not back-filled or arity-raised; the
stratified-sampling caveat carried from the prereg; the serialization bug found by a ground-truth value check and fixed
without disturbing the selection; `is_weakly_separable` and `oracles.py` untouched. Artifacts:
`results/lattice/lattice_v2_roster.json` (fixed before the parameterized charge) and `lattice_v2_occupancy.json`.
