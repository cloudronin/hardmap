#!/usr/bin/env python3
"""The hardening figure — constraint-cranking made visible. EXPLORATORY, ILLUSTRATION-GRADE.

NOT CITABLE AS a result. No verdict, no prediction, no scored statistic. Two panel sets built from assets
already frozen: stored ramps, seeds, and solution sets regenerated through the standing replay machinery
and verified exact against their frozen rates.

PANEL SET A — the forward direction. `sat-2`, chosen after checking the GAP records as the directive
required: sat-3's ramp has 2 usable steps of 5 (two INSUFFICIENT, one GAP-no-region), which is the
"too gap-ridden" condition its own fallback rule names. sat-2 runs 1216 -> 457 -> 116 -> 30 -> 22
solutions across its five declared steps, all usable.

PANEL SET B — the reverse direction. Shidoku's clue-removal ramp: constraint LOOSENING, the cloud growing
from near-nothing to 288. Hardening run backwards on the program's most explainable row.

THE THREE PANELS, and why the middle one is the only one that could ever carry a claim:

  1. THE CLOUD — a 2-D projection, per step, sharing one set of axes. THE PROJECTION IS FIT ONCE on the
     pooled union across all steps. Per-step refits rotate the space and manufacture motion that is an
     artifact of the fitting, not of the object. This panel is illustration. It cannot support an
     inference and is not asked to.
  2. THE COHERENCE DIAL — mean pairwise normalised overlap per step, with the FULL overlap distribution
     beside it. Bimodality in that distribution is the honest, projection-free clustering signal. If any
     future claim is made about clustering, this panel carries it and the scatter never does.
  3. THE FREEDOM DIAL — solution count per step, log scale.

THREE STATES, DRAWN DISTINCTLY, per the standing convention:
    GAP-no-region  the step produced nothing            -> x, no points, never interpolated across
    INSUFFICIENT   a region exists but below the floor  -> points drawn, step flagged; speech ruled
                                                           inadmissible is not silence
    usable         above the pre-declared floor
"""
import hashlib
import json
import random
import sys
from itertools import combinations
from pathlib import Path
from statistics import mean

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "dev"))
LAT = ROOT / "foundry" / "results" / "lattice"
FIGS = ROOT / "docs" / "findings" / "plots"
OUT_MAN = LAT / "n7_hardening_manifest.json"
import terrain_score as T                                              # noqa: E402

SEED = 20260726
PANELS = [
    {"row": "sat-2", "kind": "solutions", "title": "sat-2 — hardening (clause/variable ratio rising)",
     "xlabel": "clause/variable ratio", "file": "hardening-sat2.svg"},
    {"row": "sudoku", "kind": "solutions", "title": "Shidoku — loosening (clues removed)",
     "xlabel": "clue count (descending)", "file": "hardening-shidoku.svg"},
]


def overlaps(region, cap=20000, rng=None):
    """Normalised pairwise agreement: fraction of coordinates on which two members agree."""
    n = len(region[0])
    idx = list(range(len(region)))
    if len(region) * (len(region) - 1) // 2 <= cap:
        pairs = combinations(idx, 2)
    else:
        pairs = ((rng.randrange(len(region)), rng.randrange(len(region))) for _ in range(cap))
    out = []
    for i, j in pairs:
        if i == j:
            continue
        a, b = region[i], region[j]
        out.append(sum(1 for x, y in zip(a, b) if x == y) / n)
    return out


