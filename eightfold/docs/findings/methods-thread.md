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
