"""AGENTS.md — a page that is two thirds authored and one third compiled, tested at both seams.

THE FAILURES THIS GUARDS.

  1. THE PAGE COPYING A LIST THAT HAS A HOME. §2 reports how many rows are reserved, not which. The
     identities are not secret — Q6 publishes them, and a reserved row has no frames, so there is nothing
     measured about it to leak. The rule is about duplication: a sixteen-row list that moves every batch
     belongs in one place, and a compiled guide is not it.

  2. A COMPILED CLAIM THAT TRACES TO NOTHING. The whole argument for compiling §2 is that every name and
     number in it is read from the machinery. A hand-maintained line that crept in would read exactly
     like a compiled one and would decay silently.

  3. THE HAND-EDIT. A guide someone edits directly stops being derived, and the edit survives until
     someone notices — which for a rule surface may be never.
"""
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from foundry import cli                              # noqa: E402
from foundry.catalog import agents_page as AP        # noqa: E402
from foundry.catalog import freshness as F           # noqa: E402
from foundry.catalog import maptrail as M            # noqa: E402
from foundry.catalog import reservation as RES       # noqa: E402

LAT = ROOT / "foundry" / "results" / "lattice"
REPO = ROOT.parent
PAGE = REPO / "AGENTS.md"
LEDGER = LAT / "observatory_reservation.jsonl"


# ── 1. the frontier is a count, never a list ────────────────────────────────────────────────────────

def test_the_page_never_names_a_reserved_row():
    """A DUPLICATION GUARD, NOT A SECRECY GUARD — and the distinction is worth stating precisely.

    The reserved identities are NOT secret: `QUERIES.md` Q6 publishes them, correctly, because a reserved
    row is declared and uncaptured and therefore has nothing measured about it to leak. What this test
    enforces is narrower: a sixteen-row list that changes every batch and has a canonical home one query
    away must not be copied into a compiled guide, because a second copy of a moving fact is the exact
    failure the page exists to avoid."""
    text = PAGE.read_text()
    leaked = sorted(r for r in RES.reserved_rows(LEDGER) if r in text)
    assert not leaked, f"AGENTS.md names reserved rows: {leaked}"


def test_the_page_does_report_the_count():
    """The other half — withholding the names is only defensible if the count is stated, or a reader
    cannot tell the frontier exists at all."""
    n = len(RES.reserved_rows(LEDGER))
    assert f"**{n} rows are reserved.**" in PAGE.read_text()


def test_the_generator_reads_the_ledger_but_emits_only_a_number(tmp_path):
    """Belt and braces against a refactor that starts formatting the list it already has in hand — the
    natural way this decays is someone "improving" the section by printing what the ledger returned."""
    src = (ROOT / "foundry" / "catalog" / "agents_page.py").read_text()
    body = src.split("# ── the page", 1)[1]
    assert "reserved_rows" in src, "the generator no longer consults the ledger at all"
    assert "n_reserved = len(" in src, "the ledger result must be reduced to a length immediately"
    assert not re.search(r"for\s+\w+\s+in\s+.*reserved_rows", body), \
        "the generator iterates the reserved rows — one f-string away from printing them"


# ── 2. every compiled claim traces to a source ──────────────────────────────────────────────────────

def test_every_verb_in_the_table_exists_in_the_cli():
    rows = re.findall(r"^\| `foundry ([a-z-]+)` \|", PAGE.read_text(), re.M)
    assert rows, "the verb table vanished"
    known = set(cli.VERBS) | set(cli.DELEGATED)
    assert set(rows) == known, f"table/CLI disagree: {set(rows) ^ known}"


def test_every_screen_in_the_table_exists_in_the_screens_module():
    # `F2-foreclosed` carries a capital and a digit — a lowercase-only pattern silently drops it and
    # then reports the page as drifted, which is a test failing the page for the test's own defect.
    listed = re.findall(r"^\| `([\w-]+)` \| (?:HELD|REJECTED)", PAGE.read_text(), re.M)
    actual = [r for r, _ in AP.screen_rules(ROOT / "foundry" / "helm" / "screens.py")]
    assert listed == actual, f"screen table drifted: {listed} vs {actual}"


