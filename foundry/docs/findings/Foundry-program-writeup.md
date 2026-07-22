# Foundry — the synthetic-census program: what it asked, what it found

**Program in one paragraph.** Foundry built a *synthetic* charge atlas — a census of constraint languages whose
complexity charges are assigned by the CSP dichotomy theorems rather than curated from literature — to test
whether the structure the Eightfold canon found in ~118 human-chosen problems is a property of *computation* or of
the *human roster*. The answer is a clean separation with a sharp internal boundary. Over the **oracle** columns
(the theorem-assigned charges) the synthetic world is **100% theorem-forced**: netting the dichotomies out leaves
exactly zero residual, so the census re-expresses its own algebra and carries no empirical content beyond it — the
canon-vs-computation question is closed there at its ceiling, a *category difference*. Over the **measured**
columns (solution-space geometry, which no theorem assigns) the census yields a genuine new structural fact:
**complexity factors through the algebraic classification, but solution-space terrain factors through the specific
relation one resolution below** — two components of the hardness vector living at different resolutions of the same
object, with a proved impossibility separating them and a named algebraic mechanism (Maltsev rigidity) pinning one
end. Computation does not reproduce the canon's empirical shape; instead it exposes a decomposition the canon's
(all clone-level) charges could not.

Status: everything below is on `main`, reproducible, and tested (56 foundry + 72 eightfold green; eightfold
byte-identical throughout — Foundry never mutates the frozen canon kernel). Preregs v1–v11 each locked before
their analysis; the paper trail is listed at the end.

---

## 1. The question and the apparatus

Eightfold curated a cross-task charge atlas over human-chosen problems; Crucible hardened it (the
approximation↔parameterized gradient SURVIVED an adversarial battery at p=0.0001; two claims RESIZED). The open
question: is that structure *computational* or *sociological* — a fact about hardness, or about which problems
people study? Foundry answers it by building the **computational counterfactual**: a census where each row is a
constraint language Γ and each charge is assigned by a verified dichotomy theorem (Schaefer, Creignou–Hermann,
KSTW/Håstad, Bulatov–Zhuk, Barto–Kozik, Marx / Bulatov–Marx Thm 4.1), reusing the Eightfold kernel unchanged
(one-way import; `FOUNDRY_SPEC`). Two column *kinds*: **oracle** charges (theorem-derived) and **measured**
instrument charges (solution-space `landscape`, which the theorems do not assign).

## 2. The F1 predictions ledger, scored

| # | prediction (on file, pre-registered) | verdict |
|---|---|---|
| **P1** | NPI-calibration: the census's NP-intermediate row is empty by dichotomy | **PASSED** — 0 NPI rows (Schaefer/Bulatov–Zhuk) |
| **P2** | the approx↔parameterized gradient persists in CSP-land | **INSUFFICIENT → STRATIFIED**: H_P2_scaled is algebra-stratified, non-monotone, and **R25-netted to residual 0** (Task 0) — the census association is 100% theorem-forced, not the canon's empirical gradient |
| **P3** | canon-fitted factor loadings reproduce (on-file k∈{3,4}) | **MISS + DIVERGENT**: canon read **k\*=1** (Factors v1; the k∈{3,4} prediction is a scored miss); census read k\*=3 but that too is theorem-forced (Task-0 residual 0) |
| **P4** | ≥1 gap-list cell inhabited by construction (Tier-2) | **NOT ATTEMPTED** — the geometry line consumed the sprints; construction is future work, recorded honestly |
| **Factors** | effective dimensionality of the canon | **k\*=1** (v1; low-rank k\*=0 triangulation) — the canon is predictively 1-dimensional; the on-file k∈{3,4} is a miss |
| **I6 / measured** | an oracle charge predicts measured landscape ruggedness | **SUPPORTED internally, does-not-generalize** (Sprint 4) → superseded by the **resolution decomposition** (§4) |

No prediction was argued back; downgrades on new evidence are recorded, upgrades are not.

