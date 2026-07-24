"""hardmap command-line entry point.

Scaffolding only: the repro/verify/atlas subcommands are implemented in the
CLI+manifest milestone (H3), driven by repro/manifest.yaml. Until then this
prints the current status so `hardmap` is a valid, installed console script.
"""
from __future__ import annotations

import argparse
import sys

_PENDING = (
    "hardmap CLI scaffolding is in place; the repro/verify/atlas subcommands "
    "land in the CLI+manifest milestone (H3).\n"
    "Today you can: `pip install -e .`, run each folder's pytest, or load the "
    "frozen atlas via `eightfold.atlas.load_atlas`."
)


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    parser = argparse.ArgumentParser(prog="hardmap", description=__doc__)
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("repro", help="regenerate paper-cited numbers from the manifest (H3)")
    sub.add_parser("verify", help="run the H4 internal-coherence sweep (H3/H4)")
    sub.add_parser("atlas", help="dump the frozen charge atlas (H3)")
    parser.parse_args(argv)
    print(_PENDING)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
