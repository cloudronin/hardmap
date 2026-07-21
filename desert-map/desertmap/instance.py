"""Instance family — random 3-SAT + planted short-refutation construction (M1; torch-free).

Random 3-SAT at the spec's densities/sizes, plus the E0 positive control: unsat instances with a KNOWN
short Resolution refutation of controlled length (I6 primary method — a hand-built unsat implication-chain
core mixed with variable-disjoint, satisfiable filler, so the core is the unique minimal unsat subset and
the planted refutation length is exact).

Literals/clauses follow the signed-int DIMACS convention of :mod:`desertmap.verify`.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Sequence

import numpy as np

Step = tuple  # (i1, i2, pivot) — see desertmap.verify


@dataclass(frozen=True)
class CNF:
    """A CNF formula: ``n_vars`` variables and a tuple of clauses (each a tuple of signed-int literals)."""

    n_vars: int
    clauses: tuple[tuple[int, ...], ...]
    meta: tuple = field(default=(), compare=False)  # opaque provenance tag (kind, params); excluded from identity

    @property
    def n_clauses(self) -> int:
        return len(self.clauses)

    @property
    def alpha(self) -> float:
        return self.n_clauses / self.n_vars if self.n_vars else 0.0

    def clause_sets(self) -> list[frozenset]:
        """Clauses as frozensets, for :func:`desertmap.verify.verify`."""
        return [frozenset(c) for c in self.clauses]

    def content_hash(self) -> str:
        """Stable content hash (order-independent within a clause; order-sensitive across clauses).

        Canonicalizes each clause by sorting its literals, then hashes the ``(n_vars, clauses)`` structure.
        Clause *order* is preserved (it is part of the instance identity and the planted-proof indexing).
        """
        canon = [sorted(c, key=lambda x: (abs(x), x < 0)) for c in self.clauses]
        payload = json.dumps({"n": self.n_vars, "c": canon}, separators=(",", ":"), sort_keys=True)
        return hashlib.sha256(payload.encode()).hexdigest()


def gen_3sat(n: int, alpha: float, seed: int) -> CNF:
    """Random 3-SAT: ``round(alpha*n)`` clauses, each 3 distinct variables with independent random signs.

    Deterministic given ``seed`` (numpy default_rng). Does not check satisfiability — callers that need
    unsat instances filter with :func:`is_sat` (see :mod:`desertmap.fixtures`).
    """
    if n < 3:
        raise ValueError("need n >= 3 for 3-SAT clauses")
    rng = np.random.default_rng(seed)
    m = round(alpha * n)
    clauses: list[tuple[int, ...]] = []
    for _ in range(m):
        vars3 = rng.choice(n, size=3, replace=False) + 1           # 3 distinct vars in 1..n
        signs = rng.integers(0, 2, size=3) * 2 - 1                 # ±1
        clauses.append(tuple(sorted((int(v * s) for v, s in zip(vars3, signs)),
                                    key=lambda x: (abs(x), x < 0))))
    return CNF(n_vars=n, clauses=tuple(clauses), meta=("random_3sat", n, alpha, seed))


def gen_planted(n: int, k: int, seed: int, n_filler: int | None = None) -> tuple[CNF, list[Step]]:
    """Build an unsat instance that ADMITS a Resolution refutation of length ``k`` (E0 budget witness).

    Construction (I6 primary): an implication-chain unsat core on variables ``1..k`` —
    ``(x1), (¬x1∨x2), …, (¬x_{k-1}∨x_k), (¬x_k)`` — which is unsat and refuted by a ``k``-step
    unit-propagation chain. Filler is ``n_filler`` random width-3 clauses over the DISJOINT variable block
    ``{k+1..n}``, each containing ≥1 positive literal so the all-filler-true assignment satisfies every
    filler clause.

    The certifiable property (per C1) is that the **filler is satisfiable on its own** (checkable with
    python-sat, and here guaranteed by the ≥1-positive-literal construction): since a satisfiable clause
    set has no refutation, *every* refutation of the instance must engage at least one core clause. We do
    **not** claim the planted proof is the unique or shortest refutation (certifying that is the same
    W[1]-hard problem the experiment probes). ``k`` sets the proof-budget witness: a refutation of length
    ``k`` exists, so budget ``L ≥ k`` (the spec uses ``L = 4n``) is sufficient.

    Returns ``(cnf, proof)`` where ``proof`` (a valid ``k``-step refutation) indexes ``cnf.clauses`` (core
    clauses occupy indices ``0..k``, filler follows). E0 success is defined as a random-init run decoding to
    *any* proof that verifies — not as recovering this specific one (AGENTS.md invariant 2).
    """
    if k < 1:
        raise ValueError("need k >= 1")
    if k >= n:
        raise ValueError(f"chain length k={k} must leave room for filler vars (k < n={n})")
    rng = np.random.default_rng(seed)

    # --- unsat core: clause indices 0..k (that's k+1 clauses) ---
    core: list[tuple[int, ...]] = [(1,)]                                  # idx 0: (x1)
    for v in range(1, k):
        core.append((-v, v + 1))                                         # idx v: (¬x_v ∨ x_{v+1})
    core.append((-k,))                                                    # idx k: (¬x_k)

    # --- variable-disjoint, satisfiable filler over vars {k+1..n} ---
    filler_vars = list(range(k + 1, n + 1))
    if n_filler is None:
        # default: enough filler to make finding the core a real selection problem, but keep it sat.
        n_filler = max(0, 3 * len(filler_vars))
    filler: list[tuple[int, ...]] = []
    if filler_vars and len(filler_vars) >= 3:
        for _ in range(n_filler):
            v3 = rng.choice(len(filler_vars), size=3, replace=False)
            chosen = [filler_vars[i] for i in v3]
            signs = rng.integers(0, 2, size=3) * 2 - 1
            lits = [int(v * s) for v, s in zip(chosen, signs)]
            if all(s < 0 for s in signs):       # guarantee ≥1 positive literal (all-true satisfies filler)
                lits[0] = abs(lits[0])
            filler.append(tuple(sorted(lits, key=lambda x: (abs(x), x < 0))))

    clauses = tuple(core) + tuple(filler)
    cnf = CNF(n_vars=n, clauses=clauses, meta=("planted", n, k, seed, len(filler)))

    # --- the planted k-step refutation, indexing into `clauses` ---
    proof: list[Step] = []
    m = len(clauses)
    prev = 0                       # bank row holding the current derived unit clause (x_v); starts at (x1)@0
    for v in range(1, k):          # resolve (x_v)@prev with (¬x_v∨x_{v+1})@v  -> (x_{v+1})
        proof.append((prev, v, v))
        prev = m + (v - 1)         # newly appended resolvent row
    proof.append((prev, k, k))     # resolve (x_k)@prev with (¬x_k)@k on var k -> empty clause
    return cnf, proof


def planted_filler(cnf: CNF) -> CNF:
    """Return the filler-only sub-CNF of a planted instance (clauses after the length-``k`` core).

    The certifiable C1 property is ``is_sat(planted_filler(cnf)) is True`` — filler alone is satisfiable, so
    every refutation of the full instance must engage the core. Requires a planted ``meta`` tag.
    """
    if not cnf.meta or cnf.meta[0] != "planted":
        raise ValueError("planted_filler expects a CNF produced by gen_planted")
    k = cnf.meta[2]
    return CNF(cnf.n_vars, cnf.clauses[k + 1:], meta=("planted_filler",))


def is_sat(cnf: CNF) -> bool:
    """Return True iff ``cnf`` is satisfiable (exact, via python-sat / Cadical). Lazy-imports pysat."""
    from pysat.formula import CNF as PysatCNF
    from pysat.solvers import Cadical153

    f = PysatCNF()
    for c in cnf.clauses:
        f.append(list(c))
    with Cadical153(bootstrap_with=f.clauses) as solver:
        return bool(solver.solve())


# ---------------------------------------------------------------------------------------------------
# Hard negatives (C2, spec §3.5 control category): unsat instances with NO short Resolution proof. The
# relaxation is EXPECTED to fail on these within budget L — failing is the correct reading, and that
# expectation is pre-registered (see results/prereg). Do NOT use these as planted positives.
# ---------------------------------------------------------------------------------------------------

def gen_php(holes: int) -> CNF:
    """Pigeonhole PHP^{holes+1}_{holes}: put ``holes+1`` pigeons into ``holes`` holes (unsat).

    Exponentially hard for Resolution (Haken 1985). Variable ``x[p][h]`` = pigeon ``p`` in hole ``h``,
    indexed ``p*holes + h + 1``. Clauses: each pigeon in ≥1 hole; no two pigeons share a hole. For
    ``holes=4`` → 5 pigeons, 20 variables (fits the n≤60 regime).
    """
    if holes < 1:
        raise ValueError("need holes >= 1")
    pigeons = holes + 1

    def var(p: int, h: int) -> int:
        return p * holes + h + 1

    clauses: list[tuple[int, ...]] = []
    for p in range(pigeons):                                   # each pigeon in some hole
        clauses.append(tuple(var(p, h) for h in range(holes)))
    for h in range(holes):                                     # no two pigeons in the same hole
        for p in range(pigeons):
            for q in range(p + 1, pigeons):
                clauses.append((-var(p, h), -var(q, h)))
    return CNF(n_vars=pigeons * holes, clauses=tuple(clauses), meta=("php", holes))


def _xor_clauses(edge_vars: list[int], parity: int) -> list[tuple[int, ...]]:
    """CNF for (XOR of edge_vars == parity): forbid every assignment of the wrong parity."""
    d = len(edge_vars)
    out: list[tuple[int, ...]] = []
    for mask in range(1 << d):
        bits = [(mask >> i) & 1 for i in range(d)]
        if (sum(bits) & 1) != (parity & 1):                    # this assignment violates the constraint
            # clause false only at `bits`: literal +e if bit==0 else -e
            out.append(tuple(edge_vars[i] if bits[i] == 0 else -edge_vars[i] for i in range(d)))
    return out


def gen_tseitin(n_vertices: int, seed: int, degree: int = 3) -> CNF:
    """Tseitin formula on a random ``degree``-regular graph with an odd total charge (unsat).

    One variable per edge; each vertex asserts XOR(incident edges) = charge(v), with Σ charge odd ⇒ unsat.
    Hard for Resolution on expanders (random regular graphs are good expanders w.h.p.; expander quality is
    not certified here — this is a "no short proof expected" hard negative, not a proven bound). Requires
    ``n_vertices * degree`` even. ``n_vars = n_vertices * degree / 2``.
    """
    if (n_vertices * degree) % 2 != 0:
        raise ValueError("n_vertices * degree must be even for a regular graph")
    rng = np.random.default_rng(seed)

    # Configuration model: pair up degree-stubs into edges; retry on self-loops/multi-edges.
    edges: list[tuple[int, int]] = []
    for _ in range(200):
        stubs = [v for v in range(n_vertices) for _ in range(degree)]
        rng.shuffle(stubs)
        trial, seen, ok = [], set(), True
        for i in range(0, len(stubs), 2):
            u, w = stubs[i], stubs[i + 1]
            if u == w or (min(u, w), max(u, w)) in seen:
                ok = False
                break
            seen.add((min(u, w), max(u, w)))
            trial.append((u, w))
        if ok:
            edges = trial
            break
    if not edges:
        raise RuntimeError(f"could not build a simple {degree}-regular graph on {n_vertices} vertices")

    edge_var = {e: i + 1 for i, e in enumerate(edges)}
    incident: dict[int, list[int]] = {v: [] for v in range(n_vertices)}
    for e in edges:
        incident[e[0]].append(edge_var[e])
        incident[e[1]].append(edge_var[e])

    charge = [0] * n_vertices
    charge[int(rng.integers(0, n_vertices))] = 1               # make the total charge odd ⇒ unsat

    clauses: list[tuple[int, ...]] = []
    for v in range(n_vertices):
        clauses.extend(_xor_clauses(incident[v], charge[v]))
    return CNF(n_vars=len(edges), clauses=tuple(clauses), meta=("tseitin", n_vertices, degree, seed))
