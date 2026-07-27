"""The wave trail — Helm §7. The observatory's logbook, emitted at event time.

KILL 3 IS THE DESIGN CONSTRAINT: "any wave event found in the trail that was not emitted at event time
(reconstructed, backfilled, or absent) halts the wave." So these emitters are called from inside the
sweep, the screen, the slate — they are part of each stage's implementation. A trail assembled afterwards
from what a run remembers is chat-is-not-an-artifact wearing a table's clothes, and it is exactly what
this file exists to prevent.

WHAT MAKES THE TRAIL THE NOVEL OBJECT is not the events that succeeded. It is the REJECTED-CANDIDATE
LEDGER: every question the data could have supported, why each was screened, held, sealed or killed, and
the complete enumerated denominator behind every correction. A multiple-comparisons correction computed
from an enumeration nobody can audit is a number asking to be trusted. This publishes the garden of
forking paths as a map of the garden.

So `screen` records preserve REJECTIONS, not just survivors, and `sweep` records preserve the full
candidate count forever — including the candidates no human will ever see.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

COMPONENT_VERSION = "helm/v1"

EVENTS = {
    "sweep":        "generator version; catalog/db hashes swept; FULL candidate count",
    "screen":       "per-candidate disposition with the rule that fired — rejections preserved",
    "slate":        "the ranked list as shown, every disclosed prior as-displayed at ruling time",
    "ruling":       "per candidate SEAL / HOLD / KILL, dated; owner-originated entries marked",
    "hash":         "prediction files with commit ids",
    "capture":      "which frontier rows; reservation release time",
    "score":        "verdicts with artifact pointers",
    "prior_update": "what the generator learned, stated as the delta",
}


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def read(path: Path):
    if not path.exists():
        return []
    return [json.loads(x) for x in path.read_text().splitlines() if x.strip()]


def emit(path: Path, wave: str, event: str, key: str,
         component_version: str = COMPONENT_VERSION, **payload) -> dict:
    """Append one wave event. Idempotent on `key` so a re-run does not double-record a single event."""
    if event not in EVENTS:
        raise ValueError(f"unknown wave event {event!r}; known: {sorted(EVENTS)}")
    for rec in read(path):
        if rec["key"] == key:
            return rec
    rec = {"wave": wave, "event": event, "key": key, "at": _now(),
           "component_version": component_version, **payload}
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as fh:
        fh.write(json.dumps(rec) + "\n")
    return rec


def assert_kill3(path: Path) -> None:
    """Kill 3, mechanical. A wave event carrying `reconstructed` halts the wave.

    The maptrail permits a labelled one-time backfill of history that predates it; the WAVE trail does
    not, because a wave is a process this machinery runs end to end. There is no history for it to
    import — if a wave event was not emitted when it happened, it did not happen."""
    bad = [r["key"] for r in read(path) if r.get("reconstructed")]
    if bad:
        raise RuntimeError(
            f"HELM KILL 3 — wave event(s) {bad} are reconstructed rather than emitted at event time. "
            f"All open waves halt and the incident enters the ledger. The logbook is load-bearing or "
            f"it is nothing.")


def wave_ids(path: Path):
    seen = []
    for r in read(path):
        if r["wave"] not in seen:
            seen.append(r["wave"])
    return seen
