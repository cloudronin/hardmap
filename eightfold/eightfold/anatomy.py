"""Anatomy — the Structure Atlas (codename Anatomy; spec codename "Strata v2").

Artifact: `results/atlas/anatomy_v1.jsonl`. Contract: `results/atlas/Anatomy-SCHEMA.md` (sealed at S0
BEFORE any derivation ran). This module holds the vocabularies and the validators; the build lives in
`dev/build_anatomy.py` and the freeze in `dev/freeze_anatomy.py`.

FOUNDING LAW — structure never enters the charge table, and no charge value ever informs a structure
cell. The law's three operational edges are in SCHEMA §0.3 and are enforced here mechanically:
  * task *text* may be read (that is R1 typing) -> `derived:from-verified-field`, never plain `derived`;
  * charge-conditioned *coverage* is legal but must be declared in COVERAGE_CONDITIONING;
  * pre-law leakage (R17/R18 charge fields) is consolidated read-only and named as an exception.

NAMING — "Strata" is the SHIPPED charge-applicability layer (`strata.py` -> `atlas_v2.jsonl`), which
merges INTO the charge table; reusing its name would brand the new law with the old design's violation.
Anatomy is a separate artifact and never writes a charge atlas.

This module is stdlib-only, like `atlas.py`/`strata.py`, and imports the frozen kernel read-only.
"""
from __future__ import annotations

# ── §1.1 universes ────────────────────────────────────────────────────────────────────────────────────
NATURAL, BOOLEAN = "natural", "boolean"
UNIVERSES = (NATURAL, BOOLEAN)

# ── §1.3 provenance statuses ──────────────────────────────────────────────────────────────────────────
PROV_ORACLE = "derived:from-oracle"            # mechanical predicate over STRUCTURED data
PROV_FIELD = "derived:from-verified-field"     # sealed rule over agent-drafted prose (two hops, declared)
PROV_CITED = "cited"                           # R20 literature citation
PROV_CODED = "coded"                           # qualified blind-coding instrument
PROV_STRUCTURAL = "structural"                 # the cell is a sentinel
PROV_JUDGED = "judged"                         # owner assignment where a sealed rule could not resolve
PROVENANCE_STATUSES = frozenset(
    {PROV_ORACLE, PROV_FIELD, PROV_CITED, PROV_CODED, PROV_STRUCTURAL, PROV_JUDGED}
)
# `inferred` is FORBIDDEN in both atlases (instance-9's fix, now schema law). Never add it here.
FORBIDDEN_PROVENANCE = frozenset({"inferred"})

SENTINELS = frozenset({"open", "n.a."})
REASON_REQUIRED_VALUES = frozenset({"n.a."})   # `open` is honest absence; `n.a.` must say why

# ── the I3 pin gate (SCHEMA §3.6) — outcome of the Bridge Ledger pinning pass, docs/findings/ ─────────
# A cell may carry a `bridge_citation` ONLY if that ledger row is pinned. "Pinned" includes
# PINNED-WITH-CORRECTION: the correction IS the pin, and the CORRECTED wording is what may be cited.
# 15 rows examined; 3 pinned clean, 10 pinned only with correction, 2 unpinnable.
PINNED_BRIDGES = frozenset({
    "§1.decision", "§1.counting", "§1.parallelization", "§1.parameterized-tw",
    "§2.approximation", "§2.parameterized", "§2.counting",
    "§3.decision", "§4.fo_sparse", "§4.fo_minor_free", "§5.proof_size",
    "§6.kernel", "§7.self_reducibility",
})
UNPINNED_BRIDGES = frozenset({
    "§5.approximation",   # expansion is MANUFACTURED by Dinur's preprocessing -> cannot discriminate rows
    "§7.ogp",             # ensemble-typed, not row-typed; excludes stable algorithms, not P
})
# §1.counting carries a CITATION HAZARD (ledger §9.5): "Courcelle-Makowsky-Rotics 2001" must resolve to the
# DAM 108(1-2):23-52 ENUMERATION paper, NOT the TOCS 33(2):125-150 clique-width OPTIMIZATION paper, which
# forbids edge-set quantification. Cite the DAM paper or the row is mis-attributed.
# §1.parameterized-tw is the SAME Courcelle theorem as §1.decision. Citable, but the two together are ONE
# calibration point — a consumer counting them as independent evidence double-counts one theorem.
DUPLICATE_BRIDGE_GROUPS = (frozenset({"§1.decision", "§1.parameterized-tw"}),)

