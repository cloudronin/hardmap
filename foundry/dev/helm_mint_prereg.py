#!/usr/bin/env python3
"""Mint a prereg from a ruled candidate — Helm §4: THE PREREG IS THE CANDIDATE PLUS THE RULING.

Nothing is authored here. The bet, the null, the direction, the family cost and the forking-paths
denominator all come from the candidate record the sweep produced and the ruling the owner gave. A
prereg written by hand from a slate would be a second copy of the candidate, free to disagree with it.
"""
import hashlib, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from foundry.helm import trail as T                                             # noqa: E402

LAT = ROOT / "foundry" / "results" / "lattice"
PREREG = ROOT / "foundry" / "results" / "prereg"
TRAIL = LAT / "wave_trail.jsonl"
WAVE = "wave-5"

RULINGS = {
    "SEAL": {"statistic_contains": "rho(overlap_ref, r_ref) over optimization"},
    "HOLD-redesign": {"statistic_contains": "Cramer's V(bimodal_flag, charge=landscape)"},
}

RIDERS = {
    "verdict_vocabulary": (
        "CO-MOVEMENT, NOT MECHANISM. A confirm says these two move together on fresh ground. It does "
        "not say why, and the bet claims no mechanism."),
    "size_is_a_variable_of_interest_here": (
        "`r_ref` IS the size descriptor, and that is deliberate. The candidates killed at the wave-4 "
        "sitting paired size with quantities size MECHANICALLY INFLATES — arithmetic correlating with "
        "its own shadow. `overlap_ref` carries no small-sample bias: mean pairwise agreement is "
        "unbiased at any r >= 2, since two solutions can disagree everywhere and nothing forces "
        "coherence at small r. So the association is empirical, and partialing r out would condition "
        "the question on itself."),
    "theoretical_reading_acknowledged_in_advance": (
        "the freezing story PREDICTS this sign — smaller regions more internally agreed is its own "
        "covariance, and the hardening figure showed it on one row. A confirm is therefore "
        "CONSISTENCY-WITH-THEORY, not surprise, and this sentence exists so the finding cannot later "
        "be reported as the stronger thing."),
}


def main() -> int:
    cands = [json.loads(x) for x in
             (LAT / "helm_wave5_candidates.jsonl").read_text().splitlines() if x.strip()]
    sealed = next(c for c in cands
                  if RULINGS["SEAL"]["statistic_contains"] in c["statistic"])
    held = next(c for c in cands
                if RULINGS["HOLD-redesign"]["statistic_contains"] in c["statistic"])

    n = 1 + max([int(p.stem.split("_v")[-1]) for p in PREREG.glob("prereg_v*.json")] or [0])
    doc = {
        "prereg_id": f"prereg_v{n}", "schema": "helm-minted-prereg/v1",
        "minted_from": {"wave": WAVE, "candidate_id": sealed["candidate_id"],
                        "generator_version": sealed.get("sweep_total") and "sweep/v5",
                        "how": "Helm §4 — the prereg IS the candidate plus the ruling; nothing authored"},
        "sealed_bet": sealed["sealed_bet"],
        "direction": "NEGATIVE — fixed from the disclosed prior, not chosen after the fact",
        "disclosed_prior": sealed["disclosed"],
        "disclosed_prior_is_not_evidence": ("the database is published ground; this number fixes the "
                                            "bet's SIGN and is never itself a finding"),
        "statistic": sealed["statistic"],
        "null": sealed["frontier_null"],
        "population": "the reserved frontier rows' optimization clusters, on release",
        "scoring": "ONCE, per the standing law, when the reservation releases",
        "family": {"size": 2, "correction": "Holm-Bonferroni at FWER 0.05",
                   "this_member_threshold": sealed.get("family_cost"),
                   "enumerated_denominator": sealed["sweep_total"],
                   "siblings_at_birth": sealed["n_siblings"]},
        "frontier_mde_at_mint": sealed.get("frontier_mde"),
        "riders": RIDERS,
        "generating_query": sealed["generating_query"],
        "STATUS": "SEALED BY THE ACT OF COMMITTING THIS FILE",
    }
    payload = json.dumps(doc, sort_keys=True, separators=(",", ":"))
    doc["PREDICTION_HASH"] = hashlib.sha256(payload.encode()).hexdigest()
    out = PREREG / f"prereg_v{n}.json"
    out.write_text(json.dumps(doc, indent=1) + "\n")

    T.emit(TRAIL, WAVE, "ruling", key=f"{WAVE}:ruling", owner_originated=True, sitting="2026-07-27",
           per_candidate=[
               {"candidate_id": sealed["candidate_id"], "statistic": sealed["statistic"],
                "ruling": "SEAL", "prereg": out.name,
                "why": ("overlap_ref carries no small-sample bias — mean pairwise agreement is unbiased "
                        "at any r >= 2 — so pairing it with size is an EMPIRICAL question, not "
                        "arithmetic correlating with its own shadow")},
               {"candidate_id": held["candidate_id"], "statistic": held["statistic"],
                "ruling": "HOLD-redesign",
                "why": ("bimodal_flag derives from size-inflated raw BC and the landscape charge "
                        "plausibly tracks r directly, so the association could be entirely r-mediated. "
                        "V = 0.407 against MDE 0.404 is the thin edge an artifact shows."),
                "re_enters_as": "the excess-based flag, or r-stratified"}],
           screens_gained=("coupling travels the DERIVATION GRAPH — a descriptor derived from a "
                           "size-coupled one is size-coupled. The screens carried coupling as metadata "
                           "on descriptors, so a flag inheriting it through derivation was invisible."))
    T.emit(TRAIL, WAVE, "hash", key=f"{WAVE}:hash", prereg=out.name,
           prediction_hash=doc["PREDICTION_HASH"],
           sealed_before="any frontier row is captured — the reserved rows have no frames",
           note="the hash is over the prereg's own payload; the file IS the seal")

    print(f"MINTED {out.name}\n")
    print(f"  bet       : {doc['sealed_bet']}")
    print(f"  direction : {doc['direction'].split(' —')[0]}   prior {doc['disclosed_prior']:.4f}")
    print(f"  null      : {doc['null'][:88]}")
    print(f"  family    : size 2, Holm {doc['family']['this_member_threshold']}, "
          f"denominator {doc['family']['enumerated_denominator']}")
    print(f"  HASH      : {doc['PREDICTION_HASH'][:32]}...")
    print(f"\n  wave-5 ruling recorded: 1 SEAL, 1 HOLD-redesign")
    return 0


if __name__ == "__main__":
    sys.exit(main())
