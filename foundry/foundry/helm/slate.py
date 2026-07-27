"""The slate — Helm §4. A ranked list for the owner, never a launched experiment.

WHAT A SLATE IS. Helm ends a wave cycle here and stops. The owner rules SEAL / HOLD / KILL per candidate
in one sitting, and a ruled seal mints its prereg mechanically from the candidate record — the prereg IS
the candidate plus the ruling. Nothing below decides anything.

RANKED BY INFORMATION-PER-SEAL: disclosed effect x frontier power x novelty. Ties break toward candidates
that discriminate between the live mechanism hypotheses (currently coherence vs unknown), because a seal
that separates two standing explanations is worth more than one that adds a decimal to either.

THE DIRECTION IS FIXED FROM THE DISCLOSED PRIOR, and that is the whole reason a disclosed prior is worth
keeping. The in-sample number cannot be a finding, but it can fix the sign of a bet that will be scored
somewhere it could have come out either way. A slate entry whose direction were chosen after the frontier
existed would be a story with a p-value.
"""
from __future__ import annotations

COHERENCE_DESCRIPTORS = {"overlap_ref", "overlap_slope", "bimodality_max"}


def novelty(cand, bank):
    """Mechanical novelty against the standing question bank. No judgement call, and crude on purpose:
    a novelty score that required reading would reintroduce the eyeball the sweep exists to remove."""
    text = " ".join(b["statistic"].lower() for b in bank)
    ds = [d for d in (cand.get("descriptors") or [])]
    if not ds:
        return 1.0
    hits = sum(1 for d in ds if d.replace("_", " ") in text or d in text)
    return 1.0 if hits == 0 else max(0.3, 1.0 - 0.35 * hits)


def power_proxy(cand, frontier, mde):
    """How far the disclosed effect clears the frontier's MDE. Bounded to [0, 1].

    A candidate reaching this function has already passed the power screen, so `mde` is defined and
    `|disclosed| >= mde`. Returning 0 for a missing MDE would silently flatten a whole slate to a
    single tied score — which is a ranking that has stopped ranking — so the missing case raises
    instead of scoring."""
    d = cand.get("disclosed")
    if d is None or mde is None or mde <= 0:
        raise ValueError(
            f"candidate {cand['candidate_id']} reached ranking without a defined MDE; a slated "
            f"candidate must have cleared the power screen, so this is a screen/rank disagreement")
    return max(0.0, min(1.0, (abs(d) - mde) / mde + 0.5))


def sealed_bet(cand):
    """The bet the candidate would become. Direction fixed from the disclosed prior."""
    d = cand.get("disclosed")
    if cand["kind"] == "co-movement":
        sign = "negative" if (d or 0) < 0 else "positive"
        return (f"on the reserved frontier rows, the rank correlation between "
                f"{cand['descriptors'][0]} and {cand['descriptors'][1]} is {sign}, "
                f"clustered at the problem level")
    if cand["kind"] == "association":
        return (f"on the reserved frontier rows, {cand['descriptors'][0]} is associated with "
                f"charge `{cand.get('charge')}` at V > 0, direction fixed by the disclosed table")
    if cand["kind"] == "anomaly":
        return (f"the frontier reproduces the disclosed extremal behaviour of "
                f"{', '.join(cand['descriptors']) or 'the cell'}")
    return "no typed bet — the candidate needs a statistic first"


def rank(screened, frontier, mde_for):
    """Rank the SLATED candidates. Held and rejected candidates keep their records but do not rank."""
    bank = [c for c in screened if c["kind"] == "bank-import"]
    out = []
    for c in screened:
        if c["screen_disposition"] != "SLATED":
            continue
        mde = mde_for(c, frontier)
        nov = novelty(c, bank)
        pw = power_proxy(c, frontier, mde)
        eff = abs(c.get("disclosed") or 0.0)
        score = eff * pw * nov
        out.append({**c,
                    "novelty": round(nov, 3),
                    "frontier_mde": round(mde, 4) if mde else None,
                    "power_proxy": round(pw, 3),
                    "rank_score": round(score, 6),
                    "sealed_bet": sealed_bet(c),
                    "discriminates_mechanism": bool(
                        set(c.get("descriptors") or []) & COHERENCE_DESCRIPTORS),
                    "family_cost": c.get("holm_threshold_if_sealed")})
    out.sort(key=lambda c: (-c["rank_score"], not c["discriminates_mechanism"], c["candidate_id"]))
    for i, c in enumerate(out, 1):
        c["slate_rank"] = i
    return out


OWNER_SLOT = {
    "candidate_id": "owner-originated",
    "kind": "owner-originated",
    "how_it_enters": ("free-text, ruled with the same discipline as an enumerated candidate and scored "
                      "on the same frontier — but carrying NO enumeration denominator, because it was "
                      "not enumerated. Helm cannot invent the feasible-region reframe; the slot exists "
                      "so that the engine asking faster never becomes the only thing that asks."),
    "family_accounting": ("an owner-originated seal joins the wave's declared family and pays the same "
                          "Holm cost as any other member"),
}
