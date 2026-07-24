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
