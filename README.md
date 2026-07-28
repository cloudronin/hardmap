# hardmap

**Source of truth is the hashed JSONL.** Every result in this archive lives in a frozen, sha256-pinned JSONL or JSON artifact, and those files are the record. `observatory.db` — the SQL database the tables are compiled into — is a **derived artifact**: it can be deleted and rebuilt from the JSONL at any time, and it is *regenerated, never mutated*. Each of its tables carries the sha256 of the artifact it came from, so the database and its sources can be checked against each other rather than trusted. If the two ever disagree, the JSONL is right. See [`foundry/docs/QUERIES.md`](foundry/docs/QUERIES.md) for five worked joins.

Reproducible evidence for the charge-atlas / proof-space program. This repository
consolidates four research projects into one installable package whose CLI
regenerates **every statistic the write-up cites** — either from
committed, verified artifacts (fast tier, seconds–minutes) or from scratch
(full tier, wall-clock documented per claim). The repo *is* the paper's
evidence: the seal chain, the ledgers, and the numbers, checkable without
trusting the author.

> **`pip install hardmap && hardmap repro --all`** reproduces every cited number in the
> manifest — **28 claims** as of 2026-07-26, growing as results land — and `hardmap verify`
> passes the internal-coherence sweep (**11 checks**).
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
hardmap/         # the thin consolidation CLI (repro / verify / anatomy / atlas) — READS ONLY
eightfold/       # the atlas: frozen atlas.jsonl, schema, validator, Crucible, Factors
foundry/         # the oracle line: lattice / prism / ferry, netting, preregs
                 #   + the observatory and its `foundry` CLI — the WRITE surface, repo-only
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

## Two surfaces: `hardmap` reads, `foundry` writes

Everything above is the **read surface**. `hardmap` reproduces and checks; it never
writes into the archive. That is the whole of what `pip install hardmap` gives you,
and the omission is deliberate.

The **write surface** is a second binary, `foundry`, which advances the observatory:
it reserves rows, compiles the catalog, runs Helm waves, appends to the maptrail. It
is declared only in [`foundry/pyproject.toml`](foundry/pyproject.toml) and its
implementation partly lives in `foundry/dev/`, which the wheel excludes — so it comes
with a checkout and not with the package.

**Why the split is packaging rather than convention.** A declared fraction of every
fan-out batch is *reserved*: those rows are named, hashed, and **never captured**, so
predictions can be sealed before their frames exist. Blindness is physics rather than
a guard someone has to respect. A stranger reproducing the paper who could advance the
frontier by mistyping a subcommand would destroy exactly that. Keeping the verb out of
what ships makes it impossible rather than merely detected.

```bash
foundry audit             # what the CLI can do, and what still lives in dev/
foundry fresh             # every compiled artifact vs the sources it was compiled from
foundry census list       # every batch census, with the schema shape it is actually in
foundry migrate status    # one-time history: applied, pending, or drifted
foundry frontier          # the reserved rows — declared, not captured
foundry db compile        # regenerate observatory.db from the hashed artifacts
```

Two laws are enforced by the dispatch rather than by each verb:

- **Freshness.** Every compiled artifact records the sha256 of what it was compiled
  from; a verb declares what it *consumes* and is refused if any of it has moved.
  `foundry wave` against a stale database will not run, and the error names the
  rebuild. A producer consumes nothing, so no exemption is needed.
- **Event-time provenance.** A verb that writes emits its own maptrail record from
  inside the act. A trail composed afterwards from what someone remembers is not a
  record, so writing and recording are the same step.

One-time passes — a voided preregistration, a re-typing done under a ruling — are
**not** verbs. They are migrations: named, ordered, applied once, checksummed, and
visible through `foundry migrate status`. What you can do to history is ask whether it
ran.

## License

Dual-licensed. Source code under **Apache-2.0** ([`LICENSE`](LICENSE)); research
data and prose (the atlas datasets, results, preregistrations, findings, and
specs) under **CC-BY-4.0** with citation of the write-up as the attribution
condition. See [`NOTICE`](NOTICE) for the exact split and
[`CITATION.cff`](CITATION.cff) to cite.
