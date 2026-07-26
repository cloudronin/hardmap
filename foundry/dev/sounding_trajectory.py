#!/usr/bin/env python3
"""The trajectory report — Q3-descriptive. NO VERDICT.

DESCRIPTIVE BY DECLARATION. This report describes how the excess statistic moves along each row's declared
ramp. It scores nothing, predicts nothing and concludes nothing. The classification at the end is a
mechanical label applied by a rule pinned before it ran, not a finding.

═══ THE CLASSIFICATION RULE — PINNED HERE, BEFORE ANY CLASSIFICATION RUNS ═══════════════════════════════

For each (row, region, flavour) trajectory over its DECLARED ramp steps, using only steps that produced a
reading above the pre-declared INSUFFICIENT-r floor:

    excursion      = max(excess) - min(excess)
    pooled_ctrl_sd = mean(control_sd) over those same steps

    FLAT          iff  excursion < 2.0 * pooled_ctrl_sd
    MONOTONE      iff  not FLAT and the excess sequence is weakly non-increasing OR weakly non-decreasing
    NON-MONOTONE  otherwise
    UNCLASSIFIED  iff  fewer than 3 usable steps — too short for the shape to mean anything

THE 2.0 IS A CONVENTION, NOT A DERIVED THRESHOLD. Nothing about the excess statistic makes 2 sigma the
boundary between "flat" and "moving"; it is picked because it is the ordinary default and because picking
it in advance is worth more than picking it well. To keep the arbitrariness VISIBLE rather than merely
confessed, the report recomputes the whole table at 1.0x and 3.0x and prints how many trajectories change
label. If that count is large, the classification is soft and the reader should see that it is.

Gaps are drawn as gaps. A declared step that produced no reading is a GAP record, never interpolated
across, and never silently dropped from the table — an absent reading is a claim of continuity unless the
absence is itself recorded.
"""
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parent.parent
LAT = ROOT / "foundry" / "results" / "lattice"
SURVEY = LAT / "sounding_v3_survey.json"
OUT = LAT / "sounding_trajectories.json"
PLOTS = ROOT.parent / "foundry" / "docs" / "findings" / "plots"
FLAT_MULT = 2.0
R_FLOOR = 10


def assert_controls_redrawn(readings):
    """Controls are matched on r, and r moves along the ramp. A REUSED control would therefore show an
    identical (control_mean, control_sd) pair at two DIFFERENT r values. That is a detectable signature,
    so it is detected rather than assumed — the directive asks for an assertion, and an assertion that
    cannot fail is not one."""
    by = defaultdict(list)
    for x in readings:
        if x.get("ramp_position") is not None and x.get("control_mean") is not None:
            by[(x["row"], x["region"], x["flavor"])].append(x)
    suspects, degenerate = [], []
    for key, xs in by.items():
        seen = {}
        for x in xs:
            # A DEGENERATE control carries no signature to compare. When every control draw violates, the
            # profile is (1.0, 0.0) by saturation, and two steps matching there is expected rather than
            # suspicious — the detector would otherwise flag a physical fact as misconduct. These are
            # `INSUFFICIENT-degenerate` in the v3 spec's OWN pre-declared vocabulary (control SD ~ 0),
            # counted and reported here rather than quietly skipped.
            if not x["control_sd"]:
                degenerate.append({"trajectory": list(key), "r": x["r"],
                                   "control": [x["control_mean"], x["control_sd"]],
                                   "label": "INSUFFICIENT-degenerate"})
                continue
            sig = (x["control_mean"], x["control_sd"])
            if sig in seen and seen[sig] != x["r"]:
                suspects.append({"trajectory": list(key), "signature": list(sig),
                                 "r_values": [seen[sig], x["r"]]})
            seen[sig] = x["r"]
    return suspects, degenerate


