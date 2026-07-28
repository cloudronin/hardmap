"""NEXT.md is a DERIVED view — tested where it could quietly stop being one.

THE FAILURE THIS GUARDS is not a wrong entry. It is the page becoming a FOURTH HOME: someone adds a note
here that lives nowhere else, and the compiled front page silently turns into the place rulings hide —
which is the exact failure it was built to prevent.
"""
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "dev"))
from foundry.catalog import maptrail as M  # noqa: E402

LAT = ROOT / "foundry" / "results" / "lattice"
TRAIL = LAT / "maptrail.jsonl"
NEXT = ROOT.parent / "NEXT.md"


def test_openness_is_replayed_not_stored(tmp_path):
    """Discharge must be a NEW record, never an edit — replay is the state, so nothing is mutable."""
    t = tmp_path / "mt.jsonl"
    M.open_item(t, "alpha", "A", "because", sequence=1)
    M.open_item(t, "beta", "B", "because", sequence=2)
    assert [x["opens"] for x in M.open_items(t)] == ["alpha", "beta"]
    M.discharge(t, "alpha", by="commit deadbeef")
    assert [x["opens"] for x in M.open_items(t)] == ["beta"]
    recs = M.read(t)
    assert len(recs) == 3, "discharge appended a record rather than editing one"
    assert recs[0]["opens"] == "alpha", "the opening record was modified"


def test_items_come_back_in_declared_sequence():
    """Order is declared by the pass that opens the item — the `supersedes` principle. Nothing here
    infers an ordering."""
    seqs = [x.get("sequence") for x in M.open_items(TRAIL)]
    assert seqs == sorted(seqs)


def test_the_page_regenerates_byte_identically():
    """A derived view that drifts from its sources is worse than no view. Two compiles, same bytes."""
    if not NEXT.exists():
        pytest.skip("NEXT.md not built")
    before = NEXT.read_bytes()
    subprocess.run([sys.executable, str(ROOT / "dev" / "build_next.py")],
                   capture_output=True, check=True)
    assert NEXT.read_bytes() == before, "NEXT.md is not reproducible from its sources"


def test_every_open_item_on_the_page_exists_in_the_trail():
    """THE NEGATIVE-SPACE TEST. An entry with no maptrail record behind it means someone hand-edited
    the page, and the compiled front page has become a place where work lives nowhere else."""
    if not NEXT.exists():
        pytest.skip("NEXT.md not built")
    keys = {x["opens"] for x in M.open_items(TRAIL)}
    page = NEXT.read_text()
    import re
    on_page = set(re.findall(r"^- key: `([^`]+)`", page, re.M))
    assert on_page == keys, f"page and trail disagree: page-only {on_page - keys}, trail-only {keys - on_page}"


def test_the_page_declares_itself_derived():
    """A reader who does not know the convention must learn it from the artifact, not from a commit."""
    if not NEXT.exists():
        pytest.skip("NEXT.md not built")
    head = NEXT.read_text()[:800]
    assert "DERIVED" in head and "Do not edit" in head
    assert "the sources are right" in NEXT.read_text()
