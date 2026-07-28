"""The write surface — tested where it could stop being separate, or stop enforcing.

THREE FAILURES THIS GUARDS.

  1. THE SPLIT COLLAPSING. If a write verb ever becomes reachable from the published `hardmap` binary, a
     stranger reproducing the paper can advance the frontier — and the frontier is the blindness
     mechanism the program's claims rest on. Kill 2 is an impossibility here only for as long as the
     verb is absent from what ships.

  2. THE DELEGATED TABLE GROWING. Delegation is a transitional state with a cost: the dispatcher cannot
     enforce event-time emission on a script it merely calls. A count that can grow is not a transition,
     it is a habit.

  3. STALENESS BECOMING SURVIVABLE. `wave` against a stale db is the case the freshness law exists for,
     and `wave` is delegated — so the check has to fire at the boundary or it fires nowhere that matters.
"""
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from foundry import cli                          # noqa: E402
from foundry.catalog import freshness as F       # noqa: E402

LAT = ROOT / "foundry" / "results" / "lattice"


# ── 1. the two binaries stay two ────────────────────────────────────────────────────────────────────

def test_the_published_distribution_ships_only_the_read_surface():
    """`pip install hardmap` must give repro and verify, never a verb that can capture a reserved row."""
    txt = (ROOT.parent / "pyproject.toml").read_text()
    block = txt.split("[project.scripts]", 1)[1].split("[", 1)[0]
    entries = [l.split("=")[0].strip() for l in block.strip().splitlines() if "=" in l]
    assert entries == ["hardmap"], f"the write surface leaked into the published scripts: {entries}"


def test_the_read_surface_exposes_no_write_verb():
    """Belt and braces: even if packaging changed, `hardmap`'s own parser must not grow a writer."""
    sys.path.insert(0, str(ROOT.parent / "hardmap"))
    from hardmap.cli import build_parser
    actions = [a for a in build_parser()._actions if hasattr(a, "choices") and a.choices]
    verbs = {v for a in actions for v in (a.choices or {})}
    forbidden = set(cli.VERBS) | set(cli.DELEGATED)
    assert not (verbs & forbidden), f"hardmap exposes write verbs: {sorted(verbs & forbidden)}"


# ── 2. delegation is a debt, not a habit ────────────────────────────────────────────────────────────

DELEGATED_CEILING = 6   # only ever lower this


def test_the_delegated_table_only_shrinks():
    """Lower the ceiling when you lift one. Never raise it — a new dev script reachable only by path is
    the state the single dispatch surface exists to end."""
    assert len(cli.DELEGATED) <= DELEGATED_CEILING, (
        f"{len(cli.DELEGATED)} delegated verbs against a ceiling of {DELEGATED_CEILING}")


def test_every_delegated_verb_names_a_module_that_exists():
    for name, d in cli.DELEGATED.items():
        assert (ROOT / "dev" / f"{d['mod']}.py").exists(), f"{name} -> dev/{d['mod']}.py is missing"


def test_every_verb_is_reachable_from_the_parser():
    """A verb in the table but not in the parser is a verb nobody can type."""
    actions = [a for a in cli.build_parser()._actions if hasattr(a, "choices") and a.choices]
    reachable = {v for a in actions for v in (a.choices or {})}
    for name in set(cli.VERBS) | set(cli.DELEGATED):
        assert name in reachable, f"{name} is declared but unreachable"


# ── 3. the inherited checks actually fire ───────────────────────────────────────────────────────────

def test_freshness_is_declared_by_the_verb_not_coded_into_it():
    """The contract is a declaration. If `consumes` vanished, every verb would run against anything."""
    assert cli.DELEGATED["wave"]["consumes"] == ("observatory.db",)
    assert cli.VERBS["next"]["consumes"] == ("observatory.db",)
    assert cli.VERBS["db"].get("consumes", ()) == (), "a producer must not consume what it produces"


def test_a_stale_consumer_refuses_and_says_what_to_run(monkeypatch, capsys):
    """The refusal is an answer: exit 2, no traceback, and the remedy named in the message."""
    monkeypatch.setattr(F, "require", lambda a, lat: (_ for _ in ()).throw(
        RuntimeError("observatory.db is STALE — 1 source(s) changed.\n  Rebuild it with:  foundry db compile")))
    rc = cli.main(["wave"])
    assert rc == 2
    err = capsys.readouterr().err
    assert "REFUSED" in err and "foundry db compile" in err


def test_the_compiled_artifacts_are_currently_fresh():
    """The repository's own state. If this fails, something was written without its consumer rebuilt."""
    for name in F.REGISTRY:
        st = F.check(name, LAT)
        assert not st["unknown"], f"{name} records no sources"
        assert not st["stale"], f"{name} is stale: {st['diff']}  — run: {st['rebuild']}"


