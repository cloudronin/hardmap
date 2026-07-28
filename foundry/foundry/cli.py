"""Foundry CLI — THE WRITE SURFACE. One binary, one dispatch, laws inherited rather than remembered.

WHY THERE ARE TWO BINARIES AND NOT ONE (ruled 2026-07-28). `hardmap` reads: repro, verify, anatomy,
atlas, over frozen artifacts, and it is what `pip install hardmap` gives the world. `foundry` writes: it
reserves rows, advances the catalog, appends to the maptrail. These must not be the same binary, and not
for taste — THE FRONTIER IS A BLINDNESS MECHANISM. If a stranger reproducing the paper could capture a
reserved row by mistyping a subcommand, the blindness the program's claims rest on would be one typo
from gone. `foundry` is repo-only and absent from the published `[project.scripts]`, so a verb that
should not be in someone's hands cannot be typed by them. That is Kill 2 promoted from a detection rule
to an impossibility — §0.1's own reasoning, physics over guards.

WHAT THE DISPATCH ENFORCES, SO NO VERB HAS TO REMEMBER IT:

  1. FRESHNESS. A verb declares what it CONSUMES; the dispatcher refuses to run it against a compiled
     artifact older than that artifact's own sources. No per-verb vigilance and no escape hatch — a
     producer simply consumes nothing, so `db compile` is free by construction rather than by exemption.

  2. EVENT-TIME EMISSION. A verb that writes emits its own maptrail record from inside the machinery
     performing the act (Kill 3). `--audit` reports which verbs do not yet, because the honest number is
     more use than a comfortable one.

THE THIRD CATEGORY IS NOT HERE, DELIBERATELY. One-time passes that ran once under a ruling —
`void_prereg_v34` and the typing adjudications — are history, not verbs. They live in
`foundry.catalog.migrations` and the only thing you can do to them is ask whether they ran. See
`foundry migrate status`.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LAT = ROOT / "foundry" / "results" / "lattice"
TRAIL = LAT / "maptrail.jsonl"
LEDGER = LAT / "observatory_reservation.jsonl"


# ── DELEGATED VERBS ─────────────────────────────────────────────────────────────────────────────────
# Recurring operations whose logic still lives in `dev/`. They are reachable through the one binary
# NOW — which is the point of a single dispatch surface — but they have not been lifted into the
# library, so the dispatcher cannot yet enforce freshness or emission on them from the inside.
#
# THE COUNT IS THE POINT. `test_cli` asserts this table only ever shrinks. Without that, "we'll lift it
# later" is a sentence in a docstring; with it, a delegated verb is a debt with a due date attached.
#
# FRESHNESS STILL APPLIES TO THEM, AT THE BOUNDARY. A delegated verb declares what it consumes exactly
# as a lifted one does, and the dispatcher checks before handing over. This matters more than it looks:
# `wave` against a stale db is the whole motivating case for the freshness law, and `wave` is delegated.
# A law that skipped precisely the case it was written for would be decorative.
# What delegation genuinely costs is EMISSION — the dispatcher cannot make a dev script emit from inside
# the act it performs, and emitting on its behalf from out here is the reconstruction Kill 3 forbids.
DELEGATED = {
    "ambient-census":  {"mod": "observatory_ambient_census", "consumes": (),
                        "why": "ground-set width across every ramp"},
    "bimodality-fill": {"mod": "bimodality_excess_fill", "consumes": (),
                        "why": "BC minus matched-r control mean, retro-filled"},
    "catalog":         {"mod": "build_catalog", "consumes": (),
                        "why": "compile the catalog from panels + extractor"},
    "reach-census":    {"mod": "observatory_reach_census", "consumes": (),
                        "why": "reach classes over the atlas"},
    "wave":            {"mod": "helm_wave", "consumes": ("observatory.db",),
                        "why": "one Helm wave: sweep, screen, slate"},
    "mint-prereg":     {"mod": "helm_mint_prereg", "consumes": ("observatory.db",),
                        "why": "mint a prereg from a slated candidate"},
}


def _delegate(name: str) -> int:
    sys.path.insert(0, str(ROOT))
    sys.path.insert(0, str(ROOT / "dev"))
    try:
        return __import__(DELEGATED[name]["mod"]).main()
    except ModuleNotFoundError as e:
        # `dev/` is excluded from the built distribution, so this is exactly what a pip user hits. It
        # is the design working, not a packaging bug — say so, rather than handing them a traceback
        # about a module they were never meant to have.
        raise RuntimeError(
            f"`{name}` is a repo-only verb: its implementation lives in dev/, which the published "
            f"distribution does not ship. The write surface is not part of `pip install hardmap` by "
            f"design — the frontier is a blindness mechanism, and a verb absent from what ships cannot "
            f"be typed by someone who should not hold it. Work from a checkout. ({e})") from None


# ── LIFTED VERBS ────────────────────────────────────────────────────────────────────────────────────

def _census_declare(args) -> int:
    from foundry.catalog import batch_census as BC
    doc, rec = BC.declare(Path(args.declaration), LAT, LEDGER, TRAIL)
    out = LAT / f"observatory_batch{doc['batch']}_census.json"
    print(f"BATCH {doc['batch']} CENSUS — roster {doc['n_roster']}, "
          f"reserved {len(rec['reserved'])}, published {len(doc['published'])}\n")
    for r, s in doc["roster"].items():
        mark = "RESERVED " if r in rec["reserved"] else "  publish "
        print(f"  {mark}{r:<34}{s['family']:<17}{s.get('structural_expectation') or '—'}")
    print(f"\n  schema          {doc['schema']}")
    print(f"  roster sha256   {rec['roster_sha256'][:16]}")
    print(f"  reserved        {', '.join(rec['reserved'])}")
    print(f"  wrote {out.name}  sha256 {BC.sha16(out)}")
    return 0


def _census_verify(args) -> int:
    """Re-derive a census from its own recorded declaration and report what differs. Never rewrites."""
    import shutil
    import tempfile
    from foundry.catalog import batch_census as BC
    src = LAT / f"observatory_batch{args.batch}_census.json"
    tmp = Path(tempfile.mkdtemp())
    shutil.copy(LEDGER, tmp / "ledger.jsonl")
    (tmp / "d.json").write_text(json.dumps(BC.declaration_from_census(src), indent=1))
    doc, _ = BC.declare(tmp / "d.json", LAT, tmp / "ledger.jsonl", tmp / "trail.jsonl",
                        out=tmp / "out.json", before_batch=args.batch)
    orig = json.loads(src.read_text())
    diff = sorted(k for k in set(doc) | set(orig) if doc.get(k) != orig.get(k))
    shape = BC.read(src)["shape"]
    print(f"batch {args.batch}  shape on disk: {shape}   declared: {orig.get('schema')}")
    print(f"  re-derives identically except: {diff or 'nothing'}")
    if shape != "v2":
        print(f"  ({BC.SCHEMA_HISTORY[shape]})")
        print("  the difference is the schema transition, not a defect — historical censuses are "
              "retro-labelled, never re-emitted")
    return 0


def _census_list(args) -> int:
    from foundry.catalog import batch_census as BC
    print(f"{'':5s}{'shape':7s}{'declared':32s}{'roster':>7s}{'resv':>6s}  carried forward")
    for d in BC.read_all(LAT):
        cf = ",".join(d["carried_forward"]) or "—"
        print(f"b{d['batch']:<4d}{d['shape']:7s}{str(d['declared_schema']):32s}"
              f"{d['n_roster']:>7d}{d['reservation'].get('n_reserved', 0):>6d}  {cf[:44]}")
    print(f"\n  current schema: {BC.SCHEMA}   (shapes in history: {len(BC.SCHEMA_HISTORY)})")
    return 0


def _db_compile(args) -> int:
    from foundry.catalog import freshness as F, loader
    info = loader.compile_db(LAT, F.atlas_path(LAT), LAT / "observatory.db")
    (LAT / "observatory_db_manifest.json").write_text(json.dumps({
        "schema": "observatory-db/v1",
        "SOURCE_OF_TRUTH": ("the hashed JSONL artifacts. This database is DERIVED — it can always be "
                            "thrown away and rebuilt; the JSONL never can."),
        "regenerated_never_mutated": ("there is no UPDATE path and no migration path. An artifact "
                                      "changing means a rebuild from scratch."),
        **info}, indent=1) + "\n")
    print("OBSERVATORY DB COMPILED\n")
    for t, n in info["counts"].items():
        print(f"  {t:<12}{n:>6}")
    print(f"\n  db sha256 {info['db_sha256'][:16]}   {len(info['sources'])} sources")
    return 0


def _next(args) -> int:
    from foundry.catalog import next_page as NP
    info = NP.compile_page(LAT, ROOT.parent / "NEXT.md")
    print(f"NEXT.md — {info['open_items']} open item(s), {info['sources']} sources recorded")
    for t in info["titles"]:
        print(f"   {t[:74]}")
    return 0


def _agents(args) -> int:
    from foundry.catalog import agents_page as AP
    import foundry.cli as this
    info = AP.compile_page(LAT, ROOT.parent, ROOT.parent / "AGENTS.md", this)
    print("AGENTS.md compiled")
    for k, v in info.items():
        print(f"   {k:<12}{v}")
    return 0


def _fresh(args) -> int:
    from foundry.catalog import freshness as F
    rc = 0
    for name in F.REGISTRY:
        st = F.check(name, LAT)
        if st["unknown"]:
            print(f"  {name:18s} UNKNOWN — records no sources; cannot be checked")
            rc = 1
            continue
        if st["stale"]:
            print(f"  {name:18s} STALE   — {F.describe(name, st['diff']).split('— ', 1)[1]}")
            print(f"  {'':18s}           rebuild: {st['rebuild']}")
            rc = 1
        else:
            print(f"  {name:18s} fresh   — {st['n_sources']} sources")
    return rc


def _migrate(args) -> int:
    from foundry.catalog import migrations as MG
    if args.action == "status":
        for s in MG.status(TRAIL):
            print(f"  {s['state']:9s} {s['name']}")
            if s["applied_at"]:
                print(f"  {'':9s} applied {s['applied_at']}   {json.dumps(s['summary'])}")
            print(f"  {'':9s} {s['why']}")
        return 0
    for r in MG.run(TRAIL, {"trail": TRAIL, "lat": LAT}, only=args.only, dry_run=args.dry_run):
        print(f"  {r['state']:16s} {r['name']}  {r.get('summary', '')}")
    return 0


def _frontier(args) -> int:
    from foundry.catalog import reservation as RES
    held = sorted(RES.reserved_rows(LEDGER))
    print(f"FRONTIER — {len(held)} rows reserved, NOT CAPTURED\n")
    for r in held:
        print(f"  {r}")
    return 0


def _trail(args) -> int:
    from foundry.catalog import maptrail as M
    recs = M.read(TRAIL)
    if args.event:
        recs = [r for r in recs if r["event"] == args.event]
    if args.grep:
        recs = [r for r in recs if args.grep in json.dumps(r)]
    for r in recs[-args.limit:]:
        flag = " [reconstructed]" if r.get("reconstructed") else ""
        print(f"  {r['at']}  {r['event']:11s} {r['key']}{flag}")
    print(f"\n  {len(recs)} record(s)")
    return 0


def _open(args) -> int:
    from foundry.catalog import maptrail as M
    items = M.open_items(TRAIL)
    for i in items:
        print(f"  {i.get('sequence', 99):>3}. {i['opens']:<34} {i['title']}")
    print(f"\n  {len(items)} open")
    return 0


def _guards(args) -> int:
    from foundry.catalog import reservation as RES
    held = RES.reserved_rows(LEDGER)
    print(f"  {len(held)} rows withheld")
    print("  reserved-row generators: checked at batch build time (assert_no_reserved_generators)")
    print("  duplicate regions:       checked at batch build time (assert_no_duplicate_regions)")
    print("  reservation is a property of the REGION, not the name above it")
    return 0


def _audit(args) -> int:
    """The honest count: what is lifted, what is delegated, what emits its own trail record."""
    lifted = sorted(VERBS)
    print(f"LIFTED into the library — freshness and emission enforced by the dispatch ({len(lifted)})\n")
    for v in lifted:
        c = VERBS[v].get("consumes", ())
        print(f"  {v:22s} consumes: {', '.join(c) or '—'}")
    print(f"\nDELEGATED to dev/ — reachable through the one binary, not yet lifted ({len(DELEGATED)})\n")
    for v, d in sorted(DELEGATED.items()):
        c = ", ".join(d["consumes"]) or "—"
        print(f"  {v:22s} dev/{d['mod']}.py — {d['why']}\n  {'':22s} consumes: {c} "
              f"(checked at the boundary; emission is not enforced)")
    print(f"\n  {len(DELEGATED)} verb(s) still hold their logic outside the library. The dispatcher "
          f"cannot\n  enforce freshness or event-time emission on those from the inside. This number "
          f"only goes down;\n  `test_cli` fails if it grows.")
    return 0


# name -> {fn, help, consumes}. `consumes` is the whole freshness contract: declare a fact, inherit the
# check. A verb that PRODUCES an artifact consumes nothing, which is why no escape hatch is needed.
VERBS = {
    "census":   {"fn": None, "help": "batch census: declare / verify / list"},
    "db":       {"fn": _db_compile, "help": "compile observatory.db from the hashed artifacts"},
    "fresh":    {"fn": _fresh, "help": "freshness of every compiled artifact"},
    "next":     {"fn": _next, "help": "compile NEXT.md from the trail", "consumes": ("observatory.db",)},
    "agents":   {"fn": _agents, "help": "compile AGENTS.md from the machinery",
                 "consumes": ("observatory.db",)},
    "migrate":  {"fn": _migrate, "help": "one-time history: status / run"},
    "frontier": {"fn": _frontier, "help": "reserved rows (declared, not captured)"},
    "trail":    {"fn": _trail, "help": "maptrail records"},
    "open":     {"fn": _open, "help": "open items, replayed from the trail"},
    "guards":   {"fn": _guards, "help": "reservation guard status"},
    "audit":    {"fn": _audit, "help": "what is lifted, what is delegated"},
}


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="foundry",
        description="The observatory WRITE surface. Repo-only by design — see the module docstring.")
    # preserved from the original CLI; documented in foundry/README.md
    p.add_argument("--validate-toy", action="store_true",
                   help="validate the hand-checked toy stratum via the shared kernel")
    p.add_argument("--r25", action="store_true", help="R25 census residual audit")
    sub = p.add_subparsers(dest="command")

    c = sub.add_parser("census", help=VERBS["census"]["help"]).add_subparsers(dest="action")
    cd = c.add_parser("declare", help="compile a declaration into a census (checks, reserves, emits)")
    cd.add_argument("--declaration", required=True, metavar="FILE",
                    help="a batch declaration; the convention is foundry/batches/<N>.json "
                         "(see foundry/batches/README.md)")
    cv = c.add_parser("verify", help="re-derive a census and report what differs; never rewrites")
    cv.add_argument("--batch", type=int, required=True)
    c.add_parser("list", help="every census, with the schema shape it is actually in")

    sub.add_parser("db", help=VERBS["db"]["help"]).add_argument(
        "action", nargs="?", default="compile", choices=["compile"])
    sub.add_parser("fresh", help=VERBS["fresh"]["help"])
    sub.add_parser("next", help=VERBS["next"]["help"])
    sub.add_parser("agents", help=VERBS["agents"]["help"])

    m = sub.add_parser("migrate", help=VERBS["migrate"]["help"])
    m.add_argument("action", nargs="?", default="status", choices=["status", "run"])
    m.add_argument("--only", metavar="NAME")
    m.add_argument("--dry-run", action="store_true")

    sub.add_parser("frontier", help=VERBS["frontier"]["help"])
    t = sub.add_parser("trail", help=VERBS["trail"]["help"])
    t.add_argument("--event"); t.add_argument("--grep"); t.add_argument("--limit", type=int, default=30)
    sub.add_parser("open", help=VERBS["open"]["help"])
    sub.add_parser("guards", help=VERBS["guards"]["help"])
    sub.add_parser("audit", help=VERBS["audit"]["help"])

    for name, d in sorted(DELEGATED.items()):
        sub.add_parser(name, help=f"{d['why']}  [delegated to dev/{d['mod']}.py]")
    return p


def main(argv=None) -> int:
    """A refusal is an answer, not a crash. Staleness, roster rejection and migration drift are all
    states the pipeline is designed to detect and report — printing a traceback for them would dress a
    working check up as a bug in the checker."""
    try:
        return _main(argv)
    except (RuntimeError, ValueError) as e:
        print(f"\nREFUSED — {e}\n", file=sys.stderr)
        return 2


def _main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    parser = build_parser()
    args = parser.parse_args(argv)

    if getattr(args, "r25", False):
        from foundry.r25 import census_r25_selftest
        return census_r25_selftest()
    if getattr(args, "validate_toy", False):
        from eightfold import atlas
        from foundry.census import toy_census
        from foundry.charges import FOUNDRY_SPEC
        rows = toy_census()
        bad = {r.problem_id: atlas.validate(r, FOUNDRY_SPEC) for r in rows}
        bad = {k: v for k, v in bad.items() if v}
        layer = FOUNDRY_SPEC.validate_entailment_layer()
        if bad or layer:
            for pid, es in bad.items():
                print(f"[{pid}]")
                for e in es:
                    print(f"  {e}")
            if layer:
                print("entailment layer:", layer)
            print(f"FAIL: {len(bad)} invalid language(s)")
            return 1
        print(f"OK: {len(rows)} toy languages validate clean under FOUNDRY_SPEC "
              f"({len(FOUNDRY_SPEC.charges)} charges); entailment layer consistent.")
        return 0

    cmd = args.command
    if cmd is None:
        parser.print_help()
        return 0
    # THE INHERITED CHECK. Not a line in each verb — one line here, driven by what the verb declared,
    # and applied to delegated verbs as well: `wave` against a stale db is the case the law exists for.
    from foundry.catalog import freshness as F
    consumes = (DELEGATED[cmd]["consumes"] if cmd in DELEGATED
                else VERBS.get(cmd, {}).get("consumes", ()))
    for artifact in consumes:
        F.require(artifact, LAT)

    if cmd in DELEGATED:
        return _delegate(cmd)

    if cmd == "census":
        action = getattr(args, "action", None)
        if action == "declare":
            return _census_declare(args)
        if action == "verify":
            return _census_verify(args)
        if action == "list":
            return _census_list(args)
        parser.parse_args(["census", "--help"])
        return 0
    return VERBS[cmd]["fn"](args)


if __name__ == "__main__":
    raise SystemExit(main())
