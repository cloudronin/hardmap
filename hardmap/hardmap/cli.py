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

    # THE ARCHIVE. Building is DERIVATION, not archive-writing: it compiles a throwaway database from
    # frozen JSONL that ships in the wheel, reserves nothing, and emits no trail event. So it belongs on
    # the read surface without weakening the read/write split one bit.
    pdb = sub.add_parser("db", help="compile the queryable observatory database from the frozen JSONL")
    pdb.add_argument("action", nargs="?", default="build", choices=["build"])
    pdb.add_argument("--path", metavar="FILE", help="where to write it (default ./observatory.db)")

    pq = sub.add_parser("query", help="run a worked query against the database")
    pq.add_argument("name", nargs="?", help="query name; see --list")
    pq.add_argument("--list", action="store_true", dest="list_only", help="list the worked queries")
    pq.add_argument("--sql", metavar="SQL", help="run freeform SQL instead (read-only)")
    pq.add_argument("--db", metavar="FILE", help="database path (default ./observatory.db)")
    pq.add_argument("--limit", type=int, default=40, help="max rows to print (default 40)")

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
    if args.command == "db":
        from . import archive
        return archive.run_build(args.path)
    if args.command == "query":
        from . import archive
        if not (args.list_only or args.name or args.sql):
            parser.parse_args(["query", "--help"])
            return 0
        return archive.run_query(args.name, args.sql, args.list_only, args.db, args.limit)
    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
