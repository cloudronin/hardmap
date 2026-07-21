"""The eight charges — value vocabularies, coding, and the known-entailment constraint layer.

Domain module for the charge atlas: stdlib-only, no scientific stack (so the schema and its gates import
anywhere). `atlas.py` imports the vocabularies from here; `structure.py` imports the entailment layer for
occupancy triage (R5). Spec §3.2; Build addenda R1–R9.

Two design commitments live here:

* **Sentinels are universal (R2).** `open` / `unmeasured` / `n.a.` are allowed for *every* charge, on top of
  that charge's real-value vocabulary. `n.a.` = the charge structurally does not apply to this problem;
  `open` = it applies but the value is unknown; `unmeasured` = it applies and nobody has measured it. Unknown
  is never zero and never imputed.
* **Entailment rules carry exact preconditions (R6).** Every rule states the theorem's hypotheses and a
  citation; `validate_entailment_layer()` rejects any rule missing them. A rule whose `forbids` is populated
  is *column-expressible* and drives occupancy triage; a rule with `forbids=None` (e.g. the FPTAS rule, whose
  hypothesis "strongly NP-hard with a polynomially-bounded objective" is not one of our columns) is
  informational but still carries its preconditions.
"""
from __future__ import annotations

from dataclasses import dataclass, field

# ── the eight charges (column order is fixed; every ProblemEntry carries one cell per charge) ──────────────
CHARGES: list[str] = [
    "decision",         # 1 — the classical axis
    "counting",         # 2 — the #-version
    "approximation",    # 3 — the optimization version
    "parameterized",    # 4 — with a fixed parameter (see `perspective`)
    "parallelization",  # 5 — within-P: NC vs P-complete
    "proof_size",       # 6 — an unsatisfiable instance family (see `perspective` for the system)
    "average_case",     # 7 — a random ensemble
    "landscape",        # 8 — a random ensemble's solution-space geometry (clustering/OGP/freezing)
]

CHARGE_TITLES: dict[str, str] = {
    "decision": "Decision",
    "counting": "Counting",
    "approximation": "Approximation",
    "parameterized": "Parameterized",
    "parallelization": "Parallelization",
    "proof_size": "Proof-size",
    "average_case": "Average-case / phase structure",
    "landscape": "Landscape / freezing",
}

# ── sentinels (R2): allowed for every charge, on top of its real-value vocabulary ──────────────────────────
SENTINELS: frozenset[str] = frozenset({"open", "unmeasured", "n.a."})

# ── real-value vocabularies per charge (spec §3.2) ─────────────────────────────────────────────────────────
CHARGE_REAL_VALUES: dict[str, frozenset[str]] = {
    "decision": frozenset({"P", "NPI-candidate", "NPC", "harder"}),
    "counting": frozenset({"FP", "#P-complete"}),
    "approximation": frozenset({"FPTAS", "EPTAS", "PTAS", "APX-complete", "log-APX", "poly-APX", "inapprox"}),
    "parameterized": frozenset({"FPT", "W[1]", "W[2]+", "XP", "para-NP-hard"}),
    "parallelization": frozenset({"NC", "P-complete"}),
    "proof_size": frozenset({"poly", "exp"}),
    # average_case VALUE is an ALGORITHMIC-DIFFICULTY statement only (R17). The ensemble-structure fact
    # "a phase transition is known" is a SEPARATE boolean sub-field `transition_known` on the cell, not a
    # value — mixing the two statement types in one single-select vocab manufactures spurious associations.
    # R16 adds worst-case-to-average-equiv (provable via random self-reducibility, e.g. permanent/Lipton) and
    # hard-on-average-conjectured (planted-distribution assumptions, e.g. planted clique) — distinct from the
    # crypto-standard hard-on-average-crypto (factoring).
    "average_case": frozenset({"easy-on-average", "hard-on-average-crypto",
                               "worst-case-to-average-equiv", "hard-on-average-conjectured"}),
    # R14 adds freezing-measured: self-measured backbone/freezing evidence, NOT a proven overlap-gap. Used for
    # our own Census proof-space datum (no OGP theorem exists for proof space — an I3 novelty finding).
    "landscape": frozenset({"clustering-OGP-known", "clustering-OGP-refuted", "freezing-measured"}),
}


def allowed_values(charge: str) -> frozenset[str]:
    """Every value a cell for `charge` may carry: its real-value vocab plus the universal sentinels."""
    return CHARGE_REAL_VALUES[charge] | SENTINELS


