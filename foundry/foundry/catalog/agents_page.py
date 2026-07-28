"""AGENTS.md — the agent guide, two thirds authored and one third compiled.

THE SHAPE, AND WHY IT IS THIS SHAPE. Three sections with different epistemic status, and the file says so
on line one because a reader who cannot tell which is which will trust the wrong part:

  §1  AUTHORED   the constitution — judgment laws, changed only by owner ruling
  §2  COMPILED   the current rule surface, generated from the machinery it describes
  §3  AUTHORED   the escalation table — what an agent stops and asks on

THE AUTHORED SECTIONS ARE AUTHORED FILES, not prose embedded here. `docs/agents/01-constitution.md` and
`docs/agents/03-escalation.md` are the homes; this module assembles. That keeps a constitution changed by
owner ruling in a file a person edits, instead of buried in a generator where changing it looks like a
refactor. It also gives the hand-edit guard exactly the right semantics: editing an authored source and
regenerating is legitimate, editing AGENTS.md directly is reverted by the next compile and fails the test.

WHY §2 IS COMPILED AND NOT WRITTEN DOWN. A rule surface described by hand is a claim about the machinery
that decays the moment either moves, and it decays SILENTLY — the document keeps reading correctly. Every
number and name in §2 is read from the thing it describes, so the page cannot drift; it can only be
stale, and `foundry fresh` says when.

THE FRONTIER COUNT IS A COUNT AND NEVER A LIST. §2 reports how many rows are reserved and never which.
The page is an agent-facing document and the reserved rows are the blindness mechanism: a guide that
named them would hand over the one thing the frontier exists to withhold. This is the single hardest
constraint in the module and the easiest to lose in a refactor, so it has its own test.
"""
from __future__ import annotations

import ast
import json
from pathlib import Path

from . import freshness as F
from . import maptrail as M
from . import migrations as MG
from . import reservation as RES

AUTHORED = ("01-constitution.md", "03-escalation.md")


# ── reading the machinery ───────────────────────────────────────────────────────────────────────────

def screen_rules(screens_py: Path) -> list:
    """The screens, by name, read off `screen()`'s own return sites.

    AST rather than a grep or a hand-list: a screen added tomorrow appears here without anyone
    remembering to add it, which is the only way a compiled surface stays true.

    ONE RULE CAN CARRY MORE THAN ONE DISPOSITION, and reporting only the first is a compiled claim that
    does not trace to its source. `null-missing` is the case: it HOLDS a candidate whose bet has no typed
    null yet, and REJECTS one that consumes a seal-prohibited descriptor. Those are different verdicts
    about different situations under one rule name, and the page has to say both or it is describing a
    screen that does not exist.
    """
    fn = [n for n in ast.parse(screens_py.read_text()).body
          if isinstance(n, ast.FunctionDef) and n.name == "screen"][0]
    order, dispositions = [], {}
    for node in ast.walk(fn):
        if isinstance(node, ast.Return) and isinstance(node.value, ast.Tuple):
            el = node.value.elts
            if len(el) >= 2 and all(isinstance(x, ast.Constant) for x in el[:2]):
                disp, rule = el[0].value, el[1].value
                if not rule:
                    continue
                if rule not in dispositions:
                    order.append(rule)
                    dispositions[rule] = []
                if disp not in dispositions[rule]:
                    dispositions[rule].append(disp)
    return [(r, dispositions[r]) for r in order]


def gate_names() -> list:
    """The coherence gates, from `hardmap.verify`'s own declared registry."""
    try:
        from hardmap import verify
    except ImportError:
        return []
    return [name for name, _fn in verify.CHECKS]


def verb_table(cli_mod) -> list:
    """Every verb, with what it refuses on. `consumes` IS the refusal — a verb declares what it reads
    and the dispatch refuses it against anything stale."""
    rows = []
    for name, spec in sorted(cli_mod.VERBS.items()):
        rows.append((name, "lifted", spec.get("consumes", ()), spec["help"]))
    for name, spec in sorted(cli_mod.DELEGATED.items()):
        rows.append((name, "delegated", spec["consumes"], spec["why"]))
    return rows


def screen_activity(db: Path) -> dict:
    """How often each rule has actually fired. Absent db is not an error — the page still compiles."""
    if not db.exists():
        return {}
    import sqlite3
    con = sqlite3.connect(db)
    try:
        return {(r, d): n for r, d, n in con.execute(
            "SELECT screen_rule, screen_disposition, COUNT(*) FROM candidates "
            "WHERE screen_rule IS NOT NULL GROUP BY 1, 2")}
    finally:
        con.close()


# ── the page ────────────────────────────────────────────────────────────────────────────────────────

