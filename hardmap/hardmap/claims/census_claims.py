"""Adapters for the proof-census claims: backbone growth and Jaccard plurality.

Fast tier recomputes the C3 aggregate from the committed checkpoint.jsonl (the
verified-proof records, each carrying backbone_size + median_jaccard) -- the same
per-cell mean the c3.aggregate summary uses, but without its file-writing side
effect. Full tier would resample proofs from scratch (~57 h, documented).
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

import proofcensus
from proofcensus import c3


def _records() -> list[dict]:
    ckpt = Path(proofcensus.__file__).resolve().parent / "results" / "c3" / "checkpoint.jsonl"
    return [json.loads(line) for line in ckpt.read_text(encoding="utf-8").splitlines() if line.strip()]


def _mean(xs: list) -> float | None:
    return sum(xs) / len(xs) if xs else None


def _trends() -> tuple[dict, dict]:
    """Per-(n, alpha, sampler): the list of backbone sizes and median Jaccards."""
    backbone, jaccard = defaultdict(list), defaultdict(list)
    for r in _records():
        for sampler in ("s1", "s2"):
            s = r[sampler]
            backbone[(r["n"], r["alpha"], sampler)].append(s["backbone_size"])
            if s["median_jaccard"] is not None:
                jaccard[(r["n"], r["alpha"], sampler)].append(s["median_jaccard"])
    return backbone, jaccard


def backbone() -> dict:
    """census.backbone -- S2 mean backbone at n=60: ~1 (over-constrained) to ~273 (near threshold)."""
    bb, _ = _trends()
    s2 = [_mean(bb[(60, a, "s2")]) for a in c3.ALPHAS]
    return {"backbone_n60_near_threshold": s2[0], "backbone_n60_over_constrained": s2[-1]}


def plurality() -> dict:
    """census.plurality -- median-Jaccard band across the sweep, vs the 0.95 no-plurality line."""
    _, jac = _trends()
    means = [m for m in (_mean(v) for v in jac.values()) if m is not None]
    hi = max(means)
    return {"jaccard_min": min(means), "jaccard_max": hi, "below_plurality_line": bool(hi < 0.95)}
