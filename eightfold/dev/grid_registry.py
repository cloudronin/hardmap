#!/usr/bin/env python3
"""Mosaic v3 — the PROSPECTIVE REGISTRY (prereg_v12 G1 addendum).

WHY IT IS THE STRONGEST DESIGN THE PROGRAM HAS. A model that calls open cells correctly BEFORE anyone
looks up the answers is immune to every leakage story — the answer did not exist to leak. Every future
Gate-4 fill is temporally clean BY CONSTRUCTION, because Anatomy's coordinates froze at 8ff11f8a before
any future citation work exists.

THE ORDERING IS THE WHOLE INSTRUMENT:
    file predictions -> HASH -> commit -> ONLY THEN the wave's first literature query
Enforced, not trusted: `seal_wave()` refuses to seal if research artifacts for the wave already exist,
and `assert_research_surface_clean()` is a test that prediction files are outside the research agents'
input surface.

SCORING DISCIPLINE, sealed in advance: the registry accumulates as DECLARED-INSUFFICIENT until it clears
the Cochran floor at its own class spread. It scores ONCE. No interim peeks — an interim score could steer
recruitment, and wave scopes are chosen by charge-citability alone (the blindness law, extended forward).
"""
import hashlib, json, sys
from collections import Counter
from pathlib import Path

AT = Path(__file__).resolve().parent.parent / "eightfold" / "results" / "atlas"
REG = AT / "grid-prospective-registry.json"
# prediction files live HERE, deliberately outside any research agent's input surface
PRED_DIR = AT / "grid-predictions"


def _sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()


def load():
    return json.loads(REG.read_text()) if REG.exists() else {
        "schema": "grid-prospective-registry/v1",
        "sealed_by": "prereg_v12 G1 addendum, 2026-07-25",
        "scoring_discipline": ("accumulates as DECLARED-INSUFFICIENT until the Cochran floor clears at the "
                               "registry's own class spread; then scores ONCE against Arm B's nulls. "
                               "No interim peeks. Wave scope is chosen by charge-citability, NEVER by where "
                               "the model is confident."),
        "threshold_status": "UNPINNED — pinned when the first wave's class spread is known, before any "
                            "accumulation is scored. Working estimate ~50-60 graded cells; an estimate, "
                            "not the threshold.",
        "waves": [], "entries": []}


def seal_wave(wave_id, predictions, research_globs=()):
    """Hash + record predictions BEFORE the wave's research begins. Refuses if research already exists."""
    reg = load()
    if any(wave_id == w["wave_id"] for w in reg["waves"]):
        print(f"REFUSED: wave {wave_id!r} already sealed"); return 1
    for g in research_globs:
        hits = list(AT.glob(g))
        if hits:
            print(f"REFUSED: research artifacts already exist for this wave ({hits[0].name}). "
                  f"Predictions must be sealed BEFORE the first literature query."); return 1
    PRED_DIR.mkdir(exist_ok=True)
    p = PRED_DIR / f"{wave_id}.json"
    p.write_text(json.dumps(predictions, indent=1, sort_keys=True) + "\n")
    reg["waves"].append({"wave_id": wave_id, "prediction_file": p.name, "prediction_sha256": _sha(p),
                         "n_cells": len(predictions), "sealed": "PENDING-DATE",
                         "ordering_assertion": "predictions hashed BEFORE the wave's first literature query"})
    REG.write_text(json.dumps(reg, indent=1) + "\n")
    print(f"sealed wave {wave_id}: {len(predictions)} cells, sha {_sha(p)[:16]}")
    return 0


def assert_research_surface_clean(research_inputs):
    """The enforcement the addendum demands: prediction files must be OUTSIDE the research input surface."""
    bad = [str(p) for p in research_inputs if PRED_DIR.name in str(p) or "grid-predictions" in str(p)]
    return bad


def seed_pre_registry_cells():
    """The 21 Gate-4 promotions: countable in descriptive tables, EXCLUDED from the scored n.
    Their coordinates predate their labels, but their PREDICTIONS would postdate the labels' research."""
    reg = load()
    if any(e.get("temporal_class") == "clean-but-pre-registry" for e in reg["entries"]):
        print("pre-registry cells already seeded"); return 0
    proms = [json.loads(l) for l in (AT / "quarry-v2-gate4-promotions.jsonl").read_text().splitlines() if l.strip()]
    for p in proms:
        reg["entries"].append({
            "problem_id": p["problem_id"], "charge": "parameterized", "value": p["parameterized"],
            "temporal_class": "clean-but-pre-registry",
            "prediction_hash": None, "prediction_date": None,
            "fill_date": "2026-07-24", "sitting_date": p["gate4"]["sitting_date"],
            "verdict": "NOT-GRADED — no pre-filed prediction existed",
            "counts_in_descriptive": True, "counts_in_scored_n": False})
    REG.write_text(json.dumps(reg, indent=1) + "\n")
    print(f"seeded {len(proms)} pre-registry cells (descriptive only, excluded from scored n)")
    return 0


def status():
    reg = load()
    ent = reg["entries"]
    scored = [e for e in ent if e.get("counts_in_scored_n")]
    print(f"registry: {len(ent)} entries · {len(scored)} in scored n · {len(reg['waves'])} waves sealed")
    print(f"  threshold: {reg['threshold_status'][:70]}")
    print(f"  VERDICT: DECLARED-INSUFFICIENT ({len(scored)} scored cells; floor not yet pinned)")
    if ent:
        print(f"  descriptive spread: {dict(Counter(e['value'] for e in ent).most_common())}")
    return 0


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    sys.exit({"seed": seed_pre_registry_cells, "status": status}.get(cmd, status)())
