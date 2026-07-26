# N1 — the protective-structure seal, scored

**Status: SCORED ONCE. `prereg_v20`, sealed 2026-07-26 before this ran.**
**Artifact:** `n1_results.json` (sha256 `52be33f8`) · **Ran:** 51 min · 237 readings · 0 dropped

---

## Verdict: PROTECTIVE-STRUCTURE-REAL

**The primary holds.** Mean fair-null excess remains negative with a 95 % CI clear of zero.

| test | mean | 95 % CI | n | Holm (family 8) |
|---|---:|---|---:|---|
| **pooled** | **−0.0949** | **[−0.1186, −0.0713]** | 82 | REJECT, negative (p < 0.00001, thr 0.00625) |
| `sat-csp` | −0.1553 | [−0.1908, −0.1197] | 18 | REJECT, negative |
| `graph` | −0.1109 | [−0.1567, −0.0652] | 35 | REJECT, negative |
| `optimization` | −0.0589 | [−0.0830, −0.0349] | 14 | REJECT, negative |
| `number-theoretic` | −0.0187 | [−0.0323, −0.0051] | 15 | REJECT, negative (p = 0.00701, thr 0.01250) |

**All five reject, all in the negative direction, all surviving Holm–Bonferroni at FWER 0.05.**

Routes: 190 readings via tier 1.5, **47 via N2's qualified CP control**. Every reading replayed exactly;
nothing dropped.

## How the knife edge resolved — and what it decided

The seal declared before scoring that the primary **fails if absorption reaches +0.1604**.

| | |
|---|---:|
| disclosed tier-0 mean | −0.1975 |
| fair-null mean | **−0.0949** |
| **absorption** | **+0.1026** |
| flip point | +0.1604 |

**Absorption came in at +0.1026 — below the flip point, and below both prior measurements.**

| where absorption was measured | value |
|---|---:|
| Terrain, sparse, **positive-excess** readings | +0.1297 |
| N2, dense, **positive-excess** readings | +0.1586 |
| **N1, this population, mostly negative-excess** | **+0.1026** |

**This is the question the re-pose existed to ask, and it has an answer.** Terrain's absorption was
measured on readings selected for positive excess; the worry was that applying it across the selection
boundary was unwarranted. It was — **but in the direction that favours the bet, not against it.** A fair
null absorbs *less* where excess is negative than where it is positive.

So the negative excess is **not** the mirror image of the anomaly. The cardinality mismatch that
manufactured the positive excess does not account for the negative one. `ABSORBED` was the outcome this
design was built to be able to return, and it did not return it.

## The secondary is largely unaskable, and that is the honest report

The seal declared the easy–hard contrast within each of three region kinds. **Two of the three have zero
`easy` readings:**

| region kind | easy n | hard n | contrast |
|---|---:|---:|---|
| `feasible` | **0** | 45 | — INSUFFICIENT |
| `optimal` | **0** | 14 | — INSUFFICIENT |
| `solutions` | 13 | 10 | **−0.0045** |

Every surviving `feasible` and `optimal` reading carries decision `NPC`. The P-labelled rows in those
kinds — `max-flow`, `min-spanning-tree`, `reachability-stcon`, `matching` — were removed upstream as
theorem-forced, forced-saturated, or v2-unreplayable. **The population that survived the screens is
decision-homogeneous in two of three strata.**

The one contrast that could be computed is **−0.0045**, which is nothing.

**So the two-pole claim is untested here.** The primary is a statement about structure versus a fair null,
not about hardness. Nothing in this result speaks to whether the effect tracks the decision charge — and
Q5's contrast instability, which motivated the stratification, remains exactly as open as it was.

This is a real limitation of screening a survey column that was never designed to balance decision labels
within region kind. It is not fixable by re-analysis.

## What this establishes, stated narrowly

Against controls matched on **size, coordinate marginals and member cardinality**, the solution and
feasible regions of these rows violate blend-closure **less** than structureless sets of identical shape.
Structure is protective, by −0.0949 pooled, on 237 readings across 15 rows and four families.

Terrain established the mirror: the *positive* excess that looked like anti-blendability was a control
artifact, fully retired. **N1 establishes that the negative excess is not.** The two results together say
the fair null removed one direction and left the other standing.

## What it does not establish

- Nothing about the **decision charge**. The secondary is INSUFFICIENT in two of three strata.
- Nothing about rows outside the screened population — 19 `EXCLUDED-drift`, 53 v2 readings without
  per-reading seeds, and every forced or saturated flavour.
- Nothing about **why**. That structured regions blend better than cardinality-matched random sets is
  measured here, not explained.
