# Eightfold v1.1 — Crucible Spec (Adversarial Self-Review)

<!-- In-repo canonical copy of ~/Downloads/eightfold-v1-1-crucible-spec.md. Build plan (V1–V4 execution,
     the `derived` status, owner riders A/B) tracked separately; this file is the frozen spec of record. -->

**Codename:** Crucible
**Status:** Draft for review
**Owner:** Vishnu
**Relation:** hardening pass on Eightfold v1's A3/A4 findings before any external motion. The five known referee attacks are run by us, under prereg, before anyone else runs them. Every outcome is banked: SURVIVES hardens the claim, RESIZED amends A4 honestly. Nothing ships to arXiv or a venue until V4's verdict exists.

---

## 1. Objective and verdict structure

**Objective.** Subject the three load-bearing v1 claims — H1 multi-dimensionality, the approx⟷param gradient, and the multiplet amplifications — to the five strongest attacks a referee would mount, with pass/resize criteria locked in prereg_v6 before any run.

Per attack, a pre-registered boolean verdict:

| Attack | Claim at risk | SURVIVES iff |
|---|---|---|
| S1 null model (typing objection) | H1 + gradient | real atlas statistics fall outside the 95% envelope of type-respecting nulls |
| S2 dedup (row independence) | gradient + multiplets | claims hold on the deduplicated roster (direction and significance, not exact magnitudes) |
| S3 significance (no p-values) | headline associations + dims | permutation p < 0.05 for the gradient; bootstrap stability for dims (≥3 in ≥95% of resamples) and multiplet amplification |
| S4 anchor growth (n=19 block) | H1's honest anchor | complete-case block reaches n ≥ 35 and still reads ≥3 dims (phased; see §6) |
| S5 adversarial roster (sociology) | gradient | gradient persists (weakened allowed, direction intact, p < 0.05) after deliberate violator additions |

**No kill criterion in the usual sense.** A validation project's honest failure mode is not stopping — it's resizing. The binding rule instead: whatever the verdicts, the amended A4 (and any preprint) states them; a RESIZED verdict may not be argued back to SURVIVES in prose.

## 2. Scope