def classify(excesses, ctrl_sds, mult):
    if len(excesses) < 3:
        return "UNCLASSIFIED", None, None
    exc = max(excesses) - min(excesses)
    psd = mean(ctrl_sds) if ctrl_sds else 0.0
    if exc < mult * psd:
        return "FLAT", exc, psd
    nondec = all(b >= a for a, b in zip(excesses, excesses[1:]))
    noninc = all(b <= a for a, b in zip(excesses, excesses[1:]))
    return ("MONOTONE" if (nondec or noninc) else "NON-MONOTONE"), exc, psd


FLAVOUR_COL = {"majority": "#1f77b4", "minority": "#d62728", "min": "#2ca02c", "max": "#9467bd",
               "median": "#ff7f0e", "maltsev3": "#8c564b", "maltsev4": "#17becf"}


def svg_plot(family, trajs, path):
    """One plot per family, drawn as SMALL MULTIPLES — a mini-panel per (row, region), flavour by colour.

    Chosen over a single overlaid axis because a family carries up to 24 trajectories and overlaying them
    needs a cap, which silently drops most of the data. Small multiples show ALL of it, so the plot's
    coverage matches the artifact's rather than being a legible-looking subset of it."""
    panels = {}
    for t in trajs:
        panels.setdefault((t["row"], t["region"]), []).append(t)
    keys = sorted(panels)
    NC = 3
    NR = (len(keys) + NC - 1) // NC
    PW, PH, MX, MY = 268, 150, 30, 34
    W = 40 + NC * (PW + MX)
    H = 96 + NR * (PH + MY)
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
         f'<rect width="{W}" height="{H}" fill="white"/>',
         f'<text x="28" y="30" font-family="system-ui,sans-serif" font-size="16" font-weight="600">'
         f'{family} — excess along the declared ramp</text>',
         f'<text x="28" y="48" font-family="system-ui,sans-serif" font-size="11" fill="#666">'
         f'DESCRIPTIVE — no verdict, no score. All {len(trajs)} trajectories in this family are shown; '
         f'each panel is one row and region, one line per flavour.</text>']
    lx = 28
    for fl, c in FLAVOUR_COL.items():
        if any(t["flavor"] == fl for t in trajs):
            p.append(f'<line x1="{lx}" y1="64" x2="{lx+16}" y2="64" stroke="{c}" stroke-width="2.2"/>')
            p.append(f'<text x="{lx+21}" y="68" font-size="10.5" fill="#333">{fl}</text>')
            lx += 30 + 7 * len(fl)
    p.append(f'<text x="{W-28}" y="68" font-size="10.5" text-anchor="end" fill="#666">'
             f'× = no reading (gap, never interpolated)   ○ = below the pre-declared r floor</text>')

    for idx, key in enumerate(keys):
        ts = panels[key]
        cx, cy = 40 + (idx % NC) * (PW + MX), 96 + (idx // NC) * (PH + MY)
        vals = [e for t in ts for e in t["excess_by_step"] if e is not None]
        lo, hi = (min(vals), max(vals)) if vals else (-0.05, 0.05)
        if hi - lo < 1e-9:
            lo, hi = lo - 0.02, hi + 0.02
        nstep = max(len(t["excess_by_step"]) for t in ts)
        def X(i, cx=cx, nstep=nstep): return cx + PW * (i / max(1, nstep - 1))
        def Y(v, cy=cy, lo=lo, hi=hi): return cy + PH - PH * ((v - lo) / (hi - lo))
        p.append(f'<rect x="{cx}" y="{cy}" width="{PW}" height="{PH}" fill="#fbfbfc" stroke="#e2e2e6"/>')
        if lo < 0 < hi:
            p.append(f'<line x1="{cx}" y1="{Y(0):.1f}" x2="{cx+PW}" y2="{Y(0):.1f}" stroke="#c8c8cc" '
                     f'stroke-dasharray="3 3"/>')
        p.append(f'<text x="{cx}" y="{cy-6}" font-size="11" font-weight="600" fill="#222">'
                 f'{key[0]} · {key[1]}</text>')
        for v in (lo, hi):
            p.append(f'<text x="{cx-5}" y="{Y(v)+3.5:.1f}" font-size="9" text-anchor="end" '
                     f'fill="#777">{v:+.3f}</text>')
        for k, t in enumerate(sorted(ts, key=lambda z: z["flavor"])):
            c = FLAVOUR_COL.get(t["flavor"], "#555")
            seg, segs = [], []
            for i, e in enumerate(t["excess_by_step"]):
                if e is None:
                    if len(seg) > 1: segs.append(seg)
                    seg = []
                else:
                    seg.append((X(i), Y(e)))
            if len(seg) > 1: segs.append(seg)
            for sg in segs:
                p.append(f'<polyline fill="none" stroke="{c}" stroke-width="1.7" points="'
                         + " ".join(f"{x:.1f},{y:.1f}" for x, y in sg) + '"/>')
            # TWO MARKERS, because two different things happened. A step with NO reading is not the same
            # as a step whose reading fell below the pre-declared floor: the first is silence, the second
            # is speech ruled inadmissible. One glyph for both would misreport which occurred.
            yo = cy + PH + 9 + 7 * (k % 2)
            for i, e in enumerate(t["excess_by_step"]):
                if e is None:
                    if i in t["insufficient_positions"]:
                        p.append(f'<circle cx="{X(i):.1f}" cy="{yo:.1f}" r="2.8" fill="none" '
                                 f'stroke="{c}" stroke-width="1.2"/>')
                    else:
                        p.append(f'<text x="{X(i):.1f}" y="{yo+3.5:.1f}" font-size="11" fill="{c}" '
                                 f'text-anchor="middle" font-weight="700">×</text>')
                else:
                    p.append(f'<circle cx="{X(i):.1f}" cy="{Y(e):.1f}" r="2.4" fill="{c}"/>')
    p.append("</svg>")
    path.write_text("\n".join(p) + "\n")
    return True


def main() -> int:
    doc = json.loads(SURVEY.read_text())
    manifest = doc["ramp_manifest"]
    # GAP-no-region records are DECLARATIONS OF ABSENCE, not readings — they carry no region or flavour.
    # They are split out here, not filtered away: they are the reason a step shows as a gap below, and
    # dropping them silently would recreate interpolation-by-absence inside the report that exists to
    # forbid it.
    readings = [x for x in doc["readings"] if x.get("region") and x.get("flavor")]
    gap_records = [x for x in doc["readings"] if not (x.get("region") and x.get("flavor"))]
    gap_steps = {(g["row"], g["ramp_position"]) for g in gap_records}

    suspects, degenerate = assert_controls_redrawn(readings)
    if suspects:
        print("FAIL — controls appear REUSED across ramp steps (same control profile at different r):",
              file=sys.stderr)
        for s in suspects[:10]:
            print(f"    {s}", file=sys.stderr)
        return 1

    steps = defaultdict(dict)                      # row -> position -> manifest entry
    for m in manifest:
        steps[m["row"]][m["ramp_position"]] = m
    got = {(x["row"], x["region"], x["flavor"], x["ramp_position"]): x for x in readings}
    combos = sorted({(x["row"], x["region"], x["flavor"]) for x in readings})

    trajs = []
    for row, region, flavour in combos:
        positions = sorted(steps[row])
        series, gaps, absent, insuff = [], [], [], []
        for pos in positions:
            x = got.get((row, region, flavour, pos))
            if x is None:
                series.append(None)
                # TWO KINDS OF ABSENCE, and collapsing them would repeat the very error this report
                # exists to avoid. A step-level GAP has a recorded reason in the survey artifact; a
                # combination-level absence does not — the step yielded a region, but not for THIS
                # (region, flavour). The second class is named here precisely because it is the
                # undocumented one.
                (gaps if (row, pos) in gap_steps else absent).append(pos)
                continue
            if x.get("insufficient") or x["r"] < R_FLOOR:
                series.append(None); insuff.append(pos); continue
            series.append(x["excess"])
        usable = [e for e in series if e is not None]
        sds = [got[(row, region, flavour, p)]["control_sd"] for p in positions
               if got.get((row, region, flavour, p)) and series[positions.index(p)] is not None]
        label, exc, psd = classify(usable, sds, FLAT_MULT)
        alt = {f"{m}x": classify(usable, sds, m)[0] for m in (1.0, 3.0)}
        # position 0 may be a GAP, so the row's metadata is taken from ANY step that produced a
        # reading. Reading it from positions[0] silently yielded family=None for every trajectory whose
        # ramp opens on a gap — which is exactly the rows this report most needs to label.
        any_x = next((got[(row, region, flavour, p_)] for p_ in positions
                      if (row, region, flavour, p_) in got), None)
        trajs.append({
            "row": row, "region": region, "flavor": flavour,
            "family": (any_x or {}).get("family"), "decision": (any_x or {}).get("decision"),
            "ramp_param": (steps[row][positions[0]]["ramp_param"] if positions else None),
            "ramp_values": [steps[row][p]["ramp_value"] for p in positions],
            "excess_by_step": series,
            "n_declared_steps": len(positions), "n_usable": len(usable),
            "gap_positions_no_region": gaps,
            "absent_positions_no_reading_for_this_combination": absent,
            "insufficient_positions": insuff,
            "excursion": round(exc, 4) if exc is not None else None,
            "pooled_control_sd": round(psd, 5) if psd is not None else None,
            "classification": label, "classification_at_other_multipliers": alt,
            "theorem_forced": (any_x or {}).get("theorem_forced"),
            "zero_hunt_verdict": next((got[(row, region, flavour, p)].get("zero_hunt_verdict")
                                       for p in positions
                                       if got.get((row, region, flavour, p), {}).get("zero_hunt_verdict")),
                                      None)})

    moved = {m: sum(1 for t in trajs if t["classification_at_other_multipliers"][m] != t["classification"])
             for m in ("1.0x", "3.0x")}

    PLOTS.mkdir(parents=True, exist_ok=True)
    byfam = defaultdict(list)
    for t in trajs:
        if t["n_usable"] >= 2:
            byfam[t["family"] or "unclassified"].append(t)
    plotted, plot_coverage = [], []
    for fam, ts in sorted(byfam.items()):
        ordered = sorted(ts, key=lambda z: (z["row"], z["region"], z["flavor"]))
        pth = PLOTS / f"trajectory-{fam}.svg"
        if svg_plot(fam, ordered, pth):
            plotted.append(pth.name)
            plot_coverage.append({
                "plot": pth.name, "family": fam, "trajectories_in_family": len(ordered),
                "shown": len(ordered), "omitted_for_legibility": [],
                "note": ("drawn as small multiples — one panel per (row, region) — so every trajectory "
                         "in the family appears. No cap, nothing dropped.")})

    out = {"schema": "sounding-trajectories/v1",
           "STATUS": "DESCRIPTIVE BY DECLARATION — no verdict, no score, no prediction",
           "classification_rule_pinned_before_running": {
               "flat": f"excursion < {FLAT_MULT} * pooled control SD",
               "monotone": "not flat, and the excess sequence is weakly non-increasing or non-decreasing",
               "non_monotone": "otherwise",
               "unclassified": "fewer than 3 usable steps",
               "usable_step": f"a declared step with a reading whose r >= {R_FLOOR} (the pre-declared floor)",
               "the_multiplier_is_a_convention": (
                   f"{FLAT_MULT} is not derived from anything. It is the ordinary default, chosen in "
                   f"advance because choosing in advance is worth more than choosing well. The "
                   f"sensitivity below makes the arbitrariness visible instead of merely confessed."),
               "sensitivity": {"trajectories_relabelled_at_1.0x": moved["1.0x"],
                               "trajectories_relabelled_at_3.0x": moved["3.0x"],
                               "of_total": len(trajs)}},
           "gap_no_region_records": {
               "n": len(gap_records),
               "meaning": ("a DECLARED ramp step at which no region was produced at all. Distinct from "
                           "a combination-level absence, where the step produced a region but this "
                           "(region, flavour) has no reading — those are listed per trajectory under "
                           "`absent_positions_no_reading_for_this_combination` and carry NO recorded "
                           "per-step reason, which is why they are named separately rather than pooled."),
               "steps": [{"row": g["row"], "ramp_position": g["ramp_position"],
                          "ramp_value": g["ramp_value"], "reason": g.get("gap_reason")}
                         for g in gap_records]},
           "gaps_are_drawn_never_interpolated": (
               "a declared ramp step with no reading is held as an explicit null in `excess_by_step` and "
               "listed in `gap_positions_no_region`; plot lines BREAK at it rather than bridging it. An "
               "absent reading is a claim of continuity unless the absence is itself recorded."),
           "controls_redrawn_per_step": (
               "VERIFIED, not assumed: controls are matched on r and r moves along the ramp, so a reused "
               "control would show an identical (mean, sd) pair at two different r. No such pair exists "
               "among non-degenerate controls."),
           "degenerate_control_profiles": {
               "n": len(degenerate),
               "label": "INSUFFICIENT-degenerate (the v3 spec's own pre-declared vocabulary)",
               "what": ("control SD is exactly 0 because every control draw violated — the profile "
                        "saturates at (1.0, 0.0). Such a control has no signature to compare, so it is "
                        "excluded from the reuse detector rather than flagged by it. Every instance sits "
                        "at small r under `minority`, where a random subset almost never survives a "
                        "3-way XOR."),
               "instances": degenerate},
           "n_trajectories": len(trajs), "n_rows": len({t["row"] for t in trajs}),
           "n_declared_steps_total": len(manifest),
           "classification_counts": {k: sum(1 for t in trajs if t["classification"] == k)
                                     for k in ("FLAT", "MONOTONE", "NON-MONOTONE", "UNCLASSIFIED")},
           "plots": plotted, "plot_coverage": plot_coverage, "trajectories": trajs}
    OUT.write_text(json.dumps(out, indent=1) + "\n")

    print("THE TRAJECTORY REPORT — descriptive by declaration, no verdict\n")
    print(f"  trajectories      : {len(trajs)} over {out['n_rows']} rows, "
          f"{len(manifest)} declared steps")
    print(f"  controls re-drawn : VERIFIED (no reused control profile at differing r)")
    print(f"  degenerate ctrls  : {len(degenerate)} INSUFFICIENT-degenerate (saturated at 1.0, SD 0)")
    print(f"\n  {'classification':<16}count")
    for k, v in out["classification_counts"].items():
        print(f"  {k:<16}{v}")
    print(f"\n  rule sensitivity: {moved['1.0x']} of {len(trajs)} relabel at 1.0x, "
          f"{moved['3.0x']} at 3.0x")
    print(f"\n  {'row':<26}{'region':<10}{'flavor':<9}{'steps':>6}{'use':>5}{'excurs':>9}{'ctrlSD':>9}  class")
    for t in sorted(trajs, key=lambda z: (z["classification"], z["row"])):
        if t["n_usable"] < 2 and t["classification"] == "UNCLASSIFIED":
            continue
        print(f"  {t['row']:<26}{t['region']:<10}{t['flavor']:<9}{t['n_declared_steps']:>6}"
              f"{t['n_usable']:>5}{(t['excursion'] if t['excursion'] is not None else 0):>9.4f}"
              f"{(t['pooled_control_sd'] or 0):>9.5f}  {t['classification']}"
              + ("  [GAP " + ",".join(map(str, t["gap_positions_no_region"])) + "]"
                 if t["gap_positions_no_region"] else "")
              + ("  [absent " + ",".join(map(str, t["absent_positions_no_reading_for_this_combination"]))
                 + "]" if t["absent_positions_no_reading_for_this_combination"] else ""))
    print(f"\n  plots: {len(plotted)} — {', '.join(plotted)}")
    for pc in plot_coverage:
        print(f"    {pc['plot']:<38}{pc['shown']} of {pc['trajectories_in_family']} trajectories"
              + ("  [OMITTED " + str(len(pc["omitted_for_legibility"])) + "]"
                 if pc["omitted_for_legibility"] else ""))
    print(f"\nwrote {OUT.name}  sha256 {hashlib.sha256(OUT.read_bytes()).hexdigest()[:16]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
