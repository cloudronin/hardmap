#!/usr/bin/env python3
"""Shim. The page compiler was LIFTED into `foundry.catalog.next_page` (2026-07-28); this entry point
survives so existing invocations keep working. Prefer `foundry next`."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from foundry.catalog import next_page as NP                                     # noqa: E402


def main() -> int:
    info = NP.compile_page(ROOT / "foundry" / "results" / "lattice", ROOT.parent / "NEXT.md")
    print(f"NEXT.md — {info['open_items']} open item(s), {info['sources']} sources recorded")
    return 0


if __name__ == "__main__":
    sys.exit(main())
