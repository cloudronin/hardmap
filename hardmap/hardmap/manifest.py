"""Load and validate repro/manifest.yaml.

The manifest is the single source of truth mapping each paper-cited number to the
adapter that regenerates it, the expected value(s), tolerances, and tier.
"""
from __future__ import annotations

from pathlib import Path

import yaml

_REQUIRED = ("id", "description", "tier", "expected", "fast")


def find_repo_root(start: Path | None = None) -> Path:
    """Find the dir holding repro/manifest.yaml.

    Searches upward from ``start`` (or this package's location) and, as a fallback,
    from the current working directory -- so `hardmap repro` works both from an
    editable install and when run from within a cloned/wheel-installed checkout.
    """
    seeds = [(start or Path(__file__)).resolve(), Path.cwd().resolve()]
    for seed in seeds:
        for parent in (seed, *seed.parents):
            if (parent / "repro" / "manifest.yaml").is_file():
                return parent
    raise FileNotFoundError("repro/manifest.yaml not found from " + " or ".join(map(str, seeds)))


def manifest_path() -> Path:
    return find_repo_root() / "repro" / "manifest.yaml"


def load_manifest(path: Path | None = None) -> list[dict]:
    path = path or manifest_path()
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    claims = data.get("claims", []) if isinstance(data, dict) else data
    ids = set()
    for c in claims:
        missing = [k for k in _REQUIRED if k not in c]
        if missing:
            raise ValueError(f"claim {c.get('id', '?')} missing keys: {missing}")
        if c["id"] in ids:
            raise ValueError(f"duplicate claim id: {c['id']}")
        ids.add(c["id"])
        c.setdefault("tolerance", "exact")
        c.setdefault("full", None)
        c.setdefault("artifact", None)
    return claims
