# Changelog — foundry

## 0.1.0 (unreleased) — N0 scaffold

- **The four rulings of the wave-3 sitting, and the slate goes to four.** **Ruling 1:** `3-partition`
  and `MCSP` recorded as **variant frames** — frames frozen and unedited, `encoding_faithful: false` at
  descriptor@v6, barred from charge-joining candidates via a new `charge_joinable_catalog` view (the
  charge attaches to the canonical object, so the join is where a proxy encoding would poison things);
  co-movement unaffected since the variant is internally consistent. **Ruling 2:** `HELD-path-gated`
  minted, distinct from `HELD-power` — the number-theoretic family's four REACH-subset rows are ALL
  BUILT, so no reservation can ever revive that candidate; it now revives on a build decision, is
  re-reviewed at each capture-path ruling, and closes as `INSUFFICIENT-by-population` if the queue
  completes without one. `family_supply` counts only rows a reservation could actually take — counting
  REACH-assignment rows as supply would have mislabelled the hold as power-gated, which the first run
  did and a fix corrected. **Ruling 3:** lexicon **v2**, full phrase set declared before reading the 86
  misses, every v1 call a self-test FIXED POINT, stopping rule pinned in advance (two mechanical passes,
  then hand adjudication with the encoding quoted). Coverage 32.3% -> **53.5%**, clean queue 16 -> 23.
  **Ruling 4:** `covering-radius` typed out as `deferred-no-ambient-stable-framing` with its candidate
  framing and re-entry route recorded — three batches held is a queue lying about its size. The
  sounding-v1/v2 rounds' exclusion from the catalog is now **recorded as the instrument-comparability
  decision it implicitly was** (tier-0 controls, no ramp structure), with re-capture as the constructive
  route. **Batch 7** ships 3 rows, 3 excluded, frontier 8 -> **10**. **Wave 4 slates FOUR** — the
  candidates that sat one row from adjudication at wave 3. Banked: **Q23**, the association reverses sign
  across families (+0.90 number-theoretic, -0.43 sat-csp, pooled +0.50 a mixture washout) and sat-csp's
  candidate is the one that revives by construction; **Q24**, a lexicon can match a real phrase and still
  get the object wrong. 396 tests, verify 11/11, W2 passes.
- **Batch 6 and wave 3 — the slate opens.** The first roster drawn from the verified-clean queue and
  the first **vetted before hashing** under the new roster protocol: eight vertex- and item-subset rows,
  every ambient fixed by construction, 6 shipped and **0 excluded at birth** — the first batch since
  batch 2 with no exclusions, which is what vetting was supposed to buy. Its reservation took the
  frontier from 6 to **8 clusters**, the size the hold queue had been naming since wave 1.
  **Wave 3 slated one candidate:** Spearman rho(`overlap_ref`, `bimodality_max`) over `number-theoretic`
  trajectories, disclosed **+0.9025** against a frontier MDE of 0.8491, family size 1, Holm 0.05. It is
  the same candidate that topped the hold queue at 0.866 in waves 1 and 2; nothing was tuned to clear it,
  the gap was recorded at wave 1 and the frontier walked to it. Two things flagged for the ruling and not
  resolved: the two descriptors are computed from the same overlap distribution (no identity, so netting
  correctly does not fire, but part of the association may be boundary-induced), and **the frontier
  contains no `number-theoretic` row** — whether that makes the test a stronger out-of-family transfer or
  a weaker different-population test is the owner's call. Four more candidates now sit ONE reserved row
  from adjudication. 393 candidates enumerated, 103 rejected, 289 held. 392 tests, verify 11/11, W2
  passes.
