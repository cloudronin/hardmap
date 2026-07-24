"""Foundry's charge vocabulary — the synthetic-census schema (`FOUNDRY_SPEC`).

Foundry reuses the Eightfold atlas kernel (Phase K): the shared validator `eightfold.atlas.validate` and the
Crucible-hardened harness (`eightfold.crucible`, `eightfold.structure`) operate on `FOUNDRY_SPEC` exactly as
they do on `EIGHTFOLD_SPEC` — one code path, two vocabularies.

Rows are **constraint languages** (Boolean co-clone representatives; general-domain languages), NOT the
human-chosen problems of the canon. That is the whole point: a roster no human curated. Charges are assigned
by classification theorems (oracle columns — `claimed` where the literature states the class directly,
`derived` where a dichotomy is *applied* with a logged condition-check) and by the Proof-Census instrument
line (measured columns).

I-phase caveat (N0, deferred): the `parameterized` (Marx) and `parallelization` (ABISV) oracles await I1
verification; the `localization` (Barto–Kozik) condition-check awaits I6. Until verified, those columns are
filled `open`, not guessed — the width claim adjusts accordingly.
"""
from eightfold.charges import ChargeSpec, EntailmentRule

# ── the nine charges: seven oracle columns + two measured instrument columns ──────────────────────────────
FOUNDRY_CHARGES = [
    "decision",         # CSP(Γ) — Schaefer / Bulatov–Zhuk dichotomy (P or NPC)
    "counting",         # #CSP(Γ) — Creignou–Hermann / Dyer–Richerby (FP or #P-complete)
    "approximation",    # Max-CSP(Γ) — KSTW; Raghavendra (UGC-conditional)
    "parameterized",    # weighted CSP(Γ) — Marx FPT/W[1] dichotomy (I1)
    "parallelization",  # within-P: ABISV refinement of Schaefer (I1)
    "proof_size",       # random CSP(Γ) refutation size — Molloy
    "localization",     # bounded relational width — Barto–Kozik (I6, hypothesis-bearing)
    "average_case",     # random ensemble — MEASURED (instrument)
    "landscape",        # random ensemble solution-space geometry — MEASURED (instrument)
]

FOUNDRY_CHARGE_TITLES = {
    "decision": "Decision (CSP)", "counting": "Counting (#CSP)", "approximation": "Approximation (Max-CSP)",
    "parameterized": "Parameterized", "parallelization": "Parallelization", "proof_size": "Proof-size (random)",
    "localization": "Localization (bounded width)", "average_case": "Average-case", "landscape": "Landscape",
}

FOUNDRY_REAL_VALUES = {
    # Schaefer / Bulatov–Zhuk is a DICHOTOMY: P or NPC. NPI-candidate is in the vocab ONLY so the pipeline can
    # emit it — a non-empty NPI row is a pipeline failure (prediction 1's known-answer calibration), never a row.
    "decision": frozenset({"P", "NPI-candidate", "NPC"}),
    "counting": frozenset({"FP", "#P-complete"}),
    "approximation": frozenset({"PO", "PTAS", "APX", "APX-complete", "inapprox"}),
    "parameterized": frozenset({"FPT", "W[1]", "W[2]+", "XP", "para-NP-hard"}),
    "parallelization": frozenset({"NC", "P-complete"}),
    "proof_size": frozenset({"poly", "exp"}),
    "localization": frozenset({"bounded-width", "unbounded-width"}),
    "average_case": frozenset({"easy-on-average", "hard-on-average-crypto",
                               "hard-on-average-provable", "hard-on-average-conjectured"}),
    "landscape": frozenset({"clustering-proven", "clustering-physics", "clustering-OGP-refuted", "freezing-measured"}),
}

