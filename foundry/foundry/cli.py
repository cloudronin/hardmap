"""Foundry CLI — validate the census through the shared Eightfold kernel with FOUNDRY_SPEC."""
import argparse
import sys

from eightfold import atlas

from foundry.charges import FOUNDRY_SPEC
from foundry.census import toy_census


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="foundry")
    ap.add_argument("--validate-toy", action="store_true",
                    help="validate the hand-checked toy stratum via the shared kernel (proves Phase-K reuse)")
    args = ap.parse_args(argv if argv is not None else sys.argv[1:])

    if args.validate_toy:
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

    ap.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
