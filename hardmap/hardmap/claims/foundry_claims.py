"""Adapters for the foundry claims: Lattice v3 V, Prism residuals, corrected direction.

These read the committed, verified oracle matrices (the frozen artifacts); the full
tier would re-run the prism/lattice dev builds (oracle enumeration, minutes).
"""
from __future__ import annotations

import json
from pathlib import Path

import foundry


def _lattice_dir() -> Path:
    return Path(foundry.__file__).resolve().parent / "results" / "lattice"


def _load(name: str) -> dict:
    return json.loads((_lattice_dir() / name).read_text(encoding="utf-8"))


def natural_v3_v() -> dict:
    """natural.v3.v -- generated-universe coupling Cramér's V + bootstrap CI (Lattice v3)."""
    d = _load("lattice_v3_occupancy.json")
    lo, hi = d["cramers_v_boot_ci95_sized_to_classes"]
    return {"v": d["cramers_v"], "ci_lo": lo, "ci_hi": hi}


def prism_residuals() -> dict:
    """natural.prism.residuals -- bridge-completed Min-Ones residual, v1 and arity-4 v2."""
    v1 = _load("prism_matrix.json")["matrix"]["approx_minones x parameterized"]["netted_bridge_completed"]
    v2 = _load("prism_v2_matrix.json")["pred5_anti_canon"]["min_ones"]["V"]
    return {"v1_minones_bridge": v1, "v2_minones_V": v2}


def direction_corrected() -> dict:
    """natural.direction.corrected -- corrected Spearman: v1 anchor + arity-4 point with CI."""
    p = _load("prism_v2_matrix.json")["pred5_anti_canon"]
    lo, hi = p["min_ones"]["boot_ci95_classes_corrected"]
    return {
        "v1_anchor": p["v1_anchor_corrected"],
        "arity4_point": p["min_ones"]["spearman_point_corrected"],
        "ci_lo": lo,
        "ci_hi": hi,
    }
