"""C3 — full parallel sweep + H1–H3 verdict (spec §4 C3). RESUMABLE.

Sweeps all cells (n∈{20,30,40,60} × α∈{4.5,5,6,8,10}), 50 instances/cell, K=200 verified refutations per
sampler per instance. Each completed instance appends a compact record to ``results/c3/checkpoint.jsonl`` and
overwrites ``results/c3/progress.json`` — so an interrupted run resumes by skipping instances already in the
checkpoint. A shared process pool is reused across the whole sweep.

R2 fallback: at the hard n=60 cells (α∈{4.5,5.0}) S2 runs under a bounded attempt cap; if it can't reach K it
is marked ``covered=false`` and the coverage asymmetry is recorded (never silently dropped). Aggregation
(``aggregate``) reads the checkpoint, so it can be re-run independently of the sampling.
"""
from __future__ import annotations

import json
import os
import time
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures.process import BrokenProcessPool
from pathlib import Path

import numpy as np

from desertmap import fixtures
from proofcensus import metrics
from proofcensus.sweep import sample_k_parallel

def _env_tuple(name, default, cast):
    v = os.environ.get(name)
    return tuple(cast(x) for x in v.split(",")) if v else default


# Grid (env-overridable for smoke tests: PC_C3_SIZES, PC_C3_ALPHAS, PC_C3_INSTANCES, PC_C3_K, PC_C3_OUT).
SIZES = _env_tuple("PC_C3_SIZES", (20, 30, 40, 60), int)
ALPHAS = _env_tuple("PC_C3_ALPHAS", (4.5, 5.0, 6.0, 8.0, 10.0), float)
HARD_ALPHAS = {4.5, 5.0}
N_INSTANCES = int(os.environ.get("PC_C3_INSTANCES", "50"))
K = int(os.environ.get("PC_C3_K", "200"))
S2_NODE_BUDGET = int(os.environ.get("PC_C3_S2_BUDGET", "200000"))

OUT = Path(os.environ.get("PC_C3_OUT", str(Path(__file__).parent / "results" / "c3")))
CKPT = OUT / "checkpoint.jsonl"
PROG = OUT / "progress.json"


def _done_keys() -> set:
    keys = set()
    if CKPT.exists():
        for line in CKPT.read_text().splitlines():
            if line.strip():
                r = json.loads(line)
                keys.add((r["n"], r["alpha"], r["inst"]))
    return keys


def _pq_hist(qs, bins: int = 40) -> list:
    h, _ = np.histogram(qs, bins=bins, range=(-1.0, 1.0))
    return h.tolist()


def _summ(res) -> dict:
    refs = res.refutations
    return {
        "n_verified": res.n_verified, "verify_discard": res.n_verify_discard, "budget": res.n_budget_exceeded,
        "lengths": metrics.lengths(refs),
        "backbone_size": metrics.backbone_size(refs),
        "median_jaccard": metrics.median(metrics.pairwise_jaccards(refs)),
        "pq_hist": _pq_hist(metrics.overlap_qs(refs)),
    }


def _instance_record(n, alpha, inst, executor) -> dict:
    cnf = fixtures.gen_unsat_3sat(n, alpha, fixtures._cell_seed(n, alpha, inst))
    rec = {"n": n, "alpha": alpha, "inst": inst}
    r1 = sample_k_parallel(cnf, "s1", K, seed=1000 + inst, executor=executor)
    rec["s1"] = _summ(r1)
    if n == 60 and alpha in HARD_ALPHAS:                       # R2 bounded fallback
        r2 = sample_k_parallel(cnf, "s2", K, seed=1000 + inst, node_budget=S2_NODE_BUDGET,
                               max_attempts=2 * K, executor=executor)
        covered = r2.n_verified >= K
    else:
        r2 = sample_k_parallel(cnf, "s2", K, seed=1000 + inst, node_budget=S2_NODE_BUDGET, executor=executor)
        covered = True
    rec["s2"] = _summ(r2)
    rec["s2"]["covered"] = covered
    if r1.refutations and r2.refutations:
        rec["province"] = {k: round(v, 4) for k, v in
                           metrics.province_separation(r1.refutations, r2.refutations).items()}
    return rec


def main(now: float | None = None) -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    now = now if now is not None else time.time()
    tasks = [(n, a, i) for n in SIZES for a in ALPHAS for i in range(N_INSTANCES)]
    done = _done_keys()
    todo = [t for t in tasks if t not in done]
    total = len(tasks)
    start = time.time()
    print(f"C3 sweep start: {len(todo)}/{total} instances to do ({len(done)} already in checkpoint)", flush=True)

    n_workers = max(1, (os.cpu_count() or 2) - 1)
    ex = ProcessPoolExecutor(max_workers=n_workers)
    try:
        with open(CKPT, "a") as ck:
            for idx, (n, a, i) in enumerate(todo):
                t0 = time.time()
                # Self-heal against BrokenProcessPool (a worker OOM-killed abruptly kills the pool): recreate
                # the executor and retry the instance a few times; skip (uncheckpointed → retried next resume)
                # if it keeps breaking.
                rec = None
                for attempt in range(4):
                    try:
                        rec = _instance_record(n, a, i, ex)
                        break
                    except BrokenProcessPool:
                        print(f"WARN: pool broke on n={n} a={a} inst={i}; recreating executor "
                              f"(attempt {attempt + 1}/4)", flush=True)
                        try:
                            ex.shutdown(wait=False, cancel_futures=True)
                        except Exception:
                            pass
                        ex = ProcessPoolExecutor(max_workers=n_workers)
                if rec is None:
                    print(f"ERROR: n={n} a={a} inst={i} failed after 4 pool recreations; skipping "
                          f"(will retry on next resume)", flush=True)
                    continue
                rec["elapsed_s"] = round(time.time() - t0, 1)
                ck.write(json.dumps(rec) + "\n"); ck.flush()
                ndone = len(done) + idx + 1
                elapsed = time.time() - start
                rate = elapsed / (idx + 1)
                eta = rate * (len(todo) - idx - 1)
                PROG.write_text(json.dumps({
                    "done": ndone, "total": total, "current": f"n={n} a={a} inst={i}",
                    "elapsed_s": round(elapsed), "eta_s": round(eta), "updated": time.time(), "started": start,
                    "workers": n_workers, "last_instance_s": rec["elapsed_s"],
                    "s2_uncovered": rec["s2"].get("covered") is False,
                }))
                print(f"[{ndone}/{total}] n={n} a={a} inst={i}: "
                      f"s1={rec['s1']['n_verified']} s2={rec['s2']['n_verified']}"
                      f"{' (S2 UNCOVERED)' if rec['s2'].get('covered') is False else ''} "
                      f"{rec['elapsed_s']}s  eta={eta/3600:.1f}h", flush=True)
    finally:
        ex.shutdown(wait=False, cancel_futures=True)

    aggregate()
    print("C3 COMPLETE", flush=True)
    return 0