- **Batch 5 — the first CONTRAST-DIAL capture, and three mis-typings.** MCSP re-enters under the
  typing ruled 2026-07-27: two declared alphabet levels {2, 6}, trajectory descriptors reading
  `n.a.-contrast`, and the between-level delta in their place (majority -0.161, minority -0.263, min
  -0.273). The contrast group lands at **descriptor@v5** with its own loader columns; level descriptors
  stand, and a `traj_class` never reaches SQL for a contrast row. The MCSP generator is IMPORTED from the
  pilot that measured it rather than copied — the row whose ramp was amended is built by the same code
  that amended it. **Three of eight rostered rows have no subset region:** `min-sum-set-cover` scores an
  ordering, `cutwidth` a linear layout, `domatic-number` a partition. Recorded as TYPINGS, not build
  failures, and banked as **Q22** — the REACH-subset class holds 127 rows and nothing has re-examined it
  since the census. **A tooling bug found and corrected in daylight:** `conformance_at_birth` hardcoded
  its probe at ramp value 0.30, a density-shaped number, so MCSP's alphabet ramp called `randrange(0)`
  and the pipeline recorded the ROW as failing conformance rather than the probe as wrong — the same
  defect had been silently mis-probing every non-density ramp, including the algebraic rows at 1.2..3.0.
  Fixed to probe at the median declared level of the row's own ramp. The spurious exclusion record
  **stands in the maptrail with a correcting erratum beside it**, because correcting by erratum rather
  than by editing history is the only way a reader can tell a corrected mistake from one that never
  happened. Batch 5 ships 3 rows; catalog 260 -> 282 cells, frames 1234 -> 1322, frontier 4 -> 6 rows —
  two short of wave 1's first adjudicable candidate. 392 tests, verify 11/11, W2 passes.
- **Q21 ruled and executed — and the DERIVED census found twice what the hand list would have.**
  `observatory_ambient_census.py` RUNS every built row's generator across its declared ramp and measures
  the ground-set width, rather than listing the rows someone believes are edge-subset rows. It found
  **6 of 42 confounded, not the 3 predicted** — and corrected one of those three:
  `connectivity-augmentation` is STABLE (its generator caps candidate edges at 13). It caught
  `maximum-planar-subgraph` from batch 1 and **`set-cover` from the frozen v3 survey column**, neither of
  which anyone had flagged. No sealed artifact consumes a shape descriptor, checked before the policy
  landed. **Part 1 — descriptor policy at descriptor@v4:** shape, transition and `overlap_slope` read
  `n.a.-ambient-confounded`; LEVEL descriptors stand, because each step's excess is a valid measurement at
  its own (width, density) against its own matched control. Not the kink precedent: kink values are
  meaningful-but-untested, these are meaningless-as-defined. `overlap_slope` is voided too — the ruling
  named groups, and one surviving confounded slope would be an inconsistency rather than an exception.
  The JSONL keeps the marker so a reader learns why; the **db column goes NULL** so every `IS NOT NULL`
  filter excludes it without knowing the marker exists — a sentinel that reaches a column becomes a data
  value, and would have surfaced as a `traj_class` level in Helm's association candidates.
  **Part 2 — census erratum:** edge-subset rows re-ramp on a within-instance parameter at fixed ground
  set (`graph-spanner` stretch factor, `connectivity-augmentation` connectivity target, `cluster-deletion`
  deletion budget); the two birth-excluded rows stay excluded with the re-entry route named, since an
  exclusion is a typing and any ambient-stable dial falsifies it. **Part 3 —**
  `observatory_recapture_queue.json` queues 4 rows as ordinary build work; the old frames stay frozen,
  annotated via maptrail, never edited and never deleted (the Terrain two-artifact pattern). Two queued
  rows carry **no declared replacement dial** and are listed as such rather than given an invented one.
  28 cells across 4 rows now carry the confound; loader arity is read off the schema rather than typed.
  387 tests, verify 11/11, W2 passes.
