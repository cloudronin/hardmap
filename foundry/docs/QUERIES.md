# QUERIES.md — the observatory database, eight worked joins

**The database is DERIVED. The hashed JSONL artifacts are the source of truth.** `observatory.db` can
be deleted and rebuilt at any time; the JSONL cannot. Every table carries the sha256 of the artifact it
was compiled from, so a db and its sources can be *checked* against each other rather than trusted.

Rebuild: `python3 foundry/dev/build_observatory_db.py`. Open: `sqlite3 foundry/foundry/results/lattice/observatory.db`.

Every query below is executable as written, and the output shown is from the current build.

---

## Q1 — what can the observatory reach, and how is it captured?

```sql
SELECT reach_class, capture, COUNT(*) AS n
FROM problems
GROUP BY reach_class, capture
ORDER BY n DESC;
```

```
reach_class                        capture               n  
---------------------------------  --------------------  ---
REACH-subset                       RAMPED                127
REACH-assignment                   RAMPED                56 
OUT-proof-object                   n.a. — not reachable  52 
REACH-permutation                  RAMPED                39 
BUILT                              RAMPED                27 
OUT-continuous                     n.a. — not reachable  22 
REGIONLESS-unique-answer           n.a. — not reachable  9  
REGIONLESS-language-membership     n.a. — not reachable  6  
no-natural-dial-at-fixed-encoding  n.a. — not reachable  4  
STILL-UNTYPED                      n.a. — not reachable  3  
BUILT-not-in-census                RAMPED                1  
```

## Q2 — descriptors joined to charges (charges are FIXED LABELS, never dials)

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
decision  traj_class    n   mean_excess_ref
--------  ------------  --  ---------------
NPC       MONOTONE      34  -0.2878        
NPC       FLAT          23  0.0171         
NPC       UNCLASSIFIED  22  -0.2014        
NPC       NON-MONOTONE  15  -0.0908        
P         NON-MONOTONE  9   -0.3465        
P         MONOTONE      7   -0.4989        
P         FLAT          4   -0.0873        
```

## Q3 — which catalog cells are disclosed-prior material?

```sql
SELECT coherence_is_retro_filled AS retro, COUNT(*) AS cells,
       COUNT(DISTINCT problem_id) AS problems
FROM catalog
GROUP BY retro;
```

```
retro  cells  problems
-----  -----  --------
0      32     5       
1      108    18      
```

## Q4 — the coherence/excess co-movement, per row (Q16's seed, as SQL)

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
problem_id             region     overlap_ref  excess_ref  flavours
---------------------  ---------  -----------  ----------  --------
odd-cycle-transversal  optimal    0.6861       -0.1241     4       
independent-set        optimal    0.6606       -0.3637     4       
feedback-vertex-set    optimal    0.659        -0.0199     4       
vertex-cover           feasible   0.649        -0.4799     4       
set-cover              optimal    0.6461       -0.043      4       
sat-2                  solutions  0.6305       -0.4974     4       
independent-set        feasible   0.6256       -0.4898     4       
sat-3                  solutions  0.6166       -0.456      4       
```

## Q5 — provenance: every catalog cell traced to frames that exist

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

## Q6 — what is reserved, and has it been released?

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
----------------------------  -----  --------  ------------  ------------
nearest-codeword              3      0         algebraic     REACH-subset
weighted-interval-scheduling  3      0         optimization  REACH-subset
```

## Q7 — the rejected-candidate ledger

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
screen_disposition  screen_rule   n  
------------------  ------------  ---
HELD                power-fail    210
REJECTED            null-missing  57 
HELD                null-missing  47 
REJECTED            netting       30 
```

Rejections are **preserved, not summarised**. The 30 `netting` rejections are descriptor pairs whose
correlation is partly forced by the extractor's own arithmetic — they were enumerated anyway, because a
denominator that omits the questions we already knew were bad is a denominator we chose.

## Q8 — the biography of the territory

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
----------  -------------  -
annotation  0              1
expansion   0              1
annotation  1              2
exclusion   1              1
expansion   1              2
freeze      1              5
version     1              1
```

For one problem's biography: `SELECT * FROM maptrail WHERE problem_id = ? ORDER BY at`.

**Two standing views** are computed rather than kept: `hold_queue` (held candidates with the frontier size
that would revive them) and `family_ledger` (cumulative corrections derived from the sweep and ruling
records). Neither is ever hand-maintained.