# ── entailment layer ──────────────────────────────────────────────────────────────────────────────────────
# The vocab-independent rules carry over from Eightfold (restricted to Foundry's decision vocab); the CSP-native
# bounded-width⟹P rule is added (localization is hypothesis-bearing, I6). N1 adds the remaining CSP-dichotomy
# entailments once the I-phase oracles are verified.
FOUNDRY_ENTAILMENT_LAYER = [
    EntailmentRule(
        name="counting_FP_implies_decision_P",
        antecedent={"counting": frozenset({"FP"})},
        forbids={"decision": frozenset({"NPI-candidate", "NPC"})},
        preconditions=(
            "#CSP(Γ) counts exactly the satisfying assignments whose existence is CSP(Γ); if #solutions ∈ FP "
            "then (count>0) decides satisfiability in poly time, so decision ∈ P. Same object (the constraint "
            "language Γ). E1, carried from Eightfold, restricted to Foundry's decision vocab."
        ),
        citation="Creignou & Hermann, Inf. Comput. 125 (1996); Valiant, TCS 8 (1979).",
        note="Forbids (counting=FP, decision∈{NPI-candidate,NPC}).",
    ),
    EntailmentRule(
        name="parallel_defined_only_within_P",
        antecedent={"decision": frozenset({"NPC"})},
        forbids={"parallelization": frozenset({"NC", "P-complete"})},
        preconditions=(
            "NC ⊆ P. Parallelization (NC vs P-complete) is a within-P classification; for an NP-complete CSP(Γ) "
            "it is undefined (unless P=NP), so the cell must be n.a. Same object Γ. E2, carried from Eightfold."
        ),
        citation="Greenlaw, Hoover & Ruzzo, Limits to Parallel Computation (1995).",
        note="For decision=NPC the parallelization cell must be n.a.",
    ),
    EntailmentRule(
        name="bounded_width_implies_decision_P",
        antecedent={"localization": frozenset({"bounded-width"})},
        forbids={"decision": frozenset({"NPI-candidate", "NPC"})},
        preconditions=(
            "Bounded relational width — CSP(Γ) solvable by local (k-)consistency — implies CSP(Γ) ∈ P (indeed "
            "in NL). Barto–Kozik characterise bounded width by the polymorphisms Γ omits; the implication to P "
            "is unconditional. So localization=bounded-width forbids decision∈{NPI-candidate,NPC}. Same object Γ."
        ),
        citation="Barto & Kozik, Constraint satisfaction problems solvable by local consistency methods, JACM 61 (2014).",
        note="I6 hypothesis-bearing charge: bounded-width⟹P; pre-registered to co-vary with approximation + parameterized.",
    ),
]

FOUNDRY_SPEC = ChargeSpec(
    name="foundry",
    charges=FOUNDRY_CHARGES,
    charge_real_values=FOUNDRY_REAL_VALUES,
    entailment_layer=FOUNDRY_ENTAILMENT_LAYER,
    charge_titles=FOUNDRY_CHARGE_TITLES,
    # Oracle columns may carry `derived` (a dichotomy applied + logged condition-check); the two instrument
    # columns carry `measured`; `measured-scaling` on proof_size mirrors Eightfold.
    derived_allowed=frozenset({"decision", "counting", "approximation", "parameterized",
                               "parallelization", "proof_size", "localization"}),
    measured_allowed=frozenset({"average_case", "landscape"}),
    measured_scaling_allowed=frozenset({"proof_size"}),
    perspective_required=frozenset({"proof_size", "parameterized"}),
    # Coarse traceability: the Boolean co-clone regions (Schaefer classes) + the tiers. `constructed` marks
    # Tier-2 specimens (excluded from natural-population analyses by default). `registration-anchor` marks the
    # canon∩census overlap languages (3-SAT, 2-SAT, XOR-SAT, Horn-SAT, NAE-SAT, 1-in-3-SAT).
    problem_families=frozenset({
        "affine", "horn", "dual-horn", "bijunctive", "essentially-unary", "np-hard-region",
        "general-domain", "registration-anchor", "constructed",
    }),
)
