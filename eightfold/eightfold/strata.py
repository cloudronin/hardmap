"""Strata — Eightfold v2 additive metadata layer (codename Strata). A layer ABOVE the frozen atlas, never inside it.

The atlas keeps rediscovering the same structural facts by hand because they live in PROSE (`canonical_task`,
`perspective`) rather than in FIELDS. Strata promotes three of them to first-class, queryable metadata; the
deliverable of record is the coverage report — the first tabulation of the population where each charge is
observable at all.

ADDITIVE-ONLY IS STRUCTURAL, NOT A DISCIPLINE CHOICE — the frozen atlas defends itself. `tests/test_loader.py`
pins `entry_to_dict(entry_from_dict(d)) == d`, so ANY field added to a v1 `ChargeCell`/`ProblemEntry` would make
`asdict` emit it, change `atlas.jsonl`'s bytes, and fail the suite. The separate-layer design is therefore the ONLY
one that satisfies the spec. So Strata imports the eightfold kernel read-only, operates on RAW ROW DICTS (never
through `ChargeCell`), and composes a v2 validator over the frozen `atlas.validate` — the `foundry/substrate.py`
precedent, one axis over. Note: "Strata v2" (this metadata layer) is a DISTINCT axis from the queued "charge-9 v2"
(fine-grained complexity); the two must never be conflated.

Three additions (sealed here; applied by `dev/build_strata.py` under rules sealed in `Strata-SCHEMA.md`):
  3.1 charge levels        — CHARGE_LEVELS: the object each charge attaches to (per charge, one table).
  3.2 charge applicability — per cell: a value in APPLICABILITY + a MANDATORY reason + derived/judged provenance.
  3.3 objective/param pins — per row: `objective` + `parameterization`, with the covering theorem where one exists.
"""
import json
from pathlib import Path

from eightfold import atlas
from eightfold.charges import CHARGES, EIGHTFOLD_SPEC

# ── 3.1 charge levels — the object each charge attaches to (consistent with SCHEMA.md §3.2 "Canonical object (R1)") ─
LEVELS = ("decision", "counting", "refutation", "objective", "ensemble")
CHARGE_LEVELS = {
    "decision":        {"level": "decision",   "requires": "the problem"},
    "counting":        {"level": "counting",   "requires": "the #-version"},
    "parallelization": {"level": "decision",   "requires": "the problem (within P)"},
    "proof_size":      {"level": "refutation", "requires": "an unsat instance family"},
    "approximation":   {"level": "objective",  "requires": "an objective function"},
    "parameterized":   {"level": "objective",  "requires": "an objective + a parameterization"},
    "average_case":    {"level": "ensemble",   "requires": "a random instance distribution"},
    "landscape":       {"level": "ensemble",   "requires": "ensemble + samplable solutions"},
}
# The sealed finding, made visible in one glance: the two objective-level charges are EXACTLY the coupled pair;
# every other level holds multiple charges with no strong coupling among them.
OBJECTIVE_LEVEL_CHARGES = frozenset(c for c, m in CHARGE_LEVELS.items() if m["level"] == "objective")


def level_of(charge: str) -> str:
    return CHARGE_LEVELS[charge]["level"]


def cross_level_flag(predictor_level: str, charge: str):
    """3.1's mechanical consequence: a predictor at level X aimed at a charge at level Y is SUSPECT before anything
    runs (would have flagged tuple-dispersion-vs-approximation instantly). Returns a warning string, or None."""
    tgt = level_of(charge)
    if predictor_level != tgt:
        return (f"cross-level: a {predictor_level!r}-level predictor aimed at {charge!r} (a {tgt!r}-level charge) — "
                f"suspect before measurement; the object differs")
    return None


