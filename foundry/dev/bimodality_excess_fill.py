#!/usr/bin/env python3
"""Compute `bimodality_excess` — BC against the matched-r control null (declared 2026-07-27).

RULE BEFORE COMPUTATION. The descriptor was DECLARED in the maptrail before any value existed, with its
definition fixed: for a region of size r, draw control regions of the SAME r from the same ambient,
compute BC on each control's overlap distribution, and report measured BC minus the control mean. This
script is the computation that declaration authorised; it invents nothing.

WHY IT WAS NEEDED. Raw `bimodality_max` is size-coupled — BC is a coefficient statistic and few overlap
samples inflate it mechanically. Wave 4's slate came back four-for-four wearing size's costumes, and
three candidates died on exactly this. The excess discipline governs every blend reading in the program
and had simply never reached the coherence descriptors.

REGIONS ARE REGENERATED, NOT STORED. `capture_row` seeds each step as `seed + 1000*pos + hash(row)`, so
the regions are reproducible from the batch modules. This is the retro-fill pattern the coherence group
already used, and the values are STAMPED as retro-filled for the same reason: a descriptor computed after
the fact on published frames is disclosed-prior material.

CACHED AGAINST THE GENERATOR SOURCES. A cache keyed on nothing is how a stale number outlives its source.
"""
import hashlib, json, random, sys
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "dev"))
LAT = ROOT / "foundry" / "results" / "lattice"
OUT = LAT / "bimodality_excess_cache.json"
from foundry.catalog import capture as C, extract as X                          # noqa: E402
import n2_dense_control as N2                                                   # noqa: E402
import observatory_ambient_census as AC                                         # noqa: E402

SEED = 20260726          # the capture seed every batch used
K_CTRL = 8               # matched-r control draws per step — declared, not tuned
N_INST = 3


def sources_sha():
    h = hashlib.sha256()
    for n in sorted(Path(ROOT / "dev").glob("observatory_batch*.py")):
        h.update(n.read_bytes())
    return h.hexdigest()


def main() -> int:
    src = sources_sha()
    if OUT.exists():
        c = json.loads(OUT.read_text())
        if c.get("source_sha256") == src:
            print("CACHE HIT — generator sources unchanged"); return 0
        print("cache MISS — generators changed, recomputing")
    print("BIMODALITY EXCESS — BC against the matched-r control null\n")

    out = {}
    for row, batch, build, ramp in AC.batch_rows():
        for pos, val in enumerate(ramp):
            srng = random.Random(SEED + 1000 * pos + abs(hash(row)) % 997)
            acc = {}
            for _ in range(N_INST):
                try:
                    built = build(srng, val) or []
                except Exception:
                    continue
                for kind, region in built:
                    if region and len(region) >= 2:
                        acc.setdefault(kind, []).append(region)
            for kind, regs in sorted(acc.items()):
                meas, ctrl = [], []
                for r in regs:
                    o = X.overlaps(r, rng=srng)
                    b = X.bimodality_coefficient(o) if o else None
                    if b is None:
                        continue
                    meas.append(b)
                    for _ in range(K_CTRL):
                        cr = N2.cp_control(r, srng)[0]          # matched r, same ambient
                        if not cr or len(cr) < 2:
                            continue
                        co = X.overlaps(cr, rng=srng)
                        cb = X.bimodality_coefficient(co) if co else None
                        if cb is not None:
                            ctrl.append(cb)
                if meas and len(ctrl) > 1:
                    out[f"{row}|{pos}|{kind}"] = {
                        "bimodality_measured": round(mean(meas), 4),
                        "bimodality_control_mean": round(mean(ctrl), 4),
                        "bimodality_excess": round(mean(meas) - mean(ctrl), 4),
                        "n_control_draws": len(ctrl)}
        print(f"  {row:<30} done", flush=True)

    OUT.write_text(json.dumps({
        "schema": "bimodality-excess-cache/v1",
        "STATUS": "RETRO-FILLED on published frames — disclosed-prior material, stamped per cell",
        "definition": ("measured BC minus the mean BC of matched-r control regions drawn from the same "
                       "ambient by the standing CP control machinery"),
        "declared_before_computed": "maptrail version:bimodality-excess-declared",
        "k_control_draws": K_CTRL, "capture_seed": SEED,
        "source_sha256": src,
        "source_note": "keyed on the batch generator sources; a cache keyed on nothing outlives them",
        "n_cells": len(out), "values": out}, indent=1) + "\n")
    ex = [v["bimodality_excess"] for v in out.values()]
    print(f"\n  {len(out)} cells   excess range [{min(ex):.3f}, {max(ex):.3f}]   "
          f"mean {mean(ex):+.4f}")
    print(f"  wrote {OUT.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
