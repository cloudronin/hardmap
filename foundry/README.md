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

## The `foundry` CLI — the write surface

`foundry` is the **operational** binary: it advances the observatory. It is deliberately absent from the
published distribution's `[project.scripts]`, and part of its implementation lives in `dev/`, which the
wheel excludes — so it arrives with a checkout and not with `pip install hardmap`. The reason is the
frontier: a declared fraction of every batch is reserved and **never captured**, so predictions are
sealed before their frames exist. A verb that could advance the frontier must not be in the hands of
someone reproducing the paper. See the module docstring in [`foundry/cli.py`](foundry/cli.py).

```bash
foundry audit                        # what is lifted into the library, what still lives in dev/
foundry fresh                        # compiled artifacts vs the sources they were compiled from
foundry census list                  # every batch census, with the schema shape it is actually in
foundry census declare --declaration batches/11.json
foundry census verify --batch 10     # re-derive and diff; never rewrites
foundry db compile                   # regenerate observatory.db from the hashed artifacts
foundry next                         # compile NEXT.md from the maptrail
foundry migrate status               # one-time history: applied / pending / drifted
foundry frontier                     # reserved rows — declared, not captured
foundry trail --event version        # maptrail records
foundry open                         # open items, replayed from the trail
```

Two laws are enforced by the dispatch, not by each verb. **Freshness:** a verb declares what it
`consumes` and is refused against a compiled artifact whose sources have moved — `foundry wave` will not
run on a stale database, and the refusal names the rebuild. **Event-time emission:** a verb that writes
emits its own maptrail record from inside the act, because a trail composed afterwards from memory is
not a record.

One-time passes are **not** verbs. A voided preregistration or a re-typing done under a ruling is
history: named, ordered, applied once, checksummed, and inspectable through `foundry migrate status`.
Re-running a void is a second void of something already void, so the machinery does not offer it.

Six recurring operations still hold their logic in `dev/` and are reached by delegation. Freshness
reaches them at the boundary; event-time emission cannot, which is what each lift buys. `foundry audit`
prints the current count and `tests/test_cli.py` fails if it grows.

See [`AGENTS.md`](AGENTS.md) for the invariants, [`docs/specs/`](docs/specs/) for the spec, and
[`docs/findings/F1-canon-or-computation-note.md`](docs/findings/F1-canon-or-computation-note.md) for the
normative predictions.
