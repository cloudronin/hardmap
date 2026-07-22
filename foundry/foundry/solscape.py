"""Solution-space instrument (Sprint 4.1, net-new) — the `landscape` charge for the decision-P census rows.

The Proof-Census apparatus samples the PROOF space (refutations of UNSAT instances); the `landscape` charge is
SOLUTION-space geometry (the shape of the SATISFYING-assignment set). This module is the net-new solution-side
instrument, built to prereg_v5 (riders R-a..R-e):

  * TWO structurally-different samplers (R-c): `sample_dpll` (systematic randomized backtracking) and
    `sample_walksat` (stochastic local search). One sampler is an anecdote-generator; a landscape reading is
    trusted only where the two agree at trend level.
  * `sample_affine_exact`: uniform sampling over the linear solution coset (Gaussian elimination over GF(p)) —
    UNBIASED ground truth, available only on the affine arm. Lets us measure the two biased samplers' bias
    directly (the only place in the program where sampler bias is measurable — a logged deliverable).
  * Metrics transpose the Census concepts from clause-ids to assignments: overlap q = 2*agree-1, backbone =
    FROZEN variables, clustering = solution-graph connectivity + P(q) shape. ruggedness is a sampled-population
    statistic (R-d), never a uniform-solution-space claim.
  * `vega_calibration` (R-b): the instrument must read the known-RUGGED pole (k-XOR) rugged AND the known-SMOOTH
    pole (a well-connected 2-SAT/const language) smooth, both samplers concordant — else it is not calibrated.
"""
import random
from statistics import mean, pstdev

from foundry import ensemble as E


# ── samplers ─────────────────────────────────────────────────────────────────────────────────────────────────
def sample_dpll(inst, seed, K=60, max_tries=None, node_budget=20000):
    """Systematic sampler: randomized backtracking (random var order + random value order per run) yields one
    solution per successful run; collect up to K DISTINCT solutions. Biased toward the search order (R-d). Each
    run is capped at `node_budget` search nodes so an UNSAT (or hard) cell fails fast instead of hanging."""
    max_tries = max_tries if max_tries is not None else 12 * K + 40
    rng = E.rng_for("dpll", seed, inst.meta)
    sols, seen = [], set()
    dead = 0
    for t in range(max_tries):
        a = _dpll_one(inst, E.rng_for("dpllrun", seed, t), node_budget)
        if a is None:
            dead += 1
            if dead >= 8 and not sols:          # 8 straight capped/failed runs, nothing found -> give up (UNSAT/hard)
                break
            continue
        dead = 0
        if a not in seen:
            seen.add(a)
            sols.append(a)
            if len(sols) >= K:
                break
    return sols


def _dpll_one(inst, rng, node_budget=20000):
    """One random satisfying assignment via backtracking (or None if none found within node_budget). Assign vars
    in a random order, trying domain values in a random order; backtrack when a fully-scoped constraint fails."""
    n, dom = inst.n_vars, inst.domain
    order = list(range(n))
    rng.shuffle(order)
    a = [None] * n
    by_completion = {}
    pos = {v: i for i, v in enumerate(order)}
    for R, scope in inst.constraints:
        last = max(scope, key=lambda v: pos[v])
        by_completion.setdefault(last, []).append((R, scope))
    budget = [node_budget]

    def ok_after(v):
        for R, scope in by_completion.get(v, ()):
            if tuple(a[u] for u in scope) not in R:
                return False
        return True

    def bt(i):
        if i == n:
            return True
        if budget[0] <= 0:
            return False
        budget[0] -= 1
        v = order[i]
        vals = list(dom)
        rng.shuffle(vals)
        for val in vals:
            a[v] = val
            if ok_after(v) and bt(i + 1):
                return True
        a[v] = None
        return False

    return tuple(a) if bt(0) else None


