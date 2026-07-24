#!/usr/bin/env python3
"""Atlas v3 freeze finalizer (V3) — merges the read-only frozen kernel + the v3 rows into
`atlas_v3.jsonl`, emits its sha256, and validates. Models dev/build_strata.py::write_atlas_v2.

GATE: refuses to freeze while any v3 cell is still `claimed` (the owner confirm-pass, V2, must have
run) unless `--allow-claimed` is passed for a DRY RUN. Freeze waits on confirm-complete, full stop —
no other gate.

  python dev/freeze_atlas_v3.py --dry-run --allow-claimed   # rehearse: build, hash, validate, discard
  python dev/freeze_atlas_v3.py                             # the real freeze (post-confirm)

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
    ap.add_argument("--allow-claimed", action="store_true", help="bypass the confirm gate (dry run only)")
    a = ap.parse_args()

    kernel = [l for l in open(KERNEL) if l.strip()]
    v3 = []
    for w in WAVES:
        p = os.path.join(ATLAS_DIR, f"quarry-v3-{w}.jsonl")
        if os.path.exists(p):
            v3 += [l for l in open(p) if l.strip()]
    if not v3:
        print("no v3 wave rows found", file=sys.stderr); return 1

    # --- confirm gate (V2 must have run) ---
    claimed = sum(1 for l in v3 for c in json.loads(l)["charges"] if c["status"] == "claimed")
    confirmed = sum(1 for l in v3 for c in json.loads(l)["charges"] if c["status"] == "confirmed")
    print(f"v3 cells: claimed={claimed}  confirmed={confirmed}")
    if claimed and not a.allow_claimed:
        print(f"\nREFUSING TO FREEZE: {claimed} cells are still `claimed`.", file=sys.stderr)
        print("The owner confirm-pass (V2) must complete first — see dev/confirm_harness.py.", file=sys.stderr)
        print("(Use --dry-run --allow-claimed to rehearse the freeze.)", file=sys.stderr)
        return 2

    # --- CITE-debt gate (prereg_v9-clarification-01, 2026-07-24) ---
    # No cell enters the freeze with an unresolved CITE: Check-9 is the atlas's identity, and at
    # freeze time a value whose citation does not establish it is folklore with extra steps.
    cdir = os.path.join(ATLAS_DIR, "v3-confirm")
    cites = []
    if os.path.isdir(cdir):
        cur = {}
        for l in v3:
            r = json.loads(l)
            for c in r["charges"]:
                cur[(r["problem_id"], c["charge"])] = (c.get("provenance") or {}).get("citation", "")
        # walk RECURSIVELY: verdicts live at the top level (V2) and under pass2/ (the second pass).
        # A non-recursive listdir silently exempted every second-pass CITE from this gate.
        vfiles = [os.path.join(dp, fn) for dp, _, fns in os.walk(cdir)
                  for fn in sorted(fns) if fn.startswith("verdicts") and fn.endswith(".json")]
        for fn in sorted(vfiles):
            for v in json.load(open(fn)):
                if v.get("verdict", "").upper() != "CITE":
                    continue
                key = (v["problem_id"], v["charge"])
                want = (v.get("corrected_citation") or "").strip()
                if want and want[:40] not in (cur.get(key) or ""):
                    cites.append(f"{v['problem_id']}/{v['charge']}")
    if cites and not a.allow_claimed:
        print(f"\nREFUSING TO FREEZE: {len(cites)} unresolved CITE cells (citation does not establish "
              f"the value).", file=sys.stderr)
        print("  " + ", ".join(sorted(cites)[:8]) + (" ..." if len(cites) > 8 else ""), file=sys.stderr)
        print("Apply the corrected citations from results/atlas/v3-confirm/ first.", file=sys.stderr)
        return 4
    if cites:
        print(f"[dry run] {len(cites)} CITE cells still unresolved (would block a real freeze)")

    # --- dedup guard: kernel ids must not collide with v3-new ids ---
    kids = {json.loads(l)["problem_id"] for l in kernel}
    vids = [json.loads(l)["problem_id"] for l in v3]
    dupes = sorted(kids & set(vids))
    if dupes:
        print(f"REFUSING: v3 rows collide with kernel ids: {dupes[:10]}", file=sys.stderr); return 3
    if len(vids) != len(set(vids)):
        print("REFUSING: duplicate problem_id among v3 rows", file=sys.stderr); return 3

    # --- apply errata-v1 to the KERNEL COPY carried into v3 (owner ruling 2026-07-24) ---
    # v1 bytes stay frozen on disk; v3 carries the CORRECTED values. Each corrected cell is tagged
    # `erratum_v1` so the v2->v3 delta decomposition books it as ERRATUM, not drift.
    # `superpoly-APX` is a V3_SPEC rung (not in the kernel vocab) — see dev/quarry_v3_spec.py
    VOCAB_OK = {"poly-APX", "superpoly-APX", "APX-complete", "APX", "log-APX", "PTAS", "inapprox"}
    epath = os.path.join(ATLAS_DIR, "errata-v1.json")
    n_err, deferred = 0, []
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
                if e["now"] in VOCAB_OK and e["now"] != c["value"]:
                    c["value"] = e["now"]; touched = True; n_err += 1
                    if e.get("corrected_canonical_task"):      # object drift / re-derivation
                        c["canonical_task"] = e["corrected_canonical_task"]
                elif e["now"] not in VOCAB_OK:
                    deferred.append(f"{r['problem_id']}/{c['charge']}")
                    continue
                prov = c.setdefault("provenance", {})
                if e.get("citation"):
                    prov["citation"] = e["citation"]
                prov["note"] = (prov.get("note", "") + f" | [erratum_v1 2026-07-24] {e['reason'][:160]}").strip(" |")
                prov["erratum_v1"] = True          # delta decomposition: erratum, NOT drift
                touched = True
            fixed.append(json.dumps(r, ensure_ascii=False) + "\n" if touched else line)
        kernel = fixed
        print(f"errata-v1 applied to the v3 kernel copy: {n_err} value corrections"
              + (f"; {len(deferred)} DEFERRED (no valid rung — owner ruling): {', '.join(deferred)}" if deferred else ""))

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