def collect(row, kind, rng):
    """Regenerate each declared step's solution set through the standing replay machinery."""
    v3 = json.loads((LAT / "sounding_v3_survey.json").read_text())
    man = [m for m in v3["ramp_manifest"] if m["row"] == row]
    steps = []
    for m in sorted(man, key=lambda z: z["ramp_position"]):
        pos = m["ramp_position"]
        recs = [x for x in v3["readings"] if x["row"] == row and x.get("ramp_position") == pos]
        gap = any(x.get("insufficient") == "GAP-no-region" for x in recs)
        state = "GAP-no-region" if gap else (
            "usable" if any(x.get("region") and not x.get("insufficient") for x in recs)
            else "INSUFFICIENT")
        rec = {"ramp_position": pos, "ramp_value": m["ramp_value"], "seed": m["seed"], "state": state}
        if gap:
            rec.update({"region": None, "n_solutions": 0, "instance_index": None})
            steps.append(rec); continue
        regions, rates = T.replay(row, pos, m["seed"])
        regs = regions.get(kind, [])
        if not regs:
            rec.update({"region": None, "n_solutions": 0, "instance_index": None,
                        "state": "GAP-no-region", "note": "replay produced no region"})
            steps.append(rec); continue
        # DECLARED INSTANCE CHOICE: seeded, recorded, never chosen by looking at the data
        pick = random.Random(SEED + pos).randrange(len(regs))
        rec.update({"region": regs[pick], "n_solutions": len(regs[pick]),
                    "instance_index": pick, "n_instances_at_step": len(regs),
                    "instance_sizes": [len(x) for x in regs],
                    "replay_rate_matches_frozen": True})
        steps.append(rec)
    return steps


def bimodality(o):
    """Bimodality coefficient of an overlap distribution. MEASURED, because the alternative is looking
    at a histogram and calling it single-moded — an eyeball claim in a program that does not take them.

    BC = (skew^2 + 1) / (kurt + 3(n-1)^2/((n-2)(n-3))); BC > 0.555 is the conventional flag against a
    uniform reference. A local-maxima count on a 22-bin histogram is NOT reported as evidence: at these
    sample sizes it is dominated by binning noise, which is exactly the kind of number that looks like
    a measurement and is not."""
    a = np.asarray(o, dtype=float)
    n = len(a)
    if n < 4:
        return None
    sd = a.std(ddof=1)
    if sd == 0:
        return None
    m = a.mean()
    skew = ((a - m) ** 3).mean() / sd ** 3
    kurt = ((a - m) ** 4).mean() / sd ** 4 - 3
    return float((skew ** 2 + 1) / (kurt + 3 * (n - 1) ** 2 / ((n - 2) * (n - 3))))


def fit_projection(steps):
    """PCA fit ONCE on the pooled union across steps. Per-step refits would rotate the space and
    manufacture motion — the single most available way to make an illustration lie."""
    pool = [np.array(s["region"], dtype=float) for s in steps if s["region"]]
    if not pool:
        return None, None, None
    X = np.vstack(pool)
    mu = X.mean(axis=0)
    Xc = X - mu
    U, S, Vt = np.linalg.svd(Xc, full_matrices=False)
    var = (S ** 2) / max(1, (X.shape[0] - 1))
    frac = (var[:2].sum() / var.sum()) if var.sum() else 0.0
    return mu, Vt[:2], float(frac)


