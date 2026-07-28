#!/usr/bin/env python3
"""Execute every command the docs promise, and check the outputs they show.

THE SPECIES THIS CATCHES. A quickstart that drifts from the code is the worst kind of stale
documentation, because it fails in the reader's hands rather than ours, and it fails at the exact moment
they were deciding whether to trust anything else here. This repository has already produced the
identical defect one layer down: QUERIES.md carried hand-pasted outputs under a sentence promising they
were current, and showed a frontier of 2 against an actual 16 for weeks.

WHAT IT DOES. Extracts every ```bash block from the documents below, runs each line, and fails on a
nonzero exit. Where a document also SHOWS output, the shown text is compared against what the command
actually prints — a command that runs but prints something else is exactly as misleading as one that
crashes.

SKIPS ARE DECLARED, NEVER INFERRED. Some lines cannot run in CI and saying so is the whole discipline:
a checker that quietly ignored what it could not handle would report a green quickstart it never
executed. Every skip matches a rule in SKIP with a reason attached, and an unmatched failure is a
failure. `--list` prints what would run and what would be skipped, so the ratio is visible.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DOCS = ["README.md", "CONTRIBUTING.md", "foundry/foundry/queries/QUERIES.md", "foundry/README.md"]

# (pattern, reason). Ordered; first match wins.
SKIP = [
    (r"^pip install hardmap$",
     "installs the PUBLISHED wheel; CI verifies the working tree instead, via the editable install "
     "the harness does first. Running this would test PyPI, not this commit."),
    (r"^git clone",
     "CI already has the checkout it is testing"),
    (r"^cd ",
     "directory changes are the harness's business, not a command under test"),
    (r"[<>]\w+[>]|<you>|\byour\b",
     "contains a placeholder the reader is meant to substitute"),
    (r"^foundry census declare",
     "writes a census and reserves rows — a WRITE VERB. CI must never advance the frontier, which is "
     "the same reason the verb is repo-only in the first place."),
    (r"^foundry (wave|mint-prereg|catalog|ambient-census|bimodality-fill|reach-census|queries|agents|next|db|migrate run)",
     "write verb: mutates archive artifacts. The read surface is what a reader touches and what CI checks."),
    (r"^python -m pytest|^python3 -m pytest",
     "the test suite runs as its own CI job"),
    (r"^pip install -e",
     "the harness performs the editable install once, up front"),
    (r"^sqlite3 ",
     "needs an interactive sqlite3 binary; `hardmap query` is the checked path"),
]


def blocks(md: Path):
    return re.findall(r"```bash\n(.*?)```", md.read_text(), re.S)


def shown_output(md: Path):
    """Fenced plain blocks that IMMEDIATELY follow a ```bash block — the output a reader is shown.

    Neither group may contain a fence. A lazy `.*?` across `re.S` will happily span intervening prose
    and a ```sql block to reach the next output fence, which pairs a command with someone else's table
    and reports a drift that is entirely the checker's invention. (It did exactly that on first run.)

    SQL-block outputs in QUERIES.md are deliberately not checked here — `foundry queries refresh`
    regenerates them from the database, which is a stronger guarantee than comparing them.
    """
    text = md.read_text()
    pat = re.compile(r"```bash\n((?:(?!```).)*)```[ \t]*\n[ \t]*\n?```\n((?:(?!```).)*)```", re.S)
    return [(m.group(1).strip(), m.group(2).rstrip("\n")) for m in pat.finditer(text)]


def commands(md: Path):
    for blk in blocks(md):
        for line in blk.splitlines():
            line = line.split("#")[0].strip()
            if line:
                yield line


def skip_reason(cmd: str):
    for pat, why in SKIP:
        if re.search(pat, cmd):
            return why
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true", help="show what would run, and what would be skipped")
    ap.add_argument("--workdir", help="run commands here (default: a temp dir, like a fresh reader)")
    args = ap.parse_args()

    wd = Path(args.workdir) if args.workdir else Path(tempfile.mkdtemp(prefix="hardmap-docs-"))
    wd.mkdir(parents=True, exist_ok=True)
    ran = skipped = failed = 0

    for name in DOCS:
        md = ROOT / name
        if not md.exists():
            print(f"MISSING DOC: {name}")
            return 1
        cmds = list(commands(md))
        if not cmds:
            continue
        print(f"\n=== {name} — {len(cmds)} command(s) ===")
        for cmd in cmds:
            why = skip_reason(cmd)
            if why:
                skipped += 1
                print(f"  SKIP  {cmd}\n        └─ {why}")
                continue
            if args.list:
                ran += 1
                print(f"  RUN   {cmd}")
                continue
            r = subprocess.run(cmd, shell=True, cwd=wd, capture_output=True, text=True)
            ran += 1
            if r.returncode != 0:
                failed += 1
                print(f"  FAIL  {cmd}\n        exit {r.returncode}\n"
                      f"        {(r.stderr or r.stdout).strip()[:400]}")
            else:
                print(f"  ok    {cmd}")

        if not args.list:
            for cmd_blk, expected in shown_output(md):
                last = [l.split("#")[0].strip() for l in cmd_blk.splitlines() if l.split("#")[0].strip()]
                if not last or skip_reason(last[-1]):
                    continue
                r = subprocess.run(last[-1], shell=True, cwd=wd, capture_output=True, text=True)
                got = r.stdout.rstrip("\n")
                # compare the SUBSTANCE: the doc may show a trimmed view of a longer print
                exp_lines = [l.rstrip() for l in expected.splitlines() if l.strip()]
                got_lines = [l.rstrip() for l in got.splitlines() if l.strip()]
                missing = [l for l in exp_lines if l not in got_lines]
                if missing:
                    failed += 1
                    print(f"  DRIFT {last[-1]}\n        the doc shows {len(missing)} line(s) the command "
                          f"does not print:")
                    for l in missing[:6]:
                        print(f"          {l}")
                    print(f"        regenerate the shown output from a real run — it is not hand-written")
                else:
                    print(f"  ok    [output matches] {last[-1]}")

    verb = "would run" if args.list else "ran"
    print(f"\n{ran} {verb}, {skipped} skipped (each with a declared reason), {failed} failed")
    print(f"workdir: {wd}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
