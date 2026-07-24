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
        for fn in sorted(os.listdir(cdir)):
            if not fn.startswith("verdicts"):
                continue
            for v in json.load(open(os.path.join(cdir, fn))):
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

    out = kernel + v3                      # kernel first, byte-identical lines, then v3-new
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

    r = subprocess.run([sys.executable, "-m", "eightfold.atlas", "validate", "--path", dest],
                       cwd=os.path.join(ATLAS_DIR, "..", "..", ".."), capture_output=True, text=True)
    print("\n" + (r.stdout or r.stderr).strip().splitlines()[0])

    # the kernel must be untouched
    assert hashlib.sha256(open(KERNEL, "rb").read()).hexdigest() == \
        "6d53a4f1d0907f1668949ae8cba902f6b9c59209088f5b67d27bac2b5527eae7", "v1 kernel changed!"
    print("v1 kernel byte-identity: OK")
    if a.dry_run:
        os.remove(dest); print("(dry run — discarded)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
