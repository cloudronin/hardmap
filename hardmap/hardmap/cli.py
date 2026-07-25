"""hardmap command-line entry point: repro / verify / atlas."""
from __future__ import annotations

import argparse
import sys

from . import atlas as atlas_cmd
from . import repro as repro_cmd
from . import verify as verify_cmd


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="hardmap",
        description="Reproduce the paper-cited numbers and check internal coherence.",
    )
    sub = p.add_subparsers(dest="command")

    pr = sub.add_parser("repro", help="regenerate paper-cited numbers from the manifest")
    pr.add_argument("--claim", action="append", metavar="ID", help="run specific claim id(s)")
    pr.add_argument("--all", action="store_true", help="run every claim (default)")
    pr.add_argument("--full", action="store_true", help="full tier: regenerate from scratch where available")
    pr.add_argument("--list", action="store_true", help="list claim ids and exit")

    sub.add_parser("verify", help="run the internal-coherence sweep")

    pan = sub.add_parser("anatomy", help="dump the Structure Atlas (rows, or the column passport table)")
    pan.add_argument("--format", choices=["jsonl", "csv"], default="jsonl")
    pan.add_argument("--universe", choices=["natural", "boolean"], help="filter to one universe")
    pan.add_argument("--column", help="filter to rows carrying this column")
    pan.add_argument("--passports", action="store_true", help="dump the passport table instead of rows")

    pa = sub.add_parser("atlas", help="dump the frozen charge atlas")
    pa.add_argument("--format", choices=["jsonl", "csv"], default="jsonl")

    return p


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "repro":
        return repro_cmd.run(claim_ids=args.claim, full=args.full, list_only=args.list)
    if args.command == "verify":
        return verify_cmd.run()
    if args.command == "anatomy":
        from . import anatomy as anatomy_cmd
        return anatomy_cmd.run(fmt=args.format, universe=args.universe,
                               column=args.column, passports=args.passports)
    if args.command == "atlas":
        return atlas_cmd.run(fmt=args.format)
    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
