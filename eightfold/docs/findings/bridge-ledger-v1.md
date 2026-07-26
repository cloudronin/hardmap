# Bridge Ledger v1 — Proven Feature→Charge Links (netting + calibration basis for the grid)

> **Landing note (2026-07-24, Anatomy S0).** This note was authored by the owner and banked out-of-repo;
> it is landed here **verbatim** as the in-repo reference both Anatomy v1 and Mosaic v3 G0 cite. Its own
> pin-before-net rule is unsatisfied at landing time: the `pinned:` column below is filled by the I3
> pinning pass (one pass, two consumers), and **no cell nets anything or serves as a known-answer value
> until its row is pinned**. Landing ≠ pinning. Verbatim text follows; the pinning table is appended at
> §9 and never edits the cells above it.

**Status:** Note, banked 2026-07-24. Every cell below is high-confidence but **pin-before-net**:
the exact theorem statement and scope conditions get pinned at Strata-v2 / G0 I-phase before any
cell nets anything or serves as a known-answer value (house rule; memory-cited nothing).
**Verdict key:** NETTED = proven, do not test, becomes a known-answer calibration cell;
ISLAND = proven on a restricted class, only the off-island extrapolation is testable;
OPEN = the grid's real estate.

## 1. Bounded treewidth / tree-decomposability (most-bridged feature in existence)

| → charge | proven content | cite anchors (pin at I-phase) | verdict |
|---|---|---|---|
| decision | all MSO properties linear-time at bounded tw; bounded-arity CSP tractability ⟺ bounded tw (up to hom-equiv) | Courcelle 1990; Grohe–Marx | **NETTED** |
| counting | MSO **counting/evaluation** tractable at bounded tw; #SAT at bounded tw ⟵ *corrected at I3 pinning, 2026-07-24: originally read "counting/**enumeration**"; CMR's own footnote 4 warns the term "might be misleading, as we do not enumerate the solutions but we count them." Delay-bounded enumeration is **UNPINNED** — no anchor carries it.* | **treewidth primary:** Courcelle–Mosbah 1993 (TCS 109:49–82) + Arnborg–Lagergren–Seese 1991; **modern statement:** CMR 2001 (DAM 108:23–52) Thm 32; **#SAT:** Fischer–Makowsky–Ravve 2008, sharp constant 2^k Slivovsky–Szeider 2020 | **NETTED** (counting only) |
| parallelization | small-treewidth NC algorithms; optimal-speedup parallel tree decomposition + all MSO decision problems in O(log n) CRCW | Bodlaender 1988; Bodlaender–Hagerup (SICOMP) | **NETTED** — bounded-width decomposability ⟹ parallelizable; the Horn-SAT counterexample is *unbounded-width* local structure. Strata must carry the bounded/unbounded-width distinction or this cell mis-nets |
| parameterized (tw as parameter) | FPT by treewidth for MSO problems | Courcelle | **NETTED** |
| parameterized (solution size) | — | — | **OPEN** (the witness-ambiguity split, already tagged in the atlas) |
| approximation | only via planarity/minor routes | see §2 | ISLAND via §2 |

## 2. Planarity / minor-exclusion / geometric embedding

| → charge | proven | anchors | verdict |
|---|---|---|---|
| approximation | PTASs for broad families on planar/minor-free | Baker 1994; Demaine–Hajiaghayi bidimensionality | **ISLAND** — off-island population trend is testable |
| parameterized | subexponential FPT, same machinery | bidimensionality | **ISLAND, shared-cause** — theory's proof of the coupling's easy end, jointly, on the island |
| counting | planar matchings/permanent in P and NC (Pfaffian) | FKT; Mahajan et al. 2004; Cai–Lu–Xia planar #CSP dichotomies | **NETTED** as calibration |

## 3. Engine type (Bulatov–Zhuk anatomy; oracle-derivable)

