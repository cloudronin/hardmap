# Sprint 3 — the canon-vs-computation verdicts (P2, P3) on the synthetic census

**Two verdicts, both DIVERGENT from the human canon — and both honest at v1's tiny scale (n=13).**

> **P2 (gradient):** the census carries a *strong, significant* approximation⟷parameterized coupling (V=1.0,
> permutation p=0.0002, beats its S1 null) — **but with the direction REVERSED.** The affine/XOR row is
> `(inapprox, FPT)` = hard-to-approximate yet *easy* to parameterize; the canon's gradient is
> harder-approx→harder-param. The generated Boolean world's dominant approx/param signal is the **deceptive-terrain
> decoupling**, not the canon's positive gradient. → **RESIZE** (the pre-registered canon's-world outcome).
>
> **P3 (dimensionality):** the census reads **k\*=3** under the identical Factors estimator, **not** the canon's
> **k\*=1** → **DIVERGENT** (prereg_v2 P3a). The generated world is *more* structured — but that structure is
> **theorem-forced** (the classification dichotomies couple the charges by construction), whereas the canon's
> charges are empirically near-independent. The census re-expresses its own dichotomies; it does not reproduce
> the canon's shape.

**The canon-vs-computation answer, stated plainly:** the human-curated atlas and the theorem-generated census
**disagree on both structure and dimensionality**, for an illuminating reason — they source their charge values
differently. The canon's charges are independent literature facts (empirically incompressible, k\*=1, with a
weak positive approx/param gradient that is roster sociology). The census's charges are outputs of the
classification theorems (coupled by construction, k\*=3, with the affine decoupling dominating). **The canon's
structure is not manufactured by curation — if anything the invented universe is the more structured one, because
its structure is the dichotomies talking to themselves.**

**Provenance.** Pre-registered in [`prereg_v2.json`](../../foundry/results/prereg/prereg_v2.json) (P3 reframed
before any census run, riders R-i/R-vi). Census: [`census.jsonl`](../../foundry/results/census/census.jsonl)
(sha `4de6d772…`, 13 rows). Machine output:
[`census_analysis.json`](../../foundry/results/census/census_analysis.json) (sha `93676357…`,
`foundry.analysis.run_all`). Estimator: the IDENTICAL `eightfold.factors` LCM + `crucible._null_chain`/`_both_real_v`
under `FOUNDRY_SPEC` — no eightfold modification (byte-identical). **Report at size: n=13 is tiny; these are
directional v1 findings, and the meaningful comparison needs Foundry-scale data (the pre-registered path).**

---

## The census (Sprint 2.2 — the N3 general-domain tier)

13 rows = **7 Boolean co-clone** (N1) + **6 general-domain |D|=3** (N3), **7 distinct charge profiles**, validates
clean through the shared kernel, P1 NPI calibration still passes.

The domain-3 tier is a **curated set of textbook-certain languages, each re-verified by the polymorphism
machinery** (Boolean → general-domain: the closure operators are domain-agnostic). Only the charges whose
dichotomy is *verified general-domain* are filled (R20); the rest are `open` (the Boolean dichotomies do not
transfer):

| Charge | Domain-3 oracle | Verified |
|---|---|---|
| **decision** | **Bulatov 2017 / Zhuk 2020** — CSP(Γ) ∈ P iff Γ has a WNU polymorphism, else NP-complete | lin-eq-Z₃/order/median → P; 3-coloring/NAE-3 → NPC (polymorphism test agrees with textbook) |
| **localization** | **Barto–Kozik 2014** (general domain) — bounded width iff WNU of all arities; a semilattice/majority gives it, affine (Maltsev-only) does not | order/median → bounded; affine → unbounded (the |D|=3 analogue of Boolean XOR); NPC → unbounded |
| counting / approximation / parameterized / proof_size / instruments | Boolean Creignou–Hermann / KSTW / Marx do **not** transfer; general-domain analogues unverified | `open` (honest) |

The R20 discipline caught a real error mid-build: a naïve "betweenness" encoding over the fixed 3-element domain
turned out majority-closed (tractable), so the polymorphism test **refused the NP-complete label** — it was
replaced with a second affine language.

## 3.1 — between-generation noise floor

