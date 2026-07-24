# Trust labels — what each atlas version's cells actually mean

Published per owner ruling 2026-07-24 (condition 1 on the v3 freeze). `frozen` is a byte-identity claim,
NOT a claim that a human confirmed every cell. This file states, per version, how many cells carry the
`confirmed` label (owner read the primary source, Gate 4) versus the weaker labels — so no reader mistakes
`frozen` for `owner-confirmed`.

## The status ladder

| status | meaning | who can set it |
|---|---|---|
| `claimed` | a value with a citation, not owner-confirmed | agent (default) |
| `confirmed` | owner read the PRIMARY source; Gate 4 (`provenance.primary_source: true`) | owner only |
| `measured` | the program's own experiment (carries an `experiment` block, not a citation) | owner |
| `structural` | a typed sentinel (`open`/`n.a.`/`unmeasured`) | — |

## Distribution by version

### v1 — `atlas.jsonl` (`6d53a4f1`), frozen
- real-value cells: **332**  ·  owner-`confirmed`: **2**  ·  `claimed`: **329**  ·  `measured`: 1
- **v1 standard: agent-`claimed`, owner-spot-checked at the R8 norm (2/332 cells actually confirmed).**
  v1 froze without a full confirm-pass; that spot-check standard is what produced the 8-of-9 `inapprox`
  errata (E1) and the SVP/decision defects — the cost of freezing on unchecked `claimed`.

### v3 — the 752-row expansion (kernel copy + 227 v3-new rows)
- v3-new real-value cells: **420**  ·  owner-`confirmed`: **0**  ·  `claimed`: **420**
- confirm-pass coverage: **272 cells** V2 (agent) + **154 cells** second pass (agent) = **426 agent verdicts**, every cited cell double-touched.
- **v3 standard: agent-DOUBLE-passed at full Check-9 with full-text evidence, owner-UNCONFIRMED.**
  Every cited v3-new cell went draft → V2 confirm → second pass, was swept three ways (F-2,
  decision-membership, prose-vs-value), and is recursively CITE-gated. Value-error 3.8%, zero unresolved
  CITE. This is **more** verification than v1 carried at freeze — but it is agent authority, not owner
  authority. No v3-new cell is `confirmed`.

## Why v3 freezes unconfirmed (and why that is not a regression)

`confirmed` was never a freeze condition: v1 proves it, having frozen at 2/332. The real freeze gates are
CITE-clean (prereg clarification-01) and kill-criterion 1 (value-error < 15%), both met. The prior
"426-cell owner sitting before freeze" ruling rested on an agent-built zero-`claimed` gate mistaken for
freeze semantics; it is corrected (methods-thread instance 12).

## v3.1 — the rolling owner-confirm protocol (condition 2)

Owner-`confirmed` promotion is **not** a freeze blocker. It proceeds as a rolling spot-check after v3
freezes:

1. The owner promotes cells to `confirmed` at whatever depth and schedule they choose — no target, no
   deadline, no gate on the battery.
2. Because promoting a status changes the row's bytes (the additive invariant), promotions land as a
   **v3.1** re-freeze, not edits to frozen v3.0. v3.0 stays byte-identical forever.
3. If a spot-check surfaces a material correction, it rides the **errata protocol** exactly like E1 and
   the H4 batch: v3.0 bytes stay frozen, a dated erratum entry, the v3.1 kernel/row copy carries the fix
   tagged `erratum`.
4. The "first substantially owner-confirmed atlas" is a real goal — but it is a **v4 ambition**, not a
   v3 gate.

## For downstream readers (condition 3)

Any battery output or findings note that reports a v3 statistic carries this one line: **"v3 cells are
agent-double-passed and owner-unconfirmed; see trust-labels.md."** Double-passed is not owner-confirmed,
and no v3 number should be read as if it were.