# ── 3.2 charge applicability (per cell) ───────────────────────────────────────────────────────────────────────
APPLICABILITY = ("defined-informative", "defined-trivial", "ambiguous", "n.a.")
PROV_DERIVED, PROV_JUDGED = "derived", "judged"           # from existing text vs by owner judgment
STRATA_PROVENANCE = frozenset({PROV_DERIVED, PROV_JUDGED})


def validate_applicability(cell: dict) -> list:
    """Gate one cell's applicability metadata. SILENT when absent (additive). When present: value in APPLICABILITY,
    a NON-EMPTY reason (the S1 done-gate — reject applicability-without-reason), and a derived/judged provenance."""
    errs = []
    if cell.get("applicability") is None:
        return errs
    tag = cell.get("charge", "?")
    if cell["applicability"] not in APPLICABILITY:
        errs.append(f"strata[{tag}]: applicability {cell['applicability']!r} not in {list(APPLICABILITY)}")
    if not cell.get("applicability_reason"):
        errs.append(f"strata[{tag}]: applicability set but no applicability_reason (mandatory)")
    if cell.get("applicability_provenance") not in STRATA_PROVENANCE:
        errs.append(f"strata[{tag}]: applicability_provenance must be one of {sorted(STRATA_PROVENANCE)}")
    return errs


# ── 3.3 objective + parameterization pinning (per row) ────────────────────────────────────────────────────────
OBJECTIVES = ("Min-Ones", "Max-Ones", "Max-CSP", "weighted", "global-numeric", "none")
PARAMETERIZATIONS = ("solution size", "treewidth", "other", "none")


def validate_objective_pin(row: dict) -> list:
    """Gate a row's objective/parameterization pins (top-level keys). Vocab-checked; a real (non-'none') assignment
    carries a derived/judged pin_provenance. The covering theorem (pin_theorem) is recorded where one is claimed."""
    errs = []
    pid = row.get("problem_id", "?")
    obj, par = row.get("objective"), row.get("parameterization")
    if obj is not None and obj not in OBJECTIVES:
        errs.append(f"strata[{pid}]: objective {obj!r} not in {list(OBJECTIVES)}")
    if par is not None and par not in PARAMETERIZATIONS:
        errs.append(f"strata[{pid}]: parameterization {par!r} not in {list(PARAMETERIZATIONS)}")
    if (obj not in (None, "none")) or (par not in (None, "none")):
        if row.get("pin_provenance") not in STRATA_PROVENANCE:
            errs.append(f"strata[{pid}]: a real objective/parameterization pin needs derived/judged pin_provenance")
    return errs


# ── the composing v2 validator (the substrate.py precedent) ───────────────────────────────────────────────────
STRATA_CELL_KEYS = ("applicability", "applicability_reason", "applicability_provenance")
STRATA_ROW_KEYS = ("objective", "parameterization", "pin_theorem", "pin_provenance")


def strip_strata(row: dict) -> dict:
    """A v1-shaped row dict with ALL strata keys removed, so the frozen atlas.validate sees exactly v1 (its
    entry_from_dict does ChargeCell(**c)/ProblemEntry(**d), which reject any unknown key)."""
    v1 = {k: v for k, v in row.items() if k not in STRATA_ROW_KEYS}
    v1["charges"] = [{k: v for k, v in c.items() if k not in STRATA_CELL_KEYS} for c in row.get("charges", [])]
    return v1


def validate_entry_v2(row: dict, spec=EIGHTFOLD_SPEC) -> list:
    """Compose over the frozen kernel: (a) the v1 portion (strata stripped) must validate CLEAN under the unchanged
    atlas.validate; (b) the strata additions pass their own gates. Never touches ChargeCell/ProblemEntry, so the v1
    round-trip + byte-identity hold by construction."""
    errs = list(atlas.validate(atlas.entry_from_dict(strip_strata(row)), spec))
    errs += validate_objective_pin(row)
    for cell in row.get("charges", []):
        errs += validate_applicability(cell)
    return errs


