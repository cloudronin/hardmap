"""Versioned instance fixtures (M1; torch-free).

The fixture set is defined *deterministically*: every instance regenerates byte-identically from
``(n, alpha, seed)`` via numpy's default_rng, so the committed, versioned artifact is a compact **manifest
of content hashes** (not 1000 large CNF files) — matching the monorepo "regenerable outputs, committed
receipts" philosophy. Reproducibility check = regenerate + compare hashes to the manifest.

Cells (spec §3.1): sizes n∈{20,30,40,60} × densities α∈{4.5,5.0,6.0,8.0,10.0}, 50 unsat instances each.
Plus the SAT negative-control set (A1, spec §3.5) and planted E0 controls.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from desertmap import instance
from desertmap.instance import CNF

FIXTURES_VERSION = "v1"

SIZES = (20, 30, 40, 60)
ALPHAS = (4.5, 5.0, 6.0, 8.0, 10.0)
INSTANCES_PER_CELL = 50

# SAT negative control (A1): satisfiable instances well below threshold (α ≈ 3.0 ⇒ sat w.h.p.).
SAT_CTRL_N = 20
SAT_CTRL_ALPHA = 3.0
SAT_CTRL_COUNT = 10

# Planted E0 controls (spec §4 E0: 3 sizes × planted).
PLANTED_SIZES = (20, 30, 40)
PLANTED_K = 5

# Hard negatives (C2, spec §3.5): "no short proof exists" cells the relaxation is expected to FAIL.
PHP_HOLES = (3, 4)                 # PHP^{h+1}_h ; holes=4 → 20 vars
TSEITIN_VERTS = (8, 10)           # random 3-regular Tseitin, odd charge

_FIXDIR = Path(__file__).parent / "fixtures"


def _cell_seed(n: int, alpha: float, idx: int) -> int:
    """Deterministic per-instance base seed from (n, alpha, idx). Stable across runs/machines."""
    return (n * 1_000_003 + int(round(alpha * 10)) * 10_007 + idx) & 0x7FFFFFFF


def gen_unsat_3sat(n: int, alpha: float, seed: int, max_tries: int = 500) -> CNF:
    """Return an UNSAT random 3-SAT instance, resampling the seed until unsat (above threshold ⇒ few tries).

    Deterministic: uses seed, seed+A, seed+2A, … until :func:`instance.is_sat` is False.
    """
    stride = 7_919
    for t in range(max_tries):
        cnf = instance.gen_3sat(n, alpha, seed + t * stride)
        if not instance.is_sat(cnf):
            return cnf
    raise RuntimeError(f"no unsat draw for n={n}, alpha={alpha} in {max_tries} tries (alpha below threshold?)")


def gen_sat_3sat(n: int, alpha: float, seed: int, max_tries: int = 500) -> CNF:
    """Return a SATISFIABLE random 3-SAT instance (for the negative control), resampling until sat."""
    stride = 7_919
    for t in range(max_tries):
        cnf = instance.gen_3sat(n, alpha, seed + t * stride)
        if instance.is_sat(cnf):
            return cnf
    raise RuntimeError(f"no sat draw for n={n}, alpha={alpha} in {max_tries} tries")


def iter_unsat_cell(n: int, alpha: float, count: int = INSTANCES_PER_CELL):
    """Yield ``count`` deterministic unsat instances for cell (n, alpha)."""
    for idx in range(count):
        yield gen_unsat_3sat(n, alpha, _cell_seed(n, alpha, idx))


def iter_sat_control(count: int = SAT_CTRL_COUNT):
    """Yield ``count`` deterministic SATISFIABLE instances (A1 negative control)."""
    for idx in range(count):
        yield gen_sat_3sat(SAT_CTRL_N, SAT_CTRL_ALPHA, _cell_seed(SAT_CTRL_N, SAT_CTRL_ALPHA, idx))


def build_manifest(instances_per_cell: int = INSTANCES_PER_CELL,
                   sat_count: int = SAT_CTRL_COUNT) -> dict:
    """Build the versioned fixture manifest: content hashes for every cell + the SAT control + planted E0.

    This is the committable artifact. NOTE: iterating the full unsat grid solves SAT for
    len(SIZES)*len(ALPHAS)*instances_per_cell instances — pass a small ``instances_per_cell`` for a quick
    manifest; the full 50/cell manifest is built once for the sweep.
    """
    manifest: dict = {"version": FIXTURES_VERSION, "cells": {}, "sat_control": [], "planted": []}
    for n in SIZES:
        for alpha in ALPHAS:
            hashes = [c.content_hash() for c in iter_unsat_cell(n, alpha, instances_per_cell)]
            manifest["cells"][f"n{n}_a{alpha}"] = {
                "n": n, "alpha": alpha, "count": len(hashes), "hashes": hashes,
            }
    manifest["sat_control"] = [c.content_hash() for c in iter_sat_control(sat_count)]
    for n in PLANTED_SIZES:
        cnf, proof = instance.gen_planted(n=n, k=PLANTED_K, seed=_cell_seed(n, 0.0, 0))
        manifest["planted"].append({"n": n, "k": PLANTED_K, "steps": len(proof),
                                    "hash": cnf.content_hash()})
    manifest["hard_negatives"] = []
    for holes in PHP_HOLES:
        cnf = instance.gen_php(holes)
        manifest["hard_negatives"].append({"kind": "php", "holes": holes, "n_vars": cnf.n_vars,
                                           "expected": "no short proof — relaxation should FAIL",
                                           "hash": cnf.content_hash()})
    for nv in TSEITIN_VERTS:
        cnf = instance.gen_tseitin(n_vertices=nv, seed=_cell_seed(nv, 0.0, 1))
        manifest["hard_negatives"].append({"kind": "tseitin", "n_vertices": nv, "n_vars": cnf.n_vars,
                                           "expected": "no short proof — relaxation should FAIL",
                                           "hash": cnf.content_hash()})
    return manifest


def write_manifest(path: Path | None = None, **kw) -> Path:
    path = path or (_FIXDIR / f"manifest_{FIXTURES_VERSION}.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(build_manifest(**kw), indent=2))
    return path


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="desertmap fixtures", description="generate/verify versioned fixtures")
    ap.add_argument("--instances-per-cell", type=int, default=INSTANCES_PER_CELL)
    ap.add_argument("--sat-count", type=int, default=SAT_CTRL_COUNT)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args(argv)
    path = write_manifest(args.out, instances_per_cell=args.instances_per_cell, sat_count=args.sat_count)
    print(f"wrote fixture manifest {FIXTURES_VERSION} -> {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
