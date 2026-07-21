# Desert Map — Proof-Space Cartography v1

Empirical map of the loss landscape of **continuous (gradient-descent) proof search** for Resolution
refutations of small unsatisfiable random 3-SAT instances. Tests **H1**: as instances get harder, the
relaxed proof-search objective *shatters* (independent GD runs converge to distant optima; success
rate collapses at a sharp boundary rather than degrading smoothly).

Self-contained monorepo sibling product — **unrelated to PhysMAP**. v1 produces plots and a verdict on
H1; it proves no theorem. Spec: [`docs/specs/proof-space-mapping-v1-spec.md`](docs/specs/proof-space-mapping-v1-spec.md).
Investigation findings (I1–I6): [`docs/findings/`](docs/findings/).

## Install (local dev, CPU)

```bash
python -m venv .venv && . .venv/bin/activate
pip install -e ".[compute,hf,viz,dev]"
```

The **oracle path** (`instance` / `verify` / `fixtures`) is deliberately torch-free — installable and
runnable with core deps only. torch (the relaxation engine) lives behind the `[compute]` extra.

## Test

```bash
# from inside this product dir (monorepo namespace convention)
python -m pytest tests -q
```

## Hardness direction (read this first)

Resolution *refutation* hardness peaks just above the sat threshold and **falls as α rises** — the
opposite of the solution-space convention. **Hard cells = α∈{4.5,5.0}**; **easy cells = α∈{8,10}**.
All shattering signatures are predicted as α *decreases toward* ~4.267. See [AGENTS.md](AGENTS.md).

## Compute (HF Jobs)

Sweeps run on Hugging Face Jobs; local/CI is CPU-only for the M1/M2 gates. Nothing ships to a paid
flavor before the local gates pass (spec §8), and no experiment runs before the pre-registration
receipts in `desertmap/results/prereg/` are committed.

```bash
# dry-run prints a redacted argv; no token or job needed
python -m desertmap.hf.launch --stage smoke --dry-run
```

Drop the HF token at `/tmp/HF_KEY.txt` (or export `HF_TOKEN`) — never on the command line.

## Status — v1 killed at M2 (negative result)

Direct relaxation of the proof object cannot recover even a 5-step planted refutation from random init
(E0 = 0% across three operator redesigns), while a constructive resolution search recovers every instance
(100%) and a discrete local search on the same parameterization also fails (0%). The barrier is the direct
proof-object **parameterization**, not the instances or gradient descent. Kill triggered at the local M2
gate (spec §6.1); no paid compute used. Full write-up:
[`docs/findings/NEGATIVE-RESULT.md`](docs/findings/NEGATIVE-RESULT.md); calibration evidence in
[`docs/findings/M2-e0-calibration.md`](docs/findings/M2-e0-calibration.md).

**Ships:** M1 (generator + verifier + fixtures, gate passed), the M2 operator (represents proofs exactly),
and the discrete-search calibration harness. M3 metrics, the HF Jobs sweep, and E1–E5 were gated on M2 and
are not built. See [CHANGELOG.md](CHANGELOG.md).