# ── §1.2 the column registry — universe is declared ONCE, here, not per cell ───────────────────────────
# `values=None` means a structured record or an unbounded scalar (validated by `record_check`).
COLUMNS = {
    "locality_class": {
        "universe": NATURAL, "route": PROV_CODED,
        "values": ("decomposable", "local-covering", "delocalized"),
        "bridge": None},
    # PRESENTATION-RELATIVE BY THEOREM, not definitional (SCHEMA §8). Arity is a property of the CANONICAL
    # ENCODING, not of the problem: 3-SAT presented as a CSP over a ternary relation is `bounded-local`; the
    # same instance presented as a hypergraph covering problem is `unbounded-fanin`, and nothing about the
    # problem moved. So there is no problem-invariant fact in the pinned text to read, and kappa = 0.360
    # between two blind coders MEASURES that absence rather than their carelessness.
    # The problem-invariant version of "how wide are the interactions" is a WIDTH MEASURE OF THE CONSTRAINT
    # HYPERGRAPH (treewidth / hypertree width / submodular width) -- i.e. `decomposition_facts`. The two
    # columns are the same question asked at the wrong and the right level of invariance.
    # Descriptive only; no bet may rest on it (grid Flag 6). Invariance anchors are ledger CANDIDATES and
    # remain unpinned, so they may not be carried as a bridge_citation (§3.6).
    "arity_class": {
        "universe": NATURAL, "route": PROV_FIELD,
        "values": ("bounded-local", "unbounded-fanin", "global-objective"),
        "bridge": None,
        "reliability": {"inter_coder_kappa": 0.360, "raw_agreement": 0.574, "n": 345,
                        "qualification_bar": 0.6, "qualifies": False,
                        "contrast": "locality_class kappa = 0.646"},
        "invariance": "presentation-relative; see Anatomy-SCHEMA §8"},
    "encoding_type": {
        "universe": NATURAL, "route": PROV_FIELD,
        "values": ("graph", "cnf-circuit", "geometric", "matrix-vector", "string", "numeric-set", "other"),
        "bridge": None},
    "objective_type": {
        "universe": NATURAL, "route": PROV_FIELD,
        "values": ("Min-Ones", "Max-Ones", "Max-CSP", "weighted", "global-numeric", "none"),
        "bridge": None},
    "kernel_status": {
        "universe": NATURAL, "route": PROV_CITED,
        "values": ("poly-kernel", "no-poly-unless-coNP⊆NP/poly", "FPT-no-poly-known", "no-kernel-W[1]-hard"),
        "bridge": "§6"},
    "decomposition_facts": {
        "universe": NATURAL, "route": PROV_CITED, "values": None, "bridge": "§1,§2"},
    "reduction_out_degree": {
        "universe": NATURAL, "route": PROV_ORACLE, "values": None, "bridge": None},
    "self_reducibility": {
        "universe": NATURAL, "route": PROV_CITED,
        "values": ("worst-to-average", "random-self-reducible", "none"),
        "bridge": "§7"},
    "engine_type": {
        "universe": BOOLEAN, "route": PROV_ORACLE,
        "values": ("both", "bounded-width", "few-subpowers", "neither"),
        "bridge": "§3"},
    "poly_fingerprint": {
        "universe": BOOLEAN, "route": PROV_ORACLE, "values": None, "bridge": "§3"},
    "class_size": {
        "universe": BOOLEAN, "route": PROV_ORACLE, "values": None, "bridge": None},
}

# the sociology sidecar — quarantined; §3.4's law is enforced by `is_sociology`, consumers must respect it
SOCIOLOGY_COLUMNS = frozenset(
    {"source_funnel", "rn_membership", "rn_route", "admission_wave", "compendium_memberships"}
)

# §1.5 the ten persisted Post's-lattice flags, verbatim and in order
POLY_FINGERPRINT_FLAGS = (
    "0valid", "1valid", "horn", "dualhorn", "bijunctive", "affine",
    "width2affine", "strongly0valid", "IHSB", "general_wsep",
)

# §4 reserved names — typed so a later fill is purely additive (NOT shipped as data in v1)
RESERVED_COLUMNS = {
    "channelness": "coded (new instrument); deferred to Mosaic v3 G0 (prereg_v13)",
    "fo_form": "cited/derived, Ledger §4; no data exists, would require new judging",
    "tuple_density": "derived:from-oracle on the boolean universe; reserved per owner ruling",
    "dual_of": "row-relations edge layer — each edge is a claim carrying a warrant; v1.1",
    "complement_of": "row-relations edge layer; v1.1",
    "restriction_of": "row-relations edge layer; v1.1",
    "objective_variant_of": "row-relations edge layer; v1.1",
}