# ── ordinal codings (I4): recorded only where a natural order exists; used for the human-readable narrative
# and an ordinal-vs-categorical sensitivity check, NEVER forced onto the association/MCA analyses. ──────────
ORDINAL: dict[str, list[str]] = {
    # easiest → hardest
    "decision": ["P", "NPI-candidate", "NPC", "harder"],
    "approximation": ["FPTAS", "EPTAS", "PTAS", "APX-complete", "log-APX", "poly-APX", "inapprox"],
    # partial hardness order (XP is a containment, kept last as "broad"); FPT easiest
    "parameterized": ["FPT", "W[1]", "W[2]+", "para-NP-hard", "XP"],
}

# ── evidential-status ladder ───────────────────────────────────────────────────────────────────────────────
# Real-valued cells carry an evidential status; sentinel cells carry the structural marker.
STATUS_CLAIMED = "claimed"                 # real citation, not independently confirmed — the agent default
STATUS_CONFIRMED = "confirmed"             # primary source read; OWNER-promoted at review (never the agent)
STATUS_FOLKLORE = "uncited-folklore"       # asserted without a resolvable citation — a debt, must resolve or revert to open
STATUS_MEASURED = "measured"               # R9: self-generated empirical value (charges 7, 8 only)
STATUS_MEASURED_SCALING = "measured-scaling"  # R9: self-generated scaling measurement (charge 6 only)
STRUCTURAL_STATUS = "structural"           # the status a sentinel-valued cell carries

EVIDENTIAL_STATUSES: frozenset[str] = frozenset({
    STATUS_CLAIMED, STATUS_CONFIRMED, STATUS_FOLKLORE, STATUS_MEASURED, STATUS_MEASURED_SCALING,
})
ALL_STATUSES: frozenset[str] = EVIDENTIAL_STATUSES | {STRUCTURAL_STATUS}

# Statuses that count as a *cited, filled* value for coverage (excludes folklore, excludes sentinels).
CITED_STATUSES: frozenset[str] = frozenset({
    STATUS_CLAIMED, STATUS_CONFIRMED, STATUS_MEASURED, STATUS_MEASURED_SCALING,
})

# ── R9 quarantine: which charges may carry a self-generated (measured) value ──────────────────────────────
MEASURED_ALLOWED: frozenset[str] = frozenset({"average_case", "landscape"})   # status "measured"
MEASURED_SCALING_ALLOWED: frozenset[str] = frozenset({"proof_size"})          # status "measured-scaling"
# A measured cell's provenance must carry an `experiment` artifact with these keys (Census standard).
EXPERIMENT_KEYS: tuple[str, ...] = ("prereg", "manifest", "seeds", "code_commit")

# Charges whose real value requires a `perspective` tag (R1 / §3.2): the proof system / the parameter.
PERSPECTIVE_REQUIRED: frozenset[str] = frozenset({"proof_size", "parameterized"})

# Provenance keys that count as a real citation (mirror physmap gate 7).
CITATION_KEYS: tuple[str, ...] = ("citation", "doi", "page", "table", "figure", "url", "year")

# ── coarse problem-family tags (traceability only; analysis clusters over CHARGES, not this) ───────────────
PROBLEM_FAMILIES: frozenset[str] = frozenset({
    "sat-csp", "graph", "algebraic", "number-theoretic", "optimization",
    "logic-proof", "lattice", "matrix", "string", "geometric",
})


# ── the known-entailment constraint layer (R5/R6) ─────────────────────────────────────────────────────────
@dataclass(frozen=True)
class EntailmentRule:
    """A known theorem linking charge values.

    `antecedent` maps charge → the value(s) that trigger the rule. If `forbids` is set (charge → the value(s)
    the theorem rules out once the antecedent holds), the rule is column-expressible and drives occupancy
    triage: a marginal cell matching the antecedent AND a forbidden value is *theorem-forbidden*, not a gap.
    `forbids=None` marks an informational rule whose consequent is not one of our columns (kept for the record
    and for R6's preconditions discipline). `preconditions` and `citation` are MANDATORY (R6).
    """
    name: str
    antecedent: dict[str, frozenset[str]]
    preconditions: str
    citation: str
    forbids: dict[str, frozenset[str]] | None = None
    note: str = ""


