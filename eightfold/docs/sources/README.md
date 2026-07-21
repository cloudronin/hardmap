# Source snapshots (R10)

Committed archives of rot-risk **web-only** sources cited by the atlas, so
`python -m eightfold.atlas validate` still resolves its citations when the live pages go dark. Every cell in
`results/atlas/atlas.jsonl` whose provenance carries a `url` also carries a `snapshot` pointer (a Wayback
capture URL, or a path under this directory) and a `retrieved` ISO date; the validator enforces this (gate 8).

Primary rot-risk sources:

- **Crescenzi–Kann, *A Compendium of NP Optimization Problems*** — hand-maintained 1990s HTML (KTH:
  `nada.kth.se/~viggo/problemlist/`), already cited through a third-party cache. The RANDOM'97 paper and the
  book *Complexity and Approximation* (Ausiello et al., 1999) are the stable anchors; the live problem pages
  are the rot risk.
- **Complexity Zoo** (`complexityzoo.net`) — MediaWiki content that drifts; a Chris Bourke LaTeX export and a
  2023 archive.org dump exist as durable fallbacks.

**Prefer a persistent identifier (DOI, book + page) where one exists** — most atlas cells cite Garey & Johnson
(1979), Ausiello et al. (1999), or primary theorem papers by DOI and need no snapshot. Snapshot only the
web-only citations. A local snapshot committed here should be named `<source-slug>.<retrieved-date>.html` (or
`.pdf`) and referenced from the cell's `provenance.snapshot`.