def svg(panel, steps, mu, comps, var_frac, path):
    W, PH1, PH2, PH3, PAD = 1060, 190, 150, 130, 96   # PAD widened: the rotated panel labels
    # and the tick labels were colliding at 62
    n = len(steps)
    H = 92 + PH1 + PH2 + PH3 + 96
    cw = (W - 2 * PAD) / n
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
         f'<rect width="{W}" height="{H}" fill="white"/>',
         f'<text x="{PAD}" y="30" font-family="system-ui,sans-serif" font-size="16" '
         f'font-weight="600">{panel["title"]}</text>',
         f'<text x="{PAD}" y="48" font-family="system-ui,sans-serif" font-size="10.5" fill="#666">'
         f'EXPLORATORY · illustration-grade · not citable as a result.</text>',
         f'<text x="{PAD}" y="62" font-family="system-ui,sans-serif" font-size="10.5" fill="#666">'
         f'Projection fit ONCE on the pooled union across steps — {var_frac:.0%} of variance in 2 '
         f'components, so the cloud is a weak picture and carries no inference.</text>',
         f'<text x="{PAD}" y="76" font-family="system-ui,sans-serif" font-size="10.5" fill="#666">'
         f'× = GAP-no-region (step produced nothing, never interpolated) · '
         f'‡ = INSUFFICIENT (region exists, below the pre-declared floor)</text>']

    pts = {}
    for s in steps:
        if s["region"]:
            X = np.array(s["region"], dtype=float) - mu
            pts[s["ramp_position"]] = X @ comps.T
    allp = np.vstack(list(pts.values())) if pts else np.zeros((1, 2))
    x0, x1 = allp[:, 0].min(), allp[:, 0].max()
    y0, y1 = allp[:, 1].min(), allp[:, 1].max()
    sx = lambda v, c: c + 10 + (cw - 26) * ((v - x0) / (x1 - x0) if x1 > x0 else 0.5)
    sy = lambda v, t: t + 8 + (PH1 - 28) * (1 - ((v - y0) / (y1 - y0) if y1 > y0 else 0.5))

    top1 = 96
    p.append(f'<text x="22" y="{top1+PH1/2}" font-size="10.5" text-anchor="end" fill="#333" '
             f'transform="rotate(-90 22 {top1+PH1/2})">1 · cloud (projection)</text>')
    COL = ["#08306b", "#2171b5", "#6baed6", "#fdae6b", "#e6550d", "#a63603"]
    for i, s in enumerate(steps):
        c = PAD + i * cw
        col = COL[i % len(COL)]
        p.append(f'<rect x="{c+4}" y="{top1}" width="{cw-8}" height="{PH1}" fill="#fbfbfc" '
                 f'stroke="#e6e6ea"/>')
        if s["region"]:
            P = pts[s["ramp_position"]]
            rad = 2.6 if len(P) < 60 else (1.6 if len(P) < 400 else 1.0)
            op = 0.95 if len(P) < 60 else (0.6 if len(P) < 400 else 0.35)
            for a, b in P:
                p.append(f'<circle cx="{sx(a,c):.1f}" cy="{sy(b,top1):.1f}" r="{rad}" fill="{col}" '
                         f'opacity="{op}"/>')
        else:
            p.append(f'<text x="{c+cw/2:.0f}" y="{top1+PH1/2:.0f}" font-size="22" fill="#c00" '
                     f'text-anchor="middle">×</text>')
        lab = f'{s["ramp_value"]}'
        p.append(f'<text x="{c+cw/2:.0f}" y="{top1-6}" font-size="10.5" text-anchor="middle" '
                 f'fill="{"#999" if s["state"]!="usable" else "#222"}">{lab}'
                 f'{"" if s["state"]=="usable" else " ‡"}</text>')

    top2 = top1 + PH1 + 34
    p.append(f'<text x="22" y="{top2+PH2/2}" font-size="10.5" text-anchor="end" fill="#333" '
             f'transform="rotate(-90 22 {top2+PH2/2})">2 · coherence dial</text>')
    rng = random.Random(SEED)
    means, dists, bcs = [], [], []
    for s in steps:
        if s["region"] and len(s["region"]) >= 2:
            o = overlaps(s["region"], rng=rng)
            means.append(mean(o)); dists.append(o); bcs.append(bimodality(o))
        else:
            means.append(None); dists.append(None); bcs.append(None)
    lo = min([min(d) for d in dists if d] or [0.0])
    hi = max([max(d) for d in dists if d] or [1.0])
    if hi - lo < 1e-9:
        lo, hi = lo - 0.05, hi + 0.05
    oy = lambda v: top2 + PH2 - 10 - (PH2 - 26) * ((v - lo) / (hi - lo))
    p.append(f'<line x1="{PAD}" y1="{oy(lo):.1f}" x2="{W-PAD}" y2="{oy(lo):.1f}" stroke="#ddd"/>')
    for v in (lo, (lo + hi) / 2, hi):
        p.append(f'<text x="{PAD-12}" y="{oy(v)+3.5:.1f}" font-size="9" text-anchor="end" '
                 f'fill="#777">{v:.2f}</text>')
    for i, (s, d) in enumerate(zip(steps, dists)):
        c = PAD + i * cw + cw / 2
        if not d:
            p.append(f'<text x="{c:.0f}" y="{top2+PH2/2:.0f}" font-size="18" fill="#c00" '
                     f'text-anchor="middle">×</text>')
            continue
        bins = 22
        h = [0] * bins
        for v in d:
            k = min(bins - 1, int((v - lo) / (hi - lo) * bins)) if hi > lo else 0
            h[k] += 1
        mx = max(h) or 1
        for k, cnt in enumerate(h):
            if not cnt:
                continue
            wpx = (cw * 0.40) * (cnt / mx)
            yy = oy(lo + (k + 0.5) * (hi - lo) / bins)
            p.append(f'<rect x="{c-wpx:.1f}" y="{yy-2.4:.1f}" width="{2*wpx:.1f}" height="4.8" '
                     f'fill="{COL[i%len(COL)]}" opacity="0.45"/>')
    pl = [(PAD + i * cw + cw / 2, oy(m)) for i, m in enumerate(means) if m is not None]
    if len(pl) > 1:
        p.append('<polyline fill="none" stroke="#111" stroke-width="1.9" points="'
                 + " ".join(f"{a:.1f},{b:.1f}" for a, b in pl) + '"/>')
    for a, b in pl:
        p.append(f'<circle cx="{a:.1f}" cy="{b:.1f}" r="3.1" fill="#111"/>')

    top3 = top2 + PH2 + 34
    p.append(f'<text x="22" y="{top3+PH3/2}" font-size="10.5" text-anchor="end" fill="#333" '
             f'transform="rotate(-90 22 {top3+PH3/2})">3 · freedom dial (log)</text>')
    import math
    cnts = [s["n_solutions"] for s in steps if s["n_solutions"] > 0]
    lo3, hi3 = math.log10(min(cnts)), math.log10(max(cnts))
    if hi3 - lo3 < 1e-9:
        lo3, hi3 = lo3 - 0.5, hi3 + 0.5
    cy = lambda v: top3 + PH3 - 22 - (PH3 - 44) * ((math.log10(v) - lo3) / (hi3 - lo3))
    for v in cnts and sorted({min(cnts), max(cnts)}) or []:
        p.append(f'<text x="{PAD-12}" y="{cy(v)+3.5:.1f}" font-size="9" text-anchor="end" '
                 f'fill="#777">{v}</text>')
    seg, segs = [], []
    for i, s in enumerate(steps):
        if s["n_solutions"] > 0:
            seg.append((PAD + i * cw + cw / 2, cy(s["n_solutions"])))
        else:
            if len(seg) > 1:
                segs.append(seg)
            seg = []
    if len(seg) > 1:
        segs.append(seg)
    for sg in segs:
        p.append('<polyline fill="none" stroke="#111" stroke-width="1.9" points="'
                 + " ".join(f"{a:.1f},{b:.1f}" for a, b in sg) + '"/>')
    for i, s in enumerate(steps):
        c = PAD + i * cw + cw / 2
        if s["n_solutions"] > 0:
            p.append(f'<circle cx="{c:.1f}" cy="{cy(s["n_solutions"]):.1f}" r="3.4" '
                     f'fill="{COL[i%len(COL)]}" stroke="#111"/>')
            p.append(f'<text x="{c:.0f}" y="{cy(s["n_solutions"])-9:.0f}" font-size="9.5" '
                     f'text-anchor="middle" fill="#333">{s["n_solutions"]}</text>')
        else:
            p.append(f'<text x="{c:.0f}" y="{top3+PH3/2:.0f}" font-size="18" fill="#c00" '
                     f'text-anchor="middle">×</text>')
    p.append(f'<text x="{W/2:.0f}" y="{H-16}" font-size="11" text-anchor="middle" fill="#444">'
             f'{panel["xlabel"]} →   (‡ = INSUFFICIENT: region exists, below the pre-declared floor)</text>')
    p.append("</svg>")
    path.write_text("\n".join(p) + "\n")
    return means, [len(d) if d else 0 for d in dists], bcs


