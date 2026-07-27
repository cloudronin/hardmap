#!/usr/bin/env python3
"""Run one Helm wave cycle, up to the slate and no further.

    db sweep -> candidate generation -> mechanical screens -> ranked slate -> [OWNER RULING]

THE CYCLE STOPS AT THE SLATE. Helm §0.2: the owner rules every seal, one sitting per wave, and the
generator's priors update from verdicts rather than from unruled candidates. This script cannot seal
anything and has no code path that tries.

EVERY EVENT IS EMITTED HERE, AS IT HAPPENS. The sweep record is written when the sweep finishes, the
screen record when the screens finish, the slate record when the slate is ranked. Kill 3 forbids a trail
assembled afterwards, so there is no reporting pass at the end of this file that writes the history of
what the earlier lines did.

WHAT THIS READS: the published database and the question bank. It does not read a reserved row, because
reserved rows have no frames — they are declared and uncaptured. The reservation ledger IS read, and
legitimately: knowing WHICH rows are reserved is required to project the frontier's power, and a row id
is not a reading.
"""
import hashlib
import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from foundry.catalog import reservation as RES                                  # noqa: E402
from foundry.helm import screens as S                                           # noqa: E402
from foundry.helm import slate as SL                                            # noqa: E402
from foundry.helm import sweep as SW                                            # noqa: E402
from foundry.helm import trail as T                                             # noqa: E402

LAT = ROOT / "foundry" / "results" / "lattice"
DB = LAT / "observatory.db"
LEDGER = LAT / "observatory_reservation.jsonl"
TRAIL = LAT / "wave_trail.jsonl"
BANK = ROOT / "docs" / "findings" / "sounding-survey-banked-questions.md"

# THE WAVE ID IS THE NEXT UNUSED ONE, never a constant to edit. A wave that has been recorded is
# history: when the screens change under a ruling, the answer is a NEW wave, not a re-run that
# overwrites what the engine actually saw at the time. Kill 3 is about exactly this.
WAVE = f"wave-{len(T.wave_ids(TRAIL)) + 1}"


def mde_for(cand, frontier):
    if cand["kind"] == "co-movement":
        return S.mde_correlation(frontier["n_clusters"])
    if cand["kind"] == "association":
        return S.mde_association(frontier["n_cells"])
    return None


