# Sprint 3.5 — Census Enrichment memo (floor lock + domain-3 oracle investigation)

**Path-B reorder.** Corrected Sprint 3 showed both founding questions are *resolution-blocked* (7 both-real
rows, 6 identical; too theorem-coupled). This sprint attacks scale + richness before pointing Sprint 4's
instruments at anything. This memo does two owner-review things **before** any census numbers or oracle exist:
(1) locks the H_P2_scaled go/no-go floor; (2) reports the domain-3 counting/approximation/parameterized
dichotomy investigation as IMPLEMENT / DEFER / ABSENT.

---

## 1. Pre-registered floor for H_P2_scaled (LOCKED before Session 1's numbers)

`H_P2_scaled` (sealed in `prereg_v3`) is the real P2: as the Boolean tier refines, does approx|parameterized go
**positive / reversed / stratified**? It must not run on an underpowered table. **Go/no-go floor, fixed here
before Session 1 builds anything:**

> **H_P2_scaled RUNS only if the enriched census has ≥ 15 both-real (approximation, parameterized) rows spanning
> ≥ 4 distinct (approximation, parameterized) profile pairs.** Below either threshold → the same disposition
> Sprint 3 already carries, INSUFFICIENT RESOLUTION, and H_P2_scaled waits for more rows.

Rationale: the Sprint-3 failure was 7 rows / 2 distinct pairs. Requiring ≥15 rows and ≥4 distinct pairs makes a
permutation/association test non-trivial (a 2-pair table can only ever be the affine anecdote). The corrected,
selftest-locked permutation harness (`analysis._perm_p_on_table`, reproduces 1/7 and 1/3) is the test; R25-netting
of the entailment-forced component is required before any "surprising" reading.

## 2. Domain-3 oracle investigation — verdicts (R20: primary statements only, no reconstruction)

Question per charge: is a general-domain analogue of the Boolean dichotomy (a) **proven**, (b) stated in
**checkable** form, (c) **implementable** at |D|=3 within a 3 h sub-box? Verdict ∈ {IMPLEMENT, DEFER, ABSENT}.

| Charge | Proven? | Checkable / implementable at \|D\|=3? | **Verdict** |
|---|---|---|---|
| **counting** (#CSP) | **Yes** — Bulatov 2008 (congruence singularity); Dyer–Richerby 2010 (**Strong Balance**), criterion **decidable, in NP** | The condition is a **congruence-lattice + relation-balance** test, not a polymorphism-closure check. Decidable at \|D\|=3 but implementing Strong Balance / congruence singularity *faithfully* is a research-grade lift far beyond a 3 h box, and I cannot state it in implementable form from a verified primary source. | **DEFER** — cell stays `open`; a correct implementation needs Dyer–Richerby's Strong-Balance definition read + verified, out of this budget. |
| **approximation** (Max-CSP) | **Partial** — the **exact-solvability (PO) boundary** is unconditional (Thapper–Živný 2016 VCSP dichotomy: PO iff a symmetric fractional polymorphism / BLP-solvable, else NP-hard). The **finer** classes (APX-complete vs inapprox) are **UGC-conditional** (Raghavendra 2008, optimal ratio under UGC — and a *continuous* ratio, not a discrete class). | A discrete unconditional general-domain dichotomy into {PO, PTAS, APX, APX-complete, inapprox} **does not exist**. Only PO/not-PO is unconditional+checkable (fractional polymorphisms) — still a real lift. | **DEFER** — cell stays `open`. Sub-note: a PO-only sub-verdict (Thapper–Živný) is an IMPLEMENT *candidate* for a later sprint; the finer inapprox classification is **ABSENT** unconditionally (a genuine gap to log in the writeup). |
| **parameterized** (Exact-Ones / solution size) | **Yes** — Bulatov–Marx 2014 give the FPT/W[1] dichotomy **beyond Boolean domains** (general finite domain). | The general-domain tractability condition is more involved than the Boolean union+difference, and I could **not extract it** from the primary source (the arXiv/journal PDF did not render; only the *Boolean* weak-separability definition is verified). Implementing an unverified condition is exactly what R20 forbids. | **DEFER** — cell stays `open`; moving to IMPLEMENT requires reading Bulatov–Marx's general-domain FPT characterization and confirming \|D\|=3 checkability. |

**Consequence (the real result of this investigation):** the domain-3 tier's honest **2-charge scope
(decision + localization) is correct and stays**, not from laziness but because the other three general-domain
dichotomies are either UGC-conditional (approximation) or have conditions not faithfully implementable in budget
(counting: congruence singularity; parameterized: general-domain weak separability). **Therefore the finer
Boolean tier (Session 1) is the enrichment path** — which is exactly why Path B reorders to it. **No domain-3
oracle is implemented in this sprint** (all DEFER); the verdicts above are the owner-review items.

## 3. Scoped for a later sprint (not run here)

- **P3 R25-netting:** before "does the invented world agree on dimensionality" is fair, remove the
  theorem-forced (entailment) component of the census's factor structure; re-estimate k\* on the residual.
- **approximation PO-boundary (Thapper–Živný):** the one IMPLEMENT candidate surfaced — a PO/not-PO sub-charge
  over domain-3 via fractional polymorphisms / BLP, if the owner wants it built.

## Citations

Bulatov, *The complexity of the counting CSP*, JACM 60(5) (2013) / ICALP 2008 · Dyer & Richerby, *An effective
dichotomy for the counting CSP*, SICOMP 42(3) (2013) — Strong Balance, decidable in NP · Raghavendra, *Optimal
algorithms and inapproximability results for every CSP?*, STOC 2008 · Thapper & Živný, *The complexity of
finite-valued CSPs*, JACM 63(4) (2016) · Bulatov & Marx, *Constraint satisfaction parameterized by solution
size*, SICOMP 43(2) (2014) (arXiv:1206.4854).
