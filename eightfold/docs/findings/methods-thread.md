# Methods thread

Running log of methodological defects and the lessons they forced. The characteristic failure mode of
this program has a name: **metadata already recorded, inference not drawn** — the fact needed to avoid
the error was *already written down somewhere in the artifact*, and nobody joined it up. Entries are
dated and numbered continuously. (Instances 1–5 predate this file; 6 and 7 are recorded below at the
owner's direction, from the Atlas v3 V2 confirm-pass of 2026-07-23/24.)

---

## Instance 6 — 2026-07-24 — a drafter-prompt hint asserted as fact, inherited by four rows

**What happened.** In the wave-2 drafting prompt the orchestrating agent wrote, as an instruction:
*"argumentation, ASP, abduction, robust-csp, 3-coloring-extension are FPT by treewidth."* It was
partly false. The confirm-pass demoted **`robust-csp`** on *both* charges to `open` (no verified
classical Π₂ᵖ source; no treewidth result at all — CSP with unbounded domain is XP, not FPT, in primal
treewidth) and **`3-coloring-extension`**'s parameterized cell to `open` (the source parameterizes by
degree and leaf-counts, never treewidth). Four argumentation rows additionally cite the wrong paper
(Dvořák–Pichler–Woltran does not cover semi-stable/stage; Dvořák–Szeider–Woltran does).

**Why it is the characteristic mode.** The disconfirming metadata was already in the artifact: the
sources were *named in the candidate table* the drafters were told to read. One unsourced sentence in
a prompt outranked the recorded provenance for four rows.

**Lesson (new, and general).** **A factual assertion inside a drafter prompt is a citation without a
Check-9 gate.** Prompts are treated by drafters as authority, but nothing in the pipeline verifies
them the way it verifies a cell. Therefore: *any factual claim in a drafting prompt must itself carry
a source, or be explicitly marked conjecture for the drafter to verify.* Unmarked assertions in
prompts are now a defect class.

## Instance 7 — 2026-07-24 — a citation garble introduced at K3 propagated to three rows

**What happened.** The K3 pilot row `sharp-dnf` merged the two distinct 1979 Valiant papers into one
citation string. The confirm-pass found the same garble on `max-2sat`, `max-e3-sat`, and `sharp-dnf`.
#SAT-family completeness is *The complexity of enumeration and reliability problems* (SICOMP 8), **not**
*The complexity of computing the permanent* (TCS 8).

**Why it is the characteristic mode.** The distinction is recorded in the frozen atlas itself — the
`permanent` row cites the permanent paper, the `sat` row cites the enumeration paper. The artifact
already knew; the drafter reused a bad string instead of reading it.

**Lesson.** A pilot artifact is a **template**, and its defects are inherited at scale. Pilot rows
should get the confirm-pass *before* they seed a wave, not after — the 10 pilot rows here were
`claimed` and unconfirmed when they became the drafting gold standard.

## Instance 6–7 addendum — the agent as propagation vector

Both instances share a feature the earlier five did not: **the propagation vector was the agent
itself**, fanning one defect into many rows in minutes. Automation multiplies a single unverified
assertion by the fan-out width. The mitigation is not less fan-out but a gate on what enters a prompt:
see the Instance-6 lesson.

## Instance 8 — 2026-07-24 — a *written* constraint under-read (the inverse of 1–7), caught by the suite

**What happened.** The owner ruled: add a `superpoly-APX` rung *"in the **v3** vocabulary."* The agent
added it to the **shared kernel** vocabulary (`charges.py`). The frozen suite went **79 passed → 3
failed** (`test_factors::test_planted_recovered_null_quiet_rule_wellformed`,
`::test_null_parsimony_quiet_even_when_argmax_noisy`, +1). Reverted; suite green, `atlas.jsonl`
`6d53a4f1…` untouched. Correct design recorded in `prereg_v9-clarification-02`.

**Why it is the inverse of instances 1–7.** Those were *constraints supplied where none was written* —
an invented verification budget, a row-count cap, a narrowing recommendation, a resurrected preprint
gate, a prompt hint asserted as fact. This one is the mirror image: **a constraint that WAS written,
under-read.** "v3 vocabulary" scoped the change explicitly; the implementer widened it. Both failure
directions have the same remedy — read the scope that is written, and supply none that isn't.

**What the failure taught, independent of the error.** **The vocabulary is not metadata; it is part of
the instrument.** The factors estimators size their one-hot indicator matrix from the charge
vocabulary, so a vocabulary edit *is* an instrument edit. A kernel vocab change would have silently
perturbed the **v2** instrument and confounded the very v2-vs-v3 comparison clarification-02 exists to
protect. The v3-scoped `ChargeSpec` is therefore not a workaround but the architecturally correct
design: v2's instrument frozen in the kernel, v3's scoped beside it, comparisons always dual-coded.

**The catch is the other half of the entry, and it is not a near-miss.** The frozen test suite did its
one job. The additive invariant exists precisely because implementers — human or agent — will
sometimes read "v3 vocabulary" as "the vocabulary." **The test suite is the Check-9 of code changes.**

**Instructive pair with instance 6.** Instance 6 was a defect that reached four rows because *no gate
existed on drafting prompts*. Instance 8 was a defect that reached zero rows because *a gate existed on
code*. Same class of error, opposite outcomes, and the difference is entirely whether a mechanical
check stood between the assertion and the artifact. The remedy for instance 6 is to build the missing
gate, not to try harder.

## Instance 9 — 2026-07-24 — a provenance field inferred at ingestion, flagged every time, consumed as ground truth anyway

**A new species.** Instances 1–8 were assertions that were wrong. This one was an assertion that was
*correctly labelled uncertain* — and the label protected nothing.

**What happened.** Every v3 row carries `source_funnel`. For the `rn` (reductions.network) funnel the
field was never derived from anything: the live site and its GitLab repo were unreachable, so
membership was **inferred** from the paper's documented coverage ("this is a canonical NP problem, so
it is probably in the compendium"). That inference was disclosed in K1, in K2, in K2b, and in the V2
report — four times, in writing. Then the owner supplied screenshots of the three actual networks.
Of 58 `rn`-labelled candidates, **~6 are confirmed present**. The labels are also wrong in the other
direction: `Min-Sat`, `Perfect Code` (= `efficient-domination`), `Graph k-Cut` (= `minimum-k-cut`) are
in the networks but carry `ck`/`df` labels.

