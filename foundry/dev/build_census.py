"""Build the Boolean census → foundry/results/census/census.jsonl.

    python dev/build_census.py

Assembles one verified, charge-classified row per co-clone in the roster (postlattice.py) via the dichotomy
oracles (oracles.py), serialized in Eightfold's atlas JSONL format so the shared kernel validates it directly.
"""
import json
from pathlib import Path

from eightfold.atlas import entry_to_dict

from foundry.oracles import build_boolean_census

OUT = Path(__file__).resolve().parents[1] / "foundry" / "results" / "census" / "census.jsonl"


def main() -> int:
    rows = build_boolean_census()
    OUT.write_text("\n".join(json.dumps(entry_to_dict(r), ensure_ascii=False) for r in rows) + "\n",
                   encoding="utf-8")
    profiles = {tuple((c.charge, c.value) for c in sorted(r.charges, key=lambda c: c.charge)) for r in rows}
    print(f"wrote {len(rows)} co-clone rows → {OUT}  (distinct charge profiles: {len(profiles)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