def sample_walksat(inst, seed, K=60, max_flips=None, max_tries=None, p_noise=0.3):
    """Stochastic-local-search sampler (WalkSAT-style): from a random assignment, repeatedly pick a violated
    constraint and flip one of its variables (noise: random var+value; else greedy = fewest locally-broken
    constraints). Collect up to K DISTINCT solutions. Structurally different from DPLL (R-c). Biased toward
    LS-reachable solutions (R-d). Incremental: a flip of v only re-checks the constraints containing v."""
    n, dom, cons = inst.n_vars, inst.domain, inst.constraints
    m = len(cons)
    max_flips = max_flips if max_flips is not None else 30 * n + 200
    max_tries = max_tries if max_tries is not None else 12 * K + 60
    var_cons = [[] for _ in range(n)]
    for ci, (_R, scope) in enumerate(cons):
        for v in scope:
            var_cons[v].append(ci)
    rng = E.rng_for("walksat", seed, inst.meta)

    def csat(ci, a):
        R, scope = cons[ci]
        return tuple(a[u] for u in scope) in R

    def local_broken(v, a):                     # # constraints on v currently unsatisfied
        return sum(0 if csat(ci, a) else 1 for ci in var_cons[v])

    sols, seen = [], set()
    for t in range(max_tries):
        a = [rng.choice(dom) for _ in range(n)]
        unsat = {ci for ci in range(m) if not csat(ci, a)}
        for _ in range(max_flips):
            if not unsat:
                break
            ci = next(iter(unsat)) if len(unsat) == 1 else list(unsat)[rng.randrange(len(unsat))]
            scope = cons[ci][1]
            if rng.random() < p_noise:
                v = scope[rng.randrange(len(scope))]
                val = rng.choice([d for d in dom if d != a[v]] or list(dom))
            else:
                best = None
                for cand in scope:
                    old = a[cand]
                    for d in dom:
                        if d == old:
                            continue
                        a[cand] = d
                        b = local_broken(cand, a)
                        a[cand] = old
                        if best is None or b < best[0]:
                            best = (b, cand, d)
                _, v, val = best
            a[v] = val
            for ci2 in var_cons[v]:             # incremental unsat-set update
                if csat(ci2, a):
                    unsat.discard(ci2)
                else:
                    unsat.add(ci2)
        else:
            continue
        sol = tuple(a)
        if sol not in seen and inst.satisfies(sol):
            seen.add(sol)
            sols.append(sol)
            if len(sols) >= K:
                break
    return sols


# ── affine-exact sampler (GF(p) linear algebra) ─────────────────────────────────────────────────────────────
def _affine_equations(R, p):
    """The defining linear equations a·x = b of an affine relation R over GF(p) (R must be an affine subspace).
    Returns list of (coeff_tuple, rhs). Empty if R spans the whole space (no constraint)."""
    pts = [list(t) for t in R]
    r = len(pts[0])
    t0 = pts[0]
    # direction vectors (t - t0) span the solution's direction space V
    dirs = [[(pts[i][j] - t0[j]) % p for j in range(r)] for i in range(1, len(pts))]
    # the constraint rows are a basis of the LEFT null space of the direction matrix:
    # a with a·d = 0 for every direction d  ->  a·x = a·t0 for all x in R
    basis = _left_null_space(dirs, r, p)
    return [(tuple(a), sum(a[j] * t0[j] for j in range(r)) % p) for a in basis]


def _left_null_space(dirs, r, p):
    """Basis of {a in GF(p)^r : a·d = 0 for all d in dirs}. dirs is a list of length-r vectors."""
    # a·d = 0 for all d  <=>  M a = 0 where M has rows = dirs. Solve the homogeneous system for a.
    M = [row[:] for row in dirs]
    return _null_space(M, r, p)


def _null_space(M, ncols, p):
    """Basis of the null space {x : M x = 0} over GF(p), M a list of rows (each length ncols)."""
    A = [row[:] for row in M]
    pivots, row = {}, 0
    for col in range(ncols):
        piv = next((rr for rr in range(row, len(A)) if A[rr][col] % p != 0), None)
        if piv is None:
            continue
        A[row], A[piv] = A[piv], A[row]
        inv = pow(A[row][col], -1, p)
        A[row] = [(x * inv) % p for x in A[row]]
        for rr in range(len(A)):
            if rr != row and A[rr][col] % p != 0:
                f = A[rr][col]
                A[rr] = [(A[rr][j] - f * A[row][j]) % p for j in range(ncols)]
        pivots[col] = row
        row += 1
    free = [c for c in range(ncols) if c not in pivots]
    basis = []
    for fc in free:
        x = [0] * ncols
        x[fc] = 1
        for col, prow in pivots.items():
            x[col] = (-A[prow][fc]) % p
        basis.append(x)
    return basis


def _solve_affine_system(rows, rhs, n, p):
    """Particular solution + null-space basis of the affine system (rows·x = rhs) over GF(p). None if inconsistent."""
    A = [rows[i][:] + [rhs[i] % p] for i in range(len(rows))]
    pivots, row = {}, 0
    for col in range(n):
        piv = next((rr for rr in range(row, len(A)) if A[rr][col] % p != 0), None)
        if piv is None:
            continue
        A[row], A[piv] = A[piv], A[row]
        inv = pow(A[row][col], -1, p)
        A[row] = [(x * inv) % p for x in A[row]]
        for rr in range(len(A)):
            if rr != row and A[rr][col] % p != 0:
                f = A[rr][col]
                A[rr] = [(A[rr][j] - f * A[row][j]) % p for j in range(n + 1)]
        pivots[col] = row
        row += 1
    for rr in range(len(A)):                       # 0 = nonzero  ->  inconsistent
        if all(A[rr][c] % p == 0 for c in range(n)) and A[rr][n] % p != 0:
            return None
    part = [0] * n
    for col, prow in pivots.items():
        part[col] = A[prow][n] % p
    homog = _null_space([r[:n] for r in rows], n, p)
    return part, homog


