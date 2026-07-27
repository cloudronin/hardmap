#!/usr/bin/env python3
"""Compile observatory.db from the frozen artifacts. REGENERATES — never mutates."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from foundry.catalog import loader

LAT = ROOT / "foundry" / "results" / "lattice"
ATLAS = ROOT.parent / "eightfold" / "eightfold" / "results" / "atlas" / "atlas_v3.jsonl"
DB = LAT / "observatory.db"

def main():
    info = loader.compile_db(LAT, ATLAS, DB)
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
    print(f"\n  db sha256 {info['db_sha256'][:16]}")
    print("\n  sources:")
    for k, v in sorted(info["sources"].items()):
        print(f"    {k:<42}{v[:16]}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
