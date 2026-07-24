#!/usr/bin/env python3
"""Atlas v3 freeze finalizer (V3) — merges the read-only frozen kernel + the v3 rows into
`atlas_v3.jsonl`, emits its sha256, and validates. Models dev/build_strata.py::write_atlas_v2.

GATES (owner ruling 2026-07-24): v3 freezes on CITE-clean + kill-criterion 1 — the conditions v1 was
actually held to. `confirmed` status is NOT a freeze condition (frozen v1 shipped 2/331 confirmed), so
`claimed` cells freeze; the prior zero-`claimed` gate was an over-construction and is corrected in
docs/findings/methods-thread.md. Owner-`confirmed` promotion is a rolling v3.1 spot-check, not a blocker.

  python dev/freeze_atlas_v3.py --dry-run   # rehearse: build, hash, validate, discard
  python dev/freeze_atlas_v3.py             # the real freeze (CITE-clean + kill-criterion enforced)

The frozen v1 `atlas.jsonl` is read-only here and is never rewritten.
"""
import argparse, hashlib, json, os, subprocess, sys

ATLAS_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                          "..", "eightfold", "results", "atlas"))
KERNEL = os.path.join(ATLAS_DIR, "atlas.jsonl")
DEST = os.path.join(ATLAS_DIR, "atlas_v3.jsonl")
PROV_SRC = os.path.join(ATLAS_DIR, "quarry-v3-provenance.jsonl")
PROV_DEST = os.path.join(ATLAS_DIR, "atlas_v3_provenance.jsonl")
WAVES = ("w1", "w2", "w3", "w4")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="build + hash + validate, then discard")
    ap.add_argument("--allow-claimed", action="store_true", help="DEPRECATED no-op; `claimed` no longer gates")
    a = ap.parse_args()

    kernel = [l for l in open(KERNEL) if l.strip()]
    v3 = []
    for w in WAVES:
        p = os.path.join(ATLAS_DIR, f"quarry-v3-{w}.jsonl")
        if os.path.exists(p):
            v3 += [l for l in open(p) if l.strip()]
    if not v3:
        print("no v3 wave rows found", file=sys.stderr); return 1

    # --- freeze semantics (owner ruling 2026-07-24, correcting the prior zero-`claimed` gate) ---
    # v3 freezes on CITE-clean + kill-criterion — the conditions v1 was ACTUALLY held to. `confirmed`
    # status is NOT a freeze condition: the frozen v1 kernel shipped with 2 of 331 real cells confirmed
    # and 329 `claimed`, so an all-confirmed gate would hold v3 to a standard v1 never met. v3's
    # `claimed` cells are double-agent-passed at full Check-9 with full-text evidence, swept three ways
    # (F-2, decision-membership, prose-vs-value), and recursively CITE-gated — more verification than v1
    # had at freeze. Owner-`confirmed` promotion is a rolling v3.1 spot-check, never a freeze blocker.
    # The superseded "426-cell sitting before freeze" ruling is corrected in docs/findings/methods-thread.md.
    from collections import Counter
    st = Counter(c["status"] for l in v3 for c in json.loads(l)["charges"])
    real = st.get("claimed", 0) + st.get("confirmed", 0) + st.get("measured", 0)
    print(f"v3 cells: claimed={st.get('claimed',0)} confirmed={st.get('confirmed',0)} "
          f"structural={st.get('structural',0)} measured={st.get('measured',0)}")
    print(f"trust label: {st.get('confirmed',0)}/{real} owner-confirmed; the rest agent-double-passed "
          f"(v3 standard = agent-double-passed, owner-unconfirmed)")
    # NOTE: --allow-claimed is retained only as an accepted no-op; `claimed` no longer blocks a freeze.

    # Verdict files feed both the CITE gate and the kill-criterion gate; enumerate once, RECURSIVELY
    # (verdicts live at the top level (V2) and under pass2/ (the second pass)).
    cdir = os.path.join(ATLAS_DIR, "v3-confirm")
    vfiles = ([os.path.join(dp, fn) for dp, _, fns in os.walk(cdir)
               for fn in sorted(fns) if fn.startswith("verdicts") and fn.endswith(".json")]
              if os.path.isdir(cdir) else [])

    # --- CITE-debt gate (prereg_v9-clarification-01): no cell freezes with an unresolved CITE ---
    cur = {}
    for l in v3:
        r = json.loads(l)
        for c in r["charges"]:
            cur[(r["problem_id"], c["charge"])] = (c.get("provenance") or {}).get("citation", "")
    cites = []
    for fn in sorted(vfiles):
        for v in json.load(open(fn)):
            if v.get("verdict", "").upper() != "CITE":
                continue
            key = (v["problem_id"], v["charge"])
            want = (v.get("corrected_citation") or "").strip()
            if want and want[:40] not in (cur.get(key) or ""):
                cites.append(f"{v['problem_id']}/{v['charge']}")
    if cites and not a.dry_run:                      # a real freeze refuses; a dry run warns
        print(f"\nREFUSING TO FREEZE: {len(cites)} unresolved CITE cells (citation does not establish "
              f"the value).", file=sys.stderr)
        print("  " + ", ".join(sorted(cites)[:8]) + (" ..." if len(cites) > 8 else ""), file=sys.stderr)
        print("Apply the corrected citations from results/atlas/v3-confirm/ first.", file=sys.stderr)
        return 4
    if cites:
        print(f"[dry run] {len(cites)} CITE cells still unresolved (would block a real freeze)")

    # --- kill-criterion 1 gate (spec §7; prereg clarification-01: VALUE errors only, CITE excluded) ---
    # The corpus is inadmissible if its confirmed value-error rate exceeds 15%. This is the real
    # quality bar that replaces the zero-`claimed` gate.
    fo = tv = 0
    for fn in sorted(vfiles):
        for v in json.load(open(fn)):
            vd = v.get("verdict", "").upper()
            if vd in ("OK", "CITE", "FIX", "OPEN"):
                tv += 1
                fo += vd in ("FIX", "OPEN")
    if tv:
        ve = 100.0 * fo / tv
        print(f"kill-criterion 1: value-error {fo}/{tv} = {ve:.1f}%  "
              + ("clears (< 15%)" if ve <= 15 else "EXCEEDS 15% — corpus inadmissible"))
        if ve > 15 and not a.dry_run:
            print("\nREFUSING TO FREEZE: kill-criterion 1 tripped (value-error > 15%).", file=sys.stderr)
            return 5

    # --- dedup guard: kernel ids must not collide with v3-new ids ---
    kids = {json.loads(l)["problem_id"] for l in kernel}
    vids = [json.loads(l)["problem_id"] for l in v3]
    dupes = sorted(kids & set(vids))
    if dupes:
        print(f"REFUSING: v3 rows collide with kernel ids: {dupes[:10]}", file=sys.stderr); return 3
    if len(vids) != len(set(vids)):
        print("REFUSING: duplicate problem_id among v3 rows", file=sys.stderr); return 3

    # --- apply errata-v1 to the KERNEL COPY carried into v3 (owner ruling 2026-07-24) ---
    # v1 bytes stay frozen on disk; v3 carries the CORRECTED values/citations. Each corrected cell is
    # tagged `erratum_v1` so the v2->v3 delta decomposition books it as ERRATUM, not drift.
    #
    # Entry schema (problem_id/charge/reason required; the rest optional, any combination):
    #   `now`                      corrected value — validated CHARGE-AWARE against V3_SPEC.allowed_values;
    #                              an illegal value is DEFERRED (owner ruling), never half-applied. A
    #                              sentinel value (open/n.a./unmeasured) also flips status -> structural.
    #                              `superpoly-APX` is a V3_SPEC rung, so it validates here but not against
    #                              the frozen kernel spec (dev/quarry_v3_spec.py).
    #   `corrected_canonical_task` object repin (object drift / re-derivation).
    #   `citation`                 REPLACES the cell citation.
    #   `add_citation`             co-citation APPENDED (the "cited to one side" repair — e.g. add the
    #                              membership half to a hardness-only citation).
    #   `derivation_note`          a one-line derivation recorded where the value follows trivially.
    # This block runs before the V3_SPEC validation below, so set up the import path here too.
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, os.path.normpath(os.path.join(ATLAS_DIR, "..", "..", "..")))
    import quarry_v3_spec as _v3spec
    epath = os.path.join(ATLAS_DIR, "errata-v1.json")
    n_val, n_cite, deferred = 0, 0, []
    if os.path.exists(epath):
        ent = {(e["problem_id"], e["charge"]): e for e in json.load(open(epath))["entries"]}
        fixed = []
        for line in kernel:
            r = json.loads(line)
            touched = False
            for c in r["charges"]:
                e = ent.get((r["problem_id"], c["charge"]))
                if not e:
                    continue
                nv = e.get("now")
                if nv is not None and nv != c["value"]:
                    if nv not in _v3spec.V3_SPEC.allowed_values(c["charge"]):
                        deferred.append(f"{r['problem_id']}/{c['charge']} -> {nv!r}")
                        continue                       # never half-apply a value we cannot legally write
                    c["value"] = nv; n_val += 1
                    if nv in _v3spec.V3_SPEC.sentinels:
                        c["status"] = "structural"     # sentinel cells carry the structural marker
                prov = c.setdefault("provenance", {})
                if e.get("corrected_canonical_task"):
                    c["canonical_task"] = e["corrected_canonical_task"]
                if e.get("citation"):
                    prov["citation"] = e["citation"]; n_cite += 1
                if e.get("add_citation"):
                    prov["citation"] = (prov.get("citation", "") + " + " + e["add_citation"]).strip(" +")
                    n_cite += 1
                if e.get("derivation_note"):
                    prov["derivation_note"] = e["derivation_note"]
                prov["note"] = (prov.get("note", "")
                                + f" | [erratum_v1 {e.get('date', '2026-07-24')}] {e['reason'][:160]}").strip(" |")
                prov["erratum_v1"] = True              # delta decomposition: erratum, NOT drift
                touched = True
            fixed.append(json.dumps(r, ensure_ascii=False) + "\n" if touched else line)
        kernel = fixed
        print(f"errata-v1 applied to the v3 kernel copy: {n_val} value corrections, {n_cite} citation corrections"
              + (f"; {len(deferred)} DEFERRED (value not a legal rung — owner ruling): {', '.join(deferred)}"
                 if deferred else ""))

    out = kernel + v3                      # kernel (errata-corrected copy) first, then v3-new
    dest = DEST + (".dryrun" if a.dry_run else "")
    with open(dest, "w") as f:
        f.writelines(out)
    sha = hashlib.sha256(open(dest, "rb").read()).hexdigest()
    print(f"\nwrote {len(out)} rows ({len(kernel)} kernel + {len(v3)} v3-new) -> {os.path.basename(dest)}")
    print(f"sha256: {sha}")

    # provenance sidecar travels with the frozen file
    if os.path.exists(PROV_SRC) and not a.dry_run:
        with open(PROV_DEST, "w") as f:
            f.write(open(PROV_SRC).read())
        print(f"provenance sidecar -> {os.path.basename(PROV_DEST)}")

    # validate against the V3 INSTRUMENT (V3_SPEC), not the kernel spec — v3 carries `superpoly-APX`,
    # which the frozen kernel vocabulary deliberately does not contain (prereg_v9-clarification-02).
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, os.path.normpath(os.path.join(ATLAS_DIR, "..", "..", "..")))
    from eightfold import atlas as _atlas
    import quarry_v3_spec as _v3
    _entries = _atlas.load_atlas(dest)
    _errs = _v3.validate_v3(_entries)
    print(f"\nV3_SPEC validation: {len(_entries)} rows, "
          + ("CLEAN" if not _errs else f"{len(_errs)} rows with errors: {list(_errs)[:5]}"))

    # the kernel must be untouched
    assert hashlib.sha256(open(KERNEL, "rb").read()).hexdigest() == \
        "6d53a4f1d0907f1668949ae8cba902f6b9c59209088f5b67d27bac2b5527eae7", "v1 kernel changed!"
    print("v1 kernel byte-identity: OK")
    if a.dry_run:
        os.remove(dest); print("(dry run — discarded)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
