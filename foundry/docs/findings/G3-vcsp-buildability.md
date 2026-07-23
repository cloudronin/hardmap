# G3 — Is VCSP the roster with room? (I-phase memo)

**Status:** Investigation memo. Literature + feasibility only. No roster, no measurement, no prereg. Parallel-safe —
touches no Lattice artifact, amends no sealed prereg. **Discipline:** R20 (classifications pinned from primary sources;
the I-H4 witness must be reader-checkable). **Timebox 3h;** the two load-bearing items (I-H2, I-H3) resolved inside
~40 min, so the verdict is on the merits, not by timebox.

## The three possible verdicts (declared before investigating)

| Verdict | Meaning | Consequence |
|---|---|---|
| **BUILDABLE-WITH-ROOM** | both charges assignable from independent sources, witness passes, population materially exceeds Lattice's ~30 | Lattice respecced on VCSP; Boolean becomes a calibration subset |
| **BUILDABLE-BUT-NO-BIGGER** | oracles exist but classified population comparable to Boolean | no advantage; proceed with Lattice as specced |
| **NOT BUILDABLE** | no parameterized oracle for valued objectives, or partitions coincide | VCSP route closed; Lattice proceeds at ~30 rows with limits stated |

## Verdict: **NOT BUILDABLE.**

VCSP is a *larger population measured with blunter instruments*, and on the axis that matters it has no instrument at
all. In one paragraph:

- **The parameterized axis has no oracle (I-H3, decisive).** There is no named FPT/W[1] dichotomy for *valued*
  objectives under a solution-size parameterization — the analog of Bulatov–Marx that Lattice's parameterized charge
  rests on. The finite-domain VCSP *decision* borderline (P vs NP-hard) is fully classified, but the corresponding
  **FPT/W[1] borderline is an open research frontier** ("big gaps"; the newest work is titled "*Towards* a
  Classification for Parameterised VCSPs"). An open frontier is not an invocable oracle. The axis reads `open` → the
  gradient cannot be carried.
- **The approximation axis only dichotomizes (I-H2).** Thapper–Živný classify finite-valued CSP into an
  **exact-solvability dichotomy** — poly-time (by the Basic LP relaxation) or NP-hard — *not* a stratification. No
  classification assigns a stratified approximation class (PTAS / APX / poly-APX / inapprox) to generated valued
  languages; the conservative case's hard side is uniformly APX-complete. A *binary* approximation charge is coarser
  than Lattice's four-way KSTW Max-Ones/Min-Ones.
- **So the witness fails (I-H1).** Vertex-cover (APX-complete) and independent-set (poly-APX-hard) collapse to the
  *same* value under a binary approximation charge — not "opposite on both axes" — and the parameterized axis can't
  separate them either (no oracle). The scheme cannot exhibit the phenomenon it would measure.
- **The size premise is undercut.** Distinct (approx × param) profiles — the quantity kill #2 cares about — are bounded
  by **(approx granularity) × (param granularity)**, not by row count. VCSP's continuum of cost functions buys nothing
  when the approximation charge has two values and the parameterized charge has none. "Room to grow" in population is
  not room to grow in *profiles*.

## I-H1 — the witness test (runs first). **FAILS with VCSP-native charges.**

VCSP subsumes Min-Ones/Max-Ones, so vertex-cover and independent-set are *expressible* as valued problems — the pair
exists structurally. But the witness requires them to take **opposite charges on both axes**, and with the VCSP-native
classifications they do not: the approximation charge (I-H2) is binary and assigns both the "hard" value, and the
parameterized charge (I-H3) does not exist. A pipeline that assigns the witness pair the same approximation value, and
no parameterized value, "cannot exhibit the gradient and the memo stops here" (spec §2). It stops here — the remaining
items document *why* it is a root-cause failure, not a fluke of one scheme.

## I-H2 — the approximation charge. **Exact dichotomy, not a stratification.**

Pinned from the Jeavons–Krokhin–Živný survey (primary): the Thapper–Živný result is an **exact-solvability dichotomy**
— VCSP(Γ) is poly-time solvable (Γ solvable by the Basic LP relaxation) or **NP-hard**, with a clean algebraic
criterion (fractional polymorphisms / the "no-XOR" condition). The survey's approximation section produces **no theorem
assigning approximation-hardness classes** to valued languages. The one sharp approximation statement in the literature
is for the **conservative** case (Γ contains all unary cost functions): the intractable side is **APX-complete** — a
single class, not a hierarchy. So the VCSP approximation charge, where it exists at all, is **PO vs APX-complete/NP-hard:
binary.** Per the owner's own ruling for Lattice — a flattened approximation axis "discards the signal the test is
looking for," because the gradient is a claim about *ordered* approximability tracking parameterized status.

## I-H3 — the parameterized charge (the predicted blocker). **No oracle. Open frontier.**

Pinned from the same survey and the current literature: there is **no parameterized-complexity dichotomy (FPT vs W[1])
for valued objectives under a solution-size / number-of-nonzero parameterization.** The survey does not cover it; the
field states plainly that while the finite-domain VCSP P/NP borderline is fully known, "there are **big gaps** in our
understanding of the corresponding **FPT/W[1] borderline**," and the most recent work (2025) is explicitly framed as
"*Towards* a Classification for Parameterised VCSPs" — i.e. not done. The Bulatov–Marx solution-size dichotomy that
Lattice invokes is a **crisp** result (`{0,1}`-valued relations, number of ones); its valued-objective analog is
precisely what does not yet exist. **The parameterized axis reads `open` → VCSP cannot carry the gradient test.** This
is the death the spec predicted.

## I-H4 — source independence. **Moot.**

The tautology check ("do the two partitions provably disagree on a generated case, as KSTW and Marx do on the affine
cell?") cannot even be run: with no parameterized oracle (I-H3), there is no second partition to compare against the
approximation partition. Independence is undefined when one of the two classifications is absent.

## The question behind the question (spec §4) — the pattern is now the finding

Four generated rosters have hit the same wall from four directions:

| roster | wall |
|---|---|
| **census** | charges from one polymorphism fingerprint ⇒ the correlation is an identity (Task 0, residual 0) |
| **Ferry** | the canon's gradient rows have no local constraint relation (31 of 47 `n.a.`) |
| **Lattice** | both charges exist and disagree, but the reachable population is ~30 rows — a small census |
| **VCSP (G3)** | larger population, but the parameterized axis has no classification and the approximation axis only dichotomizes |

The recurring wall is itself a result worth writing, not an accumulation of separate disappointments:

> **The approx⟷param gradient lives in a population that generation cannot reach.** Its home is curated optimization
> problems with *global* objectives — Steiner, TSP, knapsack, set-cover — precisely the class for which no
> classification theory (Schaefer, KSTW, Marx, Thapper–Živný) provides *both* an approximation and a parameterized
> charge from independent sources. Every generated alternative is either theorem-tautological (census), structurally
> mismatched (Ferry), too coarse (Lattice), or classification-less on one axis (VCSP). Bias-free rostering can reach
> the *constraints* and, for crisp CSP, the *objective* — but not the *global* objective where this particular coupling
> actually lives.

*(This paragraph is promoted to its own standalone finding — `docs/findings/generation-cannot-reach-the-gradient.md` —
per owner direction; it is the more durable artifact.)*

## Consequence

**VCSP route closed.** Lattice is not respecced; it proceeds as specced at **~30 rows, Boolean, Max-Ones/Min-Ones**,
with its resolution limits stated up front (kill #2 remains live). VCSP does not offer more resolution — it offers
fewer distinct profiles behind a much larger but uninstrumented population. Lattice is not merely the available
outside-the-canon test but the **best** one: crisp CSP is the only generated setting where *both* charges have named,
independent, present oracles (approximation stratified by KSTW, parameterization by Bulatov–Marx).

## Sources (R20 — primary, reader-checkable)

- J. Thapper, S. Živný, *The complexity of finite-valued CSPs*, JACM 63(4), 2016 (STOC 2013) — the finite-valued exact
  dichotomy (BLP-solvable or NP-hard). [arXiv:1502.07327 companion / preprint `cs.ox.ac.uk/standa.zivny`]
- V. Kolmogorov, A. Krokhin, M. Rolínek, *The complexity of general-valued CSPs*, SICOMP 46(3), 2017 (arXiv:1502.07327)
  — general-valued dichotomy (still exact P vs NP-hard).
- P. Jeavons, A. Krokhin, S. Živný, *The complexity of valued constraint satisfaction* (survey, BEATCS 2014; `jkz14`
  preprint) — confirms exact-dichotomy scope; **no** approximation stratification; **no** parameterized-by-solution-size
  classification.
- V. Kolmogorov, S. Živný, *The complexity of conservative valued CSPs*, JACM 60(2), 2013 — conservative case;
  APX-completeness of the intractable side (a single class).
- *Symmetric Parameterised Holants on Hypergraphs: Towards a Classification for Parameterised VCSPs*, arXiv:2508.19794,
  2025 — evidence the parameterized VCSP classification is still **open** ("Towards").
- A. Bulatov, D. Marx, *Constraint satisfaction parameterized by solution size*, SICOMP 43(2), 2014 (arXiv:1206.4854)
  — the **crisp** solution-size dichotomy VCSP lacks a valued analog of.
- In-repo: `foundry/foundry/domain3.py` (`approximation_d3` / `_semilattice_closed`) — the program's only VCSP-adjacent
  code is a *partial Thapper–Živný PO sufficient-condition* oracle for domain-3 Max-CSP, returning `PO` or `None` — i.e.
  it too only certifies the tractable side, never a stratum. Authorizing memo: `foundry/docs/findings/G1-buildability.md`.

**Net:** G3 closes the VCSP route and, with it, the search for a roomier generated roster. The four-wall pattern is the
durable takeaway. Lattice stands as the outside-the-canon test — at ~30 rows, with its resolution limits stated, exactly
as the G2 plan specifies.
