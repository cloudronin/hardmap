# Foundry — agent guide

**What this is.** The synthetic census (proof-space line, project 5): a multi-charge atlas over a roster **no
human chose** — generated, stratified constraint languages — with charges assigned by classification theorems
(oracle columns) and the Proof-Census instrument line (measured columns). It answers the canon-vs-computation
question: does the Eightfold canon's structure reproduce free of human selection bias? Spec:
[`docs/specs/foundry-v1-synthetic-census-spec.md`](docs/specs/foundry-v1-synthetic-census-spec.md); the
normative predictions travel in [`docs/findings/F1-canon-or-computation-note.md`](docs/findings/F1-canon-or-computation-note.md).

## THE INVARIANTS (do not break)

1. **One-way dependency — foundry imports eightfold + proofcensus; it never modifies them.** Foundry reuses
   the Eightfold **atlas kernel** (the `ChargeSpec`-parametrized validator + Crucible-hardened harness) and the
   Proof-Census measurement apparatus. **Sequencing note (Rider A):** Eightfold was refactored INTO that kernel
   during Phase K — a one-time Eightfold maintenance commit that PRE-DATES this invariant. From here, eightfold
   is a frozen library dependency; never edit it to suit Foundry. Foundry's vocabulary lives in
   `foundry/charges.py::FOUNDRY_SPEC`, passed to the shared `validate` / `gap_list` / null-sampler.
2. **Rows are constraint languages, not problems.** Each row is a generated language (a Boolean co-clone
   representative or a general-domain language), carried in eightfold's `ProblemEntry`. The roster is the point;
   it is generated (§3.1), never hand-picked.
3. **Generate at the co-clone level (Rider B).** The Boolean roster is built by instantiating one
   Creignou–Kolaitis–Zanuttini plain-basis representative per co-clone off the known co-clone lattice — NOT by
   enumerating relation-sets (2^256 for arity 3 is impossible). Hand-rolled enumeration is a small-arity
   cross-check only.
4. **Oracle vs measured provenance.** Oracle columns: `claimed` where the literature states the class directly,
   `derived` (dichotomy citation + logged `condition_check` with `side==value`) where a dichotomy is applied.
   Measured columns (`average_case`, `landscape`): `measured` with a full `{prereg, manifest, seeds,
   code_commit}` experiment, via the Proof-Census apparatus + its concordance/glitch/budget discipline.
   Unverified oracles (I-phase pending) stay `open`, never guessed.
5. **Pre-register before analysis; kill honestly.** Predictions 1–4 + roster/generations policy + battery +
   tolerances commit to `results/prereg/` before any census reaches the analysis battery. Prediction 3
   (canon-loading reproduction) is **gated on Factors v1**; absent Factors it is reported **untested, never
   approximated**. The NPI calibration (prediction 1) is the first analysis run — a non-empty NPI row halts the
   pipeline (bug, not discovery). Constructed (Tier-2) specimens are flagged and excluded from
   natural-population analyses by default.
6. **Beat your own nulls; exceed the between-generation noise floor.** The Crucible-hardened battery (S1 null,
   R25 netting) runs on the census before any structure claim; the census must beat its own type-respecting
   nulls. G=3 generations; between-generation variance is computed first and is the floor every finding clears.

Run tests from inside this product dir: `python -m pytest tests -q`.