## 3. Closure I — the oracle columns are theorem-forced (Task 0)

Netting the theorem-forced component out of the census's P2/P3 statistics (the standing R25 procedure) returns
**exactly zero residual**, three independent ways: provenance netting empties the both-real table (V=0.472 →
undefined, `survives=False`, the opposite of the canon which survives); within-polymorphism-stratum pooled V = 0;
residual dimensionality = 0. Cross-validated against the *actual* canon at the six shared anchors: **18/18
perspective-free cells agree** (decision/counting/approximation), while `parameterized` is perspective-divergent
(canon treewidth vs census Exact-Ones — incomparable, not wrong). **Verdict: the oracle-only canon-vs-computation
comparison is closed at its ceiling — a category difference, cross-validated at the anchors, incomparable
elsewhere.** The synthetic world's oracle columns are its dichotomies; they hold no empirical content the canon
could be compared against. ([Sprint4-Task0-R25-netting.md](Sprint4-Task0-R25-netting.md).)

## 4. Closure II — the measured columns are a resolution decomposition (Sprints 4, 4.5, 4.6)

The measured line asked whether *any* oracle charge predicts the solution-space terrain the theorems don't assign.
It required a net-new solution-side instrument (the Proof-Census apparatus samples the *proof* side; the
`landscape` charge is the *satisfiable* side), qualified against two-pole calibration in both domains, with an
affine-exact ground truth confirming near-zero sampler bias. The answer resolved, through a domain-confound check
and two roster experiments, into four linked results:

1. **The clone-invariant impossibility (proved).** A co-clone *is* the set of relations sharing a polymorphism
   clone, so **every** language-level algebraic invariant — tractability class, connectivity class, rigidity rank
   — is constant on the co-clone by construction and **cannot** explain within-co-clone terrain variation. That
   variation is carried by the *choice of representative relation*, the information the clone discards.
2. **Connectivity classes: NOT_PREDICTIVE** (prereg_v9). The GKMP relation-level classes (OR-free / NAND-free /
   componentwise-bijunctive) are near-constant within co-clones — one instance of the impossibility. Framed as
   *worst-case structural ≠ typical-case sampled*, with the GKMP–Schwerdtfeger line credited as **convergent
   prior art**: they built finer relation-level classes *because* Schaefer's classes cannot classify solution
   structure — our headline reached first, from the worst-case side.
3. **The envelope is partially clone-predictable (rigidity: PARTIAL).** Rigidity rank (idempotent-Taylor
   hierarchy) predicts the *between*-stratum spread — **Maltsev (affine) rigidity forces near-zero within-co-clone
   spread (0.039)**, the theory-grounded mechanism naming *why* the affine strata are the one place geometry
   factors through the algebra (prereg_v10/v11; the middle of the hierarchy orders weakly, corr −0.389).
4. **Terrain itself is relation-predictable (Sprint 4.6 B: SUPPORTED).** A relation-level feature —
   `tuple_dispersion`, the relation's own tuple-geometry, which varies within a co-clone — predicts measured
   ruggedness and **beats the marginal baseline held-out by co-clone** (MSE 0.10 vs 0.23; permutation p=0.0002).
   Honestly: the *sealed density mechanism failed* (physics density→clustering does not transpose to
   relation-density); tuple-geometry carried it.

**The measured verdict:** complexity is a **clone-level** property; solution-space terrain is a **relation-level**
one — two components of the hardness vector at different resolutions of the same object. This is a sharper claim
than the latent-basis hypothesis the program retired (Factors k\*=1), and it is measured, not assumed. Foundry's
one solid *positive* charge-level result — affine coset-dispersion — is exactly the point where rigidity is maximal
and the two resolutions collapse into one. ([Sprint4-results.md](Sprint4-results.md),
[Sprint4-confound-check.md](Sprint4-confound-check.md), [Sprint4-connectivity-test.md](Sprint4-connectivity-test.md),
[Sprint4-rigidity-envelope.md](Sprint4-rigidity-envelope.md),
[Sprint4.6-resolution-decomposition.md](Sprint4.6-resolution-decomposition.md).)

