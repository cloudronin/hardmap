# Frontier Map — Note (banked idea, post-grid sequel)

**Status:** Idea note, banked 2026-07-24. Not a spec; specs only after Mosaic v3's prediction 4
lands. Origin: owner question — can a Monte Carlo over feature space, plotted through the bridge
model, bear on P vs NP?

## 1. The honest scope line, first

**This cannot touch P vs NP, and the note exists partly to record why.** Every hardness label the
bridge model trains on is conditional on the standard conjectures — an NPC cell means "hard *if*
P≠NP." A model fit on conditional labels outputs interpolations of the assumption; sampling its
feature space redraws the assumption at high resolution. A sampled point "predicted P" on a known-
NPC anatomy is a model residual, never a discovery. P vs NP is a single universally-quantified
statement about all algorithms — the class of fact the charge-typing established as reachable only
by theorem. The bridge model is a compression of the field's theorems and cannot out-know its
training labels. Any writeup of this project leads with this paragraph.

## 2. What the idea actually is: a map of the conditional tractability frontier

Run Monte Carlo over anatomy space (the Anatomy v1 coordinate system, plus whatever the grid
validated); at each sampled feature vector, predict the full hardness *type* (the joint profile,
per the grid's joint estimator); plot. The output is the **geometry of the conditional boundary**:
which feature combinations sit deep in easy territory, which deep in hard, where the boundary
surfaces run, and how sharp they are.

### 2.1 The boundary-sketch objective (owner ruling, 2026-07-25)

The map's primary product is the **sketched P/NPC boundary in anatomy space**, and the program
trains for boundary accuracy deliberately:

- **Boundary-weighted training is declared legal:** oversample near-boundary classes (boundary
  distance = minimum tuple-edits to flip the engine predicate, a derived quantity,
  census-checked) so model capacity concentrates where the line lives. Training curriculum is
  free; holdout scoring stays population-honest and sealed.
- **The sketch is gradeable on surveyed coastline:** Zhuk's criterion *is* the exact boundary on
  CSP territory, so sketched-vs-true overlays score exactly across the 4,072. The cartographer's
  license is earned there before any unsurveyed sketch means anything.
- **Ladner is the legend, not the obstacle:** off the dichotomy islands the boundary provably
  smears (intermediate problems exist if P≠NP; the atlas's NPI rows are the suspects). The
  honest artifact is a **sharpness map**: where the boundary is exact (dichotomy territory,
  validated), where it provably isn't a line (Ladner country — the model's calibrated
  uncertainty should inflate there, testable on the NPI rows), and where sketched sharpness is
  itself the conjecture output. Boundary-sharpness across anatomy space is an unclaimed
  artifact.

## 3. The three products

1. **Boundary sharpness as a measured object.** Within finite-domain CSPs the dichotomy theorems
   make the P/NPC boundary *exact* (Zhuk's proof describes it algebraically) — the "basis is
   anatomical" claim already proven on an island. The map is validated where oracles exist
   (predicted boundary vs algebraic boundary — theorem-grade ground truth) and is
   conjecture-generating cartography in feature directions no dichotomy covers.
2. **Disagreement mining.** Every *realizable* sampled vector (corresponds to a constructible
   relation) can be oracle-graded. Model-vs-theorem disagreements are either model errors
   (instructive) or regions where anatomy underdetermines fate (more instructive — a missing
   feature lives there).
3. **Impossible-anatomy regions.** Sampled vectors whose predicted profile lands in a
   theorem-forbidden occupancy cell mark incoherent feature combinations or bad extrapolation —
   the B4 forbidden-cell check run against the *model* instead of the atlas.

## 4. Discipline riders (written now so the future spec inherits them)

- **Realizable vs unrealizable typing is mandatory.** Predictions on unrealizable feature vectors
  are extrapolations with no ground truth ever; they plot as model output, clearly typed, never
  as claims about problems.
- **Post-grid gate:** a frontier map drawn by an unvalidated model is decoration. The project
  specs only after the grid's prediction 4 (joint-profile holdout) lands; the map's headline
  claims inherit that validation and its limits verbatim.
- **Netting:** boundary segments forced by theorems (dichotomy criteria, Bridge Ledger NETTED
  cells) are drawn as *proven*, visually and statistically distinct from *predicted* segments —
  the two-atlas discipline (proven vs measured bridge cells) applied to cartography.
- **The k\*=1 connection, stated once:** if the map is accurate where checkable, the reading is
  that hardness types are irreducible among themselves but generated from anatomy — the vector
  has no internal basis because its basis is anatomical. If joint prediction collapses while
  marginals hold, the charges have independent anatomical drivers. Either way the map is the
  k\*=1 finding's interpretation made visible, not a new claim beyond the grid's.

## 5. One line for the writeup queue

Not "an approach to P vs NP." The best available map of the territory the question lives in:
the conditional frontier across all of anatomy space, validated against the dichotomy theorems
where they exist, extended as measured prediction where they don't.
