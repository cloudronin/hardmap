# Atlas v3 — second pass (reliable tier, sampling retired) — running log

**Workload:** 154 cited cells outside the 272-cell V2 program — every remaining reliable-tier cell, per
the owner's amended QC table. Six verifier batches, same Check-9 protocol. Verdicts in
`results/atlas/v3-confirm/pass2/verdicts{1..6}.json`.

**Run condition that differs from V2:** this pass has **full-text PDF access** (`fitz`/`pypdf`/
`pdfplumber`). V2 ran under a false constraint — see methods-thread instance 10. Where a second-pass
verdict re-touches a V2 cell, the second-pass verdict supersedes.

## Tally

| batch | cells | OK | CITE | FIX | OPEN | seconds |
|---|---|---|---|---|---|---|
| 1 | 26 | 17 | 8 | 0 | 1 | ~1050 |
| 2 | 26 | 23 | 3 | 0 | 0 | ~400 |
| 3 | 26 | 20 | 5 | 0 | 1 | ~1000 |
| 4 | 26 | 18 | 7 | 1 | 0 | ~1200 |
| 5 | 25 | 22 | 3 | 0 | 0 | ~1450 |
| 6 | 25 | 20 | 5 | 0 | 0 | ~1300 |
| **COMPLETE** | **154** | **120** | **31** | **1** | **2** | **~6400** |

**Value-error 3/154 = 1.9%** (V2: 4.8%). **Citation-error 31/154 = 20.1%** (V2: 17.3%).

The reliable tier errs **less than half as often on values** and **at least as often on citations**. That
split is the headline: tiering predicts value quality and tells you nothing about citation quality.
Retiring the sample was right — a 15% sample of this tier would have surfaced roughly 5 of the 31
citation defects and, on the observed rate, neither of the two `open` downgrades.

**Caveat on the value comparison.** Every second-pass batch was decision/parallelization-heavy — the
reliable tier is *defined* by charges that are structurally immune to the F-2 approximation trap that
drove V2's rate. The 1.9% is a real measurement of this tier, not evidence that the corpus improved.

## The measured cost of removing the evidence ceiling

**~6,400 agent-seconds / 154 cells = 41.6 s per cell**, against V2's **28.6 s/cell** — **+45%**. That
delta is the price of full-text reading (methods-thread instance 10). What it bought, measured: the two
`open` downgrades and the one `FIX` were **all three** only visible in full text, and two independent
verifiers converged on the same one. So the ceiling cost roughly one corrected value per 50 cells, and
lifting it costs about 13 extra seconds per cell. That is the first measured exchange rate between
evidence depth and defect yield this program has.

## Value changes

| verdict | row | charge | drafted → corrected |
|---|---|---|---|
| OPEN | `lex-first-maximal-matching` | parallelization | `P-complete` → **`open`** |
| OPEN | `minimum-weight-triangulation` | decision | `NPC` → **`open`** |
| FIX | `deadlock-detection` | parallelization | `P-complete` → **`NC`** as written |

### `lex-first-maximal-matching` — found twice, independently

Batches 1 and 6 caught this separately and agree. Batch 6 adds the decisive detail: **GHR list LFMM in
their open-problems appendix as B.8.2** ("it is in CC"), and the cited Miyano paper is wrong on *both*
axes — wrong venue (Math. Systems Theory 22, 1989, not IJFCS 1990) and wrong object (vertex-induced
hereditary subgraphs, which GHR catalogue separately at A.2.16). The establishing work is Mayr &
Subramanian, JCSS 44 (1992). Two verifiers reaching the same catch from different batches is the
strongest signal in this pass.

### `deadlock-detection` — the value contradicts its own citation's remark

The cell claims single-unit deadlock detection is `P-complete`. GHR's entry A.12.2 shows the
P-completeness reduction requires resources with **two** units, and the Remarks then state verbatim that
the problem **is in NC** when there is one unit of each resource. The cell asserts P-completeness for
precisely the case Spirakis proved is in NC. Recorded as `NC` for the task as written; the preferable
repair is to retarget `canonical_task` to general multi-unit deadlock detection, which keeps
`P-complete` on a cited object. (Citation year also corrected: Spirakis is TCS 52 (1987), not 1986.)

### `type-inference-typability` — cited folklore, a subclass the folklore gate does not catch

