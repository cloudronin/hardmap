# Pebble I-SP — Susceptibility Propagation: an analytic route to ξ?

**Investigation memo, NOT a result.** Ran in parallel with P2; touches no Pebble prereg, alters no sealed rule, feeds
no ξ measurement. Timebox 3h. Literature pinned from primary sources (ar5iv HTML, equation LaTeX extracted
first-hand) under R20 discipline — verified claims are cited; unverifiable ones are flagged in §7. No novelty
language: every quantity below is already named and owned by the statistical-physics literature.

## 0. Verdict

**VALIDATOR (regime-limited) — reserved for the scale-out regime; NOT usable on the v1 roster.**

Susceptibility propagation (SuscP) is implementable and general on our roster and computes — analytically, by
message passing, without sampling — the **two-point connected correlation** `⟨s_i s_j⟩_c = ∂m_i/∂h_j`, i.e. the
*same* pairwise quantity ξ's `corr` observable samples. But its accuracy is regime-limited in exactly the way that
disqualifies it *here*: exact on trees, an uncontrolled heuristic on loopy graphs (the susceptibility itself
**diverges** on a single loop in the authors' own example), reliable only for **large, locally tree-like, below-
condensation** instances. Our v1 roster is the opposite — **small (n=8–24, hence short loops), anchored near the
structural transition** — and at n≤24 exact/sampled correlations are already in hand. So on the v1 roster the
consequence is the INAPPLICABLE one: **ξ proceeds alone.** SuscP's validator role is real but lives at scale (the
canon extension), where sampling is expensive and BP is trustworthy; adoption there requires its own prereg and its
own two-pole qualification, the same gates ξ faces.

A scope flag independent of the verdict (§4): SuscP's two-point correlation is the **pairwise shadow** of the
**point-to-set** correlation that "reach" formally is — and ξ's current pairwise observable shares that limitation.

## 1. The question and the three sealed verdicts

The pebble-drop measures correlation by **sampling**. SuscP computes correlation functions **analytically**, by
message passing on the factor graph, no solutions sampled. If implementable and accurate on our families, the cost
model for the propagation program changes.

| Verdict | Meaning | Consequence |
|---|---|---|
| SUBSTITUTE | cheap per-family correlation, accuracy covers our roster | ξ becomes validator, SuscP scales out |
| **VALIDATOR** ✅ | implementable, accuracy regime-limited (trees / fails near threshold) | run both where regimes overlap; agreement = concordance, disagreement locates regimes |
| INAPPLICABLE | not implementable, or assumptions violated by roster structure | document why; ξ proceeds alone |

We land on **VALIDATOR by type** (the limitation is accuracy-regime, not structural inapplicability — SuscP *is*
implementable on our factor graphs), but with the **v1-roster consequence of INAPPLICABLE** (no overlapping reliable
regime exists on n≤24 loopy near-transition instances, so ξ proceeds alone now).

## 2. I-SP1 — pinned equations (primary sources)

### SuscP — Higuchi & Mézard, arXiv:0903.1621 (J. Phys. Conf. Ser. 233:012003, 2010)
SuscP is the **linear response of belief propagation to an auxiliary local field** `h_j` (added to the joint law,
Eq. 1), sent to 0 at the end. Messages are field-derivatives of the BP cavity messages:
`ν_{i→a,j} = ∂ν_{i→a}/∂h_j|_0`, `ν̂_{a→i,j} = ∂ν̂_{a→i}/∂h_j|_0` (Eqs. 6–7). The clean binary (`s=±1`) form:
```
(16) n_{i→a}   = Σ_{b∈∂i\a} n̂_{b→i} + h_i           (BP field messages)
(19) n̂_{a→i}  = ½ log[ F(+1)/F(−1) ],  F(σ) = Σ_{s_∂a} δ_{s_i,σ} ψ_a(s_∂a) Π_{j∈∂a\i} e^{ n_{j→a} s_j }
(20) η_{i→a,j} = Σ_{b∈∂i\a} η̂_{b→i,j} + δ_{i,j}      (susceptibility messages, η ≡ ∂n/∂h_j)
(21) η̂_{a→i,j}= Σ_{m∈∂a\i} [∂f_{a→i}/∂n_{m→a}] η_{m→a,j}
(24) ⟨s_i s_j⟩_c = [1 − tanh²(Σ_b n̂_{b→i})] · [ Σ_c η̂_{c→i,j} + δ_{i,j} ]     (the deliverable)
```
`i` and `j` may be any two variables on the factor graph. **What it computes (Eq. 5):** the two-point connected
correlation `p_ij − p_i p_j = ∂p_i/∂h_j` — a susceptibility `χ_ij = ∂m_i/∂h_j`.

