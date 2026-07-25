#!/usr/bin/env python3
"""Assemble Channel-B round-1 param-fill research into a single review table.

Reads chanB_out1..6.json from the scratchpad, merges, tags each with its blind locality label (for
DIAGNOSTIC reporting only — never used in selection), and emits:
  * chanB_round1_fillable.json  — the fillable claims to send to dual-pass verify (round 2)
  * chanB_round1_summary.txt    — counts + the decomposable-yield diagnostic

Selection was blind (agents judged citability only). This script does NOT decide fills; it collates
round-1 for the independent round-2 verification the owner's sequence requires before any fill counts.
"""
import json, sys
from pathlib import Path
from collections import Counter

SCR = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(
    "/private/tmp/claude-501/-Users-vishnu-Library-CloudStorage-Dropbox-Praxis-hardmap--claude-worktrees-quarry-row-expansion-spec-31d212/00903a0f-aaf7-438e-a357-ef719e86aba8/scratchpad")
AT = Path("eightfold/eightfold/results/atlas")
LOC = {json.loads(l)["problem_id"]: json.loads(l)["locality_3class"]
       for l in (AT / "mosaic-locality.jsonl").read_text().splitlines() if l.strip()}
ALLOWED = {"FPT", "W[1]", "W[2]+", "XP", "para-NP-hard"}

rows = []
missing = []
for i in range(1, 7):
    f = SCR / f"chanB_out{i}.json"
    if not f.exists():
        missing.append(i); continue
    rows.extend(json.loads(f.read_text()))
if missing:
    print(f"WARNING — batches not yet present: {missing}. Assembling partial ({len(rows)} rows).")

fillable = []
for r in rows:
    v = r.get("parameterized_value")
    ok = bool(r.get("fillable")) and v in ALLOWED
    if ok:
        r["_locality_diag"] = LOC.get(r["problem_id"], "?")
        fillable.append(r)

(SCR / "chanB_round1_fillable.json").write_text(json.dumps(fillable, indent=1))

fill_ids = {r["problem_id"] for r in fillable}
diag = Counter(r["_locality_diag"] for r in fillable)
dec = sorted(r["problem_id"] for r in fillable if r["_locality_diag"] == "decomposable")
val = Counter(r["parameterized_value"] for r in fillable)
conf = Counter(r.get("confidence", "?") for r in fillable)

lines = [
    f"round-1 total researched: {len(rows)} / 55",
    f"fillable (citable, valid value): {len(fillable)}   open: {len(rows) - len(fillable)}",
    f"parameterized values: {dict(val)}",
    f"confidence: {dict(conf)}",
    f"",
    f"DIAGNOSTIC (not a selection input) — fillable locality mix: {dict(diag)}",
    f"decomposable fills ({len(dec)}): {', '.join(dec) if dec else '(none)'}",
    f"",
    f"--> dual-pass verify (round 2) runs on these {len(fillable)} fillable claims before any counts.",
]
summary = "\n".join(lines)
(SCR / "chanB_round1_summary.txt").write_text(summary)
print(summary)
