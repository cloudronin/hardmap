#!/usr/bin/env python3
"""Build catalog_v1.jsonl — the derived descriptor layer, assembled from frozen frames.

ONE EXTRACTOR. Every descriptor comes from `foundry.catalog.extract`; this file arranges inputs and
writes rows. It computes nothing itself — the test-of-a-copy law applied to the catalog layer.

THE RETRO-FILL. The v1 schema's `coherence` group (overlap, overlap_slope, bimodality_max) exists on the
frozen frames only for the two hardening-figure rows. Filling it retroactively is cheap and authorised by
the dial-panel amendment's retro-table item, so the catalog ships whole rather than with a hole in exactly
one group. Retro-filled cells are STAMPED — a descriptor computed after the fact on published frames is
disclosed-prior material, and the cell says so rather than the schema document saying it.

PROVENANCE PER CELL: the frame artifact and its sha256, the extractor's own sha256, `descriptor@version`.
A catalog cell that cannot say which bytes produced it is a number without a father.
"""
import hashlib
import json
import random
import sys
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "dev"))
LAT = ROOT / "foundry" / "results" / "lattice"
OUT = LAT / "catalog_v1.jsonl"
META = LAT / "catalog_v1_meta.json"
from foundry.catalog import extract as X                               # noqa: E402
import terrain_score as T                                              # noqa: E402

SEED = 20260726
EXTRACTOR_SHA = hashlib.sha256(
    (ROOT / "foundry" / "catalog" / "extract.py").read_bytes()).hexdigest()[:16]


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def v3_frames(retro):
    """The 27 built rows' frames, from the frozen survey column, with coherence retro-filled."""
    p = LAT / "sounding_v3_survey.json"
    doc = json.loads(p.read_text())
    man = {(m["row"], m["ramp_position"]): m for m in doc["ramp_manifest"]}
    by = {}
    for x in doc["readings"]:
        if not (x.get("region") and x.get("flavor")):
            if x.get("insufficient") == "GAP-no-region":
                by.setdefault((x["row"], None, None), []).append(
                    {"ramp_position": x["ramp_position"], "ramp_value": x.get("ramp_value"),
                     "state": "GAP-no-region"})
            continue
        key = (x["row"], x["region"], x["flavor"])
        step = {"ramp_position": x.get("ramp_position"), "ramp_value": x.get("ramp_value"),
                "state": "usable", "insufficient": x.get("insufficient"),
                "blend_excess": x.get("excess"), "control_sd": x.get("control_sd"),
                "r": x.get("r")}
        rk = (x["row"], x.get("ramp_position"), x["region"])
        if rk in retro:
            step["overlap_mean"] = retro[rk]["overlap_mean"]
            step["bimodality_coefficient"] = retro[rk]["bimodality_coefficient"]
            step["coherence_provenance"] = "RETRO-FILLED on published frames — disclosed-prior material"
        by.setdefault(key, []).append(step)
    return by, sha(p), "sounding_v3_survey.json"


def batch1_frames():
    p = LAT / "observatory_batch1_panels.json"
    if not p.exists():
        return {}, None, None
    doc = json.loads(p.read_text())
    by = {}
    for r in doc["rows"]:
        for s in r["steps"]:
            if s.get("state") != "usable":
                by.setdefault((r["row"], None, None), []).append(
                    {"ramp_position": s["ramp_position"], "ramp_value": s["ramp_value"],
                     "state": s["state"]})
                continue
            d = s["dials"]
            for fl, v in d["flavours"].items():
                by.setdefault((r["row"], s["region"], fl), []).append({
                    "ramp_position": s["ramp_position"], "ramp_value": s["ramp_value"],
                    "state": "usable", "insufficient": v.get("insufficient"),
                    "blend_excess": v.get("blend_excess"), "control_sd": v.get("control_sd"),
                    "r": d.get("r_mean"), "overlap_mean": d.get("overlap_mean"),
                    "bimodality_coefficient": d.get("bimodality_coefficient"),
                    "coherence_provenance": "captured at frame time"})
    return by, sha(p), "observatory_batch1_panels.json"


def retro_coherence():
    """Regenerate v3 regions and compute the coherence dials the frozen frames never carried."""
    doc = json.loads((LAT / "sounding_v3_survey.json").read_text())
    rng = random.Random(SEED)
    out = {}
    for m in doc["ramp_manifest"]:
        try:
            regions, _ = T.replay(m["row"], m["ramp_position"], m["seed"])
        except Exception:
            continue
        for kind, regs in regions.items():
            if not regs:
                continue
            ovs, bcs = [], []
            for r in regs:
                if len(r) < 2:
                    continue
                o = X.overlaps(r, rng=rng)
                if not o:
                    continue
                ovs.append(mean(o))
                b = X.bimodality_coefficient(o)
                if b is not None:
                    bcs.append(b)
            if ovs:
                out[(m["row"], m["ramp_position"], kind)] = {
                    "overlap_mean": round(mean(ovs), 4),
                    "bimodality_coefficient": round(mean(bcs), 4) if bcs else None}
        print(f"    retro {m['row']} step {m['ramp_position']}", flush=True)
    return out


