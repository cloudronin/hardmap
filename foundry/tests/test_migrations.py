"""Migrations are history with a checksum — tested where they could stop being either.

THE FAILURE THIS GUARDS is a migration becoming a verb. A one-time pass that can be re-run is not
history, it is a procedure with an unenforced convention attached; `void_prereg_v34` re-run is a second
void of something already void. The second failure is subtler: a migration whose source changes after it
was applied leaves an applied-record describing something that no longer exists.
"""
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from foundry.catalog import maptrail as M     # noqa: E402
from foundry.catalog import migrations as MG  # noqa: E402

TRAIL = ROOT / "foundry" / "results" / "lattice" / "maptrail.jsonl"


def test_a_migration_applies_once_and_then_reports_itself_applied(tmp_path):
    t = tmp_path / "t.jsonl"
    first = MG.run(t, {"trail": t})
    assert all(r["state"] == "applied" for r in first)
    again = MG.run(t, {"trail": t})
    assert all(r["state"] == "already applied" for r in again), "a migration re-ran"


def test_the_applied_ledger_is_the_maptrail_replayed_not_a_second_file(tmp_path):
    """No separate applied-flag file. Replay is the state, so there is nothing mutable to drift."""
    t = tmp_path / "t.jsonl"
    MG.run(t, {"trail": t})
    assert sorted(p.name for p in tmp_path.iterdir()) == ["t.jsonl"]
    assert set(MG.applied(t)) == {m.name for m in MG.REGISTRY}


def test_status_reports_pending_before_and_applied_after(tmp_path):
    t = tmp_path / "t.jsonl"
    assert {s["state"] for s in MG.status(t)} == {"pending"}
    MG.run(t, {"trail": t})
    assert {s["state"] for s in MG.status(t)} == {"applied"}


def test_a_migration_whose_source_changed_after_application_is_drift(tmp_path):
    """The checksum is what makes an applied record history rather than a claim."""
    t = tmp_path / "t.jsonl"
    MG.run(t, {"trail": t})
    recs = [json.loads(x) for x in t.read_text().splitlines()]
    for r in recs:
        if r.get("migration"):
            r["source_sha256"] = "0" * 16          # as if the source had been edited since
    t.write_text("".join(json.dumps(r) + "\n" for r in recs))
    assert [s["state"] for s in MG.status(t) if s["name"].startswith("0001")] == ["DRIFTED"]
    with pytest.raises(RuntimeError, match="MIGRATION DRIFT"):
        MG.assert_no_drift(t)
    with pytest.raises(RuntimeError, match="MIGRATION DRIFT"):
        MG.run(t, {"trail": t})


def test_names_are_unique():
    """The leading number is the order. Two migrations sharing a name would make 'applied' ambiguous."""
    names = [m.name for m in MG.REGISTRY]
    assert len(names) == len(set(names)) and names == sorted(names)


def test_registering_a_duplicate_name_is_refused():
    with pytest.raises(ValueError, match="already registered"):
        MG.register(MG.REGISTRY[0].name, "x")(lambda paths: {})


# ── migration 0001, the drift retro-label ───────────────────────────────────────────────────────────

def test_0001_rewrites_no_artifact(tmp_path):
    """Retro-label, never re-emit. The migration touches the trail and nothing else — if it ever wrote
    a census, it would be editing a pre-reading declaration after its readings exist."""
    t = tmp_path / "t.jsonl"
    before = {p: p.read_bytes() for p in
              (ROOT / "foundry" / "results" / "lattice").glob("observatory_batch*_census.json")}
    out = MG.run(t, {"trail": t})
    assert out[0]["summary"]["artifacts_rewritten"] == 0
    assert all(p.read_bytes() == b for p, b in before.items()), "a historical census was rewritten"


def test_0001_labels_the_three_historical_shapes_as_reconstructed(tmp_path):
    """History written late is fine; history written late and presented as contemporaneous is not."""
    t = tmp_path / "t.jsonl"
    MG.run(t, {"trail": t})
    vers = {r["key"]: r for r in M.read(t) if r["event"] == "version"}
    assert set(vers) == {f"version:batch-census-v1-{x}" for x in "abc"} | {"version:batch-census-v2"}
    assert all(vers[f"version:batch-census-v1-{x}"]["reconstructed"] for x in "abc")
    assert not vers["version:batch-census-v2"]["reconstructed"], \
        "v2 is being declared now, by the machinery that emits it — not reconstructed"


def test_0001_names_the_actual_transitions():
    """The two silent changes, on the record: the b3->b4 key rename and the b4->b5 field addition."""
    vers = {r["key"]: r for r in M.read(TRAIL) if r["event"] == "version"}
    b = vers["version:batch-census-v1-b"]
    assert "flagged_for_ruling" in b["old_rule"] and "carried_forward" in b["new_rule"]
    assert b["batches"] == [4]
    c = vers["version:batch-census-v1-c"]
    assert "capture_mode" in c["new_rule"] and c["batches"] == [5, 6, 7, 8, 9, 10]


def test_0001_is_applied_to_the_live_trail():
    assert MG.applied(TRAIL).get("0001-census-schema-history"), "migration 0001 has not been applied"
    MG.assert_no_drift(TRAIL)