# §6 coverage-conditioning register — a column whose COVERAGE is conditioned on something other than its
# own definition MUST declare it, because a coverage pattern read as structure is a realized failure mode.
COVERAGE_CONDITIONING = {
    "kernel_status": (
        "coverage conditioned on parameterized == FPT (kernelization is FPT-only). The rows that HAVE a "
        "kernel status all have parameterized constant, so a kernel<->param association is STRUCTURALLY "
        "BLOCKED, not merely unmeasured; only the poly- vs no-poly residual WITHIN FPT is informative."),
    "decomposition_facts": (
        "coverage conditioned on encoding_type in {graph, geometric}, and that eligibility is itself "
        "stratified by locality (decomposable 52% / local-covering 62% / delocalized 81%, grid-relevant "
        "n=111). Coverage is NOT missing-at-random w.r.t. locality; any association with a "
        "locality-conditioned quantity must be reported against this gradient."),
    "reduction_out_degree": (
        "coverage conditioned on membership in the pinned reductions.network snapshot (31 of 345). "
        "Absent is NOT zero; non-members are `open`."),
    "objective_type": (
        "two provenance regimes in one column: 118 rows inherit sealed atlas_v2 strata pins, v3-new rows "
        "derive from the Cat-3 lexicon. Consumers stratifying on it should check provenance_status."),
}


# ── COLUMN PASSPORTS: invariance verdicts (SCHEMA §9) ─────────────────────────────────────────────────
# The prior question no gate asked before: is this column WELL-DEFINED ON ITS OBJECT AT ALL? A column can
# pass coverage, pass variance, and still be measuring an artifact of presentation. Verdicts are AUDITED
# here, not inherited from expectation; two landed differently than expected and are marked as such.
INVARIANT = "invariant"                     # survives re-encoding of the object
ENCODING_RELATIVE = "encoding-relative"     # a property of the chosen presentation
PARAMETER_RELATIVE = "parameter-relative"   # meaningful only against a pinned parameter/ensemble
CORPUS_RELATIVE = "corpus-relative"         # a property of a curated snapshot, not of the problem
INVARIANCE_VERDICTS = frozenset({INVARIANT, ENCODING_RELATIVE, PARAMETER_RELATIVE, CORPUS_RELATIVE})