def sample_affine_exact(inst, seed, K=60):
    """Uniform sample of the solution coset of an affine instance (each constraint's relation is an affine
    subspace over GF(p), p=|domain|). UNBIASED. Returns [] if inconsistent (no solutions)."""
    p = len(inst.domain)
    rows, rhs = [], []
    for R, scope in inst.constraints:
        for coeff, b in _affine_equations(R, p):
            row = [0] * inst.n_vars
            for j, v in enumerate(scope):
                row[v] = (row[v] + coeff[j]) % p
            rows.append(row)
            rhs.append(b)
    if not rows:
        rows, rhs = [[0] * inst.n_vars], [0]        # unconstrained
    solved = _solve_affine_system(rows, rhs, inst.n_vars, p)
    if solved is None:
        return []
    part, homog = solved
    rng = E.rng_for("affine", seed, inst.meta)
    sols, seen = [], set()
    cap = min(K, p ** len(homog)) if homog else 1
    tries = 0
    while len(sols) < cap and tries < 40 * cap + 40:
        tries += 1
        x = part[:]
        for basis in homog:
            c = rng.randrange(p)
            if c:
                x = [(x[j] + c * basis[j]) % p for j in range(inst.n_vars)]
        sol = tuple(x)
        if sol not in seen:
            seen.add(sol)
            sols.append(sol)
    return sols


# ── solution-space metrics (Census concepts, transposed to assignments) ──────────────────────────────────────
def overlap_q(a, b):
    """Spin-overlap of two assignments: q = 2*agreement_fraction - 1 in [-1, 1]."""
    agree = sum(1 for x, y in zip(a, b) if x == y) / len(a)
    return 2 * agree - 1


def pairwise_overlaps(sols):
    return [overlap_q(sols[i], sols[j]) for i in range(len(sols)) for j in range(i + 1, len(sols))]


def frozen_fraction(sols):
    """Backbone/freezing transpose: fraction of variables that take the SAME value across ALL sampled solutions."""
    if not sols:
        return None
    n = len(sols[0])
    return sum(1 for v in range(n) if len({s[v] for s in sols}) == 1) / n


def _hamming(a, b):
    return sum(1 for x, y in zip(a, b) if x != y)


DEFAULT_LINK_FRAC = 0.1        # link solutions within normalized-Hamming <= this fraction (calibrated by Vega)


def cluster_stats(sols, link_frac=DEFAULT_LINK_FRAC):
    """Solution-graph connectivity (clustering transpose): link two solutions whose NORMALIZED Hamming distance is
    <= link_frac (a small, LOCAL neighborhood — n-robust, calibrated by the two-pole Vega). A single well-
    connected blob -> largest_component_fraction ~ 1 (smooth); solutions spread with no local neighbors fragment
    -> it collapses toward 1/m (rugged). The diagnostic confirmed this separates XOR (fragmented) from 2-SAT
    (connected)."""
    m = len(sols)
    if m < 3:
        return {"n_components": m, "largest_component_fraction": 1.0 if m else None}
    n = len(sols[0])
    thresh = max(1, int(link_frac * n))
    parent = list(range(m))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for i in range(m):
        for j in range(i + 1, m):
            if _hamming(sols[i], sols[j]) <= thresh:
                parent[find(i)] = find(j)
    comps = {}
    for i in range(m):
        comps[find(i)] = comps.get(find(i), 0) + 1
    sizes = sorted(comps.values(), reverse=True)
    return {"n_components": len(sizes), "largest_component_fraction": sizes[0] / m, "link_thresh": thresh}


def ruggedness(sols, domain_size=2, link_frac=DEFAULT_LINK_FRAC):
    """Sampled-population ruggedness (R-d), a scalar in [0,1]. The density sweep established that the robust,
    domain-comparable signal is EXCESS mean overlap above the random-agreement baseline (fragmentation turned out
    to be a solution-COUNT artifact — it tracks sample density, not geometry, so it is reported but NOT scored).

      q_random = 2/|D| - 1 (Boolean 0; |D|=3 -> -1/3). clustering = max(0, (mean_q - q_random)/(1 - q_random))
      is the excess consensus among solutions (0 = solutions spread like random draws -> RUGGED; 1 = identical ->
      maximally SMOOTH). ruggedness score = 1 - clustering (higher = more rugged).

    Rationale: a shattered/rugged solution space (affine) samples pairs from far-apart regions -> mean overlap ~
    q_random -> clustering ~ 0 -> rugged. A connected/smooth blob -> mean overlap > q_random -> clustering > 0 ->
    smooth. Sampled-population, never a uniform-solution-space claim."""
    if sols is None or len(sols) < 3:
        return {"n_solutions": len(sols) if sols is not None else 0, "score": None, "insufficient": True}
    qs = pairwise_overlaps(sols)
    q_rand = 2.0 / domain_size - 1.0
    clustering = max(0.0, (mean(qs) - q_rand) / (1 - q_rand)) if qs else None
    score = round(1 - clustering, 3) if clustering is not None else None
    cs = cluster_stats(sols, link_frac)
    return {"n_solutions": len(sols), "score": score,
            "clustering": round(clustering, 3) if clustering is not None else None,
            "mean_overlap": round(mean(qs), 3) if qs else None, "q_random": round(q_rand, 3),
            "frozen_fraction": round(frozen_fraction(sols), 3),
            "fragmentation_diagnostic": round(1 - cs["largest_component_fraction"], 3),
            "overlap_sd": round(pstdev(qs), 3) if len(qs) > 1 else 0.0, "insufficient": False}


