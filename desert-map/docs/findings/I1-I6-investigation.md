# I1–I6 Investigation — findings & build decisions

Confirm-before-build items from spec §7. Run 2026-07-20, before any `relax.py` code. Web-sourced;
negative results are stated as "we found no prior work," not "none exists."

---

## I1 — Differentiable Resolution / continuous relaxation of refutation search

**Finding:** No off-the-shelf differentiable operator for the *Resolution refutation object* exists.
The nearest neighbours relax something else:

- **NeuRes** (Kalra et al., NeurIPS 2024, arXiv:2402.08365) — keeps resolution **hard/symbolic**; a net
  autoregressively *selects clause pairs*. Guides discrete search; no soft resolvent. **Nearest prior art.**
- **SATNet** (Wang et al., ICML 2019, arXiv:1905.12149) — relaxes *satisfiability* via a MAXSAT SDP; no proof object.
- **Neural Theorem Provers** (Rocktäschel & Riedel, NeurIPS 2017, arXiv:1705.11040) — soft *unification* in a Horn/KB backward-chaining calculus; not resolution-refutation.
- **Semantic loss** (Xu et al., ICML 2018) / **LTN** / **DeepProbLog** / t-norm survey (van Krieken et al., arXiv:2002.06100) — relax *truth values* via fuzzy t-norms; these give the soft-OR/AND *primitives* but no resolvent-over-clauses.

**Decision:** Build the fresh soft-resolution operator. **Reuse the product-t-norm soft-OR primitive**
`soft_or(A,B) = 1-(1-A)(1-B)` (well-established — cite Xu 2018 / van Krieken 2020; do **not** claim it as
novel). The contribution to claim is the *differentiable refutation-search relaxation* (soft resolvent over
a growing clause pool + soft derivation chain to a soft empty clause) — genuinely not off-the-shelf.
Position NeuRes as the honest closest prior work (it guides discrete resolution; we relax the step itself).
→ **Confirms the approved M2 operator design.**

## I2 — Overlap estimator m(q) (spin-glass / random-CSP convention)

**Finding (exact definition):** For configurations σ^a, σ^b over N ±1 spins,
**q = (1/N) Σ_i σ_i^a σ_i^b ∈ [−1,1]**; q = 1 − 2·d_H/N (d_H = Hamming distance). Boolean CSP convention
(KMRSZ 2007): map x_i∈{0,1} → y_i = 2x_i−1 and use the same estimator. **P(q)** = distribution of pairwise
overlaps over independent samples/seeds of the *same* instance; estimate by histogramming all R(R−1)/2 seed
pairs, then average over instances. **Single sharp peak = replica-symmetric (one lump); bimodal / non-trivial
support = RSB / clustering / shattering** (1RSB → two overlap values: intra- vs inter-cluster). As α→α_s the
solution set passes α_d (clustering; second peak appears) → α_c (condensation) → α_s.

**Refs:** Mézard–Zecchina PRE 2002 (cond-mat/0207194); KMRSZ PNAS 2007 (cond-mat/0612365); Zdeborová–Krzakala
Adv.Phys. 2016 (1511.02476); Daudé–Mézard–Mora–Zecchina 2007 (cs/0703065).

**Decision for E2 (`metrics.py`):** proofs are **fixed-dimension soft membership vectors** → default to the
**±1-spin overlap** `q = (1/N)Σ v_i^a v_i^b` (map membership m_i→2m_i−1) for direct comparability to physics
P(q); for soft weights use the **mean-centered, variance-normalized (Pearson-style)** form so all-on
coordinates don't inflate overlap. For genuinely sparse variable-size *sets* (decoded discrete proofs) use
**Jaccard/cosine**, optionally rescaled q=2s−1. Build P(q) by the independent-seed pairwise-histogram
protocol. Bimodal E2 = operational proof-space clustering signature. **Direction (per our corrected dial):
bimodal split predicted as α DECREASES toward threshold.**

## I3 — OGP applied to proof search

**Finding:** Overlap-Gap Property (Gamarnik, PNAS 2021, arXiv:2109.14409; sharp-threshold k-SAT
arXiv:2309.09913) is defined **exclusively over solution spaces** (barrier to *solution-finding*). We found
**no work defining overlaps/a gap over refutation/proof objects** or OGP as a barrier to *proof search*.
Distinct near-miss to firewall: Ben-Sasson–Wigderson "short proofs are narrow" (JACM 2001) + Chvátal–Szemerédi
use solution-space expansion → resolution *width/size* bounds — that is **not** an OGP over proofs.

**Decision:** Strongest novelty claim. Frame v1 as *introducing* an overlap/overlap-gap lens on
refutation-search geometry; cite Gamarnik 2021 as the formalism being ported; explicitly distinguish
proof-space overlaps from BSW width/expansion; phrase as "we are not aware of prior work applying OGP to proof
search." (Medium-high confidence — a web negative is not a literature-complete proof.)

