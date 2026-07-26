#!/usr/bin/env python3
"""Mosaic v3 G2 — ARM A: can the ALGEBRA be recovered from SURFACE COMBINATORICS?

prereg_v12 A1/A2. Features: surface only, the 10 Post flags and their derivatives EXCLUDED by sealed rule.
Folds: the 46 poly-fingerprint groups (grouped CV — the key never enters the fit; it only stops
identical-profile near-duplicates straddling train/test, making the test strictly harder).
Null: the PER-CHARGE modal baseline, NOT joint-modal. Ceiling: 100% (the profile is flag-determined).

SEAL ORDERING: predictions are written and HASHED, then scored. The hash is printed with the assertion.
Model: depth-limited CART (interpretable primary, per spec §3). Pure numpy+stdlib; no new dependency.
"""
import hashlib, json, sys
from collections import Counter
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
LAT = ROOT / "foundry" / "results" / "lattice"
OUT = LAT / "grid_arm_a_results.json"
PRED = LAT / "grid_arm_a_predictions.json"
SEED, DEPTH, MINLEAF = 20260725, 6, 8
CHARGES = ("decision","counting","localization","parallelization","approx_counting",
           "parameterized","approx_maxones","approx_minones")
FLAGS = ("0valid","1valid","horn","dualhorn","bijunctive","affine",
         "width2affine","strongly0valid","IHSB","general_wsep")

def gini(y):
    if len(y)==0: return 0.0
    _,c=np.unique(y,return_counts=True); p=c/len(y); return 1.0-(p*p).sum()

def build(X,y,depth):
    if depth==0 or len(y)<2*MINLEAF or len(np.unique(y))==1:
        v,c=np.unique(y,return_counts=True); return {"leaf":v[c.argmax()]}
    best=None; g0=gini(y)
    for j in range(X.shape[1]):
        vals=np.unique(X[:,j])
        if len(vals)<2: continue
        for t in (vals[:-1]+vals[1:])/2.0:
            m=X[:,j]<=t
            if m.sum()<MINLEAF or (~m).sum()<MINLEAF: continue
            g=(m.sum()*gini(y[m])+(~m).sum()*gini(y[~m]))/len(y)
            if best is None or g<best[0]: best=(g,j,t,m)
    if best is None or g0-best[0]<1e-9:
        v,c=np.unique(y,return_counts=True); return {"leaf":v[c.argmax()]}
    _,j,t,m=best
    return {"j":int(j),"t":float(t),"L":build(X[m],y[m],depth-1),"R":build(X[~m],y[~m],depth-1)}

def pred1(node,x):
    while "leaf" not in node: node=node["L"] if x[node["j"]]<=node["t"] else node["R"]
    return node["leaf"]

def predict(tree,X): return np.array([pred1(tree,x) for x in X])