## 5. The canon-vs-computation verdict, plainly

The synthetic census and the human canon **encode different objects, and the comparison resolves differently on
each column kind.** On the oracle columns the census is a closed algebraic system (residual 0) — it cannot
reproduce the canon's *empirical* gradient because it has no empirical content; the canon's structure was a
property of hardness-as-curated, and the theorem-world simply re-states its dichotomies. On the measured columns,
where genuine measurement is possible, computation does **not** reproduce the canon's shape either — but it reveals
something the canon's charges (all clone-level, all theorem-derived) structurally *cannot*: that terrain lives one
resolution below complexity. So "is the canon's structure computational or sociological?" answers: the *oracle*
structure is neither — it is tautological in the synthetic world and empirical in the canon, two incommensurable
things; the genuinely computational structure is the *measured* decomposition, which the human roster never
exposed because it never carried a measured column.

## 6. Convergent prior art (credited, not claimed)

- **Density → clustering** (the mechanism Sprint 4.6 B sealed and that *failed* to transpose): owned outright by
  the statistical physics of random CSP ensembles (cavity method; clustering/condensation/freezing transitions).
- **Solution-space connectivity can't be read off Schaefer:** the GKMP–Schwerdtfeger connectivity line (tight,
  safely-tight, CPSS, constraint-projection separation) reached the "tractability doesn't classify geometry" wall
  first, from the worst-case side. Foundry's contribution is the *typical-case sampled* extension and the
  clone/relation **resolution decomposition** — whose own novelty is a related-work question flagged for any
  external write.

## 7. Parked, deferred, honest negatives

- **Charge 9 / Ω⁻ (Sprint 6): PARKED.** The out-of-sample basis test is vacuous at canon k\*=1 (no basis to
  predict from); its redesign waits on what the relation-level geometry line produces.
- **Proof-side `proof_size` BSW consistency check: DEFERRED.** Its ceiling is confirming a theorem already
  trusted (Ben-Sasson–Wigderson); low value, and pysat is absent in the dev venv.
- **P4 construction: not attempted.** Recorded, not hidden.
- **Foregrounded negatives:** the Factors k∈{3,4} miss; I6-as-a-width-law false (implication counterexample);
  H_I6b polymorphism ordering refuted; the domain-3 "anomaly" withdrawn; the Sprint-4.6 density mechanism wrong.
  Each is a scored result, at size.

## 8. What's next

The honest, stronger continuation the measured line gated in: a **relation-level solution-geometry study** — sample
geometry at the relation level (not one representative per co-clone), and pin the *typical-case* predictor of
ruggedness whose first evidence is `tuple_dispersion`. The framing to test: the hardness vector has a clone-level
complexity component and a relation-level geometry component, separable by resolution — and whether *that*
decomposition is itself anticipated in the adjacent literatures.

## Appendix — the paper trail

Preregs (each locked before its analysis): v1 (predictions) · v2 (P3 operationalized) · v3 (H_P2_scaled floor) ·
v4 (I6 + measured protocol) · v5 (owner riders R-a..R-e) · v6 (I6 face-value + H_I6b) · v7 (GKMP netting, before
fresh data) · v8 (Sprint-4 closure) · v9 (connectivity test) · v10 (rigidity envelope) · v11 (Sprint 4.6 A+B).
Findings: this document + F1 note, I-phase, Sprint 3 / 3.5, and the Sprint-4 suite (Task-0, I5 memo, calibration
gate, confound check, results, connectivity, rigidity, 4.6 decomposition). Code: `charges`, `postlattice`,
`oracles`, `finer`, `domain3`, `paramd3`, `analysis`, `r25`, `ensemble`, `solscape`, `landscape_run`,
`connectivity`, `rigidity`, `relfeatures`; eightfold `factors`. Verdicts are scored, negatives foregrounded, the
frozen canon untouched.
