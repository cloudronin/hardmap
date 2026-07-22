"""eightfold CLI — validate/summarize the charge atlas and run the structure preview.

Thin dispatcher; the real work lives in ``eightfold.atlas`` (validate/summary) and ``eightfold.structure``.
The submodules also run standalone:
    python -m eightfold.atlas validate
    python -m eightfold.atlas summary
    python -m eightfold.structure --pilot
    python -m eightfold.factors --selftest
"""
from __future__ import annotations

import sys


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        print("commands: validate | summary | structure | factors")
        return 0
    cmd, rest = argv[0], argv[1:]
    if cmd in ("validate", "summary"):
        from eightfold import atlas
        return atlas.main([cmd, *rest])
    if cmd == "structure":
        from eightfold import structure
        return structure.main(rest)
    if cmd == "factors":
        from eightfold import factors
        return factors.main(rest)
    print(f"eightfold: unknown command {cmd!r} (expected validate|summary|structure|factors)", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