PASSPORT_INVARIANCE = {
    "poly_fingerprint": (INVARIANT, "property_of: the constraint language, up to pp-interdefinability",
        "The Galois connection Pol-Inv (Geiger 1968; Bodnarchuk-Kaluznin-Kotov-Romov 1969): a relation's "
        "polymorphisms determine its pp-definable closure and vice versa. Polymorphism flags are therefore "
        "invariants of the language, not of any presentation of it -- that is what a polymorphism IS."),
    "engine_type": (INVARIANT, "property_of: the constraint language, up to pp-interdefinability",
        "Derived entirely from poly_fingerprint, so it inherits that invariance. The characterizations it "
        "names are themselves language-level: bounded width <-> SD(^) (Barto-Kozik JACM 2014; necessity "
        "Larose-Zadori 2007), few subpowers <-> k-edge/Maltsev (IMMVW). Bridge cite ONLY in the corrected "
        "form -- ledger §9.2b."),
    "class_size": (ENCODING_RELATIVE, "property_of: the relation AT ITS DECLARED ARITY",
        "AUDIT FINDING, not the expected landing. class_size is the orbit size under coordinate permutation "
        "at the declared arity. A relation padded to a higher arity is the same constraint with a different "
        "orbit size, so the number moves without the language moving. Usable as a weight, never as a feature."),
    "locality_class": (ENCODING_RELATIVE, "property_of: the PINNED canonical task/encoding",
        "Coded from pinned task text only. Its object is the pinned task, which is exactly why the "
        "graph-3-coloring precedent (methods instances 9, 17) governs it: when the name and the pinned task "
        "disagree, the pinned task wins. Qualified at 3-class, kappa 0.646."),
    "arity_class": (ENCODING_RELATIVE, "property_of: the canonical encoding ONLY",
        "Feder-Vardi binarization: any CSP re-encodes to a binary CSP preserving the problem, so arity does "
        "not survive re-encoding -- only the algebraic invariants do. 3-SAT as a ternary CSP is "
        "bounded-local; as a hypergraph covering problem, unbounded-fanin; the problem did not move. "
        "kappa=0.360 MEASURES that absence rather than coder carelessness (SCHEMA §8)."),
    "encoding_type": (ENCODING_RELATIVE, "property_of: the canonical encoding, definitionally",
        "The column's declared object IS the encoding, so encoding-relativity is not a defect here -- it is "
        "the column's definition. It is honest as a covariate and as a typing key for which "
        "decomposition_facts can apply; it is NOT a problem-level fact."),
    "objective_type": (ENCODING_RELATIVE, "property_of: the objective AS EXPRESSED in the pinned task",
        "AUDIT FINDING, not a free pass. The class depends on how the objective is written: a cardinality "
        "of a selected set vs a numeric quantity is a wording call, which is why the sealed Cat-3 pass "
        "needed 30 owner-judged rows and two reason tags ('structural-parameter objective', "
        "'constrained-cardinality variant'). The objective is constitutive of the problem; its CLASSIFICATION "
        "is presentation-relative."),
    "kernel_status": (PARAMETER_RELATIVE, "property_of: (problem, PINNED parameter)",
        "Kernelization is defined relative to a parameter: a problem may admit a poly kernel by one "
        "parameter and none by another. The pinned parameter travels in the cell. Coverage is additionally "
        "FPT-conditioned (§6)."),
    "self_reducibility": (PARAMETER_RELATIVE, "property_of: (problem, ensemble/approximation factor)",
        "Pinned at I3: Ajtai's worst-to-average is one-directional, for gamma = n^O(1) APPROXIMATION "
        "versions over an ENGINEERED distribution; permanent RSR needs |F| >= deg+2 and tolerates only "
        "1/poly error. Neither is a bare problem property -- both are relative to a stated ensemble."),
    "decomposition_facts": (ENCODING_RELATIVE, "property_of: (problem, PINNED structural representation)",
        "The RIGHT level of invariance for anatomy, but still relative -- and the relativity is real, not "
        "pedantic: FMR's pinning showed the treewidth bound depends on WHICH graph (primal / incidence / "
        "signed-incidence) the encoding pins. Width measures survive re-encoding of the problem in the way "
        "arity does not (SCHEMA §8); they do not float free of the chosen representation. Say which graph."),
    "reduction_out_degree": (CORPUS_RELATIVE, "property_of: the PINNED reductions.network snapshot",
        "AUDIT FINDING, and a fourth status the data forced. Out-degree counts reductions SOMEONE RECORDED. "
        "It is a fact about a curated corpus at commit 8089fb4f, not about the problem: a reduction "
        "published tomorrow changes it. Legitimate as a sociology-adjacent covariate; never a structural "
        "feature. Absent is not zero (§2.5)."),
    # reserved names get passports too, so a future fill inherits the typing (verdicts PROVISIONAL -- no data)
    "channelness": (ENCODING_RELATIVE, "property_of: the objective as related to the pinned structure",
        "PROVISIONAL (unmeasured, deferred to G0). Inherits objective_type's relativity: it asks how the "
        "objective couples to structure, and both terms are presentation-relative."),
    "fo_form": (ENCODING_RELATIVE, "property_of: the chosen FO formulation",
        "PROVISIONAL. X-positive/X-negative is a property of a FORMULA, not of a problem; a problem has many "
        "FO formulations. Ledger §4 anchors are PINNED, but they license a class-level PTAS statement, not "
        "a per-row label."),
    "tuple_density": (ENCODING_RELATIVE, "property_of: the relation at its declared arity",
        "PROVISIONAL. |R|/2^arity moves under arity padding for the same reason class_size does."),
    "row_relations": (ENCODING_RELATIVE, "property_of: the pinned encodings of BOTH endpoints",
        "PROVISIONAL (v1.1). A dual_of / complement_of edge is a claim about two pinned presentations; "
        "the spec's own rule that each edge 'is a claim carrying a warrant' is this relativity restated."),
}

