"""Per-Gamma random-CSP ensemble generator (Sprint 4.1) — native, domain-general.

A census row is a constraint language Gamma (a set of relations over a domain D). The solution-side instrument
needs random Gamma-instances whose SATISFYING-ASSIGNMENT geometry can be sampled. We represent an instance
NATIVELY (a list of (relation, variable-scope) constraints over D) rather than as CNF: this is uniform across
Boolean (|D|=2) and general-domain (|D|=3) languages, needs no direct/log CNF encoding, and lets the samplers +
metrics work directly on domain-valued assignments (the object the `landscape` charge is about).

density-dialed: n_constraints = round(alpha * n_vars). The per-family alpha-grid (I5 memo) is fixed at the
calibration gate; this module only generates.
"""
import random
from dataclasses import dataclass


@dataclass(frozen=True)
class CSPInstance:
    domain: tuple                 # e.g. (0, 1) or (0, 1, 2)
    n_vars: int
    constraints: tuple            # tuple of (relation: frozenset[tuple], scope: tuple[int])
    meta: tuple = ()              # provenance: (family_id, n_vars, alpha, seed)

    def satisfies(self, a) -> bool:
        return all(tuple(a[v] for v in scope) in R for R, scope in self.constraints)

    def num_violated(self, a) -> int:
        return sum(0 if tuple(a[v] for v in scope) in R else 1 for R, scope in self.constraints)

    def violated_constraints(self, a):
        return [(R, scope) for R, scope in self.constraints if tuple(a[v] for v in scope) not in R]

    @property
    def alpha(self) -> float:
        return len(self.constraints) / self.n_vars if self.n_vars else 0.0


def _arity(R):
    return len(next(iter(R)))


def rng_for(*parts) -> random.Random:
    """A deterministic RNG seeded from a STRING (supported seed type; tuple-hashing is deprecated in 3.9+)."""
    return random.Random("|".join(map(str, parts)))


def gen_instance(relations, domain, n_vars, alpha, seed, family_id="") -> CSPInstance:
    """Random Gamma-CSP: n_constraints = round(alpha*n_vars); each constraint = a random relation from `relations`
    applied to arity-many DISTINCT random variables. Deterministic in `seed`."""
    rng = rng_for("gen", seed, n_vars, round(alpha * 1000), family_id)
    rels = list(relations)
    m = round(alpha * n_vars)
    cons = []
    for _ in range(m):
        R = rels[rng.randrange(len(rels))]
        r = _arity(R)
        if r > n_vars:
            continue                              # can't place an arity-r constraint on < r vars
        scope = tuple(rng.sample(range(n_vars), r))
        cons.append((R, scope))
    return CSPInstance(tuple(domain), n_vars, tuple(cons), meta=(family_id, n_vars, alpha, seed))


def gen_ensemble(relations, domain, n_vars, alpha, n_instances, base_seed, family_id=""):
    """An ensemble of `n_instances` independent random Gamma-instances at one (n_vars, alpha) cell."""
    return [gen_instance(relations, domain, n_vars, alpha, base_seed + 7919 * i, family_id)
            for i in range(n_instances)]
