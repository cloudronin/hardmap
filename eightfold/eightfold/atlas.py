"""Charge atlas — schema (dataclasses + gates), loader, coverage accounting, and a validate/summary CLI.

The data asset: a JSONL file, one problem per line (line-diffable), each problem carrying one cell per charge.
Retargets the physmap calibration-corpus validator to the charge atlas. Torch-free, stdlib-only, so the
citation discipline is enforceable anywhere (and in CI). Spec §3.2–§3.4; Build addenda R1–R9; gates below.

Discipline (inherited from physmap): correct-and-partial beats complete-and-unverified. A real charge value
carries a resolvable citation or the explicit `uncited-folklore` debt flag; `confirmed` requires a
primary-source citation and is OWNER-promoted, never set by the agent (R8). Unknown ≠ zero: `open` /
`unmeasured` / `n.a.` are explicit sentinels, never imputed (R2). `measured` values are quarantined to
charges 6/7/8 and must point to a reproducible experiment (R9).

    python -m eightfold.atlas validate [--path atlas.jsonl]
    python -m eightfold.atlas summary  [--path atlas.jsonl]
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import asdict, dataclass, field
from datetime import date
from pathlib import Path

from eightfold import charges as C

# R21 / prereg_v4 — charge tiers for the per-charge A2 gate. Core = the population-viability test (gated,
# >=85%); frontier = reported-not-gated (open-rate is the deliverable, the map of unasked questions).
CORE_CHARGES = ("decision", "counting", "approximation", "parameterized")
FRONTIER_CHARGES = ("parallelization", "proof_size", "average_case", "landscape")

# ── storage resolution (single-tier v1; documented seam for a later seed/premium firewall) ────────────────
EIGHTFOLD_ATLAS_ENV = "EIGHTFOLD_ATLAS"
DEFAULT_PATH = Path(__file__).resolve().parent / "results" / "atlas" / "atlas.jsonl"


def resolve_atlas_path() -> Path:
    """Resolve the active atlas path. Precedence: ``$EIGHTFOLD_ATLAS`` override → the bundled atlas.

    Single-tier for v1. A future open-core split would insert a premium-package probe here (exactly as
    ``physmap.corpus.calibration.resolve_corpus_path`` does: env → premium → seed); the seam is deliberately a
    no-op until there is a reason to firewall a premium tier.
    """
    env = os.environ.get(EIGHTFOLD_ATLAS_ENV)
    if env:
        return Path(env).expanduser()
    return DEFAULT_PATH


# ── schema dataclasses ────────────────────────────────────────────────────────────────────────────────────
@dataclass
class ChargeCell:
    """One charge value for one problem, with the object it measures (R1) and its evidential status."""
    charge: str                              # ∈ charges.CHARGES
    value: str                               # ∈ charges.allowed_values(charge) (real value or sentinel)
    canonical_task: str                      # R1: the formal object this charge measures for this problem
    status: str                              # ∈ charges.ALL_STATUSES ("structural" for a sentinel value)
    provenance: dict = field(default_factory=dict)   # citation dict; {experiment:{...}} for measured (R9)
    perspective: str | None = None           # proof system (charge 6) / parameter (charge 4)
    contested_note: str | None = None         # if sources disagree on this cell
    transition_known: bool | None = None      # R17: average_case-only ensemble sub-field (kept out of `value`)
    worst_to_average_self_reduction: bool | None = None  # R18: average_case-only; a same-problem WC->AC self-reduction


@dataclass
class ProblemEntry:
    """One problem row: a fixed encoding + one cell per charge + curation metadata."""
    problem_id: str                          # immutable lowercase slug
    problem_name: str                        # human-readable
    problem_family: str                      # ∈ charges.PROBLEM_FAMILIES (coarse traceability only)
    canonical_encoding: str                  # I3: the fixed encoding; deviations logged in cell provenance
    charges: list[ChargeCell]                # one per charge; names must match charges.CHARGES
    last_reviewed: str                       # ISO date YYYY-MM-DD
    reviewer: str                            # who curated
    notes: str | None = None


# ── (de)serialization ─────────────────────────────────────────────────────────────────────────────────────
def entry_from_dict(d: dict) -> ProblemEntry:
    cells = [ChargeCell(**c) for c in d.get("charges", [])]
    return ProblemEntry(**{**d, "charges": cells})


def entry_to_dict(entry: ProblemEntry) -> dict:
    return asdict(entry)


# ── per-cell / per-entry validation (the QC gates) ────────────────────────────────────────────────────────
def _has_citation(prov: dict) -> bool:
    return isinstance(prov, dict) and any(prov.get(k) for k in C.CITATION_KEYS)


def validate(entry: ProblemEntry) -> list[str]:
    """Return a list of human-readable error strings; empty = the entry is valid.

    Gates:
      1. Vocab — charge ∈ CHARGES; value ∈ allowed_values(charge); status coherent with value type.
      2. Canonical task present (R1).
      3. Citation-or-flag — a real value carries a citation, or status is `uncited-folklore` (the debt).
      4. Confirmed — `confirmed` requires primary_source=true + a citation key (owner-promoted).
      5. Perspective — proof_size / parameterized real values carry a `perspective` tag (R1/§3.2).
      6. Measured quarantine (R9) — `measured` only on charges 7/8, `measured-scaling` only on 6; both require
         a reproducible `provenance.experiment` (prereg+manifest+seeds+code_commit). Rejects measured* on 1–5.
      7. Shape — one cell per charge (names match CHARGES), slug/family/encoding/date/reviewer well-formed.
    """
    errs: list[str] = []
    pid = entry.problem_id or "<no problem_id>"

    # Shape: problem_id slug
    if not entry.problem_id or not isinstance(entry.problem_id, str):
        errs.append(f"{pid}: problem_id missing or not a string")
    elif " " in entry.problem_id or entry.problem_id != entry.problem_id.lower():
        errs.append(f"{pid}: problem_id must be a lowercase slug (no spaces)")
    if not entry.problem_name:
        errs.append(f"{pid}: problem_name missing")
    if entry.problem_family not in C.PROBLEM_FAMILIES:
        errs.append(f"{pid}: problem_family {entry.problem_family!r} not in {sorted(C.PROBLEM_FAMILIES)}")
    if not entry.canonical_encoding:
        errs.append(f"{pid}: canonical_encoding missing (I3 — fix one encoding per problem)")

    # Shape: exactly one cell per charge, names match CHARGES.
    charge_names = [c.charge for c in entry.charges]
    if sorted(charge_names) != sorted(C.CHARGES):
        errs.append(
            f"{pid}: charges must be exactly one cell per charge {C.CHARGES}; "
            f"got {charge_names}"
        )

    for cell in entry.charges:
        tag = f"{pid}/{cell.charge}"
        # Gate 1a: known charge
        if cell.charge not in C.CHARGES:
            errs.append(f"{tag}: unknown charge")
            continue
        allowed = C.allowed_values(cell.charge)
        # Gate 1b: value in vocab
        if cell.value not in allowed:
            errs.append(f"{tag}: value {cell.value!r} not in vocab {sorted(allowed)}")
        is_sentinel = cell.value in C.SENTINELS
        # Gate 1c: status coherent with value type
        if is_sentinel:
            if cell.status != C.STRUCTURAL_STATUS:
                errs.append(f"{tag}: sentinel value {cell.value!r} must carry status "
                            f"{C.STRUCTURAL_STATUS!r} (got {cell.status!r})")
        else:
            if cell.status not in C.EVIDENTIAL_STATUSES:
                errs.append(f"{tag}: real value needs an evidential status "
                            f"{sorted(C.EVIDENTIAL_STATUSES)} (got {cell.status!r})")
        # Gate 2: canonical task (R1)
        if not cell.canonical_task:
            errs.append(f"{tag}: canonical_task missing (R1 — name the object this charge measures)")
        # Gate 3: citation-or-flag. Folklore is the explicit debt flag; measured cells are backed by an
        # experiment artifact instead of a paper citation (validated by gate 6), so both are exempt here.
        _citation_exempt = (C.STATUS_FOLKLORE, C.STATUS_MEASURED, C.STATUS_MEASURED_SCALING)
        if not is_sentinel and cell.status not in _citation_exempt and not _has_citation(cell.provenance):
            errs.append(f"{tag}: real value carries no citation and is not flagged uncited-folklore "
                        f"(gate 3 — every value cited or flagged)")
        # Gate 4: confirmed requires primary source + citation
        if cell.status == C.STATUS_CONFIRMED:
            if not cell.provenance.get("primary_source"):
                errs.append(f"{tag}: confirmed requires provenance.primary_source=true (owner-promoted)")
            if not _has_citation(cell.provenance):
                errs.append(f"{tag}: confirmed requires a citation key {C.CITATION_KEYS}")
        # Gate 5: perspective for proof_size / parameterized real values
        if cell.charge in C.PERSPECTIVE_REQUIRED and not is_sentinel and not cell.perspective:
            errs.append(f"{tag}: real value on a perspective-dependent charge needs `perspective` "
                        f"(proof system / parameter) — R1/§3.2")
        # Gate 5b (R22): a PH-complete decision cell must name its level in `perspective` (e.g. Sigma_2^p).
        if cell.charge == "decision" and cell.value == "PH-complete" and not cell.perspective:
            errs.append(f"{tag}: decision=PH-complete needs the PH level in `perspective` (e.g. Sigma_2^p) (R22)")
        # Gate 6: measured quarantine (R9)
        if cell.status == C.STATUS_MEASURED and cell.charge not in C.MEASURED_ALLOWED:
            errs.append(f"{tag}: status 'measured' is allowed only on charges {sorted(C.MEASURED_ALLOWED)} "
                        f"(R9 — self-generated values are quarantined; rejected on charges 1–5)")
        if cell.status == C.STATUS_MEASURED_SCALING and cell.charge not in C.MEASURED_SCALING_ALLOWED:
            errs.append(f"{tag}: status 'measured-scaling' is allowed only on charge(s) "
                        f"{sorted(C.MEASURED_SCALING_ALLOWED)} (R9)")
        if cell.status in (C.STATUS_MEASURED, C.STATUS_MEASURED_SCALING):
            exp = cell.provenance.get("experiment")
            if not isinstance(exp, dict) or any(not exp.get(k) for k in C.EXPERIMENT_KEYS):
                errs.append(f"{tag}: measured value needs provenance.experiment with all of "
                            f"{list(C.EXPERIMENT_KEYS)} (R9 — reproducible artifact, Census standard)")
        # Gate 8: web citations must be snapshotted (R10) — a url that can go dark needs an archive pointer.
        if isinstance(cell.provenance, dict) and cell.provenance.get("url"):
            if not cell.provenance.get("snapshot"):
                errs.append(f"{tag}: provenance carries a url but no snapshot "
                            f"(R10 — capture a Wayback/local archive; web sources rot)")
            retrieved = cell.provenance.get("retrieved")
            if not retrieved:
                errs.append(f"{tag}: provenance carries a url but no retrieved date (R10)")
            else:
                try:
                    date.fromisoformat(retrieved)
                except (ValueError, TypeError):
                    errs.append(f"{tag}: provenance.retrieved {retrieved!r} not an ISO date (R10)")
        # Gate 9 (R17): transition_known is an average_case-only sub-field (ensemble structure, kept separate
        # from the algorithmic-difficulty value); if asserted True it needs a citation for the transition.
        if cell.transition_known is not None and cell.charge != "average_case":
            errs.append(f"{tag}: transition_known set on a non-average_case charge "
                        f"(R17 — it is an average_case sub-field)")
        if cell.transition_known is True and not _has_citation(cell.provenance):
            errs.append(f"{tag}: transition_known=true needs a citation for the transition (R17)")
        # Gate 9b (R18): worst_to_average_self_reduction is likewise an average_case-only sub-field (a relation,
        # not a difficulty value); if asserted True it needs a citation for the self-reduction.
        if cell.worst_to_average_self_reduction is not None and cell.charge != "average_case":
            errs.append(f"{tag}: worst_to_average_self_reduction set on a non-average_case charge (R18)")
        if cell.worst_to_average_self_reduction is True and not _has_citation(cell.provenance):
            errs.append(f"{tag}: worst_to_average_self_reduction=true needs a citation (R18)")
        # Light gate: a contested cell documents both sides
        if cell.contested_note and not cell.provenance:
            errs.append(f"{tag}: contested_note set but provenance empty (record both sides, don't average)")

    # Gate 7 (shape): dates + reviewer
    if not entry.last_reviewed:
        errs.append(f"{pid}: last_reviewed missing")
    else:
        try:
            date.fromisoformat(entry.last_reviewed)
        except ValueError as e:
            errs.append(f"{pid}: last_reviewed {entry.last_reviewed!r} not ISO date ({e})")
    if not entry.reviewer:
        errs.append(f"{pid}: reviewer missing")

    # Data-vs-theorem consistency: the entry's real charge values must not violate a known entailment rule
    # (a violation is a data-entry bug — or a refutation of a theorem, which is not something we assert here).
    assignment = {c.charge: c.value for c in entry.charges if c.value not in C.SENTINELS}
    for rule_name in C.theorem_forbidden_by(assignment):
        errs.append(f"{pid}: charge values violate entailment rule {rule_name!r} "
                    f"(R5 — a theorem-forbidden combination in the data is a bug; fix or document)")

    return errs


def validate_corpus(entries: list[ProblemEntry]) -> dict[str, list[str]]:
    """Per-entry errors keyed by problem_id, plus '__corpus__' (unique ids) and '__entailment__' (R6 layer)."""
    out: dict[str, list[str]] = {}
    for e in entries:
        errs = validate(e)
        if errs:
            out[e.problem_id or "<no problem_id>"] = errs
    # Unique problem_id
    seen: dict[str, int] = {}
    for e in entries:
        seen[e.problem_id] = seen.get(e.problem_id, 0) + 1
    dups = [pid for pid, n in seen.items() if n > 1]
    if dups:
        out.setdefault("__corpus__", []).append(f"duplicate problem_id values: {sorted(dups)}")
    # Entailment-layer internal consistency (R6) — enforced in CI alongside the data.
    layer_errs = C.validate_entailment_layer()
    if layer_errs:
        out["__entailment__"] = layer_errs
    return out


# ── coverage accounting (R2: applicable-and-cited / applicable) ───────────────────────────────────────────
def cell_is_applicable(cell: ChargeCell) -> bool:
    """A charge applies to this problem unless it is structurally n.a. (open/unmeasured are applicable)."""
    return cell.value != "n.a."


def cell_is_cited_filled(cell: ChargeCell) -> bool:
    """A real value backed by a resolvable citation (claimed/confirmed/measured*) — not a sentinel, not folklore."""
    return cell.value not in C.SENTINELS and cell.status in C.CITED_STATUSES


def coverage_report(entries: list[ProblemEntry]) -> dict:
    """Coverage over applicable cells, overall and per charge, plus the status distribution and the A1 gate."""
    per_charge: dict[str, dict[str, int]] = {
        ch: {"applicable": 0, "cited_filled": 0, "open": 0, "unmeasured": 0, "na": 0, "folklore": 0}
        for ch in C.CHARGES
    }
    status_counts: dict[str, int] = {}
    for e in entries:
        for cell in e.charges:
            pc = per_charge[cell.charge]
            status_counts[cell.status] = status_counts.get(cell.status, 0) + 1
            if cell.value == "n.a.":
                pc["na"] += 1
                continue
            pc["applicable"] += 1
            if cell.value == "open":
                pc["open"] += 1
            elif cell.value == "unmeasured":
                pc["unmeasured"] += 1
            elif cell.status == C.STATUS_FOLKLORE:
                pc["folklore"] += 1
            if cell_is_cited_filled(cell):
                pc["cited_filled"] += 1
    tot_appl = sum(pc["applicable"] for pc in per_charge.values())
    tot_cited = sum(pc["cited_filled"] for pc in per_charge.values())
    tot_folklore = sum(pc["folklore"] for pc in per_charge.values())
    ratio = (tot_cited / tot_appl) if tot_appl else 0.0
    # R21 / prereg_v4 — per-charge A2 gate. Core charges are the population-viability test (raised to >=85%);
    # frontier charges are reported, not gated (their open-rate IS a deliverable: the map of unasked
    # questions). Aggregate coverage is reported for continuity, no longer load-bearing.
    core_appl = sum(per_charge[c]["applicable"] for c in CORE_CHARGES)
    core_cited = sum(per_charge[c]["cited_filled"] for c in CORE_CHARGES)
    core_ratio = (core_cited / core_appl) if core_appl else 0.0
    # The A2 gate is PER-CHARGE: EACH core charge must clear 85% (a high aggregate can't hide a weak charge).
    core_charge_ratios = {
        c: (per_charge[c]["cited_filled"] / per_charge[c]["applicable"]) if per_charge[c]["applicable"] else 1.0
        for c in CORE_CHARGES
    }
    frontier_open_rates = {
        c: {"open_unmeasured": per_charge[c]["open"] + per_charge[c]["unmeasured"],
            "applicable": per_charge[c]["applicable"]}
        for c in FRONTIER_CHARGES
    }
    return {
        "n_problems": len(entries),
        "n_cells": len(entries) * len(C.CHARGES),
        "applicable": tot_appl,
        "cited_filled": tot_cited,
        "uncited_folklore": tot_folklore,
        "coverage_ratio": ratio,
        "a1_gate_pass": ratio >= 0.70 and tot_folklore == 0,
        "core_coverage": core_ratio,
        "core_charge_ratios": core_charge_ratios,
        "a2_core_gate_pass": all(v >= 0.85 for v in core_charge_ratios.values()) and tot_folklore == 0,
        "frontier_open_rates": frontier_open_rates,
        "per_charge": per_charge,
        "status_counts": status_counts,
    }


# ── loader API ────────────────────────────────────────────────────────────────────────────────────────────
def load_atlas(path: str | Path | None = None) -> list[ProblemEntry]:
    """Parse the JSONL atlas into ProblemEntry objects. Raises on parse/schema errors; run validate_corpus()
    separately for the QC gates. path=None → resolve_atlas_path()."""
    p = Path(path) if path is not None else resolve_atlas_path()
    if not p.exists():
        raise FileNotFoundError(f"atlas file not found: {p}")
    entries: list[ProblemEntry] = []
    with open(p, encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            s = line.strip()
            if not s:
                continue
            try:
                d = json.loads(s)
            except json.JSONDecodeError as e:
                raise ValueError(f"atlas JSONL parse error at line {lineno}: {e}") from e
            try:
                entries.append(entry_from_dict(d))
            except TypeError as e:
                raise ValueError(f"atlas schema mismatch at line {lineno} "
                                 f"(problem_id={d.get('problem_id', '?')!r}): {e}") from e
    return entries


def index_by_id(entries: list[ProblemEntry]) -> dict[str, ProblemEntry]:
    return {e.problem_id: e for e in entries}


def get_charge(entry: ProblemEntry, charge: str) -> ChargeCell | None:
    for c in entry.charges:
        if c.charge == charge:
            return c
    return None


# ── CLI ───────────────────────────────────────────────────────────────────────────────────────────────────
def _print_errors(errs_by_id: dict[str, list[str]]) -> int:
    total = sum(len(v) for v in errs_by_id.values())
    print(f"atlas validation FAILED — {total} errors across {len(errs_by_id)} entries:")
    for k in sorted(errs_by_id):
        print(f"  [{k}]")
        for e in errs_by_id[k]:
            print(f"      • {e}")
    return 1


def _print_coverage(rep: dict) -> None:
    print(f"  problems: {rep['n_problems']}   cells: {rep['n_cells']}   applicable: {rep['applicable']}")
    print(f"  cited-filled / applicable = {rep['cited_filled']}/{rep['applicable']} "
          f"= {rep['coverage_ratio']:.1%}   uncited-folklore: {rep['uncited_folklore']}")
    print(f"  status: " + ", ".join(f"{k}={v}" for k, v in sorted(rep["status_counts"].items())))
    print(f"  per-charge (cited/applicable | open/unmeasured/n.a.):")
    for ch in C.CHARGES:
        pc = rep["per_charge"][ch]
        print(f"    {ch:>16s}: {pc['cited_filled']:>2d}/{pc['applicable']:<2d}  "
              f"| {pc['open']}/{pc['unmeasured']}/{pc['na']}"
              + (f"  folklore={pc['folklore']}" if pc["folklore"] else ""))
    print("  CORE per-charge (A2 gate: EACH >=85%): "
          + ", ".join(f"{c}={rep['core_charge_ratios'][c]:.0%}" for c in CORE_CHARGES)
          + f"  [{'PASS' if rep['a2_core_gate_pass'] else 'FAIL'}]")
    fr = rep["frontier_open_rates"]
    print("  FRONTIER open-rate (reported, not gated — map of unasked questions): "
          + ", ".join(f"{c}={fr[c]['open_unmeasured']}/{fr[c]['applicable']}" for c in fr))
    gate = "PASS" if rep["a1_gate_pass"] else "not yet"
    print(f"  A1 aggregate gate (>=70% & 0 folklore, reported for continuity): {gate}")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="charge atlas — validator + summary")
    sub = ap.add_subparsers(dest="cmd", required=True)
    pv = sub.add_parser("validate", help="run the QC gates + corpus invariants + entailment-layer check")
    pv.add_argument("--path", type=Path, default=None)
    ps = sub.add_parser("summary", help="per-charge / per-family coverage summary")
    ps.add_argument("--path", type=Path, default=None)
    args = ap.parse_args(argv)

    path = args.path or resolve_atlas_path()
    try:
        entries = load_atlas(path)
    except (FileNotFoundError, ValueError) as e:
        print(f"FAILED to load atlas: {e}", file=sys.stderr)
        return 2

    if args.cmd == "validate":
        errs = validate_corpus(entries)
        if errs:
            return _print_errors(errs)
        print(f"atlas validation PASSED — {len(entries)} problems clean ({path})")
        _print_coverage(coverage_report(entries))
        return 0

    if args.cmd == "summary":
        print(f"atlas: {len(entries)} problems ({path})")
        fam: dict[str, int] = {}
        for e in entries:
            fam[e.problem_family] = fam.get(e.problem_family, 0) + 1
        print("  families: " + ", ".join(f"{k}={v}" for k, v in sorted(fam.items())))
        _print_coverage(coverage_report(entries))
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
