# Methods thread

Running log of methodological defects and the lessons they forced. The characteristic failure mode of
this program has a name: **metadata already recorded, inference not drawn** — the fact needed to avoid
the error was *already written down somewhere in the artifact*, and nobody joined it up. Entries are
dated and numbered continuously. (Instances 1–5 predate this file; 6 and 7 are recorded below at the
owner's direction, from the Atlas v3 V2 confirm-pass of 2026-07-23/24.)

**Numbering history, stated so the count is never guessed (added 2026-07-26).** Instances **1–5 predate
this file**, as above. **15 is absent**, and **6 carries an addendum sharing its number** — both artefacts
of how entries were written at the time. *The past is never renumbered:* an instance number is a citation
target, and prior documents point at these.

**No document states a ledger size as a literal.** A hardcoded count in a file that grows is stale the next
time someone appends — this note said "26 entries, 6–31" and was wrong within a day. Anything quoting the
ledger's size **derives it from the headers at the time of writing**, and states the convention rather than
a round total: *N numbered entries spanning a–b, five predating the file.*

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
- ~~an absorption block that **never ran** — `governed_by: power_check.cleared`, INSUFFICIENT-terminal —
  yet left `0.0` in two fields that read as measured values. The same block writes `shrinkage_fraction:
  null`, which is the correct idiom, so **the file's own author knew it and applied it inconsistently.**~~
  → **THIS SECOND READING WAS WRONG. Corrected in [instance 26](#instance-26--2026-07-25--the-gate-was-right-the-triage-was-not).**
  The block ran; both zeros are bias-correction floors and are the estimator's correct output.

Both are itemised in the gate's `LEGACY` table with their readings rather than waived, and the gate stays
live on those files for anything new. **Recording what a widened gate finds in the gate itself is the
difference between paying a debt and hiding one.** (The quarry pair has since left the table — not waived,
*paid*: see instance 26. The permutation p remains, scorer fixed and artifact awaiting a locked-env re-run.)

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

---

## Instance 26 — 2026-07-25 — the gate was right, the triage was not

Instance 24 widened the tidy-number gate, and the widened gate did its job: it flagged
`recruited_B.absorption.unconditional_V = 0.0` and `averaged_per_class_wrong = 0.0` in
`quarry_v2_results.json`. Then the triage read the surrounding JSON and wrote down a cause — **an
uninitialised placeholder from a block that never ran** — and itemised it in the `LEGACY` table as a REAL
FLAW, with a remedy: encode the two fields as `null`.

**The cause was wrong, and the remedy would have destroyed information.** The block ran. Both zeros are
**bias-correction floors**. `structure.cramers_v` is the Bergsma-corrected V: it subtracts
`(k−1)(r−1)/(n−1)` from φ² and clamps at zero. On the 22-row recruited-B population against a 5×4 table the
correction is **0.5714** against a φ² of **0.4464** — the correction exceeds the signal, the clamp bites, and
the estimator returns **exactly 0** where the uncorrected V is **0.3857**. The same thing happens in all
three strata of the averaged-per-class estimator (n = 10 / 8 / 4). Writing `null` would have asserted *not
computed* about a statistic that was computed, and thrown away the one fact that makes the zero legible.

`shrinkage_fraction: null` was not an author's correct idiom applied inconsistently either. It is the
`uncond > 0` divide-by-zero guard in the scorer tripping **on the same floor** — shrinkage is
`(uncond − cond)/uncond`, undefined at zero. The two encodings were never in conflict; they have one cause.

**The contradiction was visible without re-running anything.** The same block reports
`correct_stratified: 0.43`. A block that never ran cannot produce 0.43. One number in the triage's own
evidence refuted its conclusion, and it was read past — because by then the conclusion already had a
narrative, and the narrative was a good one: a placeholder bug is a better find than an estimator behaving
as documented.

**The rule.** *A gate that flags a number has not diagnosed it.* The flag is a question. The triage is an
answer, and an answer needs the evidentiary standard of the finding it replaces — for these two fields, one
re-run of the estimator, which is what eventually produced every number in this entry. Confident, specific,
wrong causal stories are the failure mode of triage-by-reading, and they are *more* dangerous than an
unexplained flag, because they close the question.

**Direction matters here too.** The ledger has recorded bugs that manufactured hits (defect #15, rev-3's P4
ceiling, the Arm A flag leak) and bugs that manufactured misses (instance 22's two encoder bugs). This is a
third kind: **an error in the error-finding machinery**, whose proposed fix wore the costume of humility.
Replacing a number with `null` *looks* like restraint. It was an unmeasured claim.

**Resolution.** `score_quarry_v2.py` now emits an `extremal_acknowledged` entry carrying the floor
arithmetic (n, table shape, φ², the correction term, the uncorrected V), generated from the run rather than
hardcoded — so if a larger population stops flooring, the acknowledgement disappears with it instead of
lingering as a stale excuse. That is the mechanism instance 22 built the gate around, used as intended: the
zero stays, because the zero is what the estimator returns, and the artifact now says why. Both quarry
entries are **removed** from `LEGACY` — a legacy table is for debt, and this one is paid. The Quarry v2
verdict is untouched (pooled n = 111, power 7/9, min-exp 3.59, **BELOW FLOOR — INSUFFICIENT**); every
pre-existing byte of the artifact is unchanged.

The *other* real flaw from instance 24 survived scrutiny. `crucible._envelope` computed `one_sided_p_ge` as
`k/M`, which reports **exactly 0** when no null reaches the real statistic — an impossibility M draws cannot
establish. Fixed to the plus-one form `(k+1)/(M+1)` that `_perm_p_gradient` in the same file already used;
S1's p becomes `1/1001 = 0.000999`, and the RESIZED verdict and both excess flags are unchanged. **A
codebase that already contains the correct estimator, one function away, is the cheapest kind of defect to
find and the easiest kind to walk past.**

---

## Instance 27 — 2026-07-25 — supply is not viability: a kill criterion that passes while its purpose fails

Marrow's Kill 1 asks *"are there ≥ 40 presentable rows?"* The build exists to run Terroir-C, a within-family
residual test. At the planning estimate those two answers **disagreed**: 82 rows would have cleared the
floor comfortably while the instrument's minimum detectable effect sat at **+0.10**, against measured
residuals of **+0.0000** and **+0.0188**. A project can have a population and still have no experiment.

**So the power arithmetic became a second gate, evaluated at M0 beside the census** — and the separation
paid immediately. The census came in at **34** (Kill 1 fires), but Terroir-C's verdict is *stronger and
more robust* than Kill 1's: it fails under **every** admission reading, for three independent structural
reasons — zero families reaching n = 30, a stratum that is **constant** on the target charge (18/18 NPC),
and a fold key that cannot produce 5 non-trivial folds from 2 substantive families.

**The generalizable rule:** *a kill criterion on SUPPLY does not certify VIABILITY, and the two must be
evaluated separately.* This is the coverage-vs-usability split (`Anatomy-SCHEMA` §3.3b) — which the program
already applies to columns — lifted to the level of a whole study, and applied **prospectively** for once
instead of discovered at scoring time.

### The estimate that was 2.4× the census

The planning figure of 82 came from a regex over problem names. The census is 34. The gap is entirely
boundary cases that *look* like members: `dominating-set` is Min-Ones over an **unbounded** neighbourhood;
`equitable`/`acyclic`/`harmonious` colouring each carry a **global** side constraint no finite-arity Γ
expresses; `choosability` **quantifies** over list assignments; `betweenness` is an ordering CSP over an
**infinite** domain. The estimate was labelled as having error bars and the error was larger than the bars
implied. **A name-pattern is a sampling frame, not a census, and the difference is exactly the boundary
cases the pattern was never able to see.**

### Choosing the reading after seeing which one clears

The census also surfaced a question the spec had not settled: polymorphisms are computed **of a template**,
so the admission test is not "is this CSP-shaped?" but "is there a **fixed** finite template whose Pol we
can compute?" Where the template is in the *input* (H in graph-homomorphism, Γ in maximum-csp, k in
chromatic-number), `poly_fingerprint_natural` is **undefined** — a computability fact.

It moves the count in both directions: −7 varying-template rows, +4 fixed-template rows the first pass had
omitted. And it decides the project: **34 FIRES / 41 CLEARS / 45 CLEARS.**

> **The reading that clears the floor was available and was not taken.** Choosing an admission rule after
> seeing which one clears a kill criterion is indistinguishable from having no criterion. The band is
> reported, the recommended reading is the one that fires, and the ruling is flagged as pending.

---

## Instance 28 — 2026-07-25 — the same gate defect twice in two commits, and where the fix stopped

Terroir widened the tidy-number gate's file glob from `grid_*results*.json` after discovering it was blind
to Terroir's own results file. **One commit later, Marrow's census and power artifacts matched neither
widened pattern.** The same defect, immediately, in the work that had just documented it.

**The pattern was not the defect — the SHAPE was.** A gate keyed to whatever the last project happened to
name its files silently stops working the moment naming changes, and it **fails open**: it reports a clean
pass over files it never opened. Nothing announces a blind spot. The fix is a **declared watched set** in
one place that a new project registers against, not a glob that grows by accident.

### Where the fix deliberately stopped, and why that boundary is the entry

Adding `*factors*.json` to the watched set surfaced **16 unacknowledged extremals** across three artifacts
in a project this pass had not examined — including an `excess_over_null.null_envelope` whose real, mean,
p2.5 and p97.5 are **all exactly 0.0** beside a one-sided p of exactly **1.0**.

*(This entry guessed the cause twice and was wrong twice; the adjudication is instance 31 and both
guesses are withdrawn. First guess: "the never-ran-but-reported-as-measured pattern found in
`quarry_v2_results.json`" — refuted by instance 26, where those zeros turned out to be Bergsma
bias-correction floors. Second guess, written as the correction and passed to the backlog task as its
prior: "the same kind of floor — a clamped estimator at small n, plus a `k/M` p reporting exactly 1.0."
Also wrong, and CHECKED rather than accepted: nothing on that path clamps, n is 114 not 22, and `_envelope`
already uses the plus-one form. The true cause was a third species entirely — a VACUOUS COMPARISON, the
statistic `acc[k_hat] - acc[1]` evaluated at k*=1.*

*The reusable part is not either wrong guess but what they had in common: **both diagnosed from the SHAPE
of the artifact — a 0.0 sitting next to a null, a cluster of extremals — instead of from the EXPRESSION
that produced it.** An exact extremal has at least three causes that look identical in JSON (a clamp, a
boundary p-form, a vacuous expression) and are told apart only by reading the code path. Guessing from the
artifact was fast and wrong twice; reading the expression was decisive both times.)*

Two bad options and one good one:

- **Wave them through a LEGACY table.** This is what the table is *for* — but the Terroir entries earned
  their place by being read and classified one at a time. Sixteen entries written without reading them
  would be rubber-stamping, and a gate that rubber-stamps is worse than no gate: it converts unexamined
  debt into a recorded pass.
- **Drop the pattern silently.** Narrowing a gate until it goes green. The failure mode with no defence.
- **Leave the pattern out, record the reason IN THE GATE, and queue the backlog as its own task.**

> **A watched set that grows only as fast as someone actually adjudicates it is the honest kind.** The
> gate's docstring now carries what it is *not* watching and why — because the place a reader looks to find
> out what is checked is the same place that must tell them what isn't.

---

## Instance 29 — 2026-07-25 — a prediction that was half wrong, and the half that was wrong caught the auditor

Marrow's presentation audit compares a decision value **computed from the pinned template** against the
**cited** cell — the atlas's first check against computed ground truth rather than against other citations.
Before deriving anything, M1 wrote a prediction down: *disagreements should concentrate on
instance-restricted rows, because the template cannot see a restriction on inputs.*

The first run reported **14 disagreements out of 28** — and the split was 7 restricted, 7 unrestricted. The
prediction had called the restricted half and missed the other half entirely, which is what sent me back to
look instead of forward to write.

**The unrestricted seven were all VCSP-shaped, and the error was mine.** Deriving "decision" from the
constraint language's SATISFIABILITY is the right question for a plain CSP and the wrong one for a
value-optimisation problem: `CSP({OR2})` is trivially satisfiable — set every variable to 1 — while
**`Min-Ones({OR2})` IS vertex cover.** Schaefer answers a question the row was not asking. Thirteen of the
fourteen "disagreements" were the auditor's mis-specification, not the atlas's error.

Re-posed with the oracle matched to the objective, the audit is **well-posed on 15 of 28 rows** and returns
**12 agree / 3 disagree** — of which one is a scope limit predicted in advance, one compares against an
`n.a.`, and exactly **one is a genuine errata candidate**.

Three things make it worth an entry:

1. **A wrong prediction did more work than a right one would have.** Had the prediction been silent, a 50%
   disagreement rate would have read as a spectacular finding about the atlas's cited cells — the sort of
   number that travels. Had it been fully right, it would have confirmed and moved on. It was the MISMATCH
   between predicted and observed pattern that located a defect in the instrument.
2. **The failure mode is the netting trap wearing a third hat.** The audit was measuring an oracle against
   a question it does not answer — the same shape as scoring a lookup as a prediction (instance 21) or
   scoring recruitment bookkeeping as sociology (instance 23). *Ask what the oracle actually classifies
   before comparing its output to anything.*
3. **The honest consequence shrinks the instrument.** The 13 VCSP rows are `open`: this repo pins no
   decision oracle for Min-Ones/Max-Ones, and KSTW Thm 2.12/2.14 classify APPROXIMABILITY. Under
   not-pinned-is-not-cited that is the end of it, and the audit ships covering 15 rows rather than
   pretending to 28.

---

## Instance 30 — 2026-07-25 — the starvation gate was one-sided for eleven columns before anything noticed

The census-before-seal rule (`Anatomy-SCHEMA` §3.3b) starves a column whose **modal value swamps the
population** — `starved = modal_share > 0.90 or n_levels < 2`. It has governed every Anatomy column since
S0.

Marrow's `presentation` column walked straight through it: modal share **4%**, eleven levels' worth of
headroom under the ceiling, `starved = False`, admissible for a sealed bet. It has **28 distinct values on
28 rows** and not one cell clears the Cochran floor of 5.

> **A column with as many levels as rows is a ROW IDENTIFIER, and carries exactly as little contrast as a
> constant does. Both ends are starvation; only one end was being checked.**

The gate was written against the failure that had actually occurred — `self_reducibility` at 342/345 modal,
`objective_type` with a 2-row level — so it learned one direction. Nothing in v1 was dispersed enough to
expose the other; the first genuinely high-cardinality column found it immediately. The fix is one
condition, and it uses a floor the schema already carries: **if no level clears the Cochran floor, no
contrast is posable.** `presentation` now ships correctly as descriptive-only.

**The reusable form:** a gate built from the errors you have seen checks the directions you have seen. When
a new column is the first of its KIND rather than the first of its topic, re-derive the gate's condition
from the principle rather than trusting that it generalised. The principle here was never "modal share must
be low" — it was always *"some cell must clear the Cochran floor,"* and only one of its two failures had
ever been written down.

---

## Instance 31 — 2026-07-26 — a verdict that no input could have changed (the factors gate, Marrow M1)

Instance 28 left `*factors*.json` out of `_watched()` in writing rather than in silence, because adding it
surfaced **16 unacknowledged extremal values** across three artifacts nobody had read, and dropping 16 unread
numbers into `LEGACY` would have been the rubber stamp the table exists to prevent. That was the right call
and it came with a debt. This entry is the adjudication, one at a time, and the pattern is now in the
watched set.

**Ten were benign, with arithmetic to show for it.** Seven in `factors_v1_1.json`: four are the *k*=0
self-identity — k=0 IS the marginal baseline every gain is measured against, so `gain_over_k0` and its null
percentile are 0.0 by construction on the real table and on all 60 permutations. Three more, at ranks 1/3/4
of the core-4 arm, are a subtler thing worth naming: `null_gain_p97.5 = 0.0` is a **real percentile of a
genuinely coarse distribution**. That arm masks 6 cells and averages 4 repeats, so null gains land on a
1/24 lattice; 59 of 60 permutation draws are ≤ 0 and 12–14 sit at exactly 0, so both order statistics the
97.5th percentile interpolates between are 0.0. Coarse is not absent. Three more in
`factors_sensitivity.json` are recovery fractions of 8/8 on a power curve, where saturation at strong
separation is the design intent. One more, invisible to the gate and acknowledged anyway, is the k=1
mixture's class prior of 1.0 — there was one place for the mass to go.

**Six were a real flaw — the entire remaining block — and it is the kind this whole apparatus was built
for.** `factors_v1.json`'s
`excess_over_null` block reported `real = null_mean = p2.5 = p97.5 = 0.0`, `one_sided_p_ge = 1.0`, and a
verdict `excess_over_typing: false`, over **M = 150 drawn S1 nulls**. The statistic is
`acc[k_hat] − acc[1]`. The primary had returned k\* = 1. So the statistic was `acc[1] − acc[1]` — the same
float minus itself, **identically zero on the real table and on every null**, and the p of exactly 1.0 is
the plus-one form `(150+1)/(150+1)` reporting that faithfully. Every number in the block was forced by the
expression. *The identical block would have been emitted by an atlas with overwhelming latent structure.*

**The tell was not that the numbers were wrong. It is that they were unfalsifiable.** A null result and a
vacuous comparison print the same way, and 150 MCMC nulls were drawn, fitted, and discarded to produce a
verdict no data could have moved. Direction matters, per instance 22: this one pointed the *unflattering*
way — it under-claimed, agreeing with a k\*=1 the primary had already found — which is precisely why it
survived. A pessimistic number attracts no scrutiny. **A gate that only interrogates flattering exactness is
a gate that would have missed this one.**

**The prose already knew.** `Factors-v1.md` carried caveat R-iv — *degenerate once k\*=1* — while the machine
output next to it reported an envelope placement and a false verdict. The findings doc was ahead of the
artifact, and nothing mechanical was checking that they agreed. **A caveat in the narration does not
discharge a claim in the artifact**; a reader who trusts the JSON never sees the caveat.

**Two hypotheses were tested and killed before that conclusion.** Instance 26's floor is the right first
prior, so it was checked first: nothing on this path clamps (unlike `structure.cramers_v`'s Bergsma floor),
and n is 114, not 22. And the sibling `k/M` p-form defect does not apply either — `_envelope` already uses
the plus-one form, and with every null tied to the real value it returns `(M+1)/(M+1) = 1.0`, **exactly what
`k/M` gives**. Plus-one rescues the *lower* boundary, where "no draw reached it" is unprovable; at the upper
boundary "every draw was ≥ real" is directly observed. The 1.0 is honest arithmetic. What is defective is
the vacuity of the comparison it summarises — a third species, distinct from both prior instances.

**Resolution, and what instance 26 changed about its shape.** `factors.excess_over_null` now detects the
collapse (`len({1, k_hat}) < 2`) and returns `applicable: false` with the reason, drawing **no** nulls.
`excess_over_typing` is `null`, not `false`, because `false` is a test outcome and no test was had. But the
**gain keeps its 0.0** — a first pass encoded it as `null`, which is exactly the remedy instance 26
retracted: it asserts NOT COMPUTED about a value that was. It ships instead with an acknowledgement carrying
the identity. The envelope *is* dropped, on a different ground worth separating: not unmeasured but
**undefined** — a constant has no distribution, so its percentiles are not numbers that were missed. All
acknowledgements are **derived from each run's own numbers** (atom counts, lattice resolution, seed counts,
the collapsed k-set), so each disappears when its cause does instead of lingering as a stale excuse.
`factors_v1.json`'s k\*, ablations, LOCO, MCA sensitivity and loadings are **byte-unchanged**; k\* = 1
stands, and it never rested on this block.

**A second thing fell out of reading the same file.** `factors_sensitivity.json`'s note asserted that
recovery *falls to ~0 by modal_p = 0*, confirming the estimator is not trivially always-detecting. Its own
curve says **0.5** — at zero separation, with nothing planted to find, the 1-SE rule still returns k\*≥2 in
4 of 8 seeds. The findings doc had this right too (R-v names the uniform-marginal false-positive); the
artifact's note did not. Corrected, with the mitigation stated at its own size rather than as a dismissal:
the zero-separation generator draws cells uniformly, a weaker k=1 baseline than the canon's skewed
marginals, so that rate is an upper bound on the canon's. The floor is now reported beside the base rate it
must be read against, because **a detectability floor quoted without its false-positive rate is half a
statistic.**

**A blind spot, stated rather than left to be found.** The tidy-number walker descends into dicts only — a
float inside a JSON **array** is invisible to it, while its sibling in `check_lift_denominators_match`
recurses into lists. That is why the k=1 class prior above needed acknowledging by hand. It is written into
the check's docstring rather than fixed here: closing it widens the gate across every watched artifact at
once and will surface a fresh batch of unread numbers, and that batch deserves the same one-by-one
adjudication these 16 got. **The lesson of instance 26 was that a flag is a question, not an answer. The
lesson here is that widening a gate faster than you can answer it just relocates the debt** — which is the
same lesson instance 28 drew when it held this pattern back, now closed from the other end.

---

## Instance 32 — 2026-07-26 — chat is not an artifact, and the gate got cheaper again

The consolidation writeup opened with one law: *every number traces to a frozen artifact by hash, and the
draft contains no claim not already in a scored, sealed, or frozen record.* W0's first deliverable was
therefore not prose but the **claims-to-artifacts map** — and the map's first act was to reject three of
the nine assertions it was given.

**All three arrived the same way: from reviewer chat synthesis, not from a record.**

| candidate | what the search found | resolution |
|---|---|---|
| two-pole certificates (blending / pairwise-independence) | zero repo matches, any spelling; only scattered ingredients | **recut** — easy pole folded into an assertion where it was already load-bearing; hard pole demoted to banked, survey-confidence |
| "the unwritten theorem" | zero matches for the phrase | **receipts existed under a different name** — the free-placement disk-cover retraction; assertion stands |
| "census localization" | `localization` in the repo means only the Boolean-engine sense | **renamed** to the repo's own word, `backbone` |

Three distinct outcomes from one cause, which is the useful part: **an unsourced claim is not automatically
a false claim.** One was over-claimed and had to shrink, one was correct but misnamed, one was correct and
merely pointed at the wrong vocabulary. A gate that only ever deleted would have destroyed the second and
third.

### The trend line, which is the entry's real content

This is the **fourth** catch of the same species, and the cost curve is the point:

| # | catch | cost to catch | cost had it landed |
|---|---|---|---|
| 1 | the phantom OR | a directive refused mid-flight | a fabricated effect size in a verdict |
| 2 | the void close-out numbers | a directive refused mid-flight | a fabricated close-out |
| 3 | the Marrow forward-reference | one search, before planning | a spec asserted into existence in a findings note |
| 4 | **three assertion-candidates** | **one search pass, before any prose** | **three unsourced claims in the program's headline document** |

Each catch has come **earlier in the pipeline and cost less**, because each one moved the check further
upstream: from refusing a directive, to searching before planning, to a map that must be built before a
sentence may be written. **The ledger predicts this shape and this is the first time it has been visible
across four instances of one class.**

### The rule, stated so it binds the next document

> **A claim whose only provenance is a conversation is UNSOURCED by definition** — however confidently
> stated, however senior the speaker, and however true it may turn out to be. Chat summarises artifacts;
> it does not become one. The remedy is never "trust the summary", it is *find the artifact, rename the
> claim to match it, or bank the claim until one exists.*

The corollary that made this cheap: **build the map before the prose.** A claims-to-artifacts map written
first is a filter; the same map written afterwards is a citation exercise that finds what it was pointed
at. Every one of these three would have survived a retrofitted map, because each would have been handed a
plausible-looking pointer by the same synthesis that produced it.

**And the distinction that keeps the law usable:** it binds *claims and numbers*, not exposition. An
expository frame introduced to teach a result is new prose and is allowed to be — recorded as `framing`
with its origin, carrying no claim. A law that forbade new sentences would forbid writing the document.

---

## Instance 33 — 2026-07-26 — the third way one gate silently did not watch

The Geometry Probe qualification study put a new results file in `foundry/foundry/results/lattice/`. The
tidy-number gate passed it — while the file contained four sensitivities of **exactly 1.0**.

**The gate's lattice path was wrong, and had always been wrong.** It read
`d.parent.parent.parent / "foundry" / "foundry" / "results" / "lattice"`, one `.parent` short, resolving to
`eightfold/foundry/foundry/results/lattice` — a directory that has never existed. And then:

```python
if lat.exists():
    roots.append(lat)
```

**the guard made the miss silent.** No error, no warning, no empty-directory complaint. The gate reported
PASS over files it had never opened, and had been doing so since it was written.

Every Foundry lattice artifact was uninspected, including `grid_arm_a_results.json` — whose `1.000`
positive control is quoted in the write-up as assertion 5. Fixing the path surfaced three previously-unseen
extremals immediately; all three are explainable and now itemised, and one is the documented arithmetic
flag leak retained deliberately as evidence.

### Three distinct mechanisms, one shape

This is the **third** way this single gate has silently failed to watch something:

| # | mechanism | how it was found |
|---|---|---|
| 1 | glob scoped to one project's filenames (`grid_*results*.json`) | Terroir's own results file was invisible to it |
| 2 | walker descends into dicts only — a float inside a JSON array is unreachable | found by reading the walker while adjudicating another project's extremals |
| 3 | path resolved to a directory that does not exist, guarded by `if exists()` | a new file in the unwatched directory passed while carrying four exact 1.0s |

> **All three FAIL OPEN.** Each reports a clean pass over things it never inspected. **A gate that cannot
> distinguish "inspected and clean" from "never looked" is not a gate** — it is a green light wired to
> nothing.

### The rule this earns

*An existence guard around a scope is a silence generator.* `if path.exists()` is the correct idiom for an
artifact that may legitimately not be built yet; it is the **wrong** idiom for a directory the gate's
coverage depends on, because the failure it hides is indistinguishable from success. Where a gate's scope is
load-bearing, **assert the scope is non-empty and resolve it through the package rather than by counting
directory levels from a sibling** — which is the idiom `_eightfold_atlas()` had used correctly all along, two
functions above the bug.

The permanent test asserts the real lattice directory is in the watched set and names both files that were
missing. That is the pattern from the denominator gate and the fabrication probe: **a check never observed
to fail is not known to work**, and a check whose *scope* can silently empty needs its scope pinned too.

---

## Instance 34 — 2026-07-26 — the gate that never looked was guarding a number in the paper

Instance 33 fixed the tidy-number gate's lattice path and surfaced three extremals in Arm A's results that
had **never been inspected**. This entry is what adjudicating them found, and it is worse and better than
expected.

### Both first readings were wrong, and the same way

Writing the LEGACY entries, I read the *narrative* — Arm A had a documented arithmetic flag leak, and
`1valid` recovered at exactly 1.0000, so I recorded the leak as the mechanism. **One comparison refutes it.**
The `clean` run drops precisely the leak moments (`weight_mean`, `weight_spread`) and `1valid.acc` is
**still 1.0000**. Dropping the cause did not move the effect.

The real mechanism is the finding itself: `1valid` is **membership of one specific tuple** — is the all-ones
tuple in the relation — and surface order structure determines that exactly. Arm A's whole result is that
surfaces see membership and not closure. **The 1.0 is assertion 5's positive control**, not a defect.

And `ceiling` is not a measurement at all: `grid_arm_a.py:112` writes `"ceiling":1.0` as a **hardcoded
literal**. A new species for this gate — *a documentation constant living in a results artifact*,
indistinguishable to any reader from a computed value.

> **Third time diagnosing from artifact shape instead of expression** (instances 26, 28, and now this).
> The rule was already written. Applying it is a separate act from recording it, and the gap between the
> two is where these keep happening.

### The catch underneath: the draft had overstated a negative

Adjudicating forced a comparison of every per-flag recovery against its null, and that surfaced something
the extremal check was not looking for. The draft said *"every closure target scored at or below its
null."* **Three score above it** — `strongly0valid` +0.0439, `width2affine` +0.0108, `affine` +0.0103.

The source findings note had **always** said so, and dismissed them correctly: those nulls sit at 0.95–0.98,
so a one-point lift on a near-constant flag is noise. **The draft dropped the qualification and kept the
conclusion.** That is inflation of a negative result — the both-directions failure in its less obvious
direction, where a clean sweep reads stronger than an honest five-of-eight.

**W3's both-directions read did not catch it**, and the reason is instructive: that pass was a regex for
softening and overclaim *words*. No vocabulary check can catch a claim that is confidently worded, sourced
to a real artifact, and simply broader than what the artifact says. **Comparing a claim against its source
is a different operation from scanning it for hedging**, and only the first would have found this.

### What now exists because of it

- **`gate-checked: <date>`** on claims-map rows. Assertion 5's evidence was quoted from a file no gate had
  ever opened; absence of the field now means nobody has checked.
- **The meta-gate.** `hardmap verify` asserts that every numeric gate inspected a non-empty file set, and
  **fails** on zero. Three historical fail-opens — a glob scoped to one project's filenames, a walker that
  descends into dicts only, a path resolving nowhere — become one impossible class: *verification that
  verified nothing must say so.* Probe-tested by planting an empty root and by resolving none at all.

---

## Instance 35 — 2026-07-26 — a shape forced by its denominator, caught before first citation

The Geometry Probe's qualification study answered its pre-registered free question with what looked like a
real finding: 85–99% of nonzero blend-violation rates in a 0.05–0.50 "almost-closed" middle band, **not one**
of 4,028 classes violating majority-closure above 0.50, and the reading that *the dichotomy's binary carves
a continuum near its bottom end*. A pre-claim check was directed before it was quoted anywhere. **It does
not survive.**

**The mechanism.** The blend operations are idempotent on repeats — `maj(a,a,b) = a`, `minority(a,a,b) = b`,
`min(a,a) = a` — so a tuple containing a repeat lands back inside the region *by construction* and **cannot
violate**. Rates were computed over `product(rel, repeat=m)`, the full Cartesian product. Every denominator
therefore carried a large block of tuples incapable of moving the numerator, and each rate was capped at the
all-distinct fraction `r(r−1)…(r−m+1)/r^m`.

**The ceiling was the cap, and the arithmetic says so exactly.** At r = 3, 4 and 5 the maximum observed raw
rate *equals the cap* — 0.2222, 0.3750, 0.4800 — meaning those relations violate on **every** distinct
triple and their true rate is **1.0**. 527 classes sit at r ≤ 5, capped below 0.50 by counting alone. Under
the typed null, **341 classes** exceed 0.50 on majority rather than none, and the middle-band range is
0.31–0.90 rather than 0.85–0.99, with minority — the most striking raw figure — collapsing hardest, 0.99 to
0.31.

Retracted before first citation, per the rule sealed with the check.

### Why this is its own species

The tidy-number family has been about a single value being too clean. **This is the distribution-grade
member: the SHAPE was forced, not the value.** No individual rate was wrong — every one was correctly
computed — and no extremal check would ever have fired, because the numbers were unremarkable. It was the
*pattern across them* that carried a claim the denominator had already determined.

> **Before narrating the shape of a distribution, verify the shape is not forced by the denominator.** The
> typed null for a rate is the rate conditioned on the cases that could have moved it. A statistic whose
> range is mechanically bounded will produce a "band" and a "ceiling" whether or not the world has either.

### Two things that made the catch cheap

**The concern arrived as an alternative mechanism, not as doubt.** "Idempotent operations cap the rate at
the all-distinct fraction" is checkable in one expression and one division. Vague scepticism would have cost
a re-run; a named mechanism cost an arithmetic identity — `bad_raw == bad_distinct`, so
`rate_distinct = rate_raw / cap`, no re-enumeration at all.

**And reading the expression first was the whole of part 1.** `for ts in product(rel, repeat=m)` settles
whether the concern is live before any recomputation is designed. That is the third consecutive incident
where the expression answered in one line what the artifact could not answer at all — and the first where
the rule was applied *first* rather than after a wrong diagnosis.

**Scores 1 and 2 were never in question and are untouched:** the battery is a binary that repeats cannot
flip, and sensitivity asks only whether *any* violation was found. The instrument is still QUALIFIED. What
failed was the free question's answer, which is the part that was free.

---

## Instance 36 — 2026-07-26 — a fix that was the failure it fixed, and the half of it that survived

Design law 3 excludes theorem-forced flavours from any discovery statistic **by schema** — written into the
emitting code after the pilot found 42% of an apparent separation was forced zeros leaking into the
measured mean. Enforced in code, which was the right instinct.

Enforced *against a hand-written dictionary*.

The survey found it: ten readings returning **exactly 0.0** while not flagged forced, several of them
plainly forced and simply absent from the list. `vertex-cover`, `independent-set` and `clique` feasible
regions under majority are all Γ of 2-clauses — bijunctive, hence majority-closed — and none was listed.

> **A hand-maintained list of theorem-forced pairings is rules-that-live-in-recall wearing the costume of
> the fix for it.**

The closure was a join neither artifact had made though both computed its inputs: Marrow pins a template
per row and derives its closure flags; a polymorphism of Γ holds on every instance's solution set. So
forcedness becomes **derived provenance instead of remembered provenance**, with two boundaries that had to
be kept apart — `optimal` regions are sub-level sets and inherit nothing, and *underivable* is a third
state that is not *false*.

### The part worth the entry: the derivation lost something true

`matching`/feasible/min reads exactly 0.0. The template route calls it underivable. **But matchings are
subset-closed by a one-line argument**, and no finite template is involved — the old hand list had that
entry and **it was correct**.

The clean-sounding rule *"derive, don't list"* would have deleted a true fact in the name of rigour. The
rule that actually survives contact is narrower and less satisfying:

> **No entry without a reason — derived in code, or written as an argument that ships with it. What is
> banned is the unjustified entry, not the human one.**

Three asserted entries now carry their proof sketches. Four residual exact-zeros were left **unadjudicated
and banked**, because asserting them would have been doing the analysis a survey is not entitled to do —
and because the point of flag hygiene is to make a residual *meaningful*, not to keep shrinking it until
nothing is left to explain.

---

## Instance 37 — 2026-07-26 — interpolation-by-absence: a missing reading is a claim of continuity

Sounding v3's ramp declared 91 steps. Two of them produced no region at all — sudoku at 12 clues, `sat-3`
at clause ratio 5.5 — and those two steps were simply **not present** in the artifact. No error, no null,
no record. The readings on either side sat adjacent in the file.

Which means the trajectory **read as continuous across a hole nobody drew.** A reader joining the
surviving points gets a smooth curve through a region where the instrument never spoke.

### Why this is its own species

The program already forbids interpolating across an INSUFFICIENT step. That rule was obeyed. The defect
slipped past it because **the violation does not look like a violation — it looks like nothing.** An
INSUFFICIENT step is visible and must be argued past; an absent step has nothing to argue with. The rule
was written against a mark on the page and the failure arrived as a blank.

The general form, which is what goes in the taxonomy:

> **An absent reading is a claim of continuity unless the absence is itself recorded.**

This is the **silent gate one level down** — fail-open by omission. The silent gate passed because it
inspected nothing; this passed because it *reported* nothing. Same shape, different layer: in both cases
the absence of evidence rendered as evidence of absence of a problem.

### The fix, and the two places it had to be applied

`GAP-no-region` as an explicit record type, carrying its reason. Then the same failure had to be caught
**twice more in the same day**, in the machinery built to honour the rule:

1. **The trajectory report's own plots bridged gaps** until the line-drawing was changed to break at nulls
   — the report enforcing the rule was breaking it in its rendering.
2. **Two different absences were being drawn identically.** A step-level GAP (no region produced, reason
   recorded) and a *combination-level* absence (a region existed, but not for this region/flavour, **no
   reason recorded anywhere**) were pooled under one label. And both were marked with the same glyph as an
   INSUFFICIENT step — which is not absence at all, but **speech ruled inadmissible.** One mark for three
   states says the instrument was silent when in fact it spoke and was overruled.

The third of those is the one worth keeping: the taxonomy needs to distinguish *nothing happened*,
*something happened and went unrecorded*, and *something happened and was excluded by a declared rule*.
Only the last is honest by default; the middle one is the dangerous one, and it had no name until it was
counted (10 cells).

### The same species caught twice more in the closure tests, minutes apart

Within the same session's zero-hunt:

- The brute-force closure check returned `NOT TESTED` for all ten claims — wrong builder signatures — and
  **the run still printed a clean adjudication table** asserting the claims were tested. An untested claim
  is now a **hard failure** of the script rather than a footnote in its output.
- Then the test, once running, manufactured **two false falsifications** by truncating regions to 600
  members before checking union-closure. A truncated set is not the set. The tell was that every failing
  region was *exactly* 600.

The first is fail-open by omission again. The second is its mirror — **fail-closed by mutilation**, where a
check corrupts its own input and reports the corruption as a finding about the world. Both were caught only
because the output was read against what it should have looked like, not merely for whether it was green.

---

## Instance 38 — 2026-07-26 — the same asymmetry wearing the other face

The derived forcedness join excludes flavours a region is **closed under** — violation forced to 0. It had
no exclusion for flavours a region is forced to **leave** — violation forced to 1.

It was built to stop a theorem manufacturing a **null**. The same theorem manufactures a **hit**, and for
as long as the join existed it was blind to that direction.

Terrain's I-phase found it while grounding a seal, not while auditing the instrument: **58 of 92 admissible
positive-excess readings sat at `measured_rate` exactly 1.0.** Not near it — *at* it, with zero readings in
[0.99, 1.0). They were **29 `min` and 29 `max`, never `majority` or `minority`**, arriving in pairs on the
same (row, region), which is the signature of a region whose defining constraint is broken by *both* union
and intersection. Their excess is `1.0 − control_mean`, positive against any non-saturated control. **They
carried 45.5 % of the anomaly's total positive excess.**

The forced-credit trap is now netted at **five** scales: statistic, type signature, study design,
per-flavour mean, and **the join's own direction**.

### What made it findable

Not vigilance. The **tidy-number gate**, pointed at a new census artifact and refusing to accept
acknowledgments it could not tie to a structural argument. Two extremals halted the script; reading them
produced the constructive arguments; the arguments generalised into the screen. A gate whose acknowledgment
block accepts anything would have passed all of it silently.

### The fix, and the check that narrowed it

`forced_saturated` ships as a derived direction with the same schema exclusion, resting on five one-line
theorems (optimal regions, exact-equality regions, opposed-closure intersections, fixed-cardinality
regions, path regions). 144 readings flagged.

**The first version of the argument was too strong and the data caught it.** Rule S1 said "min of two optima
is smaller and max is larger, so neither is optimal" — true only when the objective is **coordinatewise
monotone**. `max-cut` (a quadratic form, optima in complementary pairs) and `max-flow` (value under
conservation) read 0.9429 and 0.9064, not 1.0. The derivation now **names the objective per row** and
excludes the two non-monotone ones with their reasons.

The check that caught it is the entry's second half: a derived flag nobody tests is a hand list wearing a
derivation's costume. The derivation is compared to observation in **both** directions — claims saturation
where the data disagrees (halt), and exact-1.0 readings the derivation misses (report). The final state is
0 contradictions and 0 admissible-and-uncovered; the 15 uncovered exact-1.0 readings all sit below the
pre-declared `INSUFFICIENT-r` floor, which is small-sample saturation rather than theorem saturation.

### The seal it changed

Removing the 58 dropped the anomaly from 92 readings to 34 — and **stripped almost all of the study's
tier-2 coverage with them**, because the saturated readings were disproportionately `optimal`-region, which
is the only kind where a matched-object control exists. The kill clause fired at 1/34 rather than 31/92,
and the design went single-armed. A screen applied for honesty made the study weaker, which is the correct
order of operations and worth recording as such.

---

## Instance 39 — 2026-07-26 — two rules that make a declared property as safe as a derived one

N4 converted the zero-hunt's 29 prose adjudications into a standing schema: a region declares a structural
property, and its forced flavours derive mechanically in both directions. That is only safe because of two
design choices, and both are promoted here because either one softened would reintroduce the disease the
derivation was built to cure.

### Contradictory implications are a HARD ERROR, never a precedence rule

A region may declare several properties. `upward_closed` implies `max`-closed; `fixed_cardinality` implies
`max`-**saturated**. If both were declared on one region, the flavour has two incompatible derived flags.

The tempting fix is a precedence rule — prefer the more specific, prefer the later, prefer the verified-
first. **Every one of those hides the actual fact, which is that one of the two declarations is wrong.** A
precedence rule turns a detected contradiction into a silently-resolved one, and the check exists precisely
to surface the wrong declaration. So the contradiction halts.

### An unverified declaration is DROPPED, not downgraded

A declared property is a hand-written entry wearing derivation's clothes unless it is mechanically
verified. The obvious softening is to keep an unverified declaration with a warning flag — and that is the
`rules-that-live-in-recall` failure returning under a new name, because a warning that ships is a warning
nobody reads.

So verification is a gate, not an annotation: `upward_closed` and `downward_closed` are checked
exhaustively over every single-bit raise and clear; `pairwise_exclusion` derives the conflict set from the
region and then confirms it **characterises** membership, so a region with any non-pairwise constraint
fails rather than passing on a coincidence.

    derive  UNION  assert-with-argument  UNION  verify-on-declare

### What made the pair necessary rather than tidy

The property route is strictly more powerful than the template route — it reaches rows with no finite
bounded-arity template, which is where 29 of the survey's zeros lived. Power is exactly why it needed the
guard: a route that can express more can express more that is wrong, and the template route's authority
came from being checkable rather than from being narrow.

15 of 15 declarations verified on first run once two builder mistakes of mine were fixed. Zero
contradictions. Zero derived flags disagreeing with observation.

---

## Instance 40 — 2026-07-26 — the flag was right about the template and wrong about the data

`theorem_forced = True` asserts that violation is **forced to zero**: a polymorphism of the pinned template
is closed on every instance's solution set. The flag was derived, stamped, and used to exclude readings
from every discovery statistic in the program.

**Five readings flagged forced-to-zero measure 0.1177, 0.4358, 0.4532, 0.5343 and 0.6074.**

All are `horn-sat · solutions · min`, and the cause is four lines into the generator:

```python
elif mode == "horn": ok = any(vals[i] == sg[i] for i in range(k))
else:                ok = any(vals[i] == sg[i] for i in range(k))
```

The branches are **byte-identical**, and `sg` is drawn uniformly at random. A Horn clause has at most one
positive literal; nothing enforces it. **`horn-sat` emits plain random 3-CNF.** Marrow pinned a Horn
template for the row, the join correctly derived `horn ⟹ min forced`, and the derivation was sound.
**The instances were not what the row said they were.**

### What actually failed is the check that never existed

When `forced_saturated` was built (instance 38) it shipped with a two-way comparison against observation —
claims saturation where the data disagrees, and exact-1.0 readings the derivation misses. It found zero
contradictions and that felt like diligence.

**Its older sibling never got one.** `theorem_forced` had been in service for the whole survey sequence
without anyone once asking whether a flag that says *"this reads zero"* sits on a reading that reads zero.
The contradiction was one comparison away from the day the join landed, and the comparison was written only
because a *different* direction of the same flag got built later and got a check by habit.

> **A derived flag is only as good as its comparison to the thing it predicts — and the first version of a
> flag is the one least likely to have one, because nothing has gone wrong with it yet.**

### The boundary the fix respected

The readings are **valid measurements of a plain 3-CNF row**. What was wrong is the label and the flag
derived from it. So: the flag was corrected with provenance naming the defect, measured values were
fingerprinted before and after and verified unmoved, and **the row was not renamed, no instance
regenerated, nothing re-measured.** Renaming a survey row is a ruling, not a hygiene fix.

Terrain is unaffected — none of the five had positive excess, so none would have entered its anomaly set.
Checked rather than assumed, because "my earlier result is probably fine" is exactly the inference this
ledger exists to distrust.

---

## Instance 41 — 2026-07-26 — the retrofit sweep, and a conformance test that tested a copy

Instance 40 found one drifted generator by accident, while grounding an unrelated study. The general form
was ruled immediately: **every generator with a pinned template is suspect until checked**, because the
same four-line copy-paste could sit anywhere.

### The check had to be semantic, not syntactic

The tempting version reads clause shapes — Horn means ≤1 positive literal, bijunctive means width 2. That
tests a proxy and only works on clausal generators, which is 3 of the 9 templated rows.

The universal form is the implication the join actually consumes: **if the pinned template is closed under
f, every emitted instance's solution set must be closed under f.** That is what a polymorphism *is*. It
holds for graph generators, packing generators and clause generators alike, and a generator failing it has
drifted whatever its source looks like.

Both run where both apply: **semantics detect drift, syntax localises it.** A row failing semantics with
clean syntax means the template is wrong; failing both means the generator is. `horn-sat` failed both.

**Result: 9 templated rows swept, 1 drifted, 8 clean on both axes.** The fleet is now conformance-checked
by schema rather than by accident.

### The part worth the entry: the first version tested a copy

To read clause shapes the sweep needed the clause list, which the generator did not return. So the sweep
**reimplemented the generator** — and that is a conformance test of a copy, which certifies nothing about
the thing in service.

It proved the point within minutes. After the real `horn` branch was fixed, the sweep **still reported
`horn-sat` as drifted**, because it was checking the reimplementation, which still had the old emission
rule. Had the fix and the copy happened to agree, the sweep would have reported PASS while testing nothing
that ships.

> **A check must consume the shipping artifact, never a reconstruction of it.**

That is **chat-is-not-an-artifact (instance 32) turned instrument-side**. There the rule was that a claim
must cite a record rather than a recollection; here it is that a check must exercise the code in service
rather than a parallel copy of it. Same principle, two faces: *the thing verified must be the thing that
ships.* A test that reimplements its subject tests the reimplementation — the subject must be called, not
mirrored, and where that requires the subject to expose something, expose it.

The generator now publishes `LAST_CLAUSES` and the sweep reads it. The fix is small; the failure mode it
closes is the same fail-open species as the silent gate and interpolation-by-absence, one layer further
out: **the check ran, reported, and was about the wrong object.**

### The standing practice this installs

New machinery gets built to the current standard while old machinery grandfathers in. `forced_saturated`
was born with an observation-comparison check; its elder sibling `theorem_forced` never had one and served
the whole survey sequence unchecked.

> **When a new check class is invented, ask which existing instruments predate it.**

That question is now standing practice rather than a thing that happens when something breaks. This sweep
is its first discharge, and it found the fleet clean apart from the row already known.

---

## Instance 42 — 2026-07-26 — "notable" needs a base rate the way an excess needs a control

The zero-hunt's vocabulary had three ways to explain a zero — a theorem (HIDDEN-CLOSURE), the instrument
(ENCODING-ARTIFACT), or too few subsets for a nonzero rate to be **observable** (THIN-SATURATION) — and
GENUINE-READING for *none of the above*. Two readings survived as genuine.

**Both were ordinary.**

N3 found the fourth class by measuring it: at r = 22, 231 distinct pairs were available and a nonzero rate
was perfectly observable. It did not occur because **64.5 % of random 2-CNF solution sets with r < 25 are
min-closed**. The same lens applied to the other survivor returned 24.5 % at r ≈ 10. **The hunt's residue
is zero.**

    ORDINARY-AT-SIZE — admissible by every floor, unexplained by theorem or artifact, and unremarkable
    against the size-conditioned base rate of the phenomenon.

### The distinction the old vocabulary blurred

THIN-SATURATION asks **could the instrument have spoken?** ORDINARY-AT-SIZE asks **was what it said
unusual?** Those are different questions and the hunt only had machinery for the first. A reading can clear
every observability floor — sufficient r, sufficient distinct subsets, a control that varies — and still be
exactly what typically happens at its size.

> **"Notable" requires a base rate the same way an excess requires a control.**

The program had internalised the second half completely: every reading in the survey column carries a
size-matched null, and Terrain exists because that null was not fair enough. It had not noticed that the
same demand applies to *categorical* claims. An exact zero was treated as self-evidently interesting; it
needed a denominator too.

### Two things this cost, and both are recorded

**The residue was the point.** The zero-hunt's value was partly that it left something unexplained — a
residue is what tells you the screen was not tuned until nothing remained. That residue is now gone, which
is the honest outcome and also a loss: the hunt no longer has a witness that it was not over-fitted. What
replaces it is that the dissolution was *measured*, with a rule declared before the measurement.

**One of the two calls is weak.** sat-2 cleared the 0.20 floor by 0.445; independent-set cleared it by
0.045. Both are correct by the declared rule, and the second is the one to re-examine first if the floor is
ever revisited. Recorded in the artifact rather than left to be rediscovered.

---

## Instance 43 — 2026-07-26 — the contamination was a near-miss on a false mechanism

N6's census joined predictor to outcome before the seal and disclosed the relationship it was about to bet
on. The rule minted from it was **census minimalism**: *a census computes its kill's inputs and nothing
else.* The incident read as a self-inflicted loss of a seal.

**It was better than that.** The disclosed prior — a partial Spearman of **−0.3684**, higher inflation
associating with more negative excess — was re-posed as a blind bet on a held-out synthetic population of
11,855 readings whose outcomes did not exist at prediction time.

**It does not replicate.** Partial +0.0023, inside a permutation null of [−0.0168, +0.0167]. And the
class-clustered block runs **+0.1685 against a null of [−0.033, +0.035]** — decisively *opposite* the
sealed sign, with zero of 500 permutations falling below the observed value.

So the contaminated census had disclosed a **sign that does not survive**. Had the in-sample seal been
allowed to proceed, it would have confirmed it — on the same biased subsample that produced it, with the
predictor's upper range truncated by hull growth, which is selection on the predictor axis.

> **The contamination did not cost a finding. It nearly bought a false one.**

That reverses the incident's accounting. The rule it minted is still right and still standing; what changes
is that the failure it prevented was larger than the seal it cost.

### The third sign, and what it does and does not license

Three estimates now exist, in the order obtained: the original spec's theory-driven guess (**positive**),
the contaminated census (**negative**), the blind test (**≈ 0**, leaning **positive** when clustered).

The blind test leans toward the direction the *theory* guessed and the *contaminated data* contradicted.
That is a satisfying shape and it is exactly the shape to be careful with: at reading level the effect is
**zero**, and the clustered positive is a robustness block rather than the sealed statistic.

> **A negative that happens to flatter the theory's original guess is still a negative.**

Recorded verbatim because the temptation it forecloses will recur. The pull toward reading a null as
vindication is strongest exactly when an earlier, discarded guess pointed the same way — and the clustered
block is banked as **Q15**, a sign-flips-with-aggregation question with three candidate explanations, not
as support for anything.

### What the discipline bought, measured

Phase 0's control census forecast 84.2 % usable; Phase 3 delivered 82.6 % — accurate to 1.5 points. Every
route was CP, as the census's reasoning about 4 coordinates predicted. The census that *nearly fired a
false kill on its own weighting* went on to forecast its study's coverage to within two points, once the
weighting error was fixed rather than narrated.

And the 963-wide calibration battery certified the instrument before anything froze. Whatever the study
concluded about the mechanism, the machinery is not in doubt — which is the separation that lets a negative
result be believed.

---

## The denominator we chose — Helm wave 1, 2026-07-27

Helm's first sweep enumerated 344 candidates. Two of the screens were wrong, and fixing them surfaced a
rule worth keeping.

Thirty candidates were **correlating arithmetic with itself**. `excess_ref` is a member of the value set
that `excess_max` maximises, so `excess_ref ≤ excess_max` holds always and their rank correlation read
0.976 — the strongest signal in the entire hold queue, and pure identity. Four more pairs were coupled the
same way, including `max_excursion_sd` against the two endpoints it is computed from.

The obvious fix is to stop enumerating them. That fix is wrong.

> **A denominator that omits the questions we knew were bad is a denominator we chose.**

The forking-paths count exists so a multiple-comparisons correction can be computed from an enumeration
rather than estimated from a number someone remembers. The moment the enumeration is curated — even by a
criterion as defensible as "we knew that one was junk" — it stops being a denominator and becomes a
selection, and every correction downstream inherits the selection silently. So the coupled pairs are still
enumerated, still counted in the 344, and **rejected under a named `netting` rule** whose reason is read
off the extractor's source rather than asserted. A future auditor can see exactly what was thrown out and
why, which is the only version of this that is checkable.

The second screen failure has the same shape one level up. Screen 1 checked that each candidate carried a
null, and every candidate did — because **an in-sample null always exists**, the disclosed number having
been computed with it. What a seal needs is a null for *the bet it would become*, on ground that does not
exist yet. Twenty candidates were slated on the strength of a null that answered a different question.

> **A null for the disclosed statistic is not a null for the sealed bet.**

Both defects are the same species: a check that appears to fire, on an object that is not the one the
check is about.

---

## Two from the MCSP ramp pilot, 2026-07-27

The `string` family's ramp was amended by ruling and piloted before use. The pilot was wrong twice, and
caught itself both times — which is the only reason either lesson is stated here rather than discovered
later in a catalog column.

**The dial was not isolated.** The first run drew the planted rearrangement's block count uniformly per
instance while varying the alphabet. Block count drives the number of valid partitions far harder than
alphabet size does, so the ramp read 642 → 203 → 198 → 413 → 384 with within-step spread swamping every
between-step difference. Nothing was wrong with the dial; the experiment simply did not vary it alone.

> **A ramp is not measured until everything but the dial is held fixed.**

**The direction was read off the endpoints.** With the confound removed, the pilot compared the first and
last steps, found the region smaller at the far end, and printed `RAMP CONFIRMED — larger alphabet
tightens`. A leave-one-out check overturned it in one line: drop |Σ| = 2 and the remaining means are
306 / 407 / 310 / 386 — flat under the catalog's own excursion rule. The entire signal was one endpoint.

> **An endpoint comparison is an eyeball claim with arithmetic on it.**

Both defects would have shipped a graded ramp into a column the catalog reads as a trajectory. What
caught the second one — *does the effect survive dropping its most extreme step?* — is cheap, general,
and now required of every family pilot before a declared ramp is used.

---

## Computed, not listed — the species, named after its third win

Three times now, a population that someone enumerated by hand has been wrong in a way that a computation
caught immediately:

1. **the forced-flag list** — hand-maintained, replaced by a derived join
2. **the family ledger** — hand-kept multiple-comparisons bookkeeping, replaced by a view over the trail
3. **the ambient census** (2026-07-27) — three rows named from memory; the computation found **six**,
   acquitted one of the three, and caught one inside a frozen artifact nobody suspected

> **Hand-enumerated populations are memory wearing data's clothes.**

The tell is always the same: the list looks like data, sits beside data, and is cited like data, but its
provenance is somebody's recall at one moment. It cannot be re-derived, so it cannot be checked, so it
drifts silently from the thing it describes.

The fourth instance arrived the same day and is the sharpest, because the *original* typing was the hand
list. The reach census typed 127 rows `REACH-subset` and fired `R3-subset-selection` on `cutwidth`,
`min-sum-set-cover` and `d-hitting-set` alike, attaching identical boilerplate to all three — while each
row's own `canonical_encoding` field said, respectively, "linear vertex ordering", "a linear order on the
sets", and "hit all with <= k elements". The field was there the whole time.

> **A typing that never read the row's own statement is not a typing, it is a guess with a rule name on it.**

The re-adjudication reads the field under a lexicon sealed before it runs. It covers only 32% of the
class, which is reported as the result rather than repaired by widening the lexicon after seeing what it
missed — that widening is a v2 pass, and it declares its phrases first.

---

## Two from the wave-3 rulings, 2026-07-27

**A hold must name its revival mechanism.** Helm's HOLD queue promised that a held candidate revives *by
construction* as the frontier grows. That promise turned out to be family-conditional: the
number-theoretic candidate's family has four `REACH-subset` rows and all four are built, so no reservation
can ever place one on the frontier. Its gap closes only if an unbuilt capture path lands — a build
decision, not a count.

> **A hold that cannot name its revival mechanism is a zombie.**

`HELD-path-gated` is now distinct from `HELD-power`: it revives on a build decision, is re-reviewed at
every capture-path ruling, and **closes as `INSUFFICIENT-by-population`** if the queue completes without
its path. The expiry is the part that matters — an indefinite hold is a claim nobody has to defend.

**A half-applied gate is worse than none.** The encoding-faithfulness gate spans four components —
extractor, builder, loader, sweep. Applying it to two of them would have produced a database whose
`encoding_faithful` column existed and whose queries ignored it, which reads as a working guard and is
not one. Stopping short of starting it, with the repo clean at a good commit, was the right call.

> **Ship a gate whole or not at all.** (Beside verify-before-commit.)

---

## Size is special, and the screens now know it — the wave-4 sitting, 2026-07-27

Helm's first non-empty slate came back four candidates strong. Every one of them involved a
**size-coupled descriptor**: `r_ref` directly, `insufficient_share` (whose flags *fire on* r-floors), or
`bimodality_max` (a coefficient statistic that small overlap samples inflate mechanically).

Size is this program's most-convicted confounder — the deflator, the sixth species, N3's size-driven
closure prevalence. The sweep enumerated four costumes it wears and could not see that they were one
thing, because enumeration has no theory of which variables are dangerous.

> **The sweep's job is enumeration; the screens' job is to know that size is special.**

Three mechanical consequences, all now in `screens.py`:

- **Definitional consumption.** The netting rule barred pairs linked by an identity or a forced order.
  Too narrow: a flag *derived from* a quantity is coupled to it just as hard. `insufficient_share` fires
  on r below the floor, so `rho(r_ref, insufficient_share)` is vacuous rather than structural. The
  flag-derivation graph is data, so the screen reads it.
- **Size marginals are barred, not held.** A pair containing `r_ref` itself cannot be conditioned on r —
  there is no version of that question with size held out, so holding it would be pretending a future
  frontier could rescue it.
- **Everything else size-coupled must present its r-conditioned prior to reach a slate**, and the
  *conditioned* value is what the power screen sees. A strong marginal with a weak partial now fails,
  which is the whole point.

The constructive half is `bimodality_excess`, **declared and not computed**: BC scored against the
matched-r random-control null the control machinery already generates. The excess discipline governs
every blend reading and had never reached the coherence descriptors. Once it exists, the real question
underneath the killed candidates — *is bimodality structured beyond what size forces?* — returns as a
clean candidate.

What makes this an argument for the constitution rather than against the engine: the machine proposed
four confounded bets and **stopped at the slate**, and the sitting caught in one observation what no
screen was built to see. That division of labour is what Helm was bet on.

---

## The typing law's cost-blindness clause, 2026-07-27

The region-formulation audit met two rows — `bilevel-knapsack` and `network-interdiction` — whose
certificate is a subset (the leader's choice) but whose feasibility predicate requires solving the
follower's optimum inside. The tempting call is to type them out: they are awkward, they are slow, and
the queue would get shorter.

They were given an **affordability note** instead, and kept.

> **Expensive is not mis-typed. Conflating them is how a hard row gets quietly reclassified as a wrong one.**

The queue shrinks only for reasons about **shape**, never about **effort**. A typing says what an object
IS; cost says what it takes to measure. A queue pruned on cost while claiming to be pruned on type would
report a clean population that was really a cheap one — and every rate computed over it, including the
misclassification rates this program has just spent a day establishing, would inherit the bias silently.