def main():
    surf=json.loads((LAT/"grid_surface_features.json").read_text())
    fold=json.loads((LAT/"grid_folds_and_strata.json").read_text())
    ct={f"b{r['arity']}:{_bm(r['arity'],r['relation'])}":r
        for r in json.loads((LAT/"prism_v2_charges.json").read_text())["charge_table"]}
    CLEAN="--clean" in sys.argv
    # ARITHMETIC-CLOSURE EXCLUSION (owner ruling): exclusion must be closed under arithmetic derivation,
    # not just under naming. weight_mean x n_tuples = S(strict bins) + arity*w_arity reconstructs the
    # excluded end bins EXACTLY. weight_spread = max-min touches the same extremes. Both go.
    LEAK_MOMENTS={"weight_mean","weight_spread"}
    feats=[f for f in surf["feature_names"] if f not in surf["starved_features"]]
    if CLEAN: feats=[f for f in feats if f not in LEAK_MOMENTS]
    fkey={r["row_key"]:r["fold_key"] for r in fold["rows"]}
    bdist={r["row_key"]:str(r["boundary_distance"]) for r in fold["rows"]}
    keys=[r["row_key"] for r in surf["rows"] if r["row_key"] in ct]
    X=np.array([[surf_row["features"][f] for f in feats]
                for surf_row in surf["rows"] if surf_row["row_key"] in ct],dtype=float)
    groups=np.array([fkey[k] for k in keys])

    # grouped 5-fold: assign each of the 46 groups to a fold, hash-ordered (sealed rule)
    ug=sorted(set(groups)); rng=np.random.default_rng(SEED)
    order=sorted(ug,key=lambda g:hashlib.sha256((g+str(SEED)).encode()).hexdigest())
    gfold={g:i%5 for i,g in enumerate(order)}
    folds=np.array([gfold[g] for g in groups])

    def fold_null(y, folds):
        """THE ACHIEVABLE baseline: predict the TRAINING folds' modal class on each test fold. The global
        modal share is NOT achievable by a model that only sees training data, and quoting it as the null
        mis-denominates the comparison (defect-#15's cousin: numerator and denominator on different
        populations)."""
        yp=np.empty(len(y),dtype=object)
        for f in range(5):
            tr,te=folds!=f,folds==f
            if te.sum()==0 or tr.sum()==0: continue
            yp[te]=Counter(y[tr]).most_common(1)[0][0]
        return float((yp==y).mean())

    targets={c:np.array([ct[k][c] for k in keys]) for c in CHARGES}
    targets.update({f"FLAG:{f}":np.array([int(ct[k]["flags"][f]) for k in keys]) for f in FLAGS})

    preds={}
    for name,y in targets.items():
        yp=np.empty(len(y),dtype=object)
        for f in range(5):
            tr,te=folds!=f,folds==f
            if te.sum()==0 or len(np.unique(y[tr]))==0: continue
            yp[te]=predict(build(X[tr],y[tr],DEPTH),X[te])
        preds[name]=yp

    # ---- SEAL: write + hash predictions BEFORE scoring ----
    PRED.write_text(json.dumps({"seed":SEED,"features":feats,"n":len(keys),
        "predictions":{n:[str(v) for v in p] for n,p in preds.items()},"row_keys":keys},indent=1)+"\n")
    ph=hashlib.sha256(PRED.read_bytes()).hexdigest()
    print(f"predictions sealed: {PRED.name} sha256 {ph[:16]} (hashed BEFORE scoring)")

    # ---- score ----
    res={"seed":SEED,"n_classes":len(keys),"features_used":feats,"n_features":len(feats),
         "prediction_sha256":ph,"model":f"CART depth<={DEPTH} minleaf={MINLEAF}",
         "fold_key":"46 poly-fingerprint groups, hash-ordered into 5 folds","ceiling":1.0}
    charge_acc={}; nulls={}
    for c in CHARGES:
        y=targets[c]; yp=preds[c]
        acc=float((yp==y).mean()); mode=fold_null(y,folds)
        charge_acc[c]={"acc":round(acc,4),"modal_null_foldweighted":round(mode,4),"lift":round(acc-mode,4)}
    res["per_charge"]=charge_acc
    ham=float(np.mean([[preds[c][i]==targets[c][i] for c in CHARGES] for i in range(len(keys))]))
    ham_null=float(np.mean([fold_null(targets[c],folds) for c in CHARGES]))
    exact=float(np.mean([all(preds[c][i]==targets[c][i] for c in CHARGES) for i in range(len(keys))]))
    exact_null=Counter(tuple(targets[c][i] for c in CHARGES) for i in range(len(keys))).most_common(1)[0][1]/len(keys)
    res["headline"]={"hamming":round(ham,4),"hamming_null_per_charge":round(ham_null,4),
                     "hamming_lift":round(ham-ham_null,4),
                     "exact_profile":round(exact,4),"exact_null_joint_modal":round(exact_null,4),
                     "exact_lift":round(exact-exact_null,4)}
    res["per_flag_recovery"]={f:{"acc":round(float((preds[f'FLAG:{f}']==targets[f'FLAG:{f}']).mean()),4),
                                "modal_null_foldweighted":round(fold_null(targets[f'FLAG:{f}'],folds),4)}
                              for f in FLAGS}
    # error geography by boundary distance (stratification only)
    geo={}
    for d in ("1","2",">2"):
        idx=[i for i,k in enumerate(keys) if bdist[k]==d]
        if not idx: continue
        geo[d]={"n":len(idx),
                "hamming":round(float(np.mean([[preds[c][i]==targets[c][i] for c in CHARGES] for i in idx])),4),
                "exact":round(float(np.mean([all(preds[c][i]==targets[c][i] for c in CHARGES) for i in idx])),4)}
    res["error_geography_by_boundary_distance"]=geo
    res["arithmetic_closure"]={"clean_run":CLEAN,"dropped_moments":sorted(LEAK_MOMENTS) if CLEAN else [],
        "leak_identity":"weight_mean * n_tuples = S(strict bins) + arity * w_arity -> w_arity, then w_0, EXACT"}
    (LAT/("grid_arm_a_results_clean.json" if CLEAN else "grid_arm_a_results.json")).write_text(
        json.dumps(res,indent=1)+"\n")

    print(f"\nARM A — surface-only, {len(feats)} features, {len(keys)} classes, 5 grouped folds")
    print(f"  HAMMING  {ham:.4f}  vs per-charge modal null {ham_null:.4f}   lift {ham-ham_null:+.4f}")
    print(f"  EXACT    {exact:.4f}  vs joint-modal null    {exact_null:.4f}   lift {exact-exact_null:+.4f}   (ceiling 1.0)")
    print("\n  per-charge:")
    for c,v in charge_acc.items():
        print(f"    {c:<18} {v['acc']:.4f}  null {v['modal_null_foldweighted']:.4f}  lift {v['lift']:+.4f}")
    print("\n  PER-FLAG RECOVERY (the diagnostic — profile accuracy factors through this):")
    for f,v in res["per_flag_recovery"].items():
        print(f"    {f:<16} {v['acc']:.4f}  null {v['modal_null_foldweighted']:.4f}  "
              f"lift {v['acc']-v['modal_null_foldweighted']:+.4f}")
    print("\n  error geography by boundary distance:")
    for d,v in geo.items(): print(f"    d={d:<3} n={v['n']:<5} hamming {v['hamming']:.4f}  exact {v['exact']:.4f}")
    return 0

def _bm(a,rel):
    m=0
    for t in rel:
        i=0
        for b in t: i=(i<<1)|int(b)
        m|=(1<<i)
    return f"{m:0{max(1,(2**a+3)//4)}x}"

if __name__=="__main__": sys.exit(main())
