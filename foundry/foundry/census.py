"""Census row builders + a hand-checked toy stratum.

A census row is a **constraint language** carried in Eightfold's `ProblemEntry` dataclass (reused verbatim):
`problem_id` = the language id, `problem_family` = its Boolean co-clone region, `canonical_encoding` = the
generating relation set. Cells are Eightfold `ChargeCell`s validated by the shared kernel with `FOUNDRY_SPEC`.

The toy stratum below is NOT the census — it is a hand-checked fixture proving the kernel reuse end-to-end
(and giving the harness something to run on) until N1's Post's-lattice/CKZ roster + dichotomy oracles exist.
Oracle columns awaiting I-phase verification (parameterized/Marx, parallelization/ABISV via the *dichotomy*)
are left `open` here, not guessed.
"""
from eightfold.atlas import ChargeCell, ProblemEntry

DATE = "2026-07-21"
REVIEWER = "foundry-N0"


def cell(charge, value, task, *, status="claimed", cite=None, condition_check=None, perspective=None):
    """A real-valued cell. `derived` needs a dichotomy citation + condition_check {theorem, condition, side}
    with side==value (kernel gate 6b); `claimed` needs a citation."""
    prov = {}
    if cite:
        prov["citation"] = cite
    if condition_check is not None:
        prov["condition_check"] = condition_check
    return ChargeCell(charge, value, task, status, prov, perspective)


def derived(charge, value, task, *, theorem, condition, cite, perspective=None):
    """A dichotomy-derived cell: logs the per-language condition-check whose `side` is the value.
    `perspective` is required for perspective-dependent charges (parameterized = the parameter; proof_size = the
    proof system) — kernel gate 5."""
    return cell(charge, value, task, status="derived", cite=cite, perspective=perspective,
                condition_check={"theorem": theorem, "condition": condition, "side": value})


def na(charge, why):
    return ChargeCell(charge, "n.a.", why, "structural")


def op(charge, task):
    return ChargeCell(charge, "open", task, "structural")


def language(lang_id, name, family, encoding, cells, notes=None):
    return ProblemEntry(lang_id, name, family, encoding, cells, DATE, REVIEWER, notes)


# ── toy stratum (hand-checked; three co-clone regions incl. the XOR deceptive-terrain control) ────────────
def toy_census():
    affine = language(
        "affine-xor", "Affine / XOR (linear equations over GF(2))", "affine",
        "Γ = {x⊕y⊕z=0, x⊕y=1, x=1}  (relations closed under the affine/Maltsev polymorphism)",
        [
            derived("decision", "P", "CSP(Γ) satisfiability",
                    theorem="Schaefer 1978", condition="Γ is affine (closed under x−y+z over GF(2))", cite="Schaefer, STOC 1978"),
            derived("counting", "FP", "#CSP(Γ): count satisfying assignments",
                    theorem="Creignou-Hermann 1996", condition="affine → Gaussian elimination counts the solution coset", cite="Creignou & Hermann, Inf. Comput. 125 (1996)"),
            cell("approximation", "inapprox", "Max-CSP(Γ): maximise satisfied constraints",
                 cite="Håstad, JACM 48 (2001) — Max-3LIN has no (1/2+eps)-approx unless P=NP"),
            op("parameterized", "weighted CSP(Γ), parameter = solution weight — Marx dichotomy (I1 pending)"),
            cell("parallelization", "NC", "within-P: is CSP(Γ) in NC?",
                 cite="Gaussian elimination over GF(2) is in NC (Mulmuley 1987)"),
            cell("proof_size", "exp", "resolution refutation size of random unsatisfiable Γ-instances",
                 cite="Ben-Sasson & Wigderson, JACM 48 (2001) — random 3-XOR needs exp resolution", perspective="Resolution"),
            derived("localization", "unbounded-width", "solvable by local consistency?",
                    theorem="Barto-Kozik 2014", condition="affine omits no bounded-width obstruction but is NOT bounded width (needs the Maltsev/few-subpowers algorithm, not local consistency)", cite="Barto & Kozik, JACM 61 (2014); Larose & Zádori 2007"),
            op("average_case", "random Γ-CSP ensemble (density-dialed) — instrument column (N4)"),
            cell("landscape", "clustering-proven", "solution-space geometry of random Γ-instances",
                 cite="Achlioptas-style / OGP for random XOR (rigorous)"),
        ],
        notes="Deceptive-terrain control: easy decision (P) yet hard landscape/approximation — the model must place it distinctively (a pre-registered check).",
    )
    horn = language(
        "horn", "Horn (definite clauses)", "horn",
        "Γ = Horn relations (each clause ≤ one positive literal); closed under min",
        [
            derived("decision", "P", "CSP(Γ) satisfiability",
                    theorem="Schaefer 1978", condition="Γ is Horn (closed under the min/∧ polymorphism)", cite="Schaefer, STOC 1978"),
            derived("counting", "#P-complete", "#CSP(Γ): count satisfying assignments",
                    theorem="Creignou-Hermann 1996", condition="Horn is outside the FP counting classes (affine/2-monotone)", cite="Creignou & Hermann, Inf. Comput. 125 (1996)"),
            op("approximation", "Max-Horn — KSTW class (N1)"),
            op("parameterized", "Marx dichotomy (I1 pending)"),
            cell("parallelization", "P-complete", "within-P: is CSP(Γ) in NC?",
                 cite="Horn-SAT / unit propagation is P-complete (Greenlaw-Hoover-Ruzzo 1995)"),
            op("proof_size", "resolution size of random Horn-unsat instances (N4)"),
            derived("localization", "bounded-width", "solvable by local consistency?",
                    theorem="Barto-Kozik 2014", condition="Horn has a semilattice (min) polymorphism → bounded width (arc consistency decides)", cite="Barto & Kozik, JACM 61 (2014)"),
            op("average_case", "instrument column (N4)"),
            op("landscape", "instrument column (N4)"),
        ],
    )
    threesat = language(
        "3-sat", "3-SAT (all Boolean clauses of width 3)", "np-hard-region",
        "Γ = {all ternary clauses}; NAE/1-in-3/general — the intractable co-clone",
        [
            derived("decision", "NPC", "CSP(Γ) satisfiability",
                    theorem="Schaefer 1978", condition="Γ is none of the six tractable Schaefer classes → NP-complete", cite="Schaefer, STOC 1978"),
            derived("counting", "#P-complete", "#CSP(Γ)",
                    theorem="Creignou-Hermann 1996", condition="NP-hard decision → #P-complete counting", cite="Creignou & Hermann, Inf. Comput. 125 (1996)"),
            cell("approximation", "APX-complete", "Max-3SAT: maximise satisfied clauses",
                 cite="KSTW 2001 — Max-3SAT is APX-complete"),
            op("parameterized", "Marx dichotomy (I1 pending)"),
            na("parallelization", "decision is NPC — parallelization is a within-P classification (E2)"),
            cell("proof_size", "exp", "resolution refutation size of random unsatisfiable 3-CNF",
                 cite="Chvátal & Szemerédi, JACM 35 (1988)", perspective="Resolution"),
            derived("localization", "unbounded-width", "solvable by local consistency?",
                    theorem="Barto-Kozik 2014", condition="NP-hard CSP is not bounded width (local consistency cannot decide it unless P=NP)", cite="Barto & Kozik, JACM 61 (2014)"),
            op("average_case", "instrument column (N4)"),
            op("landscape", "instrument column (N4)"),
        ],
        notes="Registration anchor (canon∩census): 3-SAT is present in both the Eightfold canon and the census.",
    )
    return [affine, horn, threesat]
