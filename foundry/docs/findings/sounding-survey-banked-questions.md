# Sounding survey — banked questions

**Status: BANKED QUESTIONS. Not findings, not claims, not scored.**
Source: `sounding_survey_readings.json` — 114 matched-null excess readings over 20 rows, exploratory, no
sealed prediction. Anything below caught the eye during a descriptive pass and is written down so a later
design can pose it properly. **Nothing here may be cited as a result.**

---

## Q1 — the FORCED table is hand-maintained, and the survey shows it is incomplete

**This is the one with an operational consequence, so it goes first.**

Ten readings return a measured rate of **exactly 0.0** while *not* being flagged `theorem_forced`. At least
five are plainly forced and were simply missing from the list:

| row | region | flavour | why it is forced |
|---|---|---|---|
| `vertex-cover` | feasible | majority | Γ = {OR₂}; a 2-clause is bijunctive, hence majority-closed |
| `independent-set` | feasible | majority | Γ = {NAND₂}, likewise a 2-clause |
| `clique` | feasible | majority | same, on the complement |
| `bipartiteness` | solutions | majority | CSP(K₂) is 2-CNF-expressible |
| `matching` | feasible | majority | to be checked, but the pattern is the same shape |

**The consequence.** Design law 3 — *forced flavours excluded from any discovery statistic by schema* — is
enforced in code against `FORCED`, **a hand-written dictionary**. Schema enforcement is only as good as the
table it consults, and a hand-maintained list of theorem-forced pairings is precisely the *rules that live
in recall* failure the program keeps naming.

**The question to pose properly:** should forcedness be **derived** — compute the closure of the row's
pinned template and mark every flavour it is closed under — rather than listed? Marrow already pins
templates for 28 rows and already computes exactly this. The two artifacts have never been connected.

*(Round 2's F2 was not scored, so nothing published depends on the omission. It would have mattered had it
been.)*

## Q2 — some regions are *anti*-blendable relative to random sets of their own size

30 of 114 readings have **positive** excess: the measured region violates *more* than a uniform random
subset of identical size in an identical space. The largest are structural rather than scattered —
spanning trees under union and intersection (+0.11 both), minimum-weight partitions (+0.12), dominating
sets under intersection (+0.18).

The shape is legible: a spanning tree is defined by a *global* constraint (connected and acyclic) that both
union and intersection destroy immediately, whereas a random set of the same size has no such structure to
break. **Being highly structured can make a region less blend-stable than being unstructured.**

If that survives a proper design, "distance from randomness" is **signed**, and the two-pole picture would
need a third position — not *blends better than random* versus *indistinguishable from random*, but a
region whose structure is actively hostile to blending. Banked, not claimed; n is small and no prediction
was made.

## Q3 — the probe reads rows closure anatomy cannot, and this is the first demonstration

`dominating-set`, `exact-cover-x3c` and `three-dimensional-matching` are **excluded from Marrow's closure
columns** — their constraint scopes are unbounded-arity, so no fixed finite template exists to take
polymorphisms of. The probe does not care: it enumerates solutions directly and read all three.

That is the geometry note's original argument, now demonstrated on three rows rather than asserted: an
instrument that measures the region reaches a population the instrument that derives from the template
cannot. **Whether those readings mean anything is a separate question and is not answered here.**

## Q4 — optimal regions are systematically tiny, and 28 readings are INSUFFICIENT-r

28 of 114 readings sit below the r ≥ 10 floor, nearly all of them `optimal` regions —
`min-spanning-tree` optimal at r ≈ 2.7, `reachability-stcon` optimal at r ≈ 3.5. This is round 2's
entanglement finding appearing again from the other side: **minimality means few members**, and no ensemble
tuning changes that.

The question: is there a region definition between *feasible* and *optimal* — near-optimal within a
declared slack — that keeps optimisation semantics while carrying enough members to measure? That is a
design question about what an optimisation row's region *should* be, not a statistical one.

## Q5 — the descriptive table does not repeat round 2's pattern, which is itself worth noting

Mean excess by region kind × decision, forced and INSUFFICIENT readings excluded:

| region | easy | hard |
|---|---:|---:|
| solutions | −0.3555 (n=12) | −0.1834 (n=16) |
| feasible | −0.1795 (n=15) | −0.3658 (n=17) |
| optimal | −0.1402 (n=8) | −0.1167 (n=10) |

The `solutions` row runs one way and the `feasible` row runs the other, with `optimal` nearly flat. **No
direction is claimed** — these are means over unmatched readings with no prediction attached, exactly the
comparison a survey is not entitled to score. It is banked because a design that intends to score it should
know in advance that the sign is not stable across region kinds, and should say which region kind it means
before looking.

---

**None of the above is a result.** Each is a question with an artifact behind it, waiting for a design that
states its prediction first.