# ── BET HISTORY: what each column has ALREADY been spent on (SCHEMA §9.6) ─────────────────────────────
# This turns the passport table from a GATE into a LEDGER. A future prereg reads not only whether a column
# CAN carry a bet but what it has ALREADY carried — closing the double-dipping variant of the failure
# class: two preregs independently spending the same column's one informative contrast and reporting the
# second as fresh evidence.
BET_HISTORY = {
    "locality_class": {
        "sealed_bets": ["prereg_v10 P2 (separate association)", "prereg_v10 P3 (absorption)",
                        "prereg_v10 P4 (composition)", "prereg_v10 P5 (violator fingerprint)",
                        "prereg_v10-addendum-01 (89-row rerun)", "prereg_v13 P3/P4 (Quarry v2 rerun)"],
        "outcomes": ("P2 two-property SPLIT (V=0.56 approx / 0.14 param); P3 3-class INSUFFICIENT then "
                     "2-class powered MISS; P5 HOLDS; P4 INSUFFICIENT"),
        "exposure": "HIGH",
        "note": ("This column's single informative contrast has been spent SIX times across three seals. "
                 "It is the most-leaned-on column in the program. A new bet on it is very likely a "
                 "re-test of an already-scored contrast, not fresh evidence — state explicitly what is "
                 "NEW about the population or the statistic before sealing.")},
    "kernel_status": {
        "sealed_bets": ["prereg_v10 P6 (kernel netting)"],
        "outcomes": ("V(kernel_status, locality) = 0.28 (weak independence); kernel<->param STRUCTURALLY "
                     "BLOCKED (kernelization is FPT-only, so param is constant where kernels exist)"),
        "exposure": "MEDIUM",
        "note": ("The admissible collapse (poly vs no-poly WITHIN FPT) is EXACTLY the contrast P6 already "
                 "scored. Re-posing it is a replication, not a new bet, and must say so.")},
    "engine_type": {
        "sealed_bets": [],
        "outcomes": "the 4-way split was RETIRED AT BUILD (grid Flag 5) before any bet was sealed on it",
        "exposure": "NONE",
        "note": ("Both binaries are UNSPENT. Bridge Ledger §3 marks engine->approx / engine->param as "
                 "'prime real estate' and it genuinely still is — this is the freshest admissible "
                 "structural contrast the program owns.")},
    "poly_fingerprint": {
        "sealed_bets": ["Prism pred-1a (NPI calibration)", "Prism pred-1b (reproduction gate)",
                        "Prism pred-2 (bounded-width marginal)", "Lattice v3 occupancy"],
        "outcomes": "reproduction gate held; pred-3b/4 declared UNTESTABLE at arity<=3 (BW constant)",
        "exposure": "MEDIUM",
        "note": "Spent on the Foundry side; unspent against the natural-atlas bridge."},
    "reduction_out_degree": {
        "sealed_bets": ["prereg_v10 P7 (out-degree probe, 31-row floor, exploratory)"],
        "outcomes": "exploratory only; never scored as a confirmatory bet",
        "exposure": "LOW", "note": "Covariate only in any case (corpus-relative)."},
    "objective_type": {
        "sealed_bets": [], "outcomes": "used descriptively in the Strata coverage report (v2)",
        "exposure": "NONE", "note": "Never carried a sealed bet."},
    "arity_class": {
        "sealed_bets": [], "outcomes": "never resolved to a sidecar; never scored",
        "exposure": "NONE",
        "note": "Unspent, but inadmissible on readability — unspent is not the same as usable."},
    "encoding_type": {"sealed_bets": [], "outcomes": "new at S2", "exposure": "NONE", "note": None},
    "class_size": {"sealed_bets": [], "outcomes": "used as a weight in the Prism/Lattice rosters",
                   "exposure": "NONE", "note": "Weight, never a feature."},
    "self_reducibility": {"sealed_bets": [], "outcomes": "never scored", "exposure": "NONE", "note": None},
    "decomposition_facts": {"sealed_bets": [], "outcomes": "new at S2", "exposure": "NONE",
                            "note": "Unspent — and the invariant-level twin of arity_class (SCHEMA §8)."},
}


# G0 BINDING (owner ruling, 2026-07-25): a sealed feature list may draw ONLY from columns whose passport
# reads invariant-or-pinned-relative AND unstarved AND (if coded) qualified. Relativity is not
# disqualifying -- UNDECLARED relativity is. This is the rule that closes the class all three build-time
# catches belonged to: no bet sealed on a column that could not carry it.
def passport_admissible(column: str, passports: dict) -> tuple:
    """Returns (admissible: bool, reasons: list[str]) for G0 feature-list eligibility."""
    p = (passports or {}).get("columns", {}).get(column)
    if p is None:
        return False, [f"{column}: no passport — undeclared columns are never admissible"]
    bad = []
    if p.get("invariance") not in INVARIANCE_VERDICTS:
        bad.append(f"{column}: invariance verdict missing or unrecognized")
    if p.get("invariance") != INVARIANT and not p.get("property_of"):
        bad.append(f"{column}: relative column must declare what it is a property of")
    # CORPUS-RELATIVE is declared and pinned, but it is a fact about a curated snapshot rather than about
    # the problem — a reduction published tomorrow moves it. Covariate only, like the sociology sidecar.
    if p.get("invariance") == CORPUS_RELATIVE:
        bad.append(f"{column}: CORPUS-RELATIVE — a property of a curated snapshot, not of the problem; "
                   f"admissible as a covariate, never as a structural feature")
    var = p.get("variance", {})
    # A RECORD-VALUED column is not itself a feature — you cannot contrast on a dict. It is admissible only
    # through a NAMED PROJECTION whose own marginals clear the floor. (Caught by running the gate on real
    # data: `decomposition_facts` and `poly_fingerprint` both read admissible purely by being typed
    # non-categorical, which is a pass by omission rather than by evidence.)
    if var.get("kind") == "record-valued":
        c = p.get("admissible_collapse")
        if not c or c.get("starved"):
            bad.append(f"{column}: RECORD-VALUED — a record cannot be contrasted on; admissible only via a "
                       f"named projection with its own unstarved marginals, and none is declared")
        else:
            bad.append(f"{column}: RECORD-VALUED — not a feature as-is; use the declared projection "
                       f"({c['collapse']}), which must be sealed in the prereg")
    if var.get("starved"):
        bad.append(f"{column}: STARVED — {var.get('starved_note', 'a cell is below the Cochran floor')}")
    # `starved: None` is NOT a pass. Distinguish "no categorical census applies" from "never censused".
    elif var.get("starved") is None and var.get("kind") != "non-categorical":
        bad.append(f"{column}: variance NOT CENSUSED ({var.get('kind')}) — an untested column cannot be "
                   f"sealed on; it becomes admissible when built and censused")
    # Readability gates on the PRESENCE of a readability verdict, not on the route. A column can be derived
    # and still have a measured readability (arity_class), and a failing kappa must exclude it either way.
    r = p.get("readability")
    if r is not None and not r.get("qualifies"):
        bad.append(f"{column}: readability FAILS — kappa {r.get('kappa')} below the "
                   f"{r.get('bar')} bar, no qualifying resolution demonstrated")
    return (not bad), bad


