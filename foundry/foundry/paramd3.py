"""Bulatov–Marx Theorem 4.1 — CSP parameterized by solution size (OCSP), the general-domain FPT/W[1] oracle.

OCSP(Γ): find a solution assigning exactly k variables a non-zero value (0 is the "free" value), parameterized
by k. **Theorem 4.1** (Bulatov & Marx, "Constraint satisfaction parameterized by solution size," SICOMP 43(2)
2014; arXiv:1206.4854): OCSP(Γ) is **W[1]-hard** iff there exist {0}⊆D₂⊆D₁⊆dom(Γ) with
  (1) D₁ **closed** in Γ,  (2) Γ|D₁ has a **contraction** to D₂,  (3) Γ|D₂ has **no proper contraction**,
  (4) Γ|D₁ has no **weakly-separable value** that is **degenerate** or **self-producing**,  (5) Γ|D₂ is **not
  weakly separable**; **otherwise FPT.**

Definitions (transcribed from the paper via the pinned source report):
  * multivalued morphism (MVM): φ: dom→2^dom with φ(0)={0} and, for every R∈Γ and (a₁..a_r)∈R,
    φ(a₁)×…×φ(a_r) ⊆ R.
  * x **produces** y: some MVM φ has φ(x)={0,y} and φ(z)={0} for z≠x.
  * value types: y **regular** if no MVM has {0,y}⊆φ(x) for any x; **self-producing** if y produces y and every
    x that produces y is produced by y; **degenerate** if not regular/semiregular/self-producing.
  * weakly separable value d: Γ|{0,d} (2-element, d↦1) is weakly separable (the Boolean union+difference test).
  * contraction of Γ|D₁ to D₂: a unary polymorphism h of Γ|D₁ with im(h)⊆D₂ and h(d)≠0 for d≠0; **proper** if
    the target is a proper subset.
  * D closed: no unary polymorphism of Γ|D (an "inner homomorphism") maps any element of D outside D.

**R20 gate: the Boolean collapse.** The paper states that for |D|=2, OCSP(Γ) is FPT iff every relation is weakly
separable. `selftest()` verifies this implementation reproduces that on Boolean languages before any |D|=3 use.
Domain-3 verdicts have no independent ground truth and are flagged as implementation-derived in the census.
"""
from itertools import product

from foundry.postlattice import is_weakly_separable


def _arity(R):
    return len(next(iter(R)))


def _domain(rels):
    return set(v for R in rels for t in R for v in t) | {0}


def restrict(rels, D):
    """Γ|D — each relation kept only on tuples entirely within D (drop empty results)."""
    out = []
    for R in rels:
        sub = frozenset(t for t in R if all(x in D for x in t))
        if sub:
            out.append(sub)
    return out


def _unary_polys(rels, A, B):
    """All h: A→B that preserve every relation (for t∈R with coords in A, h∘t ∈ R). A,B are value sets."""
    A = sorted(A)
    res = []
    for vals in product(sorted(B), repeat=len(A)):
        h = dict(zip(A, vals))
        ok = True
        for R in rels:
            for t in R:
                if all(x in h for x in t) and tuple(h[x] for x in t) not in R:
                    ok = False
                    break
            if not ok:
                break
        if ok:
            res.append(h)
    return res


def is_closed(rels, D):
    """D is closed iff no unary polymorphism of Γ|D maps an element of D outside D (into dom∖D)."""
    dom = _domain(rels)
    gd = restrict(rels, D)
    for h in _unary_polys(gd, D, dom):
        if any(h[x] not in D for x in D):
            return False
    return True


def has_contraction(rels, D1, D2):
    """Γ|D₁ has a contraction to D₂: ∃ unary polymorphism h of Γ|D₁ with im(h)⊆D₂ and h(d)≠0 ∀d≠0."""
    gd = restrict(rels, D1)
    for h in _unary_polys(gd, D1, D2):
        if all(h[d] != 0 for d in D1 if d != 0):
            return True
    return False


def has_proper_contraction(rels, D):
    """Γ|D has a contraction to some proper subset D'⊊D (with 0∈D')."""
    D = set(D)
    others = sorted(D - {0})
    for k in range(len(others)):
        for keep in _subsets(others, k):
            Dp = {0} | set(keep)
            if Dp != D and has_contraction(rels, D, Dp):
                return True
    return False


def _subsets(xs, k):
    if k == 0:
        yield ()
        return
    for i in range(len(xs)):
        for rest in _subsets(xs[i + 1:], k - 1):
            yield (xs[i],) + rest


def _mvms(rels):
    """All multivalued morphisms φ: dom→2^dom with φ(0)={0}."""
    dom = sorted(_domain(rels))
    nonzero = [x for x in dom if x != 0]
    subsets = [frozenset(s) for r in range(1, len(dom) + 1) for s in _subsets(dom, r)]
    res = []
    for choice in product(subsets, repeat=len(nonzero)):
        phi = {0: frozenset({0})}
        phi.update(dict(zip(nonzero, choice)))
        if _is_mvm(rels, phi):
            res.append(phi)
    return res


def _is_mvm(rels, phi):
    for R in rels:
        for t in R:
            for image in product(*[sorted(phi[x]) for x in t]):
                if image not in R:
                    return False
    return True


