"""The typing chain — walked from what the artifacts declare, never inferred.

THE DEFECT THIS CLOSES. Four passes typed the same 345 rows on the reach_class axis, and the loader
consumed the first two. Fifty-one rows in the database answered the PRE-adjudication question: their
`reach_class` was the answer to a question two later passes had already re-asked and re-answered. The
shape-discovery machinery was never wrong — only the ordering signal was, and only because there wasn't
one.

PRECEDENCE TRAVELS IN THE ARTIFACT. Each pass declares what it directly supersedes; this module walks
that chain and nothing else. It does not look at filenames, mtimes, directory order, or the maptrail.
That last exclusion is specific and expensive: an earlier attempt inferred precedence from the latest
trail record MENTIONING each artifact, and since the reach census is mentioned by later errata *about*
it, the census scored newest, overwrote all three adjudications, and invented an UNTYPED class for 105
rows. MENTION IS NOT AUTHORSHIP.

`written_at` IS A BACKSTOP, NOT A SORT KEY. The chain fixes the order. The dates only check it: a pass
claiming to supersede something written after it is stating a contradiction, and a contradiction in the
precedence declaration is a build failure rather than a tie to break. Sorting by date instead would
reintroduce exactly the inference the ruling removed.

ONE ROW, ONE CURRENT TYPING PER AXIS. Artifacts on different axes coexist — a region formulation and a
reach class are answers to different questions and neither supersedes the other. Each artifact declares
its `typing_axis`, and chains are walked per axis.
"""
from __future__ import annotations

import json
from pathlib import Path

TYPING_ARTIFACTS = (
    "observatory_reach_census.json",
    "observatory_untyped_adjudication.json",
    "reach_subset_readjudication.json",
    "unmatched_adjudication.json",
    "region_formulation_audit.json",
)


def load_declarations(lat: Path) -> list:
    """Every typing artifact present, with what it declares about its own precedence."""
    out = []
    for name in TYPING_ARTIFACTS:
        p = lat / name
        if not p.exists():
            continue
        d = json.loads(p.read_text())
        out.append({
            "name": name, "axis": d.get("typing_axis"), "written_at": d.get("written_at"),
            "supersedes": d.get("supersedes"), "consumed": d.get("consumed_by_loader"),
            "not_consumed_because": d.get("not_consumed_because"),
            "row_typing": d.get("row_typing"), "doc": d,
        })
    return out


def assert_declared(decls: list) -> None:
    """Every typing artifact must state its axis, its date, and what it supersedes — including the base,
    whose `supersedes: []` is a claim ('nothing came before me') and not an omission. A missing field is
    the ambiguity this whole module exists to remove, so it fails loudly rather than defaulting."""
    for d in decls:
        missing = [k for k in ("axis", "written_at", "supersedes") if d[k] is None]
        if missing:
            raise RuntimeError(
                f"UNDECLARED TYPING ARTIFACT — {d['name']} does not state {missing}. Precedence travels "
                f"IN the artifact; an artifact that does not declare it cannot be ordered, and guessing "
                f"is the failure mode this replaced.")


def chain_for(decls: list, axis: str) -> list:
    """The artifacts on one axis, oldest first, ordered by the declared links alone.

    Raises on a cycle, a fork, a dangling reference, or a date contradiction — every one of which means
    the declarations disagree with each other, and none of which is safe to resolve by picking.
    """
    on_axis = [d for d in decls if d["axis"] == axis]
    if not on_axis:
        return []
    by_name = {d["name"]: d for d in on_axis}

    for d in on_axis:
        for s in d["supersedes"]:
            if s not in by_name:
                raise RuntimeError(
                    f"DANGLING SUPERSEDES — {d['name']} claims to supersede {s!r}, which is not a "
                    f"declared artifact on axis {axis!r}. The chain cannot be walked.")
            if d["written_at"] <= by_name[s]["written_at"]:
                raise RuntimeError(
                    f"PRECEDENCE CONTRADICTION — {d['name']} (written {d['written_at']}) claims to "
                    f"supersede {s} (written {by_name[s]['written_at']}), which is later or equal. A "
                    f"pass cannot supersede something written after it. This is the `written_at` "
                    f"backstop: the chain is the order, and the dates check it.")

    roots = [d for d in on_axis if not d["supersedes"]]
    if len(roots) != 1:
        raise RuntimeError(
            f"axis {axis!r} has {len(roots)} artifacts superseding nothing ({[r['name'] for r in roots]}). "
            f"A chain has exactly one base.")

    superseded_by = {}
    for d in on_axis:
        for s in d["supersedes"]:
            if s in superseded_by:
                raise RuntimeError(
                    f"FORKED CHAIN — {s} is superseded by both {superseded_by[s]} and {d['name']}. Two "
                    f"passes claiming to be next after the same one is an ambiguity, not an ordering.")
            superseded_by[s] = d["name"]

    order, cur = [roots[0]], roots[0]["name"]
    while cur in superseded_by:
        nxt = superseded_by[cur]
        if any(o["name"] == nxt for o in order):
            raise RuntimeError(f"CYCLE in the {axis!r} chain at {nxt}")
        order.append(by_name[nxt])
        cur = nxt

    unreached = [d["name"] for d in on_axis if d not in order]
    if unreached:
        raise RuntimeError(
            f"UNREACHED ON THE CHAIN — {unreached} declare axis {axis!r} but nothing links to them. An "
            f"artifact off the chain is one whose typing silently does not apply.")
    return order


def resolve(lat: Path, axis: str = "reach_class") -> dict:
    """problem_id -> {class, source, position}. Later links win; that is the whole rule."""
    decls = load_declarations(lat)
    assert_declared(decls)
    out = {}
    for pos, d in enumerate(chain_for(decls, axis)):
        rt = d["row_typing"]
        if not rt:
            raise RuntimeError(f"{d['name']} is on the {axis} chain but declares no `row_typing`")
        for r in d["doc"][rt["rows_at"]]:
            val = r.get(rt["class_field"])
            if val:
                out[r["problem_id"]] = {"class": val, "source": d["name"], "position": pos}
    return out


def assert_complete(lat: Path, consumed: set) -> None:
    """THE COMPLETENESS GUARD. A typing artifact in the repo but absent from the loader's consumed set
    is the artifact-produced-but-unconsumed species — exactly what put 51 rows on a stale answer — and
    it is invisible from outside, because the database looks entirely well-formed either way.

    An artifact may decline to be consumed, but only out loud: `consumed_by_loader: false` plus a
    `not_consumed_because`. That keeps "different axis, deliberately" distinguishable from "forgotten",
    which are the two states that otherwise look identical.
    """
    problems = []
    for d in load_declarations(lat):
        if d["consumed"] is None:
            problems.append(f"{d['name']}: does not declare `consumed_by_loader`")
        elif d["consumed"] and d["name"] not in consumed:
            problems.append(f"{d['name']}: declares it is consumed, but the loader never read it")
        elif not d["consumed"] and not d["not_consumed_because"]:
            problems.append(f"{d['name']}: declines consumption without saying why")
    if problems:
        raise RuntimeError("TYPING ARTIFACT NOT CONSUMED — " + "; ".join(problems))