def aggregate() -> dict:
    """Aggregate the checkpoint into per-cell stats, per-n trends across α with S1/S2 trend agreement, and an
    H1–H3 verdict. Re-runnable independently of sampling."""
    records = [json.loads(l) for l in CKPT.read_text().splitlines() if l.strip()] if CKPT.exists() else []
    cells: dict = {}
    for r in records:
        for sampler in ("s1", "s2"):
            d = cells.setdefault((r["n"], r["alpha"], sampler),
                                 {"lengths": [], "backbone": [], "jac": [], "pq": None, "cov": 0, "tot": 0})
            s = r[sampler]
            d["lengths"] += s["lengths"]
            d["backbone"].append(s["backbone_size"])
            if s["median_jaccard"] is not None:
                d["jac"].append(s["median_jaccard"])
            d["pq"] = np.array(s["pq_hist"]) if d["pq"] is None else d["pq"] + np.array(s["pq_hist"])
            d["tot"] += 1
            # An instance is "covered" iff it reached the full K verified. For S2 the explicit flag also
            # applies (bounded-attempt fallback); for S1 the max_attempts ceiling is the analogous cap.
            covered = s["n_verified"] >= K and s.get("covered", True)
            d["cov"] += 1 if covered else 0

    def cell_stat(n, a, sampler, key, agg):
        d = cells.get((n, a, sampler))
        return agg(d[key]) if d and d[key] else None

    summary = {"grid": {"sizes": list(SIZES), "alphas": list(ALPHAS), "n_instances": N_INSTANCES, "K": K},
               "n_records": len(records), "trends": {}, "coverage": {}}
    mean = lambda xs: sum(xs) / len(xs) if xs else None
    for n in SIZES:
        for label, key, agg in [("median_length", "lengths", metrics.median),
                                ("mean_backbone", "backbone", mean),
                                ("mean_jaccard", "jac", mean)]:
            sa = [cell_stat(n, a, "s1", key, agg) for a in ALPHAS]
            sb = [cell_stat(n, a, "s2", key, agg) for a in ALPHAS]
            if all(x is not None for x in sa + sb):
                ag = metrics.sampler_agreement_trend(list(ALPHAS), sa, sb)
                summary["trends"].setdefault(f"n{n}", {})[label] = {
                    "s1": [round(x, 3) for x in sa], "s2": [round(x, 3) for x in sb],
                    "trend_s1": ag["trend_a"], "trend_s2": ag["trend_b"], "agree": ag["agree"]}
        for a in ALPHAS:
            for sampler in ("s1", "s2"):
                d = cells.get((n, a, sampler))
                if d and d["cov"] < d["tot"]:
                    cap = "max-attempts cap" if sampler == "s1" else "R2 node-budget fallback"
                    summary["coverage"][f"n{n}_a{a}_{sampler}"] = \
                        f"{sampler.upper()} fully covered {d['cov']}/{d['tot']} instances ({cap})"
    (OUT / "c3_summary.json").write_text(json.dumps(summary, indent=2))
    return summary


def status() -> int:
    """Print a one-line status from progress.json. Exit 42 when complete, 0 while running, 1 if not started."""
    if not PROG.exists():
        print("C3 status: not started yet (no progress.json)")
        return 1
    p = json.loads(PROG.read_text())
    complete = p["done"] >= p["total"]
    stale_s = time.time() - p.get("updated", 0)
    tag = " | S2 UNCOVERED cells so far" if p.get("s2_uncovered") else ""
    # n=60 near-threshold instances can legitimately run 50+ min (S1 near its max-attempts cap), so the
    # stall threshold must exceed the worst single-instance time to avoid false alarms.
    stalled = not complete and stale_s > 6000          # >100 min with no completed instance ⇒ likely dead
    if stalled:
        tag += f" | ⚠ STALLED (no progress in {stale_s/60:.0f} min)"
    print(f"C3 status: {p['done']}/{p['total']} instances | cell {p['current']} | "
          f"elapsed {p['elapsed_s']/3600:.1f}h | eta {p['eta_s']/3600:.1f}h | "
          f"last {p['last_instance_s']:.0f}s | {p['workers']} workers{tag}")
    return 42 if complete else (43 if stalled else 0)


if __name__ == "__main__":
    import sys
    cmd = sys.argv[1] if len(sys.argv) > 1 else "run"
    if cmd == "aggregate":
        print(json.dumps(aggregate(), indent=2))
    elif cmd == "status":
        raise SystemExit(status())
    else:
        raise SystemExit(main())
