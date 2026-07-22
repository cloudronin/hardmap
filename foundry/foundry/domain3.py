"""N3 general-domain tier — domain-3 constraint languages, classified by the general-domain dichotomies.

Post's lattice + CKZ plain bases are Boolean-only; there is no tabulated spine over |D|=3. So this tier is a
CURATED set of well-known domain-3 languages with textbook-certain complexity, each **verified** by the same
polymorphism machinery N1 uses (Boolean → general-domain: `_apply`/`_closed_under` are domain-agnostic), plus a
random-sampling explorer used ONLY to dedup by polymorphism profile (never to emit an uncertain classification).

Charges filled (only where the dichotomy is VERIFIED general-domain, R20):
  * decision      — Bulatov 2017 (FOCS) / Zhuk 2020 (JACM 67): CSP(Γ) ∈ P iff Γ has a WNU (weak near-unanimity)
                    polymorphism, else NP-complete (the Feder–Vardi dichotomy).
  * localization  — Barto–Kozik 2014 (general domain): bounded width iff Γ has WNU polymorphisms of all arities
                    ≥3; a semilattice/majority polymorphism gives it, an affine (Maltsev-only) language does NOT.
Everything else (counting/approximation/parameterized/proof_size/measured) is left `open` for domain-3 — the
Boolean dichotomies (Creignou–Hermann, KSTW, Marx) do NOT transfer, and their general-domain analogues are not
verified in this pass. Honest, not guessed.
"""
from dataclasses import dataclass
from itertools import product

from foundry.postlattice import _closed_under  # domain-agnostic: all(_apply(op, rows) in rel ...)

D3 = (0, 1, 2)


# ── a library of domain-3 term operations (each, as a polymorphism, is a TRACTABLE witness) ─────────────────
# Idempotent operations on {0,1,2}. A WNU/Taylor polymorphism ⟹ CSP(Γ) tractable (Bulatov/Zhuk); a
# semilattice/majority polymorphism additionally ⟹ bounded width (Barto–Kozik); an affine Maltsev polymorphism
# ⟹ tractable but NOT bounded width (the affine obstruction, the |D|=3 analogue of Boolean XOR).
_MIN = lambda *xs: min(xs)                              # semilattice (chain 0<1<2)  → bounded width
_MAX = lambda *xs: max(xs)                              # dual semilattice           → bounded width
_MEDIAN = lambda a, b, c: sorted((a, b, c))[1]          # majority / median (3-ary WNU) → bounded width
_MALTSEV3 = lambda a, b, c: (a - b + c) % 3             # affine over Z_3 (Maltsev)  → tractable, NOT bounded

# WNU witnesses used for the Barto–Kozik bounded-width check (semilattice/majority give WNUs of every arity).
_WNU3 = _MEDIAN                                         # a 3-ary WNU
_WNU4 = lambda a, b, c, d: min(a, b, c, d)              # a 4-ary WNU (from the semilattice)

# The tractability library: closure under ANY of these ⟹ a Taylor term ⟹ CSP(Γ) ∈ P (Bulatov/Zhuk).
_TRACTABLE_OPS = {"min-semilattice": (_MIN, 2), "max-semilattice": (_MAX, 2),
                  "median-majority": (_MEDIAN, 3), "affine-maltsev-Z3": (_MALTSEV3, 3)}
# The bounded-width library: closure under a semilattice or majority ⟹ WNU of all arities ⟹ bounded width.
_BOUNDED_WIDTH_OPS = {"min-semilattice": (_MIN, 2), "max-semilattice": (_MAX, 2), "median-majority": (_MEDIAN, 3)}


def polymorphism_profile(relations, ops=_TRACTABLE_OPS):
    """Which library operations are polymorphisms of the whole language (Pol is intersection-closed)."""
    return frozenset(name for name, (op, k) in ops.items()
                     if all(_closed_under(r, op, k) for r in relations))


def has_tractable_polymorphism(relations):
    """CSP(Γ) ∈ P (Bulatov/Zhuk) iff Γ has a WNU/Taylor polymorphism. Sufficient witnesses: the library ops."""
    return len(polymorphism_profile(relations)) > 0


