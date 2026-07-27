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
