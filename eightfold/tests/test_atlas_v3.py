"""Atlas v3 guard — protects the frozen atlas_v3.jsonl alongside the v1 kernel.

Mirrors tests/test_loader.py but targets the v3 path; touches NONE of the 118-pins (test_loader /
test_structure / test_strata keep protecting v1). Inert until the V3 freeze creates atlas_v3.jsonl
(skips cleanly), so it never breaks the suite during drafting.
"""
import hashlib
import json
import pathlib
import sys

import pytest

from eightfold import atlas

# V3_SPEC lives beside the kernel in dev/ (the Strata precedent: import read-only, never edit the
# kernel). v3 carries the `superpoly-APX` rung the frozen kernel vocabulary deliberately lacks, so v3
# validates against V3_SPEC, not EIGHTFOLD_SPEC.
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "dev"))
import quarry_v3_spec  # noqa: E402

V3_PATH = atlas.DEFAULT_PATH.parent / "atlas_v3.jsonl"
_V3_EXISTS = V3_PATH.exists()
skip_no_v3 = pytest.mark.skipif(not _V3_EXISTS, reason="atlas_v3.jsonl not frozen yet (created at V3)")

# v3.0 freeze hash (owner ruling 2026-07-24). A deliberate v3.1 re-freeze updates this pin.
V3_SHA256 = "e62f3c284b408a26d71e7f769c3742fa283f5a3bd5d874da74f0313ee3968dee"


def test_v1_still_frozen_at_118():
    """The v1 kernel is untouched by anything v3 does — always active."""
    entries = atlas.load_atlas(atlas.DEFAULT_PATH)
    assert len(entries) == 118


@skip_no_v3
def test_atlas_v3_loads_and_validates_clean():
    entries = atlas.load_atlas(V3_PATH)
    assert len(entries) > 118, "v3 must strictly extend the 118-row kernel"
    ids = [e.problem_id for e in entries]
    assert len(ids) == len(set(ids)), "problem_id unique across the whole v3 roster"
    # the 118 kernel ids are a subset of v3 (v3 = kernel + new rows)
    kernel_ids = {e.problem_id for e in atlas.load_atlas(atlas.DEFAULT_PATH)}
    assert kernel_ids <= set(ids)
    # validate against the V3 INSTRUMENT (carries superpoly-APX), not the frozen kernel spec
    assert atlas.validate_corpus(entries, quarry_v3_spec.V3_SPEC) == {}, "v3 passes the same gates as v1"


@skip_no_v3
def test_atlas_v3_byte_frozen():
    """v3.0 is byte-identical to its freeze — the same guarantee v1 has (a v3.1 re-freeze updates the pin)."""
    got = hashlib.sha256(V3_PATH.read_bytes()).hexdigest()
    assert got == V3_SHA256, f"atlas_v3.jsonl changed since freeze: {got}"


@skip_no_v3
def test_atlas_v3_roundtrips():
    for e in atlas.load_atlas(V3_PATH):
        d = atlas.entry_to_dict(e)
        assert atlas.entry_to_dict(atlas.entry_from_dict(d)) == d


@skip_no_v3
def test_atlas_v3_provenance_sidecar_covers_new_rows():
    """Every v3-new row has a provenance sidecar record (funnel/wave/membership)."""
    sidecar = V3_PATH.parent / "atlas_v3_provenance.jsonl"
    assert sidecar.exists(), "provenance sidecar must ship with atlas_v3.jsonl"
    prov = {json.loads(l)["problem_id"] for l in sidecar.read_text().splitlines() if l.strip()}
    kernel_ids = {e.problem_id for e in atlas.load_atlas(atlas.DEFAULT_PATH)}
    new_ids = {e.problem_id for e in atlas.load_atlas(V3_PATH)} - kernel_ids
    missing = new_ids - prov
    assert not missing, f"v3-new rows missing provenance: {sorted(missing)[:10]}"
