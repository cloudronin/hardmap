#!/usr/bin/env python3
"""Sounding v3 — the widened, ramped survey. EXPLORATORY. NO SCORED PREDICTIONS.

TRACK 1 — WIDEN. Seven new rows from the track-1 census, six of them MARROW-EXCLUDED (unbounded-arity
scopes, no fixed finite template, closure anatomy underivable by theorem). The probe's unique reach is
exactly there, so every such row read is territory nothing else touches.

TRACK 2 — RAMP. Every row is re-read across a declared difficulty ramp, 4-6 steps, the ramp parameter
named per family. EACH STEP DRAWS ITS OWN MATCHED CONTROL: r moves with difficulty, so a control reused
across steps would be matched to the wrong size — which is the size-confound this whole statistic exists
to remove, reintroduced through the back door.

INHERITED VERBATIM FROM v2, none of it re-litigated:
  distinct m-subsets only · matched random control at every reading · raw-difference excess with the
  standardized value shipped unscored beside it · full per-reading provenance · forcedness DERIVED from
  Marrow's pinned templates (never a hand list) with ASSERTED entries carrying their argument ·
  INSUFFICIENT-r flagged and left in the trajectory as a gap, NEVER interpolated over.

No verdicts. No shape claims. No narration. Anything interesting goes to the banked-questions file.
"""
import hashlib
import json
import random
import sys
from itertools import combinations, product
from pathlib import Path
from statistics import mean, pstdev

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "dev"))
sys.path.insert(0, str(ROOT.parent / "eightfold"))
from sounding_v1 import BOOL_OPS, D3_OPS, violation                                # noqa: E402
from sounding_forced_derive import load_marrow, forced_flavours, ASSERTED, REGIONS_INHERITING  # noqa: E402
from eightfold import atlas as A                                                    # noqa: E402

LAT = ROOT / "foundry" / "results" / "lattice"
OUT = LAT / "sounding_v3_survey.json"
CENSUS = LAT / "sounding_v3_track1_census.json"
SEED, N_INST, K_CTRL, CTRL_CAP, MEAS_CAP = 20260726, 3, 25, 800, 5000
INSUFF_R = 10


# ── domain-4 blend operations, for Sudoku (the survey's first |D|=4 row) ─────────────────────────────
D4_OPS = {
    "median":   (lambda ts: tuple(sorted(c)[1] for c in zip(*ts)), 3),
    "maltsev4": (lambda ts: tuple((c[0] - c[1] + c[2]) % 4 for c in zip(*ts)), 3),
    "min":      (lambda ts: tuple(min(c) for c in zip(*ts)), 2),
    "max":      (lambda ts: tuple(max(c) for c in zip(*ts)), 2),
}

# ASSERTED NOT-FORCED — a claim that nothing is forced is still a claim and ships its argument.
ASSERTED_NOT_FORCED = {
    "sudoku": ("the constraint template is disequality on a 4-element domain — CSP(K_4)-shaped. Like "
               "CSP(K_3), a complete-graph target admits no nontrivial polymorphism among the library "
               "operations, so NO flavour is forced to zero. Every zero that appears in this row's "
               "trajectory, if any appears, is a genuine reading rather than a definition."),
}