def compile_page(lat: Path, repo: Path, out: Path, cli_mod) -> dict:
    trail = lat / "maptrail.jsonl"
    authored = {n: (repo / "docs" / "agents" / n).read_text().strip() for n in AUTHORED}
    verbs = verb_table(cli_mod)
    rules = screen_rules(repo / "foundry" / "foundry" / "helm" / "screens.py")
    gates = gate_names()
    fired = screen_activity(lat / "observatory.db")
    n_reserved = len(RES.reserved_rows(lat / "observatory_reservation.jsonl"))
    items = M.open_items(trail)
    mig = MG.status(trail)

    L = ["# AGENTS.md — how to work in this repository", "",
         "**§2 of this file is COMPILED from the machinery it describes. If it disagrees with the "
         "machinery, the machinery is right and the build is broken.** §1 and §3 are authored and change "
         "only by owner ruling; their sources are [`docs/agents/`](docs/agents/). The whole file is "
         "generated by `foundry agents` — **do not hand-edit it**, because the next compile reverts you "
         "and the guard fails.", "",
         "Per-project research invariants live beside their code and are not repeated here: "
         "[`foundry/AGENTS.md`](foundry/AGENTS.md), [`eightfold/AGENTS.md`](eightfold/AGENTS.md), "
         "[`proof-census/AGENTS.md`](proof-census/AGENTS.md), "
         "[`desert-map/AGENTS.md`](desert-map/AGENTS.md).", "",
         "---", "", "## §1 — The constitution *(authored)*", "", authored["01-constitution.md"], "",
         "---", "", "## §2 — The current rule surface *(compiled)*", "",
         "Everything below is read from the machinery at build time. Nothing here is a description "
         "someone maintained by hand.", ""]

    # verbs
    L += ["### Verbs, and what each refuses on", "",
          "Act through these. A verb's `consumes` column **is** its refusal: the dispatch will not run "
          "it against a compiled artifact whose sources have moved. A producer consumes nothing, which "
          "is why no verb needs an exemption.", "",
          "| verb | | refuses on stale | what it does |", "|---|---|---|---|"]
    for name, kind, consumes, help_text in verbs:
        c = ", ".join(f"`{x}`" for x in consumes) or "—"
        L.append(f"| `foundry {name}` | {kind} | {c} | {help_text} |")
    n_deleg = sum(1 for _, k, _, _ in verbs if k == "delegated")
    L += ["", f"**{len(verbs) - n_deleg} lifted, {n_deleg} delegated.** Delegated verbs still hold their "
          f"logic in `dev/`; freshness reaches them at the boundary but event-time emission cannot, "
          f"since emitting on a script's behalf from outside is the reconstruction the trail exists to "
          f"prevent. That count only goes down.", ""]

    # screens
    L += ["### Screens — the mechanical dispositions", "",
          "A candidate reaching the slate has passed all of these, in order. `fired` counts how many "
          "times each has actually disposed of a candidate, per disposition, across every wave so far. "
          "One rule can carry more than one verdict: `null-missing` HOLDS a bet with no typed null yet "
          "and REJECTS one consuming a seal-prohibited descriptor.", "",
          "| screen | disposition(s) | fired |", "|---|---|---|"]
    for rule, disps in rules:
        cells = " · ".join(f"{d} {fired.get((rule, d), 0)}" for d in disps)
        L.append(f"| `{rule}` | {' / '.join(disps)} | {cells} |")
    L += ["", f"**{len(rules)} screens.** A screen added to `helm/screens.py` appears here on the next "
          f"compile without anyone remembering to add it.", ""]

    # gates
    L += ["### Coherence gates", "",
          f"`hardmap verify` runs {len(gates)} checks. All must pass before anything is committed.", "",
          *[f"- {g}" for g in gates], ""]

    # frontier — COUNT ONLY
    L += ["### Frontier", "",
          f"**{n_reserved} rows are reserved.** They are declared and **not captured** — no frames "
          f"exist for them, which is what lets predictions be hashed before their frames do.", "",
          "*This page reports the count and never the names.* An agent-facing document that listed the "
          "reserved rows would hand over the one thing the frontier exists to withhold. If you need to "
          "know whether a specific row is reserved, the guards already check it — build the batch and "
          "let them answer.", ""]

    # migrations
    L += ["### One-time history", "",
          "Not verbs. Named, ordered, applied once, checksummed.", "",
          "| migration | state |", "|---|---|"]
    for s in mig:
        L.append(f"| `{s['name']}` | {s['state']} |")
    L.append("")

    # open work
    L += ["### Open work", "",
          f"{len(items)} items, in declared order — compiled from the same trail as "
          f"[`NEXT.md`](NEXT.md), which carries the full statement of each.", ""]
    for it in items:
        L.append(f"{it.get('sequence')}. **{it.get('title')}** — `{it['opens']}`")
    L += ["", "---", "", "## §3 — What to escalate *(authored)*", "", authored["03-escalation.md"], ""]

    srcs = {n: F.sha(lat / n) for n in ("maptrail.jsonl", "observatory_reservation.jsonl",
                                        "observatory.db") if (lat / n).exists()}
    srcs.update({f"docs/agents/{n}": F.sha(repo / "docs" / "agents" / n) for n in AUTHORED})
    srcs["foundry/foundry/helm/screens.py"] = F.sha(repo / "foundry" / "foundry" / "helm" / "screens.py")
    L += [f"{F.SOURCES_MARKER} {json.dumps(srcs, sort_keys=True)} -->", ""]

    out.write_text("\n".join(L) + "\n")
    return {"verbs": len(verbs), "delegated": n_deleg, "screens": len(rules), "gates": len(gates),
            "reserved": n_reserved, "open_items": len(items), "migrations": len(mig),
            "sources": len(srcs)}