| In scope | Out of scope |
|---|---|
| S1–S3, S5 on the frozen 118-row atlas (plus S5's additions) | New charges; v2 roster work; Move Two |
| S4 phase 1: dichotomy-umbrella `derived` backfill investigation | Full counting backfill; new proofs |
| Amended A4 + verdict appendix | Venue-specific paper shaping |

## 3. Design

### 3.1 S1 — the null model (the load-bearing attack)

Generate M = 1000 synthetic atlases that preserve everything definitional and destroy everything empirical:

- Preserve per-row applicability structure exactly (which cells are n.a. — the R1 typing).
- Preserve per-charge marginal value distributions (same count of NPC, APX-complete, FPT, open, etc. per column).
- Enforce the entailment layer: any shuffle producing a theorem-forbidden combination is rejected/resampled (E1, E2, with preconditions).
- Otherwise: values permuted across rows independently per charge.

Statistics per null: effective dims (full-table and complete-case), approx⟷param Cramér's V (both-real subset), multiplet amplification for the two canonical witness pairs. The claim survives if the real values sit outside the null 95% envelope. This quantifies §5 of A4: structure in excess of typing, with a number.

### 3.2 S2 — reduction-equivalence dedup

Equivalence rule, locked in prereg before classification: two rows merge iff related by complementation or trivial re-encoding of the same combinatorial object (clique/independent-set/vertex-cover → one class; planar variants stay separate — restriction changes charges, which is the point of the planar trio; SAT variants stay separate — different constraint languages are different problems). The classification of all 118 rows into classes is itself committed before the rerun. Battery reruns on one representative per class (representative = the row with fewest open cells); both readings reported side by side.

### 3.3 S3 — significance and stability

- Permutation test: shuffle the parameterized column across rows (within applicable cells), recompute the both-real approx⟷param V; 10,000 permutations; report p.
- Same procedure for any association the amended writeup calls surprising.
- Bootstrap: resample rows with replacement (1,000 resamples); report distribution of complete-case dims, and of the two witness amplification deltas.

### 3.4 S5 — adversarial roster probe

A pre-registered attempt to break the gradient by construction: literature hunt for genuine violators — problems that are constant-factor approximable yet W[1]-hard for the standard parameter, and problems inapproximable yet FPT. (Note: capacitated-vertex-cover already in the atlas is a candidate violator — APX-membership with W[1]-hardness; the hunt starts by auditing existing rows for violators the gradient survived, then adds new ones chosen solely for violation potential.) **Uncapped by decision:** the hunt exhausts the known violators of the FPT-approximation literature (Marx's survey and successors) rather than stopping at a quota — the sociological defense is strongest when the roster provably contains every violator the field knows. Each addition still meets the full R20 citation standard; the exhaustiveness claim is scoped as "violators identifiable from the surveyed literature," logged with the search trail. Prediction committed in prereg_v6 before the hunt: the gradient weakens but persists (direction intact, p < 0.05 post-addition). If violators are abundant and the gradient dissolves, that is the finding — the gradient was roster sociology — and A4 resizes accordingly.

### 3.5 S4 — anchor growth (phase 1 only in this box)

Investigation-grade: check the 49 folklore-open counting cells and other complete-case-blocking opens against the counting-CSP dichotomy (Bulatov; Dyer–Richerby), Dyer–Greenhill homomorphism counting, and Holant umbrellas. Cells fillable as `derived` (dichotomy citation + logged condition-check, per the R9-adjacent status) get filled; target complete-case n ≥ 35, then rerun the anchor MCA. If umbrella coverage can't reach 35, report how far it got — partial growth still tightens the anchor. Full per-problem proof work stays out of scope (the theorem-factory queue).

## 4. Milestones and done-gates

| M | Deliverable | Done-gate |
|---|---|---|
| V1 | prereg_v6 (all S1–S5 criteria, dedup classification, S5 prediction) + null-model harness | Harness validates on a toy atlas with known planted structure (detects it) and a pure-null toy (doesn't); prereg committed before any real-data run |
| V2 | S1–S3 runs + verdicts | Three booleans resolved per §1 rules; machine output committed |
| V3 | S5 hunt + rerun + verdict; S4 phase-1 fills + anchor rerun | Verdicts resolved; violator provenance cited per R20 standard |
| V4 | Amended A4 + verdict appendix ("Crucible results") | Every verdict stated; any RESIZED claim rewritten at its new size; ledger line included |

## 5. Investigation items

- **I1.** Constrained-permutation sampling for S1: rejection sampling may be slow under E1/E2 constraints at 1000 nulls — check feasibility; fall back to per-charge swap-chains (MCMC over valid tables) if rejection rates are pathological.
- **I2.** S5 violator candidates: audit existing rows first (capacitated-VC, densest-k-subgraph's poly-APX × W[1]?, group-steiner log-APX × ?); then targeted search of the FPT-approximation literature (Marx's survey and successors) for canonical approximable-but-W-hard specimens.
- **I3.** Whether the S2 dedup classification has any genuinely ambiguous pairs (permanent/planar-matching-count? matching/permanent?) — resolve and lock before V1 closes.

## 6. Sizing

| Phase | Est. hours (paired) |
|---|---|
| V1 (prereg + null harness) | 4 |
| V2 (S1–S3) | 4–5 |
| V3 (S5 uncapped hunt + S4 phase 1) | 7–9 |
| V4 (amended writeup) | 2 |
| **Total** | **17–20 h** |

Two weekend blocks. $0 compute (numpy on a laptop; 1000 nulls × the battery is minutes).

## 7. Placement and sequencing

Hobby bucket, subordinate to praxis (defense Oct 2026). Hard rule inherited from the objective: no arXiv, no note, no submission until V4 exists — convince ourselves first. Census C3 chase remains step zero of any session (unrelated dependency, one hour). If the two weekend blocks aren't available before September, Crucible waits; the finding doesn't decay, and an unhardened claim ships nowhere in the meantime.
