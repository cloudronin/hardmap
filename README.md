# hardmap

Reproducible evidence for the charge-atlas / proof-space program. This repository
consolidates four research projects into one installable package whose CLI
regenerates **every statistic the write-up cites** — either from
committed, verified artifacts (fast tier, seconds–minutes) or from scratch
(full tier, wall-clock documented per claim). The repo *is* the paper's
evidence: the seal chain, the ledgers, and the numbers, checkable without
trusting the author.

> **`pip install hardmap && hardmap repro --all`** reproduces every cited number in the
> manifest — **28 claims** as of 2026-07-26, growing as results land — and `hardmap verify`
> passes the internal-coherence sweep (**10 checks**).
> The sealed verification pass is complete ([H4-verification.md](docs/findings/H4-verification.md)).

## Provenance & the seal chain

The program's epistemic argument rests on *sealed-before-measured*: each
preregistration was sealed by the act of committing it, so the seal **is** the
commit that introduced it. This repo was extracted, history-preserving, from a
private predecessor monorepo with `git filter-repo`, which rewrites commit
hashes. Every sealed prereg therefore resolves end to end —
*sealed at X (public: Y)* — via:

- [`docs/hash-map.txt`](docs/hash-map.txt) — the full old→new commit map.
- [`docs/seal-chain.md`](docs/seal-chain.md) — every sealed prereg, resolved.

The frozen charge atlas (`eightfold/eightfold/results/atlas/atlas.jsonl`) is
preserved **byte-identical** through the migration (enforced by a round-trip
test); its `code_commit` provenance field resolves through the hash-map like any
other seal.

## Layout

```
hardmap/         # the thin consolidation CLI (repro / verify / atlas)
eightfold/       # the atlas: frozen atlas.jsonl, schema, validator, Crucible, Factors
foundry/         # the oracle line: lattice / prism / ferry, netting, preregs
proof-census/    # samplers, verifier, the C1–C3 census harness
desert-map/      # banked/killed; retained for fixtures + the verifier census reuses
docs/            # hash-map, seal-chain, and (aggregated) findings / prereg / specs
repro/           # manifest.yaml: claim-id -> entrypoint -> expected value -> tolerance -> tier  (H3)
```

Internal dependencies: `foundry` imports `eightfold`; `proof-census` imports
`desertmap`. Publishing all four in one distribution keeps those edges resolved.

## Install

```bash
pip install -e .          # fast tier: numpy<2, scipy, pyyaml, py>=3.10
pip install -e ".[full]"  # + torch, for full-tier resampling (desert-map / census C3)
```

## Reproducing

```bash
hardmap repro --all       # recompute every fast-tier number, diff vs expected within tolerance
hardmap repro --claim canon.gradient.v   # a single claim
hardmap repro --full      # full tier: regenerate from scratch where available (wall-clock per claim)
hardmap repro --list      # list every claim id
hardmap verify            # coherence sweep: estimates in CIs, V in [0,1], netted <= raw, no plurality
hardmap atlas             # dump the frozen atlas (jsonl byte-identical, or --format csv)
```

`repro --all` recomputes the eightfold statistics from the frozen atlas and the
census aggregate from the committed proof checkpoint, and reads the verified
oracle matrices; it exits nonzero on any mismatch. The per-number map (entrypoint,
expected value, tolerance, tier) is [`repro/manifest.yaml`](repro/manifest.yaml).

## License

Dual-licensed. Source code under **Apache-2.0** ([`LICENSE`](LICENSE)); research
data and prose (the atlas datasets, results, preregistrations, findings, and
specs) under **CC-BY-4.0** with citation of the write-up as the attribution
condition. See [`NOTICE`](NOTICE) for the exact split and
[`CITATION.cff`](CITATION.cff) to cite.
