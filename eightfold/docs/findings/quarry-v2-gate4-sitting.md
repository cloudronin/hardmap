# Quarry v2 Channel-B fills — Gate-4 promotion sitting

**Date:** 2026-07-24  **Gate:** 4 (owner promotion — `confirmed`, `primary_source: true`)  **Authority:**
owner (Vishnu), primary sources read.  **Prereg:** `prereg_v13`.  **Population:** the 22 dual-pass
R20-verified Channel-B parameterized fills.  **Machine-readable outcome:** `quarry-v2-gate4-promotions.jsonl`
(sha `55c9f8d7`).  **Version track:** atlas **v3.1** (next minor) — frozen v3 bytes (`e62f3c28`) untouched;
these cells land at the next minor freeze, this sitting is the Gate-4 event.

> This is the program's **first owner-`confirmed` cohort since v1's 2/332**. Every prior expansion (v3's 420
> cells) froze at agent-`claimed`/double-passed (trust-labels.md). These 21 are read at the primary source by
> the owner — the strong label, not the weak one.

## Outcome: 21 promoted to `confirmed`, 1 retracted to `open`

| verdict | n | cells |
|---|---|---|
| **`confirmed` as they stood** | 19 | the FPT block (minus k-MST's secondary), the W-block (minus disk-cover), the para-NP-hard six |
| **`confirmed` on citation fix** | 2 | **#5** k-minimum-spanning-tree (secondary dropped) · **#19** minimum-sum-of-squares (proven-here) |
| **retracted to `open`** | 1 | **#11** geometric-disk-cover (object-drift; free-placement W[1] not pinned) |

### The three watch-items, resolved at the sitting

- **#5 k-minimum-spanning-tree — `confirmed`, secondary dropped.** The Hassidim–Keller–Lewenstein–Roditty
  (WADS 2013) secondary was min-weight k-**path**, not k-tree — a mislabeled cite is worse than none (the
  exact thing a referee pulls). Dropped, not relabeled. **Alon–Yuster–Zwick color-coding (J. ACM 42(4),
  1995)** carries the FPT value alone.

- **#19 minimum-sum-of-squares — `confirmed`, `proven-here`.** The disposition check found G&J **[SP19]
  MINIMUM SUM OF SQUARES** is a genuine catalog entry that *asserts* NP-completeness (its neighbors
  [SP20]/[SP21] are flagged NP-membership-open; [SP19] carries no such caveat) — but for the **general-K**
  form. Our claim is fixed **m=2** para-NP-hardness, so the F-1-clean warrant is **G&J [SP19] as catalog
  authority + a one-paragraph proven-here Partition reduction** (2 parts, minimize Σ(part-sum)²; optimum
  T²/2 iff a subset sums to T/2 iff PARTITION-yes → NP-hard at m=2 → para-NP-hard by m). Full proof text in
  the promotions sidecar. Chandra–Wong retained as problem-definition reference only. **This is the atlas's
  first original `proven-here` cell — a literature gap filled at full provenance, entered through the front
  door at a Gate-4 sitting.**

- **#11 geometric-disk-cover — RETRACTED to `open`.** The held disk check failed, and vindicated the hold.
  The atlas problem is **free-placement** ("unit disks with free centres"), and its own pre-fill note already
  read *"W[1]-hardness plausible… but not pinned."* Marx ESA 2005 proves **squares** (Thm 5), not disks; the
  correct disk citations (Marx–Pilipczuk 2015 / IWPEC 2006) cover only the **discrete** form. Free-placement
  unit-disk-cover W[1]-hardness is a theorem widely believed and never written — the folklore gap in a
  geometric costume. The value returns to `open` (matching frozen atlas v3). Recorded as **object-drift**
  (methods-thread instance 17).

## Impact on the sealed absorption run — footnote, not rerun (owner ruling)

The absorption verdicts were scored on the 22-fill population as it stood at seal time and **stand as
scored**; the sidecar input is not re-frozen. `#11` was retracted *after* the run, through the designed gate
— the system's normal metabolism, not a defect in the run. **No verdict's arithmetic turns on the one fill,
verified three ways:**

- **3-class power fails with *or* without it:** 7/9 either way (min-exp 3.59 → 3.27; decomposable 21 → 20).
  INSUFFICIENT is unchanged.
- **The 2-class MISS is nowhere near a one-row flip:** point shrinkage −60% → −59%; the sealed bootstrap CI
  is [−1.15, −0.21], wholly negative and far from the +0.5 HIT bar.
- **The split CIs do not move materially at n=110 vs 111:** V(loc,approx) 0.547 → 0.539 (CI [0.451,0.67] →
  [0.449,0.666]); V(loc,param) 0.231 → 0.230 (CI [0.149,0.384] → [0.144,0.387]).

## Version discipline & wall-clock

`confirmed` cells are **atlas-v3.1-track** — the next minor freeze absorbs `quarry-v2-gate4-promotions.jsonl`
(21 cells); frozen v3 stays byte-identical. `geometric-disk-cover` remains `open` in both v3 and v3.1. Sitting
wall-clocked per standing practice; the sealed absorption run (`quarry-v2-fills.jsonl`, 22 rows) is preserved
as the immutable record of the population the verdicts were scored on.
