# Strata coverage report — where each kind of hardness can be studied at all

**The report is the finding.** "The population where a charge is observable" is not a coverage gap to be closed; it
is a structural fact about the atlas, and nobody had tabulated it. Strata (the Eightfold v2 additive metadata layer)
turns three facts the program kept rediscovering by hand into queries over `atlas_v2.jsonl` (sha256
`784f4739360f1d7b4a3308e1f548c37ecbafeb3842878bc64d82fc6c4dd9c567`; the frozen `atlas.jsonl` is untouched — additive-
only is *structurally* enforced by the `test_loader` round-trip, so the frozen atlas defends itself). Source data:
`results/atlas/strata_coverage.json`.

## 1. Where each charge is observable (per-charge applicability, 118 rows)

| Charge | defined-informative | ambiguous | n.a. | Observable at all |
|---|---|---|---|---|
| decision | 114 | — | 4 | 114/118 |
| counting | 86 | — | 32 | 86/118 |
| approximation | 70 | — | 48 | 70/118 |
| **parameterized** | **28** | **40** | **50** | 68/118 (but 40 carry a caveat) |
| parallelization | 37 | — | 81 | 37/118 |
| proof_size | 15 | — | 103 | 15/118 |
| average_case | 89 | 4 | 25 | 93/118 |
| landscape | 28 | — | 90 | 28/118 |

Reading: decision is nearly universal (it is the atlas's spine); `proof_size` and `landscape` are the *rarest*
objects — a propositional refutation family and a samplable solution geometry exist for only ~1 row in 8. This is
not thin coverage to backfill; it is where those kinds of hardness *can be posed at all*. The `parameterized` row is
the one to sit with: of 68 rows where it is defined, **40 are `ambiguous`** — the treewidth-vs-solution-size choice
is the norm, not the exception, exactly as the level table's "objective + a *parameterization*" requirement warns.

## 2. The gradient's observable population — the three-level drill-down (R-3)

The program hand-counted this sequence three times across three sprints and never wrote it down as a category:
**118 → 47 → 16.** Strata makes it a query, and the query is *sharper* than the hand-count because it separates
"defined" from "defined-informative":

```
118  all rows
 59  both approximation AND parameterized DEFINED (not n.a.)     [-59: one charge n.a. — not an
                                                                  optimization/parameterized problem]
 25  both DEFINED-INFORMATIVE (no caveat)                        [-34: one charge is ambiguous — ALL of it
                                                                  the graph parameterization ambiguity]
 21  DEFENSIBLE local relation (+ objective & parameterization   [-4: a pin not cleanly identified]
     both pinned)
```

**The load-bearing finding is the 59 → 25 drop.** All 34 rows lost carry the parameterization ambiguity
(treewidth vs solution-size), and **that drop takes all three of the gradient's own witnesses with it —
vertex-cover, clique, independent-set.** This is not tidiness lost; it is the single most consequential fact about
those rows made visible. The charge value *flips* with the framing: independent-set is W[1] by solution-size but FPT
by treewidth, vertex-cover is FPT either way — so under a treewidth reading the witness pair *stops being a
witness*. A "clean" gradient population of 25 rows exists only because it **excludes the very rows the gradient was
built on.** Recording that as `ambiguous` metadata, rather than silently picking a framing, is the whole point of
Strata; the old hand-count of "47 gradient-carrying" hid it.

The 21 defensible rows (caveat-free, both pins identified) are SAT-family (`Max-CSP` × treewidth),
packing/covering (`Min-Ones`/`Max-Ones` × solution-size), and numeric objectives (`global-numeric`) — a population
with no parameterization ambiguity, and notably *no graph vertex-selection problems*.

## 3. The level table makes the coupling visible in one glance

The charge-level table (`strata.CHARGE_LEVELS`) records the object each charge attaches to. In one column it shows
what five sprints argued in prose: **the two `objective`-level charges — approximation and parameterized — are
exactly the coupled pair.** Every other level (decision, counting, refutation, ensemble) holds multiple charges with
no strong coupling among them. The mechanical consequence (`cross_level_flag`): a predictor aimed across levels is
suspect before it runs — which would have flagged tuple-dispersion-versus-approximation three sprints early.

## 4. A finding about the atlas's own construction

The objective TYPE was recorded only in prose (`canonical_task`), never as a field. Resolving it after the fact
measures how much structure was *implicit in our own writing*:

| Reader | derived by rule | needed a human | % human |
|---|---|---|---|
| crisp lexicon (lead token only) | 61 | 57 | **48%** |
| fuller lexicon (full task text) | 88 | 30 | **25%** |

A schema-blind reader can recover the objective **three-quarters of the time** from prose that was written per-cell
over months with no schema in mind — and the residual 25% is not noise, it is the measure of what only a human who
knows the field can supply (that `MIN-STEINER` is a *weight*, not a set count; that number-partitioning's objective
is a derived imbalance, not its weighted input). The 48%→25% gap is itself the value of writing the schema down.

## 5. Scope

Additive-only, no value changed (a suspect v1 value is a v2.1 candidate, never an in-place fix). "Strata v2" (this
metadata layer) is a distinct axis from the queued "charge-9 v2" (fine-grained complexity); do not conflate. The
`judged` provenance on 137 applicability / 30 objective / 8 parameterization cells records exactly which metadata
rests on owner judgment versus mechanical derivation, auditable to the same standard as the charge values.
