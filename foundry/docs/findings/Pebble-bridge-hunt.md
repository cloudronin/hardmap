# Sprint 6 "Pebble" — bridge hunt (P6, before any novelty language)

**Dated search trail, 2026-07-22.** Standing rule: bridge hunt completes before a word of novelty language is drafted,
because the temptation to shade a sentence is strongest while writing it. Timeboxed; searched in the literature's own
vocabulary (reconstruction, point-to-set correlation, spatial mixing, Gibbs uniqueness, cavity correlation length,
clustering α_d). Verdict up front: **the physics is entirely literature-owned; the contribution is the instrument
and the census measurement, not the object.**

## The question

Is (a) the quantity the point-to-set instrument measures, and (b) the specific finding "point-to-set reach on the
Boolean census tracks the Schaefer/algebraic dichotomy (affine long / bounded-width short), with a minority
relation-level residue" — already named in the literature?

## Search trail

1. **Query:** "reconstruction threshold point-to-set correlation Schaefer dichotomy affine bounded width CSP solution
   geometry." **Found:** Schaefer's dichotomy (affine / bounded-width / … tractable classes); "bounded width captures
   local consistency"; a *topological* version of Schaefer (affine ⇒ solution space is a disjoint union of faces;
   projection-universal iff NP-complete). **No** hit combining reconstruction/point-to-set with the Schaefer split.
2. **Query:** "reconstruction problem parity check XOR-SAT linear boolean long-range correlation cavity spatial mixing
   2-SAT Gibbs uniqueness." **Found:** reconstruction-on-trees; XOR-SAT = linear systems over GF(2), in P by Gaussian
   elimination; **"solutions within a cluster impose long-range correlations"**; **"clustering and reconstruction
   thresholds coincide"** (MRT); **reconstruction ⟺ extremality of the infinite-volume Gibbs measure (free boundary)**.

## What is literature-owned (cite, never claim)

- **Point-to-set correlation length / reconstruction / clustering α_d** — Montanari–Semerjian (cond-mat/0603018),
  Montanari–Restrepo–Tetali "Reconstruction and Clustering in Random CSPs" (arXiv:0904.2751, α_d = α_r),
  Krzakała–Montanari–Ricci-Tersenghi–Semerjian–Zdeborová (cond-mat/0612365). All pinned in the I-SP memo.
- **Reach as point-to-set, not point-to-point** — Montanari–Semerjian's own conundrum resolution (the flaw that
  disqualified `corr`). Owned.
- **Affine/XOR = long-range correlated clusters** — XOR-SAT as linear systems; long-range correlation within clusters.
  The *long* end of our dichotomy is the literature's.
- **Bounded-width = local consistency = short reach** — bounded width ⟺ local consistency decides (Barto–Kozik);
  reconstruction ⟺ Gibbs extremality / spatial mixing. The *short* end is the literature's, by implication (local
  consistency ⇒ no long-range dependence ⇒ short point-to-set length).

## What is the sprint's contribution (measurement, not physics)

- A **built and qualified instrument** (`pointset.py`: boundary-shell bucketing) that measures the literature's
  point-to-set correlation length **on the synthetic census**, with a hand-count-anchored calibration.
- A **measurement**: that point-to-set reach on the Boolean census **tracks the Schaefer split** (affine long /
  bounded-width short), strengthens with n (not finite-size), carries a **minority relation-level residue** (ratio
  0.45), and is **terrain-relevant** (P4). The two ENDS are literature-predicted; the *census-wide measurement of the
  split with the residue quantified* is what is new here — and even that is a measurement of an owned quantity, framed
  as such.
- **No novelty language** for the phenomenon: the writeup says "we measured [the reconstruction / point-to-set
  correlation length] and found it tracks Schaefer on our census," never "we discovered that reach is dichotomous."

## Consequence for the writeup

Every physics sentence carries a citation to the owned object; the instrument and the census measurement are the
foreground; the dichotomy-tracks-Schaefer observation is stated as a measured corroboration of what the algebra + the
cavity picture jointly predict, with the residue as the one quantitative addition. The topological-Schaefer result
(affine ⇒ disjoint faces) is noted as the geometric cousin of the long-reach reading.

## Sources
- [Reconstruction and Clustering in Random CSPs (MRT, arXiv:0904.2751)](https://arxiv.org/pdf/0904.2751)
- [XOR-SAT (Wikipedia)](https://en.wikipedia.org/wiki/XOR-SAT)
- [A Topological Version of Schaefer's Dichotomy Theorem (arXiv:2307.03446)](https://arxiv.org/pdf/2307.03446)
- (I-SP-pinned, primary) Montanari–Semerjian cond-mat/0603018; KMRSZ cond-mat/0612365.
