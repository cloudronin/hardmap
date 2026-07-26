# W4 — review cover

**Delivered:** [the draft](hardmap-program-v1.md) · [the claims map](claims-map.md) ·
[the outline](hardmap-program-v1-outline.md). All on `main`.

---

## What passed, and what it cost

| gate | result |
|---|---|
| **W0** outline + map | 3 of 9 assertion-candidates rejected before prose existed; recut to eight |
| **W1** §§2–4 | both NEEDS-EXTRACTION rows resolved; one misattribution caught by the halt rule |
| **W2** number audit | **509 registry values · 95 numerals · 0 orphans**, gate probe-tested |
| **W3** §§1, 5–7 + read | 8/8 evidence-class tags; both prose constraints held; conditional stated once |

**The number audit is a script, not a read-through**, and its registry opens artifacts at audit time —
never the draft, never the map, never hardcoded. It ships with a probe test that plants fabricated numerals
and asserts each is caught, because a check never observed to fail is not known to work.

That probe earned itself twice. It caught the audit going slack when the registry grew: a **fabricated
`0.61` matched a genuine, unrelated `0.6065`** through the rounding rule. Rounding is now permitted only at
three decimals or more — a two-decimal figure must appear *literally* in an artifact. The burden sits where
it belongs: the draft quotes the precision the artifact carries, rather than the audit guessing which
coarse value was meant.

## Three things to check that a gate cannot

1. **§3.4 is the one PROVEN assertion, and it is the one where the program's contribution is smallest.**
   It states the dichotomy determinism and the blending characterization, and says plainly that the program
   computed and confirmed rather than proved. Read it for whether the disclaimer is prominent enough — a
   reader skimming could take the section as a result.
2. **§3.2 cites two statistics that must not merge.** The sealed falsification (`0.0`) and the
   four-population arc (`0.73 → 0.39 → 0.26 → 0.10`) are in separate paragraphs by rule. Check the prose
   makes their difference legible, not just their separation.
3. **§5 is claimed as the most durable section.** It is also the one with no external check — a methods
   ledger cannot be audited against an artifact the way a statistic can. Its claim to generality is the
   thing most worth your scepticism.

## The venue question — posed, not answered

The draft is venue-agnostic by construction and can go three ways. The choice is yours and nothing in the
work forecloses it:

- **One preprint.** The pair of campaigns is the object; the methods ledger travels with the findings that
  produced it. Longest, and the only form in which §5's rules carry their evidence.
- **Split: findings paper + methods paper.** §§1–4, 6–7 as the empirical account; §5 as a standalone
  methods contribution. The ledger may reach a wider audience alone — and would lose the failures that
  justify it.
- **Split: two-table paper + census paper.** The census is already structurally standalone — own object,
  own instrument, own seal chain, and the program's one fully-positive result. §6 banks this option
  explicitly if the backbone line extends.

**One consideration that is evidence rather than preference.** The census is the only campaign here that
confirmed both its hypotheses with neither kill criterion firing. In a single document it is the existence
proof that the method produces positives and not only well-characterised negatives. Extracted, the
remaining document is honest but uniformly negative, and the census paper loses the discipline that makes
its positive credible. That is an argument about what each artifact can support alone — not a
recommendation.

## Standing state

Three scoped items remain queued and independent of the writeup: the array-walker extremals batch (a known
blind spot in the tidy-number gate, recorded rather than silently fixed), `3-coloring-extension`'s errata
investigation (the presentation audit's one genuine candidate), and Zoo Z0.
