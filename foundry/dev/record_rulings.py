#!/usr/bin/env python3
"""Record the owner rulings of 2026-07-27 into the maptrail, at the moment they are recorded.

WHY THIS IS NOT A REPORTING PASS. Helm Kill 3 forbids trail events assembled after the fact from what
someone remembers. A ruling is an owner act, and writing it down IS the operation that performs it —
there is no earlier moment at which these records could have been emitted. So they carry
`reconstructed: false` honestly, unlike the program's pre-trail history, which the backfill labels.

The string-family ramp erratum is NOT emitted here: it belongs to `mcsp_ramp_pilot.py`, the operation
that actually performed the amendment and measured whether the row survived it.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from foundry.catalog import maptrail as M                                       # noqa: E402
from foundry.helm import sweep as SW                                            # noqa: E402
from foundry.helm import screens as S                                           # noqa: E402

TRAIL = ROOT / "foundry" / "results" / "lattice" / "maptrail.jsonl"


def main() -> int:
    print("RECORDING RULINGS — 2026-07-27\n")

    M.emit(TRAIL, "erratum", key="erratum:helm-spec-section-5",
           artifact="helm-v1-wave-engine-spec.md", field="§5 frontier reservation",
           old="reserved rows are captured last in the batch and withheld until predictions are hashed",
           new=("reserved rows are DECLARED AT BATCH CENSUS and captured only after all open "
                "predictions against them are hashed"),
           why=("§5 as written and §0.1 differed in strength: under §5 the frames exist and blindness "
                "rests on a guard; under §0.1 — the binding constitution — the frames do not exist and "
                "blindness is physics. When a binding clause and a procedural clause disagree, the "
                "irreversible reading of the binding one governs. The asymmetry settles it "
                "independently: declare-then-capture-later can always be relaxed, capture-now can "
                "never be taken back."),
           authority="owner ratification, 2026-07-27")
    print("  erratum   Helm §5 — reserved rows declared, not captured")

    M.emit(TRAIL, "version", key=f"version:{SW.EXTREMAL_NULL_VERSION}",
           model=SW.EXTREMAL_NULL_VERSION,
           applies_to="anomaly candidates (descriptor extremals, residual zeros, fingerprint outliers)",
           strata=["family", "region-kind", "flavour"],
           matching_covariate="r-band, where supply allows",
           floor_cells=S.MIN_STRATUM_CELLS,
           floor_derivation=("a one-sided permutation test over m cells attains no p below 1/(m+1); "
                             "19 is where p = 0.05 becomes attainable at all, 20 the first size with "
                             "anything to spare"),
           below_floor="INSUFFICIENT — speech ruled inadmissible, not silence",
           why_stratified=("each axis is a paid-for lesson: family per Terroir's verdict, region-kind "
                           "per Q5's contrast instability, flavour per the fingerprint structure, and "
                           "r-conditioning as the sixth-species vaccine. Exchangeability across UNLIKE "
                           "strata is the assumption this program has disproven three times."),
           unblocks="the 22 anomaly candidates held at wave 1 for want of a typed frontier null",
           authority="owner ruling, 2026-07-27")
    print(f"  version   {SW.EXTREMAL_NULL_VERSION} — pinned, floor {S.MIN_STRATUM_CELLS} cells")

    M.emit(TRAIL, "version", key="version:structurally-flat-flag",
           model="catalog descriptor `structure` group, at descriptor@v2",
           adds=["structurally_flat", "region_size_invariant"],
           rule=("structurally_flat iff the row declares fixed_cardinality and this is its feasible "
                 "region — that region is every size-k subset, identical at every ramp value"),
           consequence=("structurally-flat cells are excluded from Helm's swept population via the "
                        "`sweepable_catalog` view, and a backstop screen rule rejects any that reach "
                        "candidacy by another path"),
           why=("their flatness is a property of the row's definition, not a measurement. A sweep that "
                "enumerates them correlates a constant with things, or reports a definition back as a "
                "discovery."),
           authority="owner addition, 2026-07-27")
    print("  version   structurally_flat — descriptor@v2, sweep exclusion + backstop screen")

    print(f"\n  {len(M.read(TRAIL))} maptrail record(s); "
          f"{sum(1 for r in M.read(TRAIL) if not r['reconstructed'])} emitted at event time")
    return 0


if __name__ == "__main__":
    sys.exit(main())
