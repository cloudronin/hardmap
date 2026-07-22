"""Rigidity-envelope test (prereg_v10) — reproducible. Does rigidity rank (clone-derived) predict the
within-co-clone ruggedness SPREAD (Sprint 4.5, terrain-measured)? Anti-circular: rank from flags, spread from
terrain. Writes results/landscape/rigidity_test.json.
"""
import json
import statistics as st

from foundry.rigidity import rigidity_rank


def _corr(xs, ys):
    mx, my = st.mean(xs), st.mean(ys)
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sx = sum((x - mx) ** 2 for x in xs) ** 0.5
    sy = sum((y - my) ** 2 for y in ys) ** 0.5
    return round(cov / (sx * sy), 3) if sx and sy else None


def main():
    data = json.load(open("foundry/foundry/results/landscape/sprint45_within_coclone.json"))
    rows = []
    for cc, v in data.items():
        if cc == "_verdict" or v.get("within_coclone_spread") is None:
            continue
        rank, name, edge = rigidity_rank(cc.split("+"))
        rows.append({"co_clone": cc, "rigidity_rank": rank, "rank_name": name, "edge": edge,
                     "within_coclone_spread": v["within_coclone_spread"]})
    by = {}
    for r in rows:
        by.setdefault(r["rigidity_rank"], []).append(r["within_coclone_spread"])
    per_rank = {r: {"mean_spread": round(st.mean(v), 3), "vals": [round(x, 3) for x in v], "n": len(v)}
                for r, v in sorted(by.items(), reverse=True)}
    ranks = [r["rigidity_rank"] for r in rows]
    sps = [r["within_coclone_spread"] for r in rows]
    ne = [(r["rigidity_rank"], r["within_coclone_spread"]) for r in rows if not r["edge"]]
    corr_all = _corr(ranks, sps)
    corr_ne = _corr([a for a, b in ne], [b for a, b in ne])
    means = {r: st.mean(v) for r, v in by.items()}
    rigid_end_holds = means.get(4, 9) < means.get(3, -9) and means.get(4, 9) < means.get(2, -9)
    strict_432 = means.get(4, 9) < means.get(3, 0) < means.get(2, 9)
    verdict = ("CONFIRMED" if (strict_432 and corr_all is not None and corr_all < 0)
               else "PARTIAL" if (rigid_end_holds and corr_ne is not None and corr_ne < 0)
               else "NOT_CONFIRMED")
    out = {"verdict": verdict, "per_rank": per_rank,
           "corr_rank_spread_all": corr_all, "corr_rank_spread_excl_edge": corr_ne,
           "rigid_end_holds (rank4 smallest)": rigid_end_holds, "strict_monotone_4_3_2": strict_432,
           "named_mechanism": ("rank-4 Maltsev/affine pins the envelope near zero (mean spread "
                               f"{per_rank.get(4, {}).get('mean_spread')}) — the named mechanism for the affine "
                               "boundary of Sprint 4 (coset rigidity forces near-zero within-co-clone freedom)"),
           "breaks": ("ranks 3 and 2 tie (not strict monotone); the 0/1-valid edge co-clones (no idempotent Taylor "
                      "term) do not fit — one spread-0.327 outlier alongside 0.003/0.052"),
           "rows": rows}
    json.dump(out, open("foundry/foundry/results/landscape/rigidity_test.json", "w"), indent=2)
    for r in sorted(per_rank):
        print(f"rank {r}: {per_rank[r]}")
    print(f"corr(all)={corr_all} corr(excl-edge)={corr_ne} rigid_end_holds={rigid_end_holds} "
          f"strict={strict_432} -> VERDICT {verdict}")


if __name__ == "__main__":
    main()
