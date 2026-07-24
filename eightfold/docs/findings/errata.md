# Errata — defects found in frozen artifacts after freeze

**Protocol.** Frozen bytes stay frozen forever. A defect found after the freeze is recorded here
(artifact, cell, wrong value, corrected value, reason, date), the corrected value is carried by the
*next* version, and the version-to-version delta decomposition marks the cell **`erratum`, not
`drift`** — so a battery comparison never books a vocabulary fix as a population shift. Machine-readable
form: [`results/atlas/errata-v1.json`](../../eightfold/results/atlas/errata-v1.json).

---

## E1 — 2026-07-24 — the F-2 `inapprox` sweep over frozen v1

**Artifact:** `atlas.jsonl` (v1 kernel, sha256 `6d53a4f1…`, 118 rows) — **bytes unchanged.**

**How it surfaced.** The Atlas v3 V2 confirm-pass (2026-07-23) demoted `chromatic-number`'s
`inapprox` to `poly-APX` in v3. The identical cell content sits in frozen v1 on `graph-3-coloring`.
Owner ruling: apply the F-2 test to **every** frozen `inapprox` cell, since four independent v3
drafters had made the same mistake and the v1 drafting process was not structurally different.
Independently adjudicated 2026-07-24.

**The rule (SCHEMA.md F-2 pin).** `inapprox` = **no poly-time f(n)-approximation for *any* polynomial
f** (unconditional unless P=NP). A problem with an n^ε-approx, a polylog gap, or conditional-only
hardness is **not** `inapprox`.

**Result: 9 cells swept — 1 HOLDS, 5 DEMOTE, 3 CITE-INSUFFICIENT. 8 of 9 were defective.**

| cell | was | corrected | why |
|---|---|---|---|
| `clique` | `inapprox` | **`poly-APX`** | one vertex = n-approx; Feige O(n(loglog n)²/(log n)³) |
| `independent-set` | `inapprox` | **`poly-APX`** | the textbook **poly-APX-complete** problem |
| `graph-3-coloring` | `inapprox` | **`poly-APX`** | n colors = n-approx; Halldórsson (IPL 1993) |
| `maximum-common-subgraph` | `inapprox` | **`poly-APX`** | O(√n) (Halldórsson); only *as hard as* MAX-IS |
| `xor-sat` | `inapprox` | **`APX-complete`** | random assignment = 2-approx; Håstad's (½+ε) proves the *constant* is tight |
| `shortest-vector-svp` | `inapprox` | **vocabulary gap** | citation gives only a *constant* factor, under *randomized* reductions |
| `closest-vector-cvp` | `inapprox` | **vocabulary gap** | DKRS hardness is n^{o(1)} — sub-polynomial, the excluded case |
| `quadratic-assignment` | `inapprox` | `inapprox` (**citation replaced**) | Sahni–Gonzalez proves only APX-hardness; the pin-level result is **Queyranne (1986)** |
| `tsp` | `inapprox` | **HOLDS** | the free gadget parameter rules out every poly-computable α(n) |

**The single root cause:** treating an n^{1−ε} or 2^{log^{1−ε}n} **lower** bound as if it established
the absence of any polynomial-factor **upper** bound. Those are independent claims; the pin requires
the upper-bound side, and nobody checked it.

### Three findings that outlive the corrections

1. **SVP and CVP expose a vocabulary gap, not just a citation defect.** Their best poly-time factors
   are *superpolynomial* (2^{O(n loglog n/log n)}; Babai's 2^{n/2} for CVP), so they cannot be demoted
   to `poly-APX` — but `inapprox` as pinned is unsupportable too. **No v1 rung is correct for either.**
   Needs an owner ruling: a v2 rung (superpolynomial-but-not-inapprox), or explicit `open` + note.
2. **`graph-3-coloring` carries an object mismatch**: the `problem_id` says 3-COLORING, the
   `canonical_task` says CHROMATIC NUMBER. Under the 3-colorable promise the best algorithm uses
   ~O(n^0.198) colors — an n^ε-approximation, which the pin names verbatim as disqualifying. Owner must
   rule which object the row is.
3. **`tsp` and `quadratic-assignment` cite the same paper and land differently**, purely on
   `canonical_task` wording. Sahni–Gonzalez's *literal* Thm 3.1 is stated for constant ε; TSP survives
   on the universally accepted reading of the free gadget parameter (Vazirani Thm 3.6; Johnson &
   McGeoch Thm A). **Under a strictly literal citation standard TSP would also be CITE-INSUFFICIENT** —
   an owner call about how literal Check-9 is.

**Disposition.** v1 bytes untouched. `atlas_v3.jsonl` carries the corrected values (applied by the
freeze finalizer from `errata-v1.json`, which tags each corrected cell `erratum_v1`). The v2→v3 delta
must exclude these cells from drift accounting.
