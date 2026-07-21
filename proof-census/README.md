# Proof Census v1

Empirical population map of the **refutation set** of unsat random 3-SAT. Instead of *searching* the proof
landscape (Desert Map's question — answered "no"), Census **samples** many valid Resolution refutations per
instance with two structurally-different randomized samplers and computes population statistics on the
verifier-passing proofs.

- **S1** — randomized constructive saturation (DAG-like), the sampler that scored 100% in Desert Map's calibration.
- **S2** — randomized DPLL → tree-resolution (tree-like), self-implemented, no external proof tooling.

**Hypotheses:** H1 (the refutation set is plural), H2 (population stats shift as α→threshold: length↑,
overlap-shape shifts, a backbone emerges), H3 (findings replicate as *trends* across the α sweep in both
samplers). All claims are **sampler-relative**. Spec: [`docs/specs`](docs/specs/proof-census-v1-spec.md);
investigation: [`docs/findings`](docs/findings/).

## Install (local, CPU)

Depends on the sibling **`desert-map`** product for the M1 verifier/fixtures. Install both editable in one venv:

```bash
python -m venv .venv && . .venv/bin/activate
pip install -e ../desert-map -e ".[viz,dev]"
```

## Test

```bash
# from inside this product dir (monorepo namespace convention)
python -m pytest tests -q
```

## Smoke

```bash
python -m proofcensus.cli sample --n 20 --alpha 4.5 --sampler s1 --k 20
```

## Status

C1 in progress (the two verifier-gated samplers). CPU-only, $20 ceiling. See [AGENTS.md](AGENTS.md) for the
invariants (verifier-gate everything; sampler-relative claims; H3 = trends not levels; S2 regression is
soundness-critical).
