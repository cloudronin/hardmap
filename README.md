# hardmap

**Hardmap starts where most complexity references stop.** The famous catalogs of computational
complexity are star charts: thousands of problems with well-documented names, positions, and
classifications, compiled from trustworthy sources. Invaluable — and almost entirely static. A
sky full of named lights, with nearly nothing recorded about how any of them *behave*.

Hardmap is an observatory pointed at that sky. First, the **atlas**: the star chart rebuilt with
receipts — every classification carries its source, checked rather than trusted. When we ran that
check over 272 drafted cells, **95.2% of the values stood, but 17.3% cited a work that does not
establish the value it was cited for**
([V2 confirm-pass report](eightfold/docs/findings/quarry-v3-V2-confirm-report.md)). The sky is
mostly charted correctly; the sourcing is where it frays. Then, the **films**: for every problem
the instruments can reach, we capture how its solution space actually behaves as difficulty ramps
up — solution clouds contracting, coherence rising, structure freezing in — and distill each film
into queryable tags in a versioned catalog. Not twinkling lights with fancy names anymore;
measured objects with trajectories.

And the whole thing opens to you. The archive ships with its own telescope: a sixty-second path
from install to querying the data, every reading paired with the calibration frames that justify
believing it, and a ledger of every confound and false lead our own instruments produced along the
way. So you can query our sky, ask questions we never thought to ask, or point the instrument
somewhere new — **without ever mistaking Venus for a new star.**

Pick your door.

---

## Query the archive — 60 seconds

```bash
pip install hardmap
hardmap db build
hardmap query rejected-candidates
```

```
Q7 — the rejected-candidate ledger

screen_disposition  screen_rule               n
------------------  ------------------------  ----
HELD                power-fail                1262
REJECTED            null-missing              328
REJECTED            netting                   165
HELD                null-missing              161
REJECTED            definitional-consumption  7
REJECTED            size-marginal             7
SLATED                                        7
HELD                path-gated                3
HELD                needs-r-conditioning      2
```

That is the garden of forking paths, published as a map of the garden. 1,942 questions
enumerated, 7 slated, and a reason on record for every one of the rest — so a
multiple-comparisons correction here is computed from an enumeration you can audit rather
than a number you have to trust.

The archive holds **346 problem rows** with charges from classification theorems, **2,032
frames** of measured region geometry along difficulty ramps, **446 catalog cells** of
descriptors extracted under a versioned rule, and the append-only trails recording how all of
it got there.

```bash
hardmap query --list          # all eight worked queries
hardmap query --sql "SELECT COUNT(*) FROM catalog WHERE excess_ref IS NOT NULL"
```

| query | |
|---|---|
| `reach-and-capture` | what the observatory can reach, and how each row is captured |
| `descriptors-by-charge` | geometry joined to complexity class (charges are fixed labels, never dials) |
| `disclosed-prior-cells` | which cells are disclosed-prior material |
| `coherence-comovement` | the coherence/excess co-movement per row |
| `provenance-check` | every catalog cell traced to frames that exist — an empty result is the pass |
| `frontier` | rows reserved as out-of-sample ground, declared and uncaptured |
| `rejected-candidates` | the ledger above |
| `territory-biography` | what changed in the archive, in the domain's own vocabulary |

The SQL and what each join is *for*: [`QUERIES.md`](foundry/foundry/queries/QUERIES.md).
Prefer a GUI? `hardmap db build` writes a plain SQLite file — open it in any browser.
Or take the prebuilt one from
[Releases](https://github.com/cloudronin/hardmap/releases) and skip the install.

## Reproduce the paper — 5 minutes

```bash
pip install hardmap
hardmap repro --all
hardmap verify
```

`repro --all` reproduces every cited number in the manifest — **28 claims** as of
2026-07-26, growing as results land — recomputing the eightfold statistics from the frozen
atlas and the census aggregate from the committed proof checkpoint. It exits nonzero on any
mismatch. `verify` runs the internal-coherence sweep (**11 checks**). The sealed
verification pass is complete ([H4-verification.md](docs/findings/H4-verification.md)).

```bash
hardmap repro --claim canon.gradient.v   # a single claim
hardmap repro --full                     # regenerate from scratch where available
hardmap repro --list                     # every claim id
hardmap anatomy --passports              # the Structure Atlas column passports
hardmap atlas                            # the frozen charge atlas, byte-identical
```

The per-number map — entrypoint, expected value, tolerance, tier — is
[`repro/manifest.yaml`](repro/manifest.yaml).

## Operate the observatory — checkout required

Running the wave engine, capturing new rows, advancing the catalog: that is the `foundry`
binary, and it deliberately does **not** come with `pip install hardmap`.

A declared fraction of every batch is *reserved* — named, hashed, and **never captured** —
so predictions are sealed before their frames exist. Blindness is physics here rather than a
guard someone has to respect, and a stranger who could advance the frontier by mistyping a
subcommand would destroy it. So the write verbs ship with a checkout and not with the
package.

```bash
git clone https://github.com/cloudronin/hardmap && cd hardmap
pip install -e ./eightfold -e ./proof-census -e ./foundry[analysis,dev]
foundry audit     # what the CLI does, and what still lives in dev/
foundry fresh     # every compiled artifact vs the sources it was compiled from
```

[`AGENTS.md`](AGENTS.md) is the operator's guide: the constitution, the compiled rule
surface (verbs, screens, gates), and what to escalate rather than decide.
[`CONTRIBUTING.md`](CONTRIBUTING.md) covers proposing an experiment — questions enter the
same screens as machine-generated ones.

---

## How to trust this repo

**Source of truth is the hashed JSONL.** Every result lives in a frozen, sha256-pinned JSONL
or JSON artifact, and those files are the record. `observatory.db` is a **derived artifact**:
it can be deleted and rebuilt at any time, and it is *regenerated, never mutated*. Each of
its tables carries the sha256 of the artifact it came from, so the database and its sources
can be checked against each other rather than trusted. If the two ever disagree, the JSONL is
right — which is why `hardmap db build` compiling it on your machine is the same operation
the authors run, not a shipped convenience.

The repo *is* the paper's evidence: the seal chain, the ledgers, and the numbers, checkable
without trusting the author.

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
AGENTS.md        # how to work here: constitution, compiled rule surface, escalation
NEXT.md          # what is open, compiled from the maptrail
repro/           # manifest.yaml: claim-id -> entrypoint -> expected value -> tolerance -> tier  (H3)
```

Internal dependencies: `foundry` imports `eightfold`; `proof-census` imports
`desertmap`. Publishing all four in one distribution keeps those edges resolved.


## License

Dual-licensed. Source code under **Apache-2.0** ([`LICENSE`](LICENSE)); research
data and prose (the atlas datasets, results, preregistrations, findings, and
specs) under **CC-BY-4.0** with citation of the write-up as the attribution
condition. See [`NOTICE`](NOTICE) for the exact split and
[`CITATION.cff`](CITATION.cff) to cite.
