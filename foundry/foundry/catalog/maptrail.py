"""The maptrail — Helm §7.1. Provenance of the territory, as data, inside the db it produced.

WHAT IT IS FOR. Git records that bytes changed. The maptrail records what changed IN THE DOMAIN'S
VOCABULARY, for an end user who has the database and no commits. `SELECT * FROM maptrail WHERE problem = ?
ORDER BY at` is the biography of a cell: when it entered, under what authority, what corrected it, what
was retracted near it.

EMITTED AT EVENT TIME BY THE OPERATION THAT PERFORMS IT. This is Helm Kill 3 extended verbatim to the
maptrail, and it is the whole design constraint: a trail composed afterwards from what someone remembers
is chat-is-not-an-artifact wearing a table's clothes. So `emit` is called from inside the freeze, the
expansion, the exclusion — not from a reporting pass that runs later and reconstructs them.

THE ONE EXCEPTION IS LABELLED IN EVERY RECORD IT TOUCHES. The program has history that predates this
module, and that history is worth having. It is imported once, and every imported record carries
`reconstructed: true`. History written late is fine; history written late and presented as contemporaneous
is not. A consumer can always exclude the reconstructed prefix with a WHERE clause, which is exactly why
the flag is a column rather than a sentence in a README.

IDEMPOTENT ON `key`. Emitters live inside scripts, and scripts get re-run. Without a stable key, a second
run of a build appends a second copy of an event that happened once, and the trail starts overcounting the
history it exists to record.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

EVENTS = {
    "freeze":     "an artifact reached a hash and was sealed at it",
    "expansion":  "rows or cells were added, under a named admission authority",
    "erratum":    "a cell's value was corrected — old and new both recorded",
    "retraction": "a finding was withdrawn; the preserved original is pointed at, never deleted",
    "annotation": "metadata event touching NO measured value — flag corrections, drift markers",
    "version":    "a schema succession under the F4 law (a changed rule is a new version)",
    "exclusion":  "rows typed out of a population, with reasons",
}


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def read(path: Path):
    if not path.exists():
        return []
    return [json.loads(x) for x in path.read_text().splitlines() if x.strip()]


def emit(path: Path, event: str, key: str, *, reconstructed: bool = False, **payload) -> dict:
    """Append one maptrail record. Returns the record (existing or new)."""
    if event not in EVENTS:
        raise ValueError(f"unknown maptrail event {event!r}; known: {sorted(EVENTS)}")
    for rec in read(path):
        if rec["key"] == key:
            return rec
    rec = {"event": event, "key": key, "at": _now(), "reconstructed": reconstructed, **payload}
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as fh:
        fh.write(json.dumps(rec) + "\n")
    return rec


# ── OPENNESS, as a replayed state rather than an inferred one (ruled 2026-07-27) ─────────────────────
# The trail says what HAPPENED. It never said what remains OUTSTANDING, so "what is open" was inferred
# by a reader who knew the story — exactly the reconstruction cost a compiled front page exists to
# remove. A generator over records that cannot say what is open would be an inference layer wearing a
# compiler's clothes.
#
# APPEND-ONLY, SO DISCHARGE IS A NEW RECORD. Never an edit to the item it closes — the same shape as the
# reservation ledger's reserve/release, and for the same reason: replay is the state, so there is no
# mutable field for drift to hide in.

def open_item(path: Path, key: str, title: str, why: str, sequence: int = 99,
              pointers=None, reconstructed: bool = False) -> dict:
    """Declare outstanding work. `sequence` is the ORDER DECLARED BY THE PASS THAT OPENS IT — the same
    principle as `supersedes`: the party that knows, states it; nothing downstream infers."""
    return emit(path, "annotation", key=f"open:{key}", reconstructed=reconstructed,
                opens=key, title=title, why=why, sequence=sequence,
                pointers=list(pointers or []), touches_no_measured_value=True)


def discharge(path: Path, key: str, by: str, note: str = "") -> dict:
    """Close an open item. A new record pointing at the original, never an edit to it."""
    return emit(path, "annotation", key=f"discharged:{key}", discharges=key,
                discharged_by=by, note=note, touches_no_measured_value=True)


def resequence(path: Path, key: str, to: int, by: str, why: str) -> dict:
    """Re-prioritise an open item. A NEW record pointing at the original — the same shape as discharge,
    and for the same reason: replay is the state, so there is no mutable field for drift to hide in.

    THE ALTERNATIVE WOULD HAVE BEEN A LIE. Without this, moving an item up means discharging it and
    opening a replacement — which writes "closed" into the trail for something that was never done, and
    loses the original's date and reasoning. Priority changing is a fact about the item, not the end of
    it, and the record should say which.

    The ORIGINAL sequence stays readable in the opening record. What changed, when, and on whose word
    is the thing being added.
    """
    return emit(path, "annotation", key=f"resequenced:{key}:{to}", resequences=key,
                to_sequence=to, by=by, why=why, touches_no_measured_value=True)


def open_items(path: Path):
    """Replay: everything opened, minus everything discharged, at its LATEST declared sequence.

    Priority is replayed exactly as openness is. A later `resequence` record wins over the opening
    one — and over an earlier resequence — so the order on the front page is the order most recently
    declared, without any record ever being edited."""
    opened, closed, moved = {}, set(), {}
    for rec in read(path):
        if rec.get("opens"):
            opened[rec["opens"]] = rec
        if rec.get("discharges"):
            closed.add(rec["discharges"])
        if rec.get("resequences"):
            moved[rec["resequences"]] = rec
    live = []
    for k, r in opened.items():
        if k in closed:
            continue
        if k in moved:
            r = {**r, "sequence": moved[k]["to_sequence"],
                 "resequenced_from": r.get("sequence"), "resequenced_why": moved[k]["why"]}
        live.append(r)
    return sorted(live, key=lambda z: (z.get("sequence", 99), z["opens"]))