## I4 — Lanczos Hessian tooling

**Finding:** PyHessian (amirgholami) is effectively **dormant** (no releases; ~18-month commit gap) and its
model+dataloader API is friction for a bespoke parameterization. hessian-eigenthings (noahgolmant) is the
healthiest *library* but still wraps a model/dataloader HVP abstraction. For a **few-thousand-param** problem
we can afford **exact** autograd HVPs.

**Decision (`hessian.py`):** Hand-roll Lanczos — **`torch.func.hvp` for exact HVPs + `scipy.sparse.linalg.eigsh`
on a `LinearOperator`, in float64** (both spectral ends via `which='LA'`/`'SA'`; shift-invert/LOBPCG for
eigenvalues near zero). No third-party Hessian dep (scipy already in `[compute]`; `torch.func` ships with
torch). hessian-eigenthings kept as a documented fallback only.

## I5 — HF flavors / timeouts / sharding (deferred to build time)

Confirm exact flavor strings with `hf jobs hardware` **when the key is dropped** — cannot auth the CLI yet.
Documented defaults live in `desertmap/config.py` (t4-small smoke, l4x1 sweep, l40sx1 OOM-fallback,
cpu-upgrade fixtures). Every launch passes an explicit `--timeout` (cost cap; HF default is 30 min). E1 is
sharded per-(n,α) so a failed cell doesn't burn the sweep. Budget ceiling **$75**, tracked vs kill §6.3.

## I6 — Planted short Resolution refutation construction

**Finding:** *Finding* a ≤k-step refutation is W[1]-complete (Fellows–Szeider–Wrightson 2004) — which is
exactly why a *planted* one is a meaningful positive control. DRAT ⊋ resolution: raw "short DRAT" ≠ short
resolution (RAT steps aren't resolution); DRUP→resolution needs `drat2er` (Kiesl, IJCAR 2018), general
DRAT→*extended*-resolution (not plain). PHP is exponentially hard for resolution (hard negative, never a
planted positive).

**Decision (`instance.py` planted builder):**
- **Primary (for E0/M2 gate):** hand-construct a small unsat core of **controlled resolution length** (e.g.
  a short implication chain `(x)`,`(¬x∨y)`,`(¬y∨z)`,`(¬z)`, or a complete contradiction over k=3–4 vars),
  **mix the core variables into satisfiable filler** over the remaining ~16 of n=20 vars so the search must
  *find* the core (not read it off a unit-propagation pass), and ensure filler creates no shorter alternate
  refutation. Exact planted length is known by construction. **No extra deps** (python-sat verifies unsat).
- **Secondary (observational only):** harvest naturally-short instances from a DRAT-logging solver
  (CaDiCaL via pysat); if reporting resolution length, run **DRUP → drat2er → resolution** and verify with
  DRAT-trim. Never quote raw DRAT step counts as resolution length. (`drat2er`/`drat-trim` are optional,
  not required for the E0 gate.)
- **Hard negatives:** PHP and Tseitin-on-expander — show the relaxation *fails* to find short proofs where
  none short exist.

---

### Build refinements after review (C1, C2)
- **C1 — E0 success = "decoded proof verifies," from random init** (not planted-proof recovery). The
  planted core only witnesses that a refutation of length ≤ chain-length exists (sets budget `L`); any
  verifying refutation counts. The uncertifiable "no shorter alternate refutation" requirement is dropped
  (same W[1] problem); the certifiable property kept is **filler is satisfiable on its own** (python-sat
  check, `instance.planted_filler`) ⇒ every refutation engages the core. Uniqueness neither claimed nor
  required.
- **C2 — PHP and Tseitin-on-expander promoted to a spec §3.5 control category** ("no short proof exists").
  The relaxation is *expected* to fail there; failure is the correct reading and is pre-registered
  (`results/prereg/prereg_v1.json`). Generators: `instance.gen_php`, `instance.gen_tseitin`.

### One-line decisions
- **I1** build fresh operator, reuse t-norm primitive (cite), claim the refutation-search relaxation; NeuRes = nearest prior art.
- **I2** ±1-spin overlap q=(1/N)Σv^a v^b for fixed-dim membership (Pearson-normalized for soft); Jaccard/cosine for sparse sets; bimodal-as-α↓threshold.
- **I3** OGP-on-proof-search unclaimed = strongest novelty; cite Gamarnik 2021, firewall from BSW.
- **I4** hand-rolled Lanczos (`torch.func.hvp` + scipy `eigsh`, float64); no PyHessian dep.
- **I5** confirm flavors via `hf jobs hardware` at key-drop; explicit `--timeout`; shard E1; $75 ceiling.
- **I6** hand-planted unsat-core+filler (controlled length) for E0; solver-DRAT observational only (DRUP→drat2er→resolution); PHP/Tseitin hard negatives.
