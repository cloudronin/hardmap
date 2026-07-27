#!/usr/bin/env python3
"""The `string` family's ramp erratum, and the pilot that decides whether the row survives it.

WHAT WENT WRONG. The reach census declared the `string` family's ramp as "pattern/text length ratio"
with "precedent: none yet — declared here, first use at build". At first use it had no referent:
`minimum-common-string-partition` takes two strings of EQUAL LENGTH and asks for a common partition.
There is no pattern and no text. The census's family-ramp declarations are typings — claims about a
family's reach — and a typing with no referent in the family's only reachable row is a typing falsified
at build time.

THE AMENDMENT, by ruling: **alphabet size at fixed string length.** A genuine structural dial — a
smaller alphabet makes substrings collide, which densifies the constraint interactions — and crucially
NOT a size knob, so it does not collide with the reserved scaling axis. The string length is held fixed
at every step precisely so that what moves is structure and not size.

THE DIRECTION IS NOT ASSERTED HERE. Which end of the alphabet ramp *hardens* is exactly the sort of
thing that gets written down from memory and turns out backwards. So the pilot measures the region
across the ramp and the direction is read off the result, alongside the derived-consequence check that
the row is upward-closed in its cut set. If the regions do not move, the row types
`no-natural-dial-at-fixed-encoding` honestly and the string family carries zero ramped rows — but it
gets its chance to move first.
"""
import json
import random
import sys
from collections import Counter
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "dev"))
from foundry.catalog import maptrail as M                                       # noqa: E402
from foundry.helm import sweep as SW                                            # noqa: E402

LAT = ROOT / "foundry" / "results" / "lattice"
TRAIL = LAT / "maptrail.jsonl"
OUT = LAT / "mcsp_ramp_pilot.json"

N = 11                      # string length, HELD FIXED across the ramp — this is not a size knob
ALPHABET_RAMP = (2, 3, 4, 6, 8)
SEED = 20260727
N_INSTANCES = 8
PLANTED_BLOCKS = 4          # HELD FIXED — see below

# THE FIRST PILOT RUN CONFOUNDED THE DIAL. It drew the planted rearrangement's block count uniformly
# from 2..4 per instance, and block count drives the number of valid partitions far harder than the
# alphabet does. The result was a trajectory reading 642 -> 203 -> 198 -> 413 -> 384 with within-step
# spread (136..512 at |Sigma| = 8) swamping every between-step difference — and an endpoint comparison
# that reported "larger alphabet TIGHTENS" from a non-monotone series. Holding the block count fixed
# isolates the dial, which is what "at fixed string length" meant in spirit: hold everything but it.

# The move/flat decision reuses the catalog extractor's OWN pinned rule rather than inventing a
# threshold here: a trajectory counts as moving iff its excursion exceeds 2x the pooled within-step SD.
FLAT_MULTIPLIER = 2.0


def make_instance(rng, k, n=N, n_blocks=PLANTED_BLOCKS):
    """A over an alphabet of size k, and B a block-rearrangement of A. B is a valid rearrangement by
    construction, so the instance is always feasible and the region is never empty for trivial reasons.

    `n_blocks` is FIXED so the alphabet is the only thing moving along the ramp."""
    A = "".join(chr(ord("a") + rng.randrange(k)) for _ in range(n))
    cuts = sorted(rng.sample(range(1, n), min(n_blocks - 1, n - 1)))
    blocks, prev = [], 0
    for c in cuts + [n]:
        blocks.append(A[prev:c]); prev = c
    rng.shuffle(blocks)
    return A, "".join(blocks)


def can_partition(B, blocks):
    """Can B be cut into exactly this multiset of blocks?"""
    need = Counter(blocks)

    def rec(i):
        if i == len(B):
            return all(v == 0 for v in need.values())
        for b in list(need):
            if need[b] and B.startswith(b, i):
                need[b] -= 1
                if rec(i + len(b)):
                    need[b] += 1
                    return True
                need[b] += 1
        return False
    return rec(0)


