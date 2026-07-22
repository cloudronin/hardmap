"""Substrate layer (Sprint 6 "Pebble", prereg_v12) — a layer BENEATH the charges, not a charge.

The substrate hypothesis: the charges are projections of one measurable quantity — reach ξ, how far information
about a partial solution propagates through a problem's constraint structure. The layer records ξ separately from
the charge columns, with a ONE-WAY predictive relation encoded in the CODE PATH, not in prose: substrate predicts
charges; charges never predict substrate.

Design constraints (from the schema review):
  * eightfold's `ChargeSpec` is frozen and `atlas.validate` demands exactly one cell per `spec.charges`, so a
    `SubstrateCell` must live OUTSIDE `ProblemEntry.charges`. This module is entirely foundry-side; it imports
    eightfold read-only and never mutates it (byte-identical safe).
  * `PredictiveRule` mirrors `eightfold.charges.EntailmentRule` (antecedent -> forbids is the existing one-way
    column relation). Here: `substrate` (trigger side) -> `predicts` (charge side). It is only ever consumed
    substrate->charge; the reverse map is never built.
  * R1 typing: every substrate cell carries its `canonical_ensemble` + `density_anchor` (ξ attaches to instances
    from an ensemble at a density, never to a problem in the abstract).
"""
from dataclasses import dataclass, field

from eightfold import atlas

# ── substrate status ladder (mirrors the charge ladder; ξ is self-generated => `measured` needs a manifest) ───
STATUS_MEASURED = "measured"
STATUS_STRUCTURAL = "structural"                 # the status a sentinel cell carries
SUBSTRATE_STATUSES = frozenset({STATUS_MEASURED, STATUS_STRUCTURAL})
SUBSTRATE_SENTINELS = frozenset({"open", "unmeasured", "n.a."})
EXPERIMENT_KEYS = ("prereg", "manifest", "seeds", "code_commit")   # a measured cell's provenance.experiment
STRENGTHS = ("strong", "moderate", "weak", "none")                 # sealed differential-prediction vocabulary
REGIMES = ("within-co-clone", "between-co-clone")                  # the resolution split (owner Q2)


@dataclass
class SubstrateCell:
    """One substrate reading for one row. Kept OUTSIDE ProblemEntry.charges (eightfold shape gate)."""
    quantity: str                    # the substrate key, e.g. "reach"
    value: str                       # a level from the substrate vocabulary, or a sentinel
    canonical_ensemble: str          # R1: the ensemble instances are drawn from
    density_anchor: str              # R1: the density (e.g. "0.9*alpha_struct")
    status: str = STATUS_MEASURED    # measured (needs experiment provenance) | structural (sentinel)
    measured: dict = field(default_factory=dict)   # raw numbers: {decay_rate, corr_length, fit_quality, scaling,...}
    provenance: dict = field(default_factory=dict)  # {experiment: {prereg, manifest, seeds, code_commit}}
    perspective: str | None = None   # e.g. sampler set / drop-point / conditioning value
    notes: str | None = None


@dataclass(frozen=True)
class PredictiveRule:
    """A one-way substrate->charge predictive relation (models EntailmentRule's antecedent->forbids asymmetry).
    `predicts` maps a charge to a sealed prediction STRENGTH; `regime` records at which resolution the prediction
    is testable (within-co-clone for measured charges; between-co-clone for clone-level oracle charges)."""
    name: str
    substrate: str                       # trigger side (the substrate quantity)
    predicts: dict                       # charge -> strength ∈ STRENGTHS   (constrained side)
    regime: str                          # ∈ REGIMES
    preconditions: str                   # MANDATORY: the mechanism/basis
    citation: str                        # MANDATORY
    note: str = ""


def validate_substrate_cell(cell: SubstrateCell) -> list:
    """Gate a substrate cell. Mirrors the charge-cell gates; the key invariant (substrate-never-derived-from-a-
    charge) is enforced at the entry level in validate_entry_with_substrate."""
    errs = []
    tag = f"substrate[{cell.quantity}]"
    is_sentinel = cell.value in SUBSTRATE_SENTINELS
    if cell.status not in SUBSTRATE_STATUSES:
        errs.append(f"{tag}: status {cell.status!r} not in {sorted(SUBSTRATE_STATUSES)}")
    if is_sentinel and cell.status != STATUS_STRUCTURAL:
        errs.append(f"{tag}: sentinel value {cell.value!r} must carry status 'structural'")
    if not is_sentinel and cell.status != STATUS_MEASURED:
        errs.append(f"{tag}: real value {cell.value!r} must carry status 'measured'")
    if not cell.canonical_ensemble or not cell.density_anchor:   # R1 typing, non-negotiable
        errs.append(f"{tag}: R1 typing — every substrate cell needs canonical_ensemble + density_anchor")
    if cell.status == STATUS_MEASURED:
        exp = cell.provenance.get("experiment")
        if not isinstance(exp, dict) or any(not exp.get(k) for k in EXPERIMENT_KEYS):
            errs.append(f"{tag}: measured cell needs provenance.experiment with all of {list(EXPERIMENT_KEYS)}")
    return errs


