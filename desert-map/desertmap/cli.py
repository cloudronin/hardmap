"""desert-map top-level CLI.

Kept torch-free: dispatches to subcommands that lazy-import their heavy deps. For HF Jobs submission
use `python -m desertmap.hf.launch` directly (its own stable, narrow-permission CLI).
"""
from __future__ import annotations

import argparse

from desertmap import __version__


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="desertmap", description="Proof-Space Cartography v1 (Desert Map).")
    ap.add_argument("--version", action="version", version=f"desert-map {__version__}")
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("fixtures", help="generate/verify versioned instance fixtures (M1)")
    args = ap.parse_args(argv)

    if args.cmd == "fixtures":
        from desertmap import fixtures
        return fixtures.main([])
    ap.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