Batch 4 found that GHR contains **no type-inference entry anywhere** in 327 pages; DKM 1984 proves
*unification* P-complete; and Henglein (TOPLAS 1993, p. 260) states the Curry–Hindley P-completeness
explicitly as a **"folk theorem."** The cell has a citation, so it passes the atlas's 0-folklore gate —
but the citation's own author calls the result folklore. **A folklore gate that checks for the presence
of a citation cannot catch folklore that has acquired one.** Left as an owner call between `open` and a
folk-theorem anchor; the value is not in dispute, its establishment is.

`capacitated-dominating-set` is the same shape confirmed across three papers in that line: **no primary
NP-completeness proof exists**; the result is inherited everywhere it appears.

### `minimum-weight-triangulation` — a SECOND vocabulary gap, in the decision column

Mulzer & Rote (JACM 55(2) 2008, arXiv:cs/0601002v3) state verbatim that **it is not known whether MWT
is in NP**, because it is open whether sums of radicals can be compared in polynomial time. MWT is
NP-hard; `NPC` overclaims membership.

**The decision vocabulary cannot express this.** Its 7 rungs — `P`, `NPC`, `coNP-complete`,
`PH-complete`, `PSPACE-complete`, `beyond-PSPACE`, `NPI-candidate` — *all assert membership*. There is no
"hard for the class, membership open" rung. This is structurally the **same defect class as errata-v1's
approximation gap** (the one that produced `superpoly-APX`): a real, published status with no
expressible value.

**Two repairs exist and the choice is the owner's**, because the precedent points both ways:
- **Extend the vocabulary** with an NP-hard rung — the SVP/CVP ruling: *"extend the vocabulary, don't
  force a wrong rung."*
- **Repin the task** to the rounded-weight ⌈‖e‖²⌉ variant, which the *same Mulzer–Rote paragraph* proves
  NP-complete — the graph-3-coloring ruling: *"the id is the object, repin the task to match."*

Unlike SVP/CVP, a correct object repin is available here, so a vocabulary extension is not forced. Unlike
graph-3-coloring, this id covers both variants, so repinning is not obviously the object's own meaning.
**A corpus-wide sweep is running** for the rest of this family (Euclidean TSP is the textbook member),
under the standing ruling that a discovered defect class gets swept before freeze —
`decision-membership-sweep.json`.

**`lex-first-maximal-matching` is the pass's real find so far, and it took full-text access.** The cell
claimed `P-complete` citing GHR (1995). Extracting the GHR compendium shows LFMM **is not in Part A
(P-complete) at all** — it sits in Part B under *CC Problems*, beside Comparator CVP and Stable
Marriage, with GHR's own remark that "a P-completeness proof for LFMM would imply that edge-weighted
matching is also P-complete," and the section preamble calling such a proof unlikely. Mayr &
Subramanian (JCSS 1992) and Cook–Filmus–Lê (ToCT 2014) place it **CC-complete**, with NL ⊆ CC ⊆ P open.
The co-citation (Miyano) proves P-completeness only for lex-first maximal *vertex-induced subgraphs* —
the wrong object, which the cell's own canonical_task already identified as an edge object.

## Systematic citation patterns

1. **Compendium-and-approximation-paper substitution — 6 of batch 1's 8 CITEs.** The citation discusses
   the problem instead of proving it. Three are compendium entries standing in for the original proof
   (Garey & Johnson [GT35], [GT27]; GHR for AGAP, where GHR itself names Chandra–Kozen–Stockmeyer and
   Immerman). Three cite an *approximation* paper for a *decision*-charge NP-completeness.
2. **`strip-packing` is the sharpest instance and is close to fabricated provenance.** Baker–Coffman–
   Rivest 1980, pulled from Rivest's own page, **contains no hardness proof at all** — its single
   intractability sentence covers the equal-widths special case and attributes even that to Ullman. The
   cell's note "NP-hard via 3-Partition" appears nowhere in the paper.
3. **Citation borrowed from the wrong charge of the same row — all 3 of batch 2's CITEs.**
   `context-free-membership` (decision/P) cites Jones & Laaser, a P-*completeness* paper giving no
   algorithm — the O(n³) CYK claim needs Younger 1967, and Jones & Laaser is correctly used for this
   row's *parallelization* charge. `max-e3-sat` (decision/NPC) cites Håstad 2001, whose home is this
   row's *approximation* charge. `datalog-evaluation` cites a survey repeating PTIME data complexity
   rather than Vardi 1982 / Immerman 1986 / Chandra–Harel 1985.
