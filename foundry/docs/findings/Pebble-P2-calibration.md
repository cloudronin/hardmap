# Sprint 6 "Pebble" — P2: the ξ reach instrument + three-pole calibration

**Verdict: QUALIFIED** (observable = `corr`), with documented limitations that ride into P3 (prereg_v18).

## The instrument

ξ measures how far information about a partial solution propagates through the constraint structure, binned by
constraint-graph distance (BFS over `structural.variable_graph` — the *same* graph the structural tier reads). Two
pre-registered observables (prereg_v17): **forcing** (conditioning marginal-shift) and **corr** (base-ensemble
two-point connected correlation). `reach_score` = mean signal beyond nearest neighbours (d≥2).

## Three-pole calibration (n=16, α=1.4)

| observable | short (decoupled) | medium (2-SAT) | long (2-affine) | ordering | verdict |
|---|---|---|---|---|---|
| **corr** | 0.000 | 0.074 | 0.500 | ✓ non-overlapping | **PASS → qualified** |
| forcing | 0.000 | 0.135 | 0.000 | ✗ (long collapses) | FAIL |

`corr` recovers the sealed ordering, and the values match the pre-registered mechanism: 2-affine transmits at full
strength (corr = 0.5, deterministic), 2-SAT attenuates (info leaks via the consequent → 0.074), decoupled ≈ 0.

## Four honest limitations (none compressed)

**1. This is a two-point separation with a floor anchor, not a three-point ordering.** The short pole (a decoupled
matching) reads reach_score **exactly 0.0 by construction** — a matching has no distance-≥2 pairs at all, so it is a
*structural absence* of the measured quantity, not a measurement of small correlation. The demonstrated capability
is that `corr` distinguishes **0.074 from 0.5**; the short pole only anchors the floor. This is precisely the
two-point capability the medium pole was meant to strengthen. **Fix (prereg_v18):** a genuinely-nonzero short pole
(a bounded-width family at low density) is sealed and **rides alongside P3**, either confirming three genuine points
or revealing a low-end resolution limit while P3's low readings are interpreted.

**2. `forcing` failed for TWO reasons, not one.** (a) The pre-registered *conceptual* blindness (parity-adjacent
media move correlations, not marginals); AND (b) a *sampling artifact* — 2-affine ensembles have very few solutions
(≤4), which drop below the sampled-marginal threshold after conditioning, so the long pole returned no valid forcing
profiles. Either way it did not recover the ordering and `corr` did, so the pre-registered selection stands — but
`forcing` is **not cleanly refuted as an observable, just unqualified here.**

**3. The two-sampler concordance and affine-exact bias checks were VACUOUS.** On these n=16 instances the solution
sets are small (medium: 42, long: 4) and **≤ the sample cap K=80, so both samplers fully enumerate** → identical
sets (Jaccard 1.000) → trivially concordant (Δ≈0) and trivially zero bias. The reach values here are therefore
**exact** (which is *why* the ordering is clean), but sampler agreement under *subsampling* was never tested. **Fix
(prereg_v18):** P3 runs concordance + affine-bias at sizes where |solutions| > K (genuine subsampling), and reports
the per-family sampling regime; concordance is claimed only where it is genuinely exercised.

**4. Scope discipline (sealed v17).** This licenses "the instrument correctly orders the tested media," **never**
"the instrument is calibrated across its range," and — until limitation 1 resolves in P3 — not yet a demonstrated
three-point ordering.

## Carried into P3

Qualified observable **`corr`** is fixed for P3. Riding alongside (prereg_v18): the nonzero short-pole re-calibration
and the genuine-subsampling concordance/affine-bias checks. The reach length λ and fit quality are reported per
family; R‑2 arity diagnostic (ξ vs mean scope size) and R‑3 conditioning-value sensitivity carry as sealed.