def validate_predictive_rule(rule: PredictiveRule, spec) -> list:
    """R6-style consistency: mandatory preconditions + citation; regime valid; every predicted charge is a real
    charge of the spec; strengths from the vocabulary; the substrate is NOT a charge (asymmetry)."""
    errs = []
    if len(rule.preconditions or "") < 20:
        errs.append(f"predictive rule {rule.name!r}: preconditions must state the mechanism (>=20 chars)")
    if len(rule.citation or "") < 5:
        errs.append(f"predictive rule {rule.name!r}: citation required")
    if rule.regime not in REGIMES:
        errs.append(f"predictive rule {rule.name!r}: regime {rule.regime!r} not in {list(REGIMES)}")
    if rule.substrate in spec.charges:
        errs.append(f"predictive rule {rule.name!r}: substrate {rule.substrate!r} must NOT be a charge column "
                    f"(the asymmetry: substrate predicts charges, never the reverse)")
    for charge, strength in rule.predicts.items():
        if charge not in spec.charges:
            errs.append(f"predictive rule {rule.name!r}: predicts unknown charge {charge!r}")
        if strength not in STRENGTHS:
            errs.append(f"predictive rule {rule.name!r}: strength {strength!r} not in {list(STRENGTHS)}")
    return errs


def validate_layer(rules, spec) -> list:
    errs, seen = [], set()
    for r in rules:
        if r.name in seen:
            errs.append(f"duplicate predictive rule name {r.name!r}")
        seen.add(r.name)
        errs += validate_predictive_rule(r, spec)
    return errs


def validate_entry_with_substrate(entry, substrate_cells, spec) -> list:
    """Compose over the frozen eightfold validator for the charge columns, then add substrate gates + the
    one-way invariant. The charge columns are validated UNCHANGED (byte-identical safe)."""
    errs = list(atlas.validate(entry, spec))                     # eightfold charge-column gates, untouched
    for cell in substrate_cells:
        errs += validate_substrate_cell(cell)
        # THE one-way invariant: a substrate cell may never cite a charge column as its source. ξ is measured from
        # instances; if its provenance references a charge, the asymmetry has been violated.
        src = " ".join(str(v) for v in cell.provenance.values())
        for charge in spec.charges:
            if isinstance(cell.provenance.get("derived_from"), (list, tuple, str)) and charge in cell.provenance.get("derived_from", ""):
                errs.append(f"substrate[{cell.quantity}]: substrate cell must NOT be derived-from charge "
                            f"{charge!r} (substrate predicts charges, never the reverse)")
    return errs


# ── the sealed differential prediction, encoded as a layer (prereg_v12; scored DESCRIPTIVELY in v1) ───────────
# reach -> charge strength + the resolution regime it is testable in. This IS the schema encoding of §2's table;
# v1 does not adjudicate it (owner Q2) — it is sealed here so phase 2 inherits a prediction, not a post-hoc story.
REACH_LAYER = [
    PredictiveRule("reach_predicts_landscape", "reach", {"landscape": "strong"}, "within-co-clone",
                   "clustering ≈ correlation decay: solution-geometry is near-definitionally what propagation does "
                   "to the answer set's shape.", "substrate hypothesis §2; Krzakala-Montanari cavity clustering"),
    PredictiveRule("reach_predicts_average_case", "reach", {"average_case": "strong"}, "within-co-clone",
                   "average-case behaviour is the propagation regime at a given density (cavity-method threshold "
                   "literature).", "Mezard-Montanari; cavity-method thresholds"),
    PredictiveRule("reach_predicts_approximation", "reach", {"approximation": "moderate"}, "between-co-clone",
                   "PCP/expander mechanism: inapproximability lives where nothing decays. Oracle charge -> testable "
                   "only between co-clones (clone-constant within).", "PCP theorem; expander-based inapprox"),
    PredictiveRule("reach_predicts_parameterized", "reach", {"parameterized": "moderate"}, "between-co-clone",
                   "kernelization/treewidth: bounded local structure permits compression. Oracle charge -> between-"
                   "co-clone.", "Downey-Fellows; treewidth kernelization"),
    PredictiveRule("reach_predicts_proof_size", "reach", {"proof_size": "weak"}, "between-co-clone",
                   "width-based bounds are suggestive; the solution-side <-> refutation-side link is a leap.",
                   "Ben-Sasson-Wigderson width-size (suggestive only)"),
    PredictiveRule("reach_predicts_counting", "reach", {"counting": "weak"}, "between-co-clone",
                   "approximate-counting decay conditions exist; exact counting is a different object.",
                   "Weitz spatial-mixing / approximate counting (partial)"),
    PredictiveRule("reach_predicts_parallelization", "reach", {"parallelization": "none"}, "between-co-clone",
                   "no mechanism the owner or reviewer can state — the pre-registered negative control.",
                   "substrate hypothesis §2 (declared none)"),
]
