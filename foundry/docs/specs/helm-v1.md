# Helm v1 — the wave engine, as built

Implements `helm-v1-wave-engine-spec.md`. This file records what exists, what differs from the spec, and
the one reading that had to be resolved before anything could be built.

---

## Rulings of 2026-07-27, and where each one lives in the code

| ruling | pinned as | enforced in |
|---|---|---|
| §5 reads under §0.1 — **ratified**, §5's text amended | `reservation.py` docstring | `maptrail` `erratum:helm-spec-section-5` |
| the anomaly frontier null — **stratified exchangeability** | `sweep.EXTREMAL_NULL`, `stratified-exchangeability/v1` | `screens.MIN_STRATUM_CELLS`, `frontier_strata` |
| `structurally_flat` forecloses the false-candidate class | `extract.structure`, descriptor@v2 | `sweepable_catalog` view + backstop screen rule |
| MCSP's ramp amended, direction pinned at pilot | `mcsp_ramp_pilot.py` | `maptrail` `erratum:string-family-ramp` |

### The stratified null, in full (Helm §3.1's precedent discharged)

An anomaly bet is adjudicated **within the candidate's own stratum**: a permutation against the pooled
distribution of frontier cells sharing its **(family × region-kind × flavour)**, with **r-band** as a
matching covariate where supply allows. A stratum below **20 cells** returns `INSUFFICIENT` rather than a
p-value.

The floor is derived, not chosen: a one-sided permutation test over *m* cells attains no p-value below
1/(m+1), so 19 is where 0.05 becomes attainable at all and 20 is the first size with anything to spare.
The three stratification axes are each a paid-for lesson — family per Terroir's verdict, region-kind per
Q5's contrast instability, flavour per the fingerprint structure — and r-conditioning is the sixth-species
vaccine. **Exchangeability across unlike strata is the assumption this program has disproven three
times**; within-stratum is the version the evidence permits.

Versioned like any descriptor, so a claim quoting it quotes `stratified-exchangeability/v1` forever.

### A wave is not re-run when the rules change

Wave 1's trail is committed and stands as what the engine saw at the time. The rulings arrived after it,
so the amended screens produced **wave 2** — a new sweep under `sweep/v2` — rather than a rewrite. The
wave id is computed as the next unused one rather than typed, so this cannot be got wrong by editing a
constant. Kill 3 is about exactly this.

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

## Deviations from the spec, all deliberate

**Anomaly candidates are held on stratum supply, not on a missing null.** At wave 1 their null typed the
*disclosed* extremal's position rather than a frontier prediction, and all 22 were held for want of a
model. The ruling pinned one; they now carry `stratified-exchangeability/v1` and are held because the
2-row frontier supplies at most 1 cell to any stratum against a floor of 20. The gap is recorded per
candidate, so the HOLD query revives them as the frontier's strata fill.

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
