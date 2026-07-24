"""`hardmap atlas` -- dump the frozen charge atlas.

jsonl streams the frozen file verbatim (byte-identical, the invariant the round-trip
test enforces); csv flattens one row per problem with a column per charge value.
"""
from __future__ import annotations

import csv
import sys

from eightfold.atlas import get_charge, load_atlas, resolve_atlas_path
from eightfold import charges as C


def run(fmt: str = "jsonl") -> int:
    if fmt == "jsonl":
        sys.stdout.write(resolve_atlas_path().read_text(encoding="utf-8"))
        return 0
    if fmt == "csv":
        entries = load_atlas()
        cols = ["problem_id", "problem_name", "problem_family", *C.EIGHTFOLD_SPEC.charges]
        w = csv.DictWriter(sys.stdout, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for e in entries:
            row = {"problem_id": e.problem_id, "problem_name": e.problem_name,
                   "problem_family": e.problem_family}
            for ch in C.EIGHTFOLD_SPEC.charges:
                cell = get_charge(e, ch)
                row[ch] = cell.value if cell else ""
            w.writerow(row)
        return 0
    print(f"unknown format: {fmt}", file=sys.stderr)
    return 2