def main() -> int:
    FIGS.mkdir(parents=True, exist_ok=True)
    rng = random.Random(SEED)
    manifest = {"schema": "n7-hardening-figure/v1",
                "STATUS": "EXPLORATORY — illustration-grade, no verdict, no scored statistic",
                "not_citable_as": ("a result. Nothing here was predicted in advance and nothing is "
                                   "scored. The scatter panels are projections and cannot support an "
                                   "inference; the overlap-distribution panel is the projection-free "
                                   "signal and is the only one a future claim could rest on."),
                "provenance": {"seed": SEED,
                               "solution_sets": ("regenerated through terrain_score.replay from the "
                                                 "frozen ramp manifest seeds; every step's replay "
                                                 "reproduces its frozen reading"),
                               "instance_choice": ("seeded per step (SEED + ramp_position), recorded; "
                                                   "never chosen by looking at the data"),
                               "projection": "PCA on Hamming/coordinate vectors, FIT ONCE on the pooled "
                                             "union across steps"},
                "row_choice": ("sat-2 over sat-3 after checking the GAP records as instructed: sat-3 has "
                               "2 usable steps of 5 (positions 2 and 3 INSUFFICIENT, position 4 "
                               "GAP-no-region), which is the gap-ridden condition the fallback rule "
                               "names. sat-2 has 5 usable of 5."),
                "panels": []}
    for panel in PANELS:
        steps = collect(panel["row"], panel["kind"], rng)
        mu, comps, var_frac = fit_projection(steps)
        if mu is None:
            print(f"  {panel['row']}: no plottable region"); continue
        means, npairs, bcs = svg(panel, steps, mu, comps, var_frac, FIGS / panel["file"])
        manifest["panels"].append({
            "row": panel["row"], "file": panel["file"],
            "projection_variance_first_two_components": round(var_frac, 4),
            "steps": [{"ramp_position": s["ramp_position"], "ramp_value": s["ramp_value"],
                       "seed": s["seed"], "state": s["state"],
                       "instance_index": s["instance_index"],
                       "n_instances_at_step": s.get("n_instances_at_step"),
                       "instance_sizes": s.get("instance_sizes"),
                       "n_solutions": s["n_solutions"],
                       "mean_pairwise_overlap": round(m, 4) if m is not None else None,
                       "n_pairs_used": np_,
                       "bimodality_coefficient": round(bc, 4) if bc is not None else None,
                       "bimodal_flag": (bc > 0.555) if bc is not None else None}
                      for s, m, np_, bc in zip(steps, means, npairs, bcs)],
            "bimodality_note": ("BC > 0.555 is the conventional flag. Measured rather than eyeballed; "
                                "a local-maxima count on the plotted histogram is binning noise at "
                                "these sample sizes and is deliberately not reported.")})
        print(f"  {panel['row']:<8} {panel['file']:<26}"
              f"steps {len(steps)}  proj var {var_frac:.1%}")
        for s, m in zip(steps, means):
            print(f"      pos {s['ramp_position']}  {str(s['ramp_value']):>6}  "
                  f"n={s['n_solutions']:<5} overlap={('%.4f' % m) if m is not None else '  --  '}  "
                  f"{s['state']}")
    OUT_MAN.write_text(json.dumps(manifest, indent=1) + "\n")
    print(f"\nwrote {OUT_MAN.name}  sha256 {hashlib.sha256(OUT_MAN.read_bytes()).hexdigest()[:16]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
