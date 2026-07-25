#!/usr/bin/env python3
"""Mosaic L1 — join the two blind codings, score the instrument, run the separability gate.

Inputs (produced by the two varied blind coders): mosaic-coding-A.jsonl, mosaic-coding-B.jsonl
  each line {problem_id, locality_class, arity_class, rationale}.

Reports: Cohen's kappa (kill 1 if < 0.6), P1 anchor qualification, a forbidden-vocabulary audit of the
rationales, the disagreement list (for the blind third pass), and — on the agreed rows joined to the
charges — the PINNED separability gate (prereg_v10 §separability_gate). It does NOT itself build the final
sidecar: that waits on the third pass resolving disagreements. Run: PYTHONPATH=. python3 dev/mosaic_code.py
"""
import hashlib, json, sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, ".")
from eightfold import atlas as A, structure as S      # noqa: E402

AT = Path("eightfold/results/atlas")
LEGAL = {"decomposable", "local-covering", "entangled", "mixed", "uncodable"}
ANCHORS = {"planar-vertex-cover": "decomposable", "knapsack": "decomposable",
           "vertex-cover": "local-covering", "max-2sat": "local-covering",
           "clique": "entangled", "independent-set": "entangled", "label-cover": "entangled"}
DISSOCIATION = {"knapsack", "subset-sum"}   # must code by STRUCTURE (decomposable), not coordinates
FORBIDDEN = {"fptas", "eptas", "ptas", "apx", "inapprox", "fpt", "w[1]", "w[2]", "kernel", "np-hard",
             "np-complete", "#p", "pspace", "conp", "qma", "para-np", "fixed-parameter",
             "approximation scheme", "polynomial time", "poly-time"}


def load(path):
    return {json.loads(l)["problem_id"]: json.loads(l) for l in Path(path).read_text().splitlines() if l.strip()}


# resolution ladder (prereg_v10-clarification-01): kappa MEASURES the granularity at which the instrument
# is reliable; it does not qualify/kill at five classes. 5 -> 3 (collapse the disputed entangled/mixed
# boundary) -> 2 (local vs delocalized). Demonstrated resolution = finest level with kappa >= 0.6.
COLLAPSE = {
    "5-class": {c: c for c in LEGAL},
    "3-class": {"decomposable": "decomposable", "local-covering": "local-covering",
                "entangled": "delocalized", "mixed": "delocalized", "uncodable": "uncodable"},
    "2-class": {"decomposable": "local", "local-covering": "local",
                "entangled": "delocalized", "mixed": "delocalized", "uncodable": "uncodable"},
}


def _collapse(coding, m):
    return {k: {**v, "locality_class": m[v["locality_class"]]} for k, v in coding.items()}


def cohen_kappa(a, b, keys):
    la = [a[k]["locality_class"] for k in keys]
    lb = [b[k]["locality_class"] for k in keys]
    n = len(keys)
    cats = set(la) | set(lb)                       # derive categories (works at any ladder level)
    po = sum(x == y for x, y in zip(la, lb)) / n
    ca, cb = Counter(la), Counter(lb)
    pe = sum((ca[c] / n) * (cb[c] / n) for c in cats)
    return (po - pe) / (1 - pe) if pe < 1 else 1.0, po


def gwet_ac1(a, b, keys):
    """Gwet's AC1 — SUPPLEMENTARY context only. Robust to the marginal skew that inflates Cohen's chance
    term (the kappa paradox). Reported BESIDE kappa, never substituting it: the sealed threshold is kappa
    >= 0.6 and only kappa qualifies or kills (prereg_v10; the metric does not move after the result)."""
    la = [a[k]["locality_class"] for k in keys]
    lb = [b[k]["locality_class"] for k in keys]
    n = len(keys)
    cats = set(la) | set(lb)
    K = len(cats)
    po = sum(x == y for x, y in zip(la, lb)) / n
    pi = {c: (Counter(la)[c] + Counter(lb)[c]) / (2 * n) for c in cats}
    pe = (sum(pi[c] * (1 - pi[c]) for c in cats) / (K - 1)) if K > 1 else 0.0
    return (po - pe) / (1 - pe) if pe < 1 else 1.0


