"""The frontier reservation — Helm §5, compiled into machinery.

WHAT THIS EXISTS FOR. Helm generates candidates by sweeping the published database. Anything found in
published ground is a `disclosed-prior`, never a finding (Helm §0.1). So the program needs standing
out-of-sample territory, and the fan-out manufactures it as a byproduct: a declared fraction of every
batch is RESERVED and does not enter the disclosed record.

THE ONE READING THAT HAD TO BE RESOLVED, stated here because it is a decision and not a detail. Helm §5
says reserved rows are "captured last in the batch" and withheld until predictions are hashed; Helm §0.1
says predictions are "hashed before their frames exist". Those differ in strength. Under §5 the frames
exist and blindness rests on a guard; under §0.1 the frames do not exist and blindness is physics. This
module implements §0.1 — THE CONSTITUTION, which the spec marks binding — so a reserved row is DECLARED
AND NOT CAPTURED. `capture last` is honoured maximally: last means after the wave's predictions are
sealed, not merely last within a run.

The asymmetry decides it independently of which clause governs. Declaring-then-capturing-later can always
be relaxed into capture-now if the owner rules the other way; capture-now can never be taken back, because
frozen bytes are forever and ground once seen cannot be unseen. The recoverable reading wins.

THE SELECTION IS OUTCOME-BLIND BY CONSTRUCTION, not by discipline. Rows are ordered by
`sha256(f"{batch}:{row}")` and the low `fraction` taken. Nothing measured exists at declaration time —
these rows have not been built — so there is no outcome for the rule to see even in principle. The rule is
declared, the roster hashed, and both are on record before a single generator runs.

THE LEDGER IS APPEND-ONLY. A release is a new record, never an edit to the reservation it releases. The
current reservation is computed by replaying the ledger, so the file's history is its state and there is no
mutable field anywhere for drift to hide in.
"""
from __future__ import annotations

import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_FRACTION = 0.25          # Helm §5's declared default
SELECTION_RULE = (
    "rows ordered by sha256(f'{batch}:{row}') ascending; the first ceil(fraction * n) are RESERVED. "
    "Deterministic, reproducible from the roster alone, and outcome-blind by construction — the "
    "reserved rows are not built at declaration time, so no measured value exists for the rule to see.")


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def roster_hash(roster) -> str:
    return hashlib.sha256(json.dumps(sorted(roster), separators=(",", ":")).encode()).hexdigest()


def select(batch: int, roster, fraction: float = DEFAULT_FRACTION):
    """The declared rule. Pure, deterministic, and dependent on nothing but the roster."""
    ordered = sorted(roster, key=lambda r: hashlib.sha256(f"{batch}:{r}".encode()).hexdigest())
    return sorted(ordered[:math.ceil(fraction * len(ordered))])


def read_ledger(path: Path):
    if not path.exists():
        return []
    return [json.loads(x) for x in path.read_text().splitlines() if x.strip()]


def declare(path: Path, batch: int, roster, fraction: float = DEFAULT_FRACTION) -> dict:
    """Append a `reserve` record. IDEMPOTENT on (batch, roster hash): re-running the census must not
    append a second record, or the ledger would grow a new timestamp on every run and the artifact it
    is supposed to fix would drift under it."""
    rh = roster_hash(roster)
    for rec in read_ledger(path):
        if rec["event"] == "reserve" and rec["batch"] == batch:
            if rec["roster_sha256"] != rh:
                raise RuntimeError(
                    f"batch {batch} is already reserved against a DIFFERENT roster "
                    f"({rec['roster_sha256'][:12]} on record, {rh[:12]} offered). A roster is declared "
                    f"once; changing it after declaration is how a reservation stops being blind.")
            return rec
    rec = {
        "event": "reserve", "batch": batch, "declared_at": _now(),
        "fraction": fraction, "rule": SELECTION_RULE,
        "roster_sha256": rh, "roster": sorted(roster),
        "reserved": select(batch, roster, fraction),
        "capture_status": "NOT CAPTURED — frames do not exist (Helm §0.1: predictions hashed before "
                          "their frames exist)",
        "released": False,
    }
    with path.open("a") as fh:
        fh.write(json.dumps(rec) + "\n")
    return rec


