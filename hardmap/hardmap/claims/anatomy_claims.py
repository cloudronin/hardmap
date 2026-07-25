"""Repro claims for the Anatomy Structure Atlas (S4).

These are the repo's FIRST artifact-hash claims: `artifact:` in the manifest has always been declarative
(never read by any code), so a hash is pinned the only way `hardmap repro` can check it — an adapter that
computes the digest and returns it as a field.
"""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

import eightfold
from eightfold import anatomy as AN


def _at() -> Path:
    return Path(eightfold.__file__).resolve().parent / "results" / "atlas"


def _rows():
    return [json.loads(l) for l in (_at() / "anatomy_v1.jsonl").read_text().splitlines() if l.strip()]


def artifact_sha256() -> dict:
    """The frozen artifact's bytes and shape."""
    p = _at() / "anatomy_v1.jsonl"
    rows = _rows()
    return {"sha256": hashlib.sha256(p.read_bytes()).hexdigest(), "n_rows": len(rows),
            "n_natural": sum(1 for r in rows if r["universe"] == AN.NATURAL),
            "n_boolean": sum(1 for r in rows if r["universe"] == AN.BOOLEAN)}


def passport_verdicts() -> dict:
    """The audit's headline: how many columns can carry a sealed bet, and how many cannot."""
    doc = json.loads((_at() / "anatomy-passports.json").read_text())
    adm = [c for c in AN.COLUMNS if AN.passport_admissible(c, doc)[0]]
    coll = [c for c, p in doc["columns"].items() if p.get("admissible_collapse")]
    inv = Counter(p["invariance"] for p in doc["columns"].values())
    return {"n_columns": len(AN.COLUMNS), "n_admissible": len(adm), "n_with_collapse": len(coll),
            "n_invariant": inv[AN.INVARIANT], "n_encoding_relative": inv[AN.ENCODING_RELATIVE]}


def instrument_kappa() -> dict:
    """The coded instrument's qualification record, extracted from stdout at S1 and pinned here."""
    m = json.loads((_at() / "anatomy-instruments.json").read_text())["instruments"]["mosaic-3class-v1"]
    lad = m["resolution_ladder"]
    return {"kappa_3class": lad["3-class"]["cohen_kappa"],
            "demonstrated_resolution": m["demonstrated_resolution"],
            "anchors_pass": m["anchors_pass"],
            "separability_fires": m["separability_gate"]["charge_reconstruction_fires"]}


def decomposition_coverage() -> dict:
    """Kill 2 (coverage) and the usability census that coverage alone would have hidden."""
    cells = [c for r in _rows() for c in r["features"] if c["feature"] == "decomposition_facts"]
    filled = [c for c in cells if isinstance(c["value"], dict)]
    planar = [c["value"]["planar_restriction"] for c in filled
              if c["value"].get("planar_restriction") is not None]
    return {"n_eligible": len(cells), "n_filled": len(filled),
            "coverage": round(len(filled) / len(cells), 3) if cells else 0.0,
            "planar_modal_share": round(sum(1 for p in planar if p) / len(planar), 3) if planar else None}