# ── TYPING SENTINELS: rows registered as instruments because they keep catching drift ─────────────────
# A row that has forced the same class of correction repeatedly is not unlucky — it is the place where the
# id / object / encoding seams cross, which makes it a TEST CASE. Registered the way `knapsack` became the
# dissociation exhibit. Any future typing rule, validator, or coder qualification SHOULD include these.
TYPING_SENTINELS = {
    "graph-3-coloring": {
        "role": "standing typing sentinel — the known-hard anchor for id/object/encoding drift",
        "forced_corrections": [
            ("methods instance 9", "audit-touched row conflated with a gradient-bending one (role drift)"),
            ("methods instance 17", "object-drift class named; the pinned task, not the id, defines the object"),
            ("Anatomy S2", "decomposition_facts: the pinned encoding is a random G(n,m) ENSEMBLE, a.a.s. "
                           "non-planar with treewidth Theta(n) (Gao, DAM 160:566-578, 2012), so general-problem "
                           "planar/treewidth facts describe a DIFFERENT object; both fields nulled"),
        ],
        "why_it_catches": ("its id names a classic decision problem, its pinned task is a promise/gap "
                           "version, and its pinned encoding is a random ensemble — three different objects "
                           "reachable from one row, so any rule that conflates them fails here first"),
        "use": "include in every typing-rule test set, validator selftest, and coder qualification batch",
    },
    "knapsack": {
        "role": "dissociation exhibit (registered earlier; recorded here for one registry)",
        "forced_corrections": [("Mosaic L0", "FPTAS x W[1] — decomposable structure, off-diagonal "
                                             "coordinate; the two-property split's originating case")],
        "why_it_catches": "structure and charge coordinates provably come apart on this row",
        "use": "anchor for any locality/structure instrument and any coupling claim",
    },
}


def is_sociology(column: str) -> bool:
    """§3.4 law: a sociology column may appear only as a control term, never in a structural claim."""
    return column in SOCIOLOGY_COLUMNS


def columns_for(universe: str) -> tuple:
    """The columns defined on a universe. Absence outside it is typed HERE, not by ceremonial n.a. cells."""
    return tuple(sorted(c for c, m in COLUMNS.items() if m["universe"] == universe))


def independent_bridge_count(citations) -> int:
    """How many INDEPENDENT calibration points a set of bridge citations is worth. Collapses each known
    duplicate group to one — §1.decision and §1.parameterized-tw are the same Courcelle theorem, and
    counting them twice would inflate the calibration layer with one theorem wearing two hats."""
    cites = set(citations)
    for group in DUPLICATE_BRIDGE_GROUPS:
        hit = cites & group
        if len(hit) > 1:
            cites -= hit
            cites.add(sorted(hit)[0])
    return len(cites)


