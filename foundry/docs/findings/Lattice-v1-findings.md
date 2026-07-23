# Lattice v1 (G2, prereg_v29) — findings: the pipeline works; the roster was too coarse

**A banked verdict, recorded at its own size before v2 exists** (owner ruling: the pre-registered floor fired on the
pre-registered roster; that verdict is sealed on its own terms first). The headline is the good news, and the verdict
is INSUFFICIENT RESOLUTION — but on a claim narrower and more honest than "the reachable universe is too coarse."

## 1. The headline: the witness gate passes — the generate-and-charge pipeline works

The instrument reproduces the calibration pair on **opposite corners of both axes**, CI-locked
(`objective_oracles.selftest_objective_oracles`, `test_lattice.py`):

- **Vertex Cover** = Min-Ones(`OR₂`) → **(approximation: APX-complete, parameterized: FPT)**
- **Independent Set** = Max-Ones(`NAND`) → **(approximation: poly-APX-complete, parameterized: W[1])**

Approximation from the KSTW Max-Ones/Min-Ones priority lists (Thm 2.12/2.14); parameterization from Marx's general
weak-separability (Def 2.1), which — unlike the census's 0-valid-normalized check — is faithful on the 0-invalid
single relations the witness needs (L1 §9). **The pipeline can produce the phenomenon it was built to measure.** Only
the roster was wrong.

## 2. The occupancy grid (the primary object) — 5 profiles, below the floor

Over the **sealed roster** (the 11 distinct single relations in the Boolean co-clone plain bases + finer tier, each ×
{Min-Ones, Max-Ones}): **22 rows, 18 both-real, 5 distinct (approximation × parameterized) profiles.**

| | param **FPT** | param **W[1]** |
|---|---|---|
| **PO** | 10 | 2 |
| **APX-complete** | 3 (incl. VC) | — |
| **poly-APX-complete** | — | 2 (incl. IS) |
| **Nearest-Codeword-complete** | 1 (`x⊕y⊕z=1`, Min-Ones) | — |

Plus `NAE-3`, `1-in-3` → **feasibility-hard** (param `open`; occupancy corner, not both-real). **Two of the seven KSTW
approximation strata carry no row at all** — `Min-Horn-Deletion-complete` and `decidable-not-approximable` are empty;
and among the occupied strata, the cells `(APX-complete, W[1])` and `(poly-APX-complete, FPT)` are empty.

**Verdict, declared on composition (before the association is read): INSUFFICIENT RESOLUTION.** 5 distinct profiles < the
pre-registered floor of 6 (`prereg_v29`). The floor was set before the count; the count came in at 5; the verdict fires
as sealed — not argued after.

## 3. The verdict, worded exactly: the *representatives* are too coarse, not the *universe*

The honest claim is the narrow one. The census's CKZ plain-basis relations were chosen as faithful **Schaefer** witnesses,
and they are overwhelmingly **0-valid / 1-valid / width-2-affine / IHS-B** — precisely the properties that send Max-Ones
and Min-Ones to **PO** and the easy strata. So the roster collapses onto four cells plus one Nearest-Codeword row. This
is a fact about **which relations the census happened to name**, not about the reachable universe: the empty strata *are*
inhabited by Boolean single relations the census did not use (e.g. `x⊕y⊕z=1`, a non-0-valid affine relation, lands in
Nearest-Codeword-complete — and it is the *only* reason the count is 5 rather than 4). **The single-relation Boolean
universe spans the KSTW stratification; the census's representatives do not.** Whether that universe is rich enough to
exhibit the gradient is a question this roster could not answer and v2 will.

**This corrects L1 §4 downward, as L1 anticipated.** L1's expected-occupancy table reasoned at the **class** level
("dual-Horn → Min-Horn-Deletion-complete", "affine → Nearest-Codeword-complete") and projected up to seven approximation
values. But the *per-representative* placement — which L1 flagged the L5 build would "confirm or correct" — is sparser:
`OR₃` (the dual-Horn representative) is IHS-B, so it hits Min-Ones **APX-complete** (line 2), never reaching
Min-Horn-Deletion (line 4); `XOR₃` (the affine representative) is 0-valid, so it hits Min-Ones **PO** (line 1), never
reaching Nearest-Codeword (line 3). The class-level reasoning over-counted; the oracle corrected it downward.

## 4. The secondary association (resolution-limited, not led with)

For completeness (ruling 4 keeps this secondary): the both-real Cramér's V — the canon's statistic
(`structure.cramers_v`) — is **0.553** on the 18 rows. **It is not interpretable as a gradient measurement**: 10 of 18
rows sit in a single cell `(PO, FPT)`, two approximation strata are empty, and two joint cells are empty, so the number
is an artifact of a degenerate table, not a coupling on a populated space. It is **not** magnitude-comparable to the
canon's 0.73 (different, and here degenerate, support). Recorded, not interpreted.

## 5. What v1 does not claim, and what v2 is

v1 does **not** claim the approx⟷param gradient is absent outside the canon, nor that a generated Boolean roster cannot
test it. It claims only that **this specific roster — the census's Schaefer representatives — is too coarse to try.**
The pipeline is proven; the missing ingredient is a roster that exercises the strata. **v2 (prereg_v30) is a separate
experiment**: a purpose-built, stratum-spanning single-relation roster, selected by a mechanical, correlation-blind,
hash-sealed rule (one generated Boolean relation per KSTW×Marx cell, committed *before* the parameterized charge or the
joint is computed on it), which can populate ~10–12 profiles and give the gradient its actual test. v2 carries its own
prereg, selection rule, kill, and — because a stratum-spanning roster is *stratified sampling on the approximation
axis* — its own caveat that the resulting statistic measures association *given deliberately uniform approximation
coverage*, not comparable in magnitude to the canon's naturally-occurring 0.73.

## Discipline honored

Prereg (`prereg_v29`) sealed before any roster-wide number; witness gate before the occupancy read; occupancy primary,
association secondary and resolution-caveated; the floor set before the count and the verdict declared on composition;
the parameterized oracle's ground-truth rule armed and reported (L1 §9, did not fire); `is_weakly_separable` and
`oracles.py` untouched (census/eightfold byte-identical); the verdict recorded at its own size before v2 is designed.
Artifact: `results/lattice/lattice_v1_occupancy.json`.
