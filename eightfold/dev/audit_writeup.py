#!/usr/bin/env python3
"""W2 — the number audit. Every statistic in the write-up, diffed against its artifact.

THE RULE THIS ENFORCES (W2 gate): an orphan number is a HALT, not a footnote. A numeric literal in the
prose either matches a value this script extracted LIVE FROM AN ARTIFACT, or the audit fails.

WHY IT IS A SCRIPT AND NOT A READ-THROUGH. A human pass over ~150 numerals confirms what it expects to
find; that is the failure mode the claims map exists to prevent, applied one level up. The registry below
is built by opening artifacts at audit time — never from the draft, never from the map's own table, and
never hardcoded. If the draft and the artifact disagree, the artifact wins and the audit says so.

STRUCTURAL NUMERALS are exempt and enumerated: section numbers, ordinals, years, and small counting words
that refer to the document's own shape ("two tables", "eight charges"). The exemption list is explicit so
that it can be audited too — anything not on it and not in the registry is an orphan.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
AT = ROOT / "eightfold" / "results" / "atlas"
REPO = ROOT.parent
DRAFT = ROOT / "docs" / "paper" / "hardmap-program-v1.md"


def num(x):
    return round(float(x), 6)


def build_registry():
    """Open every artifact the draft cites and collect the values it may legally contain."""
    reg, prov = {}, {}

    def add(v, where):
        k = num(v)
        reg.setdefault(k, set()).add(where)
        prov[k] = where

    # ── §2 artifacts: row counts and hashes ──────────────────────────────────────────────────────
    for f in ("atlas.jsonl", "atlas_v2.jsonl", "atlas_v3.jsonl", "anatomy_v1.jsonl", "anatomy_v2.jsonl"):
        rows = [l for l in (AT / f).read_text().splitlines() if l.strip()]
        add(len(rows), f"{f} row count")
    for f in ("anatomy_v1.jsonl", "anatomy_v2.jsonl"):
        rows = [json.loads(l) for l in (AT / f).read_text().splitlines() if l.strip()]
        add(sum(1 for r in rows if r["universe"] == "natural"), f"{f} natural rows")
        add(sum(1 for r in rows if r["universe"] == "boolean"), f"{f} boolean rows")
    add((REPO / "docs" / "seal-chain.md").read_text().count("prereg_v"), "seal-chain prereg count")
    # the ledger's size is DERIVED from its headers, never quoted — a hardcoded count in a growing file
    # is stale the next time someone appends (it was, within a day)
    mt = (ROOT / "docs" / "findings" / "methods-thread.md").read_text()
    inst = [int(x) for x in re.findall(r"^## Instance (\d+)", mt, re.M)]
    add(len(inst), "ledger: numbered entries")
    add(min(inst), "ledger: first number"); add(max(inst), "ledger: last number")
    # the registry's pinned floor
    regj = json.loads((AT / "grid-prospective-registry.json").read_text())
    ta = regj.get("threshold_arithmetic") or {}
    if ta.get("FLOOR_scored"):
        add(ta["FLOOR_scored"]["n"], "registry: pinned scored floor")
    add(len(regj.get("entries", [])), "registry: entries")
    add(sum(1 for e in regj.get("entries", []) if e.get("counts_in_scored_n")), "registry: scored cells")
    manifest = (REPO / "repro" / "manifest.yaml").read_text()
    add(manifest.count("\n  - id:"), "manifest claim count")
    from hardmap import verify as V
    add(len(V.CHECKS), "hardmap verify check count")

    # passports
    from eightfold import anatomy as AN
    doc = json.loads((AT / "anatomy-passports.json").read_text())
    add(len(AN.COLUMNS), "v1 column count")
    adm = [c for c in AN.COLUMNS if AN.passport_admissible(c, doc)[0]]
    add(len(adm), "v1 admissible as-is")
    add(len([c for c in AN.COLUMNS if c not in adm
             and doc["columns"].get(c, {}).get("admissible_collapse")]), "v1 via collapse")
    add(len([c for c in AN.COLUMNS if doc["columns"].get(c, {}).get("invariance") == "invariant"]),
        "v1 invariant")
    v2 = json.loads((AT / "anatomy_v2_passports.json").read_text())
    add(len(AN.V2_COLUMNS), "v2 column count")
    add(len(json.loads((AT / "anatomy_v2_freeze.json").read_text())["admissible_for_a_sealed_bet"]),
        "v2 admissible")
    add(json.loads((AT / "anatomy_v2_freeze.json").read_text())["n_rows_carrying_v2_columns"],
        "v2 rows carrying closure columns")

    # the closure-bar EXCLUSION count, derived — never quoted. The geometry-probes note carries 311,
    # computed from the census's 34 BEFORE M1's closer look reduced the presentable set to 28.
    npin = json.loads((AT / "marrow-presentations.json").read_text())["n_pinned"]
    nnat = sum(1 for l in (AT / "anatomy_v1.jsonl").read_text().splitlines()
               if l.strip() and json.loads(l)["universe"] == "natural")
    add(nnat - npin, "derived: natural rows excluded by the closure admission bar")

    # ── manifest expected values (§3 and §4 claims) ──────────────────────────────────────────────
    for m in re.finditer(r"- id: (\S+)\n(.*?)(?=\n  - id:|\Z)", manifest, re.S):
        cid, blk = m.group(1), m.group(2)
        for v in re.findall(r"[-+]?\d+\.\d+|(?<![\w.])\d+(?![\w.])", blk):
            try:
                add(v, f"manifest {cid}")
            except ValueError:
                pass

    # ── Terroir / Marrow result artifacts ────────────────────────────────────────────────────────
    def deep(o, tag):
        if isinstance(o, dict):
            for k, v in o.items():
                deep(v, tag)
        elif isinstance(o, list):
            for v in o:
                deep(v, tag)
        elif isinstance(o, (int, float)) and not isinstance(o, bool):
            add(o, tag)
    for f in ("terroir_v1_results.json", "terroir_v1_ablations.json", "marrow-i0-census.json",
              "marrow-terroir-c-power.json", "marrow-presentations.json", "marrow-derived.json",
              "marrow-presentation-audit.json", "anatomy_v2_freeze.json"):
        if (AT / f).exists():
            deep(json.loads((AT / f).read_text()), f)

    # ── the proof census ─────────────────────────────────────────────────────────────────────────
    c3p = REPO / "proof-census" / "proofcensus" / "results" / "c3" / "c3_summary.json"
    if c3p.exists():
        c3 = json.loads(c3p.read_text())
        deep(c3, "c3_summary.json")
        g = c3["grid"]
        add(c3["n_records"] * g["K"] * 2, "c3 derived: total verified proofs")
        n60 = c3["trends"]["n60"]
        L = n60["median_length"]["s2"]
        add(round(L[0] / L[-1], 1), "c3 derived: n60 s2 length ratio")
        agree = sum(1 for n in c3["trends"] for m_ in c3["trends"][n] if c3["trends"][n][m_]["agree"])
        total = sum(len(c3["trends"][n]) for n in c3["trends"])
        add(total, "c3 derived: trend comparisons")
        add(agree, "c3 derived: trends agreeing")
        add(c3["n_records"] - len(c3["coverage"]), "c3 derived: covered records")

    # ── Foundry lattice results: Arm A and the geometry probe. NOTE these were invisible to the
    # tidy-number gate until 2026-07-26 (its lattice path resolved nowhere), so the draft was quoting
    # numbers no gate had watched. The audit registry opens them explicitly.
    try:
        import foundry
        latd = Path(foundry.__file__).resolve().parent / "results" / "lattice"
        for f in ("grid_arm_a_results.json", "grid_arm_a_results_clean.json",
                  "geometry_probe_a_results.json"):
            if (latd / f).exists():
                deep(json.loads((latd / f).read_text()), f)
    except ImportError:
        pass

    # ── findings PROSE artifacts (Pebble, Arm A) — the draft quotes numbers that live only here ──
    for rel, tag in (("foundry/docs/findings/Pebble-findings.md", "Pebble-findings.md"),
                     ("foundry/docs/findings/generation-cannot-reach-the-gradient.md", "generation-note"),
                     ("eightfold/docs/findings/arm-a-surface-vs-closure.md", "arm-a-surface-vs-closure.md"),
                     ("eightfold/docs/findings/quarry-v2-gate4-sitting.md", "gate4-sitting.md"),
                     ("eightfold/docs/findings/mosaic-findings.md", "mosaic-findings.md"),
                     ("eightfold/docs/findings/mosaic-L1-findings.md", "mosaic-L1-findings.md"),
                     ("eightfold/docs/findings/absorption-closeout.md", "absorption-closeout.md"),
                     ("eightfold/docs/findings/quarry-v3-V4-battery.md", "quarry-v3-V4-battery.md"),
                     ("eightfold/docs/findings/counting-folklore-gap.md", "counting-folklore-gap.md"),
                     ("proof-census/docs/findings/C3-verdict.md", "C3-verdict.md"),
                     ("eightfold/docs/findings/methods-thread.md", "methods-thread.md"),
                     ("eightfold/docs/findings/Factors-v1.md", "Factors-v1.md"),
                     ("eightfold/docs/findings/errata.md", "errata.md"),
                     ("eightfold/docs/findings/terroir-v1-findings.md", "terroir-v1-findings.md"),
                     ("eightfold/docs/findings/marrow-i0-census.md", "marrow-i0-census.md"),
                     # BANKED NOTES are artifacts too. A number quoted AS THE NOTE'S — including a stale
                     # one the draft flags as stale — resolves here. Notes are dated positions, never
                     # evidence (claims-map rule 8), so a value sourced from one may only ever be
                     # attributed to it.
                     ("eightfold/docs/notes/geometry-probes-note.md", "notes/geometry-probes-note.md"),
                     ("eightfold/docs/notes/frontier-map-note.md", "notes/frontier-map-note.md")):
        f = REPO / rel
        if f.exists():
            for v in re.findall(r"[-+]?\d+\.\d+|(?<![\w.])\d{1,6}(?![\w.])", f.read_text()):
                try:
                    add(v, tag)
                except ValueError:
                    pass

    # ── prereg + findings values the draft quotes ────────────────────────────────────────────────
    for f, tag in ((AT / "grid_arm_b_results.json", "grid_arm_b_results.json"),):
        if f.exists():
            deep(json.loads(f.read_text()), tag)
    return reg


# numerals that refer to the document's own shape, not to a measurement
STRUCTURAL = {2, 3, 4, 5, 6, 7, 8, 1, 9, 10, 11, 12}          # section refs, small counts, ordinals
YEARS = {2005, 2015, 2006, 2026, 2001, 1978}
EXEMPT_CONTEXT = re.compile(
    r"^#{1,6}\s|§|section|Thm|ESA|IWPEC|20\d\d|H[123]\b|v[123]\b|W[0-4]\b|arity\s*≤?\s*\d|"
    r"assertion|item|\bfigure\b|sha256|\[:16\]", re.I)


def audit():
    reg = build_registry()
    text = DRAFT.read_text()
    # strip code spans and the hash table (hashes are verified separately, not numerically)
    body = re.sub(r"`[^`]*`", "`X`", text)

    orphans, checked = [], 0
    for m in re.finditer(r"(?<![\w.$])[-+−]?\d[\d,]*\.?\d*%?", body):
        raw = m.group(0)
        line_start = body.rfind("\n", 0, m.start()) + 1
        line = body[line_start:body.find("\n", m.end())]
        tok = raw.replace(",", "").replace("−", "-").rstrip("%")
        try:
            val = num(tok)
        except ValueError:
            continue
        if val in STRUCTURAL or val in YEARS:
            continue
        if EXEMPT_CONTEXT.search(line):
            continue
        checked += 1
        # MATCHING RULE, tightened after the probe caught it going slack.
        # Exact match always counts. Rounding counts ONLY at >= 3 decimals: with a registry of several
        # hundred values, a 2-decimal prose figure will find SOME value rounding to it by coincidence —
        # a fabricated 0.61 matched a genuine, unrelated 0.6065. So a 2-decimal figure must appear
        # literally in an artifact. The burden sits where it belongs: the draft quotes the precision the
        # artifact carries, rather than the audit guessing which coarse value was meant.
        cands = {val, num(abs(val))}
        if raw.endswith("%"):
            cands |= {num(val / 100)}
        decs = len(tok.split(".")[1]) if "." in tok else 0
        hit = bool(cands & set(reg))
        if not hit and decs >= 3:
            hit = any(round(r, decs) in cands or round(abs(r), decs) in cands for r in reg)
        if not hit:
            orphans.append((raw, line.strip()[:105]))
    return reg, checked, orphans


def main() -> int:
    reg, checked, orphans = audit()
    print("W2 — THE NUMBER AUDIT\n")
    print(f"  registry values extracted from artifacts : {len(reg)}")
    print(f"  numerals checked in the draft            : {checked}")
    print(f"  ORPHANS (halt, not footnote)             : {len(orphans)}\n")
    for raw, line in orphans:
        print(f"  ORPHAN  {raw:>10}   {line}")
    if orphans:
        print(f"\n  W2 FAILS — {len(orphans)} numeral(s) with no artifact. "
              f"Each is a halt: source it, correct it, or cut it.")
        return 1
    print("  W2 PASSES — every audited numeral resolves to an artifact value.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
