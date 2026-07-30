"""Roster eligibility — computed, never quoted.

THE SPECIES THIS CURES, with two exhibits. Twice in two sessions a roster figure was quoted from a
subset of the predicates a roster actually needs, and twice it reached a ruling before anyone checked:
the owner weighted a batch toward sat-csp REACH-subset rows that do not exist, and I reported 17 graph
rows "unbuilt and unreserved" when 7 were buildable. Neither was carelessness. Both were a human
assembling a population by hand from predicates they held in their head — the hand-enumerated-population
failure, at the roster layer instead of the candidate layer.

The cure is the same one the sweep already applies to candidates: DERIVE THE POPULATION. Every screen a
roster requires is declared here once, applied in order, and the number comes out the other end with a
reason attached to every row it dropped.

SCREENS ARE DECLARED, ORDERED, AND EACH SAYS WHY. A row is not simply in or out; it is out FOR A NAMED
REASON, and the per-screen counts are reported so a reader can see where a pool went rather than
comparing two totals and guessing. A screen that silently drops rows produces exactly the confident
wrong number this module exists to stop.

DISPOSITIONS ARE READ FROM THE TRAIL, NOT HARDCODED. A row excluded at birth, blocked pending a
reformulation, or cleared to re-enter is in a state somebody RULED, and rulings live in the maptrail.
Replaying them means the view reflects the current dispositions without anyone editing this file, and it
means a disposition can be revisited by appending rather than by patching code.
"""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from . import maptrail as M
from . import reservation as RES

# A row's ruled state, replayed from `disposition:<row>` records. Anything not BLOCKED is eligible as
# far as this layer is concerned; the screens below still apply.
BLOCKING_STATES = {"BLOCKED"}


def dispositions(trail: Path) -> dict:
    """row -> the latest ruled disposition. Later records win, nothing is edited."""
    out = {}
    for rec in M.read(trail):
        if rec.get("disposition_row"):
            out[rec["disposition_row"]] = rec
    return out


def eligible(lat: Path, family: str | None = None, reach_class: str = "REACH-subset") -> dict:
    """The buildable population, with every drop attributed to the screen that made it."""
    con = sqlite3.connect(lat / "observatory.db")
    trail = lat / "maptrail.jsonl"
    try:
        q = "SELECT problem_id FROM problems WHERE reach_class = ?"
        args = [reach_class]
        if family:
            q += " AND family = ?"
            args.append(family)
        pool = [r for (r,) in con.execute(q + " ORDER BY 1", args)]
        built = {r[0] for r in con.execute("SELECT DISTINCT problem_id FROM frames")}
        no_ramp = {r[0] for r in con.execute(
            "SELECT problem_id FROM problems WHERE ramp_parameter IS NULL")}
    finally:
        con.close()

    reserved = RES.reserved_rows(lat / "observatory_reservation.jsonl")
    amb = json.loads((lat / "observatory_ambient_census.json").read_text())
    confounded = set(amb.get("confounded") or [])
    audit = {r["problem_id"]: r["verdict"] for r in
             json.loads((lat / "region_formulation_audit.json").read_text())["rows"]}
    disp = dispositions(trail)

    excluded_at_birth = {}
    for p in sorted(lat.glob("observatory_batch*_panels.json")):
        n = int("".join(c for c in p.stem.split("batch")[1] if c.isdigit()))
        for e in json.loads(p.read_text()).get("excluded_at_birth", []):
            excluded_at_birth[e["row"]] = {"batch": n, "kind": e.get("kind"),
                                           "reason": e.get("reason")}

    # ORDER MATTERS: the first screen a row fails is the reason it is reported under, so the cheapest
    # and most decisive come first. `built` before everything, because a built row is not a candidate
    # for any reason and reporting it as region-blocked would be noise.
    SCREENS = [
        ("built", lambda r: r in built,
         "already has frames — re-rostering double-counts it in the catalog"),
        ("reserved", lambda r: r in reserved,
         "declared frontier: reserved rows are NEVER captured"),
        ("ruled-blocked", lambda r: disp.get(r, {}).get("state") in BLOCKING_STATES,
         "a standing ruling blocks it; see its disposition record for the re-entry route"),
        ("ambient-confounded", lambda r: r in confounded,
         "the ground set IS the dial — the ramp cannot move without moving the ambient"),
        ("region-unverified", lambda r: audit.get(r) in ("WRONG-REGION", "VARIANT-REGION"),
         "the region formulation audit found the built region is not the row's region"),
        ("no-declared-ramp", lambda r: r in no_ramp,
         "no ramp parameter declared — there is no dial to walk"),
        ("excluded-at-birth", lambda r: r in excluded_at_birth and r not in disp,
         "a previous batch attempted it and the build refused; needs a disposition before re-entry"),
    ]

    dropped, counts, out = {}, {name: 0 for name, _, _ in SCREENS}, []
    for r in pool:
        for name, pred, why in SCREENS:
            if pred(r):
                dropped[r] = {"screen": name, "why": why}
                if r in excluded_at_birth:
                    dropped[r]["prior_exclusion"] = excluded_at_birth[r]
                if r in disp:
                    dropped[r]["disposition"] = {k: v for k, v in disp[r].items()
                                                 if k in ("state", "why", "re_entry")}
                counts[name] += 1
                break
        else:
            out.append(r)

    return {
        "family": family, "reach_class": reach_class,
        "pool": len(pool), "eligible": out, "n_eligible": len(out),
        "dropped": dropped, "dropped_by_screen": counts,
        "screens": [{"screen": n, "why": w} for n, _, w in SCREENS],
        "column_provenance": ("reach_class as resolved by the declared typing chain — not the base "
                              "census column, in which 51 rows carried a superseded answer"),
    }