def main() -> int:
    print("BUILDING catalog_v1\n\n  retro-filling coherence on the frozen v3 frames ...", flush=True)
    retro = retro_coherence()
    v3, v3sha, v3name = v3_frames(retro)
    b1, b1sha, b1name = batch1_frames()

    rows, sources = [], {}
    for src, (frames, s, name) in (("v3", (v3, v3sha, v3name)), ("batch1", (b1, b1sha, b1name))):
        if not frames:
            continue
        sources[name] = s
        for (prob, region, flavour), steps in sorted(frames.items(), key=lambda z: str(z[0])):
            if region is None:
                continue
            steps.sort(key=lambda z: z["ramp_position"])
            gaps = [g for (p2, r2, f2), gs in frames.items() if p2 == prob and r2 is None for g in gs]
            d = X.descriptors(steps + gaps)
            rows.append({"problem_id": prob, "region": region, "flavour": flavour,
                         "descriptor_version": X.VERSION,
                         "frame_artifact": name, "frame_sha256": s,
                         "extractor_sha256": EXTRACTOR_SHA,
                         "coherence_is_retro_filled": any(
                             st.get("coherence_provenance", "").startswith("RETRO") for st in steps),
                         **d})

    # rollups: per (problem, region) and per problem
    for level_keys in (("problem_id", "region"), ("problem_id",)):
        g = {}
        for r in rows:
            if r.get("_rollup"):
                continue
            g.setdefault(tuple(r[k] for k in level_keys), []).append(r)
        for key, members in g.items():
            ex = [m["level"]["excess_ref"] for m in members if m["level"]["excess_ref"] is not None]
            ov = [m["coherence"]["overlap_ref"] for m in members
                  if m["coherence"]["overlap_ref"] is not None]
            rows.append({**dict(zip(level_keys, key)), "_rollup": "region" if len(level_keys) == 2 else "row",
                         "descriptor_version": X.VERSION, "extractor_sha256": EXTRACTOR_SHA,
                         "n_members": len(members),
                         "excess_ref_median": (round(sorted(ex)[len(ex) // 2], 6) if ex else None),
                         "overlap_ref_median": (round(sorted(ov)[len(ov) // 2], 6) if ov else None),
                         "flavour_order": [m["flavour"] for m in sorted(
                             (x for x in members if x["level"]["excess_ref"] is not None),
                             key=lambda z: z["level"]["excess_ref"])],
                         "traj_class_counts": {c: sum(1 for m in members
                                                      if m["shape"]["traj_class"] == c)
                                               for c in {m["shape"]["traj_class"] for m in members}}})

    with OUT.open("w") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")
    meta = {"schema": "observatory-catalog/v1", "catalog_version": "v1.0",
            "STATUS": "EXPLORATORY — descriptors on published frames are disclosed-prior material",
            "extractor": "foundry/catalog/extract.py", "extractor_sha256": EXTRACTOR_SHA,
            "descriptor_version": X.VERSION,
            "frame_sources": sources,
            "reference_step_rule": ("median admissible ramp position — positional and therefore "
                                    "OUTCOME-BLIND; the chosen step's ramp value ships beside every "
                                    "excess_ref cell"),
            "retro_fill": ("the coherence group did not exist on the frozen v3 frames and was computed "
                           "retroactively under the dial-panel amendment. Retro-filled cells are stamped "
                           "per row, not merely noted here."),
            "seal_prohibition": ("transition descriptors (kink_step, kink_sharpness) are estimates "
                                 "WITHOUT TYPED NULLS. No seal may consume them at v1, and the "
                                 "prohibition ships inside every cell."),
            "versioning": ("F4: a changed extraction rule is a NEW catalog version, never an in-place "
                           "edit. Sealed claims quote descriptor@version forever."),
            "n_cells": sum(1 for r in rows if not r.get("_rollup")),
            "n_rollups": sum(1 for r in rows if r.get("_rollup")),
            "n_problems": len({r["problem_id"] for r in rows})}
    META.write_text(json.dumps(meta, indent=1) + "\n")

    print(f"\n  cells    : {meta['n_cells']}")
    print(f"  rollups  : {meta['n_rollups']}")
    print(f"  problems : {meta['n_problems']}")
    print(f"  retro-filled cells: {sum(1 for r in rows if r.get('coherence_is_retro_filled'))}")
    print(f"\n  extractor sha {EXTRACTOR_SHA}   catalog sha {sha(OUT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
