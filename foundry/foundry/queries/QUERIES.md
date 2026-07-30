# QUERIES.md — the observatory database, eight worked joins

**The database is DERIVED. The hashed JSONL artifacts are the source of truth.** `observatory.db` can
be deleted and rebuilt at any time; the JSONL cannot. Every table carries the sha256 of the artifact it
was compiled from, so a db and its sources can be *checked* against each other rather than trusted.

**Run these without a checkout:**

```bash
pip install hardmap
hardmap db build              # compile the database from the frozen JSONL
hardmap query --list          # the eight queries below, by name
hardmap query rejected-candidates
hardmap query --sql "SELECT COUNT(*) FROM catalog"
```

Or open it in any SQLite browser: `hardmap db build --path ./observatory.db`.

**The output blocks below are COMPILED**, re-executed against the current database by
`foundry queries refresh`. They were hand-pasted once and drifted — this file promised its outputs
were current while showing a frontier of 2 against an actual 16. The SQL and the prose are authored;
the outputs are not.

---

## Q1 · reach-and-capture — what can the observatory reach, and how is it captured?

```sql
SELECT reach_class, capture, COUNT(*) AS n
FROM problems
GROUP BY reach_class, capture
ORDER BY n DESC;
```

```
reach_class                        capture               n
---------------------------------  --------------------  --
REACH-subset                       RAMPED                76
REACH-assignment                   RAMPED                71
OUT-proof-object                   n.a. — not reachable  52
REACH-permutation                  RAMPED                47
BUILT                              RAMPED                27
OUT-continuous                     n.a. — not reachable  22
REACH-partition                    RAMPED                16
REGIONLESS-unique-answer           n.a. — not reachable  9
REGIONLESS-language-membership     n.a. — not reachable  6
DECOMPOSITION                      RAMPED                5
REGIONLESS-unique-answer           RAMPED                5
no-natural-dial-at-fixed-encoding  n.a. — not reachable  4
STILL-UNTYPED                      n.a. — not reachable  3
STRATEGY                           RAMPED                2
BUILT-not-in-census                RAMPED                1
```

## Q2 · descriptors-by-charge — descriptors joined to charges (charges are FIXED LABELS, never dials)

```sql
SELECT ch.value AS decision, c.traj_class, COUNT(*) AS n,
       ROUND(AVG(c.excess_ref), 4) AS mean_excess_ref
FROM catalog c
JOIN charges ch ON ch.problem_id = c.problem_id AND ch.charge = 'decision'
WHERE c.excess_ref IS NOT NULL
GROUP BY ch.value, c.traj_class
ORDER BY decision, n DESC;
```

```
decision     traj_class    n    mean_excess_ref
-----------  ------------  ---  ---------------
NPC          FLAT          107  -0.0475
NPC          UNCLASSIFIED  56   -0.1299
NPC          NON-MONOTONE  52   -0.0837
NPC          MONOTONE      35   -0.2515
NPC                        26   -0.1289
P            NON-MONOTONE  10   -0.3226
P            FLAT          9    -0.0466
P            MONOTONE      7    -0.4989
P            UNCLASSIFIED  2    -0.1547
PH-complete  FLAT          10   -0.2037
PH-complete  UNCLASSIFIED  6    -0.1727
PH-complete  NON-MONOTONE  6    0.0427
```

## Q3 · disclosed-prior-cells — which catalog cells are disclosed-prior material?

```sql
SELECT coherence_is_retro_filled AS retro, COUNT(*) AS cells,
       COUNT(DISTINCT problem_id) AS problems
FROM catalog
GROUP BY retro;
```

```
retro  cells  problems
-----  -----  --------
0      338    46
1      108    18
```

## Q4 · coherence-comovement — the coherence/excess co-movement, per row (Q16's seed, as SQL)

```sql
SELECT problem_id, region,
       ROUND(AVG(overlap_ref), 4) AS overlap_ref,
       ROUND(AVG(excess_ref), 4)  AS excess_ref,
       COUNT(*) AS flavours
FROM catalog
WHERE overlap_ref IS NOT NULL AND excess_ref IS NOT NULL
GROUP BY problem_id, region
ORDER BY overlap_ref DESC
LIMIT 8;
```

```
problem_id                 region    overlap_ref  excess_ref  flavours
-------------------------  --------  -----------  ----------  --------
bilevel-knapsack           optimal   0.7888       -0.1877     4
maximum-induced-matching   feasible  0.7844       0.017       4
triangle-packing           feasible  0.7525       -0.0011     4
triangle-packing           optimal   0.7391       -0.0024     2
biclique-cover             optimal   0.7314       -0.0386     2
red-blue-set-cover         optimal   0.7273       0.0303      2
graph-spanner              feasible  0.7171       -0.0703     4
connectivity-augmentation  optimal   0.7126       -0.0106     4
```

## Q5 · provenance-check — provenance: every catalog cell traced to frames that exist

