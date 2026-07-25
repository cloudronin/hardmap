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
# 15 rows examined; 3 pinned clean, 9 pinned only with correction, 3 unpinnable.
PINNED_BRIDGES = frozenset({
    "§1.decision", "§1.parallelization", "§1.parameterized-tw",
    "§2.approximation", "§2.parameterized", "§2.counting",
    "§3.decision", "§4.fo_sparse", "§4.fo_minor_free", "§5.proof_size",
    "§6.kernel", "§7.self_reducibility",
})
UNPINNED_BRIDGES = frozenset({
    "§1.counting",        # open: is Courcelle-Makowsky-Rotics 2001 treewidth or CLIQUE-width?
    "§5.approximation",   # expansion is MANUFACTURED by Dinur's preprocessing -> cannot discriminate rows
    "§7.ogp",             # ensemble-typed, not row-typed; excludes stable algorithms, not P
})
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
    "arity_class": {
        "universe": NATURAL, "route": PROV_FIELD,
        "values": ("bounded-local", "unbounded-fanin", "global-objective"),
        "bridge": None},
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
    if val in SENTINELS:
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
        if val in SENTINELS and prov not in (PROV_STRUCTURAL, PROV_CITED, PROV_JUDGED):
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

    if verbose or bad:
        for b in bad:
            print(f"  FAIL {b}")
    print(f"anatomy selftest: {'PASS' if not bad else f'{len(bad)} FAILURES'}")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(selftest_anatomy(verbose=True))