def release(path: Path, batch: int, wave: str, authority: str) -> dict:
    """Append a `release` record. The reservation it releases is never edited — replay is the state."""
    res = [r for r in read_ledger(path) if r["event"] == "reserve" and r["batch"] == batch]
    if not res:
        raise RuntimeError(f"cannot release batch {batch}: no reservation on record")
    rec = {"event": "release", "batch": batch, "released_at": _now(), "wave": wave,
           "authority": authority, "released": res[-1]["reserved"]}
    with path.open("a") as fh:
        fh.write(json.dumps(rec) + "\n")
    return rec


def reserved_rows(path: Path) -> set:
    """Currently-withheld rows: reserved, minus anything a later record released."""
    held, freed = set(), set()
    for rec in read_ledger(path):
        if rec["event"] == "reserve":
            held |= set(rec["reserved"])
        elif rec["event"] == "release":
            freed |= set(rec["released"])
    return held - freed


def assert_absent(where: str, row_ids, path: Path) -> None:
    """THE ENFORCEMENT. A reserved row appearing in a disclosed artifact is a hard build failure.

    This is called by the catalog builder and by the loader, so the reservation is not a property the
    fan-out is trusted to respect but one the disclosed artifacts cannot be built in violation of."""
    leak = sorted(set(row_ids) & reserved_rows(path))
    if leak:
        raise RuntimeError(
            f"FRONTIER LEAK — {where} contains reserved row(s) {leak}. Reserved rows are excluded from "
            f"every disclosed computation until released (Helm §5). Helm Kill 2: a detected leak halts "
            f"all open waves and the tranche re-reserves from unbuilt rows.")


def assert_no_reserved_generators(module_namespace: dict, path: Path) -> None:
    """No batch module may DEFINE a generator for a reserved row (minted 2026-07-27, after a near-miss).

    The standing rule since batch 3 was that a batch defines no generator for a reserved row — a batch
    that never learned how to build one cannot burn the ground. It was enforced by reading the ROWS
    table, which is not the same as enforcing it. Batch 8 defined `minimum_fill_in` while
    `minimum-fill-in` sat on the frontier, kept it out of ROWS, and passed every check.

    Worse, `interval_completion` computed a BYTE-IDENTICAL region to it, so the reserved row would have
    been captured under a different name with every guard green. Only a conformance failure on an
    unrelated declaration stopped it.

    THE GUARDS CHECKED NAMES AND NOT WHAT WAS COMPUTED. This closes the cheap half: a function whose
    name maps to a reserved row id cannot exist in a batch module at all. The expensive half — two
    differently-named generators producing the same region — is checked separately at capture time."""
    held = reserved_rows(path)
    if not held:
        return
    bad = sorted(n for n in module_namespace
                 if callable(module_namespace.get(n)) and n.replace("_", "-") in held)
    if bad:
        raise RuntimeError(
            f"RESERVED-ROW GENERATOR PRESENT — {bad}. A batch module must not know how to build a "
            f"reserved row, whether or not it calls the function. Helm Kill 2: a reserved-row leak "
            f"halts all open waves.")


def assert_no_duplicate_regions(rows: dict, ramp_probe, path: Path, rng_factory) -> None:
    """Two differently-named generators producing the SAME region is a reserved-row leak wearing
    another row's name. Checked by construction rather than trusted."""
    seen = {}
    for row, build in rows.items():
        try:
            d = dict(build(rng_factory(), ramp_probe) or [])
        except Exception:
            continue
        r = d.get("feasible")
        if not r:
            continue
        key = hash(tuple(sorted(map(tuple, r))))
        if key in seen:
            raise RuntimeError(
                f"DUPLICATE REGION — `{row}` and `{seen[key]}` compute the identical region at the "
                f"probe step. One of them is the other under a different name, which is how a reserved "
                f"row gets captured with every name-based guard green.")
        seen[key] = row