ENTAILMENT_LAYER: list[EntailmentRule] = [
    EntailmentRule(
        name="counting_FP_implies_decision_P",
        antecedent={"counting": frozenset({"FP"})},
        forbids={"decision": frozenset({"NPI-candidate", "NPC", "harder"})},
        preconditions=(
            "The #-version counts exactly the witnesses whose existence is the decision question (canonical_task "
            "alignment, R1). If #solutions is computable in FP, existence follows from (count > 0) in poly time, "
            "so decision ∈ P. Requires the counted objects to be the decision witnesses — not a different "
            "solution notion."
        ),
        citation="Arora & Barak, Computational Complexity (2009), Ch. 17; Valiant, TCS 8 (1979).",
        note="Forbids the cell (counting=FP, decision∈{NPI-candidate,NPC,harder}).",
    ),
    EntailmentRule(
        name="parallel_defined_only_within_P",
        antecedent={"decision": frozenset({"NPC", "harder"})},
        forbids={"parallelization": frozenset({"NC", "P-complete"})},
        preconditions=(
            "NC ⊆ P. The parallelization charge (NC vs P-complete) is a *within-P* classification; an NP-"
            "complete or harder problem is not in P (unless P=NP), so NC-membership ⇔ NP ⊆ NC and "
            "P-completeness is undefined — the charge must be n.a. Antecedent is restricted to {NPC, harder} "
            "(NOT NPI-candidate, which might yet be in P), so the rule is unconditional given P≠NP. The "
            "decision and parallelization charges refer to the SAME problem (no object-mismatch)."
        ),
        citation="Greenlaw, Hoover & Ruzzo, Limits to Parallel Computation (1995).",
        note="For decision∈{NPC,harder} the parallelization cell must be n.a.; NC/P-complete there are theorem-forbidden.",
    ),
    EntailmentRule(
        name="inapprox_implies_NP_hard_SAME_OBJECT",
        antecedent={"approximation": frozenset({"inapprox"})},
        forbids=None,  # NOT column-forbidding: decision and approximation can attach to different objects (R1)
        preconditions=(
            "inapprox = no poly-time f(n)-approximation for the OPTIMIZATION object unless P=NP, whose gap "
            "problem is then NP-hard. This forbids decision=P ONLY IF the decision charge is stated for the "
            "SAME object as the approximation charge. In a charge atlas that is generally false (R1): "
            "counterexample XOR-SAT — decision=P (linear feasibility over GF(2)) but MAX-3LIN is inapprox "
            "(Håstad 2001). So (decision=P, approximation=inapprox) is OCCUPIED, not forbidden; this rule is "
            "informational only, kept to document the object-mismatch (R6 — a missing forbid is safer than a "
            "wrong one)."
        ),
        citation="Håstad, Some optimal inapproximability results, JACM 48 (2001); Arora & Barak (2009), Ch. 22.",
        note="Informational (object-dependent). Demoted from a forbid after the XOR-SAT counterexample (R6).",
    ),
    EntailmentRule(
        name="approx_hardness_requires_NP_hardness_SAME_OBJECT",
        antecedent={"decision": frozenset({"P"})},
        forbids=None,  # NOT column-forbidding: the P decision and the hard optimization can be different objects (R1)
        preconditions=(
            "If a problem's OWN optimization version is in PO (exact poly-time optimum, ratio 1), it has no "
            "super-constant inapproximability. This forbids the hardness-of-approximation values ONLY when the "
            "decision charge (=P) and the approximation charge are the SAME object. In the atlas they often "
            "are not (R1): XOR-SAT has decision=P yet MAX-3LIN inapprox; #-easy linear systems vs hard MAX-"
            "LIN. So this does NOT forbid a column cell; informational only (R6)."
        ),
        citation="Ausiello et al., Complexity and Approximation (1999), Ch. 1–3; Håstad, JACM 48 (2001).",
        note="Informational (object-dependent). Demoted from a forbid after the XOR-SAT counterexample (R6).",
    ),
    EntailmentRule(
        name="FPTAS_not_strongly_NP_hard",
        antecedent={"approximation": frozenset({"FPTAS"})},
        forbids=None,  # informational: "strongly NP-hard with poly-bounded objective" is not one of our columns
        preconditions=(
            "EXACT hypotheses (the R6 cautionary example): an NPO problem that is **strongly NP-hard** AND "
            "whose optimal objective value is **bounded by a polynomial in the input size** admits no FPTAS "
            "unless P=NP. Contrapositive (this rule): FPTAS ⟹ the problem is NOT both strongly-NP-hard and "
            "poly-bounded-objective. Dropping either hypothesis makes the rule false (e.g. KNAPSACK has an "
            "FPTAS and is NP-hard — but only weakly, with an exponentially-large objective under binary "
            "encoding), which is why it does not forbid a column cell here."
        ),
        citation="Garey & Johnson, J. ACM 25 (1978); Garey & Johnson (1979), §4.1.",
        note="Informational — carried to document why preconditions are load-bearing (R6). Not a triage rule.",
    ),
    # R12 — approximation<->parameterized bridges (the Marx line). Informational: they only forbid when the
    # approximation and parameterization are the same object/parameter (R1), so they document how much of the
    # approx|parameterized association is theorem-forced. Only the RESIDUAL after these is H2-grade signal.
    EntailmentRule(
        name="eptas_implies_fpt_SAME_PARAMETER",
        antecedent={"approximation": frozenset({"EPTAS"})},
        forbids=None,
        preconditions=(
            "An EPTAS (running time f(1/eps)*poly(n)) yields an FPT algorithm for the standard parameter (fix "
            "eps to force the optimum), so approximation=EPTAS bridges to parameterized=FPT — WHEN the "
            "approximation and parameterization are the same object/parameter (R1). Informational: our columns "
            "may carry EPTAS and a parameterized value for different objects."
        ),
        citation="Cesati & Trevisan, On the efficiency of polynomial time approximation schemes, IPL 64 (1997).",
        note="R12 bridge: part of any approx|parameterized association is theorem-forced, not surprising.",
    ),
    EntailmentRule(
        name="w1_hardness_rules_out_eptas_MARX",
        antecedent={"parameterized": frozenset({"W[1]", "W[2]+", "para-NP-hard"})},
        forbids=None,
        preconditions=(
            "W[1]-hardness for parameter k rules out an EPTAS in k unless FPT=W[1] (the Marx line). This "
            "forbids approximation=EPTAS only when the approximation and parameterization are the same "
            "object/parameter (R1); informational otherwise. The residual approx|parameterized association "
            "after accounting for this bridge is the H2-grade signal (R12)."
        ),
        citation="Marx, Parameterized complexity and approximation algorithms, The Computer Journal 51 (2008).",
        note="R12 bridge: EPTAS-vs-W[1] is theorem-forced; report the residual, not the raw association.",
    ),
]