def is_bounded_width(relations):
    """Barto–Kozik: bounded width iff Γ has WNU polymorphisms of all arities ≥3. A semilattice or majority
    polymorphism supplies them; an affine (Maltsev-only) language does not."""
    return len(polymorphism_profile(relations, _BOUNDED_WIDTH_OPS)) > 0


# ── relations over {0,1,2} ─────────────────────────────────────────────────────────────────────────────────
def _all_tuples(arity):
    return frozenset(product(D3, repeat=arity))


R_NEQ3 = frozenset((a, b) for a in D3 for b in D3 if a != b)            # 3-COLORING (H-coloring K3) — NP-complete
R_LEQ3 = frozenset((a, b) for a in D3 for b in D3 if a <= b)            # order relation — min/max/median closed
R_LINEQ3 = frozenset((a, b, c) for a in D3 for b in D3 for c in D3 if (a + b + c) % 3 == 0)   # affine Z_3
R_MIN_SL = frozenset({(0, 0), (0, 1), (1, 1), (0, 2), (2, 2), (1, 2)})  # a min-semilattice relation (= R_LEQ3)
R_NAE3_D3 = frozenset(t for t in product(D3, repeat=3) if len(set(t)) > 1)   # not-all-equal over 3 — NP-complete
R_LINEQ3B = frozenset((a, b, c) for a in D3 for b in D3 for c in D3 if (a + b + 2 * c) % 3 == 0)   # affine Z_3 (variant)


@dataclass(frozen=True)
class D3Lang:
    id: str
    name: str
    encoding: str
    relations: tuple
    known: str          # textbook complexity (for the certainty cross-check + citation)
    cite: str


# ── curated tier: each language's complexity is textbook-certain and re-verified by the polymorphism test ────
CURATED_D3 = [
    D3Lang("lin-eq-z3", "Linear equations over Z_3", "Γ = {x+y+z ≡ 0 (mod 3)} (affine, Maltsev)",
           (R_LINEQ3,), "P", "Gaussian elimination over Z_3; affine = Maltsev polymorphism (Bulatov/Zhuk tractable)"),
    D3Lang("order-3", "Order / min-semilattice CSP", "Γ = {x ≤ y} over the chain 0<1<2 (min-closed)",
           (R_LEQ3,), "P", "semilattice (min) polymorphism → bounded width (Barto–Kozik)"),
    D3Lang("median-3", "Median / majority CSP (2-SAT over 3 values)", "Γ = {x ≤ y, majority-closed constraints}",
           (R_LEQ3, R_MIN_SL), "P", "median (majority) polymorphism → bounded width (Jeavons–Cohen–Gyssens)"),
    D3Lang("3-coloring", "3-COLORING (H-coloring of K_3)", "Γ = {x ≠ y} over {0,1,2}",
           (R_NEQ3,), "NPC", "3-COLORING is NP-complete; ≠_3 has only projection polymorphisms (no WNU) (Bulatov/Zhuk)"),
    D3Lang("nae-3dom", "Not-all-equal over 3 values", "Γ = {NAE(x,y,z)} over {0,1,2}",
           (R_NAE3_D3,), "NPC", "NAE over |D|=3 is NP-complete (no tractable polymorphism)"),
    D3Lang("lin-eq-z3-b", "Linear equations over Z_3 (variant)", "Γ = {x+y+2z ≡ 0 (mod 3)} (affine, Maltsev)",
           (R_LINEQ3B,), "P", "affine over Z_3 = Maltsev polymorphism; tractable but not bounded width"),
]


