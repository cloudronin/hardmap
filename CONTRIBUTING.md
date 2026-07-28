# Contributing

There are three useful things you can do here, and one you can't. Taking them in order of
how much we want them.

## Propose an experiment

**This is the highest-value contribution and the one the machinery is actually built for.**

[Open an issue](https://github.com/cloudronin/hardmap/issues/new?template=experiment.yml)
with a question. It enters the **question bank**
([`foundry/docs/findings/sounding-survey-banked-questions.md`](foundry/docs/findings/sounding-survey-banked-questions.md)),
and from there the wave engine imports it as a candidate record alongside every question the
sweep generated for itself. It then faces the same screens, in the same order, and is ruled
at the same sitting.

That is the point, and it is not a courtesy. A question from a person and a question from an
enumeration are the same kind of object here: both must have a typed null for the bet they
would become, both must clear the power floor against the reserved tranche, both die to the
netting rule if the two quantities are related by the extractor's own arithmetic. The
machine proposes and the frontier adjudicates; where the proposal came from is not one of
the screens.

**One asymmetry, disclosed rather than smoothed over.** A banked question carries
`no_enumeration_denominator`. The sweep knows how many co-movement pairs it enumerated, so a
multiple-comparisons correction over machine candidates is computed from a denominator you
can audit. A question that arrived from outside was not enumerated by anything, so it has no
such denominator and its record says so. This does not make it worse — it makes its
correction a different and weaker object, and the artifact is honest about which.

The issue template asks for three things:

1. **The question**, stated so a screen could reject it. "Is there structure in the catalog"
   is not a question; "does `bimodality_excess` co-move with `overlap_ref` within the
   `optimization` family" is.
2. **The population it concerns** — which rows, which regions, which flavours. A question
   whose population is empty after family filtering gets `INSUFFICIENT-by-population`, and
   it is better to find that out before a sitting than at one.
3. **Any prior you have already seen.** If you looked at the data and *then* formed the
   question, say so. That is not disqualifying; it is a *disclosed prior*, and the program
   already carries several. What is disqualifying is a disclosed prior presented as a fresh
   one, because the seal's whole value is that it was made before the looking.

You do not need to know the codebase. A good question with a clearly named population is
worth more than a pull request.

## Why you can't write to the archive

A declared fraction of every batch is **reserved**: those rows are named, hashed, and never
captured, so no frames exist for them and predictions can be sealed before their outcomes do.
Blindness is physics here rather than a rule anyone has to respect. Accepting an outside
write — a new row, a new frame, a corrected descriptor — would mean trusting that it did not
touch reserved ground, and a trust relationship is exactly the thing the reservation replaces.
So the write verbs live in `foundry`, which ships with a checkout and not with the package,
and the archive takes no external commits against its measured content. Questions, yes.
Corrections, as issues. Bytes, no.

## Run your own

The licence permits it and the design expects it. Fork, clone, and `foundry` is yours:

```bash
git clone https://github.com/<you>/hardmap && cd hardmap
pip install -e ./eightfold -e ./proof-census -e ./foundry[analysis,dev]
foundry audit
```

Your fork has its own reservation ledger, so it has its own frontier. Reserve your own rows,
run your own waves, seal your own bets. Nothing about the blindness argument requires our
frontier in particular — it requires *a* frontier that was declared before the readings, and
yours will be.

If you build something that disagrees with a result here, that is the most useful outcome
available and we would like to see it. Open an issue with the query that shows the
disagreement; `hardmap query --sql` output is enough.

## Also welcome

- **Bugs in the machinery** — a screen that admits what it should reject, a query that
  returns the wrong shape, a number in the docs that does not match the artifact. For that
  last one the artifact is right and the doc is wrong; say which you found.
- **Documentation that misled you.** The README's front door was rebuilt because its author
  bounced off it. If you could not get from "heard about it" to "queried it", that is a bug
  report and we want it in those words.

Code contributions to the CLI, the loader, or the test suite are welcome as pull requests.
Anything touching `foundry/foundry/results/` will be declined — see above.

## Ground rules for changes

Read [`AGENTS.md`](AGENTS.md) first; it is the operator's guide and it is short. The parts
that will bite a newcomer:

- **Frozen bytes stay byte-identical.** If a test says an artifact is frozen, it is.
- **Compiled artifacts regenerate byte-identically** — no timestamps, no run ids, no commit
  ids. Append-only logs are the exception and legitimately stamp time.
- **Provenance is emitted by the machinery performing the act**, never added afterwards.
- **`hardmap verify` (11 checks) and the full test suite pass before a merge.**
