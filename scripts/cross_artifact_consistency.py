#!/usr/bin/env python3
"""H4 check 5 -- cross-artifact consistency.

Mechanical diff: every headline number the preprint will cite should appear in the
prose (findings / four-wall note / README) that discusses it, matching the value in
results/. Reports where each headline number is cited; exits nonzero if any headline
number is cited nowhere in prose (a drift signal). Run: python scripts/cross_artifact_consistency.py
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Distinctive headline numbers -> the string forms they may appear as in prose.
HEADLINE = {
    "gradient V (0.73)": ["0.729", "0.73"],
    "gradient dedup V (0.68)": ["0.681", "0.680", "0.68"],
    "lattice v3 V (0.256)": ["0.256"],
    "prism v1 Min-Ones (0.459)": ["0.459"],
    "prism v2 arity-4 (0.516)": ["0.516"],
    "v1 anchor Spearman (-0.564)": ["-0.564"],
    "arity-4 Spearman (-0.140)": ["-0.140", "-0.14"],
    "backbone n=60 (~273)": ["273", "272.6"],
}

# Prose sources (not results/): findings, specs, four-wall note, README.
docs = sorted(
    set(ROOT.rglob("docs/findings/*.md"))
    | set(ROOT.rglob("docs/specs/*.md"))
    | {ROOT / "README.md"}
)
# Normalize the unicode minus (U+2212) prose uses to ASCII so negative numbers match.
corpus = {p: p.read_text(encoding="utf-8", errors="ignore").replace("−", "-") for p in docs if p.is_file()}


def main() -> int:
    missing = 0
    for label, forms in HEADLINE.items():
        hits = sorted(
            p.relative_to(ROOT).as_posix()
            for p, text in corpus.items()
            if any(f in text for f in forms)
        )
        if hits:
            print(f"[cited] {label:<28} in {len(hits)} doc(s): {', '.join(hits[:3])}"
                  + (" ..." if len(hits) > 3 else ""))
        else:
            missing += 1
            print(f"[MISSING] {label:<28} not cited in any prose ({forms})")
    print(f"\n{len(HEADLINE) - missing}/{len(HEADLINE)} headline numbers cited in prose")
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
