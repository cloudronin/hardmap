"""Atlas v3 guard — protects the frozen atlas_v3.jsonl alongside the v1 kernel.

Mirrors tests/test_loader.py but targets the v3 path; touches NONE of the 118-pins (test_loader /
test_structure / test_strata keep protecting v1). Inert until the V3 freeze creates atlas_v3.jsonl
(skips cleanly), so it never breaks the suite during drafting.
"""
import json
import pathlib

import pytest

from eightfold import atlas

V3_PATH = atlas.DEFAULT_PATH.parent / "atlas_v3.jsonl"
_V3_EXISTS = V3_PATH.exists()
skip_no_v3 = pytest.mark.skipif(not _V3_EXISTS, reason="atlas_v3.jsonl not frozen yet (created at V3)")


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
    assert atlas.validate_corpus(entries) == {}, "v3 passes the same gates as v1"


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
