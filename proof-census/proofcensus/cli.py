"""proof-census CLI — sample refutations of a cell and report population stats (smoke / manual runs)."""
from __future__ import annotations

import argparse


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="proofcensus")
    sub = ap.add_subparsers(dest="cmd")
    sp = sub.add_parser("sample", help="sample K verified refutations of one (n, α) cell")
    sp.add_argument("--n", type=int, default=20)
    sp.add_argument("--alpha", type=float, default=4.5)
    sp.add_argument("--sampler", choices=["s1", "s2"], default="s1")
    sp.add_argument("--k", type=int, default=20)
    sp.add_argument("--seed", type=int, default=0)
    sp.add_argument("--instance-idx", type=int, default=0, help="which instance in the cell")
    args = ap.parse_args(argv)

    if args.cmd != "sample":
        ap.print_help()
        return 0

    from desertmap import fixtures
    from proofcensus import metrics
    from proofcensus.sample import sample_k

    cnf = fixtures.gen_unsat_3sat(args.n, args.alpha, fixtures._cell_seed(args.n, args.alpha, args.instance_idx))
    res = sample_k(cnf, args.sampler, args.k, seed=args.seed)
    lens = metrics.lengths(res.refutations)
    js = metrics.pairwise_jaccards(res.refutations)
    print(f"cell n={args.n} α={args.alpha} sampler={args.sampler} | instance clauses={cnf.n_clauses}")
    print(f"  verified={res.n_verified}/{args.k}  attempts={res.n_attempts}  "
          f"verify-discard={res.n_verify_discard}  budget-exceeded={res.n_budget_exceeded}")
    if lens:
        lens_s = sorted(lens)
        print(f"  length  min/median/max = {lens_s[0]}/{lens_s[len(lens_s)//2]}/{lens_s[-1]}")
        print(f"  backbone(≥0.95) size   = {metrics.backbone_size(res.refutations)}")
        print(f"  median pairwise Jaccard= {metrics.median(js):.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
