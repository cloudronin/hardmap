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

    # ── the second sitting, 2026-07-27 ──────────────────────────────────────────────────────────────
    M.emit(TRAIL, "erratum", key="erratum:helm-spec-kill-1",
           artifact="helm-v1-wave-engine-spec.md", field="§9 Kill 1 trigger",
           old="if the first two waves' slates are dominated by untestable candidates",
           new=("if two waves produce empty slates ON DISTINCT FRONTIER STATES — the independence "
                "condition, without which one frontier observed twice reads as two failures"),
           why=("waves 1 and 2 both slated nothing, which met the trigger as written. But wave 2 "
                "re-swept the SAME database under amended screens; no new ground entered between them, "
                "so the two empty slates are one frontier state observed twice. Kill 1 exists to detect "
                "questions the frontier can NEVER adjudicate; a frontier 2 rows old that grows by "
                "construction, with every held candidate carrying the n that revives it, is the "
                "opposite of that condition."),
           encoded_so="the next operator does not need the reasoning to get it right",
           authority="owner ratification of the recorded non-fire, 2026-07-27")
    print("  erratum   Helm Kill 1 — trigger requires DISTINCT frontier states")

    M.emit(TRAIL, "version", key="version:contrast-dial-typing",
           model="reach-census capture vocabulary",
           adds="CONTRAST-DIAL, a third capture mode beside RAMPED and point capture",
           rule=("a family dial that passes the pilot's movement check but FAILS leave-one-out — its "
                 "excursion carried by a single step — is a threshold, not a ramp. The row enters as a "
                 "declared two-level factor: full panels at each level, trajectory descriptors reading "
                 "`n.a.-contrast`, and between-level deltas in their place. Sweeps treat it as a "
                 "factor, never a trajectory."),
           why=("MCSP landed in a case the ruling did not have: neither a working graded dial nor an "
                "absent one. Minting the typing is cheaper than forcing the row into either, and the "
                "seam it names is a finding rather than a failure."),
           authority="owner ruling, 2026-07-27")
    print("  version   CONTRAST-DIAL — third capture mode minted")

    M.emit(TRAIL, "erratum", key="erratum:mcsp-capture-typing",
           artifact="observatory_reach_census.json", problem="minimum-common-string-partition",
           field="capture", old="RAMPED", new="CONTRAST-DIAL",
           levels=["|Sigma| = 2", "|Sigma| = 6 (median of the >=3 levels the pilot measured)"],
           representative_rule=("the median of the measured >=3 levels, chosen by the same positional "
                                "rule the catalog uses for its reference step — reused, not invented"),
           evidence="mcsp_ramp_pilot.json: 685 at |Sigma|=2 against 306/407/310/386 across 3..8",
           trajectory_descriptors="n.a.-contrast",
           authority="owner ruling, 2026-07-27")
    print("  erratum   MCSP capture RAMPED -> CONTRAST-DIAL, levels |Sigma| in {2, 6}")

    M.emit(TRAIL, "version", key="version:structurally-flat-narrowed-v3",
           model="catalog descriptor `structure` group, descriptor@v2 -> descriptor@v3",
           old_rule="structurally_flat iff declared fixed_cardinality on the feasible region",
           new_rule=("...AND the frames show the region size unchanged across every admissible step"),
           why=("the v2 rule was too broad. It assumed a fixed-cardinality feasible region is the whole "
                "k-uniform slice, which holds for k-center and max-coverage but not for 3sum — whose "
                "region is the size-3 subsets SUMMING TO ZERO. Every member shares a cardinality, so "
                "the row declares fixed_cardinality honestly and passes conformance, yet which members "
                "qualify is entirely instance-dependent. Under v2 that row would have been flagged flat "
                "and dropped from Helm's swept population: a real trajectory excluded for resembling a "
                "definitional one."),
           caught_by="batch 4's roster, before 3sum was built",
           preserved_as="declared_flat_but_moves — the disagreement is surfaced, not resolved quietly",
           law="F4 — a changed extraction rule is a NEW version even when it corrects an error",
           authority="build-time correction, 2026-07-27")
    print("  version   structurally_flat NARROWED at v3 — declaration alone under-determines it")

    print(f"\n  {len(M.read(TRAIL))} maptrail record(s); "
          f"{sum(1 for r in M.read(TRAIL) if not r['reconstructed'])} emitted at event time")
    return 0


if __name__ == "__main__":
    sys.exit(main())