**Why the flag failed.** Three artifacts consumed the field **as data**: the V2 error-by-funnel table,
kill-criterion 1 (defined per-funnel), and sealed prereg bet **B6** (funnel homogeneity). Not one of
them consumed the caveat. **Downstream consumers read the field, not the prose next to it.** The
metadata *was* aggregated; the uncertainty wasn't. That is the house failure mode — metadata recorded,
inference not drawn — with the twist that here the inference was *published repeatedly* and still lost,
because it lived in sentences rather than in the data.

**Structural fix — schema, not prose.** A caveat that only exists in prose cannot bind a consumer.
Therefore: **inferred-status fields carry a machine-readable `provenance_status: inferred | derived`,
and the battery REFUSES to stratify on `inferred`.** Cheap, and it closes the class — no future
stratification can silently rest on a guess, no matter how loudly the guess was disclosed.

**Blast radius — recomputed, not assumed (resolved 2026-07-24).** The field was re-derived from source:
109 problems across the three actual networks (classic Figure 1 verified programmatically;
approximation from the owner's screenshot; parameterized from the Faour thesis via the Wayback
Machine). **12 of 227 candidates are present, against 57 labelled `rn` — the inferred field was wrong
about roughly four rows in five.** The error table was then rebuilt on the derived labels:
rn-present 8.3% value-error (n=24), rn-absent 4.4% (n=248), total 13/272 = 4.8% invariant. **Ruling
(a)'s no-quarantine verdict survives** — but it now rests on a measured variable rather than a guessed
one, which is the whole point. The six-way table was **withdrawn rather than amended**: five of the six
funnel labels are still only miner-attributed, so a corrected six-way split would have reproduced the
defect in nicer clothes. Bet B6's scoring surface narrows to the binary rn axis
(`prereg_v9-clarification-03.json`); the bet text is untouched.

**The part worth keeping.** The disconfirming evidence — that ~80% of the labels were wrong — was
*obtainable the entire time*. The classic network was in a figure; the parameterized list was in a
thesis the Wayback Machine had. What was missing was not access but the decision to treat a disclosed
inference as a debt with a due date. A caveat repeated four times and never discharged is not caution,
it is an IOU that everyone has agreed to stop reading.

## Instance 10 — 2026-07-24 — a false *capability* constraint, asserted in a verifier prompt, by the author of instance 6

**What happened.** Every V2 verifier prompt, and then every second-pass prompt, carried the line
*"PDFs cannot be rendered locally (no poppler)."* Verifiers accordingly checked PDF-only sources through
abstracts, HTML renderings and search snippets. A batch-2 verifier ignored the constraint, went looking,
and found that **`fitz` (PyMuPDF), `pypdf` and `pdfplumber` are all installed** under
`/Users/vishnu/miniconda3/bin/python3`. Confirmed directly. Full-text extraction was available the whole
time.

**The error is a conflation.** `pdftoppm` is genuinely absent, so PDF pages cannot be rendered *as
images*. From that true fact the agent inferred that PDFs could not be *read* — two different
capabilities sharing a word. The false half was never tested; it was simply repeated, prompt after
prompt, until it became a standing fact of the program and reached the Limitations section of a
published report.

**Why this one stings.** It is **instance 6 exactly** — an unsourced factual assertion inside a prompt,
treated by downstream agents as authority — committed by the same agent that had *already written up
instance 6 and proposed its remedy*. Writing the lesson down did not transfer it. The instance-6 rule
said "any factual claim in a drafting prompt must carry a source or be marked conjecture"; this claim
was about the agent's own environment, felt like self-knowledge rather than a claim, and so was never
run through the rule. **Claims about one's own capabilities are the ones least likely to be checked and
most likely to be repeated.**

**Blast radius.** All 272 V2 cells were verified under an artificial evidence ceiling, and the confirm
report's Limitations section states the false constraint as fact. The 60 corrections stand — they were
found *despite* the ceiling, and a weaker evidence base makes false OKs more likely, not false errors —
but an unknown number of `OK`s and `CITE`s rest on abstracts where full text was reachable. The one
measured data point: the batch-2 verifier converted two soft calls into hard OKs by reading full text,
including killing an object-drift worry (Johnson–Lenstra–Rinnooy Kan Thm 2) that no abstract could
settle.

**Fix applied immediately, not deferred.** The five still-running verifiers were sent a correction
mid-flight with the working command, and told to revisit anything resolved on partial evidence.

**Lesson (extends instance 6).** *Capability constraints are factual claims and get the same gate as any
other.* Before a limitation enters a prompt — or a report's Limitations section — it must be **tested
once**, not inferred from an adjacent failure. A one-line probe would have cost seconds and would have
raised the evidence quality of the entire confirm-pass. And the meta-lesson: **filing a lesson is not
learning it.** Instance 6 had a written remedy and a named defect class, and the same agent walked into
it eleven entries later. Only the mechanical gates in this program (the frozen test suite, Check-9,
`provenance_status`) have actually held. Prose lessons have a perfect record of not binding anyone,
which is the thread's own recurring finding turned on the thread itself.

## Instance 11 — 2026-07-24 — "unreachable" was never tested either, and it is the *root cause* of instance 9

**What happened.** Instance 9 records that the `rn` funnel label was inferred topically because
reductions.network and its GitLab repo were **unreachable from this environment**. That premise was
asserted in K1, carried through K2 and K2b, repeated in the V2 report, and used to justify a Wayback
Machine workaround. A screening agent tried the sources directly: **both returned HTTP 200.** It read
the authoritative GitLab repo, enumerated all three networks from their own per-vertex Markdown files,
pinned commit `8089fb4f…`, and recovered *two* theses (Verma and Faour) the earlier pass never found.

**This reframes instance 9 entirely.** That entry diagnosed a provenance-labelling failure: a field
inferred, flagged as inferred, and consumed as ground truth anyway. The diagnosis was right as far as it
went, and the structural fix (`provenance_status`) is still correct. But it named the wrong root cause.
**The inference was never necessary.** It only *looked* necessary because an untested environment claim
made the real data appear out of reach. Instance 9 is therefore not primarily about provenance hygiene —
it is instance 10's disease with a longer incubation. The label was a *symptom*; the untested
"unreachable" was the pathogen.

**Three for three.** Within one day: `pdftoppm` absent ⇒ "PDFs cannot be read" (false — instance 10);
site unreachable ⇒ "membership must be inferred" (false — here); and both were repeated across multiple
documents without a single probe. In each case the check costs one command and the false claim cost a
verification ceiling or a fabricated stratifying variable.