def test_a_screen_carrying_two_dispositions_reports_both():
    """`null-missing` HOLDS a bet with no typed null and REJECTS one consuming a seal-prohibited
    descriptor. Reporting only the first is a compiled claim that does not trace to its source."""
    rules = dict(AP.screen_rules(ROOT / "foundry" / "helm" / "screens.py"))
    assert set(rules["null-missing"]) == {"HELD", "REJECTED"}
    assert "| `null-missing` | HELD / REJECTED |" in PAGE.read_text()


def test_every_gate_in_the_list_exists_in_verify():
    from hardmap import verify
    text = PAGE.read_text()
    for name, _fn in verify.CHECKS:
        assert f"- {name}" in text, f"gate missing from the page: {name}"
    assert f"runs {len(verify.CHECKS)} checks" in text


def test_open_items_match_the_trail():
    items = M.open_items(LAT / "maptrail.jsonl")
    text = PAGE.read_text()
    for it in items:
        assert f"`{it['opens']}`" in text, f"open item missing: {it['opens']}"
    assert f"{len(items)} items, in declared order" in text


def test_the_delegated_count_on_the_page_matches_the_cli():
    n = len(cli.DELEGATED)
    assert f"{len(cli.VERBS)} lifted, {n} delegated" in PAGE.read_text()


# ── 3. compiled means compiled ──────────────────────────────────────────────────────────────────────

def test_the_page_regenerates_byte_identically():
    before = PAGE.read_bytes()
    assert cli.main(["agents"]) == 0
    assert PAGE.read_bytes() == before, "AGENTS.md is not reproducible from its sources"


def test_a_hand_edit_is_reverted_by_the_next_compile():
    """The guard's actual semantics: editing an AUTHORED SOURCE and regenerating is legitimate; editing
    the compiled page is not, and does not survive."""
    before = PAGE.read_bytes()
    PAGE.write_text(PAGE.read_text() + "\n\nsomeone added a rule here by hand.\n")
    assert PAGE.read_bytes() != before
    cli.main(["agents"])
    assert PAGE.read_bytes() == before, "a hand-edit survived a recompile"


def test_line_one_states_the_pages_own_epistemics():
    """A reader who cannot tell which section is compiled will trust the wrong one."""
    head = PAGE.read_text().split("---", 1)[0]
    assert "COMPILED" in head and "the machinery is right and the build is broken" in head
    assert "do not hand-edit" in head.lower()


def test_the_authored_sections_come_from_their_own_files():
    """§1 and §3 are authored FILES, not prose in the generator — so a constitution changed by owner
    ruling is edited in a document rather than in a refactor."""
    text = PAGE.read_text()
    for name in AP.AUTHORED:
        src = (REPO / "docs" / "agents" / name).read_text().strip()
        assert src in text, f"{name} is not the source of its section"
    assert "## §1 — The constitution *(authored)*" in text
    assert "## §3 — What to escalate *(authored)*" in text


def test_the_front_door_rule_is_present():
    """The load-bearing law for an agent reading this: act through verbs, never write artifacts."""
    text = PAGE.read_text()
    assert "front-door rule" in text.lower()
    assert "a write that\nescaped its own provenance" in text or \
           "escaped its own provenance" in text


def test_the_page_declares_its_sources_and_is_currently_fresh():
    st = F.check("AGENTS.md", LAT)
    assert not st["unknown"], "AGENTS.md records no sources"
    assert not st["stale"], f"AGENTS.md is stale: {st['diff']}"
    assert "foundry/foundry/helm/screens.py" in st["recorded"], \
        "the screens module is a source of this page; if it moves, the page is stale"


def test_per_project_guides_are_linked_not_absorbed():
    """The four research AGENTS.md files keep their invariants. This page points at them and does not
    restate them — a restated invariant is a second home for a rule."""
    text = PAGE.read_text()
    for p in ("foundry", "eightfold", "proof-census", "desert-map"):
        assert f"{p}/AGENTS.md" in text
        assert (REPO / p / "AGENTS.md").exists()