Both census tiers are **deterministic** (curated CKZ / CKZ-analogue representatives) → **generations-exempt**
(the prereg's calibration property). The only sampled component is the domain-3 polymorphism-profile *explorer*;
across G=3 generations its profile-share vector drifts by at most **0.083**. Because the census rows themselves
are deterministic, the P2/P3 verdicts below are **exact**, not subject to this drift.

## 3.2 — P2 gradient verdict: RESIZE (reversed direction)

Both-real approx|parameterized rows (only the Boolean tier fills both charges; domain-3 leaves them `open`):

| rows | approximation | parameterized | reading |
|---|---|---|---|
| xor-sat (affine) ×1 | **inapprox** (hardest approx) | **FPT** (easiest param) | the **decoupling** — hard-approx, easy-param |
| horn/dual-horn/2-sat/3-sat/nae/1-in-3 ×6 | APX-complete | W[1] | medium/medium |

V=1.0 (perfect association), permutation **p=0.0002**, and it **beats the S1 null** (null-mean V=0.22, real
outside the envelope). So an association is unambiguously present — but read the **direction**: as approximation
gets *harder* (APX-complete→inapprox) parameterized gets *easier* (W[1]→FPT), the **opposite** of the canon's
"harder→harder" gradient. In the co-clone world the affine/XOR **deceptive-terrain control** (the pre-registered
distinctive placement) is not a lone outlier — it **defines** the approx/param axis. **Verdict: the canon's
positive gradient does not persist with direction intact → RESIZE**, the pre-registered "canon's-world" outcome
(the positive gradient was partly roster sociology; the theorem-world's coupling is the decoupling).

## 3.3 — P3 dimensionality verdict: DIVERGENT (census k\*=3 ≠ canon k\*=1)

The identical LCM held-out-prediction estimator on the 13-row census: held-out accuracy k=1 **0.67**, k=2 0.62,
k=3 **0.75**, k=4/5 0.75 → **k\*=3** (interval [3,4,5]). Per prereg_v2 P3a (SAME-WORLD iff census k\*≤1): the
census is **DIVERGENT** from the canon's k\*=1.

But the divergence's *meaning* is the finding, not the number. The census's charges are **derived from one
another by the classification theorems** — counting=FP iff affine, localization tracks the polymorphisms,
decision splits on the same algebra — so the rows lie on a low-dimensional manifold **by construction**. k\*=3 is
the census re-expressing its own entailment structure, **not** an emergent common cause. The canon's k\*=1, by
contrast, is a statement about *empirically sourced* charges that turned out predictively incompressible. So the
honest reading is not "the census is richer" but "**the two atlases encode fundamentally different objects** — a
theorem-coupled construction versus an empirical population — and their factor structure differs accordingly."
The hoped-for same-verdict-both-worlds does **not** hold.

## Honest caveats

1. **n=13 is tiny.** Held-out CV masks ~1–2 cells per fold; k\*=3 is a directional signal, not a precise count.
   What is robust: the census does **not** collapse to the canon's k\*=1, and the approx/param association is the
   affine decoupling. Both need Foundry-scale confirmation.
2. **The census's structure is theorem-forced.** Its associations are largely the entailment layer (R25) by
   construction; a v1.1 analysis should R25-net the census's factor structure before calling any residual
   emergent. The current k\*=3 is not net of the dichotomy coupling.
3. **The domain-3 tier fills only 2 charges** (decision, localization) — the Boolean-specific dichotomies
   (counting/approximation/parameterized) do not transfer, so the domain-3 rows contribute nothing to P2 and
   little to P3. A richer general-domain census needs verified domain-3 counting/approximation oracles (a real
   research lift), or a finer Boolean tier (0-/1-valid, chains — the documented v1.1 extension).
4. **No prior verdict argued back.** The canon's k\*=1 and its RESIZED Crucible verdicts stand; Foundry reports
   its own, DIVERGENT, world at size.

## Forward

- The **program's central question is answered directionally at v1**: the canon's low-dimensional,
  positive-gradient structure is **not reproduced** by a theorem-generated census — because the census's charges
  are dichotomy-coupled, not empirically sourced. Same-verdict-both-worlds is refuted at v1 scale.
- The **decisive test needs scale**: a much larger census (finer Boolean co-clones + verified domain-3
  counting/approximation) and an R25-netted factor analysis. That is the Foundry-scale path prereg_v2 anticipates.
- **Kill status:** K1 (domain-3 oracle) did NOT fire — decision+localization were verified general-domain in the
  timebox. K2 (profile poverty) is partially live: 7 distinct profiles is thin for a factor claim, which is why
  P3 is reported at size.
