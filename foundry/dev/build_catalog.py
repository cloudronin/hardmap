#!/usr/bin/env python3
"""Build the derived descriptor layer from the frozen frames. The output is `catalog_<VERSION>.jsonl`,
where VERSION comes from the extractor — this file never names a version itself.

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
from foundry.catalog import extract as X                               # noqa: E402
from foundry.catalog import reservation as RES                         # noqa: E402
import terrain_score as T                                              # noqa: E402

LEDGER = LAT / "observatory_reservation.jsonl"
AMBIENT = LAT / "observatory_ambient_census.json"
READJ = LAT / "reach_subset_readjudication.json"


def encoding_variants():
    """Rows CAPTURED as subsets whose canonical_encoding names a different object (Ruling 1).

    Derived from the re-adjudication, never listed: a row is a variant iff it retyped away from
    REACH-subset AND frames exist for it. Rows that retyped but were never captured are simply
    mis-typed queue entries, not variant frames."""
    if not READJ.exists():
        print("    NO RE-ADJUDICATION — no row marked encoding-variant", flush=True)
        return set()
    d = json.loads(READJ.read_text())
    return {r["problem_id"] for r in d["rows"] if r.get("retyped") and r.get("already_built")}


def ambient_confounded_rows():
    """Read the DERIVED census. Absent census -> empty set, and the builder says so rather than
    silently treating every row as clean."""
    if not AMBIENT.exists():
        print("    NO AMBIENT CENSUS — no row will be marked confounded; run "
              "dev/observatory_ambient_census.py", flush=True)
        return set()
    d = json.loads(AMBIENT.read_text())
    return {r["problem_id"] for r in d["rows"] if r.get("ambient_confounded")}

# THE OUTPUT NAME IS DERIVED FROM THE EXTRACTOR'S VERSION, never typed here. F4 makes a changed
# extraction rule a new catalog version; if the filename were a literal, a version bump would silently
# overwrite its predecessor and the law would hold only as long as someone remembered it.
OUT = LAT / f"catalog_{X.VERSION}.jsonl"
META = LAT / f"catalog_{X.VERSION}_meta.json"

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
    # the v3 survey predates declared structural expectations, so no row here can be structurally flat
    return by, sha(p), "sounding_v3_survey.json", {}


def batch_frames(p):
    """Any observatory_batch*_panels.json. Discovery is by glob so batch N costs no edit here —
    a builder that must be edited per batch is a builder that will be forgotten at batch 4."""
    if not p.exists():
        return {}, None, None, {}
    doc = json.loads(p.read_text())
    by = {}
    expects = {r["row"]: (r.get("structural_expectation"), r.get("capture_mode", "RAMPED"))
               for r in doc["rows"]}
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
    return by, sha(p), p.name, expects


RETRO_CACHE = LAT / "catalog_retro_coherence_cache.json"


def retro_coherence():
    """Regenerate v3 regions and compute the coherence dials the frozen frames never carried.

    CACHED AGAINST THE SOURCE HASH. The computation is deterministic given the frozen frames and the
    declared seed, so recomputing it on every batch is pure waste — but a cache keyed on nothing is how
    a stale number outlives its source. The key is the survey artifact's sha256: if the frames change,
    the cache misses and the fill recomputes."""
    src = sha(LAT / "sounding_v3_survey.json")
    if RETRO_CACHE.exists():
        c = json.loads(RETRO_CACHE.read_text())
        if c.get("source_sha256") == src:
            print("    retro-fill CACHE HIT (source unchanged)", flush=True)
            return {tuple(json.loads(k)): v for k, v in c["values"].items()}
        print("    retro-fill cache MISS — source changed, recomputing", flush=True)
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
    RETRO_CACHE.write_text(json.dumps(
        {"source_artifact": "sounding_v3_survey.json", "source_sha256": src,
         "note": ("cache keyed on the source artifact's sha256 — if the frames change this misses and "
                  "the fill recomputes. A cache keyed on nothing is how a stale number outlives its "
                  "source."),
         "values": {json.dumps(list(k)): v for k, v in out.items()}}, indent=1) + "\n")
    return out


def main() -> int:
    print(f"BUILDING catalog_{X.VERSION}\n\n  retro-filling coherence on the frozen v3 frames ...", flush=True)
    confounded = ambient_confounded_rows()
    variants = encoding_variants()
    retro = retro_coherence()
    v3, v3sha, v3name, v3exp = v3_frames(retro)
    batches = [batch_frames(p) for p in sorted(LAT.glob("observatory_batch*_panels.json"))]

    rows, sources = [], {}
    for frames, s, name, expects in [(v3, v3sha, v3name, v3exp)] + batches:
        if not frames:
            continue
        sources[name] = s
        for (prob, region, flavour), steps in sorted(frames.items(), key=lambda z: str(z[0])):
            if region is None:
                continue
            steps.sort(key=lambda z: z["ramp_position"])
            gaps = [g for (p2, r2, f2), gs in frames.items() if p2 == prob and r2 is None for g in gs]
            d = X.descriptors(steps + gaps, region=region,
                              structural_expectation=(expects.get(prob) or (None, None))[0],
                              capture_mode=(expects.get(prob) or (None, "RAMPED"))[1] or "RAMPED",
                              ambient_confounded=(prob in confounded),
                              encoding_faithful=(prob not in variants))
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

    # The frontier reservation, enforced where the descriptors are actually written (Helm §5). A
    # reserved row reaching the catalog is a leak whether or not any batch script intended it.
    RES.assert_absent("catalog_v1.jsonl", [r["problem_id"] for r in rows], LEDGER)

    with OUT.open("w") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")
    meta = {"schema": f"observatory-catalog/{X.VERSION}", "catalog_version": f"{X.VERSION}.0",
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
            "v2_succession": ("v2 adds the `structure` group (`structurally_flat`, "
                              "`region_size_invariant`). No v1 descriptor changed value, but the "
                              "version bumps regardless: if `v1` sometimes carried the group and "
                              "sometimes did not, `descriptor@v1` would stop identifying a schema. "
                              "catalog_v1.jsonl is left exactly as v1 last built it and is no longer "
                              "regenerated."),
            "n_cells": sum(1 for r in rows if not r.get("_rollup")),
            "n_rollups": sum(1 for r in rows if r.get("_rollup")),
            "n_problems": len({r["problem_id"] for r in rows})}
    META.write_text(json.dumps(meta, indent=1) + "\n")

    # the succession, emitted HERE by the operation that performs it (Helm Kill 3, ported)
    from foundry.catalog import maptrail as M
    M.emit(LAT / "maptrail.jsonl", "version", key=f"version:catalog-{X.VERSION}",
           schema=meta["schema"], version=meta["catalog_version"],
           descriptor_version=X.VERSION, extractor_sha256=EXTRACTOR_SHA,
           adds="the `structure` group: structurally_flat, region_size_invariant",
           law="F4 — a changed extraction rule is a NEW version, never an in-place edit")

    nvar = sum(1 for r in rows if not r.get("_rollup") and r.get("encoding_faithful") is False)
    print(f"\n  encoding-variant   : {nvar} cell(s) across {len(variants)} row(s) — barred from "
          f"charge-joining candidates; frames stand, frozen")
    nconf = sum(1 for r in rows if not r.get("_rollup") and r.get("ambient_confounded"))
    nflat = sum(1 for r in rows if not r.get("_rollup") and r["structure"]["structurally_flat"])
    print(f"\n  ambient-confounded: {nconf} cell(s) across {len(confounded)} row(s) — shape, "
          f"transition and overlap_slope read {X.NA_AMBIENT}; level descriptors stand")
    print(f"\n  cells    : {meta['n_cells']}")
    print(f"  structurally flat: {nflat}  (excluded from Helm's sweep — flatness by definition)")
    dis = [r for r in rows if not r.get("_rollup") and r["structure"].get("declared_flat_but_moves")]
    if dis:
        print(f"  DECLARED FIXED-CARDINALITY BUT THE REGION MOVES on {len(dis)} cell(s) — instance-"
              f"dependent within a cardinality class, so NOT structurally flat:")
        for r in dis[:8]:
            print(f"     {r['problem_id']} / {r['region']} / {r['flavour']}: "
                  f"declared={r['structure']['declared_expectation']} "
                  f"flat={r['structure']['structurally_flat']} "
                  f"invariant={r['structure']['region_size_invariant']}")
    print(f"  rollups  : {meta['n_rollups']}")
    print(f"  problems : {meta['n_problems']}")
    print(f"  retro-filled cells: {sum(1 for r in rows if r.get('coherence_is_retro_filled'))}")
    print(f"\n  extractor sha {EXTRACTOR_SHA}   catalog sha {sha(OUT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
