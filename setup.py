"""Dynamic package discovery for the bundled hardmap distribution.

Project metadata lives in pyproject.toml; only the multi-root package layout is
computed here. Each of the five import packages lives under a differently-named
product directory, so we scan each product dir and keep just its import package
(and subpackages) -- excluding tests/docs/dev and avoiding cross-root name
collisions (every product has its own `tests`/`docs`). This bundles all five
into one installable so the internal edges (foundry->eightfold,
proof-census->desertmap) resolve by construction.
"""
import shutil
from pathlib import Path

from setuptools import find_packages, setup

HERE = Path(__file__).resolve().parent

# Bundle the canonical repo-root manifest into the hardmap package so the built
# wheel is self-contained (`pip install hardmap` can reproduce without a checkout).
# Single source of truth: repro/manifest.yaml; this is a build-time copy.
_root_manifest = HERE / "repro" / "manifest.yaml"
if _root_manifest.is_file():
    _bundled = HERE / "hardmap" / "hardmap" / "_bundled"
    _bundled.mkdir(parents=True, exist_ok=True)
    shutil.copy2(_root_manifest, _bundled / "manifest.yaml")

# import-name -> product directory
ROOTS = {
    "hardmap": "hardmap",
    "eightfold": "eightfold",
    "foundry": "foundry",
    "desertmap": "desert-map",
    "proofcensus": "proof-census",
}

packages: list[str] = []
package_dir: dict[str, str] = {}
for imp, prod in ROOTS.items():
    package_dir[imp] = f"{prod}/{imp}"
    for pkg in find_packages(
        where=prod, exclude=("tests", "tests.*", "docs", "docs.*", "dev", "dev.*")
    ):
        if pkg == imp or pkg.startswith(imp + "."):
            packages.append(pkg)

# Ship the committed result artifacts (atlas, matrices, checkpoint, preregs, summaries)
# inside the distribution so `pip install hardmap` can reproduce, not just import.
_RESULT_GLOBS = [
    "results/*.json", "results/*.jsonl", "results/*.csv", "results/*.md",
    "results/**/*.json", "results/**/*.jsonl", "results/**/*.csv", "results/**/*.md",
]
package_data = {imp: list(_RESULT_GLOBS) for imp in ("eightfold", "foundry", "desertmap", "proofcensus")}
package_data["hardmap"] = ["_bundled/*.yaml"]

setup(
    packages=sorted(packages),
    package_dir=package_dir,
    package_data=package_data,
    include_package_data=True,
)
