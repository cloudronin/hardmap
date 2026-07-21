# I1–I4 — Investigation (confirm before build)

**Status:** COMPLETE (Phase I). Feeds the A1 schema, the canonical-encoding field, and the locked coding in
`results/prereg/prereg_v1.json`. Spec §6; Build addenda R1–R9.

The four pre-build questions from spec §6, each resolved to a decision the rest of A1 depends on.

---

## I1 — Machine-readability of the source compendia (scrape vs transcribe)

**Crescenzi–Kann, *A Compendium of NP Optimization Problems*** — the primary source for charge 3
(approximation). Live on the web as structured HTML (KTH: `nada.kth.se/~viggo/problemlist/`, with a mirror at
`vlsicad.eecs.umich.edu/BK/Slots/cache/www.nada.kth.se/~viggo/problemlist/compendium.html`); >180 entries;
also the appendix of Ausiello et al., *Complexity and Approximation* (1999). Each entry is a fielded record
(instance / solution / measure / good-approximation results / hardness / comment), so it is scrapeable into a
normalized table — but the pages are old, hand-maintained, and inconsistent in markup.

**Complexity Zoo** (Aaronson) — `complexityzoo.net` (+ Waterloo mirror; a Chris Bourke LaTeX export
`cse.unl.edu/~cbourke/latex/ComplexityZoo.pdf`; a 2023 wiki dump on archive.org; Kuperberg's "Complexity
Zoology" inclusion diagrams). **Class-centric, not problem-centric**: it catalogs ~500 *classes* and their
containments, not a per-problem charge vector. It is a secondary reference for charges 1 and 5 (which class a
problem is complete for), never the primary row source.

**Decision.** *Transcribe by hand for the A1 pilot* (20 problems × 8 charges ≈ 160 cells): accuracy and
per-cell provenance dominate at pilot scale, and hand-entry forces the verification pass (R8). *Defer scraping
to A2*: a one-time scrape of the Crescenzi–Kann HTML into a normalized side-table is worth it at ~120
problems, but only as a fill-assist whose every imported cell still passes the validator gates and a spot
check — never a bulk trust import. Garey & Johnson (1979) appendix stays hand-transcribed (no machine source).
This matches spec §3.3 ("mine the compendia before paper-by-paper work") without importing their errors
wholesale.

**Snapshot every web-only source at transcription time (R10).** The KTH compendium is 1990s HTML already
cited through a third-party cache, and the Zoo wiki drifts — both are link-rot risks. Any cell citing a `url`
records a Wayback (or local `docs/sources/`) `snapshot` + `retrieved` date, and the validator enforces it
(gate 8). Prefer the stable anchors — Garey & Johnson (1979), Ausiello et al. (1999), and primary theorem
papers by DOI — so most cells need no snapshot at all.

## I2 — Prior art (is the charge-space framing unclaimed?)

Searched for a quantitative, multi-charge, per-*problem* atlas with structure detection. **Not found.** The
nearest artifacts are each a different thing:

- **Complexity Zoo** — the closest, and loosely called "the periodic table of algorithms," but it is a
  *class* menagerie organized by *inclusion relationships*, not a table of problems each carrying a vector of
  independent charges. It answers "what is class X and what contains it," not "what is the charge signature
  of problem Y."
- **Single-charge compendia** — Crescenzi–Kann (approximation only); the Existential-Theory-of-the-Reals
  compendium (one class); parameterized-complexity tables (Downey–Fellows / Cygan et al.). Each covers *one*
  of our eight columns, for a slice of problems.
- **Zimand, *Computational Complexity: A Quantitative Perspective*** — "quantitative" in the
  resource/measure-theoretic sense, not a problem atlas.
- **Structure-detection precedents worth citing, not competing artifacts:** the CSP dichotomy program
  (Schaefer 1978 → Bulatov / Zhuk 2017) is the closest existing *forbidden-region* result — a proof that a
  structured problem family occupies only certain hardness cells; fine-grained complexity (SETH / 3SUM / APSP)
  is a distinct hardness dimension (a natural v2 charge 9, R5).

**Verdict (stated as spec §6 I2 requires): not aware of prior work** on a curated multi-charge quantitative
problem atlas with occupancy/multiplet/gap analysis. **Caveat:** the framing (charges as independent axes,
problems as the unit) is, to our knowledge, novel *as an artifact*; the constituent facts are all standard
textbook/compendium results. We claim the table and its analysis, not the charge values.

**Novelty finding surfaced by curation (R14):** there is **no overlap-gap-property (OGP) theorem for proof
space** — the clustering/OGP program is about *solution* spaces. Proof Census measures freezing-style
structure (backbone strengthening, overlap concentration) of the *refutation set*, which has no rigorous OGP
analog in the literature. That absence is itself a finding; the atlas records the Census datum under a
distinct `freezing-measured` value rather than overclaiming `clustering-OGP-known`.

## I3 — Encoding discipline (charges shift under re-encoding; fix one canonical encoding per problem)

Charges can move under re-encoding, so each problem row pins a `canonical_encoding`; deviations are logged
per-cell in `provenance.note`. The standing conventions (R1/R3 make this load-bearing — a charge value is only
meaningful against the object and encoding it was stated for):

- **Numbers are binary, not unary.** FACTORING, SUBSET-SUM, KNAPSACK, PARTITION use binary-encoded integers.
  This is the difference between weak and strong NP-hardness and decides whether an FPTAS is even on the table
  (KNAPSACK: FPTAS under binary; the pseudo-poly DP is not poly in the binary size).
- **Graphs are simple, undirected, sparse (adjacency-list), size = (n, m)** unless the row says otherwise.
  Dense-vs-sparse encoding shifts parallelization and approximation framings; note any dense-encoding
  dependence.
- **SAT family = CNF, clauses as literal-lists**; k-SAT = exactly-k-literal clauses. HORN/XOR/2-SAT are the
  clause-shape restrictions of the same object.
- **Standard parameter for charge 4 = solution size** (VC by k, CLIQUE/IS by k, …) unless a different natural
  parameter is pinned in `perspective`.
- **Proof system for charge 6 = Resolution** unless `perspective` says otherwise (extended Resolution,
  Frege, …). Charge 6 attaches to an *unsatisfiable instance family*, not the decision problem (R1).
- **Ensemble for charges 7/8** = the standard random model, pinned per cell: random k-SAT at clause density α
  (threshold ≈ 4.267 for k=3); G(n, m)/G(n, p) for graph problems; planted models flagged as such.

## I4 — Ordinal-vs-categorical coding (pre-commit before A3; prereg carries the receipt)

Locked *principles* here; the exact per-charge coding is frozen in `results/prereg/prereg_v1.json` before any
`structure.py` run on real data (R7). To prevent post-hoc coding-to-taste (spec I4 / prereg discipline):

- **Association + dimensionality analyses treat every charge as categorical** (Cramér's V, MCA). No charge is
  forced onto a numeric axis; this is what lets H1 be about *effective* dimensionality rather than an imposed
  ordinal scale.
- **A natural partial order is recorded where one exists** (decision: P < NPC < harder; approximation:
  FPTAS < PTAS < APX-c < log-APX < poly-APX < inapprox) and used only for (a) the human-readable
  occupancy/gap narrative and (b) an *ordinal-coded sensitivity check* — the clustering must be robust to
  swapping categorical for ordinal coding (spec I4 sensitivity).
- **Sentinels are first-class categories, never imputed** (R2). `open`/`unmeasured`/`n.a.` each get their own
  MCA category in the full-table analysis; the complete-case sub-block drops any row/column carrying them
  (R4). `n.a.` (structural) and `open` (unknown) are distinct categories — collapsing them would manufacture
  false association.
- **`measured` cells (R9) are coded identically to their value** in the main analysis and removed in the
  `--drop-measured` ablation; the A3 verdict must survive that removal.

---

## Sources

- [Crescenzi & Kann, *Approximation on the Web: A Compendium of NP Optimization Problems* (RANDOM'97)](https://link.springer.com/chapter/10.1007/3-540-63248-4_10) — the compendium ([KTH mirror](http://vlsicad.eecs.umich.edu/BK/Slots/cache/www.nada.kth.se/~viggo/problemlist/compendium.html)).
- [Complexity Zoo (Aaronson)](https://complexityzoo.net/Complexity_Zoo) · [Bourke LaTeX export](https://cse.unl.edu/~cbourke/latex/ComplexityZoo.pdf) · [Template:ComplexityZoo (Wikipedia)](https://en.wikipedia.org/wiki/Template:ComplexityZoo).
- [Zimand, *Computational Complexity: A Quantitative Perspective*](https://www.amazon.com/Computational-Complexity-Quantitative-Perspective-North-Holland/dp/0444828419) — different sense of "quantitative."
- [*The Existential Theory of the Reals as a Complexity Class: A Compendium*](https://arxiv.org/pdf/2407.18006) — example single-class compendium.
