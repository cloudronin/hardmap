# Sprint 6 "Pebble" — parity diagnostic: ξ-as-built DISQUALIFIED for reach-proper

**Verdict: DISQUALIFIED** (prereg_v20, sealed prediction confirmed). P3 does NOT run in this form. The design fork
(point-to-set instrument vs write-up-as-instrument-development) is an explicit **owner decision**, not a silent
redesign.

## What was tested and why

The I-SP investigation (§4) flagged, from Montanari–Semerjian, that "reach" is formally the **point-to-set**
correlation length, not the **point-to-point** (pairwise) one — and that pure ≥3-ary **parity** is the extreme case:
**zero pairwise correlation, full point-to-set correlation.** Parity is our long pole's family. The P2 calibration
could not catch this because the long pole was **2-affine**, exactly where pairwise and point-to-set coincide
(corr = 0.5, deterministic). Owner ruling escalated the flag to a decisive diagnostic.

## Result (exact coset enumeration, n=16, α=0.6; same-density 2-affine reference)

| family | corr reach_score | per-instance |
|---|---|---|
| **3-XOR (parity)** | **0.026** | 0.01–0.086 |
| **4-XOR (parity)** | **0.030** | 0.00–0.083 |
| 2-affine reference (same density) | **0.500** | 0.5 every instance |
| medium 2-SAT pole (α=1.4) | 0.074 | — |
| long 2-affine pole (α=1.4) | 0.500 | — |

Sealed rule: DISQUALIFIED iff `max(3-XOR, 4-XOR) < medium pole (0.074)`. Here **0.03 < 0.074** — and 16× below the
same-density pairwise-visible reference (0.5), which controls for the density adaptation (parity is UNSAT at the
calibration α=1.4, so measured at α=0.6). Globally-rigid parity reads **below a bounded-width family** on this
observable — the disqualifying inversion.

## What it means

- **ξ-as-built is DISQUALIFIED for the substrate hypothesis**, not merely limited. Both observables (`corr`,
  `forcing`) compute a **pairwise** object; "reach" (how far a *partial solution* — a set — biases a distant
  variable) is the **point-to-set** length (= reconstruction = clustering α_d; MRT: α_d = α_r).
- **The P2 PASS STANDS but is RESCOPED:** the instrument correctly orders **pairwise correlation** — a real
  quantity, and *not* the one "reach" means.
- **P3 does not run in this form.** Of the 14 census families, the affine/parity ones (zerovalid-affine,
  onevalid-affine, lin-eq-z3, lin-eq-z3-b, and the parity component of xor-sat) would be **systematically
  misplaced** — read as near-zero reach despite maximal propagation. A sweep on this observable would mislabel a
  fifth of the roster.

## The design fork (owner decision — pending)

1. **Build a point-to-set instrument** — condition on a far **boundary set** rather than a single variable (MS Eq. 6
   / MRT reconstruction-on-the-cavity-tree). This is a **NEW instrument** with its own prereg, its own poles
   (parity must now read LONG), and its own qualification. No silent redesign.
2. **Stop the propagation line** and write Pebble up as an **instrument-development chapter** with a located design
   flaw. A legitimate outcome, **not a failure**.

## Provenance

The I-SP memo (`Pebble-ISP-susceptibility.md`) stands as written. This diagnostic supersedes only its §4
"logged, not acted on" disposition: the flag was **escalated by owner ruling** (prereg_v20), the diagnostic run, and
ξ-as-built disqualified for reach-proper. Credit: a parallel investigation caught a design flaw the main line's
calibration structurally could not, because the pole choice concealed it.
