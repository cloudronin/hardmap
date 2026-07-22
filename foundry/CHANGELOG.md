# Changelog — foundry

## 0.1.0 (unreleased) — N0 scaffold

- **N0 scaffold — the product stands up and the Phase-K kernel reuse is proven.** New `foundry/` product
  (pyproject with the one-way `-e ./eightfold` install pattern; `AGENTS.md` invariants incl. the Rider-A
  sequencing note; README; CI leg). **`FOUNDRY_SPEC`** (`foundry/charges.py`): nine charges — seven oracle
  columns (decision/Schaefer, counting/Creignou–Hermann, approximation/KSTW, parameterized/Marx,
  parallelization/ABISV, proof-size/Molloy, **localization/Barto–Kozik** — the I6 hypothesis-bearing column) +
  two measured instrument columns (average_case, landscape); `derived` broadened to the oracle columns; a
  three-rule entailment layer (E1, E2 carried over + the CSP-native bounded-width⟹P rule). A hand-checked
  **toy stratum** (`foundry/census.py`: affine/XOR — the deceptive-terrain control — Horn, 3-SAT) exercises
  the schema. **Phase-K payoff proven** (`tests/test_kernel_reuse.py`, 7 tests): the shared eightfold validator
  + gap-list + null sampler accept Foundry's census rows under `FOUNDRY_SPEC` with **zero eightfold
  modification**; gate 6b (`side==value`) fires under `FOUNDRY_SPEC`; validating a foundry row against
  `EIGHTFOLD_SPEC` correctly fails. **`prereg_v1.json`** locks predictions 1–4 (P3 = untested, Factors absent),
  roster/generations policy, the Crucible-hardened battery, kill thresholds, and the I-phase (I1–I6) status.
  **F1 note committed** (`docs/findings/F1-canon-or-computation-note.md`, Rider C) — the predictions'
  timestamped provenance. **Next: the I-phase, then N1 (CKZ co-clone roster + dichotomy oracles).**