```sql
SELECT c.problem_id, c.region, c.flavour, COUNT(f.ramp_position) AS frames_backing
FROM catalog c
LEFT JOIN frames f
  ON f.problem_id = c.problem_id AND f.region = c.region AND f.flavour = c.flavour
GROUP BY c.problem_id, c.region, c.flavour
HAVING frames_backing = 0;
```

```
(no rows — which is the point of this query: see the note below)
```

**Note on Q5.** An empty result is the correct one: it asks for catalog cells with *no backing
frames*, and there are none. A provenance check that returns rows is a build failure — the query is here so
a reader can run it after any rebuild rather than trusting that the loader checked.

**Note on Q2.** Charges enter as **fixed row labels**, joined in from the atlas. They are worst-case facts
about a problem and never vary along a ramp. A query that made a charge look like it changes with hardness
would be the F2 category error — the schema prevents it by giving `charges` no ramp column at all.

---

# The Helm layer — three more joins

Added with Helm v1. These read the wave engine's own bookkeeping, which lives in the same database under
the same contract: byte-stable, regenerated never mutated, references engine-checked.

## Q6 · frontier — what is reserved, and has it been released?

The frontier is the ground Helm scores on. A row here is **declared and uncaptured**: it has no frames and
no catalog cells, so there is nothing about it to leak. It is visible as a *row id* — which the power
screen needs in order to count the tranche — and as nothing else.

```sql
SELECT f.problem_id, f.batch, f.released, p.family, p.reach_class
FROM frontier f
JOIN problems p ON p.problem_id = f.problem_id
ORDER BY f.problem_id;
```

```
problem_id                    batch  released  family        reach_class
----------------------------  -----  --------  ------------  ---------------
balanced-vertex-separator     4      0         graph         REACH-subset
bin-packing                   5      0         optimization  REACH-partition
capacitated-vertex-cover      4      0         graph         REACH-subset
cluster-editing               8      0         graph         REACH-subset
directed-steiner-tree         10     0         optimization  REACH-subset
group-steiner-tree            10     0         optimization  REACH-subset
k-minimum-spanning-tree       7      0         graph         REACH-subset
k-set-packing                 5      0         optimization  REACH-subset
maximum-minimal-vertex-cover  6      0         graph         REACH-subset
minimum-fill-in               8      0         graph         REACH-subset
minimum-k-cut                 9      0         graph         REACH-subset
multiway-cut                  9      0         graph         REACH-subset
nearest-codeword              3      0         algebraic     REACH-subset
planar-dominating-set         6      0         graph         REACH-subset
power-dominating-set          7      0         graph         REACH-subset
weighted-interval-scheduling  3      0         optimization  REACH-subset
```

## Q7 · rejected-candidates — the rejected-candidate ledger

**This is the archive's novel object.** Every question the data could have supported, and why each one was
screened, held, sealed or killed. A multiple-comparisons correction computed from an enumeration nobody
can audit is a number asking to be trusted; this publishes the garden of forking paths as a map of the
garden.

```sql
SELECT screen_disposition, screen_rule, COUNT(*) AS n
FROM candidates
GROUP BY 1, 2
ORDER BY n DESC;
```

```
screen_disposition  screen_rule               n
------------------  ------------------------  ----
HELD                power-fail                1262
REJECTED            null-missing              328
REJECTED            netting                   165
HELD                null-missing              161
REJECTED            definitional-consumption  7
REJECTED            size-marginal             7
SLATED                                        7
HELD                path-gated                3
HELD                needs-r-conditioning      2
```

Rejections are **preserved, not summarised**. The 30 `netting` rejections are descriptor pairs whose
correlation is partly forced by the extractor's own arithmetic — they were enumerated anyway, because a
denominator that omits the questions we already knew were bad is a denominator we chose.

## Q8 · territory-biography — the biography of the territory

`maptrail` records what changed in the domain's vocabulary, for an end user who has the database and no
commits. `reconstructed = 1` marks the one-time import of history that predates the trail; `reconstructed
= 0` is an event emitted by the operation that performed it.

```sql
SELECT event, reconstructed, COUNT(*) AS n
FROM maptrail
GROUP BY 1, 2
ORDER BY 2, 1;
```

```
event       reconstructed  n
----------  -------------  --
annotation  0              29
erratum     0              7
exclusion   0              13
expansion   0              8
retraction  0              1
version     0              17
annotation  1              10
exclusion   1              1
expansion   1              2
freeze      1              5
version     1              4
```

For one problem's biography: `SELECT * FROM maptrail WHERE problem_id = ? ORDER BY at`.

**Two standing views** are computed rather than kept: `hold_queue` (held candidates with the frontier size
that would revive them) and `family_ledger` (cumulative corrections derived from the sweep and ruling
records). Neither is ever hand-maintained.

<!-- sources: {"observatory.db": "ec8a3d7a820ee128ad12f09ff2e7161546de0015f838c79767efae881d216dac"} -->