def validate_feature_cell(cell: dict, universe: str, pinned_bridges=None) -> list:
    """Gate one feature cell. Returns a list of violation strings (empty == clean).

    Enforces, in order: known column · column defined on THIS universe · not a reserved name · value in
    the column's vocabulary or a sentinel · MANDATORY reason on `n.a.` · provenance status known and not
    forbidden · route-specific companions (citation for `cited`, instrument_ref for `coded`) · and the
    pin-before-net gate on any bridge_citation (§3.6).
    """
    errs = []
    col = cell.get("feature")
    tag = f"anatomy[{col or '?'}]"
    if col in RESERVED_COLUMNS:
        return [f"{tag}: reserved name shipped as data (v1 reserves it: {RESERVED_COLUMNS[col]})"]
    meta = COLUMNS.get(col)
    if meta is None:
        return [f"{tag}: unknown column (not in the sealed registry)"]
    if meta["universe"] != universe:
        errs.append(f"{tag}: defined on universe {meta['universe']!r} but found on a {universe!r} row")

    val, prov = cell.get("value"), cell.get("provenance_status")
    # a structured record (dict/list) is a legitimate value and is unhashable -- test membership safely
    is_sentinel = isinstance(val, str) and val in SENTINELS
    if is_sentinel:
        if val in REASON_REQUIRED_VALUES and not cell.get("reason"):
            errs.append(f"{tag}: value 'n.a.' requires a non-empty reason (mandatory)")
    elif meta["values"] is not None and val not in meta["values"]:
        errs.append(f"{tag}: value {val!r} not in {list(meta['values'])} (nor a sentinel)")

    if prov in FORBIDDEN_PROVENANCE:
        errs.append(f"{tag}: provenance_status {prov!r} is FORBIDDEN in both atlases (instance-9 fix)")
    elif prov not in PROVENANCE_STATUSES:
        errs.append(f"{tag}: provenance_status {prov!r} not in {sorted(PROVENANCE_STATUSES)}")
    else:
        if prov == PROV_CITED and not (cell.get("citation") or "").strip():
            errs.append(f"{tag}: provenance_status 'cited' requires a non-empty citation")
        if prov == PROV_CODED and not (cell.get("instrument_ref") or "").strip():
            errs.append(f"{tag}: provenance_status 'coded' requires an instrument_ref")
        if prov == PROV_JUDGED and not (cell.get("reason") or "").strip():
            errs.append(f"{tag}: provenance_status 'judged' requires a reason")
        if is_sentinel and prov not in (PROV_STRUCTURAL, PROV_CITED, PROV_JUDGED):
            errs.append(f"{tag}: sentinel value {val!r} should carry provenance 'structural' (got {prov!r})")

    bridge = cell.get("bridge_citation")
    allow = PINNED_BRIDGES if pinned_bridges is None else pinned_bridges   # gate is DEFAULT-ON
    if bridge and bridge not in allow:
        errs.append(f"{tag}: bridge_citation {bridge!r} is not PINNED in the Bridge Ledger §9 "
                    f"(pin-before-net, SCHEMA §3.6) — fall back to `open` rather than borrow the warrant")
    return errs


def validate_anatomy_row(row: dict, pinned_bridges=None) -> list:
    """Gate one artifact row: universe known, key fields present for that universe, no duplicate columns,
    every feature cell clean, and no column from the OTHER universe present."""
    errs = []
    uni = row.get("universe")
    rk = row.get("row_key")
    tag = f"anatomy[{rk or '?'}]"
    if uni not in UNIVERSES:
        return [f"{tag}: universe {uni!r} not in {list(UNIVERSES)}"]
    if not rk:
        errs.append(f"{tag}: row_key missing")
    if uni == NATURAL and not row.get("problem_id"):
        errs.append(f"{tag}: natural row requires problem_id")
    if uni == BOOLEAN:
        for k in ("arity", "relation"):
            if row.get(k) is None:
                errs.append(f"{tag}: boolean row requires {k}")

    seen = set()
    for cell in row.get("features", []):
        col = cell.get("feature")
        if col in seen:
            errs.append(f"{tag}: duplicate cell for column {col!r}")
        seen.add(col)
        errs.extend(validate_feature_cell(cell, uni, pinned_bridges))
    return errs


def validate_level_registry() -> list:
    """Self-consistency of the sealed registry itself (runs before any data is touched)."""
    errs = []
    for col, m in COLUMNS.items():
        if m["universe"] not in UNIVERSES:
            errs.append(f"registry[{col}]: bad universe {m['universe']!r}")
        if m["route"] not in PROVENANCE_STATUSES:
            errs.append(f"registry[{col}]: bad route {m['route']!r}")
        if col in RESERVED_COLUMNS:
            errs.append(f"registry[{col}]: column is both live and reserved")
    for col in COVERAGE_CONDITIONING:
        if col not in COLUMNS:
            errs.append(f"coverage-conditioning names unknown column {col!r}")
    overlap = SOCIOLOGY_COLUMNS & set(COLUMNS)
    if overlap:
        errs.append(f"sociology columns must stay out of the structural registry: {sorted(overlap)}")
    return errs