### Correlation-based transitions — KMRSZ, arXiv:cond-mat/0612365 (PNAS 104:10318, 2007)
Transitions are defined by decay of a **variable-to-boundary** correlation, in a nested hierarchy (`x̄_ℓ` = variables
at distance ≥ ℓ from i):
- **Clustering / dynamical α_d** — *extremality* (Eq. 3): `E Σ_{x̄_ℓ} μ(x̄_ℓ) Σ_{x_i}|μ(x_i|x̄_ℓ) − μ(x_i)| → 0`
  stops holding. This **is** the point-to-set / reconstruction condition; above α_d the measure splits into
  exponentially many clusters.
- **Condensation α_c** — the weaker finite-subset correlation (Eq. 5) stops decaying, equivalently the cluster
  **complexity Σ(s\*) = 0**; above α_c the mass condenses onto sub-exponentially many clusters.
- Ordering `α_u ≤ α_d ≤ α_c ≤ α_s`. **BP statements (verbatim):** exact "for tree factor graphs," a "heuristics on
  loopy factor graphs"; provably good below uniqueness α_u; empirically tracks the measure up to α_c; **"Above the
  condensation transition … the BP fixed point no longer describes the measure μ."**

### Point-to-set — Montanari–Semerjian cond-mat/0603018; reconstruction = clustering — Montanari–Restrepo–Tetali arXiv:0904.2751
- Point-to-set correlation (MS Eq. 6): `G_i(r) = sup_{|f|,|F|≤1} |⟨f(x_i)F(x_{∼i,r})⟩ − ⟨f(x_i)⟩⟨F(x_{∼i,r})⟩|`, one
  variable vs the **entire** far set; length `ℓ_i(ε)` (Eq. 7).
- MRT: reconstruction solvable iff `lim_r limsup_n E‖μ_{i,∼r} − μ_i μ_{∼r}‖_TV > 0`; **Thm 3.2/3.3: α_d = α_r**
  (clustering and reconstruction thresholds coincide).

## 3. I-SP2 — generality (the load-bearing item): **PASS**

**From source:** the SuscP update rules contract an **arbitrary** factor `ψ_a(x_∂a)` — Eq. 19's `F(σ)` sums
`ψ_a(s_∂a)` over the incident configurations with no k-SAT/occupation structure used, and the paper states verbatim
**"The rules (8,9) apply to all types of CSPs with discrete variables."** The occupation/1-in-k structure is only in
the worked examples, not the algebra.

**On our roster:** a constraint is `(R, scope)` with **R an arbitrary frozenset of tuples over {0,1}^k** — the
compatibility function is exactly `ψ_a(x) = 1[x_scope ∈ R]`, a lookup table. The factor contraction runs over the
`2^{k−1}` configurations of the other incident variables (per output state); **at arity 3–4 that is 4–8 local terms
— negligible.** Per the paper, one iteration is `O(N²)` for fixed k, memory `kMN`; at N≤24 the whole instance is
trivial. **Generality-and-cost is not the obstacle.**

## 4. I-SP4 — vocabulary map (and the decisive distinction)

| Physics term (owner) | Our term | Same or distinct |
|---|---|---|
| two-point connected correlation `⟨s_i s_j⟩_c` (MS "point-to-point"; structure factor) | ξ `corr` observable; SuscP output | **the pairwise family** — what both ξ-as-built and SuscP compute |
| susceptibility `χ_ij = ∂m_i/∂h_j` | ξ `forcing` observable (single-variable response) | pairwise family (summed/linearised two-point) |
| **point-to-set correlation** `G_i(r)` / `‖μ_{i,∼r} − μ_i μ_{∼r}‖` | (unbuilt) — the true "reach" | **DISTINCT, generally longer** |
| reconstruction threshold; clustering α_d | the density where reach diverges | = point-to-set (MRT: α_d = α_r) |

**The decisive point (MS, verbatim):** "the solution to the conundrum is that ℓ is defined in terms of **point to set
instead of point to point** correlations." The pairwise length can stay finite while the point-to-set length
diverges — pure ≥3-ary parity is the extreme case (zero pairwise correlation, full point-to-set). **So "reach" (how
far a *partial solution* — a set/boundary — biases a distant variable) is the point-to-set length, NOT the pairwise
length.** SuscP computes the pairwise object; **ξ as currently built (both observables) also computes a pairwise
object.** Neither reaches the point-to-set quantity. This is a scope flag for the bridge hunt — it does not change
the I-SP verdict (SuscP is a route to ξ-**as-built**, which is pairwise), but it flags that ξ-as-built may itself be
the pairwise shadow of the program's intended target.

## 5. I-SP3 — accuracy regime: our regime is OUTSIDE validity