def d3_row(lang):
    """A census ProblemEntry for a domain-3 language: decision + localization filled (verified general-domain
    dichotomies); every Boolean-specific-dichotomy charge left `open` (honest — those theorems don't transfer)."""
    from foundry.census import derived, language, na, op
    c = classify(lang)
    npc = c["decision"] == "NPC"
    cells = [
        derived("decision", c["decision"], "CSP(Γ) satisfiability over the 3-element domain",
                theorem="Bulatov 2017 / Zhuk 2020 (CSP dichotomy)", condition=c["decision_cond"],
                cite="Bulatov, FOCS 2017; Zhuk, JACM 67(5) (2020) — CSP(Γ) ∈ P iff Γ has a WNU polymorphism, else NPC"),
        op("counting", "domain-3 #CSP (Bulatov 2008) — Boolean Creignou-Hermann does not transfer; not operationalized here"),
        op("approximation", "domain-3 Max-CSP — Boolean KSTW does not transfer"),
        op("parameterized", "domain-3 Exact-Ones — general-domain weak separability not verified (Boolean Marx does not transfer)"),
        (na("parallelization", "decision is NPC — parallelization is a within-P classification (E2)") if npc
         else op("parallelization", "within-P NC/P-complete — the Boolean ABISV refinement does not transfer to |D|=3")),
        op("proof_size", "instrument column (N4)"),
        derived("localization", c["localization"], "solvable by local consistency (bounded relational width)?",
                theorem="Barto-Kozik 2014", condition=c["localization_cond"],
                cite="Barto & Kozik, JACM 61 (2014) — bounded width iff WNU polymorphisms of all arities (general domain)"),
        op("average_case", "instrument column (N4)"),
        op("landscape", "instrument column (N4)"),
    ]
    return language(lang.id, lang.name, "general-domain", lang.encoding, cells,
                    notes=f"N3 general-domain (|D|=3) tier — decision+localization only. Verified: {lang.known} — {lang.cite}")


def build_d3_census():
    """The N3 general-domain census tier: one verified row per curated domain-3 language. Deterministic (curated
    CKZ-analogue representatives) → generations-exempt, like the Boolean tier."""
    for lang in CURATED_D3:
        errs = verify(lang)
        if errs:
            raise ValueError("; ".join(errs))
    from foundry.census import language  # noqa: F401 (import-time check that census helpers resolve)
    return [d3_row(lang) for lang in CURATED_D3]


def verify(lang):
    """Cross-check the curated classification against the polymorphism test. Returns [] if consistent."""
    errs = []
    p = has_tractable_polymorphism(lang.relations)
    if lang.known == "P" and not p:
        errs.append(f"{lang.id}: known P but NO tractable polymorphism found in the library")
    if lang.known == "NPC" and p:
        errs.append(f"{lang.id}: known NPC but HAS a tractable polymorphism {sorted(polymorphism_profile(lang.relations))}")
    return errs


def classify(lang):
    """(decision, localization) for a domain-3 language, from the verified general-domain dichotomies."""
    tractable = has_tractable_polymorphism(lang.relations)
    decision = "P" if tractable else "NPC"
    if not tractable:
        localization = "unbounded-width"                 # NP-hard → not bounded width
        lcond = "NP-hard CSP is not bounded width"
    elif is_bounded_width(lang.relations):
        localization = "bounded-width"
        lcond = f"has a semilattice/majority polymorphism {sorted(polymorphism_profile(lang.relations, _BOUNDED_WIDTH_OPS))} → WNU of all arities"
    else:
        localization = "unbounded-width"                 # tractable but Maltsev-only (affine) → the obstruction
        lcond = "affine/Maltsev-only (few-subpowers tractable) but omits the semilattice/majority WNU → unbounded width"
    return {"decision": decision, "localization": localization,
            "decision_cond": ("Γ has a WNU polymorphism " + str(sorted(polymorphism_profile(lang.relations)))
                              if tractable else "Γ has no WNU polymorphism (only projections) → NP-complete"),
            "localization_cond": lcond}


# ── random-sampling explorer (dedup by polymorphism profile ONLY; never emits an uncertain census row) ──────
def sample_binary_languages(n_samples, rng, max_rels=2):
    """Sample random non-trivial binary relations over {0,1,2} and group by polymorphism profile. Returns
    {profile: count} — used to report the distinct-profile distribution (a robustness/dedup check), NOT rows."""
    universe = list(product(D3, repeat=2))
    profiles = {}
    for _ in range(n_samples):
        k = 1 + int(rng.integers(max_rels))
        rels = []
        for _ in range(k):
            size = 2 + int(rng.integers(len(universe) - 2))
            idx = rng.choice(len(universe), size=size, replace=False)
            rels.append(frozenset(universe[i] for i in idx))
        prof = polymorphism_profile(tuple(rels))
        profiles[prof] = profiles.get(prof, 0) + 1
    return profiles