| → charge | proven | anchors | verdict |
|---|---|---|---|
| decision | bounded-width ⟺ solvable by local consistency; few-subpowers → algebraic engine | Barto–Kozik; IMMVW | **NETTED** |
| approximation | — | — | **OPEN — prime real estate** (the grid's sealed engine-split bet) |
| parameterized | — | — | **OPEN — prime real estate** |

## 4. FO-definability + sparsity (the Gaifman route)

| → charge | proven | anchors | verdict |
|---|---|---|---|
| decision/param | FO model-checking FPT on sparse classes | Frick–Grohe 2001; Flum–Grohe | **ISLAND** |
| approximation | PTAS for X-positive/X-negative FO optimization on minor-free | Dawar–Grohe–Kreutzer–Schweikardt LICS 2006 | **ISLAND, shared-cause** (second jointly-proven easy-end instance; shared Gaifman hypothesis) |

## 5. Expansion (the anti-feature)

| → charge | proven | anchors | verdict |
|---|---|---|---|
| proof size | expander formulas resolution-hard via width-size tradeoffs | Ben-Sasson–Wigderson; Urquhart/Tseitin ancestry | **NETTED** |
| approximation | expansion powers PCP gap amplification | PCP line | NETTED as mechanism; **OPEN as per-row predictor** (typing care: "expander-like instances" is not a row fact without a stated ensemble) |

## 6. Kernel status

| → charge | proven | verdict |
|---|---|---|
| parameterized | poly-kernel ⟹ FPT (definitional-adjacent); FPT ⟺ some kernel | **NETTED**; informative residual = poly vs no-poly *within* FPT — **OPEN** (Mosaic P6's form, correct as sealed) |

## 7. Structure → average-case and → landscape

Almost entirely **OPEN**. Only islands: algebraic self-reducibility (permanent random-self-reducibility; lattice worst↔average, Ajtai) and OGP-style ensemble results (Gamarnik line) — the latter *ensemble-typed, not row-typed*. No population-level structure-predicts-average-case exists anywhere. The grid's virgin column if it ever wants one.

## 8. Operational consequences

1. **NETTED cells = the grid's known-answer calibration layer** — theorem-grade expected values,
   the strongest instrument qualification available to the program; failures there are pipeline
   bugs by definition.
2. **ISLAND cells = extrapolation bets**, sealed as "proven on class C; does the trend persist
   off-island as a population claim?" — sharper and more publishable than testing from scratch.
3. **OPEN cells = where grid hours concentrate:** engine→approx, engine→param,
   solution-size-parameter column, anything→average-case/landscape.
4. Every Strata-v2 column carries its bridge citation(s) from this ledger, so the eventual bridge
   table distinguishes proven cells from measured ones mechanically.

---

## 9. I3 pinning table (appended by the Anatomy S0 pass — shared with Mosaic v3 G0)

**Rule:** a ledger cell may be cited by an Anatomy column, net anything, or serve as a known-answer
calibration value **only once its row here reads `PINNED`.** A row that cannot be pinned to an exact
theorem statement with its scope conditions is demoted to `UNPINNED — do not net`, and the column citing
it falls back to `open` rather than borrowing an unverified warrant. This is the ledger's own house rule
(header: "memory-cited nothing"), made operational.

### 9.1 Headline — the gate paid for itself

**15 cells examined. 3 pinned clean (20%). 10 pinned only with correction. 2 unpinnable.**
*(Erratum, 2026-07-25: this headline first read "9 corrected / 3 unpinnable" — the pre-addendum count. It
was not updated when §1.counting resolved in §9.5. Corrected in place with its date; the §9.1 table row and
§9.5's revised tally were already right. Caught at Mosaic v3's grounding pass, which anchors to this file.)*
The ledger's header promised "memory-cited nothing." The pass found the opposite in nine cells, including
**two wrong-paper attributions, one claim that a cited-adjacent theorem literally refutes, one tautology
presented as a theorem, and one confirmed duplicate**. No cell was corrected by weakening it to taste —
every correction below is anchored to verbatim primary-source text.

| ledger cell | status | what the pin changed |
|---|---|---|
| §1.decision | **PINNED-WITH-CORRECTION** | anchor is **Grohe 2007 alone**, not "Grohe–Marx"; both scope conditions restored |
| §1.counting | **PINNED-WITH-CORRECTION** *(resolved after the seal commit; see §9.5)* | CMR 2001 is **both**, asymmetrically — and the citation string is **ambiguous between two CMR papers** |
| §1.parallelization | **PINNED-WITH-CORRECTION** | three-way conflation; the MSO result **bypasses the decomposition** |
| §1.parameterized-tw | **PINNED-WITH-CORRECTION** | **duplicate** of §1.decision — not independent evidence |
| §2.approximation | **PINNED-WITH-CORRECTION** | Baker is planar-only / 7 problems; "minor-free" is **not uniform** |
| §2.parameterized | **PINNED-WITH-CORRECTION** | "same machinery" true of the tool, false of the hypotheses |
| §2.counting | **PINNED-WITH-CORRECTION** | "planar matchings" is **refuted by Jerrum 1987**; both NC anchors wrong |
| §3.decision | **PINNED-WITH-CORRECTION** | "bounded-width ⟺ local consistency" is a **definition**, not a theorem |
| §4.fo_sparse | **PINNED** | — |
| §4.fo_minor_free | **PINNED** | — |
| §5.proof_size | **PINNED** | — |
| §5.approximation | **UNPINNED** | expansion is **manufactured** by the proof; it cannot discriminate rows |
| §6.kernel | **PINNED-WITH-CORRECTION** | needs **decidability**; kernel size arbitrary ⇒ no efficiency content |
| §7.self_reducibility | **PINNED-WITH-CORRECTION** | Ajtai is **one-directional**, approximation-version, engineered distribution |
| §7.ogp | **UNPINNED** | ensemble-typed, not row-typed — the ledger's own call, confirmed |

### 9.2 The four corrections that would have damaged the instrument

**(a) §2.counting — a NETTED calibration cell asserting the opposite of a theorem.**
The cell reads "planar matchings/permanent in P and NC." But *counting matchings in a planar graph is
#P-complete* — Jerrum 1987, §1, verbatim: *"the main result of this paper … is that 'counting matchings in
a planar graph is #P-complete.'"* The tractable object is **planar PERFECT matchings** (FKT / Kasteleyn
1967, via "every planar graph is Pfaffian" + Cayley's `det A = (Pf A)²`). "Permanent" is false under the
adjacency/cycle-cover reading (#P-complete for planar graphs of degree ≤ 4). Both NC anchors are
mis-attributed: the correct chain is **Kasteleyn 1967 + Csanky 1976 (det ∈ NC²) + Vazirani 1989**, not
Mahajan et al. 2004 / Cai–Lu–Xia — the sign obstruction those solve is a **GapL** obstruction, irrelevant
to NC, since NC is closed under integer square roots.
*Why it mattered:* per §8.1, NETTED cells become known-answer calibration values where "failures are
pipeline bugs by definition." Shipped as-is, every pipeline correctly reporting #P-completeness would have
been flagged as a bug, and the instrument would have been "fixed" toward the error.

**(b) §3.decision — a tautology presented as the theorem** (and this is Anatomy's own `engine_type` bridge).
"Bounded-width ⟺ solvable by local consistency" is **Barto–Kozik's definition** (Def. 3.3/3.4: a structure
*has width (k,l)* iff a nonempty (k,l)-strategy implies a homomorphism), not a result. The theorem content
is the **algebraic characterization**: sufficiency is Barto–Kozik, *JACM* 61(1) Art. 3, 2014 (SD(∧) ⇒
bounded width); **necessity is Larose–Zádori 2007**, not Barto–Kozik. Two load-bearing hypotheses were
dropped: a **finite core template**, and **all singleton unary relations added** (idempotent reduction).
The relational-width-(2,3) collapse is a *separate* paper (Barto, *JLC* 26(3):923–943, 2016). IMMVW's
few-subpowers side needs **no** core/idempotency hypothesis — the k-edge identities already force it.

**(c) §5.approximation — UNPINNED for a structural reason, not a missing citation.**
Dinur's amplification requires λ(G) ≤ λ < d, but her **Preprocessing Lemma 3.1** turns *any* constraint
graph into a d-regular self-looped graph meeting that bound, at O(1) size blowup. So **expansion is
manufactured inside the reduction, never observed on the input**: no instance is excluded for lacking it and
none is charged more for having it. Expansion therefore **cannot be a per-row predictor at all** on this
route — the deliverable is class-level NP-hardness of gap-3SAT, a statement about a problem, not a charge on
an instance. The ledger's own typing worry ("not a row fact without a stated ensemble") was correct and is
in fact stronger than stated. *This is instance-16's shape again: a proposed feature that cannot vary in the
way the design needs.*

**(d) §1.parallelization — a "+" that fuses three different results.**
Bodlaender–Hagerup, verbatim: the optimal-speedup decomposition construction is **O((log n)²) on EREW**;
the MSO results are O(log n log\* n) EREW / **O(log n) CRCW** — and they *"operate without an explicit tree
decomposition and so bypass the (time) bottleneck of our construction algorithm."* So it is **not**
decomposition-then-automaton. Those theorems are also **decision-only and nonconstructive**, and they decide
the *conjunction* P(G) ∧ tw(G) ≤ k, so the width bound is verified rather than promised.

### 9.3 Corrections of record (shorter, still binding)

- **§1.decision** — Courcelle's Prop. (4.14) takes the width-bounded **expression** as input, time O(size(e));
  the popular "linear in n from G alone" silently imports Bodlaender 1996. Logic is **counting MSO₂**. The
  constant is **non-elementary** and provably so unless P = NP (Frick–Grohe 2004). Grohe 2007's
  characterization needs **bounded arity** (he gives an unbounded-arity counterexample) and **FPT ≠ W[1]**.
- **§1.parameterized-tw** — the same Courcelle theorem read parameterized. **It must not be counted as a
  second calibration point**, or one theorem is double-counted as two independent bridges.
- **§2.approximation** — Baker 1994 is **planar-only**, over exactly seven named problems, ratio k/(k+1)
  (max) / (k+1)/k (min); "minor-free" requires the chain Eppstein 2000 → Grohe 2003 → DeVos et al. 2004 +
  DHK 2005. Crucially the ceiling is **not uniform**: minor-bidimensional → H-minor-free, but
  **contraction-bidimensional → apex-minor-free only** (contraction-bidimensionality is *undefined* for
  general H-minor-free classes — CJ 2008 fn. 1). Two "broad family" characterizations exist (DGKS LICS 2006;
  bidimensional+separation) and are **explicitly incomparable**; neither extends to MSO (planar
  3-colourability is MSO-definable and NP-hard).
- **§2.parameterized** — 2^O(√k)·n^O(1) and the shared grid-theorem engine are correct, but the **FPT side
  assumes strictly less**: the PTAS side additionally needs the separation property, an α-approximation
  subroutine, and a treewidth approximation.
- **§6.kernel** — "FPT ⟺ some kernel" is **false without decidability** (plus non-triviality), and g(k) is an
  **arbitrary computable** function, so the equivalence "carries no efficiency content; it is a restatement,
  not a preprocessing guarantee." **Polynomial** kernelization is strictly stronger and *not* equivalent to
  FPT (k-Path). This **vindicates Mosaic P6's design**: the informative residual really is poly vs no-poly
  *within* FPT.
- **§7.self_reducibility** — Ajtai's worst-to-average is **one-directional**, holds for γ = n^O(1)
  *approximation* versions over an **engineered** distribution; permanent RSR needs |F| ≥ deg + 2 and
  tolerates only 1/poly error.
- **§7.ogp** — OGP parameters are ensemble constants; barrier proofs need e-OGP/m-OGP over *sets* of
  correlated instances; the conclusion excludes only stable/insensitive algorithms, **not P**. Pinnable
  ensemble-typed representative recorded: Gamarnik–Sudan, *Ann. Prob.* 2017, Thms 2.5/2.6.

### 9.4 Operational consequences for Anatomy v1

1. **`engine_type` may cite §3 only in its corrected form** (§9.2b) — the algebraic characterization with
   its core + all-singletons hypotheses, never the definitional gloss.
2. **`kernel_status` may cite §6 only in its corrected form** (§9.3) — and the coverage-conditioning entry
   in `Anatomy-SCHEMA.md` §6 already records that the poly/no-poly residual within FPT is the only
   informative contrast.
3. **`decomposition_facts` must carry the class ceiling per problem type** (§9.3, §2.approximation):
   H-minor-free vs **apex**-minor-free is a real distinction and belongs in the cited record.
4. **No column may cite §1.counting, §5.approximation, or §7.ogp** — they are UNPINNED; per SCHEMA §3.6 the
   citing cell falls back to `open` rather than borrowing an unverified warrant.
5. **§1.decision and §1.parameterized-tw count as ONE calibration point, not two.**

### 9.5 §1.counting — resolved 2026-07-24, after the S0 seal commit (dated addendum, not a silent edit)

The re-pin returned. **Status: PINNED-WITH-CORRECTION.** The decisive question — treewidth or clique-width —
has a two-part answer, and a citation hazard sits underneath it.

**The citation is ambiguous between two different CMR papers, and only one is right:**
- ✅ Courcelle–Makowsky–Rotics, *"On the fixed parameter complexity of graph **enumeration** problems
  definable in monadic second-order logic"*, **Discrete Applied Mathematics 108(1–2):23–52, 2001** — the
  counting paper. This is the correct anchor.
- ❌ Courcelle–Makowsky–Rotics, *"**Linear Time Solvable Optimization** Problems on Graphs of Bounded
  Clique-Width"*, **Theory of Computing Systems 33(2):125–150, 2000** — optimization on clique-width, and
  **explicitly forbids edge-set quantification**. If the ledger's string resolves here, the row is
  MIS-ATTRIBUTED.

**Answer to the open question: BOTH, asymmetrically** (DAM 2001 abstract, verbatim): bounded **treewidth** →
polynomial time **with edge-set quantification allowed** (MSO₂); bounded **clique-width** → only when the
decomposition is poly-time computable **and** the formula has **no edge-set quantification** (MSO₁).

Four precision corrections:
1. **"Linear time" is model-dependent and mildly overstated.** ALS 1991 claims linear for *decision* and for
   optimization with constant-bounded weights; **counting** is claimed "in linear time **or** polynomial or
   pseudopolynomial time" — linear only under unit-cost arithmetic. CMR 2001's own abstract says
   **polynomial**, not linear.
2. **The decomposition is assumed given** in ALS (explicit in the journal abstract), in CMR's clique-width
   half, and in every FMR theorem. Removable at fpt-linear cost for treewidth (Bodlaender); **not** removable
   for clique-width (only Oum–Seymour approximation).
3. **FMR's graph representation is load-bearing**: the 4^k treewidth bound is on the **incidence** graph
   (Thm 1.3); the clique-width bound needs the **signed** incidence graph (Thm 1.8), and the *unsigned* case
   was explicitly left unproved (Remark 6.13).
4. **The sharp modern constant is 2^k, not 4^k** — Slivovsky–Szeider, SAT 2020 — and it is **optimal under
   SETH**.

**A mis-attribution to avoid before anyone makes it:** Lokshtanov–Marx–Saurabh 2011 does **not** state a
lower bound for SAT or #SAT parameterized by treewidth. CNF-SAT is their *hypothesis*, not their
*conclusion*; their catalogue covers Independent Set, Dominating Set, Max Cut, OCT, q-Coloring, Partition
Into Triangles. The #SAT-by-treewidth optimality claim is the direct SETH embedding, as invoked by
Slivovsky–Szeider.

**Cleanest anchor pair** if a single strongest citation is wanted for "MSO counting is FPT by treewidth":
**Courcelle–Mosbah 1993** (TCS 109(1–2):49–82, the semiring/evaluation framework) + **Courcelle–Engelfriet
2012, Theorem 6.56** (canonical modern statement: fp-**linear** for treewidth/CMS₂, fp-**cubic** for
clique-width/CMS — the same asymmetry). Keep ALS 1991 for the EMSO-with-arithmetic flavour. Note
Langer et al.'s caution: ALS and Courcelle–Mosbah are **orthogonal** — neither subsumes the other.

**Revised tally: 15 cells — 3 pinned clean, 10 pinned with correction, 2 unpinnable**
(§5.approximation, §7.ogp).

### 9.6 Second independent pass — corroboration plus three further corrections

A second pass ran on §1.counting / §2.approximation / §2.parameterized from primary full texts (CMR 2001
from Courcelle's author-hosted PDF; FMR 2008 Elsevier proof; DFHT JACM 2005; DH *Computer Journal* 2008).
It **independently reproduced** every correction in §9.2–§9.5 — the CMR two-paper hazard, the
H-minor-free/apex-minor-free split, the separation-property extras, the signed-vs-unsigned incidence
distinction. Two independent passes converging on the same corrections is the strongest evidence the
corrections are right. It also found three things neither pass had:

1. **"Enumeration" is itself an overstatement — in §1.counting's own wording.** The ledger row reads "MSO
   counting/**enumeration** tractable at bounded tw." CMR's **footnote 4** warns that the term "might be
   misleading, as we do not enumerate the solutions but we count them." No anchor supports enumeration in
   the delay-bounded sense. **Corrected wording: counting/evaluation, not enumeration.**
2. **CMR 2001's theorem numbers, and who actually owns the treewidth side.** Theorem 32 = bounded
   **treewidth**, MSO₂, **linear** time (so the abstract's "polynomial" is the weaker umbrella covering both
   halves; the treewidth half is linear). Theorem 31 = bounded **clique-width**, MSO₁, plus the poly-time
   parse-tree hypothesis. Decisively, **CMR introduce Thm 32 as "a generalization of the main theorem of
   [29,2]"** — Courcelle–Mosbah 1993 and ALS 1991 — which confirms the §9.5 recommendation from the other
   direction: **Courcelle–Mosbah is the better treewidth anchor, and CMR's own novelty is the clique-width
   side.**
3. **§2.parameterized: DFHT's *general framework* theorem is BOUNDED-GENUS, not H-minor-free.** On
   H-minor-free graphs DFHT deliver only dominating set, vertex cover and set cover at 2^O(√k)·n^h; the
   general H-minor-free statement rests on the *later* linear grid-minor theorem (Combinatorica 2008), not
   on DFHT itself. Also the side condition is **h(w)·n^O(1) with subexponentiality needing only
   h(w) = 2^{o(w²)}** — strictly weaker than the ledger's (and §9.3's) 2^O(tw). So "same machinery"
   overstates twice over: only the grid-minor theorem and the parameter–treewidth bound are shared.
4. *(§2.approximation, minor)* the DeVos et al./DHK low-treewidth-partition route is, in Demaine–Hajiaghayi's
   own words, **"effectively limited to deletion-closed problems"** — another place the unqualified
   "broad families" leaks.

### 9.7 Terminal statuses and verdict revisions (owner rulings, 2026-07-24)

**The epitaph, recorded verbatim because it is the honest one:**

> **Directionally right everywhere, precisely right almost nowhere.**

That is what a memory-cited proven-cell matrix looks like measured at theorem-statement resolution, and
pin-before-net converted it from a latent embarrassment into fifteen corrected cells **before a single
column cited anything**.

**(a) The two structurally unpinnable cells revert to OPEN.** *Unpinnable-as-stated* is a **legal terminal
status** — the same family as the corpus-starved INSUFFICIENT verdict — and each is recorded with its
reason, because the reason is the finding:

| cell | prior verdict | now | why no single theorem statement carries it as phrased |
|---|---|---|---|
| §5.approximation | "NETTED as mechanism; OPEN as per-row predictor" | **OPEN** | Dinur's Preprocessing Lemma *manufactures* the expansion hypothesis on **any** constraint graph, so no instance is excluded for lacking it or charged for having it. Expansion cannot discriminate rows on this route **at all**; the deliverable is class-level NP-hardness of gap-3SAT, not an instance charge. |
| §7.ogp | "islands … ensemble-typed" | **OPEN** | OGP's parameters are ensemble constants; the barrier proofs need e-OGP/m-OGP over *sets* of correlated instances; and the conclusion excludes only **stable/insensitive algorithms, not P**. Ensemble-typed, not row-typed — the ledger's own call, confirmed. |

**(b) The ISLAND coastline moves inward — and this changes what the extrapolation bets extrapolate *from*.**
§2's islands were drawn wider than the pinned theorems support, in two independent ways:

- **DFHT's *general framework* theorem is BOUNDED-GENUS, not H-minor-free.** On H-minor-free graphs DFHT
  deliver only dominating set, vertex cover and set cover at 2^O(√k)·n^h; the general H-minor-free statement
  rests on the *later* linear grid-minor theorem (Combinatorica 2008), not on DFHT.
- **The side condition is h(w) = 2^{o(w²)}, not 2^O(tw)** — strictly weaker than the ledger drew it.
- Plus the class split already recorded: minor-bidimensional → H-minor-free, but **contraction-bidimensional
  → apex-minor-free only** (undefined for general H-minor-free, CJ 2008 fn. 1).

**Consequence:** an ISLAND cell is a licence to bet on *off-island extrapolation*, so the island's boundary
is load-bearing. G0's island bets must be drawn against the **pinned** coastline, not the remembered one.
Recorded into the grid's I-phase notes (`docs/specs/mosaic-v3-grid-Iphase-flags.md`, Flag 4).

*Remaining verification gaps on this pass:* Baker's JACM full text and ALS 1991's full text are both
paywalled — Baker's seven-problem list and running-time form rest on Demaine–Hajiaghayi's Encyclopedia entry
about that exact paper, and ALS's content on consistent secondary renderings **plus CMR's own primary-source
characterization of its reference [2]**. All six anchors' bibliographic details check out against
CrossRef/DBLP.

*Verification gaps carried forward (recorded, not hidden):* Bodlaender–Hagerup theorem numbers are from the
Utrecht full version (SIAM returns 403; abstract matches verbatim); Cai–Lu–Xia numbering is from arXiv, not
SICOMP 2017; Baker's internal theorem numbers were not seen (ACM DL blocked) and the O(8^k·k·n) constants
are attributed-but-unverified — use 2^O(1/ε)·n^O(1); no numbered Cygan et al. theorem exists for the
H-minor-free/apex generalization (only p. 210 prose) — use Combinatorica 2008 Cor. 3 or CJ 2008 Thm 8.1.
