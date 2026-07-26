# hardmap program consolidation — W0 outline

**Status:** W0 deliverable. Outline and claims-map skeleton only. **No section prose is drafted, and none
will be until the outline is ruled.** Venue-agnostic.

**The governing law, restated because it governs W1–W4:** every number in the draft traces to a frozen
artifact by hash, and the draft contains no claim not already in a scored, sealed, or frozen record. This
document synthesizes; it never discovers. The map is [claims-map.md](claims-map.md).

---

## What W0 found

The map's first job is to say what cannot be sourced. The enumeration arrived 2026-07-26 and closed most of
it; four items remain, and two of them are findings rather than gaps.

### Still open

| item | § | state |
|---|---|---|
| **assertion 7's hard pole** — pairwise-independent-supporting solution sets | 3 | **UNSOURCED.** Zero repo matches; only scattered ingredients. The easy pole is fully grounded. See the map's #7 note — the nearest ledger cell is UNPINNED for a reason that touches the wording. |
| **"geometry probes"** (banked notes) | 6 | zero matches; drop or supply |
| **"census localization"** | 3 | resolved to `census.backbone` by the enumeration's own wording ("forced-core contradictions, 1 → 273"); the earlier Mosaic-`localization` reading is retired |
| **the convex-analysis framing** | 1 | one incidental hit, no framing document — position or intention? |

### Stale records the draft would otherwise inherit

- **`README.md` claims the CLI reproduces "all eight paper-cited numbers."** The manifest carries **28**,
  and the README refers to "the accompanying preprint" in the present tense. Both stale.
- **The methods ledger's numbering is not contiguous:** 26 headers spanning **6–31**, instances **1–5
  predate the file** (its own preamble says so), **15 absent**, **6 appears twice**. "~28 instances" is not
  a number any artifact supports; the honest form is *"26 numbered entries, 6–31, five predating the
  ledger."*
- **§7's obligations were never copied into the repo** — they live in the Mosaic v3 and Strata v2 specs.
  W1 lands them as a findings artifact so the writeup cites in-repo.

## Outline

### §1 — The question and the object
The two-table design: charge atlas = **fate** (cited facts about the literature), Anatomy = **what a
problem is**; the bridge between them as the research object. The founding law — *structure never enters
the charge table, and no charge value informs a structure cell* — and why it is a law rather than a
convention. Convex-analysis framing **pending B-2 above**.
*Evidence class: design, not measurement. Sources are the sealed schemas.*

### §2 — The artifacts
Charge atlas v1 / v2 / v3 (+ the v3.1 promotion track), Anatomy v1 and v2, the passport system, the seal
chain (43 sealed preregistrations resolved through `docs/hash-map.txt`), and reproducibility
(`pip install hardmap && hardmap repro`). What each froze, when, at which hash.
*Evidence class: frozen bytes. Every hash in the map is verified at W1, not quoted from here.*

### §3 — The nine assertions — **enumeration supplied 2026-07-26**
Each assertion carries its evidence class (PROVEN / MEASURED / CITED) and artifact pointer; every numeric
literal was extracted from an artifact at W0, not transcribed. **Eight of nine source cleanly.** Two
prose-level constraints carry into W1:
- **#2 cites two different statistics** — the sealed B1 falsification (v3-new corrected **V = 0.0**) and
  the four-population arc (**0.73 → 0.39 → 0.26 → 0.10**). The arc's 0.10 is a *stratum* of v3-new; the
  0.0 is the *whole population* corrected. They never share a sentence.
- **#7 ships split** — easy pole grounded in the Post-lattice machinery, hard pole carrying no repo
  receipt, and the ledger's `§5.approximation` cell UNPINNED for a reason that names the assertion's own
  "manufacturable on expanders" phrasing. Kept distinct in prose, or the ledger appears to contradict the
  assertion it is cited to support.
*Evidence class: mixed — #4 and #7-easy are PROVEN, #1/#2/#3/#5/#6/#8 MEASURED, #9 CITED + one proven-here.*

### §4 — The negative results, with their receipts
The honest arc, each with its **sealed verdict quoted verbatim**: Pebble's absorption; the unaskable
conditioning; the powered locality MISS; the circular P4; Terroir's FAMILY-BORNE; Marrow's unaskable
closure retest. Framed as *the map of where the answer isn't*.
*Evidence class: scored verdicts. This section is the most heavily sourced in the document and the one
where softening is most tempting — the both-directions check at W3 targets it first.*

### §5 — The methods contribution
The ledger as first-class: 26 numbered entries (6–31; five predate the file), the taxonomy
(both-directions errors · the tidy-number tell · census-before-seal · denominator matching ·
**expression-not-artifact** · *"it pointed the unflattering way"*), the delegation protocol, and the gates
now running in CI (`hardmap verify`, 10/10). Written as the most durable section, per the directive.
*Evidence class: the ledger itself plus the gate code. Failures included as content.*

### §6 — Open instruments and the standing state
The prospective registry (design, 0/57, the mechanism-attribution rules); the two-verdict stack; the
banked notes (**geometry probes pending A above**; the frontier map is in
`arm-a-surface-vs-closure.md`). Closes on the honest sentence: **the mechanism question now lives
exclusively prospectively.**

### §7 — Related work — **sourced to the specs, not the repo**
The obligations are recorded in `mosaic-v3-...-spec.md` §7 ("Related-work obligations (dated hunts;
mandatory in the writeup)") and `strata-v2-...-spec.md` §I2: the meta-problem line (Bulatov;
Creignou–Khanna–Sudan; AutCSP), ISA/EHM, ISGCI, CoRCoD and structure→dynamics ML.
**One scope limit:** the spec's claim that the two-table object "remains unclaimed territory per the hunts"
is citable as *the program's dated position*, not as reproducible evidence — the hunts' results are not in
the repo. Stated as a position or re-run as declared new work; not asserted as a finding.

---

## Draft-order consequence

**W1's scope as directed (§§2–4) is now drafts in full**, with #7 shipping split unless its hard pole gets
a source. §1 needs only the convex-framing disposition; §6 needs the geometry-probes disposition or a drop.
No change to the milestone table.

## Tone constraints carried into W1
Plain declarative prose. No superlatives. Negatives at full strength with their seals. Conditionals on
standard conjectures stated once, cleanly. PROVEN / MEASURED distinction enforced in prose wherever bridge
cells appear. The ledger's failures are content, not confession.