def main() -> int:
    T.assert_kill3(TRAIL)                       # a reconstructed event halts the wave before it opens
    con = sqlite3.connect(DB)
    con.execute("PRAGMA foreign_keys = ON")
    reserved = RES.reserved_rows(LEDGER)
    frontier = S.frontier_expectation(con, reserved)

    print(f"HELM {WAVE} — sweeping the published database\n")
    cands, prov = SW.sweep(con, BANK)
    hashes = SW.db_hashes(con, DB)
    T.emit(TRAIL, WAVE, "sweep", key=f"{WAVE}:sweep",
           generator_version=prov["generator_version"], n_candidates=prov["n_candidates"],
           by_kind=prov["by_kind"], db_sha256=hashes["db_sha256"], sources=hashes["sources"],
           candidate_set_sha256=hashlib.sha256(SW.canonical(cands).encode()).hexdigest(),
           forking_paths_denominator=("the full candidate count is preserved forever — every "
                                      "correction downstream is computed from this enumeration, not "
                                      "estimated from a number someone remembers"))
    print(f"  swept {prov['n_candidates']} candidates  {prov['by_kind']}")
    print(f"  db {hashes['db_sha256'][:16]}\n")

    prohibited = set()
    if con.execute("SELECT COUNT(*) FROM catalog WHERE seal_prohibited_at_v1 = 1").fetchone()[0]:
        prohibited = {"kink_step", "kink_sharpness"}     # the catalog's OWN flag governs (§3.1)

    print(f"  frontier: {frontier['n_clusters']} reserved row(s) -> ~{frontier['n_cells']} cells "
          f"({', '.join(frontier['reserved'])})")
    screened = S.run(cands, con, frontier, prohibited)
    counts = {d: sum(1 for r in screened if r["screen_disposition"] == d) for d in S.DISPOSITIONS}
    rules = {}
    for r in screened:
        if r["screen_rule"]:
            rules[r["screen_rule"]] = rules.get(r["screen_rule"], 0) + 1
    held = [r for r in screened if r["screen_disposition"] == "HELD"
            and r.get("gap_in_reserved_rows") is not None]
    held.sort(key=lambda r: r["gap_in_reserved_rows"])
    nearest = held[0]["gap_in_reserved_rows"] if held else None
    T.emit(TRAIL, WAVE, "screen", key=f"{WAVE}:screen",
           counts=counts, by_rule=rules,
           hold_queue_nearest_gap_in_reserved_rows=nearest,
           hold_queue_gaps=[{"candidate_id": h["candidate_id"], "statistic": h["statistic"],
                             "disclosed": h["disclosed"],
                             "required_clusters": h.get("required_clusters"),
                             "gap_in_reserved_rows": h["gap_in_reserved_rows"]} for h in held[:20]],
           frontier=frontier, seal_prohibited=sorted(prohibited),
           floors={"alpha": S.ALPHA, "power": S.POWER,
                   "min_frontier_clusters": S.MIN_FRONTIER_CLUSTERS,
                   "min_frontier_cells": S.MIN_FRONTIER_CELLS},
           rejections_preserved=("screened-out candidates are what a future auditor needs to verify "
                                 "the correction was honest, so they are kept, not summarised"))
    print(f"  screened: {counts}  by rule {rules}\n")

    ranked = SL.rank(screened, frontier, mde_for)
    by_id = {c["candidate_id"]: c for c in ranked}
    rows = []
    for r in screened:
        rows.append({**by_id.get(r["candidate_id"], r), "wave": WAVE})
    outc = LAT / f"helm_{WAVE.replace('-', '')}_candidates.jsonl"
    with outc.open("w") as fh:
        for r in sorted(rows, key=lambda z: z["candidate_id"]):
            fh.write(json.dumps(r, sort_keys=True) + "\n")

    T.emit(TRAIL, WAVE, "slate", key=f"{WAVE}:slate",
           n_slated=len(ranked), family_size=len(ranked),
           ranked=[{"rank": c["slate_rank"], "candidate_id": c["candidate_id"],
                    "statistic": c["statistic"], "disclosed": c["disclosed"],
                    "rank_score": c["rank_score"]} for c in ranked],
           candidates_artifact=outc.name,
           as_displayed=("every disclosed prior recorded exactly as it was shown at ruling time"))

    doc = {"schema": "helm-slate/v1", "wave": WAVE,
           "STATUS": "AWAITING OWNER RULING — nothing here is sealed, nothing here is a claim",
           "constitution": ["the machine proposes; the frontier adjudicates",
                            "the owner rules every seal"],
           "sweep": prov, "db": hashes, "frontier": frontier,
           "screen_counts": counts, "screen_rules": rules,
           "declared_floors": {"alpha": S.ALPHA, "power": S.POWER,
                               "min_frontier_clusters": S.MIN_FRONTIER_CLUSTERS,
                               "min_frontier_cells": S.MIN_FRONTIER_CELLS,
                               "pinned": "in foundry/helm/screens.py before this wave ran"},
           "family": {"size": len(ranked), "correction": "Holm-Bonferroni at FWER 0.05",
                      "enumerated_denominator": prov["n_candidates"]},
           "slate": ranked,
           "hold_queue": {
               "n_with_measurable_gap": len(held),
               "nearest_gap_in_reserved_rows": nearest,
               "how_it_resurfaces": ("held candidates carry the frontier size that would clear them; "
                                     "the db's hold_queue view is the standing query, so growth in "
                                     "the reservation revives them without anyone remembering they "
                                     "existed"),
               "entries": [{"candidate_id": h["candidate_id"], "statistic": h["statistic"],
                            "disclosed": h["disclosed"],
                            "required_clusters": h.get("required_clusters"),
                            "gap_in_reserved_rows": h["gap_in_reserved_rows"]} for h in held]},
           "owner_slot": SL.OWNER_SLOT,
           "candidates_artifact": outc.name}
    outs = LAT / f"helm_{WAVE.replace('-', '')}_slate.json"
    outs.write_text(json.dumps(doc, indent=1) + "\n")

    print(f"  SLATE — {len(ranked)} candidate(s) ranked, family size {len(ranked)}\n")
    for c in ranked:
        print(f"   {c['slate_rank']:>2}. [{c['kind']}] {c['statistic']}")
        print(f"       disclosed {c['disclosed']}   MDE {c['frontier_mde']}   "
              f"novelty {c['novelty']}   score {c['rank_score']}")
        print(f"       bet: {c['sealed_bet']}")
        print(f"       family cost: Holm threshold {c['family_cost']}")
    if not ranked:
        print("   (empty)\n")
    print(f"\n  HOLD QUEUE — {len(held)} candidate(s) carry a measurable power gap; nearest needs "
          f"{nearest} more reserved row(s)\n")
    for h in held[:8]:
        print(f"   +{h['gap_in_reserved_rows']:<4} rows   |rho|={abs(h['disclosed']):.3f}  "
              f"needs {h['required_clusters']} clusters   {h['statistic']}")
    print(f"\n  wrote {outs.name} and {outc.name}")
    print(f"  trail {TRAIL.name}: {len(T.read(TRAIL))} event(s)")
    con.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
