# Garden vocabulary rulings — decision brief (owner)

> **RULED 2026-07-24.** Both decisions are now settled; this brief is the record, not a pending ask.
> - **Decision A — QMA rung: ruled IN.** Two rungs (`QMA-complete`, `QMA1-complete`) + the membership value
>   `in-QMA`, placed above NPC / below PSPACE-complete / incomparable to PH. Filed as
>   `prereg_v9-clarification-04.json`; V3_SPEC extended (decision 7→10 values, kernel unchanged); three rows
>   admitted to v3.1 (`quarry-v3.1-quantum.jsonl`, validated). Frozen bytes untouched (6d53a4f1, e62f3c28).
> - **Decision B — communication-complexity axis: ruled SCOPED OUT.** No ninth column opens reactively.
>   `equality-communication` and the REJECT cluster are out-of-vocabulary-by-scope (a model boundary, not a
>   vocabulary gap). The three-way axis split (fine-grained = candidate 9th *column*; communication = candidate
>   *companion table*) and the carry-forward scope finding are banked in `A4-charge-atlas-move-one.md`.

The Complexity Garden screen surfaced 4 admissible-but-unexpressible problems. They split into **two
decisions of different size**, exactly as flagged: a rung *inside* an existing charge (a coding change),
and a candidate *ninth column* (a schema change). Ruling them together would conflate the two.

---

## Decision A — a QMA rung in the `decision` charge (coding change, `superpoly-APX` class)

Three of the four are the same gap: the `decision` vocabulary has no **quantum-verifiable** rung.

| problem | established value | citation |
|---|---|---|
| `k-local-hamiltonian` | **QMA-complete** (the canonical one) | KSV02 (k=5) / Kempe–Regev 2003 (k=3) / Kempe–Kitaev–Regev SICOMP 35 (k=2) |
| `quantum-k-sat` | **QMA₁-complete** (k≥3); quantum-2-SAT ∈ P | Bravyi 2006 (agent-supplied; Garden cited only a lecture) |
| `group-non-membership` | **in QMA** — *membership, not completeness* | Watrous FOCS 2000 |

**This is `superpoly-APX` again, mechanically.** A rung added to one charge's vocabulary. If ruled in, it
rides `V3_SPEC` (the Strata-scoped instrument), is dual-coded against the kernel, and **touches no frozen
bytes** — no v1/v2/v3 row is quantum, so the rung is purely additive, exactly as `superpoly-APX` was. The
things that need your ruling are the modeling choices a rung always carries:

1. **Ordinal placement.** QMA sits NP ⊆ QMA ⊆ PP ⊆ PSPACE, and is not known to be in PH. On the decision
   column's hardness ordinal it lands *above* NPC and *below* PSPACE-complete, incomparable to the PH
   rungs — a placement call like `superpoly-APX`'s between `poly-APX` and `inapprox`.
2. **One rung or two.** QMA and QMA₁ (perfect completeness) are distinct classes; `quantum-k-sat` is
   QMA₁-complete, `k-local-hamiltonian` is QMA-complete. One quantum rung that both map to, or two?
3. **Membership-only admission.** `group-non-membership` is *in QMA*, not QMA-complete — the quantum
   analogue of an `NPI-candidate` (a membership fact, not a completeness fact). Even with the rung, whether
   a membership-only quantum row is *admissible* is a separate call, the same shape as the NPI-candidate
   admission bar.

**My read (not a ruling):** rule it exactly as `superpoly-APX` — one `QMA-complete` rung plus a
`QMA₁-complete` rung if you want the perfect-completeness distinction on the record, `V3_SPEC`-scoped,
ordinal-placed above NPC and below PSPACE-complete, filed as a fourth prereg clarification. It admits
`k-local-hamiltonian` and `quantum-k-sat` cleanly; `group-non-membership` waits on the membership-admission
call.

---

## Decision B — a communication-complexity axis (schema change; collides with the parked charge-9)

The fourth is categorically bigger:

| problem | established value | citation |
|---|---|---|
| `equality-communication` | deterministic **CC = Θ(n)** (fooling-set / rank bound) | Yao STOC 1979; Kushilevitz–Nisan 1997 |

`EQ(x,y)` as a *computation* is trivially in P; its only non-trivial complexity lives in the
**communication** model — an axis the 8 charges (all Turing-machine resources) do not have. This is **not a
rung, it is a candidate 9th charge**, and that changes everything:

- **It breaks byte-identity.** A new charge adds a cell to *every* row, so it is **not additive** in the
  Strata/errata sense — it changes v1/v2/v3 bytes and cannot ride `V3_SPEC`. It requires a genuinely new
  atlas generation, with the new cell `n.a.`/`open` on all existing rows. Gate 7 (all-charges-present)
  becomes 9 cells; the factors instrument, MCA, and entailment layer all gain a dimension.
- **It is not one problem — it is a recurring pattern the Garden made visible.** The screen's 12 REJECTs
  were *almost all* problems whose only established results live outside the 8 charges: circuit-size,
  monotone gaps, AC⁰, communication (Convolution, Boolean Matrix Multiply, Boolean Sorting, Majority,
  Parity, Threshold, …). The atlas's charges are all "resource on a Turing machine"; a whole family of
  results sits in *other models*. `equality-communication` is the cleanest single instance of a real gap.
- **It collides with the parked charge-9.** A ninth charge is **already queued**: *fine-grained complexity*
  (SETH / 3SUM / APSP), recorded in the v1 spec (§charge-9), `A4-charge-atlas-move-one.md`,
  `Strata-coverage.md`, and `I1-I4-investigation.md`. So the 9th slot has a prior claimant. The real
  question is not "admit `equality-communication`" but **which axis (if any) opens the 9th column** —
  fine-grained complexity, communication complexity, both (charge-9 and -10), or neither, holding the
  atlas to Turing-machine resources by scope.

**My read (not a ruling):** Decision B is a scope decision about the atlas itself, not a candidate
admission. It should not be forced by one EQ row. The cleanest resolution is to log `equality-communication`
(and the circuit/communication REJECT cluster) as **out-of-vocabulary-by-scope pending the charge-9
ruling**, and take the axis question up as its own thread against both claimants — not to open a 9th charge
reactively.

---

## What each ruling costs

| | Decision A (QMA rung) | Decision B (comm-complexity axis) |
|---|---|---|
| class | coding change | schema change |
| precedent | `superpoly-APX` | the parked charge-9 (fine-grained) |
| frozen bytes | untouched (V3_SPEC-scoped) | **breaks** v1/v2/v3 byte-identity |
| battery | indicator-matrix widens (1 charge) | new dimension across all estimators |
| admits now | `k-local-hamiltonian`, `quantum-k-sat` | none until the axis + scope are ruled |
| filed as | prereg clarification-04 | a new charge-atlas thread |

Both are yours. A is small and I'd rule it like `superpoly-APX`; B is a scope question that deserves its
own thread and shouldn't be triggered by a single row.
