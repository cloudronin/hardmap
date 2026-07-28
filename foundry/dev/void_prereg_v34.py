#!/usr/bin/env python3
"""Void prereg_v34 — a seal minted on mis-computed power, voided before any frame existed.

THE DISTINCTION THIS TURNS ON. A seal that FAILS was validly sealed and honestly scored; a seal that
NEVER VALIDLY EXISTED had a false claim in its own paperwork at mint time. prereg_v34 cleared the power
screen against 12 frontier clusters for a bet scoped to `optimization`, a family holding 3 reserved
rows. The power claim was false when it was made — not falsified by later events — so the seal is
VOIDED rather than held or scored.

THE BYTES ARE NOT TOUCHED. `prereg_v34.json` stays exactly as it was sealed, hash and all. Voiding is a
new record pointing at a preserved original, never an edit — the retraction-preservation principle, which
is what lets a reader tell a corrected mistake from one that never happened.

NOTHING WAS CONTAMINATED. No release record was written, no generator for a reserved row exists, no frame
was captured. The frontier is intact at 14 and the candidate returns to the sweep under the corrected
screen with an honest revival condition.
"""
import hashlib, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from foundry.catalog import maptrail as M                                       # noqa: E402
from foundry.helm import screens as S                                           # noqa: E402
from foundry.helm import trail as T                                             # noqa: E402

LAT = ROOT / "foundry" / "results" / "lattice"
PREREG = ROOT / "foundry" / "results" / "prereg" / "prereg_v34.json"
WT = LAT / "wave_trail.jsonl"
MT = LAT / "maptrail.jsonl"


def main() -> int:
    doc = json.loads(PREREG.read_text())
    before = hashlib.sha256(PREREG.read_bytes()).hexdigest()
    need = S.required_clusters(abs(doc["disclosed_prior"]))

    reason = {
        "what_was_wrong": (
            "the power screen computed MDE on the frontier's TOTAL cluster count (12) for a bet scoped "
            "to `optimization`, a family holding 3 reserved rows. The candidate cleared power against "
            "nine clusters its statistic could never read."),
        "why_void_and_not_hold": (
            "a seal's validity rests on its mint-time screens being computed correctly ABOUT THE BET "
            "ACTUALLY SEALED. This one's power claim was false when made, not falsified by later "
            "events. Holding it would leave a standing bet whose own paperwork misstates its strength."),
        "why_void_and_not_score": (
            f"3 clusters cannot carry the statistic at all — Fisher's z needs n - 3 > 0, so the MDE at "
            f"3 is undefined. Scoring was not an available option and is recorded as closed rather "
            f"than left implicit."),
        "contaminated": "NOTHING — no release record, no generator, no frame. The frontier is intact.",
        "mint_time_mde_claimed": doc["frontier_mde_at_mint"],
        "consumable_clusters_at_mint": 3,
        "honest_requirement": f"{need} reserved optimization clusters for |rho| = "
                              f"{abs(doc['disclosed_prior']):.4f}",
        "screen_fixed": ("the consumable-population rule — every candidate's MDE computes on the "
                         "population its statistic can actually consume, written in general form so "
                         "the next scoping axis inherits it without a fresh incident"),
        "candidate_future": ("returns to the sweep as HELD-power under the corrected MDE, with a true "
                             "revival number. Re-mints when the family population genuinely clears "
                             "power: same candidate record, same disclosed prior, same riders."),
    }

    T.emit(WT, "wave-5", "ruling", key="wave-5:ruling:void-prereg-v34",
           owner_originated=True, sitting="2026-07-27 (the prereg_v34 pin)",
           candidate_id=doc["minted_from"]["candidate_id"],
           prereg="prereg_v34.json", ruling="VOID",
           prereg_sha256_preserved=before,
           prediction_hash_as_sealed=doc["PREDICTION_HASH"], **reason)

    M.emit(MT, "retraction", key="retraction:prereg-v34",
           artifact="prereg_v34.json", species="seal minted on mis-computed power",
           preserved_original=("prereg_v34.json is UNTOUCHED — same bytes, same hash. Voiding is a new "
                               "record pointing at a preserved original, never an edit."),
           sha256=before, prediction_hash=doc["PREDICTION_HASH"],
           voided_before_any_frame_existed=True, **reason)

    after = hashlib.sha256(PREREG.read_bytes()).hexdigest()
    assert before == after, "the prereg was modified — voiding must never edit the sealed bytes"

    print("VOIDED prereg_v34\n")
    print(f"  claimed MDE at mint : {doc['frontier_mde_at_mint']}  (12 clusters — the frontier TOTAL)")
    print(f"  consumable clusters : 3  (family = optimization)")
    print(f"  honest requirement  : {need} reserved optimization clusters")
    print(f"  sealed bytes        : UNTOUCHED, sha {before[:16]}")
    print(f"  contaminated        : nothing — no release, no generator, no frame")
    return 0


if __name__ == "__main__":
    sys.exit(main())
