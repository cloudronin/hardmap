# Charge Atlas — verification-pass / review guide

The per-cell verification protocol (spec §3.4). Written for both the reviewer and the agent preparing a
change. The validator (`python -m eightfold.atlas validate`) enforces *shape* and the citation gates; this
guide covers what a machine cannot check — **does the cited result actually say this, for this object, under
this encoding.**

## The two named traps

1. **Same-name, different object (R1).** A charge value is only meaningful for the formal object it was proved
   for. "APX-complete" is a fact about the *optimization* version; "#P-complete" about the *counting* version;
   "exp proof size" about an *unsatisfiable instance family* in a *named system*. If the cell's
   `canonical_task` names a different object than the citation actually addresses, the cell is wrong even if
   the words match. Check `canonical_task` against what the source proves.
2. **Encoding shift (I3).** A charge can move under re-encoding. FPTAS/pseudo-poly claims depend on
   binary-vs-unary number encoding; parallelization and approximation can depend on dense-vs-sparse graph
   encoding. Confirm the cited result holds under the row's `canonical_encoding`; log any deviation in
   `provenance.note`.

## Checks (per cell)

- **Check 1 — the citation states the claim, in context.** Open the cited source (compendium entry, theorem,
  table). Confirm the *actual* value, not a paraphrase. A compendium restating another paper is a `claimed`
  pointer, not a primary confirmation.
- **Check 2 — object & encoding match** (the two traps above): the source's object = `canonical_task`; the
  source's encoding = `canonical_encoding`.
- **Check 3 — perspective present** where required: `proof_size` names the proof system; `parameterized` names
  the parameter. A value without its perspective is unverifiable.
- **Check 4 — the citation is real and resolvable** (DOI / full reference / compendium URL), not fabricated.
  Verify it exists.
- **Check 5 — sentinel chosen correctly (R2).** `n.a.` (charge structurally does not apply — `canonical_task`
  must say why) vs `open` (applies, unknown) vs `unmeasured` (applies, nobody measured). Never code an unknown
  as a real value; never code an inapplicable charge as `open`.
- **Check 6 — entailment consistency (R5).** The cell's value must not violate a known theorem against the
  row's other cells (e.g. `counting=FP` with `decision=NPC`). The validator catches the column-expressible
  rules; the reviewer catches the rest and either fixes the data or documents a genuine surprise.
- **Check 7 — `measured` cells (R9).** A `measured`/`measured-scaling` value points to an **already-banked**,
  reproducible experiment (`provenance.experiment` = prereg + manifest + seeds + code_commit), and only on
  charges 6/7/8. A *new* measurement is not atlas work — it is a separate mini-project, queued from a blank
  cell.
- **Check 8 — web citations are snapshotted (R10).** If the citation is a web page (`url`), confirm a
  `snapshot` (Wayback capture or a committed copy under `docs/sources/`) and a `retrieved` date are recorded.
  Prefer a persistent identifier (DOI, book + page) where one exists; snapshot the rot-risk web-only sources
  (the online Crescenzi–Kann compendium, the Complexity Zoo). The validator rejects a bare `url`.

- **Check 9 — the citation establishes the VALUE, not just the topic (R20).** The cited work must *prove* the
  charge value, not merely discuss the problem. An upper-bound paper does not establish `APX-complete` (needs
  the hardness side too); a "sublinear parallel algorithm" does not establish `NC` (needs polylog depth); a
  conjectural bound does not establish membership; a task line must not overstate its citation. If the
  citation covers only one side, add the complementary reference in `note`; if the value is unsupported,
  downgrade to `open` + note. Run this as a pass over each batch before the next. (This gate caught the
  E-1 gcd/NC and E-2 treewidth/APX errors in batch-1 review.)
  - **Counting specifically (F-1):** `counting = #P-complete` requires a **per-problem** #P-hardness result,
    NOT a generic "counting the solutions of an NP-complete problem is #P-complete (Arora–Barak Ch.17)" stamp.
    That pattern is seductive because it is *usually* true — which is exactly why it silently flipped the
    counting column to ~58% pattern-matched before it was caught. No specific citation ⇒ `open`. A column
    that is 96% real and 4% fabricated is worse than one honestly at 42%, because no one suspects it.

## Status & promotion discipline (R8)

- **Default to `claimed`.** A single-source or handbook restatement is `claimed`. The agent fills `claimed`
  with a resolvable citation; it does **not** set `confirmed`.
- **`confirmed` is the owner's call at review**, after reading the primary source (gate 4: `primary_source:
  true` + a citation key).
- **A1 promotion quota (R8):** spot-check promotion of **~2 cells per charge (16 total)**, **decoupling-witness
  rows first** (VC/CLIQUE, permanent/determinant, 2-SAT, XOR-SAT, PHP). **Full-table confirmation is not an A1
  requirement.**
- **"Fully cited" ≠ "fully confirmed."** The A1 gate is `claimed`-or-better with **zero `uncited-folklore`**;
  it is never quietly inflated to "everything confirmed."
- **`uncited-folklore` is a debt.** It is allowed transiently but must be resolved to a citation or reverted to
  `open` before the A1 gate; the validator counts them and the gate requires zero.