4. **Object drift, two clean cases.** `node-multiway-cut` cites the *edge* multiterminal-cut paper
   (Dahlhaus et al.) for a vertex-version cell; `lz78-compression` cites an NP-completeness-of-optimal-
   parsing note for a P-completeness value.
5. **The generic-authority stamp — all 5 of batch 3's CITEs.** A monograph or a pair of famous names
   invoked for a claim it does not carry. `generalized-assignment` and `k-edge-connected-subgraph` cite
   bare "Garey & Johnson (1979)" for problems **the G&J appendix does not contain** (GAP has no entry;
   the nearest, [GT31], is the *vertex*-connectivity variant). `min-degree-spanning-tree` cites
   "[Hamiltonian Path, ND1]" — ND1 is Degree Constrained Spanning Tree; Hamiltonian Path is GT39.
   `datalog-evaluation` leans on the bare names "Immerman/Vardi" (fixpoint logic — a different object;
   plain Datalog is monotone and does not capture P). `type-inference-typability` cites O'Toole &
   Gifford, whose PLDI'89 system is second-order polymorphic — a strictly larger object.
6. **The citation field holding a DERIVATION rather than a citation — all 3 of batch 5's CITEs.** The
   sharpest instance: `list-coloring` cited to Karp 1972 on the reasoning *"generalizes 3-colouring,
   NP-complete a fortiori"* — but list colouring did not exist as a notion until Vizing 1976 /
   Erdős–Rubin–Taylor 1979, and Karp's paper says nothing about it (→ Kratochvíl & Tuza, DAM 50(3)
   (1994) 297–302). `3-dimensional-assignment` cites G&J [SP1] 3-Dimensional Matching — a *feasibility*
   problem — when the row is min-cost axial 3-index assignment, where feasibility is trivial and all the
   content is in the costs (→ Frieze, EJOR 13(2) (1983) 161–164). `capacitated-facility-location` cites
   a survey chapter about the *uncapacitated* problem; no CFL-specific hardness theorem appears to
   exist, so the remedy is to cite the strongest true restriction (Bin Packing, G&J [SR1], strongly
   NP-complete), named as a restriction. This pattern is distinct from patterns 1–5: the drafter did not
   mis-select a source, it **reasoned to a conclusion and then wrote a famous name in the citation
   field**. Check-9 exists precisely to catch this, and it did.

## Flagged for the Gate-4 sitting — not decided by the agent

- **`ultrametric-tree-fitting` — the problem_id is a trap.** The cell is OK on its own terms (pinned to
  Theorem 5.1 of Agarwala et al.), but L∞ fitting by an *ultrametric* is linear-time solvable
  (Farach–Kannan–Warnow). Task and citation both describe **tree-metric** fitting; only the id says
  ultrametric. Read off the id, the value flips to P. Verifier recommends renaming to
  `tree-metric-fitting`. **Left undecided deliberately:** the owner's graph-3-coloring ruling was *"the
  id is the object, repin the task to match"* — applied literally here it would repin to ultrametric and
  flip the value. That ruling governed a *frozen, published* id; this is an unfrozen draft whose id
  contradicts its own task and citation. Which precedent governs is the owner's call, and an id rename
  also touches the provenance sidecar and S2 dedup.
- **`lz78-compression` has an unread erratum** — TCS 234 (2000) 325–326. Should be read before that cell
  is confirmed.
- **`metric-dimension`** passed as OK on Garey & Johnson [GT61] as the origin listing, but promoting
  Khuller–Raghavachari–Rosenfeld (1996) into the citation field would give the cell a published proof
  rather than a compendium entry.

## Limitations

Batch 1 exhausted its 200-call web-search budget near the end; ResearchGate/Elsevier 403s blocked the
De Agostino texts, so `lz78-compression`'s corrected citation rests on secondary attestation rather than
a direct read. Batch 1 flagged `red-blue-set-cover`'s approximation cell as an F-2 trap — that cell was
already corrected to `poly-APX` in the V2 pass, so the flag confirms the fix rather than finding a new
defect.
