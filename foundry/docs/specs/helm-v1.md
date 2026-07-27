# Helm v1 — the wave engine, as built

Implements `helm-v1-wave-engine-spec.md`. This file records what exists, what differs from the spec, and
the one reading that had to be resolved before anything could be built.

---

## The resolved reading (§5 vs §0.1) — reserved rows are NOT CAPTURED

The spec says two things that differ in strength:

- **§5:** reserved rows are "captured last in the batch" and withheld from disclosed computation until
  predictions are hashed.
- **§0.1 (Constitution, marked binding):** "predictions hashed **before their frames exist**".

Under §5 the frames exist and blindness rests on a guard. Under §0.1 the frames do not exist and blindness
is physics. **The implementation takes §0.1** — a reserved row is declared and left uncaptured, and §5's
"captured last" is honoured maximally: *last* means after the wave's predictions are sealed, not merely
last within a run.

The asymmetry decides it independently of which clause governs. Declare-then-capture-later can always be
relaxed into capture-now if the owner rules the other way. Capture-now can never be taken back: frozen
bytes are forever and ground once seen cannot be unseen. **The recoverable reading wins.**

Consequence worth stating plainly: `foundry/dev/observatory_batch3.py` contains **no generator** for
either reserved row. A guard that forbids capturing reserved ground still needs the machinery to be
capable of it and trusted not to. A batch that never learned how to build the row cannot burn it.

## What exists

| component | file | does |
|---|---|---|
| reservation | `foundry/catalog/reservation.py` | declares the 25%, append-only ledger, `assert_absent` |
| maptrail | `foundry/catalog/maptrail.py` | §7.1 territory provenance, emitted at event time |
| sweep | `foundry/helm/sweep.py` | §2 enumeration; Spearman, Cramér's V, bank import |
| screens | `foundry/helm/screens.py` | §3 four screens, floors pinned in-file |
| slate | `foundry/helm/slate.py` | §4 information-per-seal ranking |
| wave trail | `foundry/helm/trail.py` | §7 logbook + Kill 3 check |
| cycle | `foundry/dev/helm_wave.py` | runs sweep → screens → slate, stops |
| tables | `foundry/catalog/loader.py` | `frontier` `maptrail` `waves` `wave_events` `candidates`, views `hold_queue` `family_ledger` |

## Enforcement, and where it lives

The reservation is checked in **three** places, none of which is the batch script's good intentions:

1. `build_catalog_v1.py` — asserts before the descriptors are written.
2. `loader.py` — asserts against what was actually inserted into `frames` and `catalog`, because the
   loader is the last gate before published ground exists.
3. `tests/test_frontier_reservation.py` — including `test_the_guard_can_actually_fail`, which feeds
   `assert_absent` a reserved row and requires it to raise. Without that test the others would pass just
   as happily against a function whose body was `pass`.

## Two deviations from the spec, both deliberate

**Anomaly candidates cannot reach a slate at v1.** §2 lists them as a candidate class, and the sweep
enumerates all 22. But their null types the *disclosed* extremal's position among published cells, not a
frontier prediction, and typing the reproduction bet needs an exchangeability model over frontier cells
that v1 has not pinned. They are HELD, not rejected, under the precedent §3.1 sets for change-points.
Pinning that null is a ruling, not an implementation detail.

**A `netting` rule rejects five definitionally-coupled descriptor pairs.** §3.2 names netting compliance
without enumerating what is coupled. The couplings are read off `foundry/catalog/extract.py` and listed in
`screens.DEFINITIONAL_COUPLING` with the reason each holds. Coupled candidates are still **enumerated**
and counted in the denominator; only their disposition changes.

## Not built at v1

- `hash`, `capture`, `score`, `prior_update` trail events — the emitters exist and are typed in
  `trail.EVENTS`, but no wave has reached those stages, and emitting them would require a ruling first.
- Prereg minting from a ruled candidate (§4). Nothing has been ruled.
- Verdict handling and prior update (§6). Nothing has been scored.

These are not missing pieces so much as stages no wave has reached. Building them ahead of a ruling would
be building against an imagined slate.

## Box, actual

Sweep + screens + slate + trail emitters + loader tables + reservation + maptrail: within the spec's
5–7 h estimate. Per-wave marginal cost measured at **seconds** of compute, well under the "~minutes"
the spec budgeted — the sweep is 344 candidates over a 236-cell catalog, and the expensive statistics
(permutation nulls) are deferred until a candidate survives the screens, which none did.
