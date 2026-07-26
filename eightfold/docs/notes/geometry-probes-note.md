# Geometry Probes — Note (banked idea: measured feasible-region analysis)

**Status:** Idea note, banked 2026-07-25. Not a spec. One cheap thread (the Boolean qualification
study, §4) is executable now; everything else waits on its verdict and on program posture
(registry-plus-writeup governs active hours).
**Origin:** owner reframe — closure analysis is feasible-region analysis; convexity IS a closure
property (blend-stability of the region); the program's negatives say the region's geometry is
invisible from constraint syntax. These probes measure the geometry directly instead of deriving
it, reaching rows the algebra cannot admit.

## 1. The two instruments

**Probe A — blend-violation (empirical blendability).** For an instance ensemble of a problem:
sample solutions, apply the canonical blending operations (majority vote; affine combination
a−b+c; semilattice meets), measure the **violation rate** — the fraction of blends that leave the
feasible region. Direct geometric probe of the solution space. Works wherever instances can be
generated and solutions enumerated/sampled — including prose-encoded rows Marrow's admission bar
excludes. Measures *degree* of blendability, the intermediate the yes/no algebra cannot express
("almost majority-closed" is a real and possibly load-bearing category).

**Probe B — relaxation tightness (the imported OR diagnostic).** Solve LP relaxations of sampled
instances; measure integrality gaps — distance of the region from its convex hull. Theorem
anchors exist at ISLAND grade (Sherali–Adams/Lasserre hierarchy results tying relaxation
tightness to approximability), and the probe targets exactly the charge (approximation) carrying
the program's one robust structural association (the 0.56 split).

## 2. Typing (all standing law, applied not invented)

- **Ensemble-typed, instrument-based** — both probes live beside the landscape charge: declared
  ensembles, seeds, instrument manifests; values are properties of (problem, ensemble), passport
  verdict `parameter-relative`.
- **F2 law verbatim:** probe values never impersonate worst-case charges. A low violation rate on
  an ensemble is not a tractability claim; it is a measured geometric property that may
  *associate* with charges — the association is the research object.
- **Netting:** on rows where the algebra proves closure, probe agreement is calibration credit,
  never discovery (the standing rule; here it is also the qualification design).

## 3. What they buy that nothing else does

- Geometry for the inadmissible rows: varying-template, unbounded-arity, prose-encoded — the
  population Kill 1 excluded (311 of 345), probed directly.
- A continuous blendability scale where theorems give a binary — the "almost-closed" middle is
  exactly where intermediate hardness should live if it lives anywhere.
- Registry features: future predict-then-fill waves can carry geometry-feature predictions
  beside closure and surface ones, so eventual hits attribute among three feature grades.

## 3.1 Reserved column: `pairwise_independent_support` (Probe B's theorem-grade sibling)

Relaxation-resistance has a *checkable certificate* (added 2026-07-25, owner exchange on which
problems relaxations provably cannot help):

- **The condition (Austrin–Mossel):** a predicate whose satisfying assignments support a
  balanced pairwise-independent distribution is approximation-resistant — the solution set
  impersonates randomness well enough that every low-degree continuous view (all LPs/SDPs)
  loses its grip. The closure story's evil twin: closure makes regions blendable and easy;
  pairwise-independent support makes them statistically featureless and relaxation-proof.
- **It is a finite LP feasibility check per predicate** — derivable, invariant-grade, same
  condition-check machinery as the engine column, with Austrin–Mossel as the PINNED bridge
  citation into the approximation charge. Under UGC the classification is complete
  (Raghavendra: the canonical SDP is optimal for every CSP), so the column's bridge upgrades
  from ISLAND to characterization if that conjecture resolves.
- **The generator, for roster or recruitment use:** any predicate passing the check,
  instantiated on expanders, is a certified relaxation-resistant problem — unlimited supply,
  the lower-bound literature's own industrial construction (Chan; Kothari–Meka–Raghavendra).
  Expansion is the same anti-feature already NETTED against Resolution (Ben-Sasson–Wigderson):
  it defeats local reasoning in every costume — proofs, propagation, and hierarchies alike.
- **Status: reserved, not built** — fill route named above; enters at the next schema seal per
  the F4 law; variance census before any bet, like everything else. Beside Probe B it completes
  the pair: measured gap (instrument) next to proven resistance (derived column), the two-atlas
  discipline applied to the continuous frontier.

## 4. The qualification study (the cheap thread — executable now, pure instrument science)

**On the 4,072-class Boolean roster, true closure is oracle-known for every relation** — the
strongest ground truth any instrument in this program has ever had. The study: run Probe A over
the roster (generation and solution enumeration are trivial at these sizes), and score:

1. **Known-answer battery:** majority-closed relations show ~zero majority-violation;
   affine relations ~zero affine-violation; each engine's signature operation near-silent on its
   own class. Failures are probe bugs by definition.
2. **Separation:** NPC-side relations show high violation on every flavor; the violation profile
   separates engine types at stated accuracy — the probe's measured resolution.
3. **The scientific freebie:** the *distribution* of violation rates across the roster — is
   blendability bimodal (closed vs broken, matching the dichotomy's binary) or does a real
   "almost-closed" middle exist? Either answer is a finding about the geometry the theorems
   binarize, and it costs nothing extra.

Sealed before running: the battery's pass thresholds, the separation metric, and the
INSUFFICIENT vocabulary. Box: 4–6 h paired, $0 compute. **Verdict gates everything downstream:**
qualified → the probe is licensed for natural-row ensembles with its accuracy characterized;
not qualified → the geometry-measurement route closes at instrument grade, recorded, and the
note stands as the map of why.

## 5. Placement and posture

The qualification study is the only near-term motion, and only when hobby hours exist — it
competes with the writeup, which currently outranks new instruments. Natural-row deployment
(sampler infrastructure, ensemble declarations, 15–25 h) is explicitly NOT committed by this
note and would require its own spec, sized after qualification and after the writeup ships.
The one-sentence case: the program proved the region's geometry is invisible from syntax;
these probes look at the region itself; the Boolean roster grades the looking before it is
trusted anywhere that matters.