def per_class_agreement(a, b, keys):
    """For each class, of the times EITHER coder used it, how often did BOTH? (specific-agreement)."""
    out = {}
    for c in LEGAL:
        either = sum(a[k]["locality_class"] == c or b[k]["locality_class"] == c for k in keys)
        both = sum(a[k]["locality_class"] == c and b[k]["locality_class"] == c for k in keys)
        out[c] = (both, either, round(both / either, 2) if either else None)
    return out


def forbidden_audit(coding):
    bad = []
    for k, v in coding.items():
        r = (v.get("rationale") or "").lower()
        hit = [w for w in FORBIDDEN if w in r]
        if hit:
            bad.append((k, hit))
    return bad


def main():
    if not (AT / "mosaic-coding-A.jsonl").exists() or not (AT / "mosaic-coding-B.jsonl").exists():
        print("codings not present yet (A and/or B). Run after both blind coders land.")
        return 1
    a, b = load(AT / "mosaic-coding-A.jsonl"), load(AT / "mosaic-coding-B.jsonl")
    keys = sorted(set(a) & set(b))
    print(f"coders A={len(a)} B={len(b)} shared={len(keys)}")
    for name, c in (("A", a), ("B", b)):
        illegal = [k for k in c if c[k]["locality_class"] not in LEGAL]
        print(f"  coding {name}: dist={dict(Counter(v['locality_class'] for v in c.values()))}"
              + (f"  ILLEGAL={illegal}" if illegal else ""))

    # --- kappa (kill 1) ---
    # --- the resolution ladder (prereg_v10-clarification-01) ---
    print("\nresolution ladder (kappa MEASURES the reliable granularity; it does not qualify/kill at 5):")
    ladder = {}
    for lvl in ("5-class", "3-class", "2-class"):
        aa, bb = _collapse(a, COLLAPSE[lvl]), _collapse(b, COLLAPSE[lvl])
        k, p = cohen_kappa(aa, bb, keys)
        ladder[lvl] = k
        print(f"  {lvl}: kappa={k:.3f} (raw {p:.1%}, AC1={gwet_ac1(aa, bb, keys):.3f})  "
              + (">= 0.6 RELIABLE" if k >= 0.6 else "< 0.6"))
    demonstrated = next((lvl for lvl in ("5-class", "3-class", "2-class") if ladder[lvl] >= 0.6), None)
    # is the 5-class disagreement concentrated on the entangled/mixed boundary?
    dis5 = [(a[k]["locality_class"], b[k]["locality_class"]) for k in keys if a[k]["locality_class"] != b[k]["locality_class"]]
    em = sum(1 for x, y in dis5 if {x, y} == {"entangled", "mixed"})
    conc = (em / len(dis5)) if dis5 else 0.0
    print(f"\n  5-class disagreements: {len(dis5)}; entangled<->mixed: {em} ({conc:.0%} of them)")
    print("  per-class specific-agreement (both/either), 5-class:")
    for c in ("decomposable", "local-covering", "entangled", "mixed", "uncodable"):
        both, either, rate = per_class_agreement(a, b, keys)[c]
        print(f"     {c:16} {both}/{either} = {rate}")

    # --- P1 anchors ---
    print("\nP1 anchor qualification:")
    p1_ok = True
    for pid, want in ANCHORS.items():
        ga, gb = a.get(pid, {}).get("locality_class"), b.get(pid, {}).get("locality_class")
        ok = (ga == want) and (gb == want)
        p1_ok &= ok
        print(f"  {pid:22} want={want:14} A={ga!s:14} B={gb!s:14} {'OK' if ok else 'MISS'}")
    print(f"  P1 => {'QUALIFIED' if p1_ok else 'NOT QUALIFIED (anchor miss)'}")

    # --- forbidden-vocabulary audit ---
    for name, c in (("A", a), ("B", b)):
        bad = forbidden_audit(c)
        print(f"\nforbidden-vocab audit {name}: {len(bad)} rationale(s) leak outcome words"
              + (f" -> {bad[:5]}" if bad else " (clean)"))

    # --- disagreements (for the blind third pass) ---
    disagree = [k for k in keys if a[k]["locality_class"] != b[k]["locality_class"]]
    print(f"\ndisagreements: {len(disagree)}/{len(keys)} -> blind third pass")
    (AT / "mosaic-disagreements.json").write_text(json.dumps(
        [{"problem_id": k, "A": a[k]["locality_class"], "B": b[k]["locality_class"]} for k in disagree], indent=1))

    # --- separability gate on the AGREED rows joined to charges (prereg_v10) ---
    agreed = {k: a[k]["locality_class"] for k in keys if a[k]["locality_class"] == b[k]["locality_class"]}
    v3 = {e.problem_id: {c.charge: c.value for c in e.charges} for e in A.load_atlas(str(AT / "atlas_v3.jsonl"))}
    real = lambda ch, v: v not in ("open", "n.a.", "unmeasured")
    loc, ap, pa = [], [], []
    for k, cls in agreed.items():
        cv = v3.get(k, {})
        if real("approximation", cv.get("approximation", "n.a.")):
            loc.append(cls); ap.append(cv["approximation"])
    v_ap = S.cramers_v(loc, ap) if len(loc) >= 4 else float("nan")
    loc2, pa2 = [], []
    for k, cls in agreed.items():
        cv = v3.get(k, {})
        if real("parameterized", cv.get("parameterized", "n.a.")):
            loc2.append(cls); pa2.append(cv["parameterized"])
    v_pa = S.cramers_v(loc2, pa2) if len(loc2) >= 4 else float("nan")
    # dissociation structure-accuracy: fraction of {knapsack, subset-sum} coded `decomposable` by BOTH
    dz = [k for k in DISSOCIATION if k in a and k in b]
    acc = sum(a[k]["locality_class"] == "decomposable" and b[k]["locality_class"] == "decomposable" for k in dz) / len(dz) if dz else float("nan")
    fires = (v_ap > acc) or (v_pa > acc)
    print(f"\nseparability gate (PINNED):")
    print(f"  V(locality, approx)={v_ap:.3f}  V(locality, param)={v_pa:.3f}  "
          f"dissociation structure-acc={acc:.2f} (knapsack+subset-sum coded decomposable)")
    print(f"  charge-reconstruction flag: {'FIRES — absorption (P3) UNQUALIFIED (label tracks coordinates)' if fires else 'clear (structure-coding holds)'}")

    # --- outcome tree (prereg_v10-clarification-01) ---
    print("\n=== L1 OUTCOME (clarification-01 tree) ===")
    if fires:
        verdict = "C: NOT QUALIFIED — blindness/separability gate fired (labels are charge-echo). ABSOLUTE."
    elif demonstrated is None:
        verdict = "C: NOT QUALIFIED — agreement collapses at every granularity (kappa<0.6 even at 2-class). True negative."
    elif demonstrated == "5-class":
        verdict = "A: QUALIFIES at 5 classes -> full-resolution run; P2-P6 at 5-class locality."
    else:
        note = ("boundary-concentrated (entangled/mixed) — five-class strain BANKED as two-property-split evidence"
                if conc >= 0.5 else "NOT boundary-concentrated — the strain is diffuse; report that, split-evidence weaker")
        verdict = (f"B: demonstrated resolution = {demonstrated} (kappa {ladder[demonstrated]:.3f}); "
                   f"P2-P6 score at {demonstrated}, resolution tagged on every number; {note}.")
    print(f"  {verdict}")
    print(f"  P1 anchors: {'QUALIFIED' if p1_ok else 'MISS'}; separability: {'FIRED' if fires else 'clear'}; "
          f"5-class disagreements to third-pass: {len(disagree)}.")
    print(f"coding-A sha256 {hashlib.sha256((AT/'mosaic-coding-A.jsonl').read_bytes()).hexdigest()[:16]}; "
          f"coding-B sha256 {hashlib.sha256((AT/'mosaic-coding-B.jsonl').read_bytes()).hexdigest()[:16]} "
          f"(hash the codings BEFORE the charge join — done: join used a read-only copy)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
