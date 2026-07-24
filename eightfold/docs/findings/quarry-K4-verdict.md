# Quarry K4 — Verdict note + Atlas v3 recommendation

**Date:** 2026-07-23  **Gate:** K4  **Spec:** sealed `hardmap@f74023ac4`.
**Ties:** K1 ([source verdicts](quarry-K1-source-verdicts.md)), K2
([intersection](quarry-K2-intersection.md)), K3 ([pilot](quarry-K3-pilot.md)).

**Framing honesty (the through-line, restated because it governs the recommendation):** every row
Quarry adds *sharpens canon statistics* — tighter Cramér's V, a fatter complete-case block, better-
populated occupancy cells. **It does not touch the canon-vs-computation question** (F1); more famous
rows deepen the canon bias. Quarry's value is **precision, never de-biasing.** The recommendation is
sized to buy precision where it is cheap and real, and to decline it where it is dear or illusory.

---

## Outputs 1–3 in one paragraph

**Sources (Output 1):** reductions.network is real and **machine-readable** (structured Markdown in a
public GitLab repo, BibTeX citations on both problems and reductions) — **not** assertions-only, so
kill-criterion 1 never fired. Its live data is **inaccessible from this environment** (arXiv
reachable, RWTH GitLab not); its persistent anchor is arXiv:2511.04308. The fork resolved **per
column**: reduction edges are value-citations for `decision` and `approximation` (cheap join), leads
only for `counting`/`parameterized` (F-1 / membership judgment remains). Three of six sources
(Crescenzi–Kann, GHR, Downey–Fellows) are already mined for the 118; the genuinely new supply
(reductions.network's cross-class + parsimonious sub-graph, de Haan–Szeider, Schaefer–Umans) is
concentrated in the atlas's thin/empty columns. **Candidates (Output 2):** 37 curated, **31
multi-charge** (pool ≫ 30), screened against §3 with S2 dedup applied. **Pilot (Output 3):** 10
rows through the full 9-check R20 pass, schema-valid, `claimed`, **0 folklore**, emitted beside the
byte-frozen atlas.

## Output 4 — the cost number

**Agent-draft cost:** **≈ 1.3 min/row (0.021 h/row)** to draft + schema-validate a `claimed` row.
Cheap — the agent compresses *drafting*.

**Cost is per-CHARGE, and the pilot empirically confirms the K1 per-column model:**

| column | K1 prediction | K3 outcome | verdict |
|---|---|---|---|
| `decision` (NPC/P) | STRONG — edge+membership = value | 0 corrections (Karp/GJ/GHR clean) | **cheap, reliable** |
| `parallelization` (P-complete) | thin; GHR clean | 0 corrections | **cheap, reliable** |
| beyond-NP `decision` (PH/PSPACE) | thin; high-value | **1 error caught** (Σ₂ᵖ→Π₂ᵖ semantics) | **high-value, error-prone** |
| `approximation` | STRONG (gap edges) but staleness | F-2 vocab tension + UGC-conditional + currency | **medium, judgment-heavy** |
| `counting` | MODERATE — leads only, F-1 | **downgrade to `open`** (subgraph-iso) | **dear, low yield** |

**Confirm-cost multiplier (refinement 2):** 3 cells hand-checked = **28 s/cell** vs 34 s/cell draft →
agent confirm/draft ≈ **0.8×**. But the number that matters is the **error rate: 1 of 3 spot-checked
cells was wrong.** Drafting compresses; **judgment does not.** The *paired-human* confirm cost (the
spec's 1.5 h/row frame) is a **larger, unmeasured** factor — the owner's confirm-pass is what sizes
it, and the 1/3 error rate proves it is load-bearing, exactly the constraint that stopped A2 at 118.

**Kill-criterion 2** is **not tripped at the agent-draft level** (0.021 ≪ 1.5 h/row), but the pilot
makes **no claim** that the human 1.5 h/row bar is cleared — that measurement is the owner's.

## Gap-list update (dated, per spec §7)

**2026-07-23 — one verified gap fill.** `abstract-argumentation` (skeptical acceptance under preferred
semantics, **Π₂ᵖ-complete**, FPT by treewidth) occupies the previously-empty occupancy cell
`decision=PH-complete × parameterized=FPT`. Recorded as a gap-list datum now, ahead of any v3.
(The three `sharp-*` gap-hints from K2 were **falsified** — that cell is already occupied.)

## Output 5 — Atlas v3 recommendation

**EXPAND-NARROW.**

Not *don't* (the thin columns — counting 43%, parallelization 46%, beyond-NP decision 7 rows — gain
real precision, and occupancy gaps like the argumentation cell are fillable). Not broad *expand* (the
pilot confirms the binding constraint is unchanged since A2: **verification judgment, not row
supply** — a broad sweep would blow the confirm budget on the dear columns, and the 1/3 error rate
says every row still needs the owner's confirm-pass). **Expand narrowly, column-prioritized by the
cost model:**

1. **First — `parallelization` + decision-led multi-charge rows** (cheapest, 0-correction columns).
   GHR's un-mined P-complete problems (LFMIS, path-system, AGAP, CFL-membership, unification…) and the
   reductions.network `decision`/`approximation` join. High reliability per confirm-hour.
2. **Second — beyond-NP `decision`** (de Haan–Szeider, Schaefer–Umans). Highest *precision* value (it
   fattens the sparsest column and fills occupancy gaps), but **confirm each carefully** — this is the
   error-prone column (semantics/level precision; the Σ₂ᵖ↔Π₂ᵖ trap).
3. **Last / selective — `counting`** (hold to the per-problem F-1 bar; expect many `open` downgrades —
   the folklore-gap lesson) and **`approximation`** (re-verify Crescenzi–Kann currency vs post-2000
   results before trusting any pre-2005 value).

**Row target the cost supports:** size to the **owner's confirm budget, not the agent's draft speed.**
A **narrow ~20–30-row Atlas v3 batch**, front-loaded on columns 1–2 above, materially fattens the
thin columns and adds occupancy cells (≈ the argumentation gap-fill) while staying inside a confirm
budget comparable to what produced the 118. Drafting all ~30 is hours of agent time; **confirming them
is the real project** — and it is the owner's, not the agent's. Two preconditions sharpen the cheap
path before v3: (a) get reductions.network's data locally (owner `git clone` of
`reductioncompendium/data`, or env egress) to turn the decision/approximation join from documented-
coverage into an exact file-level join; (b) treat every agent-draft value as `claimed`-pending-confirm
— the pilot's error rate makes the confirm-pass non-optional.

## K4 done-gate

- **Outputs 1–5 delivered** ✓ (K1–K3 findings + this note + the parquet-substitute JSONL/CSV data).
- **Atlas v3 recommendation stated with a cost-supported row target** ✓ (expand-narrow, ~20–30 rows,
  column-prioritized, confirm-budget-sized).
- **Gap-list update recorded, dated** ✓.
