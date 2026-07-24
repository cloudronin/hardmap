"""Dynamic package discovery for the bundled hardmap distribution.

Project metadata lives in pyproject.toml; only the multi-root package layout is
computed here. Each of the five import packages lives under a differently-named
product directory, so we scan each product dir and keep just its import package
(and subpackages) -- excluding tests/docs/dev and avoiding cross-root name
collisions (every product has its own `tests`/`docs`). This bundles all five
into one installable so the internal edges (foundry->eightfold,
proof-census->desertmap) resolve by construction.
"""
from setuptools import find_packages, setup

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

setup(packages=sorted(packages), package_dir=package_dir)
