# Sprint 3.5 results — finer Boolean tier clears the floor; H_P2_scaled → STRATIFIED

**The floor is met and the real P2 ran.** The finer Boolean tier (0-/1-valid co-clones + intersections) grew the
census to 15 both-real approximation|parameterized rows spanning 4 distinct pairs — clearing the pre-registered
`H_P2_scaled` floor — and the corrected, selftest-locked permutation test returns **STRATIFIED**: the
approx|parameterized relationship is not a monotone hardness gradient (positive or reversed) but is stratified by
the underlying algebra, and it is entirely theorem-forced.

> **H_P2_scaled → STRATIFIED.** V = 0.526, corrected permutation p = 0.049, rank-corr = 0.152. Param-hardness by
> approximation level is **non-monotone**: PO → 0.5, APX-complete → **1.0**, inapprox → 0.0. `parameterized`
> tracks affine-ness (affine → FPT); `approximation` tracks 0/1-validity (→ PO) and non-0-valid affine (→
> inapprox). Both are functions of the co-clone's polymorphisms, so the association is R25 theorem-forced — the
> stratification **is** the algebra, not an emergent gradient.

**Provenance.** `H_P2_scaled` sealed in [`prereg_v3`](../../foundry/results/prereg/prereg_v3.json); floor locked
in the [Sprint 3.5 memo](Sprint3.5-enrichment-memo.md) (commit `3180e1e`) **before** this tier was built.
Census: [`census.jsonl`](../../foundry/results/census/census.jsonl) (21 rows). Estimator: the corrected
`analysis._perm_p_on_table` (selftest reproduces 1/7, 1/3) + `eightfold.factors`, under `FOUNDRY_SPEC`.

---

## Session 1 — the finer Boolean tier (`finer.py`)

`classify_boolean` computes **every** charge for a Boolean language from its polymorphisms + the verified
theorems (no hand-assignment): Schaefer (decision), KSTW+Håstad (approximation — **0/1-valid → PO**, non-0-valid
affine → inapprox, else APX-complete), Creignou–Hermann (counting), Marx (parameterized — FPT iff affine or
0-valid-and-weakly-separable, **computed faithfully on 0-valid relations**), Barto–Kozik (localization). ABISV
parallelization is left `open` for the finer/mixed co-clones (not cleanly verified there — honest).

**Census: 7 N1 + 8 finer + 6 domain-3 = 21 rows, 10 distinct profiles** (up from 7), validates clean, **P1
holds**. The 8 finer co-clones are the 0-/1-valid intersections with each Schaefer class + the two constant
co-clones {x=0},{x=1}; they add the crucial **(PO, FPT)** and **(PO, W[1])** both-real pairs.

| Floor (prereg_v3) | Required | Achieved | |
|---|---|---|---|
| both-real approx\|param rows | ≥ 15 | **15** | ✅ |
| distinct (approx, param) pairs | ≥ 4 | **4** | ✅ |

The both-real contingency (the table H_P2_scaled runs on):

| | FPT | W[1] |
|---|---|---|
| **PO** (0/1-valid) | 4 | 4 |
| **APX-complete** (Horn/dual-Horn/bijunctive/NP-hard) | 0 | 6 |
| **inapprox** (non-0-valid affine) | 1 | 0 |

## Honest caveats — the floor is met literally, but read the composition

1. **Marginal significance.** p = 0.049 is right at the 0.05 line; with the two trivial constant co-clones
   removed it would not clear it. The robust part is the **verdict (STRATIFIED)** — the non-monotone pattern
   (PO 0.5, APX-c 1.0, inapprox 0.0) does not depend on the exact p.
2. **15 rows, but 10 distinct profiles.** The Boolean co-clone lattice caps the distinct (approx, param) pairs at
   4 — richer approx|param structure is **not reachable with Boolean co-clones**; it needs the domain-3
   counting/approximation oracles, which the Sprint-3.5 memo verdicted **DEFER** (UGC-conditional / not
   implementable in budget). So the ≥15-rows floor is cleared partly by faithful-but-degenerate co-clones.
3. **The association is theorem-forced (R25).** Both charges are polymorphism functions, so STRATIFIED is the
   algebra showing through — not an emergent, empirical gradient like the canon's. The R25-netted residual is ~0.

## What this says about the canon-vs-computation question

The canon's approx|parameterized **positive** gradient (empirical, S1/S2/S3/S5-survived at p=0.0001) does **not**
reappear as a monotone gradient in the theorem-generated census. Instead the census shows **algebra
stratification** — the same message as P3 (still k\*=3, DIVERGENT, theorem-coupled, at n=21): the two atlases
encode different objects. The generated world's structure is its dichotomies; it does not reproduce the human
canon's empirical shape. **To make P2/P3 a fair test of *hardness* rather than of *the theorems*, the next step
is R25-netting the census's factor/association structure** (scoped in the memo) and, if the owner wants, the
Thapper–Živný PO-boundary domain-3 sub-charge (the one IMPLEMENT candidate).
