"""`hardmap repro` -- run manifest claims and diff against expected within tolerance.

Fast tier (default) recomputes each statistic from the committed frozen artifacts;
``--full`` regenerates from scratch where a full adapter is declared. Exits nonzero
on any mismatch, so CI and a referee get a single go/no-go.
"""
from __future__ import annotations

import importlib
import time

from .compare import check_claim
from .manifest import load_manifest


def _call(entry: str) -> dict:
    mod_name, func_name = entry.split(":")
    fn = getattr(importlib.import_module(mod_name), func_name)
    return fn()


def _run_claim(claim: dict, full: bool) -> tuple[bool, list, float, str | None]:
    use_full = bool(full and claim.get("full"))
    entry = claim["full"] if use_full else claim["fast"]
    used = "full" if use_full else "fast"
    t = time.time()
    try:
        result = _call(entry)
    except Exception as exc:  # noqa: BLE001 - report, don't crash the whole sweep
        return False, [("<error>", False, f"{type(exc).__name__}: {exc}")], time.time() - t, used
    rows = check_claim(result, claim["expected"], claim.get("tolerance", "exact"))
    return all(ok for _, ok, _ in rows), rows, time.time() - t, used


def run(claim_ids: list[str] | None = None, full: bool = False, list_only: bool = False) -> int:
    claims = load_manifest()
    if list_only:
        for c in claims:
            print(f"{c['id']:<28} [{c['tier']}] {c['description']}")
        return 0
    if claim_ids:
        wanted = set(claim_ids)
        claims = [c for c in claims if c["id"] in wanted]
        missing = wanted - {c["id"] for c in claims}
        if missing:
            print(f"unknown claim id(s): {sorted(missing)}")
            return 2
    if not claims:
        print("no claims selected")
        return 2

    n_fail = 0
    for c in claims:
        ok, rows, secs, used = _run_claim(c, full)
        n_fail += not ok
        mark = "PASS" if ok else "FAIL"
        print(f"[{mark}] {c['id']:<28} ({used}, {secs:.1f}s)")
        for field, fok, detail in rows:
            if not fok or not ok:
                print(f"        {'ok ' if fok else 'BAD'} {field}: {detail}")
    total = len(claims)
    print(f"\n{total - n_fail}/{total} claims passed" + ("" if not n_fail else f"  ({n_fail} FAILED)"))
    return 1 if n_fail else 0
