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
| 3 | 26 | | | | | |
| 4 | 26 | | | | | |
| 5 | 25 | | | | | |
| 6 | 25 | | | | | |
| **so far** | **52** | **40** | **11** | **0** | **1** | |

**Value-error rate so far: 1/52 = 1.9%** — against 4.8% in V2. Consistent with the reliable tier being
genuinely cleaner, but the two batches drawn so far are decision/parallelization-heavy, which are
structurally immune to the F-2 approximation trap that drove V2's error rate. Not yet a comparison.

## Value changes

| verdict | row | charge | drafted → corrected |
|---|---|---|---|
| OPEN | `lex-first-maximal-matching` | parallelization | `P-complete` → **`open`** |

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
