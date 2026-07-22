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