def selftest_anatomy(verbose: bool = False) -> int:
    """Known-answer gate on the validators, run before they touch real data (the defect-#15 habit)."""
    bad = []
    reg = validate_level_registry()
    if reg:
        bad += reg

    def expect(errs, want_substr, label):
        hit = any(want_substr in e for e in errs)
        if not hit:
            bad.append(f"{label}: expected an error containing {want_substr!r}, got {errs}")

    # (a) n.a. without a reason must fail
    expect(validate_feature_cell(
        {"feature": "kernel_status", "value": "n.a.", "provenance_status": PROV_STRUCTURAL}, NATURAL),
        "requires a non-empty reason", "na-without-reason")
    # (b) a boolean column on a natural row must fail
    expect(validate_feature_cell(
        {"feature": "engine_type", "value": "both", "provenance_status": PROV_ORACLE}, NATURAL),
        "found on a 'natural' row", "wrong-universe")
    # (c) `inferred` must be rejected outright
    expect(validate_feature_cell(
        {"feature": "arity_class", "value": "bounded-local", "provenance_status": "inferred"}, NATURAL),
        "FORBIDDEN", "inferred-rejected")
    # (d) coded without an instrument_ref must fail
    expect(validate_feature_cell(
        {"feature": "locality_class", "value": "decomposable", "provenance_status": PROV_CODED}, NATURAL),
        "requires an instrument_ref", "coded-without-instrument")
    # (e) an UNPINNED bridge citation must fail with the DEFAULT gate (pin-before-net, §3.6).
    #     §5.approximation is genuinely unpinnable: Dinur's expansion is manufactured by the preprocessing
    #     lemma, so it cannot discriminate rows at all.
    expect(validate_feature_cell(
        {"feature": "decomposition_facts", "value": "open", "provenance_status": PROV_STRUCTURAL,
         "bridge_citation": "§5.approximation"}, NATURAL),
        "not PINNED", "unpinned-bridge-default-gate")
    # (e2) a PINNED bridge must pass with the same default gate
    if validate_feature_cell(
            {"feature": "engine_type", "value": "both", "provenance_status": PROV_ORACLE,
             "bridge_citation": "§3.decision"}, BOOLEAN):
        bad.append("pinned-bridge: §3.decision is PINNED and should validate clean")
    # (e3) the duplicate group collapses to ONE calibration point
    if independent_bridge_count({"§1.decision", "§1.parameterized-tw"}) != 1:
        bad.append("duplicate-collapse: §1.decision + §1.parameterized-tw are one Courcelle theorem")
    if independent_bridge_count({"§1.decision", "§3.decision"}) != 2:
        bad.append("duplicate-collapse: distinct bridges must not be merged")
    # (f) a reserved name shipped as data must fail
    expect(validate_feature_cell(
        {"feature": "channelness", "value": "x", "provenance_status": PROV_CODED}, NATURAL),
        "reserved name", "reserved-shipped")
    # (g) a clean cell must pass
    ok = validate_feature_cell(
        {"feature": "arity_class", "value": "bounded-local", "provenance_status": PROV_FIELD}, NATURAL)
    if ok:
        bad.append(f"clean-cell: expected no errors, got {ok}")

    # ── REAL-ROW CASES (SCHEMA §3.4b) ─────────────────────────────────────────────────────────────────
    # The synthetic cases above all use SCALAR values, and that is exactly how a hashability bug survived
    # a green 10-case suite until first contact with real data (methods-thread instance 19b). Every column
    # TYPE this validator guards must therefore be exercised on a shape the corpus actually contains.

    # (h) a real record-valued cell — the ten-flag poly_fingerprint, verbatim shape from prism_v2_charges
    real_fingerprint = {"0valid": True, "1valid": False, "horn": True, "dualhorn": False,
                        "bijunctive": True, "affine": False, "width2affine": True,
                        "strongly0valid": False, "IHSB": True, "general_wsep": False}
    r = validate_feature_cell(
        {"feature": "poly_fingerprint", "value": real_fingerprint, "provenance_status": PROV_ORACLE,
         "bridge_citation": "§3.decision"}, BOOLEAN)
    if r:
        bad.append(f"real-record-cell: a ten-flag poly_fingerprint must validate clean, got {r}")
    # (i) a real integer-valued cell — out-degree is an unbounded scalar, not a vocabulary member
    r = validate_feature_cell(
        {"feature": "reduction_out_degree", "value": 15, "provenance_status": PROV_ORACLE}, NATURAL)
    if r:
        bad.append(f"real-int-cell: an integer out-degree must validate clean, got {r}")

    # (j) if the artifact exists, validate real rows of BOTH universes end to end
    try:
        from pathlib import Path
        art = Path(__file__).resolve().parent / "results" / "atlas" / "anatomy_v1.jsonl"
        if art.exists():
            import json
            seen = {}
            for line in art.read_text().splitlines():
                if not line.strip():
                    continue
                row = json.loads(line)
                seen.setdefault(row["universe"], []).append(row)
            for uni, rows in seen.items():
                for row in rows[:25] + rows[-25:]:
                    errs = validate_anatomy_row(row)
                    if errs:
                        bad.append(f"real-row[{uni}/{row['row_key']}]: {errs[:2]}")
                        break
            if set(seen) != set(UNIVERSES):
                bad.append(f"real-row coverage: artifact has universes {sorted(seen)}, expected {list(UNIVERSES)}")
    except Exception as exc:  # noqa: BLE001 — a selftest must never mask a real failure as a pass
        bad.append(f"real-row case raised {type(exc).__name__}: {exc}")

    if verbose or bad:
        for b in bad:
            print(f"  FAIL {b}")
    print(f"anatomy selftest: {'PASS' if not bad else f'{len(bad)} FAILURES'}")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(selftest_anatomy(verbose=True))