def mcsp(rng, k, n=N):
    """Region = cut-position subsets of A whose induced blocks also partition B. Upward-closed: a cut
    added to a working partition splits one A-block, and the matched B-block splits identically."""
    A, B = make_instance(rng, int(round(k)), n)
    feasible = []
    for s in product((0, 1), repeat=n - 1):
        blocks, prev = [], 0
        for i, bit in enumerate(s, start=1):
            if bit:
                blocks.append(A[prev:i]); prev = i
        blocks.append(A[prev:])
        if can_partition(B, blocks):
            feasible.append(s)
    if len(feasible) < 2:
        return []
    b = min(sum(s) for s in feasible)
    return [("feasible", feasible), ("optimal", [s for s in feasible if sum(s) == b])]


def main() -> int:
    M.emit(TRAIL, "erratum", key="erratum:string-family-ramp",
           artifact="observatory_reach_census.json",
           field="family_ramp_parameters.string.param",
           old="pattern/text length ratio",
           new="alphabet size at fixed string length",
           why=("the declared ramp had no referent in the family's only reachable row — MCSP takes two "
                "equal-length strings and has neither a pattern nor a text. A family-ramp declaration "
                "is a typing, and this one was falsified at first use."),
           not_a_size_knob=("string length is held fixed across the ramp, so the dial moves structure "
                            "rather than size and does not collide with the reserved scaling axis"),
           authority="owner ruling, 2026-07-27",
           direction_pinned_by="pilot measurement, not assertion — see mcsp_ramp_pilot.json")
    print("MCSP RAMP PILOT — alphabet size at fixed string length (n = %d)\n" % N)

    rows, obs = [], []
    for k in ALPHABET_RAMP:
        rng = random.Random(SEED + k)
        sizes, opt = [], []
        for _ in range(N_INSTANCES):
            d = dict(mcsp(rng, k) or [])
            if d:
                sizes.append(len(d["feasible"])); opt.append(len(d["optimal"]))
        mean = (sum(sizes) / len(sizes)) if sizes else None
        sd = ((sum((x - mean) ** 2 for x in sizes) / len(sizes)) ** 0.5) if len(sizes) > 1 else None
        rows.append({"alphabet": k, "feasible_sizes": sizes, "optimal_sizes": opt,
                     "feasible_mean": mean, "feasible_sd": sd})
        obs += [(k, s) for s in sizes]
        print(f"  |Sigma| = {k:<2}  mean {mean:>7.1f}  sd {sd:>6.1f}   {sizes}")

    have = [r for r in rows if r["feasible_mean"] is not None]
    means = [r["feasible_mean"] for r in have]
    sds = [r["feasible_sd"] for r in have if r["feasible_sd"] is not None]
    excursion = (max(means) - min(means)) if means else 0.0
    pooled_sd = (sum(sds) / len(sds)) if sds else 0.0
    # The SAME rule the catalog uses to call a trajectory FLAT — reused rather than re-invented, so the
    # pilot cannot pass under a laxer standard than the descriptor layer applies to every other row.
    moved = bool(pooled_sd and excursion >= FLAT_MULTIPLIER * pooled_sd)
    rho = SW.spearman([o[0] for o in obs], [o[1] for o in obs]) if len(obs) >= 3 else None
    direction = None
    if moved and rho is not None:
        direction = ("larger alphabet TIGHTENS (region shrinks)" if rho < 0
                     else "larger alphabet LOOSENS (region grows)")

    # LEAVE-ONE-OUT: does the dial still move without its most extreme step? A ramp whose entire signal
    # sits on one endpoint is a THRESHOLD, not a graded dial, and shipping it as a dial would put a
    # step function into a column the catalog reads as a trajectory. The check costs nothing and is the
    # difference between "the dial works" and "the smallest alphabet is special".
    lo_i = means.index(min(means)) if means else None
    hi_i = means.index(max(means)) if means else None
    drop_i = hi_i if abs(means[hi_i] - sum(means) / len(means)) > abs(
        means[lo_i] - sum(means) / len(means)) else lo_i
    rest = [m for j, m in enumerate(means) if j != drop_i]
    rest_sd = [r["feasible_sd"] for j, r in enumerate(have)
               if j != drop_i and r["feasible_sd"] is not None]
    rest_exc = (max(rest) - min(rest)) if rest else 0.0
    rest_pooled = (sum(rest_sd) / len(rest_sd)) if rest_sd else 0.0
    moves_without_extreme = bool(rest_pooled and rest_exc >= FLAT_MULTIPLIER * rest_pooled)
    dropped_step = have[drop_i]["alphabet"] if drop_i is not None else None
    shape = ("GRADED — the dial moves across its range" if moves_without_extreme
             else f"THRESHOLD — the movement is carried by |Sigma| = {dropped_step} alone; "
                  f"drop that step and the remaining range is FLAT under the same rule")

    # the derived-consequence check, run here rather than asserted
    rng = random.Random(SEED)
    d = dict(mcsp(rng, 3) or [])
    upward = None
    if d:
        S = set(d["feasible"])
        upward = all(
            tuple(1 if j == i else s[j] for j in range(len(s))) in S
            for s in d["feasible"] for i, v in enumerate(s) if v == 0)

    verdict = ("NO NATURAL DIAL — the amended dial does not move the region" if not moved
               else ("RAMP CONFIRMED (GRADED) — the amended dial moves across its range"
                     if moves_without_extreme else
                     "RAMP CONFIRMED (THRESHOLD ONLY) — the dial moves, but the movement is carried "
                     "entirely by the smallest alphabet. This is a two-point contrast wearing a ramp's "
                     "clothes, and it is a third case the ruling did not name: not a working graded "
                     "dial, not an absent one. RAISED FOR RULING."))
    doc = {"schema": "mcsp-ramp-pilot/v1",
           "STATUS": "PILOT — descriptive, no verdict about complexity",
           "problem": "minimum-common-string-partition", "family": "string",
           "ramp_before": "pattern/text length ratio (no referent in the row)",
           "ramp_after": "alphabet size at fixed string length",
           "string_length_held_fixed_at": N,
           "alphabet_ramp": list(ALPHABET_RAMP), "measurements": rows,
           "region_moves": moved, "hardening_direction": direction,
           "ramp_shape": shape, "moves_without_extreme_step": moves_without_extreme,
           "extreme_step_dropped": dropped_step,
           "excursion": round(excursion, 2), "pooled_within_step_sd": round(pooled_sd, 2),
           "move_rule": f"moves iff excursion >= {FLAT_MULTIPLIER} x pooled within-step SD — the catalog extractor's own FLAT rule, reused not re-invented",
           "rank_correlation_alphabet_vs_region": (round(rho, 4) if rho is not None else None),
           "n_instances_per_step": N_INSTANCES, "planted_blocks_held_fixed_at": PLANTED_BLOCKS,
           "direction_provenance": "read off the pilot measurement, never asserted from memory",
           "derived_consequence_upward_closed": upward,
           "derived_consequence_note": ("adding a cut to a working partition splits one A-block, and "
                                        "the matched B-block splits identically — so the region must be "
                                        "upward-closed. Checked, not assumed."),
           "verdict": verdict}
    OUT.write_text(json.dumps(doc, indent=1) + "\n")

    print(f"\n  region moves along the amended ramp : {moved}")
    print(f"  hardening direction                 : {direction}")
    print(f"  derived consequence (upward-closed) : {upward}")
    print(f"\n  {verdict}")
    print(f"  wrote {OUT.name}; erratum emitted to {TRAIL.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