- **Trees: exact** (SuscP fixed point gives the exact 2-point correlation; demonstrated on a chain).
- **Loops: no guarantee.** Higuchi–Mézard, verbatim: "if the graph has more than one loop, there is no guarantee
  either that the fixed point exists or the iteration leads to that fixed point"; their single-ring example makes
  **SuscP diverge** ((1−M) singular). KMRSZ: loopy BP is "a heuristics … the quality of [its] results cannot be
  assessed a priori."
- **Reliable only** for large, locally tree-like, **below-condensation** instances; fails above α_c (RSB → survey
  propagation needed).
- **Our v1 roster:** n = 8–24 → **short loops** (random arity-3/4 constraints on few variables are loop-dense, not
  locally tree-like); densities anchored **near the structural transition**. This is the least-trustworthy corner for
  a BP-susceptibility. And at n≤24 we can already enumerate/sample the exact correlations, so SuscP would be both
  **unreliable and unnecessary** here.

## 6. I-SP5 — prototype: DECLINED per the gate

The prototype is gated on I-SP2 **and** I-SP3 passing. I-SP2 passes; **I-SP3 does not** (our regime is outside
validity). The source already tells us the likely outcome on our loopy instances — the susceptibility diverges on
loops (the ring example) — so a prototype would reproduce a known failure, adding nothing citable within the
timebox. No prototype was run; no throwaway numbers exist to cite. (Had I-SP3 landed "reliable at some anchored
density," a 3-pole throwaway timing + ordering check would have been warranted; it did not.)

## 7. Consequence for Pebble, and discipline

- **ξ (P2) proceeds alone on the v1 roster.** SuscP is not adopted now.
- **SuscP is a live VALIDATOR candidate for the scale-out** (the canon extension: large, locally tree-like, sub-
  condensation instances where sampling is expensive and BP is trustworthy). There it can cross-check ξ's **pairwise**
  component; **if adopted it faces its own prereg + two-pole calibration + qualification** — a method arriving with a
  literature still has to prove it measures what we think on our roster.
- **Bridge-hunt flag (logged, not acted on):** both ξ-as-built and SuscP are pairwise; the program's intended
  "reach" is arguably point-to-set (= reconstruction = clustering α_d). A future point-to-set instrument (e.g. a
  fix-a-far-boundary / reconstruction-on-the-cavity-tree measurement) is the object that would measure reach proper.
- **No novelty:** susceptibility propagation (Mézard–Mora 2008; Higuchi–Mézard 2009), point-to-set correlation
  (Montanari–Semerjian 2006), reconstruction=clustering (Montanari–Restrepo–Tetali 2011), and the clustering/
  condensation hierarchy (KMRSZ 2007) are all owned by the physics literature and named there first.

## 8. Citations
- S. Higuchi, M. Mézard, "Susceptibility Propagation for Constraint Satisfaction Problems," arXiv:0903.1621; J. Phys.
  Conf. Ser. 233 (2010) 012003. (Origin of SuscP: Mézard & Mora 2008; Montanari & Rizzo 2005.)
- F. Krzakala, A. Montanari, F. Ricci-Tersenghi, G. Semerjian, L. Zdeborová, "Gibbs states and the set of solutions
  of random CSPs," PNAS 104:10318 (2007); arXiv:cond-mat/0612365.
- A. Montanari, G. Semerjian, "Rigorous inequalities between length and time scales in glassy systems," J. Stat.
  Phys. 125:23 (2006); arXiv:cond-mat/0603018.
- A. Montanari, R. Restrepo, P. Tetali, "Reconstruction and clustering in random CSPs," SIAM J. Discrete Math.
  25:771 (2011); arXiv:0904.2751.
- (Pointer) L. Zdeborová, F. Krzakala, "Statistical physics of inference," Adv. Phys. 65:453 (2016); arXiv:1511.02476.

## 9. Verification caveats (R20)
- SuscP updates Eqs. (8)–(9) as *printed* in the arXiv source carry two apparent typos (a shared dummy index; a
  trivial `δ_{x'_i,x'_i}`); the corrected linear-response form was inferred, not quoted — the clean binary Eqs.
  (16)–(24) are unambiguous and are what §2 relies on. The published IOP text was not accessible (no PDF tooling);
  arXiv equation numbers may renumber there.
- The `2^{k−1}` per-factor contraction cost is derived from the sum structure of Eq. (19), not quoted (the paper
  states only "O(N²) for fixed k").
- KMRSZ/MRT equation numbers are from the ar5iv rendering; `Ω_k` in `α_d=α_r=(Ω_k/k){log k+…}` was not extracted.
  Textbook identities (χ_SG, χ ∝ S(k→0)) and the Kesten–Stigum two-point threshold were not fetched verbatim and are
  not load-bearing here.
