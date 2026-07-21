"""The core (atlas + charges) must import with no scientific stack — the citation gates run anywhere.

Mirrors desert-map/raitune's light-core-import tests. The structure harness (numpy/scipy) is quarantined
behind the [analysis] extra and is NOT imported by the core.
"""
import os
import pathlib
import subprocess
import sys

PRODUCT_DIR = pathlib.Path(__file__).resolve().parents[1]


def test_core_imports_without_numpy_scipy():
    code = (
        "import sys\n"
        "for m in ['numpy', 'scipy', 'pandas', 'sklearn', 'prince']:\n"
        "    sys.modules[m] = None\n"          # force ImportError on `import <m>`
        "import eightfold.atlas, eightfold.charges\n"
        "assert eightfold.atlas.load_atlas\n"
        "print('core-ok')\n"
    )
    env = {**os.environ, "PYTHONPATH": str(PRODUCT_DIR)}
    r = subprocess.run([sys.executable, "-c", code], cwd=str(PRODUCT_DIR),
                       capture_output=True, text=True, env=env)
    assert r.returncode == 0, r.stderr
    assert "core-ok" in r.stdout


def test_cli_module_is_light():
    # eightfold.cli must import without the scientific stack (it imports structure lazily).
    code = (
        "import sys\n"
        "for m in ['numpy', 'scipy']:\n"
        "    sys.modules[m] = None\n"
        "import eightfold.cli\n"
        "print('cli-ok')\n"
    )
    env = {**os.environ, "PYTHONPATH": str(PRODUCT_DIR)}
    r = subprocess.run([sys.executable, "-c", code], cwd=str(PRODUCT_DIR),
                       capture_output=True, text=True, env=env)
    assert r.returncode == 0, r.stderr
    assert "cli-ok" in r.stdout
