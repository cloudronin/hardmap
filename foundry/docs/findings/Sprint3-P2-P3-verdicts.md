# Sprint 3 — the census verdicts (P2, P3), corrected

**P2 → INSUFFICIENT RESOLUTION. P3 → DIVERGENT (directional at n=13).** At v1 census scale (13 rows) neither
question is powered; both are reported at their true size, and the one genuinely new object is stated as a
one-row observation plus a single pre-registered hypothesis for the scaled census.

> **Correction (this supersedes the first-pass Sprint-3 writeup).** The first pass reported a P2 permutation
> p=0.0002 and read it as a "roster sociology" ruling. **Both were wrong.** (1) The p-value was a **bug**: the
> harness permuted `parameterized` among *all* non-`n.a.` cells — which injected the 6 domain-3 `open` values —
> instead of permuting among the 7 both-real rows. On the correct table (6 identical rows + 1 distinct) the
> permutation p is **1/7 ≈ 0.143 by counting**, non-significant; a selftest now reproduces 1/7 and 1/3 exactly
> (`foundry.analysis.selftest_p2_perm`). Fixing a broken statistic is the byte-identical ethic applied to
> statistics, not arguing a verdict back. (2) The **"roster sociology" sentence is struck** — it contradicts a
> banked verdict: Crucible **S5** retired that explanation on the actual canon (roster deliberately exhausted
> with every known violator; the gradient survived at p=0.0001). A 7-row theorem-world anecdote cannot reinstate
> it.

**Provenance.** Pre-registered in [`prereg_v2.json`](../../foundry/results/prereg/prereg_v2.json) (P3) and
[`prereg_v3.json`](../../foundry/results/prereg/prereg_v3.json) (the scaled-census P2 hypothesis). Census:
[`census.jsonl`](../../foundry/results/census/census.jsonl) (13 rows). Output:
[`census_analysis.json`](../../foundry/results/census/census_analysis.json) (sha `7a468a7f…`). Estimator: the
identical `eightfold.factors` + corrected permutation test under `FOUNDRY_SPEC` — no eightfold modification.

---

## The census (Sprint 2.2 — the N3 general-domain tier) — stands unchanged

13 rows = **7 Boolean co-clone** (N1) + **6 general-domain |D|=3** (N3), **7 distinct profiles**, validates clean,
**P1 still passes**, **K1 did not fire**. The domain-3 tier is a curated set of textbook-certain languages, each
re-verified by the polymorphism machinery, filling only the **verified general-domain** charges — **decision**
(Bulatov 2017 / Zhuk 2020: P iff a WNU polymorphism exists) and **localization** (Barto–Kozik 2014, general;
affine is Maltsev-tractable but unbounded). counting/approximation/parameterized stay `open` for domain-3 (the
Boolean dichotomies do not transfer — honest). R20 caught a mislabelled "betweenness" mid-build (majority-closed
over the fixed 3-element domain → tractable) and refused the NP-complete label.

## 3.1 — between-generation noise floor — stands unchanged

Both tiers are deterministic → **generations-exempt**; the sampled polymorphism-profile explorer drifts ≤ **0.083**
across G=3. The census rows are deterministic, so the verdicts below are exact.

## 3.2 — P2: INSUFFICIENT RESOLUTION

The both-real approximation|parameterized table is **only the 7 Boolean rows** (domain-3 leaves both `open`), and
**six of them are identical**:

| rows | approximation | parameterized |
|---|---|---|
| horn / dual-horn / 2-sat / 3-sat / nae / 1-in-3 ×6 | APX-complete | W[1] |
| xor-sat (affine) ×1 | inapprox | FPT |

A 7-row table with six identical rows **cannot test the gradient.** V=1.0 is real but empty: the permutation p is
**1/7 ≈ 0.143** (V=1.0 exactly when the lone FPT lands on the lone inapprox row) — the corrected harness returns
0.149, non-significant. **Disposition: INSUFFICIENT RESOLUTION**, the same disposition the Boolean tier already
carries on this question. One distinctive row is an anecdote wearing a V of 1.0.

**The one genuinely new object, at its honest one-row size:** in the theorem-generated world the affine/XOR
**decoupling** — `(inapprox, FPT)`, hard-to-approximate yet FPT — is *not an outlier*; on this census it **is the
entire approx|parameterized axis.** That connects directly to **I6**: affine is the sole bounded-width obstruction
(Barto–Kozik) — the one language easy to solve, resistant to local consistency, FPT (Maltsev) yet inapproximable
(Håstad). It is a **descriptive observation**, not a ruling, and it earns **exactly one pre-registered
hypothesis** for the scaled census ([`prereg_v3.json`](../../foundry/results/prereg/prereg_v3.json), `H_P2_scaled`):
as the Boolean tier refines to many distinct rows, does the approx|param association go **(a) positive**
(canon-like), **(b) stay reversed** (affine-dominated), or **(c) split by stratum**? **That, at scale, is the real
P2.**

The canon's positive gradient is **not** touched by this: it survived Crucible S1/S2/S3 and the **S5** adversarial
roster at p=0.0001. Nothing here reinstates "roster sociology."

## 3.3 — P3: DIVERGENT (directional at n=13), with the caveat promoted to the finding

The identical LCM held-out-prediction estimator on the 13-row census reads **k\*=3** (interval [3,4,5]; curve
0.67→0.62→0.75), against the canon's **k\*=1**. Per prereg_v2 P3a (SAME-WORLD iff census k\*≤1), the census is
**DIVERGENT** — but two caveats *are* the finding, not footnotes to it:

1. **Power.** n=13 with ~1–2 masked cells per fold. **k\*=3 is directional at best, not a precise count.**
2. **The comparison was structurally loaded.** The census's charges are **derived from one another by the
   classification theorems** (counting=FP iff affine, localization tracks the polymorphisms, decision splits on
   the same algebra); the canon's charges are **independent literature facts**. So the operationalized comparison
   contrasts a **theorem-coupled construction** against an **empirical population** — divergence was structurally
   likely *regardless of what hardness is*. k\*=3 is the census re-expressing its own entailment layer, not
   emergent structure.

So P3 is DIVERGENT, but the honest reading is not "the census is richer" — it is "the two atlases encode
different objects, and the comparison as posed could hardly have come out otherwise." **P3 becomes meaningful only
after the v1.1 path: R25-net the census's factor structure (remove the theorem-forced component) and refine the
Boolean tier to escape profile poverty.**

## What stands, what was struck

**Stands:** the census build + provenance, P1 passing, K1 not firing, the domain-3 tier's honest 2-charge scope,
the generations-exemption logic, and P3's DIVERGENT verdict (with caveats promoted). **Struck:** the P2 p=0.0002
(bug → 1/7) and the "canon's-world / roster sociology" ruling (contradicts S5). **No banked verdict is argued
back;** the correction removes an unsupported claim and a broken number.

## Forward

- **The real P2 is `H_P2_scaled` at scale** (prereg_v3): positive / reversed / stratified, on a refined Boolean
  tier with the corrected, selftest-locked permutation test + R25-netting.
- **The real P3 needs R25-netting + more distinct profiles** before "does the invented world agree" is a fair
  question. The v1 answer is: at this scale, structurally divergent, not yet informative about hardness.