SAMPLERS = {"dpll": sample_dpll, "walksat": sample_walksat, "affine_exact": sample_affine_exact}


# ── aggregate landscape reading + concordance (R-c) + Vega calibration (R-b) + affine bias (R-c bonus) ────────
def landscape_reading(rels, domain, n, alpha, base_seed=200, K=40, n_instances=4, samplers=("dpll", "walksat")):
    """The measured landscape ruggedness of a family at one (n, alpha) cell: aggregate the per-sampler ruggedness
    score over `n_instances` random instances, for each of the (two, R-c) structurally-different samplers.
    Returns per-sampler scores, the pooled score, and the CONCORDANCE (max pairwise |score| gap) — a reading is
    trusted only where the samplers concord. Sampled-population provenance (R-d)."""
    from foundry import ensemble as E
    ds = len(domain)
    per = {s: [] for s in samplers}
    for i in range(n_instances):
        inst = E.gen_instance(rels, domain, n, alpha, base_seed + i, "reading")
        for s in samplers:
            sols = SAMPLERS[s](inst, i, K=K)
            r = ruggedness(sols, ds)
            if not r["insufficient"]:
                per[s].append(r["score"])
    means = {s: (round(mean(v), 3) if v else None) for s, v in per.items()}
    vals = [m for m in means.values() if m is not None]
    concord = round(max(vals) - min(vals), 3) if len(vals) > 1 else 0.0
    pooled = round(mean(vals), 3) if vals else None
    return {"family_alpha": (n, alpha), "per_sampler": means, "pooled_score": pooled,
            "concordance_gap": concord, "n_instances_ok": {s: len(v) for s, v in per.items()},
            "provenance": "sampled-population"}


def affine_bias(rels, domain, n, alpha, base_seed=200, K=40, n_instances=4):
    """R-c bonus (affine arm only): the exact uniform sampler is ground truth, so we can measure the two biased
    samplers' bias directly. Returns each biased sampler's mean |ruggedness - exact_ruggedness|."""
    from foundry import ensemble as E
    ds = len(domain)
    gaps = {"dpll": [], "walksat": []}
    for i in range(n_instances):
        inst = E.gen_instance(rels, domain, n, alpha, base_seed + i, "bias")
        ex = ruggedness(sample_affine_exact(inst, i, K=K), ds)
        if ex["insufficient"]:
            continue
        for s in ("dpll", "walksat"):
            r = ruggedness(SAMPLERS[s](inst, i, K=K), ds)
            if not r["insufficient"]:
                gaps[s].append(abs(r["score"] - ex["score"]))
    return {s: round(mean(v), 3) if v else None for s, v in gaps.items()}


def vega_calibration(rugged_pole, smooth_pole, sep_margin=0.12, concord_max=0.1):
    """R-b two-pole calibration. `rugged_pole`/`smooth_pole` = dicts {rels, domain, n, alpha}. PASS iff the rugged
    pole reads MORE rugged than the smooth pole by >= sep_margin AND both readings are sampler-concordant. An
    instrument that only ever reads rugged is CONFIRMED, not calibrated — so BOTH poles must land on their side."""
    rr = landscape_reading(**rugged_pole)
    sr = landscape_reading(**smooth_pole)
    sep = (rr["pooled_score"] - sr["pooled_score"]) if (rr["pooled_score"] and sr["pooled_score"]) else None
    ok = (sep is not None and sep >= sep_margin and rr["concordance_gap"] <= concord_max
          and sr["concordance_gap"] <= concord_max)
    return {"rugged_pole_score": rr["pooled_score"], "smooth_pole_score": sr["pooled_score"],
            "separation": round(sep, 3) if sep is not None else None, "sep_margin": sep_margin,
            "rugged_concord": rr["concordance_gap"], "smooth_concord": sr["concordance_gap"],
            "passes": bool(ok)}
