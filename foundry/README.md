# Foundry — synthetic census

The fifth project in the proof-space line (Desert Map → Proof Census → Eightfold → Crucible → **Foundry**).
Foundry builds a multi-charge atlas over a roster **no human chose** — generated, stratified constraint
languages — with charges assigned by classification theorems (oracle columns) and the measured Proof-Census
instrument line, then tests whether the **Eightfold canon's structure reproduces** free of human selection
bias. It answers the canon-vs-computation question.

**Status:** N0 scaffold. The atlas kernel (Eightfold Phase K) + `FOUNDRY_SPEC` + a hand-checked toy stratum
exist and the shared validator/harness reuse is proven (`tests/test_kernel_reuse.py`). The generated Boolean
census (N1), the dichotomy oracles, and the measured instrument columns (N4) are **later-phase** work.

## Reuse (never rebuilt, never modified)

- **Eightfold atlas kernel** — the `ChargeSpec`-parametrized validator (`eightfold.atlas.validate(row, spec)`)
  and Crucible-hardened harness (`eightfold.crucible` null model, `eightfold.structure` gap-list / R25).
  Foundry supplies `foundry.charges.FOUNDRY_SPEC`; one code path, two vocabularies.
- **Proof-Census apparatus** — the verifier-gated sampler pair + glitch/concordance/budget discipline, for the
  measured instrument columns (N4).

## Install & run (editable, one venv — the proof-census→desert-map pattern)

```bash
pip install -e ./eightfold -e ./proof-census -e ./foundry[analysis,dev]
foundry --validate-toy         # validate the toy stratum through the shared kernel
python -m pytest tests -q      # run from inside foundry/
```

See [`AGENTS.md`](AGENTS.md) for the invariants, [`docs/specs/`](docs/specs/) for the spec, and
[`docs/findings/F1-canon-or-computation-note.md`](docs/findings/F1-canon-or-computation-note.md) for the
normative predictions.