def _produces(mvms, x, y, dom):
    target = {0: frozenset({0}), x: frozenset({0, y})}
    for z in dom:
        if z != 0 and z != x:
            target[z] = frozenset({0})
    return any(all(phi[k] == v for k, v in target.items()) for phi in mvms)


def weakly_separable_value(rels, d):
    """Is d a weakly-separable value? Γ|{0,d}, with d↦1, must be Boolean-weakly-separable."""
    gd = restrict(rels, {0, d})
    mapped = [frozenset(tuple(1 if x == d else 0 for x in t) for t in R) for R in gd]
    return is_weakly_separable(mapped) if mapped else True


def _value_type(rels, mvms, y, dom):
    reachable = any(({0, y} <= phi[x]) for phi in mvms for x in dom)
    if not reachable:
        return "regular"
    if _produces(mvms, y, y, dom):
        producers = [x for x in dom if _produces(mvms, x, y, dom)]
        if all(_produces(mvms, y, x, dom) for x in producers):
            return "self-producing"
    # producers exist but not self-producing, or reachable-but-not-produced
    produced_by_something = any(_produces(mvms, x, y, dom) for x in dom)
    return "semiregular" if not produced_by_something else "degenerate"


def ocsp_fpt(rels):
    """Theorem 4.1: FPT iff NO nested pair (D₁,D₂) meets conditions (1)–(5)."""
    Gamma = restrict(rels, _domain(rels))            # normalize
    dom = _domain(Gamma)
    mvms = _mvms(Gamma)
    nonzero = sorted(dom - {0})
    subsets_all = [{0} | set(s) for r in range(len(nonzero) + 1) for s in _subsets(nonzero, r)]
    for D1 in subsets_all:
        if not is_closed(Gamma, D1):
            continue                                  # (1)
        gD1 = restrict(Gamma, D1)
        # (4): no weakly-separable value in D1 that is degenerate or self-producing
        bad4 = any(weakly_separable_value(Gamma, d) and _value_type(Gamma, mvms, d, dom) in ("degenerate", "self-producing")
                   for d in D1 if d != 0)
        if bad4:
            continue
        for D2 in subsets_all:
            if not D2 <= D1:
                continue
            if not has_contraction(Gamma, D1, D2):
                continue                              # (2)
            if has_proper_contraction(Gamma, D2):
                continue                              # (3)
            gD2 = restrict(Gamma, D2)
            d2_ws = all(weakly_separable_value(Gamma, d) for d in D2 if d != 0) and _is_language_ws(gD2, D2)
            if d2_ws:
                continue                              # (5): Γ|D₂ not weakly separable
            return False                              # a witnessing pair → W[1]-hard
    return True                                       # no witness → FPT


def _is_language_ws(rels_D2, D2):
    """Γ|D₂ weakly separable: on the ≤2 nonzero values, every value weakly separable AND (for |D₂|>2) jointly.
    At |D₂|<=2 this is exactly the Boolean WS of Γ|D₂ (nonzero ↦ 1)."""
    nz = sorted(D2 - {0})
    if len(nz) <= 1:
        d = nz[0] if nz else None
        if d is None:
            return True
        mapped = [frozenset(tuple(1 if x == d else 0 for x in t) for t in R) for R in rels_D2]
        return is_weakly_separable(mapped) if mapped else True
    # |D₂| = 3 (0 + two nonzero): require weak separability on each Γ|{0,d}
    return all(weakly_separable_value(rels_D2, d) for d in nz)


def parameterized_d3(rels):
    """Domain-3 parameterized charge via Theorem 4.1: FPT or W[1] (=W[1]-complete)."""
    return "FPT" if ocsp_fpt(rels) else "W[1]"


# ── R20 gate: the Boolean collapse (FPT iff every relation weakly separable) ─────────────────────────────────
def selftest(verbose=True):
    from foundry import postlattice as PL
    cases = [
        ("R_XOR3 (homogeneous affine, WS)", (PL.R_XOR3,), True),
        ("R_NOR3 (0-valid Horn, fails union → not WS)", (PL.R_NOR3, PL.R_FALSE), False),
        ("R_NEG2 (¬x∨¬y, fails union → not WS)", (PL.R_NEG2,), False),
        ("implication x→y (fails difference → not WS)", (frozenset({(0, 0), (0, 1), (1, 1)}),), False),
        ("R_XOR3 + R_NEG2 (one non-WS → not WS)", (PL.R_XOR3, PL.R_NEG2), False),
    ]
    ok = True
    for name, rels, expect_all_ws in cases:
        all_ws = all(is_weakly_separable([R]) for R in rels)          # Boolean ground truth
        fpt = ocsp_fpt(rels)
        agree = (fpt == all_ws)
        ok = ok and agree
        if verbose:
            print(f"  {name}: all-WS={all_ws} → Thm4.1 FPT={fpt}  {'OK' if agree else 'MISMATCH'}")
    if verbose:
        print(f"Bulatov-Marx Thm 4.1 Boolean-collapse selftest: {'PASSED' if ok else 'FAILED'}")
    return 0 if ok else 1
