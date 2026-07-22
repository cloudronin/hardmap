"""GKMP connectivity relation-level classes (prereg_v9) — R20-verified from Gopalan-Kolaitis-Maneva-Papadimitriou,
SICOMP 38(6) 2009 (arXiv cs/0609072), Definitions 5-6.

These classify an individual Boolean relation R (a set of same-arity 0/1 tuples) by properties that govern its
solution-space CONNECTIVITY / diameter — a FINER, geometry-facing classification than Schaefer tractability
(every Schaefer relation is tight, so the discriminating features are the tight-WITNESS + the component structure
of G(R)). Boolean only; |D|=3 relations are out of jurisdiction.
"""
from itertools import combinations, product


def _arity(R):
    return len(next(iter(R)))


OR = frozenset({(0, 1), (1, 0), (1, 1)})
NAND = frozenset({(0, 0), (0, 1), (1, 0)})


def _induced_pair(R, i, j, rest, vals):
    """The 2-ary relation on coords (i,j) after fixing coords `rest` to `vals`."""
    fixed = dict(zip(rest, vals))
    return frozenset((t[i], t[j]) for t in R if all(t[c] == v for c, v in fixed.items()))


def _obtainable(R, target):
    """Can `target` (a 2-ary relation) be obtained from R by fixing k-2 coordinates to constants?"""
    k = _arity(R)
    for i, j in combinations(range(k), 2):
        rest = [c for c in range(k) if c not in (i, j)]
        for vals in product((0, 1), repeat=len(rest)):
            if _induced_pair(R, i, j, rest, vals) == target:
                return True
    return False


def or_free(R):
    """GKMP Def 5(2): R is OR-free iff OR={(0,1),(1,0),(1,1)} cannot be obtained by fixing k-2 coordinates."""
    return not _obtainable(R, OR)


def nand_free(R):
    """GKMP Def 5(3): R is NAND-free iff NAND={(0,0),(0,1),(1,0)} cannot be so obtained."""
    return not _obtainable(R, NAND)


def _hamming(a, b):
    return sum(1 for x, y in zip(a, b) if x != y)


def components(R):
    """Connected components of G(R): tuples of R, edges at Hamming distance 1 (union-find)."""
    ts = list(R)
    parent = list(range(len(ts)))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a in range(len(ts)):
        for b in range(a + 1, len(ts)):
            if _hamming(ts[a], ts[b]) == 1:
                parent[find(a)] = find(b)
    comps = {}
    for a in range(len(ts)):
        comps.setdefault(find(a), set()).add(ts[a])
    return list(comps.values())


def _maj3(a, b, c):
    return tuple(1 if (x + y + z) >= 2 else 0 for x, y, z in zip(a, b, c))


def componentwise_bijunctive(R):
    """GKMP Def 5(1): every connected component of G(R) is bijunctive (closed under majority within itself)."""
    for comp in components(R):
        cs = list(comp)
        for a in cs:
            for b in cs:
                for c in cs:
                    if _maj3(a, b, c) not in comp:
                        return False
    return True


def classify_relation(R):
    """The GKMP connectivity classification of a single Boolean relation R."""
    orf, nandf, cbij = or_free(R), nand_free(R), componentwise_bijunctive(R)
    comps = components(R)
    tight = orf or nandf or cbij
    # the tight-witness label (the discriminating feature within Schaefer): which of the three holds
    witnesses = [w for w, ok in (("componentwise-bijunctive", cbij), ("OR-free", orf), ("NAND-free", nandf)) if ok]
    return {"or_free": orf, "nand_free": nandf, "componentwise_bijunctive": cbij, "tight": tight,
            "n_components": len(comps), "n_tuples": len(R),
            "tight_witness": "+".join(witnesses) if witnesses else "NONE (not tight)"}