def shidoku_grids():
    """All 288 valid 4x4 Shidoku grids. Enumerated once, verified against the known count."""
    out = []
    def fill(g, i):
        if i == 16:
            out.append(tuple(g)); return
        r, c = divmod(i, 4)
        for v in range(4):
            if any(g[4 * r + cc] == v for cc in range(c)):  continue
            if any(g[4 * rr + c] == v for rr in range(r)):  continue
            br, bc = 2 * (r // 2), 2 * (c // 2)
            if any(g[4 * (br + a) + bc + b] == v for a in (0, 1) for b in (0, 1)
                   if 4 * (br + a) + bc + b < i):           continue
            g.append(v); fill(g, i + 1); g.pop()
    fill([], 0)
    assert len(out) == 288, f"Shidoku ground truth moved: {len(out)} != 288"
    return out


_SHIDOKU = None


def sudoku(rng, clues):
    """THE RAMP RUNS ON CONSTRAINT REMOVAL, not instance size — the survey's first such row. `clues` is
    the number of revealed cells; the region is every valid grid agreeing with them. Descending clue count
    walks from the puzzle regime (r -> 1, honestly INSUFFICIENT) to the blank board (all 288)."""
    global _SHIDOKU
    if _SHIDOKU is None:
        _SHIDOKU = shidoku_grids()
    k = int(clues)
    if k == 0:
        return [("solutions", list(_SHIDOKU))]
    src = _SHIDOKU[rng.randrange(len(_SHIDOKU))]
    cells = rng.sample(range(16), k)
    region = [g for g in _SHIDOKU if all(g[c] == src[c] for c in cells)]
    return [("solutions", region)] if region else []


def G(n, p, rng):
    return [(i, j) for i in range(n) for j in range(i + 1, n) if rng.random() < p]


# ── track 1: the new generators (six Marrow-excluded) ─────────────────────────────────────────────────
def set_cover(rng, m):
    U = 9; S = [tuple(rng.sample(range(U), 3)) for _ in range(m)]
    f = [s for s in product((0, 1), repeat=len(S))
         if len({e for i, b in enumerate(s) if b for e in S[i]}) == U]
    if not f: return []
    best = min(sum(s) for s in f)
    return [("feasible", f), ("optimal", [s for s in f if sum(s) == best])]


def hitting_set(rng, m):
    U = 10; S = [tuple(rng.sample(range(U), 3)) for _ in range(m)]
    f = [s for s in product((0, 1), repeat=U) if all(any(s[e] for e in st) for st in S)]
    if not f: return []
    best = min(sum(s) for s in f)
    return [("feasible", f), ("optimal", [s for s in f if sum(s) == best])]


def _acyclic(E, keep):
    adj = {v: [] for v in keep}
    for a, b in E:
        if a in keep and b in keep: adj[a].append(b); adj[b].append(a)
    seen = set()
    for s in keep:
        if s in seen: continue
        st = [(s, -1)]; seen.add(s)
        while st:
            u, par = st.pop()
            for w in adj[u]:
                if w == par: continue
                if w in seen: return False
                seen.add(w); st.append((w, u))
    return True


def fvs(rng, p):
    n = 10; E = G(n, p, rng)
    f = [s for s in product((0, 1), repeat=n) if _acyclic(E, {v for v in range(n) if not s[v]})]
    if not f: return []
    best = min(sum(s) for s in f)
    return [("feasible", f), ("optimal", [s for s in f if sum(s) == best])]


def _bipartite(E, keep):
    adj = {v: [] for v in keep}
    for a, b in E:
        if a in keep and b in keep: adj[a].append(b); adj[b].append(a)
    col = {}
    for s in keep:
        if s in col: continue
        col[s] = 0; st = [s]
        while st:
            u = st.pop()
            for w in adj[u]:
                if w not in col: col[w] = 1 - col[u]; st.append(w)
                elif col[w] == col[u]: return False
    return True


def oct_(rng, p):
    n = 10; E = G(n, p, rng)
    f = [s for s in product((0, 1), repeat=n) if _bipartite(E, {v for v in range(n) if not s[v]})]
    if not f: return []
    best = min(sum(s) for s in f)
    return [("feasible", f), ("optimal", [s for s in f if sum(s) == best])]


def indep_dom(rng, p):
    n = 10; E = G(n, p, rng)
    adj = {i: {i} for i in range(n)}
    for a, b in E: adj[a].add(b); adj[b].add(a)
    f = [s for s in product((0, 1), repeat=n)
         if all(any(s[u] for u in adj[v]) for v in range(n))
         and all(not (s[a] and s[b]) for a, b in E)]
    if not f: return []
    best = min(sum(s) for s in f)
    return [("feasible", f), ("optimal", [s for s in f if sum(s) == best])]


def monotone2(rng, ratio):
    n = 12; m = max(1, int(ratio * n))
    cl = [tuple(rng.sample(range(n), 2)) for _ in range(m)]
    f = [a for a in product((0, 1), repeat=n) if all(a[c[0]] or a[c[1]] for c in cl)]
    return [("solutions", f)] if f else []


def knapsack(rng, frac):
    w = [rng.randint(2, 12) for _ in range(14)]; cap = int(sum(w) * frac)
    f = [s for s in product((0, 1), repeat=14) if sum(x for x, b in zip(w, s) if b) <= cap]
    if not f: return []
    best = max(sum(x for x, b in zip(w, s) if b) for s in f)
    return [("feasible", f), ("optimal", [s for s in f if sum(x for x, b in zip(w, s) if b) == best])]


# ── carried rows, now ramp-parameterised ──────────────────────────────────────────────────────────────
LAST_CLAUSES = []          # the clauses the most recent sat() call emitted — read by the conformance
                           # sweep so it can inspect the REAL generator instead of a reimplementation


def sat(rng, ratio, k, mode, n=12):
    m = max(1, int(ratio * n))
    cls = []
    for _ in range(m):
        vs = rng.sample(range(n), k)
        if mode == "horn":
            # A HORN CLAUSE HAS AT MOST ONE POSITIVE LITERAL. This branch previously drew signs
            # uniformly at random and was byte-identical to `plain`, so the row emitted uniform random
            # k-CNF while carrying a pinned Horn template — object drift at the generator level
            # (methods 40). Every reading produced BEFORE this fix is frozen, annotated
            # `instance_object_drift`, and excluded from anything consuming the row's identity; true
            # horn-sat re-enters as NEW readings at the next survey increment.
            pos = rng.randrange(k + 1)                      # k+1 choices: no positive, or one at pos
            sg = tuple(1 if i == pos else 0 for i in range(k))
        else:
            sg = tuple(rng.randint(0, 1) for _ in range(k))
        cls.append((tuple(vs), sg))
    LAST_CLAUSES.clear(); LAST_CLAUSES.extend(cls)
    out = []
    for a in product((0, 1), repeat=n):
        ok = True
        for vs, sg in cls:
            vals = [a[v] for v in vs]
            if mode == "xor":   ok = sum(vals) % 2 == sum(sg) % 2
            elif mode == "nae": ok = len(set(vals)) > 1
            elif mode == "horn":ok = any(vals[i] == sg[i] for i in range(k))
            else:               ok = any(vals[i] == sg[i] for i in range(k))
            if not ok: break
        if ok: out.append(a)
    return [("solutions", out)] if out else []


def gsub(rng, p, kind, n=11):
    E = G(n, p, rng)
    if kind == "vc":
        f = [s for s in product((0, 1), repeat=n) if all(s[i] or s[j] for i, j in E)]
    elif kind == "is":
        f = [s for s in product((0, 1), repeat=n) if all(not (s[i] and s[j]) for i, j in E)]
    elif kind == "dom":
        adj = {i: {i} for i in range(n)}
        for a, b in E: adj[a].add(b); adj[b].add(a)
        f = [s for s in product((0, 1), repeat=n) if all(any(s[u] for u in adj[v]) for v in range(n))]
    else:
        f = list(product((0, 1), repeat=n))
    if not f: return []
    key = (lambda s: sum(s)) if kind in ("vc", "dom") else (lambda s: -sum(s))
    best = min(key(s) for s in f)
    return [("feasible", f), ("optimal", [s for s in f if key(s) == best])]


def col3(rng, p, n=8):
    E = G(n, p, rng)
    f = [s for s in product((0, 1, 2), repeat=n) if all(s[i] != s[j] for i, j in E)]
    return [("solutions", f)] if f else []


def subsum(rng, span, n=13):
    nums = [rng.randint(1, span) for _ in range(n)]
    tgt = sum(nums[i] for i in rng.sample(range(n), n // 2))
    f = [s for s in product((0, 1), repeat=n) if sum(v for v, b in zip(nums, s) if b) == tgt]
    return [("solutions", f)] if f else []


# row -> (family, domain, ramp_param_name, [ramp values], builder)
RAMP = {
    "sat-3":   ("sat-csp", 2, "clause/var ratio", [1.5, 2.5, 3.5, 4.27, 5.5], lambda r, v: sat(r, v, 3, "plain")),
    "sat-2":   ("sat-csp", 2, "clause/var ratio", [0.4, 0.7, 1.0, 1.3, 1.6], lambda r, v: sat(r, v, 2, "plain")),
    "horn-sat":("sat-csp", 2, "clause/var ratio", [0.8, 1.4, 2.0, 2.8, 3.6], lambda r, v: sat(r, v, 3, "horn")),
    "xor-sat": ("sat-csp", 2, "clause/var ratio", [0.3, 0.5, 0.7, 0.92, 1.1], lambda r, v: sat(r, v, 3, "xor")),
    "nae-sat": ("sat-csp", 2, "clause/var ratio", [0.6, 1.0, 1.5, 2.1, 2.8], lambda r, v: sat(r, v, 3, "nae")),
    "sharp-monotone-2sat": ("sat-csp", 2, "clause/var ratio", [0.5, 0.9, 1.3, 1.8, 2.4], monotone2),
    "graph-3-coloring": ("graph", 3, "edge density", [0.20, 0.30, 0.40, 0.50, 0.60], col3),
    "vertex-cover": ("graph", 2, "edge density", [0.15, 0.25, 0.35, 0.45, 0.60], lambda r, v: gsub(r, v, "vc")),
    "independent-set": ("graph", 2, "edge density", [0.15, 0.25, 0.35, 0.45, 0.60], lambda r, v: gsub(r, v, "is")),
    "dominating-set": ("graph", 2, "edge density", [0.15, 0.25, 0.35, 0.45, 0.60], lambda r, v: gsub(r, v, "dom")),
    "feedback-vertex-set": ("graph", 2, "edge density", [0.15, 0.22, 0.30, 0.40, 0.50], fvs),
    "odd-cycle-transversal": ("graph", 2, "edge density", [0.15, 0.22, 0.30, 0.40, 0.50], oct_),
    "independent-dominating-set": ("graph", 2, "edge density", [0.12, 0.20, 0.28, 0.36, 0.45], indep_dom),
    "set-cover": ("optimization", 2, "n sets", [9, 11, 13, 15, 17], lambda r, v: set_cover(r, int(v))),
    "hitting-set": ("optimization", 2, "n sets", [8, 10, 12, 14, 16], lambda r, v: hitting_set(r, int(v))),
    "knapsack": ("number-theoretic", 2, "capacity fraction", [0.15, 0.25, 0.35, 0.45, 0.55], knapsack),
    "subset-sum": ("number-theoretic", 2, "value range", [8, 14, 20, 28, 36], lambda r, v: subsum(r, int(v))),
    # the ramp parameter here is INFORMATION GIVEN TO THE SOLVER, descending — not instance size
    "sudoku": ("graph", 4, "clue count (descending)", [12, 8, 6, 4, 2, 0], sudoku),
}
NEW_ROWS = {"set-cover", "hitting-set", "feedback-vertex-set", "odd-cycle-transversal",
            "independent-dominating-set", "sharp-monotone-2sat", "knapsack", "sudoku"}


def control(r, n, dom, op, m, rng):
    N = dom ** n
    if r >= N or r < m:
        return None, None
    vals = []
    for _ in range(K_CTRL):
        S = []
        for x in rng.sample(range(N), r):
            v = []
            for _ in range(n):
                v.append(x % dom); x //= dom
            S.append(tuple(reversed(v)))
        rate, _, _, _ = violation(S, op, m, rng)
        if rate is not None:
            vals.append(rate)
    return (mean(vals), pstdev(vals)) if vals else (None, None)


def main() -> int:
    der = load_marrow()
    v3a = {e.problem_id: e for e in A.load_atlas(
        str(ROOT.parent / "eightfold" / "eightfold" / "results" / "atlas" / "atlas_v3.jsonl"))}
    def dec(p):
        # NOT EVERY SURVEY ROW IS AN ATLAS ROW. `sudoku` is a puzzle and carries no cited charge; it enters
        # the survey as a measured object, not as a labelled one. Recorded as `n.a.` with `in_atlas: false`
        # rather than silently given a label it does not have.
        if p not in v3a:
            return "n.a."
        return next((c.value for c in v3a[p].charges if c.charge == "decision"), "n.a.")
    rng = random.Random(SEED)
    readings, manifest = [], []

    for row, (fam, dom, pname, steps, build) in RAMP.items():
        ops = BOOL_OPS if dom == 2 else (D3_OPS if dom == 3 else D4_OPS)
        ff = forced_flavours(row, der)
        for pos, pval in enumerate(steps):
            step_seed = SEED + 1000 * pos + abs(hash(row)) % 997
            srng = random.Random(step_seed)
            manifest.append({"row": row, "ramp_position": pos, "ramp_param": pname,
                             "ramp_value": pval, "seed": step_seed})
            acc = {}
            for _ in range(N_INST):
                regs = build(srng, pval)
                for rname, region in regs or []:
                    if not region: continue
                    for fl, (op, m) in ops.items():
                        rate, r, nsub, cap = violation(region, op, m, srng)
                        if rate is None: continue
                        d = acc.setdefault((rname, fl), {"rates": [], "r": [], "n": [], "ns": [], "cap": []})
                        d["rates"].append(rate); d["r"].append(r); d["n"].append(len(region[0]))
                        d["ns"].append(nsub); d["cap"].append(cap)
            if not acc:
                # A STEP THAT PRODUCED NOTHING IS A GAP, AND A GAP MUST BE VISIBLE. Silently omitting it
                # leaves a trajectory that looks continuous across a hole — which is the interpolation the
                # INSUFFICIENT-r discipline exists to forbid, achieved by absence instead of by drawing.
                readings.append({
                    "row": row, "family": fam, "decision": dec(row), "in_atlas": row in v3a, "domain": dom,
                    "ramp_param": pname, "ramp_position": pos, "ramp_value": pval, "seed": step_seed,
                    "region": None, "flavor": None, "measured_rate": None, "control_mean": None,
                    "control_sd": None, "excess": None, "standardized_excess_UNSCORED": None,
                    "r": None, "ambient_n": None, "ambient_size": None,
                    "distinct_subsets_used": 0, "uniform_tuple_cap_for_reference": None,
                    "n_instances": 0, "control_draws": 0,
                    "theorem_forced": None, "forced_provenance": "n/a — no reading at this step",
                    "marrow_excluded_row": row not in der, "new_in_v3": row in NEW_ROWS,
                    "insufficient": "GAP-no-region",
                    "gap_reason": ("every instance at this ramp step yielded a region too small to blend "
                                   "(r < m) or empty. The step is recorded as a GAP and is never "
                                   "interpolated over.")})
                continue
            for (rname, fl), d in acc.items():
                r_m = int(round(mean(d["r"]))); n_m = int(round(mean(d["n"])))
                meas = mean(d["rates"])
                cmu, csd = control(r_m, n_m, dom, ops[fl][0], ops[fl][1], srng)
                if ff is None:
                    forced, prov = None, "underivable — no pinned template for this row"
                elif rname not in REGIONS_INHERITING:
                    forced, prov = False, "not applicable — optimal region is a sub-level set"
                else:
                    forced = fl in ff
                    prov = ("derived from the pinned template's closure flags (Marrow M2)" if forced
                            else "derived: template not closed under this flavour")
                if (row, rname, fl) in ASSERTED:
                    forced, prov = True, "ASSERTED with argument: " + ASSERTED[(row, rname, fl)]
                elif row in ASSERTED_NOT_FORCED:
                    forced, prov = False, "ASSERTED NOT-FORCED with argument: " + ASSERTED_NOT_FORCED[row]
                readings.append({
                    "row": row, "family": fam, "decision": dec(row), "in_atlas": row in v3a, "domain": dom,
                    "ramp_param": pname, "ramp_position": pos, "ramp_value": pval, "seed": step_seed,
                    "region": rname, "flavor": fl,
                    "measured_rate": round(meas, 4),
                    "control_mean": round(cmu, 4) if cmu is not None else None,
                    "control_sd": round(csd, 5) if csd is not None else None,
                    "excess": round(meas - cmu, 4) if cmu is not None else None,
                    "standardized_excess_UNSCORED": (round((meas - cmu) / csd, 2)
                                                     if cmu is not None and csd else None),
                    "r": r_m, "ambient_n": n_m, "ambient_size": dom ** n_m,
                    "distinct_subsets_used": int(round(mean(d["ns"]))),
                    "uniform_tuple_cap_for_reference": round(mean(d["cap"]), 4),
                    "n_instances": len(d["rates"]),
                    "control_draws": K_CTRL if cmu is not None else 0,
                    "theorem_forced": forced, "forced_provenance": prov,
                    "marrow_excluded_row": row not in der,
                    "new_in_v3": row in NEW_ROWS,
                    "insufficient": "INSUFFICIENT-r" if r_m < INSUFF_R else None})
        print(f"  {row:<28}{len(steps)} steps  "
              f"{sum(1 for x in readings if x['row']==row)} readings")

    rows_seen = {x["row"] for x in readings}
    doc = {"schema": "sounding-survey/v3",
           "STATUS": "EXPLORATORY SURVEY — NO SCORED PREDICTIONS, NO SEALED BET, DESCRIPTIVE ONLY",
           "not_citable_as": ("a result. Nothing here was predicted in advance and nothing is scored. "
                              "Interesting readings go to sounding-survey-banked-questions.md for a later "
                              "design to pose properly."),
           "tracks": {"track_1_widen": f"{len(NEW_ROWS & rows_seen)} new rows, "
                                       f"{len({x['row'] for x in readings if x['marrow_excluded_row'] and x['new_in_v3']})} "
                                       f"of them Marrow-excluded",
                      "track_2_ramp": "every row re-read across a declared difficulty ramp; each step "
                                      "draws ITS OWN matched control, never reused across steps, because "
                                      "r moves with difficulty"},
           "provenance": {"seed": SEED, "instances_per_step": N_INST, "control_draws": K_CTRL,
                          "control_subset_cap": CTRL_CAP, "measured_subset_cap": MEAS_CAP,
                          "distinct_subsets_only": True, "insufficient_r_floor": INSUFF_R,
                          "forcedness": "DERIVED from Marrow's pinned templates; ASSERTED entries carry "
                                        "their argument; `null` means underivable, which is not `false`"},
           "ramp_manifest": manifest,
           "n_readings": len(readings), "n_rows": len(rows_seen),
           "n_marrow_excluded_rows": len({x["row"] for x in readings if x["marrow_excluded_row"]}),
           "n_insufficient_readings": sum(1 for x in readings if x["insufficient"]),
           "readings": readings}
    OUT.write_text(json.dumps(doc, indent=1) + "\n")
    print(f"\n{len(readings)} readings · {len(rows_seen)} rows · "
          f"{doc['n_marrow_excluded_rows']} Marrow-excluded · "
          f"{doc['n_insufficient_readings']} INSUFFICIENT-r")
    print(f"wrote {OUT.name}  sha256 {hashlib.sha256(OUT.read_bytes()).hexdigest()[:16]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