def validate_entailment_layer(rules: list[EntailmentRule] | None = None) -> list[str]:
    """Return a list of error strings; empty = the layer is internally consistent.

    Enforces R6 (every rule states preconditions + a citation) plus vocabulary coherence: every charge named
    in an antecedent/forbids is a real charge, and every value named is in that charge's allowed vocabulary.
    """
    rules = ENTAILMENT_LAYER if rules is None else rules
    errs: list[str] = []
    seen: set[str] = set()
    for r in rules:
        tag = r.name or "<unnamed>"
        if not r.name:
            errs.append("a rule is missing `name`")
        if r.name in seen:
            errs.append(f"{tag}: duplicate rule name")
        seen.add(r.name)
        # R6: preconditions + citation are mandatory and non-trivial.
        if not r.preconditions or len(r.preconditions.strip()) < 20:
            errs.append(f"{tag}: missing/'too-thin' preconditions (R6 — every rule states exact hypotheses)")
        if not r.citation or len(r.citation.strip()) < 5:
            errs.append(f"{tag}: missing citation (R6)")
        # Vocabulary coherence for antecedent and forbids.
        for role, block in (("antecedent", r.antecedent), ("forbids", r.forbids or {})):
            for charge, values in block.items():
                if charge not in CHARGES:
                    errs.append(f"{tag}: {role} names unknown charge {charge!r}")
                    continue
                bad = set(values) - set(allowed_values(charge))
                if bad:
                    errs.append(f"{tag}: {role} charge {charge!r} has values {sorted(bad)} not in its vocab")
        if not r.antecedent:
            errs.append(f"{tag}: empty antecedent")
    return errs


def theorem_forbidden_by(assignment: dict[str, str]) -> list[str]:
    """Given a (partial) charge assignment {charge: value}, return the names of column-expressible rules that
    forbid it. Used by occupancy triage (R5) to separate theorem-forbidden empty cells from genuine gaps."""
    hits: list[str] = []
    for r in ENTAILMENT_LAYER:
        if r.forbids is None:
            continue
        if not all(assignment.get(c) in vs for c, vs in r.antecedent.items()):
            continue
        for charge, badvals in r.forbids.items():
            if assignment.get(charge) in badvals:
                hits.append(r.name)
                break
    return hits
