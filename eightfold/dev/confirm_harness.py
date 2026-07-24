#!/usr/bin/env python3
"""Atlas v3 confirm harness (V2) — the OWNER runs this; the agent only built it.

Implements the sealed QC tier table (Quarry-SCHEMA.md section 3):
  reliable       decision(NP-level) + parallelization  -> SAMPLED confirm, sealed random 15% per funnel
                                                          (escalate that funnel to FULL if sample error > 5%)
  judgment-heavy approximation + beyond-NP decision     -> FULL confirm
  dear           counting                               -> FULL confirm (open downgrades expected)

  `python dev/confirm_harness.py plan`   -> the confirm workload, per tier x funnel
  `python dev/confirm_harness.py sample` -> the sealed 15% reliable-tier sample (seed-fixed, reproducible)
  `python dev/confirm_harness.py sheet`  -> a per-sitting worksheet (markdown) to record verdict + wall-clock

Confirm outcomes go back into the funnel error table; wall-clock per sitting is the measurement
K4 declined to invent. Nothing here writes atlas data — it only selects and reports.
"""
import argparse, json, os, random, sys
from collections import defaultdict

ATLAS_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                          "..", "eightfold", "results", "atlas"))
SEED = 20260723           # sealed: the sample must be reproducible/auditable
SAMPLE_FRAC = 0.15        # reliable tier
ESCALATE_AT = 0.05        # sample error > 5% => that funnel escalates to full confirm

BEYOND_NP = {"PH-complete", "PSPACE-complete", "beyond-PSPACE", "coNP-complete"}


def load():
    rows, prov = [], {}
    for w in ("w1", "w2", "w3", "w4"):
        p = os.path.join(ATLAS_DIR, f"quarry-v3-{w}.jsonl")
        if os.path.exists(p):
            rows += [json.loads(l) for l in open(p) if l.strip()]
    pp = os.path.join(ATLAS_DIR, "quarry-v3-provenance.jsonl")
    if os.path.exists(pp):
        for l in open(pp):
            if l.strip():
                d = json.loads(l); prov[d["problem_id"]] = d
    return rows, prov


def tier_of(cell):
    """Which confirm tier a CITED cell falls in (sentinels need no confirm)."""
    if cell["status"] == "structural":
        return None
    ch, val = cell["charge"], cell["value"]
    if ch == "counting":
        return "dear"
    if ch == "approximation":
        return "judgment-heavy"
    if ch == "decision":
        return "judgment-heavy" if val in BEYOND_NP else "reliable"
    if ch == "parallelization":
        return "reliable"
    return "judgment-heavy"          # parameterized/proof_size/average_case/landscape: judgment


def cited_cells(rows, prov):
    out = []
    for r in rows:
        f = prov.get(r["problem_id"], {}).get("source_funnel", "?")
        w = prov.get(r["problem_id"], {}).get("admission_wave", "?")
        for c in r["charges"]:
            t = tier_of(c)
            if t:
                out.append({"problem_id": r["problem_id"], "charge": c["charge"], "value": c["value"],
                            "tier": t, "funnel": f, "wave": w,
                            "citation": (c.get("provenance") or {}).get("citation", "")[:90]})
    return out


def cmd_plan(cells):
    by = defaultdict(lambda: defaultdict(int))
    for c in cells:
        by[c["tier"]][c["funnel"]] += 1
    print(f"=== confirm workload: {len(cells)} cited cells ===\n")
    print(f"{'tier':16} {'funnel':8} {'cells':>6}  {'to confirm':>10}")
    tot_confirm = 0
    for tier in ("reliable", "judgment-heavy", "dear"):
        for funnel, n in sorted(by[tier].items()):
            need = max(1, round(n * SAMPLE_FRAC)) if tier == "reliable" else n
            tot_confirm += need
            print(f"{tier:16} {funnel:8} {n:6d}  {need:10d}")
    print(f"\n  reliable = sampled {int(SAMPLE_FRAC*100)}% (escalates to FULL if that funnel's sample error > {int(ESCALATE_AT*100)}%)")
    print(f"  judgment-heavy + dear = FULL confirm")
    print(f"\n  TOTAL cells to confirm at V2: {tot_confirm}  (of {len(cells)} cited)")
    print("  NOTE: wall-clock per sitting is logged in the sheet — that is the cost measurement.")


def cmd_sample(cells):
    rng = random.Random(SEED)
    by_funnel = defaultdict(list)
    for c in cells:
        if c["tier"] == "reliable":
            by_funnel[c["funnel"]].append(c)
    print(f"=== sealed reliable-tier sample (seed={SEED}, {int(SAMPLE_FRAC*100)}% per funnel) ===")
    for funnel, cs in sorted(by_funnel.items()):
        cs = sorted(cs, key=lambda x: (x["problem_id"], x["charge"]))
        k = max(1, round(len(cs) * SAMPLE_FRAC))
        for c in rng.sample(cs, k):
            print(f"  [{funnel}] {c['problem_id']:38} {c['charge']:16} {c['value']:18} | {c['citation']}")
        print(f"  -- {funnel}: {k} of {len(cs)}")


def cmd_sheet(cells):
    """Markdown worksheet: the owner records verdict + wall-clock per sitting."""
    print("# Atlas v3 — confirm sitting worksheet\n")
    print("Record per cell: `OK` (promote to confirmed) / `FIX` (value corrected) / `OPEN` (downgraded).")
    print("Log the sitting's wall-clock at the bottom — that is the measured confirm cost.\n")
    print("| # | problem_id | charge | drafted value | tier | funnel | verdict | corrected value | note |")
    print("|---|---|---|---|---|---|---|---|---|")
    full = [c for c in cells if c["tier"] in ("judgment-heavy", "dear")]
    for i, c in enumerate(sorted(full, key=lambda x: (x["tier"], x["funnel"], x["problem_id"]))[:400], 1):
        print(f"| {i} | `{c['problem_id']}` | {c['charge']} | `{c['value']}` | {c['tier']} | {c['funnel']} |  |  |  |")
    print(f"\n**Sitting:** date ______  start ______  end ______  **wall-clock ______**")
    print(f"**Cells confirmed this sitting:** ______   **errors found:** ______")
    print("\n## Funnel error table (fill as sittings complete)\n")
    print("| funnel | cells confirmed | errors | error rate | > 15% => QUARANTINE (kill-criterion 1) |")
    print("|---|---|---|---|---|")
    for f in sorted({c["funnel"] for c in cells}):
        print(f"| {f} |  |  |  |  |")


def main():
    ap = argparse.ArgumentParser(description="Atlas v3 confirm harness (owner-run)")
    ap.add_argument("command", choices=["plan", "sample", "sheet"])
    a = ap.parse_args()
    rows, prov = load()
    if not rows:
        print("no v3 wave files found", file=sys.stderr); return 1
    cells = cited_cells(rows, prov)
    {"plan": cmd_plan, "sample": cmd_sample, "sheet": cmd_sheet}[a.command](cells)
    return 0


if __name__ == "__main__":
    sys.exit(main())