def validate_level_table() -> list:
    """The level table covers exactly CHARGES, uses only known levels, and the objective coupling holds."""
    errs = []
    if set(CHARGE_LEVELS) != set(CHARGES):
        errs.append(f"CHARGE_LEVELS must cover exactly {list(CHARGES)}; got {sorted(CHARGE_LEVELS)}")
    for c, m in CHARGE_LEVELS.items():
        if m.get("level") not in LEVELS:
            errs.append(f"CHARGE_LEVELS[{c!r}]: level {m.get('level')!r} not in {list(LEVELS)}")
        if not m.get("requires"):
            errs.append(f"CHARGE_LEVELS[{c!r}]: missing 'requires'")
    if OBJECTIVE_LEVEL_CHARGES != {"approximation", "parameterized"}:
        errs.append(f"the two objective-level charges must be exactly {{approximation, parameterized}}; "
                    f"got {sorted(OBJECTIVE_LEVEL_CHARGES)}")
    return errs


# ── the v2 artifact writer (merge frozen v1 rows + strata additions; never re-serialize through ChargeCell) ─────
def _default_v2_path() -> Path:
    return atlas.DEFAULT_PATH.parent / "atlas_v2.jsonl"


def merge_row(row: dict, strata: dict) -> dict:
    """Attach the strata additions to one raw v1 row dict. `strata` = {'row_pins': {...}, 'cell_meta': {charge:{...}}}."""
    merged = {**row, **strata.get("row_pins", {})}
    cm = strata.get("cell_meta", {})
    merged["charges"] = [{**c, **cm.get(c["charge"], {})} for c in row.get("charges", [])]
    return merged


def write_atlas_v2(strata_by_row: dict, out_path=None) -> tuple:
    """Read the FROZEN atlas.jsonl as raw dicts (read-only), merge the strata additions per problem_id, and write
    atlas_v2.jsonl in the builder's exact JSONL format (json.dumps(row, ensure_ascii=False)+'\\n'; no indent, no
    sort_keys — dev/build_atlas.py). Returns (dest_path, merged_rows)."""
    src = atlas.resolve_atlas_path()
    rows = [json.loads(line) for line in src.read_text().splitlines() if line.strip()]
    merged = [merge_row(r, strata_by_row.get(r["problem_id"], {})) for r in rows]
    dest = Path(out_path) if out_path else _default_v2_path()
    with dest.open("w") as f:
        for r in merged:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    return dest, merged


def selftest_strata(verbose: bool = False) -> int:
    """Hand-checks: level table valid; a good v2 cell passes; applicability-without-reason is rejected; a v1-only
    row (no strata keys) validates as clean as v1; cross_level_flag catches a mismatch. Returns error count."""
    errs = validate_level_table()
    good = {"applicability": "defined-informative", "applicability_reason": "APX-complete objective is non-degenerate",
            "applicability_provenance": PROV_DERIVED, "charge": "approximation"}
    if validate_applicability(good) != []:
        errs.append("a fully-provenanced applicability cell should pass")
    if validate_applicability({**good, "applicability_reason": ""}) == []:
        errs.append("applicability without a reason must be rejected (the S1 gate)")
    if validate_applicability({**good, "applicability": "bogus"}) == []:
        errs.append("an out-of-vocab applicability must be rejected")
    if validate_applicability({"charge": "decision"}) != []:
        errs.append("a v1-only cell (no strata keys) must validate silently")
    if cross_level_flag("ensemble", "approximation") is None:
        errs.append("cross_level_flag must catch an ensemble-level predictor aimed at an objective-level charge")
    if cross_level_flag("objective", "approximation") is not None:
        errs.append("cross_level_flag must be silent when levels match")
    if verbose:
        for e in errs:
            print("  strata selftest:", e)
    return len(errs)


if __name__ == "__main__":
    n = selftest_strata(verbose=True)
    print("strata selftest:", "OK" if n == 0 else f"FAIL ({n})")
