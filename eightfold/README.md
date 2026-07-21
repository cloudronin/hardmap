# Eightfold v1 — Charge Atlas

The first quantitative **charge atlas** of computational problems: each row is a natural problem under a fixed
encoding; each column is one of eight literature-sourced hardness "charges." Every cell carries a value and a
citation, or an explicit `open` / `unmeasured` / `n.a.` / `uncited-folklore` flag. Structure detection over
the atlas looks for **multiplets** (recurring charge signatures), **forbidden regions** (combinations no known
problem occupies), and **gaps** (combinations the structure predicts should be occupied but aren't).

Third project in the proof-space line (Desert Map → Proof Census → Eightfold); "Move One" of the Gell-Mann
sequence — Mendeleev card-sorting done honestly, no claimed periodic table. Spec:
[`docs/specs`](docs/specs/eightfold-v1-charge-atlas-spec.md) (with Build addenda R1–R8); investigations:
[`docs/findings`](docs/findings/).

## The eight charges

decision · counting · approximation · parameterized · parallelization · proof-size · average-case ·
landscape/freezing. Value vocabularies and the QC gates are in
[`SCHEMA.md`](eightfold/results/atlas/SCHEMA.md).

## Install (local, CPU, $0 compute)

```bash
python -m venv .venv && . .venv/bin/activate
pip install -e ".[analysis,dev]"      # core is stdlib-only; [analysis] adds pandas/prince/scipy/sklearn
```

## Validate & summarize the atlas

```bash
python -m eightfold.atlas validate    # QC gates + corpus invariants; must show zero uncited-folklore
python -m eightfold.atlas summary     # per-charge / per-family coverage (applicable vs open/n.a.)
```

## Structure preview (harness sanity-check on the pilot)

```bash
python -m eightfold.structure --pilot # Cramér's V, dual-missingness MCA, clustering, marginal occupancy
```

## Test

```bash
# from inside this product dir (monorepo namespace convention)
python -m pytest tests -q
```

## Status

A1 pilot (20 problems, fully cited) — the first kill-gate (population viability) before the full ~120-problem
atlas. CPU-only, $0 compute. See [AGENTS.md](AGENTS.md) for the invariants (unknown ≠ zero; every value cited
or flagged; canonical task per charge; occupancy over marginals; prereg before analysis).