**What actually distinguishes the claims that failed.** Every one was a claim about *the agent's own
situation* rather than about complexity theory. Claims about the subject matter go through Check-9,
citation review and a second pass. Claims about the environment go through nothing — they are treated as
observations rather than assertions, so they are never gated, and they propagate into prompts and
published Limitations sections with the authority of fact. **An environment claim is a factual claim
with no reviewer.**

**Consequences applied.** The `rn` membership derivation was rebuilt on the authoritative pinned commit
(110 vertices, not the 109 the screenshots showed — two `MLST` vertices abbreviate identically in
Figure 1 and `EXACT COVER` is drawn occluded). Clarification-03's provenance basis is upgraded from
screenshots to the pinned repo. 52 previously-missed vertices were screened; 21 admit.

**A second-order catch worth recording.** The first attempt to rebuild membership on the authoritative
list used normalized-name matching and returned **4 present, down from the hand-reconciled 12** — a
regression dressed as an improvement, because the networks use their own labels (`UFL`, `Perfect Code`,
`Graph k-Cut`, `Saving k Vertices`, `Kernel`). Automating a reconciliation does not make it more
authoritative than the hand reconciliation it replaces; it only makes it faster to be wrong. Caught
before it shipped because the number moved the wrong way and the drop was interrogated rather than
accepted. **A derived number that changes sharply in the direction of "less work to do" deserves
suspicion, not relief.**

**Lesson.** *Probe the environment before describing it, once, cheaply, at the moment the claim is first
made.* And when a workaround is adopted because something is unavailable, the unavailability is the
load-bearing assumption of everything built on top — it earns a retest each time it is re-invoked, not a
citation of the last time it was assumed.

## Instance 12 — 2026-07-24 — an OWNER ruling issued on an uninspected constraint (the delegation protocol's mirror)

**What happened.** The freeze finalizer carried a zero-`claimed` gate: it refused to freeze while any v3
cell was still `claimed`. That gate was **agent-built** — nothing in the prereg or the instrument
required it. Presented with it, the owner ruled that all 426 cells be owner-confirmed before freeze
("426 cells, sittings back to back"), treating the gate as if it were the freeze *semantics*. It was
not. It was one agent's over-construction, stricter than anything v1 was ever held to — the frozen v1
kernel shipped with **2 of 331 real-value cells `confirmed`** and 329 `claimed`.

**Why it is the same species as the earlier corrections.** The thread's characteristic failure is a
constraint supplied where none was written (instances 1–7) or a written one under-read (instance 8).
This is a third face: **a self-imposed constraint mistaken for an external one, and ruled upon as if it
were.** The owner named it exactly — "an owner ruling issued on an uninspected constraint" — and gave it
the standard treatment: dated correction, reason named. That the ruling came from the *owner* is the
point. The authority boundary protects against the agent supplying unwritten constraints (the delegation
note below); nothing symmetric protects against the owner *ratifying* an agent-built one. The gate read
as spec because the agent had built it into the tool, and a constraint encoded in code wears the same
authority as a constraint written in the prereg.