def test_every_registered_artifacts_declared_shape_covers_what_it_records():
    """THE NEGATIVE-SPACE GUARD. Discovery is what catches a source the artifact never saw; if the
    declared globs drift from what the compiler actually consumes, a new batch would land unnoticed and
    the freshness law would pass while being blind."""
    for name in F.REGISTRY:
        recorded = set(F.REGISTRY[name]["recorded"](LAT))
        if not recorded:
            continue
        missed = recorded - F.discover(name, LAT)
        assert not missed, f"{name}: recorded sources no declared glob would find: {sorted(missed)}"


# ── the CLI runs end to end ─────────────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("argv", [["audit"], ["fresh"], ["census", "list"], ["migrate", "status"],
                                  ["frontier"], ["open"], ["guards"], ["trail", "--limit", "3"]])
def test_read_only_verbs_run_clean(argv):
    assert cli.main(argv) == 0


def test_census_verify_reports_the_shape_without_rewriting(capsys):
    before = {p: p.read_bytes() for p in LAT.glob("observatory_batch*_census.json")}
    assert cli.main(["census", "verify", "--batch", "10"]) == 0
    assert all(p.read_bytes() == b for p, b in before.items()), "verify rewrote a census"
    assert "re-derives identically except: ['schema']" in capsys.readouterr().out


def test_next_regenerates_byte_identically_through_the_cli():
    """The determinism law, now including the source-hash block — a hash moves only when its source does."""
    page = ROOT.parent / "NEXT.md"
    before = page.read_bytes()
    assert cli.main(["next"]) == 0
    assert page.read_bytes() == before, "NEXT.md is not reproducible from its sources"


def test_next_records_its_sources():
    """The page claimed in prose to be a pure function of its sources; now the claim is checkable."""
    rec = F._next_recorded(LAT)
    assert set(rec) == set(__import__("foundry.catalog.next_page", fromlist=["x"]).SOURCES)


def test_the_original_flags_still_work():
    """`foundry --validate-toy` is documented in foundry/README.md. Consolidation is not a licence to
    break the surface someone already uses."""
    r = subprocess.run([sys.executable, "-m", "foundry.cli", "--validate-toy"],
                       cwd=ROOT, capture_output=True, text=True,
                       env={**__import__("os").environ,
                            "PYTHONPATH": f"{ROOT}:{ROOT.parent / 'eightfold'}"})
    assert r.returncode == 0, r.stderr[-500:]
    assert "validate clean under FOUNDRY_SPEC" in r.stdout


def test_the_operator_path_does_declare_the_write_surface():
    """The other half of the split: an operator working from a checkout must actually get `foundry`.
    A split that only removes is a split that leaves nobody able to run the pipeline."""
    txt = (ROOT / "pyproject.toml").read_text()
    assert 'foundry = "foundry.cli:main"' in txt.split("[project.scripts]", 1)[1]


def test_the_distribution_does_not_ship_dev():
    """Delegated verbs are repo-only BECAUSE dev/ is excluded from the wheel. If that exclusion were
    dropped, the write surface would start travelling with the published package."""
    setup_py = (ROOT.parent / "setup.py").read_text()
    assert '"dev", "dev.*"' in setup_py, "dev/ is no longer excluded from the distribution"


def test_a_repo_only_verb_explains_itself_when_dev_is_absent(monkeypatch):
    """What a pip user hits. It is the design working, so it should read like a design, not a crash."""
    monkeypatch.setitem(cli.DELEGATED, "wave",
                        {"mod": "a_module_that_does_not_exist", "consumes": (), "why": "x"})
    with pytest.raises(RuntimeError, match="repo-only verb"):
        cli._delegate("wave")


# ── the documentation cannot drift from the surface it documents ────────────────────────────────────

def _documented_verbs():
    """Every `foundry <verb>` the READMEs advertise, from their fenced bash blocks."""
    out = set()
    for md in (ROOT / "README.md", ROOT.parent / "README.md"):
        for block in md.read_text().split("```bash")[1:]:
            for line in block.split("```")[0].splitlines():
                line = line.split("#")[0].strip()
                if line.startswith("foundry ") and not line.startswith("foundry --"):
                    out.add(line.split()[1])
    return out


def test_every_verb_the_readmes_advertise_actually_exists():
    """A README promising a verb that was renamed or dropped is worse than one that says nothing —
    it sends a reader to a command that fails, and the failure looks like their mistake."""
    documented = _documented_verbs()
    assert documented, "no foundry commands found in either README — the parser above stopped working"
    known = set(cli.VERBS) | set(cli.DELEGATED)
    assert documented <= known, f"the READMEs advertise verbs that do not exist: {sorted(documented - known)}"


def test_the_batch_declaration_convention_has_a_home():
    """`foundry census declare --declaration batches/<N>.json` is advertised in both READMEs and in the
    argparse help. The directory and its convention must exist, or the example sends a reader nowhere."""
    conv = ROOT / "batches" / "README.md"
    assert conv.exists(), "the declaration convention is documented in three places and lives in none"
    assert "census = declaration + reservation + status" in conv.read_text()
