"""Regression guard for object drift at the generator level (methods 40).

`horn-sat` emitted uniform random 3-CNF for the whole survey sequence while carrying a pinned Horn
template, because its generator branch was byte-identical to the plain one. This test is the guard that
would have caught it on the day it was written.

It asserts the SEMANTIC implication the forcedness join actually consumes — if the pinned template is
closed under f, every emitted instance's solution set is closed under f — and, for clausal generators,
the syntactic emission rule that localises a failure to the generator.
"""
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "dev")); sys.path.insert(0, str(ROOT))

import generator_conformance as GC   # noqa: E402


def test_every_templated_generator_conforms():
    rng = random.Random(4242)
    flags, B = GC.load_flags(), GC.builders(rng)
    failures = []
    for row in sorted(set(flags) & set(B)):
        want = flags[row]
        if not want:
            continue
        for _ in range(3):
            region, cls = B[row]()
            if not region or len(region) < 3:
                continue
            for f in want:
                op, m, _ = GC.FLAG_OP[f]
                ok, _seen = GC.closed_under(region, op, m, rng)
                if ok is False:
                    failures.append(f"{row}: solution set NOT closed under {f}")
                if cls and f in GC.SYNTACTIC and not GC.SYNTACTIC[f][1](cls):
                    failures.append(f"{row}: emitted clauses violate '{GC.SYNTACTIC[f][0]}'")
    assert not failures, "generator drift:\n  " + "\n  ".join(sorted(set(failures)))


def test_horn_generator_emits_horn_clauses():
    """The specific defect, pinned so it cannot silently return."""
    import sounding_v3_survey as S3
    rng = random.Random(7)
    S3.sat(rng, 2.0, 3, "horn")
    assert S3.LAST_CLAUSES, "generator did not publish its clauses"
    for _vs, sg in S3.LAST_CLAUSES:
        assert sum(sg) <= 1, f"Horn clause with {sum(sg)} positive literals: {sg}"
