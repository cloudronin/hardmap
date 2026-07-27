#!/usr/bin/env python3
"""Record the owner rulings of 2026-07-27 into the maptrail, at the moment they are recorded.

WHY THIS IS NOT A REPORTING PASS. Helm Kill 3 forbids trail events assembled after the fact from what
someone remembers. A ruling is an owner act, and writing it down IS the operation that performs it —
there is no earlier moment at which these records could have been emitted. So they carry
`reconstructed: false` honestly, unlike the program's pre-trail history, which the backfill labels.

The string-family ramp erratum is NOT emitted here: it belongs to `mcsp_ramp_pilot.py`, the operation
that actually performed the amendment and measured whether the row survived it.
"""
import json
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

    # ── Q21, ruled in three parts ───────────────────────────────────────────────────────────────────
    cen = json.loads((ROOT / "foundry" / "results" / "lattice" /
                      "observatory_ambient_census.json").read_text())
    conf = cen["confounded"]

    M.emit(TRAIL, "version", key="version:ambient-confound-policy",
           model="catalog descriptor policy, descriptor@v3 -> descriptor@v4",
           level_descriptors="STAND — each step's excess is valid at its own (width, density)",
           voided=["shape.traj_class", "shape.slope_sign", "shape.max_excursion_sd",
                   "transition.kink_step", "transition.kink_sharpness", "coherence.overlap_slope"],
           marker="n.a.-ambient-confounded",
           why=("slope, traj_class and kink presuppose a tightening dial over a FIXED space. Where the "
                "ground set is what the dial ramps, the x-axis moves the universe too and there is no "
                "quantity left for them to estimate. A semantically confounded number does not ship "
                "with a warning; it does not ship."),
           not_the_kink_precedent=("kink values are meaningful-but-untested — a referent, no null. "
                                   "These are meaningless-as-defined."),
           overlap_slope_note=("the ruling named groups rather than fields; overlap_slope is a slope "
                               "over the same confounded axis and is voided for consistency"),
           sql_handling=("the JSONL keeps the marker so a reader learns why; the db column goes NULL so "
                         "every IS NOT NULL filter excludes it without knowing the marker exists"),
           rows_affected=conf, authority="owner ruling on Q21, 2026-07-27")
    print(f"  version   ambient-confound policy at v4 — {len(conf)} row(s) affected")

    M.emit(TRAIL, "erratum", key="erratum:graph-family-ramp-edge-subset",
           artifact="observatory_reach_census.json",
           field="family_ramp_parameters.graph.param, for EDGE-SUBSET rows only",
           old="edge density",
           new="within-instance parameter at fixed ground set — per-row parameter declared",
           per_row={"graph-spanner": "stretch factor t at fixed graph",
                    "connectivity-augmentation": "connectivity target k at fixed candidate set",
                    "cluster-deletion": "deletion budget at fixed graph"},
           why=("edge density ramps the ground set itself for these rows. The family has natural "
                "tightening dials that never touch the ambient, and they ask the hardening question "
                "the density ramp was mis-asking."),
           birth_excluded_rows={"edge-dominating-set": "stays excluded", "feedback-arc-set": "stays excluded"},
           re_entry_route=("any ambient-stable dial someone declares later falsifies the exclusion, "
                           "per the reach-typing law — an exclusion is a typing, not a verdict"),
           authority="owner ruling on Q21, 2026-07-27")
    print("  erratum   graph family ramp — edge-subset rows re-ramp at fixed ground set")

    M.emit(TRAIL, "annotation", key="annotation:confounded-frames-stand",
           what=("the frozen frames of the confounded rows are NEITHER edited NOR deleted. They are "
                 "honest per-step measurements of a confounded ramp, and they stay exactly that."),
           two_artifact_truth=("the Terrain pattern: the old measurement stands at its own scope, the "
                               "new capture answers the question the old one could not"),
           rows=conf, touches_no_measured_value=True,
           authority="owner ruling on Q21 part 3, 2026-07-27")
    print("  annot     confounded frames stand, frozen and unedited")

    queue = {"schema": "observatory-recapture-queue/v1",
             "STATUS": "WORK QUEUE — ordinary build work, no verdict attached",
             "why": ("edge-subset rows re-ramp on a within-instance parameter at fixed ground set. New "
                     "frames enter as new capture versions; the old frames are untouched."),
             "old_frames": "frozen, annotated via maptrail, never edited, never deleted",
             "rows": [{"problem_id": "graph-spanner", "new_dial": "stretch factor t at fixed graph",
                       "old_capture": "observatory_batch2_panels.json"},
                      {"problem_id": "cluster-deletion", "new_dial": "deletion budget at fixed graph",
                       "old_capture": "observatory_batch2_panels.json"},
                      {"problem_id": "maximum-planar-subgraph",
                       "new_dial": "UNDECLARED — needs a within-instance parameter; planarity has no "
                                   "obvious budget dial at fixed edge set",
                       "old_capture": "observatory_batch1_panels.json"},
                      {"problem_id": "set-cover",
                       "new_dial": "UNDECLARED — the v3 survey row ramps set count, which is its ground "
                                   "set; a fixed-universe form needs declaring",
                       "old_capture": "sounding_v3_survey.json"}],
             "note": ("two rows have no declared replacement dial yet and are listed as such rather "
                      "than given an invented one — the census's own lesson, applied to its repair")}
    (ROOT / "foundry" / "results" / "lattice" / "observatory_recapture_queue.json").write_text(
        json.dumps(queue, indent=1) + "\n")
    print(f"  queued    {len(queue['rows'])} row(s) for re-capture under corrected dials")

    M.emit(TRAIL, "erratum", key="erratum:batch5-mcsp-spurious-exclusion",
           artifact="observatory_batch5_panels.json",
           problem="minimum-common-string-partition",
           old="EXCLUDED at birth — builder raised: empty range for randrange()",
           new="captured as the first CONTRAST-DIAL row, levels |Sigma| in {2, 6}",
           why=("the exclusion was a TOOLING ARTIFACT, not a property of the row. "
                "`conformance_at_birth` hardcoded its probe at ramp value 0.30 — a density-shaped "
                "number — and MCSP's ramp is alphabet size, so the probe called randrange(0) and the "
                "pipeline recorded the ROW as failing conformance rather than the probe as wrong."),
           scope=("the same defect silently mis-probed every non-density ramp: the algebraic rows were "
                  "probed at 0.30, below their whole declared range of 1.2..3.0"),
           fix="capture_row now probes at the MEDIAN DECLARED LEVEL of the row's own ramp",
           why_not_deleted=("the exclusion record stands. It is what the run did, and the maptrail "
                            "corrects by erratum rather than by editing history — which is the only "
                            "way a reader can tell a corrected mistake from one that never happened."),
           authority="build-time correction, 2026-07-27")
    print("  erratum   batch 5 MCSP exclusion was a probe bug, corrected not deleted")

    print(f"\n  {len(M.read(TRAIL))} maptrail record(s); "
          f"{sum(1 for r in M.read(TRAIL) if not r['reconstructed'])} emitted at event time")
    return 0


if __name__ == "__main__":
    sys.exit(main())
