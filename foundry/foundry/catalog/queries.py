"""Named queries — parsed out of QUERIES.md, executed against the derived database.

ONE HOME. The markdown a reader browses is the same file the runner parses. The alternative — a python
dict of SQL beside a markdown file showing the same SQL — is two homes for one fact, and they diverge on
the first edit that touches only one.

A heading carries the slug the CLI answers to:

    ## Q7 · rejected-candidates — the rejected-candidate ledger

WHY THE OUTPUTS ARE COMPILED. Every output block in the file was pasted by hand once and then went
stale under a sentence promising it had not. `refresh()` re-executes each query against the current
database and rewrites the blocks, so a worked example is worked rather than remembered. The SQL and the
prose stay authored; nothing regenerates a human's explanation of what a join is for.
"""
from __future__ import annotations

import json
import re
import sqlite3
from pathlib import Path

HEADING = re.compile(r"^##\s+(Q\d+)\s+·\s+([a-z0-9-]+)\s+—\s+(.+)$", re.M)


def path() -> Path:
    return Path(__file__).resolve().parent.parent / "queries" / "QUERIES.md"


def parse(md: Path | None = None) -> list:
    """[{id, name, title, sql}] in file order. A heading without a slug is not a named query — the
    file's front matter and section dividers are prose and stay prose."""
    text = (md or path()).read_text()
    out = []
    for m in HEADING.finditer(text):
        qid, name, title = m.group(1), m.group(2), m.group(3).strip()
        body = text[m.end():]
        nxt = HEADING.search(body)
        if nxt:
            body = body[:nxt.start()]
        sql = re.search(r"```sql\n(.*?)```", body, re.S)
        if sql:
            out.append({"id": qid, "name": name, "title": title, "sql": sql.group(1).strip()})
    return out


def get(name: str, md: Path | None = None) -> dict:
    for q in parse(md):
        if q["name"] == name:
            return q
    raise KeyError(name)


def run(db: Path, sql: str) -> tuple:
    """(columns, rows). Read-only by construction: the connection is opened in immutable mode, so a
    query that tried to write would fail rather than mutate a derived artifact through the read
    surface."""
    con = sqlite3.connect(f"file:{db}?immutable=1", uri=True)
    try:
        cur = con.execute(sql)
        return ([d[0] for d in cur.description or []], cur.fetchall())
    finally:
        con.close()


def tabulate(cols, rows, limit: int = 40) -> str:
    """sqlite3-shell-shaped output, so what the README shows is what a reader's own shell shows."""
    if not cols:
        return "(no columns)"
    shown = rows[:limit]
    body = [[("" if v is None else str(v)) for v in r] for r in shown]
    w = [max(len(c), *(len(r[i]) for r in body)) if body else len(c) for i, c in enumerate(cols)]
    lines = ["  ".join(c.ljust(w[i]) for i, c in enumerate(cols)),
             "  ".join("-" * w[i] for i in range(len(cols)))]
    lines += ["  ".join(v.ljust(w[i]) for i, v in enumerate(r)) for r in body]
    if len(rows) > limit:
        lines.append(f"... {len(rows) - limit} more row(s)")
    return "\n".join(l.rstrip() for l in lines)


def refresh(db: Path, md: Path | None = None) -> dict:
    """Re-execute every named query and rewrite its output block. Authored prose is untouched.

    RECORDS ITS SOURCE, so the drift is detectable rather than merely fixable (ruled 2026-07-28). A
    refresh verb that exists but nothing obliges anyone to run is a rule living in a verb — the file
    went stale under a sentence promising currency precisely because nothing checked. With the database
    hash written into the file, `foundry fresh` reports it and CI fails on it, which is the
    physics-over-guards form of the same intention.
    """
    md = md or path()
    text = md.read_text()
    n = 0
    for q in parse(md):
        cols, rows = run(db, q["sql"])
        rendered = tabulate(cols, rows) if rows else \
            "(no rows — which is the point of this query: see the note below)" \
            if q["name"] == "provenance-check" else "(no rows)"
        # the output block is the first plain ``` fence after this query's ```sql fence
        start = text.index(q["sql"])
        after = text.index("```", start + len(q["sql"]))
        blk = re.compile(r"```\n(.*?)```", re.S)
        m = blk.search(text, after + 3)
        if not m:
            continue
        text = text[:m.start()] + f"```\n{rendered}\n```" + text[m.end():]
        n += 1

    from . import freshness as F
    marker = re.compile(re.escape(F.SOURCES_MARKER) + r".*?-->\n?", re.S)
    text = marker.sub("", text).rstrip("\n") + "\n\n"
    text += f"{F.SOURCES_MARKER} " + json.dumps({"observatory.db": F.sha(db)}, sort_keys=True) + " -->\n"
    md.write_text(text)
    return {"refreshed": n, "queries": len(parse(md))}