- **Batch 4, the second sitting's rulings, and a rule narrowed the day after it shipped.**
  **CONTRAST-DIAL minted** as a third capture mode: a family dial that passes the movement check but
  fails leave-one-out is a threshold, not a ramp, and the row enters as a declared two-level factor with
  trajectory descriptors reading `n.a.-contrast`. MCSP retyped RAMPED -> CONTRAST-DIAL at levels
  |Sigma| in {2, 6} (the representative chosen by the catalog's own median rule, reused not invented) and
  deferred to batch 5, where the contrast-capture path gets built. **Kill 1's trigger amended** to require
  two empty slates ON DISTINCT FRONTIER STATES — the independence condition that made the recorded
  non-fire correct, now in the text. **`ramp-pilot-protocol.md` minted**: four checks a declared family
  dial must survive at first use, with leave-one-out required of every new pilot.
  **The structurally-flat rule was too broad and is narrowed at descriptor@v3.** v2 assumed a
  fixed-cardinality feasible region is the whole k-uniform slice; that holds for `k-center` but not for
  `3sum`, whose region is the triples SUMMING TO ZERO — every member shares a cardinality, so the row
  declares honestly and passes conformance, yet which members qualify is entirely instance-dependent.
  Under v2 that row would have been flagged flat and dropped from Helm's swept population. Caught by
  batch 4's roster before 3sum was built; v3 requires the frames to show the region standing still, and
  `declared_flat_but_moves` preserves the disagreement (8 cells).
  **`ambient_stability` minted** and it excluded two rostered rows at birth: for EDGE-subset rows the
  ground set IS the dial, so `2^w` grows with edge density and a trajectory confounds tightening with a
  growing space (`edge-dominating-set` widths [7, 8, 12], `feedback-arc-set` [7, 11, 12]). Banked as Q21
  — three batch-2 rows have the same shape, their frames untouched and NOT retrofitted.
  Batch 4 ships **4 rows, 2 excluded at birth**; catalog 236 -> 260 cells, frames 1124 -> 1234, frontier
  2 -> 4 rows. Q19 (a dial that moves exactly once is a structural dichotomy at that value), Q20 (which
  other declared dials are secretly thresholds?) and Q21 banked. Two ledger lines: *a ramp is not
  measured until everything but the dial is held fixed*, and *an endpoint comparison is an eyeball claim
  with arithmetic on it*. 382 tests, verify 11/11, W2 passes.
- **The four rulings of 2026-07-27 — executed, and one of them turned into a third case.** **Ruling 1
  (MCSP):** the `string` family's ramp amended by maptrail `erratum` to *alphabet size at fixed string
  length*, with the hardening direction pinned at pilot rather than asserted. The first pilot run
  confounded the dial — it randomised the planted block count per instance, which drives region size far
  harder than the alphabet, producing a non-monotone series and an endpoint comparison that reported a
  direction the data did not support. With the block count held fixed the dial moves (excursion 379 vs
  2x pooled SD 291) and the derived-consequence check confirms upward closure. **But a leave-one-out
  check shows the movement is carried entirely by |Sigma| = 2**: drop that step and the remaining range
  is FLAT under the catalog's own rule. That is a THRESHOLD, not a graded dial — a third case the ruling
  did not name, RAISED FOR RULING. **Ruling 2 (the anomaly null):** `stratified-exchangeability/v1`
  pinned — permutation within the candidate's (family x region-kind x flavour) stratum, r-band as
  matching covariate, floor 20 cells derived from 1/(m+1) <= alpha. The 22 held extremals now clear
  screen 1 and fail on stratum supply instead, with a shrinking gap. **Ratified:** §0.1 over §5, with
  §5's text amended by erratum. **Addition:** `structurally_flat` at descriptor@v2 — 20 cells across 5
  fixed-cardinality rows excluded from the sweep via `sweepable_catalog`. Not cosmetic: removing the
  constants moved optimization's `overlap_ref x r_ref` from 0.843 to 0.810. Catalog bumps to **v2** under
  F4 (no v1 descriptor changed value, but a version that sometimes carries a group stops identifying a
  schema); `build_catalog_v1.py` becomes `build_catalog.py` and derives its output name from the
  extractor. **Wave 2** runs under `sweep/v2` — wave 1 is NOT re-run, its trail being what the engine saw
  before the rulings existed. Slate still empty; nearest candidate still needs 6 more reserved rows.
  Kill 1's condition is now met and is recorded as a **deliberate non-fire** with its reason. Two ledger
  lines minted: *a denominator that omits the questions we knew were bad is a denominator we chose*, and
  *a null for the disclosed statistic is not a null for the sealed bet*. 378 tests, verify 11/11, W2
  passes.
- **Batch 3 + Helm v1 — the frontier exists, and the first wave measures it.** Batch 3 leaves `graph`
  for the first time: six rows across `optimization`, `number-theoretic` and `algebraic`, testing three
  census-declared family ramps that had never been used (two recorded with "precedent: none yet"). All six
  ramps move their regions; 0 excluded at birth. Catalog 188 -> 236 cells, frames 888 -> 1124.
  **The frontier reservation** (`foundry/catalog/reservation.py`, Helm SS5): 25% of every batch declared and
  hashed before capture, by a rule that sees only a batch number and row names. Resolving SS5 against the
  binding SS0.1, reserved rows are **declared and left uncaptured** — the batch script contains no generator
  for them, so it cannot burn the ground it does not know how to build. Enforced in the catalog builder, in
  the loader, and by a guard test that proves it can fail. **Helm v1** (`foundry/helm/`): sweep, four
  mechanical screens, information-per-seal ranking, and `wave_trail.jsonl` emitted at event time (Kill 3
  checked before a wave opens). New loader tables `frontier` `maptrail` `waves` `wave_events` `candidates`,
  with `hold_queue` and `family_ledger` as computed views. **Wave 1 slated nothing**, and the emptiness is
  the result: 344 candidates enumerated, 87 rejected, 257 held, and the nearest adjudicable candidate needs
  **6 more reserved rows** — three more batches. Kill 1's first observation, one wave in; the kill needs two.
  Two screen defects found and fixed mid-build: screen 1 was accepting a null for the *disclosed statistic*
  where a seal needs a null for *the bet*, and 30 candidates were correlating arithmetic with itself
  (`excess_ref <= excess_max` holds by construction) — now rejected under a `netting` rule read off the
  extractor, and still enumerated so the denominator stays honest. **`minimum-common-string-partition`
  raised for ruling:** the `string` family's declared ramp (pattern/text length ratio) has no referent in
  the family's only reachable row, and no substitute was invented. 367 tests, `hardmap verify` 11/11, W2
  passes, frozen bytes intact.
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
  spine; finer/0-1-valid/chain co-clones are a documented v1.1 extension. Next (later phase): N2 analysis
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
  change H_P2_scaled (domain-3 still lacks parameterized → not both-real). 30 foundry tests.
- **Bulatov–Marx Thm 4.1 parameterized oracle BUILT (`paramd3.py`).** The full OCSP FPT/W[1] criterion — the
  nested (D₁,D₂) search with cc-closure, multivalued-morphism value-typing, contractions, closed subsets —
  implemented at |D|=3 and **verified against the Boolean collapse** (must reduce to "FPT iff every relation
  weakly separable" at |D|=2; a 5-case selftest confirms). Domain-3 verdicts: **affine → FPT, else → W[1]** (the
  Boolean Marx shape); flagged implementation-derived (no independent |D|=3 ground truth). Fills the last domain-3
  charge → the 4 tractable domain-3 languages become **both-real**, so **H_P2_scaled runs on 19 rows**: still
  **STRATIFIED**, V=0.472, and **p rises 0.049→0.061 (non-significant)** — the association weakens toward noise as
  real data is added, the honest direction. The theorem-world's approx|param is algebra-stratified, not a
  gradient (positive or reversed); same message as P3 (k\*=3 DIVERGENT). 31 foundry tests; eightfold
  byte-identical. **Next: R25-net the census residuals; Sprint 4 (N4 instruments).**

## 0.1.4 (unreleased) — Sprint 4 Task 0 (R25-netting confirmation)

- **R25-netting confirmed: the oracle-only census nets to exactly zero residual** (`foundry/r25.py`,
  `tests/test_r25.py`; `python -m foundry.cli --r25`). Netting the theorem-forced component out of the P2/P3
  statistics per the standing R25 procedure (`cai_chen_residual_audit`) returns the predicted **zero, three
  independent ways**: (1) **provenance netting** — all 19 both-real rows are theorem-`derived`, so netting
  empties the table (raw approx|param **V = 0.472 → residual V undefined**, `survives = False`, the OPPOSITE of
  the canon); (2) **within-stratum pooled V = 0.0** over 15 polymorphism-profile strata; (3) **residual
  dimensionality = 0** (0 non-`derived` oracle cells; census k\*=3 → 0). This is a **selftest of the netting
  machinery**, not a discovery run — a non-zero residual would STOP the line, and none appeared. The zero is
  given teeth by a **functional-determination** check (same polymorphism profile ⟹ same oracle charges, holding
  across 4 multi-row strata that span the two independent oracle code paths) and a **perspective-aware anchor
  cross-validation** against the real canon atlas: **18/18 perspective-free cells agree** (decision/counting/
  approximation over 6 anchors), while `parameterized` is perspective-divergent (canon treewidth vs census
  Exact-Ones) and `localization` is canon-absent — "cross-validated at the anchors, incomparable elsewhere."
  Findings: `docs/findings/Sprint4-Task0-R25-netting.md`. The oracle-only canon-vs-computation comparison is
  **closed permanently**; all remaining census science runs through the measured instrument columns. 37 foundry
  + 72 eightfold tests green; no oracle cell touched; eightfold byte-identical. **Next: prereg_v4 (I6 lock) +
  the I5 per-family ensemble memo (owner-review checkpoint, before any generation).**

## 0.1.5 (unreleased) — Sprint 4.1 (solution-side landscape instrument + calibration gate)

- **prereg_v4 (I6 lock) + I5 ensemble memo + prereg_v5 (owner riders R-a..R-e).** prereg_v4 locked the I6
  hypothesis + measured-column protocol before any measured cell. The I5 memo (owner-review) surfaced the
  load-bearing finding that the Proof-Census `sampler_s1/s2` are PROOF-space samplers, not solution-space — so
  the `landscape` charge needs a net-new solution-side instrument, applied (per the hybrid split) to the
  decision-P rows, which DECONFOUNDS I6 (9 bounded-P vs 5 affine-P). Owner approved Option C; prereg_v5 amended
  I6: affine is the unbounded-width ARM (not a side-control), two-pole Vega calibration (R-b), two-sampler
  concordance + affine-exact ground truth (R-c), sampled-population provenance (R-d), INSTRUMENT_NOT_QUALIFIED as
  a legal outcome + build kill-box (R-e).
- **Solution-side instrument BUILT + calibrated (`ensemble.py`, `solscape.py`; net-new, pure-Python).** Native
  domain-general random-CSP generator; two structurally-different samplers (`sample_dpll` systematic +
  `sample_walksat` local search) + `sample_affine_exact` (uniform over the GF(p) solution coset — unbiased ground
  truth). Ruggedness = excess mean overlap above the random-agreement baseline (the density sweep showed
  solution-graph fragmentation is a solution-COUNT artifact, discarded). **Two-pole Vega PASSES** (XOR rugged
  0.998 vs Horn smooth 0.829, sep 0.169); samplers concord (max gap 0.037); affine-exact confirms sampler bias
  0.005 (near-zero). **Calibration finding:** bounded-width is NOT a uniform smooth class — ruggedness tracks the
  specific polymorphism (Horn/semilattice smooth 0.83; 2-SAT/majority mid 0.89; order/median 0.93 ≈ affine), so
  I6's binary width predictor is weak (+0.11 direction) while the polymorphism GRADIENT is the genuine measured
  cross-structure. 44 foundry + 72 eightfold tests green; eightfold byte-identical. **Owner-review checkpoint
  (calibration gate, `docs/findings/Sprint4-calibration-gate.md`): 4 decisions before the measurement runs.**

## 0.1.6 (unreleased) — Sprint 4.2/4.5 (measured columns: a clean negative)

- **The measured-column line ends negative, and honestly: complexity factors through the algebraic
  classification; solution geometry does not.** Confirmation run (fresh seeds, prereg_v6/v7, GKMP netting locked
  before the data) initially read H_I6a SUPPORTED (Mann-Whitney p=0.002) and H_I6b CONFIRMED with an apparent
  domain-3 anomaly — but the owner-mandated **domain-confound check** dissolved it: the metric is unbiased (a
  known-smooth |D|=3 pole reads 0.53; the same-relation cross-domain gap collapses 0.40 raw → 0.05 normalized),
  yet ruggedness is **relation-specific** — Boolean implication (bounded-width) is as rugged (0.79) as affine
  while NAND-Horn (also bounded-width) is smooth (0.48). Verdicts (prereg_v8, no rescue): **H_I6a SUPPORTED
  internally / external validity BROKEN** (arm composition drives it, not width); **H_I6b REFUTED as law**;
  **anomaly WITHDRAWN** (order-3's ruggedness is the ≤ relation's, Boolean-visible, inside GKMP's jurisdiction —
  the theory-silent tier emptied itself); **theory-forced tier CONFIRMED** (affine coset dispersion); **instrument
  QUALIFIED**.
- **Sprint 4.5 within-co-clone replication → SCATTER.** Three genuine same-6-flag-profile representatives per
  tractable arity-3 co-clone: affine co-clones cluster (coset-forced, spread 0.002–0.075) but non-affine scatter
  up to **0.327** (pure 0-valid ranges 0.44–0.77). **The census one-representative-per-co-clone roster is valid
  for oracle columns (Task 0 residual=0) and INVALID for measured columns** (F1 §3 amended). Measured columns
  need relation-level sampling — the honest, stronger next move.
- Instrument: `ensemble.py` + `solscape.py` (net-new, pure-Python; two structurally-different samplers +
  affine-exact ground truth). Findings: `docs/findings/Sprint4-results.md`, `Sprint4-confound-check.md`. Evidence:
  `results/landscape/{confirm_v7,confound_check,sprint45_within_coclone}.json`. 44 foundry + 72 eightfold tests
  green; no oracle cell touched; eightfold byte-identical. **Next: relation-level solution-geometry study (gated
  in); Sprints 5–6 (construction + charge-9/Ω⁻) unaffected.**

## 0.1.7 (unreleased) — the clone-invariant impossibility + Sprint 4.6 (resolution decomposition)

- **Structural result: the clone-invariant impossibility.** A co-clone is the set of relations sharing a
  polymorphism clone, so every language-level algebraic invariant (tractability, connectivity, rigidity rank) is
  constant on the co-clone by construction and cannot explain within-co-clone terrain variation. The connectivity
  test (prereg_v9, GKMP OR-free/NAND-free/componentwise-bijunctive) came back **NOT_PREDICTIVE** — one instance of
  the impossibility; framed as worst-case-structural ≠ typical-case-sampled, with the GKMP–Schwerdtfeger
  convergent prior art credited (they built finer relation-level classes because Schaefer can't classify
  geometry). The rigidity-envelope test (prereg_v10) came back **PARTIAL** with a named mechanism: **Maltsev
  (affine) rigidity forces near-zero within-co-clone spread (0.039)** — the theory-grounded reason the affine
  strata are where geometry factors through the algebra.
- **Sprint 4.6 (prereg_v11): the hardness vector at two resolutions.** Expanded roster (arity-3 full + arity-4
  sampled, 77 relations). **A (rigidity middle-rank retest): PARTIAL** — the Sprint-4.5 3≈2 tie resolves into a
  weak ordering in the predicted direction (rank 3 spread 0.274 < rank 2 0.353, corr −0.389); thin-strata, not a
  real absence. **B (relation-level terrain prediction): SUPPORTED** — a relation-level feature predicts terrain
  and beats the marginal baseline **held-out by co-clone** (MSE 0.10 vs 0.23; perm p=0.0002). Carried by
  **tuple_dispersion** (relation tuple-geometry, sealed +, marginal +0.74) — the **sealed density mechanism FAILED**
  (marginal +0.26, opposite the sealed −; the physics density→clustering law does not transpose to relation-
  density). Headline: **complexity is a clone-level property; terrain is a relation-level one** — two components of
  the hardness vector at different resolutions of the same object. `connectivity.py`, `rigidity.py`,
  `relfeatures.py`; findings `Sprint4-connectivity-test.md`, `Sprint4-rigidity-envelope.md`,
  `Sprint4.6-resolution-decomposition.md`. 56 foundry + 72 eightfold tests green; eightfold byte-identical.
  **Next: Sprint 5 program writeup.**
