# Arm B — the natural-side bridge: one charge moves, three do not

**Date:** 2026-07-25. Mosaic v3 G3, prereg_v12 B1 under the full contamination protocol. Population: the
345-row natural atlas (Anatomy coordinates → *cited* charges). Folds group by `problem_family`; nulls are
fold-weighted (train-fold mode → test fold). Predictions hashed before scoring. Nothing rescores.

**Why this arm is the main event:** Arm A established that the Boolean universe cannot test the bridge —
there the dichotomy theorems *are* the bridge. The empirical question lives here, where charges are **cited
facts about the literature** rather than computed functions of structure.

## Result

| charge | n | fold-weighted null | with locality | lift | without locality | lift | channel-2 dependence |
|---|---|---|---|---|---|---|---|
| **decision** | 336 | 0.5923 | **0.6607** | **+0.0684** | 0.6250 | +0.0327 | +0.0357 |
| approximation | 154 | 0.4221 | 0.4286 | +0.0065 | 0.4026 | −0.0195 | +0.0260 |
| counting | 51 | 0.8627 | 0.8627 | 0.0000 | 0.8627 | 0.0000 | 0.0000 |
| parameterized | 129 | 0.6434 | 0.5969 | **−0.0465** | 0.5659 | −0.0775 | +0.0310 |
| average_case | 24 | — | *skipped, n < 40* | | | | |

**`decision` is the single charge that moves**, and it survives a within-fold label permutation null:
observed 0.6607, **p = 0.0033** at N = 300, passing Bonferroni (α = 0.0125 for four charges).

**`counting` collapsed exactly to the modal baseline** (lift 0.0000) — the tree found no split worth making
at n = 51. **`parameterized` is below its null**, and `approximation` is at it.

## Channel 2, measured rather than assumed

The blind coders received `problem_name`, so `locality_class` could encode charge knowledge. Every charge
was scored with and without it. **Dependence is small and consistent: +0.026 to +0.036.** It never rescues a
charge from below-null to above-null, and `decision` clears its null at **+0.0327 even with locality removed
entirely**. So the name-knowledge channel is *live but minor*, and the one positive result does not rest on
it. That is the measurement the protocol demanded; had it come out the other way, the leak would have been
the finding.

## What the result is, stated at its real size

**Anatomy coordinates predict the decision charge modestly and nothing else.** This is not the bridge
landing. Three readings are live and this run does not separate them:

1. `decision` is the **coarsest** charge (P / NPC / harder). A lift there may reflect broad family-level
   regularity — "graph problems tend to be NP-complete" — rather than structural anatomy. Folds group by
   `problem_family`, which controls some of this, but `encoding_type` correlates with family by construction.
2. The three charges that *don't* move are the ones with finer vocabularies (approximation 7 rungs,
   parameterized 5). Finer targets at smaller n are simply harder, and n = 51–154 is thin.
3. A genuine but weak bridge would look exactly like this too.

**Arm A constrains the interpretation, and this is what that calibration buys:** since closure structure
leaves *no* surface fingerprint on the Boolean side, whatever `decision` accuracy is coming from, **it is
not hidden algebra-recovery.** It is family-level regularity, citation-era structure, or a real weak bridge —
and separating those is the next question, not this one's answer.

## Honest limits

- One model family (depth-≤5 CART), one feature encoding, no tuning. Absolute accuracy is not the claim.
- `average_case` skipped at n = 24; `counting` at n = 51 is thin enough that its exact-zero lift means "no
  split was found", not "structure is irrelevant".
- The prospective registry (prereg_v12 G1 addendum) exists precisely because this retrospective result
  cannot settle the contamination question by construction. **0/57 toward its pinned floor.**

## Two bugs caught before this was reported, both mine

1. **Hash-encoded categoricals.** Categories were mapped by `abs(hash(v)) % 997` and fed to a
   threshold-splitting CART — imposing an **arbitrary total order** on unordered categories, so splits fell
   on noise. Fixed to one-hot. **The fix changed the answer**: `decision` moved from +0.009 to +0.068.
   Reporting the first run would have been reporting the bug.
2. **Non-reproducible encoding.** Python's string hash is randomised per process — the same value coded to
   592 / 475 / 278 across three runs. The seed discipline was broken *at the encoder*, so that result could
   never have been re-derived. The fixed run is byte-identical across two different `PYTHONHASHSEED` values.