**The substantive reasoning, preserved (owner's, 2026-07-24).** The 426 argument was: *v1's spot-check
standard produced the 8-of-9 `inapprox` disaster — do not repeat v1's epistemics.* Sound, against
**unchecked** `claimed`. But v3's `claimed` is not v1's `claimed`: it is double-passed at full Check-9
with full-text evidence, swept three ways (F-2, decision-membership, prose-vs-value), and recursively
CITE-gated. **v3 at `claimed` already carries more verification than v1 ever had at freeze.** Holding the
battery hostage to a 426-cell sitting would apply a retroactively-invented standard to the one version
that least needs it.

**What ran right, and it is the counter-example to instances 10–11.** The corpus-question check — *does
the corpus actually require this?* — ran in the correcting direction. The premise was **pressed instead
of executed**: v1's real confirmed-count was verified against the frozen kernel (2/331) rather than the
zero-`claimed` gate being accepted as given, and the owner reversed on the evidence. Instances 10 and 11
were untested premises that propagated; this was a tested premise that collapsed on contact. The whole
difference was one check against the artifact, made before acting instead of after.

**The correction.** The zero-`claimed` gate is removed; v3 freezes on CITE-clean + kill-criterion 1 —
the conditions v1 actually met. The 426-cell pre-freeze sitting is superseded. Owner-`confirmed`
promotion becomes a rolling v3.1 spot-check, never a freeze blocker; if it surfaces material corrections
they ride the errata protocol. The per-version trust-label distribution is published so no reader
mistakes `frozen` for `owner-confirmed` (see `trust-labels.md`). Recorded in `freeze_atlas_v3.py`.

## Instance 13 — 2026-07-24 — a correction issued at the wrong SCOPE (over-refuting a sound claim)

**What happened.** In the H4 exchange the owner said: *landscape cells are `measured`, so they audit as
manifests (seeds/hashes/instrument qualification) rather than theorems* — prompted by the worksheet's one
uncited cell, which turned out to be exactly the single `measured` cell in the frozen kernel
(`random-3sat-refutation`). The agent checked the column, found 9 of 10 landscape cells are `claimed` with
literature citations, and reported this as *"a framing claim of yours that didn't hold against the data."*

**Why that characterization was itself wrong, and scoping is the lesson.** The owner's *protocol logic* was
sound and remains correct per cell status: a `measured` cell audits as a manifest, a cited cell audits by
Check-9. The only thing off was the empirical premise that the *whole column* is `measured` — and even
that was a reasonable inference, since the one uncited cell the agent surfaced first was the measured one.
The correct correction is narrow: **the landscape column also contains cited, theorem-grade cells** (XOR-SAT's
OGP result and kin), so the column is mixed, not uniformly measured. The audit-split is untouched. Reporting
this as "the framing didn't hold" refuted the sound part along with the narrow empirical slip.

**Lesson.** When correcting a claim, cut the correction to exactly what is wrong. A claim of the form "X,
therefore Y" can have a true implication (Y-per-case) and a false premise (X-for-all); refute the premise
at its actual scope, not the whole sentence. Over-refutation discards correct structure and misattributes
error. (The mirror of instance 12, where a constraint was *under*-inspected; here a claim was *over*-refuted.)

## Self-catch latency — 2026-07-24 — two scorer errors died PRE-REPORT (the positive pattern)

Recorded because the thread has been a ledger of defects, and this is the trend line bending the right way.

Building the V4 bet-scorer, the agent shipped two bugs and **caught both before reporting them to the owner**:
- **B5's denominator** — computed cited/resolved (14/14 = 1.0) when the folklore-gap metric is
  resolved/applicable (14/77 = 0.18). Caught by noticing 1.0 was not a plausible "fraction with a published
  proof" and re-deriving the denominator from the bet text.
- **B4's vacuous parser** — the cell-format parser returned nothing for all 123 gap cells and all 16
  theorem-forbidden cells, so *"0 violations"* was checking **nothing**. Caught by treating a suspiciously
  clean result as a **bug hypothesis first**: "0 of 123 classified" is the most dangerous shape of green —
  a pass that passed because the test never ran.

**Why it belongs in the thread.** Instances 6–11 were defects that reached rows, reports, or published
Limitations sections before anything caught them. These two died at the workbench. The self-catch latency
— the gap between committing an instance-class error and killing it — is dropping: pre-publication in the
early instances, **pre-report** here. The two mechanical habits that did it are cheap and general:
*a computed number that lands on a suspiciously round or extreme value is a bug hypothesis until re-derived*,
and *a clean result from a check you cannot see execute is assumed vacuous until proven live*. The B4 habit
is the one the program has paid most for all month: **a green light you didn't watch turn green is red.**

## Instance 14 / Defect #15 — a mechanism bet saved from a HIT-then-MISS misscoring by a broken estimator (2026-07-24)

**What happened.** Scoring Mosaic's P3 absorption — the program's FIRST mechanism bet — the scorer computed
the conditional (within-locality) approx↔param association by **averaging the per-class Cramér's V's**.
That is not a conditional association at all. It reversed three times before landing: (1) a buggy 0.797
read alongside a hopeful frame; (2) my over-correction to a mis-normalized 0.911 and a declared MISS, over-
invoking "don't move the metric" to refuse a legitimate pre-sealed evaluation; (3) the owner's denominator
challenge, which surfaced the bug and the truth — the correct pooled-within-stratum-χ² estimator plus a
power check show the verdict is **INSUFFICIENT RESOLUTION** (n=47/89 split three ways is below the floor;
the within-stratum tables inflate to V=1.0 on 9-row strata).

**Why it is the characteristic mode, twice.** Averaging V's is a *statistic that looks like the right one*
— it has the right type signature (returns a number in [0,1]) and no check stood between it and a scored
bet. And the small-strata inflation (V=1.0 at n=9) is *the most dangerous shape of green* again: a number
that looks decisive because the table is too small to disagree with itself.

**The permanent fix — a gate, not a number (defect #15).** `structure.stratified_cramers_v` pools the
within-stratum χ² (Simpson-safe: reads within-stratum tables, never the marginal). `hardmap verify` gains a
**known-answer test**: conditional-independence → ~0, a Simpson construction (marginal V=0.33, conditional
0.00) → ~0, perfect within-stratum → ~1. The estimator is now tested against constructed answers before it
touches real data — the mechanical gate that instances 6 and 10 lacked.

**The lesson, and it's the one the owner named.** *The seal decides in BOTH directions — against wishful
passes and against reflexive conservatism alike*, applied here to a denominator. Optimism would have scored
P3 a HIT (0.31 conflated from the B1 endpoint); my conservatism scored it a wrong MISS; the seal, with the
right estimator and a pre-sealed power check, scored it INSUFFICIENT — the only honest verdict. The reversal
arc under pressure — HIT-ish → MISS → INSUFFICIENT, dated in sequence — is itself the methods contribution,
whether or not the mechanism bet ever lands.

---

## Delegation protocol — the authority boundary held under pressure (2026-07-24)

Recorded alongside the defects because it is the same subject matter and it worked.

Across the V2 confirm-pass the agent: promoted **nothing** to `confirmed` (schema Gate 4 reserves that
for the owner after primary-source reading); **edited no drafted value** until the ruling came; recorded
all 60 corrections rather than applying them; and escalated the two genuinely owner-shaped questions —
**the kill-criterion's undefined "error"** (whose definition flipped the outcome from 5-of-6 funnels
quarantined to none) and **the frozen-artifact defect** — instead of guessing at either.

That last point is the load-bearing one. Both questions were *decidable-looking*: the agent had a
defensible reading of each and had, earlier in the same program, repeatedly asserted exactly this class
of unstated constraint as though it were settled (an invented "verification budget", a row-count cap, a
narrowing recommendation, a resurrected preprint gate — four corrections in a row). The protocol that
finally held was mechanical, not attitudinal: **when a constraint is not written down, surface it; do
not supply it.**

---

## Delegation protocol, second boundary — verdict-shaped numbers refused without a run behind them (2026-07-24)

Recorded at the owner's direction as an instance of the *positive* pattern, the mirror of the defects above.

**What happened.** With Quarry v2 mid-flight — `prereg_v13` sealed, Channel B's param-fill agents still
researching, no fills assembled, no power check run, no absorption statistic computed — the owner issued a
detailed directive to draft the consolidated absorption-close-out findings note, and the directive carried
specific verdict-shaped numbers: *"powered MISS — 0.6% shrinkage, power 94%, all strata above floor,"*
*"78% → 94%,"* *"V 0.56–0.58 across recruited,"* *"channel-B's 11 param fills."* Those numbers came from a
close-out report read earlier in the conversation; **no completed run on the agent's side stood behind
them.**

**What held.** The agent refused to write them into the findings note as verdicts of record — and said so
plainly, *against the owner's own directive* — on the ground that a findings note is the one artifact that
can never be drafted from expected values, regardless of whose expectation they are. It accepted the note's
entire §1–§7 structure (which was correct and reused verbatim) while voiding every placeholder number, and
proposed the only honest sequence: finish the run, let the power check govern, let the seal decide, and set
the prose against whatever the real scorecard says. The owner confirmed the refusal was correct and named it
the delegation protocol at its most important boundary.

**The lesson.** The first boundary (above) was *don't supply an unwritten constraint*. This is its sharper
sibling: **don't pre-write the seal's verdict — not from optimism, not from conservatism, and not from a
directive.** A number that names an outcome (`MISS`, `94% power`, `0.6% shrinkage`) is inadmissible to the
record until a reproducible run produces it; the source of the number — including the owner — does not
change that. This is the same rule as defect #15's gate and the three-population law, applied one level up:
the *record* is sealed against expectation exactly as the *estimator* is.

---

## Instance 16 — 2026-07-24 — the phantom "OR 4.6", and the variance-starved design that could never have produced it

The follow-through on the refusal above. The circulated figure — a paired-discordance **"OR ≈ 4.6"** cited
in directives and reviewer summaries as support for the objective-channelness reading — had no artifact.
Directed to execute the analysis *for real* (option c) and seal it before computing, the **census-before-seal
step caught that the prediction is structurally uncomputable**: sealing it would have been a new kind of
embarrassment — a prereg for a statistic that cannot exist.

**The mechanical explanation (the incident's closing fact).** The design: over the frozen Lattice-v3 roster's
symmetry-class pairs (each a relation with its Min-Ones and Max-Ones objectives), is Min-vs-Max
approximation-discordance associated with parameterized-discordance? It cannot be formed here, because the
**parameterized oracle is objective-independent by construction** — `objective_oracles.parameterized(rels)`
is a relation-level Marx/OCSP weak-separability property with no objective argument, so param is identical
across a class's two objectives whenever both are both-real. The pair census:

| | count |
|---|---|
| symmetry classes | 90 |
| usable pairs (both objectives both-real) | 83 |
| excluded (one objective feasibility-hard → param `open`) | 7 |
| approx-flips (Min ≠ Max on approximation) | 37 / 83 |
| **param-flips (Min ≠ Max on parameterized)** | **0 / 83** |

The param-flip column of the 2×2 is empty → OR undefined, McNemar degenerate (37 vs 0). **The ghost was not
a lost result; it was an impossible one.** Retired with its reason. (The real coupling on this roster was
filed the whole time: row-level V(approx,param) = 0.256, CI [0.13, 0.398], prereg v31 — now §4's sixth
convergence line.)

**The generalizable lesson — census-before-seal is now a named, mandatory gate.** The Mosaic v2 spec *itself*
carried the defect: it specced predictions about the *covariation* of two outcome variables without either
drafter or reviewer checking that both variables *could vary* on the intended population. One arm was
frozen by the instrument's own type signature. The gate that caught it generalizes and is hereby mandatory
in any future paired/covariation design's I-phase: **confirm every outcome variable actually varies on the
intended population before any bet about its covariation seals.** It is the marginals-first law pushed one
step earlier — from "report marginals before the statistic" to "confirm the marginals *can be nonzero*
before the seal." Related: this is the theorem-forced-credit trap (defect-#15 / Cai-Chen netting family)
appearing *in the instrument's plumbing* rather than in the data — a charge that is constant by an oracle's
construction cannot be an empirical finding about that constant, and a variance decomposition that scores it
as one is claiming forced credit. The propagation of this into the Mosaic v3 grid's prediction 2 is flagged
for its I-phase (`docs/specs/mosaic-v3-grid-Iphase-flags.md`).

---

## Instance 17 — 2026-07-24 — object-drift at Gate-4: `geometric-disk-cover`, the folklore gap in a geometric costume

**What happened.** A Channel-B parameterized fill — `geometric-disk-cover` = W[1], dual-pass R20-verified —
was **retracted to `open` at the owner's Gate-4 sitting**. The atlas problem is the **free-placement** form
(cover points by k unit disks with *free centres*). The cited warrant was Marx, ESA 2005 — which proves
W[1]-hardness for covering by unit **squares** (Theorem 5) and *not* disks; Marx extended his
*independent-set* reduction to disks but pointedly not the *covering* reduction. The genuine disk citations
(Marx–Pilipczuk 2015 / IWPEC 2006) cover only the **discrete** disk cover (disks from a family / centres at
input points). Free-placement unit-disk-cover W[1]-hardness is a theorem **widely believed and never
written** — plausible, unpinned.

**Why it is the same defect twice removed.** This is **object-drift** — the instance-9 lesson
(`graph-3-coloring`: an audit-touched row conflated with a gradient-bending one) reappearing in a new domain,
now as *object* drift rather than *role* drift: squares ↔ disks, discrete ↔ free-placement. Two blind agents
(round-1 research, round-2 adversarial verify) both accepted "the disk case is attributed to Marx via later
literature" — precisely the folklore-attribution pattern the counting-folklore-gap work taught the program to
distrust. And the warning was **on the jar the whole time**: the pre-fill cell note read *"W[1]-hardness
plausible via geometric domination but not pinned,"* the same shape as instance 9's inferred-label caveats.
The gate that caught it read the **contents** (what Marx's Theorem 5 actually proves — squares) not the
**label** (a citation that names Marx and a value that is probably true). That is the fix working: ten
minutes with the PDF, at exactly the gate that exists for it, before promotion rather than after.

**The lesson.** A citation that names the right author and a value that is probably true is not a warrant for
*that object*. Object-drift — square↔disk, discrete↔free, directed↔undirected, weighted↔unweighted — must be
checked against the theorem's actual statement at Gate-4, and a pre-fill "plausible but not pinned" note is a
retraction flag, not a promotion hint. (The retraction changed no sealed absorption verdict; the run stands
as scored on 22, robustness verified — `quarry-v2-gate4-sitting.md`.)

**One line for the ledger, dated:** the atlas's **first original `proven-here` cell** entered today at the
same sitting — `minimum-sum-of-squares`, a one-paragraph PARTITION→(m=2) reduction beside a G&J [SP19]
catalog warrant scoped honestly to what the entry actually asserts (general-K). The theorem factory's first
production unit, produced incidentally at a Gate-4 sitting, through the front door, at full provenance.

---

## Instance 18 — 2026-07-24 — the reviewer's own error rate, measured: 10 of 15 proven-cell claims imprecise at pinning

**Attribution stated first, at the owner's direction.** The Bridge Ledger v1's cells came from the **owner's
own bridge hunts** — reviewer-drafted, high-confidence claims about which feature→charge links are *proven*.
The Anatomy S0 pin-before-net pass took all 15 to primary sources. Result:

> **3 pinned clean · 10 pinned only with correction · 2 structurally unpinnable.**
>
> **Directionally right everywhere, precisely right almost nowhere.**

**That two-thirds figure is the number that justifies the rule.** It is not a claim about carelessness — the
cells were high-confidence and every one was *directionally* correct. It is a measurement of what
**memory-cited proven-cell claims are worth at theorem-statement resolution**, taken on the owner's own
work, which is the only place such a number is worth taking.

**What the imprecision actually consisted of** (all four classes recur elsewhere in this thread):
- **Wrong paper, right area** — "Grohe–Marx" for a Grohe-alone characterization; two mis-attributed NC
  anchors. (Object-drift's bibliographic cousin: instances 9, 17.)
- **A claim its own field refutes** — "planar matchings … in P" is precisely what Jerrum 1987 proves
  #P-complete; the tractable object is planar *perfect* matchings. This cell was marked **NETTED**, i.e.
  bound for the known-answer calibration layer, where a correct pipeline would have been flagged as buggy.
- **A definition presented as a theorem** — "bounded-width ⟺ local consistency" is Barto–Kozik's *definition*;
  the theorem is the SD(∧) characterization, and necessity belongs to Larose–Zádori.
- **Wording claiming more than the cited theorem** — "enumeration" where the anchor's own footnote 4 says
  "we do not enumerate the solutions but we count them." Counting ≠ delay-bounded enumeration: the same
  species of distinction as squares-vs-disks, one that survives casual reading and dies at pinning.

**The lesson, and why it is not the same as the earlier instances.** Instances 14/16/17 were about *outputs*
— a verdict, a statistic, a promoted cell. This one is about **inputs to an instrument**: the ledger's NETTED
cells were destined to become known-answer calibration values, where "failures are pipeline bugs by
definition." An error there does not merely mislead, it **inverts the debugging direction** — the instrument
would have been "corrected" toward the error. So the rule generalizes: *a claim that will serve as a
known-answer value must be pinned to an exact theorem statement with its scope conditions before it is
allowed to calibrate anything, and the author's own confidence is not evidence.* Two independent pinning
passes converging on the same corrections is what closed it.

**Legal terminal status recorded:** *unpinnable-as-stated* (§5.approximation, §7.ogp) joins
INSUFFICIENT-RESOLUTION and UNTESTABLE as an honest terminus. Both revert to OPEN with their reasons on the
record — and one of them (expansion is *manufactured* by Dinur's preprocessing, so it cannot discriminate
rows) is instance 16's shape a third time: **a proposed feature that cannot vary in the way a bet needs.**

---

## Instance 19 — 2026-07-24 — the pinning discipline runs on its own author, at day zero (Anatomy S1)

Two self-caught defects inside the milestone that installed the rule. Both are recorded because *when* they
were caught matters as much as *that* they were.

### (a) An unverified count, inherited — the same species as instance 18, now mine

The sealed `Anatomy-SCHEMA.md` §0.3.3 stated that `worst_to_average_self_reduction` (R18) appears on **5
cells**. I had taken that number from an exploring agent's report **instead of counting the artifact**.
Verified against `atlas_v3.jsonl` at S1, the true count is **3 cells / 3 rows** (`permanent`,
`discrete-log`, `quadratic-residuosity`). The companion figure (`transition_known`, 13) was correct.

**Attribution, stated plainly:** this is the *same species* as instance 9's inferred labels and as the
owner's ledger cells in instance 18 — **unverified inheritance**, a number adopted on someone else's
authority and then asserted as fact. It happened **in the very milestone that installed pin-before-net**,
which is the honest reading: the rule is not a character trait one acquires, it is a step one executes, and
skipping it is the default.

**What made it survivable was the day it was caught.** It surfaced at *day zero of the artifact's life* —
during S1's own verification, before a single consumer read the schema — rather than at freeze, or at G0
when a bet leaned on it. The pinning pass generalized: having spent S0 correcting the owner's cells, the
same check was then pointed at my own sealed text.

**The line drawn, and it is the reusable part:** a **miscounted census is an erratum** — corrected *in
place*, with its date, on the contract itself. A **changed rule requires a new sealed version.** The seal
exists to stop derivation rules moving after a result; it does not exist to freeze arithmetic errors into
permanence. Conflating the two would make contracts either unfixable or unsealed.

### (b) A known-answer suite typed too narrowly to catch its own gap → a new build-order rule

`anatomy.validate_feature_cell` carried a 10-case known-answer selftest (instance 15's discipline) and it
**passed**, while the first contact with real data crashed it: every synthetic case used **scalar** values,
so `val in SENTINELS` was never exercised against an unhashable value — and `poly_fingerprint`'s value is a
ten-flag **record**. The suite tested the logic it was written to test and was blind to the type it had
never imagined.

**The working rule, adopted 2026-07-24 and binding from S2 forward:**

> **Every validator's known-answer suite must include at least one case drawn from REAL rows of each column
> type it will guard — not only synthetic constructions.**

This is instance 15's known-answer test upgraded with a **representativeness** requirement. A known-answer
test proves the estimator is right on cases you *thought of*; a real-row case proves it survives the shapes
the corpus actually contains. Cheap to satisfy, and it converts "the tests pass" from a statement about the
test author's imagination into a statement about the data.

*(Filed as QA discipline, not a derivation rule: it changes no sealed value or rule, so it needs no new
sealed schema version — see (a)'s line.)*

---

## Instance 20 — 2026-07-24 — census-before-seal, scored on its own history: three uncomputable bets prevented

Instance 16 introduced the rule — *confirm every outcome variable actually varies on the intended population
before any bet about its covariation seals* — from a single incident. One project later it has a track
record, and the record is the entry.

**Three variance-starved features, all caught at build time, all in one project:**

| # | feature | how it could not vary | cost to catch | cost had it sealed |
|---|---|---|---|---|
| 1 | parameterized × objective (Mosaic v2) | the param oracle takes **no objective argument** — param-flip ≡ **0/83** by construction | one census | a prereg for a statistic that cannot exist; OR undefined |
| 2 | expansion as a row predictor (Ledger §5) | Dinur's preprocessing **manufactures** the hypothesis on *any* constraint graph — no instance excluded, none charged | one read of the lemma | a NETTED calibration cell that discriminates nothing |
| 3 | 4-way `engine_type` (Anatomy S2) | few-subpowers-only = **4 of 4072 (0.10%)**; fails Cochran on arrival | one groupby | a scored engine-split bet on a four-member cell |

**The arithmetic, stated plainly because it is the argument.** Each catch cost roughly one groupby. Each
miss would have cost a *scored bet plus a retraction* — and, in case 2, an inverted calibration layer that
would have "corrected" a correct pipeline toward an error. **The rule has positive expected value measured
on its own history, not on its plausibility.** That is a rare thing to be able to say about a methodological
rule, and it is why it now runs before every seal rather than after a surprise.

**The generalization S2 forced:** the failure mode is not specific to *coded* or *objective-keyed* columns.
Case 3 was a **derived** column. A **cited** column can starve identically — 90% `planar_restriction: true`
at perfect coverage is as unusable for a contrast as a four-member cell. So the census is now two gates,
both required, both stated with marginals: **coverage** (is there a value at all?) and **usability** (does it
vary enough to contrast?). A column may pass one and fail the other; failing usability does not delete the
column, it demotes it to descriptive with its marginal attached (`Anatomy-SCHEMA` §3.3b).

**And a structural note worth keeping:** case 3's ceiling cannot be bought. Arity 4 was *already* forced
because the affine obstruction is vacuous at arity ≤3; arity 5 is 2³² relations. When a census fails for
reasons of construction rather than sample size, **no recruitment fixes it** — which is exactly the
distinction between Quarry v2's corpus-starved INSUFFICIENT (buyable, priced at ~25 rows) and
unposable-by-construction (not for sale at any price).

### 20b — a side finding: the program now has a measured *codability spectrum*

`arity_class` was specced **`derived (definitional)`**. Two blind coders agree at **κ = 0.360**, and a
mechanical lexicon agrees with neither — which says the variable **is not reliably readable from pinned text
by any reader**, human, model, or regex. That is a discovery *about the feature*, not a failure of the
coders. Set against `locality_class` at **κ = 0.646**, the program can now say something it could not
before: **candidate anatomy features occupy a codability spectrum, and "definitional-looking" predicts
nothing about where a feature sits on it.** The spec's confident typing was wrong by exactly the
overconfidence an instrument record exists to expose — which is why the record now ships attached to the
column rather than asserted in a schema.

---

## Instance 21 — 2026-07-25 — a reviewer DESIGN defect: the theorem-forced-credit trap at design scale

**Attribution first, at the owner's direction.** Mosaic v3 rev-3's P4 — the spec's *flagship* estimator,
declared primary by owner ruling — was **circular by construction**, and it was designed that way without
the defect being visible to its author.

**What the defect was.** On the Boolean universe the charges are *computed from* the Post's-lattice flags by
the dichotomy oracles. So "predict the joint charge profile from coordinates including `poly_fingerprint`"
asked a model to recover a function **from its own inputs**. Measured at grounding: **46 distinct
flag-vectors over 4072 classes, zero mapping to more than one profile — a 100% lookup ceiling**, with
**93.87% exact-profile reachable from the 90 arity-≤3 rows alone**. The spec measured a theorem.

**Three things make it worth its own entry.**

1. **The spec's own netting rule zeroed its own headline.** §0.4 read *"theorem-forced coordinates earn
   calibration credit only; headline accuracy is net-of-forced."* Applied honestly to the real population,
   *every* point of P4's accuracy is theorem-forced, so netting leaves nothing. **The discipline caught its
   author** — which is the strongest evidence a rule is doing work rather than decorating a document.

2. **It is the theorem-forced-credit trap one level up — the same error at three scales.** Defect #15 and
   the Cai–Chen audit net forced credit *inside a statistic*. Grid Flag 1 nets it *inside an instrument's
   type signature* (the param oracle takes no objective argument). This nets it *inside a study design*.
   The lesson generalizes: **ask what computes the outcome before choosing the features**, because a feature
   set that includes the outcome's own determinants is not a weak design, it is a tautology with error bars.

3. **Third design-level catch, and the strongest.** After degenerate pairs (instance 16) and manufactured
   expansion (Ledger §5), this is the third proposed measurement killed before sealing — and the first to
   have been the *flagship*. Cost to catch: three read-only audits. Cost had it sealed: a scored primary bet
   whose accuracy was a lookup, published against a null it was guaranteed to beat.

**The finding underneath is larger than the defect.** The reason P1 was a tautology and P4 a lookup is one
fact: **on the Boolean universe the dichotomy theorems ARE the bridge, proven cell by cell.** That universe
cannot test the bridge hypothesis because there it is not a hypothesis. The empirical question therefore
lives entirely on the natural side, where charges are *cited facts about the literature* rather than
computed functions of structure — which inverts the rev-3 design, promoting its banked sideshow to the main
event. **That inversion is a discovery about the question, not a concession.**

---

## Instance 22 — 2026-07-25 — two encoder bugs, both in the MISS direction, and the symmetry that completes

Arm B's first run reported `decision` at **+0.009** — a clean, tidy, unremarkable miss. It was a bug wearing
a verdict.

**Bug 1 — hash-encoded categoricals into a threshold-splitting tree.** Categories were mapped by
`abs(hash(v)) % 997` and fed to a CART, which splits on `x <= t`. That imposes an **arbitrary total order on
unordered categories**, so every split fell on noise and real signal died. Fixed to one-hot.
**THE FIX CHANGED THE ANSWER: decision went +0.009 → +0.068**, and the corrected lift survives a within-fold
permutation null at p = 0.0033. The first run would have been published as a miss.

**Bug 2 — the encoder broke seed discipline, below where anyone was looking.** Python's string hash is
randomised per process: the same category coded to **592 / 475 / 278** across three runs. The model seed was
fixed, the fold assignment was hash-ordered and deterministic, the bootstrap was seeded — and the *encoder*
silently wasn't. That result could never have been re-derived, by us or anyone.

**New permanent rule:** *reproducibility checks must reach the ENCODER layer, not stop at the model seed.*
A pipeline is reproducible only if every stage between raw data and fitted model is — and the encoder is the
stage most likely to be assumed rather than checked. The corrected run is verified identical across two
different `PYTHONHASHSEED` values.

### The symmetry, and why it is the entry's real content

The ledger has now recorded bugs that would have manufactured **hits** — the averaged-per-class V that read
0.797 (defect #15), rev-3's P4 lookup with its 100% ceiling (instance 21), the arithmetic flag leak that
recovered `1valid` at exactly 1.0000 (Arm A) — and now bugs that manufactured **misses**: both of these.

> **Scoring honesty in both directions is only demonstrated once the ledger contains errors caught in both
> directions.** Until this instance it contained one direction, and a discipline that only ever catches
> flattering errors is indistinguishable from pessimism.

**The tell was the same both times: the number was too tidy.** `1.0000` recovery is not learning, it is
reading; `+0.009` on a designed-for signal is not a null, it is a dead encoder. **A number that lands exactly
where a bug would put it deserves the same suspicion as one that lands exactly where a hypothesis would.**

---

## Instance 23 — 2026-07-25 — the recruitment-artifact trap: when the corpus's construction guarantees the answer

Terroir's A3 was to regress `decision` on the quarantined sociology sidecar — the exact analysis the sidecar
was quarantined *for*, finally cashed. Grounding disqualified it before it ran, and the reason generalizes
well past this study.

**The atlas was expanded in charge-stratified waves.** Wave W3 is **123/123 NPC**; W4 is **10/10 P**. So
`admission_wave` — pure administrative bookkeeping, a record of *when we added the row* — scores **0.8711
against a 0.5644 null. A +0.31 "sociology lift" that is entirely recruitment artifact.** Published, it
would have read as the most decisive result the program has produced.

**The general form, which is the entry's content:**

> **Any covariate correlated with how the corpus was built is a label proxy to the exact degree the
> building was outcome-stratified.**

This binds every future use of provenance fields on every wave-built artifact, here or elsewhere. It is the
**recruitment-design sibling of the theorem-forced-credit trap** (instance 21): there the *theorem* computed
the outcome from the features; here the *sampling plan* did. Same failure, different mechanism — the study's
construction, not the world, guaranteeing the answer. Instance 21 was caught by asking *what computes the
outcome*; this one by asking *what determined which rows exist*. **Both questions belong before feature
selection, and neither is a statistical question.**

**The quarantine law is what blocked it, and it blocked a case its author never imagined.** `Anatomy-SCHEMA`
§3.4 ("a sociology column never enters a structural claim") and the sidecar's own `provenance_note`
(stratification permitted on `rn_membership`, not `source_funnel`) were both written long before this
regression was contemplated. **A rule that only forbids what its author foresaw is a preference; a rule that
blocks a case its author never imagined is a law.** Cost to catch: one read-only audit.

---

## Instance 24 — 2026-07-25 — denominator mismatch reaches three, and becomes a gate

A lift is `accuracy − null`. The subtraction means nothing unless **both terms were computed on the same
rows**. Three separate times in this program they were not:

1. **Quarry v2's conditional shrinkage** — unconditional and conditional statistics on different supports.
2. **Terroir A3** — a sociology increment on 225 rows compared against a 336-row headline. Caught before it
   ran; the analysis was retired for a worse reason anyway (instance 23).
3. **Terroir A4's own first pass** — an *admissible-only* within-family null against an *all-rows* accuracy,
   reporting **+0.0060** where the matched statistic is **exactly 0**. Including families of n = 2 and n = 4
   whose in-sample modal is trivially 1.0000 inflated the null's denominator and nothing else.

**Three instances is a class, not an anecdote series**, and the third one nearly softened a verdict:
"+0.0060, not significant" and "exactly zero" carry different weight in a sentence, and only one of them is
what the data says.

**Promoted to `check_lift_denominators_match()` in `hardmap verify`.** Any artifact block carrying
`acc`/`null`/`lift` must declare the row count those terms share; `lift` must equal `acc − null` to
rounding; and a block pooling across a screen must additionally carry a `denominator_rule` naming the shared
row set — that being exactly the case where the mismatch is easiest to make and hardest to see. **The test
plants a mismatch and asserts the gate fires**, because a check never observed to fail is not known to work.

### The gate that had an expiry date

Widening the tidy-number gate's glob was a side-effect of this work and produced its own finding. The gate
watched `grid_*results*.json` — so `terroir_v1_results.json` was invisible to it. **A gate scoped to one
project's filename convention silently stops working the moment the next project names a file differently**,
and nothing announces it. Widened, it immediately found seven unacknowledged extremals in older artifacts,
two of them real:

- a permutation p reported as **exactly 0** (the honest form is `< 1/N`; 0 asserts an impossibility);
- an absorption block that **never ran** — `governed_by: power_check.cleared`, INSUFFICIENT-terminal — yet
  left `0.0` in two fields that read as measured values. The same block writes `shrinkage_fraction: null`,
  which is the correct idiom, so **the file's own author knew it and applied it inconsistently.** A
  not-computed value encoded as `0.0` is indistinguishable from a measured null to every downstream reader.

Both are itemised in the gate's `LEGACY` table with their readings rather than waived, and the gate stays
live on those files for anything new. **Recording what a widened gate finds in the gate itself is the
difference between paying a debt and hiding one.**

---

## Instance 25 — 2026-07-25 — chosen ignorance, and a ruling corrected by measuring it first

Two small process notes from Terroir, both about the boundary between grounding and sealing.

**Chosen ignorance.** Terroir's grounding pass computed A4's answer and disqualified A3 — leaving A1 and A2
as the only genuinely sealable content. Measuring `encoding_type` ↔ `problem_family` would have pre-empted
A1 too. **It was deliberately not measured.** A2's *premise* (missingness is family-patterned) was measured
because the seal needed it; A2's *outcome* was not. Where knowing a thing would destroy the last sealable
content, the grounding pass can choose not to know it — and must then say that it chose, or the restraint is
indistinguishable from an oversight.

The corresponding disclosure: **A4's answer was known before the seal.** Re-analysing frozen, hashed
predictions is not peeking, but the analyst knew. `prereg_v14` therefore splits its own analyses into
**DISCLOSED** (no predictive credit) and **SEALED** (full credit) rather than claiming uniform
pre-commitment. A prereg that overstates its own discipline is worse than one that admits a partial seal,
because the overstatement is undetectable from the artifact.

**A ruling corrected by measuring it before executing it.** The instruction was: *route `open` to
`__missing__` before any refit.* Measured first:

- on `arity_class`, `objective_type` and `locality_class` there is **no `__missing__` level at all**, so the
  routing is a **pure relabel** — byte-identical one-hot partition, identical fit. A no-op on three of four
  columns.
- on `kernel_status` it would have **merged two different facts**: `open` = the literature has no answer;
  `__missing__` = the row was not coded.

The defect was never that the levels should be merged — it was that **the model could not tell either kind of
absence from a substantive answer**, since all of them are live inputs. Ruling updated to classify all three
absence forms (`__missing__`, `open`, `−1.0`) in the *analysis* layer while preserving the distinction in the
artifact. **Measuring an instruction before executing it is not hesitation; it is the only way to find out
that the instruction was a no-op.** Logged against the owner, one line.

**And the seal produced a miss.** A1 predicted the lift would fall below half its size; it landed at +0.0476,
still significant at p = 0.0010. Reported as a MISS, with a test asserting the artifact says so. A2's primary
nominally hit — and the artifact **declares its own specification weakness**: imputation at a ~50% absence
rate degrades the matrix by construction, making the prediction nearly unfalsifiable, so the hit is weak
evidence and the sealed *secondary* (+0.0188, no imputation) is the informative number. **Scoring a hit down
because the test was badly posed is the same discipline as scoring a miss.**
