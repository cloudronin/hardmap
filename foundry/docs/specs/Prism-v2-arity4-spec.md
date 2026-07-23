# Prism v2 — arity-≤4 anti-canon replication (localization arm dropped)

**Codename:** Prism v2
**Status:** SEALED (`prereg_v33`, this commit), **run deferred behind the preprint** (owner ruling 2026-07-23).
Supersedes the banked `Absorption-arity4-spec.md`.
**Owner:** Vishnu
**Relation:** successor to Prism v1 (`Prism-v1-findings.md`, prereg_v32) and Lattice v3. Drafted by the owner to carry
v1's two unresolved questions to arity 4; **re-scoped at review** — one of the two questions is provably confounded and
comes out of the seal, leaving a single sealed prize.

---

## 1. The re-scope, in one paragraph

Prism v2 was drafted with two headline arms: (a) the **I6 localization-absorption** test (untestable at arity ≤3
because bounded-width ⟺ tractability there), and (b) **replication of the anti-canon Min-Ones residual** (v1 post-hoc:
netted V 0.459, Spearman −0.428). Review established that arm (a) **does not become testable at arity 4** — it trades
v1's degeneracy for an *affine confound* (below) — and is provable from theorems already on the table, so measuring it
would fail the program's "don't measure what you can prove" standard. **Owner ruling (Option 1):** drop the localization
arm (preds 3 & 4) from the seal; **pred 5 (anti-canon replication) is the headline**; preds 1 & 6 stay as gates; pred 2
is demoted to a descriptive marginal. Prism v2 is now a lean, single-prize project.

## 2. Why the localization arm is confounded (the dropped-arm argument)

In the Boolean single-relation domain, **unbounded-width-tractable = purely-affine** (Schaefer: the tractable classes
are exactly Horn / dual-Horn / bijunctive / affine, and bounded width = tractable minus purely-affine). NP-hard
relations are param-open (v1 marginal: 7 unbounded-width = 7 NP-complete = 7 param-open), so among **param-real** rows
the only unbounded-width relations are purely-affine — which are param-**FPT** (affine ⟹ weakly-separable ⟹ FPT) and
which the affine bridge **nets out**. Therefore:

- conditioning the **bridge-completed** residual on bounded-width = conditioning on a **constant** (one stratum,
  UNTESTABLE — v1's degeneracy relocated), and
- conditioning the **raw** residual on bounded-width = **re-deriving the affine netting** (non-independent).

Arity 4 removes the marginal degeneracy (bounded-width now varies) but replaces it with an affine confound. **Sharpened
I6 statement (banked, spec nothing):** localization absorption is unaskable in the Boolean single-relation domain at
*any* arity; the smallest well-posed home is **domain ≥3** (Mal'tsev-but-not-bounded-width languages exist, so
bounded-width and affine separate), but the Sprint 3.5 flag that the domain-3 approximation charge may be thin/absent
means that needs its own I-phase before it is worth committing. No domain-3 spec authorized here (queue inflation).

## 3. What the code review found (against the live code, two Explore agents)

| Item | Verdict |
|---|---|
| Sizing ("$0, minutes") | **CORRECT.** `is_weakly_separable_general` is O(\|R\|³·n) over the relation's ≤16 tuples → seconds across 4074 classes; roster canonicalization (65 534 rels × 4! perms) dominates, still seconds-to-low-minutes. `Absorption-arity4-spec.md`'s 4 h timebox + sampled fallback was over-specced — **retired.** |
| Oracles arity-general | **CONFIRMED.** `build_roster(4)`, all four `postlattice` predicates, both `objective_oracles` dispatchers, the `prism_matrix` netting/CI machinery run unchanged; only `build_roster(3)→(4)` and stale arity-3 comments/gates need touching. |
| Symmetry group | **permutation-only S_n** (`canonical`, `prism.py:32`). The draft's "± complementation" is a **defect**: complementation swaps horn↔dual-horn, 0-valid↔1-valid, **Max-Ones↔Min-Ones** — it would fold the Min-Ones headline into Max-Ones. Class count = 3984 (arity 4) + 90 (arity ≤3) = **4074**. |
| `bounded_width` predicate | **CORRECT (interim "bug" flag retracted).** A 0/1-valid single relation has a *constant* polymorphism ⟹ trivially bounded width; even-parity-4 correctly bounded, odd-parity-4 (purely affine) correctly unbounded. Matches v1 §2's "smallest witness arity 4." Verified by enumeration. **No predicate change.** |

## 4. Sealed predictions (`prereg_v33`)

1. **Reproduction gate (known-answer):** arity-≤3 subset (`build_roster(3)`'s 90 classes) reproduces v1's approx⟷param
   raw V = **0.256** and empty NPI row. Violation ⇒ HALT.
2. **Bounded-width marginal — descriptive, not a bet:** on the *existing* predicate; arity-4 tractable-unbounded classes
   are the **purely-affine** ones (odd-parity-4 = `x₁⊕x₂⊕x₃⊕x₄=1` and its S₄-orbit; even-parity-4 bounded via its
   constant polymorphism). Descriptive only — **not** a gate for the dropped 3/4.
3–4. **DROPPED from the seal** (provably confounded; §2). Recorded, not scored.
5. **Anti-canon replication — THE headline:** the Min-Ones **bridge-completed non-affine** residual is anti-canon —
   netted Spearman **< 0**, bootstrap CI (sized to symmetry classes) **excluding 0**. Max-Ones and Min-Ones reported
   **separately** before any pooled number. **Three-outcome scoring:** REPLICATES (CI < 0) / REFUTED (CI > 0, or on 0
   with −0.428 excluded) / **INSUFFICIENT RESOLUTION** (CI includes *both* 0 and −0.428 → declared on interval width,
   **not** a miss).
6. **Outlier persistence (gate):** approx⟷param stays the largest bridge-completed netted residual — pinned to the
   **pooled** (166-row analog) number, with per-objective maxima alongside.

Standing rules: marginals before any V; CIs sized to the 4074 classes, never raw relations; per-pair shared-input
netting **with the affine⟹WS⟹FPT bridge from the start**; both residual sets paired; affine traced; per-objective
before pooled; no metric substituted after results.

## 5. Design (reuse; the only new engineering is two drivers)

- **Roster:** `prism.build_roster(4)` — arity-general already (`prism.py:24-46,116-121`); arity ≤4 = 4074 S₄-classes.
- **Drivers (new):** `dev/prism_v2_build.py`, `dev/prism_v2_matrix.py` — clones of the v1 drivers with `build_roster(4)`,
  the reproduction gate on the arity-≤3 sub-roster, pred 2 marginal, pred 5 (reuse `prism_direction_check.py` Spearman +
  a class-resampled bootstrap CI), pred 6 pooled. Refresh stale arity-3 strings.
- **Tests:** `tests/test_prism_v2.py` — repro gate; known-answer rows (odd-parity-4 → unbounded/affine/FPT, even-parity-4
  → bounded; VC/IS opposite corners); netting identity + affine bridge at arity 4; pred-5 sign. `test_prism.py` (arity 3)
  stays green untouched.

## 6. Milestones (on execution, post-preprint)

| M | Deliverable | Done-gate |
|---|---|---|
| Q0 | `prereg_v33` (sealed this commit) | group = S_n; sealed before any arity-4 column ✓ |
| Q1 | Roster + reproduction gate | dedup selftest green; arity-≤3 subset reproduces 0.256 or HALT |
| Q2 | Columns + marginals | NPI passes; pred 2 marginal persisted per objective; purely-affine unbounded classes enumerated |
| Q3 | Matrix + netting | both residual sets; pred 6 scored; derivations logged |
| Q4 | Anti-canon direction | **pred 5 scored** (Min-Ones netted Spearman + class-sized CI), per objective before pooled |
| Q5 | Findings + ledger | preds 1,2,5,6 scored incl. misses; dropped-arm reasoning + sharpened I6 statement as findings-implications |

## 7. Placement

**Seal now, run after the preprint.** Sealed at this commit: this spec, `prereg_v33`, the `Absorption-arity4-spec.md`
supersession, spec-defect #5 in the methods thread. The run waits — the preprint is unambiguously next. Hobby bucket,
$0 compute, generated roster, no curation contact. Outcome map: REPLICATES → v1's post-hoc −0.428 becomes the program's
second hardened finding and amends the preprint's decomposition section; REFUTED → the anti-canon number was
arity-≤3-specific, stated as such; INSUFFICIENT RESOLUTION → declared on interval width. Nothing decays by waiting.