- **I-phase — dichotomy oracles verified** (`docs/findings/I-phase-investigation.md`). Web-verified the exact
  statements/scopes: Schaefer (decision), Creignou–Hermann (#CSP ∈ FP iff affine), KSTW+Håstad (Max-CSP),
  ABISV (within-P NC/P-complete), Barto–Kozik (bounded width iff a weak-NU polymorphism; affine is the sole
  obstruction), Marx (parameterized dichotomy exists), CKZ (a plain basis per co-clone — the roster generator,
  R-B). Per discipline: cleanly-per-cell columns fill `derived`; `parameterized` (Marx verified, weakly-
  separable per-co-clone check deferred) and `proof_size` (Molloy, N4) are honestly `open`, never guessed.
- **N1 — Boolean census built + validated.** `postlattice.py`: the Post's-lattice spine as concrete relations
  (R-B — CKZ plain-basis representatives, never enumeration); `oracles.py`: the oracles **compute** each
  co-clone's class by testing polymorphism closure (a real logged `condition_check`, not a hand flag) + a
  faithfulness gate (a non-trivial tractable witness must not be 0-/1-valid). `dev/build_census.py` →
  **`results/census/census.jsonl`** (7 co-clone rows: affine/xor-sat, Horn, dual-Horn, bijunctive/2-SAT, +
  3 NP-hard anchors; **4 distinct charge profiles**). `derived`: decision, counting, approximation,
  parallelization, localization; `open`: parameterized, proof_size, average_case, landscape. **Validates clean
  through the shared kernel** with FOUNDRY_SPEC; **P1 NPI calibration passes** (zero NPI rows — Schaefer
  dichotomy); affine is the distinct deceptive-terrain control (P decision, FP counting, yet inapprox +
  unbounded-width). 16 foundry tests (test the dichotomy *rules*, not verdicts). **v1 = the distinct-profile
  spine; finer/0-1-valid/chain co-clones are a documented v1.1 extension. Next (post-defense): N2 analysis
  (predictions 1-2 on the census) + N3-N5.**

## 0.1.1 (unreleased) — Sprint 2.1 (Marx parameterized oracle)

- **The `parameterized` column is filled by the Marx dichotomy (was `open`).** Verified the Exact-Ones (CSP by
  solution size) dichotomy from the primary source — Marx, Comput. Complexity 14 (2005); weak-separability
  definition + W[1] membership from **Bulatov–Marx, SICOMP 43 (2014) / arXiv:1206.4854**: **Exact-Ones CSP(Γ) is
  FPT iff Γ is weakly separable, else W[1]-complete** (a complete dichotomy over all Boolean Γ; W[1]-membership
  even when decision is NP-complete). `postlattice.is_weakly_separable` implements the verified **union +
  difference** criterion (faithful on 0-valid relations). **Key R20 subtlety:** weak separability *implies*
  0-validity, and the CKZ representatives trade 0-validity away for the Max/decision charges, so a naive
  per-relation check misfires (affine's `x⊕y=1` is not 0-valid, yet affine *is* weakly separable) — the oracle
  keys the verdict on the **Schaefer class**, like counting. Result: **xor-sat (affine) → FPT; every other
  co-clone → W[1]** (Horn/dual-Horn/bijunctive each contain implication `x→y`, which fails the difference
  condition; NP-hard a fortiori). All 7 rows re-validate through the shared kernel (gate 5 perspective + gate 6b
  side==value); **4 distinct profiles unchanged**; P1 still passes. 18 foundry tests (+2: the Marx oracle rule
  + the WS definition on hand-checked relations). **Next: Sprint 2.2 — the N3 general-domain tier (K1 timebox).**

## 0.1.2 (unreleased) — Sprint 2.2 (N3 general-domain tier) + Sprint 3 (P2/P3 verdicts)

- **Sprint 2.2 — the N3 general-domain (|D|=3) tier (`domain3.py`).** Post's lattice is Boolean-only, so this
  tier is a CURATED set of textbook-certain domain-3 languages, each **re-verified by the polymorphism
  machinery** (the closure operators generalize Boolean→any domain). Only the charges whose dichotomy is
  *verified general-domain* are filled (R20): **decision** — Bulatov 2017 (FOCS) / Zhuk 2020 (JACM 67), CSP(Γ) ∈
  P iff Γ has a WNU polymorphism, else NP-complete; and **localization** — Barto–Kozik 2014 (general), bounded
  width iff WNU of all arities (affine is Maltsev-tractable but **unbounded** — the |D|=3 analogue of Boolean
  XOR). The Boolean dichotomies (Creignou–Hermann / KSTW / Marx) do **not** transfer → counting / approximation /
  parameterized stay `open` for domain-3 (honest). **R20 caught a real error mid-build:** a naïve "betweenness"
  encoding over the fixed 3-element domain was majority-closed (tractable), so the polymorphism test *refused*
  the NP-complete label — replaced with a second affine language. Census grows to **13 rows (7 Boolean + 6
  domain-3), 7 distinct profiles**; validates clean; P1 still passes. **K1 did not fire.**
- **Sprint 3 — the canon-vs-computation verdicts** ([`docs/findings/Sprint3-P2-P3-verdicts.md`](docs/findings/Sprint3-P2-P3-verdicts.md),
  `census_analysis.json`). Built from the already-spec-threaded eightfold primitives (`crucible._null_chain` /
  `_both_real_v`, `eightfold.factors`) under FOUNDRY_SPEC — **no eightfold modification**. **3.1 noise floor:**
  both tiers deterministic → generations-exempt; the sampled explorer drifts ≤0.083, so the census verdicts are
  exact. **3.2 P2 → INSUFFICIENT RESOLUTION:** the both-real approx|param table is 7 rows, **6 identical** — it
  cannot test the gradient. Corrected permutation **p=1/7≈0.143** (non-significant), after a **bug** that had
  permuted parameterized among all non-`n.a.` cells (injecting the 6 domain-3 `open` values) and reported an
  arithmetically-impossible 0.0002; a **selftest now reproduces 1/7 and 1/3 exactly**. The direction-reversal
  (affine/XOR decoupling: inapprox+FPT) is a **descriptive one-row observation** + a single pre-registered
  hypothesis for the scaled census (**`prereg_v3` H_P2_scaled**: positive / reversed / stratified). The earlier
  "roster sociology" reading is **STRUCK** — it contradicts Crucible **S5** (roster exhausted with every known
  violator; the gradient survived at p=0.0001; a 7-row anecdote cannot reinstate it). **3.3 P3 → DIVERGENT
  (directional at n=13):** the identical Factors estimator reads census **k\*=3** (interval [3,4,5]) vs the
  canon's k\*=1 — but the caveat **is** the finding: the census's charges are theorem-coupled (the dichotomies
  derive them from one another) while the canon's are empirically sourced, so divergence was structurally likely
  regardless of what hardness is; k\*=3 is the census re-expressing its own entailment. Meaningful only after
  R25-netting + a finer Boolean tier. **No banked verdict argued back;** the correction removes a broken number
  and an unsupported claim. 25 foundry tests. **Next: N4 (Sprint 4); the scaled census where P2/P3 become real.**

## 0.1.3 (unreleased) — Sprint 3.5 (census enrichment): finer Boolean tier + H_P2_scaled

- **Floor locked + domain-3 oracle memo** ([`docs/findings/Sprint3.5-enrichment-memo.md`](docs/findings/Sprint3.5-enrichment-memo.md)).
  The H_P2_scaled go/no-go floor (≥15 both-real approx|param rows, ≥4 distinct pairs) was committed **before** any
  enriched-census numbers existed. Domain-3 counting/approximation/parameterized investigation (R20, primary
  statements) → verdicts later refined by a verbatim source pin (Thapper–Živný approximation IMPLEMENTABLE via a
  binary symmetric fractional polymorphism / semilattice-sufficient; #CSP counting = Mal'tsev-necessity partial;
  Bulatov–Marx parameterized IMPLEMENTABLE-heavy via Thm 4.1).
- **Session 1 — finer Boolean tier (`finer.py`) clears the floor.** `classify_boolean` computes every charge from
  a language's polymorphisms + the verified theorems (Schaefer / KSTW+Håstad / Creignou–Hermann / Marx /
  Barto–Kozik); 0-/1-valid languages get **approximation = PO** (all-0/all-1 maximise Max) and a **computable**
  parameterized value (Marx weak-separability is faithful on 0-valid relations). Census → **21 rows (7 N1 + 8
  finer + 6 domain-3), 10 distinct profiles**; validates clean; P1 holds. Both-real = **15 rows / 4 distinct
  pairs → floor MET** (adds the (PO,FPT) and (PO,W[1]) pairs).
- **H_P2_scaled → STRATIFIED** ([`docs/findings/Sprint3.5-results.md`](docs/findings/Sprint3.5-results.md)). On the
  3×2 contingency: V=0.526, corrected permutation p=0.049, rank-corr=0.152; param-hardness by approx level is
  non-monotone (PO 0.5, APX-complete 1.0, inapprox 0.0). The approx|param relationship is **not** a monotone
  gradient (positive or reversed) but **stratified by the algebra** (parameterized tracks affine-ness; approx
  tracks 0/1-validity) — and it is entirely **R25 theorem-forced**. Honest caveats: p is marginal (0.049) and
  composition-sensitive; the Boolean lattice caps distinct pairs at 4. The canon's empirical positive gradient
  does **not** reproduce as a monotone gradient in the theorem-world; same message as P3 (still k\*=3 DIVERGENT
  at n=21). 29 foundry tests.
- **Domain-3 oracles implemented (the memo's "implement everything implementable").** Verbatim-source pin
  (`domain3.py`): **approximation** — Thapper–Živný (PO iff constant-valid or 2-semilattice → BLP; *majority is
  not sufficient*, the Max-Cut trap) → lin-eq-Z₃/order/median/lin-eq-Z₃-b = PO, 3-coloring/NAE = open
  (UGC-conditional); **counting** — NP-complete decision ⟹ #P-complete → 3-coloring/NAE = #P-complete,
  tractable = open (strong balance not built); **parameterized** — Bulatov–Marx Thm 4.1 IMPLEMENTABLE-heavy,
  left `open` rather than risk a rushed wrong build (R20). Census re-validates (21 rows, P1 holds); does not
  change H_P2_scaled (domain-3 still lacks parameterized → not both-real). 30 foundry tests. **Next: R25-net the
  census (P2/P3 residuals); the Thm-4.1 parameterized oracle as a dedicated build; Sprint 4 (N4 instruments).**
